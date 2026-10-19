# PL-3 — C3 citation-drift recheck coverage

**Delivery:** patch text only, as required for C3. I did not edit the citation-drift instrument, its pointer table, `expected.json`, custody tool, or any tracked source. The proposed improvement is to grade the three new `ev_` corpus entries' `recheck:` anchors in the existing citation-drift pointer table.

## Re-derived state at HEAD

`git rev-parse HEAD`:

```text
0436f4940283072db08e73c0117195847c50d31d
```

Fresh source/table recount (`python3` JSON/line scan; output):

```text
entries=57 quoted=5 exempt=8
corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md: recheck_lines=1 entry_refs=0 quoted_refs=0
  5: recheck: `mkdir -p /var/tmp/kaidoku-ex3-r7-recheck && TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-evm-interface "$PWD/.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/fixtures/base/selector.hex" hex --format json` → on this host's cached `rea-agents@6.7.0`, expect `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`; `TMPDIR` must be disk-backed here.
corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md: recheck_lines=1 entry_refs=0 quoted_refs=0
  7: recheck: from the lane root, use the cached REA 6.7.0 command shown in `evidence/rederive-commands.txt`; then run `node .ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids.mjs`. The latter recomputes each recorded envelope's semantic projection ID, mutates only excluded display fields, and substitutes only the path-bearing fields to test the copied-path result. The `rustc` inspection is read-only; it does not execute the target.
corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: recheck_lines=1 entry_refs=0 quoted_refs=0
  7: recheck: use the pinned `rea-agents@6.7.0` cache path recorded in `identity.txt`, set `TMPDIR` to a directory under `/var/tmp`, and run the four exact calls in `calls.txt` after making byte-identical copies of `/usr/bin/jq` at the two recorded alternate paths. Then run `python3 .ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids.py`. Do not use `/tmp` for scratch.
```

The three exact target lines are independently readable at r7 entry `:5`, r10 entry `:7`, and r11 entry `:7`. The 57-entry table contains no `file` reference to any of these three entries (also confirmed by a direct search of `pointer-table.json`). The instrument's current behavior does not grade those rechecks.

Current baseline measurements:

```text
$ TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

```text
$ TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

Source basis: pointer-table entries currently end before the quoted section at `.ufo/gates/citation-drift/pointer-table.json:525-537`; the current frozen table digest is `.ufo/gates/citation-drift/expected.json:11-13`. `anchor` checks search file content without needing a line pin (`citation-drift-probe.py:180-189`); strict failures return 1 (`:77-93`).

## Proposed patch text — not applied

Insert these three objects at the end of `entries`, immediately before the existing `"quoted"` array in `.ufo/gates/citation-drift/pointer-table.json`:

```json
    {
      "id": "arc3-r7-recheck-anchor",
      "kind": "anchor",
      "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
      "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052",
      "note": "Grades the r7 EVM entry recheck field: preserve its disk-backed TMPDIR and independently expected Evidence ID; substring anchor is relocatable with no pinned line."
    },
    {
      "id": "arc3-r10-recheck-anchor",
      "kind": "anchor",
      "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
      "must_match": "^recheck: .*evidence/rederive-commands\\.txt.*evidence/recompute-ids\\.mjs",
      "note": "Grades the r10 Rust entry recheck field: retain the recorded CLI command source and independent ID-recomputation script; does not execute either."
    },
    {
      "id": "arc3-r11-recheck-anchor",
      "kind": "anchor",
      "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
      "must_match": "^recheck: .*identity\\.txt.*calls\\.txt.*recompute-ids\\.py",
      "note": "Grades the r11 artifact entry recheck field: retain the pinned identity, exact calls, and independent ID-recomputation script; does not execute them."
    }
```

In the same patch, change only `expected.json`'s `pointer_table.sha256` (`:12`) from the current `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` to the proposed table-byte digest:

```diff
-    "sha256": "1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b",
+    "sha256": "075db60f9a61975f7d013ff082d28d215d277d4eb0db3110fde8634b9ab6e383",
```

The proposed bytes add three rows (table count 57 → 60); quoted/exempt arrays are unchanged. Digest `075db60f…` was recomputed over the existing table bytes with exactly the three JSON objects above inserted before `quoted`. Recompute it if integration changes any whitespace or text; the table pin and table must land together.

## Candidate and seeded-fault measurements

The exact candidate table with real corpus paths and the proposed digest was run against immutable revision `0436f4940283072db08e73c0117195847c50d31d` using the live script (table/expected supplied from `/var/tmp`):

```text
CASE=patched-clean-head EXIT=0
CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: /var/tmp/kaidoku-pl3-wzx76tir/candidate-live-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

For seeded faults, scratch copies of the three corpus entries and candidate table were placed under `/var/tmp/kaidoku-pl3-gwi5akbc/`; no Git object or repository source was changed. The scratch table used the same three proposed anchors, with only their `file` targets redirected to byte-hash-pinned `@r7`, `@r10`, and `@r11` snapshots. The current table was the baseline control. Each `before-*` run returned `clean findings=0 exit=0`; each patched `after-clean-*` run returned `clean findings=0 exit=0`. One fault was then injected into only the corresponding snapshot's `recheck:` line; the three exact after-fault findings were:

```text
r7:  CITATION_DRIFT: citation_dead entry=arc3-r7-recheck-anchor @r7: no line matches '^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*ev_ffd8f'
r10: CITATION_DRIFT: citation_dead entry=arc3-r10-recheck-anchor @r10: no line matches '^recheck: .*evidence/rederive-commands\\.txt.*evidence/recomp'
r11: CITATION_DRIFT: citation_dead entry=arc3-r11-recheck-anchor @r11: no line matches '^recheck: .*identity\\.txt.*calls\\.txt.*recompute-ids\\.py'
```

All three after-fault runs ended `CITATION_DRIFT_VERDICT: failed findings=1 exit=1`; the same mutated snapshots with the unextended baseline table stayed `clean findings=0 exit=0`. The harness concluded `ASSERTIONS=PASS`. The scratch CLI shape was the live script with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 0436f4940283072db08e73c0117195847c50d31d --table <scratch>/<case>/pointer-table.json --expected <scratch>/<case>/expected.json --snapshot-dir <scratch>/<fault-or-clean-r7-r10-r11> --strict`.

## Per-item verdicts and limit

- **VERIFIED — measured gap:** each of three Evidence-ID entries has one `recheck:` line and zero pointer-table entries at HEAD (paths/lines and recount above).
- **REPRODUCED — candidate clean behavior:** the proposed anchors leave the actual HEAD tree clean, findings 0, exit 0.
- **REPRODUCED — seeded-fault sensitivity:** each of three mutations is silent with the baseline table and becomes its matching `citation_dead`, exit 1, with the proposed anchor.
- **UNVERIFIABLE / intentionally not claimed:** these anchors grade the presence of selected recheck text, not successful execution of the commands or liveness of every file named by them. The patch improves citation-drift table coverage only; it does not alter tool semantics or establish REA runtime behavior.
