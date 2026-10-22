// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GovernorBravo {
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
    function propose(address[] calldata a0, uint256[] calldata a1, string[] calldata a2, bytes[] calldata a3, string calldata a4) external { v_dyn = keccak256(abi.encode(a0)); v_dyn = keccak256(abi.encode(a1)); v_dyn = keccak256(abi.encode(a2)); v_dyn = keccak256(abi.encode(a3)); v_dyn = keccak256(abi.encode(a4)); }
    function queue(uint256 a0) external { v_uint256 = a0; }
    function castVote(uint256 a0, uint8 a1) external { v_uint256 = a0; v_uint8 = a1; }
    function castVoteWithReason(uint256 a0, uint8 a1, string calldata a2) external { v_uint256 = a0; v_uint8 = a1; v_dyn = keccak256(abi.encode(a2)); }
    function state(uint256 a0) external { v_uint256 = a0; }
    function proposalCount() external { v_uint256 = block.number; }
    function votingDelay() external { v_uint256 = block.number; }
    function votingPeriod() external { v_uint256 = block.number; }
    function proposalThreshold() external { v_uint256 = block.number; }
    function quorumVotes() external { v_uint256 = block.number; }
    function getVotes(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
    function delegate(address a0) external { v_address = a0; }
    function delegates(address a0) external { v_address = a0; }
    function getCurrentVotes(address a0) external { v_address = a0; }
    function getPriorVotes(address a0, uint256 a1) external { v_address = a0; v_uint256 = a1; }
}
