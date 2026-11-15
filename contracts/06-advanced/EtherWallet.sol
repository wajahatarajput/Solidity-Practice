// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title EtherWallet
 * @notice Receive and send ETH; prefer `call` over `transfer`/`send` for gas flexibility.
 * @dev Always follow checks-effects-interactions when sending value.
 */
contract EtherWallet {
    address public owner;

    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {
        emit Deposited(msg.sender, msg.value);
    }

    function deposit() external payable {
        require(msg.value > 0, "zero");
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(msg.sender == owner, "not owner");
        require(address(this).balance >= amount, "insufficient");

        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "call failed");
        emit Withdrawn(msg.sender, amount);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
