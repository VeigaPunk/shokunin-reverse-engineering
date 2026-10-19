# @version ^0.4.0
# CR-1 decoy carrier: selector-shaped constants as bytes4 imm data + raw_call embed.
# a9059cbb / 095ea7b3 / 2ae1431c are selector-shaped but NOT dispatched by this contract.

MAGIC: constant(bytes4) = 0xa9059cbb
OTHER: constant(bytes4) = 0x095ea7b3

@external
@view
def local_a(x: uint256) -> uint256:
    return x + convert(MAGIC, uint256)

@external
@view
def local_b(x: uint256) -> uint256:
    return x + convert(OTHER, uint256)

@external
def relay(t: address):
    raw_call(t, slice(convert(MAGIC, bytes32), 0, 4), max_outsize=0)
