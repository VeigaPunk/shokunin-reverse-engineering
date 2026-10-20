# Round 15 w1 — BaseLookup: GoApiSnapshot base name selection and missing-file path

- Seat: `KaidokuR15.BaseLookup` (leaf scout; no subagent dispatch; read-only source inspection)
- Target: Trace `GoApiSnapshot` base name selection and missing-file path, exact source lines.
- Axes: **depth** (complete end-to-end trace from version parsing to `Application` data resolution and analyzer exception abort) and **calibration** (observed source facts distinguished from inference, exact line anchors, uncalled helper disambiguation, and explicit historical causality limits)
- Repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Report path: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/BaseLookup.md`
- Verification executed by this seat: none (read-only source inspection; no test, build, lint, gate, or provider execution)
- Tool installs / updates: none

---

## 1. Sources opened and verified

| Source ID | Path / Archive member | SHA-256 / Size | Role in trace |
|---|---|---|---|
| S003 archive | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (7,481,132 bytes) | Primary Ghidra 12.1.4 Base source archive |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` (534 lines) | — | Snapshot loading, base version zeroing, patchverdiff search, `EMPTY` sentinel, `isInvalid()` |
| S003 member | `ghidra/app/util/bin/format/golang/GoVer.java` (161 lines) | — | Version parsing, `withPatch(0)` normalization, 3-segment string formatting |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` (786 lines) | — | Entry point, advisory version check, mapper instantiation, `initStructMappings`, `BootstrapInfoException` |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/JsonPatchApplier.java` (84 lines) | — | Patch applier taking base `File` |
| S003 member | `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` (273 lines) | — | Analyzer consumer checking `goBinary == null` |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java` (1,154 lines) | — | Type lookup delegating to `apiSnapshot.getTypeDef` |
| Generic archive | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Generic/lib/Generic-src.zip` | `dfaa7ff553ea1a04d80a1cf65ffce27ca0ebae4df841328ebcc474586d1b262a` (1,677,931 bytes) | Ghidra Application framework source archive |
| Generic member | `ghidra/framework/Application.java` (1,030 lines) | — | Module data file resolution (`getModuleDataFile`, `getDataFileInModule`) |
| Utility archive | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Utility/lib/Utility-src.zip` | `7be33f6706e22c9535eb0fc69eb24a919f2982d6da8d338f0e5b746ca79d7247` (978,401 bytes) | Utility source archive |
| Utility member | `generic/jar/ResourceFile.java` (367 lines) | — | `getFile(true)` extracting filesystem file |
| Installed layout | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` | Directory | 11 base JSON files (`go1.15.0.json` .. `go1.25.0.json`); 123 patch diffs; no `go1.26.0.json` |

---

## 2. Base name selection mechanism

The selection of the base snapshot filename proceeds through a strict 4-step sequence within `GoApiSnapshot` and `GoVer`:

### Step 2.1: Input version reception and patch clamping
- **Entry point**: `GoRttiMapper.getGoBinary` (`GoRttiMapper.java:176-177`) passes `goVer` to `GoApiSnapshot.get(goVer, goArch, goOS, monitor)`.
- `GoApiSnapshot.get` (`GoApiSnapshot.java:105`) calls `getApiSnapshotJsonFile(goVer, monitor)`.
- In `GoApiSnapshot.getApiSnapshotJsonFile` (`GoApiSnapshot.java:122`):
  ```java
  GoVer baseVer = goVer.withPatch(0);
  ```
- **Patch normalization**: In `GoVer.java:136-138`:
  ```java
  public GoVer withPatch(int newPatchNum) {
      return new GoVer(major, minor, newPatchNum);
  }
  ```
  The incoming binary version (e.g. Go 1.25.3 or 1.26.1) has its patch component replaced with `0`. The `major` and `minor` fields are preserved unchanged.

### Step 2.2: String formatting of `baseVer`
- In `GoVer.java:154-159`:
  ```java
  @Override
  public String toString() {
      return patch != -1 
              ? "%d.%d.%d".formatted(major, minor, patch)
              : "%d.%d".formatted(major, minor);
  }
  ```
