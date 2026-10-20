HOLDS

Seat KaidokuR18.Runs1246swissnethttp — wave-2 falsification of carrier run `s1246-swiss-nethttp` (C3 diagnostic, held-out D label). Axes: calibration (per-field verdict vs. artifacts), operability (every finding carries a reproducing command + exit), depth (independent re-derivation of route/failure/read values, bindings, freeze integrity, and an emulator re-run).

Anchor basis: `git rev-parse HEAD` → `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (EXIT:0) and `git status --porcelain -- .ufo/waves/round-18/predictions/ .ufo/waves/round-18/runs/s1246-swiss-nethttp/` → empty (EXIT:0), so working-tree path:line == `git show REV:path`. Paths below are lane-relative. [O] = observation, [I] = inference. No tool installs (none needed; nothing installed by this seat). No REA/Ghidra invocation, no carrier execution, read-only git only.

## 1. Frozen prediction (baseline)

```
$ git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1246-swiss-nethttp.prediction.json
EXIT:0
```
[O] `expected` = {fallback_to: null, missing_bootstrap: false, snapshot_label: "1.24.6", snapshot_route: "info", untested_version: null}; `extra_expectations` = {analyzer_errors_contain: "Go analysis failure", eof_reads: [], invalid_index_reads: [22386945]}; `c3` = {diagnostic: true, h1_kind: "invalid_index", hypothesis_frozen: "H1", misread_map_types: 2, true_kind: "swiss", uncommon_map_types: 2}; carrier sha256 `5c9faf239ed2c683…201b6`; selection `exact_diff` (base go1.24.0.json `aab28c8f…`/10039962 B, diff go1.24.6.json.diff `e169e8dd…`/118810 B). Decision rule: `predictions/decision-rule.json:2` (binding_gate), `:15-18` (held_out_D includes this label), `:136-149` (its row: route info, h1 invalid_index, invalid_index_reads_h1 [22386945], eof_reads_h1 []).

## 2. Independent re-derivation from the retained raw log

```
$ grep -nE 'GoApiSnapshot|Go analysis failure|Invalid index:|Unable to read past EOF:|Untested Go version' .ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log
EXIT:0 — hits only at :180 (GoApiSnapshot INFO), :408 (Go analysis failure), :451 (Invalid index: 22386945); zero "Unable to read past EOF:" and zero "Untested Go version" lines
```
[O] Raw lines (all in `runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log`):
- :180 `2026-10-20 13:29:00 INFO  (GoApiSnapshot) Using Go API snapshot for 1.24.6` — the only GoApiSnapshot line; route=info, label=1.24.6.
- :181 GoRttiMapper echo "Using Go API snapshot for version 1.24.6"; :407 `GolangSymbolAnalyzer Go version 1.24.6`; :191 `DWARF producers: [Go cmd/compile go1.24.6; regabi]` — version corroborated three ways.
- :408 `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` — sole occurrence.
- :451 `Caused by: java.io.EOFException: Invalid index: 22386945` — sole occurrence; stack :452-468 goes `GoName.getPkgPath → GoRttiMapper.resolveNameOff/getGoName → GoName.readStructure → BinaryReader.readNextUnsignedByte → MemoryByteProvider.ensureBounds`.

## 3. Per-field verdict (frozen prediction vs. re-derived observation)

| Field | Predicted | Re-derived from raw log | Verdict |
|---|---|---|---|
| snapshot_route | `info` | sole GoApiSnapshot line is INFO (ghidra.log:180) | MATCH |
| snapshot_label | `1.24.6` | ghidra.log:180/:181/:407/:191 | MATCH |
| fallback_to | `null` | no fallback lines; observation.json:84 `snapshot_fallbacks: []` | MATCH |
| untested_version | `null` | zero "Untested Go version" lines; observation.json:92 `[]` | MATCH |
| missing_bootstrap | `false` | snapshot loaded (:180); observation.json:8 `bootstrap_attempts: 1`, :83 `false` | MATCH |
| extra.analyzer_errors_contain | `"Go analysis failure"` | ghidra.log:408; observation.json:2-4 | MATCH |
| extra.eof_reads | `[]` | zero "Unable to read past EOF:" lines; observation.json:10 `[]` | MATCH |
| extra.invalid_index_reads | `[22386945]` | ghidra.log:451 sole occurrence; observation.json:73-75 | MATCH |

[O] Pipeline agreement: observation.exit=0, compare.exit=0, carrier-run.exit=0 (file contents `0`); compare.json:2 `all_match: true` with per-field match:true (:25-28 route shown). [I] The compare tool's own verdict is corroborated field-by-field by my grep re-derivation above, so `all_match` is not taken on trust.

## 4. Log binding and carrier identity

```
$ sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp <ghidra.log> && md5sum <carrier>
EXIT:0
carrier  sha256 = 5c9faf239ed2c68304666992a8d2c1dc40c36e90f8021c62fef4cc4453f201b6  (size 4785233)
carrier  md5    = a0fdc0cd3e31f9c02162447b3aa78faf
ghidra.log sha256 = 05ea153e7f9a758cc8eac25c38cf2ad2ff583a7d35a248faf110f350cf080334  (52372 B)
script.log  sha256 = 9750b757b7dc141e0db2c4cad8febfeb2fbd4ce2e3e28cbd032b0514f51ddb7c  (106 B)
```
- Session path [O]: ghidra.log:2 self-declares `/tmp/kr17-rea-8yf3uehw/rea-ghidra-zHRS1l/ghidra.log` == receipt.json:2-4 `bound_sessions[0]` == receipt.json:1911 `retained_logs[0].session_dir` == observation.json:79 `log_file_line`.
- target-<sha12> [O]: ghidra.log:46 `IMPORTING: …/target-5c9faf239ed2.bin`; `5c9faf239ed2` = first 12 hex of the carrier sha256 (computed above).
- MD5 [O]: ghidra.log:63 `Loading …target-5c9faf239ed2.bin?MD5=a0fdc0cd3e31f9c02162447b3aa78faf...` == receipt.json:6 `md5_pre` == computed md5sum.
- Carrier sha256 [O]: computed == prediction `carrier.sha256` == receipt.json:8-9 (`sha256_pre` == `sha256_post`, no drift) == inspect-go.json subject digest; inspect-go.json build_info `go_version: "go1.24.6"`, GOARCH=amd64/GOOS=linux, bytes 4785233.
- Log integrity [O]: computed ghidra.log sha256/bytes == observation.json:78,81 and receipt.json:1898-1902; script.log sha256 == receipt.json:1903-1907. Receipt binding block receipt.json:1892-1895 `logfile_ok/md5_ok/target_ok` all true — consistent with my independent checks.
- [O] Live session root `/tmp/kr17-rea-8yf3uehw` no longer exists (`ls` → "No such file or directory", EXIT:2), matching receipt `session_parent_leftovers: []` and the recorded caveat receipt `log_capture_limit` ("polling copy; lines written after the final poll … can be missing").

## 5. Receipt validation

```
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1246-swiss-nethttp/receipt.json
EXIT:0
{"counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "exit": 0, "pins_available": true,
 "receipts": [{"checks_performed": 360, "findings": [], "kind": "carrier", "status": "valid", "valid": true}],
 "require_mid_maps": true, "tool": "receipt-validate.py"}
