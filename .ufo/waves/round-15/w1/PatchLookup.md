# PatchLookup — GoApiSnapshot patch-diff ordering, application logic, and fallback limits (round 15, w1)

- Seat: `KaidokuR15.PatchLookup` (leaf scout; no subagent dispatch; no live binary/provider execution; no test/build/gate runs).
- Target: Trace `GoApiSnapshot` patch-diff ordering/application logic; distinguish exact target patch vs earlier patches; name limits.
- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Destination: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/PatchLookup.md`
- Access date: 2026-10-20
- Axes evaluated:
  - **depth** (C1): complete structural trace of `GoApiSnapshot` patch resolution, loop decrement logic, non-cumulative diff design, and type fidelity across exact vs fallback states.
  - **calibration** (C2): strict separation of observed source facts, derived inferences, and empirical limits; verbatim quotes $\le$ 25 whitespace words; exact line citations; no claims of historical causality or provider execution.

---

## 1. Sources opened and verified

All sources were opened and verified locally this round:

| id | path / archive member | sha256 / identity | access date | notes |
|---|---|---|---|---|
| S001 | `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0` | 2026-10-20 | Installed REA skill |
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (7,481,132 bytes) | 2026-10-20 | Installed Ghidra 12.1.4 Base source archive |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` | 534 lines | 2026-10-20 | Primary snapshot loader, patch fallback loop, and provider creation |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/JsonPatch.java` | 215 lines | 2026-10-20 | Joseph Burnett `jd` diff parser and section representation |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/JsonPatchApplier.java` | 152 lines | 2026-10-20 | Single-pass JSON diff applier against base JSON |
| S003 member | `ghidra/app/util/bin/format/golang/GoVer.java` | 161 lines | 2026-10-20 | Version record: `prevPatch()`, `withPatch(0)`, `compareTo()` |
| S003 member | `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` | 786 lines | 2026-10-20 | Caller of `GoApiSnapshot.get()`, structure registration and error logging |
| S007 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` | `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` | 2026-10-20 | Line 585 confirms migration from `.gdt` to JSON snapshots |
| Host fs | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` | 11 base JSONs, 123 patch diffs, 9 `.gdt` files | 2026-10-20 | Installed snapshot assets in Ghidra 12.1.4 distribution |

---

## 2. Installed snapshot census

An inventory of `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` reveals the exact distribution of base JSON snapshots and patch diffs in Ghidra 12.1.4:

| Go minor version | Base file (`go1.<minor>.0.json`) | Base size (bytes) | Patch diff count (`patchverdiffs/`) | Patch diff range |
|---|---|---|---|---|
| Go 1.15 | present | 4,267,141 | 15 | `go1.15.1.json.diff` – `go1.15.15.json.diff` |
| Go 1.16 | present | 4,671,548 | 15 | `go1.16.1.json.diff` – `go1.16.15.json.diff` |
| Go 1.17 | present | 6,100,205 | 13 | `go1.17.1.json.diff` – `go1.17.13.json.diff` |
| Go 1.18 | present | 6,325,742 | 10 | `go1.18.1.json.diff` – `go1.18.10.json.diff` |
| Go 1.19 | present | 6,469,362 | 13 | `go1.19.1.json.diff` – `go1.19.13.json.diff` |
| Go 1.20 | present | 8,875,175 | 14 | `go1.20.1.json.diff` – `go1.20.14.json.diff` |
| Go 1.21 | present | 9,039,469 | 13 | `go1.21.1.json.diff` – `go1.21.13.json.diff` |
| Go 1.22 | present | 9,203,666 | 12 | `go1.22.1.json.diff` – `go1.22.12.json.diff` |
| Go 1.23 | present | 9,368,866 | 12 | `go1.23.1.json.diff` – `go1.23.12.json.diff` |
| Go 1.24 | present | 10,039,962 | 6 | `go1.24.1.json.diff` – `go1.24.6.json.diff` |
| Go 1.25 | present | 10,081,618 | **0** | **none** (only base `go1.25.0.json` exists) |
| Go 1.26+ | **absent** | — | **0** | **none** (no base, no diffs) |
| **Total** | **11 base files** | — | **123 diff files** | **134 total JSON snapshot files** |

---

## 3. End-to-end trace of patch-diff ordering and application logic

