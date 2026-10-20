# Round 14 — InstalledGoGate (S003 Go RTTI version-gate analysis)

- Lane: `KaidokuR14.InstalledGoGate` (leaf scout; no subagent dispatch; no tests, gates, builds, linters, or target runs)
- Worktree: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Scope: Source-only analysis of S003 (`Base-src.zip`) tracing `GoRttiMapper` declared range and unsupported-version stoppage.
- Access date: 2026-10-20 (UTC)
- Tooling directive: No packages installed or upgraded. Used existing core tools (`sha256sum`, `stat`).

---

## 1. Archive Identity & Environment

| Property | Value |
|---|---|
| Registry ID | S003 |
| Absolute path | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` |
| SHA-256 | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` |
| Byte size | 7,481,132 bytes |
| File timestamp | 2026-09-21 16:34:28.000000000 -0300 (Ghidra 12.1.4 PUBLIC release) |
| Shipped snapshots | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.{15..25}.0.json` (11 snapshots: 1.15.0 through 1.25.0) |

---

## 2. Sources Opened

All quotes below are verbatim contiguous substrings ≤25 words, opened from local verified source bytes on 2026-10-20.

| id | Member / path | Exact location | Quote (≤25 words) | Notes / Limits |
|---|---|---|---|---|
| S003 | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | Line 79 | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | Pinned declared range constant in installed Ghidra 12.1.4. |
| S003 | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | Lines 170–171 | `if (!SUPPORTED_VERSIONS.contains(goVer) ) { Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer)); }` | Version gate logging; does not throw directly at this line. |
| S003 | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | Lines 356–360 | `if (apiSnapshot.isInvalid()) { throw new BootstrapInfoException( "Missing Go bootstrap type info, unable to extract Go RTTI info." .formatted(goVer)); }` | Hard stop when snapshot is missing or invalid. |
| S003 | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` | Line 116 | `return GoApiSnapshot.EMPTY;` | Returned when no JSON snapshot file matches the requested Go version. |
| S003 | `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` | Lines 135–138 | `if (goBinary == null) { Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper"); return false; }` | Analyzer aborts analysis when `GoRttiMapper` instantiation fails. |

---

## 3. Declared Version Range

In `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`:
- **Line 79**:
  ```java
  public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");
  ```
- **Parsing logic** (`ghidra/app/util/bin/format/golang/GoVerRange.java:42–57`):
  `GoVerRange.parse("1.15-1.25")` splits the string on `[+-]` into `"1.15"` and `"1.25"`.
  Both endpoints are parsed via `GoVer.parseWildcardPatch(s)`, which yields:
  - `start = new GoVer(1, 15, -1)` (major 1, minor 15, wildcard patch -1)
  - `end = new GoVer(1, 25, -1)` (major 1, minor 25, wildcard patch -1)
- **Range containment** (`GoVerRange.java:83–87`):
  ```java
  public boolean contains(GoVer ver) {
      return (!start.isInvalid() && !end.isInvalid()) &&
          (start.isWildcard() || start.compareTo(ver) <= 0) &&
          (end.isWildcard() || end.compareTo(ver) >= 0);
  }
  ```
- **Comparison behavior** (`GoVer.java:142–152`):
  `compareTo` returns `0` when major and minor match if either patch value is `-1` (wildcard).
  Therefore, any patch release for Go 1.15 (`1.15.0` through `1.15.x`) up to Go 1.25 (`1.25.0` through `1.25.x`) is within `SUPPORTED_VERSIONS`.
- **Enumeration** (`GoRttiMapper.java:269–276` calling `GoVerRange.asList()` at `GoVerRange.java:96–107`):
  `getAllSupportedVersions()` iterates minors 15 through 25, yielding the 11 base versions `1.15.0` through `1.25.0`.
- **Boundary status**:
  - `1.14.x` and earlier: `start.compareTo(ver) > 0` $\rightarrow$ `contains == false`.
  - `1.26.x` and later: `end.compareTo(ver) < 0` $\rightarrow$ `contains == false`.

---

## 4. Where Unsupported Versions Stop Analysis

Tracing execution flow from analyzer entry to failure reveals a two-stage gate:

