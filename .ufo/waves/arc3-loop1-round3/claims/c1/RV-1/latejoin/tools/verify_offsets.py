#!/usr/bin/env python3
"""RV-1 LATE-JOIN — independent verification of the probe offsets and the
input-shape trap legs, plus a mutability cross-check.

For every joined envelope:
  * every `bytecodeOffset` must be a 0x5b (JUMPDEST) byte in the DECODED runtime;
  * for the CarrierA linear-chain carrier, the offset must be the JUMPI target of
    the EQ leg whose PUSH4 immediate is that selector (my own disassembler);
  * probe `inferred_state_mutability` must equal the source-derived mutability.
Trap legs (raw encoding over a hex-TEXT file) must yield functions=[] and a
decoded digest equal to the sha256 of the file's TEXT bytes.
"""
import glob
import hashlib
import json
import os
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
C1 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round3/claims/c1")
sys.path.insert(0, os.path.join(C1, "RV-1/latejoin/tools"))
import keccak_bits as KD  # noqa: E402
from recompute_carriers import extract, push4_sites  # noqa: E402

RUNTIME = {
    "9f7392acccea72cd42bdd8095a8578cab0727766f218b5399da22bc21d23741a":
        ("CarrierA", os.path.join(C1, "EX-02/evidence/carrierA.runtime.hex")),
    "aaf85ceaf124bac2d3a32428927194158c9211e4472a0cf06f88a721cf239412":
        ("VaultB", os.path.join(C1, "EX-04/evidence/carrierB.runtime-opt200.hex")),
    "679678e9a67aee701094a4bfeafd2a02311460658aa4b400202340b47d83d005":
        ("VaultB", os.path.join(C1, "EX-04/evidence/carrierB.runtime-noopt.hex")),
}

SRC = {"CarrierA": os.path.join(C1, "EX-02/carrierA.sol"),
       "VaultB": os.path.join(C1, "EX-04/carrierB.sol")}

codes, mut = {}, {}
for cname, path in SRC.items():
    txt = open(path).read()
    fns = extract(txt, cname)
    mut[cname] = {KD.selector(f["sig"]): f["mutability"] for f in fns}
for bc, (cname, path) in RUNTIME.items():
    t = open(path).read().strip()
    codes[bc] = bytes.fromhex(t[2:] if t.startswith("0x") else t)


def eq_targets(code, sel):
    """Every PC that is the PUSH2 target of an EQ leg for `sel`."""
    sels = {imm: pc for pc, imm in push4_sites(code)}
    if sel not in sels:
        return []
    p = sels[sel]
    # DUP1 PUSH4 <sel> EQ PUSH2 <t> JUMPI  → EQ is p+5, PUSH2 at p+6
    if p + 7 < len(code) and code[p + 5] == 0x14 and code[p + 6] == 0x61:
        return [(code[p + 7] << 8) | code[p + 8]]
    return []


rows = []
traps = []
for p in sorted(glob.glob(os.path.join(C1, "**", "*.json"), recursive=True)):
    base = os.path.basename(p)
    if "probe" not in base and "leg" not in base:
        continue
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    nr = d.get("normalized_result") or {}
    if not isinstance(nr, dict):
        continue
    bc = (nr.get("bytecode") or {}).get("sha256")
    fns = nr.get("functions") or []
    if bc not in RUNTIME:
        # candidate trap leg: decoded digest == sha256 of the file TEXT
        art = nr.get("artifact") or {}
        apath = art.get("path", "")
        if fns == [] and apath and os.path.exists(apath):
            tsha = hashlib.sha256(open(apath, "rb").read()).hexdigest()
            traps.append({"envelope": os.path.relpath(p, C1), "n": len(fns),
                          "decoded_is_filetext": bc == tsha, "bc": bc, "text": tsha})
        continue
    cname = RUNTIME[bc][0]
    code = codes[bc]
    for f in fns:
        sel = str(f["selector"]).replace("0x", "").lower()
        # NOTE: normalized_result uses snake_case (bytecode_offset); raw_result
        # uses camelCase (bytecodeOffset).  My first pass read the camelCase key
        # from the normalized dict and got None for every entry — caught and
        # fixed here (self-inflicted, not a plant defect).
        off = f.get("bytecode_offset", f.get("bytecodeOffset"))
        pmut = f.get("inferred_state_mutability", f.get("stateMutability"))
        rows.append({
            "envelope": os.path.relpath(p, C1), "carrier": cname, "sel": sel,
            "off": off,
            "is_jumpdest": (off is not None and 0 <= off < len(code) and code[off] == 0x5b),
            "eq_targets": eq_targets(code, sel),
            "eq_match": off in eq_targets(code, sel),
            "mut_probe": pmut,
            "mut_src": mut[cname].get(sel),
        })

bad_jd = [r for r in rows if not r["is_jumpdest"]]
bad_mut = [r for r in rows if r["mut_probe"] != r["mut_src"]]
no_eq = [r for r in rows if r["carrier"] == "CarrierA" and not r["eq_match"]]

print(f"entries checked (carrier envelopes x functions): {len(rows)}")
print(f"offsets that are NOT 0x5b JUMPDEST: {len(bad_jd)}")
print(f"mutability mismatches probe-vs-source: {len(bad_mut)}")
print(f"CarrierA entries whose offset != my parsed EQ/JUMPI target: {len(no_eq)}")
print(f"trap-leg candidates found: {len(traps)}")
for t in traps:
    print(f"  {t['envelope']}: functions={t['n']} decoded_digest_is_file_text={t['decoded_is_filetext']}")
if bad_mut:
    for r in bad_mut[:10]:
        print("  MUT", r["envelope"], r["sel"], r["mut_probe"], "!=", r["mut_src"])
if bad_jd:
    for r in bad_jd[:10]:
        print("  JD", r["envelope"], r["sel"], r["off"])
if no_eq:
    for r in no_eq[:10]:
        print("  EQ", r["envelope"], r["sel"], r["off"], "vs", r["eq_targets"])

# eq_match counts by carrier
from collections import Counter
c = Counter((r["carrier"], r["eq_match"]) for r in rows if r["carrier"] == "CarrierA")
print("\nCarrierA eq_match distribution:", dict(c))
json.dump({"rows": rows, "traps": traps}, open("/var/tmp/rv1-latejoin/out/offset-check.json", "w"), indent=2)
