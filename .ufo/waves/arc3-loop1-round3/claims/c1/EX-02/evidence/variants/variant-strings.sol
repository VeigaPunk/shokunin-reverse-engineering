// SPDX-License-Identifier: MIT
// CarrierA — arc3-loop1-round3 c1/EX-02 (kaidoku-shokunin).
// Role: optimizer-enabled (`--optimize --optimize-runs 200`) dispatch-shape
// carrier for the inspect-evm-interface leg. Non-ERC-20 shape: payable receive
// + payable fallback, mixed mutability (payable/nonpayable/view/pure),
// custom-error revert paths (non-dispatch PUSH4 constants in code).
pragma solidity 0.8.37;

contract CarrierA {
    address public owner;
    uint256 public totalCredited;
    mapping(address => uint256) private _creditOf;

    event Credited(address indexed who, uint256 amount);
    event Swept(address indexed to, uint256 amount);

    error NotOwner();
    error Insufficient(uint256 available, uint256 wanted);

    constructor() payable {
        owner = msg.sender;
    }

    receive() external payable {
        _credit(msg.sender, msg.value);
    }

    fallback() external payable {
        _credit(msg.sender, msg.value);
    }

    function deposit() external payable {
        _credit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        uint256 held = _creditOf[msg.sender];
        if (amount > held) revert Insufficient(held, amount);
        _creditOf[msg.sender] = held - amount;
        totalCredited -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "ZZZ");
    }

    function creditOf(address who) external view returns (uint256) {
        return _creditOf[who];
    }

    function isSolvent() external view returns (bool) {
        return address(this).balance >= totalCredited;
    }

    function sweep(address payable to) external returns (uint256 amount) {
        if (msg.sender != owner) revert NotOwner();
        amount = address(this).balance;
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "ZZZ");
        emit Swept(to, amount);
    }

    function rotate(address next) external {
        if (msg.sender != owner) revert NotOwner();
        owner = next;
    }

    function stamp() external pure returns (bytes4) {
        return 0xca11ab1e;
    }

    function _credit(address who, uint256 amount) private {
        _creditOf[who] += amount;
        totalCredited += amount;
        emit Credited(who, amount);
    }
}