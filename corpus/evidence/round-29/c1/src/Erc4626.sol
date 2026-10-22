// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Erc4626 {
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
    function asset() external { v_uint256 = block.number; }
    function totalAssets() external { v_uint256 = block.number; }
    function convertToShares(uint256 a0) external { v_uint256 = a0; }
    function convertToAssets(uint256 a0) external { v_uint256 = a0; }
    function maxDeposit(address a0) external { v_address = a0; }
    function previewDeposit(uint256 a0) external { v_uint256 = a0; }
    function deposit(uint256 a0, address a1) external { v_uint256 = a0; v_address = a1; }
    function maxMint(address a0) external { v_address = a0; }
    function previewMint(uint256 a0) external { v_uint256 = a0; }
    function mint(uint256 a0, address a1) external { v_uint256 = a0; v_address = a1; }
    function maxWithdraw(address a0) external { v_address = a0; }
    function previewWithdraw(uint256 a0) external { v_uint256 = a0; }
    function withdraw(uint256 a0, address a1, address a2) external { v_uint256 = a0; v_address = a1; v_address = a2; }
    function maxRedeem(address a0) external { v_address = a0; }
    function previewRedeem(uint256 a0) external { v_uint256 = a0; }
    function redeem(uint256 a0, address a1, address a2) external { v_uint256 = a0; v_address = a1; v_address = a2; }
}
