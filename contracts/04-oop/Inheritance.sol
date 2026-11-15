// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Inheritance
 * @notice Single inheritance with virtual / override — OOP "is-a" relationships.
 * @dev Mark functions `virtual` so children can `override` them.
 */
contract Animal {
    string public name;

    constructor(string memory _name) {
        name = _name;
    }

    function speak() public pure virtual returns (string memory) {
        return "...";
    }

    function describe() public view virtual returns (string memory) {
        return string(abi.encodePacked("Animal: ", name));
    }
}

contract Dog is Animal {
    constructor(string memory _name) Animal(_name) {}

    function speak() public pure override returns (string memory) {
        return "woof";
    }

    function describe() public view override returns (string memory) {
        return string(abi.encodePacked("Dog: ", name));
    }
}
