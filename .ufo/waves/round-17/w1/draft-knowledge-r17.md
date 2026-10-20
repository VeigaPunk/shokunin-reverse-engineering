source: S003 in `corpus/SOURCES.md` — installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`), members `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`, `rtti/GoApiSnapshot.java`, `GoVer.java`, `GoVerRange.java`, `GoBuildInfo.java`, `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java`, `structmapping/DataTypeMapper.java`; S023 for the installed `go1.25.0.json` identity only (`go1.23.0.json` identity observed by `sha256sum` 2026-10-20, not in S023); S004 contrast only, upstream not installed: https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 (anchor: commit `385e8cd9`, `GoRttiMapper.java` diff); carriers `/usr/bin/shfmt` and `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild`; PILOT logs `.ufo/waves/round-17/pilot/`.
verified-at: 2026-10-20 — DRAFT. Source anchors, `inspect-go-binary` metadata and source-model selection were observed on 2026-10-20; the analyze logs are PILOT only, not final measured runs. <FINAL:verified-at date of the final carrier runs>
recheck: `sha256sum /usr/bin/shfmt /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` and compare with the digests in this entry; `npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json`; `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request 1.27.0 --goos linux --goarch amd64`; reopen the named archive members. <FINAL:recheck argv for carrier-run.py, log-extract.py, predict.py and compare.py with retained receipt paths>

# Go carrier diagnostics — analyzer-log predictions against observed Ghidra Go messages

**DRAFT status.** This is the author-side draft for round 17 (kaidoku, hyaku phase 2). Final carrier runs are pending. Every number marked PILOT comes from `.ufo/waves/round-17/pilot/` and is not a retained receipt. Every `<FINAL:...>` slot must be filled by the producing tool's output, never by hand.

## Question

For two real Go carriers, does Ghidra's Go analyzer log match what the installed Ghidra 12.1.4 source predicts for three fields: the untested-version flag, the snapshot label, and the missing-bootstrap flag? Does the retained log expose the failure route that `r14` described only as source reasoning?

## Carriers and pins

| carrier | path | SHA-256 | size (bytes) | Go version per REA (`inspect-go-binary`) | source of identity |
|---|---|---|---|---|---|
| shfmt | `/usr/bin/shfmt` | `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459` | 3601168 | `go1.27.0-X:nodwarf5` | OBSERVATION: `inspect-go-binary` run 2026-10-20, evidence `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`; `.ufo/waves/round-17/pilot/README.txt:5-6` |
| esbuild 0.25.12 | `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild` | `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014` | 10358936 | `go1.23.12` | OBSERVATION: `inspect-go-binary` run 2026-10-20, evidence `ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626` |

- OBSERVATION: the esbuild path is a mutable pnpm install directory under another project. The SHA-256 pin is the identity; the path alone is not (QUALITY #4).
- OBSERVATION: the Ghidra log names the target only by hash prefix: `target-58f765638eed.bin` (shfmt, `pilot/shfmt-log/ghidra.log:82`) and `target-bab29b2ca7a9.bin` (esbuild, `pilot/esbuild-0.25.12-log/ghidra.log:62`). The binding to the carrier therefore runs through the SHA-256 pin, not through the log's own file name.
- UNKNOWN: whether any retained pre/post pins existed for the pilot. The pilot README states that pins were not recorded (`pilot/README.txt`, last lines).
- Provider identities: `rea-agents@6.5.0`; provider `rea-workflow` v1 over upstream Ghidra 12.1.4 (`pilot/esb.json` and `pilot/shfmt.json`, `analysis_profile.parameters.upstream_analysis_profile`); Go metadata provider `go-build-info` v1 (inspect output). Ghidra's installed Base archive is pinned above; the JDK version was not examined.

## Source-derived predictions

Anchors below are the S003 members named in `source:`. Each is opened and read in this draft.

1. **Version normalization.** `GoBuildInfo.java:488-489` strips a leading `go` from the build-info string. `GoVer.java:65` then applies `replaceAll("[^.0-9].*$", "")`, which drops everything from the first character that is neither a dot nor a digit. Result: `go1.27.0-X:nodwarf5` → `1.27.0`; `go1.23.12` → `1.23.12`.
   - INFERENCE, checked by re-evaluating the same regular expression: applying the `GoVer.java:65` rule to the literal `go1.27.0-X:nodwarf5` yields the empty string and therefore `GoVer.INVALID` (`GoVer.java:67-68`). The `go` strip at `GoBuildInfo.java:488-489` must run first. A predictor that skips it would report a parse failure for every real carrier, not a version.
2. **Range.** `GoRttiMapper.java:79` declares `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`. `GoVerRange.java:83-86` tests `start <= ver <= end`, with wildcard patch compared as equal (`GoVer.java:149`). So `1.27.0` is outside the range and `1.23.12` is inside.
3. **Untested message.** `GoRttiMapper.java:170-172` logs `Msg.error("Untested Go version [%s]")` and continues. There is no throw or return. Prediction: the ERROR line appears for `1.27.0` and does not appear for `1.23.12`.
4. **Snapshot selection.** `GoApiSnapshot.java:118-128` requests the base file at patch 0 and returns null if it is absent. `:115` then returns `GoApiSnapshot.EMPTY`. `GoApiSnapshot.java:148-166` searches downward for the patch diff only when a base exists.
   - Installed bases in `.../data/typeinfo/golang/`: `go1.15.0.json` through `go1.25.0.json` (listing, observed 2026-10-20). There is no `go1.26.0.json` or `go1.27.0.json`.
   - SOURCE-MODEL: `.ufo/waves/round-16/selection.py` run 2026-10-20 with `--request 1.27.0 --goos linux --goarch amd64` returned `status: missing_base`, `base: null`, `selected_diff: null`, `patch_applied: false`, `evidence_class: source_model`.
   - SOURCE-MODEL: the same tool with `--request 1.23.12` returned `status: exact_diff`, base `go1.23.0.json` (size 9368866, SHA-256 `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692`), diff `patchverdiffs/go1.23.12.json.diff` (size 111215, SHA-256 `e1fdbc7e690cf6a1bb7c56969c2308ecc51a532daf6b1c7e8cd4dab3b7a99c53`), `selected_patch: 12`.
   - The `patch_applied: false` field is part of the model. Neither result says that the Java loader applied a diff.
5. **Bootstrap failure.** `GoRttiMapper.java:351-367` calls `registerStructures`. An `IOException` on an invalid snapshot becomes `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")` (`:356-360`). `GoRttiMapper.java:114-125` catches it, logs at WARN, and returns null. `GolangSymbolAnalyzer.java:133-137` then logs `Go symbol analyzer error: unable to get GoRttiMapper` and returns false. `DataTypeMapper.java:172-181` is the structure-lookup throw that starts the chain.
   - `GolangSymbolAnalyzer.java:139` (`Go version %s`) comes after the early return. Prediction: no `Go version` line for a carrier that fails at `:133-137`.
