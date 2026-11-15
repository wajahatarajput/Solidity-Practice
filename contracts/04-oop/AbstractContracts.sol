// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title AbstractContracts
 * @notice Abstract base defines the interface of behavior; children fill in details.
 * @dev An abstract contract cannot be deployed until all unimplemented functions exist.
 */
abstract contract Shape {
    function area() public view virtual returns (uint256);

    function name() public pure virtual returns (string memory) {
        return "Shape";
    }
}

contract Rectangle is Shape {
    uint256 public width;
    uint256 public height;

    constructor(uint256 _width, uint256 _height) {
        width = _width;
        height = _height;
    }

    function area() public view override returns (uint256) {
        return width * height;
    }

    function name() public pure override returns (string memory) {
        return "Rectangle";
    }
}

contract Circle is Shape {
    uint256 public radius;

    constructor(uint256 _radius) {
        radius = _radius;
    }

    function area() public view override returns (uint256) {
        // Integer approximation of pi * r^2 using 314/100
        return (314 * radius * radius) / 100;
    }

    function name() public pure override returns (string memory) {
        return "Circle";
    }
}
