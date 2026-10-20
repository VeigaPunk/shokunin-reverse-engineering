# ScoutLogFirstFailures — first Go-analysis failure in every bound Ghidra log (oracle for `W20/tools/first-failure-extract.py`)

- Seat `KaidokuR20.ScoutLogFirstFailures-2` (leaf; no subagents). Written `2026-10-20T17:52:34-03:00` (clock read at write time, §8 C23).
- Axes: depth (C3 oracle), calibration (predicate traps), coverage (all 31 bound logs, both round-19 passes + round-18).
- Method: `grep -n` only for log text, `wc -l` for counts; Ghidra 12.1.4 **source** read from the installed `*-src.zip` only to name exception semantics. No REA, no Ghidra run, no Go-toolchain run, no installs (nothing installed, nothing to record).
- Path form: `.ufo/waves/round-1[89]/runs/[pass2/]<label>/logs/<id>/ghidra.log`. Tables give `wave · pass · label · id`, which fully determines the path; line columns are exact `:line` anchors into those files.
- 31 `ghidra.log` on disk, 31 bound by a `receipt.json` (`retained_logs[*].files["ghidra.log"]`), 31/31 sha256+bytes match the receipt (§6).

## 1. Predicates used (all [OBSERVED] unless marked)

- **GSA** = line matching `ERROR \(GolangSymbolAnalyzer\) Go analysis failure `. Five such lines exist, in five files; the text after the timestamp is byte-identical in all five (line **A**).
- **ATW** = line matching `ERROR \(AnalysisTaskWrapper\) Analysis Task: `. Two such lines, two files (line **B**). The failing task is a **Go** task (`Golang RTTI Propagation (deferred)`) but Ghidra logs it under the wrapper, not under the Go analyzer. Both adjudications are spelled out in §4.
- **Other** = `ERROR (GoFuncData)` GFD · `ERROR (DWARFDataTypeImporter)` DTI · `ERROR (DWARFImportSummary)` DIS · `ERROR (PngDataType)`/`ERROR (GifDataType)` PNG/GIF.
- **`none up to line N`** = the captured file has N lines and contains no GSA line. It is a statement about the captured bytes, not a claim that the analyzer never threw (§7).
- Every line containing `ERROR` in the corpus matches `ERROR (`: 75,530 = 75,530 (§8 C24). No untagged error line; no `FATAL`/`SEVERE`/`OutOfMemory`/`StackOverflowError`/`AssertionError` line anywhere (C24).

### A — GSA failure line (5 logs, identical text; only the timestamp differs)
```
2026-10-20 HH:MM:SS ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException
```

### B — ATW failure line (2 logs, identical text; only the timestamp differs)
```
2026-10-20 HH:MM:SS ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key java.lang.NullPointerException: element cannot be mapped to a null key
```

## 2. The seven failure-bearing logs (verbatim lines, root cause, frames)

