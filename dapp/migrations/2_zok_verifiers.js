const Migrations = artifacts.require("Migrations");
const MinAgeVerifier = artifacts.require("MinAgeVerifier");

module.exports = async (deployer) => {
  return deployer.deploy(MinAgeVerifier);
};