- Because `baseVer` was constructed via `withPatch(0)`, its `patch` field is `0`.
- The condition `patch != -1` evaluates to `true`.
- Therefore, `baseVer.toString()` strictly formats as `"%d.%d.%d".formatted(major, minor, 0)`.
- **Concrete examples**:
  - `go1.24.3` $\rightarrow$ `baseVer` is `(1, 24, 0)` $\rightarrow$ `baseVer.toString()` is `"1.24.0"`.
  - `go1.25.0` $\rightarrow$ `baseVer` is `(1, 25, 0)` $\rightarrow$ `baseVer.toString()` is `"1.25.0"`.
  - `go1.26.1` $\rightarrow$ `baseVer` is `(1, 26, 0)` $\rightarrow$ `baseVer.toString()` is `"1.26.0"`.
- Note: A two-segment string (`"%d.%d"`) is emitted by `GoVer.toString()` only if `patch == -1` (wildcard patch parsed via `parseWildcardPatch`). Because `withPatch(0)` explicitly passes `0`, the base version string is **never** two-segment.

### Step 2.3: Relative data path construction in `getApiSnapshotFile`
- In `GoApiSnapshot.java:123`:
  ```java
  File jsonFile = getApiSnapshotFile(baseVer, "", "");
  ```
- In `GoApiSnapshot.java:168-178`:
  ```java
  static File getApiSnapshotFile(GoVer goVer, String subdir, String suffix) {
      try {
          ResourceFile rfile = Application.getModuleDataFile(
              "typeinfo/golang/%sgo%s.json%s".formatted(subdir, goVer.toString(), suffix));
          return rfile.getFile(true);
      }
      catch (IOException e) {
          return null;
      }
  }
  ```
- With parameters `subdir = ""` and `suffix = ""`, the format string `"typeinfo/golang/%sgo%s.json%s"` evaluates to:
  `"typeinfo/golang/go" + baseVer.toString() + ".json"`.
- For Go 1.25.x: `"typeinfo/golang/go1.25.0.json"`.
- For Go 1.26.x: `"typeinfo/golang/go1.26.0.json"`.

### Step 2.4: Disambiguation of uncalled helper `getApiFile`
- Lines 183–192 of `GoApiSnapshot.java` define:
  ```java
  public static File getApiFile(File baseDir, GoVer ver) {
      String filename =
          "go%d.%d.%d.json".formatted(ver.getMajor(), ver.getMinor(), ver.getPatch());
      File f = new File(baseDir, filename);
      if (!f.isFile() && ver.getPatch() == 0) {
          filename = "go%d.%d.json".formatted(ver.getMajor(), ver.getMinor());
          f = new File(baseDir, filename);
      }
      return f.isFile() ? f : null;
  }
  ```
- **Crucial distinction**: `getApiFile` contains logic falling back from `"go%d.%d.%d.json"` to `"go%d.%d.json"`. However:
  1. `getApiFile` is **never called** anywhere in Ghidra's Base source code (confirmed by global symbol scan across `Base-src.zip`). It appears only in generated Python predefs/typestubs.
  2. Runtime snapshot resolution exclusively invokes `getApiSnapshotFile`, which directly uses `Application.getModuleDataFile("typeinfo/golang/go%s.json".formatted(baseVer.toString()))`.
  3. Consequently, runtime base selection **never** searches for or accepts two-segment filenames such as `go1.25.json` or `go1.26.json`. It strictly demands the three-segment filename `go<major>.<minor>.0.json`.
  4. Base selection also contains **no fallback across minor versions**: a binary with version 1.26.0 will never fall back to `go1.25.0.json`.

---

## 3. Missing-file path and exception propagation trace

When a base JSON file is absent (such as `go1.26.0.json` on Ghidra 12.1.4), the execution path traces through seven distinct stages across three source packages:

```
[GoRttiMapper.getGoBinary:176]
  │
  ▼
[GoApiSnapshot.get:105]
  │
  ▼
[GoApiSnapshot.getApiSnapshotJsonFile:123]
  │
  ▼
[GoApiSnapshot.getApiSnapshotFile:170]
  │
  ▼
[Application.getModuleDataFile:954] ──(Base module data/ directory)
  │
  ▼
[Application.getDataFileInModule:362]
  │ ──> module.findModuleFile("data/typeinfo/golang/go1.26.0.json") == null
  │ ──> throws FileNotFoundException (line 365)
  ▼
[GoApiSnapshot.getApiSnapshotFile:175]
  │ ──> catches IOException, silently returns null
  ▼
[GoApiSnapshot.getApiSnapshotJsonFile:124-126]
  │ ──> jsonFile == null: returns null immediately! (patch diff search bypassed)
  ▼
[GoApiSnapshot.get:115]
  │ ──> bp == null: returns GoApiSnapshot.EMPTY (arches empty, ver INVALID)
  ▼
[GoRttiMapper.getGoBinary:178-187]
  │ ──> apiSnapshot.getVer().isInvalid() == true: suppresses "Using Go API snapshot" log
  │ ──> returns new GoRttiMapper(..., apiSnapshot)
  ▼
[GoRttiMapper.<init>:348 -> initStructMappings:352]
  │ ──> registerStructures throws IOException (types not found via empty snapshot)
  │ ──> catches IOException; apiSnapshot.isInvalid() == true (line 356)
  │ ──> throws BootstrapInfoException("Missing Go bootstrap type info...") (line 358)
  ▼
[GoRttiMapper.getSharedGoBinary:114-117]
  │ ──> catches BootstrapInfoException; logs Msg.warn; logs to AutoAnalysisManager MessageLog
  │ ──> returns null
  ▼
[GolangSymbolAnalyzer.added:134-137]
  │ ──> goBinary == null; logs Msg.error("...unable to get GoRttiMapper"); returns false
```

