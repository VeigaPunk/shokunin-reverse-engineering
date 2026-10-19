# RV-5 — C3 citation-drift recheck pins (patch draft)

Patch text and scratch-only measurement. I did not edit `.ufo/gates/`, corpus files, custody paths, or any tracked file. The proposed change extends the citation-drift pointer table and re-pins its expected digest.

## Re-derived at frozen HEAD

- **VERIFIED — revision:** `git rev-parse HEAD` returned `0436f4940283072db08e73c0117195847c50d31d`.
- **VERIFIED — named gap:** a fresh parse of `.ufo/gates/citation-drift/pointer-table.json` measured SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, `entries=57`, `quoted=5`, and `corpus_knowledge_rows=18`. None of the three candidate files is present in either array. `.ufo/gates/citation-drift/expected.json:11-14` independently pins that same current table digest.
- **VERIFIED — source fields:** frozen Git objects contain the `recheck:` lines at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, `...r10-rust-evidence-id-domain.md:7`, and `...r11-inspect-artifact-evidence-id-domain.md:7`. The r7 line gives the input path, verb and expected `ev_` ID; r10 names its command list and recomputation script; r11 names its identity, calls and recomputation files.
- **VERIFIED — baseline probe:** at the same frozen revision, both documented modes returned zero findings:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: reported findings=0 exit=0

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## Proposed patch text

These `exact` entries pin the stated command/evidence identity on each append-only entry's `recheck:` line. They test recorded text at frozen Git content; they do not execute REA or prove external/cache paths remain available. The table digest becomes `06517dc6303d42985735874241ddabbca8f9fc5093827df0deb65a63d6f60318` (57 → 60 entries).

```diff
--- a/.ufo/gates/citation-drift/pointer-table.json
+++ b/.ufo/gates/citation-drift/pointer-table.json
@@ -532,6 +532,30 @@
       "target_group_end": 2,
       "must_match": "^## arc2-loop1-round4",
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "arc3-r7-evm-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "line": 5,
+      "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-evm-interface.*arc3-loop1-round7/claims/c2/EX-3/evidence/fixtures/base/selector\\.hex.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052.*$",
+      "note": "Pins the append-only recheck recipe, disk-backed TMPDIR, input path, verb and measured ID; text check only, not a REA rerun."
+    },
+    {
+      "id": "arc3-r10-rust-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: .*rederive-commands\\.txt.*arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids\\.mjs.*$",
+      "note": "Pins the append-only recheck recipe to its recorded command list and independent ID-recomputation script; text check only, does not execute either."
+    },
+    {
+      "id": "arc3-r11-inspect-artifact-recheck",
+      "kind": "exact",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "line": 7,
+      "must_match": "^recheck: .*identity\\.txt.*TMPDIR.*calls\\.txt.*arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids\\.py.*$",
+      "note": "Pins the append-only recheck recipe to its package identity, disk-backed scratch, captured calls and independent ID-recomputation script; text check only, does not execute them."
     }
   ],
   "quoted": [
--- a/.ufo/gates/citation-drift/expected.json
+++ b/.ufo/gates/citation-drift/expected.json
@@ -9,7 +9,7 @@
     ]
   },
   "pointer_table": {
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "06517dc6303d42985735874241ddabbca8f9fc5093827df0deb65a63d6f60318",
     "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"
   },
```

## Scratch measurement

The proposed table plus digest passed against the unchanged frozen Git tree in strict mode: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`. All three proposed regexes matched their exact frozen corpus lines. Scratch was under `/var/tmp/kaidoku-rv5-bt5g1f40/`.

**REPRODUCED — patch artifact:** the delivered diff passed `patch --dry-run -p1` and was applied to an isolated copy of the two JSON files under `/var/tmp/kaidoku-rv5-patchcheck-01pz3kte/` (both exit 0). The resulting table SHA-256 was `06517dc6303d42985735874241ddabbca8f9fc5093827df0deb65a63d6f60318`, and the expected file contained that pin.

**REPRODUCED — seeded recheck drift:** I copied the r7 corpus entry into a `/var/tmp` snapshot and changed only the ID in its line 5 `recheck:` text from `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052` to the well-formed but wrong `ev_` + 64 zeroes. I pinned that snapshot and the scratch table in scratch `expected.json`, and ran the proposed r7 row against the snapshot:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table /var/tmp/kaidoku-rv5-bt5g1f40/pointer-table-seeded-final.json --expected /var/tmp/kaidoku-rv5-bt5g1f40/expected-seeded-final.json --snapshot-dir /var/tmp/kaidoku-rv5-bt5g1f40/snapshots-final --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-rv5-bt5g1f40/pointer-table-seeded-final.json
CITATION_DRIFT: citation_dead entry=arc3-r7-evm-recheck @r7-recheck-seeded:5 lacks '^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
```

The fault existed only in the scratch snapshot; Git and corpus custody were read-only. This demonstrates the added row detects drift in the measured recheck text. **UNVERIFIABLE —** I did not execute the REA/recomputation recipes themselves; they are not run by this citation-text probe. The probe's `--selftest` also was not run because its fixture builder performs `git init/add/commit` (`citation-drift-probe.py:347-368`), disallowed by the seat's Git-read-only constraint; the direct clean and seeded probe runs exercised the relevant entry path without Git mutation.
