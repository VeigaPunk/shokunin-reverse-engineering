# ArchLookup — S003 GoApiSnapshot OS/architecture applicability selection and empty-arches analysis

- Author: `KaidokuR15.ArchLookup` (leaf scout; no subagent dispatch; no live binary execution; no verification/build/test runs)
- Target: Trace `GoApiSnapshot` OS/architecture applicability selection; explain present-file empty arches alternative with exact source lines.
- Access date: 2026-10-20
- Axes: **depth** (complete source-anchored trace from buildinfo resolution and archSearchOrder derivation to streaming JSON deserialization and structure-mapping failure) and **calibration** (strict separation of observed code facts, source inferences, and empirical limits; quotes $\le$ 25 whitespace words; no target causality claims)
- Status: Source analysis completed; no gate or test executed; verification checks named for L1.

---

## 1. Sources opened and verified

All archive members are from S003 installed Base source archive:

| Source ID | Absolute path / archive member | SHA-256 / Size | Opened / Access | Notes |
|---|---|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (7,481,132 bytes) | 2026-10-20 | Installed Ghidra 12.1.4 Base source archive (registered in `corpus/SOURCES.md:9`) |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` | 534 lines | 2026-10-20 | Snapshot JSON loader, `archSearchOrder`, `read()`, `isInvalid()`, `getTypeDef()`, `getFuncdef()` |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | 786 lines | 2026-10-20 | Caller of `GoApiSnapshot.get`, `initStructMappings()`, `BootstrapInfoException` generation, `getType()` override |
| S003 member | `ghidra/app/util/bin/format/golang/GoBuildInfo.java` | 545 lines | 2026-10-20 | Resolution of `GOOS` and `GOARCH` from build settings or Ghidra loader/language fallbacks |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java` | 1,154 lines | 2026-10-20 | `findDataType()`, `findTypeRec()`, delegating non-primitive lookups to `apiSnapshot.getTypeDef()` |
| S003 member | `ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java` | 394 lines | 2026-10-20 | Base mapper: `registerStructure()` invoking `getType()` and throwing `IOException` upon missing definitions |
| Host fs data | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` | 11 base JSON files, 89 patch diffs | 2026-10-20 | Pinned installed snapshot JSON files (`go1.15.0.json` through `go1.25.0.json`) |

---

## 2. End-to-end trace: OS and architecture applicability selection

### 2.1 Derivation of `goOS` and `goArch` parameters

In `GoRttiMapper.java:175–177`:
```java
apiSnapshot = GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program),
	buildInfo.getGOOS(program), monitor);
```

The string values for `goOS` and `goArch` originate from `GoBuildInfo`:

1. **`GOOS` resolution (`GoBuildInfo.java:284–307`)**:
   - Primary: `getBuildSetting("GOOS")` queries compiled-in build settings from the `.go.buildinfo` section (`GoBuildInfo.java:285`).
   - Fallback (`getProgramGOOS(Program)`, `:294–307`): if build settings lack `"GOOS"`, Ghidra maps the executable format:
     - `ElfLoader.ELF_NAME` $\to$ `"linux"`
     - `PeLoader.PE_NAME` $\to$ `"windows"`
     - `MachoLoader.MACH_O_NAME` $\to$ `"darwin"`
     - Otherwise $\to$ `"unknown"`

2. **`GOARCH` resolution (`GoBuildInfo.java:314–335`)**:
   - Primary: `getBuildSetting("GOARCH")` queries compiled-in build settings (`GoBuildInfo.java:315`).
   - Fallback (`getProgramGOARCH(Program)`, `:324–335`): if build settings lack `"GOARCH"`, Ghidra queries the Program's language ID and pointer size, looking up `GHIDRA_GOARCH_MAP` (`GoBuildInfo.java:57–64`):
     - `"aarch64_64"` $\to$ `"arm64"`
     - `"arm_32"` $\to$ `"arm"`
     - `"mips_64"` $\to$ `"mips64"`
     - `"mips_32"` $\to$ `"mips"`
     - `"x86_64"` $\to$ `"amd64"`
     - `"x86_32"` $\to$ `"386"`
     - Unmapped architectures default to `"unknown"`
     - Dual-endian architectures (`"mips"`, `"mips64"`, `"ppc64"`, `:66`) on little-endian targets append `"le"` (`:332–333`).

### 2.2 Applicability search order construction

In `GoApiSnapshot.java:108–111`:
```java
List<String> archSearchOrder = List.of(goOS + "-" + goArch, goOS,
	IS_GOOS_UNIX.contains(goOS) ? "unix" : "", goArch, "all");

