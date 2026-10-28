#!/usr/bin/env python3
"""C1FreezeWindow: run tools/round-46/gate.py's own arms over the merge fixtures under
(a) the frozen flag order, (b) the reversed order, (c) two forgeries that keep the
frozen literal but override it later (last-wins), (d) a correct-order but reformatted
call. Also evaluate tools/round-47/exact.py clause 7's textual counts on each text.
"""
import hashlib
import importlib.util
import json
import os
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
GATE = os.path.join(LANE, "tools", "round-46", "gate.py")
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'

sys.path.insert(0, os.path.dirname(GATE))
import gate  # noqa: E402  (the frozen module, unmodified)

src = open(GATE).read()
assert src.count(ORDER) == 1, src.count(ORDER)
assert src.count(REVERSED) == 0


def load(name, text):
    path = os.path.join(S, name + ".py")
    with open(path, "w") as fh:
        fh.write(text)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


variants = {"frozen": src}
variants["reversed"] = src.replace(ORDER, REVERSED, 1)
variants["forged_trailing_m"] = src.replace(
    ORDER, '"-m", "--diff-merges=first-parent", "-m"', 1)
variants["forged_trailing_separate"] = src.replace(
    ORDER, '"-m", "--diff-merges=first-parent", "--diff-merges=separate"', 1)
variants["reformatted_correct_order"] = src.replace(
    '"log", "-m", "--diff-merges=first-parent", "--name-status", "-z",',
    '"log",\n            "-m",\n            "--diff-merges=first-parent",\n'
    '            "--name-status", "-z",', 1)

mods = {"frozen": gate}
texts = {"frozen": src}
for name in ("reversed", "forged_trailing_m", "forged_trailing_separate",
             "reformatted_correct_order"):
    mods[name], _ = load("gate_" + name, variants[name])
    texts[name] = variants[name]

out = {"gate_sha256_frozen": hashlib.sha256(src.encode()).hexdigest(), "fixtures": {}}


def probe(fx, base, tip, entries):
    paths = [p + "/" for p, d in entries if d] + [p for p, d in entries if not d]
    row = {}
    for name, mod in mods.items():
        touched, err = mod.history_touched(fx, base, tip, paths)
        row[name] = {"history_touched": touched, "err": err,
                     "literal_order": texts[name].count(ORDER),
                     "literal_reversed": texts[name].count(REVERSED)}
    changed = gate.blob_changed(fx, base, tip, entries)
    row["blob_changed_frozen_arm"] = changed
    for name in mods:
        t = row[name]["history_touched"] or []
        row[name]["restored"] = [p for p in t
                                 if p.rstrip("/") not in {c.rstrip("/") for c in changed}]
        row[name]["gate_verdict"] = 2 if row[name]["restored"] else 0
    return row


fx2_dir = open(os.path.join(S, "fx2-base.txt")).read().split()[0]  # unused
fx2 = os.path.join(S, "merge-fx2")
b2 = open(os.path.join(S, "fx2-base.txt")).read().strip()
t2 = open(os.path.join(S, "fx2-tip.txt")).read().strip()
out["fixtures"]["merge-fx2"] = {
    "dir": fx2, "base": b2, "tip": t2,
    "entries": [["tools/round-47", True], ["plans/round-47-claims.md", False]],
    "result": probe(fx2, b2, t2, [("tools/round-47", True),
                                  ("plans/round-47-claims.md", False)]),
}

fx3 = open(os.path.join(S, "fx3-dir.txt")).read().strip()
b3 = open(os.path.join(S, "fx3-base.txt")).read().strip()
t3 = open(os.path.join(S, "fx3-tip.txt")).read().strip()
out["fixtures"]["merge-fx3"] = {
    "dir": fx3, "base": b3, "tip": t3,
    "result": probe(fx3, b3, t3, [("tools/round-47", True),
                                  ("plans/round-47-claims.md", False)]),
    "freeze_state": {},
}
for name, mod in mods.items():
    code, receipt = mod.freeze_state(fx3, b3, t3, claims="plans/round-47-claims.md")
    out["fixtures"]["merge-fx3"]["freeze_state"][name] = {
        "exit": code,
        "reason": receipt.get("reason"),
        "touched": receipt.get("touched"),
        "restored": receipt.get("restored"),
        "blob_changed": receipt.get("blob_changed"),
        "dirty": receipt.get("dirty"),
        "frozen_derived": receipt.get("frozen_derived"),
    }

print(json.dumps(out, indent=1, sort_keys=True))
