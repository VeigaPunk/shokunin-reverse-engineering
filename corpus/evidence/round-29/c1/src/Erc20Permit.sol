// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Erc20Permit {
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
    function name() external { v_uint256 = block.number; }
    function symbol() external { v_uint256 = block.number; }
    function decimals() external { v_uint256 = block.number; }
    function totalSupply() external { v_uint256 = block.number; }
    function balanceOf(address a0) external { v_address = a0; }
    function transfer(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function allowance(address a0, address a1) external { v_address = a0; v_address = a1; }
    function approve(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function transferFrom(address a0, address a1, uint256 a2) external { v_address = a0; v_address = a1; v_uint256 = a2; }
    function permit(address a0, address a1, uint256 a2, uint256 a3, uint8 a4, bytes32 a5, bytes32 a6) external { v_address = a0; v_address = a1; v_uint256 = a2; v_uint256 = a3; v_uint8 = a4; v_bytes32 = a5; v_bytes32 = a6; }
    function nonces(address a0) external { v_address = a0; }
    function DOMAIN_SEPARATOR() external { v_uint256 = block.number; }
    function increaseAllowance(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function decreaseAllowance(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
}
