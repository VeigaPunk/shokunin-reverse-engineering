// SPDX-License-Identifier: MIT
pragma solidity ^0.8.37;

/// VaultB — carrier B for the arc3 c1 EVM leg: a non-ERC-20 shaped 2-of-3
/// multisig vault. Mixed mutability surface: view / pure / nonpayable /
/// payable (deposit + receive). No ERC-20 selector is present by construction.
contract VaultB {
    address[3] private _owners;
    uint256 private _threshold;
    mapping(bytes32 => uint256) private _confirmations;

    event Deposited(address indexed from, uint256 amount);
    event Submitted(bytes32 indexed txHash, address indexed by);
    event Confirmed(bytes32 indexed txHash, address indexed by);
    event Executed(bytes32 indexed txHash, address indexed to, uint256 value);
    event ThresholdChanged(uint256 threshold);

    constructor(address[3] memory owners_, uint256 threshold_) {
        _owners = owners_;
        require(threshold_ > 0 && threshold_ <= 3, "bad threshold");
        _threshold = threshold_;
    }

    function isOwner(address who) public view returns (bool) {
        return who == _owners[0] || who == _owners[1] || who == _owners[2];
    }

    function ownerCount() external view returns (uint256) {
        return 3;
    }

    function threshold() external view returns (uint256) {
        return _threshold;
    }

    function vaultBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function confirmationCount(bytes32 txHash) external view returns (uint256) {
        return _confirmations[txHash];
    }

    function computeTxHash(address to, uint256 value, bytes32 payloadHash, uint256 nonce)
        external
        pure
        returns (bytes32)
    {
        return _hashTx(to, value, payloadHash, nonce);
    }

    function submit(bytes32 txHash) external {
        require(isOwner(msg.sender), "not owner");
        emit Submitted(txHash, msg.sender);
    }

    function confirm(bytes32 txHash) external {
        require(isOwner(msg.sender), "not owner");
        _confirmations[txHash] += 1;
        emit Confirmed(txHash, msg.sender);
    }

    function execute(address to, uint256 value, bytes32 payloadHash, uint256 nonce) external {
        require(isOwner(msg.sender), "not owner");
        bytes32 txHash = _hashTx(to, value, payloadHash, nonce);
        require(_confirmations[txHash] >= _threshold, "not confirmed");
        require(value <= address(this).balance, "insufficient");
        _confirmations[txHash] = 0;
        (bool ok, ) = to.call{value: value}("");
        require(ok, "call failed");
        emit Executed(txHash, to, value);
    }

    function setThreshold(uint256 newThreshold) external {
        require(isOwner(msg.sender), "not owner");
        require(newThreshold > 0 && newThreshold <= 3, "bad threshold");
        _threshold = newThreshold;
        emit ThresholdChanged(newThreshold);
    }

    function deposit() external payable {
        emit Deposited(msg.sender, msg.value);
    }

    receive() external payable {
        emit Deposited(msg.sender, msg.value);
    }

    function _hashTx(address to, uint256 value, bytes32 payloadHash, uint256 nonce)
        internal
        pure
        returns (bytes32)
    {
        return keccak256(abi.encodePacked(to, value, payloadHash, nonce));
    }
}