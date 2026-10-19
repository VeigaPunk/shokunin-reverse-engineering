# @version ^0.4.0
# CR-1 decoy carrier: revert strings (PUSH32 revert-data words) + assert paths.

@external
@view
def local_a(x: uint256) -> uint256:
    assert x > 0, "must be positive"
    return x + 1

@external
@view
def local_b(x: uint256) -> uint256:
    if x == 0:
        raise "zero not allowed"
    return x + 2
