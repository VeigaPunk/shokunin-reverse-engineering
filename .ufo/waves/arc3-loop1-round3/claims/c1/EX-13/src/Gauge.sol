// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Library-bound shape carrier: internal library via `using for` (inlined at
// compile time) + an external library call surface (delegatecall stubs).
library MathLib {
    function scaled(uint256 a, uint256 b) internal pure returns (uint256) {
        return a * b + 1;
    }

    function shout(uint256 a) external pure returns (uint256) {
        return a + 7;
    }
}

contract Gauge {
    using MathLib for uint256;

    uint256 public base;
    mapping(address => uint256) public weight;

    function set(uint256 v) external {
        base = v;
    }

    function measure(uint256 factor) external view returns (uint256) {
        return base.scaled(factor);
    }

    function weightOf(address who) external view returns (uint256) {
        return weight[who];
    }

    function bump() external {
        weight[msg.sender] += 1;
        base += weight[msg.sender].scaled(2);
    }
}