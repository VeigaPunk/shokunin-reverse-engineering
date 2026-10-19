#!/usr/bin/env python3
"""EX-13 prologue/dispatch-shape analyzer (v2, disassembler-based).

Per runtime carrier:
  * anchor classes: PUSH0 (5f3560e01c), LEGACY (60003560e01c), OFF4 (60043560e01c)
  * preamble bytes 0..anchor and what they contain (freemem store / CALLVALUE
    guard / CALLDATASIZE guards)
  * post-anchor mini-disassembly of the dispatch region: PUSH4 constant sites
    with the immediately following comparison opcode (EQ/GT/LT), PUSH2+JUMPI
    destinations, JUMPDEST PCs, and the pre-first-jump structure class:
      linear-EQ  = only EQ compares before the first JUMPI
      pivot-GT   = a PUSH4+GT compare participates (sorted binary-search pivot)
  * chain completeness: every PUSH4 compare dest must land on byte 0x5b.
No third-party deps.
"""
import hashlib
import json
import sys

PUSH_LEN = {}
PUSH_LEN[0x60] = 1
PUSH_LEN[0x61] = 2
PUSH_LEN[0x62] = 3
PUSH_LEN[0x63] = 4
PUSH_LEN[0x64] = 5
PUSH_LEN[0x65] = 6
PUSH_LEN[0x66] = 7
PUSH_LEN[0x67] = 8
PUSH_LEN[0x68] = 9
PUSH_LEN[0x69] = 10
PUSH_LEN[0x6a] = 11
PUSH_LEN[0x6b] = 12
PUSH_LEN[0x6c] = 13
PUSH_LEN[0x6d] = 14
PUSH_LEN[0x6e] = 15
PUSH_LEN[0x6f] = 16
PUSH_LEN[0x70] = 17
PUSH_LEN[0x71] = 18
PUSH_LEN[0x72] = 19
PUSH_LEN[0x73] = 20
PUSH_LEN[0x74] = 21
PUSH_LEN[0x75] = 22
PUSH_LEN[0x76] = 23
PUSH_LEN[0x77] = 24
PUSH_LEN[0x78] = 25
PUSH_LEN[0x79] = 26
PUSH_LEN[0x7a] = 27
PUSH_LEN[0x7b] = 28
PUSH_LEN[0x7c] = 29
PUSH_LEN[0x7d] = 30
PUSH_LEN[0x7e] = 31
PUSH_LEN[0x7f] = 32

CMP = {0x14: "EQ", 0x10: "LT", 0x11: "GT", 0x12: "SLT", 0x13: "SGT"}
PATTERNS = {
    "PUSH0": bytes.fromhex("5f3560e01c"),
    "LEGACY": bytes.fromhex("60003560e01c"),
    "OFF4": bytes.fromhex("60043560e01c"),
}


def find_all(code, pat):
    idx, start = [], 0
    while True:
        j = code.find(pat, start)
        if j < 0:
            return idx
        idx.append(j)
        start = j + 1


def decode(code, start, stop):
    """Yield (pc, op, operand_int_or_None, imm_bytes) linearly from start."""
    pc = start
    while pc < stop:
        op = code[pc]
        imm = None
        n = PUSH_LEN.get(op, 0)
        if n:
            raw = code[pc + 1:pc + 1 + n]
            imm = int.from_bytes(raw, "big")
        yield (pc, op, imm, code[pc + 1:pc + 1 + n])
        pc += 1 + n


