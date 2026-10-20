# ScoutGhidraGoStructMapping — how Ghidra 12.1.4 binds `GoMapType` to snapshot JSON type names

Author: `KaidokuR18.ScoutGhidraGoStructMapping` (leaf, author-side advisory). Lane files untouched; this file is
the only write. L1 integrates.

**Question.** In the installed Ghidra 12.1.4, how does the Go struct-mapping layer bind a Java class
(`GoMapType` et al.) to the snapshot-JSON type `runtime.maptype` / `internal/abi.*MapType`? Is there any
Swiss-map class or version switch? Compare with the master change named by S032 (PR #9348), *files list only*.

**Inputs (pinned).** `Z` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`,
sha256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`. Members cited as
`Z:ghidra/app/util/bin/format/golang/...:LINE`. `D` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`.
`D/go1.24.0.json` sha256 `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571`;
`D/go1.25.0.json` sha256 `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`.
Only local files and the PR `/files` page were read; no REA, no Ghidra/`analyzeHeadless`, no carrier execution,
no installs, no lane edits.

## Bottom line

1. **Binding is by name, lazily, from the JSON snapshot — not from a `.gdt` archive.** `@StructureMapping`
   carries an ordered list of Ghidra-structure names; registration walks the list and each name is resolved by
   `GoTypeManager` from the version's JSON `Types` map, synthesising a `StructureDataType` in memory. (OBSERVED,
   §1.)
2. **For Go 1.24/1.25 the chain lands on `internal/abi.OldMapType` (88 B).** `runtime.maptype` is an *alias* in
   those snapshots and becomes a `TypedefDataType`, which the `Structure.class` check rejects; `internal/abi.MapType`
   is absent; `internal/abi.OldMapType` is the first struct candidate. (OBSERVED JSON + OBSERVED resolution code;
   the final landing point is INFERENCE, §4.)
3. **No Swiss-map class and no map-layout version switch exist in 12.1.4.** `grep -ri swiss` over the whole Go
   source set yields 0 lines; `GoMapType` has 0 `presentWhen` gates; `internal/abi.SwissMapType` sits unused in
   the 1.24/1.25 JSON. (OBSERVED, §3.)
4. **Version machinery exists but is not wired to the map struct**: `SUPPORTED_VERSIONS 1.15-1.25`, JSON selected
   by `GoVer`, and the generic `presentWhen` predicate (used by `GoModuledata`, `GoFuncData`, `GoPcHeader`, …).
5. **PR #9348's `/files` list is exactly 3 files (+35/−7).** Its `GoMapType` base-master name list matches
   12.1.4's line 33 entry-for-entry; the other two files correspond to 12.1.4 members that lack the added
   guards. So 12.1.4 is the PR's "before" state. (OBSERVED, §5.)

## 1. The binding chain (OBSERVED; each hop anchored)

Registry and construction order:

- `Z:.../rtti/GoRttiMapper.java:294-300` — `GOLANG_STRUCTMAPPED_CLASSES` lists every mappable class; `GoMapType.class`
  is at `:298`. A class absent from this list "can't be used" (`:292`).
- `Z:.../rtti/GoRttiMapper.java:346` — `goTypes = new GoTypeManager(this, apiSnapshot)` runs **before**
  `:348 initStructMappings()`, so the resolver is live when registration starts.
- `:351-354` — `initStructMappings()` calls `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`.

Per-class registration and name resolution:

1. `Z:.../structmapping/DataTypeMapper.java:172-198` — `registerStructure()` reads the annotation
   (`:174-175`) and calls `getType(structNames, Structure.class)` (`:176`).
2. `:310-320` — the `List<String>` overload loops the names **in annotation order** and calls
   `getType(dtName, clazz)` (`:313`). That call is virtual; on a `GoRttiMapper` instance it dispatches to the
   override at `Z:.../rtti/GoRttiMapper.java:379-396` (`@Override` at `:379`), whose body is
   `goTypes.findDataType(name)` (`:382`) plus `clazz.isInstance(result)` (`:390`).
3. `Z:.../rtti/GoTypeManager.java:355-358` `findDataType(String)` → `findTypeRec` (`:402-455`). If the name is
   not already in `typeNameIndex`, the snapshot is consulted: `apiSnapshot.getTypeDef(typeName)` (`:449`), then
   `convertApiTypeDef` (`:468-480`).
4. `Z:.../rtti/GoApiSnapshot.java:524-532` — `getTypeDef` scans the per-arch `Types` maps (the JSON's `all`
   bucket is one of them). Deserialisation dispatches on the JSON `Kind` string at `:450-465`.
5. Conversion splits by JSON `Kind`:
   - **alias** → `GoTypeManager:549-556`: resolves `aliasDef.Target` recursively (`:550`) and wraps it in a
     `TypedefDataType` (`:554-555`), cached under the alias name via `newTypeRecFromDT` (`:391-400`).
   - **struct** → `:559-596`: computes length/alignment from the JSON field list (`:563`, algorithm at
     `:1115-1128`, primitives at `:1034-1051`), builds a `StructureDataType` (`:564-566`), pre-caches it
     (`:569-574`), adds each JSON field in order with its JSON name (`:580-588`), and verifies packed length
     equals declared length (`:590-593`).
   - **slice/pointer/array/map** shortcuts: `:422-442`.
6. Because step 2 requires `Structure.class`, an alias's `TypedefDataType` is rejected at `GoRttiMapper:390`
   and the loop advances to the next candidate. This is the decisive detail for `runtime.maptype`.
7. The winning `Structure` is stored by `StructureMappingInfo.fromClass` (`Z:.../structmapping/StructureMappingInfo.java:46-55`);
   `structureName` becomes *the found structure's* name (`:76-78`), so the resolved name — not the first
   annotation entry — is what the mapping description reports (`:102-104`).
8. Field binding is by **case-insensitive component name**, not by JSON order:
   `StructureMappingInfo:406-418` builds `fieldNameLookup` from `DataTypeComponent.getFieldName().toLowerCase()`;
   `FieldMapping.fieldName` allows alternates and is documented case-insensitive
   (`Z:.../structmapping/FieldMapping.java:44-52`). Read width is the *component's* length
   (`FieldMappingInfo.java:44-50`, reads at `:246-268`).
9. Which subclass reads a given type descriptor is decided from the type's `kind` byte, not from the struct name:
   `Z:.../rtti/types/GoType.java:56-64` reads a `GoTypeDetector` (`:24-31`, field `kind`/`Kind_`) and maps
   `GoKind.Map` → `GoMapType.class` (`:35-44`, `GoKind.java:47`). `GoTypeManager.readType` uses it at `:292-296`.

**No archive GDT participates, and registration does not consult the program DTM.** `Z:.../rtti/GoRttiMapper.java:331`
calls `super(program, null)`; more decisively, `GoRttiMapper` *overrides* `getType(String, Class)` (`:379-396`), so
the generic `DataTypeMapper.getType` search order — program DTM → archive → builtin (`DataTypeMapper:282-295`) — is
bypassed for Go. The override delegates to `GoTypeManager.findDataType`, which resolves only through
`typeNameIndex` plus the JSON snapshot (`GoTypeManager:402-455`) and never queries a `DataTypeManager`. Bootstrap
structs are therefore synthesised from JSON, not looked up in DWARF/DTM. The only Go data path referenced in
source is the JSON (`GoApiSnapshot:171`, `typeinfo/golang/%sgo%s.json%s`). `D` contains 11 JSON files
(1.15.0–1.25.0) and 9 `golang_*_anybit_any.gdt` files (1.15–1.23 only); no Java string references
`golang_`/`anybit` (exit 1), and there is **no** 1.24/1.25 `.gdt`. (OBSERVED.) The `.gdt` role is outside this
pipeline — see §8.

## 2. Candidate-name inventory (OBSERVED, `Z:.../rtti/types/*.java`)

| class | `@StructureMapping(structureName=…)` | anchor |
|---|---|---|
| `GoMapType` | `runtime.maptype`, `internal/abi.MapType`, `internal/abi.OldMapType` | `GoMapType.java:32-34` |
| `GoBaseType`, `GoPlainType`, `GoTypeDetector` | `runtime._type`, `internal/abi.Type` | `GoBaseType.java:37`, `GoPlainType.java:35`, `GoTypeDetector.java:24` |
| `GoUncommonType` | `runtime.uncommontype`, `internal/abi.UncommonType` | `GoUncommonType.java:29` |
| `GoStructType` | `runtime.structtype`, `internal/abi.StructType` | `GoStructType.java:31` |
| `GoStructField` | `runtime.structfield`, `internal/abi.StructField` | `GoStructField.java:27` |
| `GoArrayType` / `GoChanType` / `GoFuncType` / `GoInterfaceType` | `runtime.<x>type`, `internal/abi.<X>Type` | `:29` / `:29` / `:34` / `:32` |
| `GoPointerType` / `GoSliceType` | `runtime.ptrtype` / `runtime.slicetype`, `internal/abi.PtrType` / `SliceType` | `:30` / `:32` |
| `GoMethod` / `GoIMethod` / `GoItab` | `runtime.method` / `runtime.imethod` / `runtime.itab`, `internal/abi.Method` / `Imethod` / `ITab` | `:30` / `:28` / `:34` |
| `GoSlice` / `GoString` / `GoName` / `GoVarlenString` | `runtime.slice` / `string` / `GoName` / `GoVarlenString` (custom/variable-length) | `:42` / `:30` / `:41` / `:36` |

`GoMapType` is the only class with **three** names; the extra `internal/abi.OldMapType` is the 1.24+ noswiss
layout name. The naming convention is the JSON's own: `runtime.*` names for the old runtime aliases,
`internal/abi.*` for the canonical definitions used by newer snapshots.

## 3. Swiss-map and version-switch answer (OBSERVED unless marked)

- **No Swiss class.** `grep -rn -i swiss` over the extracted `ghidra/app/util/bin/format/golang` tree plus both
  Golang analyzers returns **0 lines, exit 1**; the zip member listing also has 0 Swiss-named members (exit 1).
  There is no `GoSwissMapType` and no branch that constructs the Swiss layout.
- **No layout version switch in `GoMapType`.** `grep -c presentWhen GoMapType.java` → `0`, exit 1. All eight
  `@FieldMapping`s are unconditional (`GoMapType.java:37-62`), including `elemsize` alternate `ValueSize` (`:55`).
- **The framework does have one.** `presentWhen` (`FieldMapping.java:65-79`) is evaluated at registration by
  `StructureMappingInfo:306-312` (`context.isFieldPresent(...)`), implemented in `GoRttiMapper:398-417` via
  `GoVerSet.parse` (`:406`). Existing annotation users: `GoModuledata` (4), `GoFuncData` (3), `GoPcHeader` (6),
  `GoFunctabEntry` (2), `GoStructField` (2); `DataTypeMapperContext` declares the predicate (`:27-30`).
  `GoMapType` opts out.
- **Only global version gates:** `GoRttiMapper:79` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`
  (out-of-range logs `Msg.error` "Untested Go version", `:170-172`), and snapshot selection by `GoVer`
  (`GoApiSnapshot:102-116`, file-name construction `:168-178`, patch-diff fallback `:118-166`).
- **The 1.24/1.25 snapshot itself is noswiss-flavoured.** In `D/go1.24.0.json` and `go1.25.0.json`,
  `runtime.maptype` is `{"Kind":"alias","Target":"internal/abi.OldMapType"}` with position
  `runtime/map_noswiss.go:67` / `:68`; `runtime.hmap` resolves to a 56-byte struct positioned in
  `map_noswiss.go`; `internal/abi.SwissMapType` is present (112 B) but no Java name list references it. In
  `go1.23.0.json`, `runtime.maptype` aliases `internal/abi.MapType` instead. So the *data* also steers the binder
  away from Swiss even before the rejection rule in §1 step 6 applies.

Per-version facts derived from the JSON (layout computed with a faithful re-implementation of
`GoTypeManager:1034-1128`; script and exit codes in §7):

| Go | `runtime.maptype` | `internal/abi.MapType` | `OldMapType` | `SwissMapType` | `runtime.hmap` |
|---|---|---|---|---|---|
| 1.23.0 | alias → `MapType` | struct, 88 B | absent | absent | 48 B |
| 1.24.0 | alias → `OldMapType` | **absent** | struct, 88 B | struct, **112 B** | 56 B |
| 1.25.0 | alias → `OldMapType` | **absent** | struct, 88 B | struct, **112 B** | 56 B |

Field offsets (JSON-derived; agrees with the compiled-toolchain numbers in `ScoutAbiSwissLayout.md` §3):

- `OldMapType` (88 B): `Type` 0 (48), `Key` 48, `Elem` 56, `Bucket` 64, `Hasher` 72, `KeySize` 80 (1),
  `ValueSize` 81 (1), `BucketSize` 82 (2), `Flags` 84 (4).
- `SwissMapType` (112 B): `Type` 0 (48), `Key` 48, `Elem` 56, `Group` 64, `Hasher` 72, `GroupSize` 80 (8),
  `SlotSize` 88 (8), `ElemOff` 96 (8), `Flags` 104 (4), +4 pad.

## 4. What 12.1.4 actually reads for a Go 1.24/1.25 map type (INFERENCE, high confidence)

Landing point per version, following §1: **1.23 → struct `internal/abi.MapType` (88 B); 1.24/1.25 → struct
`internal/abi.OldMapType` (88 B)**. Reasons, in order: `runtime.maptype`'s alias yields a `TypedefDataType`
(rejected at `GoRttiMapper:390`); `internal/abi.MapType` has no definition in the 1.24/1.25 snapshot (query in
§7); the alias conversion has already cached `internal/abi.OldMapType` in `typeNameIndex`, so the third
candidate hits. If `runtime.maptype` were ever absent, candidate 3 would convert the same struct directly, so
the landing point does not depend on the alias.

For 1.24/1.25 the mapped Java fields land on the **Swiss** descriptor as follows. Note that `GoMapType` inherits
`GoType.typ` (`GoType.java:72-75`, field names `typ`/`Type`), so the embedded `Type` header is mapped separately
at offset 0 (48 B) and the table's offsets start after it. Widths are the bound structure's component widths
(`FieldMappingInfo:44-50`/`:246-268`); byte positions are amd64/little-endian, offsets are endian-independent.

| Java field (`GoMapType`) | bound component | offset | width | bytes it actually touches in `SwissMapType` |
|---|---|---|---|---|
| `key` | `Key` | 48 | 8 | `Key` (same) |
| `elem` | `Elem` | 56 | 8 | `Elem` (same) |
| `bucket` | `Bucket` | 64 | 8 | **`Group` pointer** |
| `hasher` | `Hasher` | 72 | 8 | `Hasher` (same) |
| `keysize` | `KeySize` | 80 | 1 | `GroupSize` byte 0 |
| `elemsize` | `ValueSize` | 81 | 1 | `GroupSize` byte 1 |
| `bucketsize` | `BucketSize` | 82 | 2 | `GroupSize` bytes 2–3 |
| `flags` | `Flags` | 84 | 4 | `GroupSize` bytes 4–7 |

Consequences, all anchored but not executable here (labels: anchors OBSERVED, mechanism INFERENCE):

- **Structure end is 88, truth is 112 → a 24-byte under-read.** `StructureContext.getStructureEnd()` is
  `start + structureDataType.getLength()` (`StructureContext.java:190-204`); `GoType.getUncommonType()` reads at
  exactly that end (`GoType.java:144-149`), i.e. at the Swiss `SlotSize` word instead of the true uncommon block
  at +112. `getEndOfTypeInfo()` (`GoType.java:137-141`) and `GoUncommonType.getEndOfTypeInfo()`
  (`GoUncommonType.java:95-103`) then compute the type's end from misread `Mcount`/`Moff` (JSON
  `internal/abi.UncommonType`: `PkgPath` int32, `Mcount` uint16, `Xcount` uint16, `Moff` uint32, pad).
- **The phantom gap is then scanned.** `GoTypeManager.init` calls `findUnindexedClosureStructTypes` (`:142`);
  ranges use `getAlignedEndOfTypeInfo` (`:157-165`) and the scan (`:169-209`) reads at 8-byte steps in the gap
  and, if the bytes look like an anonymous `GoStructType` (`:196-198`), indexes them via `getTypeRec`
  (`:203`). A 24-byte gap is exactly the window the PR names.
- **Far reads become possible with no bounds check.** `GoRttiMapper.resolveNameOff` computes
  `module.getTypesOffset() + off` (`:1062`) and calls `getGoName` (`:1063`) with **no `[types, etypes)` check**
  in 12.1.4; `getGoName` reads a `GoName` at that address (`:1073-1075`), and `GoName` is a variable-length
  `StructureReader` (`GoName.java:41`). A bogus `str`/`pkgpath` offset from a phantom or misread type therefore
  reaches the reader as-is. `getSafeName` (`GoRttiMapper:1000`, used by `GoBaseType:116-118`) masks some name
  failures, so *which* path emits aether's logged pair `[17645861, 111938854]` is left to C3's replay — I did not
  execute anything. (INFERENCE.)
- **One IOException aborts the pass.** `GolangSymbolAnalyzer.analyze` wraps `recoverGhidraDataTypes`,
  `markupGoTypes` and the rest in a single `try` (`GolangSymbolAnalyzer.java:144-183`); the catch logs
  `"Go analysis failure"` at `:182`. `GoTypeManager.markupGoTypes` itself has no per-type guard (`:147-155`).
  This is precisely the missing guard PR #9348 adds.

## 5. Comparison with the master change named by S032 (PR #9348), files list only

Source read: `https://github.com/NationalSecurityAgency/ghidra/pull/9348/files` (rendered page, read-only). A
secondary `api.github.com` files call was attempted and **rate-limited** (body:
`{"message":"API rate limit exceeded for 179.218.13.209...`, `curl_exit=0` but no file data); it was not used as
evidence. The page header reports **+35 −7**, 3 commits, base `master`.

Files in the list (exactly 3; master paths under `Ghidra/Features/Base/src/main/java/`):

| file | change |
|---|---|
| `ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java` | +7 −6: candidate list gains `"internal/abi.SwissMapType"` inserted **before** `"internal/abi.OldMapType"`; `bucket`, `keysize`, `elemsize`, `bucketsize` gain `presentWhen="-1.23"`; new `group` field with `presentWhen="1.24-"` |
| `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java` | +11 −1: `markupGoTypes` wraps each `markupSession.markup(goType,false)` in `try/catch (IOException)` and logs `"Failed to markup Go type at %s"`, continue |
| `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | +17 −0: `resolveNameOff` rejects `nameStart < typesOffset || nameStart >= typesEndOffset`, warns and returns `null` instead of reading out of bounds |

The page's diff renders the `GoMapType` base-master line as
`structureName = { "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }` — the same
structure-name list and ordering as `Z:.../types/GoMapType.java:33` — and shows paired `presentWhen` lines
(`-1.25` / `-1.23` for the old fields, `1.26-` / `1.24-` for `group`); the extracted HTML lost the +/− cell
markup, so the direction is taken from the PR description, which states the old fields are present for `-1.23`
and `group` for `1.24-`. The PR text adds: `1.26`'s swiss struct uses the canonical
`internal/abi.MapType` and is unaffected; no snapshot regeneration is needed because the 1.24/1.25 snapshots
already contain `internal/abi.SwissMapType`; the two guards are "defense in depth" and the `GoMapType` change
alone restores recovery.

Comparison verdict (OBSERVED by string/method comparison, no patched build run):

- 12.1.4 is the PR's **"before"** for all three files: same 3-entry annotation list (`GoMapType.java:33`), no
  per-type `try/catch` in `markupGoTypes` (`GoTypeManager.java:151-154`), no range check in `resolveNameOff`
  (`GoRttiMapper.java:1057-1063`).
- The PR adds **no new class** and **no code-level Go-version branch**; its "switch" is the generic
  `presentWhen` machinery already present in 12.1.4, plus name-list ordering. It also does not touch the
  snapshot JSONs.
- Therefore a 12.1.4 install cannot avoid the 1.24/1.25 map-layout misread by configuration; only a patched
  build (or avoiding the affected version) changes it. This is consistent with C3's premise; correctness of the
  PR's fix on a carrier is *not* verified here.

## 6. Calibration notes

- OBSERVED: every member:line anchor above; all grep/JSON/layout outputs in §7; the PR files page content.
- INFERENCE: the per-version landing struct (§4) and the byte-level consequence chain. They follow
  deterministically from the resolution code plus the JSON, but no Ghidra run was permitted.
- `OldMapType` = 88 B is invariant under Ghidra data-organisation alignment because no field after offset 48
  needs more than 4-byte alignment. `SwissMapType` = 112 B assumes natural 8-byte alignment for `uintptr`
  (matches the Go ABI and the compiled measurements in `ScoutAbiSwissLayout.md`); with a 4-aligned 8-byte
  organisation the JSON-derived length would be 108 B. This does not change the bound 88 B or the fact of a
  ≥20-byte under-read.
- No conflict with sibling reports: `ScoutAbiTypeUncommon.md` §6 explicitly deferred "Ghidra's `GoMapType` size
  or JSON selection"; this report answers that. Go-side layouts are owned by `ScoutAbiSwissLayout.md`; its
  88/112 numbers match my JSON-derived ones.
- No tool installs or upgrades were made. Network: only the PR page (and the rate-limited API attempt).

## 7. Commands and exit codes (as run; working dir `/tmp/r18-ghidra-base`, an extraction of `Z`)

| # | command | observed output | exit |
|---|---|---|---|
| 1 | `unzip -l Z \| grep -ic swiss` | `0` | 1 |
| 2 | `grep -rn -i swiss ghidra/app/util/bin/format/golang ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` | (no lines) | 1 |
| 3 | `grep -c presentWhen ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java` | `0` | 1 |
| 4 | `grep -rn OldMapType ghidra/app/util/bin/format/golang` | `rtti/types/GoMapType.java:33: structureName = { "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }` | 0 |
| 5 | `grep -n GOLANG_STRUCTMAPPED_CLASSES -A 7 ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | `294:` list; `:298 GoMapType.class, …`; `:353 registerStructures(...)` | 0 |
| 6 | `ls D/*.gdt \| wc -l` | `9` | 0 |
| 7 | `ls D/*.gdt \| grep -E '_1\.(24\|25)'` | (no lines) | 1 |
| 8 | `python3 -I -B -c` JSON lookup on `D/go1.24.0.json` | `runtime.maptype -> {"Kind":"alias","Target":"internal/abi.OldMapType", …}`; `internal/abi.MapType -> null`; `OldMapType` struct; `SwissMapType` struct | 0 |
| 9 | `python3 -I -B maplayout.py` (cwd `/tmp`) | `OldMapType size=88`; `SwissMapType size=112`; offsets as §3 | 0 |
| 10 | `grep -rn 'golang_' --include='*.java' . \| grep -v 'GOLANG_'` | (no lines) | 1 |
| 11 | `grep -rn 'typeinfo/golang' --include='*.java' .` | `rtti/GoApiSnapshot.java:171: "typeinfo/golang/%sgo%s.json%s"…` | 0 |
| 12 | `sha256sum Z D/go1.24.0.json D/go1.25.0.json` | the three digests in the header | 0 |
| 13 | `curl -sS … api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348/files` | rate-limit JSON (no file list) | 0 (curl) |
| 14 | `grep -rIl 'anybit' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` | (no files) | 1 |

Note: for piped commands the exit code is the last element's, as reported by the shell; the negative claims
(1,2,3,7,10,14) are the no-match greps themselves, so 1 means "no match".

## 8. Remaining unknowns

1. Which exact call site produced aether's `[17645861, 111938854]` EOF pair in 12.1.4 — the source admits
   several (uncommon read at +88, gap-scan indexing, phantom name resolution, method-array markup); C3's
   byte-level emulator and the retained log decide it. This report only fixes the offset arithmetic and the
   missing guards.
2. The 9 `golang_*.gdt` archives (1.15–1.23) are not referenced by Base-src Java; their consumer (user-applied
   archive, tooling outside `Base-src.zip`, or dead data) is not established. They are irrelevant to the map
   binding observed here.
3. Go 1.26/1.27 naming is only PR text in this report; 12.1.4 ships data through 1.25 and declares
   `1.15-1.25`, so the statements about 1.26's canonical `internal/abi.MapType` are not independently checked
   against an installed snapshot.
4. Whether the PR's patched build actually restores symbols on the two calibration carriers is claimed by the PR
   (table of counts) but was not reproduced here — out of scope and forbidden (no Ghidra runs).
