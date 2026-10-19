// CR-1 adversarial carrier O2: non-ERC-20 shape (payable receive/fallback, mixed mutability)
pragma solidity ^0.8.0;

contract Cr1Vault {
    address public owner;
    uint256 public stored;
    mapping(bytes4 => uint256) public counters;

    event Deposited(address indexed who, uint256 amount, bytes4 indexed sig);
    error NotOwner();

    constructor() payable {
        owner = msg.sender;
    }

    receive() external payable {
        stored += msg.value;
        emit Deposited(msg.sender, msg.value, msg.sig);
    }

    fallback() external payable {
        counters[msg.sig] += 1;
    }

    function deposit() external payable {
        stored += msg.value;
        emit Deposited(msg.sender, msg.value, msg.sig);
    }

    function withdraw(uint256 amount) external {
        if (msg.sender != owner) revert NotOwner();
        stored -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "xfer");
    }

    function peek() external view returns (uint256) {
        return stored;
    }

    function tag() external pure returns (string memory) {
        return "cr1";
    }

    function setStored(uint256 v) external {
        stored = v;
    }

    function hits(bytes4 sig) external view returns (uint256) {
        return counters[sig];
    }
}