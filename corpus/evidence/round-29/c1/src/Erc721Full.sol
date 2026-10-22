// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Erc721Full {
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
    function ownerOf(uint256 a0) external { v_uint256 = a0; }
    function safeTransferFrom(address a0, address a1, uint256 a2) external { v_address = a0; v_address = a1; v_uint256 = a2; }
    function safeTransferFrom(address a0, address a1, uint256 a2, bytes calldata a3) external { v_address = a0; v_address = a1; v_uint256 = a2; v_dyn = keccak256(abi.encode(a3)); }
    function setApprovalForAll(address a0, bool a1) external { v_address = a0; v_bool = a1; }
    function getApproved(uint256 a0) external { v_uint256 = a0; }
    function isApprovedForAll(address a0, address a1) external { v_address = a0; v_address = a1; }
    function tokenURI(uint256 a0) external { v_uint256 = a0; }
    function tokenOfOwnerByIndex(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function tokenByIndex(uint256 a0) external { v_uint256 = a0; }
    function supportsInterface(bytes4 a0) external { v_bytes4 = a0; }
    function baseURI() external { v_uint256 = block.number; }
    function mint(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function burn(uint256 a0) external { v_uint256 = a0; }
}
