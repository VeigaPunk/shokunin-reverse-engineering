#!/usr/bin/env python3
"""r95-unbound-at-base.py - R96-C1 before arms over the frozen round-95 counter.

Runs the round-95 counter's own `verify_receipt` and `main()` (the bytes are first checked
byte-identical to the base revision via `git show`) over the six round-96 unbound-field
forged receipts and the no-json-out scenario. The expected honest outcome (exit 1, the
before side of R96-C1):

  unbound leg    the round-95 counter ACCEPTS five of the six forgeries (ok true, reasons
                 empty: it never bound head, the counter pin, the verdict pin, the repair
                 pin, or the downward met direction) and CRASHES on the unlabelled-counts
                 forgery with a bare `KeyError` (typed-refusal gap, round-95 named limit 5).
  nojson leg     the round-95 counter's public `main()` on a met-True faked verdict without
                 `--json-out` exits 0 and writes no receipt: self-verification was
                 skippable and a green verdict could exist without any receipt (M95-g).

Exit 0 iff both before behaviours are observed exactly; any other outcome is exit 1 and
falsifies the claim's premise.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-96/r95-unbound-at-base.py"
V5 = "tools/round-95/stop-boundary-repair-battery-v5.py"
FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
COUNTS = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
          "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}
INTENDED = {"unlabelled": "counts-missing-key:fresh_scored",
            "met-lying": "met-not-recomputed",
            "head-mismatch": "head-not-bound",
            "counter-pin": "counter-pin-not-bound",
            "verdict-pin": "verdict-pin-not-bound",
            "repair-pin": "repair-pin-not-bound"}


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", required=True, help="base revision for the pinned bytes")
    ap.add_argument("--fixtures", default=".ufo/waves/round-96/forgery")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    rev = subprocess.run(["git", "-C", root, "rev-parse", "--verify", args.rev],
                         capture_output=True, text=True, timeout=30).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", rev):
        print("cannot resolve %s" % args.rev, file=sys.stderr)
        return 2

    work_bytes = open(os.path.join(root, V5), "rb").read()
    p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, V5)],
                       capture_output=True, timeout=60)
    bytes_identical = p.stdout == work_bytes

    spec = importlib.util.spec_from_file_location("r96_v5_base",
                                                  os.path.join(root, V5))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    rows = []
    for name, intended in INTENDED.items():
        path = os.path.join(args.fixtures, "forge-%s.json" % name)
        with open(path, encoding="utf-8") as fh:
            fixture = json.load(fh)
        try:
            v = mod.verify_receipt(path, FROZEN_LABEL, fixture.get("revision"), 6)
            accepted = bool(v["ok"])
            reasons = v["reasons"]
            error = None
        except Exception as exc:  # the typed-refusal gap: a bare exception
            accepted = False
            reasons = None
            error = "%s: %s" % (type(exc).__name__, exc)
        rows.append({"fixture": "forge-%s" % name, "intended_reason": intended,
                     "accepted": accepted, "reasons": reasons, "error": error,
                     "typed_refusal": bool(reasons)})

    accepted_n = sum(1 for r in rows if r["accepted"])
    crashed_n = sum(1 for r in rows if r["error"])
    unbound_ok = (accepted_n == 5 and crashed_n == 1
                  and all(not r["typed_refusal"] for r in rows))

    # nojson leg: met-True faked verdict, no --json-out -> v5 exits 0, no receipt.
    base = dict(COUNTS)
    def fake(args, _l=FROZEN_LABEL, _c=base):
        return 0, {"class": "before-arm", "label": _l, "met_target": True,
                   "exit": 0, "counts": _c, "revision": args.rev, "fresh_cells": []}
    orig = mod.v3.score
    mod.v3.score = fake
    out_path = None
    try:
        buf_o, buf_e = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_o), contextlib.redirect_stderr(buf_e):
            code = mod.main(["--root", root, "--work", os.path.join(
                     os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                     "kaidoku-r96", "l1", "nojson-work"),
                     "--rev", rev, "--expect", FROZEN_LABEL])
    finally:
        mod.v3.score = orig
    nojson = {"exit": code, "receipt_written": False,
              "note": "no --json-out passed; a receipt path to write does not exist"}
    nojson_ok = code == 0

    met = unbound_ok and nojson_ok and bytes_identical
    receipt = {
        "class": "R96-C1 before arm: the round-95 counter leaves the fields unbound",
        "counter": TOOL,
        "counter_sha256": sha256_file(os.path.abspath(__file__)),
        "target": V5,
        "target_bytes_identical_to_rev": bytes_identical,
        "world_revision": rev,
        "rows": rows,
        "unbound": {"accepted": accepted_n, "crashed": crashed_n,
                    "typed_refusals": 0, "total": 6, "ok": unbound_ok},
        "nojson": nojson,
        "nojson_ok": nojson_ok,
        "expected": "accepted 5 of 6, crash 1 of 6, typed refusals 0, nojson exit 0",
        "label": "unbound accepted %d of 6 (1 crash); nojson exit %d"
                 % (accepted_n, code),
        "met_target": met,
        "exit": 0 if met else 1,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    print(receipt["label"], "met", met, "exit", 0 if met else 1)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
