# Round 15 w1 — InstalledLayout: Installed Go typeinfo directory, filename layout, 1.25/1.26 resources, and revision ambiguity

- **Seat**: `KaidokuR15.InstalledLayout` (leaf scout; read-only inspection; no subagent dispatch)
- **Role**: UFO-FSD scout
- **Target**: Discover actual installed Go typeinfo directory and filename layout only; list selected 1.25/1.26 resources and locate any installation/revision ambiguity. No scripts/tests.
- **Axes**: **depth** (concrete byte-level filesystem and archive observations, exact SHA-256 digests, and source code anchors) and **calibration** (strict separation of observed filesystem facts from source control-flow inferences; explicit limits on historical proof)
- **Repository**: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Access date**: 2026-10-20
- **Verification run by this seat**: None (per contract, leaf seats never run build, test, lint, or gate checks; proposed checks are named for L1 verification)
- **Tooling installs/updates**: None (used Python stdlib via session `eval` and standard shell reading tools; no packages installed or upgraded)

---

## 1. Installed Go typeinfo directory and file layout census

### 1.1 Directory hierarchy and module path
The installed Ghidra distribution is located at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`. Go type information is housed under the Base feature data path:

```text
/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/
├── generic/
│   ├── generic_clib.gdt (18,485 bytes)
│   └── generic_clib_64.gdt (18,485 bytes)
├── golang/                                      <-- Target Go typeinfo directory
│   ├── go1.15.0.json ... go1.25.0.json         <-- 11 base JSON snapshots
│   ├── golang_1.15_anybit_any.gdt ... .gdt      <-- 9 legacy GDT archives (1.15–1.23)
│   └── patchverdiffs/                           <-- 123 patch diff files
├── mac_10.9/
│   └── mac_osx.gdt (21,557 bytes)
├── rust/
│   └── rust-common.gdt (10,307 bytes)
└── win32/
    ├── windows_vs12_32.gdt (34,869 bytes)
    ├── windows_vs12_64.gdt (34,869 bytes)
    └── msvcrt/ (4 text files: clsids, guids, iids, syntaxes)
```

### 1.2 Direct entries in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`
The directory contains exactly **21 entries**: **20 regular files** and **1 subdirectory** (`patchverdiffs/`). There are no symlinks, hidden files, or unreadable entries.

#### 11 Base JSON snapshots
All base snapshot filenames follow the exact pattern `go<major>.<minor>.0.json`. There are no `.1`, `.2`, or unversioned patch base files. All 11 files share the distribution modification timestamp `2026-09-21 19:37:26 UTC`.

| Filename | Exact byte size | SHA-256 digest |
|---|---:|---|
| `go1.15.0.json` | 4,267,141 | `cd070f2165716fd63643c722e50722295367fb7d36ff7a153d56178877da5b10` |
| `go1.16.0.json` | 4,671,548 | `d668acd92c30102dc85243c4ef580d5294e6c6f494d16f45a95c42959de00dee` |
| `go1.17.0.json` | 6,100,205 | `fb1f31849c303642739cfe907f810e1606eb1b34ddee41486b359bd9df28d549` |
| `go1.18.0.json` | 6,325,742 | `86a0687c9ce129bf9cf94faa20bee250fc13a298935d3b0ca3e0dee68ef91f67` |
| `go1.19.0.json` | 6,469,362 | `79c93ea499226c79e234053ea886779a26d3be363e437b102c046d8b6bb98885` |
| `go1.20.0.json` | 8,875,175 | `6def34993dd352b01f749dc44935178bdf2dbd13f585adf631798919ad6d0a32` |
| `go1.21.0.json` | 9,039,469 | `7bfe8f9a0f316ba3e6258152e35181c1d1c5c6b0bb0e6e9e95355490bb447b31` |
| `go1.22.0.json` | 9,203,666 | `c8feb28695499d1631af5ae441c8fd39c7eb75ce54dc8472673f2693e6974640` |
| `go1.23.0.json` | 9,368,866 | `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692` |
| `go1.24.0.json` | 10,039,962 | `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571` |
| `go1.25.0.json` | 10,081,618 | `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` |

