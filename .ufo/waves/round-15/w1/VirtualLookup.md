# Round 15 w1 — VirtualLookup: Tracing GoRttiMapper.getType override and GoTypeManager.findTypeRec to snapshot

seat: `KaidokuR15.VirtualLookup` (leaf scout, read-only)
axes: depth, calibration
scope: Trace polymorphic method dispatch from `DataTypeMapper.registerStructure` through `GoRttiMapper.getType` and `GoTypeManager.findTypeRec` to `GoApiSnapshot.getTypeDef`; falsify the Round 14 advisory claim in `.ufo/waves/round-14/w1/ReviewGoInference.md:57-61` asserting that `registerStructures` is independent of the snapshot.
repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
verification run by this seat: none (source reading only; no build, test, lint, gate, or target execution)
tool installs/updates: none

---

## 1. Sources and exact anchors

- **S003 Base source archive:** `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
  - SHA-256: `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches `corpus/SOURCES.md`).
  - `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`:
    - `:78`: class declaration `public class GoRttiMapper extends DataTypeMapper implements DataTypeMapperContext`
    - `:102-129`: `getSharedGoBinary(Program, TaskMonitor)` caching, `BootstrapInfoException` and `IOException` catch blocks returning `null`
    - `:165-187`: `getGoBinary(Program, TaskMonitor)` version range check, `GoApiSnapshot.get`, and `new GoRttiMapper(...)`
    - `:294-300`: `GOLANG_STRUCTMAPPED_CLASSES` list, beginning with `GoModuledata.class`
    - `:330-349`: `GoRttiMapper(...)` constructor, `super(program, null)` at `:331`, `this.goTypes = new GoTypeManager(this, apiSnapshot)` at `:346`, and `initStructMappings()` at `:348`
    - `:351-367`: `initStructMappings()` calling `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`, catching `IOException`, checking `if (apiSnapshot.isInvalid())` at `:356`, and throwing `BootstrapInfoException` at `:358-360`
    - `:379-396`: `@Override public <T extends DataType> T getType(String name, Class<T> clazz)` delegating to `goTypes.findDataType(name)` at `:382`
    - `:440-475`: `init(TaskMonitor)` called only after successful construction
  - `ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java`:
    - `:70-95`: constructor `protected DataTypeMapper(Program program, ResourceFile archiveGDT)` setting `archiveDTM = archiveGDT != null ? ... : null`
    - `:172-188`: `registerStructure(Class<T> clazz, DataTypeMapperContext context)` calling `getType(structNames, Structure.class)` at `:176` and throwing `IOException` at `:180-181` if null and not `StructureReader`
    - `:207-212`: `registerStructures(List<Class<?>> classes, DataTypeMapperContext context)` iterating over classes
    - `:282-295`: `getType(String name, Class<T> clazz)` base implementation querying `programSearchCPs`, `archiveSearchCPs`/`archiveDTM`, and `BuiltInDataTypeManager`
    - `:310-319`: `getType(List<String> names, Class<T> clazz)` calling `getType(dtName, clazz)` on `this` at `:313`
  - `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java`:
    - `:355-358`: `findDataType(String typeName)` calling `TypeRec rec = findTypeRec(typeName); return getDataType(rec);`
    - `:402-455`: `findTypeRec(String typeName)` resolving aliases, prefixes, and at `:449`: `else if ((typeDef = apiSnapshot.getTypeDef(typeName)) != null)`
    - `:825-831`: `getDataType(TypeRec rec)` returning `null` when `rec == null`
  - `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`:
    - `:102-116`: `get(GoVer, String, String, TaskMonitor)` returning `GoApiSnapshot.EMPTY` at `:115` when base file is missing
    - `:242`: `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());`
    - `:503-505`: `isInvalid()` implementation: `return arches.isEmpty();`
    - `:524-531`: `getTypeDef(String typeName)` iterating over `arches.values()`
  - `ghidra/app/util/bin/format/golang/rtti/GoModuledata.java`:
    - `:37-38`: `@StructureMapping(structureName = "runtime.moduledata")`
    - `:38`: `public class GoModuledata implements StructureMarkup<GoModuledata>` (does NOT implement `StructureReader`)
  - `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java`:
    - `:133-137`: calls `GoRttiMapper.getSharedGoBinary(program, monitor)`; returns `false` if `null`
- **S007 ChangeHistory:** `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md`
  - SHA-256: `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`
  - `:585`: "Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files."
