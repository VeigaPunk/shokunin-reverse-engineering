// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// ViaIrVault — EX-7 seat (arc3-loop1-round6): viaIR dispatcher carrier.
/// 14 explicit external functions + receive() = 15 dispatched entries.
/// Mixed mutability, no ERC-20 surface. Compiled with via_ir:true.
contract ViaIrVault {
    address private owner_;
    uint256 private total_;
    uint256 private fee_;
    bool private paused_;
    mapping(address => uint256) private balances_;
    mapping(bytes32 => bool) private marks_;

    constructor() {
        owner_ = msg.sender;
    }

    receive() external payable {
        require(!paused_, "paused");
        balances_[msg.sender] += msg.value;
        total_ += msg.value;
    }

    function deposit() external payable {
        require(!paused_, "paused");
        balances_[msg.sender] += msg.value;
        total_ += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(!paused_, "paused");
        require(balances_[msg.sender] >= amount, "short");
        balances_[msg.sender] -= amount;
        total_ -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "xfer");
    }

    function sweep(address to) external {
        require(msg.sender == owner_, "auth");
        (bool ok, ) = to.call{value: address(this).balance}("");
        require(ok, "xfer");
    }

    function pause() external {
        require(msg.sender == owner_, "auth");
        paused_ = true;
    }

    function unpause() external {
        require(msg.sender == owner_, "auth");
        paused_ = false;
    }

    function setFee(uint256 bps) external {
        require(msg.sender == owner_, "auth");
        require(bps <= 10000, "range");
        fee_ = bps;
    }

    function mark(bytes32 k) external {
        marks_[k] = true;
    }

    function readTotal() external view returns (uint256) {
        return total_;
    }

    function readFee() external view returns (uint256) {
        return fee_;
    }

    function readPaused() external view returns (bool) {
        return paused_;
    }

    function readOwner() external view returns (address) {
        return owner_;
    }

    function readBalance(address who) external view returns (uint256) {
        return balances_[who];
    }

    function marked(bytes32 k) external view returns (bool) {
        return marks_[k];
    }

    function digestOf(bytes32 k) external view returns (bytes32) {
        return keccak256(abi.encode(k, block.chainid));
    }

    function scale(uint256 x, uint256 n) external pure returns (uint256) {
        require(n < 256, "range");
        return (x << n) | (x >> (256 - n));
    }
}