#### 9 Legacy GDT type archives
Follow the pattern `golang_<major>.<minor>_anybit_any.gdt`. They exist only for Go 1.15 through 1.23. There are **no GDT files for Go 1.24 or Go 1.25**.

| Filename | Exact byte size | SHA-256 digest |
|---|---:|---|
| `golang_1.15_anybit_any.gdt` | 10,654 | `8d00d7804eb32cfa204c8895c042b6f2670e2b898cdcd21adc2971552dc1b95b` |
| `golang_1.16_anybit_any.gdt` | 11,043 | `e1004ee298129f3ab2604373e8f001e8c5e9692a45a07af665a46efb2284a603` |
| `golang_1.17_anybit_any.gdt` | 10,983 | `0e65de82ea6cef692bd21778c616b3658d5f42b841eefb2e6143bd9cf6c9c667` |
| `golang_1.18_anybit_any.gdt` | 11,067 | `b6d598e8660187976669f3e07b0a52d24b909efec1f7c2bd23ac33e7040a60ad` |
| `golang_1.19_anybit_any.gdt` | 11,066 | `3b57b171b9d91b131c33d7d3e92f77f420671b7906b61d6966b5746bb6a9ee5b` |
| `golang_1.20_anybit_any.gdt` | 11,162 | `668c026d03a4f026ededa0d15816c48af2b23491834e5579a13e4debf9b399e1` |
| `golang_1.21_anybit_any.gdt` | 11,834 | `637edc46c85e61bd0b27b0c582bdc7e3a6c6e74ceb7a7f0c2134cae58e5c4251` |
| `golang_1.22_anybit_any.gdt` | 11,817 | `38d5c1c7586f860b1311447502447f9548226dce580519b22c57323c2d4f6b7c` |
| `golang_1.23_anybit_any.gdt` | 11,650 | `9de4f96727c96c2f4a7c85211a7cb35db2838e2621fd6754d314cf0d2bfdac1a` |

### 1.3 Patch diff layout in `patchverdiffs/`
The subdirectory `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/` contains exactly **123 files** (all regular non-symlink files, 0 subdirectories).

- Every filename strictly matches `go<major>.<minor>.<patch>.json.diff` where `<patch> >= 1`.
- There are no `.0.json.diff` files.
- Each diff file is structured as native `jd` diff sections starting with `@ ["<container>", ...]` followed by `-` and `+` lines. Each diff is relative to its minor's base `go<major>.<minor>.0.json` (applied directly via `JsonPatchApplier(jsonFile)`), not chained cumulatively.
- **Breakdown by minor version**:
  - **Go 1.15**: 15 diffs (`go1.15.1.json.diff` through `go1.15.15.json.diff`)
  - **Go 1.16**: 15 diffs (`go1.16.1.json.diff` through `go1.16.15.json.diff`)
  - **Go 1.17**: 13 diffs (`go1.17.1.json.diff` through `go1.17.13.json.diff`)
  - **Go 1.18**: 10 diffs (`go1.18.1.json.diff` through `go1.18.10.json.diff`)
  - **Go 1.19**: 13 diffs (`go1.19.1.json.diff` through `go1.19.13.json.diff`)
  - **Go 1.20**: 14 diffs (`go1.20.1.json.diff` through `go1.20.14.json.diff`)
  - **Go 1.21**: 13 diffs (`go1.21.1.json.diff` through `go1.21.13.json.diff`)
  - **Go 1.22**: 12 diffs (`go1.22.1.json.diff` through `go1.22.12.json.diff`)
  - **Go 1.23**: 12 diffs (`go1.23.1.json.diff` through `go1.23.12.json.diff`)
  - **Go 1.24**: 6 diffs (`go1.24.1.json.diff` through `go1.24.6.json.diff`)
  - **Go 1.25**: **0 diffs** (no `go1.25.*.json.diff` files exist)
  - **Go 1.26**: **0 diffs** (no `go1.26.*.json.diff` files exist)
  - **Total**: $15 + 15 + 13 + 10 + 13 + 14 + 13 + 12 + 12 + 6 = 123$ diff files.

