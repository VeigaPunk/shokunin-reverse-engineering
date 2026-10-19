// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Rv2Many {
    uint256[] private xs;
    function f0(uint256 a) external { xs.push(a); }
    function f1(uint256 a) external { xs.push(a + 1); }
    function f2(uint256 a) external { xs.push(a + 2); }
    function f3(uint256 a) external { xs.push(a + 3); }
    function f4(uint256 a) external { xs.push(a + 4); }
    function f5(uint256 a) external { xs.push(a + 5); }
    function f6(uint256 a) external { xs.push(a + 6); }
    function f7(uint256 a) external { xs.push(a + 7); }
    function f8(uint256 a) external { xs.push(a + 8); }
    function f9(uint256 a) external { xs.push(a + 9); }
    function count() external view returns (uint256) { return xs.length; }
}
