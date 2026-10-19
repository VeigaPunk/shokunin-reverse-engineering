# arc3-loop1-round1 — chain c2 consolidated changeset (seat SC-4, scribe)

Assembled 2026-10-19T07:09, finalized 07:18 by seat SC-4. Sources: EX-16's landed
real-target writes (captured read-only via `git diff`), PL-2's authoring patch
text, EX-20's `SKILL.md` registry-row patch text, EX-21's prototype patch.
**Nothing here was applied or committed by SC-4**; the parent integrates.

Baseline: HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`. The worktree also
carries a pre-existing unrelated modification (`.ufo/waves/arc2-loop1-round10/C3.md`)
— not part of this changeset.

**Landing status: EX-16's change LANDED in the worktree at 07:15** (per PL-2's
`frozen-run-guard.patch.md`, applied by EX-16). Captured sha256s:
probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`,
expected `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`,
table unchanged `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`.

C2 frozen claim (`.ufo/waves/arc3-loop1-round1/claims-frozen.md:40-54`): pin the
sha256 of `pointer-table.json` in `expected.json`; a tampered or absent table
yields the declared preflight could-not-evaluate class (exit 2), never silent
findings; the `SKILL.md` registry row states the guard semantics; selftest
11 → 13 cases at exit 0; findings = 0 at HEAD.

## 1. Manifest

| # | Target | Action | Source seat | before sha256 | after sha256 | Status |
|---|---|---|---|---|---|---|
| A | `.ufo/gates/citation-drift/citation-drift-probe.py` | **landed (real target)** | PL-2 authored → EX-16 applied | `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` | **verified by SC-4** (§2) |
| B | `.ufo/gates/citation-drift/expected.json` | **landed (real target)** | PL-2 authored → EX-16 applied | `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` | **verified by SC-4** (§2) |
| C | `.ufo/gates/citation-drift/pointer-table.json` | must stay byte-stable | — | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` | unchanged (pin matches it) | **verified** |
| D | `SKILL.md:371` (citation-drift registry row) | patch text only — **two competing texts** | EX-20 and PL-2 (patch 3) | row `6413e8dc…` | EX-20 row `08be1ec2…` (file `fa94a469…`); PL-2 row `d25c5292…` (file `483b0eba…`) | **DECISION NEEDED** (§3) |
| E | candidate probe+expected (EX-21 prototype) | prototype, superseded by A/B | EX-21 | — | probe `776cef6a…`, expected `376f9fc5…` | defects D1/D2 (§4); not the landing shape |
| F | SC-4 landing kit (fail-closed variant, flat `table_sha256` shape) | patch text, superseded by A/B | SC-4 | applies to A `3067621a…` | probe `28cc1187…` | kept as a fallback shape (§4 note) |

Artifacts referenced:

| Artifact | sha256 | Seat |
|---|---|---|
| `claims/c2/SC-4/diff-ex16.txt` (verbatim capture of the landed diff, 95 lines) | `78ae7971d12627cba45bc75ba22288f55cc2effaf951b6165e61a26a63fc7836` | SC-4 |
| `claims/c2/SC-4/verify-before.txt` / `verify-after.txt` | 11 checks each, pre/post | SC-4 |
| `claims/c2/SC-4/verify-proto.txt` / `verify-failclosed.txt` | prototype + fail-closed matrices | SC-4 |
| `claims/c2/SC-4/verify-changeset.sh`, `verify-proto.sh`, `verify-failclosed.sh` | harnesses (TMPDIR redirected into `claims/c2/SC-4/scratch/tmp`; /tmp hit the user quota) | SC-4 |
| `claims/c2/SC-4/proposed-guard-failclosed.patch.md` | verified patch text (extracted diff re-applies byte-identical) | SC-4 |
| `claims/c2/PL-2/frozen-run-guard.patch.md` | 3 patches: probe, expected.json, SKILL.md row | PL-2 |
| `claims/c2/EX-20/registry-row.patch.md` | `3a6a4230c9f2d1daea3ab5d276e5dbc46a46f663f70eb7505b0c8f626c32bc8e` | EX-20 |
| `claims/c2/EX-21/tmp/proto/probe.py`, `logs/proto-probe.diff` | `776cef6a…`, `bb22aa8a…` (stale) | EX-21 |

## 2. Landed diff (real target) — captured and verified

`git diff --stat -- .ufo/gates/citation-drift/`:

```
 .ufo/gates/citation-drift/citation-drift-probe.py | 48 +++++++++++++++++++----
 .ufo/gates/citation-drift/expected.json           |  2 +-
 2 files changed, 41 insertions(+), 9 deletions(-)
