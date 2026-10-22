// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Weth9 {
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
    function deposit() external { v_uint256 = block.number; }
    function withdraw(uint256 a0) external { v_uint256 = a0; }
}
