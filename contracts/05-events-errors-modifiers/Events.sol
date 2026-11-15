// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Events
 * @notice Events are append-only logs clients and indexers can filter cheaply.
 * @dev Up to 3 `indexed` parameters become searchable topics.
 */
contract Events {
    event Transfer(address indexed from, address indexed to, uint256 amount);
    event Message(address indexed sender, string text);

    mapping(address => uint256) public balances;

    constructor() {
        balances[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        balances[to] += amount;
        emit Transfer(msg.sender, to, amount);
    }

    function logMessage(string calldata text) external {
        emit Message(msg.sender, text);
    }
}
