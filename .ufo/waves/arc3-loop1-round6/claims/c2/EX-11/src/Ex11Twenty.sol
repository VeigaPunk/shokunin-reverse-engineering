// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Ex11Twenty {
    uint256 private s_;
    address private o_;
    constructor() { o_ = msg.sender; }
    function f01() external view returns (uint256) { return s_; }
    function f02(uint256 v, uint256 w) external pure returns (uint256) { return v ^ w; }
    function f03(address a) external view returns (uint256) { return a == o_ ? 1 : 0; }
    function f04(bytes32 k) external { s_ = uint256(k); }
    function f05(uint256 v) external payable { s_ = msg.value + v; }
    function f06() external view returns (uint256) { return s_; }
    function f07(uint256 v, uint256 w) external pure returns (uint256) { return v ^ w; }
    function f08(address a) external view returns (uint256) { return a == o_ ? 1 : 0; }
    function f09(bytes32 k) external { s_ = uint256(k); }
    function f10(uint256 v) external payable { s_ = msg.value + v; }
    function f11() external view returns (uint256) { return s_; }
    function f12(uint256 v, uint256 w) external pure returns (uint256) { return v ^ w; }
    function f13(address a) external view returns (uint256) { return a == o_ ? 1 : 0; }
    function f14(bytes32 k) external { s_ = uint256(k); }
    function f15(uint256 v) external payable { s_ = msg.value + v; }
    function f16() external view returns (uint256) { return s_; }
    function f17(uint256 v, uint256 w) external pure returns (uint256) { return v ^ w; }
    function f18(address a) external view returns (uint256) { return a == o_ ? 1 : 0; }
    function f19(bytes32 k) external { s_ = uint256(k); }
    function f20(uint256 v) external payable { s_ = msg.value + v; }
}
