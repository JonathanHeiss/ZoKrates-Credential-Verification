// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

import "./MinAgeVerifier.sol";
import "./DateTime.sol";

contract Voting {
	mapping(uint256 => uint256) public votes;
	MinAgeVerifier minAgeVerifier;

	DateTime internal dt = new DateTime();

	constructor(MinAgeVerifier _minAgeVerifier) {
		minAgeVerifier = _minAgeVerifier;
	}

	function vote(uint256 _vote, MinAgeVerifier.Proof memory _proof, uint[2] memory _input) public returns (bool _isValid, bool _isAdult, bool _success, uint256 yrs18Ago) {
		 yrs18Ago = (dt.getYear(block.timestamp) - 18) * 10000 + dt.getMonth(block.timestamp) * 100 + dt.getDay(block.timestamp);

		_isValid = minAgeVerifier.verifyTx(_proof, _input);

		_isAdult = _input[0] < yrs18Ago;

		if(_isValid && _isAdult) {
			votes[_vote]++;
			_success = true;
		}
	}
}

