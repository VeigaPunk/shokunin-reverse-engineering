# W2 Runs1250noswissnethttp — independent re-derivation of carrier run `s1250-noswiss-nethttp`

HOLDS

Seat: KaidokuR18.Runs1250noswissnethttp (author-side advisory, leaf). REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` = lane HEAD; all anchors cited at REV via `git show REV:path` / worktree files verified byte-identical to REV blobs. No tool installs or updates were performed. Read-only lane; only this report written.

Axes worked: (1) field-accuracy of the frozen prediction vs raw log, (2) binding integrity (session/target/hash custody), (3) scope honesty (what "empty errors" actually scopes).

## Baseline integrity

- `git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1250-noswiss-nethttp.prediction.json` → exit 0. Expected: `snapshot_route:"info"`, `snapshot_label:"1.25.0"`, `fallback_to:null`, `missing_bootstrap:false`, `untested_version:null`, `analyzer_errors_empty:true`, `eof_reads:[]`, `invalid_index_reads:[]`; carrier sha256 `4c8eb02f…6797`.
- `git diff --stat eb6c2668… b2aad08… -- .ufo/waves/round-18/predictions/s1250-noswiss-nethttp.prediction.json` → empty output, exit 0. Observation: prediction blob unchanged since freeze (decision-rule binding_gate clause 3 satisfied). [INFERENCE] intent: freeze intact.
- `git status --porcelain` → 8 entries, all untracked wave-2 orchestration files (`gen-wave2.py`, `w2/`, `wave2-*.json/txt`). No tracked run/prediction/tool file dirty. Exit 0.

## Raw-log extraction (independent of observation.json)

Log: `.ufo/waves/round-18/runs/s1250-noswiss-nethttp/logs/rea-ghidra-Tikfv1/ghidra.log` (10,516 lines). REV-blob identity: `git cat-file -p REV:<log> | sha256sum` = `e42aed9fdb9c9a0f64623433792ce2a9ee5492550f088671b43e282c982c5b91` = `sha256sum` of worktree file; exit 0 both.

```
for p in "GoApiSnapshot" "Go analysis failure" "Invalid index:" "Unable to read past EOF:" \
         "Untested Go version" "Falling back from" "Reading Go binary info"; do \
  printf '%s => %s\n' "$p" "$(grep -c -- "$p" ghidra.log)"; done; echo "LOOP_EXIT=$?"
# GoApiSnapshot => 1 ; Go analysis failure => 0 ; Invalid index: => 0
# Unable to read past EOF: => 0 ; Untested Go version => 0 ; Falling back from => 0
# Reading Go binary info => 1 ; LOOP_EXIT=0
```
(0-count greps are grep's standard no-match exit 1 inside the loop; the absence is the evidence.)

Route lines found (observation):
- `ghidra.log:180` — `INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0` (exactly one GoApiSnapshot record; no WARN, no fallback line).
- `ghidra.log:181` — `INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0`; `ghidra.log:179` — `Reading Go binary info: target-4c8eb02f3ee9.bin`; `ghidra.log:358` — `GolangSymbolAnalyzer Go version 1.25.0`; `ghidra.log:185` — `DWARF producers: [Go cmd/compile go1.25.0; regabi]`.

## Verdict per field

| Field | Predicted | Independently observed | Verdict |
|---|---|---|---|
| `snapshot_route` | `info` | 1 GoApiSnapshot INFO record (ghidra.log:180), 0 WARN/fallback | HOLDS |
| `snapshot_label` | `1.25.0` | ghidra.log:180,181,358; DWARF producer :185 | HOLDS |
| `fallback_to` | `null` | 0 `Falling back from`; observation `snapshot_fallbacks: []` | HOLDS |
| `missing_bootstrap` | `false` | `Reading Go binary info` ×1 → `bootstrap_attempts=1`, `classification=snapshot_loaded` | HOLDS |
| `untested_version` | `null` | 0 `Untested Go version` | HOLDS |
| `extra.analyzer_errors_empty` | `true` | 0 ERROR records from `Golang*` components (contract scope, see F2) | HOLDS (scoped) |
| `extra.eof_reads` | `[]` | 0 `Unable to read past EOF:` over all 10,516 raw lines | HOLDS |
| `extra.invalid_index_reads` | `[]` | 0 `Invalid index:` | HOLDS |

`compare.json` (wave 1) records the same values, `all_match:true`, `compare.exit: 0`; my re-derivation agrees with it on every field (observation of file + independent extraction). [INFERENCE] the compare is faithful for this carrier.

## Binding and custody

- `sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-noswiss-nethttp` → `4c8eb02f3ee914979d0b50d5826f79d2622b8dd14d1007d441432969751a6797`, exit 0 = prediction `carrier.sha256` = receipt `sha256_pre` == `sha256_post` (receipt.json:4-8).
- `md5sum` same file → `6ee46a6c0b30d12f9bcc5e79e83d8d26`, exit 0 = receipt `md5_pre` (receipt.json:5). Carrier byte-identical pre/post run.
- Session path: receipt `bound_sessions[0] = /tmp/kr17-rea-x_3wn1vb/rea-ghidra-Tikfv1` = `Using log file:` target at ghidra.log:2 = retained `logs/rea-ghidra-Tikfv1/` dir name; `unbound_sessions: []`. `observation.json` `import_target = …/rea-ghidra-Tikfv1/target-4c8eb02f3ee9.bin` — `target-<sha12>` = first 12 hex of carrier sha256 (also ghidra.log:173,179). HOLDS.
- Log custody: observation `log_sha256 = e42aed9f…` == retained file == REV blob; `log_bytes 1783206` == `wc -c`. HOLDS.
- Carrier self-identity: `inspect-go.json` buildinfo `go_version = "go1.25.0 X:noswissmap"`, module text `GOEXPERIMENT=noswissmap`, `GOOS=linux`, `GOARCH=amd64` — matches prediction `input`/`selection`. HOLDS.
- `receipt.pin` set includes the prediction, `swiss-misread.py` (sha `14924bd6…` = prediction `c3.emulator_sha256`, producer.json), `go1.25.0.json` and all base/diff pinpoints. `carrier-run.exit`, `observation.exit`, `compare.exit` all `0`.

## Receipt validation

```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
  .ufo/waves/round-18/runs/s1250-noswiss-nethttp/receipt.json ; echo EXIT=$?
