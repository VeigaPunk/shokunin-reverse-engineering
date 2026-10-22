#!/usr/bin/env python3
"""Resolve REA-recovered EVM selectors to candidate text signatures, with checks.

Round 25 (attempt 2), kaidoku. Standard library only. The Keccak-256 sponge is
adapted from .ufo/waves/arc3-loop1-round1/claims/c1/RV-1/keccak_ref.py
(written from the Keccak reference; Ethereum pad byte 0x01).

Subcommands
  selftest                      fixed vectors, including a SHA3-256 negative control
  fetch   --envelope E --out D  query 4byte.directory (all pages) and openchain
                                (filter=false) for every selector in a REA
                                inspect-evm-interface envelope; save each raw
                                response with UTC time and sha256 in D/manifest.json
  analyze --envelope E --responses D [--abi A]
                                offline replay over saved responses; labels every
                                candidate and, when an ABI is given, scores the
                                ground truth. Never outputs a single "the name".

Candidate labels
  keccak-mismatch      keccak256(text)[:4] != selector: a database error
  args-mismatch        keccak matches, but the candidate's parameter list differs
                       from REA's inferred_arguments for that selector
  consistent           keccak matches and the parameter list equals REA's inference
A `consistent` candidate is still an inference: a 32-bit selector can collide.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

MASK64 = (1 << 64) - 1
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROT = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14]


def _rol(v, n):
    n %= 64
    return v & MASK64 if n == 0 else ((v << n) | (v >> (64 - n))) & MASK64


def _f1600(a):
    for rnd in range(24):
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rol(a[x + 5 * y], ROT[x + 5 * y])
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y] & MASK64)
        a[0] ^= RC[rnd]


def keccak256(data):
    rate = 136
    p = bytearray(data)
    p.append(0x01)
    while len(p) % rate:
        p.append(0)
    p[-1] |= 0x80
    a = [0] * 25
    for off in range(0, len(p), rate):
        for i in range(rate // 8):
            a[i] ^= int.from_bytes(p[off + 8 * i:off + 8 * i + 8], "little")
        _f1600(a)
    return b"".join(a[i].to_bytes(8, "little") for i in range(4))


def selector_of(text):
    return keccak256(text.encode("utf-8"))[:4].hex()


def params_of(text):
    """Top-level parameter list of 'name(a,b,(c,d)[])' as written, without spaces."""
    i = text.find("(")
    if i < 0 or not text.endswith(")"):
        return None
    return text[i + 1:-1].replace(" ", "")


def canon_type(p):
    t = p["type"]
    if t.startswith("tuple"):
        return "(" + ",".join(canon_type(c) for c in p.get("components", [])) + ")" + t[len("tuple"):]
    return t


def abi_signatures(abi):
    if isinstance(abi, dict):
        abi = abi.get("abi", abi.get("output", []))
    out = {}
    for e in abi:
        if e.get("type") == "function":
            sig = e["name"] + "(" + ",".join(canon_type(p) for p in e.get("inputs", [])) + ")"
            out[selector_of(sig)] = sig
    return out


def envelope_functions(path):
    with open(path, encoding="utf-8") as f:
        env = json.load(f)
    fns = env["normalized_result"]["functions"]
    return env.get("evidence_id"), [
        {"selector": fn["selector"].lower().removeprefix("0x"),
         "inferred_arguments": fn.get("inferred_arguments"),
         "inferred_state_mutability": fn.get("inferred_state_mutability")} for fn in fns]


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "kaidoku-shokunin/round-25 (research)",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def cmd_fetch(a):
    os.makedirs(a.out, exist_ok=True)
    _, fns = envelope_functions(a.envelope)
    manifest = []
    for fn in fns:
        sel = fn["selector"]
        url = f"https://www.4byte.directory/api/v1/signatures/?hex_signature=0x{sel}"
        page = 0
        while url:
            status, body = _get(url)
            name = f"4byte-{sel}-p{page}.json"
            with open(os.path.join(a.out, name), "wb") as f:
                f.write(body)
            manifest.append({"file": name, "url": url, "status": status,
                             "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "sha256": hashlib.sha256(body).hexdigest()})
            url = json.loads(body).get("next")
            page += 1
            time.sleep(1.1)
        url = f"https://api.openchain.xyz/signature-database/v1/lookup?function=0x{sel}&filter=false"
        status, body = _get(url)
        name = f"openchain-{sel}.json"
        with open(os.path.join(a.out, name), "wb") as f:
            f.write(body)
        manifest.append({"file": name, "url": url, "status": status,
                         "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "sha256": hashlib.sha256(body).hexdigest()})
        time.sleep(1.1)
    with open(os.path.join(a.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(json.dumps({"fetched": len(manifest), "out": a.out}))
    return 0


def _load_candidates(d, sel):
    fourbyte, page = [], 0
    while os.path.exists(os.path.join(d, f"4byte-{sel}-p{page}.json")):
        with open(os.path.join(d, f"4byte-{sel}-p{page}.json"), encoding="utf-8") as f:
            body = json.load(f)
        fourbyte += [{"text": r["text_signature"], "id": r.get("id"), "created_at": r.get("created_at")}
                     for r in body.get("results", [])]
        page += 1
    oc_path = os.path.join(d, f"openchain-{sel}.json")
    openchain = None
    if os.path.exists(oc_path):
        with open(oc_path, encoding="utf-8") as f:
            body = json.load(f)
        rows = ((body.get("result") or {}).get("function") or {}).get("0x" + sel) or []
        openchain = [{"text": r["name"], "filtered": r.get("filtered"),
                      "hasVerifiedContract": r.get("hasVerifiedContract")} for r in rows]
    return (fourbyte if page else None), openchain


def _label(text, sel, inferred):
    if selector_of(text) != sel:
        return "keccak-mismatch"
    if inferred is not None and params_of(text) != inferred.replace(" ", ""):
        return "args-mismatch"
    return "consistent"


def cmd_analyze(a):
    evid, fns = envelope_functions(a.envelope)
    truth = {}
    if a.abi:
        with open(a.abi, encoding="utf-8") as f:
            truth = abi_signatures(json.load(f))
    rows = []
    for fn in fns:
        sel = fn["selector"]
        fb, oc = _load_candidates(a.responses, sel)
        row = {"selector": sel, "inferred_arguments": fn["inferred_arguments"],
               "abi_signature": truth.get(sel), "databases": {}}
        for db, cands in (("4byte", fb), ("openchain", oc)):
            if cands is None:
                row["databases"][db] = None
                continue
            for c in cands:
                c["label"] = _label(c["text"], sel, fn["inferred_arguments"])
            consistent = [c["text"] for c in cands if c["label"] == "consistent"]
            row["databases"][db] = {
                "candidates": len(cands),
                "keccak_mismatch": sum(c["label"] == "keccak-mismatch" for c in cands),
                "args_mismatch": sum(c["label"] == "args-mismatch" for c in cands),
                "consistent": consistent,
                "first_candidate": cands[0]["text"] if cands else None,
                "truth_present": (truth.get(sel) in [c["text"] for c in cands]) if sel in truth else None,
                "truth_first": (cands[0]["text"] == truth.get(sel)) if (sel in truth and cands) else (False if sel in truth else None),
                "truth_sole_consistent": (consistent == [truth.get(sel)]) if sel in truth else None,
                "detail": cands,
            }
        rows.append(row)

    def tally(db, key):
        return sum(1 for r in rows if r["databases"].get(db) and r["databases"][db].get(key) is True)

    summary = {"envelope_evidence_id": evid, "selectors": len(rows),
               "abi_functions_matched": sum(1 for r in rows if r["abi_signature"])}
    for db in ("4byte", "openchain"):
        present = [r for r in rows if r["databases"].get(db)]
        summary[db] = {
            "selectors_with_any_candidate": sum(1 for r in present if r["databases"][db]["candidates"] > 0),
            "truth_present": tally(db, "truth_present"),
            "truth_first": tally(db, "truth_first"),
            "truth_sole_consistent": tally(db, "truth_sole_consistent"),
            "selectors_with_collisions": sum(1 for r in present if r["databases"][db]["candidates"] - r["databases"][db]["keccak_mismatch"] > 1),
            "keccak_mismatch_rows": sum(r["databases"][db]["keccak_mismatch"] for r in present),
            "args_mismatch_rows": sum(r["databases"][db]["args_mismatch"] for r in present),
        }
    print(json.dumps({"summary": summary, "rows": rows}, indent=1))
    return 0


def cmd_selftest(_a):
    checks = [
        ("keccak256('')", keccak256(b"").hex(), "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
        ("transfer(address,uint256)", selector_of("transfer(address,uint256)"), "a9059cbb"),
        ("balanceOf(address)", selector_of("balanceOf(address)"), "70a08231"),
        ("transferFrom(address,address,uint256)", selector_of("transferFrom(address,address,uint256)"), "23b872dd"),
        ("approve(address,uint256)", selector_of("approve(address,uint256)"), "095ea7b3"),
        ("multi-block input (200 bytes)", keccak256(b"a" * 200).hex()[:8], None),
        ("tuple canon", canon_type({"type": "tuple[]", "components": [{"type": "address"}, {"type": "uint256"}]}), "(address,uint256)[]"),
    ]
    ok = True
    out = []
    for name, got, want in checks:
        good = want is None or got == want
        ok &= good
        out.append({"check": name, "got": got, "want": want, "ok": good})
    sha3 = hashlib.sha3_256(b"transfer(address,uint256)").hexdigest()[:8]
    neg = sha3 != "a9059cbb"
    ok &= neg
    out.append({"check": "negative control: hashlib.sha3_256 is not Keccak-256", "got": sha3,
                "want": "not a9059cbb", "ok": neg})
    lab = _label("gasprice_bit_ether(int128)", "23b872dd", "address,address,uint256")
    out.append({"check": "known collision is labelled args-mismatch", "got": lab, "want": "args-mismatch",
                "ok": lab == "args-mismatch"})
    ok &= lab == "args-mismatch"
    print(json.dumps({"ok": ok, "checks": out}, indent=1))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    f = sub.add_parser("fetch")
    f.add_argument("--envelope", required=True)
    f.add_argument("--out", required=True)
    n = sub.add_parser("analyze")
    n.add_argument("--envelope", required=True)
    n.add_argument("--responses", required=True)
    n.add_argument("--abi")
    a = ap.parse_args()
    return {"selftest": cmd_selftest, "fetch": cmd_fetch, "analyze": cmd_analyze}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
