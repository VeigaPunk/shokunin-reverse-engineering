#!/usr/bin/env python3
"""EX-08 (arc3-loop1-round4, chain c1) — independent selector extraction + 3-way reconciler.

Seat task: planted (EX-05) vs probe (EX-06/07) vs an independent extraction from the
runtime bytes. Two probe-independent methods:

  M1  chained-comparison parse : own EVM linear-sweep disassembler; walks the
      dispatcher from prologue anchors. Handles the strict linear chain
      (`DUP1 PUSH4 <sel> EQ PUSH1|PUSH2 <dest> JUMPI`, 10/11-byte strides) and,
      as a fallback, the loose compare-site scan (PUSH4 <sel> ... EQ|GT within a
      short window, then PUSH1|PUSH2 <dest> JUMPI) which carries binary-search
      dispatchers.
  M2  planted-value PUSH4 scan : every planted selector is searched as a raw
      4-byte PUSH4 immediate in the code, and each hit's participation in a
      comparison is reported. This leg is a confirmation scan, not a derivation.
  M3  (optional) keccak derivation : pure-Python keccak-256 derives
      keccak(sig)[:4] from a signature list and cross-checks each against the
      runtime bytes — used when the carrier's signature list is available.

The probe (`inspect-evm-interface` envelopes) is never invoked by M1/M2/M3.

Subcommands:
  keccak-test                                   standard vectors
  extract <code-file> [hex|raw]                 M1 + PUSH4 census + anchor report
  scan4 <code-file> <hex|raw> <values-file>     M2: each value's PUSH4 sites + cmp context
  keccak-sigs <sigs-file>                       M3: sig -> selector
  reconciler <code-file> <hex|raw> --planted <f> --probe <f>... [--sigs <f>] [--values <f>]
"""
import hashlib
import json
import sys

# ---------------------------------------------------------------- keccak-256
# Keccak-f[1600] (rate 136, pad 0x01), pure Python, no third-party deps.
_RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
_R = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]
_M64 = (1 << 64) - 1


