// SPDX-License-Identifier: MIT
pragma solidity 0.8.37;

library Fees {
    function cut(uint256 amount) internal pure returns (uint256) {
        return amount / 100;
    }
}

contract VaultB {
    address public owner;
    uint256 public totalDeposits;
    uint256 public feeBps;
    bool public paused;
    mapping(address => uint256) public balances;
    mapping(address => uint256) public locked;

    event Deposited(address indexed who, uint256 amount);
    error NotOwner();
    error IsPaused();
    error Insufficient();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() payable {
        owner = msg.sender;
    }

    receive() external payable {
        _credit(msg.sender, msg.value);
    }

    fallback() external payable {
        totalDeposits += msg.value;
    }

    function deposit() public payable {
        _credit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        if (amount > balances[msg.sender]) revert Insufficient();
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "xfer");
    }

    function setFee(uint256 bps) external onlyOwner {
        feeBps = bps;
    }

    function feeOn(uint256 amount) external view returns (uint256) {
        return Fees.cut(amount);
    }

    function pause() external onlyOwner {
        paused = true;
    }

    function unpause() external onlyOwner {
        paused = false;
    }

    function lockFor(address who, uint256 amount) external onlyOwner {
        locked[who] += amount;
    }

    function _credit(address who, uint256 amount) internal {
        if (paused) revert IsPaused();
        balances[who] += amount;
        totalDeposits += amount;
        emit Deposited(who, amount);
    }
}