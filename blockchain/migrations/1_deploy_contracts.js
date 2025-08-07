const LoanAgreement = artifacts.require("LoanAgreement");
const LendingMarket = artifacts.require("LendingMarket");
const DocumentVerification = artifacts.require("DocumentVerification");

module.exports = async function(deployer, network, accounts) {
  // Platform fee: 1% (100 basis points)
  const platformFeePercent = 100;
  
  // Deploy LoanAgreement
  await deployer.deploy(LoanAgreement, platformFeePercent);
  const loanAgreement = await LoanAgreement.deployed();
  
  // Deploy LendingMarket
  await deployer.deploy(LendingMarket, loanAgreement.address, platformFeePercent);
  
  // Deploy DocumentVerification
  await deployer.deploy(DocumentVerification);
  
  console.log("Contracts deployed:");
  console.log("LoanAgreement:", loanAgreement.address);
  console.log("LendingMarket:", (await LendingMarket.deployed()).address);
  console.log("DocumentVerification:", (await DocumentVerification.deployed()).address);
};