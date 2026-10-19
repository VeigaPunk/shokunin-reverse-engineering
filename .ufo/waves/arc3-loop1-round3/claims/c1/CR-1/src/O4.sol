// CR-1 adversarial carrier O4: library-bound shape (public library functions get a runtime dispatch)
pragma solidity ^0.8.0;

library Cr1Lib {
    function twice(uint256 x) external pure returns (uint256) { return x * 2; }
    function thrice(uint256 x) external pure returns (uint256) { return x * 3; }
    function identity(address a) external pure returns (address) { return a; }
}

contract Cr1LibUser {
    using Cr1Lib for uint256;
    event Used(uint256 v);

    function useIt(uint256 x) external returns (uint256) {
        uint256 y = Cr1Lib.twice(x);
        emit Used(y);
        return y;
    }
}