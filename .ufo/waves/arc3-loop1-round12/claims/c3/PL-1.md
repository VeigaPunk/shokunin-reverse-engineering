# PL-1 — C3 operability: citation-drift recheck coverage

**Deliverable:** patch text plus a scratch seeded-fault measurement. The instrument and custody tool were not edited. The proposed patch is the two-file diff below; it extends the citation-drift pointer table and re-pins that table in `expected.json`.

## Claim and verdicts

Claim: extend `.ufo/gates/citation-drift/pointer-table.json` so the three arc3 `ev_` corpus entries' `recheck:` fields are graded. At frozen HEAD `0436f4940283072db08e73c0117195847c50d31d`, the recheck-field gap is **3 present / 0 graded**. With the proposed rows on scratch, all three grade clean; a seeded change to one recheck field is detected as `citation_dead` (strict exit 1). **C3 candidate: REPRODUCED on scratch.** Nothing was landed in the instrument, so an applied source-tree before/after is **UNVERIFIABLE / not claimed**.

Per-item verdicts:

- **REPRODUCED — baseline gap.** `git show` at the frozen revision found one `recheck:` line in each target file (r7 line 5, r10 line 7, r11 line 7), and zero pointer-table rows whose `file` names any target. The table had 57 `entries`, 5 `quoted`, and the measured table digest matched the digest in `expected.json`.
- **REPRODUCED — proposed rows.** The scratch candidate had 60 pointer-table entries, valid JSON, and a matching scratch `expected.json` digest. Strict probe result: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
- **REPRODUCED — seeded fault.** A scratch-only Git-read overlay changed the r11 field from `` `calls.txt` `` to `` `callx.txt` ``. The new `arc3r11-artifact-entry-recheck` anchor reported `citation_dead`; strict verdict was failed, exit 1. The repository Git objects and source file were not changed.
- **REPRODUCED — existing probe self-test.** 13/13 cases passed (command and summary below).
- **UNVERIFIABLE / not claimed — landed instrument change.** This seat delivers the patch as text only, as instructed; it does not apply it.

## First-hand measurements

The frozen revision was resolved with `git rev-parse HEAD`: `0436f4940283072db08e73c0117195847c50d31d`. The root `SCORECARD.md:88-124` Command A recipe was re-run against that revision; exact output:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "0436f4940283072db08e73c0117195847c50d", "rule_blocks": 16}
```

For the gap census, the command loaded the table and target files as immutable Git objects (`git show <rev>:<path>`), counted lines beginning `recheck:`, and matched each target against `entries + quoted` by exact `file` path. Output:

```json
{"expected_digest_matches": true, "expected_pins_table_sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b", "pointer_table_entries": 57, "pointer_table_quoted": 5, "pointer_table_sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b", "revision": "0436f4940283072db08e73c0117195847c50d31d", "target_fields_graded": 0, "target_rechecks": 3, "targets": [{"graded": false, "path": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md", "pointer_table_entry_ids": [], "recheck_field_count": 1, "recheck_lines": [5]}, {"graded": false, "path": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md", "pointer_table_entry_ids": [], "recheck_field_count": 1, "recheck_lines": [7]}, {"graded": false, "path": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md", "pointer_table_entry_ids": [], "recheck_field_count": 1, "recheck_lines": [7]}]}
```

The three target fields and their contents were read directly at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`. The proposed anchors check the invoked verb plus expected ID for r7, the recorded command-source and recomputation references for r10, and the pinned package/scratch/call/recomputation/never-`/tmp` recipe for r11. These are content anchors, not line pins, and they do not execute REA or claim that the commands were run by this probe.

At the frozen revision, the existing strict citation-drift probe printed:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Command: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict`. Its unmodified `expected.json` pointer-table digest was verified before the run. The self-test ran with `TMPDIR` set to a newly created directory under `/var/tmp` (never `/tmp`); output summary: `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` (`--selftest` implementation: `.ufo/gates/citation-drift/citation-drift-probe.py:405-471`; expected cases: `.ufo/gates/citation-drift/expected.json:18-84`).

Scratch candidate output (table and expected files generated from frozen Git objects, not applied):

```text
candidate_entries=['arc3r7-evm-entry-recheck', 'arc3r10-rust-entry-recheck', 'arc3r11-artifact-entry-recheck']
candidate_pointer_count=60
candidate_table_sha256=b151c647ad347af4c76fd155c020b57ced07fb56444d891d190868f01eaa6beb
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Seeded-fault output (the only overlaid Git read was the r11 corpus file; all other Git reads delegated to the real `git` executable):

```text
CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: <scratch>/pointer-table.json
CITATION_DRIFT: citation_dead entry=arc3r11-artifact-entry-recheck corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: no line matches '^recheck: use the pinned `rea-agents@6\\.7\\.0` cache path rec'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
SEEDED_FAULT_EXPECTED_RC=1 OBSERVED_RC=1
```

The scratch directory was under `/var/tmp` and removed after the run. `CUSTODY_PATHS` and `.ufo/gates/custody-pair/custody-pair.py` were not invoked or written; this claim targets citation-drift only.

## Proposed patch text (not applied)

```diff
--- .ufo/gates/citation-drift/pointer-table.json
+++ .ufo/gates/citation-drift/pointer-table.json
@@ -532,6 +532,27 @@
       "target_group_end": 2,
       "must_match": "^## arc2-loop1-round4",
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "arc3r7-evm-entry-recheck",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "must_match": "^recheck: .*inspect-evm-interface .*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052",
+      "note": "The arc3 round-7 entry recheck must retain the invoked verb and its expected Evidence ID; no line pin, so content movement is allowed."
+    },
+    {
+      "id": "arc3r10-rust-entry-recheck",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "must_match": "^recheck: from the lane root, use the cached REA 6\\.7\\.0 command shown in `evidence/rederive-commands\\.txt`; then run `node \\.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids\\.mjs`\\.",
+      "note": "The arc3 round-10 entry recheck must retain both its recorded REA invocation source and the independent ID-recomputation command."
+    },
+    {
+      "id": "arc3r11-artifact-entry-recheck",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "must_match": "^recheck: use the pinned `rea-agents@6\\.7\\.0` cache path recorded in `identity\\.txt`, set `TMPDIR` to a directory under `/var/tmp`, and run the four exact calls in `calls\\.txt`.*Then run `python3 \\.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids\\.py`\\. Do not use `/tmp` for scratch\\.$",
+      "note": "The arc3 round-11 entry recheck must retain its pinned package identity, disk-backed scratch rule, four-call receipt, recomputation step, and never-/tmp constraint."
     }
   ],
   "quoted": [
--- .ufo/gates/citation-drift/expected.json
+++ .ufo/gates/citation-drift/expected.json
@@ -9,7 +9,7 @@
     ]
   },
   "pointer_table": {
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "b151c647ad347af4c76fd155c020b57ced07fb56444d891d190868f01eaa6beb",
     "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"
   },
   "snapshots": {
```

The candidate table digest above was calculated over the exact bytes generated by inserting the three rows into the frozen table (retaining its formatting) and was used in the scratch `expected.json`. The patch adds rows in the existing `entries` array; it does not modify the gate implementation or custody tool. Apply only after independent review and rerun the strict probe and its self-test.