def dispatch_shape(code, anchor, window=640):
    stop = min(len(code), anchor + window)
    ins = list(decode(code, anchor, stop))
    # PUSH4 followed by compare, and the branch destination (next PUSH2+JUMPI)
    cmp_sites = []
    for i, (pc, op, imm, immb) in enumerate(ins):
        if op == 0x63 and i + 1 < len(ins) and ins[i + 1][1] in CMP:
            nxt = ins[i + 1]
            dest = None
            if i + 3 < len(ins) and ins[i + 2][1] == 0x61 and ins[i + 3][1] == 0x57:
                dest = ins[i + 2][2]
            cmp_sites.append({
                "push4_pc": pc,
                "sel": immb.hex(),
                "cmp": CMP[nxt[1]],
                "dest": dest,
                "after": ins[i + 2][1] if i + 2 < len(ins) else None,
            })
    jumpis = [pc for (pc, op, _i, _b) in ins if op == 0x57]
    jumpdests = [pc for (pc, op, _i, _b) in ins if op == 0x5b]
    # structure class: first JUMPI on a selector compare
    first_cmp_jumpi = None
    cls = "no-compare"
    for i, (pc, op, imm, immb) in enumerate(ins):
        if op == 0x63 and i + 1 < len(ins) and ins[i + 1][1] in CMP:
            c = CMP[ins[i + 1][1]]
            if c == "EQ":
                cls = cls if cls not in ("no-compare",) else "linear-EQ"
            else:
                cls = "pivot-" + c
            first_cmp_jumpi = pc
            break
    # destinations: PUSH2 immediately followed by JUMPI
    dests = []
    for i, (pc, op, imm, immb) in enumerate(ins):
        if op == 0x61 and i + 1 < len(ins) and ins[i + 1][1] == 0x57:
            dests.append({"pc": pc, "dest": imm, "dest_byte": code[imm] if imm < len(code) else None})
    return {
        "structure_class": cls,
        "first_cmp_push4_pc": first_cmp_jumpi,
        "eq_sites": [s for s in cmp_sites if s["cmp"] == "EQ"],
        "non_eq_sites": [s for s in cmp_sites if s["cmp"] != "EQ"],
        "n_eq": sum(1 for s in cmp_sites if s["cmp"] == "EQ"),
        "n_non_eq": sum(1 for s in cmp_sites if s["cmp"] != "EQ"),
        "jumpi_pcs": jumpis,
        "jumpdest_pcs": jumpdests,
        "branch_dests": dests,
        "window_end": stop,
    }


def analyze(path):
    code = open(path, "rb").read()
    out = {
        "path": path,
        "bytes": len(code),
        "sha256": hashlib.sha256(code).hexdigest(),
        "head64": code[:64].hex(),
        "anchors": {name: find_all(code, pat) for name, pat in PATTERNS.items()},
    }
    anchor, cls = None, None
    for name in ("PUSH0", "LEGACY", "OFF4"):
        if out["anchors"][name]:
            anchor, cls = out["anchors"][name][0], name
            break
    out["prologue_class"] = cls
    out["anchor_pc"] = anchor
    if anchor is None:
        return out
    pre = code[:anchor + 5]
    out["pre_anchor_hex"] = pre.hex()
    out["preamble"] = {
        "freemem_store_6080604052": pre[:8].hex() == "6080604052" or pre[:6].hex().startswith("60806040"),
        "callvalue_check_348015": b"\x34\x80\x15" in pre,
        "calldatasize_iszero_3615": b"\x36\x15" in pre,
        "calldatasize_lt_60043610": b"\x60\x04\x36\x10" in pre,
    }
    out["dispatch"] = dispatch_shape(code, anchor)
    return out


def main():
    args = sys.argv[1:]
    outpath = None
    if args and args[0] == "-o":
        outpath = args[1]
        args = args[2:]
    results = [analyze(p) for p in args]
    if outpath:
        with open(outpath, "w") as f:
            json.dump(results, f, indent=1)
        print("wrote", outpath, len(results), "records")
        return
    print(json.dumps(results, indent=1))
    print("\n== summary ==")
    for r in results:
        name = r["path"].split("/")[-1]
        d = r.get("dispatch", {})
        print(f"{name:40s} bytes={r['bytes']:5d} class={r['prologue_class']} anchor={r['anchor_pc']:3d} "
              f"struct={d.get('structure_class')} eq={d.get('n_eq')} noneq={d.get('n_non_eq')}")


if __name__ == "__main__":
    main()