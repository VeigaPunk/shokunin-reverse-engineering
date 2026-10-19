#!/usr/bin/env python3
"""verify-planted.py — seat EX-05 (chain c1, arc3-loop1-round4).

Re-derives every claim in planted.txt from the pinned inputs and writes the
evidence files into this seat's directory:

  planted-vs-method-identifiers.txt  Vyper's own method_identifiers.json vs mine
  planted-vs-ex04-planted.txt        EX-04's independent planted-K vs mine
  planted-vs-ex08.txt                EX-08's independent file vs mine
  planted-vs-source-derived.txt      mechanical source derivation vs ABI derivation
  runtime-presence.txt               byte-level presence of each selector
  digest-agreement.txt               full 32-byte digest agreement A vs B
  erc20-absence.txt                  the 8 known ERC-20 selectors absent

All paths are relative to the repo root; run from there:
  python3 .ufo/waves/arc3-loop1-round4/claims/c1/EX-05/verify-planted.py
"""
import hashlib
import json
import os
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SEAT = f"{REPO}/.ufo/waves/arc3-loop1-round4/claims/c1/EX-05"
EX04 = f"{REPO}/.ufo/waves/arc3-loop1-round4/claims/c1/EX-04"
EX02 = f"{REPO}/.ufo/waves/arc3-loop1-round4/claims/c1/EX-02"
EX08 = f"{REPO}/.ufo/waves/arc3-loop1-round4/claims/c1/EX-08"

