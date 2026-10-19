# pragma version 0.4.3
# @license MIT
"""
StewardToken — arc3-loop1-round4, chain c1, seat EX-03 (kaidoku-shokunin).

Vyper carrier for the `inspect-evm-interface` selector-recovery leg (C1).

Shape: an ERC-20-selector-bearing token (the r1 entry's `Rv2Token` class)
carrying a steward role, a payable 1:1 wei->unit deposit, and a burn-and-send
redeem. This is the ERC-20-shaped Vyper class that EX-04's vault carrier
(`claims/c1/EX-04/src/CarrierV.vy`) deliberately omits — the chain therefore
holds both the ERC-20-present and the ERC-20-absent Vyper controls.

Mutability classes present, by design:
  payable    — `deposit`, `__default__`
  nonpayable — `transfer`, `approve`, `transferFrom`, `mint`, `set_steward`,
               `set_fee`, `pause`, `unpause`, `redeem`
  view       — the nine public getters, `preview_fee`, `is_steward`
  pure       — `fee_of`

`__default__` carries no selector (it is the Vyper fallback); every other
external is selector-bearing. Source of the pinned bytes is this file only;
no imports, no interfaces, no ERC-20 `implements:` conformance claim.
"""

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Deposited:
    who: indexed(address)
    amount: uint256

event Redeemed:
    who: indexed(address)
    amount: uint256

event StewardRotated:
    previous: indexed(address)
    next: indexed(address)

name: public(String[32])
symbol: public(String[32])
decimals: public(uint8)
totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
steward: public(address)
feeBps: public(uint256)
paused: public(bool)


@deploy
def __init__():
    self.name = "StewardToken"
    self.symbol = "STWD"
    self.decimals = 18
    self.steward = msg.sender


@external
@payable
def __default__():
    self._credit(msg.sender, msg.value)


@external
@payable
@nonreentrant
def deposit() -> uint256:
    return self._credit(msg.sender, msg.value)


@external
@nonreentrant
def redeem(_amount: uint256):
    assert not self.paused, "paused"
    assert _amount <= self.balanceOf[msg.sender], "insufficient units"
    self.balanceOf[msg.sender] -= _amount
    self.totalSupply -= _amount
    log Redeemed(who=msg.sender, amount=_amount)
    send(msg.sender, _amount)


@external
def transfer(_to: address, _value: uint256) -> bool:
    self._move(msg.sender, _to, _value)
    return True


@external
def approve(_spender: address, _value: uint256) -> bool:
    self.allowance[msg.sender][_spender] = _value
    log Approval(owner=msg.sender, spender=_spender, value=_value)
    return True


@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    self.allowance[_from][msg.sender] -= _value
    self._move(_from, _to, _value)
    return True


@external
def mint(_to: address, _amount: uint256):
    assert msg.sender == self.steward, "not steward"
    self.totalSupply += _amount
    self.balanceOf[_to] += _amount
    log Transfer(sender=empty(address), receiver=_to, value=_amount)


@external
def set_steward(_next: address):
    assert msg.sender == self.steward, "not steward"
    assert _next != empty(address), "zero steward"
    log StewardRotated(previous=self.steward, next=_next)
    self.steward = _next


@external
def set_fee(_bps: uint256):
    assert msg.sender == self.steward, "not steward"
    assert _bps <= 1000, "fee too high"
    self.feeBps = _bps


@external
def pause():
    assert msg.sender == self.steward, "not steward"
    self.paused = True


@external
def unpause():
    assert msg.sender == self.steward, "not steward"
    self.paused = False


@external
@view
def preview_fee(_amount: uint256) -> uint256:
    return _amount * self.feeBps // 10000


@external
@view
def is_steward(_who: address) -> bool:
    return _who == self.steward


@external
@pure
def fee_of(_amount: uint256, _bps: uint256) -> uint256:
    return _amount * _bps // 10000


@internal
def _credit(_who: address, _amount: uint256) -> uint256:
    assert not self.paused, "paused"
    self.totalSupply += _amount
    self.balanceOf[_who] += _amount
    log Transfer(sender=empty(address), receiver=_who, value=_amount)
    log Deposited(who=_who, amount=_amount)
    return _amount


@internal
def _move(_from: address, _to: address, _value: uint256):
    assert not self.paused, "paused"
    assert _to != empty(address), "zero receiver"
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    log Transfer(sender=_from, receiver=_to, value=_value)
