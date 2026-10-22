#!/usr/bin/env python3
"""Round 28 R28-C1: freeze the held-out EVM carrier list before any REA run or lookup.

Selection rule (deterministic, reads only committed bytes at --rev):
  1. Candidate ABI files: every tracked path ending in `abi.json` or `.abi` (not `.stderr`)
     that parses as a JSON ABI holding at least one function.
  2. Pairing: the runtime file is the first tracked path in the ABI's own directory among
     <stem>.runtime.hex, <stem>runtime.hex, <stem>.runtime.hex with a separator added,
     runtime.hex, <stem>.bin-runtime, <stem>.runtime.1.hex, where <stem> is the ABI file
     name without `.abi.json`, `.abi`, `abi.json` or `.json`. ABIs with no paired runtime drop.
  3. Grouping: pairs are grouped by the set of canonical ABI signatures; each group keeps
     its first pair in path order (one carrier per distinct interface).
  4. Held-out filter: a group is kept only if at least one of its selectors is not among
     the round-25 in-sample selectors (every ABI selector of the six carriers in
     corpus/evidence/round-25/a2/c2/carriers.tsv) and its runtime bytes differ from every
     round-25 runtime.
  5. Held-out selectors: the distinct selectors over the kept carriers that are not
     round-25 selectors, each tied to its ABI signature and to the first kept carrier (in
     carrier order) whose ABI holds it.

Writes <out>/carriers.tsv and <out>/heldout.tsv. Prints counts. Exit 0.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

R25 = "corpus/evidence/round-25/a2/c2/carriers.tsv"
RESOLVER = "tools/round-25/a2/resolve-selectors.py"


def show(root, rev, path):
    return subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)], capture_output=True, check=True).stdout


def load_resolver(root, rev):
    src = show(root, rev, RESOLVER)
    spec = importlib.util.spec_from_loader("resolver", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(src, RESOLVER, "exec"), mod.__dict__)
    return mod


def stem_of(base):
    for suf in (".abi.json", ".abi", "abi.json", ".json"):
        if base.endswith(suf):
            return base[: -len(suf)]
    return base


def pair(path, tracked):
    d, b = os.path.split(path)
    s = stem_of(b)
    sep = "" if (not s or s.endswith(("-", ".", "_"))) else "."
    for rt in (s + ".runtime.hex", s + "runtime.hex", s + sep + "runtime.hex", "runtime.hex",
               s + ".bin-runtime", s + ".runtime.1.hex"):
        p = os.path.join(d, rt)
        if p in tracked:
            return p
    return None


def select(root, rev):
    rs = load_resolver(root, rev)
    tracked = set(subprocess.run(["git", "-C", root, "ls-tree", "-r", "--name-only", rev],
                                 capture_output=True, text=True, check=True).stdout.split("\n"))
    r25_sel, r25_rt = set(), set()
    for ln in show(root, rev, R25).decode().splitlines():
        if not ln.strip():
            continue
        _n, h, a = ln.split("\t")
        r25_sel |= set(rs.abi_signatures(json.loads(show(root, rev, a))))
        r25_rt.add(hashlib.sha256(show(root, rev, h)).hexdigest())
    groups = {}
    for p in sorted(tracked):
        if not (p.endswith("abi.json") or p.endswith(".abi")) or p.endswith(".stderr"):
            continue
        try:
            sigs = rs.abi_signatures(json.loads(show(root, rev, p)))
        except Exception:
            continue
        if not sigs:
            continue
        rt = pair(p, tracked)
        if rt is None:
            continue
        key = frozenset(sigs.values())
        groups.setdefault(key, (p, rt, sigs))
    carriers = []
    for key, (abi, rt, sigs) in sorted(groups.items(), key=lambda kv: kv[1][0]):
        rt_sha = hashlib.sha256(show(root, rev, rt)).hexdigest()
        if rt_sha in r25_rt or not (set(sigs) - r25_sel):
            continue
        carriers.append((abi, rt, rt_sha, hashlib.sha256(show(root, rev, abi)).hexdigest(), sigs))
    rows, seen = [], set()
    named = []
    for i, (abi, rt, rt_sha, abi_sha, sigs) in enumerate(carriers, 1):
        name = "h%02d" % i
        named.append((name, rt, abi, rt_sha, abi_sha))
        for sel in sorted(sigs):
            if sel in r25_sel or sel in seen:
                continue
            seen.add(sel)
            rows.append((sel, sigs[sel], name))
    return named, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    named, rows = select(os.path.abspath(a.root), a.rev)
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, "carriers.tsv"), "w", encoding="utf-8") as f:
            f.write("carrier\truntime\tabi\truntime_sha256\tabi_sha256\n")
            for r in named:
                f.write("\t".join(r) + "\n")
        with open(os.path.join(a.out, "heldout.tsv"), "w", encoding="utf-8") as f:
            f.write("selector\tabi_signature\tcarrier\n")
            for r in rows:
                f.write("\t".join(r) + "\n")
    print(json.dumps({"carriers": len(named), "heldout_selectors": len(rows)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