# counts: receipts 1, valid 1, invalid 0, unreadable 0; status valid; checks_performed 366; findings []
# require_mid_maps: true (pins/mid-1.json, pins/mid-2.json present); EXIT=0
```
Decision-rule binding_gate (`git show eb6c2668:…/predictions/decision-rule.json`): all three clauses hold for this label (validator exit 0; bound-log carrier sha256 == prediction; prediction blob unchanged since freeze).

## Findings (advisory; none load-bearing for this label's verdict)

- **F1 [observation+inference, low] go_lines doc/contract-text drift.** `git show REV:.ufo/waves/round-17/contract.md` :56-58 and the `log-extract.py` docstring :17-18 say go_lines keeps components "in the named set **or starting with `Go`/`Golang`**", but `log-extract.py:122-130` implements `GO_COMPONENTS ∪ GO_BACKGROUND_COMMANDS ∪ Golang*-alnum` only (deliberate anti-forgery tightening, comment :71-73, "w2 LogExtractFuzz D2"). Net effect here: 10,103 `GoFuncData` ERROR records (e.g. ghidra.log:359 `Failed to add source file mapping…`) are absent from `observation.json go_lines` (21 entries), while `PropagateRttiBackgroundCommand`/`FixClosureFuncArgsBackgroundCommand` (in neither contract clause) are present (:10472-10474). Reproducer: `grep -c " ERROR " ghidra.log | …` counts vs python dump of `go_lines`. Docs should be aligned with the tightened implementation; the compared C3 fields are unaffected (eof/invalid-index scan all raw lines; analyzer_errors is `Golang*`-scoped by contract :55-56 and `log-extract.py:243-244`).
- **F2 [observation+inference, low] naming-calibration risk on `analyzer_errors_empty`.** The raw log contains 10,113 ERROR-level records (10,103 `GoFuncData`, 5 `DWARFDataTypeImporter` :174-178, 5 `DWARFImportSummary` :353-357), yet the field asserts "empty". This is contract-correct (scope: ERROR from `Golang*` only) and the discriminating H1 signatures (`Go analysis failure`, EOF/index reads) are component-independent raw-line scans, but a face-value reading of the prediction field misleads. Suggest a prediction-side gloss or a sibling field for GoFuncData/DWARF error volumes.
- **F3 [observation, info] 4 WARN records from `GoTypeManager`** (`Failed to get subtype …`, ghidra.log:557-559,7053). Not GoApiSnapshot route lines; per `log-extract.py:98-102` only the GoApiSnapshot component discriminates route, so `snapshot_route=info` stands. No action.

## Residual risk / verification gaps

- The retained log is a polling copy (`receipt.log_capture_limit`); the copy is internally complete (byte count matches, final line :10516 is the normal `REPORT: Analysis succeeded` for the bound target), so no truncation is observable — but absence-of-error claims inherit the capture caveat by construction. Not resolvable from retained data.
- I did not re-verify the emulator (`swiss-misread.py`) logic or the base-JSON selection law; both are pinned by hash in receipt/producer and were out of scope for this seat (per-carrier field re-derivation only). [INFERENCE] within scope, the label's H1 outcome is `none`, matching the frozen `h0`/`h1` agreement for non-diagnostic noswiss-nethttp in `decision-rule.json` table.

Commands recorded above: all exit 0 (per-pattern 0-count greps exit 1 = no match, noted inline). No pacman/uv/npm installs; no REA analyze/search/decompile; no carrier execution; no lane writes besides this report.
