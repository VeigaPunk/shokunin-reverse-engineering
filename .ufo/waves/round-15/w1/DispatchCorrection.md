# Round 15 — virtual-dispatch advisory correction

**Scope:** C2 advisory route only; source reading, no target/provider execution. This report is the named correction for the mistaken mechanism in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md:52-61` (especially line 57). It does not alter that filed artifact or the quote gate.

## Finding

The statement that `registerStructures` “does not consult the snapshot” is true only of its own loop body; it is false as a description of the complete registration path. The prior advisory missed Java virtual dispatch from `DataTypeMapper` into `GoRttiMapper.getType`.

**Concrete source case — `GoModuledata` / `runtime.moduledata`:**

1. In pinned source S003 (registry provenance: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md:9`), `GoRttiMapper` extends `DataTypeMapper`; its `GOLANG_STRUCTMAPPED_CLASSES` list includes `GoModuledata`. The constructor creates `GoTypeManager(this, apiSnapshot)` and then calls `initStructMappings()`. That method calls `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)` and wraps an `IOException` as “Missing Go bootstrap type info…” when `apiSnapshot.isInvalid()` (`GoRttiMapper`, source lines 270-390; especially 330-365).
2. Inherited `DataTypeMapper.registerStructures` iterates the classes; `registerStructure` reads each `@StructureMapping` name and calls `getType(structNames, Structure.class)`. The base list overload iterates names and calls `getType(dtName, clazz)` (`DataTypeMapper`, source lines 165-215 and 260-335).
3. That call is virtual: overload resolution selects the base `List<String>` overload, but its unqualified call to the `String` overload dispatches on the actual receiver, which is the `GoRttiMapper` passed as `this`. The override calls `goTypes.findDataType(name)`, not the base program/archive data-type search (`GoRttiMapper`, lines 380-386; `DataTypeMapper`, lines 260-335).
4. `GoModuledata` is annotated `@StructureMapping(structureName = "runtime.moduledata")` and implements `StructureMarkup`, not `StructureReader`. For this ordinary non-primitive Go type, `GoTypeManager.findTypeRec` consults `apiSnapshot.getTypeDef(typeName)`; the manager's type-name index starts empty. If that lookup yields no type, `findDataType` returns no `Structure`, and `DataTypeMapper.registerStructure` throws because a missing structure is allowed only for a `StructureReader` (`GoTypeManager`, lines 35-135 and 320-460; `GoModuledata` / `StructureMarkup`, lines 15-40; `DataTypeMapper`, lines 165-205).
5. `GoApiSnapshot.get` returns `EMPTY` when no base JSON is found, and `isInvalid()` is `arches.isEmpty()`. Thus a missing or inapplicable snapshot can both remove a lookup source and satisfy the constructor's error-to-diagnostic branch (`GoApiSnapshot`, lines 95-140 and 503-505). The source also contains a `GoPcHeader` artificial-structure exception for versions <=1.15; that exception does not supply `runtime.moduledata` for Go 1.26. On bootstrap failure, `getSharedGoBinary` catches the constructor exception and returns null rather than calling normal mapper initialization (`GoRttiMapper`, lines 105-130).

This is a minimal conditional source case, not a replay: if `runtime.moduledata` is unavailable through the snapshot-backed override while `GoModuledata` is being registered, lookup-null → `IOException` → invalid-snapshot `BootstrapInfoException` is an outcome-affecting path. The snapshot does not merely choose the wording after an unrelated failure.

## Limits and confidence

- **High confidence — source mechanism:** the virtual call chain and the snapshot-dependent non-primitive type lookup are explicit in S003. The exact failed mapping need not be guessed to reject the advisory's claim that snapshot absence is wording-only.
- **Unknown — historical attribution:** this does **not** prove that the earlier Go 1.26.8 analysis actually failed on `runtime.moduledata`, or that missing `go1.26.0.json` was its precise cause. The constructor's message requires a registration `IOException` plus an invalid snapshot; invalidity may also mean a present JSON file yielded no applicable OS/architecture records. The retained failing inner exception / analyzer log or an authorized replay would be needed to identify the historical failure. This pass did not independently inventory installed JSON files or recompute S003's recorded digest.
- The out-of-range `SUPPORTED_VERSIONS` branch still logs “Untested Go version” and continues to snapshot lookup (`GoRttiMapper`, lines 170-176). The correction is that the later snapshot-dependent bootstrap path can stop mapper creation, not that the version-range warning itself is a hard rejection.
- No LSP device is exposed in this session; I read the pinned source members directly. No grep result is used as semantic evidence. No build, test, gate, or runtime check was executed. No tool was installed or updated.

## Proposed L1 checks

1. Reopen the cited S003 member/range anchors against the registry-pinned archive, especially the base overload → subclass override and `GoModuledata` registration case.
2. Integrate a named virtual-dispatch correction into the appropriate final lesson/LOG and qualify the pointer to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md`; preserve the original advisory as historical evidence.
3. Keep the separate QUALITY/manual-only quote-input correction distinct; confirm no quote-gate implementation change is bundled into this dispatch correction.
