# RV-8 — citation-drift coverage for `ev_` rechecks (C3 draft)

**Status:** proposal for parent integration only. I changed only this artifact. The gate, pointer table, expected pin, corpus, and custody sources were not edited in the repository.

## First-hand measurement at immutable HEAD

`VERIFIED` — project `HEAD` is `0436f4940283072db08e73c0117195847c50d31d`. The live citation-drift script hash is `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`, identical to `git show HEAD`'s script hash. The pointer-table hash at HEAD is `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, equal to `expected.json`'s pinned hash (`.ufo/gates/citation-drift/expected.json:11-13`).

`REPRODUCED` — parsed the pointer-table from the HEAD Git object: `entries=57`, `quoted=5`, `exempt=8`. For each of the three named corpus entries below, no table entry's `file` or `target` names that corpus file; the corresponding one-line `recheck:` field is therefore not evaluated by the table:

- r7 `inspect-evm-interface`: `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`.
- r10 `inspect_rust_binary`: `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`.
- r11 `inspect_artifact`: `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`.

Exact HEAD-object census output:

```text
HEAD 0436f4940283072db08e73c0117195847c50d31d
script_sha256_HEAD e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a
script_sha256_worktree e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a
table_sha256_HEAD 1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b
table_sha256_pinned 1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b
table_entries 57 quoted 5 exempt 8
ENTRY corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md: recheck_line_count=1 recheck_line_numbers=[5] gated_table_refs=[]
ENTRY corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md: recheck_line_count=1 recheck_line_numbers=[7] gated_table_refs=[]
ENTRY corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: recheck_line_count=1 recheck_line_numbers=[7] gated_table_refs=[]
all_3_rechecks_ungraded True
```

The current instrument reports no finding for this gap:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Its existing `anchor` evaluator searches the named file for `must_match` and emits `citation_dead` if there is no hit (`.ufo/gates/citation-drift/citation-drift-probe.py:180-189`); table entries are graded at `:314-319`. The existing self-test remains green: `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` → `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`.

## Proposed patch text (not applied)

Append these three `anchor` entries to `.ufo/gates/citation-drift/pointer-table.json`'s `entries` array. They use no corpus line pins: the table grades the command-bearing recheck form, not a volatile line number. In the same integration commit, update the frozen pointer-table SHA in `expected.json` as shown.

```diff
--- a/.ufo/gates/citation-drift/pointer-table.json
+++ b/.ufo/gates/citation-drift/pointer-table.json
@@ -532,6 +532,27 @@
       "target_group_end": 2,
       "must_match": "^## arc2-loop1-round4",
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "arc3r7-evm-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck .*inspect-evm-interface .* hex --format json",
+      "note": "Grade this command-bearing recheck signature without pinning the corpus line number; this does not execute the command or prove cache availability."
+    },
+    {
+      "id": "arc3r10-rust-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "must_match": "^recheck: .*evidence/rederive-commands\\.txt.*recompute-ids\\.mjs",
+      "note": "Grade the rederive-command and recomputation references without pinning the corpus line number; referenced evidence stays read-only."
+    },
+    {
+      "id": "arc3r11-artifact-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "must_match": "^recheck: .*TMPDIR.*/var/tmp.*calls\\.txt.*recompute-ids\\.py",
+      "note": "Grade the disk-backed scratch, calls, and recomputation signature without pinning the corpus line number; this does not execute the command."
     }
   ],
   "quoted": [
--- a/.ufo/gates/citation-drift/expected.json
+++ b/.ufo/gates/citation-drift/expected.json
@@ -10,5 +10,5 @@
   },
   "pointer_table": {
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "986e63d3405f2a55656f452febf3c204c39f2d86dad47adfe860042e98343d76",
     "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"
   },
```

The candidate table was constructed in `/var/tmp` from the HEAD table bytes and these rows. It parses as `entries=60`, `quoted=5`, `exempt=8`, SHA-256 `986e63d3405f2a55656f452febf3c204c39f2d86dad47adfe860042e98343d76`. Independent regex checks found exactly one expected line in each live HEAD corpus entry: r7 line 5, r10 line 7, r11 line 7. Running the unmodified project probe against that complete scratch table and the immutable project HEAD reproduced a clean control:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed/full-candidate-pointer-table-v2.json --expected /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed/full-candidate-expected-v2.json --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed/full-candidate-pointer-table-v2.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## Seeded-fault measurement

`REPRODUCED` — a three-entry scratch table using the proposed anchors passed on a small scratch Git fixture. I then removed the r11 `recheck:` line only in that `/var/tmp` fixture, committed the scratch fault there, and reran the unchanged project probe in strict mode. The detector identified the missing field as `citation_dead` with exit 1:

```text
# Clean fixture control
CITATION_DRIFT_ROOT: /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0

# Faulted fixture: r11 recheck line removed
CITATION_DRIFT_ROOT: /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-rv8-arc3-loop1-round12-seed/pointer-table.json
CITATION_DRIFT: citation_dead entry=arc3r11-artifact-recheck corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: no line matches '^recheck: .*TMPDIR.*/var/tmp.*calls\\.txt.*recompute-ids\\.py'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
SEEDED_PROBE_EXIT=1
```

The fault was seeded only under `/var/tmp/kaidoku-rv8-arc3-loop1-round12-seed`; the live instrument and worktree corpus were not altered. This patch grades that the three recheck fields retain their named command signatures. It does **not** execute those commands, resolve every path mentioned inside them, or establish that the external REA cache/toolchain remains available; those are outside this measurement.

## Verdicts

- `REPRODUCED` — the current 57-entry table misses all three named `ev_` recheck fields while the probe reports clean.
- `VERIFIED` — adding three no-line-pin anchors yields a 60-entry candidate table that parses, stays clean on unmodified HEAD, and preserves the frozen-run digest guard with the proposed same-commit SHA update.
- `REPRODUCED` — the seeded removal of r11's recheck field is flagged as `citation_dead`, strict exit 1.
- `UNVERIFIABLE` — actual integration and its post-commit result; this seat was restricted to its own artifact directory and scratch.
