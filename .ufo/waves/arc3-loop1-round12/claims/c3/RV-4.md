# RV-4 — citation-drift coverage for `ev_` rechecks

## Scope and claim

C3 / operability, candidate (a): extend the citation-drift probe's pinned pointer table so the `recheck:` lines in the three recent `ev_` knowledge entries are graded. I chose this measured gap rather than a custody-pair change. Per the frozen seat contract, this is patch text plus a seeded scratch measurement only: **no gate, pointer table, expected file, corpus entry, or other tracked source was edited.**

The patch payload is `.ufo/waves/arc3-loop1-round12/claims/c3/RV-4/proposed-entries.json`; it is the exact JSON array to append to `pointer-table.json`'s `entries`. `expected.json`'s `pointer_table.sha256` must be recalculated from the final table bytes in the same integration commit, as required by `.ufo/gates/citation-drift/citation-drift-probe.py:34-40`.

## First-hand re-derivation

Actual repository revision: `git rev-parse HEAD` → `0436f4940283072db08e73c0117195847c50d31d`.

I read the three current corpus lines and scanned the current pointer table by target path and exact `recheck:` line number:

```text
entries=57 quoted=5 exempt=8
r7: recheck_lines=[5] matching_entries=0 any_file_entries=0
r10: recheck_lines=[7] matching_entries=0 any_file_entries=0
r11: recheck_lines=[7] matching_entries=0 any_file_entries=0
```

Source locations are `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`. The count is scoped to these three exact recheck lines, not all citations in those files.

The existing probe did not flag the gap: command
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict` returned:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

## Patch text and seeded result

The proposed three exact entries are in `proposed-entries.json`. They pin the current recheck lines and selected consequential content: r7's disk-backed scratch, operation and expected ID; r10's recorded command recipe, ID recomputation and read-only constraint; r11's disk-backed scratch, recorded calls, ID recomputation and never-`/tmp` constraint. These are string-drift checks, not execution or semantic validation of the recheck commands or Evidence IDs.

I ran `python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py`. It imports the **unmodified** gate module, adds the three proposed rows to a scratch table, re-pins that scratch table's digest in a scratch `expected.json`, and overlays only the selected corpus line for each seeded case. Other targets resolve through read-only `git show HEAD`; the helper uses `TemporaryDirectory(dir="/var/tmp")`, performs no Git writes, and leaves the live instrument/table/expected unchanged. Exact output:

```text
CONTROL: no findings; strict_exit=0
SEEDED arc3r7-evm-recheck: citation_dead entry=arc3r7-evm-recheck; strict_exit=1
SEEDED arc3r10-rust-recheck: citation_dead entry=arc3r10-rust-recheck; strict_exit=1
SEEDED arc3r11-artifact-recheck: citation_dead entry=arc3r11-artifact-recheck; strict_exit=1
SCRATCH: /var/tmp only; no Git writes; live instrument/table/expected unchanged
```

The seeded edits were limited to the targeted `recheck:` line: r7 changed its `TMPDIR` from `/var/tmp` to `/tmp`; r10 and r11 changed the named `recompute-ids` script basename. This demonstrates that the candidate rows preserve a clean baseline and that each single-line mutation is reported as `citation_dead` by the real gate logic. Reproducible helper: `.ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py`.

## Side-harm checks

- `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` → `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` (the output listed each case as `CLEAN`).
- Re-derived Command A from `SCORECARD.md:88-124` at the revision above:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
```

These checks establish current source-map/craft counts only; they do not measure the proposed rows in the live table because the instrument was intentionally not edited.

## Per-item verdicts

- **VERIFIED — live gap:** the current table has 57 entries, and zero entries grade each of the three named recheck lines; the live probe reports clean with zero findings. The exact line paths and counts are above.
- **REPRODUCED — scratch patch:** with all three proposed rows, the unchanged HEAD corpus is clean; each seeded one-line mutation independently produces `citation_dead` / strict exit 1.
- **VERIFIED — self-test and side-harm:** citation-drift self-test 13/13; Command A 90/90 mapped with no missing or dangling tokens and 16/16 citation-resolved rule blocks (outputs above).
- **CORRECTED — patch draft:** the first r7 matcher omitted the closing backtick after the expected ID; the scratch control exposed that false positive. The candidate recorded in `proposed-entries.json` includes the delimiter and passes the clean control. The seed helper was also narrowed to mutate only the specified recheck line after its first draft counted duplicate script-name occurrences elsewhere in the same file.
- **UNVERIFIABLE — integrated after-state:** no live instrument change was allowed or made, so a post-integration probe run and the final `expected.json` digest remain for the integrator. The scratch result is not a claim that the live table has already improved.

## Operational deviation

I initially ran the citation-drift self-test once as `python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` without setting `TMPDIR`. Its fixture builder uses Python temporary directories (`.ufo/gates/citation-drift/citation-drift-probe.py:347-368,415-466`); a subsequent same-environment check printed `TMPDIR=None tempfile.gettempdir()=/tmp`, so the first invocation used `/tmp`, contrary to the wave scratch rule. It passed 13/13 and the self-test cleans its fixture directories; I then re-ran the accepted measurement with `TMPDIR=/var/tmp` (result above). The initial invocation is disclosed, not counted as the compliant scratch measurement.
