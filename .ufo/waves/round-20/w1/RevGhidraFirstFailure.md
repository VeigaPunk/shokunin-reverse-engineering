# Ghidra Go RTTI order and first fatal read

Evidence: Ghidra 12.1.4 `Base-src.zip` source and the retained round-18 `calib-aether` Ghidra log. No Go toolchain binary, REA analysis, or Ghidra analysis was run. `B` below means `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`; archive anchors use `B!/member/path:line`.

## Observations

**Order.** `GoRttiMapper.init` finds the first module, initializes function data, calls `goTypes.init`, then initializes method info (`B!/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:444-465`; module lookup begins at `:1116`). Within `GoTypeManager.init`, each module's typelink list is read first; each valid type is indexed and recursively discovered; then it reads itabs, associates both concrete/interface types and discovers from each itab; then it runs the gap scan (`B!/ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java:96-145`). The typelink slice is decoded as int32 offsets relative to `typesOffset` (`B!/ghidra/app/util/bin/format/golang/rtti/GoModuledata.java:398-405`); itabs precede the gap scan (`GoTypeManager.java:121-142`). The scan sorts discovered type ranges by unsigned address, scans intervening gaps at pointer-size steps, and indexes only anonymous `GoStructType` candidates (`GoTypeManager.java:169-208`).

The markup walk is a later phase: `GolangSymbolAnalyzer.added` calls `recoverGhidraDataTypes`, then `markupGoTypes`, then labels/marks up `firstmoduledata`, known symbols, context, and functions (`B!/ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:145-155`). `markupGoTypes` iterates `allTypes()` and marks each; `allTypes()` sorts the index by unsigned address (`B!/ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java:147-155,263-268`). The retained run independently shows `Discovered 188 unindexed Go types` followed by `Found 6115 Go types` before the analyzer's failure (`.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:94-97`).

**Exception boundary.** A read `IOException` is not automatically fatal during indexing: `getTypeUnchecked` and `readTypeUnchecked` catch it and return null (`GoTypeManager.java:283-289,639-645`); discovery warns and continues when a typelink read returns null (`:112-118`), and the gap scan advances by pointer alignment when candidate reads fail (`:194-200`). `getAlignedEndOfTypeInfo` also catches `IOException` and falls back to the type offset (`:157-165`). Conversely, markup recursion calls field/external/structure markup without a per-type IOException catch (`B!/ghidra/app/util/bin/format/golang/structmapping/MarkupSession.java:98-127,324-349`); the data-type-application catch at `:302-311` rethrows a wrapped IOException rather than continuing. `ReflectionHelper.callGetter` wraps `InvocationTargetException` as `IOException` (`B!/ghidra/app/util/bin/format/golang/structmapping/ReflectionHelper.java:317-330`). The analyzer's enclosing catch logs `Msg.error(this, "Go analysis failure", e)` and returns false (`GolangSymbolAnalyzer.java:181-184`). Thus the markup read failure exits this analyzer pass; it is not a per-type skip. A distinct per-function continuation path catches `DuplicateNameException | InvalidInputException | IllegalArgumentException`, logs a warning, then `continue`s (`GolangSymbolAnalyzer.java:294-298`). `CancelledException` is separately declared by `added` and `markupGoTypes`, not converted to this IOException log (`GolangSymbolAnalyzer.java:110-111`; `GoTypeManager.java:147-148`).

**Observed first fatal log.** The retained aether run's first analyzer error is exactly:

> `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException`

at `.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:97`. Its causal read failure is logged at line 177:

> `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`

The trace identifies `MemoryByteProvider.ensureBounds` at `:312`, then a `GoVarlenString.readFrom` and `GoName.getPkgPath` path, reached during `MarkupSession.markupFields` / `GoTypeManager.markupGoTypes` / `GolangSymbolAnalyzer.added` (`ghidra.log:98-105,153-156,177-196`). The source formats this exception as `Unable to read past EOF: %s, %d` (`B!/ghidra/app/util/bin/MemoryByteProvider.java:289-313`).

## Comparison with round-18 `swiss-misread.py`

The docstring states module/typelink discovery → discovery index → unindexed-closure gap scan → VA-sorted markup walk (`.ufo/waves/round-18/tools/swiss-misread.py:18-21`), and its cited GoTypeManager anchors for discovery/gap scan and sorted `allTypes` agree (`:30-35`). Implementation order agrees: `analyse` calls `discover_modules` (`:1291`); each hypothesis calls `discover_index`, then `gap_scan`, then walks `sorted(index)` (`:1311-1319`). On first `ReadError`, it records `first_failure` and breaks (`:1319-1329`). This models the same first-failure stopping point as Ghidra's outer IOException catch, though the emulator's Python `ReadError`/`break` is not Ghidra's Java exception path. The emulator's `discover_index` covers typelinks, itab references, and recursive type references (`:1086-1157`); its gap scanner covers anonymous struct candidates (`:1205-1244`); its markup traversal handles fields, interface methods, map members, func parameters, and uncommon pkgPath/method chains (`:841-872,875-995`).

One docstring anchor is path-inaccurate: `swiss-misread.py:33` says `structmapping/MemoryByteProvider.java:289-313`; the actual source member is `ghidra/app/util/bin/MemoryByteProvider.java:289-313`. Its quoted generic form `Unable to read past EOF: A, B` is explanatory; the real source format and observed run use numeric index and length as above.

## Commands and exit codes

- `unzip -l /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip | grep -iE 'golang|Golang'` — exit 0 (Go source members listed).
- Initial `unzip` extraction requested the nonexistent member `ghidra/app/util/bin/format/golang/structmapping/MemoryByteProvider.java` — exit 11 (`filename not matched`); this located the path mismatch, not a source failure.
- Corrected `unzip -o -q ... 'ghidra/app/util/bin/MemoryByteProvider.java' ...` extraction — exit 0.
- `unzip -o -q ... 'ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java' ...` — exit 0.

**Confidence:** High for the source control flow and quoted log line (direct source plus retained stack trace). The phase comparison is direct; the emulator deliberately simplifies the Java reflection/wrapping path.