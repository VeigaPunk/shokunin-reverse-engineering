// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Cr1Sample {
    mapping(address => uint256) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint256 value);
    function transfer(address to, uint256 amount) external returns (bool) { balanceOf[to] += amount; emit Transfer(msg.sender, to, amount); return true; }
    function approve(address spender, uint256 amount) external returns (bool) { return true; }
    function totalSupply() external view returns (uint256) { return 1; }
    function allowance(address owner, address spender) external view returns (uint256) { return 0; }
    function decimals() external pure returns (uint8) { return 18; }
    function supportsInterface(bytes4 interfaceId) external pure returns (bool) { return interfaceId == 0x01ffc9a7 || interfaceId == 0x80ac58cd; }
}
