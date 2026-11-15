// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ValueTypes
 * @notice Demonstrates Solidity value types: integers, bool, address, bytes, enum.
 * @dev Value types are copied when assigned or passed (except when in storage references).
 */
contract ValueTypes {
    enum Status {
        Pending,
        Active,
        Closed
    }

    uint256 public unsignedInt = 42;
    int256 public signedInt = -7;
    bool public flag = true;
    address public owner;
    bytes32 public fixedBytes = keccak256("solidity");
    bytes public dynamicBytes = hex"deadbeef";
    Status public status = Status.Pending;

    constructor() {
        owner = msg.sender;
    }

    function setUnsigned(uint256 value) public {
        unsignedInt = value;
    }

    function setSigned(int256 value) public {
        signedInt = value;
    }

    function toggleFlag() public {
        flag = !flag;
    }

    function setStatus(Status newStatus) public {
        status = newStatus;
    }

    /// @notice Addresses are 20-byte identifiers; payable allows receiving ETH.
    function setOwner(address newOwner) public {
        owner = newOwner;
    }
}