### Step 1: Base version requirement and absence gate
In `GoApiSnapshot.java:118–126`:
```java
public static ByteProvider getApiSnapshotJsonFile(GoVer goVer, TaskMonitor monitor)
        throws IOException, CancelledException {
    FileSystemService fsService = FileSystemService.getInstance();

    GoVer baseVer = goVer.withPatch(0);
    File jsonFile = getApiSnapshotFile(baseVer, "", "");
    if (jsonFile == null) {
        return null;
    }
```
- **OBSERVATION — Base file is mandatory prerequisite**:
  `goVer.withPatch(0)` forces the lookup of `go<major>.<minor>.0.json`.
  If this base file is absent (e.g. for Go 1.26.0 or Go 1.26.2), `jsonFile` is `null`, and `getApiSnapshotJsonFile` immediately returns `null`.
- **OBSERVATION — Zero cross-minor fallback**:
  Patch diffs are **never searched or opened** if the major.minor base file does not exist. Ghidra never attempts to fall back from Go 1.26 to Go 1.25.
- Downstream consequence: Returning `null` causes `GoApiSnapshot.get()` (`GoApiSnapshot.java:115`) to return `GoApiSnapshot.EMPTY`.

### Step 2: Backward patch-decrement search loop in `getPatchVerDiffFile`
In `GoApiSnapshot.java:148–166`:
```java
static File getPatchVerDiffFile(GoVer goVer) {
    // returns the closest patch file that is present, or null if patch-ver-num is already 0
    // or no patch diff files are found for the specified major.minor version.
    GoVer patchVer = goVer;
    File patchDiffFile = null;
    while (patchVer.getPatch() > 0 &&
        (patchDiffFile = getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")) == null) {
        patchVer = patchVer.prevPatch();
    }

    if (patchVer.getPatch() != goVer.getPatch()) {
        Msg.warn(GoApiSnapshot.class,
            "Falling back from %s to %s for Go API snapshot".formatted(goVer, patchVer));
    }
    else {
        Msg.info(GoApiSnapshot.class, "Using Go API snapshot for %s".formatted(goVer));
    }
    return patchDiffFile;
}
```
- **OBSERVATION — Loop mechanics**:
  - The search begins with `patchVer = goVer`.
  - If `patchVer.getPatch() == 0`, the while loop is skipped entirely, and `patchDiffFile` remains `null`.
  - If `patchVer.getPatch() > 0`, it queries `getApiSnapshotFile(patchVer, "patchverdiffs/", ".diff")`, which resolves `typeinfo/golang/patchverdiffs/go<ver>.json.diff` via `Application.getModuleDataFile()`.
  - If that file does not exist, `patchVer = patchVer.prevPatch()` decrements the patch number by 1 (`new GoVer(major, minor, patch > 0 ? patch - 1 : 0)`, `GoVer.java:141`).
  - The loop continues until either:
    1. A diff file is found (`patchDiffFile != null`), terminating at `0 < patchVer <= goVer`; OR
    2. `patchVer.getPatch()` reaches `0`, terminating with `patchDiffFile == null`.
- **OBSERVATION — Branch logging and discrepancy detection**:
  - When `patchVer.getPatch() == goVer.getPatch()`, it logs:
    `Msg.info(GoApiSnapshot.class, "Using Go API snapshot for %s".formatted(goVer));`
  - When `patchVer.getPatch() != goVer.getPatch()`, it logs:
    `Msg.warn(GoApiSnapshot.class, "Falling back from %s to %s for Go API snapshot".formatted(goVer, patchVer));`
  - *Calibrated note*: This warning is emitted even if no patch diff was found and `patchVer` fell back all the way to `0` (e.g. falling back from `1.25.1` to `1.25.0`).

### Step 3: Unpatched base bypass when `patchDiffFile == null`
In `GoApiSnapshot.java:128–131`:
```java
    File patchDiffFile = getPatchVerDiffFile(goVer);
    if (patchDiffFile == null) {
        return fsService.getByteProvider(fsService.getLocalFSRL(jsonFile), false, monitor);
    }
```
- **OBSERVATION — Direct ByteProvider bypass**:
  If `patchDiffFile == null` (which occurs either when the target binary is patch 0, or when no diffs exist for that minor version, such as Go 1.25.1), Ghidra bypasses all patch parsing and returns a direct ByteProvider for the unpatched base `jsonFile`.

