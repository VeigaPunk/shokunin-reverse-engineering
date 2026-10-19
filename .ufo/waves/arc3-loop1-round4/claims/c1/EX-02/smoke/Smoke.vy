# @version ^0.4.0
# kaidoku-shokunin arc3-loop1-round4 EX-02 installer smoke carrier.
# Deliberately minimal: one constructor, one mutating external, one view,
# two public storage getters -> 4 ABI-derived selectors for the K set.

owner: public(address)
counter: public(uint256)

@deploy
def __init__():
    self.owner = msg.sender

@external
def increment() -> uint256:
    self.counter += 1
    return self.counter

@external
@view
def get() -> uint256:
    return self.counter
