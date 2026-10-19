# EX-23 — reference recipe: the citation-drift frozen-run guard (patch text, NOT applied)

Seat EX-23 | chain c2 | executor | 2026-10-19 | HEAD `e845c2b`

Owner note: `.ufo/gates/citation-drift/` is **EX-16's** real target; nothing here
was applied or committed. This artifact is the exact recipe the EX-23 census
measured (`falsepositives.md`), offered so the landing can adopt a
selftest-green shape in one pass. Raw diff: `harness/guard-recipe.diff` (65
lines, sha256 `ccea662ab643f8e9d13a8ee764225e653e7dce6fb58103fb40481a5fe59cd26f`).

## 1. What the census proved the recipe must satisfy

1. **The new finding id must be registered in `Findings.verdict()`'s CNE
   tuple.** Without it: probe semantics `exit=0`, `--strict` `exit=1` (a false
   failure on honest edits) — the declared exit-2 class fails (census D1).
2. **The guard must hash the file actually loaded (`--table`),** not only the
   default path (RV-6 attack 6; census §5.2).
3. **The selftest's per-case `expected.json` must pin the fixture table it was
   built with**, else 9 of the 11 existing cases fail (census D2). The two new
   cases then demonstrate the classes: `table_tampered` → exit 2
   `pointer_table_tampered`; `table_absent` → exit 2 `pointer_table_unreadable`.
4. **Guard code + pin land in the same commit** — a revision whose
   `expected.json` lacks the pin reads `unpinned_legacy` exit 2 for every run
   (census W2). The pin is the digest of the **landing-commit** table
   `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
   (the table does not exist at `frozen_run.revision` `679af5d…`; census W3).
5. Optional hardening (census §5.7): parse the bytes that were hashed
   (`table = json.loads(table_bytes)`) instead of re-reading the file, closing
   the microsecond TOCTOU window. Not required for the census's measurements.

## 2. Diff — `citation-drift-probe.py`

```diff
--- a/.ufo/gates/citation-drift/citation-drift-probe.py	(HEAD, 3067621a…)
+++ b/.ufo/gates/citation-drift/citation-drift-probe.py	(guardC recipe)
@@ -70,7 +70,8 @@
         if not self.rows:
             return CLEAN
         if any(f in ("snapshot_tampered", "snapshot_missing",
-                     "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_unreadable", "pointer_table_tampered",
+                     "unpinned_legacy",
                      "root_unreadable", "revision_unresolvable", "internal_error")
                for f, _, _ in self.rows):
             return CNE
@@ -287,6 +288,25 @@
     except (OSError, ValueError) as exc:
         expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
+    # Frozen-run guard: the table is the contract, so its bytes are pinned in
+    # expected.json. The run cannot tell an honest in-flight re-key from a
+    # tamper, so a digest mismatch is could-not-evaluate, never a finding set.
+    try:
+        table_bytes = open(table_path, "rb").read()
+    except OSError as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path),
+                     str(exc))
+        return findings
+    pinned_table = (expected.get("frozen_run") or {}).get("table_sha256")
+    if pinned_table is None:
+        findings.add("unpinned_legacy", os.path.basename(table_path),
+                     "no table digest pinned in expected.json")
+        return findings
+    if sha256_bytes(table_bytes) != pinned_table:
+        findings.add("pointer_table_tampered", os.path.basename(table_path),
+                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes),
+                                                 pinned_table))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -399,7 +419,8 @@
                 else:
                     root = build_fixture(case)
                     table = os.path.join(case_dir, "table.json")
-                    json.dump(fixture_table(case), open(table, "w"))
+                    if case != "table_absent":
+                        json.dump(fixture_table(case), open(table, "w"))
 
                 snapshot_dir = os.path.join(case_dir, "snap")
                 os.makedirs(snapshot_dir)
@@ -413,6 +434,16 @@
                 else:
                     digests = {}
                 expected = {"snapshots": digests}
+                # frozen-run guard: the fixture run pins the digest of the
+                # table it was built with, so the guard stays universal
+                if case == "table_tampered":
+                    expected["frozen_run"] = {"table_sha256": "0" * 64}
+                elif case == "table_absent":
+                    expected["frozen_run"] = {
+                        "table_sha256": sha256_bytes(b"absent on purpose")}
+                else:
+                    expected["frozen_run"] = {
+                        "table_sha256": sha256_bytes(open(table, "rb").read())}
                 exp_file = os.path.join(case_dir, "expected.json")
                 json.dump(expected, open(exp_file, "w"))
```

## 3. `expected.json` — pin + the two new selftest cases

`frozen_run` gains one key (the digest of the committed
`pointer-table.json`):

```json
"table_sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f"
```

`selftest` gains two rows (verbatim shape measured):

```diff
     {
       "case": "rev_unresolvable",
       "exit_code": 2,
       "finding": "revision_unresolvable"
+    },
+    {
+      "case": "table_tampered",
+      "exit_code": 2,
+      "finding": "pointer_table_tampered"
+    },
+    {
+      "case": "table_absent",
+      "exit_code": 2,
+      "finding": "pointer_table_unreadable"
     }
   ]
 }
```

The frozen claim names the new coverage "clean-tree, tampered-table,
absent-table"; the arithmetic 11 + 2 = 13 matches two new cases. If EX-16
prefers a `clean-tree` case name for a third row, the count must still land at
13 and the case table stays authoritative in `expected.json`.

## 4. Measured with this recipe (all re-runnable: `harness/census.py`,
`harness/selftest-proof.py`)

| check | result |
|---|---|
| selftest, 13-case table, 6 reps | `CLEAN cases=13 passed=13 failed=0 exit=0` |
| 11 honest in-flight edits, probe + strict | exit 2 both, `pointer_table_tampered`, no traceback |
| clean tree | `findings=0 exit=0` (unchanged) |
| honest edit + same-commit re-pin | `findings=0 exit=0` |
| absent / invalid / dir / binary / unpinned / malformed-pin | exit 2, typed CNE finding (§4 of `falsepositives.md`) |
| variants that fail the recipe | `guardA` (id unregistered): probe 0 / strict 1; `guardB` (no selftest pin): 9/11 cases fail |

## 5. Not covered here (other seats' scope)

- `SKILL.md:371` registry-row text — EX-20's patch text (verified by SC-4);
  the row must name the exact ids this recipe emits.
- The final wording of the mismatch finding's detail line: the census proposes
  appending a remediation hint (`re-pin expected.json frozen_run.table_sha256
  in the same commit if this edit is yours`) — optional, clarity-only.
