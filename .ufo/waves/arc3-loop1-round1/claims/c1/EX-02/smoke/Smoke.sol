// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Smoke {
    uint256 private value;
    mapping(address => uint256) public balanceOf;

    event ValueSet(uint256 indexed v);

    function set(uint256 v) external {
        value = v;
        emit ValueSet(v);
    }

    function get() external view returns (uint256) {
        return value;
    }

    function deposit() external payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
