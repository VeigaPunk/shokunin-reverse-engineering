// SPDX-License-Identifier: MIT
pragma solidity =0.8.37;

// CarrierB — arc3-loop1-round3 C1 non-ERC-20-shaped carrier (seat EX-05).
// Shape planted deliberately:
//   * payable receive() + payable fallback() — neither carries a selector,
//     and both change the runtime prologue (CALLDATASIZE branch);
//   * mixed mutability: view getters, a pure function, a payable function,
//     nonpayable mutators;
//   * internal-library-bound arithmetic (Ledger) — inlined under the optimizer.
// External surface (planted K = 8 selectors, all account-level ABI functions):
//   owner(), tally(), credit(address), tag(), rate(uint256),
//   fund(uint256), sweep(address,uint256), note(bytes32,uint256)

library Ledger {
    function plus(uint256 a, uint256 b) internal pure returns (uint256) {
        unchecked {
            return a + b;
        }
    }

    function minus(uint256 a, uint256 b) internal pure returns (uint256) {
        require(a >= b, "Ledger: underflow");
        unchecked {
            return a - b;
        }
    }

    function scaled(uint256 units, uint256 rate_) internal pure returns (uint256) {
        unchecked {
            return units * rate_;
        }
    }
}

contract CarrierB {
    using Ledger for uint256;

    address public owner;
    uint256 public tally;
    mapping(address => uint256) public credit;

    bytes32 private _tag;
    uint256 private constant RATE = 3;

    event Funded(address indexed who, uint256 amount);
    event Swept(address indexed to, uint256 amount);
    event Noted(bytes32 indexed key, uint256 value);
    event FellBack(address indexed who, uint256 value, bytes data);

    constructor(bytes32 tag_) payable {
        owner = msg.sender;
        _tag = tag_;
    }

    receive() external payable {
        credit[msg.sender] = credit[msg.sender].plus(msg.value);
        tally = tally.plus(msg.value);
        emit Funded(msg.sender, msg.value);
    }

    fallback() external payable {
        emit FellBack(msg.sender, msg.value, msg.data);
    }

    function tag() external view returns (bytes32) {
        return _tag;
    }

    function rate(uint256 units) external pure returns (uint256) {
        return units.scaled(RATE);
    }

    function fund(uint256 amount) external payable {
        require(msg.value == amount, "CarrierB: value mismatch");
        credit[msg.sender] = credit[msg.sender].plus(amount);
        tally = tally.plus(amount);
        emit Funded(msg.sender, amount);
    }

    function sweep(address to, uint256 amount) external {
        require(msg.sender == owner, "CarrierB: not owner");
        credit[msg.sender] = credit[msg.sender].minus(amount);
        (bool ok, ) = payable(to).call{value: amount}("");
        require(ok, "CarrierB: send failed");
        tally = tally.minus(amount);
        emit Swept(to, amount);
    }

    function note(bytes32 key, uint256 value) external {
        emit Noted(key, value);
    }
}