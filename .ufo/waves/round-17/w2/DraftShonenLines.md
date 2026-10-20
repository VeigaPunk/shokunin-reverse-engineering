# DraftShonenLines — round-17 wave 2 falsification (author-side advisory)

Lane revision attacked: `da64646adcb19c1ede7537b799b8c7d283fe43da` (HEAD). Draft: `.ufo/waves/round-17/w2/draft-shonen.md` (four lines, all `[~]`, no `[x]`).
Scope: leaf seat; no subagents; no REA analyze/search/decompile, no Ghidra, no carrier execution. Commands run: `python3 -I -B` on round-17 tools (`receipt-validate.py`, `invocation-audit.py`, `temporal-sweep.py`) against retained files; `git` object reads; `sha256sum -c`; read-only `pacman -Qo` / `pacman -Q`; scratch script `/tmp/kr17_w2_check.py`. Tool installs/updates: none.

## Verdict
The four SHONEN pointers resolve. Round-17 evidence is real and digest-consistent, but it is not validator-clean and does not discharge the claims that depend on validation (C1(b), C2 receipt criterion). It strengthens box 2 only as a candidate; box 3 is not strengthened.

## Findings (ranked)

**F1 — HIGH — all eight retained carrier receipts fail the round-17 validator.**
- Command: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/calib-shfmt/receipt.json`
- Output (excerpt): `"exit": 1`, `"status": "invalid"`, finding `{"code": "unrecognized_shape", "where": "$"}`, `checks_performed: 306`. Identical for `calib-esbuild-0.25.12`, `pro-aether`, `pro-containerd-shim`, `pro-esbuild-0.21.5`, `pro-esbuild-0.27.7`, `pro-notesmd-cli`, `pro-op`.
- Cause: producer and validator disagree on `steps`. Producer `tools/carrier-run.py:309` `steps = {}`, keyed `analyze` / `inspect-go-binary` (plus `search:NAME`). Validator `tools/receipt-validate.py` `classify()` requires `isinstance(receipt.get("steps"), list)` for `carrier`; otherwise `unknown`. `CARRIER_STEP_REQUIRED` (`:62`) is applied per list entry (`:291`) and never reached.
- [INFERENCE] The validator selftest builds its own fixture in-process, so it cannot catch a producer mismatch; not verified by running it.
- Impact: C2 falsifier "+1 only if the capture runs and its receipt validates" is unmet. The SKILL.md round-17 `receipt-validate` row (`SKILL.md:536`) says exit 0 means valid. Digests are consistent (N1), so this is a shape defect, not tampering.
- Direction (not applied; I may not edit tools): one shape; fix producer or validator and re-run retained receipts.

**F2 — HIGH (calibration) — log classifier reports a Go analysis failure as `snapshot_loaded`.**
- `.ufo/waves/round-17/runs/pro-aether/observation.json`: `"classification": "snapshot_loaded"`, `"analyzer_errors": ["Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException"]`, `"snapshot_fallbacks": [{"from":"1.25.14","to":"1.25.0"}]`.
- Retained log: `.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log:97` `ERROR (GolangSymbolAnalyzer) Go analysis failure …`; `:177` `Caused by: java.io.EOFException: Unable to read past EOF`.
- Code: `tools/log-extract.py:213-219`: `missing_bootstrap → bootstrap_missing; elif snapshot_labels → snapshot_loaded; elif not go_lines → no_go_analysis; else other`. `analyzer_errors` never affects classification. `contract.md:58-59` mandates this order, so the defect sits in the contract.
- Consequence: `runs/pro-aether/compare.json` is `all_match: true`. The "unpredicted" aether EOF/markup failure (`LOG.md:2047-2049`) is therefore invisible to compare.py; the SKILL table row "Bootstrap OK, then Go analysis failure" has no classifier output that names it.

**F3 — HIGH (C1(b) not discharged) — every new round-17 registry row is an unlabelled variant.**
- Command: `python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev da64646adcb19c1ede7537b799b8c7d283fe43da` → exit 0; counts `rows 17, exercised_match 6, labelled_unexercised 0, unlabelled_variant 11, argv_records 74, receipt_glob_pathform_excluded 71`.
- Unlabelled: custody-pair, go-carrier-run, go-log-extract, go-route-predict, go-route-compare, receipt-validate, pins, temporal-sweep, invocation-audit, go-buildinfo-probe, round17-structural-controls. C1(b) requires zero.
- Baseline comparison: LOG.md r17 section (`LOG.md:2041-2042`) records 7 rows, 5 exercised, 2 unlabelled at b563c79. Post-integration rows grew to 17 and unlabelled to 11.
- `go-carrier-run` row (`bash …/run-carriers.sh <LABEL>`) can never match: no receipt records a bash argv. Needs a `labelled_unexercised` tag or a retained argv.
- `receipt_glob_pathform_excluded: 71` (`invocation-audit.py:343`): 71 of 74 argv records are excluded by a path-form rule. I did not trace the rule; match counts may be understated. [INFERENCE on effect]

**F4 — MEDIUM (calibration) — "8/8 compare exit 0" includes a field that tests the request echo, not selection.**
- `runs/calib-shfmt/compare.json` and `runs/calib-esbuild-0.25.12/compare.json` rules: `"snapshot_label": "contains-or-both-empty (non-discriminating: request echo)"`; `"fallback_to"` and `"untested_version"` are contains-or-both-empty.
- In calib-shfmt the snapshot_label field is `observed: [], predicted: null` → pass by both-empty. The 8/8 headline (`SKILL.md:515`; `LOG.md:2047`) therefore overstates selection evidence. Only `missing_bootstrap` and `snapshot_route` are equality checks.

**F5 — MEDIUM — retained Ghidra logs are polling copies; tail completeness unknown.**
- `runs/calib-shfmt/logs/rea-ghidra-j5AXOZ/ghidra.log` last line `2026-10-20 10:47:36 … ANALYZING changes made by post scripts`; `pins_post` at 10:47:37 -03. No session-close line retained. Receipt field `log_capture_limit` admits lines may be missing.
- Consequence: no box line may describe these logs as complete.

**F6 — LOW — measured round-17 LOG entry not appended.**
- `tail -n 3 LOG.md`: r17 section ends "Measured values follow in the next entry after the single post-integration execution pass." LOG.md is 2067 lines and has no following entry. Pre-falsify; box lines must cite `runs/` directly, not LOG, for r17 measurements.

**F7 — LOW — reproducibility of the registry command.**
- `run-carriers.sh` sets `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` for `pro-op` and passes ~146 `--pin` args; neither appears in the SKILL row `bash …/run-carriers.sh <LABEL>` or the contract CLI spec. `orig_argv` records `python3 -I -B tools/carrier-run.py` (relative path), not the isolated absolute argv R16-INVOCATION asked for.

**F8 — LOW — temporal-sweep `corrected` is path-substring matching.**
- `temporal-sweep.py --rev da64646…` → `{'corrected': 4, 'sites': 4, 'unqualified': 0}`. Per contract (`contract.md:94-95`) a site is corrected if any R16-PROVENANCE line names its file path, not its line. Correct per contract, weak as evidence. Out-of-lane sites (e.g. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60`) are not counted; that is correct scope but should be stated.

