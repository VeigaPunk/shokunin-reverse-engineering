// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Erc1155 {
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
    function balanceOf(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function balanceOfBatch(address[] calldata a0, uint256[] calldata a1) external { v_dyn = keccak256(abi.encode(a0)); v_dyn = keccak256(abi.encode(a1)); }
    function safeTransferFrom(address a0, address a1, uint256 a2, uint256 a3, bytes calldata a4) external { v_address = a0; v_address = a1; v_uint256 = a2; v_uint256 = a3; v_dyn = keccak256(abi.encode(a4)); }
    function safeBatchTransferFrom(address a0, address a1, uint256[] calldata a2, uint256[] calldata a3, bytes calldata a4) external { v_address = a0; v_address = a1; v_dyn = keccak256(abi.encode(a2)); v_dyn = keccak256(abi.encode(a3)); v_dyn = keccak256(abi.encode(a4)); }
    function uri(uint256 a0) external { v_uint256 = a0; }
}
