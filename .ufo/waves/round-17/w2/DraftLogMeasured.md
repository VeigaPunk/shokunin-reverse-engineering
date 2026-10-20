# DraftLogMeasured — w2 falsify report (author-side advisory, not outside review)

Seat: KaidokuR17.DraftLogMeasured (leaf, no dispatch). Lane revision attacked:
`da64646adcb19c1ede7537b799b8c7d283fe43da` (git objects; working tree also had
`M run-carriers.sh`, untracked `verify.py`, `w2/`, wave-2 files — not used as evidence).
Deliverable: `.ufo/waves/round-17/w2/draft-log-measured.md`. Only this report and that
draft were written. No REA analyze/search/decompile, no Ghidra, no carrier executed.

Installs/updates by this seat: none. Commands used: `python3 -B -I` on round-17 tools,
`git show/grep/diff/rev-parse/log`, `sed`/`grep` reads, one `python3 -B -I -c` JSON read per
receipt. Scratch files only under `/tmp/r17w2/`.

## Findings (ranked; observation unless labelled INFERENCE)

### F1 HIGH — receipt-validate rejects all eight carrier receipts
- Command: `python3 -B -I .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/calib-shfmt/receipt.json` → exit 1;
  output `"findings": [{"code": "unrecognized_shape", "where": "$", "detail": "receipt matches neither retain nor carrier shape"}]`, `"status": "invalid"`.
  Same for all eight `runs/*/receipt.json` (batch: `invalid 8`).
- Cause (observed): `runs/calib-shfmt/receipt.json` `steps` is an object with keys `analyze`, `inspect-go-binary`.
  `tools/receipt-validate.py:95-104` `classify()` requires `steps` to be a list, so the carrier shape is never recognised.
  The producer `tools/carrier-run.py` writes the dict form; the contract (`contract.md:43-47`) describes "every step {…}".
- Consequence: the knowledge entry's own recheck (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) fails on its own receipts;
  the lesson gate (`corpus/lessons/round-17.md:26`) and SKILL `receipt-validate` row (`SKILL.md:536`) are contradicted; the C2 capability gate
  ("admitted only if receipt-validate exits 0") is not met. Measure confirms: `scorecard_capability_rows_matching: 0`.
- Fix direction: one side must change (producer to list, or validator to dict), then re-run all eight receipts.

### F2 HIGH — mid-run pin statements with no retained mid-run record
- Quoted: knowledge `…r17-go-carrier-diagnostics.md:27-30`: "hashed before, every 30 s during, and after each session … All eight pre/post compares are equal and no mid-run check differed."
  Lesson `corpus/lessons/round-17.md:26`: "pins equal pre/mid/post".
- Observed: receipt top-level keys (`python3 -B -I` read of all eight) are `bound_sessions, carrier, label, log_capture_limit, orig_argv, pins_compare, pins_post, pins_pre, python, rea_ghidra_env, retained_logs, session_dir_baseline, session_parent, session_parent_leftovers, steps, unbound_sessions`. No mid-run map, count or instant.
  `tools/carrier-run.py:422-433` runs the 30 s check (`PIN_CHECK_S = 30.0`, line 35) and writes only `pins_changed_during_run` on drift (line 430). Absence of the key is not a count of checks.
- Why it matters: QUALITY #19 (`corpus/QUALITY.md:29`) admits during-run claims only with records at named instants. The lesson's own rule
  (`round-17.md` "Equal maps establish identical bytes at those instants, not continuity") is contradicted by "no mid-run check differed".
  `temporal-sweep.py --rev da64646…` reports unqualified 0 while these sentences stand, because its regex does not match them.
- Fix: retain the mid-run check count and maps, or state only "pre and post maps equal at two instants".

### F3 HIGH — C1(b) falsifier not met; "re-exercised this round with retained argv" is unsupported
- Command: `python3 -B -I .ufo/waves/round-17/tools/invocation-audit.py --root <lane> --rev da64646…`. Counts: rows 17, exercised_match 6, labelled_unexercised 0, unlabelled_variant 11.
  Baseline `b563c79`: rows 7, exercised 5, unlabelled 2 (matches `LOG.md:2042-2043`).
- Citation-drift (`SKILL.md:448`) is "exercised_match" only against `.ufo/waves/round-16/verification.json` (`commands[17]/argv`, rev `27b8fc1`).
  No round-17 receipt exists: `ls .ufo/waves/round-17/verification.json` → not found.
