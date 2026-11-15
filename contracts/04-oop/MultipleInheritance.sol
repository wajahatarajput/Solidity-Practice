// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title MultipleInheritance
 * @notice Diamond inheritance and C3 linearization.
 * @dev When two parents define the same function, list bases from most base-like
 *      to most derived, and use `override(A, B)` to pick the implementation path.
 */

contract A {
    function greet() public pure virtual returns (string memory) {
        return "A";
    }
}

contract B is A {
    function greet() public pure virtual override returns (string memory) {
        return string(abi.encodePacked(super.greet(), " -> B"));
    }
}

contract C is A {
    function greet() public pure virtual override returns (string memory) {
        return string(abi.encodePacked(super.greet(), " -> C"));
    }
}

/// @dev Linearization for `D is B, C` is D, C, B, A (right-most parent first for `super`).
contract D is B, C {
    function greet() public pure override(B, C) returns (string memory) {
        return string(abi.encodePacked(super.greet(), " -> D"));
    }
}
