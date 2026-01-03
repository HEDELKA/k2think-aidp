FROM nvidia/cuda:12.2-runtime-ubuntu22.04 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY k2think/package*.json ./
RUN npm ci --only=production

FROM nvidia/cuda:12.2-runtime-ubuntu22.04

LABEL maintainer="AIDP Builder"
LABEL description="Custom AI Agent Wrapper optimized for Decentralized Compute"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/node_modules ./node_modules
COPY k2think/src ./src
COPY k2think/.env.example .env
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || exit 1

ENTRYPOINT ["./entrypoint.sh"]
