// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title CallDelegatecall
 * @notice Low-level call vs delegatecall (learning demo — handle with care).
 * @dev
 * - call: executes in the callee's context (their storage)
 * - delegatecall: executes callee code in the caller's context (proxy pattern)
 * Never delegatecall to untrusted contracts — they can rewrite your storage.
 */

contract Logic {
    uint256 public number;
    address public sender;

    function setNumber(uint256 _number) external {
        number = _number;
        sender = msg.sender;
    }
}

contract Caller {
    uint256 public number;
    address public sender;

    /// @notice Regular call: updates Logic's storage, not Caller's.
    function callSetNumber(address logic, uint256 _number) external {
        (bool ok, ) = logic.call(abi.encodeWithSignature("setNumber(uint256)", _number));
        require(ok, "call failed");
    }

    /// @notice Delegatecall: Logic's code runs but writes to Caller's storage slots.
    function delegateSetNumber(address logic, uint256 _number) external {
        (bool ok, ) = logic.delegatecall(
            abi.encodeWithSignature("setNumber(uint256)", _number)
        );
        require(ok, "delegatecall failed");
    }
}
