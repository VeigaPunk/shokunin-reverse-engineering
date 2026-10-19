// CR-1 adversarial carrier O5: 24 external functions (binary-search dispatch pressure)
pragma solidity ^0.8.0;

contract Cr1Big {
    uint256 public slot;
    error BigErr(uint256);
    event Pinged(uint256 indexed n);

    function f00(uint256 x) external returns (uint256) { slot = x; return x + 0; }
    function f01(uint256 x) external view returns (uint256) { return slot + 1; }
    function f02(uint256 x) external pure returns (uint256) { return 2; }  // identical body across the pure set
    function f03(uint256 x) external payable { slot += x; emit Pinged(3); }
    function f04(uint256 x) external returns (uint256) { slot = x; return x + 4; }
    function f05(uint256 x) external view returns (uint256) { return slot + 5; }
    function f06(uint256 x) external pure returns (uint256) { return 6; }  // identical body across the pure set
    function f07(uint256 x) external payable { slot += x; emit Pinged(7); }
    function f08(uint256 x) external returns (uint256) { slot = x; return x + 8; }
    function f09(uint256 x) external view returns (uint256) { return slot + 9; }
    function f10(uint256 x) external pure returns (uint256) { return 10; }  // identical body across the pure set
    function f11(uint256 x) external payable { slot += x; emit Pinged(11); }
    function f12(uint256 x) external returns (uint256) { slot = x; return x + 12; }
    function f13(uint256 x) external view returns (uint256) { return slot + 13; }
    function f14(uint256 x) external pure returns (uint256) { return 14; }  // identical body across the pure set
    function f15(uint256 x) external payable { slot += x; emit Pinged(15); }
    function f16(uint256 x) external returns (uint256) { slot = x; return x + 16; }
    function f17(uint256 x) external view returns (uint256) { return slot + 17; }
    function f18(uint256 x) external pure returns (uint256) { return 18; }  // identical body across the pure set
    function f19(uint256 x) external payable { slot += x; emit Pinged(19); }
    function f20(uint256 x) external returns (uint256) { slot = x; return x + 20; }
    function f21(uint256 x) external view returns (uint256) { return slot + 21; }
    function f22(uint256 x) external pure returns (uint256) { return 22; }  // identical body across the pure set
    function f23(uint256 x) external payable { slot += x; emit Pinged(23); }
}
