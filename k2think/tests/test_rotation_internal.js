const AccountPool = require('../src/auth/account_pool');
const assert = require('assert');

async function testRotation() {
  console.log('=== Testing Account Rotation & Cooldown ===\n');

  const mockAccounts = [
    { email: 'acc1@test.com', password: 'pass', note: 'Account 1' },
    { email: 'acc2@test.com', password: 'pass', note: 'Account 2' }
  ];

  const pool = new AccountPool({ accounts: mockAccounts });

  // Test 1: Round-robin rotation
  console.log('1. Testing round-robin...');
  const a1 = pool.getNextAccount();
  const a2 = pool.getNextAccount();
  const a3 = pool.getNextAccount();

  console.log('   - First:', a1.email);
  console.log('   - Second:', a2.email);
  console.log('   - Third (should be first again):', a3.email);

  assert.strictEqual(a1.email, 'acc1@test.com');
  assert.strictEqual(a2.email, 'acc2@test.com');
  assert.strictEqual(a3.email, 'acc1@test.com');
  console.log('✓ Round-robin works\n');

  // Test 2: Cooldown
  console.log('2. Testing cooldown...');
  pool.reportError('acc1@test.com', 'rate_limit');
  
  const a4 = pool.getNextAccount();
  const a5 = pool.getNextAccount();
  
  console.log('   - Next after acc1 limit:', a4.email);
  console.log('   - Next again (should skip acc1):', a5.email);

  assert.strictEqual(a4.email, 'acc2@test.com');
  assert.strictEqual(a5.email, 'acc2@test.com'); 
  console.log('✓ Cooldown/Skip works\n');

  // Test 3: Recovery from cooldown (simulated)
  console.log('3. Testing recovery...');
  const acc1 = pool.accounts.find(a => a.email === 'acc1@test.com');
  acc1.cooldownUntil = Date.now() - 1000; // Force recovery
  
  const a6 = pool.getNextAccount();
  console.log('   - Next after acc1 recovery:', a6.email);
  assert.strictEqual(a6.email, 'acc1@test.com');
  console.log('✓ Recovery works\n');

  console.log('=== ✅ Rotation tests passed! ===');
}

testRotation().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