- **Prior advisory artifact under review:**
  - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md:52-62` (Finding 2)
- **Round 14 closure adjudication (routed defect 1):**
  - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14-verifier-spotcheck.md:169-173`

---

## 2. Complete source execution trace: from constructor to snapshot

Tracing the concrete execution path through Ghidra 12.1.4 Base source demonstrates how `registerStructures` is intimately and dynamically bound to `apiSnapshot`:

```text
GolangSymbolAnalyzer.added (GolangSymbolAnalyzer.java:133)
  │
  ▼
GoRttiMapper.getSharedGoBinary (GoRttiMapper.java:107)
  │
  ▼
GoRttiMapper.getGoBinary (GoRttiMapper.java:176, 187)
  ├─► GoApiSnapshot.get(goVer, ...) (GoApiSnapshot.java:102-116)
  │     └─► Missing base JSON (e.g. go1.26.0.json) returns GoApiSnapshot.EMPTY (:115, :242)
  │           └─► apiSnapshot.isInvalid() == true (:503-505)
  │
  ▼
new GoRttiMapper(program, buildInfo, ptrSize, goVer, apiSnapshot) (GoRttiMapper.java:330-349)
  ├─► super(program, null) (:331)  [archiveDTM = null in DataTypeMapper]
  ├─► this.goTypes = new GoTypeManager(this, apiSnapshot) (:346)
  └─► initStructMappings() (:348, :351-367)
        │
        ▼
      try { registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this) } (:353)
        │
        ▼ (Inherited method DataTypeMapper.registerStructures:207-212)
      for (Class<?> clazz : classes) -> clazz = GoModuledata.class (:210)
        │
        ▼ (DataTypeMapper.registerStructure:172-188)
      sma = clazz.getAnnotation(StructureMapping.class) -> structureName: ["runtime.moduledata"] (:174-175)
      structDT = getType(structNames, Structure.class) (:176)
        │
        ▼ (DataTypeMapper.getType(List, Class):310-319)
      T result = getType(dtName, clazz) on "this" (:313)
        │
        ▼ [POLYMORPHIC VIRTUAL DISPATCH: resolved to GoRttiMapper.getType, NOT DataTypeMapper.getType]
      GoRttiMapper.getType("runtime.moduledata", Structure.class) (GoRttiMapper.java:379-396)
        │
        ▼
      goTypes.findDataType("runtime.moduledata") (:382)
        │
        ▼ (GoTypeManager.findDataType:355-358)
      findTypeRec("runtime.moduledata") (:356)
        │
        ▼ (GoTypeManager.findTypeRec:402-455)
      Not primitive, not slice/ptr/array/map
      else if ((typeDef = apiSnapshot.getTypeDef("runtime.moduledata")) != null) (:449)
        │
        ▼ (GoApiSnapshot.getTypeDef:524-531)
      arches.values() is empty (GoApiSnapshot.EMPTY) -> returns null (:529)
        │
        ▼
      findTypeRec returns null (:454)
      findDataType returns null (:357, :825-827)
      GoRttiMapper.getType returns null (:390)
        │
        ▼ Back in DataTypeMapper.registerStructure (:177-182)
      structDT == null; GoModuledata is not StructureReader (:179)
      throw new IOException("Missing struct definition for class GoModuledata, structure name: [runtime.moduledata]") (:180-181)
        │
        ▼ Caught in GoRttiMapper.initStructMappings (:355-366)
      catch (IOException e) (:355)
      if (apiSnapshot.isInvalid()) (:356) -> TRUE (arches.isEmpty() == true)
      throw new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.") (:358-360)
        │
        ▼ Caught in GoRttiMapper.getSharedGoBinary (:114-118)
      catch (BootstrapInfoException mbie) -> logs warning to MessageLog, returns null (:125)
        │
        ▼ Back in GolangSymbolAnalyzer.added (:134-137)
      goBinary == null -> returns false; analyzer aborts
```

### Detailed control-flow steps:

1. **Instantiation and Null Archive Parameter (`GoRttiMapper.java:330-349`):**
   `GoRttiMapper` invokes `super(program, null)` at line 331. In `DataTypeMapper` (`DataTypeMapper.java:85-90`), passing `null` for `ResourceFile archiveGDT` leaves `archiveDTM = null`. `programSearchCPs` and `archiveSearchCPs` remain empty. Ghidra 12.0 explicitly eliminated GDT archives in favor of JSON snapshots (S007 line 585).
