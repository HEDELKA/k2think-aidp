const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const AuthManager = require('./auth/auth_manager');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE = process.env.K2THINK_API_BASE || 'https://www.k2think.ai';

// Initialize auth manager with account rotation support
// It will automatically look for accounts.json or use credentials from .env
const authManager = new AuthManager(API_BASE);

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Chat completion endpoint - mirrors OpenAI's API
app.post('/v1/chat/completions', async (req, res) => {
  try {
    const { model, messages, temperature = 1, max_tokens, stream = false } = req.body;
    
    const k2thinkPayload = {
      stream: stream,
      model: model || 'MBZUAI-IFM/K2-Think',
      messages: messages,
      ...(temperature !== undefined && { temperature: temperature }),
      ...(max_tokens && { max_tokens: max_tokens })
    };

    // Make authenticated request using auth manager (it handles rotation internally)
    const response = await authManager.makeAuthenticatedRequest(
      `${API_BASE}/api/chat/completions`,
      'POST',
      k2thinkPayload,
      {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    );

    res.status(200).json(response.data);
  } catch (error) {
    const status = error.response?.status || 500;
    const detail = error.response?.data?.detail || error.message;
    
    console.error(`Chat completion error (${status}):`, detail);
    
    res.status(status).json({
      error: {
        message: detail || 'Chat completion failed',
        type: 'api_error',
        param: null,
        code: status === 429 ? 'rate_limit_exceeded' : 'internal_error'
      }
    });
  }
});

// List models endpoint
app.get('/v1/models', async (req, res) => {
  try {
    const response = await authManager.makeAuthenticatedRequest(
      `${API_BASE}/api/v1/models`,
      'GET',
      null,
      { 'Accept': 'application/json' }
    );
    
    const models = Array.isArray(response.data) ? response.data : (response.data.data || []);
    
    res.status(200).json({
      object: 'list',
      data: models.map(model => ({
        id: model.id || model.name,
        object: 'model',
        created: Math.floor(Date.now() / 1000),
        owned_by: model.owned_by || 'k2think'
      }))
    });
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: {
        message: error.response?.data?.detail || error.message || 'Failed to list models'
      }
    });
  }
});

// Health check
app.get('/', (req, res) => {
  res.json({
    status: 'OK',
    service: 'K2Think AI API Proxy with Account Rotation',
    version: '1.1.0',
    timestamp: new Date().toISOString(),
    accounts_available: authManager.pool.accounts.length
  });
});

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: { message: 'Internal server error' } });
});

app.listen(PORT, () => {
  console.log(`K2Think AI API Proxy (v1.1.0) is running on port ${PORT}`);
  console.log(`Account rotation pool size: ${authManager.pool.accounts.length}`);
});