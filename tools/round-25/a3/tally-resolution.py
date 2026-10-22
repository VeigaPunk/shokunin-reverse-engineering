#!/usr/bin/env python3
"""Round 25 (attempt 3) C2 evidence: tally selector-name resolution over saved lookups.

Offline only. For every carrier row in corpus/evidence/round-25/a2/c2/carriers.tsv,
runs tools/round-25/a2/resolve-selectors.py analyze over the saved REA 6.5.0
envelope, the saved 4byte.directory and openchain responses and the carrier's
compiler ABI (ground truth), then counts how often each naming rule returns the
ABI name. Selector rows are counted per carrier (69) and, separately, per distinct
selector (deduplicated by selector hex).

Usage: python3 -I -B tools/round-25/a3/tally-resolution.py --root <lane> [--out DIR]
With --out, writes DIR/<carrier>.json (the analyze output) and DIR/tally.json.
Prints the tally JSON. Exit 0 when every analyze run exits 0, 1 otherwise.
"""
import argparse
import json
import os
import subprocess
import sys

EVID = "corpus/evidence/round-25/a2/c2"
RESOLVER = "tools/round-25/a2/resolve-selectors.py"

RULES = {
    "fourbyte_first": "first 4byte.directory result (API default order)",
    "fourbyte_sole_args_consistent": "the only 4byte candidate whose keccak and parameter list match REA",
    "openchain_first": "first openchain result (filter=false response order)",
    "openchain_sole_unfiltered": "the only openchain candidate with filtered=false",
    "openchain_sole_unfiltered_args_consistent": "the only openchain candidate with filtered=false whose parameter list matches REA",
}


def rule_outputs(row):
    """Name each rule returns for one selector row, or None when it returns nothing."""
    out = {}
    fb = row["databases"].get("4byte")
    oc = row["databases"].get("openchain")
    fbd = fb["detail"] if fb else []
    ocd = oc["detail"] if oc else []
    out["fourbyte_first"] = fbd[0]["text"] if fbd else None
    c = [x["text"] for x in fbd if x["label"] == "consistent"]
    out["fourbyte_sole_args_consistent"] = c[0] if len(c) == 1 else None
    out["openchain_first"] = ocd[0]["text"] if ocd else None
    u = [x for x in ocd if x.get("filtered") is False]
    out["openchain_sole_unfiltered"] = u[0]["text"] if len(u) == 1 else None
    ua = [x["text"] for x in u if x["label"] == "consistent"]
    out["openchain_sole_unfiltered_args_consistent"] = ua[0] if len(ua) == 1 else None
    return out


def tally(rows):
    t = {"selector_rows": len(rows),
         "no_candidate_in_either_database": sum(
             1 for r in rows
             if not any(r["databases"].get(db) and r["databases"][db]["candidates"] for db in ("4byte", "openchain"))),
         "truth_in_some_database": sum(
             1 for r in rows
             if any(r["databases"].get(db) and r["databases"][db]["truth_present"] for db in ("4byte", "openchain"))),
         "keccak_mismatch_candidates": sum(
             r["databases"][db]["keccak_mismatch"] for r in rows for db in ("4byte", "openchain") if r["databases"].get(db)),
         "rules": {}}
    for k, desc in RULES.items():
        named = right = wrong = 0
        for r in rows:
            got = rule_outputs(r)[k]
            if got is None:
                continue
            named += 1
            if got == r["abi_signature"]:
                right += 1
            else:
                wrong += 1
        t["rules"][k] = {"rule": desc, "named": named, "right": right, "wrong": wrong,
                         "no_name": len(rows) - named}
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    rows, per, ok = [], {}, True
    with open(os.path.join(root, EVID, "carriers.tsv"), encoding="utf-8") as f:
        carriers = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]
    for name, _hex, abi in carriers:
        p = subprocess.run([sys.executable, "-I", "-B", os.path.join(root, RESOLVER), "analyze",
                            "--envelope", os.path.join(root, EVID, name, "envelope.json"),
                            "--responses", os.path.join(root, EVID, name, "db"),
                            "--abi", os.path.join(root, abi)], capture_output=True, text=True)
        if p.returncode != 0:
            ok = False
            per[name] = {"exit": p.returncode, "stderr": p.stderr[-400:]}
            continue
        d = json.loads(p.stdout)
        if a.out:
            os.makedirs(a.out, exist_ok=True)
            with open(os.path.join(a.out, f"{name}.json"), "w", encoding="utf-8") as g:
                g.write(p.stdout)
        for r in d["rows"]:
            r["carrier"] = name
        rows += d["rows"]
        per[name] = {"exit": 0, "selectors": len(d["rows"])}
    distinct = {}
    for r in rows:
        distinct.setdefault(r["selector"], r)
    wrong_examples = []
    for r in rows:
        for k, got in rule_outputs(r).items():
            if got is not None and got != r["abi_signature"]:
                wrong_examples.append({"carrier": r["carrier"], "selector": r["selector"], "rule": k,
                                       "returned": got, "abi": r["abi_signature"]})
    result = {"carriers": per, "per_carrier_rows": tally(rows),
              "distinct_selectors": tally(list(distinct.values())),
              "wrong_names": wrong_examples,
              "no_candidate_selectors": sorted({(r["selector"], r["abi_signature"]) for r in rows
                                                if not any(r["databases"].get(db) and r["databases"][db]["candidates"]
                                                           for db in ("4byte", "openchain"))})}
    if a.out:
        with open(os.path.join(a.out, "tally.json"), "w", encoding="utf-8") as g:
            json.dump(result, g, indent=1)
    print(json.dumps(result, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
