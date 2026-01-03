const axios = require('axios');
const AccountPool = require('./account_pool');

class AuthManager {
  constructor(apiBase, options = {}) {
    this.apiBase = apiBase;
    this.pool = new AccountPool(options);
    
    // Store tokens per account email
    // Map<email, {token, expiration}>
    this.tokens = new Map();
  }

  /**
   * Authenticate a specific account
   */
  async authenticate(email, password) {
    try {
      const response = await axios.post(
        `${this.apiBase}/api/v1/auths/signin`,
        { email, password },
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          proxy: false
        }
      );

      const token = response.data.token || response.data.access_token || response.data.data?.token;
      
      let expiration;
      if (response.data.expires_in) {
        expiration = new Date(Date.now() + (response.data.expires_in * 1000));
      } else {
        expiration = new Date(Date.now() + (59 * 60 * 1000));
      }
      
      this.tokens.set(email, { token, expiration });
      return { token, expiration };
    } catch (error) {
      console.error(`Authentication failed for ${email}:`, error.response?.data || error.message);
      this.pool.reportError(email, 'auth_failure');
      throw new Error(error.response?.data?.detail || error.message || 'Authentication failed');
    }
  }

  /**
   * Get a valid token from the pool (rotates if needed)
   */
  async getValidToken() {
    const account = this.pool.getNextAccount();
    if (!account) {
      throw new Error('No available accounts in the pool or all are in cooldown');
    }

    const cached = this.tokens.get(account.email);
    if (cached && cached.token && cached.expiration > new Date()) {
      return { token: cached.token, email: account.email };
    }

    // Need new token
    console.log(`Refreshing token for account: ${account.email}`);
    const { token } = await this.authenticate(account.email, account.password);
    return { token, email: account.email };
  }

  /**
   * Make authenticated request with pool support and automatic retry/switch on failure
   */
  async makeAuthenticatedRequest(url, method = 'GET', data = null, headers = {}) {
    let { token, email } = await this.getValidToken();
    
    const executeRequest = async (currentEmail, currentToken) => {
      const config = {
        method,
        url,
        headers: {
          'Authorization': `Bearer ${currentToken}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...headers
        },
        proxy: false
      };

      if (['POST', 'PUT', 'PATCH'].includes(method.toUpperCase()) && data) {
        config.data = data;
      }

      try {
        const response = await axios(config);
        return response;
      } catch (error) {
        // Handle auth errors
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          console.log(`Token expired or invalid for ${currentEmail}, switching account...`);
          this.tokens.delete(currentEmail);
          
          // Retry with a NEW token (possibly from a different account)
          const next = await this.getValidToken();
          return await executeRequest(next.email, next.token);
        }
        
        // Handle rate limits
        if (error.response && error.response.status === 429) {
          console.warn(`Rate limit hit for ${currentEmail}, marking as cooldown and switching...`);
          this.pool.reportError(currentEmail, 'rate_limit');
          
          const next = await this.getValidToken();
          return await executeRequest(next.email, next.token);
        }

        throw error;
      }
    };

    return await executeRequest(email, token);
  }
}

module.exports = AuthManager;