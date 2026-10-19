#!/usr/bin/env python3
"""EX-03 (arc3-loop1-round4, chain c1) — Vyper dispatcher decoder + K/K derivation.

Decodes the Vyper 0.4.3 runtime dispatcher from bytes alone and derives the
independent selector set (K) from the ABI with keccak-256, so the recovered set
can be compared K/K without trusting `method_identifiers`.

Vyper 0.4.3 prologue (measured on two independently authored carriers,
`token.vy` here and EX-04's `CarrierV.vy`):

    PUSH0 CALLDATALOAD PUSH1 0x01 SHR PUSH1 0x02 PUSH1 <N> DUP3 MOD
    PUSH1 0x01 SHL PUSH2 <table_off> ADD PUSH1 <len> CODECOPY PUSH0 MLOAD JUMP
    <N x 2-byte big-endian jump targets>          <- table, ends at runtime end
    ...
    <target> 5b 63 <sel4> DUP2 XOR PUSH2 <next> JUMPI   <- collision chain
    <target> 5b 5b 33 60 40 52 ...                      <- shared fallback body

Slot for selector `s` is `int(s) % N`. A slot's target heads a collision chain
of inline `JUMPDEST PUSH4 <sel4>` sites linked by `PUSH2 <next> JUMPI`; the
match branch jumps to the shared body entry, the exhaust branch to the next
chain member, and a chain that runs out reaches the fallback at `0x0a33`.

Usage: python3 decode-vyper-dispatch.py <runtime.hex> <abi.json> <method-identifiers.json>
"""
import json
import re
import sys
import hashlib
from collections import Counter

