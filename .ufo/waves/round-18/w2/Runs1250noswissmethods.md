HOLDS

# W2 falsify: carrier run `s1250-noswiss-methods`, re-derived independently

Seat: KaidokuR18.Runs1250noswissmethods (author-side advisory, leaf). REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`, freeze F `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
Run dir `RUN=.ufo/waves/round-18/runs/s1250-noswiss-methods`. Retained log `LOG=$RUN/logs/rea-ghidra-yI43cD/ghidra.log`. All 16 run files at REV are byte-identical to disk (`git show REV:p | sha256sum` against `sha256sum p`, 16 SAME, 0 extra on disk).
No REA, Ghidra or carrier execution. No installs or updates. The only writes were this report and the scratch dir `/tmp/r1250nsm-DqKcv5`, which is a `git clone --depth 1 --branch main` of the lane at REV with origin removed and was deleted afterwards.

## Verdict per field
Predictions are from `git show F:.ufo/waves/round-18/predictions/s1250-noswiss-methods.prediction.json`. That blob is `91def4ed…dc47` at F, at REV and on disk; F added it, and no commit in F..REV touches it. The REV line anchors below refer to that same file.

| Field | Frozen (REV line) | Raw log, observed | Verdict |
|---|---|---|---|
| route (GoApiSnapshot) | `info` (:34) | 1 GoApiSnapshot record, `LOG:113` `INFO (GoApiSnapshot) Using Go API snapshot for 1.25.0`; 0 `WARN (GoApiSnapshot)`; 0 `Falling back from` | HOLDS |
| snapshot_label | `1.25.0` (:33) | `LOG:113`, `LOG:114` | HOLDS (request echo) |
| untested_version / fallback_to | null / null (:35, :31) | 0 `Untested Go version`, 0 fallback | HOLDS |
| missing_bootstrap | false (:32) | 0 `Missing Go bootstrap`; `LOG:112` `Reading Go binary info: target-450e3e5e1501.bin` | HOLDS |
| `Go analysis failure` (analyzer_errors_empty) | true (:38) | 0 matches; 0 `ERROR (Golang…`; 0 `Exception` anywhere in the log | HOLDS |
| `Invalid index:` values | `[]` (:40) | 0 (also 0 case-insensitive) | HOLDS |
| `Unable to read past EOF:` values | `[]` (:39) | 0 (also 0 case-insensitive `eof`) | HOLDS |
| session path | — | `LOG:2` `Using log file: /tmp/kr17-rea-ot9vacvb/rea-ghidra-yI43cD/ghidra.log` matches `receipt.json:3` and `:1911` | HOLDS |
| target-<sha12> | — | `LOG:46` `IMPORTING: file:///tmp/kr17-rea-ot9vacvb/rea-ghidra-yI43cD/target-450e3e5e1501.bin` = carrier sha256[:12] | HOLDS |
| MD5 | — | `LOG:66` `?MD5=9e496ce3cc05a7eada54f1fd332bdbd9` = `md5sum` of the carrier = `receipt.json:6` | HOLDS |
| carrier sha256 | `450e3e5e…ac23` (:28) | `sha256sum` of the carrier = `receipt.json:8-9` = `carriers/SHA256SUMS:7` (F and REV) = inspect-go/analyze subject digest | HOLDS |
| retained-log integrity | — | sha256 `0c1df94b…0d7c`, 993216 B, 5937 lines = `receipt.json:1899-1901` = `observation.json:161` | HOLDS |
| receipt-validate `--require-mid-maps` | exit 0 required (`decision-rule.json:2`) | exit 0, valid, 360 checks, 0 findings | HOLDS |
| freeze before run | — | reflog: `main@{13:23:55}` = eb6c266, then `@{13:38:08}` = b2aad08. Run started 13:27:29 (`runs/run-log.txt:14`). The pre-run pins in the receipt (`pins_pre`, taken 16:27:29Z, `receipt.json:1884`) record the prediction as sha `91def4ed…` with mtime 13:23:20 (`receipt.json:1872-1874`). `producer.json` branch_tip = F | HOLDS (local evidence only) |
| tool identity | — | carrier-run, pins, log-extract, compare, receipt-validate, swiss-misread and selection blobs are identical at F, REV and on disk, and equal `producer.json` tool_sha256 | HOLDS |

