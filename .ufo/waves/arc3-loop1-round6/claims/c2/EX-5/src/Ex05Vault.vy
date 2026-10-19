# @version ^0.4.0
# EX-5 round6 independent carrier: 7 functions, mixed mutability, 4 arg-taking / 3 zero-arg.

@external
@view
def alpha(x: uint256) -> uint256:
    return x + 1

@external
@pure
def beta(x: uint256) -> uint256:
    return x * 2

@external
def gamma(x: uint256) -> uint256:
    return x - 1

@external
@payable
def delta(x: uint256) -> uint256:
    return x + 3

@external
@view
def epsilon() -> uint256:
    return 5

@external
def zeta() -> uint256:
    return 6

@external
@payable
def eta() -> uint256:
    return 7
