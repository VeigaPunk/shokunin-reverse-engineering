# @version ^0.4.0
# CR-1 decoy carrier: embedded FOREIGN selector literal via raw_call.
# a9059cbb = transfer(address,uint256) — a selector this contract does NOT dispatch.

@external
@view
def local_a(x: uint256) -> uint256:
    return x + 1

@external
@view
def local_b(x: uint256) -> uint256:
    return x + 2

@external
def poke(t: address) -> bool:
    raw_call(t, b"\xa9\x05\x9c\xbb", max_outsize=0)
    return True