6. **Prediction table** (the same values are carried into `compare.py`):

| carrier | `untested_version` | `snapshot_label` | `missing_bootstrap` | classification (`log-extract` rule) |
|---|---|---|---|---|
| shfmt `1.27.0` | `1.27.0` | null | true | `bootstrap_missing` |
| esbuild `1.23.12` | null | `1.23.12` | false | `snapshot_loaded` |

## PILOT observations (not final)

Pilot argv and logs are in `pilot/README.txt`. The shfmt run used `analyze /usr/bin/shfmt --format json`; the esbuild run used the same verb on the path above. Both exited 0 (`pilot/shfmt.exit`, `pilot/esb.exit`). The log hashes match `pilot/SHA256SUMS`.

**shfmt (`pilot/shfmt-log/ghidra.log`):**

- OBSERVATION `:83` `ERROR (GoRttiMapper) Untested Go version [1.27.0]`
- OBSERVATION `:84` `WARN (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.`
- OBSERVATION `:85` `ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper`
- OBSERVATION `:86-89` the same route runs again for `GolangStringAnalyzer`: `:87` untested, `:88` missing bootstrap, `:89` `Go string analyzer error: unable to get GoRttiMapper`.
- OBSERVATION: no `Using Go API snapshot` line and no `Go version` line appear in lines 82-89.
- OBSERVATION: `script.log` records `REA no-return fix: cleared=2 sites=3274 refit=952` (`pilot/shfmt-log/script.log`, line 1).
- OBSERVATION: `binary_overview` returned `procedure_count: 2581`, `string_count: 7813`, `segment_count: 38` (`pilot/shfmt.json`, `normalized_result`).
- UNKNOWN: whether these Ghidra default-analysis counts include any Go recovery. The log shows the Go analyzers failing, so they should not be read as Go-function recovery.

**esbuild (`pilot/esbuild-0.25.12-log/ghidra.log`):**

