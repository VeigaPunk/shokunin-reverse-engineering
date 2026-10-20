# DraftLessonEvidence — round-17 wave-2 falsification (author-side advisory)

Lane revision attacked: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Installs/updates: none.
Host safety: no pacman, no credential/auth file opened, no REA analyze/search/decompile, no carrier executed.

## 0. Target status (finding F0, blocking for the draft)

- The draft `.ufo/waves/round-17/w2/draft-lesson-evidence.md` does not exist; `w2/` is empty.
- `git show da64646:corpus/lessons/round-17.md | grep -n '^## '` returns only `Claims`, `Gate`, `Mistakes`, `Integration boundaries` (lines 6, 20, 69, 91). No `## Executed L1 evidence and verdicts` section exists in any file at da64646 (`grep -rl "Executed L1 evidence"` finds none in the new round).
- `git ls-tree -r --name-only da64646 -- .ufo/waves/round-17 | grep -c verification.json` → `0`. No round-17 `verification.json` exists, so the slots in the requested section have no retained source yet.
- I attacked the artifacts that do exist, below. Every slot is judged on what it would retain.

## 1. Slot-by-slot verdicts

| Slot | Command (as run) | Result | Verdict |
|---|---|---|---|
| selftests (11 tools) | `python3 -I -B tools/<t>.py --selftest` | All `SELFTEST: CLEAN` (buildinfo 11, census 10, carrier-run 2, compare 10, invocation-audit 6, log-extract 8, pins 7, predict 17, receipt-validate 5, retain 3, temporal-sweep 6). pins prints `red case observed: compare exit 1 names …` | clean; but see F1: receipt-validate selftest cannot catch its own failure |
| pins red demo | pins selftest above | `red case observed: compare exit 1` | clean |
| temporal-sweep | `temporal-sweep.py --root . --rev da64646…` | `{'corrected': 4, 'unqualified': 0, 'sites': 4}` | clean for the phrase set (F5 bounds it) |
| invocation-audit | `invocation-audit.py --root . --rev da64646…` | rows 17, `unlabelled_variant` **11**, `exercised_match` 6 | **FAIL vs C1(b)** (F2). Baseline `--rev b563c79`: unlabelled 2 of 7 rows |
| citation-drift strict | `citation-drift-probe.py … --strict` | `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` (text, not JSON) | clean, but **not retained** (F2) |
| custody-pair capture | not run | — | bounded no-finding: the five paths include `~/.omp/agent/mcp.json` and `~/.config/devin/mcp_config.json`; contract forbids opening credential/auth files |
| controls | `controls.py b563c79 da64646…` | exit 0, `conformance_gate: false`, craft 17/17 both sides | clean |
| measure | `measure.py da64646…` | `run_receipts 8`, `knowledge_files 95`, `C2_scorecard_capability_row 0`, `C1_quality_row19 1`, `missing []`, `dangling []` | clean; capability row correctly absent (gate unmet, see F1) |
| receipt-validate ×8 | `receipt-validate.py runs/<label>/receipt.json` | **8/8 exit 1**, `unrecognized_shape` at `$` | **FAIL** (F1). Cannot satisfy "exit 0" slots |
| compare red demo | `compare.py --prediction predictions/pro-op.prediction.json --observation runs/calib-shfmt/observation.json` | exit 1, mismatch `untested_version` predicted `1.26.8` observed `['1.27.0']`; green control (pro-op self) exit 0 | clean |

## 2. Defects (ordered by severity)

### F1 — receipt-validate rejects every real carrier receipt (blocking; producer/validator shape mismatch)

