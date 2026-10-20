# DraftReportR17 — W2 falsification of round-17 artifacts

Revision attacked: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Baseline `b563c799d97774aae4351276fe43cb897311e349`. Read-only: round-17 tools against git objects and retained files; `git`; `grep`; `sha256sum -c`; `pacman -Qo` (read-only); `go version`; `python3 -I -B` only. No REA analyze/search/decompile, no Ghidra, no carrier execution, no subagents, no edits outside `w2/`.

Deliverables written: `.ufo/waves/round-17/w2/draft-report.md` (fleet report draft with required sections and slots), and this file.

## Findings (ordered by claim impact)

### F1 — HIGH — `receipt-validate.py` rejects every carrier receipt; C2 "receipt validates" gate is unmet
- Command: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-17/runs/calib-shfmt/receipt.json` → exit 1, `kind: unknown`, `findings: [{code: unrecognized_shape, where: "$"}]`. Same for all 8 receipts (`counts: {valid: 0, invalid: 1}` per call).
- Cause: `classify()` requires `receipt["steps"]` to be a **list** (`tools/receipt-validate.py:95-104`); `carrier-run.py` writes `steps` as a **dict** keyed by step name (`runs/calib-shfmt/receipt.json` → `"steps": {"analyze": {...}, "inspect-go-binary": {...}}`).
- Why the selftest did not catch it: `receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`; its fixtures use the list shape, so the mismatch is invisible to it.
- Consequence: knowledge entry line 3 (`recheck:`) tells a reader to run this validator on each receipt; it fails on all eight. claims.json C2 requires "capability rows +1 only if the capture runs and its receipt validates" — not satisfied. Withhold the capability row until the shape is reconciled and a real receipt validates.

### F2 — HIGH — C1b target not met: unlabelled registry variants rose 2 → 11, not → 0
- Command: `python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root . --rev da64646…` → `counts: {rows: 17, exercised_match: 6, labelled_unexercised: 0, unlabelled_variant: 11}`.
- Unlabelled rows: `custody-pair` (SKILL.md:449), `go-carrier-run` (:532), `go-log-extract` (:533), `go-route-predict` (:534), `go-route-compare` (:535), `receipt-validate` (:536), `pins` (:537), `temporal-sweep` (:538), `invocation-audit` (:539), `go-buildinfo-probe` (:540), `round17-structural-controls`. Ten of the eleven are round-17 rows appended by this round; none has a retained receipt whose argv matches.
- Baseline for comparison: `--rev b563c79` → `rows: 7, exercised_match: 5, unlabelled_variant: 2`.
- claims.json C1 "falsifiable_before_after": `unlabelled-variant registry rows M -> 0`. Measured after = 11. The LOG entry (`LOG.md:2066` "Measured values follow in the next entry") defers this; no measured after-value is recorded anywhere at `da64646`.

### F3 — HIGH — SKILL.md custody-pair row cites a receipt that does not exist
- `SKILL.md:449`: "(exercised argv retained in `.ufo/waves/round-17/verification.json`)".
- Command: `git cat-file -e da64646:.ufo/waves/round-17/verification.json` → `fatal: path '.ufo/waves/round-17/verification.json' does not exist in 'da64646'`. The file is absent from the committed tree and the working tree.
- This is an introduced defect (the row was "aligned in place" this round, per `LOG.md:2065`). It also explains why custody-pair stays `unlabelled_variant` in F2.

### F4 — MEDIUM-HIGH — citation-drift "re-exercised with its isolated absolute argv and the receipt retained" is not a round-17 re-exercise
- `invocation-audit.py` at `da64646` reports `citation-drift exercised_match .ufo/waves/round-16/verification.json` — a round-16 receipt, pre-existing (verified in that file at line ~321 / argv array).
- `grep -rl citation-drift .ufo/waves/round-17/runs .ufo/waves/round-17/*.json` returns only `claims.json`, `wave1-*.json`, `wave2-*.json` (specs and dispatch); no round-17 receipt exercises it.
- claims.json C1(b) requires the round-17 re-exercise and its retained receipt. Not present at `da64646`. The `exercised_match` for SKILL.md:448 is a false comfort: it matches old evidence.

### F5 — MEDIUM — "N → 0" temporal count is scope-bounded; lane-wide unqualified sites remain
- Tool scope and regex differ from the contract: `temporal-sweep.py:55-57` regex is wider than `contract.md:93` (adds `unchanged across`, `during the run`, etc.); tool header lines 35, 52 disclose this. The contract-regex count from w1 was 2 (`w1/DraftReport.md` item 2); the tool counts 4. LOG (`LOG.md:2047-2066`) reports 4 and mentions "widened" only in the seat-integration note.
- Outside the tool's file scope, `git grep -n -E "unchanged (during|across|throughout) (the )?(run|execution)|stable throughout|pins_unchanged_during_run|remained unchanged during" da64646 -- '*.md' '*.json'` still returns:
  - `.ufo/waves/arc2-loop1-round1/CR6.md:157` "mtime-stable throughout"
  - `.ufo/waves/arc2-loop1-round3/S2.md:222` "stable throughout"
  - `.ufo/waves/arc3-loop1-round3/claims/c2/EX-22/aftersmoke.md:58` "(unchanged during run)"
  - `.ufo/waves/arc3-loop1-round6/claims/verdicts/CR-5.md:434` "stable throughout"
  - Outside the lane (cited by w1 `ConnProvenanceRoutes.md:56`, not re-read by this seat): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` "Producer/input hashes stayed unchanged during execution."
- Not all of these are round-16 pin claims; the C1 text ("every lane statement asserting that round-16 pins stayed unchanged") does not clearly reach the arc files. The draft must say "0 unqualified in tool scope", not "0 unqualified".

### F6 — MEDIUM — admitted knowledge entry has the wrong freeze-commit hash
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:37`: "committed at `2716747` before the first run".
- `git rev-parse 2711674` → `271167473d87ef710f07ecdd98caf0ce12091686`; the freeze commit is `2711674`. `2716747` is not a commit in this lane. `git log 2711674..da64646 -- .ufo/waves/round-17/predictions` is empty, so the freeze itself holds; only the citation is wrong.

### F7 — MEDIUM — "every 30 s … no mid-run check differed" is not recorded anywhere retained
- `knowledge:26-29` states pins were hashed "before, every 30 s during, and after" and "no mid-run check differed".
- `tools/carrier-run.py:422-432` runs the mid-run check every `PIN_CHECK_S` = 30 s (`:35`), but records only on failure (`rec["pins_changed_during_run"]`). No receipt contains a mid-run field (`runs/*/receipt.json` key list: no `mid`, no count). A reader cannot tell whether 0, 1 or 2 mid-run checks ran; "no field present" is the only evidence.
- Verified: `grep -c pins_changed_during_run runs/*/receipt.json` → 0 for every run. This is consistent with "no change"; it does not show a check happened.

### F8 — MEDIUM — knowledge names "interface-type markup" for a failure the log does not name
- `knowledge:89`: the EOF occurred "during interface-type markup (`runs/pro-aether/logs/*/ghidra.log:97-177`)".
- `grep -n -i "interface\|markup" runs/pro-aether/logs/*/ghidra.log` returns only `markup`-named frames (`MarkupSession`, `FieldMappingInfo.makeMarkupReferenceFunc`, `StructureMappingInfo`); the token "interface" does not appear in the log. The specific label is an inference presented as an observation.

### F9 — MEDIUM — "all Go lines were captured" is unverifiable and contradicts the entry's own limit
- `knowledge:132`: "Every Go line precedes the bridge script, so all Go lines were captured."
- `runs/*/receipt.json` `log_capture_limit`: "polling copy; lines written after the final poll before REA deletes its runtime root can be missing". The same bullet then says "Absence claims hold only up to the last retained line." The capture cannot establish completeness. Replace with "all Go lines retained are listed; completeness not established".

### F10 — MEDIUM — LOG states an unobserved cause for the dispatch refusals
- `LOG.md:2053`: "dispatch refused twice at the host job cap, spawned on the third identical attempt."
- `.ufo/waves/round-17/wave1-dispatch-attempts.json` records `refused: 78, 78, 0` with no cause field. `grep -rn "job cap" .ufo/waves/round-17/w1 .ufo/waves/round-17/wave1-*` returns nothing. `w1/DraftReport.md` item 8 correctly says the cause is not recorded and is [INFERENCE] at most. LOG upgraded it to fact. Fix: "refused twice (cause not recorded)".

### F11 — LOW-MEDIUM — compare.py ignores the frozen prediction's `extra_expectations`; "match: true" for esbuild 0.27.7 covers five fields only
- `predictions/pro-esbuild-0.27.7.prediction.json` contains `extra_expectations`: `analyzer_errors_contain`, `bootstrap_attempts_at_least`, `invalid_version_strings`, `language_compiler`. `tools/compare.py` never reads these keys (`grep -n extra_expectations tools/compare.py` → no match).
- This seat checked them by hand against `runs/pro-esbuild-0.27.7/observation.json`: all four pass (`analyzer_errors` contains `unable to get GoRttiMapper`; `bootstrap_attempts` 2 ≥ 1; `language_compiler` `x86:LE:64:default:golang`; `invalid_version_strings` []). So no hidden mismatch exists; the mechanical gate is weaker than the knowledge table implies. The 0.27.7 row is also a hand prediction (disclosed at `knowledge:39` and in the prediction's `author` field).

### F12 — MEDIUM — QUALITY row 20 is unrequested and circular
- `corpus/QUALITY.md:30`: row 20 is admitted with "Sources: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`" and "sharpens 5, 6, 9". The same knowledge entry is the sole evidence for the rule it sharpens.
- claims.json C1 asks only for row 19 (C1c); C2 asks for a knowledge entry and a capability row. Row 20 is neither. `LOG.md:2063-2066` lists "QUALITY #19/#20". Contract rule: no inferred scope. Withhold row 20 or name it as a separate admission with its own claim.

