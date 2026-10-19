# pragma version 0.4.3

owner: address
paused: bool
total: uint256
fee: uint256
balances: HashMap[address, uint256]
marks: HashMap[bytes32, bool]

@deploy
def __init__():
    self.owner = msg.sender

@external
@payable
def deposit():
    assert not self.paused, "paused"
    self.balances[msg.sender] += msg.value
    self.total += msg.value

@external
def withdraw(amount: uint256):
    assert not self.paused, "paused"
    assert self.balances[msg.sender] >= amount, "short"
    self.balances[msg.sender] -= amount
    self.total -= amount
    send(msg.sender, amount)

@external
def sweep(to: address):
    assert msg.sender == self.owner, "auth"
    send(to, self.balance)

@external
def pause():
    assert msg.sender == self.owner, "auth"
    self.paused = True

@external
def unpause():
    assert msg.sender == self.owner, "auth"
    self.paused = False

@external
def set_fee(bps: uint256):
    assert msg.sender == self.owner, "auth"
    assert bps <= 10000, "range"
    self.fee = bps

@external
def mark(k: bytes32):
    self.marks[k] = True

@external
@view
def read_total() -> uint256:
    return self.total

@external
@view
def read_fee() -> uint256:
    return self.fee

@external
@view
def read_balance(who: address) -> uint256:
    return self.balances[who]

@external
@view
def is_marked(k: bytes32) -> bool:
    return self.marks[k]

@external
@view
def digest_of(k: bytes32) -> bytes32:
    return keccak256(concat(k, convert(chain.id, bytes32)))

@external
@pure
def scale(x: uint256, n: uint256) -> uint256:
    assert n < 256, "range"
    return (x << n) | (x >> (256 - n))
