#!/usr/bin/env python3
"""Assemble receipts.json from the recorded runs."""
import json
import os

R = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-45/w2/R45W2PreflightReal"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

CMDS = {
 "a1-r44-pathspec": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures/ --freeze-path tools/round-44/control-fixtures --require-pathspec",
 "a2-r45-clean": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty",
 "a3-r44-whole-tree": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --freeze-path tools/round-44/control-fixtures   # no --pathspec, no --require-pathspec",
 "a4-r44-whole-tree-untouched-freezepath": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --freeze-path plans/round-44-claims.md   # control: nothing touched this path",
 "a5-r45-measured-rev": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev 1f4b27f82353d6544dc0c8048b3cfdadd8525d12 --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty",
 "a6-r45-head": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev HEAD --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty   # HEAD resolved to 0ee50aaf at run time",
 "a7-r45-no-require": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty   # same command without --require-pathspec",
 "a8-selftest": "python3 -I -B <SCRATCH>/frozen-preflight.py --selftest   # byte-identical to f762b727:tools/round-45/frozen-path-preflight.py (sha256 633ebc05...)",
 "b1-r45-two-pathspec": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --pathspec tools/round-45/ --pathspec plans/round-45-claims.md --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec --check-dirty",
 "f1-f3-fixtures": "python3 -I -B <SCRATCH>/fixtures.py   # imports the frozen interpreter, builds private repos under <SCRATCH>/fx",
 "c1a-decoy-sibling-pathspec": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures-extra/ --freeze-path tools/round-44/control-fixtures --require-pathspec",
 "c2a-cover-plus-exclude": "python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures/ --pathspec ':(exclude)tools/round-44/control-fixtures/pos/' --freeze-path tools/round-44/control-fixtures --require-pathspec",
}

rows = []
for line in open(os.path.join(R, "exits.tsv")):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 4:
        continue
    name, rc, sha, utc = parts
    receipt = None
    p = os.path.join(R, name + ".stdout")
    if os.path.exists(p):
        try:
            receipt = json.load(open(p))
        except Exception:
            receipt = {"note": "not single-json stdout"}
    rows.append({"run": name, "command": CMDS.get(name, "<see driver>"),
                 "exit": int(rc), "stdout_sha256": sha, "utc": utc,
                 "receipt": receipt})

doc = {
 "seat": "R45W2PreflightReal",
 "lane": LANE,
 "freeze": "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
 "landing": "e715263cb51b713c342ab992d527fe9d61d6f8ff",
 "amendment_a1": "1f4b27f82353d6544dc0c8048b3cfdadd8525d12",
 "interpreter_sha256": "633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b",
 "interpreter_blob_at_freeze": "b42398273da0449c01f6f26cc630853d58ea55ec",
 "env": {"python": "3.14.8", "git": "2.56.0"},
 "lane_read_only": True,
 "installs": [],
 "runs": rows,
}
out = os.path.join(R, "receipts.json")
with open(out, "w") as fh:
    json.dump(doc, fh, indent=1, sort_keys=True)
print(out, len(rows))
