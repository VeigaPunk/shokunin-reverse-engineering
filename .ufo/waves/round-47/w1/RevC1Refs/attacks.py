#!/usr/bin/env python3
"""Clause-8 attack matrix against the landed block 24 (lane kaidoku, round 47)."""
import hashlib
import json
import os
import shutil
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs")
import drive  # noqa: E402

S = drive.S
base = drive.base_files()["SKILL.md"]
R46 = drive.blob("corpus/lessons/round-46.md")
R45 = drive.blob("corpus/lessons/round-45.md")
rows = []


def v(name, refs, extra_files=None, interpreter=None):
    skill = drive.swap_refs(base, refs)
    rec = drive.run(name, skill, interpreter=interpreter, extra=extra_files)
    rows.append(rec)
    return rec


# b0: landed block untouched
v("b0_landed", None)

# a1: three citations that resolve but say nothing about the rows
v("a1_offtopic", "`corpus/lessons/round-46.md:1-1`, `plans/round-47-claims.md:1-1`, "
                 "`tools/round-47/exact.py:1-1`")

# a2: one file, one line, three times
v("a2_samefile3x", "`corpus/lessons/round-46.md:5`, `corpus/lessons/round-46.md:5`, "
                   "`corpus/lessons/round-46.md:5`")

# a3: two bare SELF citations (no line selector) + one selector
v("a3_self_bare", "`tools/round-47/exact.py`, `tools/round-47/exact.py`, "
                  "`corpus/lessons/round-46.md:1-1`")

# a4: directory citations (a tree object has a line count)
v("a4_dir", "`tools/round-47/:1-2`, `plans/:1-2`, `corpus/lessons/round-46.md:1-1`")

# a5: whole-file and last-line ranges
v("a5_wholefile", "`corpus/lessons/round-46.md:1-102`, `corpus/lessons/round-46.md:102`, "
                  "`corpus/lessons/round-46.md:102-102`")

# a5b: one past the last line
v("a5b_pasteof", "`corpus/lessons/round-46.md:103`, `corpus/lessons/round-46.md:1-102`, "
                 "`plans/round-47-claims.md:1-1`")

# a6: a prefix of the allowlist that is not inside it
v("a6_prefix_evil",
  "`corpus/lessons-evil/round-46.md:1-5`, `corpus/lessons-evil/round-46.md:6`, "
  "`corpus/lessons/round-46.md:1-1`",
  extra_files={"corpus/lessons-evil/round-46.md": R46})

# a6b: a byte copy of the lesson inside the allowlist, off-topic name
v("a6b_sibling_copy",
  "`corpus/lessons/round-46.md.bak:1-5`, `corpus/lessons/round-46.md.bak:6`, "
  "`corpus/lessons/round-46.md:1-1`",
  extra_files={"corpus/lessons/round-46.md.bak": R46})

# a8: a different round entirely
v("a8_wronground", "`corpus/lessons/round-45.md:1-5`, `corpus/lessons/round-45.md:6-9`, "
                   "`corpus/lessons/round-46.md:1-1`",
  extra_files={"corpus/lessons/round-45.md": R45})

json.dump(rows, open(os.path.join(S, "receipts", "matrix.json"), "w"), indent=1)
print("\n== summary ==")
for r in rows:
    print(f"{r['variant']:18s} exit={r['exit']} refs={r.get('refs')} "
          f"battery_v3_green={(r.get('battery') or {}).get('v3_green')} "
          f"failing={r.get('failing')}")