ERC20 = {
    "transfer(address,uint256)": "a9059cbb",
    "approve(address,uint256)": "095ea7b3",
    "transferFrom(address,address,uint256)": "23b872dd",
    "balanceOf(address)": "70a08231",
    "allowance(address,address)": "dd62ed3e",
    "totalSupply()": "18160ddd",
    "name()": "06fdde03",
    "symbol()": "95d89b41",
}


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sel(sig):
    out = subprocess.run(
        [sys.executable, f"{SEAT}/keccak_ref.py", "--sel", sig],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out


def write(name, text):
    with open(f"{SEAT}/{name}", "w") as f:
        f.write(text)
    print(f"wrote {name}")


def main():
    full = json.load(open(f"{SEAT}/planted-full.json"))
    abi_sel = {e["sig"]: e["selector"][2:] for e in full["entries"]}
    lines = []

    # 0. input pins
    lines.append("input pins (re-derived at this run):")
    lines.append(f"  abi.json              sha256 {sha256_file(f'{EX04}/out/abi.json')}")
    lines.append(f"  method-identifiers    sha256 {sha256_file(f'{EX04}/out/method-identifiers.json')}")
    lines.append(f"  runtime.hex           sha256 {sha256_file(f'{EX04}/out/runtime.hex')}")
    lines.append(f"  planted-full.json     sha256 {sha256_file(f'{SEAT}/planted-full.json')}")
    lines.append("")

    # 1. Vyper's own method-identifiers vs mine
    mi = json.load(open(f"{EX04}/out/method-identifiers.json"))
    mi_norm = {k: v[2:].zfill(8) for k, v in mi.items()}
    mi_funcs = {k: v for k, v in mi_norm.items() if k != "__default__()"}
    mi_raw = {k: v[2:] for k, v in mi.items() if k != "__default__()"}
    mism = {k: (abi_sel.get(k), v) for k, v in mi_funcs.items() if abi_sel.get(k) != v}
    naive = {k: (abi_sel.get(k), v) for k, v in mi_raw.items() if abi_sel.get(k) != v}
    lines.append("== planted-vs-method-identifiers ==")
    lines.append(f"vyper method_identifiers entries: {len(mi)} (incl __default__())")
    lines.append(f"function entries compared: {len(mi_funcs)}")
    lines.append(f"keys equal to ABI-derived sigs: {set(mi_funcs) == set(abi_sel)}")
    lines.append(f"selectors mismatched (after zfill-8 normalization): {mism or 'none'}")
    lines.append(f"selectors mismatched if compared naive (no zfill): {naive or 'none'}")
    lines.append("  NOTE: vyper's method_identifiers emits the 4-byte value with leading")
    lines.append("  zero STRIPPED (e.g. 0xc751377 = 0x0c751377). The naive comparison")
    lines.append("  therefore reports two false mismatches; normalization is required.")
    lines.append("")
    write("planted-vs-method-identifiers.txt", "\n".join(lines))

    # 2. EX-04 planted-K
    p4 = json.load(open(f"{EX04}/evidence/planted-K.json"))
    p4_sel = p4["planted_selectors"]
    lines = ["== planted-vs-ex04-planted =="]
    lines.append(f"EX-04 planted-K sha256 {sha256_file(f'{EX04}/evidence/planted-K.json')}")
    lines.append(f"EX-04 K: {p4['K']} | EX-05 K: {len(abi_sel)}")
    lines.append(f"keys equal: {set(p4_sel) == set(abi_sel)}")
    lines.append(f"selector mismatches: {({k: (abi_sel.get(k), v) for k, v in p4_sel.items() if abi_sel.get(k) != v}) or 'none'}")
    lines.append("")
    write("planted-vs-ex04-planted.txt", "\n".join(lines))

    # 3. EX-08 independent file
    x8 = {}
    for ln in open(f"{EX08}/sigs-CarrierV.selectors.txt"):
        ln = ln.rstrip("\n")
        if not ln.strip():
            continue
        sig, s = ln.split("\t")
        x8[sig] = s
    lines = ["== planted-vs-ex08 =="]
    lines.append(f"EX-08 file sha256 {sha256_file(f'{EX08}/sigs-CarrierV.selectors.txt')}")
    lines.append(f"EX-08 K: {len(x8)} | EX-05 K: {len(abi_sel)}")
    lines.append(f"keys equal: {set(x8) == set(abi_sel)}")
    lines.append(f"selector mismatches: {({k: (abi_sel.get(k), v) for k, v in x8.items() if abi_sel.get(k) != v}) or 'none'}")
    lines.append("")
    write("planted-vs-ex08.txt", "\n".join(lines))

    # 4. source-derived list
    src = set()
    for ln in open("/var/tmp/ex05-r4/siglist-from-source.txt"):
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            src.add(ln)
    lines = ["== planted-vs-source-derived =="]
    lines.append(f"source: {EX04}/src/CarrierV.vy sha256 {sha256_file(f'{EX04}/src/CarrierV.vy')}")
    lines.append(f"source-derived K: {len(src)} | ABI-derived K: {len(abi_sel)}")
    lines.append(f"sets equal: {src == set(abi_sel)}")
    lines.append(f"only in source-derived: {sorted(src - set(abi_sel)) or 'none'}")
    lines.append(f"only in ABI-derived: {sorted(set(abi_sel) - src) or 'none'}")
    lines.append("")
    write("planted-vs-source-derived.txt", "\n".join(lines))

    # 5. runtime presence + PUSH4 census
    runtime = bytes.fromhex(open(f"{EX04}/out/runtime.hex").read().strip())
    missing = [e["selector"] for e in full["entries"] if runtime.find(bytes.fromhex(e["selector"][2:])) < 0]
    push4, i = set(), 0
    while i < len(runtime):
        if runtime[i] == 0x63 and i + 4 < len(runtime):
            push4.add(runtime[i + 1:i + 5].hex())
            i += 5
        else:
            i += 1
    planted = {e["selector"][2:] for e in full["entries"]}
    lines = ["== runtime-presence =="]
    lines.append(f"runtime bytes: {len(runtime)} sha256 {hashlib.sha256(runtime).hexdigest()}")
    lines.append(f"planted selectors absent as byte sequences: {missing or 'none'}")
    lines.append(f"PUSH4 immediates: {len(push4)} | planted among them: {len(planted & push4)}/{len(planted)}")
    lines.append(f"PUSH4 immediates not in planted set: {sorted(push4 - planted)}")
    lines.append("  08c379a0 = Error(string) revert selector (keccak('Error(string)')[:4])")
    lines.append("  69656e74 = ASCII 'ient' fragment of the revert string 'insufficient' (offset 732)")
    lines.append(f"__default__ 89402a72 present as bytes: {runtime.find(bytes.fromhex('89402a72')) >= 0} (fallback = no-match path)")
    lines.append("")
    write("runtime-presence.txt", "\n".join(lines))

    # 6. digest agreement
    bad = [e["sig"] for e in full["entries"] if e["keccak256_js_sha3"] != e["keccak256_node_crypto"]]
    lines = ["== digest-agreement =="]
    lines.append(f"entries: {len(full['entries'])}")
    lines.append(f"full 32-byte digest mismatches (js-sha3 vs node:crypto): {bad or 'none'}")
    lines.append("")
    write("digest-agreement.txt", "\n".join(lines))

    # 7. ERC-20 absence
    present = sorted(set(abi_sel.values()) & set(ERC20.values()))
    lines = ["== erc20-absence =="]
    lines.append(f"known ERC-20 selectors checked: {len(ERC20)}")
    lines.append(f"present in the planted set: {present or 'none'}")
    for k, v in ERC20.items():
        lines.append(f"  {v} {k}")
    lines.append("")
    write("erc20-absence.txt", "\n".join(lines))

    print("all evidence files written")


if __name__ == "__main__":
    main()
