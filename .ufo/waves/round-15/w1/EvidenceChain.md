# EvidenceChain — Inventory-to-Diagnostic Inference Chain & Epistemic Boundaries

- Seat: `KaidokuR15.EvidenceChain` (leaf member; UFO-FSD connector; no subagent dispatch).
- Round: Kaidoku round 15 (wave `kaidoku-r15-w1`).
- Evaluated axes: `depth` (C1) and `calibration` (C2).
- Access date: 2026-10-20.
- Assigned report path: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/EvidenceChain.md`.
- Target: Map inventory → source selection → diagnostic inference chain; discriminate independent observations vs shared source origin; formalize forbidden historical causality conclusions; synthesize C1 and C2 into a single bounded move.
- Limits & Custody: Source and filesystem inspection only. No builds, tests, linters, formatters, gate executions, or live REA/target operations. No tools installed or upgraded (record: none). All repository references are absolute under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

---

## 1. Grounded Evidence: The Inventory → Selection → Diagnostic Chain

### 1.1 The Pinned Snapshot Asset Inventory

Inspection of the installed Ghidra 12.1.4 distribution at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` establishes the concrete on-disk asset boundary:

1. **Base Snapshot JSON Files (`go{major}.{minor}.0.json`):**
   - Present: 11 base JSON files spanning `go1.15.0.json` through `go1.25.0.json`.
   - Absent: `go1.26.0.json` (and all higher versions) is physically absent from disk.
2. **Patch Version Diffs (`patchverdiffs/go{major}.{minor}.{patch}.json.diff`):**
   - Present: 123 patch diff files spanning `go1.15.1.json.diff` to `go1.24.6.json.diff` (grounded by complete read-only directory filename census; an earlier 98-file figure was an unverified pagination truncation artifact of the tool default window).
   - Absent: No patch diff files exist for Go 1.25 (i.e. `go1.25.*.json.diff` is empty/absent), nor for Go 1.26.
3. **Legacy GDT Type Archives (`golang_{major}.{minor}_anybit_any.gdt`):**
   - Present: 9 files spanning `golang_1.15_anybit_any.gdt` through `golang_1.23_anybit_any.gdt`.
   - Inactive: Inactive for RTTI bootstrapping on this path per S007 (`ChangeHistory.md:585`).
4. **Architecture/OS Key Filter Set:**
   - Inspection of `go1.25.0.json` top-level keys reveals 27 target architectures/OS keys: `386`, `all`, `amd64`, `arm`, `arm64`, `cgo`, `darwin`, `darwin-amd64`, `darwin-amd64-cgo`, `darwin-arm64`, `darwin-arm64-cgo`, `linux`, `linux-386`, `linux-386-cgo`, `linux-amd64`, `linux-amd64-cgo`, `linux-arm`, `linux-arm-cgo`, `linux-arm64`, `linux-arm64-cgo`, `linux-cgo`, `unix`, `windows`, `windows-386`, `windows-386-cgo`, `windows-amd64`, `windows-amd64-cgo`.

### 1.2 The 5-Stage Control-Flow Cascade

