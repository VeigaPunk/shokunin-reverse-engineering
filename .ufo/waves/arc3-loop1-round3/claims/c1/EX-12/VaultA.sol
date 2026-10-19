// SPDX-License-Identifier: MIT
pragma solidity 0.8.37;

contract VaultA {
    address public owner;
    uint256 public fee;
    mapping(address => uint256) public balances;

    event Deposited(address indexed who, uint256 amount);

    constructor() {
        owner = msg.sender;
        fee = 3;
    }

    function deposit() external payable {
        require(msg.value > fee, "fee");
        balances[msg.sender] += msg.value - fee;
        emit Deposited(msg.sender, msg.value);
    }

    function setFee(uint256 fee_) external {
        require(msg.sender == owner, "owner");
        fee = fee_;
    }

    function quote(uint256 amount) external view returns (uint256 net) {
        net = amount > fee ? amount - fee : 0;
    }

    function sweep(address payable to) external {
        require(msg.sender == owner, "owner");
        (bool ok, ) = to.call{value: address(this).balance}("");
        require(ok, "sweep");
    }

    receive() external payable {}

    fallback() external payable {}
}