def _rol(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & _M64 if n else v


def keccak_f(a):
    for rc in _RC:
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x + 4) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x][y] ^= d[x]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rol(a[x][y], _R[x][y])
        for x in range(5):
            for y in range(5):
                a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y]) & _M64 & b[(x + 2) % 5][y])
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
        keccak_f(a)
    return b"".join(a[i % 5][i // 5].to_bytes(8, "little") for i in range(4))


def selector(sig: str) -> str:
    return keccak256(sig.encode())[:4].hex()


# ------------------------------------------------------------- EVM disassembly
def sweep(code: bytes):
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


def landing(code: bytes, off):
    if off is None or not (0 <= off < len(code)):
        return {"offset": off, "byte": None, "is_jumpdest": False,
                "next_5b": None, "prev_5b": None}
    b = code[off]
    nxt = next((off + k for k in range(1, 9) if off + k < len(code) and code[off + k] == 0x5b), None)
    prv = next((off - k for k in range(1, 9) if off - k >= 0 and code[off - k] == 0x5b), None)
    return {"offset": off, "byte": f"{b:02x}", "is_jumpdest": b == 0x5b,
            "next_5b": nxt, "prev_5b": prv}


def extract(code: bytes) -> dict:
    ins = list(sweep(code))
    # anchors: solc prologue classes seen in this family + vyper-style candidates
    anchor_pats = {
        "5f3560e01c": "5f3560e01c",   # PUSH0 CALLDATALOAD PUSH1 0xe0 SHR
        "60003560e01c": "60003560e01c",  # PUSH1 0 CALLDATALOAD PUSH1 0xe0 SHR
        "60043610": "60043610",       # PUSH1 4 CALLDATASIZE LT  (older vyper guard)
        "60043560e01c": "60043560e01c",  # PUSH1 4 CALLDATALOAD PUSH1 0xe0 SHR
    }
    anchors = {k: code.find(bytes.fromhex(v)) for k, v in anchor_pats.items()}
    anchor = min([v for v in anchors.values() if v >= 0], default=-1)

    push4_all = [(o, imm.hex()) for o, op, imm in ins if op == 0x63]

    # strict linear chain from anchor
    chain = []
    if anchor >= 0:
        # anchor length: whichever pattern matched decides; walk from first match end
        first = min((v, k) for k, v in anchors.items() if v >= 0)
        p = first[0] + len(first[1]) // 2
        while p + 10 <= len(code) and code[p] == 0x80 and code[p + 1] == 0x63 \
                and code[p + 6] == 0x14 and code[p + 7] in (0x60, 0x61):
            width = code[p + 7] - 0x5F
            if p + 8 + width >= len(code) or code[p + 8 + width] != 0x57:
                break
            dest = int.from_bytes(code[p + 8:p + 8 + width], "big")
            chain.append({"push4_offset": p + 1, "selector": code[p + 2:p + 6].hex(),
                          "dest": dest, "dest_width": width,
                          "jumpi_offset": p + 8 + width,
                          "landing": landing(code, dest)})
            p += 11 if width == 2 else 10

    # Vyper linear XOR chain: `PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI`
    # (11 bytes); on match the body falls through at +11, else jump to the next
    # test. Measured on the round-4 CarrierV runtime (vyper 0.4.3).
    vyper_chain = []
    for o, op, imm in ins:
        if op != 0x63 or o + 11 > len(code):
            continue
        if code[o + 5] == 0x81 and code[o + 6] == 0x18 \
                and code[o + 7] == 0x61 and code[o + 10] == 0x57:
            dest = int.from_bytes(code[o + 8:o + 10], "big")
            vyper_chain.append({"push4_offset": o, "selector": imm.hex(),
                                "next_test": dest, "body_offset": o + 11,
                                "next_test_landing": landing(code, dest),
                                "body_landing": landing(code, o + 11)})

    # Vyper linear XOR chain: `PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI`
    # (11 bytes); on match the body falls through at +11, else jump to the next
    # test. Measured on the round-4 CarrierV runtime (vyper 0.4.3).
    vyper_chain = []
    for o, op, imm in ins:
        if op != 0x63 or o + 11 > len(code):
            continue
        if code[o + 5] == 0x81 and code[o + 6] == 0x18 \
                and code[o + 7] == 0x61 and code[o + 10] == 0x57:
            dest = int.from_bytes(code[o + 8:o + 10], "big")
            vyper_chain.append({"push4_offset": o, "selector": imm.hex(),
                                "next_test": dest, "body_offset": o + 11,
                                "next_test_landing": landing(code, dest),
                                "body_landing": landing(code, o + 11)})

    # loose compare-site scan: each PUSH4 followed within 8 instrs by EQ/GT/LT,
    # then nearest PUSH1|PUSH2 + JUMPI within the window. Sites whose push4
    # offset is already a Vyper chain site are excluded (the chain parse is the
    # stricter reading; the loose window otherwise picks up body comparisons
    # like `PUSH0 SLOAD PUSH1 01 EQ`).
    vyper_offsets = {c["push4_offset"] for c in vyper_chain}
    eq_sites, gt_sites = [], []
    for idx, (o, op, imm) in enumerate(ins):
        if op != 0x63 or o in vyper_offsets:
            continue
        win = ins[idx + 1:idx + 9]
        hit = None
        for j, (o2, op2, _) in enumerate(win):
            if op2 in (0x14, 0x11, 0x10):
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
               "cmp_offset": win[j][0], "cmp": {0x14: "EQ", 0x11: "GT", 0x10: "LT"}[cmp_op],
               "dest": dest, "dest_width": width, "jumpi": jumpi,
               "landing": landing(code, dest) if dest is not None else None}
        (eq_sites if cmp_op == 0x14 else gt_sites).append(row)

    return {
        "code_len": len(code),
        "code_sha256": hashlib.sha256(code).hexdigest(),
        "anchors": anchors,
        "anchor_min": anchor,
        "instruction_count": len(ins),
        "push4_all": push4_all,
        "dispatch_chain": chain,
        "chain_selectors": sorted({c["selector"] for c in chain}),
        "dispatch_eq_sites": eq_sites,
        "dispatch_eq_selectors": sorted({s["selector"] for s in eq_sites}),
        "dispatch_non_eq_sites": gt_sites,
        "vyper_chain": vyper_chain,
        "vyper_chain_selectors": sorted({c["selector"] for c in vyper_chain}),
        "jumpdest_positions": [i for i, b in enumerate(code) if b == 0x5b],
    }


# ------------------------------------------------------------- input loaders
def norm_set(sels):
    return sorted({s.strip().lower().removeprefix("0x") for s in sels if s and s.strip()})


def load_planted(path: str):
    txt = open(path).read()
    if path.endswith(".json"):
        doc = json.loads(txt)
        if isinstance(doc.get("selectors"), list):          # EX-07/Rv2TokenOpt + EX-06 shapes
            sels = [e.get("selector") if isinstance(e, dict) else e for e in doc["selectors"]]
            return norm_set(sels), doc
        if isinstance(doc.get("planted_selectors"), dict):  # EX-04 CarrierV shape
            return norm_set(doc["planted_selectors"].values()), doc
        entries = doc.get("entries") or doc.get("functions") or []
        sels = [e.get("selector") if isinstance(e, dict) else e for e in entries]
        return norm_set(sels), doc
    sels = []
    for line in txt.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            tok = line.split()[0]
            if tok.startswith("0x") or all(c in "0123456789abcdefABCDEF" for c in tok):
                sels.append(tok)
    return norm_set(sels), None


def load_probe(path: str) -> dict:
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
    enc_, ab, bb = leg.get("encoding"), leg.get("artifact_bytes"), leg.get("bytecode_bytes")
    if enc_ == "raw":
        return ab == bb and leg.get("subject_sha256") == leg.get("bytecode_sha256")
    if enc_ == "hex":
        return bb is not None and 2 * bb <= ab <= 2 * bb + 4
    return False


# ------------------------------------------------------------- reconciler
def recon(args) -> int:
    code_path, enc = args[0], args[1]
    planted_path, sigs_path, values_path = None, None, None
    probe_paths = []
    i = 2
    while i < len(args):
        if args[i] == "--planted":
            planted_path = args[i + 1]; i += 2
        elif args[i] == "--sigs":
            sigs_path = args[i + 1]; i += 2
        elif args[i] == "--values":
            values_path = args[i + 1]; i += 2
        elif args[i] == "--probe":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                probe_paths.append(args[i]); i += 1
        else:
            i += 1
    code = load_code(code_path, enc)
    code_sha = hashlib.sha256(code).hexdigest()
    m1 = extract(code)

    out = []
    def emit(line=""):
        print(line); out.append(line)

    emit(f"code: {code_path} ({enc})  bytes={len(code)}  sha256={code_sha}")
    emit(f"M1 anchors: {m1['anchors']} (min={m1['anchor_min']})")
    emit("M1 strict chain (linear `DUP1 PUSH4 <sel> EQ PUSH1|PUSH2 <dest> JUMPI`):")
    for c in m1["dispatch_chain"]:
        L = c["landing"]
        emit(f"   {c['selector']}  push4@{c['push4_offset']}  dest={c['dest']} "
             f"(PUSH{c['dest_width']})  land_byte={L['byte']} jumpdest={L['is_jumpdest']}"
             + ("" if L["is_jumpdest"] else f"  (next 5b @{L['next_5b']})"))
    if not m1["dispatch_chain"]:
        emit("   (no strict linear chain — dispatcher uses another compare shape)")
    emit("M1 Vyper XOR chain (`PUSH4 <sel> DUP2 XOR PUSH2 <next_test> JUMPI`; body falls through):")
    for c in m1["vyper_chain"]:
        Ln, Lb = c["next_test_landing"], c["body_landing"]
        emit(f"   {c['selector']}  push4@{c['push4_offset']}  next_test={c['next_test']} "
             f"(land_byte={Ln['byte']},jumpdest={Ln['is_jumpdest']})  body@{c['body_offset']} "
             f"(land_byte={Lb['byte']},jumpdest={Lb['is_jumpdest']})")
    if not m1["vyper_chain"]:
        emit("   (no Vyper XOR chain in this carrier)")
    emit("M1 EQ compare sites (all shapes):")
    for c in m1["dispatch_eq_sites"]:
        L = c["landing"]
        land = "n/a" if L is None else (f"land_byte={L['byte']} jumpdest={L['is_jumpdest']}"
                                        + ("" if L["is_jumpdest"] else f" (next 5b @{L['next_5b']})"))
        emit(f"   {c['selector']}  push4@{c['push4_offset']}  EQ@{c['cmp_offset']}  "
             f"dest={c['dest']} (PUSH{c['dest_width']})  jumpi={c['jumpi']}  {land}")
    emit(f"M1 GT/LT pivot sites: {[(g['selector'], g['cmp'], g['dest']) for g in m1['dispatch_non_eq_sites']]}")
    ref = set(m1["dispatch_eq_selectors"]) or set(m1["chain_selectors"]) or set(m1["vyper_chain_selectors"])
    non_dispatch = [f"{h}@{o}" for o, h in m1["push4_all"] if h not in ref]
    emit(f"M1 non-dispatch PUSH4 constants: {non_dispatch}")
    emit(f"M1 JUMPDEST positions: {m1['jumpdest_positions']}")
    emit()

    sources = {}
    if m1["dispatch_eq_selectors"]:
        sources["M1_eq_sites"] = m1["dispatch_eq_selectors"]
    if m1["chain_selectors"]:
        sources["M1_chain"] = m1["chain_selectors"]
    if m1["vyper_chain_selectors"]:
        sources["M1_vyper_chain"] = m1["vyper_chain_selectors"]
    if not sources:
        sources["M1_eq_sites"] = []

    if sigs_path:
        sigs = [l.strip() for l in open(sigs_path) if l.strip() and not l.startswith("#")]
        m3 = []
        for s in sigs:
            sel = selector(s)
            offs = [o for o, h in m1["push4_all"] if h == sel]
            m3.append({"signature": s, "selector": sel, "push4_offsets": offs})
        sources["M3_keccak_sigs"] = norm_set([x["selector"] for x in m3 if x["push4_offsets"]])
        emit("M3 keccak(sig) -> selector -> PUSH4 sites in runtime:")
        for x in m3:
            emit(f"   {x['signature']:44s} {x['selector']}  @{x['push4_offsets']}")
        emit()

    if values_path:
        vals = norm_set([l.split()[0] for l in open(values_path)
                         if l.strip() and not l.startswith("#")])
        emit("M2 planted-value PUSH4 scan (each value's immediate sites + cmp context):")
        m2_set = set()
        for v in vals:
            sites = [o for o, h in m1["push4_all"] if h == v]
            ctx = []
            for c in m1["dispatch_eq_sites"] + m1["dispatch_non_eq_sites"]:
                if c["selector"] == v:
                    ctx.append(f"{c['cmp']}@{c['cmp_offset']}->{c['dest']}"
                               + (f"(land={c['landing']['byte']})" if c["landing"] else ""))
            if sites:
                m2_set.add(v)
            emit(f"   {v}  push4_sites={sites}  cmp_context={ctx}")
        sources["M2_planted_scan"] = sorted(m2_set)
        emit()

    if planted_path:
        planted, _ = load_planted(planted_path)
        sources["PLANTED"] = planted

    legs = [load_probe(p) for p in probe_paths]
    for leg in legs:
        sources["PROBE:" + leg["path"].split("/")[-1]] = norm_set([f["selector"] for f in leg["functions"]])

    emit("source set reconciliation (reference = M1 sites, all shapes):")
    verdict_all = True
    for name, sels in sources.items():
        s = set(sels)
        missing, extra = sorted(ref - s), sorted(s - ref)
        ok = s == ref
        verdict_all &= ok
        emit(f"  {name:52s} n={len(s):2d}  {'MATCH' if ok else 'MISMATCH'}  missing={missing} extra={extra}")
    emit()

    # candidate offsets per selector: EQ/chain dests, plus Vyper push4-site and body
    my_dest = {}
    for c in m1["dispatch_eq_sites"]:
        if c["dest"] is not None and c["jumpi"]:
            my_dest.setdefault(c["selector"], []).append(c["dest"])
    for c in m1["dispatch_chain"]:
        my_dest.setdefault(c["selector"], []).append(c["dest"])
    for c in m1["vyper_chain"]:
        my_dest.setdefault(c["selector"], []).extend([c["push4_offset"], c["body_offset"]])

    emit("probe legs — set, offsets vs my parse, landing, digest pins, form:")
    landing_fail = 0
    vyper_shape = bool(m1["vyper_chain_selectors"]) and not m1["dispatch_eq_selectors"]
    if vyper_shape:
        emit("  (Vyper-shape carrier: probe bytecodeOffset is expected to equal the")
        emit("   chain body offset — the fall-through target after the XOR/JUMPI —")
        emit("   which is NOT a JUMPDEST; the landing column is a shape reading.)")
    for leg in legs:
        name = leg["path"].split("/")[-1]
        sels = norm_set([f["selector"] for f in leg["functions"]])
        offs = {f["selector"]: f["offset"] for f in leg["functions"]}
        ok_set = set(sels) == ref
        off_mism = {s: (my_dest.get(s), o) for s, o in offs.items() if o not in my_dest.get(s, [])}
        digest_ok = leg["bytecode_sha256"] == code_sha
        form_ok = form_check(leg)
        land_rows = []
        for s, o in sorted(offs.items()):
            L = landing(code, o)
            if not L["is_jumpdest"] and not vyper_shape:
                landing_fail += 1
            land_rows.append(f"{s}@{o}:byte={L['byte']},jumpdest={L['is_jumpdest']}")
        verdict_all &= ok_set and not off_mism and digest_ok and form_ok
        emit(f"  {name}")
        emit(f"      set {'MATCH' if ok_set else 'MISMATCH'} n={len(sels)}  "
             f"offsets {'equal' if not off_mism else off_mism}  "
             f"digest {'SAME' if digest_ok else 'DIFFER'}  form {'OK' if form_ok else 'WRONG-FORM'}")
        emit(f"      offsets landing: {'; '.join(land_rows)}")
    emit()
    if verdict_all and vyper_shape:
        emit("VERDICT: ALL SOURCES AGREE (sets+offsets+pins); Vyper-shape offsets land on chain "
             "body starts (fall-through), not JUMPDESTs — measured shape, not a defect")
        return 0
    if verdict_all and landing_fail == 0:
        emit("VERDICT: ALL SOURCES AGREE (sets+offsets+pins); every offset lands on a JUMPDEST")
        return 0
    if verdict_all:
        emit(f"VERDICT: SETS/OFFSETS/PINS AGREE — LANDING ANOMALY: {landing_fail} non-JUMPDEST landing(s)")
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
            print(f"{'OK ' if got == expect else 'FAIL'} keccak256({msg!r})")
        for sig, sel in [("transfer(address,uint256)", "a9059cbb"),
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
    if cmd == "scan4":
        code = load_code(sys.argv[2], sys.argv[3])
        vals = norm_set([l.split()[0] for l in open(sys.argv[4]) if l.strip() and not l.startswith("#")])
        m1 = extract(code)
        rows = []
        for v in vals:
            sites = [o for o, h in m1["push4_all"] if h == v]
            rows.append({"value": v, "push4_sites": sites, "found": bool(sites)})
        print(json.dumps({"code_len": len(code), "rows": rows,
                          "found": sum(r["found"] for r in rows), "total": len(rows)}, indent=2))
        return 0
    if cmd == "keccak-sigs":
        for l in open(sys.argv[2]):
            l = l.strip()
            if l and not l.startswith("#"):
                print(f"{l}\t{selector(l)}")
        return 0
    if cmd == "reconciler":
        return recon(sys.argv[2:])
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
