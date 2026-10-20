# ScoutGhidraVariadic — GoFuncType variadic mask, GoTypeManager :639-646, first-failure order

- Seat: `KaidokuR20.ScoutGhidraVariadic` (wave 1, leaf scout, read-only). No subagents, no installs.
- Write clock at report authoring: `2026-10-20T17:58:15-03:00` (`date -Iseconds`, final edit pass).
- Lane revision observed while reading: `refs/heads/main` = `d1d981d2cc041dda4656c5b01d2c8445d8d17124`
  (`git rev-parse refs/heads/main`, exit 0). Contract baseline B = `14f0260ad319ecc26994381b2415d5a999003375`;
  I did not write, clone, or check out anything.
- Artifact: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`,
  sha256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; `Ghidra/application.properties:17`
  `application.version=12.1.4`. Extracted sources (sha256):
  `GoFuncType.java` `f06988a39e6e7f63ac67a9c440be179debd187af7d1db38119e95d8f915584b1`,
  `GoTypeManager.java` `c1b737da6dae12b7db310b52f6cdbdec3ceb83772f166dd4aba2662cd2c41c34`,
  `GolangSymbolAnalyzer.java` `b9b70998570b18d4619de28e41e99beb17f9c04e0197d4888b0688b66054ab80`,
  `MemoryByteProvider.java` `8a4ce2a7c11608ce2370bc1dfe000f8d417906a066ea7ac97c0a812614912fea`.
- Work dir `/tmp/kr20-scout-ghidra-variadic.doRBJ2` (`mktemp -d`); no lane file other than this report was written.
- Labels: **[OBS]** = quoted from a named file/command output; **[INF]** = follows from those sources but
  was not executed for a carrier.

## Bottom line

1. `GoFuncType` masks the variadic flag everywhere: `isVarArg = (outCount & 0x8000) != 0` (:65),
   `getOutCount = outCount & 0x7fff` (:79), `getParamCount = inCount + (outCount & 0x7fff)` (:86);
   the param slice's `len`/`cap` are that masked count (:97-100). This is exactly Go 1.24.6's
   `NumOut`/`IsVariadic` (`internal/abi/type.go:515-517`, :545-547).
2. `GoTypeManager.getTypeUnchecked` (:639-646) is total — `IOException` → `null`; it can never abort the
   pass. Bad param *element* types are therefore silent, not failures.
3. `GolangSymbolAnalyzer.added()` has one `try` (:144) around the whole stage sequence and one
   `catch (IOException)` (:181-183) that logs `Go analysis failure` and returns false (:184). The first
   escaping `IOException` is the only one; every later stage (including `markupGoFunctions` after a
   `markupGoTypes` failure) never runs.
4. "First failure" in the log is therefore the earliest terminal Go marker **in file order**:
   `ERROR (GoRttiMapper) Failed to read Go info` (bootstrap/`init`, `GoRttiMapper.java:121`, before the
   analyzer try) or `ERROR (GolangSymbolAnalyzer) Go analysis failure` (inside the try). Per-item
   `Msg.error`/`logWarningAt` lines from `Golang*` components are not failures; `AnalysisTaskWrapper`
   lines are background jobs after the pass.
5. Stage order = source order (§4); type order = ascending type offset (`sortedTypeRecs`/`allTypes`,
   `GoTypeManager.java:263-269`, :271-277) for `recoverGhidraDataTypes` and `markupGoTypes`;
   function order = `HashMap` iteration (`GoRttiMapper.java:309`, :1112-1114), not address or functab
   order.
6. `kind`/`va` come from the deepest cause (`MemoryByteProvider.java:302` `Invalid index: N`,
   :311-312 `Unable to read past EOF: index, length`); `phase` from the deepest `added(...:line)` frame
   (145/146/150/151/153/154/155/157/160). The outer `InvocationTargetException` line is never the kind.
7. The round-18/19 emulator is unmasked at `swiss-misread.py:939` and `:1047-1048`; v2 must apply
   `& 0x7fff` at both, or its predicted first failure is biased by 32768 slots per variadic func type.

## 1. GoFuncType: the variadic bit is masked in every count path [OBS]

`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoFuncType.java`

```java
51:	@FieldMapping
52:	private int inCount; // uint16
53:
54:	@FieldMapping
55:	private int outCount; // uint16
...
64:	public boolean isVarArg() {
65:		return (outCount & 0x8000) != 0;
66:	}
...
78:	public int getOutCount() {
79:		return outCount & 0x7fff;
80:	}
...
85:	public int getParamCount() {
86:		return inCount + (outCount & 0x7fff);
87:	}
```

(line spans :51-55, :64-66, :78-80, :85-87; the `& 0x8000` test is at :65 and the only `& 0x7fff`
arithmetic is :79 and :86 — `grep -nE '0x8000|0x7fff'` returned exactly those three lines.)

Consequences, all from the same file:

- The param list is `count = getParamCount()` pointers starting at `getOffsetEndOfFullType()`:
  `:97-100` — `int count = getParamCount(); return new GoSlice(getOffsetEndOfFullType(), count, count, programContext);`
- The count is used as both `len` and `cap` of that synthetic `GoSlice` (:98-99), so an unmasked
  `outCount` would make the slice length/cap 32768 larger, not just one element larger.
- `getParamTypeAddrs()` reads exactly `count` pointer-sized entries: `:89-95`
  (`GoSlice slice = getParamListSlice(); long[] typeOffsets = slice.readUIntList(programContext.getPtrSize());` at :90-91).
- `getParamTypes()` (:107-111) resolves each offset through `GoTypeManager.getTypeUnchecked`, i.e. through
  the swallowing path in §2, so a bad *element* type yields `null`, never `IOException`.
- Markup does not read the elements: `additionalMarkup` (:113-119) calls
  `slice.markupArray(..., GoBaseType.class, true, session)`; `GoSlice.markupArray` at
  `GoSlice.java:320-337` only builds `new ArrayDataType(elementType, (int) cap, -1, dtm)` (:331) and calls
  `session.markupAddress(addr, arrayDT)` (:333). `MarkupSession.markupAddress` (`MarkupSession.java:150-164`)
  catches only `CodeUnitInsertionException` (warn). So the variadic count's read cost lands in
  `readUIntList`, not in array markup.
- `getParamListString`'s catch is narrow and non-fatal: `:169-170` `} catch (IOException e) { return "(???)"; }`.
- `getFunctionSignature` throws a plain `IOException` when the recovered data type is not the closure
  struct/function-def shape: `:243` `throw new IOException("Unable to extract function sig for " + this.toString());`.
- `discoverGoTypes` also walks the params: `:266-277`, loop at `:271` `for (GoType paramType : getParamTypes())`.
- `isValid()` requires `typ.getSize() == programContext.getPtrSize()` (:288-290).
- The param base is `GoType.getOffsetEndOfFullType()` = `context.getStructureEnd() + (hasUncommon ?
  UncommonType length : 0)` (`GoType.java:124-128`; `typ.getSize()` is the FuncType structure length only).

Go-side corroboration (read, not executed): `/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/type.go`
`:501-505` declares `type FuncType struct { Type; InCount uint16; OutCount uint16 // top bit is set if last input parameter is ... }`;
`:515-517` `NumOut() { return int(t.OutCount & (1<<15 - 1)) }`; `:545-547` `IsVariadic() { return t.OutCount&(1<<15) != 0 }`;
`:528-542` place the param/result pointer arrays at `unsafe.Sizeof(*t) (+ UncommonType when TFlagUncommon)`.
Ghidra's `& 0x7fff` / `& 0x8000` are therefore exactly Go's `NumOut` / `IsVariadic`.

**[OBS]** Installed snapshot layout (computed with the lane emulator's own `Layout`, see §5):
`internal/abi.FuncType` size **56**, `InCount` at **48**, `OutCount` at **50**,
`internal/abi.UncommonType` size **16** for both go1.24.x and go1.25.0. **[INF]** 56 = 48-byte
`internal/abi.Type` + 2 + 2, padded to 8; the param array starts at `type_addr+56` (+16 if `tflag&1`).

## 2. GoTypeManager:639-646 — failure is converted to `null`, never rethrown [OBS]

`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java`

```java
639:	public GoType getTypeUnchecked(Address addr) {
640:		try {
641:			return getType(addr.getOffset(), false);
642:		}
643:		catch (IOException e) {
644:			return null;
645:		}
646:	}
```

Precise meaning:

- The method is total: no `IOException` can escape it; it cannot produce the analyzer's abort.
- `null` is ambiguous. `getType` → `getTypeRec(offset, cacheOnly)` returns `null` for offset 0
  (`:243-245` `if (offset == 0) { return null; }`), so a legitimate zero offset and a read failure are
  indistinguishable to every caller.
- The sibling fallback is `getTypeName(long)` `:657-667`: an `IOException` "falls thru" (`:664-666`) to
  `"unknown_type_%x".formatted(offset)`; a name is always produced.
- Callers in the func-type path: `GoFuncType.getParamTypes` (`GoFuncType.java:107`) and
  `GoTypeManager.init`'s discovery loop (`:112` `GoType goType = getTypeUnchecked(typeAddr);`, `:113-114`
  `goType.discoverGoTypes(...)`, `:117` `Msg.warn(this, "Failed to read Go type at " + typeAddr)`).
- Because element resolution is total, a variadic/mask error can only surface as `IOException` from
  `readUIntList`/`readStructure` (the structural reads at `GoFuncType.java:89-95`, read at :91), or as a later
  `NullPointerException` at `paramType.getName()` (`GoFuncType.java:162`, in-loop at :149) / `goTypes.getDataType(null)`
  (`GoTypeManager.java:799-801` returns `null` for `typ == null`) — **[INF]** the NPE case is not caught
  by `catch (IOException)` in §3 and would not produce a "Go analysis failure" line.

## 3. GolangSymbolAnalyzer: first `IOException` ends the whole Go pass [OBS]

`Base-src.zip:ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java`, `added()`:

```java
110:	public boolean added(Program program, AddressSetView set, TaskMonitor monitor, MessageLog log)
111:			throws CancelledException {
112:		long txId = program.getCurrentTransactionInfo().getID();
113:		if (txId == lastTxId) {
114:			// Only run once per analysis session - as denoted by being in the same transaction
115:			return true;
116:		}
117:		lastTxId = txId;
118:
119:		if (isAlreadyAnalyzed(program)) { ... return false; }
...
134:		goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
135:		if (goBinary == null) {
136:			Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");
137:			return false;
...
144:		try {
145:			goTypes.recoverGhidraDataTypes(monitor);
146:			goTypes.markupGoTypes(markupSession, monitor);
147:
148:			GoModuledata firstModule = goBinary.getFirstModule();
149:			if (firstModule != null) {
150:				markupSession.labelStructure(firstModule, "firstmoduledata", null);
151:				markupSession.markup(firstModule, false);
152:			}
153:			markupWellknownSymbols();
154:			setupProgramContext();
155:			markupGoFunctions(monitor);
156:			if (analyzerOptions.fixupDuffFunctions) {
157:				fixDuffFunctions();
158:			}
159:			if (analyzerOptions.fixupGcWriteBarrierFunctions) {
160:				fixGcWriteBarrierFunctions();
161:			}
...  // :163-176 schedule PropagateRtti / FixClosureFuncArgs / FixGcWriteBarrierFlag
178:			program.getOptions(Program.PROGRAM_INFO).setBoolean(ANALYZED_FLAG_OPTION_NAME, true);
179:			return true;
180:		}
181:		catch (IOException e) {
182:			Msg.error(this, "Go analysis failure", e);
183:		}
184:		return false;
185:	}
```

(`nl -ba` gives `144: try {`, `181: catch (IOException e) {`, `182: Msg.error(...)`,
`184: return false;`.)

What the structure guarantees:

1. **A single try wraps every stage.** The first `IOException` thrown by any stage skips every later
   stage, skips the background-command scheduling, skips `ANALYZED_FLAG_OPTION_NAME`, and returns
   `false` after logging one `ERROR (GolangSymbolAnalyzer) Go analysis failure <throwable>` with stack
   trace (the round-19 log shows exactly this: `ghidra.log:186`, stack frames
   `GolangSymbolAnalyzer.added(GolangSymbolAnalyzer.java:146)` at `:207` and
   `GoTypeManager.markupGoTypes(GoTypeManager.java:153)` at `:206`).
2. **Stage order is source order** (§4). Within `markupGoTypes` the order is `allTypes()` sorted by
   unsigned type offset (`GoTypeManager.java:263-269` + `:271-277`), and `markupGoTypes` iterates that
   order (`:147-155`). Within `recoverGhidraDataTypes` the order is `sortedTypeRecs()`
   (`GoTypeManager.java:271-277`), also unsigned-offset ascending, and that loop has **no** per-type
   catch (`:736-742`).
3. **Not every error is a failure.** Per-item/warn paths that do not abort:
   `markupGoFunctions` catches `DuplicateNameException | InvalidInputException | IllegalArgumentException`
   around `GoFunctionFixup.apply` (`:291-299`) → `MarkupSession.logWarningAt` + `continue`;
   `fixGcWriteBarrierFunctions`/`fixDuffFunctions` log `Msg.error` and continue (`:375`, `:424`, `:466`,
   `:491`, `:539`, `:589`, `:656`, `:726`, `:752`, `:983`, `:1014`, `:1041`);
   `readNoReturnFuncNames` catches `IOException | XmlParseException` (`:509-511`).
   `CancelledException` is **not** caught by :181, so a cancel unwinds without any "Go analysis failure".
   `RuntimeException`s (e.g. NPE from §2's nulls) also escape unwrapped.
4. **Re-entry:** the `lastTxId` guard (:112-117) suppresses a second invocation in the same transaction;
   on failure the `ANALYZED` flag is never set, so a later transaction/session can run again and log a
   second identical-class line. In a one-shot headless import+analyze run, at most one such line exists.
5. **`markupGoFunctions`'s iteration order is not address order.** `goBinary.getAllFunctions()` is
   `new ArrayList<>(funcdataByAddr.values())` where `funcdataByAddr` is a **`HashMap<Address,GoFuncData>`**
   (`GoRttiMapper.java:309`, return at `:1112-1114`), filled by `initFuncdata` in functab order
   (`GoRttiMapper.java:467-473`, `GoModuledata.java:278-288`). A failure in that loop is therefore the
   first element of HashMap iteration order — deterministic per carrier/JVM but neither ascending VA nor
   functab index. The failing function's *name* is not in an EOF message; only `getFunctionSignature`'s
   `IOException` carries `this.toString()` (`GoFuncType.java:243`).

## 4. What "first failure" in the log means, in Ghidra's order [OBS source / INF mapping]

Chronological order of Go-related terminal events for one import+analyze:

1. `INFO (GoRttiMapper) Reading Go binary info: <program>` (`GoRttiMapper.java:107`);
   snapshot lines (`GoRttiMapper.java:180` "Using Go API snapshot for version %s";
   `GoApiSnapshot.java:159-163` fallback/using). For go1.24.6 there is no `go1.24.6.json` base but there
   **is** `patchverdiffs/go1.24.6.json.diff` (118810 bytes), so base go1.24.0 + patch is used and the
   path logs `INFO (GoApiSnapshot) Using Go API snapshot for 1.24.6` (`GoApiSnapshot.java:148-164`),
   not a fallback warning. [OBS: directory listing + file size]
2. **Pre-try terminal site:** `GoRttiMapper.getSharedGoBinary` runs `getGoBinary` + `init()` inside a
   supplier and catches `IOException` → `ERROR (GoRttiMapper) Failed to read Go info` with stack
   (`GoRttiMapper.java:102-127`, error at `:121`); `added()` then logs
   `ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper` (`:135-136`)
   and returns `false`. `init()` order is `findFirstModuledata` → ptrSize check → `initFuncdata()`
   → `goTypes.init(monitor)` → `initMethodInfo()` (`GoRttiMapper.java:444-464`). Discovery-phase
   failures — including `GoFuncType.discoverGoTypes` → `getParamTypes()` → `readUIntList`
   (`GoFuncType.java:271`, `GoTypeManager.java:110-120`, unwrapped) — land **here**, not in the
   "Go analysis failure" line.
3. `INFO (GolangSymbolAnalyzer) Go version X` (`:139`).
4. **In-try terminal site:** the first `IOException` out of
   `recoverGhidraDataTypes` → `markupGoTypes` → firstmoduledata label/markup → `markupWellknownSymbols`
   → `setupProgramContext` → `markupGoFunctions` → `fixDuffFunctions` → `fixGcWriteBarrierFunctions`
   (`:145-161`) → `ERROR (GolangSymbolAnalyzer) Go analysis failure <throwable>` (`:181-184`) and
   `return false`. This is the only line that means "the pass aborted mid-way".
5. Later, independent jobs: `AnalysisTaskWrapper` errors from the scheduled RTTI/closure/gcWriteBarrier
   fixups (observed: `.ufo/waves/round-19/runs/t1250-compile/.../ghidra.log:347`
   `ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - element cannot be
   mapped to a null key java.lang.NullPointerException`) and `GolangStringAnalyzer` info. These are
   after the pass and must not be folded into the first failure.

Therefore, for the extractor, **"first Go-analysis failure" = the first line in the log, in file order,
that is one of the two terminal Go markers**: `ERROR (GoRttiMapper) Failed to read Go info` or
`ERROR (GolangSymbolAnalyzer) Go analysis failure`. The second is the abort of a stage block; the first
is a bootstrap abort that precedes it and pre-empts it (both can appear: `Failed to read Go info`, then
`unable to get GoRttiMapper`). Component-tag-only matching (`Golang*/GoRttiMapper/GoTypeManager`) is too
wide: `GolangSymbolAnalyzer` also emits non-aborting `Msg.error` lines (list in §3.3), and
`MarkupSession`/`GoFuncData`/`GoBuildId` emit yet others.

Field mapping that the log actually supports:

- `kind`: read the **deepest** `Caused by:`. In the observed type-markup path the outer message is the
  reflection wrapper (`java.io.IOException: java.lang.reflect.InvocationTargetException`,
  observed `ghidra.log:186`), but direct `IOException`s also occur (e.g.
  `Unable to extract function sig for ...` at `GoFuncType.java:243`, `Invalid Go moduledata at ...`
  at `GoRttiMapper.java:1134-1136`).
  With `MemoryByteProvider.ensureBounds` (`MemoryByteProvider.java:289-313`) the two distinguishable
  deepest causes are:
  - `EOFException: Invalid index: <N>` — `:302`/`:173`; emitted when `index` is past `maxOffset`
    (`Long.compareUnsigned(index, maxOffset) > 0`).
  - `EOFException: Unable to read past EOF: <index>, <length>` — `:311-312`; emitted when the read
    would extend past the end.
  Both numbers are decimal unsigned; the first is the virtual read address (address space minimum 0,
  as reconstructed in `.ufo/waves/round-17/w2/ScoutGhidraEOFIssue.md`).
- `va`: the `Invalid index` value, or the `index` token of `Unable to read past EOF`.
  `index` (element ordinal) is **not** in either message; it is only in the emulator's prediction.
  **[INF]** if the contract's `index` field is meant to be the element ordinal, the log side must emit
  `null` and comparison must be kind+va only, or the comparison tool must treat a predicted ordinal as
  unevaluable when the log gives only an address.
- `phase`: the deepest `GolangSymbolAnalyzer.added(GolangSymbolAnalyzer.java:<line>)` frame:
  `145` → `recoverGhidraDataTypes`, `146` → `markupGoTypes`, `150/151` → firstmoduledata,
  `153` → `markupWellknownSymbols`, `154` → `setupProgramContext`, `155` → `markupGoFunctions`,
  `157` → `fixDuffFunctions`, `160` → `fixGcWriteBarrierFunctions`; no `added` frame → pre-try
  bootstrap (`init`/discovery). Observed example: `added:146` → phase `markupGoTypes`
  (`ghidra.log:207`), deepest cause `Invalid index: 13902080` (`:229`), via
  `GoName.readStructure(GoName.java:94)` (`:235`).
- Absence: "none up to line N" must be scoped to the last line read, because the `AnalysisTaskWrapper`
  and `GolangStringAnalyzer` lines come after the pass — a Go pass that never started (no Go build
  info) logs neither terminal marker.

## 5. Calibration consequences for the round-20 emulator (C3)

**[OBS]** The round-18/19 emulator does **not** mask, at two sites:

- `.ufo/waves/round-18/tools/swiss-misread.py:933-953` (`_markup_func`), the count line is
  `939: count = in_count + out_count`; the guard `:940-941` is `if count > 100000: return`, which a
  variadic type (`outCount = 0x8000|n`, count ≈ 32768+n) never trips. `:942-944` then walks
  `count` pointer slots (`base = type_addr + size`, `+ UncommonType` when `tflag & 0x01`).
- `:1041-1052` (the kind-19 reference extractor) repeats the same unmasked sum (`:1047-1048`) with a
  `min(count, 4096)` clamp.

Correct v2 law, matching `GoFuncType.java:64/75/83` exactly:
`count = InCount + (OutCount & 0x7fff)`, `isVariadic = (OutCount & 0x8000) != 0`,
base = `FuncType` end + `UncommonType` size when `tflag & 0x01`. With the installed layout
(size 56, `InCount` +48, `OutCount` +50, uncommon 16) a variadic `func(...)` type with `inCount=1`,
`outCount=0x8001` must read **2** slots, not 32770. Under v1 the walk over-reads by 32768 slots per
variadic type, which both inflates `steps` toward `MAX_MARKUP_STEPS` (truncation) and manufactures
`ReadError("invalid_index"|"past_eof")` at addresses Ghidra never reads — a false-positive source for
`first_failure` on any carrier with variadic func types. The reverse error — predicting silence where
Ghidra fails — is also possible because masking changes which addresses are read at all.

Snapshot parity check [OBS]: the emulator's `select_snapshot`/`load_snapshot_types`
(`swiss-misread.py:245-333`) load only the **base** JSON and explicitly do not apply patch diffs
(docstring `:246` "without applying diffs"). For go1.24.6 carriers Ghidra applies
`patchverdiffs/go1.24.6.json.diff`; that diff has 104 `@ ["all","Types",...]` hunks, **0** of them under
`internal/` (so no `internal/abi.*` layout moves); its non-`Position` hunks are field edits to
`go/types.Checker` (:1697), `go/types.PkgName` (:1714), `go/types.Var` (:1721-1728), `runtime.m`
(:1855), `testing.B` (:1946-1949) and one anonymous struct (:1982). So the FuncType/UncommonType/Type
layouts used by `Layout` (verified 56/48/50/16) equal what Ghidra uses for go1.24.6 — the no-diff
shortcut does not bias this slice. It would bias any type whose layout the diff does change.

## 6. Commands and exits

| # | Command (abridged; absolute paths where outside LANE) | exit |
|---|---|---|
| 1 | `ls -la /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | 0 |
| 2 | `unzip -l …/Base-src.zip \| grep -Ei 'GoFuncType\|GoTypeManager\|GolangSymbolAnalyzer'` | 0 |
| 3 | `unzip -o -q …/Base-src.zip <3 java paths>` into `mktemp -d`; `wc -l`; `sha256sum` | 0 |
| 4 | `grep -n -E 'getTypeUnchecked\|getTypeName\(long offset\)\|catch \(IOException\|unknown_type_' GoTypeManager.java` | 0 |
| 5 | `grep -n -E 'IOException\|catch\|throw\|return false\|Msg\.' GolangSymbolAnalyzer.java` | 0 |
| 6 | `grep -n -E '0x8000\|0x7fff\|inCount\|outCount' GoFuncType.java` | 0 |
| 7 | `unzip -o -q … 'ghidra/app/util/bin/format/golang/*'`; `grep -rn 'recoverFunctionSignature\|getAllFunctions'` | 0 |
| 8 | `grep -n 'funcdataByAddr' GoRttiMapper.java`; `grep -n 'readUIntList' GoSlice.java` | 0 |
| 9 | `grep -rn 'getFunctionSignature(' ghidra/app/util/bin/format/golang/` | 0 |
| 10 | `grep -n 'getFuncDefFor\|getDataType(GoType\|recoverDataType(' …` | 0 |
| 11 | `grep -rn 'Go analysis failure' .ufo/waves/round-19/runs` (LANE) | 0 |
| 12 | `grep -rn -E 'ERROR \(\|Unable to read past EOF\|Invalid index' .ufo/waves/round-19/runs/*/logs/*/ghidra.log` | 0 |
| 13 | `sed -n '150,240p' .ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log` | 0 |
| 14 | same log: `grep -n 'Go analysis failure\|added(\|markupGoTypes(\|EOFException'` → 186, 206, 207, 229, 235 | 0 |
| 15 | `sed -n '184,190p;226,232p'` same log | 0 |
| 16 | `sed -n '900,975p;1025,1065p' .ufo/waves/round-18/tools/swiss-misread.py` | 0 |
| 17 | `grep -n -i 'functype\|class .*Layout\|def size\|def offsets' swiss-misread.py` | 0 |
| 18 | `sed -n '345,380p;455,500p;245,333p' swiss-misread.py` | 0 |
| 19 | `sed -n '496,550p' /home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/type.go` | 0 |
| 20 | `ls …/typeinfo/golang/`; python read `go1.24.6.json` → `FileNotFoundError` (corrected probe) | 1 |
| 21 | python read `go1.24.0.json` `/all/Types/internal/abi.FuncType` and `go1.25.0.json` same | 0 |
| 22 | `sed -n '80,190p' GoApiSnapshot.java`; `grep -n 'Falling back from\|Using Go API snapshot for' …` | 0 |
| 23 | `sed -n '96,140p;180,270p;440,520p' GoRttiMapper.java` | 0 |
| 24 | `sed -n '285,315p' ghidra/app/util/bin/MemoryByteProvider.java` (after extracting it) | 0 |
| 25 | `sed -n '270,305p;395,415p' GoModuledata.java` | 0 |
| 26 | `sed -n '370,420p;315,360p' MarkupSession.java`; `sed -n '300,360p' GoSlice.java` | 0 |
| 27 | `sed -n '90,175p;630,672p;700,770p;790,835p' GoTypeManager.java` | 0 |
| 28 | python: import `swiss-misread.py` via importlib, `select_snapshot`/`load_snapshot_types`/`Layout`; print FuncType size/offsets → `56 {'Type':0,'InCount':48,'OutCount':50} 16` | 0 |
| 29 | python: search whole `go1.25.0.json` for `FuncType`; list `patchverdiffs` for `1.24.*`; size `go1.24.6.json.diff` = 118810 | 0 |
| 30 | `grep -n '@ \["all","Types"' go1.24.6.json.diff`; `grep -c 'internal/abi.FuncType'` = 0 | 0 |
| 31 | `date -Iseconds` → `2026-10-20T17:53:52-03:00`; `git rev-parse refs/heads/main` → `d1d981d2…` | 0 |
| 32 | `sha256sum` Base-src.zip / MemoryByteProvider.java; `grep application.version` | 0 |
| 33 | `nl -ba GoFuncType.java \| sed -n '50,90p;89,104p;105,125p;130,145p;144,168p;190,200p;235,246p;265,280p;285,292p'` (numbered anchors) | 0 |
| 34 | `nl -ba GolangSymbolAnalyzer.java \| sed -n '140,190p;288,300p;505,512p'`; `nl -ba GoTypeManager.java \| sed -n '145,156p;260,280p;735,745p;792,802p'` | 0 |
| 35 | `grep -c '@ \["all","Types"' go1.24.6.json.diff` = 104; `grep -c '@ \["all","Types","internal/'` = 0; non-`Position` hunks listed (:1697-1982) | 0 |
| 36 | `grep -n -A8 'public boolean isValid' GoSlice.java` | 0 |
| 37 | `date -Iseconds` (final edit pass) → `2026-10-20T17:58:15-03:00` | 0 |

`read` tool calls (not shell) were used for line-anchored excerpts; they have no exit code.

## 7. Remaining unknowns / limits

- `ghidra.program.model.address.Address` source is not in `Base-src.zip` (only `MemoryByteProvider` is),
  so the exact `HashMap` iteration order of `funcdataByAddr` for a given carrier is not derivable
  read-only from this artifact; `Address.hashCode` semantics are [INF] offset-based.
  Function-level `index` forecasts for `markupGoFunctions` are therefore unevaluable against a log that
  prints only a VA.
- I did not run Ghidra, did not execute any Go toolchain binary, and did not run REA analyze/search/
  decompile on any carrier (contract `REA / Ghidra / carriers`).
- This report covers the three named source files plus the call chain needed to answer "first failure";
  it does not re-verify the round-19 emulator's map/uncommon/name models beyond the func-type sites.

Report: .ufo/waves/round-20/w1/ScoutGhidraVariadic.md
