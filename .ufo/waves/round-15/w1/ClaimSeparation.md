# ClaimSeparation — C1/C2 Separability, Lowest-Axis Tie & Carrier-Target Mapping

- **Seat:** `KaidokuR15.ClaimSeparation` (connector, leaf member; no subagent dispatch).
- **Round / Wave:** Kaidoku round 15 (`kaidoku-r15-w1`).
- **Lane Root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- **Target:** Assess C1/C2 separability and lowest-axis tie; map planned real-carrier move to missing caller-selected target and justify source-inventory route without claiming replay.
- **Assigned Output:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/ClaimSeparation.md`.
- **Declared Round Axes:** `depth` (Claim C1) and `calibration` (Claim C2).
- **Date:** 2026-10-20.
- **Limits & Custody:** Read-only inspection of repository files, S003 archive, installed Ghidra files, and sibling candidate drafts. Zero builds, tests, linters, formatters, gate runs, or target/provider executions were conducted by this seat. Tool installs or upgrades: none (record: none).

---

## 1. Grounded Evidence: C1 and C2 Claims and Anchors

Round 15 defines two explicit claims in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/claims.json:4-11`:

- **Claim C1 (`depth`):**
  > "A pinned installed Go JSON snapshot inventory and source-selection decision record discriminate missing base, patch-diff, and OS/architecture applicability without asserting historical target causality. Before no round15 inventory/decision record; after one reproducible inventory plus sourced knowledge."
- **Claim C2 (`calibration`):**
  > "Resolve both round14 outside-routed defects: append named virtual-dispatch advisory correction and superseding QUALITY criterion explicitly requiring manual-only rendered/code/JSON inputs not be submitted to raw quote machine grading. Existing gate raw behavior retained and exercised as a documented limit, not a new gate capability."

### Exact Source Anchors

