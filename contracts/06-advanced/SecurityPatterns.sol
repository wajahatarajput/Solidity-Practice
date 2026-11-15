// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title SecurityPatterns
 * @notice Checks-effects-interactions and a simple reentrancy guard.
 * @dev Educational sketch — production code should use audited libraries (e.g. OpenZeppelin).
 */
contract SecurityPatterns {
    mapping(address => uint256) public balances;
    bool private locked;

    error ReentrantCall();

    modifier nonReentrant() {
        if (locked) revert ReentrantCall();
        locked = true;
        _;
        locked = false;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    /// @notice CEI: update state before external interaction.
    function withdraw(uint256 amount) external nonReentrant {
        // Checks
        require(amount > 0, "zero");
        require(balances[msg.sender] >= amount, "insufficient");

        // Effects
        balances[msg.sender] -= amount;

        // Interactions
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "transfer failed");
    }
}