## Commands (observed exit codes)
```
# C1 raw per-field counts + binding lines                                   exit 0
cd $RUN && LOG=logs/rea-ghidra-yI43cD/ghidra.log && for p in '(GoApiSnapshot)' 'INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0' 'WARN  (GoApiSnapshot)' 'Falling back from' 'Untested Go version' 'Missing Go bootstrap' 'Go analysis failure' 'Invalid index:' 'Unable to read past EOF:' 'Exception' 'ERROR (Golang'; do printf '%s\t%s\n' "$(grep -c -F "$p" $LOG)" "$p"; done
  -> 1,1,0,0,0,0,0,0,0,0,0 ; binding lines 2,46,66 ; 'REPORT: Analysis succeeded' at 5931
# C2 carrier identity                                                        exit 0
sha256sum ~/.local/share/kaidoku-r18/carriers/s1250-noswiss-methods   -> 450e3e5e1501813eddf068d49c65523830d1bd6209a0d5bde7aaed99b3b4ac23
md5sum    ~/.local/share/kaidoku-r18/carriers/s1250-noswiss-methods   -> 9e496ce3cc05a7eada54f1fd332bdbd9
# C3 frozen prediction                                                       exit 0
git show eb6c266:.ufo/waves/round-18/predictions/s1250-noswiss-methods.prediction.json
# C4 validator (as assigned)                                                 exit 0
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $RUN/receipt.json
  -> {"counts":{"invalid":0,"valid":1,...},"receipts":[{"checks_performed":360,"findings":[],"status":"valid"}]}
```

### Independent re-derivations (REV tool copies run from the scratch clone)
- **R1** `log-extract.py --log $LOG`: exit 0. Output is byte-identical (`cmp`) to the committed `observation.json`.
- **R2** `compare.py --prediction <lane prediction> --observation $RUN/observation.json`: exit 0. Output is byte-identical to the committed `compare.json`.
- **R3** `compare.py` with the F-extracted prediction blob and the fresh R1 output: exit 0, `all_match True`, 8/8 fields.
- **R4** `swiss-misread.py --carrier <carrier> --golang-root …/typeinfo/golang`: exit 0. The output is JSON-equal to `F:predictions/swiss-misread/s1250-noswiss-methods.json`, but the bytes differ by one trailing `\n` (see N2).
- **R5** I re-assembled the full prediction with the `gen-predictions.py` per-label logic (`F:.ufo/waves/round-18/gen-predictions.py:43-72`). Inputs: `buildinfo-probe.py`, which read `go1.25.0 X:noswissmap`; `predict.py`; and R4. The result is byte-identical to the frozen blob: sha `91def4ed0cc4821d0ed6eb9fdee6718e90805d7b268ec8ed4f934a2f9c9dcc47`, which is `predictions/SHA256SUMS:12` at REV.
- **Validator mutation probes.** Each probe edits a copy of `receipt.json` in the scratch clone; every exit code is from `receipt-validate.py --require-mid-maps` (REV copy).
  - M0 is an unchanged relocated copy: exit 0, `[]`.
  - M1 swaps in the `s1250-noswiss-nomethods` session and log: exit 1, `binding_mismatch` (logfile_ok=True, target_ok=False, md5_ok=False).
  - M2 is this log with only the MD5 zeroed, sha256 and bytes re-recorded: exit 1, `binding_mismatch` (md5_ok=False).
  - M3 is this log truncated before the IMPORTING line: exit 1, `binding_mismatch` (target_ok=False, md5_ok=False).
  - Result: on this receipt the binding check detects all three forgeries (3/3), and the control passes.

## Findings
No BROKEN or PARTIAL field. Calibration notes, most important first:

- **N1 (calibration, INFO): this match supports neither hypothesis.**
  - **Observed:** the prediction marks `"diagnostic": false` with `h0_kind`=`h1_kind`=`none` (REV :16, :19-20).
  - **Observed:** the route cannot come out any other way for x.y.0 versions. In Base-src.zip `GoApiSnapshot.java`, the fallback loop at :153 needs `patch > 0`, and the WARN at :159-160 runs only when patch versions differ, so a 1.25.0 run always takes the INFO branch at :163.
  - **Observed:** `snapshot_label` just repeats the requested version (`compare.json` rules).
  - **Consequence:** "8/8 match" is a negative-control pass. Its only effect on the mechanism question is that it does not trigger the `refuted` clause "any noswiss synthetic label fails" (`decision-rule.json:19`).