- OBSERVATION `:63` `INFO (GoApiSnapshot) Using Go API snapshot for 1.23.12`
- OBSERVATION `:64` `INFO (GoRttiMapper) Using Go API snapshot for version 1.23.12`
- OBSERVATION `:67` `INFO (GolangSymbolAnalyzer) Go version 1.23.12`
- OBSERVATION: no `Untested` line and no `Missing Go bootstrap` line.
- OBSERVATION, not predicted: `:68-70` three `WARN (GoTypeManager) Failed to get subtype …` lines (for `runtime.elfSym`, `byte`, `uint16` subtypes). UNKNOWN cause. They are reported here and not hidden.
- OBSERVATION, not predicted: `:65-66` `Discovered 188 unindexed Go types` and `Found 4881 Go types`; `:80` callsite fixup `9908/9798/2`; `:85` `Go missing type names: 19`; `:83` `Go strings found: 6264`.
- OBSERVATION, not Go: `:77-79` `ERROR (GifDataType)` and `ERROR (PngDataType)` lines. They fall outside the `log-extract` Go component filter and are excluded from Go diagnostics.
- OBSERVATION: `script.log` records `REA no-return fix: cleared=12 sites=2035 refit=1115`.
- OBSERVATION: `binary_overview` returned `procedure_count: 8109`, `string_count: 17573`, `segment_count: 16` (`pilot/esb.json`).

**Log binding.** Both runs logged the Ghidra runtime root `/tmp/rea-ghidra-<random>/ghidra.log` (`pilot/shfmt-log/ghidra.log:2`, `pilot/esbuild-0.25.12-log/ghidra.log:2`). REA removes that root at session close (`pilot/README.txt`), so the copies in this lane are the only retained copies. Copies were made by 1-second polling, and the README says the last copy can miss lines written after the final poll.

## Prediction-vs-observation table

PILOT columns are hand-read from the logs above, not produced by `compare.py`. FINAL columns are slots for the producing tools.

**shfmt `1.27.0`**

| field | predicted (source / selection) | PILOT observed (hand-read) | FINAL observed (`log-extract.py`) | FINAL `compare.py` | label |
|---|---|---|---|---|---|
| `untested_version` | `1.27.0` (`GoRttiMapper.java:170-171`) | `1.27.0` (`:83`, `:87`) | `<FINAL:untested_versions>` | `<FINAL:match>` | predicted: INFERENCE from source; observed: OBSERVATION |
| `snapshot_label` | null (selection `missing_base`) | null (no snapshot line) | `<FINAL:snapshot_labels>` | `<FINAL:match>` | predicted: SOURCE-MODEL; observed: OBSERVATION (absence of a line) |
| `missing_bootstrap` | true (`GoRttiMapper.java:356-360`) | true (`:84`, `:88`) | `<FINAL:missing_bootstrap>` | `<FINAL:match>` | predicted: INFERENCE from source; observed: OBSERVATION |
| classification | `bootstrap_missing` | by hand: `bootstrap_missing` | `<FINAL:classification>` | n/a | INFERENCE from the contract rule |
| `analyzer_errors` | two messages, from `GolangSymbolAnalyzer` and `GolangStringAnalyzer` (`GolangSymbolAnalyzer.java:133-137`) | `:85`, `:89` | `<FINAL:analyzer_errors>` | n/a | predicted: INFERENCE; observed: OBSERVATION |
| `go_version_logged` | empty (early return precedes `:139`) | empty | `<FINAL:go_version_logged>` | n/a | INFERENCE from source ordering |

**esbuild `1.23.12`**

| field | predicted (source / selection) | PILOT observed (hand-read) | FINAL observed (`log-extract.py`) | FINAL `compare.py` | label |
|---|---|---|---|---|---|
| `untested_version` | empty | empty | `<FINAL:untested_versions>` | `<FINAL:match>` | predicted: INFERENCE from range; observed: OBSERVATION |
| `snapshot_label` | `1.23.12` (`GoRttiMapper.java:180`, base `go1.23.0.json`, diff patch 12) | `1.23.12` (`:63-64`) | `<FINAL:snapshot_labels>` | `<FINAL:match>` | predicted: SOURCE-MODEL; observed: OBSERVATION |
| `missing_bootstrap` | false | false (no WARN line) | `<FINAL:missing_bootstrap>` | `<FINAL:match>` | predicted: INFERENCE; observed: OBSERVATION |
| classification | `snapshot_loaded` | by hand: `snapshot_loaded` | `<FINAL:classification>` | n/a | INFERENCE from the contract rule |
| `go_version_logged` | `1.23.12` (`GolangSymbolAnalyzer.java:139`) | `1.23.12` (`:67`) | `<FINAL:go_version_logged>` | n/a | predicted: INFERENCE; observed: OBSERVATION |
| unpredicted `GoTypeManager` WARNs | not predicted | three WARN lines (`:68-70`) | `<FINAL:count>` | n/a | UNKNOWN cause; reported, not scored |

