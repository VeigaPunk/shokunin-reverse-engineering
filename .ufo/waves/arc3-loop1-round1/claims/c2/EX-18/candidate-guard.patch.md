# EX-18 candidate guard — PATCH TEXT (proposal only; NOT applied)

Status: **proposal for EX-16** (the only seat authorized to write
`.ufo/gates/citation-drift/`). This seat wrote nothing outside its own artifact
dir. The candidate was built and measured in scratch (`/dev/shm/ex18-absent`),
which is why the evidence in `absent-results.md` §4 is reproducible at all.

What it fixes, from the injection matrix: at HEAD, `json.load(open(table_path))`
(`citation-drift-probe.py:280-284`) accepts **any readable JSON** at the table
path, so a symlink to a stale table (R3: exit 0/1), an in-place needle tamper
(R6: exit 0/1) and a shrunk table (R7: exit 0 **clean**) all bypass the declared
could-not-evaluate class. Absent / directory / dangling-symlink shapes already
land in exit 2 and must keep doing so.

Design constraint the patch must honour: **digest the content, not the path.**
R5 (symlink → the live table) must stay `exit 0, findings=0`; a content digest
satisfies that automatically, a path/lstat check would not.

## 1. `citation-drift-probe.py` — diff (from `candidate-guard.diff`, verbatim)

```diff
--- .ufo/gates/citation-drift/citation-drift-probe.py
+++ .ufo/gates/citation-drift/citation-drift-probe.py
@@ -278,15 +278,29 @@
                      "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
         return findings
     try:
-        table = json.load(open(table_path))
-    except (OSError, ValueError) as exc:
-        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
-        return findings
-    try:
         expected = json.load(open(expected_path))
     except (OSError, ValueError) as exc:
         expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+    try:
+        raw = open(table_path, "rb").read()
+    except OSError as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
+    pinned = (expected.get("pointer_table") or {}).get("sha256") if isinstance(expected, dict) else None
+    if pinned is None:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path),
+                     "no table digest pinned in expected.json (unpinned table)")
+        return findings
+    if sha256_bytes(raw) != pinned:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path),
+                     "table sha256 %s != pinned %s" % (sha256_bytes(raw), pinned))
+        return findings
+    try:
+        table = json.loads(raw)
+    except ValueError as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -392,10 +406,22 @@
         with tempfile.TemporaryDirectory(prefix="citation-drift-case-") as case_dir:
             root = None
             try:
+                pin_override = None
                 if case == "table_unreadable":
                     table = os.path.join(case_dir, "table.json")
                     open(table, "w").write("{ not json")
                     root = build_fixture("clean")
+                elif case == "absent_table":
+                    table = os.path.join(case_dir, "table-absent.json")
+                    root = build_fixture("clean")
+                elif case == "tampered_table":
+                    root = build_fixture("clean")
+                    table = os.path.join(case_dir, "table.json")
+                    json.dump(fixture_table("clean"), open(table, "w"))
+                    pin_override = sha256_bytes(open(table, "rb").read())
+                    tampered = open(table).read().replace(
+                        "pinned claim lives here", "PWNED")
+                    open(table, "w").write(tampered)
                 else:
                     root = build_fixture(case)
                     table = os.path.join(case_dir, "table.json")
@@ -413,6 +439,11 @@
                 else:
                     digests = {}
                 expected = {"snapshots": digests}
+                if pin_override:
+                    expected["pointer_table"] = {"sha256": pin_override}
+                elif os.path.isfile(table):
+                    expected["pointer_table"] = {
+                        "sha256": sha256_bytes(open(table, "rb").read())}
                 exp_file = os.path.join(case_dir, "expected.json")
                 json.dump(expected, open(exp_file, "w"))
```

Notes on the diff:

* `expected` must be loaded **before** the table, since the pin lives in it.
* An absent pin (`expected.json` has no `pointer_table.sha256`) is itself CNE,
  never a silent pass — a legacy/unpinned expected file must not re-open the hole.
* The selftest must pin each fixture table's own digest, otherwise all 11
  existing cases would newly read as unpinned CNE. That is the coupling that
  makes this patch touch the selftest, not just `run_check`.

## 2. `expected.json` — data changes (not expressible as a line diff here)

Add the pin (digest of the table as committed at HEAD `e845c2b`):

```json
"pointer_table": {"sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f"},
```

and the two new selftest cases (claim: 11 → 13):

```json
{"case": "absent_table",   "exit_code": 2, "finding": "pointer_table_unreadable"},
{"case": "tampered_table", "exit_code": 2, "finding": "pointer_table_unreadable"}
```

Measured with these in place: `CITATION_DRIFT_SELFTEST: CLEAN cases=13
passed=13 failed=0 exit=0`.

## 3. Consequence to record (maintenance cost, not a defect)

The pin makes every future edit to `pointer-table.json` a two-file commit:
table edit + digest re-pin in `expected.json`. An un-re-pinned table now reads
CNE (`exit 2`) rather than silently evaluating — fail-closed, which is the
point, but it means the round's own re-pin must land atomically with the table
change, and `SCORECARD.md`'s measurement recipe should say so.

## 4. What this proposal does NOT do

* No `SKILL.md` registry-row text (EX-16's claim requires the guard semantics be
  stated there) — this seat may not edit SKILL.md.
* No changes to the snapshot-pin machinery, entry kinds, or finding ids other
  than reusing `pointer_table_unreadable` for the new class.
* The `--expected` file itself is not digest-pinned (self-referential; out of
  scope, flagged in `absent-results.md` §5).
