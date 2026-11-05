#!/usr/bin/env python3
"""allowlist-check.py - round-98 frozen counter for R98-C2 (calibration).

Routed defect 1 of the round-97 non-author closure: the landed v7 counter's
counts allow-list holds nine keys while the verdict it certifies emits
fourteen, so every honest public run exits 1.  This counter scores a
candidate stop-boundary battery counter on four legs:

  public   the candidate's public command on the real battery
           (--expect <frozen v3 label> --json-out <receipt>) exits 0 and
           prints `selfverify ok=True`.
  real14   candidate.count_problems(<the 14-key counts of that public
           receipt>) returns no reason (an honest verdict is accepted).
  stub9    candidate.count_problems(<the nine label keys of those counts>)
           returns >= 1 reason (the round-97 nine-key stub is refused).
  extra    candidate.count_problems(<14-key counts plus key `bogus`>)
           returns >= 1 reason (an unknown key is still refused).

The public receipt's counts feed legs real14/stub9/extra.  When the public
run writes no receipt, the committed round-97 public verdict counts
(.ufo/waves/round-97/l1/public/v6-public.json, produced by v3.score) are used
instead, so a failing public leg cannot zero the other three.

Label: `legs passed K of 4; public P; real14 R; stub9 S; extra E` (each 0/1).
Frozen predicate (R98-C2): label == `legs passed 4 of 4; public 1; real14 1;
stub9 1; extra 1`, exit 0.  Exit 1 otherwise; exit 2 usage/unevaluable.
Scratch: --work is mandatory (no /tmp default).
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

FALLBACK_COUNTS = ".ufo/waves/round-97/l1/public/v6-public.json"
NINE = ("repaired", "scored", "wrong", "unsafe", "intact",
        "far", "far_refused", "fresh_roundtrip", "fresh_scored")
TARGET = "legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True, help="lane-relative candidate path")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    os.makedirs(a.work, exist_ok=True)
    os.chdir(root)
    try:
        cand = load(os.path.join(root, a.counter), "r98_candidate")
        frozen = cand.v3.FROZEN_LABEL
    except Exception as e:  # unevaluable candidate
        print("unevaluable: %r" % (e,), file=sys.stderr)
        return 2
    rec_path = os.path.join(a.work, "public-receipt.json")
    if os.path.exists(rec_path):
        os.unlink(rec_path)
    cmd = [sys.executable, "-I", "-B", a.counter, "--root", root, "--rev", a.rev,
           "--work", os.path.join(a.work, "public"), "--expect", frozen,
           "--json-out", rec_path]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    public = int(p.returncode == 0 and "selfverify ok=True" in p.stdout)
    counts = None
    source = rec_path
    try:
        with open(rec_path) as fh:
            counts = json.load(fh).get("counts")
    except (OSError, ValueError):
        counts = None
    if not isinstance(counts, dict) or len(counts) != 14:
        source = FALLBACK_COUNTS
        with open(os.path.join(root, FALLBACK_COUNTS)) as fh:
            counts = json.load(fh)["counts"]
    real14 = int(cand.count_problems(dict(counts)) == [])
    stub9 = int(len(cand.count_problems({k: counts[k] for k in NINE})) >= 1)
    extra = int(len(cand.count_problems(dict(counts, bogus=0))) >= 1)
    k = public + real14 + stub9 + extra
    label = "legs passed %d of 4; public %d; real14 %d; stub9 %d; extra %d" % (
        k, public, real14, stub9, extra)
    met = label == TARGET
    out = {"tool": "tools/round-98/allowlist-check.py", "counter": a.counter,
           "rev": a.rev, "label": label, "met": met, "exit": 0 if met else 1,
           "counts_source": source, "public_rc": p.returncode,
           "public_stdout": p.stdout[-2000:], "public_stderr": p.stderr[-2000:],
           "cmd": cmd}
    with open(a.json_out, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(label, "met", met)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
