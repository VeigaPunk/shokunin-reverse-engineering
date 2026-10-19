#!/usr/bin/env python3
"""EX-09 (arc3-loop1-round3) independent selector extractor + 3-way reconciler.

Modeled on the r1 lineage extractor (.ufo/waves/arc3-loop1-round1/claims/c1/
EX-07/selector-recon.py, sha256 99c3c32d…): same two probe-independent methods,
re-implemented for this seat with two extensions the carrier-A shape requires:

  M1  dispatch-table parse : own EVM linear-sweep disassembler; walks the
                              dispatcher chain from the prologue anchor.  Handles
                              BOTH dest encodings: `... EQ PUSH1 <dest1> JUMPI`
                               (10-byte stride, carrier-A shape) and
                              `... EQ PUSH2 <dest2> JUMPI` (11-byte stride,
                              solc shape).
  M2  keccak scan          : pure-Python keccak-256 (reference implementation,
                              no third-party deps); computes keccak(sig)[:4] for
                              each signature and searches the raw code bytes.

Extension vs r1: every extracted dispatch target carries a JUMPDEST landing
check (`code[dest] == 0x5b`), and probe legs' `bytecodeOffset`s are checked the
same way.  The probe is never invoked by this tool.

Subcommands:
  keccak-test                            vectors for the pure-Python keccak
  extract <code-file> [hex|raw]          M1 + full PUSH4 inventory + anchor report
  scan <code-file> <sigs-file> [hex|raw] M2 keccak scan
  jumpdests <code-file> [hex|raw] o1 [o2 ...]   landing-byte check for offsets
  reconciler <code-file> <hex|raw> --planted <f> --probe <f> [<f> ...]
             [--sigs <f>]
"""
import hashlib
import json
import sys

