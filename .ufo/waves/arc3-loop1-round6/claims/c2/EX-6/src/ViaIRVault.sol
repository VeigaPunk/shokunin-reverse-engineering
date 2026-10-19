// SPDX-License-Identifier: MIT
pragma solidity ^0.8.37;

/// ViaIRVault — EX-6 seat carrier, arc3-loop1-round6 (kaidoku-shokunin).
/// Compiled with solc standard-JSON settings.viaIR = true (the r3/r4 named
/// Unknown) plus a same-source legacy-pipeline control. 12 selector functions
/// (6 view / 2 pure / 3 nonpayable / 1 payable) + payable receive() +
/// payable fallback(). No ERC-20-named surface (checked against the 8 known
/// selectors at planted-K time).
contract ViaIRVault {
    address private s_owner;
    uint256 private s_fee;
    uint256 private s_scale;
    bool private s_paused;
    uint256 private s_total;
    mapping(address => uint256) private s_bal;

    event Deposit(address indexed who, uint256 amount);
    event FeeSet(uint256 fee);
    event OwnershipTransferred(address indexed from, address indexed to);

    error NotOwner();
    error BadFee();

    constructor() payable {
        s_owner = msg.sender;
        s_scale = 1000000;
        s_fee = 30;
    }

    receive() external payable {
        s_bal[msg.sender] += msg.value;
        s_total += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    fallback() external payable {
        revert("ViaIRVault: no such function");
    }

    function owner() external view returns (address) {
        return s_owner;
    }

    function feeBps() external view returns (uint256) {
        return s_fee;
    }

    function scaleUnits() external view returns (uint256) {
        return s_scale;
    }

    function pausedFlag() external view returns (bool) {
        return s_paused;
    }

    function totalHeld() external view returns (uint256) {
        return s_total;
    }

    function heldBy(address a) external view returns (uint256) {
        return s_bal[a];
    }

    function computeFee(uint256 amount) external pure returns (uint256) {
        return (amount * 30) / 10000;
    }

    function halve(uint256 x) external pure returns (uint256) {
        return x / 2;
    }

    function setFee(uint256 f) external {
        if (msg.sender != s_owner) revert NotOwner();
        if (f > 1000) revert BadFee();
        s_fee = f;
        emit FeeSet(f);
    }

    function depositFor(address a) external payable {
        s_bal[a] += msg.value;
        s_total += msg.value;
        emit Deposit(a, msg.value);
    }

    function pauseSwitch(bool p) external {
        if (msg.sender != s_owner) revert NotOwner();
        s_paused = p;
    }

    function transferOwnership(address n) external {
        if (msg.sender != s_owner) revert NotOwner();
        emit OwnershipTransferred(s_owner, n);
        s_owner = n;
    }
}
