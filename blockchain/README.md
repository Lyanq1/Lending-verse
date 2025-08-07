# LendingVerse Blockchain Contracts

This directory contains the smart contracts for the LendingVerse P2P lending platform.

## Contracts

### LoanAgreement.sol

The LoanAgreement contract manages loan agreements between lenders and borrowers. It handles:
- Loan creation
- Loan funding
- Payment processing
- Loan completion
- Default handling

### LendingMarket.sol

The LendingMarket contract manages the marketplace for loan offers and requests. It handles:
- Loan offer creation and management
- Loan request creation and management
- Matching loan offers with requests
- Creating loan agreements

### DocumentVerification.sol

The DocumentVerification contract handles document verification on the blockchain. It:
- Stores document hashes
- Tracks document ownership
- Manages document verification status
- Provides a verification system for trusted verifiers

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example` and fill in your configuration.

3. Compile contracts:
```bash
npm run compile
```

4. Run tests:
```bash
npm test
```

## Deployment

### Local Development
```bash
npm run deploy:development
```

### Sepolia Testnet
```bash
npm run deploy:sepolia
```

### Goerli Testnet
```bash
npm run deploy:goerli
```

### Mainnet
```bash
npm run deploy:mainnet
```

## Contract Verification

After deployment, you can verify your contracts on Etherscan:

```bash
npm run verify:sepolia
npm run verify:goerli
npm run verify:mainnet
```

## Integration with Backend

The backend interacts with these contracts through a blockchain service that:
1. Creates loan agreements when matches are confirmed
2. Monitors loan status and payments
3. Verifies documents using the DocumentVerification contract
4. Handles blockchain events for real-time updates

## Gas Optimization

These contracts have been optimized for gas efficiency:
- Using appropriate data structures
- Minimizing storage operations
- Batching operations where possible
- Using events for off-chain tracking

## Security Considerations

The contracts implement several security measures:
- Access control for sensitive operations
- Input validation
- Reentrancy protection
- Error handling

## Future Improvements

Planned improvements include:
- Multi-signature functionality for loan approval
- Integration with DeFi protocols for yield generation
- Support for multiple tokens/currencies
- Improved collateral management