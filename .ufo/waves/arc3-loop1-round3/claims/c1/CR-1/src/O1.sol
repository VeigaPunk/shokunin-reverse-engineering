// CR-1 adversarial carrier O1: optimizer-enabled ERC-20 + error/event ABI entries + receive()
pragma solidity ^0.8.0;

contract Cr1OptToken {
    string public name = "Cr1Opt";
    string public symbol = "CR1";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    error InsufficientBalance(address who, uint256 have, uint256 want);
    error Unauthorized();

    constructor(uint256 initial) {
        totalSupply = initial;
        balanceOf[msg.sender] = initial;
    }

    receive() external payable {}

    function transfer(address to, uint256 value) external returns (bool) {
        _move(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        uint256 a = allowance[from][msg.sender];
        if (a != type(uint256).max) {
            if (a < value) revert Unauthorized();
            allowance[from][msg.sender] = a - value;
        }
        _move(from, to, value);
        return true;
    }

    function mint(address to, uint256 value) external {
        if (msg.sender != address(0xdead)) revert Unauthorized();
        totalSupply += value;
        balanceOf[to] += value;
        emit Transfer(address(0), to, value);
    }

    function burn(uint256 value) external {
        uint256 b = balanceOf[msg.sender];
        if (b < value) revert InsufficientBalance(msg.sender, b, value);
        balanceOf[msg.sender] = b - value;
        totalSupply -= value;
        emit Transfer(msg.sender, address(0), value);
    }

    function _move(address from, address to, uint256 value) internal {
        uint256 b = balanceOf[from];
        if (b < value) revert InsufficientBalance(from, b, value);
        balanceOf[from] = b - value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
    }
}