```

Verbatim capture: `claims/c2/SC-4/diff-ex16.txt` (sha256 `78ae7971…`), also
reproduced in EX-16's `landing-diff.md`. Re-verified unchanged at 07:19 (same
three sha256s), so this listing matches the worktree state at close. The diff:

```diff
diff --git i/.ufo/gates/citation-drift/citation-drift-probe.py w/.ufo/gates/citation-drift/citation-drift-probe.py
index ab3146c..f88dc28 100644
--- i/.ufo/gates/citation-drift/citation-drift-probe.py
+++ w/.ufo/gates/citation-drift/citation-drift-probe.py
@@ -31,6 +31,14 @@ TARGETS
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
 
@@ -70,7 +78,8 @@ class Findings:
         if not self.rows:
             return CLEAN
         if any(f in ("snapshot_tampered", "snapshot_missing",
-                     "pointer_table_unreadable", "unpinned_legacy",
+                     "pointer_table_unreadable", "pointer_table_tampered",
+                     "pointer_table_unpinned", "unpinned_legacy",
                      "root_unreadable", "revision_unresolvable", "internal_error")
                for f, _, _ in self.rows):
             return CNE
@@ -277,16 +286,31 @@ def run_check(root, rev, table_path, expected_path, snapshot_dir):
         findings.add("revision_unresolvable", rev,
                      "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
         return findings
-    try:
-        table = json.load(open(table_path))
-    except (OSError, ValueError) as exc:
-        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
-        return findings
     try:
         expected = json.load(open(expected_path))
     except (OSError, ValueError) as exc:
-        expected = {}
         findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
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
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
+    if sha256_bytes(table_bytes) != pin:
+        findings.add("pointer_table_tampered", os.path.basename(table_path),
+                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pin))
+        return findings
+    try:
+        table = json.loads(table_bytes.decode("utf-8"))
+    except (ValueError, UnicodeDecodeError) as exc:
+        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
+        return findings
     tree = Tree(root, rev, snapshot_dir, expected, findings)
     for entry in table.get("entries", []):
         check_entry(entry, tree, findings)
