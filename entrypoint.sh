#!/bin/bash
set -e

echo "============================================"
echo "K2Think AI Agent - GPU Compute Wrapper"
echo "Powered by AIDP Decentralized Network"
echo "============================================"
echo ""

echo "=== GPU Status Check ==="
if command -v nvidia-smi &> /dev/null; then
    echo "✓ NVIDIA GPU Tools Available"
    echo ""
    echo "=== GPU Information ==="
    nvidia-smi --query-gpu=index,name,driver_version,memory.total --format=csv,noheader
    echo ""
    echo "=== Current GPU Usage ==="
    nvidia-smi --query-gpu=index,utilization.gpu,utilization.memory,memory.used,memory.free --format=csv,noheader
    echo ""
else
    echo "⚠ Warning: NVIDIA GPU tools not found"
    echo ""
fi

echo "=== Environment Configuration ==="
echo "✓ Node.js version: $(node --version)"
echo "✓ npm version: $(npm --version)"
echo ""

echo "=== Starting K2Think AI Agent ==="
echo "Port: ${PORT:-3000}"
echo ""

(
    while true; do
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] === GPU Status ===" >> gpu-monitor.log
        if command -v nvidia-smi &> /dev/null; then
            nvidia-smi >> gpu-monitor.log 2>&1
        fi
        sleep 30
    done
) &
GPU_MONITOR_PID=$!

trap "kill $GPU_MONITOR_PID 2>/dev/null || true" EXIT

echo "$(date +'%Y-%m-%d %H:%M:%S') - Starting K2Think API Server..."
exec node src/server.js
