// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ViewPurePayable
 * @notice view, pure, payable functions plus receive and fallback.
 * @dev
 * - view: reads state, does not modify it
 * - pure: neither reads nor writes state
 * - payable: can receive ETH with the call
 * - receive: plain ETH transfers (empty calldata)
 * - fallback: unknown function selector or non-empty calldata with no match
 */
contract ViewPurePayable {
    uint256 public totalReceived;
    address public lastSender;

    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function deposit() public payable {
        require(msg.value > 0, "send ETH");
        totalReceived += msg.value;
        lastSender = msg.sender;
    }

    receive() external payable {
        totalReceived += msg.value;
        lastSender = msg.sender;
    }

    fallback() external payable {
        totalReceived += msg.value;
        lastSender = msg.sender;
    }
}
