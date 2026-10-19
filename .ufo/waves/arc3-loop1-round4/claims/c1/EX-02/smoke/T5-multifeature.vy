# @version ^0.4.0

struct P:
    a: uint256
    b: address

paused: public(bool)

event Log:
    who: indexed(address)
    val: uint256

@deploy
def __init__():
    self.paused = False

@external
def setPaused(v: bool) -> bool:
    self.paused = v
    log Log(msg.sender, 7)
    return self.paused

@external
@payable
def deposit() -> uint256:
    return msg.value
