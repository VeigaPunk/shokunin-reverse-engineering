# t1250-go — C3 outcome from the raw log (round-19 wave 2)

Seat: KaidokuR19.OutcomeGo-3. Date 2026-10-20. Read-only; no REA analyze, no carrier
execution, no installs. LANE = /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
LANE `refs/heads/main` observed at `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`
(`git --no-optional-locks rev-parse refs/heads/main`, exit 0); baseline B
`8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; predictions frozen at `a1140e7`.

Subject: `runs/t1250-go/logs/rea-ghidra-AiWB8A/ghidra.log` (576 lines, 88010 bytes,
sha256 `ebb305d61ad7c0e9616b8da8c472468bb06b6e5f78bbb9e28b7295e6dcaa3676`;
same bytes as the Git blob at tip, `git cat-file blob ... | sha256sum`, exit 0).
Carrier `/home/vgpnk/.local/opt/go-1.25.0/bin/go`, sha256
`b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25`, 14939693 bytes
(`sha256sum`/`stat`, exit 0) == prediction `carrier.sha256`
(`predictions/t1250-go.prediction.json:32-35`) == receipt `carrier.sha256_pre`/`_post`.

## Commands (all pasted results are exit codes of the shown command)

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python3 -I -B .ufo/waves/round-17/tools/log-extract.py --selftest` | 0 | `SELFTEST: CLEAN cases=13` |
| 2 | `python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log runs/t1250-go/logs/rea-ghidra-AiWB8A/ghidra.log` | 0 | reparse of the raw log |
| 3 | same reparse diffed against `runs/t1250-go/observation.json` (19 fields) | 0 | `field_diffs_vs_retained_observation: NONE` |
| 4 | `python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction predictions/t1250-go.prediction.json --observation runs/t1250-go/observation.json` | 0 | `all_match: True`, 8/8 fields, mismatches `[]` |
| 5 | `sha256sum -c predictions/SHA256SUMS` (cwd W19) | 0 | all 19 entries OK |
| 6 | `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest` | 0 | `SELFTEST: CLEAN cases=21` |
| 7 | `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps runs/t1250-go/receipt.json` | **1** | 2 findings, validator self-pin only (see Binding) |
| 8 | independent pin recompute over all 152 `pins_post` entries (Python, sha256/size) | 0 | 1 mismatch: the validator itself |
| 9 | `grep -ic` failure tokens on the raw log (loop; grep exits 1 per zero-count pattern) | 0 | counts below |

Parser bytes used in #2 are the run-time bytes: live
`.ufo/waves/round-17/tools/log-extract.py` = `eb8f2c785886…`, the value pinned in the
receipt; `compare.py` `582a77f3df75…` and `pins.py` `9e9c72507de4…` also unchanged.

## Observed facts (raw log; observation, not inference)

Level histogram over the 68 timestamped records: INFO 53, DEBUG 11, **WARN 4, ERROR 0**;
first record 15:57:53, last 15:59:59. Case-insensitive token counts on the raw bytes:

| token | count |
|---|---|
| `Invalid index` | 0 |
| `Unable to read past EOF` | 0 |
| `Go analysis failure` | 0 |
| `Falling back` | 0 |
| `Missing Go bootstrap` | 0 |
| `Untested Go version` | 0 |
| `Analysis succeeded` | 1 |
| `Failed to get subtype` | 4 |

Route and identity, with line anchors in the raw log:

- `:46` `IMPORTING: file:///tmp/kr17-rea-7b8hb9ib/rea-ghidra-AiWB8A/target-b93cdfdbc72f.bin`
  (target stem = carrier sha256 prefix).
- `:48` `Using Language/Compiler: x86:LE:64:default:golang`.
- `:517` `INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0` (INFO form, no
  `version`; this component alone decides the route).
- `:518` `INFO (GoRttiMapper) Using Go API snapshot for version 1.25.0` (request echo).
- `:519-520` `Discovered 242 unindexed Go types`, `Found 7259 Go types`.
- `:521` `GolangSymbolAnalyzer) Go version 1.25.0`.
- `:522-525` the only four WARNs, all `GoTypeManager) Failed to get subtype '…' in *…'`
  (`runtime.elfSym`, `byte`, `uint16`, `time.Ticker`). Not read failures: the analysis
  continues and reports success.
