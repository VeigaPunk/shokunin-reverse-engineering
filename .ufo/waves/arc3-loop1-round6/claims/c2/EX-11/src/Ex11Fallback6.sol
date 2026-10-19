// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Ex11Fallback6 {
    uint256 private a_;
    address private owner_;
    constructor() { owner_ = msg.sender; }
    function setA(uint256 v) external { require(msg.sender == owner_, "auth"); a_ = v; }
    function getA() external view returns (uint256) { return a_; }
    function bump() external { a_ += 1; }
    function tag(bytes32 k) external pure returns (bytes32) { return k; }
    function pay(address to) external payable { (bool ok, ) = to.call{value: msg.value}(""); require(ok, "x"); }
    function close() external { require(msg.sender == owner_, "auth"); a_ = 0; }
    fallback() external payable { a_ += msg.value; }
}
