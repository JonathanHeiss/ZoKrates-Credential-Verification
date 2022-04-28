const fs = require("fs");

const Verifier = artifacts.require("Verifier");

contract("Verifier", (accounts) => {
	let verifier;

	let proof;

	before(() => {
		return Verifier.new()
			.then((_verifier) => {
				verifier = _verifier;
			})
	});

	it("loads proof", async () => {
		let txt = await fs.readFileSync("../artifacts/proof.json", "utf8");
		assert.ok(txt.length > 0);

		proof = JSON.parse(txt);
		assert.ok(proof);
	});

	it("verifies proof", () => {
		return verifier.verifyTx(
					proof.proof,
					proof.inputs
			)
			.then((_verified) => {
				assert.ok(_verified);
			});
	});
});