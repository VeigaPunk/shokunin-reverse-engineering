#!/usr/bin/env python3
"""R46-C1 falsification receipts.

    python3 -I -B receipts.py <pinned-tool-dir> <repo-rev>

Every instrument byte is loaded from <pinned-tool-dir> (a byte copy of
`tools/round-46/` at the pinned rev); every repository read is `git show <rev>:path`.
Prints one JSON object: per-attack command, exit, stdout sha256, UTC time.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PINDIR, GREV = sys.argv[1], sys.argv[2]
S = os.environ["HYAKU_SCRATCH"]
REV = subprocess.run(["git", "-C", LANE, "rev-parse", GREV + "^{commit}"],
                     capture_output=True, text=True).stdout.strip()

gs = importlib.util.spec_from_file_location("gate", os.path.join(PINDIR, "gate.py"))
gate = importlib.util.module_from_spec(gs)
sys.modules["gate"] = gate
gs.loader.exec_module(gate)
a_s = importlib.util.spec_from_file_location("attest", os.path.join(PINDIR, "attest.py"))
attest = importlib.util.module_from_spec(a_s)
sys.modules["attest"] = attest
a_s.loader.exec_module(attest)
SPEC = attest.SPECS["r46"]
ROWS = {}
FULL = ("forgeries_total", "v1_green", "v2_green", "genuine_green", "v2_crash")


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def files_at(rev):
    return lambda p: gate.show(LANE, rev, p)


def battery(text):
    marked = [b for b in attest.craft_blocks(text) if SPEC["marker"] in b]
    if len(marked) != 1:
        return {"error": "marker blocks %d" % len(marked)}
    block = marked[0]
    need = {"SKILL.md", SPEC["pin"], attest.CLAIMS, "corpus/lessons/round-45.md"}
    need |= {n for n, _, _ in attest.refs_in(block, True)}
    need = sorted(p for p in need if p)
    out = dict.fromkeys(FULL, 0)
    code, _ = attest.score(text, files_at(REV), "r46", "v2", REV, battery=None)
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
        d, frev = attest.fixture_repo(LANE, REV, text.replace(block, forged), need, S)
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


def attack(label, text, cmdtail):
    code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=None)
    bat = None
    if code == 0:
        bat = battery(text)
        if "error" not in bat:
            code, rec = attest.score(text, files_at(REV), "r46", "v2", REV, battery=bat)
    payload = json.dumps({"label": label, "exit": code, "receipt": rec}, sort_keys=True)
    ROWS[label] = {
        "command": "python3 -I -B %s/receipts.py %s %s   # artefact sha256 %s" % (
            S, PINDIR, GREV, hashlib.sha256(text.encode()).hexdigest()),
        "scope": cmdtail,
        "exit": code,
        "stdout_sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "utc": now(),
        "met_target": rec.get("met_target"),
        "failing": rec.get("failing"),
        "rows": rec.get("rows"), "refs": rec.get("refs"),
        "marker_occurrences": rec.get("marker_occurrences"),
        "battery": None if bat is None else {k: bat.get(k) for k in FULL},
        "artefact_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }
    print("%-34s exit=%d met=%s %s" % (label, code, rec.get("met_target"),
                                       json.dumps(rec.get("failing") or [])[:150]))
    return code, rec


def data_rows(block):
    return attest._table_line_indexes(block)


def set_cell(block, col, fn):
    lines, data = data_rows(block)
    for i in data:
        c = attest._cells(lines[i])
        c[col] = fn(c[col])
        lines[i] = "| " + " | ".join(c) + " |"
    return "\n".join(lines) + "\n"


def replace_data(block, rows):
    lines, data = data_rows(block)
    keep = [l for i, l in enumerate(lines) if i not in data]
    first = min(data)
    return "\n".join(keep[:first] + rows + keep[first:]) + "\n"


def replace_refs(block, text):
    return "\n".join(("  Refs: " + text) if l.strip().startswith("Refs:") else l
                     for l in block.splitlines()) + "\n"


skill = gate.show(LANE, REV, "SKILL.md")
block = [b for b in attest.craft_blocks(skill) if SPEC["marker"] in b][0]
six = ", ".join(f"`corpus/lessons/round-45.md:{a}-{b}`"
                for a, b in [(1, 5), (10, 14), (20, 24), (30, 34), (40, 44), (50, 54)])
allids = " ".join(attest.ROUTED)
one = ["| %s | nothing | commit | 1 |" % allids] + \
      ["| filler %d | nothing | commit | 1 |" % k for k in range(12)]

attack("GENUINE", skill, "the landed artefact at rev, unmodified")
attack("A1_lorem_v1_hole", skill.replace(block, set_cell(block, 1, lambda c: "lorem ipsum")),
       "col 1 ('v1 hole') of all 13 rows replaced with lorem ipsum")
attack("A2_marker_second_section",
       skill.replace("\n## Config custody for live-probe rounds (SOP)",
                     "\n<!-- freeze-integrity-table v2 -->\n\n"
                     "## Config custody for live-probe rounds (SOP)", 1),
       "marker repeated in a later craft-adjacent section")
attack("A4_blobberish_arm", skill.replace(block, set_cell(block, 2, lambda c: "blobberish")),
       "every arm cell replaced by 'blobberish' (contains 'blob')")
attack("A5_six_refs_one_file", skill.replace(block, replace_refs(block, six)),
       "refs replaced by six line-selected citations to corpus/lessons/round-45.md")
attack("A6_one_row_all_ids", skill.replace(block, replace_data(block, one)),
       "one row names all 13 ids in cell 0, 12 filler rows")
cheap = set_cell(block, 1, lambda c: "lorem ipsum")
cheap = set_cell(cheap, 2, lambda c: "blobberish")
cheap = replace_data(cheap, one)
cheap = replace_refs(cheap, six)
attack("CHEAPEST_GREEN", skill.replace(block, cheap),
       "all weak axes at once: lorem hole column, blobberish arms, one id row, six same-file refs")

out = {"seat": "R46W1CritC1", "rev": REV, "utc": now(),
       "instrument": {f: hashlib.sha256(open(os.path.join(PINDIR, f), "rb").read()).hexdigest()
                      for f in ("attest.py", "gate.py", "registry.py")},
       "pin_in_block": (attest.PIN.search(block).group(1) if attest.PIN.search(block) else None),
       "sha256_of_bytes_at_rev": hashlib.sha256(
           (gate.show(LANE, REV, SPEC["pin"]) or "").encode()).hexdigest(),
       "receipts": ROWS}
path = os.path.join(S, "receipts-C1.json")
json.dump(out, open(path, "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items() if k != "receipts"}, indent=1, sort_keys=True))
print("wrote", path)
