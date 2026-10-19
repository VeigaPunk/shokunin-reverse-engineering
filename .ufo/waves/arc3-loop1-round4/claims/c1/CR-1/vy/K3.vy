# @version ^0.4.0
# CR-1 round4 adversarial Vyper carriers

@external
@view
def f0(x: uint256) -> uint256:
    return x + 1

@external
@view
def f1(x: uint256) -> uint256:
    return x + 2

@external
@view
def f2(x: uint256) -> uint256:
    return x + 3

