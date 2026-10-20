HOLDS

Independent re-derivation of carrier run `s1250-swiss-nomethods` at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, against frozen prediction `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1250-swiss-nomethods.prediction.json`. All paths below relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; anchors verified identical at REV and working tree. Read-only session; no tool installs performed. REA/Ghidra not run; carrier not executed.

## Verdict per field

| Field | Predicted | Observed (independent, raw log) | Verdict |
|---|---|---|---|
| `expected.snapshot_route` | `info` | `ghidra.log:112` = `INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0`; zero `(GoApiSnapshot)` WARN lines in 6052-line log | HOLDS (observation) |
| `expected.snapshot_label` | `1.25.0` | same line 112: `for 1.25.0`; `observation.json:api_snapshot_info_labels=["1.25.0"]` | HOLDS (observation) |
| `expected.fallback_to` | `null` | `grep -iE 'fallback\|untested'` over whole log → no match (exit 1) | HOLDS (observation) |
| `expected.untested_version` | `null` | no `Untested` string (same grep, exit 1) | HOLDS (observation) |
| `expected.missing_bootstrap` | `false` | `ghidra.log:111` `INFO (GoRttiMapper) Reading Go binary info: target-83c4f558d322.bin`; observation.json `missing_bootstrap=false` | HOLDS (observation) |
| `extra_expectations.analyzer_errors_empty` | `true` | `Go analysis failure` → 0 matches (grep exit 1); observation.json `analyzer_errors=[]`, `symbol_analysis_failures=[]`, `mapper_errors=[]` | HOLDS (observation) |
| `extra_expectations.eof_reads` | `[]` | `Unable to read past EOF:` → 0 matches | HOLDS (observation) |
| `extra_expectations.invalid_index_reads` | `[]` | `Invalid index:` → 0 matches | HOLDS (observation) |
| `carrier.sha256` | `83c4f558d3224f5de6b3eab99a48cb6176ae790b03dd571265bed0f9e702a68b` | recomputed on `/home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nomethods` = same; = receipt `sha256_pre`=`sha256_post` | HOLDS (observation) |

## Commands and exit codes (each pasted as run)

```
$ grep -nE 'GoApiSnapshot|Go analysis failure|Invalid index:|Unable to read past EOF:' .ufo/waves/round-18/runs/s1250-swiss-nomethods/logs/rea-ghidra-4Xh0g3/ghidra.log
112:2026-10-20 13:28:38 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0
(exit 0; only line 112 matched all four patterns — the other three have zero occurrences)
```

```
$ grep -nE 'Invalid index|past EOF|analysis failure|Untested' <same log>      → no output, exit 1
$ grep -inE 'fallback|untested' <same log>                                    → no output, exit 1
```

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1250-swiss-nomethods/receipt.json
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,"pins_available":true,
 "receipts":[{"checks_performed":360,"findings":[],"kind":"carrier","status":"valid","valid":true}],
 "require_mid_maps":true,"tool":"receipt-validate.py"}
VALIDATE_EXIT:0
```

```
$ md5sum <carrier> → 3d0945e5bc14d59075d486305daf1689   (exit 0)
$ sha256sum <carrier> → 83c4f558d3224f5de6b3eab99a48cb6176ae790b03dd571265bed0f9e702a68b   (exit 0)
$ sha256sum <ghidra.log> → bb9e74790c7265b213ae6697939aa5b22741926112b998d8f8bf898df8396970   (exit 0)
```

```
$ sha256sum .ufo/waves/round-18/predictions/s1250-swiss-nomethods.prediction.json
  → 2586ba703604e7638cbd70976bb6d4d28b0363b543bf675b2bee244f3c411893
$ git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1250-swiss-nomethods.prediction.json | sha256sum
  → 2586ba703604e7638cbd70976bb6d4d28b0363b543bf675b2bee244f3c411893   (unchanged from freeze)
$ git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:<same> | sha256sum → same digest
```
All exit 0.

## Log binding (independent checks)

- **Session path**: `ghidra.log:2` records `Using log file: /tmp/kr17-rea-6f2hhth7/rea-ghidra-4Xh0g3/ghidra.log` = receipt.json `bound_sessions[0]` = `/tmp/kr17-rea-6f2hhth7/rea-ghidra-4Xh0g3` = retained dir `logs/rea-ghidra-4Xh0g3/` (observation).
- **target-<sha12>**: `ghidra.log:46` `IMPORTING: file:///tmp/kr17-rea-6f2hhth7/rea-ghidra-4Xh0g3/target-83c4f558d322.bin`; `83c4f558d322` = first 12 hex of my recomputed carrier sha256 (observation).
- **MD5**: `ghidra.log:65` `Loading ...target-83c4f558d322.bin?MD5=3d0945e5bc14d59075d486305daf1689` = my recomputed carrier MD5 = receipt `carrier.md5_pre` (observation). Ghidra computed this digest at import time from the bytes it actually read — binds log→carrier.
- Log bytes/sha256 at REV (`git show REV:...ghidra.log | sha256sum` → `bb9e7479…`) equal the working-tree file and receipt `retained_logs[0].files["ghidra.log"].sha256`; same for receipt.json itself (`e6eba3ca…` at REV = working tree) (observation).
- Pins: receipt `pins_compare` = `equal:true, changed:[], missing:[]`; pinned prediction `2586ba70…` = freeze blob; pinned `tools/swiss-misread.py` = `14924bd6…` = prediction `c3.emulator_sha256`; pinned Ghidra `go1.25.0.json` = `54d10162…` = prediction `selection.base.sha256` (observation).
- Run exits: `carrier-run.exit`=0, `compare.exit`=0, `observation.exit`=0; `compare.json` `all_match:true` with observed values agreeing with my independent extraction on all 8 fields (observation).

## Residual risk and verification gaps

- **Polling-copy truncation (observation → low risk)**: receipt `log_capture_limit` = "polling copy; lines written after the final poll before REA deletes its runtime root can be missing" (39 polls, last copy 16:28:54.65Z). The retained log ends at `ghidra.log:6052` (post-script ANALYZING line); headless teardown lines are absent. A failure marker emitted only during teardown would be missed — but success was already reported at `ghidra.log:6046` (`REPORT: Analysis succeeded`), and EOF/index errors, when they occur (calib-aether), fire during snapshot bootstrap well before completion. Inference: truncation does not plausibly hide a missed marker for this label.
- **Non-counted ERROR lines (observation)**: the log contains `DWARFDataTypeImporter` array-size errors (`ghidra.log:106-110`) and ~50 `GoFuncData` "Failed to add source file mapping: new entry would overlap" errors (`ghidra.log:183-217+`). These are outside every predicted field (`analyzer_errors`, `eof_reads`, `invalid_index_reads` all empty and matched), so no prediction mismatch — noted so "no errors" is never overclaimed; only the three predicted marker classes are clean.
- **Diagnostic weight (inference)**: per prediction `c3` this label is `diagnostic:false`, `h1_kind:"none"` — it is a negative control; its clean log supports the decision-rule "confirmed" arm (no non-D synthetic shows a failure) but cannot by itself confirm the H1 misread mechanism. Pair-level verdict is out of this seat's scope.
- `compare.json` agreement is corroborating, not independent — its "observed" values were read from the same log; my greps are the independent leg.
