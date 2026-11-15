// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ReferenceTypes
 * @notice Arrays, structs, mappings, and nested mappings.
 * @dev Reference types point to data; location (storage/memory/calldata) matters.
 */
contract ReferenceTypes {
    struct Person {
        string name;
        uint256 age;
        address wallet;
    }

    uint256[] public numbers;
    Person[] public people;
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowances;

    function pushNumber(uint256 value) public {
        numbers.push(value);
    }

    function getNumber(uint256 index) public view returns (uint256) {
        return numbers[index];
    }

    function addPerson(string memory name, uint256 age, address wallet) public {
        people.push(Person({name: name, age: age, wallet: wallet}));
    }

    function getPerson(uint256 index) public view returns (Person memory) {
        return people[index];
    }

    function setBalance(address account, uint256 amount) public {
        balances[account] = amount;
    }

    function setAllowance(address owner, address spender, uint256 amount) public {
        allowances[owner][spender] = amount;
    }
}
