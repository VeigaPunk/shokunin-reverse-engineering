// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SafeOwners {
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
    function getOwners() external { v_uint256 = block.number; }
    function getThreshold() external { v_uint256 = block.number; }
    function isOwner(address a0) external { v_address = a0; }
    function nonce() external { v_uint256 = block.number; }
    function addOwnerWithThreshold(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function removeOwner(address a0, address a1, uint256 a2) external { v_address = a0; v_address = a1; v_uint256 = a2; }
    function swapOwner(address a0, address a1, address a2) external { v_address = a0; v_address = a1; v_address = a2; }
    function changeThreshold(uint256 a0) external { v_uint256 = a0; }
    function enableModule(address a0) external { v_address = a0; }
    function disableModule(address a0, address a1) external { v_address = a0; v_address = a1; }
    function isModuleEnabled(address a0) external { v_address = a0; }
    function setGuard(address a0) external { v_address = a0; }
    function VERSION() external { v_uint256 = block.number; }
}
