# @version ^0.4.0
# CR-1 arc3-r6 guard-byte probe carrier

@external
@payable
def pay(x: uint256) -> uint256:
    return x + 1

@external
@view
def look(x: uint256) -> uint256:
    return x + 2