- Custody-pair (`SKILL.md:449`) names `.ufo/waves/round-17/verification.json` as its retained argv (absent).
- Ten round-17 rows (`SKILL.md:532-541`) are unlabelled and have no retained argv.
- `corpus/lessons/round-17.md:74` says both rows were "re-exercised this round with retained argv": not supported at this revision.
- The audit classes citation-drift `exercised_match` with `row_says_unexercised: true` (its text says "an unexercised variant"); the labelled count therefore reads 0. INFERENCE: this hides a labelled row from the count; state it in the entry.
- Claim C1(b) "unlabelled M → 0" is therefore not met at `da64646`. The entry must report the final count, not 0.

### F4 MEDIUM — temporal-sweep "before" value depends on the tool version
- `TemporalSweepTool.md:31-37` (w1) reports baseline `sites 2, corrected 0, unqualified 2` for the first tool version.
  Committed tool at `b563c79…`: `sites 4, corrected 0, unqualified 4` (sites LOG.md:2012, round-16.md:154, verification.json:419, knowledge r16:95).
- Contract site list/regex (`contract.md:90-96`) was widened in the tool (`site_dirs: corpus/knowledge/`, joined lines, run/execution-scoped regex).
  LOG round-17 (`LOG.md:2041`) cites 4 without naming the widening; the C1 falsifier "N→0" compares two different definitions.
- Fix: state the widening and the before count under the same tool.

### F5 MEDIUM — undisclosed run environment override for pro-op
- `run-carriers.sh:17`: `[ "$label" = "pro-op" ] && envs=(env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000)`; receipt `rea_ghidra_env: {"REA_GHIDRA_STARTUP_TIMEOUT_MS": "900000"}` for pro-op only; `{}` for the other seven.
- Grep of `LOG.md`, `corpus/lessons/round-17.md`, `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` for `900000`/`STARTUP`: no round-17 hit. The knowledge method section does not list the override.
- `run-carriers.sh:15` (`rm -rf "$out"`) removes each label's directory before the run, so any earlier attempt is unretained. INFERENCE: pro-op's override suggests a prior timeout; the entry must say whether it did.

### F6 MEDIUM — "all Go lines were captured" overreaches the retained prefix
- Knowledge `…r17-go-carrier-diagnostics.md:131-133`: "Every Go line precedes the bridge script, so all Go lines were captured."
- Observed: the last line of all eight retained `ghidra.log` files is `ANALYZING changes made by post scripts` (tail read). The last Go line precedes the `SCRIPT:` line in each (e.g. calib-esbuild Go 10:49:20 < SCRIPT 10:49:22; pro-aether Go 10:50:39 < SCRIPT 10:51:10).
- Not observed: any Go lines from the post-script analysis pass, which the capture ends before (the lesson, `round-17.md:81-82`, concedes the prefix).
- Supported wording: "no Go line follows the bridge SCRIPT line in the retained prefix."