### Step 4: Patch application via `JsonPatchApplier`
In `GoApiSnapshot.java:133–145`:
```java
    FSRL fsrl = fsService.getFullyQualifiedFSRL(fsService.getLocalFSRL(jsonFile), monitor);
    ByteProvider bp = fsService.getDerivedByteProviderPush(fsrl, null,
        "go%s.json".formatted(goVer), -1, os -> {
            JsonPatch jsonPatch = JsonPatch.read(patchDiffFile);
            JsonPatchApplier jpa = new JsonPatchApplier(jsonFile);
            monitor.initialize(jsonPatch.getSectionCount(),
                "Patching Go API snapshot %s -> %s".formatted(baseVer, goVer));
            jpa.apply(jsonPatch, monitor);
            OutputStreamWriter osw = new OutputStreamWriter(os, StandardCharsets.UTF_8);
            new Gson().toJson(jpa.getJson(), osw);
            osw.flush(); // don't close outputstream, handled by caller
        }, monitor);
    return bp;
```
- **OBSERVATION — Non-cumulative single-diff design**:
  - `JsonPatchApplier jpa = new JsonPatchApplier(jsonFile);` initializes the applier with the **base JSON file** (`go<major>.<minor>.0.json`), which it parses into an internal `JsonObject rootContainer` (`JsonPatchApplier.java:47–51`).
  - Exactly **one** `patchDiffFile` is read (`JsonPatch.read(patchDiffFile)`) and applied (`jpa.apply(jsonPatch, monitor)`).
  - *Architectural invariant*: In Ghidra's design, diffs are **NOT cumulative chains** ($0 \to 1 \to 2 \dots$). Each diff file `go<major>.<minor>.<patch>.json.diff` is an independent, complete delta from the base `go<major>.<minor>.0.json` directly to `go<major>.<minor>.<patch>.json`.
  - *Diff format*: Native `jd` format (`https://github.com/josephburnett/jd`) (`JsonPatch.java:27–28`), comprising path headers (`@ ["all", "Funcs", ...]`) and line operations (`+` ADD, `-` REMOVE) (`JsonPatch.java:163–214`).
  - *Application semantics*: `JsonPatchApplier.applySection()` navigates the in-memory Gson tree and directly adds/removes object fields or array elements (`JsonPatchApplier.java:75–120`).

---

## 4. Distinguishing exact target patch vs earlier patches

The table below contrasts the exact system behavior across the five possible version scenarios:

| Dimension | Case A: Exact Patch 0 (e.g. `1.21.0`) | Case B: Exact Target Patch (e.g. `1.21.3`) | Case C: Earlier Patch Fallback (e.g. `1.21.14` $\to$ `1.21.13`) | Case D: Zero-Diff Fallback to Base (e.g. `1.25.1` $\to$ `1.25.0`) | Case E: Missing Base Version (e.g. `1.26.0` or `1.26.1`) |
|---|---|---|---|---|---|
| **Base file lookup** | Finds `go1.21.0.json` | Finds `go1.21.0.json` | Finds `go1.21.0.json` | Finds `go1.25.0.json` | Returns `null` (no `go1.26.0.json`) |
| **`getPatchVerDiffFile` loop** | Not executed (`patch == 0`) | Terminates on 1st iteration (`patchVer == 1.21.3`) | Iterates: 14 (null) $\to$ 13 (found) | Decrements: 1 (null) $\to$ 0 (loop ends) | Never reached (`getApiSnapshotJsonFile` returned null) |
| **Returned `patchDiffFile`** | `null` | `go1.21.3.json.diff` | `go1.21.13.json.diff` | `null` | N/A |
| **Logged message** | `Msg.info`: `"Using Go API snapshot for 1.21.0"` | `Msg.info`: `"Using Go API snapshot for 1.21.3"` | `Msg.warn`: `"Falling back from 1.21.14 to 1.21.13 for Go API snapshot"` | `Msg.warn`: `"Falling back from 1.25.1 to 1.25.0 for Go API snapshot"` | None in `GoApiSnapshot` |
| **Patch application** | Bypassed; unpatched base returned | `JsonPatchApplier` applies `go1.21.3.diff` to `go1.21.0.json` | `JsonPatchApplier` applies `go1.21.13.diff` to `go1.21.0.json` | Bypassed; unpatched base returned | None; returns `GoApiSnapshot.EMPTY` |
| **Underlying snapshot data** | Exact `1.21.0` types & funcs | Exact `1.21.3` types & funcs | **Exact `1.21.13` types & funcs** (stale relative to 1.21.14) | **Exact `1.25.0` types & funcs** (stale relative to 1.25.1) | No types; `arches.isEmpty() == true` |
| **`snapshot.getVer()`** | `1.21.0` | `1.21.3` | **`1.21.14`** (masks underlying data version) | **`1.25.1`** (masks underlying data version) | `GoVer.INVALID` (`0.0.0`) |
| **`GoRttiMapper:139` log** | `"Using Go API snapshot for version 1.21.0"` | `"Using Go API snapshot for version 1.21.3"` | **`"Using Go API snapshot for version 1.21.14"`** | **`"Using Go API snapshot for version 1.25.1"`** | Skipped (`!apiSnapshot.getVer().isInvalid()` is false) |
| **RTTI Recovery Fidelity** | Full fidelity for 1.21.0 | Full fidelity for 1.21.3 | **Type drift**: any fields/types modified in 1.21.14 are missing/wrong | **Type drift**: any fields/types modified in 1.25.1 are missing/wrong | **Fatal abort**: `registerStructures` fails $\to$ `BootstrapInfoException` |

