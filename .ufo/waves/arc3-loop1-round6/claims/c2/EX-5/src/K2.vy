# @version ^0.4.0
# EX-5 round6: K=2 codesize-fallback probe

@external
@payable
def pay(x: uint256) -> uint256:
    return x + 1

@external
@view
def look(x: uint256) -> uint256:
    return x + 2
