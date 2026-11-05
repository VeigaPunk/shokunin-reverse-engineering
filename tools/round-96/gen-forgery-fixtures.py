#!/usr/bin/env python3
"""gen-forgery-fixtures.py - author the six round-96 unbound-field forged receipt triples.

Each triple violates exactly ONE of the bindings kill-rule-v2's K-forgeries check asserts,
so the refusal must carry exactly one typed reason (the v6 counter's reason vocabulary):

  forge-unlabelled     counts missing `fresh_scored`      -> counts-missing-key:fresh_scored
  forge-met-lying      met_target false, label == expect  -> met-not-recomputed
  forge-head-mismatch  head != revision (both valid hex)  -> head-not-bound
  forge-counter-pin    counter_sha256 != these bytes      -> counter-pin-not-bound
  forge-verdict-pin    verdict_sha256 != v3 bytes         -> verdict-pin-not-bound
  forge-repair-pin     repair_sha256 != repair bytes      -> repair-pin-not-bound

The honest pins, the world revision and the repair digest are computed from the live lane
at generation time (`--rev` names the revision baked into every fixture's revision/head
fields). Every other field stays honest, so a counter that passes one of these triples has
admitted a receipt lying about exactly one field.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os

FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
COUNTS = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
          "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", required=True)
    ap.add_argument("--rev", required=True, help="revision baked into revision/head")
    ap.add_argument("--counter", default="tools/round-96/stop-boundary-repair-battery-v6.py")
    ap.add_argument("--verdict", default="tools/round-93/stop-boundary-repair-battery-v3.py")
    ap.add_argument("--repair", default="tools/round-92/upx-stop-boundary-search-repair.py")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    os.makedirs(args.out, exist_ok=True)
    pins = {"counter": sha256_file(os.path.join(root, args.counter)),
            "verdict": sha256_file(os.path.join(root, args.verdict)),
            "repair": sha256_file(os.path.join(root, args.repair))}
    honest = {"class": "forgery fixture", "label": FROZEN_LABEL, "met_target": True,
              "exit": 0, "counts": dict(COUNTS), "revision": args.rev,
              "head": args.rev, "counter_sha256": pins["counter"],
              "verdict_sha256": pins["verdict"], "repair_sha256": pins["repair"]}
    fixtures = {
        "unlabelled": dict(honest, met_target=False, exit=1,
                           counts={k: v for k, v in COUNTS.items()
                                   if k != "fresh_scored"}),
        "met-lying": dict(honest, met_target=False, exit=1),
        "head-mismatch": dict(honest, head="a" * 40),
        "counter-pin": dict(honest, counter_sha256="0" * 64),
        "verdict-pin": dict(honest, verdict_sha256="f" * 64),
        "repair-pin": dict(honest, repair_sha256="0123456789abcdef" * 4),
    }
    for name, rec in fixtures.items():
        base = os.path.join(args.out, "forge-%s" % name)
        with open(base + ".json", "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
            fh.write("\n")
        with open(base + ".stdout", "w", encoding="utf-8") as fh:
            fh.write("%s met %s exit %d\n" % (rec["label"], rec["met_target"],
                                              rec["exit"]))
        with open(base + ".rc", "w", encoding="utf-8") as fh:
            fh.write("%d\n" % rec["exit"])
    print(json.dumps({"out": args.out, "rev": args.rev, "pins": pins}, indent=1,
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