| wave · pass | label · log id | lines | failure line (verbatim, timestamp included) | root cause line (verbatim) | Go frame chain (file:line anchors) | sub-phase [OBSERVED], kind [INFERENCE] |
|---|---|---|---|---|---|---|
| r18 · p1 | calib-aether · `rea-ghidra-HtDopV` | 244 | `97: 2026-10-20 13:24:13 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` | `177: Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854` | `:182 GoVarlenString.readFrom(71)` → `:188 GoName.readStructure(95)` → `:194 GoRttiMapper.getGoName(1074)` → `:196 GoName.getPkgPath(124)`; outer: `:124 GoInterfaceType.additionalMarkup(77)`, `:147 GoStructType.additionalMarkup(94)`, `:154 GoTypeManager.markupGoTypes(153)`, `:155 GolangSymbolAnalyzer.added(146)` | markupGoTypes / interface+struct additionalMarkup; kind `eof` (emulator `past_eof`), index 17645861, length 111938854 |
| r18 · p1 | real-kimi-webbridge · `rea-ghidra-ZSUHpG` | 263 | `73: 2026-10-20 13:31:14 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` | `206: Caused by: java.io.EOFException: Invalid index: 15606016` | `:212 GoName.readStructure(94)` → `:218 GoRttiMapper.getGoName(1074)` → `:220 GoName.getPkgPath(124)`; outer: `:100/:114/:176 GoInterfaceType.additionalMarkup(77)`, `:123/:136/:149/:162 GoStructType.additionalMarkup(94)`, `:183 GoTypeManager.markupGoTypes(153)`, `:184 GolangSymbolAnalyzer.added(146)` | markupGoTypes / additionalMarkup; kind `invalid_index`, index 15606016 |
| r18 · p1 | s1246-swiss-nethttp · `rea-ghidra-zHRS1l` | 504 | `408: 2026-10-20 13:29:05 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` | `451: Caused by: java.io.EOFException: Invalid index: 22386945` | `:457 GoName.readStructure(94)` → `:463 GoRttiMapper.getGoName(1074)` → `:465 GoName.getPkgPath(124)`; outer: `:411 FieldMappingInfo.addRefToFieldWithGetter(296)`, `:428 GoTypeManager.markupGoTypes(153)`, `:429 GolangSymbolAnalyzer.added(146)` | markupGoTypes / direct field markup (no additionalMarkup frames); kind `invalid_index`, index 22386945 |
| r19 · p1 | t1250-vet · `rea-ghidra-CSKBVG` | 282 | `186: 2026-10-20 16:06:20 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` | `229: Caused by: java.io.EOFException: Invalid index: 13902080` | `:235 GoName.readStructure(94)` → `:241 GoRttiMapper.getGoName(1074)` → `:243 GoName.getPkgPath(124)`; outer: `:189 FieldMappingInfo.addRefToFieldWithGetter(296)`, `:206 GoTypeManager.markupGoTypes(153)`, `:207 GolangSymbolAnalyzer.added(146)` | markupGoTypes / direct field markup; kind `invalid_index`, index 13902080 |
| r19 · p2 | t1250-vet · `rea-ghidra-PEkTou` | 282 | `186: 2026-10-20 16:30:15 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` | `229: Caused by: java.io.EOFException: Invalid index: 13902080` | identical line numbers to pass 1 (`:235`, `:241`, `:243`, `:206`, `:207`) | same as pass 1 |
| r19 · p1 | t1250-compile · `rea-ghidra-uEQQSP` | 432 | `347: 2026-10-20 16:04:10 ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key java.lang.NullPointerException: element cannot be mapped to a null key` | NPE is on the error line itself: `java.lang.NullPointerException: element cannot be mapped to a null key`; first frame `348: at java.base/java.util.Objects.requireNonNull(Objects.java:259)`, `349: ...Collectors.lambda$groupingBy$53(Collectors.java:1105)` | `:363 GolangSymbolAnalyzer$PropagateRttiBackgroundCommand.getReferencesToRttiFunc(1211)` → `:364 ...lambda$getInformationAboutCallsites$0(1179)` → `:372 ...getInformationAboutCallsites(1183)` → `:373/:374 ...applyTo(1103/1053)` → `:375 AnalysisTaskWrapper.run(660)` | deferred RTTI propagation; kind `null_key` (no index/length in the log) |
| r19 · p2 | t1250-compile · `rea-ghidra-07WMDZ` | 432 | `347: 2026-10-20 16:28:05 ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key java.lang.NullPointerException: element cannot be mapped to a null key` | same text; `348: Objects.requireNonNull(259)`, `349: Collectors.lambda$groupingBy$53(1105)` | identical line numbers to pass 1 (`:363`,`:364`,`:372`,`:373`,`:374`,`:375`) | same as pass 1 |

Note on the two GSA sub-phases (observation): `GoInterfaceType.additionalMarkup(77)`/`GoStructType.additionalMarkup(94)` frames appear only in calib-aether (`:124`,`:147`) and real-kimi-webbridge (`:100`,`:123`); s1246-swiss-nethttp and both vet logs go `GoTypeManager.markupGoTypes` → `MarkupSession.markupFields` → `FieldMappingInfo.addRefToFieldWithGetter(296)` without any outer type `additionalMarkup` frame. An extractor must not require the interface frames to recognise the class.

## 3. Every bound log (31) — first Go-analysis failure or `none up to line N`

Shorthands: GSA/ATW = §1; counts are line counts; "first ERROR" = line number of the earliest `ERROR (` line in that file, with its tag.

