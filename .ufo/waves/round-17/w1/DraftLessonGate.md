# DraftLessonGate — round-17 `## Gate` draft report (author seat, advisory)

Seat: `KaidokuR17.DraftLessonGate-3` (leaf; no subagent dispatch). Base `b563c79`.

## Behavior

Drafted the `## Gate` section for `corpus/lessons/round-17.md` covering C1 (calibration) and C2 (depth), with admit/reject/defer per candidate, reasons, anchors, and `[SLOT]` evidence placeholders. Output: `.ufo/waves/round-17/w1/draft-lesson-gate.md`. This report is `.ufo/waves/round-17/w1/DraftLessonGate.md`. No other file was written. `corpus/lessons/round-17.md` does not exist yet and was not created.

## Gate

- Gate rule: `LEARNING.md:69-71` (fleet root `/home/vgpnk/Projects/shokunin/LEARNING.md`, not in the kaidoku repo; the assignment's “LEARNING.md:68-71” resolves to lines 67-71 “Files the path writes”). Spot-check rule: `LEARNING.md:42-45`. Mistakes rule: `LEARNING.md:19-21`.
- Format mirrors `corpus/lessons/round-16.md:12-24` (candidate table, decision, evidence and limits).
- Spot-check: not performed. Slot left open; this seat is not a non-author reviewer.

## Touched surfaces

- New: `w1/draft-lesson-gate.md`, `w1/DraftLessonGate.md`.
- Read only: kaidoku `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/round-16*.md`, `.ufo/waves/round-16/verification.json` (via `git show b563c79:`), `.ufo/waves/round-17/{claims,contract}`, pilot logs, Base-src.zip members (extracted to a temp dir and removed).
- Temp files outside the repo: `/tmp/kr17-insp-{shfmt,esb}.{json,err}` (inspect outputs; removable).
- Tools: `npx -y rea-agents@6.5.0 inspect-go-binary` on both carriers (allowed by contract; read-only). No analyze, search, decompile, Ghidra, or carrier execution. No installs or updates by this seat. `sha256sum`, `unzip`, `git show`, `pacman -Qo` (read-only).

## Findings — calibration (C1)

1. **Sweep undercounts (observation).** `contract.md:93` regex misses `LOG.md:2012` (“Producer/fixture hashes remain unchanged across execution”). Regex hits at `b563c79`: `corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`. So the `N→0` metric as written is incomplete (expected N ≥ 3).
2. **Route claim about SCORECARD not located (observation).** `round-16-verifier-spotcheck.md:183` says “LOG and scorecard say pins stayed unchanged during execution.” At `b563c79` `SCORECARD.md` has no pins-temporal statement under the wordings searched (`during execution`, `across execution`, `pins … unchanged`). LOG has one (line 2012). Route claim partly unverified.
3. **Correction must be appended, not edited (observation + constraint).** `contract.md:120-122` requires pre-existing `.ufo/waves/**` blobs and LOG prefix to stay byte-identical, so the correction goes in `corpus/lessons/round-17.md` naming the paths. L1 must append the `LOG.md` correction itself.
4. **SKILL row 448 is an unexercised variant (observation).** `SKILL.md:448` uses relative `python3 … --root .` without `-I` and without `--strict`. The exercised `citation-strict` argv (`round-16/verification.json` lines 317-334) uses `-I`, absolute paths and `--strict`. Row text says `--strict` restores the gate map (inference: the advertised default does not reproduce the exercised verdict; not run).
5. **QUALITY #19 is provenance only (inference, from `corpus/QUALITY.md:26`).** #18 already requires that recheck guidance match the exercised argv. R16-INVOCATION was a miss in applying #18, not a missing criterion, so a second invocation row would be duplicative. R16-PROVENANCE (no pre/post records) is not covered by #18, so #19 is admitted for that alone.
6. **Blanket “unexercised” relabel rejected for row 448.** It would turn `M→0` by labelling the very row the route asked to repair. Rows 447/449/450 may be labelled only where the audit shows no exercised match (not checked here: `invocation-audit.py` has not run).

## Findings — depth (C2)

7. **Pilot is not evidence for the final claim (observation).** Pilot ran 10:17–10:19 before `claims.json` (10:25). `pilot/README.txt` records no pins. Predictions cannot be frozen after seeing the pilot logs; `[SLOT: S7]` freezes them.
8. **`snapshot_label` cannot falsify fallback (observation + source).** `GoApiSnapshot.java:205` and `:239` store the requested version; `GoRttiMapper.java:179-180` logs it; the fallback signal is only the WARN at `GoApiSnapshot.java:159-160`, which `log-extract` (`contract.md:53-54`) does not capture. Requires a schema addition before the field is admissible.
9. **Carriers exercise 2 of 4 selector statuses (observation).** shfmt → `missing_base` (no `go1.27` JSON in `typeinfo/golang/`). esbuild 1.23.12 → `exact_diff` (`patchverdiffs/go1.23.12.json.diff`). The claimed `go1.20.12` carrier also has its own diff (`go1.20.12.json.diff`), so it is also `exact_diff`. `base_only` and `fallback_diff` have no carrier.
10. **Predicted `untested`/`missing_bootstrap` source anchors (observation).** `GoRttiMapper.java:79` range `1.15-1.25`; `:170-171` `Msg.error` untested; `:356` `isInvalid` branch; `:359` bootstrap message. `GoVerRange.java:83-87` and `GoVer.java:143-149`: patch ignored when `-1`, so `1.25.x` is in range and `1.27.0` is not. `missing_bootstrap ⇔ missing_base` is inference from the branch, not verified across other IOException causes.
11. **Log-capture is incomplete at the tail (observation).** Pilot `shfmt-log/ghidra.log` (125 lines) and `esbuild-0.25.12-log/ghidra.log` (123 lines) stop at the `ReaGhidraBridge` post-script stage. Go diagnostics all precede `REPORT: Analysis succeeded` (shfmt line 119; esbuild line 118), so the Go fields are present in the pilot; post-script output is absent. The capability row needs a completeness check in addition to “capture runs and receipt validates”.
12. **Carrier identities confirmed (observation).** `sha256sum` matches both pilot hashes. `inspect-go-binary` returns `go1.27.0-X:nodwarf5` (shfmt, `ev_f8ef12a8…`) and `go1.23.12` (esbuild, `ev_0cabcc66…`). S003 zip sha256 `f00d29c2…d804` matches `corpus/SOURCES.md:9`.

## Out of scope / not done

- No spot-check, no admissions, no `QUALITY.md`/`LOG.md`/`SCORECARD.md`/`SKILL.md` edits, no commit or push.
- No REA analyze/search/decompile, no Ghidra run, no carrier execution, no pin snapshots (executors own those).
- `temporal-sweep.py`, `invocation-audit.py`, `log-extract.py`, `predict.py`, `compare.py` were not run; their outputs are slots.

## Limits

- Anchors are from `b563c79` working-tree-clean reads; `:356`/`:359` and `GoApiSnapshot.java:108-112` line numbers derived from extracted source excerpts (checked by `cat -n` offsets) and not re-verified against a second copy.
- Predictions are source-model inference (INFERENCE) until `S7` freezes them and `S9` compares them.
- Non-author spot-check is required by `LEARNING.md:42-45` and remains open.

## Handoff to L1

- Append LOG.md correction (`LOG.md:2012`) per `draft-lesson-gate.md` correction text.
- Extend the temporal-sweep regex (`contract.md:93`) to match “remain(s|ed) unchanged across execution” before reporting `N`.
- Add a `Falling back from` field to `log-extract.py` before C2.6 can be admitted.
- Add a completeness check (`Analysis succeeded` or failure line present) to the capability admission.
- Freeze `predictions.json` (sha256 + mtime) before the first final `carrier-run.py` analyze.

Commands for the main agent to run once after landing (not run by this seat): `python3 -I .ufo/waves/round-17/tools/temporal-sweep.py --root … --rev <REV>`, `invocation-audit.py --root … --rev <REV>`, `receipt-validate.py` over `W/runs/*/receipt.json`, `controls.py BEFORE AFTER`.

Cleanup: this seat removed its `/tmp/kr17-insp-*` inspect outputs and the temporary Base-src extraction directory; nothing it created remains outside the two files above.
