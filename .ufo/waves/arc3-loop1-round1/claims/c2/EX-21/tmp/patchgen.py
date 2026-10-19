#!/usr/bin/env python3
"""EX-21 patch generator: build the SKILL.md self-invocation cell-4 patch text.
Scratch only — writes the patched SKILL.md under tmp/patchgen/, never the repo."""
import hashlib
import os

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "patchgen")
os.makedirs(OUT, exist_ok=True)

src = open(os.path.join(REPO, "SKILL.md")).read()
lines = src.split("\n")
assert len(lines) == 372 and lines[-1] == "", "unexpected SKILL.md shape"
row = lines[370]  # line 371, 0-based 370
assert row.startswith("| citation-drift |"), "row moved"
pieces = row.split("|")
assert len(pieces) == 7, "row is not 5 cells: %d pieces" % len(pieces)

old_cell = pieces[4]
print("OLD CELL-4 REPR:")
print(repr(old_cell))

new_cell = (" same command with `--selftest`; 13 isolated-fixture cases "
            "asserting exit code and a stable finding id (the dead/absent "
            "`--rev` case \u2192 exit 2, finding `revision_unresolvable`; the "
            "guard cases `table_tampered` and `table_absent` \u2192 exit 2, "
            "findings `table_tampered` and `pointer_table_unreadable`, each "
            "fixture's `expected.json` pinning that fixture's table digest "
            "\u2014 the guard-pass path rides the existing `clean` case), the "
            "case table committed in `expected.json` rather than in the script ")

assert old_cell.count("11 isolated-fixture cases") == 1
assert "the eleventh is dead/absent `--rev`" in old_cell

new_row = "|".join(pieces[:4] + [new_cell] + pieces[5:])
new_src = src.replace(row, new_row, 1)
assert new_src != src

with open(os.path.join(OUT, "SKILL.md"), "w") as fh:
    fh.write(new_src)

sha = lambda b: hashlib.sha256(b).hexdigest()
row_old = row.encode()
row_new = new_row.encode()
print("row sha256 old:", sha(row_old))
print("row sha256 new:", sha(row_new))
print("file sha256 old:", sha(src.encode()))
print("file sha256 new:", sha(new_src.encode()))
print("line count old/new:", len(lines) - 1, len(new_src.split("\n")) - 1)
print("new row cells:", len(new_row.split("|")))
print("NEW CELL-4 REPR:")
print(repr(new_cell))
