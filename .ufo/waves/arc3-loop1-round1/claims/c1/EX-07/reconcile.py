#!/usr/bin/env python3
"""EX-07 reconciliation driver — selector sets across independent sources.

Sources:
  M1  my dispatch-table parse (selector-recon.py extract: chain + EQ sites)
  M2  my keccak scan over signature strings (selector-recon.py scan)
  ABI solc ABI json -> keccak(sig)[:4]
  PLANTED  planted-K.json / planted-selectors.txt style list
  PROBE    rea inspect-evm-interface evidence json (raw_result.functions)

Usage:
  reconcile.py --code <runtime.hex> <hex|raw> --abi <abi.json> \
      --planted <planted-K.json> --probe <p1.json> [<p2.json> ...] \
      [--sigs <sigs.txt>]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sr", os.path.join(HERE, "selector-recon.py"))
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)


def norm(sels):
    return sorted(s.strip().lower().removeprefix("0x") for s in sels if s and s.strip())


def load_planted(path):
    """Accept planted-K.json (EX-06 shape) or a plain `0x.. sig` list."""
    txt = open(path).read()
    if path.endswith(".json"):
        d = json.loads(txt)
        return norm([f["selector"] for f in d["functions"]]), d
    sels = []
    for line in txt.splitlines():
        line = line.strip()
        if line.startswith("0x"):
            sels.append(line.split()[0])
    return norm(sels), None


def load_probe(path):
    d = json.load(open(path))
    fns = d.get("raw_result", {}).get("functions", [])
    sels = norm([f["selector"] for f in fns])
    offsets = {f["selector"].lower().removeprefix("0x"): f["bytecodeOffset"] for f in fns}
    sha = d.get("normalized_result", {}).get("bytecode", {}).get("sha256")
    return sels, offsets, sha, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", nargs=2, required=True, metavar=("PATH", "ENC"))
    ap.add_argument("--abi")
    ap.add_argument("--planted", required=True)
    ap.add_argument("--probe", nargs="+", default=[])
    args = ap.parse_args()

    code = sr.load_code(args.code[0], args.code[1])
    code_sha = hashlib.sha256(code).hexdigest()
    m1 = sr.extract(code)

    sources = {}
    sources["M1_chain"] = m1["chain_selectors"]
    sources["M1_eq_sites"] = m1["dispatch_selectors"]

    if args.abi:
        abi = json.load(open(args.abi))
        sigs = [e["name"] + "(" + ",".join(i["type"] for i in e["inputs"]) + ")"
                for e in abi if e.get("type") == "function"]
        sources["ABI"] = norm([sr.selector(s) for s in sigs])
        m2 = {s: sr.selector(s) for s in sigs}
    else:
        m2 = {}

    planted, planted_doc = load_planted(args.planted)
    sources["PLANTED"] = planted

    probe_offsets = {}
    for p in args.probe:
        sels, offsets, sha, _ = load_probe(p)
        sources["PROBE:" + os.path.basename(p)] = sels
        probe_offsets[os.path.basename(p)] = offsets

    # M2 keccak scan over ABI signatures: verify each selector's bytes are present
    m2_found = {}
    for sig, sel in m2.items():
        m2_found[sel] = code.hex().find(sel)
    sources["M2_keccak_scan"] = norm([s for s, off in m2_found.items() if off >= 0])

    ref_name = "M1_chain"
    ref = set(sources[ref_name])
    print(f"code: {args.code[0]} ({args.code[1]}), bytes={len(code)}, sha256={code_sha}")
    print(f"M1 dispatcher anchor(s): {m1['dispatcher_anchors']}")
    print(f"M1 chain (push4_site -> JUMPDEST dest):")
    for c in m1["dispatch_chain"]:
        print(f"   {c['selector']}  push4@{c['push4_offset']}  dest={c['dest']}")
    print(f"M1 non-dispatch PUSH4 constants: "
          f"{[p[1] + '@' + str(p[0]) for p in m1['push4_all'] if p[1] not in ref]}")
    print()
    verdict_all = True
    for name, sels in sources.items():
        s = set(sels)
        missing = sorted(ref - s)
        extra = sorted(s - ref)
        ok = s == ref
        verdict_all &= ok
        print(f"{name:28s} n={len(s):2d}  {'MATCH' if ok else 'MISMATCH'}  "
              f"missing={missing} extra={extra}")
    print()
    print("probe offsets vs my parsed JUMPDEST dests:")
    my_dest = {c["selector"]: c["dest"] for c in m1["dispatch_chain"]}
    for pname, offsets in probe_offsets.items():
        mism = {sel: (my_dest.get(sel), off) for sel, off in offsets.items()
                if my_dest.get(sel) != off}
        print(f"  {pname}: {'all offsets equal' if not mism else mism}")
        verdict_all &= not mism
    print()
    print("probe code-digest pins vs my sha256:")
    for p in args.probe:
        _, _, sha, _ = load_probe(p)
        if sha:
            same = sha == code_sha
            verdict_all &= same
            print(f"  {os.path.basename(p)}: pinned={sha} mine={code_sha} {'SAME' if same else 'DIFFER'}")
    print()
    print("VERDICT:", "ALL SOURCES AGREE" if verdict_all else "MISMATCH PRESENT")
    return 0 if verdict_all else 1


if __name__ == "__main__":
    sys.exit(main())