### F13 — MEDIUM (process) — C2 capability row not landed at `da64646`
- `measure.py` `scorecard_capability_rows_matching: 0`; `grep -c "retained REA Ghidra-session log" SCORECARD.md` → 0. claims.json C2 after-state is "capability rows +1 only if the capture runs and its receipt validates". Neither condition is met at this revision (F1). Record as not landed.

### F14 — LOW — private TMPDIR roots persist; leftover recorded but not disclosed
- `ls -d /tmp/kr17-rea-*` → 8 directories, one per carrier run. Each `runs/*/receipt.json` has `session_parent_leftovers: ["node-compile-cache"]`. Knowledge does not mention either. The "private TMPDIR" claim (`knowledge` Method "Capture") holds for isolation but not for cleanup. Disclose; decide whether to remove.

### F15 — LOW — the w1 "LOG has no matching phrase" finding is wrong and must not be carried forward
- `w1/DraftReport.md` item 4 says LOG.md and SCORECARD.md "contain no matching phrase" and the LOG attribution is "not reproduced".
- `LOG.md:2012` reads "Producer/fixture hashes remain unchanged across execution." `temporal-sweep.py --sites-rev b563c79` flags it (`corrected: false` at baseline; `corrected_by: LOG.md:2059` at `da64646`). The draft uses LOG:2012 as a site. Do not write "not reproduced".

