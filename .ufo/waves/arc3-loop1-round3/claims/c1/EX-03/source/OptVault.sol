// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OptVault {
    address private _owner;
    bool private _paused;
    mapping(address => uint256) private _credit;

    constructor() { _owner = msg.sender; }

    receive() external payable {}
    fallback() external payable {}

    function deposit() external payable returns (uint256) {
        _credit[msg.sender] += msg.value;
        return _credit[msg.sender];
    }

    function withdraw(uint256 amount) external {
        require(!_paused, "paused");
        _credit[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function creditOf(address a) external view returns (uint256) {
        return _credit[a];
    }

    function paused() external view returns (bool) {
        return _paused;
    }

    function setPaused(bool p) external {
        require(msg.sender == _owner, "owner");
        _paused = p;
    }
}