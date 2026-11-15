// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title AssemblyBasics
 * @notice Minimal inline assembly (Yul) for low-level operations.
 * @dev Prefer high-level Solidity unless you need gas tweaks or custom slot access.
 */
contract AssemblyBasics {
    uint256 public stored;

    function addAssembly(uint256 a, uint256 b) external pure returns (uint256 result) {
        assembly {
            result := add(a, b)
        }
    }

    function storeAssembly(uint256 value) external {
        assembly {
            // slot 0 is the first state variable (`stored`)
            sstore(0, value)
        }
    }

    function loadAssembly() external view returns (uint256 value) {
        assembly {
            value := sload(0)
        }
    }

    function getCodeSize(address account) external view returns (uint256 size) {
        assembly {
            size := extcodesize(account)
        }
    }
}