### F16 — LOW — S024 citation
- `knowledge:1` cites "S024 (Go `debug/buildinfo` reader, https://go.dev/src/debug/buildinfo/buildinfo.go at go1.27.3)". The URL is a master view; the go1.27.3 tree is the local tarball (`w1/DraftSourcesRows.md:47` says so). Write the local tarball path, or "URL (master) and go1.27.3 tree".

### F17 — LOW — Go toolchain install location deviates from the operator directive
- Directive: official release binary "into `~/.local/bin`". Seat `DraftSourcesRows` installed the go1.27.3 tree to `~/.local/opt/go-1.27.3` (not on PATH; `go version` only works with the full path). Verified: `/home/vgpnk/.local/opt/go-1.27.3/bin/go version` → `go1.27.3 linux/amd64`. Record the deviation in the fleet report; it is not a defect of the artifacts.

### F18 — LOW — draft slot not yet filled: Stale-lane
- `LOG.md` round-17 entry (`2032-2066`) has no stale-lane watchdog line. The round-16 precedent (`corpus/lessons/round-16.md:69-71`) has one. The draft carries a slot; L1 must run the sweep at record time.

## Bounded no-findings (what was run and held)

- `sha256sum -c predictions/SHA256SUMS` (from round-17 dir): all OK. `sha256sum -c pilot/SHA256SUMS` (from pilot dir): all OK. My first pilot check ran from the wrong directory and failed; that was my invocation error, not an artifact defect.
- `git log 2711674..da64646 -- .ufo/waves/round-17/predictions` → empty. Predictions were not edited after the freeze.
- `receipt-validate.py --selftest` → CLEAN cases=5; `pins.py --selftest` → CLEAN cases=7. Selftests pass; see F1 for the real-receipt failure.
- Pins: `pins_pre`/`pins_post` equal on 8/8 receipts; 146 entries per run (143 under `typeinfo/golang/`).
- Bound sessions: 1 bound, 0 unbound on the three receipts checked (`calib-shfmt`, `pro-op`, `pro-esbuild-0.27.7`); the other five were not individually checked.
- Predicted inspect-go vs run inspect-go Evidence IDs and Go versions: equal for the seven prediction files I compared (`calib-esbuild-0.25.12`, `calib-shfmt`, `pro-aether`, `pro-containerd-shim`, `pro-esbuild-0.21.5`, `pro-notesmd-cli`, `pro-op`). `pro-esbuild-0.27.7` was not compared against its inspect file.
- `compare.json` for 8/8 runs: five fields (`untested_version`, `snapshot_label`, `missing_bootstrap`, `snapshot_route`, `fallback_to`) match. The `snapshot_route`/`fallback_to` fields go beyond contract.md:75's three fields; the knowledge entry discloses this (`knowledge:45`).
- Analyzer EOF exists at `runs/pro-aether/logs/*/ghidra.log:177` (`Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`); `Go strings found: 7200` at `:207`.
- Log-count claims: "Missing Go bootstrap" ×2 for calib-shfmt, pro-containerd-shim, pro-op; ×0 for in-range; "Falling back" ×1 for pro-aether, pro-notesmd-cli. All match the knowledge table.
- `buildinfo-probe.py` on the esbuild 0.27.7 carrier: `found: false`, `magic_file_offsets: []`, agrees with REA `build_info: null`. Read-only.
- `pacman -Qo` owners: `/usr/bin/shfmt` → shfmt 3.14.1-1; `/usr/bin/aether` → aether 4.32.0-2; `/usr/bin/op` → 1password-cli 2.41.0-1; `/usr/bin/containerd-shim-runc-v2` → containerd 2.4.2-1; `~/.local/bin/notesmd-cli` → no owner. All match the knowledge table.
- `go version -m /usr/bin/shfmt` (go1.27.3 binary) → `go1.27.0-X:nodwarf5`, matches calib-shfmt receipt.
- `measure.py` at `b563c79` and `da64646`: `missing: []`, `dangling: []`, `tools_present: 11`, `run_receipts: 8`, `sources_rows: 23 → 30`, `knowledge_files: 94 → 95`.
- `controls.py b563c79 da64646`: `quality_admission_rows.violations: {}` with rows 1–18 byte-identical; `log_old_prefix.prefix_preserved: true`. I did not individually review the other control sections.
- Temporal corrections present: `corrected_by` for the four sites = `LOG.md:2059`, `:2060`, `:2061`, `:2062`.
- SHONEN.md: `git diff b563c79 da64646 -- SHONEN.md` empty; all four boxes remain `[~]`.
- Round-16 verifier-cited pins (`corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`) are real and match the sweep text.

## Tool installs/updates by this seat

None. Read-only queries only (`pacman -Qo` is read-only). No pacman transaction.

## Calibration note on this report

Where the artifacts claim a number, this seat either reproduced it with the named command or marked it as not verified. Where a number in the round-17 LOG or knowledge entry depends on an unrecorded fact (F7, F9, F10), it is flagged rather than accepted.
