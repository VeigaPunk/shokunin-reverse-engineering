# SnapshotBootstrap — S003 GoApiSnapshot get/load and version gate analysis (round 14, w1)

- Seat: `KaidokuR14.SnapshotBootstrap` (leaf scout; no subagent dispatch; no live binary execution; no test/build runs)
- Target: S003 (`Base-src.zip`) GoApiSnapshot get/load behavior; identify missing-snapshot outcomes and distinguish them from Go version-range gate; trace bounded source chain with exact clauses
- Access date: 2026-10-20
- Axes: **coverage** (complete end-to-end source chain from analyzer entry, through GoTypeManager and structure mapping, to exception propagation) and **calibration** (observed code facts separated from inference, exact line-anchored quotes $\le$ 25 whitespace words, digest-verified source, explicit historical proof limits)
- Tools: none installed or upgraded. Used Python stdlib (`zipfile`, `hashlib`) via session `eval` for read-only zip inspection. Nothing installed under RULES.md.

---

## 1. Sources opened and verified

| id | path / archive member | sha256 / identity | opened / access | notes |
|---|---|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (7,481,132 bytes) | 2026-10-20 | Installed Ghidra 12.1.4 Base source archive; SHA-256 matches `corpus/SOURCES.md` line 9 |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | 786 lines | 2026-10-20 | Primary RTTI mapper, `SUPPORTED_VERSIONS` gate, `initStructMappings`, `getType` override |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` | 534 lines | 2026-10-20 | Snapshot JSON loader, intra-minor patch fallback, OS/arch filtering, `EMPTY` sentinel, `isInvalid()` |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java` | 1,154 lines | 2026-10-20 | Constructor, `findDataType`, `findTypeRec`, type cache, and snapshot `getTypeDef` lookups |
| S003 member | `ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java` | 394 lines | 2026-10-20 | Base mapper: `archiveGDT` management, `registerStructures`, and `IOException` throw |
| S003 member | `ghidra/app/util/bin/format/golang/GoVerRange.java` | 109 lines | 2026-10-20 | Version range representation, parsing, and `contains()` |
| S003 member | `ghidra/app/util/bin/format/golang/GoVer.java` | 161 lines | 2026-10-20 | Version parsing, wildcard patch handling, `compareTo()` |
| S003 member | `ghidra/app/util/bin/format/golang/BootstrapInfoException.java` | 38 lines | 2026-10-20 | Subclass of `IOException` used for bootstrap failures |
| S003 member | `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` | 273 lines | 2026-10-20 | Consumer analyzer: calls `getSharedGoBinary`, aborts on `null` |
| S003 member | `ghidra/app/plugin/core/analysis/GolangStringAnalyzer.java` | 299 lines | 2026-10-20 | Consumer analyzer: calls `getSharedGoBinary`, aborts on `null` |
| S003 member | `ghidra/app/util/bin/format/golang/GolangDWARFFunctionFixup.java` | 305 lines | 2026-10-20 | DWARF fixup consumer: calls `getSharedGoBinary` |
| Host fs | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` | 11 base JSONs, 89 diffs | 2026-10-20 | Base snapshots: `go1.15.0.json` through `go1.25.0.json`; no `go1.26.0.json` |

---

## 2. Executive summary: Two distinct mechanisms and exact failure mechanics

Inspection of S003 source demonstrates that Ghidra 12.1.4 contains **two distinct version-related mechanisms** with completely different semantics, control flows, and failure pathways:

1. **The Go version-range gate (`SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`)**:
   - Location: `GoRttiMapper.java:79, 170–172`.
   - Effect: **Advisory log error only; does not abort**.
   - Behavior: When `!SUPPORTED_VERSIONS.contains(goVer)` holds (e.g. for Go 1.26), Ghidra logs `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`.
   - Control flow: It **does NOT throw an exception**, does **NOT** return `null`, does **NOT** post to `AutoAnalysisManager`'s UI message log, and does **NOT** halt analysis. Execution immediately proceeds to snapshot loading.

2. **The snapshot get/load and structure-mapping bootstrap gate**:
   - Location: `GoApiSnapshot.java:102–146` and `GoRttiMapper.java:351–367`.
   - Effect: **Fatal initialization failure (`BootstrapInfoException`)**.
   - Triggering condition: `apiSnapshot.isInvalid()` evaluates to `true` either when:
     1. The major.minor base snapshot JSON does not exist (such as `go1.26.0.json`), returning `GoApiSnapshot.EMPTY`; OR
     2. The snapshot JSON exists, but does not contain matching keys for the binary's `GOOS`/`GOARCH` search list, leaving the snapshot's `arches` map empty.
   - Exact failure path:
     - `GoRttiMapper` does **not** abort simply upon receiving an invalid snapshot.
     - Instead, construction continues until `initStructMappings()` invokes `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`.
     - `registerStructures` attempts to resolve mandatory Go runtime structures (such as `runtime.moduledata`).
     - Because `GoRttiMapper` overrides `getType` to query `GoTypeManager.findDataType()` without any Program DTM or archive GDT fallback, the missing snapshot causes type lookup to fail.
     - `DataTypeMapper.registerStructure()` throws an `IOException`.
     - `initStructMappings()` catches this `IOException`, checks `if (apiSnapshot.isInvalid())`, and only then converts it into `throw new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`.
     - `getSharedGoBinary()` catches `BootstrapInfoException`, logs a warning, posts to the UI analysis message log, and returns `null`.
     - Downstream analyzers (`GolangSymbolAnalyzer`, `GolangStringAnalyzer`) receive `goBinary == null` and abort.

**Diagnostic consequence**: Analysis failure on Go 1.26 in Ghidra 12.1.4 is caused by the **missing snapshot and subsequent structure registration failure**, **NOT** by `SUPPORTED_VERSIONS`. Patching `SUPPORTED_VERSIONS` alone leaves analysis completely non-functional.

---

## 3. End-to-end bounded source trace

### Step 1: Analyzer consumers request `GoRttiMapper`
Ghidra's Go analyzers request the session singleton via `GoRttiMapper.getSharedGoBinary`:
- `GolangSymbolAnalyzer.java:133–137`:
  ```java
  goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
  if (goBinary == null) {
      Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");
      return false;
  }
  ```
- `GolangStringAnalyzer.java:103–107`:
  ```java
  goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
  if (goBinary == null) {
      Msg.error(this, "Go string analyzer error: unable to get GoRttiMapper");
      return false;
  }
  ```

### Step 2: `getSharedGoBinary()` session caching and exception handling
In `GoRttiMapper.java:102–129`:
```java
public static GoRttiMapper getSharedGoBinary(Program program, TaskMonitor monitor) {
    GoRttiMapper goBinary = TransientProgramProperties.getProperty(program, GoRttiMapper.class,
        TransientProgramProperties.SCOPE.ANALYSIS_SESSION, GoRttiMapper.class, () -> {
            Msg.info(GoRttiMapper.class, "Reading Go binary info: " + program.getName());
            try {
                GoRttiMapper supplier_result = getGoBinary(program, monitor);
                if (supplier_result != null) {
                    supplier_result.init(monitor);
                    return supplier_result;
                }
            }
            catch (BootstrapInfoException mbie) {
                Msg.warn(GoRttiMapper.class, mbie.getMessage());
                logAnalyzerMsg(program, mbie.getMessage());
            }
            catch (IOException e) {
                Msg.error(GoRttiMapper.class, "Failed to read Go info", e);
                logAnalyzerMsg(program, e.getMessage());
            }

            return null;
        });

    return goBinary;
}
```
- `BootstrapInfoException` is caught, logged at `Msg.warn`, and passed to `logAnalyzerMsg()` (`AutoAnalysisManager.getAnalysisManager(program).getMessageLog().appendMsg(msg)`), which surfaces in a modal popup at analysis end.
- The method returns `null`, causing calling analyzers to abort.

### Step 3: `getGoBinary()` version-range check only logs
In `GoRttiMapper.java:151–188`:
1. Version extraction from `GoBuildInfo`:
   `GoVer goVer = buildInfo.getGoVer();`
   If `goVer.isInvalid()`, it throws `BootstrapInfoException("Invalid Go version string...")`.
2. Version-range check:
   ```java
   if (!SUPPORTED_VERSIONS.contains(goVer) ) {
       Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));
   }
   ```
   `SUPPORTED_VERSIONS` (`GoRttiMapper.java:79`):
   `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`
   - For Go 1.26, `contains(goVer)` is `false`.
   - **Observed behavior**: Ghidra logs `Msg.error(..., "Untested Go version [1.26]")`.
   - **No exception is thrown**, `null` is not returned, and execution proceeds directly to line 174.

### Step 4: Snapshot lookup (`GoApiSnapshot.get`) and invalidation paths
Lines 174–187:
```java
GoApiSnapshot apiSnapshot;
try {
    apiSnapshot = GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program),
        buildInfo.getGOOS(program), monitor);
    if (!apiSnapshot.getVer().isInvalid()) {
        Msg.info(GoRttiMapper.class,
            "Using Go API snapshot for version %s".formatted(apiSnapshot.getVer()));
    }
}
catch (CancelledException e) {
    throw new IOException("Error fetching Go API snapshot file: cancelled");
}