Source reading of S003 (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`) maps the exact mechanical sequence executed when Ghidra analyzes a Go binary:

```
Binary BuildInfo (goVer, goOS, goArch)
  │
  ├── [Stage 1: Advisory Version Range Check]
  │   `GoRttiMapper.java:79, 170-176`
  │   SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");
  │   Out-of-range: logs Msg.error("Untested Go version [%s]"), does NOT throw/return.
  │   Continues directly to Stage 2.
  │
  ├── [Stage 2: Base File Lookup & Patch Fallback]
  │   `GoApiSnapshot.java:105-166`
  │   goVer.withPatch(0) -> checks `typeinfo/golang/go{baseVer}.json`.
  │   ├── Case 2A: Base JSON Absent (e.g. Go 1.26)
  │   │   Returns null -> GoApiSnapshot.get returns EMPTY (`arches` is empty).
  │   └── Case 2B: Base JSON Present (e.g. Go 1.24 or 1.25)
  │       Searches backwards in `patchverdiffs/` for closest patch diff.
  │       - Found: applies JSON patch diff to base.
  │       - Not found (e.g. Go 1.25.3): falls back to base JSON directly (non-fatal!).
  │
  ├── [Stage 3: OS / Architecture Key Filtering]
  │   `GoApiSnapshot.java:205-239, 503-505`
  │   archSearchOrder = [goOS-goArch, goOS, unix?, goArch, all].
  │   Filters JSON to matching keys.
  │   If arches map is empty: `apiSnapshot.isInvalid() == true`.
  │
  ├── [Stage 4: Virtual Struct Registration & Exception Discrimination]
  │   `GoRttiMapper.java:340-390`, `DataTypeMapper.java:172-176, 310-313`, `GoTypeManager.java:448-450`
  │   registerStructures calls virtual getType() -> delegates to GoTypeManager -> queries apiSnapshot.
  │   If apiSnapshot.isInvalid():
  │   ├── struct lookup returns null -> registerStructure throws IOException.
  │   └── initStructMappings catches IOException:
  │       if (apiSnapshot.isInvalid()) -> throws BootstrapInfoException("Missing Go bootstrap type info...")
  │       else -> throws IOException("Invalid Go bootstrap struct mapping info: ...")
  │
  └── [Stage 5: Outer Analyzer Termination]
      `GoRttiMapper.java:114-126`, `GolangSymbolAnalyzer.java:133-137`
      BootstrapInfoException caught in getSharedGoBinary -> logs warning -> returns null.
      GolangSymbolAnalyzer sees null -> logs Msg.error -> returns false (aborts).
      CRITICAL: findFirstModuledata() and pclntab parsing are NEVER REACHED.
```

### 1.3 Resolution of Routed Defect 1: Virtual Dispatch Call Edge

In round 14, advisory reviewer artifact `.ufo/waves/round-14/w1/ReviewGoInference.md:57-61` asserted:
> "registerStructures does not consult the snapshot; snapshot absence only changes the log text, not the analyzer outcome."

This assertion is structurally **refuted** by the Java AST in S003:
1. `GoRttiMapper.java:353`: `initStructMappings` invokes `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`.
2. `DataTypeMapper.java:176`: `registerStructure` queries `Structure structDT = getType(structNames, Structure.class);`.
3. `DataTypeMapper.java:310-313`: `getType(List<String> names, Class<T> clazz)` loops over names and calls polymorphic `getType(dtName, clazz)`.
4. `GoRttiMapper.java:379-382`: `GoRttiMapper` overrides `getType(String name, Class<T> clazz)` and delegates to `goTypes.findDataType(name)`.
5. `GoTypeManager.java:448-450`: for non-primitive types, `findTypeRec` queries `typeDef = apiSnapshot.getTypeDef(typeName)`.
6. When `apiSnapshot` is `EMPTY` (or invalid), `apiSnapshot.getTypeDef(typeName)` returns `null`. Consequently, `findDataType` returns `null`, `structDT` is `null`, and `DataTypeMapper.java:176` throws `IOException("Missing struct definition for class...")`.
7. `GoRttiMapper.java:356-361`: catches the `IOException`, inspects `apiSnapshot.isInvalid()`, and throws `BootstrapInfoException`.

**Conclusion**: Snapshot validity is an active computational dependency of struct type resolution during `registerStructures`, not merely a log-formatting selector.

---

## 2. Epistemic Categorization: Independent Observations vs. Shared Source Origin

To prevent pseudo-corroboration and score inflation, we must categorize evidence by source lineage:

```
[Upstream Ghidra Git Repository (NSA)]
  │
  ├── Commit 385e8cd9 (S004: GP-6528 Go 1.26 support)  <── DEPENDENT EVOLUTION
  │
  └── Release Tag 12.1.4
        │
        ├── Distribution Archive: Base-src.zip (S003) ──┐
        ├── Distribution Data: typeinfo/golang/ (*.json) ──┼── SHARED SOURCE ORIGIN
        └── Distribution Docs: ChangeHistory.md (S007) ──┘   (O_Ghidra12.1.4)

[Mandiant GoReSym Repository]
  └── Commit d7f23b7a (S005)                           <── INDEPENDENT CODEBASE
                                                           (Bounded to <= 1.20)
```

### 2.1 The Shared Source Origin Principle (O_Ghidra12.1.4)
- **Observation**: S003 (`Base-src.zip`), the installed typeinfo data files (`go1.15.0.json` ... `go1.25.0.json`), and S007 (`ChangeHistory.md`) are extracted from the identical binary/source release package (`ghidra_12.1.4_PUBLIC`).
- **Epistemic Limit**: Inspecting `GoApiSnapshot.java` (code) and observing the absence of `go1.26.0.json` in the filesystem (data) does **not** constitute two independent corroborating witnesses. They are two manifestations of the same monolithic release boundary. Treating them as independent confirmation would commit a representation-confusion error (Santos-Grueiro, S011).

### 2.2 Dependent Upstream Evolution (S004) vs. Independent Bounded Parsers (S005)
- **S004 (Ghidra GP-6528 Commit `385e8cd9`)**:
  - Dependent lineage: S004 is an upstream patch to S003, authored by the same maintainers in the same codebase.
  - S004 changes the range in `GoRttiMapper.java`, adds `go1.26.0.json`, and updates moduledata locators and type structures.
  - S004 confirms that Go 1.26 support required multiple coordinated changes, but it does **not** provide independent external validation of how Go 1.26 binaries are laid out in the wild.
- **S005 (Mandiant GoReSym Commit `d7f23b7a`)**:
  - Independent codebase: GoReSym is a clean-room Go-based parser independent of NSA/Ghidra.
  - Stated boundary: GoReSym's README explicitly caps its pclntab parser at Go 1.20. It cannot corroborate or falsify Ghidra's behavior on Go 1.26 binaries because Go 1.26 layout parsing falls outside GoReSym's declared envelope.

---

## 3. Forbidden Historical Causality Conclusions

A central calibration requirement for Round 15 is preventing false retrospective causality claims regarding past round observations.

### 3.1 Necessary Preconditions vs. Historical Causality Fallacy
In Round 4 (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73`), it was asserted:
> "Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout (transient `Missing Go bootstrap type info, unable to extract Go RTTI info` seen in its `ghidra.log` during the session — dir since deleted, so this is observed-not-cited)."

