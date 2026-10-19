# PL-2 — citation-drift coverage for `ev_` recheck fields

## Disposition

Selected C3 candidate (a): grade the `recheck:` fields of the three `ev_` corpus entries. This is a **patch draft**, not an instrument edit: add three `exact` rows to `.ufo/gates/citation-drift/pointer-table.json` and update the frozen table digest in `expected.json` in the same landing. The proposed rows check recorded recipe text and stable command/input anchors; they do not execute REA or establish that a future invocation will succeed.

## First-hand re-derivation

**VERIFIED — coverage gap at HEAD.** `git rev-parse HEAD` returned `0436f4940283072db08e73c0117195847c50d31d`. I read the corpus files and pointer table from that immutable Git revision and matched each `recheck:` line number against the table's `entries` and `quoted` rows:

```text
revision=0436f4940283072db08e73c0117195847c50d31d
table_entries=57 quoted=5 total_graded=62
corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5: recheck_lines=1 graded_recheck_entries=[]
corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7: recheck_lines=1 graded_recheck_entries=[]
corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7: recheck_lines=1 graded_recheck_entries=[]
```

The actual recipe lines are `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`. Their contents respectively carry the `inspect-evm-interface` fixture command and expected ID, the Rust command/recomputation evidence paths, and the artifact call/identity inputs plus recomputation script. The baseline table ends with its 57th `entries` row at `pointer-table.json:525-535`; no row targets those three files/lines. `expected.json:11-14` pins the existing table digest.

**REPRODUCED — current instrument baseline.** Command:

```text
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict
```

Exact verdict line: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

**Attempted, inadmissible — selftest (not verification evidence).** The rerun with `TMPDIR=/var/tmp/kaidoku-pl2-selftest.HWjnQC` printed `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`, but `--selftest` calls `git init`, `git add`, and `git commit` in temporary fixture repositories (`citation-drift-probe.py:347-367`), violating this wave's Git-read-only rule. An earlier invocation also omitted `TMPDIR`, using Python's default temp root. Neither selftest run is counted as evidence; I did not repeat it.

The probe's exact-entry check is `citation-drift-probe.py:191-209`; it grades table rows from the pinned table in `:294-320`. The table's digest guard is described in `citation-drift-probe.py:34-40` and registered as same-commit work at `SKILL.md:426`.

## Proposed patch text — not applied

```diff
diff --git a/.ufo/gates/citation-drift/pointer-table.json b/.ufo/gates/citation-drift/pointer-table.json
@@
     {
       "id": "census-cites-sc-round4-range",
       "kind": "extracted",
       "file": ".ufo/gates/c1-census-v10.py",
       "line": 27,
       "pattern": "SCORECARD\\.md:(\\d+)-(\\d+)",
       "target": "SCORECARD.md",
       "target_group": 1,
       "target_group_end": 2,
       "must_match": "^## arc2-loop1-round4",
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "arc3r7-ev-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "line": 5,
+      "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck .*inspect-evm-interface .*fixtures/base/selector\\.hex.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`; ",
+      "note": "Grades the r7 ev_ recheck recipe line, including its disk-backed TMPDIR, selected fixture, verb, and recorded expected ID. Textual pointer check only; it does not execute REA."
+    },
+    {
+      "id": "arc3r10-rust-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: from the lane root, use the cached REA 6\\.7\\.0 command shown in `evidence/rederive-commands\\.txt`; then run `node \\.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids\\.mjs`\\.",
+      "note": "Grades the r10 rust ev_ recheck recipe line and its named command/recomputation paths. Textual pointer check only; it does not execute REA."
+    },
+    {
+      "id": "arc3r11-artifact-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: use the pinned `rea-agents@6\\.7\\.0` cache path recorded in `identity\\.txt`, set `TMPDIR` to a directory under `/var/tmp`, and run the four exact calls in `calls\\.txt` .* Then run `python3 \\.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids\\.py`\\. Do not use `/tmp` for scratch\\.$",
+      "note": "Grades the r11 artifact ev_ recheck recipe line, including its identity/call inputs, disk-backed TMPDIR, and recomputation script. Textual pointer check only; it does not execute REA."
     }
   ],
```

```diff
diff --git a/.ufo/gates/citation-drift/expected.json b/.ufo/gates/citation-drift/expected.json
@@
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "78d86b550b6a1e88d1c109b54c4ad8c666c141ee9db5028be3f82b75d7f9281c",
```

The proposed table has 60 `entries`, 5 `quoted`, and 8 `exempt`; the 60 `entries` IDs are distinct. Thus 65 rows are graded (60 entries + 5 quoted records); exempt tokens are not graded rows. The SHA-256 above was derived from the exact JSON round-trip of the current table plus these three rows (round-trip byte-identical to the original); it must be regenerated if the text changes.

## Scratch measurement

Scratch files only: `/var/tmp/kaidoku-pl2-c3-4054ziha/pointer-table.after2.json` and `expected.after2.json`. I ran the unmodified probe with the proposed table and updated pin against the immutable HEAD tree:

```text
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table /var/tmp/kaidoku-pl2-c3-4054ziha/pointer-table.after2.json --expected /var/tmp/kaidoku-pl2-c3-4054ziha/expected.after2.json --strict
```

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-pl2-c3-4054ziha/pointer-table.after2.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

**REPRODUCED — seeded fault.** Because the probe resolves targets with `git show` and the wave forbids Git mutation, I injected the fault only in an in-memory `git_show` overlay while running the unchanged `run_check()` against the scratch table: on the r10 line 7, `recompute-ids.mjs` became `missing-recompute-ids.mjs`. Result:

```text
FAULT_INJECTED: corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7 recompute-ids.mjs -> missing-recompute-ids.mjs (in-memory git_show overlay; no Git mutation)
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-pl2-c3-4054ziha/pointer-table.after2.json
CITATION_DRIFT: citation_dead entry=arc3r10-rust-recheck corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7 lacks '^recheck: from the lane root, use the cached REA 6\\.7\\.0 com'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
```

The seeded input change therefore turns the clean scratch run into exactly one declared failure; it does not alter the repository, the instrument, or any Git object.

## Limits and process note

`VERIFIED` for the gap; `REPRODUCED` for the proposed checks and seeded fault. **UNVERIFIABLE** as a landed instrument improvement: the patch was not applied, per the seat's write boundary. The exact rows grade text anchors only; they do not check filesystem existence of every referenced artifact nor execute the external REA call.

Process deviation: the first selftest invocation omitted `TMPDIR` and used Python's default temporary root; the second used `/var/tmp`, but both executed the selftest's temporary `git init/add/commit` fixture setup. Its `TemporaryDirectory` and fixture cleanup paths removed the case data (`citation-drift-probe.py:415-466`). No Git mutation touched the repository; temporary Git repositories were nevertheless created/committed, contrary to the wave constraint. No gate, custody, corpus, skill, scorecard, province, or log file was modified by this seat.