- **N2 (operability, LOW): the frozen emulator file is not the raw tool output.**
  - **Observed:** `F:.ufo/waves/round-18/gen-predictions.py:49-50` writes `json.dump(sm, f, …)` with no trailing newline. The tool itself ends its output with `\n` (`tools/swiss-misread.py:1840-1841` at REV).
  - **Observed:** a fresh emulator run hashes to sha `5b318081…5191`, not the `6025f893…c5bb` recorded at `predictions/SHA256SUMS:27`.
  - **Observed:** all 15 frozen `swiss-misread/*.json` files end in `}` with no newline. I re-ran the emulator only for this label.
  - **Consequence:** anyone re-hashing raw emulator stdout gets a false mismatch. Strip the final `\n` or re-serialize before hashing.
  - **Reproduce:** `cmp <(python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier <carrier> --golang-root <typeinfo/golang>) <(git show F:.ufo/waves/round-18/predictions/swiss-misread/s1250-noswiss-methods.json)` prints `EOF on … after byte 8218`.
- **N3 (calibration, LOW): `analyzer_errors_empty: true` does not mean the log has no errors.**
  - **Observed:** the field covers only ERROR records from `Golang*` components (`log-extract.py:243` at REV).
  - **Observed:** the log holds 5,705 ERROR records: 5,700 `ERROR (GoFuncData) Failed to add source file mapping` (from `LOG:184`) and 5 `DWARFDataTypeImporter` (`LOG:107-111`).
  - **Observed:** `GoFuncData` is not in `GO_COMPONENTS` (`log-extract.py:74`), so those records are also missing from `go_lines`.
  - **Observed:** the `s1250-noswiss-nomethods` log has the same counts (5700/5), and both s1250 swiss logs have 5816/5. These records vary by carrier family, not with the methods variant.
  - **Consequence:** this is not a mismatch; it is a caveat for anyone reading the field name.
- **N4 (residual, INFO): the log is cut off at the end.**
  - **Observed:** the retained log ends at `LOG:5937`, `ANALYZING changes made by post scripts`; the receipt says the polling copy can miss the tail (`receipt.json:24`). All four s1250 synthetic logs end on that same line.
  - **Observed:** in all three D-label logs, `Go analysis failure` comes before `REPORT: Analysis succeeded`: calib-aether 97 < 238, s1246-swiss-nethttp 408 < 498, real-kimi-webbridge 73 < 257. This log reaches `Analysis succeeded` at 5931.
  - **[INFERENCE]** The phase where failures appear is fully captured here.
- **N5 (gate scope, INFO): the binding gate does not cover the observation or compare files.**
  - **Observed:** `decision-rule.json:2` and `receipt-validate.py` do not tie `observation.json` or `compare.json` to the retained log (`git show REV:.ufo/waves/round-17/tools/receipt-validate.py | grep -c -E 'observation|compare\.json'` gives 0).
  - **Consequence:** for this label, the byte-identical R1/R2 re-derivations close that gap. For the other labels it remains a residual risk.

## Depth: cross-label signal (outside this label's verdict)
- **Observed (method-info fix counts):** log line `GolangSymbolAnalyzer Fixed N Go function signatures from method info`; shown as methods − nomethods.
  - s1250-noswiss: 134 − 132 = **+2**
  - s1246-noswiss: 133 − 131 = **+2**
  - s1250-swiss: 132 − 131 = **+1**
  - s1246-swiss: 131 − 130 = **+1**
- **Observed (type counts):** `Found N Go types` is +2 in all four pairs.
- **Observed (frozen emulator, per type):**
  - For `*main.Counts` in this label, H0 and H1 both predict `mcount 2` at 0x4ABA18, which is the map type at 0x4AB9C0 plus 0x58.
  - For `s1250-swiss-methods`, H0 predicts `mcount 2`, but H1 predicts `mcount 0, pkg_path 24` read 24 bytes early, with outcome `silent`.
  - The carrier source `carriers/src/methods/main.go` declares exactly two methods, `Keys` and `String`.
- **[INFERENCE]** This label's +2 fits Ghidra reading the named map type's method table intact, which is what the prediction says.
- **[INFERENCE]** The swiss +1 is directionally what H1's silent misread predicts. The frozen compare fields cannot see this, so the synthetic swiss-methods labels are not diagnostic under the frozen rule, while the method-info count may be. One possible reason the swiss delta is +1 rather than 0 is that `String` is recovered through the `fmt.Stringer` itab; this is untested.
- **Reproduce:** `cd .ufo/waves/round-18/runs && for l in s1250-{noswiss,swiss}-{methods,nomethods} s1246-{noswiss,swiss}-{methods,nomethods}; do grep -oE 'Fixed [0-9]+ Go function signatures from method info' $l/logs/*/ghidra.log; done`.

## Residual risk / verification gaps
- The freeze-before-run order rests on lane-local evidence only (commit dates, reflog, receipt pins). There is no external timestamp.
- I did not inspect Ghidra's markup for `main.Counts` directly, because analyze and decompile are out of bounds. The method-table claim above relies on log counts and the emulator only.
