// SPDX-License-Identifier: MIT
pragma solidity 0.8.37;

library HarborLib {
    function scale(uint256 x, uint256 f) external pure returns (uint256) {
        return x * f;
    }

    function tag() external pure returns (bytes32) {
        return keccak256("harbor-bound");
    }
}

contract HarborBound {
    error Unauthorized();
    error TooDeep(uint256 given, uint256 cap);

    event Anchored(address indexed who, uint256 depth);
    event Donated(address indexed who, uint256 amount);

    uint256 public depth;
    uint256 private immutable _limit;
    address public immutable keeper;

    constructor(uint256 limit_) {
        _limit = limit_;
        keeper = msg.sender;
    }

    function limit() external view returns (uint256) {
        return _limit;
    }

    function anchor(uint256 d) external {
        if (msg.sender != keeper) revert Unauthorized();
        depth = d;
        emit Anchored(msg.sender, d);
    }

    function survey(uint256 x) external view returns (uint256) {
        if (x > _limit) revert TooDeep(x, _limit);
        return HarborLib.scale(x, depth + 1);
    }

    function beacon() external pure returns (bytes32) {
        return HarborLib.tag();
    }

    function donate() external payable {
        if (msg.value == 0) revert Unauthorized();
        emit Donated(msg.sender, msg.value);
    }

    function sweep(address to) external {
        if (msg.sender != keeper) revert Unauthorized();
        (bool ok, ) = to.call{value: address(this).balance}("");
        if (!ok) revert Unauthorized();
    }

    receive() external payable {
        depth += 1;
    }

    fallback() external payable {
        emit Donated(msg.sender, msg.value);
    }
}