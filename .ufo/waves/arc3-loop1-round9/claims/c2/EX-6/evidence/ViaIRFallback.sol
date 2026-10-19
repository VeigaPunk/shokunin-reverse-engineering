// SPDX-License-Identifier: MIT
pragma solidity 0.8.37;

contract ViaIRFallback {
    uint256 private saved;

    receive() external payable {
        saved += msg.value;
    }

    fallback() external payable {
        saved = uint256(keccak256(msg.data)) + msg.value;
    }

    function alpha() external pure returns (uint256) {
        return 17;
    }

    function store(uint256 value) external payable returns (uint256) {
        saved = value + msg.value;
        return saved;
    }

    function load() external view returns (uint256) {
        return saved;
    }
}
