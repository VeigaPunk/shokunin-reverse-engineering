# ConnScorecardCapability — measure.py's capability-row predicate vs the retained run receipts

Revision under test: `da64646adcb19c1ede7537b799b8c7d283fe43da` (worktree read-only; all
counts from `git show`/`git cat-file` at that commit). Baseline
`b563c799…`, predictions `271167473d87ef…`.

Axes named: **calibration** (does the declared measurement see the artifact, and does
the declared validator accept it?) and **depth** (does the receipt set actually carry the
log capture the row would claim?). Adjacency: untouched — no gate, registry, or sibling
file was written. No carrier was executed and no REA analyze/search/decompile was run;
no tools installed.

Method: `measure.py` at `da64646`; `tools/receipt-validate.py` on the eight receipts;
16/16 retained log/script digests re-derived from the commit; all 96 `go_lines` line
anchors resolved against the committed logs; strict citation-drift at `da64646`;
placement simulations in a `/tmp` clone of the lane.

## F1 (HIGH, calibration+depth) — the declared validator rejects every receipt its own producer writes

`tools/receipt-validate.py:95-100` classifies a carrier receipt only when
`steps` is a **list**; `tools/carrier-run.py:275,312,331` writes `steps` as a **dict**
keyed by step name (`analyze`, `inspect-go-binary`).

```
$ cd .ufo/waves/round-17 && python3 -I -B tools/receipt-validate.py \
    runs/{calib-esbuild-0.25.12,calib-shfmt,pro-aether,pro-containerd-shim,pro-esbuild-0.21.5,pro-esbuild-0.27.7,pro-notesmd-cli,pro-op}/receipt.json
EXIT=1
{'invalid': 8, 'receipts': 8, 'unreadable': 0, 'valid': 0}      # kind=unknown, code=unrecognized_shape, 8/8
```

The selftest cannot catch this because its fixture emits the list shape
(`receipt-validate.py:470`): `--selftest` → `SELFTEST: CLEAN cases=5`, exit 0.

