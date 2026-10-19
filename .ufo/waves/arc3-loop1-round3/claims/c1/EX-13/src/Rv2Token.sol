// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Rv2Token {
    mapping(address => uint256) private _bal;
    mapping(address => mapping(address => uint256)) private _allow;
    uint256 private _supply;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256) {
        return _supply;
    }

    function balanceOf(address a) external view returns (uint256) {
        return _bal[a];
    }

    function transfer(address to, uint256 value) external returns (bool) {
        _bal[msg.sender] -= value;
        _bal[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        _allow[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        _allow[from][msg.sender] -= value;
        _bal[from] -= value;
        _bal[to] += value;
        emit Transfer(from, to, value);
        return true;
    }
}