### Detailed stage breakdown:

1. **Module resolution in `Application`**:
   - `Application.getModuleDataFile("typeinfo/golang/go1.26.0.json")` (`Application.java:954-963`).
   - Line 956: `ResourceFile moduleDirectory = getMyModuleRootDirectory();` identifies the caller's module root (`Ghidra/Features/Base`).
   - Line 962: Delegates to `app.getDataFileInModule(relativeDataPath, moduleDirectory.getName())`.
2. **Data directory traversal in `Application`**:
   - In `Application.java:354-375`:
     - Line 62: `private static final String DATA_DIRNAME = "data/";`.
     - Line 362: `ResourceFile foundFile = module.findModuleFile(DATA_DIRNAME + relativeDataPath);`.
     - For `relativeDataPath = "typeinfo/golang/go1.26.0.json"`, it checks for physical file:
       `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json`.
     - When absent, `foundFile` is `null`.
     - Lines 364-367:
       ```java
       if (foundFile == null) {
           throw new FileNotFoundException(
               "file " + relativeDataPath + " does not exist in module " + moduleName);
       }
       ```
3. **Silent exception suppression in `GoApiSnapshot`**:
   - In `GoApiSnapshot.java:175-177`:
     ```java
     catch (IOException e) {
         return null;
     }
     ```
   - The `FileNotFoundException` is caught silently. No warning or error message is written to the log.
4. **Immediate termination of file provider**:
   - In `GoApiSnapshot.java:124-126`:
     ```java
     if (jsonFile == null) {
         return null;
     }
     ```
   - **Critical observation**: Because `jsonFile == null`, `getPatchVerDiffFile(goVer)` at line 128 is **never reached**. The entire patch-diff machinery is bypassed when the base snapshot is absent.
5. **Sentinel return**:
   - In `GoApiSnapshot.java:105-116`: `bp` is `null`, so lines 106–113 are skipped.
   - Line 115: `return GoApiSnapshot.EMPTY;`.
   - In `GoApiSnapshot.java:249`:
     ```java
     public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());
     ```
   - `EMPTY.getVer()` returns `GoVer.INVALID` (`major=0, minor=0, patch=0`).
   - `EMPTY.isInvalid()` returns `true` (`GoApiSnapshot.java:503-505`: `return arches.isEmpty();`).
6. **Consumer structure registration failure**:
   - In `GoRttiMapper.java:178-181`: `apiSnapshot.getVer().isInvalid()` is `true`, so `Msg.info` ("Using Go API snapshot...") is skipped.
   - Line 187: `new GoRttiMapper(..., apiSnapshot)` is instantiated.
   - Line 346: `this.goTypes = new GoTypeManager(this, apiSnapshot);`.
   - Line 348: calls `initStructMappings()`.
   - Lines 352-366:
     ```java
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
         throw new IOException(
             "Invalid Go bootstrap struct mapping info: %s".formatted(goVer), e);
     }
     ```
   - `registerStructures` attempts to resolve required Go structures (`runtime.moduledata`, `runtime.type`, etc.).
   - `GoRttiMapper.getType` delegates to `GoTypeManager.findDataType` $\rightarrow$ `findTypeRec`, which queries `apiSnapshot.getTypeDef(typeName)` (`GoTypeManager.java:448-449`).
   - Because `apiSnapshot` is empty, type resolution fails, throwing `IOException`.
   - Caught at line 355; `apiSnapshot.isInvalid()` is `true` (line 356).
   - Throws `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")` (lines 358-360).
