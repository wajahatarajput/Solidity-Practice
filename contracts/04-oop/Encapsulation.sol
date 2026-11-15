// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Encapsulation
 * @notice Hide internal state; expose controlled getters/setters (OOP encapsulation).
 * @dev Private/internal state prevents arbitrary writes; modifiers enforce rules.
 */
contract BankAccount {
    address private owner;
    uint256 private balance;

    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        require(msg.value > 0, "zero");
        balance += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external onlyOwner {
        require(amount <= balance, "insufficient");
        balance -= amount;
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "transfer failed");
        emit Withdrawn(msg.sender, amount);
    }

    function getBalance() external view returns (uint256) {
        return balance;
    }

    function getOwner() external view returns (address) {
        return owner;
    }
}
