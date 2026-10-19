#!/usr/bin/env python3
"""RV-1 r3 — decoy (false-positive pressure) audit.

Compiles a carrier, scans EVERY PUSH4 immediate in the deployed code with my
own linear scanner, computes the carrier's declared custom-error selectors with
my own keccak (path A, cross-checked with js-sha3 path B), and classifies each
immediate: in the planted set / an error selector / other.  Reported so the
probe's "zero extras" result can be judged against the decoy pressure that
actually exists in the bytes.
"""
import argparse
import re
import subprocess
import sys
import json
import os
import hashlib

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import keccak_slice as K  # noqa: E402
from scan_push4 import disasm_push4  # noqa: E402

ENV = dict(os.environ, TMPDIR="/var/tmp/rv1-r3")


def compile_src(src, optimize, runs):
    extra = ["--optimize", "--optimize-runs", str(runs)] if optimize else []
    r = subprocess.run(["node", os.path.join(TOOLS, "solc_methodids.js"), src] + extra,
                       capture_output=True, text=True, env=ENV)
    if r.returncode:
        raise SystemExit("solc error: " + r.stderr[:500])
    out = json.loads(r.stdout)
    return out


def parse_errors(src):
    txt = open(src).read()
    errs = []
    for m in re.finditer(r"\berror\s+(\w+)\s*\(([^)]*)\)\s*;", txt):
        name, args = m.group(1), m.group(2).strip()
        types = [a.strip().split()[0] for a in args.split(",")] if args else []
        errs.append(f"{name}({','.join(types)})")
    return sorted(set(errs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--planted", required=True)
    ap.add_argument("--optimize", action="store_true")
    ap.add_argument("--optimize-runs", type=int, default=200)
    ap.add_argument("--contract")
    args = ap.parse_args()

    out = compile_src(args.src, args.optimize, args.optimize_runs)
    contracts = out["contracts"]
    cname = args.contract or max(contracts, key=lambda n: len(contracts[n]["methodIdentifiers"]))
    c = contracts[cname]
    code = bytes.fromhex(c["deployedBytecode"])
    planted = set()
    for raw in open(args.planted):
        t = raw.strip().split()[0].replace("0x", "") if raw.strip() and not raw.strip().startswith("#") else ""
        if re.fullmatch(r"[0-9a-fA-F]{8}", t or ""):
            planted.add(t.lower())
    if args.planted.endswith(".json"):
        d = json.load(open(args.planted))
        planted = set()
        for row in (d.get("functions") or d.get("rows") or d.get("entries") or []):
            planted.add(str(row.get("selector", "")).replace("0x", "").lower())
        for s in d.get("selectors") or []:
            planted.add(str(s).replace("0x", "").lower())

    errs = parse_errors(args.src)
    err_sels = {K.selector(e): e for e in errs}
    # js-sha3 cross-check of the error selectors
    for sel, sig in err_sels.items():
        r = subprocess.run(["node", os.path.join(TOOLS, "js_keccak.js"), "/dev/stdin"],
                           input=sig + "\n", capture_output=True, text=True, env=ENV)
        js = r.stdout.strip().splitlines()[-1].split()[0] if r.stdout.strip() else "?"
        assert js == sel, f"keccak path disagreement on {sig}: A={sel} B={js}"

    sites = disasm_push4(code)
    print(f"# carrier={cname} src={args.src}")
    print(f"# source sha256={hashlib.sha256(open(args.src,'rb').read()).hexdigest()}")
    print(f"# deployed sha256={hashlib.sha256(code).hexdigest()} bytes={len(code)} optimize={args.optimize} runs={args.optimize_runs}")
    print(f"# planted K={len(planted)}  error-selector candidates={len(err_sels)} {err_sels}")
    print(f"# PUSH4 sites total={len(sites)}")
    seen_dispatch = 0
    for pc, imm in sites:
        s = f"{imm:08x}"
        if s in planted:
            kind = "PLANTED"
            seen_dispatch += 1
        elif s in err_sels:
            kind = f"DECOY-error({err_sels[s]})"
        else:
            kind = "other"
        print(f"  0x{s}@{pc} {kind}")
    print(f"# planted immediates present in code: {seen_dispatch}/{len(planted)}"
          f"  (absent: {sorted(planted - {f'{i:08x}' for _, i in sites})})")
    decoys = [f"{i:08x}" for _, i in sites if f"{i:08x}" in err_sels]
    print(f"# decoy error selectors materialized as PUSH4 constants: {decoys}")
    not_in_dispatch = [f"{i:08x}" for _, i in sites if f"{i:08x}" not in planted and f"{i:08x}" not in err_sels]
    print(f"# other PUSH4 constants (non-planted, non-error): {not_in_dispatch}")


if __name__ == "__main__":
    main()