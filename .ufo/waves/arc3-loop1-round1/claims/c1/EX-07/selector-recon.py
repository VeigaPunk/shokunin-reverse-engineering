#!/usr/bin/env python3
"""EX-07 independent selector extractor + 3-way reconciliation tool.

Two independent extraction methods, neither of which calls the `rea` probe:
  M1 dispatch-table parse : own EVM linear-sweep disassembler; extracts PUSH4
                            immediates that sit at EQ/JUMPI dispatch sites,
                            anchored on the `PUSH1 00 CALLDATALOAD PUSH1 e0 SHR`
                            (60003560e01c) dispatcher prologue.
  M2 keccak scan          : pure-Python keccak-256 (reference implementation,
                            no third-party deps); computes keccak(sig)[:4] for
                            each signature and searches the raw bytecode bytes.

Subcommands:
  keccak-test                      vectors for the pure-Python keccak
  extract <code-file> [hex|raw]    M1 + full PUSH4 inventory + anchor report
  scan <code-file> <sigs-file> [hex|raw]   M2 keccak scan
  compare <a.txt> <b.txt> ...      set comparison across selector lists
"""
import json
import sys

# ---------------------------------------------------------------- keccak-256
# Keccak-f[1600], 24 rounds. Reference-derived, no external dependency.
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROT = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]
M64 = (1 << 64) - 1


def _rot(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & M64 if n else v


def _keccak_f(a):
    for rc in RC:
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rot(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x][y] ^= d[x]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rot(a[x][y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y] & M64) & b[(x + 2) % 5][y])
        a[0][0] ^= rc


