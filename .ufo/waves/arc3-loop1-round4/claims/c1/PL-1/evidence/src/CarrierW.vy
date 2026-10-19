# pragma version ^0.4.0
# @license MIT
"""
CarrierW — arc3-loop1-round4 PL-1 planner pre-measurement carrier (chain c1).

Second Vyper carrier design, structurally independent of EX-04's CarrierV:
  * six selective externals spanning all four mutability classes
  * a payable `__default__` (the Vyper fallback — the pseudo-entry hazard)
  * a constructor WITH an argument (ABI constructor entry carries no selector)
  * canonicalization probes in the signature set: a fixed array (`uint256[2]`),
    a dynamic bytes (`Bytes[32]` -> `bytes`) and a string (`String[32]` ->
    `string`), so the keccak canonical-form rule is exercised, not assumed
  * deliberately zero ERC-20 selectors

This file is the pre-measurement prototype for the plan; it is NOT a claim
carrier. Byte-exactness is claimed only for the bytes compiled from this text.
"""

owner: public(address)
seen: public(HashMap[address, uint256])
last_tag: public(String[32])
threshold: public(uint256)

@deploy
@payable
def __init__(start_threshold: uint256):
    self.owner = msg.sender
    self.threshold = start_threshold

@external
@payable
def __default__():
    self.seen[msg.sender] += msg.value

@external
@payable
def stake():
    self.seen[msg.sender] += msg.value

@external
def bump(by: uint256):
    assert msg.sender == self.owner, "not owner"
    self.threshold += by

@external
@view
def quote(amount: uint256) -> uint256:
    return amount * self.threshold // 10000

@external
@pure
def scale(amount: uint256, factor: uint256) -> uint256:
    return amount * factor

@external
def tag(name: String[32], payload: Bytes[32], pair: uint256[2], flag: bool):
    assert msg.sender == self.owner, "not owner"
    self.last_tag = name
