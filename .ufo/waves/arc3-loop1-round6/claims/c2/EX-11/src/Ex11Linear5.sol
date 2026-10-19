// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Ex11Linear5 {
    uint256 private a_;
    address private owner_;
    constructor() { owner_ = msg.sender; }
    function setA(uint256 v) external { require(msg.sender == owner_, "auth"); a_ = v; }
    function getA() external view returns (uint256) { return a_; }
    function owner() external view returns (address) { return owner_; }
    function poke() external { a_ = a_ + 1; }
    function tag(bytes32 k) external pure returns (bytes32) { return k; }
}
