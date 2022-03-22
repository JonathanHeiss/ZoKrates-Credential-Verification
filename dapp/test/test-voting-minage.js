const fs = require("fs");

const Voting = artifacts.require("Voting");
const MinAgeVerifier = artifacts.require("MinAgeVerifier");

const { initialize } = require("zokrates-js/node");

contract("Voting", (accounts) => {
	let voting;
	let zok;

	let proof;

	before(() => {
		return MinAgeVerifier.new()
			.then((_minAgeVerifier) => {
				return Voting.new(_minAgeVerifier.address);
			})
			.then((_voting) => {
				voting = _voting;
			})
	});

	it("generates proof", () => {
		let artifacts;
		let pk;

		return initialize()
			.then(_zok => zok = _zok)
			.then(async () => {
				pk = await fs.readFileSync("../verifier/proving.key");
			})
			.then(async () => {
				return await fs.readFileSync("../verifier/minAge.zok", "utf8");
			})
			.then((_source) => {
				return zok.compile(_source);
			})
			.then((_artifacts) => {
				artifacts = _artifacts;
			})
			.then(async () => {
				let years18ago = new Date();
				years18ago.setFullYear(years18ago.getFullYear() - 18);
				let { witness, output } = await zok.computeWitness(artifacts, ["315555217", Math.floor(years18ago / 1000).toString()]);

				return zok.generateProof(artifacts.program, witness, pk);
			})
			.then(async (_proof) => {
				proof = _proof;

				return voting.vote.call(
					1337,
					_proof.proof,
					_proof.inputs,
				);
			})
			.then((_votingStatus) => {
				assert.ok(_votingStatus._isValid);
				assert.ok(_votingStatus._isAdult);
				assert.ok(_votingStatus._success);
				
				return voting.vote(
					1337,
					proof.proof,
					proof.inputs,
				);
			})
			.then(() => {
				return voting.votes(1337);
			})
			.then(_votes => assert.equal(_votes, 1));
	});
});