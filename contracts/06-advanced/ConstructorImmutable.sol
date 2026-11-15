// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ConstructorImmutable
 * @notice Constructors run once at deploy; immutable/constant save gas vs storage.
 * @dev
 * - constant: must be known at compile time
 * - immutable: set in constructor, then forever read-only (still cheaper than storage)
 */
contract ConstructorImmutable {
    uint256 public constant MAX_SUPPLY = 1_000_000;
    address public immutable deployer;
    uint256 public immutable createdAt;
    string public name;

    constructor(string memory _name) {
        deployer = msg.sender;
        createdAt = block.timestamp;
        name = _name;
    }

    function info()
        external
        view
        returns (address, uint256, uint256, string memory)
    {
        return (deployer, createdAt, MAX_SUPPLY, name);
    }
}