### Detailed Behavioral Distinctions

1. **Exact match vs Fallback diff selection**:
   - In **Case B**, `patchVer == goVer`. The diff file corresponds precisely to the target binary's patch level. All standard library types, functions, and layout changes up to that patch level are faithfully applied.
   - In **Case C**, `patchVer < goVer`. Ghidra applies the closest lower patch diff available (`1.21.13`) directly to the base file (`1.21.0`). Any types or functions added, removed, or modified between `1.21.13` and `1.21.14` will **not** be reflected in analysis.
   - Empirical evidence of patch-level variance: In `go1.21.1.json.diff`, 497 total sections exist, modifying not only positions (288 func positions, 181 type positions) but also 9 struct fields (`Category ('Types', 'Fields')`) and function parameters/results (`crypto/tls`, `encoding/gob`, `runtime`). Thus, falling back to an earlier patch level can cause concrete field-offset and type mismatches.

2. **The Version Masking Anomaly in `GoApiSnapshot.read`**:
   - In `GoApiSnapshot.get(goVer, ...)` (`GoApiSnapshot.java:102–116`), the ByteProvider is read and passed to:
     `GoApiSnapshot.read(is, archSearchOrder, goVer);`
   - Notice that the third argument is `goVer` (the target version, e.g. `1.21.14` or `1.25.1`), **not** `patchVer` (`1.21.13` or `1.25.0`).
   - Consequently, the created `GoApiSnapshot` instance has `this.ver = goVer` (`GoApiSnapshot.java:391`).
   - Downstream in `GoRttiMapper.java:137–140`:
     ```java
     if (!apiSnapshot.getVer().isInvalid()) {
         Msg.info(GoRttiMapper.class,
             "Using Go API snapshot for version %s".formatted(apiSnapshot.getVer()));
     }
     ```
   - *Consequence*: `GoRttiMapper` logs that it is using the snapshot for version `1.21.14`, completely obscuring the fact that the underlying type data is actually from `1.21.13` (or `1.25.0`). The only place the fallback is recorded is the prior `Msg.warn` in `getPatchVerDiffFile`.

3. **Fallback to unpatched base (Case D)**:
   - When a minor release has a base file but zero diff files (such as Go 1.25 in Ghidra 12.1.4, which has `go1.25.0.json` but 0 diff files in `patchverdiffs/`), any binary compiled with Go 1.25.1 or later will decrement down to patch 0, log `Msg.warn("Falling back from 1.25.1 to 1.25.0...")`, and return `null` as the diff file.
   - The unpatched `go1.25.0.json` is returned directly without error. Analysis proceeds using Go 1.25.0 type definitions.

---

## 5. Architectural limits and vulnerabilities

