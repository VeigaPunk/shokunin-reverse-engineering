// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EnsRegistry {
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
    function owner(bytes32 a0) external { v_bytes32 = a0; }
    function resolver(bytes32 a0) external { v_bytes32 = a0; }
    function ttl(bytes32 a0) external { v_bytes32 = a0; }
    function setOwner(bytes32 a0, address a1) external { v_bytes32 = a0; v_address = a1; }
    function setSubnodeOwner(bytes32 a0, bytes32 a1, address a2) external { v_bytes32 = a0; v_bytes32 = a1; v_address = a2; }
    function setResolver(bytes32 a0, address a1) external { v_bytes32 = a0; v_address = a1; }
    function setTTL(bytes32 a0, uint64 a1) external { v_bytes32 = a0; v_uint64 = a1; }
    function recordExists(bytes32 a0) external { v_bytes32 = a0; }
    function setRecord(bytes32 a0, address a1, address a2, uint64 a3) external { v_bytes32 = a0; v_address = a1; v_address = a2; v_uint64 = a3; }
}
