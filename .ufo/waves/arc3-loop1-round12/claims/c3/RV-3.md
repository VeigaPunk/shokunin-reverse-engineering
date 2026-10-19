# RV-3 — C3 citation-drift recheck coverage (patch draft)

## Claim and scope

C3 asks for a measurable instrument/custody gap, patch text, and a seeded-fault measurement on scratch (`.ufo/waves/arc3-loop1-round12/claims-frozen.md:50-63`). I selected the citation-drift pointer table: its exact/extracted/anchor entry checks are implemented at `.ufo/gates/citation-drift/citation-drift-probe.py:168-261`, but the three recent `ev_` corpus entries' own `recheck:` lines are not registered. This is a proposed table-only gate patch. I did not edit the live probe, pointer table, expected file, corpus, or custody tool.

**Verdict:** `VERIFIED` — the gap exists at committed HEAD. `REPRODUCED` — proposed rows pass on a clean scratch overlay and flag a seeded recheck fault. `UNVERIFIABLE` — post-integration behavior; this is patch text only, not a landed instrument change.

## First-hand re-derivation

Revision used: `0436f4940283072db08e73c0117195847c50d31d` (`git rev-parse HEAD`). Read-only `git show` inspection of `.ufo/gates/citation-drift/pointer-table.json:287-536` plus the three source entries found 57 `entries`, 5 `quoted` records, and these recheck lines, with no table reference to any of the three files:

- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5` — one `recheck:` line; no table reference.
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7` — one `recheck:` line; no table reference.
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7` — one `recheck:` line; no table reference.

The inventory command read the pointer table and all three texts from HEAD and checked both `file` and `target` table fields. Its exact output:

```json
{"candidate_recheck_fields": 3, "candidates": [{"path": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md", "recheck_lines": [5], "table_reference": false}, {"path": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md", "recheck_lines": [7], "table_reference": false}, {"path": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md", "recheck_lines": [7], "table_reference": false}], "graded_candidates": 0, "pointer_entries": 57, "quoted": 5, "revision": "0436f4940283072db08e73c0117195847c50d31d"}
```

Current gate behavior confirms why this is a gap rather than an existing finding:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

The current self-test also reproduces its committed expected behavior, but does not cover these corpus lines. An earlier exploratory invocation omitted `TMPDIR` and used Python's default temporary directory; its fixtures were cleaned up. The authoritative rerun below set `TMPDIR=/var/tmp`.

```text
$ TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

I reran the Command A recipe at `SCORECARD.md:88-124` against the same revision; the C3 patch changes neither corpus nor map:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "0436f4940283072db08e73c0117195847c50d31d", "rule_blocks": 16}
```

## Patch text — not applied

Add these three objects to the `entries` array in `.ufo/gates/citation-drift/pointer-table.json` (before its closing `]`, currently at line 536). They use the probe's existing `exact` matcher, so no gate-code change is required. Each check pins a distinctive, reproducible part of that entry's own `recheck:` line.

```json
{
  "id": "rv3-r7-evm-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
  "line": 5,
  "must_match": "^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-evm-interface.*--format json",
  "note": "Grade the R7 entry's recheck command, disk-backed scratch requirement and operation."
},
{
  "id": "rv3-r10-rust-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
  "line": 7,
  "must_match": "^recheck: .*rederive-commands\\.txt.*recompute-ids\\.mjs.*read-only",
  "note": "Grade the R10 entry's command record, independent Evidence-ID recomputation and read-only scope."
},
{
  "id": "rv3-r11-inspect-artifact-recheck",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
  "line": 7,
  "must_match": "^recheck: .*TMPDIR.*calls\\.txt.*recompute-ids\\.py.*Do not use.*scratch",
  "note": "Grade the R11 entry's disk-backed scratch instruction, exact calls, recomputation and /tmp exclusion."
}
```

Update `.ufo/gates/citation-drift/expected.json:11-14` in the same change so `pointer_table.sha256` is `1e8bda152a2426027e69dd2678b5da52fa20fdfab5c70cb19a9a06651fc44b5c` for the table bytes generated by the scratch harness (2-space JSON indentation, ASCII escaping, trailing newline). The probe rejects a changed pointer table as `pointer_table_tampered` unless this digest is refreshed; see `.ufo/gates/citation-drift/citation-drift-probe.py:294-308`.

## Seeded-fault measurement

The reproducible harness is `claims/c3/RV-3/evidence/seeded-fault.py`. Run from the lane root:

```text
python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-3/evidence/seeded-fault.py "$PWD"
```

It loads the gate and input files from the named HEAD using read-only Git commands, makes a scratch copy of the gate/table under `/var/tmp`, overlays byte-identical copies of the three corpus files, adds the draft rows and repins the table in scratch, then corrupts only the scratch R11 line (`recompute-ids.py` → `recompute-ids.txt`). It writes no Git objects or refs and never touches the live instrument or custody paths. Exact result:

```text
REVISION: 0436f4940283072db08e73c0117195847c50d31d
PATCH_TABLE: entries=60 quoted=5 total=65 sha256=1e8bda152a2426027e69dd2678b5da52fa20fdfab5c70cb19a9a06651fc44b5c
SCRATCH_BASELINE: verdict=clean findings=0 exit=0
SEEDED_FAULT: corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7 recompute-ids.py -> recompute-ids.txt
FAULT_FINDING: citation_dead entry=rv3-r11-inspect-artifact-recheck corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7 lacks '^recheck: .*TMPDIR.*calls\\.txt.*recompute-ids\\.py.*Do not us'
SCRATCH_FAULT: verdict=failed findings=1 ids=['citation_dead'] exit=1
```

This demonstrates table-driven detection of a changed recheck instruction; it does **not** execute the commands described by those fields or establish REA behavior. The patch remains unlanded and needs a post-integration frozen run and self-test re-run to verify its actual committed digest and result.

## Write boundary

Only this report and `claims/c3/RV-3/evidence/seeded-fault.py` were written, both under RV-3's artifact directory. `AGENTS.md:4` requests a LOG entry for changes, but this seat's explicit scope forbids touching `LOG.md`; I left it unchanged. No claim is made that C3 has been landed or admitted.
