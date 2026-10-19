#!/usr/bin/env python3
"""EX-21 prototype v2: table-digest preflight guard (fail-closed on unpinned)
+ 2 selftest cases on a scratch COPY of the citation-drift probe.
Never touches the real gate. v2 changes vs v1: finding id `table_tampered`
(E14.md:391/:493 precedent), fail-closed unpinned (`table_pin_absent`,
per EX-24's pin-mutability attack)."""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- 1. guard in verdict(): CNE class gains table_tampered + table_pin_absent ----
p = open(os.path.join(HERE, "probe.py")).read()

old = '''        if any(f in ("snapshot_tampered", "snapshot_missing",
                     "pointer_table_unreadable", "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error")
               for f, _, _ in self.rows):'''
new = '''        if any(f in ("snapshot_tampered", "snapshot_missing",
                     "pointer_table_unreadable", "table_tampered",
                     "table_pin_absent", "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error")
               for f, _, _ in self.rows):'''
assert old in p, "verdict CNE list not found"
p = p.replace(old, new)

# ---- 2. run_check(): load expected first; fail-closed pin + digest verify ----
old = '''    try:
        table = json.load(open(table_path))
    except (OSError, ValueError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        expected = {}
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
    tree = Tree(root, rev, snapshot_dir, expected, findings)'''
new = '''    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        expected = {}
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
    try:
        table_bytes = open(table_path, "rb").read()
        table = json.loads(table_bytes)
    except (OSError, ValueError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    pinned_table = expected.get("table_sha256")
    if pinned_table is None:
        findings.add("table_pin_absent", os.path.basename(expected_path),
                     "no table_sha256 pinned; fail-closed preflight")
        return findings
    if sha256_bytes(table_bytes) != pinned_table:
        findings.add("table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pinned_table))
        return findings
    tree = Tree(root, rev, snapshot_dir, expected, findings)'''
assert old in p, "run_check table load not found"
p = p.replace(old, new)

# ---- 3. selftest(): build table bytes + pinned digest per case ----
old = '''                if case == "table_unreadable":
                    table = os.path.join(case_dir, "table.json")
                    open(table, "w").write("{ not json")
                    root = build_fixture("clean")
                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table(case), open(table, "w"))'''
new = '''                if case in ("table_absent", "table_tampered", "table_unreadable"):
                    root = build_fixture("clean")
                else:
                    root = build_fixture(case)
                table = os.path.join(case_dir, "table.json")
                if case == "table_absent":
                    # pin the digest of the table that is never written
                    table_bytes = None
                    pinned_digest = sha256_bytes(
                        json.dumps(fixture_table("clean")).encode())
                elif case == "table_tampered":
                    # pin the honest digest, then write different bytes
                    good = json.dumps(fixture_table("clean")).encode()
                    pinned_digest = sha256_bytes(good)
                    table_bytes = good + b" "
                elif case == "table_unreadable":
                    table_bytes = b"{ not json"
                    pinned_digest = sha256_bytes(table_bytes)
                else:
                    table_bytes = json.dumps(fixture_table(case)).encode()
                    pinned_digest = sha256_bytes(table_bytes)
                if table_bytes is not None:
                    open(table, "wb").write(table_bytes)'''
assert old in p, "selftest fixture build not found"
p = p.replace(old, new)

old = '''                expected = {"snapshots": digests}'''
new = '''                expected = {"snapshots": digests, "table_sha256": pinned_digest}'''
assert old in p, "selftest expected build not found"
p = p.replace(old, new)

open(os.path.join(HERE, "probe.py"), "w").write(p)

# ---- 4. expected.json: pin real table digest + append the two cases ----
epath = os.path.join(HERE, "expected.json")
root = json.load(open(epath))
table_digest = hashlib.sha256(
    open(os.path.join(HERE, "pointer-table.json"), "rb").read()).hexdigest()
root["table_sha256"] = table_digest
root["selftest"].append({"case": "table_tampered", "exit_code": 2,
                         "finding": "table_tampered"})
root["selftest"].append({"case": "table_absent", "exit_code": 2,
                         "finding": "pointer_table_unreadable"})
json.dump(root, open(epath, "w"))
print("proto v2 applied; pinned table_sha256 =", table_digest)
print("selftest cases =", len(root["selftest"]))