**Mismatches are reported, not hidden.** Any `compare.py` mismatch, any unpredicted Go-component line, and any missing expected line goes into the FINAL table as is.

**Retained receipt slots (per carrier).**

- `<FINAL:carrier path + SHA-256 pre/post>`
- `<FINAL:REA evidence_id from analyze stdout>`
- `<FINAL:retained ghidra.log path and SHA-256, polls, last_copy_utc>`
- `<FINAL:script.log path and SHA-256>`
- `<FINAL:argv, cwd, exit, stdout/stderr SHA-256 for inspect-go-binary, analyze and each search>`
- `<FINAL:receipt-validate.py exit>`

## Observation, inference and unknown labels

- OBSERVATION: the log lines, anchors, hashes and REA metadata quoted above, each traceable to the cited file and line.
- INFERENCE: the predicted `bootstrap_missing` route for shfmt is the source reading of `GoRttiMapper.java:351-367`, `:114-125` and `GolangSymbolAnalyzer.java:133-137`. It is consistent with the PILOT log, but the PILOT log does not prove the control flow.
- INFERENCE: the `missing_base` status is one cause of an invalid snapshot. The same message can also come from a present file with no applicable records, since `GoApiSnapshot.java:503-505` tests `arches.isEmpty()`. The pilot log cannot separate these two causes, and no `go1.27` base file is installed to test the first.
- UNKNOWN: why the same bootstrap route runs under two analyzers (`:82-85` and `:86-89`). The shared-binary cache path was not read in this draft.
- UNKNOWN: the cause of the esbuild `GoTypeManager` subtype WARNs (`:68-70`).
- UNKNOWN: the completeness of the log copies (see the polling limit above).

## Corrections to the earlier entries

- Consistent with `2026-10-20-r14-go-version-diagnosis.md`: the source anchors `GoRttiMapper.java:79`, `:170-172`, `:351-367`, `:114-125`, `GolangSymbolAnalyzer.java:133-137` and `GoApiSnapshot.java:115`, `:122-126`, `:148-166`, `:503-505` were reopened and match the text quoted there.
- Not previously stated: the r14 rule that a missing bootstrap file yields EMPTY is consistent with `GoApiSnapshot.java:122-126`. The version normalization step in INFERENCE item 1 above is new and is a precondition for any predictor.
- The r4-10 causal attribution remains superseded as stated in r14; this entry adds no historical claim.

## NOT examined

- Final measured runs. Every PILOT value above is pending FINAL.
- Any target execution. Carriers are never run (contract). The REA `analyze` workflow was run only in the PILOT, not in this draft.
- Go symbol recovery. No `search`, `decompile`, function-level comparison, or Go function name count was taken. `procedure_count` and `string_count` are observed but are not Go-recovery evidence.
- Other carriers. go1.20.12 esbuild builds named in the claims were not inspected in this draft.
- Other platforms. Only linux/amd64 was requested; darwin, windows, riscv64 and arm64 selections were not examined in this entry.
- Upstream support. S004 (GP-6528, range `1.15-1.26`) is named as the contrast only. Nothing here checks an upstream or released Ghidra build.
- Bundle sufficiency. Changing the range alone, or adding a snapshot alone, is not tested (S004 notes the upstream change is a bundle).
- Ghidra class identity. The S003 source archive is not authenticated against the classes the installed provider loads (r14 limitation, unchanged).
- Pin coverage of the pilot. No pre/post pins were recorded for either pilot carrier.
- Log completeness. Lines written after the final 1-second poll may be missing (`pilot/README.txt`).
- Python source model fidelity. `selection.py` models file selection, not Java/Gson parsing; base-file parse and record usability were not checked.
- `GoRttiMapper.getSharedGoBinary` caching and the second analyzer pass (UNKNOWN above).
- The REA `ReaGhidraNoReturnFix` script's effect on Go analysis (observed only in `script.log`).
- JDK version and Ghidra launch flags.