1. **Installed Ghidra 12.1.4 Distribution Filesystem State:**
   - Physical directory: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`
   - Observed Base Snapshots: Exactly 11 base JSON files (`go1.15.0.json` through `go1.25.0.json`). No `go1.26.0.json` or higher exists on disk.
   - Observed Patch Diffs: Under `patchverdiffs/`, exactly 123 `.diff` files exist across the 10 supported minor versions, confirmed by the grounded per-minor histogram (1.15: 15, 1.16: 15, 1.17: 13, 1.18: 10, 1.19: 13, 1.20: 14, 1.21: 13, 1.22: 12, 1.23: 12, 1.24: 6 = 123 total; $15+15+13+10+13+14+13+12+12+6 = 123$). No `go1.25.*.diff` files and no `go1.26.*.diff` files exist. (The earlier 114 count is withdrawn as unsupported).
   - Legacy GDT Files: 9 `.gdt` files (`golang_1.15_anybit_any.gdt` to `golang_1.23_anybit_any.gdt`), inactive for RTTI bootstrapping per S007 (`ChangeHistory.md:585`).

2. **S003 Source Control Flow (`Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`):**
   - `GoRttiMapper.java:79`: `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`.
   - `GoRttiMapper.java:170-176`: Range check logs `Msg.error("Untested Go version [%s]")` and falls through; does NOT throw or return.
   - `GoApiSnapshot.java:105-116, 122-126`: `getApiSnapshotJsonFile` requests `goVer.withPatch(0)`. If base file is absent (e.g. Go 1.26), returns `null`, causing `GoApiSnapshot.get` to return `GoApiSnapshot.EMPTY`.
   - `GoApiSnapshot.java:148-166`: `getPatchVerDiffFile` walks backwards via `prevPatch()` within the same minor version. If no diff is found (e.g. Go 1.25.x), returns `null`, and line 128 falls back to raw base snapshot bytes without throwing.
   - `GoApiSnapshot.java:108-109, 205-239, 503-505`: `archSearchOrder` includes `"all"`. Every installed base file contains `"all"`, so `arches` is non-empty and `isInvalid()` evaluates to `false` for any present base file.
   - `GoRttiMapper.java:353-365`: `initStructMappings` invokes `registerStructures`. If `IOException` is thrown, checks `apiSnapshot.isInvalid()`. If true, throws `BootstrapInfoException("Missing Go bootstrap type info...")`.
   - `DataTypeMapper.java:176, 310-313` & `GoRttiMapper.java:379-382` & `GoTypeManager.java:443-451`: Struct resolution invokes virtual `getType(name, clazz)` on `this` (`GoRttiMapper`), which queries `GoTypeManager.findDataType` -> `findTypeRec` -> `apiSnapshot.getTypeDef(typeName)`. For `EMPTY` snapshot, returns `null`, throwing `IOException("Missing struct definition...")`.

3. **Existing Gate Control Flow (`.ufo/waves/round-14/tools/quote-fidelity.py`, SHA-256 `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`):**
   - `:78`: `CNE_FINDINGS = frozenset({"invalid_manifest", "source_tampered", "snapshot_tampered"})`.
   - `:97-100`: `exit_code` returns 2 only for `CNE_FINDINGS`; otherwise returns 1 if findings exist, or 0 if clean.
   - `:250-258`: `grade_quote` performs literal `if quote["quote"] not in text:` on raw UTF-8 bytes without tag stripping, normalization, or formatting awareness. If not found, emits `quote_not_contiguous` (exit 1).

---

## 2. Assessment of C1 / C2 Separability

Claims C1 and C2 are structurally, epistemically, and operationally **separable**:

| Dimension | Claim C1 (`depth`) | Claim C2 (`calibration`) | Separability Assessment |
|---|---|---|---|
| **Primary Domain** | Static reverse engineering of Ghidra 12.1.4 Go RTTI typeinfo bootstrap assets and control flow. | Governance calibration of quote verification gate and correction of prior advisory review text. | **Orthogonal domains**: C1 investigates decompiler provider internals; C2 governs evidence verification discipline. |
| **Substrate / File Boundaries** | New knowledge entry (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`), read-only inventory tool (`.ufo/waves/round-15/snapshot-inventory.py`), and map token in `corpus/README.md`. | Appended row in `corpus/QUALITY.md` (row 17), append-only correction in `corpus/lessons/round-14.md` / `LOG.md`, and synthetic fixtures under `.ufo/waves/round-15/boundary-fixtures/`. | **Disjoint write surfaces**: Zero overlapping target files. No code or doc edit in C1 touches any file modified by C2. |
| **Verification Tooling** | Verified by stdlib filesystem/Git object inspection (`measure.py`, `ls-tree`, `sha256sum`). | Verified by unchanged `quote-fidelity.py` running on synthetic raw/rendered limitation fixtures. | **Independent verification mechanisms**: Neither claim's automated or manual checks execute or evaluate the other. |
| **Failure Modes & Independence** | If C1's inventory script fails or the decision table is rejected, C2's QUALITY row 17 and advisory correction remain 100% valid. | If C2's wording is challenged or boundary fixtures fail, C1's snapshot inventory and Go control-flow analysis remain 100% valid. | **Decoupled fates**: Neither claim is a prerequisite or causal consequence of the other. |
| **Shared Epistemic Thread** | Replaces speculative version assumptions with exact static structural preconditions. | Replaces inaccurate "does not grade" claims with an exact raw-byte submission precondition. | **Epistemic synergy without functional coupling**: Both enforce negative boundary definitions. |

---

## 3. Analysis of Lowest-Axis Tie & Zero-Headroom Reality

In `claims.json:12`, the lowest axis is declared as:
> `"lowest_axis": "three owned proxies tie at 10; calibration worked; no numeric inflation"`

### 3.1 The Mathematical Basis of the Tie
Inspection of `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:21-32` and `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/ReviewMeasurement.md:27-32` reveals why all owned axes tie at 10.0:

