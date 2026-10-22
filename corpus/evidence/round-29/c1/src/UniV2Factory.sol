// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UniV2Factory {
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
    function getPair(address a0, address a1) external { v_address = a0; v_address = a1; }
    function allPairs(uint256 a0) external { v_uint256 = a0; }
    function allPairsLength() external { v_uint256 = block.number; }
    function createPair(address a0, address a1) external { v_address = a0; v_address = a1; }
    function feeTo() external { v_uint256 = block.number; }
    function feeToSetter() external { v_uint256 = block.number; }
    function setFeeTo(address a0) external { v_address = a0; }
    function setFeeToSetter(address a0) external { v_address = a0; }
}
