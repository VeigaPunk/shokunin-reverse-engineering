// SPDX-License-Identifier: MIT
pragma solidity =0.8.37;

// CarrierBErr — ATTACK variant of CarrierB (seat EX-05, chain c1).
// Not carrier B; a falsification carrier for the same probe.
// Delta vs CarrierB.sol, exactly two things:
//   1. two custom errors are declared and used -> their 4-byte selectors are
//      emitted as code constants in the optimized runtime, so a naive
//      "PUSH4 sweep" extractor should report them as functions (false
//      positives). The planted function set stays K = 8;
//   2. no `receive()` — only a payable `fallback()` -> the CALLDATASIZE==0
//      branch shape differs from CarrierB's (prologue delta leg).

error NotOwner(address caller);
error Underfunded(uint256 want, uint256 have);

library LedgerErr {
    function minus(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a < b) revert Underfunded(a, b);
        unchecked {
            return a - b;
        }
    }

    function plus(uint256 a, uint256 b) internal pure returns (uint256) {
        unchecked {
            return a + b;
        }
    }
}

contract CarrierBErr {
    using LedgerErr for uint256;

    address public owner;
    uint256 public tally;
    mapping(address => uint256) public credit;
    bytes32 private _tag;

    event Funded(address indexed who, uint256 amount);
    event Swept(address indexed to, uint256 amount);
    event Noted(bytes32 indexed key, uint256 value);
    event FellBack(address indexed who, uint256 value, bytes data);

    constructor(bytes32 tag_) payable {
        owner = msg.sender;
        _tag = tag_;
    }

    fallback() external payable {
        emit FellBack(msg.sender, msg.value, msg.data);
    }

    function tag() external view returns (bytes32) {
        return _tag;
    }

    function rate(uint256 units) external pure returns (uint256) {
        unchecked {
            return units * 3;
        }
    }

    function fund(uint256 amount) external payable {
        credit[msg.sender] = credit[msg.sender].plus(amount);
        tally = tally.plus(amount);
        emit Funded(msg.sender, amount);
    }

    function sweep(address to, uint256 amount) external {
        if (msg.sender != owner) revert NotOwner(msg.sender);
        credit[msg.sender] = credit[msg.sender].minus(amount);
        (bool ok, ) = payable(to).call{value: amount}("");
        require(ok, "CarrierBErr: send failed");
        tally = tally.minus(amount);
        emit Swept(to, amount);
    }

    function note(bytes32 key, uint256 value) external {
        emit Noted(key, value);
    }
}