# Linear-vesting
Linear vesting contract created with Solidity for the Ethereum blockchain. The contract allows an owner of ERC20 tokens to lock them into the contract for a specified period of time, after which the tokens are progressively released to a beneficiary over a defined duration.

The contract starts with a "cliff" period, during which no allocations are released.

After the cliff period, tokens are released linearly over the vesting period.