# --- keccak-256 (pure python, Keccak padding 0x01..0x80, rate 136) -----------
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
       [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
MASK = (1 << 64) - 1


def _rotl(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & MASK


def _keccak_f(a):
    for rc in RC:
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x + 4) % 5] ^ _rotl(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rotl(a[x + 5 * y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y] & MASK) & b[(x + 2) % 5 + 5 * y])
        a[0] ^= rc
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
    a = [0] * 25
    pad = bytearray(((len(data) + rate) // rate) * rate)
    pad[: len(data)] = data
    pad[len(data)] = 0x01
    pad[-1] |= 0x80
    for off in range(0, len(pad), rate):
        for i in range(rate // 8):
            a[i] ^= int.from_bytes(pad[off + i * 8: off + i * 8 + 8], "little")
        _keccak_f(a)
    return b"".join(a[i].to_bytes(8, "little") for i in range(4))


def canonical_type(inp):
    t = inp.get("type", "")
    if t.startswith("tuple"):
        return "(" + ",".join(canonical_type(c) for c in inp.get("components", [])) + ")" + t[5:]
    return t


def main():
    rt_path, abi_path, mi_path = sys.argv[1], sys.argv[2], sys.argv[3]
    raw = open(rt_path).read().strip()
    b = bytes.fromhex(raw[2:] if raw.startswith("0x") else raw)
    abi = json.load(open(abi_path))
    mi = json.load(open(mi_path))

    print(f"# runtime: {rt_path}")
    print(f"# runtime sha256: {hashlib.sha256(b).hexdigest()}")
    print(f"# runtime bytes: {len(b)}")

    # --- self-test the local keccak against Ethereum's own vectors -----------
    assert keccak256(b"").hex() == \
        "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470", "keccak empty vector"
    assert keccak256(b"transfer(address,uint256)").hex().startswith("a9059cbb"), "keccak transfer vector"
    print("# keccak self-test: OK (empty + transfer(address,uint256))")

    # --- decode the prologue -------------------------------------------------
    tbl_off = int.from_bytes(b[15:17], "big")
    n = b[8]
    print(f"# prologue: PUSH2 table_off={tbl_off} (0x{tbl_off:04x})  PUSH1 N={n}")
    assert tbl_off + 2 * n == len(b), "table does not end exactly at runtime end"
    targets = [int.from_bytes(b[tbl_off + 2 * i: tbl_off + 2 * i + 2], "big") for i in range(n)]
    assert all(b[t] == 0x5b for t in targets), "a table target is not a JUMPDEST"

    fallback = Counter(targets).most_common(1)[0][0]
    print(f"# fallback target: 0x{fallback:04x} (slots {[i for i, t in enumerate(targets) if t == fallback]})")

    # --- index every inline dispatch site ------------------------------------
    site = {}
    for i in range(len(b) - 6):
        if b[i] == 0x5b and b[i + 1] == 0x63:
            site.setdefault(b[i + 2: i + 6].hex(), i)
    all_sites = sorted(site.values())
    print(f"# inline '5b 63 <sel4>' sites: {len(all_sites)}  distinct selectors: {len(site)}")

    # --- follow collision chains: head -> PUSH2 <next> JUMPI -----------------
    def successors(head):
        nxt = [s for s in all_sites if s > head]
        end = nxt[0] if nxt else len(b)
        out = []
        for m in re.finditer(r"61([0-9a-f]{4})57", b[head:end].hex()):
            out.append(int(m.group(1), 16))
        return out

    def chain_from(head):
        """Walk the collision chain and yield every selector reachable."""
        seen, seq, cur = set(), [], head
        while cur is not None and cur not in seen:
            seen.add(cur)
            if cur in site.values():
                sel = "0x" + next(s for s, o in site.items() if o == cur)
                seq.append(sel)
                nxts = [d for d in successors(cur) if d in site.values() and d != cur]
                cur = nxts[0] if nxts else None
            else:
                break
        return seq

    # --- derive K independently from the ABI ---------------------------------
    kset = {}
    for e in abi:
        if e.get("type") != "function":
            continue
        sig = f"{e['name']}({','.join(canonical_type(i) for i in e.get('inputs', []))})"
        kset["0x" + keccak256(sig.encode()).hex()[:8]] = (sig, e.get("stateMutability", ""))
    print(f"\n# ABI-derived K = {len(kset)} (from {abi_path})")

    # --- recover the set from the runtime bytes alone ------------------------
    recovered = {}
    for slot, t in enumerate(targets):
        if t == fallback:
            continue
        for sel in chain_from(t):
            recovered.setdefault(sel, []).append(slot)
    print(f"# runtime-recovered selectors = {len(recovered)}")

    kk = sorted(set(kset) & set(recovered))
    missing = sorted(set(kset) - set(recovered))
    extra = sorted(set(recovered) - set(kset))
    print(f"# K/K: matched {len(kk)}/{len(kset)}   missing={missing}   extra={extra}")

    slot_ok = sum(1 for s, idxs in recovered.items() if all(int(s, 16) % n in idxs for _ in idxs)
                  and (int(s, 16) % n) in idxs)
    print(f"# slot == int(selector) % {n}: {slot_ok}/{len(recovered)} selectors land in their hash slot")
    direct = sum(1 for s in kset if targets[int(s, 16) % n] == site.get(s[2:]))
    print(f"#   of which direct (slot target IS the site): {direct}/{len(kset)};"
          f" chain-resolved: {len(kset) - direct}/{len(kset)}")

    # --- the two traps -------------------------------------------------------
    short = {s: v for s, v in mi.items() if len(v[2:]) < 8}
    print(f"\n# TRAP 1 leading-zero stripping: {len(short)}/{len(mi)} method_identifiers are <8 hex digits")
    for s, v in sorted(short.items(), key=lambda kv: kv[1]):
        print(f"#   printed {v:<10} -> real 0x{v[2:].rjust(8, '0')}  {s}")
    phantom = sorted(set(mi) - {v[0] for v in kset.values()})
    print(f"# TRAP 2 phantom method_identifiers entries absent from the ABI: {phantom}")
    for p in phantom:
        sel = mi[p]
        print(f"#   {p} -> {sel}; occurrences in runtime: {b.hex().count(sel[2:].rjust(8, '0'))}"
              f"; occurrences in creation: n/a (runtime-only check)")

    print("\n# --- recovered selector set (runtime bytes only) ---")
    for s in sorted(recovered):
        sig = kset.get(s, ("<UNKNOWN>", ""))[0]
        print(f"{s} {sig} slots={recovered[s]}")

    ok = (not missing) and (not extra)
    print(f"\n# VERDICT: {'K/K CLEAN — ' + str(len(kset)) + '/' + str(len(kset)) if ok else 'PARTIAL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
