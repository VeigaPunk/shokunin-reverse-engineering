# Scout — GolangSymbolAnalyzer / GolangStringAnalyzer: error lines and count semantics

Seat: KaidokuR17.ScoutGolangAnalyzers-3 (advisory, read-only). Axes: calibration, depth.
Source: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
(members cited as `Base-src.zip:<member>:<line>`). Installed tree: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`.
Observed runs: `.ufo/waves/round-17/pilot/{esbuild-0.25.12-log,shfmt-log}/ghidra.log` (pilot, not measured runs).
Labels: **OBSERVED** = read in a file; **INFERENCE** = derived from source, not executed.

## 1. Anchors (exact, verified by extraction)

| Anchor | Path:line |
|---|---|
| `Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper")` | `Base-src.zip:ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:135` |
| same message, string analyzer | `Base-src.zip:ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java:105` |
| `Marked %d Go funcs as NoReturn` | `GolangSymbolAnalyzer.java:327` |
| `Fixed %d Go function signatures from runtime snapshot signatures` | `GolangSymbolAnalyzer.java:328-329` |
| `Fixed %d Go function signatures from method info` | `GolangSymbolAnalyzer.java:330-331` |
| `Go strings found: %d` | `GolangStringAnalyzer.java:128` |
| `Go version %s` | `GolangSymbolAnalyzer.java:139` |
| `Go analysis already performed, skipping.` | `GolangSymbolAnalyzer.java:120` |

Absolute paths for the two analyzers when unzipped:
`…/Base-src.zip:ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` and `…/GolangStringAnalyzer.java`.
The archive lists them under `ghidra/app/plugin/core/analysis/` (`unzip -l`, 14422 B / 52666 B, 2026-09-21 16:12).

Adjacent message vocabulary that a log-extract must key on (BootstrapInfoException path):
`Missing Go bootstrap type info, unable to extract Go RTTI info.` — `GoRttiMapper.java:358-360`;
`Untested Go version [%s]` — `GoRttiMapper.java:171`;
`Using Go API snapshot for version %s` — `GoRttiMapper.java:179-180`;
`Using Go API snapshot for %s` / `Falling back from %s to %s for Go API snapshot` — `GoApiSnapshot.java:163` / `:159-160`;
`Go missing type names: N` — `GoRttiMapper.java:373`.

## 2. Why the two error lines appear (source chain)

- `canAnalyze` is `GoRttiMapper.isGolangProgram` (`GolangSymbolAnalyzer.java:105-107`, `GolangStringAnalyzer.java:94-96`), i.e. the program's compiler-spec name equals `"golang"` (`GoConstants.java:26`, `GoRttiMapper.java:196-199`). The program can therefore be marked Go while Go RTTI extraction still fails.
- `getSharedGoBinary` (`GoRttiMapper.java:102-129`) calls the supplier; `getGoBinary` returns `null` for "probably not a Go binary" (`:160-163`), throws `BootstrapInfoException` for an invalid version string (`:167-168`) or a missing type snapshot (`:356-360` inside `initStructMappings`, reached though `supplier_result.init(monitor)` at `:110`). The exception is caught at `:114-117` (warn + `logAnalyzerMsg`), and `getSharedGoBinary` returns null → each analyzer logs its own error and returns false.
- **Null is not cached**: `TransientProgramProperties.getProperty` returns early when the supplier yields null (`TransientProgramProperties.java:108-111`), so *every* analyzer pass repeats the full bootstrap attempt, including the pclntab search (`GoRttiMapper.java:1116-1139`). **INFERENCE**, confirmed below by observation.
- Only the symbol analyzer has a re-entry guard (`lastTxId` at `:112-117`, persisted flag `isAlreadyAnalyzed` `:119-122` / `:1356-1359`). The string analyzer has none (`GolangStringAnalyzer.java:99-107`), so it always attempts, even when symbol analysis was skipped.
- The symbol analyzer sets `ANALYZED_FLAG_OPTION_NAME` only on success (`:178-179`), so a failed run retries in a later analysis session.

## 3. Observed confirmation (pilot, direct)

shfmt, `go1.27.0-X:nodwarf5` — `shfmt-log/ghidra.log:82-89` (OBSERVED):
```
82 INFO  (GoRttiMapper) Reading Go binary info: target-58f765638eed.bin
83 ERROR (GoRttiMapper) Untested Go version [1.27.0]
84 WARN  (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.
85 ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper
86 INFO  (GoRttiMapper) Reading Go binary info: target-58f765638eed.bin   (+10 s)
87 ERROR (GoRttiMapper) Untested Go version [1.27.0]
88 WARN  (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.
89 ERROR (GolangStringAnalyzer) Go string analyzer error: unable to get GoRttiMapper
```
This is exactly the source-predicted cascade: two independent bootstrap attempts, one error line each, 10 s apart. **The two error lines are one failure, not two.**

