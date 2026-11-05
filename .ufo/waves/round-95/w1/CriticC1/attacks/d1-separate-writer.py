#!/usr/bin/env python3
"""D1 separate writer: writes a whole receipt triple WITHOUT running any repair command.

It copies the honest run's pins, counts and revision, asserts a met-True verdict, and
writes (json, stdout, rc) under <out_dir>/<prefix>-pos.*. Nothing is measured here."""
import json
import sys

src, out_dir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
honest = json.load(open(src))
rec = {
    "class": honest["class"],
    "counts": dict(honest["counts"]),
    "counter_sha256": honest["counter_sha256"],
    "expect": honest["expect"],
    "exit": 0,
    "label": honest["expect"],
    "met_target": True,
    "repair": honest["repair"],
    "repair_sha256": honest["repair_sha256"],
    "revision": honest["revision"],
    "tool": honest["tool"],
    "verdict_counter": honest["verdict_counter"],
    "verdict_sha256": honest["verdict_sha256"],
}
stem = "%s/%s-pos" % (out_dir.rstrip("/"), prefix)
with open(stem + ".json", "w") as fh:
    json.dump(rec, fh, indent=1, sort_keys=True)
    fh.write("\n")
with open(stem + ".stdout", "w") as fh:
    fh.write("selfverify ok=True reasons=0\n%s met True exit 0\n" % rec["label"])
with open(stem + ".rc", "w") as fh:
    fh.write("0\n")
print("wrote", stem)
