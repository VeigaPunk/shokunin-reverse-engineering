#!/usr/bin/env python3
"""Round 7: fence-blind row/ID counting inside block 23; minimal green artefact."""
import importlib.util
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PINDIR = sys.argv[1]
GREV = sys.argv[2]
sys.path.insert(0, PINDIR)
gs = importlib.util.spec_from_file_location("gate", os.path.join(PINDIR, "gate.py"))
gate = importlib.util.module_from_spec(gs); sys.modules["gate"] = gate; gs.loader.exec_module(gate)
as_ = importlib.util.spec_from_file_location("attest", os.path.join(PINDIR, "attest.py"))
attest = importlib.util.module_from_spec(as_); sys.modules["attest"] = attest
as_.loader.exec_module(attest)

SPEC = attest.SPECS["r46"]
REV = gate.resolve(LANE, GREV)
S = os.environ["HYAKU_SCRATCH"]
OUT = {}


def files_at(rev):
    return lambda p: gate.show(LANE, rev, p)


def data_rows(block):
    return attest._table_line_indexes(block)


def cell(block, col, fn):
    lines, data = data_rows(block)
    for i in data:
        c = attest._cells(lines[i])
        c[col] = fn(c[col])
        lines[i] = "| " + " | ".join(c) + " |"
    return "\n".join(lines) + "\n"


def battery(rev, text):
    marked = [b for b in attest.craft_blocks(text) if SPEC["marker"] in b]
    if len(marked) != 1:
        return {"error": "marker blocks %d" % len(marked)}
    block = marked[0]
    need = {"SKILL.md", SPEC["pin"], attest.CLAIMS, "corpus/lessons/round-45.md"}
    need |= {n for n, _, _ in attest.refs_in(block, True)}
    need = sorted(p for p in need if p)
    out = {"forgeries_total": 0, "v1_green": 0, "v2_green": 0, "genuine_green": 0,
           "v2_crash": 0}
    code, _ = attest.score(text, files_at(rev), "r46", "v2", rev, battery=None)
    out["genuine_green"] = 1 if code == 0 else 0
    for name, fn in attest.MUTATIONS:
        try:
            forged = fn(block, SPEC)
        except ValueError:
            out["forgeries_total"] += 1
            continue
        if forged == block:
            out["forgeries_total"] += 1
            out["v2_green"] += 1
            continue
        d, frev = attest.fixture_repo(LANE, rev, text.replace(block, forged), need, S)
        try:
            ff = lambda p, d=d: gate.show(d, frev, p)
            st = text.replace(block, forged)
            c1, _ = attest.score(st, ff, "r46", "v1", frev, battery=None)
            c2, _ = attest.score(st, ff, "r46", "v2", frev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out["forgeries_total"] += 1
        out["v1_green"] += 1 if c1 == 0 else 0
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v2_crash"] += 1 if c2 == 2 else 0
    return out


def run(label, text, save=False):
    code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=None)
    bat = None
    if code == 0:
        bat = battery(REV, text)
        if "error" not in bat:
            code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=bat)
    OUT[label] = {"exit": code, "met_target": rec.get("met_target"),
                  "failing": rec.get("failing"), "rows": rec.get("rows"),
                  "refs": rec.get("refs"),
                  "battery": None if bat is None else {k: bat.get(k) for k in
                                                       ("forgeries_total", "v1_green",
                                                        "v2_green", "genuine_green")}}
    if save and code == 0:
        open(os.path.join(S, "artefact-%s.md" % label), "w").write(text)
    print(json.dumps({label: OUT[label]}, sort_keys=True)[:400])


skill = gate.show(LANE, REV, "SKILL.md")
block = [b for b in attest.craft_blocks(skill) if SPEC["marker"] in b][0]

# F1: one honest row + a fenced example carrying the other twelve ids and the vocab.
lines, data = data_rows(block)
keep = [l for i, l in enumerate(lines) if i not in data]
fenced = ["```"]
for rid in attest.ROUTED[1:]:
    fenced.append("| %s | example row, inside a fence | commit | 1 |" % rid)
fenced.append("```")
first = min(data)
f1 = "\n".join(keep[:first] + [lines[data[0]]] + fenced + keep[first:]) + "\n"
run("F1_fenced_example_rows", skill.replace(block, f1))

# F2: minimal edit -- only the v1-hole column replaced, everything else genuine.
run("F2_minimal_lorem_column",
    skill.replace(block, cell(block, 1, lambda c: "lorem ipsum")), save=True)

# F3: trigger cell empty, ids carried in the v1-hole cell instead.
f3 = cell(block, 1, lambda c: c + " " + " ".join(attest.ROUTED))
lines, data = data_rows(f3)
for i in data:
    c = attest._cells(lines[i])
    c[0] = ""
    lines[i] = "| " + " | ".join(c) + " |"
run("F3_ids_in_wrong_column", skill.replace(block, "\n".join(lines) + "\n"))

# F4: two pins, the wrong one first (PIN.search takes the first match).
wrong = "sha256:" + "a" * 64
f4 = block.replace("sha256:", wrong + " sha256:", 1)
run("F4_decoy_pin_first", skill.replace(block, f4, 1))

# F5: arm cell = the arm token as a substring of prose that contradicts it.
run("F5_arm_prose", skill.replace(
    block, cell(block, 2, lambda c: "no arm here, merely the word commit inside prose")))

print(json.dumps({"instrument": PINDIR, "rev": REV}, indent=1))
json.dump(OUT, open(os.path.join(S, "attacks7.json"), "w"), indent=1, sort_keys=True)
