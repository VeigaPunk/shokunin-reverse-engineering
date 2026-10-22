// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UniV2Pair {
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
    function token0() external { v_uint256 = block.number; }
    function token1() external { v_uint256 = block.number; }
    function factory() external { v_uint256 = block.number; }
    function getReserves() external { v_uint256 = block.number; }
    function price0CumulativeLast() external { v_uint256 = block.number; }
    function price1CumulativeLast() external { v_uint256 = block.number; }
    function kLast() external { v_uint256 = block.number; }
    function mint(address a0) external { v_address = a0; }
    function burn(address a0) external { v_address = a0; }
    function swap(uint256 a0, uint256 a1, address a2, bytes calldata a3) external { v_uint256 = a0; v_uint256 = a1; v_address = a2; v_dyn = keccak256(abi.encode(a3)); }
    function skim(address a0) external { v_address = a0; }
    function sync() external { v_uint256 = block.number; }
    function initialize(address a0, address a1) external { v_address = a0; v_address = a1; }
    function MINIMUM_LIQUIDITY() external { v_uint256 = block.number; }
    function PERMIT_TYPEHASH() external { v_uint256 = block.number; }
}