return GoApiSnapshot.read(is, archSearchOrder, goVer);
```

Applicability selection enforces a strict 5-tier hierarchical search list:

| Priority | Key selector | Example (`linux`, `amd64`) | Purpose and semantics |
|:---:|---|---|---|
| 1 | `goOS + "-" + goArch` | `"linux-amd64"` | Exact OS and architecture pairing |
| 2 | `goOS` | `"linux"` | OS-specific definitions common to all architectures of that OS |
| 3 | `IS_GOOS_UNIX.contains(goOS) ? "unix" : ""` | `"unix"` | Artificial pseudo-arch grouping POSIX/UNIX-like operating systems |
| 4 | `goArch` | `"amd64"` | Architecture-specific definitions common across operating systems |
| 5 | `"all"` | `"all"` | Platform-independent definitions generically compatible with all targets |

**The UNIX pseudo-arch filter (`GoApiSnapshot.java:173–174`)**:
`IS_GOOS_UNIX` is a static immutable `Set<String>`:
```java
private static final Set<String> IS_GOOS_UNIX = Set.of("aix", "android", "darwin", "dragonfly",
	"freebsd", "hurd", "illumos", "ios", "linux", "netbsd", "openbsd", "solaris");
```
When `goOS` is not in this set (e.g. `"windows"` or `"unknown"`), priority slot 3 evaluates to the empty string `""`.

### 2.3 Streaming JSON deserialization and key retention

In `GoApiSnapshot.java:205–244`:
1. `archNamesToKeep = new HashSet<>(archNames)` (`:212`).
2. Streaming parser reads top-level JSON keys via Gson `JsonReader` (`:214–227`):
   - For each section name `archName`:
     - If `!archNamesToKeep.contains(archName)`: `reader.skipValue()` skips the entire JSON object without parsing (`:218–221`).
     - If `archNamesToKeep.contains(archName)`: `gson.fromJson(reader, GoArch.class)` deserializes `Funcs` and `Types` maps (`:222–224`).
3. Priority-ordered output assembly (`:230–240`):
   In `GoApiSnapshot.java:230–235`:
   ```java
   Map<String, GoArch> results = new LinkedHashMap<>();
   for (String archName : archNames) {
   	if (archName == null || archName.isEmpty()) {
   		continue;
   	}
   ```
   and `GoApiSnapshot.java:236–242`:
   ```java
   	GoArch arch = arches.get(archName);
   	if (arch != null) {
   		results.put(archName, arch);
   	}
   }
   return new GoApiSnapshot(ver, results);
   ```
   - Empty string entries (such as the non-UNIX slot 3 `""`) are explicitly skipped (`:232–234`).
   - Matching sections are placed into a `LinkedHashMap`, preserving the search priority order.

### 2.4 Hierarchical lookup resolution

During analysis, `getTypeDef` and `getFuncdef` query the retained tiers in iteration order (`GoApiSnapshot.java:519–525`):
```java
for (GoArch arch : arches.values()) {
	GoTypeDef typeDef = arch.Types.get(typeName);
	if (typeDef != null) {
		return typeDef;
	}
}
```
Because `arches` is a `LinkedHashMap`, iteration proceeds from most specific to least specific:
`goOS-goArch` $\to$ `goOS` $\to$ `"unix"` $\to$ `goArch` $\to$ `"all"`.
The first non-null match shadows all definitions in broader scopes.

---

## 3. The present-file empty arches alternative

### 3.1 The definition of `isInvalid()`

In `GoApiSnapshot.java:503–505`:
```java
public boolean isInvalid() {
	return arches.isEmpty();
}
```
`GoApiSnapshot.isInvalid()` tests only whether the retained `arches` map is empty. It does **not** test whether the file was present on disk or whether JSON parsing succeeded.

### 3.2 Two distinct pathways to `apiSnapshot.isInvalid() == true`

There are two mutually exclusive causes that result in `apiSnapshot.isInvalid() == true`:

| Feature | Pathway A: Missing base JSON file | Pathway B: Present file, empty arches |
|---|---|---|
| **Underlying condition** | `getApiSnapshotJsonFile(goVer, monitor)` returns `null` because no base JSON exists on disk | Base JSON exists on disk (`bp != null`), parses cleanly, but contains none of the requested arch keys |
| **Source line** | `GoApiSnapshot.java:115` | `GoApiSnapshot.java:242` |
| **Constructed snapshot** | `GoApiSnapshot.EMPTY` (`ver = GoVer.INVALID`, `arches = Map.of()`) | `new GoApiSnapshot(goVer, results)` where `results.isEmpty() == true` |
| **`apiSnapshot.getVer()`** | `GoVer.INVALID` | Valid target `goVer` (e.g. `1.21.0`) |
| **`!apiSnapshot.getVer().isInvalid()`** | `false` | `true` |
| **Advisory info log (`GoRttiMapper.java:178–181`)** | **Omitted** (no log message emitted) | **Emitted**: `Using Go API snapshot for version <goVer>` |
| **`apiSnapshot.isInvalid()`** | `true` (`arches.isEmpty()`) | `true` (`arches.isEmpty()`) |
| **Downstream result** | Fatal `BootstrapInfoException` at structure registration | Fatal `BootstrapInfoException` at structure registration |

### 3.3 The exact mechanism of the present-file empty arches alternative

1. **How empty arches occurs with a present file**:
   - A valid JSON snapshot file (e.g. `go1.21.0.json`) exists in `typeinfo/golang/`.
   - The file is successfully opened and parsed by `GoApiSnapshot.read(is, archSearchOrder, goVer)`.
   - However, none of the keys in `archSearchOrder` (`[goOS-goArch, goOS, unix, goArch, all]`) match any top-level key in the JSON file.
   - For example:
     - A binary for an unrepresented or unusual target where `getProgramGOOS` and `getProgramGOARCH` fall back to `"unknown"`, and the snapshot JSON either lacks `"all"` or has stripped architecture blocks.
     - A custom or vendor-modified snapshot JSON containing only selected targets (e.g. only Windows keys in an environment analyzing an ELF binary).
     - Any scenario where the intersection between `archNamesToKeep` and the file's JSON keys is $\emptyset$.
   - In `read()` (`:230–240`), `results` receives zero entries and remains empty.
   - `read()` returns `new GoApiSnapshot(ver, results)` with `results.isEmpty() == true`.

2. **The deceptive info log**:
   - In `GoRttiMapper.java:178–181`:
     ```java
     if (!apiSnapshot.getVer().isInvalid()) {
     	Msg.info(GoRttiMapper.class,
     		"Using Go API snapshot for version %s".formatted(apiSnapshot.getVer()));
     }
     ```
   - Because `apiSnapshot.getVer()` holds the valid `goVer` from `read()`, `!apiSnapshot.getVer().isInvalid()` is `true`.
   - Ghidra logs `Using Go API snapshot for version <goVer>`, creating the misleading appearance that snapshot lookup succeeded completely.

3. **Fatal structure-mapping failure**:
   - Execution proceeds to `GoRttiMapper.initStructMappings()` (`GoRttiMapper.java:353–365`):
     At `GoRttiMapper.java:353–354`:
     ```java
     try {
     	registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);
     }
     ```
     and in the catch handler at `GoRttiMapper.java:356–357`:
     ```java
     if (apiSnapshot.isInvalid()) {
     	// a normal'ish situation where we don't have type info for this arch/binary
     ```
     throwing at `GoRttiMapper.java:358–360`:
     ```java
     	throw new BootstrapInfoException(
     		"Missing Go bootstrap type info, unable to extract Go RTTI info."
     				.formatted(goVer));
     }
     ```
   - During `registerStructures`:
     - `DataTypeMapper.registerStructure` calls `getType(structNames, Structure.class)` (`DataTypeMapper.java:169`).
     - `GoRttiMapper.getType` delegates to `goTypes.findDataType(name)` (`GoRttiMapper.java:380–382`).
     - `GoTypeManager.findTypeRec` queries `apiSnapshot.getTypeDef(typeName)` (`GoTypeManager.java:448–450`).
     - Because `arches.isEmpty() == true`, `getTypeDef` returns `null` for all types.
     - `DataTypeMapper.registerStructure` throws `IOException("Missing struct definition for class %s, structure name: [%s]")` (`DataTypeMapper.java:173–175`).
   - The catch block in `initStructMappings` checks `if (apiSnapshot.isInvalid())` (`GoRttiMapper.java:356`).
   - Because `apiSnapshot.isInvalid()` checks `arches.isEmpty()`, it evaluates to `true`.
   - The method executes the comment-annotated branch:
     `// a normal'ish situation where we don't have type info for this arch/binary`
     and throws `throw new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`.
   - `GoRttiMapper.getSharedGoBinary` catches `BootstrapInfoException`, logs a warning, and returns `null` (`GoRttiMapper.java:114–125`).
   - Downstream analyzers (`GolangSymbolAnalyzer.java:133–137`, `GolangStringAnalyzer.java:103–107`) receive `null` and abort.

