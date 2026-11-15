// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Libraries
 * @notice Reusable code deployed once and linked — similar to static utility classes.
 * @dev `using Lib for Type` attaches library functions as methods on that type.
 */
library MathLib {
    function max(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }

    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a < b ? a : b;
    }

    function clamp(uint256 value, uint256 lo, uint256 hi) internal pure returns (uint256) {
        return max(lo, min(value, hi));
    }
}

library ArrayLib {
    function sum(uint256[] memory arr) internal pure returns (uint256 total) {
        for (uint256 i = 0; i < arr.length; i++) {
            total += arr[i];
        }
    }
}

contract LibraryDemo {
    using MathLib for uint256;
    using ArrayLib for uint256[];

    function bigger(uint256 a, uint256 b) public pure returns (uint256) {
        return a.max(b);
    }

    function bounded(uint256 value) public pure returns (uint256) {
        return value.clamp(10, 100);
    }

    function total(uint256[] memory values) public pure returns (uint256) {
        return values.sum();
    }
}
