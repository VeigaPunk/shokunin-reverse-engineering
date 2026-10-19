// CR-1 adversarial carrier O3: optimizer dedup pressure + overloads + ABI/non-dispatch mix
pragma solidity ^0.8.0;

interface ICr1 {
    function ping() external view returns (uint256);
    function pong() external view returns (uint256);
}

contract Cr1Dedup is ICr1 {
    uint256 public constant K = 7;
    error Cr1Err(uint256);

    // identical bodies: optimizer may merge targets
    function ping() external pure returns (uint256) { return 7; }
    function pong() external pure returns (uint256) { return 7; }

    // overload pair: two distinct selectors, same name
    function set(uint256 v) external {}
    function set(uint8 v) external {}

    // payable + view + nonpayable mix
    function pay() external payable returns (uint256) { return msg.value; }
    function view7() external view returns (uint256) { return K; }
    function boom() external pure { revert Cr1Err(7); }
}