---

## 4. Grounded findings summary

- **OBSERVATION — 5-tier priority hierarchy**: `GoApiSnapshot.java:108–111` strictly constructs search order: `goOS-goArch`, `goOS`, `unix` (if POSIX), `goArch`, `"all"`.
- **OBSERVATION — selective streaming parsing**: `GoApiSnapshot.java:214–228` uses `JsonReader.skipValue()` to bypass unneeded architecture keys without allocating memory.
- **OBSERVATION — priority preservation via LinkedHashMap**: `GoApiSnapshot.java:230–240` iterates through `archNames` and populates `results` in priority order, skipping empty strings.
- **OBSERVATION — resolution order**: `GoApiSnapshot.java:510–526` queries `arches.values()`, ensuring specific OS/arch records shadow generic `"all"` records.
- **OBSERVATION — definition of `isInvalid()`**: `GoApiSnapshot.java:503–505` defines `isInvalid()` strictly as `arches.isEmpty()`.
- **OBSERVATION — developer intent in source comments**: `GoRttiMapper.java:357` explicitly annotates this outcome as: `// a normal'ish situation where we don't have type info for this arch/binary`.
- **INFERENCE FROM SOURCE — observable discrepancy**: A present file with empty arches will log `Using Go API snapshot for version <goVer>` at `GoRttiMapper.java:178–181`, whereas a missing file logs nothing at that line. Both fail with identical `BootstrapInfoException` at `:358–360`.
- **INFERENCE FROM SOURCE — failure equivalence**: From the perspective of `registerStructures` and `initStructMappings`, a missing snapshot file and a snapshot file with empty applicable arches are functionally equivalent. Both produce an empty `arches` map, return `null` from `getTypeDef()`, and trigger `BootstrapInfoException`.

