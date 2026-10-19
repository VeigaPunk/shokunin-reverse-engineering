# RV-2 — C3 citation-drift coverage

## Claim and selected surface

RV-2 is in C3 (instrument/custody). I selected the citation-drift probe table rather than the custody-pair candidate: the frozen claim says the new `ev_` corpus entries' `recheck:` fields are not graded (`.ufo/waves/arc3-loop1-round12/claims-frozen.md:50-63`). The proposed change is limited to the pointer table and its frozen-run digest; it does not edit either instrument.

The proposed `kind: exact` rows grade the current recheck command text at its pinned corpus line. They do **not** execute the command, establish current availability of an external REA package/cache, or prove that a future recheck reproduces the recorded result.

## First-hand re-derivation at HEAD `0436f4940283072db08e73c0117195847c50d31d`

- **VERIFIED — gap is present.** Parsed `.ufo/gates/citation-drift/pointer-table.json`: `entries=57 quoted=5 exempt=8 total_structural=62`. Filtering entries for the three recheck corpus paths and their recheck lines returned `recheck_line_rows=[]` and `recheck_files_covered=0/3`. The table's pinned source digest is `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` (`expected.json:11-13`).
- **VERIFIED — exact source lines from immutable HEAD objects.** `git show HEAD:<path>` returned:
  - `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5` — `recheck:` names the `inspect-evm-interface` fixture and recorded `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`.
  - `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7` — `recheck:` names `evidence/rederive-commands.txt` and `recompute-ids.mjs`.
  - `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7` — `recheck:` names `identity.txt`, `calls.txt`, and `recompute-ids.py`.
- **REPRODUCED — current probe baseline.** Command: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$PWD" --rev HEAD --strict`

  ```text
  CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  CITATION_DRIFT_REVISION: HEAD
  CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
  CITATION_DRIFT_VERDICT: clean findings=0 exit=0
  ```

  Clean is the baseline only: it does not cover the three recheck lines because the current table has no rows for them. Existing exact-row behavior is in `.ufo/gates/citation-drift/citation-drift-probe.py:168-212`; table digest preflight and entry iteration are at `:294-320`.
- **VERIFIED — custody alternative is already covered at this HEAD.** I re-ran `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch "$scratch"` with `$scratch` created under `/var/tmp`. Output included `case coverage-gate-rejects-duplicate-stanzas PASS`, `case coverage-gate-passes-distinct-five PASS`, and `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. The implementation counts `distinct_paths` by resolved path (`.ufo/gates/custody-pair/custody-pair.py:637-651`); its duplicate and distinct controls are at `:1157-1193`. I therefore did not propose another stanza-count change.

## Patch text — NOT APPLIED

This uses the existing `exact` matcher; the scope is adding three rows and updating the frozen table digest in the same commit. The digest below was computed from the exact serialized candidate table (57 → 60 `entries`).

```diff
--- a/.ufo/gates/citation-drift/pointer-table.json
+++ b/.ufo/gates/citation-drift/pointer-table.json
@@ -532,6 +532,30 @@
       "target_group_end": 2,
       "must_match": "^## arc2-loop1-round4",
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "r7-evm-evidence-id-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "line": 5,
+      "must_match": "^recheck: .*inspect-evm-interface .*arc3-loop1-round7/claims/c2/EX-3/evidence/fixtures/base/selector\\.hex\" hex --format json.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052.*",
+      "note": "Grade the verb-specific recheck command and its pinned expected Evidence ID; this does not attest current external package/cache availability."
+    },
+    {
+      "id": "r10-rust-evidence-id-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: .*cached REA 6\\.7\\.0 command.*evidence/rederive-commands\\.txt.*recompute-ids\\.mjs.*",
+      "note": "Grade the recheck recipe and its local derivation helper reference; this does not attest a fresh REA call."
+    },
+    {
+      "id": "r11-inspect-artifact-evidence-id-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: .*rea-agents@6\\.7\\.0.*identity\\.txt.*calls\\.txt.*recompute-ids\\.py.*",
+      "note": "Grade the recheck recipe and its recorded-call / recomputation references; this does not attest a fresh REA call."
     }
   ],
```

```diff
--- a/.ufo/gates/citation-drift/expected.json
+++ b/.ufo/gates/citation-drift/expected.json
@@
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "8a97f595f77828da87388f42524929c5bf34e07ff50e9c1e3a529051936b3662",
```

The `expected.json` update is coupled to the table rows: changing only the table must produce the probe's declared `pointer_table_tampered` preflight, not grade citations.

## Seeded-fault measurement on scratch

Scratch root: `/var/tmp/kaidoku-r12-rv2-citation-tht61yj_`. The probe was run with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD`, using the scratch table and scratch `expected.json` with the candidate digest. No repository gate or corpus file was changed.

- **REPRODUCED — proposed clean extension.** `entries=57` → `60`; candidate table SHA-256 `8a97f595f77828da87388f42524929c5bf34e07ff50e9c1e3a529051936b3662`.

  ```text
  CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  CITATION_DRIFT_REVISION: HEAD
  CITATION_DRIFT_TABLE: /var/tmp/kaidoku-r12-rv2-citation-tht61yj_/proposed-clean-pointer-table.json
  CITATION_DRIFT_VERDICT: clean findings=0 exit=0
  ```

- **REPRODUCED — seeded stale pointer is caught.** In a separate scratch table only, changed the r11 row's pinned line from `7` to `8`, leaving its `^recheck:` needle unchanged, and re-pinned that scratch table (`a6bea96ef2cc0546915e556d601798d58c264dd67b8aa5eb634e6c791387818b`). Line 8 is not the recheck line in the immutable HEAD source.

  ```text
  CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  CITATION_DRIFT_REVISION: HEAD
  CITATION_DRIFT_TABLE: /var/tmp/kaidoku-r12-rv2-citation-tht61yj_/seeded-stale-pin-pointer-table.json
  CITATION_DRIFT: citation_dead entry=r11-inspect-artifact-evidence-id-recheck corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:8 lacks '^recheck: .*rea-agents@6\\.7\\.0.*identity\\.txt.*calls\\.txt.*r'
  CITATION_DRIFT_VERDICT: failed findings=1 exit=1
  ```

The probe truncates the displayed regex in its diagnostic, but the full needle is stored in the scratch table. This is a citation-liveness check, not verification that the command itself still runs. The proposed extension is scratch-validated only; it is not landed or counted as an after-state at HEAD.

## Per-item verdicts and limits

- r7 `recheck:` row: **VERIFIED** ungraded at HEAD; **REPRODUCED** as part of the clean three-row scratch extension.
- r10 `recheck:` row: **VERIFIED** ungraded at HEAD; **REPRODUCED** as part of the clean three-row scratch extension.
- r11 `recheck:` row: **VERIFIED** ungraded at HEAD; **REPRODUCED** in the clean extension and independently **REPRODUCED** as the seeded stale-line failure.
- Initial draft regex: **CORRECTED** before the final measurement. It omitted the quote between the r7 `.hex` path and the `hex` argument; the final needle includes the quote and the final clean run returned exit 0.
- Landing / integrated after-state: **UNVERIFIABLE** here by scope; this artifact contains patch text only.

The first scratch draft's false findings were caused by that regex typo and by a second incorrect R10 phrase; both were corrected and the final clean/fault pair above was re-run. The live gate files remain untouched. The worktree also had a pre-existing modification at `.ufo/waves/arc2-loop1-round10/C3.md`; this seat did not alter it.