7. **Analyzer consumer abort**:
   - In `GoRttiMapper.getSharedGoBinary` (`GoRttiMapper.java:114-117`):
     ```java
     catch (BootstrapInfoException mbie) {
         Msg.warn(GoRttiMapper.class, mbie.getMessage());
         logAnalyzerMsg(program, mbie.getMessage());
     }
     ```
   - Catches `BootstrapInfoException`, logs a warning, appends message to `AutoAnalysisManager.getMessageLog()`, and returns `null`.
   - In `GolangSymbolAnalyzer.added` (`GolangSymbolAnalyzer.java:133-137`):
     ```java
     goBinary = GoRttiMapper.getSharedGoBinary(program, monitor);
     if (goBinary == null) {
         Msg.error(this, "Go symbol analyzer error: unable to get GoRttiMapper");
         return false;
     }
     ```
   - The analyzer logs error and returns `false`.

---

## 4. Calibration, limits, and non-claims

1. **Observed vs Inferred**:
   - *Observed (Code facts)*:
     - `baseVer = goVer.withPatch(0)` in `GoApiSnapshot.java:122`.
     - `GoVer.toString()` emits 3 segments when `patch != -1` (`GoVer.java:155-157`).
     - `"typeinfo/golang/%sgo%s.json%s"` path formatting in `GoApiSnapshot.java:170-171`.
     - `Application.getModuleDataFile` prepending `DATA_DIRNAME = "data/"` and throwing `FileNotFoundException` in `Application.java:362-366`.
     - `jsonFile == null` returning `null` before patch diffs in `GoApiSnapshot.java:124-126`.
     - `apiSnapshot.isInvalid()` throwing `BootstrapInfoException` in `GoRttiMapper.java:356-360`.
     - Installed host filesystem holds 11 base snapshots (`go1.15.0.json` through `go1.25.0.json`) and no `go1.26.0.json`.
   - *Inferred (Control flow)*:
     - When base JSON is absent, `patchverdiffs` directory is never consulted.
     - `getApiFile` is dead code with respect to runtime snapshot loading.
   - *Unknown / Unobserved*:
     - Whether any third-party Ghidra extensions or standalone tools call `getApiFile`.
2. **Historical target causality limit**:
   - The source chain proves that Ghidra 12.1.4 fails to initialize Go RTTI on Go 1.26 binaries due to missing `go1.26.0.json`.
   - This finding **does NOT assert or prove** that the historical round 4 failure on `1password-cli 2.40.0-2` was caused solely by missing base snapshot metadata. The transient analysis log from that execution was not preserved, and layout/moduledata incompatibilities were not re-tested.
3. **No gate / test execution**:
   - This seat performed read-only static analysis and non-verdict filesystem inventory. No verification checks, test suites, or gates were executed.

---

## 5. Proposed L1 verification checks

L1 may verify the concrete source findings and line anchors using the following non-mutating commands:

1. **Verify base version normalization and string formatting**:
   ```sh
   python3 -c "
   import zipfile
   with zipfile.ZipFile('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip') as z:
       lines = z.read('ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java').decode('utf-8').splitlines()
       print(lines[121]) # GoVer baseVer = goVer.withPatch(0);
       print(lines[122]) # File jsonFile = getApiSnapshotFile(baseVer, \"\", \"\");
       print(lines[123]) # if (jsonFile == null) {
       print(lines[124]) #     return null;
       print(lines[125]) # }
   "
   ```
2. **Verify resource formatting path in `GoApiSnapshot`**:
   ```sh
   python3 -c "
   import zipfile
   with zipfile.ZipFile('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip') as z:
       lines = z.read('ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java').decode('utf-8').splitlines()
       for i in range(167, 178):
           print(f'{i+1}: {lines[i]}')
   "
   ```
3. **Verify `Application.getModuleDataFile` path resolution and exception**:
   ```sh
   python3 -c "
   import zipfile
   with zipfile.ZipFile('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Generic/lib/Generic-src.zip') as z:
       lines = z.read('ghidra/framework/Application.java').decode('utf-8').splitlines()
       print('954:', lines[953])
       print('962:', lines[961])
       print('362:', lines[361])
       print('364-367:', lines[363:367])
   "
   ```
4. **Verify installed base JSON inventory**:
   ```sh
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go*.json | sort -V
   ```
   (Should list exactly 11 files, `go1.15.0.json` through `go1.25.0.json`, with none for `go1.26.0.json`).
