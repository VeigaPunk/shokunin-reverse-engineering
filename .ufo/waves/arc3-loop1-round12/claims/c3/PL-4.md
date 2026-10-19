# PL-4 — citation-drift recheck coverage patch and seeded measurement

**Claim:** C3 operability, instrument improvement (frozen claim candidate a). This is a patch-text artifact only. I did not edit the probe, its table, `expected.json`, corpus entries, or any other lane file.

## First-hand baseline

I re-derived the revision with `git rev-parse HEAD`: `0436f4940283072db08e73c0117195847c50d31d`. The current pointer table has 57 `entries` plus 5 `quoted` records (62 total), SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`; that digest matches `.ufo/gates/citation-drift/expected.json`'s `pointer_table.sha256` (`expected.json:11-13`). I parsed both the `file` and `target` fields: there are **zero table references** to any of the three new ev-ID corpus files below.

The three ungraded recheck fields are at:

- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5` — cached `inspect-evm-interface` invocation, disk-backed `TMPDIR`, expected ID.
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7` — cached command source plus independent `recompute-ids.mjs`.
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7` — pinned cache identity, `TMPDIR`, `calls.txt`, and `recompute-ids.py`.

The live instrument command at this pin was:

```text
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 0436f4940283072db08e73c0117195847c50d31d --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict
```

Exact output:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

**VERIFIED — gap:** a clean verdict here only means the 57 current entries found no drift. Since the table has no reference to these three recheck lines, none is graded at this pin. The table is the declared citation inventory (`citation-drift-probe.py:4-8, 279-320`); its preflight pins its exact bytes (`:294-308`).

## Proposed patch text

Append these three objects to the `entries` array in `.ufo/gates/citation-drift/pointer-table.json`, after the current last entry (`census-cites-sc-round4-range`) and before the array's closing `]`:

```json
{
  "id": "pl4-r7-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
  "line": 5,
  "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-evm-interface.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052",
  "note": "Grade the append-only ev-ID corpus entry recheck instruction at its cited line."
},
{
  "id": "pl4-r10-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
  "line": 7,
  "must_match": "^recheck: .*evidence/rederive-commands[.]txt.*recompute-ids[.]mjs",
  "note": "Grade the append-only ev-ID corpus entry recheck instruction at its cited line."
},
{
  "id": "pl4-r11-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
  "line": 7,
  "must_match": "^recheck: .*identity[.]txt.*TMPDIR.*calls[.]txt.*recompute-ids[.]py.*Do not use `/tmp` for scratch[.]",
  "note": "Grade the append-only ev-ID corpus entry recheck instruction at its cited line."
}
```

In the same patch, set `expected.json`'s `pointer_table.sha256` to:

```json
"sha256": "7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2"
```

That digest was re-derived from the existing table plus exactly the three objects above, serialized in the table's existing `json.dumps(..., indent=2) + "\\n"` formatting. The existing self-test case array does not need a new case: the scratch measurement below exercises all three real table entries through the probe's entry checker. Table-hash refresh and table edit must land together.

## Seeded-fault measurement

I imported the current probe module and called its actual `run_check` / `report(..., strict=True)` using the proposed table and matching scratch `expected.json`. Scratch was created under `/var/tmp`; the three pinned corpus files were copied there. A read shim supplied only those three paths from scratch and delegated all other `git_show` lookups to immutable HEAD. No Git object or repository file was changed. The unmodified scratch copies formed the patched-table control; then I replaced one `recheck:` line at a time with `recheck: SEEDED-FAULT`, retaining earlier faults so each new entry's catch was visible as an increment.

Measured output (probe output truncates displayed regex text to 60 characters):

```text
BEFORE: entries=57 quoted=5 matching_recheck_rows=0
CURRENT_TABLE_SERIALIZES_WITH_JSON_DUMPS: True
CURRENT_TABLE_SHA256: 1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b
PATCH_TABLE: entries=60 quoted=5 sha256=7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
PATCH_CONTROL_STRICT_EXIT: 0
CITATION_DRIFT: citation_dead entry=pl4-r7-recheck corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5 ...
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
SEEDED_FAULT: pl4-r7-recheck strict_exit=1
CITATION_DRIFT: citation_dead entry=pl4-r7-recheck corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5 ...
CITATION_DRIFT: citation_dead entry=pl4-r10-recheck corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7 ...
CITATION_DRIFT_VERDICT: failed findings=2 exit=1
SEEDED_FAULT: pl4-r10-recheck strict_exit=1
CITATION_DRIFT: citation_dead entry=pl4-r7-recheck corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5 ...
CITATION_DRIFT: citation_dead entry=pl4-r10-recheck corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7 ...
CITATION_DRIFT: citation_dead entry=pl4-r11-recheck corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7 ...
CITATION_DRIFT_VERDICT: failed findings=3 exit=1
SEEDED_FAULT: pl4-r11-recheck strict_exit=1
```

**REPRODUCED — seeded behavior:** the patch control is clean; each independently named line fault adds its corresponding `citation_dead` finding. Findings rose 0 → 1 → 2 → 3; strict exits were 0 → 1 → 1 → 1. The measurement uses the probe's normal table hash preflight and full entry traversal, not a reimplementation of the regex checker.

The installed probe self-test was also re-run without `/tmp` scratch:

```text
TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

**VERIFIED — self-test:** 13/13 cases passed. `citation-drift-probe.py:323-334` defines strict exit 0/1/2 behavior; its self-test reads the independent case table from `expected.json` (`:405-471`).

## Per-item verdicts and limits

- **VERIFIED — baseline:** HEAD, table count/hash, and the clean strict live run are re-derived above.
- **VERIFIED — named gap:** zero existing entries reference any of the three files as either `file` or `target`; the three `recheck:` lines are at the stated path:line locations.
- **REPRODUCED — proposed patch:** the three added entries pass on clean scratch copies; each seeded line fault is reported as `citation_dead` and fails strict mode.
- **VERIFIED — existing regression suite:** citation-drift self-test 13/13.
- **UNVERIFIABLE — runtime rechecks:** I did not execute the three corpus `recheck:` commands or rerun REA analysis. These table entries grade the recorded instruction text at fixed append-only lines; they do not execute the commands or prove the cached packages, referenced evidence files, or target analyses remain runnable.

No patch was applied to the gate or custody tool. Landing this move requires the table additions and expected digest update in one integration commit, then a clean strict probe at that commit. No `LOG.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, corpus, or gate source was modified.