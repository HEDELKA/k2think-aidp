# Project Context: k2think-api-nodejs

## Overview

This project is a Node.js client library and API proxy for the K2Think AI platform. It provides an OpenAI-compatible interface, allowing users to switch from OpenAI to K2Think with minimal code changes.

## Architecture

- **src/client.js**: Main exported library for Node.js apps. Delegated to `AuthManager`.
- **src/server.js**: Express Proxy server mirroring OpenAI API.
- **src/auth/auth_manager.js**: Centralized authentication orchestrator.
- **src/auth/account_pool.js**: Manages account rotation, error tracking, and cooldowns.

## Tech Stack

- **Node.js**: Runtime
- **Express**: Proxy server
- **Axios**: HTTP requests
- **Dotenv**: Configuration

## Account Rotation

The system supports multiple K2Think accounts to bypass platform limits:

1. It loads accounts from `accounts.json` (root) or fallbacks to `.env`.
2. Uses a round-robin strategy for rotation.
3. Automatically switches accounts on `429 (Too Many Requests)` or `401/403` errors.
4. Puts rate-limited accounts into "cooldown" for 15 minutes.
