// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ControlFlow
 * @notice if/else, loops, require, assert, and revert.
 * @dev Prefer require/custom errors for input checks; assert for invariants (0.8+ panics).
 */
contract ControlFlow {
    uint256 public counter;

    function classify(uint256 n) public pure returns (string memory) {
        if (n == 0) {
            return "zero";
        } else if (n % 2 == 0) {
            return "even";
        } else {
            return "odd";
        }
    }

    function sumTo(uint256 n) public pure returns (uint256 sum) {
        for (uint256 i = 1; i <= n; i++) {
            sum += i;
        }
    }

    function incrementWhile(uint256 times) public {
        uint256 i = 0;
        while (i < times) {
            counter++;
            i++;
        }
    }

    function mustBePositive(int256 value) public pure {
        require(value > 0, "must be positive");
    }

    function forceRevert(string memory reason) public pure {
        revert(reason);
    }

    /// @notice Assert is for internal invariants that should never fail.
    function checkInvariant(uint256 a, uint256 b) public pure returns (uint256) {
        uint256 result = a + b;
        assert(result >= a);
        return result;
    }
}
