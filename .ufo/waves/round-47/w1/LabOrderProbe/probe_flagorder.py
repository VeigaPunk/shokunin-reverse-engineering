#!/usr/bin/env python3
"""Isolate R47-C1 clause 7 (flag order) on a GREEN synthetic block 24.

Imports the frozen counter read-only; each variant is a one-commit fixture repo.
No writes outside the scratch root.
"""
import hashlib
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))

import gate  # noqa: E402
import exact  # noqa: E402

GATE46 = os.path.join(LANE, "tools", "round-46", "gate.py")
BASE = open(GATE46, "rb").read().decode()
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'

VARIANTS = {
    # name: (gate.py text, expectation for score()'s exit code)
    "baseline": (BASE, 0),
    "reversed-pair": (BASE.replace(ORDER, REVERSED, 1), 1),
    # the pair is present and forward, but a third -m re-establishes -m's win
    "trailing-m-after-pair": (BASE.replace(ORDER, ORDER + ', "-m"', 1), 1),
    # correct semantics, only the formatting differs (line break after the comma)
    "line-broken-correct": (BASE.replace(ORDER, '"-m",\n            "--diff-merges=first-parent"', 1), 0),
    # correct semantics via the long spelling only
    "long-spelling": (BASE.replace('"-m", ', '"--diff-merges=separate", "-m", ', 1), 1),
}

root, err = gate.scratch("kaidoku-r47-orderprobe-")
if err:
    print(json.dumps({"reason": err}))
    sys.exit(2)

block = exact.good_block()
skill = exact.skill_text(block)
out = {"order_literal": ORDER, "reversed_literal": REVERSED, "cases": []}

for name, (gtext, expect) in VARIANTS.items():
    files = {"SKILL.md": skill,
             "plans/round-47-claims.md": exact.CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(os.path.join(LANE, "tools", "round-47",
                                                          "exact.py")).read(),
             "tools/round-46/gate.py": gtext}
    d = None
    try:
        d, rev = exact._repo(files, root, prefix="fo-")
        got, rec = exact.score(files["SKILL.md"], lambda p: gate.show(d, rev, p),
                               "v3", rev, battery=None)
        row = {"variant": name, "expect": expect, "got": got,
               "ok": got == expect,
               "gate_order_literal": rec.get("gate_order_literal"),
               "gate_order_reversed": rec.get("gate_order_reversed"),
               "failing": rec.get("failing")}
    except Exception as exc:  # noqa: BLE001
        row = {"variant": name, "expect": expect, "got": "crash",
               "ok": False, "error": f"{type(exc).__name__}: {exc}"}
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    out["cases"].append(row)

out["failures"] = [c["variant"] for c in out["cases"] if not c["ok"]]
print(json.dumps(out, indent=1))
shutil.rmtree(root, ignore_errors=True)
sys.exit(0 if not out["failures"] else 1)
