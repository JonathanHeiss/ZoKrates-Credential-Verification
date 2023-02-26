const fs = require("fs");

const Verifier = artifacts.require("Verifier");
const MinAgeVerifier = artifacts.require("MinAgeVerifier");

module.exports = function (deployer) {
  let verifier, dateTime, minAgeVerifier;

  deployer.deploy(Verifier)
    .then((_verifier) => {
      verifier = _verifier;
      return deployer.deploy(MinAgeVerifier, verifier.address);
    })
    .then((_minAgeVerifier) => {
      minAgeVerifier = _minAgeVerifier;
    })
    .then(async() => {
      let proof = JSON.parse(await fs.readFileSync("../artifacts/proof.json", "utf8"));

      return minAgeVerifier.verifyTx.sendTransaction(proof.proof, proof.inputs);
    })
    .then((_verifyTx) => {
      console.log("Gas used: " + _verifyTx.receipt.gasUsed);
    })
};
