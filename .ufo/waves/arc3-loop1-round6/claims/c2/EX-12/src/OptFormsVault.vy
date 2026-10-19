# pragma version ^0.4.0
# @license MIT
"""
OptFormsVault — seat EX-12 (arc3-loop1-round6, c2 chain).

Independent Vyper 0.4.3 carrier for byte-characterizing the non-default
optimizer forms named as an Unknown in
corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28:
`--no-optimize`, `-O none`, `-O codesize` (plus the default `-O gas`
baseline on the same source).

Function set deliberately differs from r4's CarrierV (13 ABI functions,
5 public getters + 8 explicit externals, one payable default, zero ERC-20
selectors) so the selector set and bucket count are independent.
"""

owner: public(address)
count: public(uint256)
fee: public(uint256)
active: public(bool)
ledger: public(HashMap[address, uint256])

@deploy
def __init__():
    self.owner = msg.sender

@external
@payable
def __default__():
    self.count += 1

@external
@payable
def top_up():
    self.ledger[msg.sender] += msg.value
    self.count += 1

@external
def take(amount: uint256):
    assert self.ledger[msg.sender] >= amount, "short"
    self.ledger[msg.sender] -= amount
    self.count -= 1
    send(msg.sender, amount)

@external
def set_fee(bps: uint256):
    assert msg.sender == self.owner, "auth"
    assert bps <= 5000, "range"
    self.fee = bps

@external
def flip():
    assert msg.sender == self.owner, "auth"
    self.active = not self.active

@external
@view
def ledger_of(who: address) -> uint256:
    return self.ledger[who]

@external
@view
def fee_on(amount: uint256) -> uint256:
    return amount * self.fee // 10000

@external
@view
def owner_is(who: address) -> bool:
    return who == self.owner

@external
@pure
def bump(x: uint256) -> uint256:
    return x + 1