return new GoRttiMapper(program, buildInfo, buildInfo.getPointerSize(), goVer, apiSnapshot);
```

In `GoApiSnapshot.java:102–146`:
```java
public static GoApiSnapshot get(GoVer goVer, String goArch, String goOS, TaskMonitor monitor)
        throws IOException, CancelledException {

    try (ByteProvider bp = getApiSnapshotJsonFile(goVer, monitor)) {
        if (bp != null) {
            try (InputStream is = bp.getInputStream(0)) {
                List<String> archSearchOrder = List.of(goOS + "-" + goArch, goOS,
                    IS_GOOS_UNIX.contains(goOS) ? "unix" : "", goArch, "all");

                return GoApiSnapshot.read(is, archSearchOrder, goVer);
            }
        }
    }
    return GoApiSnapshot.EMPTY;
}
```

Two distinct conditions cause `apiSnapshot.isInvalid() == true`:

#### Invalidation Path A: Missing base JSON file
In `getApiSnapshotJsonFile(GoVer goVer, ...)` (lines 118–127):
```java
GoVer baseVer = goVer.withPatch(0);
File jsonFile = getApiSnapshotFile(baseVer, "", "");
if (jsonFile == null) {
    return null;
}
```
- `getApiSnapshotFile(baseVer, "", "")` attempts to locate `typeinfo/golang/go%s.json` via Ghidra's `Application.getModuleDataFile()`.
- For Go 1.26.x, `baseVer` is `1.26.0`. No `go1.26.0.json` exists in Ghidra 12.1.4.
- `getApiSnapshotFile` catches the missing file `IOException` and returns `null`.
- `getApiSnapshotJsonFile` returns `null`.
- `GoApiSnapshot.get()` returns `GoApiSnapshot.EMPTY` (line 115).
- `GoApiSnapshot.EMPTY` is defined as `new GoApiSnapshot(GoVer.INVALID, Map.of())` (line 242).
- `apiSnapshot.isInvalid()` evaluates `arches.isEmpty()`, returning `true`.
- **Intra-minor patch fallback limit**: In `getPatchVerDiffFile(GoVer goVer)` (lines 148–166), patch fallback walks backwards via `patchVer.prevPatch()`. This applies strictly within the same minor version (e.g. `1.24.9` $\to$ `1.24.6.diff` $\to$ `1.24.0.json`). There is **zero cross-minor fallback** (it never falls back from `1.26` to `1.25`).

#### Invalidation Path B: Missing or unsupported GOOS / GOARCH in existing JSON
Even when the base JSON exists (e.g. for Go 1.25):
- `archSearchOrder` is constructed as `[goOS + "-" + goArch, goOS, "unix" (if unix), goArch, "all"]`.
- In `GoApiSnapshot.read(InputStream is, List<String> archNames, GoVer ver)` (lines 205–240):
  ```java
  Set<String> archNamesToKeep = new HashSet<>(archNames);
  ...
  while (reader.peek() == JsonToken.NAME) {
      String archName = reader.nextName();
      if (!archNamesToKeep.contains(archName)) {
          reader.skipValue();
          continue;
      }
      GoArch arch = gson.fromJson(reader, GoArch.class);
      arches.put(archName, arch);
  }
  ...
  Map<String, GoArch> results = new LinkedHashMap<>();
  for (String archName : archNames) {
      GoArch arch = arches.get(archName);
      if (arch != null) {
          results.put(archName, arch);
      }
  }
  return new GoApiSnapshot(ver, results);
  ```
- If the binary has a `GOOS` / `GOARCH` combination that has no entries in the snapshot JSON (and no matching generic fallback key), `results` is empty.
- `arches.isEmpty()` is `true`, and `apiSnapshot.isInvalid()` returns `true`.
- This explains the developer comment at `GoRttiMapper.java:357`: `"// a normal'ish situation where we don't have type info for this arch/binary"`.

### Step 5: `GoTypeManager` construction and absence of DTM/GDT fallback
In `GoRttiMapper` constructor (`GoRttiMapper.java:329–349`):
```java
public GoRttiMapper(Program program, GoBuildInfo buildInfo, int ptrSize, GoVer goVer,
        GoApiSnapshot apiSnapshot) throws IOException, BootstrapInfoException {
    super(program, null);
    ...
    this.apiSnapshot = apiSnapshot;
    ...
    this.goTypes = new GoTypeManager(this, apiSnapshot);

    initStructMappings();
}
```
Critical structural facts:
1. `super(program, null)`: Passes `null` for `archiveGDT` to the base `DataTypeMapper`. Base `archiveDTM` is therefore `null`.
2. `GoTypeManager` constructor (`GoTypeManager.java:81–87`):
   ```java
   public GoTypeManager(GoRttiMapper goBinary, GoApiSnapshot apiSnapshot) {
       this.goBinary = goBinary;
       this.apiSnapshot = apiSnapshot;
       this.dtm = goBinary.getDTM();
       this.ptrSize = goBinary.getPtrSize();
       this.voidPtrDT = dtm.getPointer(VoidDataType.dataType);
   }
   ```
   `GoTypeManager` holds only references to `goBinary`, `apiSnapshot`, and program `dtm`.
3. `GoTypeManager.findTypeRec(String typeName)` (`GoTypeManager.java:402–455`):
   - Handles static aliases (`byte` $\to$ `uint8`, `rune` $\to$ `int32`).
   - Recursively unpacks slices (`[]`), pointers (`*`), arrays (`[N]`), and maps (`map[`).
   - If primitive (`primitiveTypeKind.isPrimitive()`), calls `makeBasicType`.
   - For all other types (named structs, interfaces, etc.):
     ```java
     else if ((typeDef = apiSnapshot.getTypeDef(typeName)) != null) {
         result = convertApiTypeDef(typeSymbolName, typeDef);
     }
     ```
   - **No fallback**: If `apiSnapshot.getTypeDef(typeName)` returns `null`, `result` remains `null`. `GoTypeManager` does **NOT** search the program `dtm`, does not query built-in DTMs, and has no GDT archive.
4. `GoRttiMapper.getType` override (`GoRttiMapper.java:380–396`):
   ```java
   @Override
   public <T extends DataType> T getType(String name, Class<T> clazz) {
       try {
           DataType result = goTypes.findDataType(name);
           if (result == null && GoPcHeader.GO_STRUCTURE_NAME.equals(name) &&
               Structure.class.isAssignableFrom(clazz)) {
               result = clazz.cast(GoPcHeader.createArtificialGoPcHeaderStructure(GOLANG_CP,
                   program.getDataTypeManager()));
           }
           return clazz.isInstance(result) ? clazz.cast(result) : null;
       }
       catch (IOException e) {
           Msg.warn(this, "Unable to find Go type %s".formatted(name), e);
           return null;
       }
   }
   ```
   `GoRttiMapper` overrides `DataTypeMapper.getType` and delegates directly to `goTypes.findDataType(name)`. It does **not** call `super.getType(name, clazz)` (which would have searched `programDTM` / `archiveDTM`). The only synthetic fallback in the entire class is for `runtime.pcHeader` on Go $\le 1.15$.
   For all other types (specifically `runtime.moduledata`), if `apiSnapshot` is empty, `getType` returns `null`.

### Step 6: `initStructMappings()` failure mechanics
In `GoRttiMapper.java:351–367`:
```java
private void initStructMappings() throws IOException {
    try {
        registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);
    }
    catch (IOException e) {
        if (apiSnapshot.isInvalid()) {
            // a normal'ish situation where we don't have type info for this arch/binary
            throw new BootstrapInfoException(
                "Missing Go bootstrap type info, unable to extract Go RTTI info."
                        .formatted(goVer));
        }

        // we have type info, but something failed in the struct mappings 
        throw new IOException(
            "Invalid Go bootstrap struct mapping info: %s".formatted(goVer), e);
    }
}
```

Notice the exact logic:
- `apiSnapshot.isInvalid()` is **NOT an entry guard** in `initStructMappings()`.
- Ghidra unconditionally attempts `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`.
- `GOLANG_STRUCTMAPPED_CLASSES` contains 25 classes (`GoModuledata.class`, `GoName.class`, `GoSlice.class`, etc.).
- In `DataTypeMapper.registerStructure(Class<T> clazz, DataTypeMapperContext context)` (`DataTypeMapper.java:172–188`):
  ```java
  StructureMapping sma = clazz.getAnnotation(StructureMapping.class);
  List<String> structNames = sma != null ? Arrays.asList(sma.structureName()) : List.of();
  Structure structDT = getType(structNames, Structure.class);
  if (structDT == null) {
      String dtName = structNames.isEmpty() ? "<missing>" : String.join("|", structNames);
      if (!StructureReader.class.isAssignableFrom(clazz)) {
          throw new IOException("Missing struct definition for class %s, structure name: [%s]"
                  .formatted(clazz.getSimpleName(), dtName));
      }
  ...
  ```
- For `GoModuledata.class`, `structNames` is `["runtime.moduledata"]`.
- `getType(["runtime.moduledata"], Structure.class)` calls `GoRttiMapper.getType("runtime.moduledata", Structure.class)`, which calls `goTypes.findDataType("runtime.moduledata")`.
- Because `apiSnapshot` is empty, `findDataType` returns `null`. `structDT` is `null`.
- `GoModuledata` does not implement `StructureReader`.
- `registerStructure` throws `new IOException("Missing struct definition for class GoModuledata, structure name: [runtime.moduledata]")`.
- `initStructMappings()` catches this `IOException`.
- Only inside the catch block does it evaluate `if (apiSnapshot.isInvalid())`:
  - If `true` $\to$ throws `new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`.
  - If `false` (valid snapshot present, but mapping failed due to internal layout corruption) $\to$ throws `new IOException("Invalid Go bootstrap struct mapping info: ...", e)`.

---

## 4. Exact verified clauses from S003 ($\le$ 25 whitespace words each)

All clauses below are contiguous exact substrings from S003 (`Base-src.zip`), verified against source bytes:

| # | Source file & line | Contiguous clause | Word count | Function in chain |
|---|---|---|---|---|
| Q1 | `GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | 7 | Pinned version-range constant |
| Q2 | `GoRttiMapper.java:170–172` | `if (!SUPPORTED_VERSIONS.contains(goVer) ) {`<br>`Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`<br>`}` | 10 | Range check only logs error, does not abort |
| Q3 | `GoRttiMapper.java:176–177` | `apiSnapshot = GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program),`<br>`buildInfo.getGOOS(program), monitor);` | 6 | Snapshot acquisition call |
| Q4 | `GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | 2 | Sentinel returned on missing snapshot |
| Q5 | `GoApiSnapshot.java:242` | `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());` | 9 | `EMPTY` definition with empty arches map |
| Q6 | `GoApiSnapshot.java:503–505` | `public boolean isInvalid() {`<br>`return arches.isEmpty();`<br>`}` | 7 | Invalidation test based on empty arches |
| Q7 | `GoApiSnapshot.java:123–126` | `File jsonFile = getApiSnapshotFile(baseVer, "", "");`<br>`if (jsonFile == null) {`<br>`return null;`<br>`}` | 14 | Missing base JSON returns null provider |
| Q8 | `GoApiSnapshot.java:158–161` | `if (patchVer.getPatch() != goVer.getPatch()) {`<br>`Msg.warn(GoApiSnapshot.class,`<br>`"Falling back from %s to %s for Go API snapshot".formatted(goVer, patchVer));`<br>`}` | 18 | Intra-minor patch fallback logging |
| Q9 | `DataTypeMapper.java:179–182` | `if (!StructureReader.class.isAssignableFrom(clazz)) {`<br>`throw new IOException("Missing struct definition for class %s, structure name: [%s]"`<br>`.formatted(clazz.getSimpleName(), dtName));`<br>`}` | 17 | `registerStructure` throws `IOException` when type missing |
| Q10 | `GoRttiMapper.java:356–357` | `if (apiSnapshot.isInvalid()) {`<br>`// a normal'ish situation where we don't have type info for this arch/binary` | 16 | Catch block check distinguishing missing snapshot |
| Q11 | `GoRttiMapper.java:358–360` | `throw new BootstrapInfoException(`<br>`"Missing Go bootstrap type info, unable to extract Go RTTI info."`<br>`.formatted(goVer));` | 15 | Fatal bootstrap exception thrown from catch block |
| Q12 | `GoRttiMapper.java:114–117` | `catch (BootstrapInfoException mbie) {`<br>`Msg.warn(GoRttiMapper.class, mbie.getMessage());`<br>`logAnalyzerMsg(program, mbie.getMessage());`<br>`}` | 9 | Singleton supplier logs warn and returns null |
| Q13 | `GolangSymbolAnalyzer.java:134–137` | `if (goBinary == null) {`<br>`Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");`<br>`return false;`<br>`}` | 17 | Consumer analyzer aborts when mapper is null |

---

## 5. Comparative distinction matrix

| Dimension | Go Version-Range Gate | Snapshot Bootstrap Gate |
|---|---|---|
| **Source location** | `GoRttiMapper.java:79, 170–172` | `GoApiSnapshot.java:102–146`; `GoRttiMapper.java:351–367` |
| **Evaluated condition** | `!SUPPORTED_VERSIONS.contains(goVer)` | `apiSnapshot.isInvalid()` after `registerStructures` throws `IOException` |
| **Trigger conditions** | Go version `< 1.15` or `> 1.25` | 1. Absent base JSON (e.g. `go1.26.0.json`), OR<br>2. Snapshot exists but lacks binary's `GOOS`/`GOARCH` keys |
| **Direct action** | Logs `Msg.error` to application log | Throws `BootstrapInfoException` inside `initStructMappings` catch block |
| **Impact on execution** | **Zero control flow impact**: does not abort, does not return null | **Fatal abort**: `getSharedGoBinary` returns `null`; analyzers abort |
| **Surfaces in GUI?** | **No** (does not call `logAnalyzerMsg`) | **Yes** (`logAnalyzerMsg` triggers modal dialog at analysis completion) |
| **Alternative fallback** | None | Intra-minor patch fallback (`prevPatch()`); **no cross-minor fallback**, **no DTM/GDT fallback** |
| **Effect of isolated patch** | Updating range to `1.15-1.26` suppresses log, but **analysis still aborts** at `initStructMappings` | Providing `go1.26.0.json` allows full structure mapping despite "Untested Go version" log |

---

## 6. Calibration note: Historical operation vs. Source-proven mechanism

In historical testing (e.g. `1password-cli` / `op` 2.34.1 $\to$ 2.40.0, Go 1.25.7 $\to$ 1.26.8 documented in `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`), symbol recovery collapsed from 33,060 names to 11,588 generic `FUN_*` labels under Ghidra 12.1.4.

**Calibration boundaries**:
1. **Source route is mechanically proven**: Tracing S003 proves deterministically that stock Ghidra 12.1.4 cannot initialize `GoRttiMapper` on Go 1.26 binaries because `go1.26.0.json` is absent, triggering `BootstrapInfoException` and returning `null`.
2. **Historical causal path remains unproven**: Because Ghidra application and analysis session logs from that original run were deleted and not retained, it cannot be strictly proven from preserved artifacts whether the historical failure was caused specifically by this `BootstrapInfoException`, by an unhandled DWARF error, or by another runtime condition.
3. **Plausibility vs certainty**: The S003 source chain establishes that the missing snapshot route is an unavoidable, deterministic blocker in stock 12.1.4 that precedes any binary parsing. However, the historical operation's precise causal path must remain classified as **plausible based on source analysis, but unproven on historical run records**.

---

## 7. Residual risk and limitations

- **Source evidence scope**: Analysis is derived strictly from S003 source code and file presence in installed Ghidra 12.1.4.
- **No live execution performed**: No binaries were analyzed in Ghidra; no dynamic tests or builds were executed in this seat.
- **Upstream commit distinction**: Upstream GP-6528 commit `385e8cd923d09f10b1a7874108e71748875fa174` (S004) confirms this dual requirement: it both bumped `SUPPORTED_VERSIONS` to `1.15-1.26` AND introduced `go1.26.0.json`.
