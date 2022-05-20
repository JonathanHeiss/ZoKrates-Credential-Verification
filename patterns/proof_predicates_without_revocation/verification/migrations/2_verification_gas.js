const fs = require("fs");

const Verifier = artifacts.require("Verifier");

module.exports = function (deployer) {
  deployer.deploy(Verifier)
    .then(async (_verifier) => {
      let proof = JSON.parse(await fs.readFileSync("../artifacts/proof.json", "utf8"));
      return _verifier.verifyTx.sendTransaction(proof.proof, proof.inputs);
    })
    .then((_verifyTx) => {
      console.log("Gas used: " + _verifyTx.receipt.gasUsed);
    })
};