1. **`coverage` (10.0):** Defined as `10 * mapped / knowledge_files` over `corpus/README.md:11-69`. At baseline `9719dd232687f5ee78a4ed323b37f8810e833d10`, 92 of 92 files are mapped ($10 \times 92/92 = 10.0$).
2. **`depth` (10.0):** Defined as `10 * resolved / rule_blocks` over `SKILL.md:77-191` queue-drain rules. At baseline, 17 of 17 rules resolve ($10 \times 17/17 = 10.0$).
3. **`calibration` (10.0):** Defined as the historical reconciliation of rubric obligations / receipts in round 1 / round 2. Clamped at 10.0.

All three owned proxy formulas have reached their maximum scalar ceiling ($10.0 / 10.0 / 10.0$).

### 3.2 Epistemic Consequences: Zero Headroom and Prohibition of Score Inflation
- **No Scalar Room to Move:** A finite proxy score of 10.0 represents proxy saturation, not total mastery of the reverse engineering domain (`SCORECARD.md:31`: *"A perfect finite proxy retires no domain axis and closes no promotion gate"*).
- **Fraudulent Inflation Rejected:** Attempting to report scores above 10.0 (e.g. 10.1 or 11/10) or inventing arbitrary decimal increments violates the scoring contract and calibration bar.
- **Scorecard Sensitivity Trap (The Coverage Risk):** As documented in `ReviewMeasurement.md` (H3), if C1 commits a new knowledge entry (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`) and L1 fails to add its corresponding token into `corpus/README.md:11-69`, the coverage proxy will **drop** from 10.0 to 9.89 ($10 \times 92/93$).
- **Qualitative Resolution:** Because all numerical proxies tie at 10.0 with zero headroom, the round focuses strictly on **qualitative depth and calibration**:
  - Advancing `depth` by moving from code-level hypotheses to reproducible installed snapshot asset inventories and multi-case decision tables.
  - Advancing `calibration` by rectifying advisory review misstatements and establishing rigorous negative boundaries for machine-checking tools.

---

## 4. Mapping Planned Real-Carrier Move to Missing Caller-Selected Target

In reverse engineering investigations, there is a recurring temptation to execute a "real-carrier move": running Ghidra or REA dynamic analysis on a real Go executable (such as `1password-cli` 2.40.0-2, `/usr/bin/docker`, or a freshly compiled Go binary) to observe whether Go RTTI analysis succeeds or fails.

This planned move maps directly to a **missing caller-selected target** and is contractually and technically inadmissible:

```
[Planned Real-Carrier Move]
            │
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Why it maps to a MISSING CALLER-SELECTED TARGET:                       │
│                                                                        │
│ 1. Historical 1Password Target Lacks Execution Artifacts:              │
│    The round-4 run on 1password-cli 2.40.0-2 deleted its transient      │
│    analyzer logs. The original binary is not caller-selected for        │
│    dynamic execution in round 15.                                      │
│                                                                        │
│ 2. Unsanctioned Target Substitution Violates REA Doctrine:             │
│    Selecting an arbitrary host binary (e.g. docker) or synthesizing a  │
│    toy Go ELF does not test the historical failure conditions. Target  │
│    selection in REA must be caller-driven, not agent-invented.         │
│                                                                        │
│ 3. Explicit Contractual Prohibition:                                   │
│    The round-15 contract strictly commands: "Skip all builds/tests/    │
│    linters/formatters/gate/smoke execution... No target/provider       │
│    execution or fabricated claims."                                    │
│                                                                        │
│ 4. Province Boundary Crossing:                                         │
│    Executing a target binary under a live provider would absorb dynamic│
│    RE responsibilities belonging to sibling provinces (revenger/host). │
└────────────────────────────────────────────────────────────────────────┘
```

When an assignment provides no caller-selected target and forbids provider execution, demanding or attempting a real-carrier run is a category mistake. The absence of a caller-selected target mandates an analytical pivot: rather than executing an ungrounded carrier, the lane must analyze the static substrate of the toolchain itself.

---

## 5. Justifying the Source-Inventory Route Without Claiming Replay

The **source-inventory route** replaces unauthorized, speculative target execution with verifiable static facts about the installed provider and its source code:

### 5.1 The Mechanical Discrimination Power of the Source-Inventory Route
By combining direct filesystem inspection of `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` with source analysis of S003 (`Base-src.zip`), the route cleanly discriminates three structural failure tiers without executing any binary:

1. **Tier 1: Advisory Version Range Check (`GoRttiMapper.java:170-176`):**
   - Out-of-range versions (e.g. Go 1.26) log `Untested Go version` and continue.
   - Proves definitively: the range check itself never halts analysis.
2. **Tier 2: Base Snapshot Lookup (`GoApiSnapshot.java:122-126`):**
   - Resolves `goVer.withPatch(0)`. If `go{baseVer}.0.json` is missing (e.g. `go1.26.0.json`), `getApiSnapshotJsonFile` returns `null` immediately.
   - `GoApiSnapshot.get()` returns `EMPTY` (`arches` is empty; `isInvalid()` is `true`).
   - `registerStructures` calls polymorphic `getType()`, which reaches `GoTypeManager.findTypeRec` (`GoTypeManager.java:449`), fails to find non-primitive types in `EMPTY`, and throws `IOException`.
   - `initStructMappings` (`GoRttiMapper.java:356-360`) catches `IOException`, sees `apiSnapshot.isInvalid() == true`, and throws `BootstrapInfoException("Missing Go bootstrap type info...")`.
   - Proves definitively: for Go 1.26, missing base JSON is a guaranteed fatal static barrier that stops RTTI bootstrap before moduledata or pclntab parsing can ever be reached!
3. **Tier 3: Patch-Diff Fallback & Architecture Filtering:**
   - For a nonzero patch whose diff is missing (e.g. Go 1.25.8, where base `go1.25.0.json` exists but no `go1.25.8.json.diff` exists), `getPatchVerDiffFile` walks backwards to patch 0, emits a warning, and **falls back to raw base JSON bytes** without failing (`GoApiSnapshot.java:128, 153-161`). Struct registration succeeds using base types!
   - For OS/architecture filtering: `archSearchOrder` contains `"all"`, and every installed base file contains `"all"`. Therefore, on the installed dataset, OS/arch filtering **never** results in `arches.isEmpty() == true`.

### 5.2 Why This Route Formally Refuses Replay
The source-inventory route establishes what the installed Ghidra 12.1.4 software is **structurally capable of resolving**, but explicitly refuses to assert historical target causality:

- **Unretained Execution Logs:** The transient analyzer logs from round 4 were deleted; whether the original run failed at snapshot loading, architecture matching, symbol filtering, or memory parsing remains permanently **UNKNOWN**.
- **Upstream Multi-Component Bundle (S004 Commit `385e8cd9`):** Upstream commit GP-6528 proves that supporting Go 1.26 required changing ten files: updating `SUPPORTED_VERSIONS`, adding `go1.26.0.json`, adding `go.module` section lookup in `GoModuledata.java`, bounding `textStart` in `GoPcHeader.java`, adding `group` field in `GoMapType.java`, updating `GoTypeFlag.java`, and adding magic checks in `GoBuildId.java`.
- **Precondition $\neq$ Cause:** Proving that an installed snapshot is a *necessary structural precondition* for Go 1.26 analysis does not prove that adding a snapshot would have repaired the historical run, nor that snapshot absence was the sole historical barrier.

By strictly bounding the claim to toolchain capability while classifying historical causality as UNKNOWN, the source-inventory route achieves high depth and calibration without fabricating replay evidence.

---

## 6. The Non-Obvious Move: Compatible Synthesis Across Proposals

### 6.1 The Synthesis: The "Necessary-Precondition Static Discrimination Protocol"
Scanning the round's proposals across executor, reviewer, and critic lanes (`SnapshotCensus`, `SnapshotEntry`, `BoundaryFixtures`, `ReviewPatchCases`, `ReviewManualRoute`, `SiblingBoundary`, `EvidenceChain`) reveals a striking structural symmetry between C1 and C2:

- In C1, agents are tempted to conflate snapshot absence with operational recovery, or demand dynamic execution of Go targets.
- In C2, agents are tempted to add format-detection heuristics to `quote-fidelity.py` (which would absorb `chousa`'s province and mutate frozen gate pins) or mischaracterize exit 1 as an evaluation refusal.

The non-obvious move synthesizes both claims into a unified **Necessary-Precondition Static Discrimination Protocol** across both axes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│              NECESSARY-PRECONDITION STATIC DISCRIMINATION PROTOCOL                      │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│           Claim C1 (Depth Axis)           │       Claim C2 (Calibration Axis)          │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ Necessary Precondition:                   │ Necessary Precondition:                    │
│ Presence of installed base JSON snapshot  │ Exact raw UTF-8 byte match in excerpt      │
│ (`go{major}.{minor}.0.json`).             │ body without markup transformations.       │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ Negative Exclusion Mechanism:             │ Negative Exclusion Mechanism:              │
│ Missing base snapshot yields `EMPTY`,     │ Rendered quotes evaluate under ordinary    │
│ triggering fatal `BootstrapInfoException` │ gate rules without format classification:  │
│ before layout parsing begins.             │ can return 0, 1, or 2 (not universally 1). │
│                                           │ C2 #17 voids manual-only machine results.  │
├───────────────────────────────────────────┼────────────────────────────────────────────┤
│ Non-Sufficiency / Contractual Refusal:    │ Non-Sufficiency / Contractual Refusal:     │
│ Snapshot presence is NOT sufficient for   │ Raw byte presence is NOT sufficient for    │
│ Go RTTI recovery (S004 proves moduledata/ │ semantic citation support; non-raw formats │
│ pcHeader bundle required). Historical     │ MUST NOT be submitted to machine grading   │
│ causality remains UNKNOWN.                │ (QUALITY #17 not-submitted policy).        │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

### 6.2 Contradictions Resolved by the Synthesis
1. **Contradiction in C1 Advisory Review (`ReviewGoInference.md:57-61`):**
   - *Past Misstatement:* `registerStructures` does not consult the snapshot; snapshot absence only changes wording.
   - *Resolution:* Tracing the virtual call edge (`DataTypeMapper.registerStructure` -> `GoRttiMapper.getType` -> `GoTypeManager.findTypeRec` -> `apiSnapshot.getTypeDef`) proves snapshot absence is an active computational cause of struct registration failure.
2. **Contradiction in C2 QUALITY Bar (`QUALITY.md:26`, Row 16):**
   - *Past Misstatement:* The local quote instrument "does not grade" markup-spanning quotations.
   - *Resolution:* Code trace and synthetic limitation fixtures (`BoundaryFixtures.md`) prove the instrument *does* evaluate them under ordinary substring rules: a rendered quote can return 0 (if raw bytes happen to match without tags), 1 (if raw substring is missing/misplaced), or 2 (if manifest/source is malformed/tampered). It lacks an input classifier, so exit 1 is not universal. QUALITY #17 resolves this by establishing an explicit standard that **voids any machine-checked result on manual-only inputs**. QUALITY #17 does not claim the policy physically prevents submissions; rather, it specifies that submitting manual-only inputs violates the quality contract and renders any machine verdict void.
3. **Contradiction in OS/Architecture Failure Hypothesis:**
   - *Past Hypothesis:* Round 14 suggested OS/arch filtering might have reached `isInvalid() == true` on installed snapshots.
   - *Resolution:* `ReviewPatchCases.md:70` observed that every installed base snapshot carries `"all"`, so `arches` is never empty for installed bases. This eliminates OS/arch filtering as a candidate cause of `Missing Go bootstrap type info` on present base files, isolating base snapshot absence as the sole static structural blocker.

---

## 7. Affected Axes, Second-Order Effects & Risks

### 7.1 Axis Impact
- **`depth` (Improved):** Grounded in reproducible filesystem census (11 base JSONs, 123 patch diffs, 0 in 1.26) and exact Java AST call tracing in S003, replacing vague version incompatibility assumptions with a deterministic 5-stage cascade.
- **`calibration` (Improved):** Completely eliminates speculative historical causality, corrects advisory review misstatements, accurately documents gate limits via synthetic boundary fixtures, and respects scorecard saturation without numeric inflation.
- **`coverage`, `operability`, `freshness`, `adjacency` (Unimpaired):** No unheld REA ground claimed; zero gate code mutations; zero encroachment on adjacent provinces (`chousa`, `tsukuroi`, `tameshi`, `revenger`).

### 7.2 Second-Order Risks and Mitigations

| Risk | Surface | Second-Order Consequence | Enforced Mitigation |
|---|---|---|---|
| **Coverage Proxy Drop** | `SCORECARD.md` / `corpus/README.md` | Adding `2026-10-20-r15-go-snapshot-inventory.md` without updating `corpus/README.md:11-69` causes coverage score to drop from 10.0 to 9.89 ($92/93$). | L1 must add the coverage map token to `corpus/README.md` in the work commit. |
| **Tool Tampering** | `.ufo/waves/round-14/tools/` | Modifying `quote-fidelity.py` to add format parsing breaks frozen pins (`expected.json`) and violates C2 contract. | Pin `quote-fidelity.py` SHA-256 (`0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`) and enforce empty git diff. |
| **Historical Causal Overclaim** | `corpus/knowledge/` | Claiming that missing `go1.26.0.json` explains the round-4 `1password-cli` failure. | Strictly label historical causality as `UNKNOWN` in the knowledge entry. |
| **Cross-Contamination of Tooling** | Verification Workflows | Submitting JSON inventory outputs or Java code snippets to `quote-fidelity.py`. | Formally enforce the bifurcated artifact contract: JSON verified via stdlib/Git; prose verified via quote gate. |

---

## 8. Proposed Verification Checks for L1 (Integrator)

In strict accordance with leaf bounds, this seat executed zero verification commands. Main agent (L1) should execute these exact checks during the final integration pass:

### Check 1: Tool and Fixture Immutability Check
Verify that round-14 tools, frozen expectations, and measure scripts are byte-unchanged:
```sh
sha256sum \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py
```
*Expected digests:*
- `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`
- `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf`
- `ee546111cb19e70eae63634f0795325465d58d3f3d0e098cbafc1fdb0c4dd2ab`

### Check 2: Existing Gate Regression & Selftest Verification
Verify that existing quote gate behavior remains completely green:
```sh
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --selftest
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --frozen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json
```
*Expected:* Selftest passes 28/28 CLEAN (exit 0); frozen regression passes 7 manifests with 0 findings (exit 0).

### Check 3: Boundary Limitation Fixture Demonstration
Verify the raw vs. rendered limitation behavior on the synthetic fixtures:
```sh
# Raw literal quote: must exit 0 (CLEAN)
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json

# Rendered quote spanning markup: must exit 1 (FAILED, quote_not_contiguous)
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json
```

### Check 4: Installed Go Snapshot Directory Census
Verify installed base JSON files and absence of Go 1.26:
```sh
# 11 base JSON files present (1.15 to 1.25)
ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go*.0.json | wc -l
# Confirm exactly 123 patch diffs across supported minor versions
ls -1 /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/*.diff | wc -l
# Confirm absence of go1.26 base JSON
test ! -f /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json
```
*Expected:* Counts equal 11 base JSON files and 123 patch diffs; test exits 0.

### Check 5: S003 Virtual Dispatch AST Anchor Verification
Confirm polymorphic `getType` override in S003 archive:
```sh
unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
  ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | grep -n "public <T extends DataType> T getType"
```
*Expected:* Confirms method declaration at line 379 delegating to `goTypes.findDataType(name)`.

### Check 6: Immutable Git Measurement of Delivered Commit
```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <after-commit-sha>
```
*Expected:* Reports presence of C1 knowledge entry (1), C1 snapshot inventory tool (1), C2 QUALITY row 17 with `must not be submitted` (1), and C2 virtual-dispatch correction marker (1); 93 mapped knowledge files with empty missing/dangling sets.

---

## 9. Addendum & Correction: Grounded Census and Gate Evaluation Semantics

This section incorporates authoritative feedback from `KaidokuR15` regarding census counts and quote gate evaluation semantics:

1. **Withdrawal of 114 Diff Count & Affirmation of 123 Grounded Count:**
   - The earlier citation of "114 patch diffs" is formally **withdrawn as unsupported**.
   - The actual grounded count of patch diff files under `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/` is **exactly 123**.
   - Grounded filename histogram across the 10 minor versions with diffs:
     - Go 1.15: 15 diffs (`go1.15.1` to `go1.15.15`)
     - Go 1.16: 15 diffs (`go1.16.1` to `go1.16.15`)
     - Go 1.17: 13 diffs (`go1.17.1` to `go1.17.13`)
     - Go 1.18: 10 diffs (`go1.18.1` to `go1.18.10`)
     - Go 1.19: 13 diffs (`go1.19.1` to `go1.19.13`)
     - Go 1.20: 14 diffs (`go1.20.1` to `go1.20.14`)
     - Go 1.21: 13 diffs (`go1.21.1` to `go1.21.13`)
     - Go 1.22: 12 diffs (`go1.22.1` to `go1.22.12`)
     - Go 1.23: 12 diffs (`go1.23.1` to `go1.23.12`)
     - Go 1.24: 6 diffs (`go1.24.1` to `go1.24.6`)
     - Sum: $15 + 15 + 13 + 10 + 13 + 14 + 13 + 12 + 12 + 6 = 123$ patch diff files.
     - Go 1.25: 0 diffs.
     - Go 1.26: 0 diffs.

2. **Ordinary Gate Evaluation Semantics for Rendered Input (Not Universally Exit 1):**
   - The gate script `quote-fidelity.py` possesses no substrate or input-class detector. It evaluates any submitted input under its standard, ordinary rules:
     - **Exit 0 (`CLEAN`):** Occurs if the submitted quote text happens to match raw UTF-8 bytes verbatim (for example, if a rendered sentence contained no markup tags or styling in that passage).
     - **Exit 1 (`FAILED`):** Occurs if the quote text is absent from raw bytes (`quote_not_contiguous`), misplaced outside section bounds (`quote_location_mismatch`), or exceeds 25 words (`quote_too_long`).
     - **Exit 2 (`CNE`):** Occurs if the manifest or source file is malformed or tampered (`invalid_manifest`, `source_tampered`, `snapshot_tampered`).
   - Therefore, a rendered input does not universally emit exit 1; it evaluates under the ordinary rules according to its raw bytes.

3. **Governance Nature of QUALITY #17 (Voiding Manual-Only Results):**
   - QUALITY #17 does **not** claim to physically or mechanically prevent submissions (the gate script contains no upload filter or input-blocking layer).
   - Instead, QUALITY #17 is a **normative quality standard** that explicitly:
     a) Directs all non-raw formats (rendered markup, code members, JSON, commit objects, command outputs) to manual-only source review under QUALITY #1.
     b) **Voids any machine-checked result on manual-only inputs**: an accidental or intentional exit 0 on a manual-only input has zero evidentiary authority.
     c) Forbids treating a machine green as evidence of rendered fidelity.