In Round 14, static source analysis revealed that `Missing Go bootstrap type info` is thrown during RTTI constructor initialization, long before moduledata parsing is attempted.

However, the reverse causal assertion is **strictly forbidden**:
> *Forbidden Claim*: "Because `go1.26.0.json` is missing from Ghidra 12.1.4's installation, the Round 4 analysis failed specifically because of the missing JSON snapshot."

### 3.2 Epistemic Status: UNKNOWN Historical Reality
Why is this historical causal conclusion forbidden?
1. **Unretained Artifacts**: The transient analysis directory, heap state, and full execution log from Round 4 were deleted. No raw log records remain.
2. **Multiple Sufficient Barriers**:
   - Barrier A: If build info extraction failed or returned invalid version, it aborted.
   - Barrier B: If the snapshot base file was missing, it aborted.
   - Barrier C: If OS/arch keys were unrepresented, it aborted.
   - Barrier D: If the binary was stripped or packed, symbol parsing aborted earlier.
3. **Absence of Historical Target Replay**: No controlled execution replay of the exact 1password-cli 2.40.0-2 binary under instrumented Ghidra 12.1.4 was conducted in Round 14 or Round 15.
4. **Logical Asymmetry and Non-Universal Static Scope**:
   - Source companion code (`Base-src.zip`) and data files (`typeinfo/golang/`) establish necessary structural preconditions in the inspected source path.
   - Crucially, **installed data and source files are not executing compiled classes**. We did not inspect or trace the compiled JVM bytecode or runtime classloading of the installed Ghidra build, nor did we execute the binary under test.
   - Therefore, we avoid any universal claim that "Ghidra as an executing runtime cannot parse Go 1.26 under any circumstances." We assert only what is directly observed: in the installed release's companion source and data files, `go1.26.0.json` is physically absent, and the inspected source code path requires a snapshot to complete struct registration.
   - Furthermore, deductive analysis of static source code can never reconstruct the actual causal trajectory of an unrecorded past execution.

