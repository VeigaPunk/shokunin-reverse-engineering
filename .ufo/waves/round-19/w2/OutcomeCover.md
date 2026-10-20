# Outcome cover — C3 raw-log audit of t1250-cover

Seat: KaidokuR19.OutcomeCover-3 (wave 2, read-only scout). No delegation, no production
edits, no REA/MCP device, no REA `analyze`/`search`/`decompile`, no Ghidra run, no carrier
execution, no installs. Scratch only under `/tmp/kr19-w2-oc-*` (validator copy) and
`/tmp/kr19-w2-oc-*.json` (outputs).

- Lane (read-only): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Observed main tip: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`, exit 0).
- Contract baseline B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; C3 freeze commit
  `a1140e76fffdc1be032d9d813dbb686157803bbc` (parent of `4f6c73f`, ancestor of the tip).
- Label under test: `t1250-cover`; carrier
  `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cover`.
- Raw log: `.ufo/waves/round-19/runs/t1250-cover/logs/rea-ghidra-XVD7qp/ghidra.log`.

## Verdict (short)

- **Prediction match: exact, 8/8 fields**, parsed from the raw `ghidra.log` without using
  `compare.json` [OBSERVATION]. Route `info` at `1.25.0`; no Go analysis failure, no
  `Invalid index`, no EOF read, no fallback, no bootstrap miss, no `Untested Go version`.
- **Frozen mechanism rule for this label (non-D, predicted silent): holds** on the bound log
  [OBSERVATION]. The cohort direction also holds on raw logs: only `t1250-vet` reports
  `Go analysis failure`, with `Invalid index: 13902080` (in the frozen H1-only set), and no
  other label reports one [OBSERVATION].
- **Frozen decision-rule binding gate is red at the delivered revision for cover — and for
  all eight labels — solely on `receipt-validate.py`'s own bytes** [OBSERVATION]. The receipt
  pins the validator at `70672eb3…`/46047 B (the blob at the freeze commit); the lane now
  holds `9276b198…`/51075 B (the blob at `4f6c73f`, the C1 wave-one integration that added
  the R18-MIDMAP-LISTSTEP fix). Every receipt reports exactly two findings
  (`sha256_mismatch`, `size_mismatch`) on that one path; carrier, log and mid-map checks pass.
- **Consequence for the frozen rule as written** (`predictions/decision-rule.json:3`): at the
  tip, zero labels are "bound", so C3's `0 -> 8` count is 0 under the literal gate at the
  delivered revision and 8 only under the run-time validation recorded at revision `a1140e7`.
  The L1's `.ufo/waves/round-19/verify.py:110,569,669-683`
  already substitutes `expected exit 1 + drift-only content` for that gate plus the retained
  freeze-time green; **the frozen rule text was never amended to say so**
  (`claims.json:36` amendment does not mention it). Report the label as
  *match with a declared binding-drift exception*, or as *unresolved (unbound log)* under the
  literal text — the two cannot both stand without an append-only amendment.
- **Calibration/depth findings, cover-scoped:** (1) "silent" is not literal silence — the log
  carries three `GoTypeManager` subtype WARNs (`ghidra.log:197-199`) that no prediction field
  enumerates, and the same three strings appear in 7/7 silent labels and in 0/1 failing label;
  (2) adjacent, for `OutcomeCompile`: `t1250-compile` has a Go-analyzer `ERROR` on
  `AnalysisTaskWrapper` (`ghidra.log:347`) that neither the frozen `Go analysis failure`
  predicate nor the extractor's `analyzer_errors` rule (`log-extract.py:244`, component
  prefix `Golang`) can see, so the non-D "silent" predicate is extractor-defined rather than
  "no Go-related error". That label's verdict belongs to its own seat.

## 1. Binding of the raw log to the frozen prediction

```
$ sha256sum runs/t1250-cover/logs/rea-ghidra-XVD7qp/ghidra.log
630a40d4d5d45258cfa45c4720672dc671c088106cecaa5fdbcfe221427df5ad; exit=0
$ md5sum  /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cover
4b81886d22d4bbb7cc47fc6605d9601b; exit=0
$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cover
64686d22f3b4055386bbcbf0aeac54249cdbff771ffd7b54c8d4abd330df8166; exit=0
$ sha256sum -c predictions/SHA256SUMS
… t1250-cover.prediction.json: OK …; exit=0
$ git rev-parse a1140e7:.ufo/waves/round-19/predictions/t1250-cover.prediction.json
6fb22f4d17a313ce83cd9a341280e547bdbb683c   # exit=0
$ git rev-parse refs/heads/main:.ufo/waves/round-19/predictions/t1250-cover.prediction.json
6fb22f4d17a313ce83cd9a341280e547bdbb683c   # exit=0 (blob unchanged since freeze)
```

[OBSERVATION] Chain, all four links exact:

1. Log bytes `31862` (`wc -l -c`: 250 lines) equal `receipt.json.retained_logs[0].files.ghidra.log.bytes`
   and `observation.json.log_bytes`; digest equals `observation.json.log_sha256` and the
   receipt's retained-log digest.
2. The log names the carrier itself: `ghidra.log:46` imports
   `target-64686d22f3b4.bin` (first 12 hex of the prediction sha256) and `ghidra.log:59`
   loads `…?MD5=4b81886d22d4bbb7cc47fc6605d9601b`, equal to the carrier's md5.
3. `receipt.json.carrier.sha256_pre == sha256_post == 64686d22…`, equal to
   `predictions/t1250-cover.prediction.json.carrier.sha256`.
4. `receipt.json.retained_logs[0].binding == {logfile_ok: true, md5_ok: true, target_ok: true}`;
   `bound_sessions` holds the session dir, `unbound_sessions` is empty; mid-run pins
   `pins/mid-1.json` / `mid-2.json` (152 entries each) were taken at 19:05:07Z and 19:05:37Z
   inside the run window 19:05:06–19:05:50Z and are `equal` to `pins_pre` with no changes.

The `log_capture_limit` field ("polling copy; lines written after the final poll … can be
missing") bounds completeness: the last line is `ghidra.log:250` at 16:05:49 local and the
last copy at 19:05:49.71Z, ≤0.5 s before the step end. The Go phase and
`REPORT: Analysis succeeded` (`ghidra.log:244`) are fully inside the retained bytes, so the
four signals are unaffected; the same truncated tail shape occurs in all eight logs (each
ends at `ANALYZING changes made by post scripts`), so it is harness-wide, not label-specific
[OBSERVATION + bounded INFERENCE].

## 2. The four assigned signals in the raw log

Prediction fields are from `predictions/t1250-cover.prediction.json`; exits are from this seat's
greps, not from `compare.json`.

| Signal | Frozen prediction | Raw log | Exit |
|---|---|---|---|
| Go analysis failure | `c3.h1_kind=none`, `h0_map_path_failure=false`, `h1_map_path_failure=false`, `extra.analyzer_errors_empty=true` | no `Go analysis failure`; **zero** `ERROR` lines in 250; `Analysis succeeded` at `:244` | `grep 'Go analysis failure'` = 1; `grep 'ERROR'` = 1 |
| Invalid index | `extra.invalid_index_reads=[]`; `c3.h0_reads_including_walk.invalid_index=[]` | no `Invalid index` token | `grep 'Invalid index'` = 1 |
| EOF read | `extra.eof_reads=[]` | no `EOF`, no `EOFException`, no "end of file" | `grep 'EOF'` = 1; `grep -i 'end of file'` = 1 |
| GoApiSnapshot route | `expected.snapshot_route=info`; `snapshot_label=1.25.0`; `fallback_to=null`; `missing_bootstrap=false`; `untested_version=null` | `:192 INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0`; `:193 INFO (GoRttiMapper) Using Go API snapshot for version 1.25.0`; no fallback/bootstrap/Untested text | found at `:192` (grep exit 0); fallback/bootstrap/Untested absent (grep exit 1 each) |

Exact commands and exits (log `L=runs/t1250-cover/logs/rea-ghidra-XVD7qp/ghidra.log`):

```
$ grep -n 'Invalid index' "$L"        # exit=1
$ grep -n 'EOF' "$L"                  # exit=1
$ grep -in 'end of file' "$L"         # exit=1
$ grep -n 'Go analysis failure' "$L"  # exit=1
$ grep -n 'Exception' "$L"            # exit=1
$ grep -n 'Analysis succeeded' "$L"   # exit=0 -> :244
$ grep -n 'GoApiSnapshot' "$L"        # exit=0 -> :192
$ grep -n 'Untested' "$L"             # exit=1
$ grep -in 'fallback' "$L"            # exit=1
$ grep -in 'bootstrap' "$L"           # exit=1
$ grep -n 'ERROR' "$L"                # exit=1 (no lines)
$ grep -n 'WARN' "$L"                 # exit=0 -> :197-199 only
```

Parse trap recorded: `grep -in 'invalid'` **does** hit `ghidra.log:60` —
`Skipping section [.gosymtab] with invalid size 0x0` (import "Additional info", exit 0). Only
the exact token `Invalid index` (the `EOFException` formatter) is the H1 signal; a
case-insensitive substring search would fabricate a hit.

## 3. Exact match computation

| Field (prediction path) | Predicted | Observed from raw log | Match |
|---|---|---|---|
| `expected.snapshot_label` | `1.25.0` | `:192`, `:193` (INFO) | yes (non-discriminating: request echo, per prediction `basis` GoApiSnapshot.java:111,122-126) |
| `expected.snapshot_route` | `info` | `:192 INFO (GoApiSnapshot)`; no WARN, no fallback | yes |
| `expected.fallback_to` | `null` | no fallback line | yes |
| `expected.missing_bootstrap` | `false` | no bootstrap line; `bootstrap_attempts=1` (the `Reading Go binary info` line, `:191`) | yes |
| `expected.untested_version` | `null` | no `Untested Go version` | yes |
| `extra.analyzer_errors_empty` | `true` | zero `ERROR` lines | yes |
| `extra.eof_reads` | `[]` | no EOF read | yes |
| `extra.invalid_index_reads` | `[]` | no `Invalid index` | yes |

**8/8 exact.** Cross-check only (not the basis): `runs/t1250-cover/compare.exit` = `0`,
`compare.json.all_match=true`, all eight fields `match`; `observation.json` independently
reports `snapshot_route=info`, `snapshot_labels=["1.25.0"]`, `snapshot_fallbacks=[]`,
`analyzer_errors=[]`, `symbol_analysis_failures=[]`, `invalid_index_reads=[]`, `eof_reads=[]`,
`classification=snapshot_loaded`. This seat's raw-log parse agrees with all of them.

## 4. Frozen mechanism rule: cover, cohort, and the binding clause

Rule text (`predictions/decision-rule.json:3,5,28`): a label counts only if
`receipt-validate.py --require-mid-maps` exits 0 on its receipt, the log's carrier sha256 equals
the prediction's, and the prediction blob is unchanged; `confirmed` needs every D label's log to
report a Go analysis failure with an H1-only `Invalid index` and no outside index, and every
non-D label to show no Go analysis failure; `refuted` on a non-D failure.

- **Cover (non-D): mechanism holds.** No `Go analysis failure`; no Invalid index/EOF; route
  info. The emulator's own walk failure for cover (`walk.failed.h0=h1=true`, index 8
  "unmapped") is predicted under both hypotheses and is deliberately outside the map-path
  boolean rule (`H0H1Semantics.md`); it does not appear in the log as an `Invalid index`
  [OBSERVATION + the rule's own definition].
- **Cohort direction (needed by the rule's global clause): holds on raw logs** [OBSERVATION].
  `grep -c 'Go analysis failure'` = 1 for `t1250-vet`, 0 for the other seven. Vet's only
  `Invalid index` is `13902080` (`t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:229`), inside
  `h1_only_invalid_indexes.t1250-vet = [13902080, 852107777]`; `852107777` and the walk value
  `1801722468838924630` occur **0** times there. Cover's log contains none of the three.
- **Binding clause: red at the tip, cover and all seven siblings.** Current tool:

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-*/receipt.json; echo $?
{"counts": {"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}, ...}; exit=1
# per receipt: exactly 2 findings, codes {sha256_mismatch, size_mismatch},
# path /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py
# expected 70672eb3bd0c... / 46047 B   actual 9276b1984cd5... / 51075 B
```

  Causes and timeline, all read from git objects:

