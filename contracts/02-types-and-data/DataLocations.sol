// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title DataLocations
 * @notice storage vs memory vs calldata for reference types.
 * @dev
 * - storage: persistent on-chain state (expensive to write)
 * - memory: temporary, mutable during the call
 * - calldata: read-only, cheaper for external function args
 */
contract DataLocations {
    struct Item {
        string name;
        uint256 quantity;
    }

    Item[] public items;

    /// @notice Append using calldata (cheapest for external string inputs).
    function addItem(string calldata name, uint256 quantity) external {
        items.push(Item({name: name, quantity: quantity}));
    }

    /// @notice Return a memory copy of an item.
    function getItem(uint256 index) external view returns (Item memory) {
        return items[index];
    }

    /**
     * @notice Mutate via a storage pointer; a memory copy does not persist.
     * @dev `Item storage ref = items[i]` aliases on-chain data; `Item memory copy` does not.
     */
    function updateFirst(string memory newName, uint256 newQuantity) external {
        require(items.length > 0, "empty");

        Item storage storageRef = items[0];
        storageRef.name = newName;
        storageRef.quantity = newQuantity;

        Item memory memCopy = items[0];
        // Local only — does not write back to storage:
        memCopy.quantity = memCopy.quantity + 1;
    }
}
