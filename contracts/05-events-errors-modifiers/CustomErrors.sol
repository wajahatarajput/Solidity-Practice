// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title CustomErrors
 * @notice Custom errors cost less gas than require(string) reverts.
 * @dev Declare with `error Name(args...)` and use `revert Name(args)`.
 */
contract CustomErrors {
    error Unauthorized(address caller);
    error InsufficientBalance(uint256 available, uint256 required);
    error ZeroAddress();

    address public owner;
    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender;
        balances[msg.sender] = 100;
    }

    function withdraw(uint256 amount) external {
        if (msg.sender != owner) {
            revert Unauthorized(msg.sender);
        }
        uint256 available = balances[msg.sender];
        if (amount > available) {
            revert InsufficientBalance(available, amount);
        }
        balances[msg.sender] = available - amount;
    }

    function setOwner(address newOwner) external {
        if (msg.sender != owner) {
            revert Unauthorized(msg.sender);
        }
        if (newOwner == address(0)) {
            revert ZeroAddress();
        }
        owner = newOwner;
    }
}
