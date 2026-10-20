# DraftScorecardR17 — w2 falsification report (author-side advisory leaf)

Deliverable: `.ufo/waves/round-17/w2/draft-scorecard.md` (`## Round 17` draft, shape of `SCORECARD.md:2294-2348`, `{FINAL:...}` slots). Written only: that draft and this report. No `SCORECARD.md`, LOG, QUALITY, SKILL, SOURCES, README, lesson, knowledge, tool, corpus or carrier was edited. No commit, no push. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier executed, no `rea inspect-go-binary` run.

Evidence base: committed tree at `da64646adcb19c1ede7537b799b8c7d283fe43da`, exported to `/tmp/r17-da646` with `git archive` (scratch). Tools were run from that export with `python3 -B -I`. `measure.py` and `controls.py` need the real repo, so they ran from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` against the same commit. Working tree was clean for `runs/`, `tools/`, `predictions/`, `pilot/`. Untracked files in `w2/` are peers' outputs and were not used.

## Axes and lane
- Claims (`.ufo/waves/round-17/claims.json`): C1 calibration (R16-PROVENANCE, R16-INVOCATION, QUALITY #19); C2 depth with capability acquisition (Go carrier diagnostics).
- Calibration is tied-lowest. Depth is the C2 capability move.

## Verdict in one paragraph
Most of the C2 *measurement* holds up under reproduction: 8 bound, pinned, retained runs; logs match their digests; the extractor, predictor and compare reproduce every committed output byte for byte. The C2 *capability* entry condition does not hold: the committed validator rejects all 8 real receipts (F1). C1 is partly discharged: the temporal-sweep and pins red case hold, but the registry-variant count went from 2 to 11, not to 0 (F2), and the artifact the registry and lesson cite for round 17 does not exist (F3). Several prose claims exceed their records (F4, F6, F8, F9). A post-commit gitignored pyc landed in the frozen round-16 directory (F5).

## Findings (observation unless marked [INFERENCE])

**F1 — high (C2 capability gate): `receipt-validate.py` rejects all eight real receipts; its selftest passes.**
- Code: `tools/receipt-validate.py:98-101` classifies as `carrier` only when `steps` is a **list**; `tools/receipt-validate.py:284` iterates `steps` as a list. The producer writes `steps` as a **dict**: `tools/carrier-run.py:275` (`"steps": {}`), `:317` and `:349` (`receipt["steps"] = steps`, keys like `analyze`, `inspect-go-binary`).
- Command: `cd /tmp/r17-da646/.ufo/waves/round-17 && python3 -B -I tools/receipt-validate.py $(ls runs/*/receipt.json)`
- Output (excerpt): exit `1`; `"counts": {"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}`; every receipt: `"code": "unrecognized_shape", "detail": "receipt matches neither retain nor carrier shape", "where": "$"`.
- Selftest: `python3 -B -I tools/receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=5`, exit 0. The fixtures use the shape the validator expects, not the shape the producer writes.
- Impact: the draft's capability entry condition (validator exit 0) is false at `da64646`. The knowledge recheck line (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) and the SKILL row (`SKILL.md:536`) both direct use of this validator. [Repair is outside this seat; the draft keeps the entry conditional.]

**F2 — high (C1 sub-claim b not discharged): unlabelled registry variants rose 2 → 11.**
- Command: `python3 -B -I tools/invocation-audit.py --root <LANE> --rev b563c79` → `{'rows': 7, 'exercised_match': 5, 'labelled_unexercised': 0, 'unlabelled_variant': 2}` (`citation-drift` and `custody-pair`).
- Command: same at `--rev da64646` → `{'rows': 17, 'exercised_match': 6, 'labelled_unexercised': 0, 'unlabelled_variant': 11}`.
- The 11 unlabelled rows: `SKILL.md:449` custody-pair, and ten round-17 rows `SKILL.md:532-541` (`go-carrier-run`, `go-log-extract`, `go-route-predict`, `go-route-compare`, `receipt-validate`, `pins`, `temporal-sweep`, `invocation-audit`, `go-buildinfo-probe`, `round17-structural-controls`). None carries the label `unexercised`, and none matches a receipt argv.
- `citation-drift` (`SKILL.md:448`) now matches only the round-16 receipt (`.ufo/waves/round-16/verification.json`).
- The claim "re-exercised this round with retained argv" (`corpus/lessons/round-17.md:74`) has no round-17 receipt behind it (see F3). The claims file's target of "unlabelled-variant rows M → 0" (`claims.json`, C1 `falsifiable_before_after`) is not met at `da64646`.

**F3 — high (provenance): the round-17 `verification.json` that the registry, lesson and draft cite is not committed.**
- Command: `git ls-tree -r da64646 --name-only | grep -c 'round-17/verification.json'` → `0`. Only the round-16 file exists (`git ls-tree da64646 .ufo/waves/round-16/verification.json` → blob `b088efb6…`).
- Cited at `SKILL.md:448` ("exercised argv: … `.ufo/waves/round-17/verification.json`"), `SKILL.md:449` ("retained in `.ufo/waves/round-17/verification.json`"), and `corpus/lessons/round-17.md:78` ("(retained in verification)"). The compare-field demonstration (notesmd route forced to `info`, exit 1) is therefore not reproducible from the commit.

**F4 — medium (temporal claim exceeds record): "pre/mid/post" pins.**
- Prose: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:26-29` ("hashed before, every 30 s during, and after … All eight pre/post compares are equal and no mid-run check differed"); `corpus/lessons/round-17.md:26` ("pins equal pre/mid/post"); `corpus/lessons/round-17.md:73` ("pre, 30 s mid-run and post maps with timestamps"); `SKILL.md:532`.
- Code: `tools/carrier-run.py:35` `PIN_CHECK_S = 30.0`; `:422-432` performs the mid check and writes `pins_changed_during_run` **only if unequal**.
- Records: every receipt has `pins_pre`, `pins_post`, `pins_compare` (`equal: true`, 146 entries each, taken at 13:47–14:00 UTC) and no mid map or check count. `git grep -c pins_changed_during_run da64646 -- .ufo/waves/round-17/runs` → no output.
- So "every 30 s" and "no mid-run check differed" are code behaviour plus absence of a key; the number of mid checks is not retained. QUALITY #19 (`corpus/QUALITY.md:29`) requires retained pre/post maps with timestamps and comparison — which exist — but the knowledge text claims more. [INFERENCE: the statement is true of the code path; it is not measured.]

**F5 — medium (frozen-directory landing after commit): gitignored pyc in `.ufo/waves/round-16/`.**
- Command: `ls -la --time-style=full-iso .ufo/waves/round-16/__pycache__/` → `selection.cpython-314.pyc`, mtime `2026-10-20 11:08:56.134992659 -0300`.
- Commit time: `git log -1 --format=%ci da64646` → `2026-10-20 11:06:06 -0300`. The pyc was therefore written **after** the commit.
- `.gitignore:1` (`__pycache__/`) hides it from Git-object controls. The lesson says the pyc was "Removed before commit" (`corpus/lessons/round-17.md:77`); LOG says "-B everywhere … (removed)" (`LOG.md:2055-2056`). Every invocation this seat ran used `-B`, and none imported round-16 `selection.py` with bytecode writes enabled. The writer is not identified. [INFERENCE: a peer process without `-B`.]

**F6 — medium (unsupported completion claim): "W1 78 seats, all completed".**
- Prose: `LOG.md:2051-2052` ("78 seats … all completed"); `corpus/lessons/round-17.md:97` ("W1 was 78 seats, all completed").
- Records: `wave1-dispatch.json` counts `{'spawn': 78, 'resume': 0, 'total': 78}`; `wave1-registration.json` has 78 members with keys `kind, agentId, role, item, axes` and **no status field** (`Counter({None: 78})`); `wave1-result.txt` is a spawn list. No committed artifact records completion.
- Draft treatment: `{FINAL:W1 completion evidence}`.

**F7 — medium (tool drift during the run window; no retained output for a cited check).**
- `git diff --stat 271167473d87ef710f07ecdd98caf0ce12091686 da64646 -- .ufo/waves/round-17/tools` → `buildinfo-probe.py` (7 lines), `temporal-sweep.py` (182 lines) changed after the freeze.
- mtimes (working tree, equal to HEAD for these files): `buildinfo-probe.py` `10:47:16 -0300`; `temporal-sweep.py` `10:49:23 -0300`. First carrier pin snapshot `calib-shfmt` at `13:47:05 UTC` = `10:47:05 -0300`, so both edits fell inside the run window. The carrier-path tools (`pins.py` 10:40:40, `predict.py` 10:44:46, `log-extract.py` 10:44:25, `compare.py` 10:45:03, `carrier-run.py` 10:46:00) predate it. The run outputs are therefore not affected by these two edits.
- Knowledge `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:80` says the `buildinfo-probe.py` "whole-file scan agrees". No committed output records that: `git grep -l buildinfo-probe da64646 -- .ufo/waves/round-17/runs .ufo/waves/round-17/predictions` → nothing. My own run of the committed version reproduces it (see verification below), so the claim is true now but unrecorded at run time.

**F8 — medium (undisclosed deviation): `pro-op` ran with a startup-timeout override.**
- `run-carriers.sh:17`: `[ "$label" = "pro-op" ] && envs=(env REA_GHIDRA_STARTUP_TIMEOUT_MS=900000)`.
- `runs/pro-op/receipt.json` `rea_ghidra_env: {"REA_GHIDRA_STARTUP_TIMEOUT_MS": "900000"}`; `runs/calib-shfmt/receipt.json` `rea_ghidra_env: {}`.
- Knowledge: `grep -c -i STARTUP corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` → `0`. The method section does not mention the override.

**F9 — medium (calibration of the headline): "8/8 compare exit 0" overstates discrimination.**
- All eight `compare.json` have `all_match: true`. `snapshot_label` is non-discriminating by its own rule (`rules.snapshot_label: "contains-or-both-empty (non-discriminating: request echo)"`).
- `pro-esbuild-0.27.7`: prediction is hand-written (`predictions/pro-esbuild-0.27.7.prediction.json`, `author` field). Its observed `classification` is `"other"` (`observation.json`), because Go lines exist; the tool cannot express "no build-info". Its 4 comparable fields match only by absence: no bootstrap line → `missing_bootstrap` false; no version → `snapshot_route` none. The knowledge's "no mapper" label (`knowledge:58`) and decision row (`knowledge:106`) carry that distinction in prose only.
- The honest headline is "8/8 all_match; four fields per carrier, one hand-predicted carrier matched by absence". The draft reports this.

**F10 — low (scope): QUALITY #20 is not a claimed deliverable.**
- `controls.py` output: `quality_admission_rows: {added_rows: ["19","20"], rows_before: 18, rows_after: 20}`; `corpus/QUALITY.md:30` (#20). `claims.json` C2 names no QUALITY row. The lesson presents #20 as "added" from the round's own findings (`corpus/lessons/round-17.md:17`, `:27`). The draft lists it only as a non-claim addition (it is not in the C2 row).

**F11 — low (incomplete run record): `calib-shfmt` absent from `runs/run-log.txt`.**
- `git show da64646:.ufo/waves/round-17/runs/run-log.txt | head -1` → `== calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00`. The log has 7 labels; `calib-shfmt` ran first (receipt pins_pre `13:47:05 UTC`). `run-carriers.sh` does not write this log. The knowledge says the runs were "run sequentially by the round-17 L1" (`knowledge:2`).

**F12 — low (capability and stagnation bookkeeping, for L1 integration).**
- `claims.json` C2 says "capability rows 4 (+r13/r14 appended)". The main table has 4 rows at `SCORECARD.md:619-622` (header `:617`); round-13 and round-14 rows sit at `:2135` and `:2207`, in sub-tables.
- Stagnation: last explicit counter `3/10` at `SCORECARD.md:1500`; capability interval reset by round 14 at `SCORECARD.md:2226`; round 15 "no … stagnation reset" (`SCORECARD.md:2248`); round 16 "no capability-table row or stagnation reset" (`SCORECARD.md:2317`). [INFERENCE: pre-round-17 counter 2/10.] The draft leaves `{stagnation_before}` as a slot with that inference labelled.

## Verifications that passed (positive evidence; not defects)
- **Prediction freeze.** `git merge-base --is-ancestor 271167473d87ef710f07ecdd98caf0ce12091686 da64646` → ancestor; `git diff --stat 2711674 da64646 -- .ufo/waves/round-17/predictions` → no lines; `sha256sum -c predictions/SHA256SUMS` (run from the round-17 root) → `17 OK`.
- **Pilot digests.** `sha256sum -c pilot/SHA256SUMS | tail -3` (run from `pilot/`) → `shfmt-log/script.log: OK`, `esb.json: OK`, `shfmt.json: OK` (the pilot is calibration only, per `pilot/README.txt`).
- **Carrier identity.** `sha256sum` of the eight carrier paths on disk (read-only) matches the 16-character prefixes in the knowledge table and the receipt `carrier.sha256_pre`/`sha256_post` for every run (`58f765638eed5309`, `bab29b2ca7a9e89b`, `412dc532d278b9e4`, `06c91f55df4117e5`, `b567f467fdac92c6`, `d3aa80d720b80f70`, `c638273fcf95573c`, `f4ac474fd0202c73`).
- **Retained logs.** 16 retained log files (8 runs × `ghidra.log`/`script.log`); each sha256 and byte count equals the committed blob (`git show da64646:<path> | sha256sum`), 0 mismatches.
- **Binding.** Every receipt: `bound_sessions` length 1, `unbound_sessions` `[]`, `pins_compare.equal` true, `changed` and `missing` empty.
- **Extraction and comparison reproduce.** For all eight runs `tools/log-extract.py --log <bound ghidra.log>` output equals `observation.json` (dict equality, `identical []`); `tools/compare.py` exit 0 on each.
- **Prediction reproduces.** `tools/predict.py --go-version <inspect-go go_version> --golang-root <data dir>` exit 0 for the seven versioned carriers, and the `expected` block equals each committed prediction; `predict.py --go-version ''` exit 2 (`{"error": "unparseable Go version '' …"}`), as the hand-prediction note says.
- **Selftests (committed tools).** `pins.py --selftest` → `red case observed: compare exit 1 names /tmp/pins-selftest-…/a.txt`, `SELFTEST: CLEAN cases=7`; `log-extract` 8, `predict` 17, `compare` 10, `receipt-validate` 5, all CLEAN (F1 applies to the last).
- **Sweep.** `temporal-sweep.py --root <LANE> --rev da64646 --sites-rev b563c79` → `{'sites': 4, 'corrected': 4, 'unqualified': 0}`, with each correction at `LOG.md:2059-2062`. Baseline same command: `{'sites': 4, 'corrected': 0, 'unqualified': 4}`.
- **Controls.** `controls.py b563c79 da64646` exit 0 (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`); 14,943 wave blobs checked, 0 changed; 20 old lessons and 94 old knowledge prefixes preserved; five prior verifiers unchanged; QUALITY rows 18→20 with prior rows byte-identical; craft 17/17 both revisions.
- **Measure.** `measure.py da64646` exit 0: knowledge mapped 95/95 (baseline 94/94), missing and dangling empty, run receipts 8, SOURCES 30 rows (A26/B2/C2; mined 28, rejected 2), baseline 23 rows (A21/B1/C1; mined 22, rejected 1).
- **Source anchors (installed Base-src.zip).** `GoRttiMapper.java:79` `GoVerRange.parse("1.15-1.25")`; `:170-172` `Msg.error(… "Untested Go version …")` with no other action; `:179-180` `Using Go API snapshot for version %s`; `GoBuildInfo.java:488-489` strips `go`; `GoVer.java:62` `parse(String s, int missingPatchValue)`; `GoApiSnapshot` is at `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (not `golang/`), whose `getPatchVerDiffFile` emits the `Falling back …` WARN and `Using Go API snapshot for %s` INFO. [Line numbers for the `GoApiSnapshot` anchors were not individually re-checked; the knowledge cites `GoApiSnapshot.java:122-126`, `:158-161`, `:162-164`, `:148-166` without the `rtti/` path.] `TransientProgramProperties.java:107-110` returns null without caching. `GoRttiMapper.java:355-361` throws `BootstrapInfoException` only when `apiSnapshot.isInvalid()`.
- **Aether anomaly.** `pro-aether` log: `97:` `Go analysis failure … InvocationTargetException`, `177:` `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`, `207:` `Go strings found: 7200` — matches knowledge `:84-91`.
- **Buildinfo probe (read-only bytes).** `buildinfo-probe.py /usr/bin/shfmt` → `found: true`, `go_version: go1.27.0-X:nodwarf5`; on the esbuild 0.27.7 file → `found: false`, `bytes: 11120788`. Matches the knowledge.
- **Pilot evidence IDs.** `pilot/esb.json` `ev_391dbfe6…` and `pilot/shfmt.json` `ev_2b29a1dd…` equal the calib runs' `analyze.json`. [The repetition is one observation; the knowledge labels it so.]
- **Corrections present.** `LOG.md:2059-2062` and `corpus/lessons/round-17.md:85-88` contain the four `R16-PROVENANCE:` lines with exact `file:line` and "temporal stability not evidenced" (the sweep counted them).

## Not verified (bounded)
- `GoApiSnapshot` line ranges beyond content (above).
- The 14,943-blob control is verified as "no change flagged by controls.py", not by an independent hash sweep.
- `inspect-go-binary` was not re-run; receipts' inspect-go outputs were used as committed.
- Ghidra, REA and the 8 analyses were not re-executed (contract: never).
- W2 results are not committed and are not cited.

## Tooling record
None. No install, update or upgrade by this seat. No pacman transaction. Scratch under `/tmp` only (`/tmp/r17-da646`, `/tmp/r17-*.json`, `/tmp/r17-audit-summ.py`).

## Artifacts
- `.ufo/waves/round-17/w2/draft-scorecard.md` (draft, `{FINAL:…}` slots)
- `.ufo/waves/round-17/w2/DraftScorecardR17.md` (this report)

## Checks for the main agent (after integration)
1. Repair `receipt-validate.py` classify/iteration to the producer's dict-`steps` shape, or repair the producer; re-run on all eight receipts; retain the exit. Then the capability row decision follows the exit.
2. Label or retire the ten round-17 unlabelled registry rows and the custody-pair row; commit the cited round-17 `verification.json` or remove the citation (F2, F3).
3. Re-run `temporal-sweep.py --rev <FINAL> --sites-rev b563c79`, `invocation-audit.py --rev <FINAL>`, `measure.py <FINAL>`, `controls.py b563c79 <FINAL>` at the final revision; fill the `{FINAL:…}` slots from those outputs only.
4. Check the pyc in `.ufo/waves/round-16/__pycache__/` is absent at the final revision (F5).
