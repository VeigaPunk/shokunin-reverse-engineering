// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PayK7 {
    receive() external payable {}

    function p0(uint256 x) external returns (uint256) { return x + 1; }
    function p1(uint256 x) external returns (uint256) { return x + 2; }
    function p2(uint256 x) external returns (uint256) { return x + 3; }
    function p3(uint256 x) external returns (uint256) { return x + 4; }
    function p4(uint256 x) external returns (uint256) { return x + 5; }
    function p5(uint256 x) external returns (uint256) { return x + 6; }
    function p6(uint256 x) external returns (uint256) { return x + 7; }
}