The epistemic status of the historical failure mechanism remains permanently **UNKNOWN**.

---

## 4. Resolution of Routed Defect 2: The Machine-Gradeable Input Boundary

### 4.1 Byte-Substring Truth vs. "Does Not Grade" Overclaim
In round 14, `corpus/QUALITY.md` row 16 asserted that `.ufo/waves/round-14/tools/quote-fidelity.py` "does not grade" markup-spanning quotations, commit objects, or JSON.

Inspection of `.ufo/waves/round-14/tools/quote-fidelity.py`:
- Lines 250–257: `grade_quote` performs a raw, non-normalizing byte substring search: `if quote["quote"] not in text: findings.append(...)`.
- Exit mapping (`lines 97-100`):
  - Exit 0: All quotes match raw text contiguously.
  - Exit 1: Substring mismatch (`quote_not_contiguous` or `quote_location_mismatch`).
  - Exit 2: Tool failure / invalid manifest (`invalid_manifest`, `source_tampered`, `snapshot_tampered`).

If a human-rendered quote (such as Markdown text where newlines or formatting have been reflowed, or HTML where tags were stripped) is submitted, `quote-fidelity.py` **does not skip or refuse to grade it**. Instead, it executes `not in text`, evaluates to false, and issues a failing verdict with exit code 1 (`quote_not_contiguous`).

### 4.2 Superseding Specification for QUALITY #16
The assertion that the instrument "does not grade" these formats is factually incorrect and miscalibrated. The correct operational boundary is:
> **Superseding QUALITY Criterion**: The quote fidelity instrument operates strictly on raw, verbatim UTF-8 byte substrings without markup parsing, AST tokenization, or whitespace normalization. Therefore, inputs that have undergone rendering, whitespace collapsing, HTML decoding, or format transformation fall outside the tool's valid grading domain and **MUST NOT** be submitted to machine quote grading. Such inputs require manual verification. Submitting transformed inputs to the machine grader constitutes an input error, as the tool will mechanically grade and reject them as `quote_not_contiguous` (exit 1).

---

## 5. Affected Axes Evaluation

### 5.1 Axis 1: Depth (C1)
- **Deepened Diagnostic Fidelity**: Replaces vague notions of "version incompatibility" or "snapshot missing" with a 5-stage deterministic evaluation cascade:
  1. Advisory Range (`SUPPORTED_VERSIONS`)
  2. Base JSON Snapshot (`go{base}.0.json`)
  3. Patch Diff Fallback (`getPatchVerDiffFile` backward walk across 123 patch diff files)
  4. OS/Arch Filtering (`archSearchOrder`)
  5. Virtual Struct Resolution (`GoRttiMapper.getType` -> `GoTypeManager.findTypeRec`)
- **Discriminates Non-Fatal from Fatal Absences**: Proves from S003 source that missing patch diffs (e.g. Go 1.25.3) are gracefully handled via base snapshot fallback without error, whereas missing base JSON files (e.g. Go 1.26.0) cause immediate return of `EMPTY` and fatal struct registration failure.

### 5.2 Axis 2: Calibration (C2)
- **Calibrated Epistemic Boundaries**:
  - Distinguishes shared-origin release artifacts from independent corroboration.
  - Formally bars retrospective causal claims about lost historical runs.
  - Distinguishes deductive source capability bounds from unrecorded execution history.
