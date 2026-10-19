// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Non-ERC-20-shaped carrier (arc3-loop1-round3, seat SC-1 reference ledger leg B):
// payable receive/fallback + mixed mutability (payable/nonpayable/view/pure).
contract VaultCourt {
    address public owner;
    uint256 public totalDeposits;
    mapping(address => uint256) public balances;

    event Deposit(address indexed who, uint256 amount);
    event OwnershipTransferred(address indexed from, address indexed to);

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    fallback() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function deposit() external payable {
        require(msg.value > 0, "zero");
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
    }

    function setOwner(address newOwner) external {
        require(msg.sender == owner, "not owner");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

    function balancesOf(address who) external view returns (uint256) {
        return balances[who];
    }

    function summary() external view returns (address, uint256) {
        return (owner, totalDeposits);
    }

    function doubleValue(uint256 x) external pure returns (uint256) {
        return x * 2;
    }

    function timestampProbe() external view returns (uint256) {
        return block.timestamp;
    }
}