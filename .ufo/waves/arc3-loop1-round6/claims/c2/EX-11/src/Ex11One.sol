// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Ex11One {
    uint256 private a_;
    function only(uint256 v) external { a_ = v; }
}