```
GolangSymbolAnalyzer.added() (or GolangStringAnalyzer.added())
  └─ GoRttiMapper.getSharedGoBinary(program, monitor)
       └─ GoRttiMapper.getGoBinary(program, monitor)
            ├─ [Line 170-171] if (!SUPPORTED_VERSIONS.contains(goVer)) -> Msg.error("Untested Go version")
            ├─ [Line 176] apiSnapshot = GoApiSnapshot.get(goVer, ...)
            │    └─ No typeinfo/golang/go1.26.0.json -> returns GoApiSnapshot.EMPTY (isInvalid() == true)
            ├─ [Line 187] return new GoRttiMapper(..., apiSnapshot)
            │    └─ [Line 349] initStructMappings()
            │         ├─ [Line 353] registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)
            │         │    └─ DataTypeMapper.registerStructure() -> structDT == null
            │         │         └─ throws IOException("Missing struct definition...")
            │         └─ [Line 355-360] catch (IOException) -> if (apiSnapshot.isInvalid())
            │              └─ throws BootstrapInfoException("Missing Go bootstrap type info...")
       └─ [Line 115-118] catch (BootstrapInfoException) -> log warning & return null
  └─ [Line 135-138] if (goBinary == null) -> Msg.error(...) & return false (ANALYSIS HALTED)
```

### Detailed Trace:

1. **Analyzer Entry**:
   - `GolangSymbolAnalyzer.java:105–107` / `GolangStringAnalyzer.java:95–97`:
     `canAnalyze(Program program)` checks `GoRttiMapper.isGolangProgram(program)`.
   - `GolangSymbolAnalyzer.java:134`:
     Calls `goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);`.

2. **Factory Initialization**:
   - `GoRttiMapper.java:102–129` (`getSharedGoBinary`):
     Invokes `getGoBinary(program, monitor)`. If an instance is returned, calls `supplier_result.init(monitor)`.

3. **Version Check & Snapshot Fetch**:
   - `GoRttiMapper.java:152–169` (`getGoBinary`):
     Parses `buildInfo.getGoVer()`. If invalid, throws `BootstrapInfoException("Invalid Go version string...")`.
   - `GoRttiMapper.java:170–172`:
     Checks `if (!SUPPORTED_VERSIONS.contains(goVer))`.
     **Fact**: It executes `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`. It does **not** abort or throw here.
   - `GoRttiMapper.java:176`:
     Calls `GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program), buildInfo.getGOOS(program), monitor);`.

4. **Snapshot Lookup Failure**:
   - `GoApiSnapshot.java:102–117`:
     Calls `getApiSnapshotJsonFile(goVer, monitor)`.
   - `GoApiSnapshot.java:122–124`:
     `baseVer = goVer.withPatch(0); File jsonFile = getApiSnapshotFile(baseVer, "", "");`.
   - `GoApiSnapshot.java:168–177`:
     Attempts to resolve resource `typeinfo/golang/go%s.json`.
     In Ghidra 12.1.4, files exist only for `go1.15.0.json` through `go1.25.0.json`. For `goVer >= 1.26`, `getApiSnapshotFile` returns `null`.
   - `GoApiSnapshot.java:116`:
     `bp == null` leads directly to `return GoApiSnapshot.EMPTY;` (where `EMPTY.isInvalid() == true`, line 242).

5. **Constructor & Struct Mapping Failure (The Hard Stop)**:
   - `GoRttiMapper.java:187`:
     Proceeds to `new GoRttiMapper(program, buildInfo, buildInfo.getPointerSize(), goVer, apiSnapshot)`.
   - `GoRttiMapper.java:347–349`:
     Instantiates `this.goTypes = new GoTypeManager(this, apiSnapshot);` and calls `initStructMappings();`.
   - `GoRttiMapper.java:353`:
     Calls `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);` for 25 core classes (`GoModuledata.class`, etc.).
   - `DataTypeMapper.java:176–184`:
     `Structure structDT = getType(structNames, Structure.class);` queries `goTypes.findDataType(name)` (`GoTypeManager.java:355–453`).
     Because `apiSnapshot.isInvalid() == true`, `apiSnapshot.getTypeDef(typeName)` returns `null`, and no types can be derived.
     `structDT` is `null`. Since `GoModuledata` is not a `StructureReader`, `registerStructure` throws:
     `IOException("Missing struct definition for class GoModuledata, structure name: [runtime.moduledata]")`.
   - `GoRttiMapper.java:355–360`:
     `initStructMappings` catches the `IOException`. Because `apiSnapshot.isInvalid()` is true, it throws:
     ```java
     throw new BootstrapInfoException(
         "Missing Go bootstrap type info, unable to extract Go RTTI info.".formatted(goVer));
     ```

