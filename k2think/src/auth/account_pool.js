const fs = require("fs");
const path = require("path");

/**
 * AccountPool manages a collection of K2Think account credentials
 * and provides a rotation strategy (round-robin).
 */
class AccountPool {
  constructor(options = {}) {
    this.accounts = [];
    this.currentIndex = 0;
    this.accountsPath =
      options.accountsPath || path.join(process.cwd(), "accounts.json");

    this._loadAccounts(options.accounts);
  }

  /**
   * Load accounts from provided array or accounts.json
   */
  _loadAccounts(providedAccounts) {
    if (providedAccounts && Array.isArray(providedAccounts)) {
      this.accounts = providedAccounts.map((acc) => ({
        ...acc,
        status: "active",
        lastUsed: 0,
        errorCount: 0,
        cooldownUntil: null,
      }));
    } else if (fs.existsSync(this.accountsPath)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.accountsPath, "utf8"));
        this.accounts = (Array.isArray(data) ? data : data.accounts || []).map(
          (acc) => ({
            ...acc,
            status: "active",
            lastUsed: 0,
            errorCount: 0,
            cooldownUntil: null,
          })
        );
      } catch (error) {
        console.error(
          `Failed to load accounts from ${this.accountsPath}:`,
          error.message
        );
      }
    }

    // Add individual credentials from env if pool is empty
    if (
      this.accounts.length === 0 &&
      process.env.K2THINK_EMAIL &&
      process.env.K2THINK_PASSWORD
    ) {
      this.accounts.push({
        email: process.env.K2THINK_EMAIL,
        password: process.env.K2THINK_PASSWORD,
        status: "active",
        lastUsed: 0,
        errorCount: 0,
        cooldownUntil: null,
      });
    }

    if (this.accounts.length === 0) {
      console.warn("Warning: AccountPool initialized with 0 accounts.");
    } else {
      console.log(
        `AccountPool initialized with ${this.accounts.length} accounts.`
      );
    }
  }

  /**
   * Get the next available account from the pool
   */
  getNextAccount() {
    if (this.accounts.length === 0) return null;

    const originalIndex = this.currentIndex;
    const now = Date.now();

    for (let i = 0; i < this.accounts.length; i++) {
      const idx = (originalIndex + i) % this.accounts.length;
      const account = this.accounts[idx];

      if (
        account.status === "active" ||
        (account.cooldownUntil && account.cooldownUntil <= now)
      ) {
        if (account.cooldownUntil <= now) {
          account.status = "active";
          account.cooldownUntil = null;
          account.errorCount = 0;
        }

        this.currentIndex = (idx + 1) % this.accounts.length;
        account.lastUsed = now;
        return account;
      }
    }

    // If no active accounts, return the least cooled-down one or null
    return null;
  }

  /**
   * Mark an account as rate-limited/errored
   */
  reportError(email, type = "rate_limit") {
    const account = this.accounts.find((a) => a.email === email);
    if (!account) return;

    account.errorCount++;
    console.error(
      `Account ${email} reported error: ${type}. Error count: ${account.errorCount}`
    );

    if (type === "rate_limit" || account.errorCount >= 3) {
      account.status = "cooldown";
      // Standard cooldown 15 minutes for rate limit, 1 hour for errors
      const cooldownMs =
        type === "rate_limit" ? 15 * 60 * 1000 : 60 * 60 * 1000;
      account.cooldownUntil = Date.now() + cooldownMs;
      console.warn(
        `Account ${email} put in cooldown until ${new Date(
          account.cooldownUntil
        ).toISOString()}`
      );
    }
  }

  /**
   * Check if any account is available
   */
  hasAvailableAccounts() {
    const now = Date.now();
    return this.accounts.some(
      (a) =>
        a.status === "active" || (a.cooldownUntil && a.cooldownUntil <= now)
    );
  }
}

module.exports = AccountPool;