@@ -412,9 +436,17 @@ def selftest(expected_path):
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
diff --git i/.ufo/gates/citation-drift/expected.json w/.ufo/gates/citation-drift/expected.json
index b089564..1bd661d 100644
--- i/.ufo/gates/citation-drift/expected.json
+++ w/.ufo/gates/citation-drift/expected.json
@@ -1 +1 @@
-{"_doc": "Committed expected values for the citation-drift gate. Per the PROTOCOL Gate standard: the frozen-run baseline pins the digest of every snapshot input file, and the self-test's expected exit codes and finding ids live here rather than in the script, so the expected values are independent of the recomputation.", "frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement", "verdict": "failed", "expected_findings": ["citation_dead"]}, "snapshots": {"config-toml-landmarks": "387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154"}, "selftest": [{"case": "clean", "exit_code": 0, "finding": "citations_clean"}, {"case": "dead", "exit_code": 1, "finding": "citation_dead"}, {"case": "out_of_range", "exit_code": 1, "finding": "citation_out_of_range"}, {"case": "file_absent", "exit_code": 1, "finding": "citation_file_absent"}, {"case": "moved", "exit_code": 1, "finding": "citation_moved"}, {"case": "stamped", "exit_code": 0, "finding": "citation_historical_ok"}, {"case": "no_snapshot_dir", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "snapshot_missing", "exit_code": 2, "finding": "snapshot_missing"}, {"case": "snapshot_tampered", "exit_code": 2, "finding": "snapshot_tampered"}, {"case": "table_unreadable", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "rev_unresolvable", "exit_code": 2, "finding": "revision_unresolvable"}]}
\ No newline at end of file
+{"_doc": "Committed expected values for the citation-drift gate. Per the PROTOCOL Gate standard: the frozen-run baseline pins the digest of every snapshot input file AND of the pointer table itself (a tampered or absent table is could-not-evaluate, never silent findings), and the self-test's expected exit codes and finding ids live here rather than in the script, so the expected values are independent of the recomputation.", "frozen_run": {"revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f", "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement", "verdict": "failed", "expected_findings": ["citation_dead"]}, "pointer_table": {"sha256": "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f", "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"}, "snapshots": {"config-toml-landmarks": "387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154"}, "selftest": [{"case": "clean", "exit_code": 0, "finding": "citations_clean"}, {"case": "dead", "exit_code": 1, "finding": "citation_dead"}, {"case": "out_of_range", "exit_code": 1, "finding": "citation_out_of_range"}, {"case": "file_absent", "exit_code": 1, "finding": "citation_file_absent"}, {"case": "moved", "exit_code": 1, "finding": "citation_moved"}, {"case": "stamped", "exit_code": 0, "finding": "citation_historical_ok"}, {"case": "no_snapshot_dir", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "snapshot_missing", "exit_code": 2, "finding": "snapshot_missing"}, {"case": "snapshot_tampered", "exit_code": 2, "finding": "snapshot_tampered"}, {"case": "table_unreadable", "exit_code": 2, "finding": "pointer_table_unreadable"}, {"case": "rev_unresolvable", "exit_code": 2, "finding": "revision_unresolvable"}, {"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"}, {"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"}]}
\ No newline at end of file
```

**Traceability to the authoring patch (SC-4 checks):**

- PL-2 patch 1 (probe diff, `frozen-run-guard.patch.md`) extracted and applied
  to a pristine `git show HEAD:` copy with `patch -p1` → rc 0, result sha
  `e2665074…` = the landed probe, **byte-identical**.
- PL-2 patch 2 (three text edits on `expected.json`) replayed by SC-4 →
  result **byte-identical** to the landed file, sha `ff47bfd6…`; valid JSON.
  (PL-2's note that the recorded hash "includes a trailing newline" is
  inaccurate — the landed file ends at `}` with no trailing newline and still
  hashes to `ff47bfd6…`; a doc nit only.)

**Acceptance — after leg, `claims/c2/SC-4/verify-after.txt` (11 checks):**

| # | Run | Before (HEAD) | After (landed) |
|---|---|---|---|
| 1 | `--selftest` | `CLEAN cases=11 passed=11 failed=0 exit=0` | `CLEAN cases=13 passed=13 failed=0 exit=0` |
| 2 | probe at HEAD | `reported findings=0 exit=0` | `reported findings=0 exit=0` |
| 3 | `--strict` at HEAD | `clean findings=0 exit=0` | `clean findings=0 exit=0` |
| 4 | emptied table via `--table` | `reported findings=0 exit=0` (silent) | `pointer_table_tampered … exit=2` |
| 5 | weakened `must_match` table | silent rc 0 | `pointer_table_tampered … exit=2` |
| 6 | absent table path | `pointer_table_unreadable … exit=2` | same |
| 7 | pin vs table bytes | no pin present | `PINNED pointer_table.sha256 = 738b3a56…`, equals actual |
| 8 | unpinned expected + real table | silent rc 0 | `pointer_table_unpinned … exit=2` |
| 9 | findings on a tampered run | `finding_lines=0` | `finding_lines=1` (no entry evaluation) |
| 10 | default-path run, foreign CWD | `reported findings=0 exit=0` | same |
| 11 | forged `--expected` (pin recomputed for a tampered table) | silent rc 0 | silent rc 0 — residual limit (§6) |

## 3. `SKILL.md:371` registry row — two competing patch texts (DECISION NEEDED)

Both texts replace the same row and both leave `SKILL.md` at 371 lines with a
5-cell row (SC-4 verified both by application to a pristine copy):

- **EX-20's** `registry-row.patch.md`: applies with `patch -p1` (rc 0); row
  `6413e8dc…` → `08be1ec2…`; file `5c93c7c1…` → `fa94a469…`. But its cell 3
  names the tampered-table finding **`table_tampered`** — the landed code emits
  **`pointer_table_tampered`**; and its "unpinned" clause is generic (true under
  the landed fail-closed guard). **Applying as written would publish a wrong
  finding id.**
- **PL-2's patch 3** (`frozen-run-guard.patch.md`, "Patch 3 — SKILL.md:371"):
  new row sha `d25c5292…`; resulting file sha `483b0eba…`; 5 cells, 371 lines.
  It names the landed ids exactly (`pointer_table_tampered`,
  `pointer_table_unreadable`, `pointer_table_unpinned`), states the
  preflight ordering, the 13-case count with the twelfth/thirteenth described,
  and the re-pin rule.

**SC-4 recommendation:** land PL-2's patch 3 (id-consistent with the code and
with the landed `expected.json`), or apply EX-20's with the
`table_tampered` → `pointer_table_tampered` substitution. Do not apply both.

## 4. EX-21 prototype and SC-4 kit — superseded, kept for the record

- EX-21's prototype (`776cef6a…`) implemented the guard with a flat
  `table_sha256` key and skip-on-unpinned. Measured (`verify-proto.txt`): guard
  fires when pinned (exit 2), but **P4** showed the one-field pin deletion
  restores silence — the hole the landed fail-closed shape closes.
- **Defect D1:** EX-21's published `proto-probe.diff` (`bb22aa8a…`) is stale
  relative to its own prototype: applying it yields sha `ea364f2d…` and a
  selftest failing 4 cases (`passed=9 failed=4 exit=1`). The diff must not be
  applied as a landing patch.
- SC-4's kit (`proposed-guard-failclosed.patch.md`) measured the fail-closed
  option before the landing; it uses the flat `table_sha256` key, so it is a
  fallback shape only — the landed shape uses `pointer_table.sha256`.

## 5. Coupling verdicts against the landed code

1. **Finding ids (landed):** `pointer_table_tampered` (digest mismatch),
   `pointer_table_unreadable` (absent/unreadable/undecodable table),
   `pointer_table_unpinned` (no pin). EX-20's row needs the substitution in §3;
   PL-2's patch 3 is already consistent. EX-21's case names (`table_tampered`,
   `table_absent`) match the landed `expected.json` case table.
2. **Unpinned semantics:** the landed guard is **fail-closed** (`pointer_table_unpinned`
   → exit 2 before any entry is graded; measured check 8). EX-20's row's
   "unpinned → could-not-evaluate" clause is therefore true as written; EX-24's
   R2 recommendation is satisfied.
3. **Case count:** 13 landed (11 + `table_tampered` + `table_absent`), matching
   both row texts.
4. **Selftest harness coupling:** the landed selftest pins each fixture table's
   digest and writes the tampered/absent shapes after the pin — 13/13 measured.
5. **Behavior change to note:** an unreadable `expected.json` now returns early
   with `pointer_table_unreadable` (before: `expected = {}` and continue). Same
   exit class, earlier stop — consistent with the guard's preflight ordering.
6. **`--table` path independence:** the guard hashes the table path actually
   loaded (checks 4/5 use non-default paths and fire; check 10 shows the default
   path resolves from a foreign CWD).

## 6. Residual risks and housekeeping (for the parent's round report)

- **Forged `--expected` remains silent** (measured on the landed code, check 11):
  a caller who passes an `expected.json` whose pin was recomputed for a tampered
  table reads `findings=0 exit=0`. Inherent to a pin that lives in a file the
  caller can point elsewhere (EX-24 T2/T5/T6 class). The guard is drift
  detection among honest writers, not tamper-proofing.
- **Re-pin rule:** every future edit to `pointer-table.json` must re-pin
  `expected.json.pointer_table.sha256` in the same commit or the probe exits 2 in
  both modes. Stated in the landed docstring and in PL-2's row text.
- **Housekeeping at integration:** untracked bytecode appeared this wave —
  `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` and
  `.ufo/gates/citation-drift/__pycache__/citation-drift-probe.cpython-314.pyc`.
  Neither belongs in the landing commit (precedent: the stray `e16-table.json`
  removed in `265e1aa`).
- Pre-existing, not introduced here: `expected.json`'s
  `snapshots.config-toml-landmarks` pin is unreferenced by the table (no `@`
  targets remain), and the `exempt`/`frozen_run` blocks are inert (RV-6
  attack 9).

## 7. Close-out

Verified by SC-4: the landed probe and `expected.json` (patch-fidelity from
PL-2's text, byte-identical), the pin against the table bytes, selftest 13/13,
probe findings=0 in both modes, all three guard exit-2 classes, guard ordering
(single finding), default-path/CWD independence, both `SKILL.md` row candidates,
and the pre-state gap (11/11, silent tamper classes) for the before→after pair.

Open items handed to the parent: (a) choose and apply one `SKILL.md` row text
(§3); (b) drop the two `__pycache__` strays at integration; (c) EX-21's stale
`proto-probe.diff` (D1) should be regenerated or marked superseded in its
report; (d) SCORECARD/LOG records for this claim are other seats' patch texts,
not part of this listing.

No repo file was modified by SC-4 beyond this seat's own artifact directory; no
git mutation was run; the real target was only read.
