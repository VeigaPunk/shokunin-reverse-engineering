// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// EX-6 independent verification carrier (arc3-loop1-round6).
/// Deliberately different function names/arity/mutability mix from EX-7's
/// ViaIrVault, so a dispatcher-shape match cannot be a carrier artifact.
/// variant with fallback(): 10 externals + receive() + fallback().
contract RelayDeskFb {
    address private admin_;
    uint256 private head_;
    uint256 private cap_;
    bool private live_;
    mapping(address => uint256) private credit_;
    mapping(uint64 => bytes32) private slots_;

    constructor() {
        admin_ = msg.sender;
        live_ = true;
    }

    receive() external payable {
        credit_[msg.sender] += msg.value;
    }

    fallback(bytes calldata payload) external payable returns (bytes memory) {
        require(live_, "off");
        emit Poked(payload.length, msg.value);
        return payload;
    }

    event Poked(uint256 indexed size, uint256 value);

    function fund(uint64 slot, bytes32 payload) external payable {
        require(live_, "off");
        slots_[slot] = payload;
        head_ += 1;
    }

    function crank(uint256 delta) external {
        require(msg.sender == admin_, "auth");
        require(delta <= cap_, "cap");
        head_ += delta;
    }

    function setCap(uint256 next) external {
        require(msg.sender == admin_, "auth");
        cap_ = next;
    }

    function halt() external {
        require(msg.sender == admin_, "auth");
        live_ = false;
    }

    function resume() external {
        require(msg.sender == admin_, "auth");
        live_ = true;
    }

    function readHead() external view returns (uint256) {
        return head_;
    }

    function readCap() external view returns (uint256) {
        return cap_;
    }

    function readCredit(address who) external view returns (uint256) {
        return credit_[who];
    }

    function readSlot(uint64 slot) external view returns (bytes32) {
        return slots_[slot];
    }

    function probe(uint64 slot) external view returns (bytes32, uint256) {
        return (slots_[slot], block.timestamp);
    }
}
