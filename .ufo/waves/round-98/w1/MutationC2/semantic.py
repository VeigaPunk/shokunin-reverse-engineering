#!/usr/bin/env python3
"""Semantic probe for a v8 counter (mutation seat MutationC2). Diagnostic only.

Calls the same leg logic as tools/round-98/allowlist-check.py (real14/stub9/extra)
directly on the counter module, bypassing the public subprocess and therefore the
byte-pin confound (an in-place mutant dirties the tree and fails byte-pin-not-bound).
Also probes verify_receipt on the honest pristine receipt and on malformed copies.
Usage: semantic.py <counter.py> <pristine-receipt.json> <out.json>
"""
import copy
import importlib.util
import json
import os
import sys

counter, receipt_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
NINE = ("repaired", "scored", "wrong", "unsafe", "intact",
        "far", "far_refused", "fresh_roundtrip", "fresh_scored")
spec = importlib.util.spec_from_file_location("mut_probe", os.path.abspath(counter))
cand = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cand)
rec = json.load(open(receipt_path))
counts = rec["counts"]
pins = {"counter": rec["counter_sha256"], "verdict": rec["verdict_sha256"],
        "repair": rec["repair_sha256"],
        "imported_r92_battery_sha256": rec["imported_r92_battery_sha256"],
        "imported_v2_sha256": rec["imported_v2_sha256"]}


def vr(obj, name):
    p = os.path.join(os.path.dirname(os.path.abspath(receipt_path)), "probe-%s.json" % name)
    with open(p, "w") as fh:
        json.dump(obj, fh)
    return cand.verify_receipt(p, rec["public_label"], rec["revision"], 6, pins)["ok"]


probes = {
    "real14": int(cand.count_problems(dict(counts)) == []),
    "stub9": int(len(cand.count_problems({k: counts[k] for k in NINE})) >= 1),
    "extra": int(len(cand.count_problems(dict(counts, bogus=0))) >= 1),
    "bool_int_refused": int(len(cand.count_problems(dict(counts, wrong=False))) >= 1),
    "missing_key_refused": int(len(cand.count_problems(
        {k: v for k, v in counts.items() if k != "silent"})) >= 1),
    "verify_honest_ok": int(vr(rec, "honest") is True),
    "verify_missing_key_refused": int(vr(dict(rec, counts={k: v for k, v in counts.items()
                                                         if k != "silent"}), "miss") is False),
    "verify_bool_refused": int(vr(dict(rec, counts=dict(counts, wrong=False)), "bool") is False),
}
os.unlink(os.path.join(os.path.dirname(os.path.abspath(receipt_path)), "probe-honest.json")) \
    if False else None
with open(out_path, "w") as fh:
    json.dump({"counter": counter, "probes": probes}, fh, indent=1, sort_keys=True)
    fh.write("\n")
print(" ".join("%s=%d" % kv for kv in probes.items()))
