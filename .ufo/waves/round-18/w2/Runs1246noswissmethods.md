# w2 · Runs1246noswissmethods — independent re-derivation of `s1246-noswiss-methods`

HOLDS

Seat: author-side advisory (leaf, read-only; only this file written). Lane REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (worktree HEAD verified: `git rev-parse HEAD` → `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, exit 0). Prediction frozen at `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. All paths below relative to `kaidoku-shokunin/` unless absolute.

## Commands (each with exit code)

```
$ git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1246-noswiss-methods.prediction.json
# full JSON printed; exit=0 (re-checked: gitshow_exit=0, git cat-file -e → catfile_exit=0)

$ grep -n 'GoApiSnapshot' .ufo/waves/round-18/runs/s1246-noswiss-methods/logs/rea-ghidra-2bOinT/ghidra.log
112:2026-10-20 13:26:03 INFO  (GoApiSnapshot) Using Go API snapshot for 1.24.6
# route_exit=0

$ grep -c 'Go analysis failure' <ghidra.log>   # → 0, exit=1 (absence)
$ grep -c 'Invalid index:'       <ghidra.log>   # → 0, exit=1 (absence)
$ grep -c 'Unable to read past EOF:' <ghidra.log> # → 0, exit=1 (absence)
$ grep -c 'Untested Go version'  <ghidra.log>   # → 0, exit=1 (absence)
$ grep -n -i -E 'fallback|falling back|bootstrap' <ghidra.log>  # no output, exit=1 (absence)

$ sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-methods
93f3546cbb924aba632ed2b0bfebd9e0275dddb449bf65fdf3e64fa3d5d88031  (exit 0)
$ md5sum   /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-methods
2c9383d00c73e72f7bbd35b35e820026  (exit 0)
$ sha256sum logs/rea-ghidra-2bOinT/ghidra.log logs/rea-ghidra-2bOinT/script.log
738830bf2eebc7fa01292d6c8c9ff6bc96aaa9a5f11946a2fa7c72e6e71ecf5d  ghidra.log (952724 bytes)
334250ba295e6aa8c25074e27fc3e06b5aca29163bb3f54815d0469d8215437d  script.log (105 bytes)  (exit 0)

$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1246-noswiss-methods/receipt.json
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,"pins_available":true,...,"require_mid_maps":true,...}
# status "valid", findings [], checks_performed 360; exit=0

$ git diff --stat eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/predictions/s1246-noswiss-methods.prediction.json
# no output, pred_diff_exit=0 (prediction unchanged between freeze point and REV)
```

## Per-field verdicts (raw-log re-derivation vs frozen prediction)

Raw-log source: `.ufo/waves/round-18/runs/s1246-noswiss-methods/logs/rea-ghidra-2bOinT/ghidra.log` (5721 lines, OBSERVATION).

| Field | Prediction (eb6c2668 `expected`/`extra_expectations`) | My independent extraction | Verdict |
|---|---|---|---|
| `snapshot_route` | `"info"` | exactly one GoApiSnapshot record, level INFO: ghidra.log:112 (`Using Go API snapshot for 1.24.6`) | HOLDS |
| `snapshot_label` | `"1.24.6"` | ghidra.log:112 label `1.24.6`; corroborated ghidra.log:113 (`GoRttiMapper … for version 1.24.6`), ghidra.log:219 area (`GolangSymbolAnalyzer Go version 1.24.6`, observation.json go_lines) | HOLDS |
| `untested_version` | `null` | zero `Untested Go version` records (grep -c → 0, exit 1) | HOLDS |
| `fallback_to` | `null` | zero fallback records; only GoApiSnapshot record in whole log is the INFO at :112 (grep -i fallback → none) | HOLDS |
| `missing_bootstrap` | `false` | zero `bootstrap` substrings anywhere in ghidra.log; `Reading Go binary info` present at ghidra.log:111 (observation.bootstrap_attempts=1) | HOLDS |
| `analyzer_errors_empty` | `true` | extraction law is scoped: ERROR ∧ component `Golang*` (round-17/tools/log-extract.py:243-244) — zero such records. See caveat F1 | HOLDS (scoped law) |
| `eof_reads` | `[]` | zero `Unable to read past EOF: A, B` records (grep -c → 0, exit 1) | HOLDS |
| `invalid_index_reads` | `[]` | zero `Invalid index: N` records (grep -c → 0, exit 1) | HOLDS |

Lane's own `compare.json` (`.ufo/waves/round-18/runs/s1246-noswiss-methods/compare.json`, `all_match: true`, 8 fields) agrees with every one of my independent derivations — no divergence found between lane extraction and raw-line truth.

## Log binding (session path, target-<sha12>, MD5) — HOLDS

- Session path: ghidra.log:46 `IMPORTING: file:///tmp/kr17-rea-2nt5ngt3/rea-ghidra-2bOinT/target-93f3546cbb92.bin` == receipt `bound_sessions[0]` == `retained_logs[0].session_dir` (receipt.json, OBSERVATION). observation.json `log_file_line`/`import_target` match the same session dir.
- target-<sha12>: `93f3546cbb92` = first 12 hex of carrier sha256 `93f3546cbb92…` (ghidra.log:46,64,105,111,5715,5721 all reference the same target name; receipt.steps.analyze ran REA against the same carrier path).
- MD5: ghidra.log:64 `Loading file:///tmp/…/target-93f3546cbb92.bin?MD5=2c9383d00c73e72f7bbd35b35e820026` == my recomputed carrier md5 `2c9383d00c73e72f7bbd35b35e820026` == receipt `carrier.md5_pre`.
- Log integrity: retained ghidra.log sha256 `738830bf…`/952724 B and script.log sha256 `334250ba…`/105 B both recomputed identical to receipt `retained_logs[0].files.*` and `steps.analyze.retained_logs[0].files.*`. receipt-validate exit 0 with `binding.md5_ok/logfile_ok/target_ok` all true (receipt.json retained_logs[0].binding).
- Carrier sha256: recomputed `93f3546c…88031` == receipt `carrier.sha256_pre` == `sha256_post` == prediction `carrier.sha256`. Pin map `pins/mid-1.json` equal=true, 152 entries, no changed/missing (receipt.steps.analyze.pin_checks[0]).

## Findings

F1 (depth note, OBSERVATION + INFERENCE, no defect): the raw log contains 5448 `ERROR (GoFuncData) Failed to add source file mapping: new entry would overlap entry …` records (first at ghidra.log:220; plus 42 `DWARFImportSummary`, 5 `DWARFDataTypeImporter` ERROR, 3 `GoTypeManager` WARN). `analyzer_errors_empty: true` holds only under the frozen extraction law's scoped definition (ERROR ∧ component `Golang*`, log-extract.py:243-244); a naive "no ERROR-severity lines" reading would be false. The prediction's basis cites Ghidra source-law messages (GoApiSnapshot/GoRttiMapper/GolangSymbolAnalyzer classes), so the scoping is faithful to the claim; but the run is not literally error-free. [INFERENCE] GoFuncData overlap errors are a known benign class for Go DWARF source maps and unrelated to the snapshot-selection mechanism under test.

F2 (OBSERVATION, context only): `s1246-noswiss-methods` is one of the 15 C3 labels but is NOT in the frozen diagnostic set D = {calib-aether, s1246-swiss-nethttp, real-kimi-webbridge} (claims.json:39, C3 amendment). The wave-1 amendment records the methods/nomethods pair as non-diagnostic (claims.json amendments, C3 `why`). So this run's HOLDS verdict corroborates H1 but does not by itself decide the mechanism rule.

## Residual risk / verification gaps

- The prediction's `c3` block (`true_kind: old`, `misread_map_types: 0`, `uncommon_map_types: 1`, swiss-misread sha256 `14924bd6…`) is NOT re-derivable from ghidra.log raw lines; I verified only that the pinned swiss-misread.py sha256 in receipt pins matches prediction `c3.emulator_sha256` (`14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`, receipt pins map). Re-derivation of map-type counts belongs to the swiss-misread reviewer seats.
- `log_capture_limit` (receipt.json): polling copy — lines written after the final poll before REA deleted its runtime root could be missing. [INFERENCE] Risk is low here: the log ends with the normal post-script ANALYZING record (ghidra.log:5721) and analysis succeeded (ghidra.log:5715), but tail truncation cannot be fully excluded from the retained copy alone.
- No installs performed; no tools installed or upgraded (tooling directive: nothing needed beyond `python3`/`git` already present).