Consequences at `da64646`: the L1's worktree-only `verify.py:93` (untracked at this
revision) runs `receipt-validate.py <run>/receipt.json`
with `expect=0` for all eight labels, so the round's verification pass will record
eight `exit_as_expected: false`; the knowledge entry's `recheck:` command
(`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) returns red; and
`claims.json` gates the capability row on "its receipt validates".

Smallest fix (3 hunks, verified on a `/tmp` clone at `da64646`):
1. `classify`: `isinstance(receipt.get("steps"), (list, dict))`.
2. `check_required` (`:284`): iterate `steps.items()` when dict, label `where` by step name.
3. `_carrier_receipt` (`:470`): emit `"steps": {"inspect-go-binary": {…}}` so the green
   selftest case matches the producer. Add a dict-shape red case only if the list shape
   must stay supported.

Verified after the fix, same bytes:
```
$ python3 -I -B tools/receipt-validate.py <same eight paths>   → exit 0
{'invalid': 0, 'receipts': 8, 'unreadable': 0, 'valid': 8}     # 336 checks/receipt
$ python3 -I -B tools/receipt-validate.py --selftest           → CLEAN cases=5, exit 0
```

Inference, not observation: the receipts are substantive; the defect is the checker's
shape contract, not the evidence (see no-findings N1–N3).

## F2 (HIGH, calibration) — the predicate's scope and the append-only placement are mutually exclusive

`measure.py:121-130` reads only the delimited `## Capabilities` section
(`split("## Capabilities\n")` → `split("\n## ")`). That section is
`SCORECARD.md:615-625` (`## Saturation` at :626). The capability records added by r13
(`:2131`) and r14 (`:2203`) — the shape the target points at — are **outside** it.

Measured on the committed bytes (same split/regex as `measure.py`):

| placement | `capability_rows_matching` |
|---|---|
| as-is | 0 |
| row appended at EOF in a `## Round 17` section (r14 shape) | **0** — predicate blind |
| row inserted after `SCORECARD.md:622` | 1 |

The in-table insert is not free: in the `/tmp` clone one inserted line turns the strict
gate red with **six** findings, all from line-addressed pointers at `SCORECARD.md:908`
and `:1338`/`:1419`/`:1435`/`:699` shifting by one, plus
`readme175-sc1217` (`corpus/README.md:175` cites `SCORECARD.md:1216`):
`CITATION_DRIFT_VERDICT: failed findings=6 exit=1` (strict baseline at `da64646` is
`clean findings=0 exit=0`).

Synthesis (verified): keep the append-only placement and scan the whole SCORECARD for
rows, preserving the structural anchor —

```python
    try:
        scorecard.split("## Capabilities\n", 1)[1]
    except IndexError:
        fail("SCORECARD.md has no delimited '## Capabilities' section")
    capability_rows = [
        line for line in scorecard.splitlines()
        if line.startswith("|") and CAPABILITY_TEXT in line
    ]
```

Measured in the clone with that one change and the EOF-placed row committed:
`C2_scorecard_capability_row: 1`, `scorecard_capability_rows_matching: 1`;
`measure.py --selftest` → `CLEAN cases=22`; strict citation gate → `clean findings=0
exit=0`. Under the **unpatched** predicate the same commit reads 0, i.e. the placement,
not the artifact, decides the observable. Before-values are unchanged by the patch
(`b563c79`, `2711674`, `da64646` all read 0/0), so 0→1 is not outcome-shopping.

Required addition: the current selftest seeds the row in-section, so it does not
discriminate the appended form (still 22 cases clean). Add one fixture case with the row
only in an appended `### Capability addition` table and assert `== 1`; that is the only
control that would catch a regression of this predicate.

Also restate the claim's delta honestly: `claims.json` says "capability rows 4
(+r13/r14 appended) -> +1". The proxy that moves is the phrase-presence boolean
`0→1` (matching rows `0→1`). Counting all capability records is `6→7` (canonical 4 +
r13 `:2131` + r14 `:2203`), a different number from the same round; do not print both
as one delta.

## F3 (MED, depth) — the row's evidence pointer must not cite a passing validator at `da64646`

Until F1 lands, no command in the lane validates these receipts. What does verify today
(commands run, outputs observed):

- `git cat-file -p da64646:<log>` sha256 == `receipt.retained_logs[].files[*].sha256`
  for all **16/16** files (8 `ghidra.log` + 8 `script.log`), sizes equal too.
- `observation.json.log_sha256` == the receipt's `ghidra.log` digest and `log_bytes` ==
  `bytes`, for all 8 — extraction and retained copy are the same bytes.
- all **96/96** `go_lines[].line` anchors resolve to the committed `ghidra.log` line
  with identical text (trailing-space identity not tested; the comparison rstripped).
- 8/8 receipts: exactly one bound session, `unbound_sessions: []`,
  `binding.logfile_ok: true`, `binding.target_ok: true`; the binding strings are
  derived from the log itself (`carrier-run.py:136-137`), e.g.
  `pro-op/logs/rea-ghidra-yRmWqx/ghidra.log:2` `Using log file: …/ghidra.log` and
  `:46` `IMPORTING: file://…/target-f4ac474fd020.bin`.

## F4 (LOW, calibration) — run-log covers 7 of 8 runs

`runs/run-log.txt:1` starts at `calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00`;
`calib-shfmt` is absent, although its receipt records
`steps.analyze.started_at_utc = 2026-10-20T13:47:06Z` and it is the first label in
`predictions/carriers.tsv:1`. No evidence is lost (receipts carry start/end), but any
"eight sequential runs logged" wording overstates the log. Smallest fix: state the log's
coverage (7/8) and cite receipt timestamps as authoritative. Worktree `run-carriers.sh`
is modified (`RUNS_DIR` support) relative to `da64646`; cite committed blobs only.

## F5 (LOW, calibration) — "no mid-run check differed" is a recorded negative only in the weak sense

`carrier-run.py:35,425-433` performs a throttled pin snapshot every 30 s and writes
`pins_changed_during_run` only on mismatch. No receipt contains that key (grep: absent
in all 8) and no receipt records the check count. So the knowledge entry's
"no mid-run check differed" is supported by absence of a mismatch key, not by a logged
count or explicit `equal` result. Smallest fix (wording): "no mid-run check recorded a
difference; the check itself is not logged". Recording `mid_checks`/`mid_equal` in the
step would be the durable fix.

## F6 (LOW, depth) — capture completeness has a real boundary; every run reaches the analysis-success line

Tail census of the eight retained logs (observed): every one contains
`INFO (HeadlessAnalyzer) REPORT: Analysis succeeded for file: …`
(lines 98–276 across the eight), and every file's last line is
`ANALYZING changes made by post scripts: …`. So the Go diagnostics are complete for the
analysis phase, but the post-script tail is not captured in any run. That is consistent
with `log_capture_limit` (identical string in 8/8 receipts: "polling copy; lines written
after the final poll before REA deletes its runtime root can be missing") and must be in
the Limits paragraph. Not a defect — a limit that the draft row must not elide.

## Bounded no-finding checks

- N1 digest binding: 16/16 retained files match the committed blobs (no finding).
- N2 extraction identity: `observation.log_sha256/bytes` == receipt (8/8) (no finding).
- N3 line anchors: 96/96 `go_lines` resolve to the committed log text (no finding).
- N4 binding: 1 bound / 0 unbound / both flags true (8/8) (no finding).
- N5 strict citation-drift at `da64646`: `clean findings=0 exit=0` (no finding).
- N6 `measure.py` at `da64646` runs exit 0; `run_receipts: 8`,
  `run_receipt_paths` lists exactly the eight; map 95/95, missing/dangling empty
  (no finding).

## Proposed capability row (exact text; one physical line)

```markdown
| retained REA Ghidra-session log capture | copies the new `rea-ghidra-*` session's `ghidra.log`/`script.log` every 0.5 s from a private `TMPDIR` before REA's close deletes them, and admits a copy only when the log's own `Using log file:` and `IMPORTING: … target-<carrier sha256[:12]>.bin` lines bind it to the run; eight REA 6.5.0 analyze runs (3 untested/missing-bootstrap 1.26.8–1.27.2, 1 no-build-info with `unable to get GoRttiMapper`, 2 `Falling back` 1.25.x→1.25.0, 2 exact snapshots 1.20.12/1.23.12) yield line-anchored Go diagnostics for field-by-field comparison with predictions frozen before the run; every retained log reaches `REPORT: Analysis succeeded` | `.ufo/waves/round-17/runs/{calib-shfmt,calib-esbuild-0.25.12,pro-notesmd-cli,pro-aether,pro-esbuild-0.21.5,pro-containerd-shim,pro-esbuild-0.27.7,pro-op}/receipt.json`; `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py` on those eight → `valid: 8, invalid: 0`, exit 0; each `observation.json.log_sha256` equals its receipt's `ghidra.log` digest | round-17 |
```

Limits paragraph (place directly under the table, r14 shape at
`SCORECARD.md:2209-2212`):

```markdown
Limits: a polling copy, not a complete session record — `log_capture_limit` is identical
in all eight receipts: lines written after the final 0.5 s poll and before REA deletes
`/tmp/kr17-rea-*/rea-ghidra-*` can be missing. Every retained log stops at
`ANALYZING changes made by post scripts`; `REPORT: Analysis succeeded` and all Go
diagnostic lines precede it, so those fields are complete here, but the post-script tail
is not captured and no run proves it complete. A retained log is static-analysis output
from a copy imported into Ghidra headless — no carrier was executed. Mid-run pin checks
run every 30 s but neither their count nor a negative result is recorded; only a
mismatch would appear (`pins_changed_during_run`), and pre/post equality is
same-bytes-at-two-instants, not continuity. Capture proves which route the provider
logged, not that the selected snapshot data is correct, not a 1.26/1.27 recovery, and
not the cause of the unpredicted pro-aether `EOFException`. Validation recomputes the
recorded digests against the bytes present now; it cannot prove during-run integrity.
```

Preconditions for entering the row:
1. F1's three hunks land first (otherwise the cited command exits 1, not 0) — verified on
   a `/tmp` clone at `da64646`.
2. F2's predicate change lands in the same commit — the predicate change is verified
   above; the appended-form selftest case named above is **not yet written** and must
   accompany it. The row is appended at EOF under a `## Round 17` section; the row
   string itself must keep the substring `retained REA Ghidra-session log` verbatim
   (`measure.py:46`). Do not put the phrase in a second table row (e.g. a `| Limits |`
   row): `scorecard_capability_rows_matching` would read 2 and the +1 control would fail.

## Risks / second-order effects

- F1 changes a checker after the evidence was produced; the change only broadens shape
  acceptance, and a tampered-file/dict-shape red case should be kept so it still fails.
- F2 changes a measurement tool mid-round. Mitigation: before-values recomputed with the
  patched tool at `b563c79`, `2711674`, `da64646` all remain 0, and the selftest gains a
  discriminating case; print both the boolean and the matching-row count so a duplicated
  row is visible.
- Adjacency: the in-table alternative was measured and rejected (6 strict findings,
  including a pointer owned by `.ufo/gates/c1-census-v10.py:33`); do not repair it by
  editing the gate's pointer table.
- Axis harm check: calibration improves (declared instrument sees the declared artifact;
  validator stops rejecting its producer); depth improves (96 anchored log lines, 16/16
  digest bindings, one unpredicted in-range failure retained); runtime/contract unchanged.

## Verification for integration

(The eight-argument form uses brace expansion, so run it under `bash`; the harness shell
here is not bash and will pass the braces literally.)

```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py \
  .ufo/waves/round-17/runs/{calib-shfmt,calib-esbuild-0.25.12,pro-notesmd-cli,pro-aether,pro-esbuild-0.21.5,pro-containerd-shim,pro-esbuild-0.27.7,pro-op}/receipt.json
python3 -I -B .ufo/waves/round-17/measure.py <post-integration-rev>   # expect capability 1, receipts 8
python3 -I .ufo/gates/citation-drift/citation-drift-probe.py --root <lane> --rev <rev> \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json --strict        # expect clean 0
```

No installs were performed. Scratch work stayed under `/tmp` (`/tmp/r17-sim`, removed by
the reader if desired); no lane file other than this report was written.
