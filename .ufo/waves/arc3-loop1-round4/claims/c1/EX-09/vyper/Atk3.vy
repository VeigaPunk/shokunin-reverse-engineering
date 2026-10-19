# pragma version ^0.4.0
# @license MIT
"""
Atk3 — EX-09 attack carrier (arc3-loop1-round4, c1).

Tests one hypothesis: in the Vyper 0.4.3 dispatch shape, does the extractor's
`inferred_state_mutability` default to `payable` for every function that takes
an argument? Every function here takes exactly one argument, with four
different ABI mutabilities (view / pure / nonpayable / payable).
"""

owner: public(address)
n: public(uint256)

@deploy
@payable
def __init__():
    self.owner = msg.sender

@external
@view
def a_view(x: uint256) -> uint256:
    return self.n + x

@external
@pure
def a_pure(x: uint256) -> uint256:
    return x * 3

@external
def a_nonpay(x: uint256):
    self.n = x

@external
@payable
def a_pay(x: uint256):
    self.n = x

@external
@view
def b_view(x: address, y: uint256) -> uint256:
    return y

@external
def b_nonpay(x: address, y: bool):
    self.n = convert(y, uint256)
