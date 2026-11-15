// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title SimpleStorage
 * @notice Store and retrieve a single unsigned integer.
 * @dev Shows state variables, public getters, and a setter that mutates storage.
 */
contract SimpleStorage {
    uint256 private storedNumber;

    event NumberUpdated(uint256 oldValue, uint256 newValue);

    /// @notice Write a new value into storage.
    function set(uint256 _number) public {
        uint256 old = storedNumber;
        storedNumber = _number;
        emit NumberUpdated(old, _number);
    }

    /// @notice Read the stored value.
    function get() public view returns (uint256) {
        return storedNumber;
    }
}
