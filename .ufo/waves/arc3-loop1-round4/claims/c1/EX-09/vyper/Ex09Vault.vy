# pragma version ^0.4.0
# @license MIT
"""
Ex09Vault — EX-09 (arc3-loop1-round4, c1 controls) minimal Vyper carrier.

Purpose: produce Vyper-emitted *creation* (deploy) and *runtime* bytecode so
that inspect-evm-interface can be probed on both envelopes. Non-ERC-20 dispatch
shape, mixed mutability, payable __default__, and a constructor that writes
storage (so the initcode is non-trivial and the runtime begins after it).
"""

event Stored:
    who: indexed(address)
    amount: uint256

owner: public(address)
total: public(uint256)
paused: public(bool)

@deploy
@payable
def __init__():
    self.owner = msg.sender
    self.total = 0

@external
@payable
def __default__():
    self.total += msg.value

@external
@payable
def deposit():
    assert not self.paused, "paused"
    self.total += msg.value
    log Stored(who=msg.sender, amount=msg.value)

@external
def set_paused(p: bool):
    assert msg.sender == self.owner, "owner only"
    self.paused = p

@external
@view
def get_total() -> uint256:
    return self.total

@external
@pure
def scale(x: uint256) -> uint256:
    return x * 7
