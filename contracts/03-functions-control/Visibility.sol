// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Visibility
 * @notice Function and state-variable visibility: public, private, internal, external.
 * @dev
 * - public: callable internally and externally; auto getter for state vars
 * - private: only this contract
 * - internal: this contract + derived contracts
 * - external: only from outside (cheaper calldata for large args)
 */
contract Visibility {
    uint256 public publicValue = 1;
    uint256 private privateValue = 2;
    uint256 internal internalValue = 3;

    function publicFn() public pure returns (string memory) {
        return "public";
    }

    function privateFn() private pure returns (string memory) {
        return "private";
    }

    function internalFn() internal pure returns (string memory) {
        return "internal";
    }

    function externalFn() external pure returns (string memory) {
        return "external";
    }

    /// @notice Shows calling public/private/internal from inside the contract.
    function callInternals() public pure returns (string memory, string memory, string memory) {
        return (publicFn(), privateFn(), internalFn());
    }

    /// @notice External functions must be called via `this` from inside.
    function callExternalFromInside() public view returns (string memory) {
        return this.externalFn();
    }
}

/**
 * @title VisibilityChild
 * @notice Derived contract can use internal (and public) members of the parent.
 */
contract VisibilityChild is Visibility {
    function readInternal() public view returns (uint256) {
        return internalValue;
    }

    function callParentInternal() public pure returns (string memory) {
        return internalFn();
    }
}
