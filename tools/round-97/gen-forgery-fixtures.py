#!/usr/bin/env python3
"""gen-forgery-fixtures.py - round-97 forgery fixtures for R97-C1.

Generates the 13 unbound-field forgery receipts the kill rule's K-forgeries check
requires, baking the pins of the LIVE v7 counter bytes at generation time. Six carry
the round-96 refusal classes (regression), seven carry the round-97 closures
(met-not-typed x2, counts-extra-key, repair-cmd-not-bound, imported-pin-not-bound,
public-met-not-bound, public-label-not-bound). Run AFTER the last instrument byte
change, then regenerate pins.sha256 (stale fixture pins false-refuse every forgery -
the round-96 lesson).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
V7 = "tools/round-97/stop-boundary-repair-battery-v7.py"
V3 = "tools/round-93/stop-boundary-repair-battery-v3.py"
REPAIR = "tools/round-92/upx-stop-boundary-search-repair.py"
R92_BATTERY = "tools/round-92/stop-boundary-repair-battery.py"
R92_V2 = "tools/round-92/stop-boundary-battery-v2.py"
OUTDIR = os.path.join(ROOT, ".ufo/waves/round-97/forgery")

FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
COUNTS = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
          "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}


def sha(path: str) -> str:
    with open(os.path.join(ROOT, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    os.makedirs(OUTDIR, exist_ok=True)
    pins = {"counter": sha(V7), "verdict": sha(V3), "repair": sha(REPAIR),
            "imported_r92_battery_sha256": sha(R92_BATTERY),
            "imported_v2_sha256": sha(R92_V2)}
    rev = "e" * 40

    def base(**over):
        rec = {"class": "R97-C1 forgery fixture", "label": FROZEN_LABEL,
               "met_target": True, "exit": 0, "counts": dict(COUNTS),
               "revision": rev, "head": rev,
               "counter_sha256": pins["counter"],
               "verdict_sha256": pins["verdict"],
               "repair_sha256": pins["repair"],
               "imported_r92_battery_sha256": pins["imported_r92_battery_sha256"],
               "imported_v2_sha256": pins["imported_v2_sha256"],
               "repair_cmd": REPAIR,
               "public_met": True, "public_label": FROZEN_LABEL,
               "fresh_cells": []}
        rec.update(over)
        return rec

    fixtures = {
        # round-96 classes (regression; refused by v6 as well)
        "unlabelled": base(counts={k: v for k, v in COUNTS.items()
                                   if k != "fresh_scored"}),
        "met-lying": base(met_target=False, exit=1, public_met=False),
        "head-mismatch": base(head="a" * 40),
        "counter-pin": base(counter_sha256="0" * 64),
        "verdict-pin": base(verdict_sha256="0" * 64),
        "repair-pin": base(repair_sha256="0" * 64),
        # round-97 closures (accepted by v6, refused by v7)
        "met-null": base(met_target=None, public_met=None),
        "met-str": base(met_target="true", public_met="true"),
        "counts-extra": base(counts=dict(COUNTS, forged=1)),
        "repair-cmd": base(repair_cmd="tools/round-87/upx-magic-repair.py"),
        "imported-pin": base(imported_r92_battery_sha256="0" * 64),
        "public-met": base(public_met=False),
        "public-label": base(public_label="repaired 0 of 0"),
    }
    for name, rec in fixtures.items():
        path = os.path.join(OUTDIR, "forge-%s.json" % name)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("wrote %s" % os.path.relpath(path, ROOT))
    print("pins: %s" % json.dumps(pins, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
