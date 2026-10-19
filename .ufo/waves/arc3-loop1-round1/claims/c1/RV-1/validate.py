import sys, json, hashlib, subprocess
sys.path.insert(0, '/var/tmp/rv1')
import keccak_ref as K

# inputs crossing the 136-byte rate boundary and the 272-byte 2-block boundary
inputs = [b"", b"a", b"abc", b"testing", b"transfer(address,uint256)",
          b"balanceOf(address)", b"approve(address,uint256)",
          b"x"*135, b"y"*136, b"z"*137, b"w"*271, b"v"*272, b"u"*273,
          bytes(range(256)), b"\x00", b"\xff"*200]
hexes = [i.hex() for i in inputs]

# --- oracle 1: node/OpenSSL SHA3-256 (independent implementation of the permutation)
node_js = """
const crypto = require('crypto');
const inps = JSON.parse(process.argv[1]);
console.log(JSON.stringify(inps.map(h => crypto.createHash('sha3-256').update(Buffer.from(h,'hex')).digest('hex'))));
"""
node_out = subprocess.run(['node', '-e', node_js, json.dumps(hexes)],
                          capture_output=True, text=True, check=True).stdout.strip()
node_sha3 = json.loads(node_out)

# --- oracle 2: python stdlib hashlib SHA3-256 (openssl-backed, separate binding)
py_sha3 = [hashlib.sha3_256(i).hexdigest() for i in inputs]

rows, all_ok = [], True
for inp, h, n, p in zip(inputs, hexes, node_sha3, py_sha3):
    mine = K.sha3_256(inp).hex()
    ok = (mine == n == p)
    all_ok &= ok
    rows.append({"len": len(inp), "sha3_mine": mine[:16], "sha3_node": n[:16],
                 "sha3_stdlib": p[:16], "match": ok})

print("=== A. permutation+sponge vs two independent SHA3-256 oracles ===")
for r in rows:
    print(f"  len={r['len']:>4}  mine={r['sha3_mine']}  node={r['sha3_node']}  stdlib={r['sha3_stdlib']}  {'OK' if r['match'] else 'MISMATCH'}")
print("A. ALL_SHA3_MATCH:", all_ok)

# --- B. Keccak-256 public vectors (canonical Ethereum values, independent of my code)
VECTORS = {
    "": "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
    "abc": "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45",
}
print("\n=== B. Keccak-256 public vectors ===")
b_ok = True
for msg, want in VECTORS.items():
    got = K.keccak_256(msg.encode()).hex()
    ok = got == want
    b_ok &= ok
    print(f"  keccak256({msg!r}) = {got}  want {want}  {'OK' if ok else 'MISMATCH'}")
print("B. ALL_KECCAK_VECTORS_MATCH:", b_ok)

# --- C. ERC-20 selectors (cross-check vs widely published selector table)
ERCSEL = {
    "transfer(address,uint256)": "a9059cbb",
    "balanceOf(address)": "70a08231",
    "approve(address,uint256)": "095ea7b3",
    "totalSupply()": "18160ddd",
    "transferFrom(address,address,uint256)": "23b872dd",
}
print("\n=== C. ERC-20 selector table cross-check ===")
c_ok = True
for sig, want in ERCSEL.items():
    got = K.selector(sig)
    ok = got == want
    c_ok &= ok
    print(f"  {sig:<40} -> {got}  want {want}  {'OK' if ok else 'MISMATCH'}")
print("C. ALL_SELECTORS_MATCH:", c_ok)

# --- D. negative control: prove the padding byte matters (guards against a
#        false "keccak==sha3" implementation that would pass B by accident)
neq = K.keccak_256(b"").hex() != K.sha3_256(b"").hex()
print("\n=== D. negative control: keccak-256 != sha3-256 for same input ===")
print("  keccak256('')=", K.keccak_256(b"").hex()[:16], " sha3_256('')=", K.sha3_256(b"").hex()[:16], " distinct:", neq)

print("\nSUMMARY:", {"A_sha3": all_ok, "B_vectors": b_ok, "C_selectors": c_ok, "D_padding_distinct": neq})
sys.exit(0 if (all_ok and b_ok and c_ok and neq) else 1)
