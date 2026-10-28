#!/usr/bin/env python3
"""Attack the frozen R47-C1 exactness counter on contentless (structurally valid) rows.

Imports score() from an unmodified byte copy of tools/round-47/exact.py (sha pinned),
feeds it the real bytes at REV for every file the block cites, and mutates only the
block-24 copy in memory. Never touches the lane tree.
"""
import hashlib
import json
import os
import re
import sys

S = os.environ["HYAKU_SCRATCH"]
COPY = os.path.join(S, "copy")
sys.path.insert(0, os.path.join(COPY, "tools", "round-47"))
import exact  # noqa: E402

FILES = {}
for p in ("SKILL.md", "plans/round-47-claims.md", "corpus/lessons/round-46.md",
          "corpus/lessons/round-45.md", "tools/round-47/exact.py",
          "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md",
          "tools/round-46/gate.py"):
    with open(os.path.join(COPY, p)) as fh:
        FILES[p] = fh.read()

SKILL = FILES["SKILL.md"]
BLOCK = [b for b in exact.blocks_of(SKILL) if exact.MARKER in b][0]


def rows_of(block):
    return exact.table(block)[1]


def rewrite(block, rows):
    return exact.rewrite_rows(block, rows)


def set_cells(block, fn):
    rows = [list(r) for r in rows_of(block)]
    for r in rows:
        fn(r)
    return rewrite(block, rows)


def run(name, block):
    skill = SKILL.replace(BLOCK, block, 1)
    out = {}
    for prof in ("v3", "v2"):
        code, rec = exact.score(skill, lambda p: FILES.get(p), prof, "HEAD", battery=None)
        out[prof] = {"exit": code, "failing": rec.get("failing"),
                     "arm_tokens": rec.get("arm_tokens"),
                     "routed_counts": rec.get("routed_counts")}
    print(json.dumps({"case": name, "v3": out["v3"], "v2": out["v2"]}, sort_keys=True))
    return out


CASES = {}
CASES["genuine"] = run("genuine-landed-block", BLOCK)
CASES["hole_dash"] = run("hole-cells-contentless-dash",
                         set_cells(BLOCK, lambda r: r.__setitem__(1, "`-`")))
CASES["hole_empty"] = run("hole-cells-empty",
                          set_cells(BLOCK, lambda r: r.__setitem__(1, "")))
CASES["hole_echo"] = run("hole-echoes-arm-token",
                         set_cells(BLOCK, lambda r: r.__setitem__(1, r[2])))
CASES["hole_and_prose_gone"] = run(
    "hole-and-title-prose-contentless",
    set_cells(BLOCK.replace(
        "each row is a defect the round-46 non-author spot-check routed",
        "").replace("the loose binding that let a forgery pass it, and the clause of "
                    "`tools/round-47/exact.py` that now fails the forgery.", ""),
        lambda r: r.__setitem__(1, "`-`")))
# containment residual in clause 6: the four mutation names are matched with `in block`
names = [n for n, _ in exact.MUTATIONS]
prose = ", ".join("`%s`" % n for n in names)
assert prose in BLOCK, "name list not found verbatim"
decoy = BLOCK.replace(prose, "`-`", 1)
def _name(r):
    i = ["R46-CL2", "R46-CL3", "R46-CL4", "R46-CL6"].index(exact.ID.search(r[0]).group(0))
    r[1] = "`%s` (name only)" % names[i]
decoy = set_cells(decoy, _name)
def _dup4(block):
    rows = [list(r) for r in rows_of(block)]
    rows[1][0] = rows[0][0].split(" ")[0]  # same routed id, still 4 rows
    return rewrite(block, rows)
CASES["dup_id_four_rows"] = run("duplicate-id-keeping-4-rows", _dup4(BLOCK))
CASES["names_only_in_cells"] = run("mutation-names-only-inside-cells", decoy)
# clause 7 binds a source literal, not the executed argv: literal in a constant, runtime reversed
g = FILES["tools/round-46/gate.py"]
lit = '"-m", "--diff-merges=first-parent"'
assert g.count(lit) == 1, g.count(lit)
g2 = g.replace('git(root, "log", "-m", "--diff-merges=first-parent",',
               'git(root, "log", *reversed(LOG_ORDER),')
g2 = g2.replace("def history_touched(root, base, tip, paths):",
                'LOG_ORDER = ("-m", "--diff-merges=first-parent")\n\n\n'
                "def history_touched(root, base, tip, paths):", 1)
assert g2.count(lit) == 1 and g2.count('"--diff-merges=first-parent", "-m"') == 0, (g2.count(lit),)
_old = FILES["tools/round-46/gate.py"]
FILES["tools/round-46/gate.py"] = g2
CASES["literal_only_order"] = run("clause7-literal-in-constant-runtime-reversed", BLOCK)
FILES["tools/round-46/gate.py"] = _old

print(json.dumps({"summary": {k: {"v3": v["v3"]["exit"], "v2": v["v2"]["exit"]}
                              for k, v in CASES.items()}}, indent=1))
print("interpreter_copy_sha256", hashlib.sha256(
    FILES["tools/round-47/exact.py"].encode()).hexdigest())