---

## 2. Selected Go 1.25 and 1.26 resources

### 2.1 Go 1.25 Resource Inventory and Runtime Resolution

- **Base Snapshot File**:
  - Path: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json`
  - Status: **PRESENT** (regular file)
  - Size: 10,081,618 bytes
  - SHA-256: `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`
  - Internal JSON structure: Top-level object containing **27 platform container keys**:
    `['386', 'all', 'amd64', 'arm', 'arm64', 'cgo', 'darwin', 'darwin-amd64', 'darwin-amd64-cgo', 'darwin-arm64', 'darwin-arm64-cgo', 'linux', 'linux-386', 'linux-386-cgo', 'linux-amd64', 'linux-amd64-cgo', 'linux-arm', 'linux-arm-cgo', 'linux-arm64', 'linux-arm64-cgo', 'linux-cgo', 'unix', 'windows', 'windows-386', 'windows-386-cgo', 'windows-amd64', 'windows-amd64-cgo']`.
    Each container defines two subdictionaries: `Funcs` and `Types`.
  - Bootstrap types: Mandatory structures `runtime.moduledata` and `runtime.pcHeader` are defined within the container `Types` maps.
- **Patch Diffs**:
  - Count: **0** files.
  - Status: **ABSENT**. There are no `go1.25.1.json.diff` or higher patch diff files.
- **Legacy GDT Archive**:
  - Status: **ABSENT** (`golang_1.25_anybit_any.gdt` does not exist).
- **Runtime Resolution Behavior (from S003 source)**:
  - **Go 1.25.0 binary**:
    - `GoRttiMapper.java:79`: `SUPPORTED_VERSIONS` (`1.15-1.25`) includes 1.25.0; no range error logged.
    - `GoApiSnapshot.java:122-131`: `baseVer` resolves to `1.25.0`, `jsonFile` resolves to `go1.25.0.json`. `patchDiffFile` is null because patch is 0. Unpatched base snapshot is read directly.
    - `GoRttiMapper.java:178-180`: logs `Using Go API snapshot for version 1.25.0`.
  - **Go 1.25.x binary (patch $x \ge 1$)**:
    - `GoRttiMapper.java:79`: `contains()` treats wildcard/positive patch in range `1.15-1.25` as valid.
    - `GoApiSnapshot.java:148-166`: `getPatchVerDiffFile` decrements `patchVer` looking for `go1.25.x.json.diff`. Finding none, it reaches patch 0 and exits with `patchDiffFile == null`.
    - `GoApiSnapshot.java:158-161`: logs warning `Msg.warn(GoApiSnapshot.class, "Falling back from 1.25.x to 1.25.0 for Go API snapshot")`.
    - `GoApiSnapshot.java:129-131`: returns raw `go1.25.0.json` bytes.
    - `GoApiSnapshot.java:111`: reads snapshot and stamps it with requested version `1.25.x`.
    - `GoRttiMapper.java:178-180`: logs `Using Go API snapshot for version 1.25.x`.

### 2.2 Go 1.26 Resource Inventory and Runtime Resolution

- **Base Snapshot File**:
  - Expected path: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json`
  - Status: **ABSENT** (file does not exist).
  - Size: null.
  - SHA-256: null.
- **Patch Diffs**:
  - Count: **0** files.
  - Status: **ABSENT**.
- **Legacy GDT Archive**:
  - Status: **ABSENT**.
- **Installation-wide census**:
  - A recursive search of the entire `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` tree across all filenames, file paths, and `.jar` archive entries revealed **zero matches** for string `1.26` or `go1.26` in connection with Golang.
