# RV-1 — C3 citation-drift recheck coverage patch draft

Claim: add durable citation-drift coverage for the `recheck:` fields of the r7/r10/r11 `ev_` Evidence-ID entries. This is patch text only; the gate and its files were not edited.

## Re-derived findings

- **VERIFIED — revision and current probe.** `git rev-parse HEAD` → `0436f4940283072db08e73c0117195847c50d31d`. The current strict probe, run on that revision, reports `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` (full output below).
- **VERIFIED — coverage hole at HEAD.** Re-read each entry from `git show HEAD:<path>`. Each has exactly one `recheck:` field: r7 at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`; r10 at `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`; r11 at `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`. A direct count against the HEAD pointer table found zero `entries` and zero `quoted` rows targeting each of those three files. The table has 57 `entries`, 5 `quoted` rows, and 8 exemptions. Thus the clean probe result is not coverage of these recheck fields: no row asks the probe to inspect them.
- **REPRODUCED — proposed coverage.** In `/var/tmp/kaidoku-rv1-c3-full-5pfwhzkq`, the full 60-entry proposed table ran against immutable HEAD and returned clean, exit 0. Replacing only the proposed r11 target with the probe's digest-pinned snapshot input, first with intact bytes and then with its sole `recheck:` line deleted, produced clean then `citation_dead` for `arc3r11-artifact-recheck-field`, exit 1. The snapshot digest was re-pinned after fault injection so the result tests the recheck anchor, not snapshot tampering. The existing probe's anchor semantics check that a regex occurs somewhere in the target (`.ufo/gates/citation-drift/citation-drift-probe.py:180-188`); its table digest guard remains active (`:294-320`).
- **CORRECTED — frozen custody alternative (b) is historical, not a live gap.** `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp` returned `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. At HEAD, coverage uses distinct resolved paths (`custody-pair.py:637-651`); duplicate-stanza rejection and distinct-five control are explicit at `:1157-1193`. No custody patch is proposed on that already-closed debt.
- **UNVERIFIABLE — landed improvement.** No instrument was changed, by seat scope. The 60-entry result is a scratch simulation of the proposed table; only integration can establish the post-landing gate identity and durable result.

The custody selftest used `/var/tmp` for its fixture root and made no custody-path writes. The citation-drift scratch runs read repository Git objects and scratch snapshots only; no Git mutation or `/tmp` scratch was used.

## Patch text (not applied)

Append these three entries to `.ufo/gates/citation-drift/pointer-table.json`'s `entries` array immediately before its closing `]`:

```diff
@@ -534,2 +534,23 @@
       "note": "the disposition's declared scope range must still begin at the round-4 records section (the span is a scope declaration, so the needle grades its start, not a claim inside it). Reddens on: the declared range no longer starting at the round-4 section header."
+    },
+    {
+      "id": "arc3r7-evm-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
+      "must_match": "^recheck: .*inspect-evm-interface .*selector\\.hex.*--format json",
+      "note": "Grade the r7 entry's recheck invocation; it must retain the pinned inspect-evm-interface selector fixture command."
+    },
+    {
+      "id": "arc3r10-rust-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
+      "must_match": "^recheck: .*rederive-commands\\.txt.*recompute-ids\\.mjs",
+      "note": "Grade the r10 entry's recheck recipe; it must retain its command receipt and independent ID recomputation."
+    },
+    {
+      "id": "arc3r11-artifact-recheck-field",
+      "kind": "anchor",
+      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
+      "must_match": "^recheck: .*calls\\.txt.*recompute-ids\\.py",
+      "note": "Grade the r11 entry's recheck recipe; it must retain its exact calls and independent ID recomputation."
     }
```

Re-pin `.ufo/gates/citation-drift/expected.json`'s `pointer_table.sha256` in the same change:

```diff
-"sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b"
+"sha256": "e63e8580e3f8f997c3f60cee94156ee9d31e9850b098d63d70bca858c9e1e27f"
```

The before digest was re-derived from the HEAD table and agrees with HEAD's expected pin. The after digest was computed over the exact HEAD table bytes plus the three appended JSON objects above. Proposed count: 57 → 60 entries. These anchors deliberately grade the continued presence of the corresponding command-bearing `recheck:` line; they do not execute the commands or prove every referenced evidence file exists. A future, separate liveness check would be needed for that stronger claim.

## Commands and measurements

HEAD pointer-table inventory (the `table_entries=[]`/`quoted_entries=[]` result was independently obtained for each of the three paths):

```text
corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md: recheck_fields=1; table_entries=[]; quoted_entries=[]
corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md: recheck_fields=1; table_entries=[]; quoted_entries=[]
corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: recheck_fields=1; table_entries=[]; quoted_entries=[]
table_entries_total=57; quoted_total=5; exempt_total=8
```

Current instrument at HEAD:

```sh
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict
```

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
COMMAND_EXIT=0
```

Full proposed table against HEAD (scratch paths are exact):

```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --table /var/tmp/kaidoku-rv1-c3-full-5pfwhzkq/pointer-table.json --expected /var/tmp/kaidoku-rv1-c3-full-5pfwhzkq/expected.json --strict
```

```text
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
PROPOSED_AFTER_COMMAND_EXIT=0
```

Seeded fault command (r11 snapshot; table and snapshot are scratch inputs):

```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --table /var/tmp/kaidoku-rv1-c3-full-5pfwhzkq/pointer-table.json --expected /var/tmp/kaidoku-rv1-c3-full-5pfwhzkq/expected.json --strict --snapshot-dir /var/tmp/kaidoku-rv1-c3-full-5pfwhzkq/snapshots
```

The intact snapshot control was clean (`findings=0 exit=0`). After deleting only the `recheck:` line from snapshot `ev-r11` and updating its expected snapshot digest:

```text
CITATION_DRIFT: citation_dead entry=arc3r11-artifact-recheck-field @ev-r11: no line matches '^recheck: .*calls\\.txt.*recompute-ids\\.py'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
SEEDED_FAULT_COMMAND_EXIT=1
```

Command A (`SCORECARD.md:88-124`) was not rerun: this c3 draft changes neither corpus files nor the coverage map. No corpus, gate, SCORECARD, SKILL, PROVINCE, or LOG file was edited.
