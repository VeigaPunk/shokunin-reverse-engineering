# pragma version ^0.4.0
# @license MIT
"""
CarrierV — arc3-loop1-round4 C1 Vyper leg (EX-04).

Non-ERC-20 dispatch shape: a payable vault with mixed mutability
(5 public getters + payable/nonpayable/view/pure externals) and a
payable `__default__`. Deliberately carries zero ERC-20 selectors so
the recovered selector set is a clean K/K test against Vyper's own
ABI-derived set. Source of the pinned bytes is this file only.
"""

event Deposited:
    who: indexed(address)
    amount: uint256

owner: public(address)
total_deposits: public(uint256)
fee_bps: public(uint256)
paused: public(bool)
balances: public(HashMap[address, uint256])

@deploy
@payable
def __init__():
    self.owner = msg.sender

@external
@payable
def __default__():
    self.total_deposits += msg.value

@external
@payable
def deposit():
    assert not self.paused, "paused"
    self.balances[msg.sender] += msg.value
    self.total_deposits += msg.value
    log Deposited(who=msg.sender, amount=msg.value)

@external
def withdraw(amount: uint256):
    assert amount <= self.balances[msg.sender], "insufficient"
    self.balances[msg.sender] -= amount
    self.total_deposits -= amount
    send(msg.sender, amount)

@external
def set_fee(bps: uint256):
    assert msg.sender == self.owner, "not owner"
    assert bps <= 1000, "fee too high"
    self.fee_bps = bps

@external
@view
def fee_on(amount: uint256) -> uint256:
    return amount * self.fee_bps // 10000

@external
@pure
def fee_of(amount: uint256, bps: uint256) -> uint256:
    return amount * bps // 10000

@external
def pause():
    assert msg.sender == self.owner, "not owner"
    self.paused = True

@external
def unpause():
    assert msg.sender == self.owner, "not owner"
    self.paused = False

@external
@view
def balance_of(who: address) -> uint256:
    return self.balances[who]

@external
@view
def is_owner(who: address) -> bool:
    return who == self.owner

@external
@view
def fee_quote(amount: uint256) -> uint256:
    return amount * self.fee_bps // 10000