- **Runtime Resolution Behavior (from S003 source)**:
  - **Go 1.26.x binary**:
    - `GoRttiMapper.java:79, 170-172`: `SUPPORTED_VERSIONS` (`1.15-1.25`) does not contain 1.26. Ghidra logs `Msg.error(GoRttiMapper.class, "Untested Go version [1.26]")`. This is an advisory log only; control flow continues to snapshot lookup.
    - `GoApiSnapshot.java:122-126`: `baseVer` resolves to `1.26.0`. `getApiSnapshotFile(1.26.0, "", "")` attempts to locate `typeinfo/golang/go1.26.0.json` via `Application.getModuleDataFile()`, catches `IOException`, and returns `null`.
    - `GoApiSnapshot.java:115`: returns `GoApiSnapshot.EMPTY`.
    - `GoApiSnapshot.java:242, 503-505`: `EMPTY` has `arches = Map.of()`. `isInvalid()` evaluates `arches.isEmpty()`, returning `true`.
    - `GoRttiMapper.java:353-365`: during mapper construction, `initStructMappings()` invokes `registerStructures()`. Because `GoTypeManager.findDataType()` finds no definitions in `EMPTY` (`GoTypeManager.java:449`), `registerStructures` throws an `IOException`.
    - `GoRttiMapper.java:356-360`: catches `IOException`, checks `if (apiSnapshot.isInvalid())`, and throws `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`.
    - `GoRttiMapper.java:95-98, 104`: `getSharedGoBinary()` catches `BootstrapInfoException`, logs a warning, appends to the UI analyzer message log, and returns `null`.
    - `GolangSymbolAnalyzer.java:133-137`: receives `null` and returns `false`, causing symbol recovery to halt completely.

---

## 3. Identification of installation and revision ambiguities

Four concrete ambiguities were uncovered through direct inspection of the installed filesystem, compiled bytecode, and source companion:

### Ambiguity A: Upstream Commit vs Installed Build Date (Trunk vs Maintenance Branch Divergence)
- **Observed fact**: Upstream commit GP-6528 (`385e8cd923d09f10b1a7874108e71748875fa174`, S004) titled *"GP-6528 add support for golang 1.26"* was committed to GitHub master on **2026-03-03**.
- **Observed fact**: The installed Ghidra 12.1.4 was built on **2026-09-21 16:13 UTC** (`application.properties:2`, commit hash `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`).
- **Ambiguity**: An analyst examining commit dates might assume an installation built in September 2026 contains a commit from March 2026. However, Ghidra 12.1.4 is a maintenance patch release on the 12.1 release branch. Upstream master feature additions (such as GP-6528, which bumped the version range and introduced `go1.26.0.json`) were slated for a future minor/major release (e.g. Ghidra 12.2) and were **not backported** to the 12.1.x maintenance branch.
- **Proof**: `docs/ChangeHistory.md` lines 1–22 record only point-release fixes for 12.1.4 (e.g. GP-7238, GP-7171, GP-7190, GP-7267), with no mention of GP-6528 or Go 1.26. Bytecode inspection of `Base.jar:ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.class` confirmed the literal string `1.15-1.25`, proving the installed binary matches the S003 companion source (`1.15-1.25`) and not S004 (`1.15-1.26`).

### Ambiguity B: Filename Construction Discrepancy in Source (`getApiSnapshotFile` vs `getApiFile`)
- **Observed fact**: In `GoApiSnapshot.java`, there are two separate methods constructing JSON filenames:
  1. `getApiSnapshotFile(GoVer goVer, String subdir, String suffix)` (lines 161–170):
     `Application.getModuleDataFile("typeinfo/golang/%sgo%s.json%s".formatted(subdir, goVer.toString(), suffix))`
     Because `GoVer.toString()` (`GoVer.java:155-158`) outputs `"%d.%d.%d"` when patch is non-negative, and `baseVer = goVer.withPatch(0)` forces patch to 0, this method queries `go<major>.<minor>.0.json`.
  2. `getApiFile(File baseDir, GoVer ver)` (lines 175–183):
     Attempts `go%d.%d.%d.json`. If not found and `patch == 0`, it falls back to `go%d.%d.json` (two-part filename, e.g. `go1.25.json`).
- **Ambiguity**: An analyst inspecting `getApiFile` might conclude that `go1.25.json` or `go1.26.json` is a supported layout convention.
- **Resolution**: `getApiFile` is an uncalled utility helper. The active runtime loader (`getApiSnapshotJsonFile` and `getPatchVerDiffFile`) exclusively invokes `getApiSnapshotFile`, which strictly requires the three-part format `go<major>.<minor>.0.json`. In the actual filesystem, 100% of the 11 base files use `go1.X.0.json`; no `go1.X.json` files exist.

