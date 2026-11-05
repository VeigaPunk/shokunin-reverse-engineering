#!/usr/bin/env python3
"""dirty-v6-admits.py - round-97 BEFORE-side demonstration of the M96-a class.

Builds a scratch clone of the lane at HEAD, dirties the pinned round-96 counter bytes
uncommitted, fakes a green verdict through the module API, and runs the v6 public main:
the receipt's pins match the live (dirty) bytes, self-verification passes, and the run
exits 0 - a receipt naming revision HEAD while measuring bytes HEAD does not contain.
The round-97 kill rule's K-bytes check (frozen) refuses the same scenario on the v7
counter with `byte-pin-not-bound`. Read-only against the lane: the clone lives under
$HYAKU_SCRATCH/kaidoku-r97 and is removed by the caller.
"""

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = os.path.join(
    os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r97",
    "l1", "dirty-demo")
OUT = os.path.join(LANE, ".ufo/waves/round-97/pre/c1-dirty-v6-admits.json")
FROZEN = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
          "far-refused 12 of 12; fresh-roundtrip 2 of 2")
COUNTS = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
          "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}


def main() -> int:
    shutil.rmtree(SCRATCH, ignore_errors=True)
    os.makedirs(SCRATCH, exist_ok=True)
    head = subprocess.check_output(["git", "-C", LANE, "rev-parse", "HEAD"],
                                   text=True).strip()
    clone = os.path.join(SCRATCH, "clone")
    subprocess.run(["git", "clone", "--shared", "--quiet", LANE, clone], check=True)
    target = "tools/round-96/stop-boundary-repair-battery-v6.py"
    with open(os.path.join(clone, target), "a", encoding="utf-8") as fh:
        fh.write("\n# DIRTY-BYTES-FOR-BYTE-BINDING-DEMO\n")
    spec = importlib.util.spec_from_file_location("v6_dirty", os.path.join(clone, target))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.v3.score = (lambda args: (
        0, {"class": "demo", "label": FROZEN, "met_target": True, "exit": 0,
            "counts": dict(COUNTS), "revision": args.rev, "fresh_cells": []}))
    out = os.path.join(SCRATCH, "v6-dirty-receipt.json")
    code = mod.main(["--root", clone, "--work", os.path.join(SCRATCH, "w"),
                     "--rev", head, "--expect", FROZEN, "--json-out", out])
    dirty_sha = hashlib.sha256(open(os.path.join(clone, target), "rb").read()).hexdigest()
    receipt = {
        "class": "R97-C1 before-side: v6 admits the byte lie (M96-a)",
        "world_head": head,
        "dirty_counter_sha256": dirty_sha,
        "v6_dirty_exit": code,
        "v6_admits": code == 0,
        "receipt_revision": head,
        "note": ("the v6 run exits 0 on a dirty tree under the clean revision name; "
                 "the round-97 kill rule refuses the same scenario on v7 "
                 "(byte-pin-not-bound) and requires v6_admitted true as the "
                 "before-side of the frozen dirtyrefuse check"),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
