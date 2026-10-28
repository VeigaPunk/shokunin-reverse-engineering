#!/usr/bin/env python3
"""Probe: what the FROZEN-3182047 battery computes once its dead name is patched.

The frozen `m_self_refs` calls `REF`, which is not defined in that file (NameError,
uncaught).  This probe rebinds `attest.REF` to `attest.HARD_REF` in memory — the
later fix did the equivalent by rewriting the mutation — so the remaining battery
behaviour can be measured.  The patch is in memory only; the frozen file is untouched.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "frozen"))
import attest  # noqa: E402

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
REV = "HEAD"

attest.REF = attest.HARD_REF
code, rec = attest.evaluate(ROOT, FREEZE, REV, "r46", "v2", with_battery=True)
battery = rec.get("battery") or {}
out = {
    "probe": "frozen-battery-with-REF-patched",
    "exit": code,
    "met_target": rec.get("met_target"),
    "failing": rec.get("failing"),
    "structural": {k: rec.get(k) for k in ("rule_blocks", "rows", "refs",
                                           "marker_occurrences")},
    "battery": {k: battery.get(k) for k in ("forgeries_total", "v1_green", "v2_green",
                                            "v2_crash", "genuine_green", "genuine_exit")},
    "fixtures": [{"name": f.get("name"), "v1_exit": f.get("v1_exit"),
                  "v2_exit": f.get("v2_exit"),
                  "v1_failing": f.get("v1_failing")} for f in battery.get("fixtures", [])],
}
print(json.dumps(out, indent=1, sort_keys=True))