### Ambiguity C: Coexistence of Deprecated GDT Archives and JSON Snapshots
- **Observed fact**: For Go 1.15 through 1.23, `.gdt` binary type archives coexist in `Ghidra/Features/Base/data/typeinfo/golang/` alongside `.json` snapshots. For Go 1.24 and 1.25, `.gdt` files are completely absent.
- **Ambiguity**: External tooling or documentation might assume that Go RTTI type resolution relies on Ghidra Data Type (`.gdt`) archives.
- **Resolution**: S007 (`ChangeHistory.md:585`) explicitly states: *"Added support for Golang 1.24 and 1.25. Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files. (GP-5470)"*. S003 `GoRttiMapper.java:331` demonstrates that `GoRttiMapper` calls `super(program, null)`, passing `null` for the GDT archive. The `.gdt` files are obsolete legacy artifacts retained from pre-12.0 releases and are never loaded by the 12.1.4 Go RTTI mapper.

### Ambiguity D: Intra-Minor Patch Diff Coverage Gaps vs Prior Report Discrepancy
- **Observed fact**: In the round 14 advisory report (`.ufo/waves/round-14/w1/SnapshotBootstrap.md:26`), the file census noted *"11 base JSONs, 89 diffs"*.
- **Ambiguity**: This created confusion over whether the installation had 89 diffs or whether files were missing.
- **Resolution**: Fresh directory enumeration confirms exactly **123 diff files** in `patchverdiffs/`. The discrepancy stems from an incomplete census in the earlier report. Furthermore, patch coverage is asymmetric across recent versions: Go 1.24 contains diffs through `go1.24.6.json.diff`, whereas Go 1.25 has **zero** diffs despite being within `SUPPORTED_VERSIONS`. Consequently, Go 1.25.1+ binaries experience a silent fallback to `go1.25.0.json` with a log warning, whereas Go 1.24.1–1.24.6 receive exact patch diff application.

---

## 4. Limits and non-claims

1. **Presence is not behavioral proof**: The physical presence of `go1.25.0.json` and absence of `go1.26.0.json` are filesystem observations. They do not constitute experimental verification that Ghidra successfully decompiles or recovers symbols from any specific Go 1.25 compiled binary.
2. **No runtime execution**: Neither Ghidra, the headless analyzer, nor any REA binary target was executed to produce these findings. All control-flow assertions are derived strictly from static code reading of S003 companion source and verified against bytecode constants in S003/installed `Base.jar`.
3. **No modification to shared registries or gates**: No modifications were made to `corpus/SOURCES.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, or any code gate.

---

## 5. Proposed L1 verification checks

To verify this report without executing tests or gates during seat work, L1 should execute the following read-only inventory checks:

1. **Verify directory layout and entry counts**:
   ```sh
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang | wc -l
   # Expected output: 21 (20 files + patchverdiffs)
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/*.diff | wc -l
   # Expected output: 123
   ```
2. **Verify Go 1.25 base snapshot presence and SHA-256**:
   ```sh
   sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json
   # Expected: 54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252
   ```
3. **Verify Go 1.26 resource absence**:
   ```sh
   ls /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/*1.26* 2>&1
   # Expected: No such file or directory
   ls /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/*1.26* 2>&1
   # Expected: No such file or directory
   ```
4. **Verify installed Ghidra build properties vs Go range constant in bytecode**:
   ```sh
   grep -E 'application.version|application.build.date|application.revision.ghidra=' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties
   # Expected: 12.1.4, 2026-Sep-21 1613 UTC, 8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc
   python3 -c "import zipfile; z=zipfile.ZipFile('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base.jar'); data=z.read('ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.class'); print('Contains 1.15-1.25:', b'1.15-1.25' in data); print('Contains 1.15-1.26:', b'1.15-1.26' in data)"
   # Expected: Contains 1.15-1.25: True, Contains 1.15-1.26: False
   ```