esbuild, `go1.23.12` — `esbuild-0.25.12-log/ghidra.log:62-88` (OBSERVED), in order:
`Reading Go binary info` (62) → `Using Go API snapshot for 1.23.12` (63, `GoApiSnapshot`) →
`Using Go API snapshot for version 1.23.12` (64, `GoRttiMapper`) → `Go version 1.23.12` (67) →
`Marked 61 Go funcs as NoReturn` (71) → `Fixed 2248 … snapshot` (72) → `Fixed 2055 … method` (73) →
`Go RTTI callsite fixup 9908/9798/2` (80) → `closure/method wrapper types found 174/14` (81) →
`closure/method wrapper funcs fixed 214/16` (82) → `Go strings found: 6264` (83) →
`Go missing type names: 19` (85).

Two calibration facts fall out:
- `Go version` prints **without** the `go` prefix (esbuild:67 `1.23.12`, shfmt:83 `[1.27.0]`): `GoBuildInfo` strips `go` (`GoBuildInfo.java:488-489`) and `GoVer.toString` is `%d.%d.%d` (`GoVer.java:154-159`); `GoVer.parse` also truncates at the first non-`[.0-9]` char (`GoVer.java:62-81`), which is why `1.27.0-X:nodwarf5` appears as `1.27.0`. A regex expecting `go1.23.12` will silently miss.
- `Missing Go bootstrap type info…` carries **no version** (the `.formatted(goVer)` at `GoRttiMapper.java:360` is a no-format no-op). Version must come from the neighbouring `Untested Go version` or `Go version` line — and in the failure case only `Untested` exists.

## 4. Count semantics — which counts are meaningful observations

**No count has a denominator in the log.** Nothing prints the funcdata table size (`getAllFunctions` `GoRttiMapper.java:1112-1114`), so all function counts are raw integers comparable only within one carrier and one first-analysis pass.

### 4.1 `Marked N Go funcs as NoReturn` (`GolangSymbolAnalyzer.java:327`) — meaningful, with one trap
Computed at `:322-324` from the flip test at `:244` / `:322`. It counts *newly* NoReturn funcs over the processed loop, and the flip can come from **two** sources:
1. name match against `data/GolangFunctionsThatDoNotReturn` (`:316-320`, file read at `:498-513` via `noReturnFunctionConstraints.xml:3-4`), and
2. the snapshot funcdef's own NoReturn flag applied inside `GoFunctionFixup.apply` (`GoFunctionFixup.java:193-194`; flag built at `GoRttiMapper.java:950-951`).

Excluded from N: funcs skipped at `:239-242` (no function created, or signature source higher priority than `IMPORTED`, i.e. user-defined — priority order `USER_DEFINED > IMPORTED > ANALYSIS/AI > DEFAULT`, `SoftwareModeling-src.zip:ghidra/program/model/symbol/SourceType.java:27-35,44-65`), and funcs already NoReturn before this run.
The name file holds **116 non-comment, non-blank names** (124 newline-terminated lines = 116 names + 2 comment lines + 6 blank lines; no duplicates — `wc -l` and `awk 'NF && $0 !~ /^#/' | uniq -d` on `…/Features/Base/data/GolangFunctionsThatDoNotReturn`, OBSERVED). Observed N=61 for esbuild. So "61" is **not** "61 of 116 recovered"; the log cannot decompose the other 55 (absent `.abi0` variants, already flagged, or skipped at 239-242). A knowledge entry should state 61/116 as an upper-bound-relative fraction and mark the decomposition unresolved.

### 4.2 `Fixed N … snapshot` (328) and `Fixed N … method` (330) — meaningful as *provenance* counts, not as "fixed"
- Provenance flags are single-valued per result: `EnumSet.of(FROM_RTTI_METHOD)` (`GoRttiMapper.java:838`) and `EnumSet.of(FROM_SNAPSHOT)` (`:902`); the record carries one flag set (`GoRttiMapper.java:642-644`). Counters at `:280-285` are therefore **disjoint**, and `2248 + 2055 = 4303` is a valid count of funcdef-results with those two provenances (OBSERVED numbers).
- They are incremented **before** application (`:280-285` precede `:287-300`), and application is skipped entirely for ASM funcs (`funcdata.getFlags()` non-empty, `:287`) and aborted with a warning on `DuplicateName/InvalidInput/IllegalArgument` (`:294-299`). **INFERENCE:** "Fixed" can over-count; the delta is only visible as per-function `Failed to update function signature` warnings (`:296-297`), never as a number.
- The counters miss every other provenance: closure/method-wrapper (`:702-707`), dot-equals/hash (`:676-681`), missing-info (`:716`, flags `PARAMS_MISSING|RETURN_INFO_MISSING`, `:859`). So `0/0` does **not** mean no signature work happened; and `snapshot+method` is not "the number of signatures fixed".
- Recommended reformulation in a knowledge entry: *"…funcdefs sourced from snapshot / RTTI method info"*, with the over-count caveat, not "fixed".

