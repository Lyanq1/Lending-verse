/**
 * Truffle configuration file for LendingVerse P2P lending platform
 */

require('dotenv').config();
const HDWalletProvider = require('@truffle/hdwallet-provider');

// Read environment variables
const MNEMONIC = process.env.MNEMONIC || '';
const INFURA_API_KEY = process.env.INFURA_API_KEY || '';
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || '';

module.exports = {
  /**
   * Networks define how you connect to your ethereum client
   */
  networks: {
    // Development network (local)
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*", // Match any network id
      gas: 6721975,
    },
    
    // Sepolia testnet
    sepolia: {
      provider: () => new HDWalletProvider(
        MNEMONIC,
        `https://sepolia.infura.io/v3/${INFURA_API_KEY}`
      ),
      network_id: 11155111,
      gas: 5500000,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    },
    
    // Goerli testnet
    goerli: {
      provider: () => new HDWalletProvider(
        MNEMONIC,
        `https://goerli.infura.io/v3/${INFURA_API_KEY}`
      ),
      network_id: 5,
      gas: 5500000,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    },
    
    // Mainnet
    mainnet: {
      provider: () => new HDWalletProvider(
        MNEMONIC,
        `https://mainnet.infura.io/v3/${INFURA_API_KEY}`
      ),
      network_id: 1,
      gas: 5500000,
      gasPrice: 50000000000, // 50 gwei
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: false
    },
  },

  // Configure mocha for testing
  mocha: {
    timeout: 100000
  },

  // Configure compilers
  compilers: {
    solc: {
      version: "0.8.17",
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        },
      }
    }
  },

  // Configure plugins
  plugins: [
    'truffle-plugin-verify'
  ],

  // Configure verification API keys
  api_keys: {
    etherscan: ETHERSCAN_API_KEY
  }
};