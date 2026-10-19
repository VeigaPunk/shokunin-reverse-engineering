// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library MmMath {
    function mulDiv(uint256 x, uint256 y, uint256 d) internal pure returns (uint256) {
        return (x * y) / d;
    }
}

contract MutMix {
    uint256 private _acc;
    address private _who;

    function poke() external pure returns (uint256) {
        return 7;
    }

    function viewAcc() external view returns (uint256) {
        return _acc;
    }

    function setAcc(uint256 a) external {
        _acc = a;
    }

    function scaleAcc(uint256 x, uint256 y) external returns (uint256) {
        _acc = MmMath.mulDiv(_acc, x, y);
        return _acc;
    }

    function pay() external payable {
        _who = msg.sender;
    }

    function who() external view returns (address) {
        return _who;
    }
}