2. **Registration loop (`GoRttiMapper.java:353`, `DataTypeMapper.java:207-212`):**
   `initStructMappings()` passes `GOLANG_STRUCTMAPPED_CLASSES` (`GoRttiMapper.java:294-300`) to `registerStructures`. The first class registered is `GoModuledata.class`.
3. **Structure name extraction (`DataTypeMapper.java:174-175`):**
   `GoModuledata.class` carries `@StructureMapping(structureName = "runtime.moduledata")` (`GoModuledata.java:37-38`).
4. **Virtual Method Dispatch (`DataTypeMapper.java:176, 310-313` vs `GoRttiMapper.java:379-396`):**
   `DataTypeMapper.registerStructure` calls `getType(structNames, Structure.class)` at line 176, which loops and calls `this.getType(dtName, clazz)` at line 313. Because the executing object is an instance of `GoRttiMapper`, Java's virtual method dispatch executes the override `GoRttiMapper.getType(String name, Class<T> clazz)` (`GoRttiMapper.java:379-396`). The base `DataTypeMapper.getType` implementation at lines 282-295 is bypassed entirely.
5. **Snapshot Resolution (`GoRttiMapper.java:382`, `GoTypeManager.java:356, 449`, `GoApiSnapshot.java:524`):**
   `GoRttiMapper.getType` calls `goTypes.findDataType(name)` at line 382. `GoTypeManager.findDataType` calls `findTypeRec(typeName)` at line 356. For non-primitive named structures like `"runtime.moduledata"`, line 449 evaluates `else if ((typeDef = apiSnapshot.getTypeDef(typeName)) != null)`.
6. **Absence Cascade (`GoApiSnapshot.java:115, 240, 503-505, 524-531`):**
   If the target binary version lacks an installed base snapshot (such as Go 1.26 on Ghidra 12.1.4), `GoApiSnapshot.get(...)` returns `GoApiSnapshot.EMPTY`. Under `EMPTY` (`:242`), `arches` is empty (`Map.of()`). `getTypeDef` finds no matching architecture record and returns `null`. `findTypeRec` returns `null`, and `findDataType` returns `null`.
7. **IOException Throw (`DataTypeMapper.java:177-182`):**
   `getType` returns `null`. `structDT` is `null`. `GoModuledata` does not implement `StructureReader` (it implements `StructureMarkup`, `GoModuledata.java:36`). Thus, `DataTypeMapper.registerStructure` throws `IOException("Missing struct definition for class GoModuledata, structure name: [runtime.moduledata]")` at lines 180-181.
8. **Catch and BootstrapInfoException (`GoRttiMapper.java:355-361`):**
   `initStructMappings` catches the `IOException` at line 355. Because `apiSnapshot.isInvalid()` returns `true` (`arches.isEmpty()` at `GoApiSnapshot.java:503-505`), line 358 throws `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.".formatted(goVer))`.

---

## 3. Systematic falsification of the Round 14 advisory claim

In `.ufo/waves/round-14/w1/ReviewGoInference.md:57-61`, Finding 2 asserted:

> "Crucially, `registerStructures` does not consult the snapshot. It looks up struct data types in the program and built-in data type managers (`DataTypeMapper.java:172-198, 282-295`). The snapshot only decides which message is thrown.
> The `IOException` branch (`initStructMappings` else-path, :364-365) and the `BootstrapInfoException` branch both return `null` from `getSharedGoBinary`. So for this site, snapshot absence changes the log text, not the analyzer outcome.
> **What is still unexplained:** why `registerStructure` failed for go1.26.8. The struct data-type source was not traced to the point of knowing whether a `runtime.moduledata`/`GoPcHeader` struct is present for a 1.26 program. `UNKNOWN`.
> Support: strong that snapshot absence is not, by itself, the outcome-level cause at this site."

Every clause of this claim is falsified by the concrete source trace:

