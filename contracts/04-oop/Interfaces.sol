// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Interfaces
 * @notice Interfaces define function signatures without implementation (like OOP interfaces).
 * @dev All interface functions are implicitly external; no state variables allowed.
 */
interface ICounter {
    function increment() external;
    function current() external view returns (uint256);
}

contract Counter is ICounter {
    uint256 private count;

    function increment() external override {
        count += 1;
    }

    function current() external view override returns (uint256) {
        return count;
    }
}

/**
 * @title CounterUser
 * @notice Talks to any contract that implements ICounter — loose coupling.
 */
contract CounterUser {
    function bumpTwice(ICounter counter) external {
        counter.increment();
        counter.increment();
    }
}