| wave · pass | label · id | lines | first Go-analysis failure (GSA) | ATW | other ERROR lines (count) | first ERROR |
|---|---|---|---|---|---|---|
| r18 · p1 | calib-aether · `HtDopV` | 244 | `:97` — A | — | PNG 4, GIF 2 | `:97` GSA |
| r18 · p1 | calib-notesmd-cli · `tpzD5t` | 127 | none up to 127 | — | — | — |
| r18 · p1 | real-kimi-webbridge · `ZSUHpG` | 263 | `:73` — A | — | PNG 1, GIF 2 | `:73` GSA |
| r18 · p1 | s1246-noswiss-methods · `2bOinT` | 5721 | none up to 5721 | — | GFD 5448 (first `:220`), DTI 5, DIS 42 | `:106` DTI |
| r18 · p1 | s1246-noswiss-nethttp · `PBi1r9` | 10242 | none up to 10242 | — | GFD 9779 (first `:409`), DTI 5, DIS 59 | `:176` DTI |
| r18 · p1 | s1246-noswiss-nomethods · `jDVuh0` | 5723 | none up to 5723 | — | GFD 5448 (first `:222`), DTI 5, DIS 42 | `:107` DTI |
| r18 · p1 | s1246-swiss-methods · `mXzzav` | 5828 | none up to 5828 | — | GFD 5554 (first `:221`), DTI 5, DIS 42 | `:105` DTI |
| r18 · p1 | s1246-swiss-nethttp · `zHRS1l` | 504 | `:408` — A | — | DTI 5, DIS 59 | `:174` DTI |
| r18 · p1 | s1246-swiss-nomethods · `nUpjsE` | 5829 | none up to 5829 | — | GFD 5554 (first `:222`), DTI 5, DIS 42 | `:106` DTI |
| r18 · p1 | s1250-noswiss-methods · `yI43cD` | 5937 | none up to 5937 | — | GFD 5700 (first `:184`), DTI 5 | `:107` DTI |
| r18 · p1 | s1250-noswiss-nethttp · `Tikfv1` | 10516 | none up to 10516 | — | GFD 10103 (first `:359`), DTI 5, DIS 5 | `:174` DTI |
| r18 · p1 | s1250-noswiss-nomethods · `9XZBsW` | 5937 | none up to 5937 | — | GFD 5700 (first `:184`), DTI 5 | `:107` DTI |
| r18 · p1 | s1250-swiss-methods · `KX6ybk` | 6051 | none up to 6051 | — | GFD 5816 (first `:182`), DTI 5 | `:106` DTI |
| r18 · p1 | s1250-swiss-nethttp · `I0vJ0A` | 10651 | none up to 10651 | — | GFD 10240 (first `:357`), DTI 5, DIS 5 | `:173` DTI |
| r18 · p1 | s1250-swiss-nomethods · `4Xh0g3` | 6052 | none up to 6052 | — | GFD 5816 (first `:183`), DTI 5 | `:106` DTI |
| r19 · p1 | t1250-go · `AiWB8A` | 576 | none up to 576 | — | — | — |
| r19 · p1 | t1250-gofmt · `kDM6dB` | 182 | none up to 182 | — | — | — |
| r19 · p1 | t1250-asm · `cWUKB0` | 227 | none up to 227 | — | — | — |
| r19 · p1 | t1250-cgo · `bdYUwH` | 180 | none up to 180 | — | — | — |
| r19 · p1 | t1250-compile · `uEQQSP` | 432 | none up to 432 | `:347` — B | — | `:347` ATW |
| r19 · p1 | t1250-cover · `XVD7qp` | 250 | none up to 250 | — | — | — |
| r19 · p1 | t1250-preprofile · `aURSDn` | 163 | none up to 163 | — | — | — |
| r19 · p1 | t1250-vet · `CSKBVG` | 282 | `:186` — A | — | — | `:186` GSA |
| r19 · p2 | t1250-go · `WJgbct` | 576 | none up to 576 | — | — | — |
| r19 · p2 | t1250-gofmt · `DttY3R` | 182 | none up to 182 | — | — | — |
| r19 · p2 | t1250-asm · `nVeBgA` | 227 | none up to 227 | — | — | — |
| r19 · p2 | t1250-cgo · `vPyu5c` | 180 | none up to 180 | — | — | — |
| r19 · p2 | t1250-compile · `07WMDZ` | 432 | none up to 432 | `:347` — B | — | `:347` ATW |
| r19 · p2 | t1250-cover · `OkHIR2` | 250 | none up to 250 | — | — | — |
| r19 · p2 | t1250-preprofile · `npYN1g` | 163 | none up to 163 | — | — | — |
| r19 · p2 | t1250-vet · `PEkTou` | 282 | `:186` — A | — | — | `:186` GSA |