### 4.3 `Go strings found: N` (`GolangStringAnalyzer.java:128`) — meaningful only as an intra-carrier marker
- Counts (a) distinct string structs newly created per data reference (`:186-190`) plus (b) inline `(ptr,len)` strings with no struct body (`:196-203`) plus (c) data-segment scan hits (`:282-288`). Slice hits are counted but **not** logged (`sliceCount` only in the monitor message, `:287-288`; final line prints `stringCount` only).
- `canCreateStructAt` refuses already-defined data (`:363-367`), so a *second* analysis of the same program (data already defined) yields a much smaller N — hence not comparable across runs. A new analysis session with the persisted `Golang Analyzed` flag set prints only `Go analysis already performed, skipping.` (`GolangSymbolAnalyzer.java:120`) while the string analyzer still runs and logs a near-zero count. **INFERENCE** from `:119-122` + `:363-367`.
- `IOException` in the string phase is caught and the method still returns true (`:124-130`), so N can be a partial count with only a `Go analysis failure` error beside it.

### 4.4 Counts to prefer for depth (observed, currently unmentioned in the contract's log-extract)
These are printed by the same session and are strictly richer than the three headline counts, because each carries a total/denominator:
- `Go RTTI callsite fixup info (total/updated/skipped): 9908/9798/2` — `GolangSymbolAnalyzer.java:1110-1111`.
- `Go closure/method wrapper types found: 174/14` and `…funcs fixed: 214/16` — `:882-885`.
- `Go missing type names: 19` — `GoRttiMapper.java:373`, printed at `close()`.
- `Found 4881 Go types` / `Discovered 188 unindexed Go types` — `GoTypeManager` (esbuild:65-66), a type-space denominator.

### 4.5 What is *not* a meaningful observation
- Counting `analyzer_errors` occurrences: 2 lines = 1 root cause (§3).
- Absence of the three count lines ⇒ **not** zero: they are emitted at the end of `markupGoFunctions` (`:327-331`), which throws `IOException`/`CancelledException` (`:213`); a cancel/exception leaves no line (§4.2's `continue` paths are per-function, but a throw skips the trio).
- `Go strings found` as a literal-string count (it is a struct/inline-char-array count, §4.3).

## 5. Recommendation for the knowledge entry

Rank the observation table by information per line:

1. **Bootstrap outcome block** (highest): the presence/order of `Reading Go binary info` ×2, `Untested Go version [X]`, `Missing Go bootstrap type info…`, and one error per analyzer. This is the falsifiable prediction for C2's out-of-range carrier; the pilot already matches it (`shfmt-log/ghidra.log:82-89`).
2. **Snapshot identity**: `Using Go API snapshot for version X` (`GoRttiMapper.java:179-180`) equals the *requested normalized* version (constructed with `read(..., goVer)` `GoApiSnapshot.java:239`), so it matches `predict.py`'s `snapshot_label` by construction; the *distinct* `GoApiSnapshot` line (`:163`) and the `Falling back from A to B` warn (`:159-160`) reveal patch-diff coverage and are currently absent from the log-extract contract — worth a fourth compared field if L1 wants it.
3. **Yield counts with semantics as §4.1/§4.2** (61 / 2248 / 2055 on esbuild), plus the denominator-free caveat and the "Fixed ≠ applied" caveat.
4. **Richer denominators** (§4.4) if the entry wants ratios rather than raw integers.

## 6. Remaining unknowns (bounded)

- Whether any esbuild funcdef application actually failed (`:296-297` warnings) — the pilot log has no `Failed to update function signature` line, but the copy is poll-truncated (README.txt) and failures are per-function WARNs, so absence is weak. **UNRESOLVED.**
- The funcdata total for esbuild (no log line); would need an external count, which this seat may not produce (no REA analyze/search).
- Whether REA 6.5.0 reuses a program across runs (`Golang Analyzed` flag) — affects whether a second retained run can show the trio at all. **UNRESOLVED** from source alone.
- `GoVerRange` treats `1.15-1.25` at minor granularity via wildcard patch (`GoVerRange.java:42-57`, `GoVer.java:149`), so `1.25.99` is "tested" and `1.26.0` is not, independent of snapshot availability. No contradiction with observation, but a 1.26 carrier would show `Untested` *and* bootstrap failure for a different reason (missing base json) — a distinction the log preserves only via line order.

## 7. Tooling / side effects

Read-only. No installs, no REA analyze/search/decompile, no Ghidra, no carrier execution. Only file written: this report.
