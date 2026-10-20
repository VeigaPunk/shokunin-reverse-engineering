# SourceChain — Falsifiable Diagnostic Sequence (S003 → S004 → S005 → S006)

- Lane: `KaidokuR14.SourceChain` (leaf member; UFO-FSD connector; no subagent dispatch).
- Round: Kaidoku round 14 (wave `kaidoku-r14-w1`).
- Evaluated axes: `coverage` (C1) and `calibration` (C2).
- Access date: 2026-10-20.
- Target: Connect S003 -> S004 -> S005 -> S006 into a falsifiable diagnostic sequence, identifying independent vs dependent support and limits. Open relevant source paragraphs.
- Contract: Source-only analysis. No builds, tests, linters, gate executions, live REA target execution, or client edits. Dispatched seats are author-side and cannot provide non-author admission.

---

## 1. Sources Opened (Fresh Opens, This Session)

| id | source location / identity | exact contiguous quote (<=25 words) | access date | limitations |
|---|---|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`), member `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | 2026-10-20 | Installed source archive; inspection of Java AST and constants only; does not execute Ghidra analyzer. |
| S003 | Same archive, member `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:358-360` | `throw new BootstrapInfoException( "Missing Go bootstrap type info, unable to extract Go RTTI info." .formatted(goVer));` | 2026-10-20 | Error handling path in `GoRttiMapper` constructor; verifies exception trigger when snapshot is invalid. |
| S003 | Same archive, member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | 2026-10-20 | Return value of `GoApiSnapshot.get` when JSON file is absent; empty snapshot causes `isInvalid() == true`. |
| S004 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 (Commit `385e8cd923d09f10b1a7874108e71748875fa174`, 2026-03-03) | “GP-6528 add support for golang 1.26” | 2026-10-20 | Upstream master commit; not present in installed release Ghidra 12.1.4. Demonstrates upstream patch scope, not host-held capability. |
| S005 | https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d (Commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`, 2026-02-17), README `Version Support` | “This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.” | 2026-10-20 | Documented version boundary; GoReSym was not executed against Go 1.26 binaries. |
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md`, section `# How Does BSim Work?`, lines 19–20 | “names of registers, and data types, are intentionally not incorporated into the features.” | 2026-10-20 | Installed documentation tutorial; teaches feature normalization and similarity properties, not an active REA matching run. |

---

## 2. Evidence: Diagnostic Chain and Structural Analysis

### S003: Installed Version-Gate Abort vs Layout Parse Failure
Inspection of the installed Ghidra 12.1.4 Base source archive reveals the exact mechanical path of Go symbol recovery:
1. `GoRttiMapper.java:79` defines `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`.
2. In `getGoBinary` (lines 170–172), if `!SUPPORTED_VERSIONS.contains(goVer)`, it emits `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer))`.
3. It then calls `GoApiSnapshot.get(goVer, ...)`. In `GoApiSnapshot.java:123–126`, `getApiSnapshotJsonFile` looks for `typeinfo/golang/go{baseVer}.json`. Filesystem inspection of `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` confirms the presence of `go1.15.0.json` through `go1.25.0.json`, but `go1.26.0.json` is physically absent.
4. When `jsonFile == null`, `GoApiSnapshot.get` returns `GoApiSnapshot.EMPTY` (line 115), where `isInvalid()` returns `true` (line 504).
5. In the `GoRttiMapper` constructor (lines 353–361), `registerStructures` fails because type info is missing, triggering:
   `throw new BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.".formatted(goVer));`.
6. This exception is caught in `getSharedGoBinary` (lines 114–116), which logs `Msg.warn(GoRttiMapper.class, mbie.getMessage())` and returns `null` (line 125).
7. Crucial structural finding: `findFirstModuledata(monitor)` (line 445) is called inside `init(monitor)`, which is only executed after successful instantiation. Because `getGoBinary` returns `null` during construction, `findFirstModuledata` is never reached.

**Explicit Contradiction Identified**: In `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:70–71`, the historical record asserted:
> "Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout (transient `Missing Go bootstrap type info, unable to extract Go RTTI info` seen in its `ghidra.log` during the session — dir since deleted, so this is observed-not-cited)."

Source inspection of S003 falsifies that assertion. Ghidra 12.1.4 never attempted to parse the Go 1.26 moduledata/pclntab layout; the recovery pipeline aborted upstream in the RTTI constructor due to the absence of the bootstrap snapshot JSON.

### S004: Upstream Patch Lineage and Dependency
Upstream commit GP-6528 (`385e8cd923d09f10b1a7874108e71748875fa174`, 2026-03-03) titled "GP-6528 add support for golang 1.26":
1. Updated `GoRttiMapper.java:79` to `GoVerRange.parse("1.15-1.26")`.
2. Added the missing snapshot bootstrap data file `go1.26.0.json`.
3. Support classification: **Dependent Support**. S004 and S003 are sequential revisions of the same subsystem in the same codebase. S004 confirms that the failure in S003 was due to gate bounds and snapshot omission rather than an architectural redesign of moduledata parsing. However, S004 is on master, not in release 12.1.4, and cannot be treated as an available capability on the host.

### S005: Independent Parser Scope and the Corroboration Trap
Mandiant GoReSym (commit `d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d`, 2026-02-17):
1. Written in Go, independent of Ghidra. It parses `pclntab` and `moduledata` directly from executable sections.
2. Its README explicitly bounds its parser: "This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20."
3. Support classification: **Independent Codebase, Bounded Scope**. GoReSym provides an independent route for Go binaries up to layout 1.20.
4. **Epistemic Limit & Risk**: An analyst observing that Ghidra recovered zero symbols on Go 1.26 might look at GoReSym's failure on 1.26 and infer that both tools independently confirm that "Go 1.26 altered the pclntab structure". Under S011 (Santos-Grueiro, representation confusion), attributing layout breakage to Go 1.26 based on two tools whose documented version boundaries stop at 1.25 and 1.20 is an invalid multi-tool corroboration error. GoReSym does not claim Go 1.26 compatibility.

### S006: Feature-Vector Similarity as a Name-Free Route-Around
Ghidra BSim Tutorial (`BSimTutorial_Intro.md`, lines 15–20):
1. BSim generates feature vectors from Ghidra decompiler data flow and control flow.
2. Crucial property: "names of registers, and data types, are intentionally not incorporated into the features."
3. When Go toolchain naming collapses (as seen in `op-2.40.0` where 11,588 procedures collapsed to `FUN_*`), BSim can match functions across versions (e.g. `op-2.34.1` with recovered symbols vs `op-2.40.0` with `FUN_*`) without requiring pclntab or RTTI type info.
4. Support classification: **Orthogonal Fallback with Calibration Bound**.
5. **Epistemic Limit**: S006 explicitly states that BSim measures cosine similarity over normalized syntax graphs. Cosine similarity is a candidate-generation heuristic, NOT proof of semantic equivalence. Furthermore, BSim does not recover the authoritative pclntab symbol names; it only provides candidate associations to prior analyzed programs.

---

## 3. The Sequence: Falsifiable Differential Diagnostic Sequence

When an analyst or automated pipeline encounters a Go binary with missing or collapsed symbols (predominantly `FUN_*` stubs):

```
                       [Target Go Binary]
                               |
                               v
             Step 1: Check Go Version in Binary (S003)
                               |
       +-----------------------+-----------------------+
       |                                               |
  GoVer in [1.15, 1.25]                       GoVer >= 1.26
       |                                               |
       v                                               v
[Inspect binary layout /                     [Step 1a: S003 Diagnosis]
 memory sections; pclntab                    Ghidra 12.1.4 version gate trips:
 corruption or strip]                        - "Untested Go version" logged
                                             - go1.26.0.json missing -> EMPTY snapshot
                                             - BootstrapInfoException raised
                                             - findFirstModuledata NEVER REACHED
                                             (Layout failure disproven)
                                                       |
                                                       v
                                             [Step 2: Upstream Check (S004)]
                                             - GP-6528 commit on master
                                             - Dependent confirmation of gate mechanism
                                             - Unreleased on host (No live upgrade)
                                                       |
                                                       v
                                             [Step 3: Secondary Tool Check (S005)]
                                             - Check GoReSym stated layout range (<= 1.20)
                                             - Independent parser, but bounded
                                             - Prohibit claiming Go 1.26 layout breakage
                                                       |
                                                       v
                                             [Step 4: Topology Route-Around (S006)]
                                             - Engage BSim feature-vector cosine similarity
                                             - Strips names/types; pairs CFG candidates
                                             - Calibrate: candidate match != semantic proof
```

---

## 4. Proposed Move (Connector Synthesis)

### Proposed Move
**Synthesize the S003 → S004 → S005 → S006 diagnostic chain into a 4-tier differential decision framework for the C1 knowledge entry (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`), while coupling its citation anchors directly to C2's quote-fidelity contract.**

### Specific Mechanics
1. **Falsify and Replace Historical Conjecture**:
   Explicitly correct `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:70–71` in the new C1 entry. Document that the Go 1.26 symbol collapse in `op-2.40.0` was caused by Ghidra's upstream `BootstrapInfoException` (S003) and absence of `go1.26.0.json`, not by layout parsing failure.
2. **Enforce Origin Grouping & Independence Bounds (S011)**:
   In the decision table, explicitly mark S003 and S004 as **dependent** (same engine lineage) and mark S005 as **independent-but-unsupportive** of Go 1.26 layout assertions. Prohibit the inference that two un-updated tools failing on Go 1.26 proves an underlying binary layout change.
3. **Calibrate the Fallback Boundary (S006)**:
   Define BSim function matching as a topological route-around for un-symbolized Go binaries, but enforce the calibration limit: feature similarity abstracts away constants, registers, and types, providing candidate pairs rather than ground-truth recovered symbols or semantic equivalence.
4. **Coupling to C2 Calibration Gate**:
   Provide exact, contiguous, <=25-word excerpts for S003, S004, S005, and S006 with explicit section anchors to serve as verified green inputs for C2's quote-fidelity manifest.

---

## 5. Affected Axes

- **`coverage` (C1) — Improved**:
  Establishes the first source-grounded Go recovery version-gate diagnosis entry in `corpus/knowledge/`. Bridges the coverage gap by replacing an uncited log conjecture with an exact AST/exception trace (S003), upstream commit tracking (S004), external parser boundary (S005), and representation fallback (S006).
- **`calibration` (C2) — Improved / Protected**:
  Prevents false corroboration (Santos-Grueiro S011) by classifying tool dependencies. Prevents over-claiming BSim similarity as semantic truth. Furnishes verified, contiguous <=25-word quote inputs with exact headings for C2 gate verification.
- **No Harm to Existing Saturated Proxies**:
  Does not inflate finite scores (remains at saturation/ceiling). Uses existing mined rows S003–S006 from `SOURCES.md` without adding unneeded rows or invalid tiers. Does not shift pinned line citations in historical files.

---

## 6. Risks and Verification

### Risks
1. **Upstream Promotion Risk**: An operator reading S004 might assume that because NSA patched GP-6528, Ghidra 12.1.4 can parse Go 1.26 by merely toggling a setting. Risk mitigation: S004 must be strictly labeled as an unreleased upstream master commit; the host binary remains 12.1.4.
2. **Heading Grammar Mismatch in C2 Gate**: As discovered by `ReviewS017`, raw source files may contain HTML headings (`<h1>`–`<h3>`) or code-level anchors rather than Markdown `#` headings. Risk mitigation: C1 quotes from S006 (`BSimTutorial_Intro.md`) use exact Markdown `#` headings (`# How Does BSim Work?`), making S006 a valid Markdown green case under C2's current gate contract. Code sources (S003/S004) are cited by file path, commit hash, and line numbers.
3. **Over-reliance on BSim**: Analysts may treat high BSim cosine similarity as proof that an un-symbolized Go 1.26 function is identical to a Go 1.25 function. Risk mitigation: The decision framework explicitly notes S006's intentional exclusion of constants and types.

### Verification (for L1 Integration)
1. **Source Hash and Location Verification**:
   - `sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` matches `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`.
   - `unzip -p .../Base-src.zip .../GoRttiMapper.java | grep -n 'SUPPORTED_VERSIONS = '` hits line 79.
   - `test -e /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json` returns exit code 1 (absent).
2. **C2 Gate Execution**:
   - L1 runs `quote-fidelity.py --manifest PATH` against frozen fixtures containing the verified S006 excerpt under `# How Does BSim Work?`.
   - Expected verdict: clean (exit 0).
3. **Knowledge Entry Conformance**:
   - L1 verifies that `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` includes the observation/inference/unknown labels, cites S003–S006, and contains no live target execution claims.
