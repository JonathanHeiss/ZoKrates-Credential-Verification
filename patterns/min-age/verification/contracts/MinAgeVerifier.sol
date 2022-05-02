pragma solidity ^0.8.0;

import "./Verifier.sol";
import "./DateTime.sol";

contract MinAgeVerifier {
	Verifier verfier;

	DateTime internal dt = new DateTime();

	constructor(Verifier _verfier) {
		verfier = _verfier;
	}

	function verifyTx(Verifier.Proof memory _proof, uint[20] memory _input) public returns (bool) {
 		uint256 yrs18Ago = uint256(dt.getYear(block.timestamp) - 18) * 10000 + uint256(dt.getMonth(block.timestamp)) * 100 + uint256(dt.getDay(block.timestamp));

		bool isValid = verfier.verifyTx(_proof, _input);

		bool isAdult = _input[0] < yrs18Ago;

		return isValid && isAdult;
	}
}