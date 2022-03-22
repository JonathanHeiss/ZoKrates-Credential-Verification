// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

import "./MinAgeVerifier.sol";

contract Voting {
	mapping(uint256 => uint256) public votes;
	MinAgeVerifier minAgeVerifier;

	constructor(MinAgeVerifier _minAgeVerifier) public {
		minAgeVerifier = _minAgeVerifier;
	}

	function vote(uint256 _vote, MinAgeVerifier.Proof memory _proof, uint[2] memory _input) public returns (bool _isValid, bool _isAdult, bool _success, uint256 diff) {
		uint256 yrs18Ago = block.timestamp - (365 days * 18);

		diff = (_input[0] > yrs18Ago ? _input[0] - yrs18Ago : yrs18Ago - _input[0]);

		_isValid = diff < 5 * 60 * 60 * 24; // make sure the comparison timestamp is actually 18 years ago (+- 5 days for longer Februaries)

		_isAdult = minAgeVerifier.verifyTx(_proof, _input);

		if(_isValid && _isAdult) {
			votes[_vote]++;
			_success = true;
		}
	}
}