Command: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/pro-op/receipt.json`
Output (all 8 runs identical in shape): `"findings": [{"code": "unrecognized_shape", "detail": "receipt matches neither retain nor carrier shape", "where": "$"}], "status": "invalid"`.

Cause:
- `tools/receipt-validate.py:98-101` `classify()` returns `carrier` only if `receipt["steps"]` is a **list**.
- `tools/carrier-run.py:275` initialises `"steps": {}`; `:309` `steps = {}`; `:317`, `:349` write `steps` keyed by step name (`inspect-go-binary`, `analyze`, `search:<NAME>`). Real receipts: `runs/pro-op/receipt.json` `steps` keys = `['analyze', 'inspect-go-binary']`.
- `tools/receipt-validate.py:470` selftest fixture uses `"steps": [{...}]` (list), so the selftest passes (`CLEAN cases=5`) while every real carrier receipt is rejected.
- Confirmed root cause: a copy of `runs/pro-op/receipt.json` with only `steps` converted to a list validates: exit 0, `status: valid`, `checks_performed: 336` (experiment in /tmp/r17_exp; repo untouched).

Consequences:
- The eight `receipt-validate` slots cannot be exit 0 as the tool stands.
- Gate for the capability row is unmet. `w1/ConnCapabilityHistory.md:70` requires each run receipt to validate exit 0 with `pins_compare.equal` true; C2 requires the row only "if the capture runs and its receipt validates".
- The contract (`contract.md:106-108`) does not pin the `steps` shape, so the mismatch is a producer/validator disagreement, not a spec-stated requirement. Fix direction for L1: pick one shape and make the selftest fixture use the producer's real output.

### F2 — registry and retention claims point at a round-17 receipt that does not exist (C1(b) unmet)

- `SKILL.md:448` (citation-drift) and `SKILL.md:449` (custody-pair) state "exercised argv: `.ufo/waves/round-16/verification.json` and `.ufo/waves/round-17/verification.json`" and "exercised argv retained in `.ufo/waves/round-17/verification.json`". At da64646 the round-17 file is absent (`verif-count=0`).
- `invocation-audit.py --rev da64646…` → `unlabelled_variant: 11` (`rows 17`). Baseline at `b563c79`: `unlabelled_variant: 2`, `rows 7`. C1 requires unlabelled rows M → 0. The round-17 rows (`go-carrier-run`, `go-log-extract`, `go-route-predict`, `go-route-compare`, `receipt-validate`, `pins`, `temporal-sweep`, `invocation-audit`, `go-buildinfo-probe`, `round17-structural-controls`, `custody-pair`) carry no retained argv, so the count rises instead of falling.
- `citation-drift` is `exercised_match` only against `.ufo/waves/round-16/verification.json` (the pre-existing r16 receipt). No round-17 receipt retains the isolated strict argv, so the "re-exercised with receipt retained" requirement (C1(b)) is unmet. Re-running the row argv myself gave `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`, but it is not retained.
- Counter-check (harmless): `invocation-audit` excludes 71 path-form `*receipt*.json` files. I tested all 71 at da64646: none carries an `argv` array, so the exclusion does not hide exercised argv.

### F3 — prediction comparison is narrower than the prediction it claims to check

- `tools/compare.py` evaluates five fields (`untested_version`, `snapshot_label`, `missing_bootstrap`, `snapshot_route`, `fallback_to`). `grep -c extra_expectations tools/compare.py` → `0`.
- `predictions/pro-esbuild-0.27.7.prediction.json` carries `extra_expectations` (`language_compiler`, `bootstrap_attempts_at_least: 1`, `analyzer_errors_contain: "unable to get GoRttiMapper"`). These are never checked. The run would satisfy them (its `observation.json` has two "unable to get GoRttiMapper" analyzer errors), but the compare output does not show it.
- That prediction is hand-written (`author` field; `input: ""`; `selection: null`), not produced by `predict.py` (which exits 2 on an empty version). `predictions/carriers.tsv` labels it "hand prediction". C2 claims predictions "derived from installed source via r16 selection.py". This one is not, and the lesson must say so.
- Discriminating gap: `runs/pro-esbuild-0.27.7/observation.json` has `classification: "other"` and `missing_bootstrap: false`, yet the run is a GoRttiMapper null failure. `tools/log-extract.py` `MISSING_BOOTSTRAP_TEXT` (line 75) matches only "Missing Go bootstrap type info", so the analyzer-failure path of 0.27.7 is labelled "other". The field C2 targets ("bootstrap failure") reads false for it.

### F4 — calibration: a non-discriminating field is counted as a match

- Every `runs/*/compare.json` lists `"snapshot_label": "contains-or-both-empty (non-discriminating: request echo)"` in its `rules` block, and that field's `match: true` is counted in `all_match` for all 8 runs. The tool says it does not discriminate, yet it contributes to the tally.
- Effect: the "all fields match" claims overstate. Count only `missing_bootstrap`, `untested_version`, `snapshot_route`, `fallback_to` as evidence, and report the echo separately.

### F5 — uncontracted condition in one prospective run

- `run-carriers.sh` (line `[ "$label" = "pro-op" ] && envs=(env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000)`) and `runs/pro-op/receipt.json` `rea_ghidra_env: {"REA_GHIDRA_STARTUP_TIMEOUT_MS": "900000"}`. The contract never authorises an environment override, and the other seven runs use defaults. The receipt records it, so it is not hidden, but pro-op is not an identical-condition comparison. The lesson's Limits must say so.

### F6 — temporal sweep is pattern-bounded (bounded no-finding)

- Sweep: 4 sites, all corrected, 0 unqualified.
- Independent grep at da64646 over `LOG.md SCORECARD.md corpus README.md SKILL.md PROVINCE.md` for `unchanged (during|across|throughout)|remain(ed|s) unchanged|stayed unchanged|stable (during|throughout)` returns three of the four sites (`LOG.md:2012`, `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`) and no other temporal-stability claim in that scope. The fourth, `.ufo/waves/round-16/verification.json:419` (`pins_unchanged_during_run`), lies outside that grep scope (`.ufo/`) and was confirmed by a separate `git grep` over `da64646 -- .ufo/waves/round-16`.
- Bounded: this holds for that phrase set only. Phrasings such as "pins were stable" are not searched.

## 3. Verified clean (bounded no-findings)

- Carrier receipts, all 8: `carrier.sha256_pre == sha256_post`; `pins_compare.equal == true`, `changed == []`, `errors == []`; `analyze.exit == 0`; `evidence_id` present; `bound_sessions == 1`, `unbound == 0`; `retained_logs` binding `logfile_ok` and `target_ok` true; `session_parent_leftovers == ["node-compile-cache"]` (benign).
- Predictions: `sha256sum -c predictions/SHA256SUMS` from the round root → 17/17 OK; `git diff 271167473d… da64646… -- .ufo/waves/round-17/predictions` empty (frozen).
- Pilot: `sha256sum -c pilot/SHA256SUMS` from pilot dir → 6/6 OK.
- Go bootstrap rule: `missing_bootstrap` in `log-extract` is grounded in the `Missing Go bootstrap type info` WARN line. For `calib-shfmt` and `pro-op` the line is present in `ghidra.log` (`GoRttiMapper`, 10:47:09 and 10:55:59). The `esbuild 0.27.7` buildinfo premise holds: `go version -m` → "not a Go executable"; `buildinfo-probe.py` → `found:false`.
- Log capture: every `ghidra.log` ends at the post-script "ANALYZING changes" step. This matches the documented polling-copy limit (`log_capture_limit`), so I count it as a known limit, not a defect.

## 4. Requested for L1 (no edits made by me)

1. Fix F1: align `classify()`/selftest with the producer's dict-shaped `steps` (or change producer); re-run receipt-validate on all 8 receipts; retain the exit-0 outputs.
2. Resolve F2: either retain round-17 receipts for `citation-drift --strict`, `custody-pair` (if run by an authorised path), and the 11 round-17 rows, or label each row `unexercised` so the audit count reflects the truth; correct SKILL.md:448-449 so they no longer name a non-existent round-17 `verification.json`.
3. Address F3–F5 in the lesson's Limits and in compare output: report the hand prediction as hand, evaluate or drop `extra_expectations`, flag the 0.27.7 analyzer-failure class, separate the snapshot-echo field, and state the pro-op env override.
4. The draft section named in the target does not exist. Write it only after F1–F2 are resolved, so its slots can be filled with exit-0 receipts.

Artifacts I generated (outside the lane, /tmp only): `/tmp/r17_sweep.json`, `/tmp/r17_inv.json`, `/tmp/r17_measure.json`, `/tmp/r17_controls.json`, `/tmp/r17_cd.json`, `/tmp/r17_red.json`, `/tmp/r17_exp/receipt-steps-as-list.json`.
