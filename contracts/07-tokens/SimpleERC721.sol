// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title SimpleERC721
 * @notice Minimal ERC-721-style NFT mint and transfer for learning.
 * @dev Simplified — omits full ERC-165/approval-for-all edge cases of production NFTs.
 */
contract SimpleERC721 {
    string public name;
    string public symbol;

    uint256 private nextId = 1;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    constructor(string memory _name, string memory _symbol) {
        name = _name;
        symbol = _symbol;
    }

    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "zero");
        return _balances[owner];
    }

    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "nonexistent");
        return owner;
    }

    function approve(address to, uint256 tokenId) external {
        address owner = ownerOf(tokenId);
        require(msg.sender == owner, "not owner");
        _tokenApprovals[tokenId] = to;
        emit Approval(owner, to, tokenId);
    }

    function getApproved(uint256 tokenId) public view returns (address) {
        require(_owners[tokenId] != address(0), "nonexistent");
        return _tokenApprovals[tokenId];
    }

    function mint(address to) external returns (uint256 tokenId) {
        require(to != address(0), "zero");
        tokenId = nextId++;
        _owners[tokenId] = to;
        _balances[to] += 1;
        emit Transfer(address(0), to, tokenId);
    }

    function transferFrom(address from, address to, uint256 tokenId) external {
        require(to != address(0), "zero");
        address owner = ownerOf(tokenId);
        require(owner == from, "from");
        require(
            msg.sender == owner || msg.sender == _tokenApprovals[tokenId],
            "not authorized"
        );

        delete _tokenApprovals[tokenId];
        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }
}