| Old advisory claim in `ReviewGoInference.md:57-61` | Source observation & ground truth | Falsification verdict |
|---|---|---|
| "`registerStructures` does not consult the snapshot." | `DataTypeMapper.registerStructure` calls `getType`, which dynamically dispatches to `GoRttiMapper.getType` (`:379-396`), which calls `GoTypeManager.findDataType` (`:355-358`), which calls `findTypeRec` (`:402-455`), which directly queries `apiSnapshot.getTypeDef` (`:449`). | **FALSIFIED** (direct consultation via virtual dispatch). |
| "It looks up struct data types in the program and built-in data type managers (`DataTypeMapper.java:172-198, 282-295`)." | `GoRttiMapper` overrides `getType(String, Class)` (`GoRttiMapper.java:379-396`) without calling `super.getType`. The base implementation at `DataTypeMapper.java:282-295` is never executed. Furthermore, `archiveDTM` is explicitly `null` (`GoRttiMapper.java:331`). | **FALSIFIED** (virtual override completely replaces base lookup). |
| "The snapshot only decides which message is thrown." | A missing/invalid snapshot causes `apiSnapshot.getTypeDef("runtime.moduledata")` to return `null`, causing `getType` to return `null`, which causes `registerStructure` to throw `IOException`. Snapshot absence is the direct mechanical cause of the `IOException` inside `try { registerStructures(...) }`, not merely an selector in `catch`. | **FALSIFIED** (snapshot absence directly causes the exception). |
| "**What is still unexplained:** why `registerStructure` failed for go1.26.8... `UNKNOWN`." | Fully explained: Go 1.26 has no base JSON snapshot installed in Ghidra 12.1.4. `GoApiSnapshot.get` returns `GoApiSnapshot.EMPTY`. Without snapshot type records, `GoTypeManager.findTypeRec` cannot synthesize `runtime.moduledata`, causing `registerStructure` to fail. | **FALSIFIED / RESOLVED** (the structural lookup mechanism is fully explained by source control flow). |
| "Support: strong that snapshot absence is not, by itself, the outcome-level cause at this site." | At `initStructMappings`, snapshot absence (`EMPTY`) alone is sufficient to cause `registerStructures` to throw `IOException`, triggering `BootstrapInfoException` and returning `null` from `getSharedGoBinary`. | **FALSIFIED** (snapshot absence is sufficient to abort this constructor site). |

---

## 4. Calibration: limits, distinctions, and non-claims

To maintain strict calibration and prevent overclaiming:

1. **Constructor abort vs end-to-end Go 1.26 support:**
   Proving that snapshot absence causes `initStructMappings` to abort does **NOT** imply that merely dropping a `go1.26.0.json` snapshot file into Ghidra 12.1.4 would achieve full Go 1.26 symbol recovery.
   - Upstream commit `385e8cd` (S004) proves that supporting Go 1.26 required a coordinated bundle of modifications:
     - Adding `go.module` section lookup in `GoModuledata.java`
     - Changing `textStart` field presence in `GoPcHeader.java` from `"1.18+"` to `"1.18-1.25"`
     - Updating `GoMapType.java` for new 1.26 bucket layouts
     - Updating `GoTypeFlag.java` for 1.24+ runtime flags
   - Therefore, while snapshot absence is sufficient to abort `GoRttiMapper` at initialization, a valid snapshot alone is not sufficient for complete downstream Go 1.26 analysis.
2. **Source mechanism vs historical run cause:**
   This analysis proves the deterministic control-flow mechanism in Ghidra 12.1.4 Base source. However, because the analyzer log from the Round 4 execution on `1password-cli 2.40.0-2` was not preserved, the historical cause of that specific past failure remains **UNKNOWN** (consistent with `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:81-90`).
3. **Static source evidence vs runtime execution:**
   All findings are derived from source code analysis of the installed `Base-src.zip` archive. No live Ghidra process, target binary, or runtime analyzer was executed.

---

## 5. Proposed L1 verification checks

The following read-only commands are proposed for the L1 integrator to verify these findings once all seats finish:

```bash
# 1. Verify S003 archive digest
sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip

# 2. Verify GoRttiMapper extends DataTypeMapper and overrides getType
python3 -c '
import zipfile
z = zipfile.ZipFile("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip")
src = z.read("ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java").decode("utf-8").splitlines()
print("extends DataTypeMapper:", any("extends DataTypeMapper" in line for line in src))
print("getType override:", any("public <T extends DataType> T getType" in line for line in src))
'

# 3. Verify DataTypeMapper.registerStructure calls getType
python3 -c '
import zipfile
z = zipfile.ZipFile("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip")
src = z.read("ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java").decode("utf-8").splitlines()
for i, line in enumerate(src[171:188], 172):
    print(f"{i}: {line}")
'

# 4. Verify GoTypeManager.findTypeRec queries apiSnapshot.getTypeDef
python3 -c '
import zipfile
z = zipfile.ZipFile("/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip")
src = z.read("ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java").decode("utf-8").splitlines()
for i, line in enumerate(src[442:454], 443):
    print(f"{i}: {line}")
'
```
