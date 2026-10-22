// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UniV2Router {
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
    function WETH() external { v_uint256 = block.number; }
    function addLiquidity(address a0, address a1, uint256 a2, uint256 a3, uint256 a4, uint256 a5, address a6, uint256 a7) external { v_address = a0; v_address = a1; v_uint256 = a2; v_uint256 = a3; v_uint256 = a4; v_uint256 = a5; v_address = a6; v_uint256 = a7; }
    function addLiquidityETH(address a0, uint256 a1, uint256 a2, uint256 a3, address a4, uint256 a5) external { v_address = a0; v_uint256 = a1; v_uint256 = a2; v_uint256 = a3; v_address = a4; v_uint256 = a5; }
    function removeLiquidity(address a0, address a1, uint256 a2, uint256 a3, uint256 a4, address a5, uint256 a6) external { v_address = a0; v_address = a1; v_uint256 = a2; v_uint256 = a3; v_uint256 = a4; v_address = a5; v_uint256 = a6; }
    function removeLiquidityETH(address a0, uint256 a1, uint256 a2, uint256 a3, address a4, uint256 a5) external { v_address = a0; v_uint256 = a1; v_uint256 = a2; v_uint256 = a3; v_address = a4; v_uint256 = a5; }
    function swapExactTokensForTokens(uint256 a0, uint256 a1, address[] calldata a2, address a3, uint256 a4) external { v_uint256 = a0; v_uint256 = a1; v_dyn = keccak256(abi.encode(a2)); v_address = a3; v_uint256 = a4; }
    function swapTokensForExactTokens(uint256 a0, uint256 a1, address[] calldata a2, address a3, uint256 a4) external { v_uint256 = a0; v_uint256 = a1; v_dyn = keccak256(abi.encode(a2)); v_address = a3; v_uint256 = a4; }
    function swapExactETHForTokens(uint256 a0, address[] calldata a1, address a2, uint256 a3) external { v_uint256 = a0; v_dyn = keccak256(abi.encode(a1)); v_address = a2; v_uint256 = a3; }
    function swapExactTokensForETH(uint256 a0, uint256 a1, address[] calldata a2, address a3, uint256 a4) external { v_uint256 = a0; v_uint256 = a1; v_dyn = keccak256(abi.encode(a2)); v_address = a3; v_uint256 = a4; }
    function getAmountsOut(uint256 a0, address[] calldata a1) external { v_uint256 = a0; v_dyn = keccak256(abi.encode(a1)); }
    function getAmountsIn(uint256 a0, address[] calldata a1) external { v_uint256 = a0; v_dyn = keccak256(abi.encode(a1)); }
    function quote(uint256 a0, uint256 a1, uint256 a2) external { v_uint256 = a0; v_uint256 = a1; v_uint256 = a2; }
    function getAmountOut(uint256 a0, uint256 a1, uint256 a2) external { v_uint256 = a0; v_uint256 = a1; v_uint256 = a2; }
    function getAmountIn(uint256 a0, uint256 a1, uint256 a2) external { v_uint256 = a0; v_uint256 = a1; v_uint256 = a2; }
}
