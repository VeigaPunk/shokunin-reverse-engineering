// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Non-ERC-20-shaped carrier: payable receive + fallback, mixed mutability
// (view/pure/nonpayable/payable), no token-ish selectors.
contract Treasury {
    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    address public owner;
    uint256 public tally;
    mapping(address => uint256) public credited;

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {
        tally += msg.value;
        credited[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    fallback() external payable {
        tally += 1;
    }

    function deposit() external payable {
        tally += msg.value;
        credited[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(msg.sender == owner, "not owner");
        tally -= amount;
        (bool ok, ) = owner.call{value: amount}("");
        require(ok, "send failed");
        emit Withdrawn(owner, amount);
    }

    function peek() external view returns (uint256) {
        return tally;
    }

    function creditOf(address who) external view returns (uint256) {
        return credited[who];
    }

    function tag() external pure returns (string memory) {
        return "treasury-v1";
    }
}