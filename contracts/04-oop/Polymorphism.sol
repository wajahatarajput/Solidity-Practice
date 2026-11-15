// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title Polymorphism
 * @notice Same call site, different runtime behavior via overrides.
 * @dev Hold a base-type reference; the child's override runs when you call virtual functions.
 */
abstract contract PaymentMethod {
    function pay(uint256 amount) public pure virtual returns (string memory);
}

contract CashPayment is PaymentMethod {
    function pay(uint256) public pure override returns (string memory) {
        return "paid with cash";
    }
}

contract CardPayment is PaymentMethod {
    function pay(uint256) public pure override returns (string memory) {
        return "paid with card";
    }
}

contract Checkout {
    /// @notice Accepts any PaymentMethod; dispatch uses the concrete type.
    function checkout(PaymentMethod method, uint256 amount)
        public
        pure
        returns (string memory)
    {
        return method.pay(amount);
    }
}