1. **Single-Diff Non-Cumulative Fragility**:
   - As documented in `JsonPatchApplier.java:31–33`:
     > "Does not use any context hints in the diff to correct for mismatches, hence should only be used against the exact original value"
   - Because each diff file is designed strictly as a delta against the exact base `go<major>.<minor>.0.json`, the applier does not support 3-way merges or fuzzy offsets. If the base JSON file is modified, corrupted, or replaced with an incompatible version, `JsonPatchApplier.applySection()` throws an `IOException("Could not find next element in path...")` or `IOException("unsupported section")` (`JsonPatchApplier.java:114, 118`).
2. **Uncaught IOException in ByteProvider Push Lambda**:
   - In `getApiSnapshotJsonFile` (`GoApiSnapshot.java:135–144`), patch reading and application occurs inside the push lambda passed to `fsService.getDerivedByteProviderPush(...)`.
   - If an `IOException` occurs during patch parsing or application, it is caught when reading the ByteProvider stream in `GoApiSnapshot.get()`, which rethrows `IOException`.
   - In `GoRttiMapper.java:181–187`, this `IOException` escapes `getGoBinary` and is caught by `getSharedGoBinary` (`GoRttiMapper.java:99–102`), which logs `Msg.error(GoRttiMapper.class, "Failed to read Go info", e)` and returns `null`. This results in analyzer failure, but logs a generic error rather than a `BootstrapInfoException`.
3. **No Cross-Minor Fallback**:
   - The search loop `while (patchVer.getPatch() > 0)` operates strictly on patch numbers within the same minor version.
   - If `baseVer` (`go<major>.<minor>.0.json`) is absent (e.g. Go 1.26), the system aborts immediately with `GoApiSnapshot.EMPTY`. It never attempts to fall back to the highest available minor version (e.g. Go 1.25.0).
4. **Analysis Grounding and Limits of this Investigation**:
   - **Observed facts**: The control-flow branches, method invocations, logging statements, file presence counts, and JSON diff contents cited above were observed and verified directly from S003 archive source and the installed Ghidra 12.1.4 filesystem.
   - **[INFERENCE]**: That patch-level field differences (such as the 9 type field modifications observed in `go1.21.1.json.diff`) will cause struct layout divergence in downstream decompilation when earlier patches are selected. This is a logical consequence of `GoTypeManager.convertApiTypeDef`, not a measured target run.
   - **Limits**:
     - No live Ghidra analyzer execution or binary reverse engineering was performed this round.
     - No claims are made regarding historical target recovery outcomes (e.g. round 4 `1password-cli` `2.40.0-2`).
     - Not all 123 diff files were individually parsed and applied to their respective base files; the non-cumulative property was verified by inspection of the `JsonPatchApplier` implementation and sampling of `go1.21.1.json.diff` and `go1.21.2.json.diff`.

---

## 6. Proposed L1 checks (named; not executed by this seat)

L1 runs these once during final wave integration:

1. **Source digest check**: Verify SHA-256 digests of S001, S003, and S007:
   ```sh
   sha256sum /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md \
             /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
             /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md
   ```
2. **Anchor inspection in S003**: Inspect exact lines in `GoApiSnapshot.java` (lines 118–166) and `JsonPatchApplier.java` (lines 47–67, 75–120):
   ```sh
   unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
     ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java | sed -n '118,166p'
   ```
3. **Census confirmation**: Count base files and diff files under installed typeinfo directory:
   ```sh
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.*.0.json | wc -l
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/*.diff | wc -l
   ```
   (Expect 11 base JSON files and 123 patch diff files).
4. **Diff non-cumulative property check**: Verify that `go1.21.2.json.diff` diffs against base `go1.21.0.json` by inspecting the minus lines in `go1.21.1.json.diff` and `go1.21.2.json.diff` at the same symbol:
   ```sh
   grep -A 2 'crypto/tls.certificateRequestInfoFromMsg' \
     /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.21.1.json.diff \
     /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.21.2.json.diff
   ```
   (Both show `- "$GOROOT/crypto/tls/handshake_client.go:1011:6"`, matching `go1.21.0.json`).
5. **No worktree modification**: Confirm this seat edited no files outside `.ufo/waves/round-15/w1/PatchLookup.md`.

---

## 7. Tooling

No tools installed or updated. Used Python stdlib via bash for read-only archive inspection. Record: none.
