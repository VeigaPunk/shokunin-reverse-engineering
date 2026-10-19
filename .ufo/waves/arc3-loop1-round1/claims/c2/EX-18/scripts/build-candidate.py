#!/usr/bin/env python3
"""EX-18 scratch candidate: digest-pin the pointer table (proposal for EX-16).

Edits a COPY of the pristine probe in scratch; the diff between pristine and
candidate is the patch text EX-18 ships as a proposal. The real target is never
written by this script.
"""
import hashlib
import json
import os
import sys

SRC = "/dev/shm/ex18-absent/gate/citation-drift-probe.py"       # pristine copy
DST = "/dev/shm/ex18-absent/cand/citation-drift-probe.py"       # candidate
EXP_SRC = "/dev/shm/ex18-absent/gate/expected.json"
EXP_DST = "/dev/shm/ex18-absent/cand/expected.json"
REAL_TABLE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json"

os.makedirs(os.path.dirname(DST), exist_ok=True)
text = open(SRC).read()

# ---- edit 1: run_check — pin the table digest before evaluating entries -------
old_load = '''    try:
        table = json.load(open(table_path))
    except (OSError, ValueError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        expected = {}
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
'''
new_load = '''    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        expected = {}
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
    try:
        raw = open(table_path, "rb").read()
    except OSError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    pinned = (expected.get("pointer_table") or {}).get("sha256") if isinstance(expected, dict) else None
    if pinned is None:
        findings.add("pointer_table_unreadable", os.path.basename(table_path),
                     "no table digest pinned in expected.json (unpinned table)")
        return findings
    if sha256_bytes(raw) != pinned:
        findings.add("pointer_table_unreadable", os.path.basename(table_path),
                     "table sha256 %s != pinned %s" % (sha256_bytes(raw), pinned))
        return findings
    try:
        table = json.loads(raw)
    except ValueError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
'''
assert text.count(old_load) == 1, "edit-1 anchor not unique"
text = text.replace(old_load, new_load)

# ---- edit 2: selftest — pin each fixture table, add the two new cases --------
old_dispatch = '''                if case == "table_unreadable":
                    table = os.path.join(case_dir, "table.json")
                    open(table, "w").write("{ not json")
                    root = build_fixture("clean")
                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table(case), open(table, "w"))
'''
new_dispatch = '''                pin_override = None
                if case == "table_unreadable":
                    table = os.path.join(case_dir, "table.json")
                    open(table, "w").write("{ not json")
                    root = build_fixture("clean")
                elif case == "absent_table":
                    table = os.path.join(case_dir, "table-absent.json")
                    root = build_fixture("clean")
                elif case == "tampered_table":
                    root = build_fixture("clean")
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table("clean"), open(table, "w"))
                    pin_override = sha256_bytes(open(table, "rb").read())
                    tampered = open(table).read().replace(
                        "pinned claim lives here", "PWNED")
                    open(table, "w").write(tampered)
                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table(case), open(table, "w"))
'''
assert text.count(old_dispatch) == 1, "edit-2 anchor not unique"
text = text.replace(old_dispatch, new_dispatch)

old_exp = '''                expected = {"snapshots": digests}
                exp_file = os.path.join(case_dir, "expected.json")
'''
new_exp = '''                expected = {"snapshots": digests}
                if pin_override:
                    expected["pointer_table"] = {"sha256": pin_override}
                elif os.path.isfile(table):
                    expected["pointer_table"] = {
                        "sha256": sha256_bytes(open(table, "rb").read())}
                exp_file = os.path.join(case_dir, "expected.json")
'''
assert text.count(old_exp) == 1, "edit-3 anchor not unique"
text = text.replace(old_exp, new_exp)

open(DST, "w").write(text)

# ---- edit 4: expected.json gains the table digest pin ------------------------
expected = json.load(open(EXP_SRC))
digest = hashlib.sha256(open(REAL_TABLE, "rb").read()).hexdigest()
expected["pointer_table"] = {"sha256": digest}
cases = expected["selftest"]
if not any(c["case"] == "absent_table" for c in cases):
    cases.append({"case": "absent_table", "exit_code": 2,
                  "finding": "pointer_table_unreadable"})
if not any(c["case"] == "tampered_table" for c in cases):
    cases.append({"case": "tampered_table", "exit_code": 2,
                  "finding": "pointer_table_unreadable"})
json.dump(expected, open(EXP_DST, "w"), indent=None)

print("candidate probe ->", DST)
print("candidate expected ->", EXP_DST, "| pinned table sha256:", digest)
print("selftest case count:", len(cases))
