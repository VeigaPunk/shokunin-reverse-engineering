# @version 0.4.3

@external
@view
def blob_hash(index: uint256) -> bytes32:
    return blobhash(index)

@external
@view
def blob_fee() -> uint256:
    return block.blobbasefee

@external
@view
def marker() -> uint256:
    return block.number