---

## 5. Calibration and empirical limits

1. **Source companion vs compiled bytecode**:
   - Analysis is performed on S003 `Base-src.zip`. The source archive reflects the source tree companion of Ghidra 12.1.4, not decompiled or executed jar classes.
2. **Installed baseline snapshot contents**:
   - All 11 installed base JSON files (`go1.15.0.json` through `go1.25.0.json`) in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` contain an `"all"` key populated with thousands of definitions.
   - Therefore, for standard installed versions $\le 1.25$, standard supported architectures will not trigger empty arches under default installation files unless custom, stripped, or platform-restricted snapshots are supplied, or target mapping fails.
3. **No claim of historical target causality**:
   - This analysis proves the existence and exact mechanism of the present-file empty arches pathway in Ghidra's source code.
   - It does **not** assert that the historical 1password-cli analysis failure was caused by empty arches rather than missing base JSON or layout incompatibility, as the original execution log was not retained.
4. **No execution performed**:
   - In accordance with leaf scout bounds, no live target execution, provider execution, build, or test was run by this seat.

---

## 6. Proposed L1 verification checks

The following read-only checks are proposed for L1 canonical integration:

1. **S003 archive and digest verification**:
   ```sh
   sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
   ```
   Confirm matches `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`.

2. **Source line anchor verification in S003**:
   Inspect zip entry `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`:
   - Lines 108–111: `archSearchOrder` declaration and `GoApiSnapshot.read` call.
   - Lines 173–174: `IS_GOOS_UNIX` set definition.
   - Lines 218–227: `reader.skipValue()` and `gson.fromJson`.
   - Lines 230–240: `LinkedHashMap` priority population.
   - Lines 503–505: `isInvalid()` returning `arches.isEmpty()`.
   - Lines 519–526: `getTypeDef()` iterating `arches.values()`.

3. **Structure-mapping error path verification in S003**:
   Inspect zip entry `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java`:
   - Lines 175–181: `GoApiSnapshot.get()` and `!apiSnapshot.getVer().isInvalid()` log check.
   - Lines 353–365: `initStructMappings()`, `apiSnapshot.isInvalid()` check, and comment at line 357.
   - Lines 380–394: `getType()` override delegating to `goTypes.findDataType()`.

4. **Quote word-count verification**:
   Confirm that all verbatim code quotes in this report are $\le 25$ whitespace-delimited words.
