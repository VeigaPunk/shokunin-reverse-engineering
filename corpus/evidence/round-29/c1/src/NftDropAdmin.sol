// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NftDropAdmin {
    address internal v_address;
    bool internal v_bool;
    bytes32 internal v_bytes32;
    bytes4 internal v_bytes4;
    uint256 internal v_uint256;
    uint64 internal v_uint64;
    uint8 internal v_uint8;
    uint80 internal v_uint80;
    uint96 internal v_uint96;
    bytes32 internal v_dyn;
    function royaltyInfo(uint256 a0, uint256 a1) external { v_uint256 = a0; v_uint256 = a1; }
    function setDefaultRoyalty(address a0, uint96 a1) external { v_address = a0; v_uint96 = a1; }
    function contractURI() external { v_uint256 = block.number; }
    function setBaseURI(string calldata a0) external { v_dyn = keccak256(abi.encode(a0)); }
    function withdrawAll() external { v_uint256 = block.number; }
    function maxSupply() external { v_uint256 = block.number; }
    function mintPrice() external { v_uint256 = block.number; }
    function setMintPrice(uint256 a0) external { v_uint256 = a0; }
    function publicMint(uint256 a0) external { v_uint256 = a0; }
    function airdrop(address[] calldata a0, uint256[] calldata a1) external { v_dyn = keccak256(abi.encode(a0)); v_dyn = keccak256(abi.encode(a1)); }
}