def keccak256(data: bytes) -> bytes:
    rate = 136
    a = [[0] * 5 for _ in range(5)]
    pad = rate - (len(data) % rate)
    if pad == 1:
        padded = data + b"\x81"
    else:
        padded = data + b"\x01" + b"\x00" * (pad - 2) + b"\x80"
    for off in range(0, len(padded), rate):
        blk = padded[off:off + rate]
        for i in range(rate // 8):
            a[i % 5][i // 5] ^= int.from_bytes(blk[i * 8:(i + 1) * 8], "little")
        _keccak_f(a)
    out = bytearray()
    for i in range(4):
        out += a[i % 5][i // 5].to_bytes(8, "little")
    return bytes(out)


def selector(sig: str) -> str:
    return keccak256(sig.encode())[:4].hex()


# ------------------------------------------------------------- EVM disassembly
def linear_sweep(code: bytes):
    """Yield (offset, opcode, immediate_bytes); PUSH1..32 consume immediates."""
    i = 0
    n = len(code)
    while i < n:
        op = code[i]
        if 0x60 <= op <= 0x7F:
            ln = op - 0x5F
            yield i, op, code[i + 1:i + 1 + ln]
            i += 1 + ln
        else:
            yield i, op, b""
            i += 1


def load_code(path: str, enc: str) -> bytes:
    raw = open(path, "rb").read()
    if enc == "hex":
        return bytes.fromhex(raw.decode().strip().removeprefix("0x"))
    return raw


def extract(code: bytes) -> dict:
    anchors = {name: code.find(bytes.fromhex(hx)) for name, hx in
               (("60003560e01c", "60003560e01c"), ("5f3560e01c", "5f3560e01c"))}
    anchor = min([v for v in anchors.values() if v >= 0], default=-1)
    ins = list(linear_sweep(code))
    push4_all = [(o, imm.hex()) for o, op, imm in ins if op == 0x63]
    # EQ/JUMPI dispatch sites: PUSH4 <sel> EQ ... JUMPI within a short window
    eq_sites = []
    for idx, (o, op, imm) in enumerate(ins):
        if op != 0x63:
            continue
        window = ins[idx + 1:idx + 4]
        ops = [w[1] for w in window]
        if ops and 0x14 in ops:  # EQ follows (possibly after DUP)
            jidx = next((k for k, w in enumerate(ins[idx + 1:idx + 6])
                         if w[1] == 0x57), None)  # JUMPI
            eq_sites.append({"push4_offset": o, "selector": imm.hex(),
                             "eq_offset": ins[idx + 1 + ops.index(0x14)][0],
                             "jumpi_offset": ins[idx + 1 + jidx][0] if jidx is not None else None})
    # strict chain mode: from the anchor, repeated `DUP1 PUSH4 <sel> EQ PUSH2 <dest> JUMPI`
    chain = []
    if anchor >= 0:
        anchor_len = 5 if code[anchor:anchor + 1] == b"\x5f" else 6
        p = anchor + anchor_len
        while (p + 11 <= len(code) and code[p] == 0x80 and code[p + 1] == 0x63
               and code[p + 6] == 0x14 and code[p + 7] == 0x61 and code[p + 10] == 0x57):
            chain.append({"push4_offset": p + 1, "selector": code[p + 2:p + 6].hex(),
                          "dest": int.from_bytes(code[p + 8:p + 10], "big")})
            p += 11
    return {
        "code_len": len(code),
        "code_sha256": __import__("hashlib").sha256(code).hexdigest(),
        "dispatcher_anchors": anchors,
        "dispatcher_anchor_min": anchor,
        "instruction_count": len(ins),
        "push4_all": push4_all,
        "dispatch_eq_sites": eq_sites,
        "dispatch_selectors": sorted({s["selector"] for s in eq_sites}),
        "dispatch_chain": chain,
        "chain_selectors": sorted({s["selector"] for s in chain}),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "keccak-test":
        vectors = [
            ("", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
            ("abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
            ("transfer(address,uint256)", "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b"),
            ("balanceOf(address)", "70a082313deadceb61a2a0e5f36b2d21b28f1a3c2c0c9b7c0c6b0a7b6d0b4f5f"),
        ]
        ok = True
        for msg, expect in vectors:
            got = keccak256(msg.encode()).hex()
            if msg == "balanceOf(address)":
                expect = "70a08231b98ef4ca268c9cc3f6b4590e4bfec28280db06bb5d45e689f2a360be"
            mark = "OK " if got == expect else "FAIL"
            ok &= got == expect
            print(f"{mark} keccak256({msg!r}) = {got}")
        for sig, sel in [("transfer(address,uint256)", "a9059cbb"),
                         ("balanceOf(address)", "70a08231"),
                         ("approve(address,uint256)", "095ea7b3"),
                         ("transferFrom(address,address,uint256)", "23b872dd")]:
            got = selector(sig)
            mark = "OK " if got == sel else "FAIL"
            ok &= got == sel
            print(f"{mark} selector({sig}) = {got}")
        print("VECTORS", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    if cmd == "extract":
        code = load_code(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "hex")
        print(json.dumps(extract(code), indent=2))
        return 0
    if cmd == "scan":
        code = load_code(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "hex")
        sigs = [l.strip() for l in open(sys.argv[4]) if l.strip() and not l.startswith("#")]
        res = []
        for sig in sigs:
            s = selector(sig)
            offsets = [i for i in range(len(code) - 3) if code[i:i + 4].hex() == s]
            res.append({"signature": sig, "selector": s, "found": bool(offsets),
                        "offsets": offsets})
        print(json.dumps({"code_len": len(code), "results": res,
                          "found": sum(r["found"] for r in res), "total": len(res)}, indent=2))
        return 0
    if cmd == "compare":
        sets = []
        for path in sys.argv[2:]:
            vals = [l.strip().lower().removeprefix("0x") for l in open(path)
                    if l.strip() and not l.strip().startswith("#")]
            sets.append((path, set(vals)))
        base_path, base = sets[0]
        print(f"reference: {base_path} ({len(base)} selectors)")
        for path, s in sets[1:]:
            print(f"{path}: {len(s)} selectors; "
                  f"missing_vs_ref={sorted(base - s)} extra_vs_ref={sorted(s - base)} "
                  f"{'MATCH' if s == base else 'MISMATCH'}")
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