## No-findings (bounded)
- **N1 Retained digests (8/8 run dirs):** for `analyze` and `inspect-go-binary` steps, stdout/stderr sha256 match files; retained `ghidra.log`/`script.log` sha256 and byte counts match; carrier sha256 pre = post (`/usr/bin/shfmt` 58f76563…; esbuild bab29b2c…); `pins_compare.equal: true`, 146 entries each. Script: `/tmp/kr17_w2_check.py`.
- **N2 Carrier and bundle identity:** `sha256sum /usr/bin/shfmt /usr/lib/libjq.so.1.0.4` matches receipt and bundle digests (58f76563…, 7e8bccc6…).
- **N3 Prediction freeze:** `git diff --stat 271167473d87ef710f07ecdd98caf0ce12091686 HEAD -- .ufo/waves/round-17/predictions .ufo/waves/round-17/claims.json` empty; `sha256sum -c predictions/SHA256SUMS` (from round-17 root) all OK; `pilot/SHA256SUMS` all OK.
- **N4 compare:** `all_match: true` for all eight `runs/*/compare.json`.
- **N5 SKILL pointer:** `git diff -U0 3e99fbd6… HEAD -- SKILL.md` hunks at :448, :464, :470 only; 81-314 contains 17 `- ` bullets.
- **N6 Round-1 pointers:** `corpus/lessons/2026-10-15-round-1.md` exists (206 lines); bundle is valid JSON, 18991 B, one record `ev_f5e5da50…` `inspect_native_instruction` bytes `f30f1efa`; `LOG.md:464` under header `:425`; `LOG.md:985` under header `:888` (2026-10-16 entry, not 2026-10-15 — cite both).
- **N7 PROVINCE:** `PROVINCE.md:114-116` is the safety-refusal bullet. `PROVINCE.md:52` added sentence verified: `pacman -Qo /usr/bin/op` → `1password-cli 2.41.0-1`; `runs/pro-op/observation.json` go1.26.8, untested, missing_bootstrap true; knowledge row `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:57`.
- **N8 SCORECARD:** `SCORECARD.md:88` is the "A — source-derived controls" recipe; box pointers should carry `:88`, not just "command A".
- **N9 Temporal wording:** sweep scope (LOG.md, SCORECARD.md, round-16 lesson, SKILL.md, verification.json) shows 0 unqualified sites. Other "unchanged throughout" wording exists outside round-16 (e.g. `.ufo/waves/arc3-loop1-round3/claims/c2/EX-22/aftersmoke.md:58`); outside C1(a) scope, not counted.

## Box-line effect (for L1)
- Box 1: no strengthening; new SKILL section is outside the pointer and currently contradicted (F1, F3).
- Box 2: candidate strengthening (eight real carriers, retained logs, digest-consistent). Keep `[~]`; do not cite receipts as validated (F1) or logs as complete (F5).
- Box 3: not strengthened (F3). Do not use "this round" for historical round-1 evidence (r16 verifier counts that phrase).
- Box 4: r17 `PROVINCE.md:52` addition verified accurate (N7); no boundary test added.

## Artifacts
- Draft: `.ufo/waves/round-17/w2/draft-shonen.md`
- Report: `.ufo/waves/round-17/w2/DraftShonenLines.md`
- Scratch (outside lane): `/tmp/kr17_w2_check.py`, `/tmp/kr17_w2_inv.json`, `/tmp/kr17_w2_ts.json`
