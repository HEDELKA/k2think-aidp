const AuthManager = require('./auth/auth_manager');

/**
 * K2Think AI Client - Use K2Think like OpenAI SDK
 * Consolidated with AuthManager to support account rotation.
 */
class K2ThinkClient {
  constructor(options = {}) {
    this.apiBase = options.apiBase || process.env.K2THINK_API_BASE || 'https://www.k2think.ai';
    
    // Auth manager handles credentials/pool/rotation
    this.authManager = new AuthManager(this.apiBase, options);
    
    // OpenAI-style API structure
    this.chat = {
      completions: {
        create: this._createChatCompletion.bind(this)
      }
    };
    
    this.models = {
      list: this._listModels.bind(this)
    };
  }
  
  /**
   * Make authenticated request (delegated to authManager)
   */
  async _makeRequest(url, method, data = null) {
    const response = await this.authManager.makeAuthenticatedRequest(url, method, data);
    return response.data;
  }
  
  /**
   * Create chat completion (OpenAI compatible)
   */
  async _createChatCompletion(options) {
    const { 
      model = 'MBZUAI-IFM/K2-Think', 
      messages, 
      temperature, 
      max_tokens, 
      stream = false 
    } = options;
    
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      throw new Error('messages array is required');
    }
    
    const payload = {
      stream,
      model,
      messages,
      ...(temperature !== undefined && { temperature }),
      ...(max_tokens && { max_tokens })
    };
    
    return await this._makeRequest(
      `${this.apiBase}/api/chat/completions`,
      'POST',
      payload
    );
  }
  
  /**
   * List available models (OpenAI compatible)
   */
  async _listModels() {
    const response = await this._makeRequest(
      `${this.apiBase}/api/v1/models`,
      'GET'
    );
    
    const models = Array.isArray(response) ? response : (response.data || []);
    
    return {
      object: 'list',
      data: models.map(model => ({
        id: model.id || model.name,
        object: 'model',
        created: Math.floor(Date.now() / 1000),
        owned_by: model.owned_by || 'k2think'
      }))
    };
  }
}

module.exports = K2ThinkClient;
