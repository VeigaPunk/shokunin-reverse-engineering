# @version 0.4.3

@external
@view
def blob_fee() -> uint256:
    return block.blobbasefee