```
$ git show -s --format='%h %ci %s' a1140e7 4f6c73f d0690fd
a1140e7 2026-10-20 15:57:44 -0300 round-19: frozen C3 predictions ...
4f6c73f 2026-10-20 16:09:17 -0300 round-19: wave-one integration, routed fixes ...
d0690fd 2026-10-20 16:15:31 -0300 round-19: wave-two assignment records ...
$ git merge-base --is-ancestor 4f6c73f a1140e7; echo $?   # 1 (predates it in time, not ancestry)
$ git merge-base --is-ancestor a1140e7 d0690fd; echo $?   # 0
$ git cat-file -p a1140e7:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145
$ git cat-file -p refs/heads/main:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum
9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45
$ sha256sum .ufo/waves/round-17/tools/receipt-validate.py
9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45
```

  The runs happened 16:05:06–16:07:06 local (receipt timestamps; `producer.json.branch_tip`
  `a1140e7…`, `recorded_at_utc` 19:05:06Z), i.e. after the freeze and **before** `4f6c73f`
  (16:09:17) rewrote the validator (+102/−8, the R18-MIDMAP-LISTSTEP fix visible in its new
  `mid_checks_absent` doc/selftest). All eight receipts pin `70672eb3…`/46047 B in both
  `pins_pre` and `pins_post`; the freeze-time validation is retained green:
  `evidence/receipt-validation/t1250-cover.json` = `{"counts": {"invalid": 0, …, "valid": 1},
  "exit": 0, "require_mid_maps": true}` with `checks_performed: 366`.

  This is **not** a tool-version artifact: running the freeze-pinned validator blob from a
  scratch dir still exits 1, because the tool re-hashes the *live lane path* the receipt
  commits to:

