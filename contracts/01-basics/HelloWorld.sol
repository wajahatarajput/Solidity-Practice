// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title HelloWorld
 * @notice Your first Solidity contract: store and read a greeting.
 * @dev Demonstrates a state variable, constructor, and a view getter.
 */
contract HelloWorld {
    string public greeting;

    constructor(string memory _greeting) {
        greeting = _greeting;
    }

    /// @notice Update the greeting string.
    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    /// @notice Read the greeting (same as the auto-generated public getter).
    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
