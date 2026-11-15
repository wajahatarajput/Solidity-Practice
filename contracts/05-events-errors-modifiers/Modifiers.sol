// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Modifiers
 * @notice Reusable pre/post conditions for functions (access control, validation).
 * @dev The `_` placeholder marks where the function body runs.
 */
contract Modifiers {
    address public owner;
    bool public paused;
    uint256 public value;

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "paused");
        _;
    }

    modifier validAmount(uint256 amount) {
        require(amount > 0 && amount <= 1000, "invalid amount");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
    }

    function setValue(uint256 amount) external onlyOwner whenNotPaused validAmount(amount) {
        value = amount;
    }
}
