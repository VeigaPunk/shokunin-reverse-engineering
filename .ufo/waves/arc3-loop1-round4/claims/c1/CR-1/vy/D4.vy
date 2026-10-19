# @version ^0.4.0
# CR-1 shape carrier: payable receive + fallback + mixed mutability (Vyper analogue of solc CarrierB).

owner: public(address)
paused: public(bool)

@deploy
def __init__():
    self.owner = msg.sender

@external
@payable
def deposit() -> uint256:
    return self.balance

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
def isPaused() -> bool:
    return self.paused
