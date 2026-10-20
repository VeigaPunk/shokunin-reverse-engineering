# Round-18 measurement/control reuse

## Axes
**Calibration, freshness, depth.** Reusing the old revision-pinned instruments can protect the prior calibration/depth record and make the before/after boundary auditable; it does not itself measure round-19 claims or add a freshness score.

## Findings (observation)

- **`measure.py`: call with revision arguments for round-18 continuity; do not treat it as round-19’s measure.** Its CLI takes a positional revision and optional `--root` (`.ufo/waves/round-18/measure.py:882-910`). It reads committed tree/blob contents (`:16-23`), but its instrument paths and C3 pattern are explicitly fixed to `.ufo/waves/round-18` (`:54-61`). It reports R18 C1/C2/C3, not W19 claims. Exit 0 means a report was emitted, not that all claims evaluated or passed (`:25-33`, `:466-485`).
- **`controls.py`: call with BEFORE and AFTER for the existing historical no-harm surface.** Its two positional revisions are resolved and read as Git objects, without reading the worktree or executing the material under test (`.ufo/waves/round-18/controls.py:4-13,448-469`). It compares LOG/SCORECARD prefixes and prior QUALITY admission rows (`:50,357-385,460-480`). It is a bounded report, not an enforcing gate (`:8-13,497`). For W19, require `quality_admission_rows.prior_rows_byte_identical == true` as well as `rows_1_20_identical == true`: at the W19 baseline there are already 21 prior rows, while the latter named facet covers only rows 1–20 (`:360-380`).
- **`verify.py`: do not call the R18 copy with a parameter. Copy/adapt it for W19’s pass.** It accepts a baseline revision, but its lane, R17/R18 roots, output directory and verification file are constants (`.ufo/waves/round-18/verify.py:17,27-39`); its command list runs R18 tools/artifacts (`:104-114,155-171,173-237`), and it creates/writes R18 output locations (`:269-273,303-310`). Calling it would overwrite/extend retained R18 evidence rather than verify W19. Adapt its source pin and command list and route every output into W19.

The R18 shared contract likewise scopes `measure` to W18 artifacts, `controls` to its listed no-harm surfaces, and `verify.py` to the single post-integration pass (`.ufo/waves/round-18/contract.md:138-146`). The scorecard’s R18 table records calibration `10.0→10.0`, depth `10.0→10.0`, and freshness as having no owned numeric proxy (`SCORECARD.md:2449-2458`). `controls.py`’s `craft` fields are command-A file/range counts, not those numeric axis scores (`controls.py:11-13,471-479`). The full prior SCORECARD byte prefix protects its existing score rows; W19’s own measure must compare its declared proxy at baseline and source rather than relabel R18 counts as scores.

## No-harm invocation and assertions

After W19 has a committed source revision `<R19_SOURCE>`, the reusable invocations are:

```text
python3 -I -B .ufo/waves/round-18/measure.py 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
python3 -I -B .ufo/waves/round-18/measure.py <R19_SOURCE>
python3 -I -B .ufo/waves/round-18/controls.py 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 <R19_SOURCE>
```

Check the two measure reports’ `status`/`could_not_evaluate` and relevant R18 counts; do not use their process exit alone as a pass signal. In the controls JSON require:

1. `old_prefix.LOG.md.prefix_preserved` and `old_prefix.SCORECARD.md.prefix_preserved` are true (append-only, not necessarily byte-identical).
2. `quality_admission_rows.prior_rows_byte_identical` and `rows_1_20_identical` are true, with no prior-row violations. Additions are separately listed.
3. `craft.before` and `craft.after` retain the same `rule_blocks`, `citation_resolved_rules`, and `craft_sha256`; this is only the bounded command-A check, not an axis score.
4. Read `prior_verifiers_unchanged`, `prior_wave_evidence_blobs`, and `sources_registry` under their stated R18 exception rules; the report does not make these semantic verdicts.

**Observation, executed commands and exits:**

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main && git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/remotes/origin/main` — exit **0**; both returned `85589ac757f9ca3cb25efcd702d0963e25c9c4df`.
- `python3 -I -B .ufo/waves/round-18/measure.py --selftest` — exit **0**, `SELFTEST: CLEAN cases=68`.
- `python3 -I -B .ufo/waves/round-18/controls.py --selftest` — exit **0**, `SELFTEST: CLEAN cases=23`.
- `python3 -I -B .ufo/waves/round-18/measure.py 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` — exit **0**; evaluated, `could_not_evaluate=false`, C1 `open_count=0`, C2 `live_count=0`, C3 15/15 compare artifacts carry the selected extra field(s), and all 15 recorded `all_match` values are true.
- `set -o pipefail; python3 -I -B .ufo/waves/round-18/measure.py 85589ac757f9ca3cb25efcd702d0963e25c9c4df | jq -c '{revision, c1_open_count, c2_live_count, c3_compare_jsons, c3_compare_jsons_with_extra, c3_all_match_by_label, could_not_evaluate}'` — exit **0**; same C1/C2/C3 counts and all 15 `all_match=true` at the observed tip.
- `set -o pipefail; python3 -I -B .ufo/waves/round-18/controls.py 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 85589ac757f9ca3cb25efcd702d0963e25c9c4df | jq -c '{revisions, old_prefix, quality_admission_rows, craft}'` — exit **0**; LOG and SCORECARD prefixes preserved (both byte-identical in this comparison), all 21 prior QUALITY rows identical including rows 1–20, no row violations, and craft 17/17 with the same SHA-256 on both sides.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- .ufo/waves/round-18/measure.py .ufo/waves/round-18/controls.py .ufo/waves/round-18/verify.py; rc=$?; printf 'diff_exit=%s\n' "$rc"; exit 0` — wrapper exit **0**, inner diff exit **0** (`diff_exit=0`): the three R18 scripts at the observed tip are unchanged from the W19 baseline.

## Proposed bounded move (inference)

Use R18 `measure.py` at the W19 baseline and final source, and R18 `controls.py` once from baseline to final source as **prior-round continuity/no-harm reports**. Have the adapted W19 verifier assert the JSON conditions above and run W19’s own metric commands at both revisions for the actual calibration/freshness/depth claim outcomes. This reuses checked behavior without duplicating it, while keeping the old scorecard values protected by the prefix check. Do not run R18 `verify.py` or describe R18 measurement counts as W19 scores.

## Risks / contradiction

The names “measure” and “controls” can suggest verdicts, but both are expressly observation/report tools: `measure.py` returns exit 0 for a complete report even when a claim is `could-not-evaluate`, and `controls.py` emits `conformance_gate: false`. A green process exit alone is therefore not a no-harm acceptance. R18 controls also cover only their coded facets and exception set; they do not semantically verify a newly written score or new W19 claim. No tool was installed or updated.