### F7 MEDIUM — wrong commit hash in two provenance sites
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37`: "committed at `2716747`". `run-carriers.sh:2`: "frozen at lane commit 2716747".
  `git rev-parse --verify -q 2716747` → not a commit. The freeze commit is `2711674` (`git log`), and `knowledge:1` correctly gives `271167473d87ef710f07ecdd98caf0ce12091686`.

### F8 MEDIUM — compare coverage is narrower than the prose
- Knowledge reports the hand prediction "matched" for pro-esbuild-0.27.7. `compare.py` output for that run has five fields only (`untested_version, snapshot_label, missing_bootstrap, snapshot_route, fallback_to`).
  The prediction's `extra_expectations` (`analyzer_errors_contain: "unable to get GoRttiMapper"`, `bootstrap_attempts_at_least: 1`, `language_compiler`) are not evaluated by any tool.
  Observed log-extract classification for this run: `other`. Its five fields are null or false by construction.
- Supported wording: "five contract fields match; extra expectations unchecked."

### F9 LOW — "retained" red-run and "retained in verification" claims with no retained artifact
- `corpus/lessons/round-17.md:78`: forced-route compare "(retained in verification)". No `verification.json` exists at `da64646`.
  Reproduced (attack-pass): forced `snapshot_route=info` on pro-notesmd-cli → `compare.py` exit 1 with `snapshot_route: false`; the other fields true. Claim holds when re-run, not retained.
- QUALITY #19 (`corpus/QUALITY.md:29`) requires "a retained red run". `pins.py --selftest` (attack-pass: `SELFTEST: CLEAN cases=7`; red line `red case observed: compare exit 1 names /tmp/pins-selftest-…/a.txt`) builds and deletes a temp fixture. Nothing is retained in-tree.

### F10 LOW — SCORECARD has no round-17 section
- `grep -n "round 17\|round-17\|r17" SCORECARD.md` → no lines. The round-16 measured entry records SCORECARD verdicts; the round-17 declared entry does not. The entry needs an explicit "not appended" or an appended section.

### F11 LOW — `controls.py` prints a constant gate
- `controls.py:370` `"conformance_gate": False` (docstring line 34: "computes no conformance gate"). Output exits 0 with `conformance_gate: false`. Do not quote it as pass or fail.

### F12 LOW — working tree differs from the attacked revision
- `git status --short`: ` M .ufo/waves/round-17/run-carriers.sh` (one-line `RUNS_DIR` change, `run-carriers.sh:14`, post-commit), untracked `verify.py`. The measured entry must name the script bytes used by the runs.

### F13 LOW — run-log.txt omits the first carrier run
- `runs/run-log.txt` has 14 lines and no `calib-shfmt` entry (`grep -c calib-shfmt runs/run-log.txt` → 0). The calib-shfmt receipt has `pins_pre` 13:47:05 UTC and analyze end 13:47:36 UTC (10:47 -03), before the first logged start (calib-esbuild-0.25.12, 10:47:42 -03). The run happened outside the logged sequence. The entry must record it.

## Bounded no-findings (what was checked and held)
- Predictions frozen: `git diff --stat 2711674 da64646 -- .ufo/waves/round-17/predictions` is empty; `predictions/` commit 2711674 (10:46:45 -0300) precedes the earliest run, calib-shfmt (receipt `pins_pre` 13:47:05 UTC = 10:47:05 -03). `runs/run-log.txt` starts at calib-esbuild-0.25.12 (10:47:42) and omits calib-shfmt (see F13).
- Pins: `pins_pre` has 146 entries (`pro-op`); `pins_compare.equal` true for 8/8 receipts.
- Binding: each retained `ghidra.log` has one `Using log file` and two `IMPORTING` lines; `bound_sessions` length 1, `unbound_sessions` empty for 8/8.
- Exits: analyze, inspect-go-binary, carrier-run, observation and compare exit 0 for 8/8 (`runs/*/*.exit`).
- Route claims: the eight `compare.json` `all_match` true; observed routes and versions match the knowledge table (`inspect-go.json` go versions: shfmt `go1.27.0-X:nodwarf5`, esbuild-0.25.12 `go1.23.12`, op `go1.26.8`, containerd-shim `go1.27.2-X:nodwarf5`, esbuild-0.27.7 `None`).
- Aether: `ghidra.log:97` ERROR `Go analysis failure`, `:177` `Caused by: java.io.EOFException`, `:207` `Go strings found: 7200`. Knowledge line refs correct.
- Evidence IDs: `calib-shfmt` `ev_2b29a1dd…` and `calib-esbuild` `ev_391dbfe6…` equal the pilot IDs (`pilot/shfmt.json`, `pilot/esb.json`).
- Temporal sweep corrections: the four `corrected_by` lines resolve to LOG.md:2059-2062 and point to the right sites.
- Controls at `b563c799…`→`da64646…`: exit 0; prefixes preserved (LOG appended 2627 bytes; knowledge 94/94; lessons 20/20; prior verifiers 5/5; prior wave/evidence blobs 14943/14943 unchanged); QUALITY rows 1–18 identical; rows 19–20 added; SOURCES immutable cells identical.
- Measure at `da64646`: knowledge 95 mapped/0 missing/0 dangling; SOURCES 30 rows, A26/B2/C2, mined 28, rejected 2; QUALITY row 19 present; `skill_registry_new_tool_names` 12.
- Selftests run once each, all exit 0 (`SELFTEST: CLEAN`): pins 7, retain 3, carrier-run 2, log-extract 8, predict 17, compare 10, invocation-audit 6, temporal-sweep 6, buildinfo-probe 11, receipt-validate 5, carrier-census 10, controls 11. `measure.py --selftest` not run (not assigned to this seat).
- `predict.py --go-version ""` → exit 2 (`{"error": "unparseable Go version ''…"}`), matching the contract.
- Wave-1 seat count in `LOG.md:2051`: 14+20+12+10+8+6+4+2+2 = 78 (arithmetic only; completion not re-checked).

## Not reviewed
buildinfo-probe and the BuildinfoGoCrossCheck seat; SCORECARD axis arithmetic (no round-17 section exists); REA behaviour beyond the retained receipts.

## Calibration
- High (command-observed): F1, F2 (key listing and grep), F3 (audit output and `ls`), F7, F11.
- Medium (observed plus one inference): F4, F5, F6, F8.
- Low (presentation or retention): F9, F10, F12.

## Slots the L1 pass must fill (also in the draft)
Final source sha; verification.json sha; per-tool selftest lines; pins red/green; sweep before/after under one tool version; mid-run record form; invocation-audit final unlabelled count and met/not-met; per-run ghidra.log sha256, polls, evidence IDs; per-run attempt list for pro-op; receipt-validate per-receipt exits; capability row admitted or not; controls rev; measure output; SCORECARD verdicts or "not appended"; installs (none so far).