- **Calibrated Verification Contracts**:
  - Rectifies the virtual dispatch oversight in the advisory review record without altering production gate code.
  - Replaces the inaccurate "does not grade" description with a precise definition of the tool's raw-byte domain and prohibited input classes.

---

## 6. The Proposed Move: Integrated Diagnostic Cascade & Epistemic Separation

### 6.1 Compatible Synthesis
We propose a single, bounded synthesis connecting C1 and C2:
**The Precondition-Precedence & Epistemic Boundary Framework**:
1. **Admit C1 as a Static Capability & Inventory Boundary Record**:
   - Record the exact census of installed base snapshots (11), patch diffs (123 grounded by read-only filename census, correcting an earlier 98-file tool-truncated count), and architecture keys (27).
   - Document the 5-stage evaluation cascade as a model of *toolchain companion source capability*, explicitly classified under `[INFERENCE FROM SOURCE]` and `[OBSERVATION]`. Installed data and source files are qualified as not being executing compiled classes.
   - Explicitly classify any attribution of historical run failures to this mechanism as `[FORBIDDEN HISTORICAL CAUSALITY CONCLUSION / STATUS: UNKNOWN]`.
2. **Fulfill C2 Routed Duties via Documentation & Advisory Addenda Only**:
   - Duty 1: Append an advisory correction to the round-14 review record documenting the virtual dispatch call edge (`DataTypeMapper.registerStructure` → `GoRttiMapper.getType` → `GoTypeManager` → `apiSnapshot`), refuting the "does not consult snapshot" error.
   - Duty 2: Update QUALITY criterion #16 to formally define the raw-substring domain and prohibit submission of transformed/rendered quotes, without modifying the underlying `quote-fidelity.py` script.

---

## 7. Second-Order Risks and Structural Limitations

1. **Substrate & Version Drift Risk**:
   - The analysis binds strictly to Ghidra 12.1.4 (S003). Upstream commits (S004) indicate that later versions of Ghidra refactored moduledata structures and added Go 1.26 snapshots. Applying these conclusions to newer Ghidra releases without re-verifying `Base-src.zip` would introduce version skew.
2. **Verification Contract Risk**:
   - If an agent attempts to submit a code-comment excerpt or rendered HTML block to `quote-fidelity.py`, the tool will emit exit 1. The documentation must clearly enforce that L1 and future waves route non-raw citations to manual review.
3. **No Execution Replay**:
   - Static AST and control-flow tracing do not guarantee that unexpected runtime edge cases (such as ClassLoader failures or corrupted memory) cannot alter execution order in a live JVM.

---

## 8. Proposed L1 Verification Checks

In strict accordance with leaf bounds, this seat executed zero verification, builds, or tests. L1 is proposed to run the following checks once all wave seats complete:

1. **Hash Verification of Shared Release Sources**:
   ```sh
   sha256sum \
     /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md \
     /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
     /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md
   ```
   *Expected*: `c8639823...`, `f00d29c2...`, `c6b25301...`.

2. **Snapshot Inventory Census Verification**:
   ```sh
   # Verify base JSON count (11 files)
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go*.0.json | wc -l
   # Verify patch diff count (123 files)
   ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/*.diff | wc -l
   # Verify absence of Go 1.26 base JSON
   test ! -f /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json

3. **Virtual Dispatch AST Cross-Check**:
   ```sh
   unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
     ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | grep -n "public <T extends DataType> T getType"
   ```
   *Expected*: Line 379 confirms override in `GoRttiMapper`.

4. **Quote Gate Behavior & Quality Criterion Consistency**:
   ```sh
   # Verify quote gate preserves existing raw-matching logic without code mutation
   git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff .ufo/waves/round-14/tools/quote-fidelity.py
   ```
   *Expected*: Zero diffs on `quote-fidelity.py`.