6. **Analyzer Abort**:
   - `GoRttiMapper.java:115–118`:
     `getSharedGoBinary` catches `BootstrapInfoException`, logs a warning (`Msg.warn`), logs to the analyzer UI (`logAnalyzerMsg`), and returns `null`.
   - `GolangSymbolAnalyzer.java:135–138`:
     ```java
     if (goBinary == null) {
         Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");
         return false;
     }
     ```
     Analysis returns `false` and halts immediately. All downstream analysis (RTTI markup, function symbol recovery, closure fixes, and write barrier analysis) is never executed.
   - `GolangStringAnalyzer.java:102–106`:
     Simultaneously halts with `return false;` when `goBinary == null`.

---

## 5. Discrimination & Calibration Analysis

| Distinction | Finding |
|---|---|
| Informational vs. Blocking | `SUPPORTED_VERSIONS` (line 79 / line 170) is an **informational gate** (`Msg.error`), not a throw. It flags untested versions in logs. |
| Structural Blocker | The **hard blocking gate** is the bootstrap requirement for type information in `GoRttiMapper.initStructMappings()` (lines 356–360) throwing `BootstrapInfoException` when `GoApiSnapshot.isInvalid()` is true. |
| Dependency on Shipped Data | In installed Ghidra 12.1.4, `SUPPORTED_VERSIONS` (`1.15-1.25`) exactly mirrors the shipped snapshot files in `Ghidra/Features/Base/data/typeinfo/golang/` (`go1.15.0.json` to `go1.25.0.json`). Analysis of Go 1.26 binaries fails not merely because of a version check, but because Ghidra 12.1.4 lacks the data types and RTTI structure definitions for Go 1.26. |

---

## 6. Observed Facts, Inferences, and Unknowns

### Observed Facts:
1. `Base-src.zip` SHA-256 is `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (size 7,481,132 bytes).
2. `GoRttiMapper.SUPPORTED_VERSIONS` is declared as `GoVerRange.parse("1.15-1.25")` at line 79.
3. `GoApiSnapshot` ships JSON definitions for Go `1.15.0` through `1.25.0` only in Ghidra 12.1.4.
4. When `goVer` is not in `SUPPORTED_VERSIONS`, `GoRttiMapper.getGoBinary` emits `Msg.error` at line 171 but proceeds to attempt snapshot lookup.
5. Missing snapshots cause `initStructMappings()` to catch an `IOException` and throw `BootstrapInfoException` at line 357.
6. `GolangSymbolAnalyzer:138` and `GolangStringAnalyzer:105` check for `goBinary == null` and return `false`, aborting analysis.

### Inferences:
- Even if a user patched `SUPPORTED_VERSIONS` to include `"1.26"`, analysis of Go 1.26 binaries would still fail at `initStructMappings:357` unless a matching `go1.26.0.json` snapshot is added to `typeinfo/golang/`.

### Remaining Unknowns:
- Upstream commit S004 (`385e8cd923d09f10b1a7874108e71748875fa174`, GP-6528) details regarding how master added Go 1.26 support (e.g. whether it introduced `go1.26.0.json` and bumped `SUPPORTED_VERSIONS` to `1.15-1.26`) were scoped to peer `UpstreamGo126` and are not asserted here.

---

## 7. Checks for L1 (Not Run by Me)

1. Verify archive SHA-256: `sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`.
2. Inspect line numbers in `GoRttiMapper.java` (lines 79, 170–172, 356–360) inside `Base-src.zip`.
3. Confirm snapshot inventory: check that `Ghidra/Features/Base/data/typeinfo/golang/` contains `go1.15.0.json` through `go1.25.0.json` and lacks `go1.26.0.json`.