- `:526-536` analyzer completions (NoReturn 4, 3112 snapshot signatures, 5832 method
  signatures, RTTI 9428/9172/40, closures 209/33, strings 7485) and
  `:536 Go missing type names: 34` (INFO).
- `:570` `REPORT: Analysis succeeded for file: …target-b93cdfdbc72f.bin`.
- `:576` last record: `ANALYZING changes made by post scripts` (log capture is a
  polling copy; see limits).

Control for the failure token (observation): the known H1-failing round-18 carrier
`runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log` has
`:408 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: …` and
`:451 Caused by: java.io.EOFException: Invalid index: 22386945`. Four round-17/18 logs
contain that text; `Failed to get subtype` occurs in **12** round-18 logs including the
silent `noswiss` controls, so the four WARNs above are not analysis failures.

## Frozen prediction vs raw-log observation

Prediction `predictions/t1250-go.prediction.json` (fields at `:21-46`); comparison is
made directly against the raw log, not `compare.json`, then cross-checked with the
retained `observation.json` (identical on all 19 extractor fields, command #3).

| field | predicted | observed (raw log) | match |
|---|---|---|---|
| `expected.snapshot_route` | `info` (`:40`) | `:517` GoApiSnapshot INFO, 0 fallbacks → `info` | yes |
| `expected.snapshot_label` | `1.25.0` (`:39`) | `:517`/`:518` `1.25.0` (request echo; non-discriminating) | yes |
| `expected.untested_version` | `null` | 0 `Untested Go version` records (1.25 is inside `1.15-1.25`) | yes |
| `expected.fallback_to` | `null` | 0 `Falling back` records | yes |
| `expected.missing_bootstrap` | `false` | 0 `Missing Go bootstrap` records | yes |
| `extra.analyzer_errors_empty` | `true` | 0 ERROR records overall | yes |
| `extra.eof_reads` | `[]` | 0 past-EOF reads | yes |
| `extra.invalid_index_reads` | `[]` | 0 `Invalid index` records | yes |
| `c3.h1_kind` | `none` (`:25`) | no Go analysis failure → none | yes |
| `c3.misread_map_types` | `12` (`:28`) | not observable in a silent log | n/a |

**Exact match, 0 mismatches.** `compare.py` reproduces `all_match: True` (exit 0), and
the frozen compare's `all_match` is therefore not a compare-only artifact.

## Does the frozen mechanism rule hold for this label?

Frozen rule (`predictions/decision-rule.json`): `confirmed` (`:5`) needs every D-label
(D = `t1250-vet`, `:7`) to report a Go analysis failure carrying an H1-only index and
every non-D label to show **no** Go analysis failure. `t1250-go`'s table row is
`{"d": false, "h1": "none", "invalid_index_reads_h1": [], "invalid_index_reads_h0_incl_walk":
[], "eof_reads_h1": [], "label": "t1250-go", "route": "info"}` (`:30-40`) and the
emulator prescan has `predicted_failure_h1 = predicted_failure_h0 = false`,
`predicted_failure_kind = none` (`evidence/prescan/kr19-sm-go.json`).

- **Holds, as written, for this label (observation + rule application):** the label is
  non-D and shows no Go analysis failure, so its half of the `confirmed` conjunction is
  satisfied; nothing here triggers `refuted` or `unresolved`.
  INFERENCE: the cohort verdict still depends on `t1250-vet`, outside this slice.
- **Discriminating power is nil at this label.** The prediction for a non-D label is
  silence, and silence is equally consistent with (a) the 12 Swiss/OldMapType misreads
  existing but never reaching a read that faults, and (b) the map path not being
  exercised. The frozen fields cannot distinguish these; only the D label can.
  INFERENCE: `t1250-go` is a negative control, not evidence for H1.
- **Walk-channel sub-prediction did not materialise.** The prescan's full markup walk
  predicts failure under *both* hypotheses (`walk.failed.h0 = walk.failed.h1 = true`,
  kind `unmapped`, index 8, length 48, `type@0xab49e0` path), yet the log contains no
  failed read at all. This is not a scored mismatch: the emulator excludes the walk from
  the boolean by construction (`round-18/tools/swiss-misread.py:1461-1464` comment;
  `:1469-1478` computes `predicted_failure_kind` with `walk=None`), and the frozen
  H1/H0 index lists carry only `invalid_index`/EOF kinds. The same pattern is on record:
  round-18 `calib-notesmd-cli` had `predH1=false`, `walkH1=unmapped/8`, and no log
  failure; `real-kimi-webbridge` had the same walk with a logged failure. Round-18
  lessons already disclose "walk-channel merge and false positives disclosed"
  (`corpus/lessons/round-18.md:80`). INFERENCE: known approximation, not evidence
  against the map-path hypothesis.
- **Silence is not clean recovery.** `:536` reports 34 missing type names (round-18
  silent carriers report 2-11) on top of 242 unindexed types. INFERENCE: the non-D test
  scores absence of a *read fault*, not binding correctness; "match" here should not be
  read as a recovery-quality result.

## Binding/freshness finding: the gate is not replay-stable at tip

This is independent of the log content and affects how the C3 count may be audited.

- At run time the gate passed: retained
  `evidence/receipt-validation/t1250-go.json` records `exit: 0` (`:8`), `valid: 1`
  (`:6`), `findings: []` (`:14`), 384 checks, `require_mid_maps: true`.
  Receipt `pins_pre`/`pins_post` (`runs/t1250-go/receipt.json:1869-1872`,
  `:1103-1106`) pin the validator at `70672eb3… / 46047` bytes — the B and `a1140e7`
  blob (`git cat-file blob`, exit 0) — and `pins_compare.equal = true` with
  `mid_run_drift_steps = []` and 5 mid-map snapshots.
- Re-running the frozen gate now exits **1** for `t1250-go` and for all eight
  `t1250-*` receipts: exactly 2 findings each, `sha256_mismatch` + `size_mismatch`, both
  on `.ufo/waves/round-17/tools/receipt-validate.py` — the validator's own pinned bytes.
  The tip blob is `9276b198… / 51075` (commit `4f6c73f`, committed 16:09:17), and the
  live worktree file is `6afb7ef6… / 52682` (uncommitted `M`, mtime 16:19:33; observed
  at 19:22Z). `decision-rule.json:3` literally requires
  `receipt-validate.py --require-mid-maps` to "exit 0 on its receipt"; at tip it does not.
- The independent recompute (command #8) shows exactly **1 of 152** pinned entries
  changed — the validator. Carrier, retained log, mid maps, `compare.py`,
  `log-extract.py`, `pins.py`, `carrier-run.py` and the `swiss-misread.py` pin all still
  match their run-time bytes.
- This is anticipated by the L1's verifier, not by the frozen rule:
  `verify.py:106-110` declares `"receipt-validate-": 1` as expected red ("Live receipts
  correctly detect the forward-edited producer validator"), `verify.py:563-580` invokes
  every live receipt expecting exit 1, and `verify.py:668-681` requires exactly these
  two findings on the validator path while requiring the retained run-time evidence to
  be `{valid: 1}`.
  INFERENCE: the operational reading is "run-time validation, retained at 19:00Z"; the
  frozen gate text should say so. A literal tip-time audit makes all eight labels
  unbound and C3 `unresolved` for a tool-repair reason, even though no run data drifted.

## Remaining unknowns / limits

- Log capture is a polling copy (`receipt.json log_capture_limit`): lines written after
  the last poll before REA deletes its runtime root can be missing. The Go analysis and
  its summary (`:521-:570`) precede the last captured record (`:576`), so the absence of
  a failure is credible, but the post-script tail is not fully retained.
- The 12-misread count is state of the emulator, not something a silent run can confirm;
  no claim is made here that the misreads occurred at runtime.
- `t1250-vet` (the only D label) and the cohort verdict are outside this slice.
- No mutation tests were needed or run; no clone was created; no production edits; no
  tool installs or upgrades.