Totals (observation): 5 GSA logs, 2 ATW logs, 13 logs with zero `ERROR` lines at all (calib-notesmd-cli + all 6 non-failing r19 labels in both passes), 11 GFD-bearing r18 logs, 12 r18 logs with DWARF errors (the 11 GFD logs + s1246-swiss-nethttp), 2 r18 logs with PNG/GIF errors. No file contains both a GSA line and an ATW line; no file contains more than one GSA line.

## 4. ATW adjudication (the one judgement the oracle does not make for you)

Two defensible readings; the extractor must pick one explicitly:

- **(a) tag-strict.** Only GSA lines are "Go-analysis failures". Then the two compile logs answer `none up to 432`, and their `:347` line is reported only as a non-Golang error line (the ticket's own phrasing, "AnalysisTaskWrapper NPE etc.").
- **(b) task-substance.** The task name (`Golang RTTI Propagation (deferred)`) and the frames (`GolangSymbolAnalyzer$PropagateRttiBackgroundCommand.getReferencesToRttiFunc:1211`) make it a Go-analysis failure in the **deferred** phase. Then the compile logs are Go failures with `kind = null_key`, and `index`/`length`/`va` are `null`.

Recommendation: emit both as separate fields (`go_analysis_failure` = (a), `go_task_failure` = (b)) and never merge them silently. If only one field exists, use (b) but with a kind outside the memory-read family; flattening B into `invalid_index`/`eof` would invent a read failure that the log does not contain.

## 5. Rules the corpus forces on `first-failure-extract.py` (each [OBSERVED])

1. **Anchor on the tag+message.** `ERROR (GolangSymbolAnalyzer) Go analysis failure` — never on bare `ERROR`, never on `ERROR (Go`, never on `GoTypeManager` (`GoTypeManager` WARNs occur 89 times across 26 logs, including `:338` in compile *before* the NPE). `ERROR (GoFuncData)` fires 75,158 times (75,155 `Failed to add source file mapping: new entry would overlap entry …`, 3 `…must have the same length as existing entry`, at `s1246-noswiss-nethttp:4983`, `s1250-swiss-nethttp:877`, `s1250-noswiss-nethttp:6922`) in 11 logs, **all eleven with zero GSA failure**; an `ERROR (Go` rule misassigns every one of them.
2. **Anchor ATW on `ERROR (AnalysisTaskWrapper)`.** The bare string also occurs in frames: compile `:375`, vet `:211`. A raw `grep -c AnalysisTaskWrapper` gives 2 (compile) / 1 (vet); only `:347` in compile is an error line.
3. **Never use "the first `ERROR` line".** 12 logs have a non-Go first error: the 11 GFD logs (whose earliest `ERROR` is a DWARF-import complaint) and s1246-swiss-nethttp (first `ERROR` is DTI `:174` while its GSA failure is `:408`). A first-error rule loses the only Go failure in that file, and reports a DWARF complaint as the "first Go failure" in the other eleven.
4. **Read the deepest `Caused by:`, not the header.** The GSA line carries no numbers. Parse end-anchored:
   - `Caused by: java.io.EOFException: Invalid index: ([0-9]+)$` → `kind=invalid_index`, `index=N`, no length.
   - `Caused by: java.io.EOFException: Unable to read past EOF: ([0-9]+), ([0-9]+)$` → `kind=eof` (round-18 emulator spells it `past_eof`), `index=first`, `length=second`.
   Both branches are `MemoryByteProvider.ensureBounds` (`:302` for the `EOFException` invalid-index branch, `:310-312` for past-EOF). The same "Invalid index" text also exists as an `IOException` at `:173` (address-space overflow in `getAddress`), which no log here shows — all five carry the `java.io.EOFException` class, so anchor on that class too. (Source read in §8 C20.) The round-17 extractor already anchors `Invalid index` at end-of-line (`round-17/tools/log-extract.py:114`) — keep that anchor; `Invalid index: 12 (retrying)` must not match (its own selftest line `:607`).
5. **`index` is a virtual address.** The provider is built on `program.getImageBase().getAddressSpace()` whose base is 0 (`round-17/w2/ScoutGhidraEOFIssue.md:40`), so `va = index`. Independent corroboration for 13902080: `round-19/w2/KnowledgeMechanism.md:192-198` — `0x722000 + 0x620100 = 0xD42100 = 13902080`, above the last `PT_LOAD` end `0xB6BD9F`.
6. **Frames separate the read that failed (deterministic, 5/5).**
   - `GoName.readStructure(GoName.java:94)` = the flags byte (source `GoName.java:94` = `flags = context.getReader().readNextUnsignedByte();`) → precedes `Invalid index` (4 logs).
   - `GoName.readStructure(GoName.java:95)` = the name's `GoVarlenString` (source `GoName.java:95`; `GoVarlenString.readFrom:71` = `readNextByteArray(strLen)`) → precedes `Unable to read past EOF` (1 log, calib-aether).
   So `kind` is predictable from the frame, and the frame line number is itself a cheap cross-check.
7. **This line class is not a run failure.** Every one of the 31 logs prints `REPORT: Analysis succeeded for file:` (4 `REPORT:` lines each), including all seven failure logs: calib-aether `:238`, real-kimi-webbridge `:257`, s1246-swiss-nethttp `:498`, compile `:426`, vet `:276` (pass-2 compile `:426`, pass-2 vet `:276`). The analyzer exception is caught; never map it to a non-zero run exit.
8. **Cross-check invariant, 31/31:** GSA present ⟺ `Fixed … Go function signatures` absent **and** `Marked … NoReturn` absent. The 5 GSA files have 0/0; the other 26 have 2/1. Use it to catch a missed pattern, never as the primary predicate (it cannot distinguish ATW, which has 2/1).
9. **Failure is single-shot.** One GSA line per file; no file carries both classes.

## 6. Determinism, continuity, binding

- **Both round-19 passes agree exactly.** After normalising only the log timestamp, the `/tmp/kr17-rea-…/rea-ghidra-…` path prefix, `(N ms)`, `N.NNN secs` and `Total Time`, the pass-1 vs pass-2 diff is **0 lines for all 8 labels** (§8 C21). Raw line counts and failure anchors are identical (`:186`/`:229` vet, `:347` compile). [OBSERVED]
- **r18 calib-aether is the r17 `aether` carrier re-run.** `.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log` (22463 B) vs `.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log` (22463 B): normalised diff is one line, `Total Time 69 secs` vs `64 secs`; GSA `:97` and root cause `:177` are identical (§8 C28). This also makes the round-17 report's byte-level analysis (`ScoutGhidraEOFIssue.md`) directly applicable to this r18 log. [OBSERVED]
- **Binding.** 31/31 on-disk logs are the `retained_logs[*].files["ghidra.log"]` of a receipt, and their sha256 + `bytes` match the receipt (§8 C15). Line numbers below are therefore tied to those exact bytes.

## 7. Limits (declared, not inferred away)

1. **Capture truncation.** Every receipt declares `log_capture_limit = "polling copy; lines written after the final poll before REA deletes its runtime root can be missing"`. All 31 files end on the same line shape, `INFO (HeadlessAnalyzer) ANALYZING changes made by post scripts: file://…`, with nothing after it. The post-script re-analysis tail is **not captured**. Therefore `none up to N` means "no GSA line in the captured N lines"; a failure thrown during the post-script analysis would be invisible here.
2. **Log-level failure ≠ symbol outcome.** Nothing measured here says how many symbols survived. (Round-17's reconstruction says the exception aborts the Go pass under one `try/catch` — `ScoutGhidraEOFIssue.md` bottom-line item 3 — but that is an inference from that report, not re-measured here.)
3. **Line numbers are captured-file line numbers.** They are reproducible only against the sha256-verified bytes of §6.
4. **No extractor was run.** `.ufo/waves/round-20/tools/` does not exist at the baseline (C14), so `first-failure-extract.py` is not available. These values are an independent oracle from `grep -n`, not a comparison against a tool.

## 8. Commands and exit codes

All were run from `LANE/.ufo/waves`. `rc=1` from `grep` means "no match" and from `diff` means "differs" — neither is a tool failure. Where a pipeline ends in `head`, the reported status is that of `head`.

| # | command (abbreviated) | exit |
|---|---|---|
| C1 | `find round-19/runs round-18/runs -type f -printf '%p\t%s\n' \| sort` | 0 |
| C2 | `wc -l "$L"; grep -n -i -E 'error\|exception\|fail\|warn' "$L" \| head -60` | grep 141 (SIGPIPE from `head`), no match failure |
| C3 | `cat round-19/runs/run-log.txt`; `cat round-19/runs/pass2/run-log.txt`; `cat round-18/runs/run-log.txt` | 0 |
| C4 | per-log `grep -i -c 'golang'` loop | 0 |
| C5 | per-log `grep -c -E 'AnalysisTaskWrapper\|NullPointerException\|ERROR\|Exception\|Caused by\|IndexOutOfBounds\|StackOverflow'` loop | 0 |
| C6 | `grep -rn 'AnalysisTaskWrapper' …`; `grep -rn 'NullPointerException' …`; `grep -rn 'Caused by' …`; `grep -rn 'Exception' …` | 0, 0, 0, 0 |
| C7 | `grep -rh 'ERROR (' … \| sed -E 's/.*ERROR \(([^)]*)\).*/\1/' \| sort \| uniq -c \| sort -rn` | 0 |
| C8 | `grep -rh 'ERROR (GoFuncData)' … \| sed … \| sort -u \| head`; same for `WARN (GoTypeManager)`; `grep -rh 'GoApiSnapshot'` | 0 |
| C9 | `grep -rn 'ERROR (GolangSymbolAnalyzer)' …`; `grep -rn -E 'ERROR \(AnalysisTaskWrapper\)' …` | 0; 0 |
| C10 | per-log census loop (lines, GSA/ATW counts+first line, GFD/DWARF counts) | 0 |
| C11 | `grep -rn 'WARN  *(GoApiSnapshot)'`; `grep -rn -E 'ERROR \((Png\|Gif)DataType\)'`; per-log first-`ERROR (` loop | 0; 0; 0 |
| C12 | per-log `grep -n 'Caused by'` + Go-frame `grep -n -E 'GoVarlenString\|GoName\|GoRttiMapper\|GolangSymbolAnalyzer\|PropagateRttiBackgroundCommand\|processWithLoader\|AnalysisScheduler'` | 0 |
| C13 | `cat` of 5 `script.log`; python walk of `receipt.json` `retained_logs` | 0; 0 |
| C14 | python: compare disk `**/ghidra.log` set vs receipt-bound set; `ls -la .ufo/waves/round-20/tools` | 0; `ls` printed `No such file or directory` (its own status was masked by the pipeline; not separately captured) |
| C15 | python: sha256+bytes of each bound log vs receipt | 0 (31 verified, 0 mismatched) |
| C16 | per-label `diff <(sed timestamp-strip a) <(sed timestamp-strip b) \| wc -l` | 0 |
| C17 | per-log `sed -n '1,6p'`; `tail -12`; `grep -rhc -E 'REPORT\|Analysis succeeded\|…'` | 0 |
| C18 | `grep -n 'REPORT:'` on compile/vet/calib-aether; tail of each | 0 |
| C19 | `unzip -l Base-src.zip \| grep GoName`; `unzip -p … GoName.java \| sed -n '85,100p'`; same `GoVarlenString.java '60,80p'` | 0; 0; 0 |
| C20 | locate + `unzip -p … MemoryByteProvider.java \| sed -n '240,320p'` | 0 |
| C21 | normalised pass-1 vs pass-2 diff per label (first version: `[a-z0-9]+` missed `_` in `/tmp/kr17-rea-…__gs`, giving cgo=50; corrected `[A-Za-z0-9_]+`) | 1 (8 diff lines total, all path-normalisation artefacts); corrected run: 0, all labels 0 |
| C22 | `grep -rn 'same length as existing entry' …` | 0 (3 lines) |
| C23 | `date -Iseconds` | 0 → `2026-10-20T17:52:34-03:00` |
| C24 | `grep -rh 'ERROR' … \| wc -l` vs `grep -rh 'ERROR (' … \| wc -l`; `grep -rn -E 'FATAL\|SEVERE\|OutOfMemory\|StackOverflowError\|AssertionError\|IllegalState' … \| head` | 0; no output (pipeline status 0; `grep` status masked by `head`) |
| C25 | per-log `grep -c` for GSA/ATW/GFD/DTI/DIS/PNG/GIF | 0 |
| C26 | per-log `grep -n 'WARN  *(GoTypeManager)'` + `GoApiSnapshot` | 0 |
| C27 | `grep -n` of compile pass-2 NPE + `PropagateRttiBackgroundCommand` frames | 0 |
| C28 | `sha256sum` r17/r18 aether logs; normalised `diff` of the two | 0; 1 (one differing line: `Total Time 69` vs `64`) |
| C29 | `grep -n 'space minimum\|virtual address' ScoutGhidraEOFIssue.md`; `grep -n -B4 -A6 '13902080' KnowledgeMechanism.md` | 0; 0 |

No tool was installed or upgraded for this report.
