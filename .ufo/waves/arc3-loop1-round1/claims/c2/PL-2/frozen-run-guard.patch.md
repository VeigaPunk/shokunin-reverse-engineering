# PL-2 patch text — C2 citation-drift frozen-run guard

Validated on scratch copies (see `plan.md` §6). Target files, in apply order:
1. `.ufo/gates/citation-drift/citation-drift-probe.py` (EX-16, real target)
2. `.ufo/gates/citation-drift/expected.json` (EX-16, real target)
3. `SKILL.md:371` (protected file — patch text only; parent integrates)

Base hashes: probe `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f`,
expected.json `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33`,
pointer-table.json `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
(pin value = that digest). Prototype-verified result: probe
`e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`, expected.json
`ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` (scratch
carried a trailing newline; the real edit should preserve the committed
single-line no-trailing-newline style).

## Patch 1 — citation-drift-probe.py

```diff
--- a/.ufo/gates/citation-drift/citation-drift-probe.py
+++ b/.ufo/gates/citation-drift/citation-drift-probe.py
@@ -31,6 +31,14 @@
                            against expected.json `snapshots` (a mismatched
                            snapshot is `snapshot_tampered`, exit 2).
 
+FROZEN-RUN GUARD  expected.json pins the sha256 of the pointer table (the
+`pointer_table` key). A table whose bytes differ from the pinned digest is
+`pointer_table_tampered`; an absent table is `pointer_table_unreadable`; a
+baseline that pins no digest is `pointer_table_unpinned`. All three are
+preflight could-not-evaluate (exit 2) and run before any entry is graded, so a
+tampered table can never produce silent findings. Any edit to the table must
+re-pin the digest in the same commit.
+
 VERDICT  exit 0 clean, 1 failed, 2 could-not-evaluate. Every finding carries a
 stable id so the self-test can assert on it.
 
@@ -70,7 +78,8 @@
         if not self.rows:
             return CLEAN
         if any(f in ("snapshot_tampered", "snapshot_missing",
-                     "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_unreadable", "pointer_table_tampered",
+                     "pointer_table_unpinned", "unpinned_legacy",
                      "root_unreadable", "revision_unresolvable", "internal_error")
                for f, _, _ in self.rows):
             return CNE
@@ -278,15 +287,30 @@
                      "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
         return findings
     try:
-        table = json.load(open(table_path))
+        expected = json.load(open(expected_path))
     except (OSError, ValueError) as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+        return findings
+    pin = expected.get("pointer_table")
+    pin = pin.get("sha256") if isinstance(pin, dict) else None
+    if pin is None:
+        findings.add("pointer_table_unpinned", os.path.basename(expected_path),
+                     "no pointer-table digest pinned in expected.json")
+        return findings
+    try:
+        table_bytes = open(table_path, "rb").read()
+    except OSError as exc:
         findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
         return findings
+    if sha256_bytes(table_bytes) != pin:
+        findings.add("pointer_table_tampered", os.path.basename(table_path),
+                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pin))
+        return findings
     try:
-        expected = json.load(open(expected_path))
-    except (OSError, ValueError) as exc:
-        expected = {}
-        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+        table = json.loads(table_bytes.decode("utf-8"))
+    except (ValueError, UnicodeDecodeError) as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -412,9 +436,17 @@
                     digests = {"external.cfg": "0" * 64}
                 else:
                     digests = {}
-                expected = {"snapshots": digests}
+                table_bytes = open(table, "rb").read()
+                expected = {"snapshots": digests,
+                            "pointer_table": {"sha256": sha256_bytes(table_bytes)}}
                 exp_file = os.path.join(case_dir, "expected.json")
                 json.dump(expected, open(exp_file, "w"))
+                if case == "table_tampered":
+                    # the silent-clean shape: a valid table with no entries
+                    # grades findings=0 at rc 0 without the frozen-run guard
+                    open(table, "w").write(json.dumps({"entries": []}))
+                elif case == "table_absent":
+                    os.remove(table)
 
                 rev = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef" if case == "rev_unresolvable" else "HEAD"
                 findings = run_check(root, rev, table, exp_file,
```

## Patch 2 — expected.json

Three text edits on the single committed line (shown here against the scratch
copy; the real edit keeps the file's no-trailing-newline style):

1. `_doc`: `the frozen-run baseline pins the digest of every snapshot input
   file, and` → `the frozen-run baseline pins the digest of every snapshot
   input file AND of the pointer table itself (a tampered or absent table is
   could-not-evaluate, never silent findings), and`
2. insert before `"snapshots": {`:

```json
"pointer_table": {"sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f", "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"}, 
```

3. append two rows to `selftest` (after the `rev_unresolvable` row):

```json
{"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"}, {"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"}
```

Resulting file sha256 on the scratch copy:
`ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` (includes a
trailing newline the real file should not gain).

## Patch 3 — SKILL.md:371 (registry row; protected file, patch text only)

Replace the entire row (old row shown abbreviated at the changed cells only;
new row is the full replacement text):

Old (abbreviated): `| citation-drift | probe / kaidoku | …; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; --strict restores the gate map 0 clean / 1 failed / 2 could-not-evaluate** | same command with --selftest; 11 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent --rev → exit 2, finding revision_unresolvable), the case table committed in expected.json rather than in the script | .ufo/gates/citation-drift/pointer-table.json pins every in-repo citation and expected.json pins the self-test case table; … |`

New (full row):

```
| citation-drift | probe / kaidoku | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; **probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate**; **frozen-run preflight: the table's sha256 must match the digest pinned in `expected.json` — a tampered table (exit 2, finding `pointer_table_tampered`) or an absent table (exit 2, finding `pointer_table_unreadable`) is could-not-evaluate before any entry is graded; a baseline that pins no digest is exit 2, finding `pointer_table_unpinned`; drift reporting is unchanged (rc 0)** | same command with `--selftest`; 13 isolated-fixture cases asserting exit code and a stable finding id (the eleventh is dead/absent `--rev` → exit 2, finding `revision_unresolvable`; the twelfth is a tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is an absent table → exit 2, finding `pointer_table_unreadable`), the case table committed in `expected.json` rather than in the script | `.ufo/gates/citation-drift/pointer-table.json` pins every in-repo citation and `expected.json` pins the self-test case table **and the sha256 of `pointer-table.json` (frozen-run guard; any edit to the table must re-pin the digest in the same commit)**; normal entry read-only over the tree it grades; selftest writes only isolated temp fixture repos; **no line number into an operator-mutable file is pinned** (rule #11) |
```
