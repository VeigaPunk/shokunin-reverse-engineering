#!/usr/bin/env python3
"""C1FreezeWindow: clause-7 textual counts using exact.py's OWN constants, plus the
freeze-derivation arms of probe 4 evaluated by gate.freeze_state."""
import hashlib
import json
import os
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402

out = {"exact_ORDER": exact.ORDER, "exact_REVERSED": exact.REVERSED,
       "exact_MUT_DIGEST": exact.MUT_DIGEST,
       "gate_sha256_frozen": hashlib.sha256(
           open(os.path.join(LANE, "tools", "round-46", "gate.py")).read().encode()
       ).hexdigest(),
       "variants": {}}
for name in ("frozen", "reversed", "forged_trailing_m", "forged_trailing_separate",
             "reformatted_correct_order"):
    p = os.path.join(S, "gate_" + name + ".py")
    if name == "frozen":
        p = os.path.join(LANE, "tools", "round-46", "gate.py")
    text = open(p).read()
    out["variants"][name] = {
        "path": p,
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "count_ORDER": text.count(exact.ORDER),
        "count_REVERSED": text.count(exact.REVERSED),
        "clause7_green": text.count(exact.ORDER) == 1 and text.count(exact.REVERSED) == 0,
    }

fx4 = open(os.path.join(S, "fx4-dir.txt")).read().strip()
pinned = open(os.path.join(S, "fx4-pinned.txt")).read().strip()
tip = open(os.path.join(S, "fx4-tip.txt")).read().strip()
derived = open(os.path.join(S, "fx4-derived.txt")).read().strip()
out["fx4"] = {"dir": fx4, "pinned_freeze": pinned, "tip": tip,
              "derived_freeze": derived,
              "derived_equals_pinned": derived == pinned, "arms": {}}
for label, freeze in (("pinned", pinned), ("derived", derived)):
    code, receipt = exact.gate.freeze_state(fx4, freeze, tip,
                                           claims="plans/round-47-claims.md")
    out["fx4"]["arms"][label] = {
        "exit": code, "reason": receipt.get("reason"),
        "frozen_path_changed": receipt.get("frozen_path_changed"),
        "blob_changed": receipt.get("blob_changed"),
        "touched": receipt.get("touched"),
        "restored": receipt.get("restored"),
        "frozen_derived": receipt.get("frozen_derived"),
    }
print(json.dumps(out, indent=1, sort_keys=True))