```
[O] Mid-map pin: `runs/s1246-swiss-nethttp/pins/mid-1.json` sha256 `e5f3f381bb21511c7066927a96f667263b775742b59663305f0c314abca38f2b` (computed) == receipt `steps.analyze.pin_checks[0].map_sha256`, entries=152, taken 16:28:56 UTC; `pins_compare` equal=true, changed/missing/errors all empty; `mid_run_drift_steps: []`. [O] Step output digests recomputed: analyze.json `7610863a…` and inspect-go.json `ef3bf7c7…` == receipt `stdout_sha256`; analyze.stderr / inspect-go.stderr / carrier-run.stderr all 0 B with empty-sha256 `e3b0c442…` == receipt `stderr_sha256`. [O] All 7 `producer.json` tool_sha256 values match recomputed digests (carrier-run.py `6665dc7a…`, pins.py `9e9c7250…`, log-extract.py `eb8f2c78…`, compare.py `582a77f3…`, receipt-validate.py `70672eb3…`, swiss-misread.py `14924bd6…`, selection.py `6917da09…`). [I] The toolchain that produced the observation/compare/receipt is the pinned toolchain.

## 6. Freeze integrity (prediction frozen before run, unchanged since)

```
$ git show -s --format='%H %ci %s' eb6c2668… b2aad08…   → EXIT:0
eb6c2668… 2026-10-20 13:23:55 -0300 round-18: frozen C3 predictions and decision rule, wave-1 tools and evidence (pre-run)
b2aad08…  2026-10-20 13:38:07 -0300 round-18: carrier runs, corpus corrections, knowledge entry, registry and SOURCES (pre-falsify)
$ git show eb6c2668…:.ufo/waves/round-18/predictions/s1246-swiss-nethttp.prediction.json | cmp - .ufo/waves/round-18/predictions/s1246-swiss-nethttp.prediction.json
CMP-EXIT:0        (byte-identical)
$ git diff --stat eb6c2668… b2aad08… -- .ufo/waves/round-18/predictions/   → no output (unchanged)
$ git ls-tree -r b2aad08… --name-only -- .ufo/waves/round-18/runs/s1246-swiss-nethttp/   → all 16 run files tracked at REV
```
[O] Freeze commit 13:23:55 -0300 precedes run start 2026-10-20T16:28:55Z (= 13:28:55 -0300, receipt `steps` timestamps and ghidra.log:1-2) by ~5 min; producer.json `branch_tip` = eb6c2668… = the freeze commit; prediction blob byte-identical from freeze commit through REV and working tree. [I] The decision-rule binding_gate (decision-rule.json:2) is satisfied for this label on all three clauses.

## 7. Emulator re-derivation (prediction reproducible from bytes)

```
$ python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
EMU-EXIT:0
```
[O] Output equals the frozen prediction on every compared field: `predicted_failure_h1: true` kind `invalid_index`; `predicted_invalid_index_reads_h1: [22386945]`; `predicted_eof_reads_h1: []` (h0 silent, `predicted_failure_h0: false`); `true_kind: "swiss"` (SwissMapType 112 B read as OldMapType 88 B); `diagnostic: true`; `misread_map_types: 2` / `uncommon_map_types: 2` — exactly `*textproto.MIMEHeader` (addr 5812384) and `*url.Values` (addr 5823584), the two 40-byte-slot method-carrying named maps the C3 amendment added for the nethttp carriers; `snapshot_status: "exact_diff"`. [O] Selection inputs verified against the installed Ghidra typeinfo: go1.24.0.json sha256 `aab28c8f…`/10039962 B and patchverdiffs/go1.24.6.json.diff sha256 `e169e8dd…`/118810 B == prediction `selection`. [I] The observed failure stack (ghidra.log:451-468, pkgPath→name read past bounds) is the same read path the emulator models (h1 walk `["type@0x580fa0","elem"]`), i.e. the aether mechanism (method-carrying Swiss map types misread via the installed OldMapType layout) is what this log actually shows. [I] Scope note: the emulator re-run is a consistency check (same pinned tool generated the frozen blob); the independent leg is the §2 grep re-derivation — both agree.

## 8. Residual risks / verification gaps

1. [O] The retained ghidra.log is a polling copy cut at 16:29:24.103 UTC — it ends at ghidra.log:504 ("ANALYZING changes made by post scripts"), and the live session root is deleted, so no full-log cross-check is possible. [I] Post-cut lines belong to the no-return-fix/bridge phases, not Go type markup; Go analysis completed earlier (analysis summary 13:29:22, ghidra.log:470-500), so additional Go-analysis `Invalid index:`/EOF lines after the cut are unlikely. Risk: low, nonzero; the receipt records the caveat (`log_capture_limit`).
2. [O] compare.json:66 marks `snapshot_label` "non-discriminating: request echo". [I] Mitigated: version independently corroborated by DWARF producer (ghidra.log:191), GolangSymbolAnalyzer (:407), and inspect-go build_info — the label match is not load-bearing.
3. [O] carrier-run.stdout vs receipt.json differ only by the self-referential `"receipt_path"` line (diff at stdout :1890) and a trailing newline — benign, no content drift.
4. [O] Not verified here (out of seat scope): the other 14 labels, the mechanism verdict (`confirmed` requires all held-out D labels + noswiss siblings per decision-rule.json:9-13), and the Base-src.zip source-line basis citations — the observed log, not the cited source law, is this report's ground truth.

Tool installs: none (no pacman/uv/binary installs; pacman pause respected, read-only queries only).