```
$ T=$(mktemp -d); git cat-file -p a1140e7:.ufo/waves/round-17/tools/receipt-validate.py > $T/receipt-validate.py
$ git cat-file -p a1140e7:.ufo/waves/round-17/tools/pins.py > $T/pins.py
$ python3 -I -B $T/receipt-validate.py --require-mid-maps runs/t1250-cover/receipt.json; echo $?
… "actual_sha256": "9276b198…", "expected_sha256": "70672eb3…" …; exit=1
```

  So the only routes to a literal-green gate are (a) evaluate at the freeze revision
  `a1140e7`, (b) an append-only rule amendment declaring the drift-only exception, or
  (c) new runs whose receipts pin the current validator. The L1's integrated verifier already
  takes route (b) implicitly: `verify.py:110` sets expected exit 1 for every
  `receipt-validate-<label>`, `verify.py:569` runs it expecting 1, and `verify.py:669-683`
  constrains the red to exactly two findings on that one path plus the retained
  `receipt-source-bound-valid-<label>` green. Frozen `decision-rule.json:3` contains no such
  clause, and the `claims.json:36` amendment is silent on it [OBSERVATION for the code paths;
  INFERENCE that the intended reading is freeze-revision + declared drift].

  Concurrent-state note (write-time check, 2026-10-20 16:20:27 -0300): the lane worktree copy
  of `receipt-validate.py` changed again after this seat's reads to
  `6afb7ef6…`/52682 B (`git status` now `M`, `git diff --stat` = 33 insertions/5 deletions,
  mtime 16:19:33). This seat made no such edit; every digest above is anchored to
  `refs/heads/main` `d0690fd` (`9276b198…`). Under the later worktree bytes the same clause
  stays red (the live file still differs from the receipt's `70672eb3…` pin); only the
  reported `actual_sha256` would differ. No signal or match in §2–§3 depends on it.

**Answer to "does the frozen mechanism rule hold":** yes for cover's mechanism and for the
cohort's D/non-D direction as parsed from raw logs; **no for its binding clause at the
delivered revision as written** — the clause is falsified by a validator-bytes-only drift that
the integrated verifier pre-declares but the frozen rule text does not. C3's count is 8 under
the run-time validation recorded at `a1140e7` and 0 at the tip under the literal gate.

## 5. Depth: what "silent" does and does not mean in this log

```
$ grep -n 'WARN' runs/t1250-cover/logs/rea-ghidra-XVD7qp/ghidra.log
197:2026-10-20 16:05:17 WARN (GoTypeManager) Failed to get subtype '[46912496118442]runtime.elfSym' in *[46912496118442]runtime.elfSym
198:2026-10-20 16:05:17 WARN (GoTypeManager) Failed to get subtype '[1125899906842623]byte' in *[1125899906842623]byte
199:2026-10-20 16:05:17 WARN (GoTypeManager) Failed to get subtype '[562949953421311]uint16' in *[562949953421311]uint16
```

- These are the only diagnostics in the log besides INFO. They are **not** Go analysis
  failures and are neither refuting nor predicted: the frozen prediction's
  `extra_expectations` enumerates only errors/EOF/invalid-index, and the emulator's `per_type`
  table (`predictions/swiss-misread/t1250-cover.json`) marks all 53 map types `silent` with
  `detail: null`, `eof: null`. "Silent" therefore means *no failure on the map path*, not
  *no Go diagnostic* [OBSERVATION + definitional reading].
- The same three subtype strings occur in cover and in **all six other silent labels**
  (`asm`, `cgo`, `compile`, `go`, `gofmt`, `preprofile`; 7/7), with a fourth carrier-specific
  `time.Timer`/`time.Ticker` warning in four of them, and in **0/1** failing label
  (`vet` has 0 WARN lines). Their identity across carriers with different map sets argues
  against a carrier-map cause [OBSERVATION + INFERENCE]. Vet's failure stack
  (`t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:206-207`:
  `GoTypeManager.markupGoTypes(GoTypeManager.java:153)` /
  `GolangSymbolAnalyzer.added(GolangSymbolAnalyzer.java:146)`; `:229`, `:235` for the
  `EOFException` and `GoName.readStructure`) is the same markup phase that emits cover's
  WARNs at `:197-199`, i.e. the hard-failure route aborts before the warnings are reached
  [INFERENCE, grounded in the cited stack and timestamps].
- The three lengths are all-ones-ish bit patterns: `0x2aaaaaaaaaaa` (46 bits),
  `0x3ffffffffffff` (50 bits), `0x1ffffffffffff` (49 bits). Consistent with misread length
  fields, but the frozen prediction binds no WARN and no address, so the cause is
  **unresolved**; it is not used by the match.
- **Adjacent (not this seat's verdict):** `t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log:347`
  has `ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) -
  element cannot be mapped to a null key java.lang.NullPointerException`. The frozen predicate
  `Go analysis failure` is `GolangSymbolAnalyzer`-only (`log-extract.py` `SYMBOL_FAILURE_TEXT`),
  and `analyzer_errors` requires `level == ERROR and component.startswith("Golang")`
  (`log-extract.py:244`); `AnalysisTaskWrapper` fails both, so compile's recorded
  `extra.analyzer_errors_empty=true` and `compare.exit=0` are true *by extractor scope*, not
  because no Go-task error occurred. The literal non-D clause still holds for compile, but the
  lesson's "silent" should be stated as "no GolangSymbolAnalyzer failure", and the compile
  seat owns the rest.

## 6. Remaining unknowns

1. Cause of the three cohort-wide `Failed to get subtype` WARNs (Swiss-map downstream vs an
   independent Go 1.25 type-resolution limit). No frozen field or emulator table binds them;
   this seat did not decode carrier RTTI, to respect the no-REA/no-execution lane.
2. Up to one poll interval (≤0.5 s) of post-script lines may be absent from every retained log
   (`receipt.json.log_capture_limit`); the four signals are inside the retained bytes, so this
   does not affect the match, but "no failure after post scripts" is not asserted.
3. Emulator `walk.indexed_types.h1 = 2422` and Ghidra's `Found 2470 Go types`
   (`ghidra.log:195`) are different counters; no frozen field reconciles them, and none is
   used here.
4. The C3 provenance is REA `rea-agents@6.5.0` (`receipt.json.steps.analyze.argv`) over Ghidra
   `12.1.4` (`analyze.json`), matching the contract's CLI convention; the C3 claim text does not
   name the REA version. Recorded, not a defect.
5. `evidence/receipt-validation/t1250-cover.json.pins_path` is `/tmp/pins.py`, outside custody.
   The file still exists and hashes `9e9c7250…`, identical to `pins.py` at `a1140e7` **and** at
   the tip (unchanged), so the dependency is recoverable from git; still, the retained evidence
   names an ephemeral path.
