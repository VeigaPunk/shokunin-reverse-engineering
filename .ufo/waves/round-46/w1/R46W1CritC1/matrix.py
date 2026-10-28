#!/usr/bin/env python3
"""Consolidated six-attack matrix, run against a PINNED instrument copy.

Usage: matrix.py <pinned-rev-dir> <git-rev-to-read-SKILL-and-files-at>
Every instrument byte comes from the pinned dir; every repo read is `git show`.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PINDIR = sys.argv[1]
GREV = sys.argv[2]

sys.path.insert(0, PINDIR)
spec_g = importlib.util.spec_from_file_location("gate_p", os.path.join(PINDIR, "gate.py"))
gate = importlib.util.module_from_spec(spec_g)
sys.modules["gate"] = gate
spec_g.loader.exec_module(gate)
spec_a = importlib.util.spec_from_file_location("attest_p", os.path.join(PINDIR, "attest.py"))
attest = importlib.util.module_from_spec(spec_a)
sys.modules["attest"] = attest
spec_a.loader.exec_module(attest)

SPEC = attest.SPECS["r46"]
REV = gate.resolve(LANE, GREV)
SCRATCH = os.environ["HYAKU_SCRATCH"]
OUT = {"instrument_dir": PINDIR,
       "instrument_sha256": {f: hashlib.sha256(open(os.path.join(PINDIR, f), "rb").read()).hexdigest()
                             for f in sorted(os.listdir(PINDIR)) if f.endswith(".py")},
       "rev": REV, "attacks": {}}


def files_at(rev):
    return lambda p: gate.show(LANE, rev, p)


def data_rows(block):
    return attest._table_line_indexes(block)


def set_cells(block, col, fn):
    lines, data = data_rows(block)
    for i in data:
        c = attest._cells(lines[i])
        c[col] = fn(c[col])
        lines[i] = "| " + " | ".join(c) + " |"
    return "\n".join(lines) + "\n"


def replace_refs(block, text):
    return "\n".join(("  Refs: " + text) if l.strip().startswith("Refs:") else l
                     for l in block.splitlines()) + "\n"


def replace_data(block, rows):
    lines, data = data_rows(block)
    keep = [l for i, l in enumerate(lines) if i not in data]
    first = min(data)
    return "\n".join(keep[:first] + rows + keep[first:]) + "\n"


def battery_for(rev, text):
    marked = [b for b in attest.craft_blocks(text) if SPEC["marker"] in b]
    if len(marked) != 1:
        return {"error": "marker blocks %d" % len(marked)}
    block = marked[0]
    need = {"SKILL.md", SPEC["pin"], attest.CLAIMS, "corpus/lessons/round-45.md"}
    need |= {n for n, _, _ in attest.refs_in(block, True)}
    need = sorted(p for p in need if p)
    out = {"forgeries_total": 0, "v1_green": 0, "v2_green": 0, "genuine_green": 0,
           "v2_crash": 0, "fixtures": []}
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
            out["fixtures"].append({"name": name, "note": "no-op"})
            continue
        d, frev = attest.fixture_repo(LANE, rev, text.replace(block, forged), need, SCRATCH)
        try:
            ff = lambda p, d=d: gate.show(d, frev, p)  # noqa: E731
            st = text.replace(block, forged)
            c1, _ = attest.score(st, ff, "r46", "v1", frev, battery=None)
            c2, _ = attest.score(st, ff, "r46", "v2", frev, battery=None)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        out["forgeries_total"] += 1
        out["v1_green"] += 1 if c1 == 0 else 0
        out["v2_green"] += 1 if c2 == 0 else 0
        out["v2_crash"] += 1 if c2 == 2 else 0
        out["fixtures"].append({"name": name, "v1_exit": c1, "v2_exit": c2})
    return out


def run(label, text):
    code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=None)
    bat = None
    if code == 0:
        bat = battery_for(REV, text)
        if "error" not in bat:
            code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=bat)
    OUT["attacks"][label] = {
        "exit": code, "met_target": rec.get("met_target"),
        "failing": rec.get("failing"), "reason": rec.get("reason"),
        "rows": rec.get("rows"), "refs": rec.get("refs"), "cited": rec.get("cited"),
        "battery": None if bat is None else {k: bat.get(k) for k in
                                             ("forgeries_total", "v1_green", "v2_green",
                                              "genuine_green", "v2_crash", "error")}}
    print(json.dumps({label: OUT["attacks"][label]}, sort_keys=True)[:500])
    return rec


def main():
    skill = gate.show(LANE, REV, "SKILL.md")
    gen = [b for b in attest.craft_blocks(skill) if SPEC["marker"] in b]
    if not gen:
        OUT["error"] = "no genuine marker block at this rev"
        print(json.dumps(OUT, indent=1)[:400])
        return
    block = gen[0]
    OUT["genuine_structural"] = dict(zip(("rows", "refs"), (None, None)))
    c, r = attest.score(skill, files_at(REV), "r46", "v2", REV, battery=None)
    OUT["genuine"] = {"exit": c, "rows": r.get("rows"), "refs": r.get("refs"),
                      "failing": r.get("failing")}

    six = ", ".join(f"`corpus/lessons/round-45.md:{a}-{b}`"
                    for a, b in [(1, 5), (10, 14), (20, 24), (30, 34), (40, 44), (50, 54)])
    five = ", ".join(f"`corpus/lessons/round-45.md:{a}-{b}`"
                     for a, b in [(1, 5), (10, 14), (20, 24), (30, 34), (40, 44)])
    allids = " ".join(attest.ROUTED)
    one = ["| %s | nothing | commit | 1 |" % allids] + \
          ["| filler %d | nothing | commit | 1 |" % k for k in range(12)]

    # 1: every clause met, no actionable content.
    run("A1_lorem_v1_hole", skill.replace(block, set_cells(block, 1, lambda c: "lorem ipsum")))
    # 2: marker in a second, non-craft section.
    run("A2_marker_in_second_section",
        skill.replace("\n## Config custody for live-probe rounds (SOP)",
                      "\n<!-- freeze-integrity-table v2 -->\n\n"
                      "## Config custody for live-probe rounds (SOP)", 1))
    # 3: the pin — binds bytes at --rev, not the executing file.
    OUT["attacks"]["A3_pin_binds"] = {
        "pin_in_block": attest.PIN.search(block).group(1) if attest.PIN.search(block) else None,
        "sha256_of_bytes_at_rev": hashlib.sha256(
            (gate.show(LANE, REV, SPEC["pin"]) or "").encode()).hexdigest(),
        "sha256_of_executing_copy_patched": None, "note": "see D3 in report"}
    # 4: arm vocabulary by substring.
    run("A4_blobberish_arm", skill.replace(block, set_cells(block, 2, lambda c: "blobberish")))
    # 5: refs >= 6 as six citations to one file.
    run("A5_six_refs_one_file", skill.replace(block, replace_refs(block, six)))
    # 6: ids present as a whole-cell blob, not per row.
    run("A6_one_row_all_ids", skill.replace(block, replace_data(block, one)))
    # 6b: refs floor met with 5 citations + the pinned interpreter.
    run("A6b_five_refs_plus_pin",
        skill.replace(block, replace_refs(block, five + ", `tools/round-46/attest.py`")))
    # cheapest green: all of the weak axes at once.
    cheap = set_cells(block, 1, lambda c: "lorem ipsum")
    cheap = set_cells(cheap, 2, lambda c: "blobberish")
    cheap = replace_data(cheap, one)
    cheap = replace_refs(cheap, six)
    rec = run("CHEAPEST_GREEN", skill.replace(block, cheap))
    if OUT["attacks"]["CHEAPEST_GREEN"]["exit"] == 0:
        with open(os.path.join(SCRATCH, "cheapest-green-block.md"), "w") as fh:
            fh.write(cheap)

    print(json.dumps({k: v for k, v in OUT.items() if k != "attacks"}, indent=1, sort_keys=True)[:1200])
    with open(os.path.join(SCRATCH, "matrix-%s.json" % PINDIR.rstrip("/").split("/")[-1]), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)


main()
