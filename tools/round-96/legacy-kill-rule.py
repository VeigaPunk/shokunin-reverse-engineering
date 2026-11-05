#!/usr/bin/env python3
"""legacy-kill-rule.py - the round-95 frozen kill rule, formalized (R96-C1 before arm).

Re-measures, with one committed receipt, the round-95 finding M95-h: the frozen round-95
kill rule - the four checks MutationC1 ran per mutant - kills only 5 of the 10 round-95
mutants. The checks are exactly the round-95 rule's surface; nothing from kill rule v2
(main()-level negative control, fsync count, probe receipt check, no-json-out refusal)
is used here:

  (i)   the mutated round-95 counter's `--selftest` exits 0;
  (ii)  the mutated round-95 agreement instrument's `--selftest` exits 0;
  (iii) the forgery battery's `--selftest` exits 0 (run from a copy so its HERE-relative
        import exercises the mutated agreement copy);
  (iv)  the forgery battery over the committed round-95 fixtures exits 0 (before admits,
        after refuses, honest accepted - run from the same copy).

A mutant is killed when any applicable check exits non-zero. The round-95 mutants are the
committed one-line diffs `.ufo/waves/round-95/w1/MutationC1/mutant-diffs/M{1..10}.diff`,
applied with `git apply` inside a scratch copy tree (the lane is never mutated).

Exit 1 with `met false` is the EXPECTED honest outcome (5 of 10): the before side of
R96-C1. Exit 0 would falsify the claim's premise (the r95 rule would already cover the
survivors). Exit 2 = could-not-evaluate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

TOOL = "tools/round-96/legacy-kill-rule.py"
V5 = "tools/round-95/stop-boundary-repair-battery-v5.py"
V2 = "tools/round-95/c1-agreement-v2.py"
BATTERY = "tools/round-95/c1-forgery-refusal.py"
PROBE = "tools/round-95/symlink-probe.py"
TOTAL_MUTANTS = 10


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(cmd: list, timeout: int = 600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def build_mutant(name: str, diff: str, root: str, work: str) -> str:
    d = os.path.join(work, "mut-%s" % name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for rel in (V5, V2, BATTERY, PROBE,
                "tools/round-93/stop-boundary-repair-battery-v3.py",
                "tools/round-94/c1-receipt-agreement.py",
                "tools/round-92/stop-boundary-repair-battery.py",
                "tools/round-92/stop-boundary-battery-v2.py"):
        dst = os.path.join(d, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(root, rel), dst)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True, timeout=60)
    diff_abs = os.path.abspath(diff)
    p = subprocess.run(["git", "-C", d, "apply", diff_abs],
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        p = subprocess.run(["patch", "-p1", "--silent", "-d", d, "-i", diff_abs],
                           capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError("mutant %s: apply failed: %s" % (name, p.stderr[-300:]))
    return d


def checks_for(d: str, root: str, work: str, fixtures: str, prefix: str,
               expect: str) -> dict:
    out = {}
    rc, _, _ = run([sys.executable, "-I", "-B", os.path.join(d, V5),
                    "--selftest", "--work", os.path.join(work, "i")], 300)
    out["i-counter-selftest"] = {"exit": rc, "ok": rc == 0}
    rc, _, _ = run([sys.executable, "-I", "-B", os.path.join(d, V2),
                    "--selftest", os.path.join(work, "ii")], 300)
    out["ii-agreement-selftest"] = {"exit": rc, "ok": rc == 0}
    rc, _, _ = run([sys.executable, "-I", "-B", os.path.join(d, BATTERY),
                    "--selftest", os.path.join(work, "iii")], 300)
    out["iii-forgery-selftest"] = {"exit": rc, "ok": rc == 0}
    rc, _, _ = run([sys.executable, "-I", "-B", os.path.join(d, BATTERY),
                    "--root", root, "--fixtures", fixtures, "--old-prefix", prefix,
                    "--old-counter", "tools/round-94/c1-receipt-agreement.py",
                    "--honest-dir", ".ufo/waves/round-95/l1/scores",
                    "--honest-prefix", "honest",
                    "--world-rev", "b5331db1fb0ce0bf93695ce1730cf831effef6a9",
                    "--instrument-rev", "4bda1d1dd3788973f10e61212b70df18b3b14ea0",
                    "--expect", expect,
                    "--json-out", os.path.join(work, "iv-forgery.json")], 300)
    out["iv-forgery-battery"] = {"exit": rc, "ok": rc == 0}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--work", required=True)
    ap.add_argument("--mutant-diffs", default=".ufo/waves/round-95/w1/MutationC1/mutant-diffs")
    ap.add_argument("--fixtures", default=".ufo/waves/round-95/forgery")
    ap.add_argument("--prefix", default="forge")
    ap.add_argument("--expect", default=("repaired 12 of 12; wrong 0; unsafe 0; "
                                         "intact 6 of 6; far-refused 12 of 12; "
                                         "fresh-roundtrip 2 of 2"))
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    os.makedirs(os.path.abspath(args.work), exist_ok=True)
    diffs = sorted(f for f in os.listdir(args.mutant_diffs) if f.endswith(".diff"))
    if len(diffs) != TOTAL_MUTANTS:
        print("legacy-rule: expected %d diffs, found %d" % (TOTAL_MUTANTS, len(diffs)),
              file=sys.stderr)
        return 2
    rows = []
    for f in diffs:
        name = f[:-len(".diff")]
        d = build_mutant(name, os.path.join(args.mutant_diffs, f), root, args.work)
        cks = checks_for(d, root, os.path.join(args.work, name), args.fixtures,
                         args.prefix, args.expect)
        killed = any(not c["ok"] for c in cks.values())
        rows.append({"name": name, "killed": killed, "checks": cks})
    killed_n = sum(1 for r in rows if r["killed"])
    met = killed_n == TOTAL_MUTANTS
    receipt = {
        "class": "R96-C1 before arm: the round-95 frozen kill rule",
        "counter": TOOL,
        "counter_sha256": sha256_file(os.path.abspath(__file__)),
        "world_revision": subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                                         capture_output=True, text=True,
                                         timeout=30).stdout.strip(),
        "mutant_diffs": args.mutant_diffs,
        "rows": rows,
        "counts": {"killed": killed_n, "mutants": TOTAL_MUTANTS},
        "label": "r95-rule mutants killed %d of %d" % (killed_n, TOTAL_MUTANTS),
        "met_target": met,
        "expected": "met false (5 of 10) - exit 1 is the honest before side",
        "exit": 0 if met else 1,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    print("r95-rule mutants killed %d of %d met %s exit %d"
          % (killed_n, TOTAL_MUTANTS, met, 0 if met else 1))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