# ---------------------------------------------------------------- keccak-256
# Keccak-f[1600], 24 rounds. Reference-derived (r1 lineage), no dependency.
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
    padded = data + (b"\x81" if pad == 1 else b"\x01" + b"\x00" * (pad - 2) + b"\x80")
    for off in range(0, len(padded), rate):
        blk = padded[off:off + rate]
        for i in range(rate // 8):
            a[i % 5][i // 5] ^= int.from_bytes(blk[i * 8:(i + 1) * 8], "little")
        _keccak_f(a)
    return b"".join(a[i % 5][i // 5].to_bytes(8, "little") for i in range(4))


def selector(sig: str) -> str:
    return keccak256(sig.encode())[:4].hex()


# ------------------------------------------------------------- EVM disassembly
def linear_sweep(code: bytes):
    """Yield (offset, opcode, immediate_bytes); PUSH1..PUSH32 consume immediates."""
    i, n = 0, len(code)
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


def landing(code: bytes, off: int) -> dict:
    """JUMPDEST landing check with local neighbourhood report."""
    b = code[off] if 0 <= off < len(code) else None
    nxt = next((off + k for k in range(1, 9)
                if off + k < len(code) and code[off + k] == 0x5b), None)
    prv = next((off - k for k in range(1, 9)
                if off - k >= 0 and code[off - k] == 0x5b), None)
    return {"offset": off,
            "byte": None if b is None else f"{b:02x}",
            "is_jumpdest": b == 0x5b,
            "next_5b": nxt, "prev_5b": prv}


def extract(code: bytes) -> dict:
    anchors = {name: code.find(bytes.fromhex(hx)) for name, hx in
               (("60003560e01c", "60003560e01c"), ("5f3560e01c", "5f3560e01c"))}
    anchor = min([v for v in anchors.values() if v >= 0], default=-1)
    ins = list(linear_sweep(code))
    push4_all = [(o, imm.hex()) for o, op, imm in ins if op == 0x63]
    # EQ/GT compare sites (loose): PUSH4 <sel> ... EQ-or-GT within 6 instrs,
    # then PUSH1|PUSH2 <dest> then JUMPI. GT nodes are binary-search pivots;
    # EQ nodes are the equality leaves whose dests are the dispatch targets.
    eq_sites, gt_sites = [], []
    for idx, (o, op, imm) in enumerate(ins):
        if op != 0x63:
            continue
        win = ins[idx + 1:idx + 8]
        hit = None
        for j, (o2, op2, _) in enumerate(win):
            if op2 in (0x14, 0x11):
                hit = (j, op2)
                break
        if hit is None:
            continue
        j, cmp_op = hit
        dest = width = None
        jumpi = False
        if j + 1 < len(win) and win[j + 1][1] in (0x60, 0x61):
            width = win[j + 1][1] - 0x5F
            dest = int.from_bytes(win[j + 1][2], "big")
            jumpi = (j + 2 < len(win) and win[j + 2][1] == 0x57)
        row = {"push4_offset": o, "selector": imm.hex(),
               "cmp_offset": win[j][0], "cmp": "EQ" if cmp_op == 0x14 else "GT",
               "dest": dest, "dest_width": width, "jumpi": jumpi,
               "landing": landing(code, dest) if dest is not None else None}
        (eq_sites if cmp_op == 0x14 else gt_sites).append(row)
    # strict chain from anchor: repeated `DUP1 PUSH4 <sel4> EQ PUSH1|PUSH2 <dest> JUMPI`
    chain = []
    if anchor >= 0:
        anchor_len = 6 if code[anchor:anchor + 1] == b"\x60" else 5
        p = anchor + anchor_len
        while p + 11 <= len(code) and code[p] == 0x80 and code[p + 1] == 0x63 \
                and code[p + 6] == 0x14 and code[p + 7] in (0x60, 0x61) \
                and code[p + 8 + (code[p + 7] - 0x5F)] == 0x57:
            width = code[p + 7] - 0x5F  # PUSH1 -> 1, PUSH2 -> 2
            dest = int.from_bytes(code[p + 8:p + 8 + width], "big")
            chain.append({"push4_offset": p + 1, "push4_site_selector_hex": code[p + 2:p + 6].hex(),
                          "selector": code[p + 2:p + 6].hex(), "dest": dest,
                          "dest_width": width,
                          "jumpi_offset": p + 8 + width,
                          "landing": landing(code, dest)})
            p += 11 if width == 2 else 10
    return {
        "code_len": len(code),
        "code_sha256": hashlib.sha256(code).hexdigest(),
        "dispatcher_anchors": anchors,
        "dispatcher_anchor_min": anchor,
        "instruction_count": len(ins),
        "push4_all": push4_all,
        "dispatch_eq_sites": eq_sites,
        "dispatch_gt_sites": gt_sites,
        "dispatch_selectors": sorted({s["selector"] for s in eq_sites}),
        "dispatch_chain": chain,
        "chain_selectors": sorted({s["selector"] for s in chain}),
        "jumpdest_positions": [i for i, b in enumerate(code) if b == 0x5b],
    }


# ------------------------------------------------------------- probe leg loader
def load_probe(path: str) -> dict:
    """Accept bare data envelopes and {ok,data,meta} wrappers (and evidence bundles)."""
    d = json.load(open(path))
    if isinstance(d, dict) and "evidence_bundle" in d:
        d = d["evidence_bundle"]["records"][0]
    if isinstance(d, dict) and "data" in d and isinstance(d["data"], dict) \
            and "raw_result" in d["data"]:
        d = d["data"]
    fns = d.get("raw_result", {}).get("functions", [])
    norm = d.get("normalized_result", {})
    return {
        "path": path,
        "evidence_id": d.get("evidence_id"),
        "subject_sha256": (d.get("subject") or {}).get("digest", {}).get("sha256"),
        "encoding": (norm.get("artifact") or {}).get("encoding"),
        "artifact_bytes": (norm.get("artifact") or {}).get("bytes"),
        "bytecode_sha256": (norm.get("bytecode") or {}).get("sha256"),
        "bytecode_bytes": (norm.get("bytecode") or {}).get("bytes"),
        "functions": [{"selector": f["selector"].lower().removeprefix("0x"),
                       "offset": f.get("bytecodeOffset")} for f in fns],
    }


def form_check(leg: dict) -> bool:
    """Per-leg encoding-form invariant (r1 CR-1 attack-1 detector)."""
    enc_ = leg.get("encoding"); ab = leg.get("artifact_bytes"); bb = leg.get("bytecode_bytes")
    if enc_ == "raw":
        return ab == bb and leg.get("subject_sha256") == leg.get("bytecode_sha256")
    if enc_ == "hex":
        # r1 CR-1 detector, widened for tolerated shape variants (0x-prefix /
        # trailing newline / uppercase measured by r1 and EX-06): 2*bb .. 2*bb+4.
        return bb is not None and 2 * bb <= ab <= 2 * bb + 4
    return False


def norm_set(sels):
    return sorted({s.strip().lower().removeprefix("0x") for s in sels if s and s.strip()})


def load_planted(path: str):
    txt = open(path).read()
    if path.endswith(".json"):
        doc = json.loads(txt)
        entries = doc.get("entries") or doc.get("functions") or []
        sels = [e.get("selector") for e in entries]
        return norm_set(sels), doc
    sels = []
    for line in txt.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            tok = line.split()[0]
            if tok.startswith("0x") or all(c in "0123456789abcdefABCDEF" for c in tok):
                sels.append(tok)
    return norm_set(sels), None


def recon(args) -> int:
    code_path, enc = args[0], args[1]
    planted_path, probe_paths, sigs_path = None, [], None
    i = 2
    while i < len(args):
        if args[i] == "--planted":
            planted_path = args[i + 1]; i += 2
        elif args[i] == "--probe":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                probe_paths.append(args[i]); i += 1
        elif args[i] == "--sigs":
            sigs_path = args[i + 1]; i += 2
        else:
            i += 1
    code = load_code(code_path, enc)
    code_sha = hashlib.sha256(code).hexdigest()
    m1 = extract(code)

    out = []
    def emit(line=""):
        print(line); out.append(line)

    emit(f"code: {code_path} ({enc})  bytes={len(code)}  sha256={code_sha}")
    emit(f"M1 anchor: {m1['dispatcher_anchors']} (min={m1['dispatcher_anchor_min']})")
    emit("M1 dispatch chain (linear shape; selector: push4_site -> encoded dest; landing):")
    for c in m1["dispatch_chain"]:
        L = c["landing"]
        emit(f"   {c['selector']}  push4@{c['push4_offset']}  dest={c['dest']} (PUSH{2 if c['dest_width']==2 else 1})  "
             f"land_byte={L['byte']} jumpdest={L['is_jumpdest']}"
             + ("" if L['is_jumpdest'] else f"  (next 5b @{L['next_5b']})"))
    emit("M1 EQ dispatch sites (filled by both shapes; dest = encoded dispatch target):")
    for c in m1["dispatch_eq_sites"]:
        L = c["landing"]
        land = "n/a" if L is None else f"land_byte={L['byte']} jumpdest={L['is_jumpdest']}" \
             + ("" if (L and L['is_jumpdest']) else (f" (next 5b @{L['next_5b']})" if L else ""))
        emit(f"   {c['selector']}  push4@{c['push4_offset']}  EQ@{c['cmp_offset']}  "
             f"dest={c['dest']} (PUSH{2 if c['dest_width']==2 else 1})  jumpi={c['jumpi']}  {land}")
    emit(f"M1 GT pivot sites: {[(g['selector'], g['dest']) for g in m1.get('dispatch_gt_sites', [])]}")
    ref = set(m1["dispatch_selectors"]) or set(m1["chain_selectors"])
    non_dispatch = [f"{h}@{o}" for o, h in m1["push4_all"] if h not in ref]
    emit(f"M1 non-dispatch PUSH4 constants: {non_dispatch}")
    emit(f"M1 JUMPDEST positions in code: {m1['jumpdest_positions']}")
    emit()

    sources = {"M1_eq_sites": m1["dispatch_selectors"]}
    if m1["chain_selectors"]:
        sources["M1_chain"] = m1["chain_selectors"]
    else:
        emit("M1 linear-chain parser: no linear chain in this carrier "
             "(dispatch shape differs; EQ sites carry the dispatch table)")
    gt_pivots = sorted({g["selector"] for g in m1.get("dispatch_gt_sites", [])})
    if gt_pivots:
        emit(f"M1 GT pivots informational (subset of dispatch set expected): {gt_pivots} "
             f"subset_of_dispatch={set(gt_pivots) <= ref}")
        emit()

    if sigs_path:
        sigs = [l.strip() for l in open(sigs_path) if l.strip() and not l.startswith("#")]
        m2 = [{"signature": s, "selector": selector(s),
               "push4_offsets": [o for o, h in m1["push4_all"] if h == selector(s)]}
              for s in sigs]
        sources["M2_keccak_scan"] = norm_set([x["selector"] for x in m2 if x["push4_offsets"]])
        emit("M2 keccak scan (sig -> selector -> PUSH4 immediate offsets):")
        for x in m2:
            emit(f"   {x['signature']:34s} {x['selector']}  @{x['push4_offsets']}")
        emit()

    if planted_path:
        planted, _ = load_planted(planted_path)
        sources["PLANTED"] = planted

    legs = [load_probe(p) for p in probe_paths]
    for leg in legs:
        sources["PROBE:" + leg["path"].split("/")[-1]] = norm_set([f["selector"] for f in leg["functions"]])

    verdict_all = True
    landing_fail_total = 0
    emit("source set reconciliation (reference = M1 eq sites, else chain):")
    for name, sels in sources.items():
        s = set(sels)
        missing, extra = sorted(ref - s), sorted(s - ref)
        ok = s == ref
        verdict_all &= ok
        emit(f"  {name:44s} n={len(s):2d}  {'MATCH' if ok else 'MISMATCH'}  missing={missing} extra={extra}")
    emit()

    emit("probe legs — payload, offsets, landing, digest pins vs my parse:")
    my_dest = {c["selector"]: c["dest"] for c in m1["dispatch_eq_sites"] if c["dest"] is not None and c["jumpi"]}
    for c in m1["dispatch_chain"]:
        my_dest.setdefault(c["selector"], c["dest"])
    my_land_rows = [f"{s}@{d}:byte={landing(code, d)['byte']},jumpdest={landing(code, d)['is_jumpdest']}"
                    for s, d in sorted(my_dest.items())]
    emit(f"  MY-PARSE dests: {'; '.join(my_land_rows)}")
    for leg in legs:
        name = leg["path"].split("/")[-1]
        sels = norm_set([f["selector"] for f in leg["functions"]])
        offs = {f["selector"]: f["offset"] for f in leg["functions"]}
        ok_set = set(sels) == ref
        off_mism = {s: (my_dest.get(s), o) for s, o in offs.items() if my_dest.get(s) != o}
        digest_ok = leg["bytecode_sha256"] == code_sha
        form_ok = form_check(leg)
        land_rows = []
        for s, o in sorted(offs.items()):
            L = landing(code, o)
            if not L['is_jumpdest']:
                landing_fail_total += 1
            land_rows.append(f"{s}@{o}:byte={L['byte']},jumpdest={L['is_jumpdest']}")
        verdict_all &= ok_set and not off_mism and digest_ok and form_ok
        emit(f"  {name}")
        emit(f"      set {'MATCH' if ok_set else 'MISMATCH'} n={len(sels)}  offsets {'equal' if not off_mism else off_mism}"
             f"  digest {'SAME' if digest_ok else 'DIFFER'}  form {'OK' if form_ok else 'WRONG-FORM(' + str(leg['encoding']) + ')'}")
        emit(f"      offsets landing: {'; '.join(land_rows)}")
    emit()
    for s, d in sorted(my_dest.items()):
        if not landing(code, d)['is_jumpdest']:
            landing_fail_total += 1
    if verdict_all and landing_fail_total == 0:
        emit("VERDICT: ALL SOURCES AGREE (sets+offsets+pins); every offset lands on a JUMPDEST")
        return 0
    if verdict_all:
        emit(f"VERDICT: SETS/OFFSETS/PINS AGREE — LANDING ANOMALY: {landing_fail_total} offset-checks hit non-0x5b bytes")
        return 1
    emit("VERDICT: MISMATCH PRESENT (set/offset/pin/form)")
    return 1


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
            ("balanceOf(address)", "70a08231b98ef4ca268c9cc3f6b4590e4bfec28280db06bb5d45e689f2a360be"),
        ]
        ok = True
        for msg, expect in vectors:
            got = keccak256(msg.encode()).hex()
            ok &= got == expect
            print(f"{'OK ' if got == expect else 'FAIL'} keccak256({msg!r}) = {got}")
        for sig, sel in [("transfer(address,uint256)", "a9059cbb"),
                         ("balanceOf(address)", "70a08231"),
                         ("approve(address,uint256)", "095ea7b3"),
                         ("transferFrom(address,address,uint256)", "23b872dd")]:
            got = selector(sig)
            ok &= got == sel
            print(f"{'OK ' if got == sel else 'FAIL'} selector({sig}) = {got}")
        print("VECTORS", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    if cmd == "extract":
        code = load_code(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "hex")
        print(json.dumps(extract(code), indent=2))
        return 0
    if cmd == "scan":
        code = load_code(sys.argv[2], sys.argv[3])
        sigs = [l.strip() for l in open(sys.argv[4]) if l.strip() and not l.startswith("#")]
        res = [{"signature": s, "selector": selector(s),
                "offsets": [i for i in range(len(code) - 3) if code[i:i + 4].hex() == selector(s)]}
               for s in sigs]
        print(json.dumps({"code_len": len(code), "results": res,
                          "found": sum(bool(r["offsets"]) for r in res), "total": len(res)}, indent=2))
        return 0
    if cmd == "jumpdests":
        code = load_code(sys.argv[2], sys.argv[3])
        rows = [landing(code, int(o, 0)) for o in sys.argv[4:]]
        for r in rows:
            print(f"offset {r['offset']}: byte={r['byte']} jumpdest={r['is_jumpdest']}"
                  f" next_5b={r['next_5b']} prev_5b={r['prev_5b']}")
        return 0
    if cmd == "reconciler":
        return recon(sys.argv[2:])
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())