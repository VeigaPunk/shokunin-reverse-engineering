# Province Adjacent Boundaries, Scope Risk & Non-Obvious Move Synthesis — Round 15

- **Lane:** `kaidoku-shokunin`
- **Seat:** `KaidokuR15.SiblingBoundary` (connector, leaf member)
- **Repo Root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Date:** 2026-10-20
- **Target:** Scan province adjacent boundaries and proposed claims; no source-target run, config/engine work, or chousa admission method absorbed. Identify scope risk.
- **Declared Round Axes:** `depth` (Claim C1), `calibration` (Claim C2).
- **Lowest Axis:** Three owned proxies tie at 10.0; calibration worked; no numeric inflation.
- **Status:** Scoped analysis complete. One non-obvious move synthesized. No verification executed (reserved for L1).

---

## 1. Province Adjacent Boundaries & Fleet Interface Scan

The fleet architecture under `/home/vgpnk/Projects/shokunin` strictly delineates domain ownership and requires out-of-province concerns to be reported, never absorbed (`PROVINCE.md:95-117`). A comprehensive review of `kaidoku-shokunin`'s own boundaries alongside adjacent sibling provinces reveals key ownership invariants for round 15:

| Province / Surface | Declared Ownership & Core Domain | Out-of-Province Boundary Relative to `kaidoku` Round 15 | Scope Crossing Risk & Refusal Invariant |
|---|---|---|---|
| `chousa-shokunin` (`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md:3-9`) | Owns deep-research method (調査), source hierarchy, citation chaining, claim-vs-source verification via `tools/research-gate.sh`. Refuses RE. | `kaidoku`'s C2 local gate (`quote-fidelity.py`) is strictly a local UTF-8 raw-substring and heading regression instrument on captured Markdown excerpts. | **Do NOT absorb chousa's admission method.** Must NOT add HTML/AST stripping, entity decoding, multi-hop citation parsing, or general web claim verification into `quote-fidelity.py`. Existing gate raw behavior must remain unmutated. |
| `tameshi-shokunin` (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:3-18`) | Owns reusable verification-fixture craft, mutation testing, fail-closed arms, verdict-line discipline. Explicitly refuses product domains ("every lane's gate remains its own"). | `kaidoku` owns its internal isolated `--selftest` and frozen regression fixtures (`.ufo/waves/round-14/fixtures/`). | **Do NOT export or generalize local gates.** `quote-fidelity.py` and `snapshot-inventory.py` must remain internal to `kaidoku`. Do not attempt to define fleet-wide fixture frameworks or general mutation suites. |
| `tsukuroi-shokunin` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:8-14,25-28,51`) | Owns host operability & system repair (繕): pacman state, systemd units, drivers/firmware health. Refuses binary RE (defers to `kaidoku`/`revenger`). | `kaidoku` reads installed Ghidra 12.1.4 files read-only. Operating system package state and engine installations belong to the host/operator. | **Do NOT modify installed engine or package files.** Must NOT attempt to install Go packages, add missing `go1.26.0.json` into Ghidra's system tree, edit `GoRttiMapper.java` in place, or alter system configs. Substrate remains immutable. |
| `revenger-shokunin` (`/home/vgpnk/Projects/shokunin/revenger-shokunin/PROVINCE.md:3-7,19-25`) | Owns reverse engineering of shipped artifacts under evidence-ledger discipline. Refuses harness auditing and target execution beyond declared target lifecycle. | `kaidoku` owns Linux ELF via the Ghidra 12.1.4 provider on this host. Historical target runs (e.g. `op` 2.34.1 vs 2.40.0) lack retained logs. | **Do NOT claim historical target replay or carrier runs.** C1 must strictly remain a static installed snapshot inventory and source-decision record. No carrier execution is authorized or performed this round. |
| `protocol` / aggregator (`scripts/sources-census.sh`) | Governs fleet tabular source registry standards (11-column header, enum validity, disk existence of `used-by` paths). | `kaidoku` maintains its own `corpus/SOURCES.md` rows. No new rows may be opened in round 15 without L1 authorization. | **Do NOT rewrite immutable registry fields.** Only permitted `used-by` updates for reopened S003/S007 are allowed; no source tier reclassification. |
| `kaidoku` Internal Adjacent Limits (`PROVINCE.md:95-117`) | Refuses malware triage at scale, non-REA dynamic analysis, repository reconstruction, and engine/client configuration installs (operator-owned). | All work in round 15 is static inspection of installed files and code archives. | **Do NOT run target processes or engine setups.** Provider configuration keys (`GHIDRA_INSTALL_DIR`, `JAVA_HOME`) and MCP server registrations remain read-only. |

---

## 2. Proposed Claims & Concrete Local Evidence

Round 15 proposes two specific claims in `.ufo/waves/round-15/claims.json`:
- **Claim C1 (`depth`):** "A pinned installed Go JSON snapshot inventory and source-selection decision record discriminate missing base, patch-diff, and OS/architecture applicability without asserting historical target causality. Before no round15 inventory/decision record; after one reproducible inventory plus sourced knowledge."
- **Claim C2 (`calibration`):** "Resolve both round14 outside-routed defects: append named virtual-dispatch advisory correction and superseding QUALITY criterion explicitly requiring manual-only rendered/code/JSON inputs not be submitted to raw quote machine grading. Existing gate raw behavior retained and exercised as a documented limit, not a new gate capability."

### A. Grounded Evidence for C1 (Installed Provider State & Source Control Flow)

1. **Installed Ghidra 12.1.4 Snapshot Directory Layout:**
   - Physical location: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`
   - Observed Base JSON Files: Exactly 11 files (`go1.15.0.json`, `go1.16.0.json`, `go1.17.0.json`, `go1.18.0.json`, `go1.19.0.json`, `go1.20.0.json`, `go1.21.0.json`, `go1.22.0.json`, `go1.23.0.json`, `go1.24.0.json`, `go1.25.0.json`).
   - Legacy GDT Files: 9 files (`golang_1.15_anybit_any.gdt` through `golang_1.23_anybit_any.gdt`).
   - Subdirectory `patchverdiffs/`: Contains exactly 123 `.diff` patch files (from `go1.15.1.json.diff` to `go1.24.6.json.diff`; no Go 1.25 diffs exist).
   - **Crucial Negative Finding:** There is **zero** `go1.26*` file anywhere in installed Ghidra 12.1.4 (neither `go1.26.0.json` base file nor any patch diff under `patchverdiffs/`).

2. **Source Control Flow in S003 (`Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`):**
   - `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:125-132`:
     ```java
     GoVer baseVer = goVer.withPatch(0);
     File jsonFile = getApiSnapshotFile(baseVer, "", "");
     if (jsonFile == null) {
         return null;
     }
     ```
     When evaluating a Go 1.26.x target, `baseVer` resolves to `1.26.0`. Because `go1.26.0.json` is missing, `jsonFile` is `null`, and `getApiSnapshotJsonFile` immediately returns `null` without scanning `patchverdiffs/`.
   - `GoApiSnapshot.java:115`: When `getApiSnapshotJsonFile` returns `null`, `get()` returns `GoApiSnapshot.EMPTY`.
   - `GoApiSnapshot.java:503-505`:
     ```java
     public boolean isInvalid() {
         return arches.isEmpty();
     }
     ```
     `GoApiSnapshot.EMPTY` has an empty `arches` map, so `isInvalid()` evaluates to `true`.
   - `GoRttiMapper.java:353-365`:
     ```java
     try {
         registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);
     }
     catch (IOException e) {
         if (apiSnapshot.isInvalid()) {
             throw new BootstrapInfoException(
                 "Missing Go bootstrap type info, unable to extract Go RTTI info."
                     .formatted(goVer));
         }
         throw new IOException("Invalid Go bootstrap struct mapping info: %s".formatted(goVer), e);
     }
     ```
   - **Virtual Dispatch Anchor (Routed Defect 1 Resolution):**
     During `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this)`, `DataTypeMapper.registerStructure` (`DataTypeMapper.java:172-176`, `:310-313`) invokes `getType(name, clazz)` on `this`. In `GoRttiMapper.java:379-382`:
     ```java
     @Override
     public <T extends DataType> T getType(String name, Class<T> clazz) {
         DataType result = goTypes.findDataType(name); ...
     }
     ```
     `GoTypeManager.findDataType` calls `findTypeRec(typeName)` at `GoTypeManager.java:443-451`, which queries `apiSnapshot.getTypeDef(typeName)`. Because `apiSnapshot` is `EMPTY`, non-primitive type lookup fails, triggering the `IOException` caught in `initStructMappings`. This proves that `registerStructures` *does* consult the snapshot via polymorphic virtual dispatch, falsifying the flawed statement in round 14's advisory review (`ReviewGoInference.md:57-61`).

### B. Grounded Evidence for C2 (Routed Defect 2 & Quote Gate Behavior)

1. **Existing Gate Behavior (`.ufo/waves/round-14/tools/quote-fidelity.py`):**
   - The gate implements raw UTF-8 substring searching (`grade_quote` lines 250-258) against section bodies discovered by regex `^(#{1,6})[ \t]+(.+?)[ \t]*\Z` (line 75).
   - If a quote text contains rendered characters that differ from raw markup bytes (e.g. `Use raw bytes.` vs `Use <em>raw</em> bytes.`), `quote in text` fails.
   - Lines 97-100: Only `invalid_manifest`, `source_tampered`, and `snapshot_tampered` emit exit 2. A quote absence emits `quote_not_contiguous`, which produces exit 1 (FAILURE).
   - The tool contains **zero** input-classification logic, zero HTML parsing, and zero AST stripping.
2. **Boundary Fixture Evidence (`.ufo/waves/round-15/boundary-fixtures/`):**
   - `raw-source.md` (SHA-256 `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270`):
     ```text
     ## Intro

     Use <em>raw</em> bytes.
     ```
   - `raw-accepted.json` (SHA-256 `95c995035ebf539e4e3cce3410a8e52461f5f7c88d5b58563381f0cd19cd4537`): Submits raw quote `Use <em>raw</em> bytes.` → expected exit 0 (clean; `[INFERENCE from static code reading, unexecuted]`).
   - `rendered-rejected.json` (SHA-256 `bc97c4699bfcc06d5f6197d63592982f5a9ee245dd787c06ba6ca336746399e3`): Submits rendered quote `Use raw bytes.` → expected exit 1 (`quote_not_contiguous@rendered-text`; `[INFERENCE from static code reading, unexecuted]`).
   - Static analysis of the gate path shows that submitting rendered markup to the gate causes an exit 1 rejection, confirming that the tool *does* grade the input (contrary to QUALITY #16's phrasing "does not grade them") and that the defect must be resolved by a **not-submitted policy** (QUALITY #17), not an automatic unsupported classification branch.

---

## 3. Scope Risks Across Surfaces

Scanning the interface between round 15's proposed deliverables and fleet boundaries identifies five concrete scope risks:

1. **Risk of Absorbing `chousa` Admission Method into `quote-fidelity.py`:**
   - *Risk:* Attempting to make `quote-fidelity.py` "smart" by adding HTML tag-stripping, entity normalization, or AST traversal to accept rendered quotes.
   - *Second-Order Effect:* Mutating `quote-fidelity.py` would violate the C2 contract ("no quote gate implementation change"), absorb `chousa-shokunin`'s research method, and blur the boundary between raw byte verification and semantic citation parsing.
   - *Mitigation:* Retain the existing raw gate as an immutable fixture; resolve routed defect 2 purely through documentation policy (superseding QUALITY #17 explicitly forbidding submission of rendered/code/JSON inputs).

2. **Risk of Target Execution or Provider Replay (Crossing into `revenger` / Dynamic RE):**
   - *Risk:* Running headless Ghidra or `rea analyze` on a Go binary (`op`, `1password-cli`, or synthetic ELF) to test the snapshot selection logic or attempt to "reproduce" the historical r4-10 failure.
   - *Second-Order Effect:* Violates the strict contract ("no source-target run"), overclaims capability without a caller-selected target, and falsely asserts historical causality where logs were lost.
   - *Mitigation:* Confine C1 strictly to static filesystem inventory of installed JSON snapshots and source control-flow reading from S003 archive. Explicitly document historical causality as UNKNOWN.

3. **Risk of Substrate Modification (Crossing into `tsukuroi` / Operator Domain):**
   - *Risk:* Writing files into `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/` (such as importing upstream `go1.26.0.json`) or modifying `GoRttiMapper.java` to bypass the `1.15-1.25` range.
   - *Second-Order Effect:* Corrupts the host's installed baseline, breaks digest pins of installed files, and crosses into operator-owned engine maintenance.
   - *Mitigation:* `snapshot-inventory.py` must only perform read-only traversal (`os.scandir` or `pathlib.Path.iterdir`) of the installed directory; zero writes outside `.ufo/waves/round-15/`.

4. **Risk of Reusable Verification Craft Overreach (Crossing into `tameshi`):**
   - *Risk:* Promoting `quote-fidelity.py` or `snapshot-inventory.py` as a generalized fleet test framework.
   - *Second-Order Effect:* Violates `tameshi-shokunin`'s province rule requiring two independent lanes before a verification pattern is generalized.
   - *Mitigation:* Keep both scripts hermetically sealed inside `kaidoku-shokunin/.ufo/waves/` with local-only scope.

5. **Risk of Domain Expansion Overclaiming / Score Inflation (Violating Calibration):**
   - *Risk:* Claiming that inventorying installed Go JSON files expands REA domain coverage into Go 1.26.
   - *Second-Order Effect:* Violates SCORECARD contract and round-14 verifier spotcheck ("expansion: unchanged — same held Go ground; a file count or local bookkeeping instrument is not new REA domain ground").
   - *Mitigation:* Credit C1 strictly as `depth` on held ground; keep `expansion` and `coverage` unchanged. Lowest-axis proxies remain tied at 10.0 without numeric inflation.

---

## 4. Connector Synthesis: One Bounded Non-Obvious Move

### The Proposed Move
**Hermetic Artifact-Type Partitioning Contract between Structural Snapshot Censuses and Raw Prose Excerpts**

Synthesize Claim C1's installed snapshot inventory and Claim C2's manual-only gate boundary by formally establishing a **bifurcated artifact-type verification contract**:

1. **Structural Metadata Census Partition (Governing C1):**
   - The output of `snapshot-inventory.py` (JSON metadata, snapshot filenames, base counts, and patch-diff listings) belongs strictly to the **structural census domain**.
   - Verification of C1 claims is governed by immutable Git/filesystem census (exact file existence, JSON schema validation, and SHA-256 digest matching) and manual source-anchor review (#1, #8).
   - **Contractual Refusal:** Structured JSON files, diff files, and tool outputs must **never** be submitted to `quote-fidelity.py`. Attempting to machine-grade JSON or code through the quote gate is formally classified as an *invalid gate invocation* (operator misuse), not a gate bug.
2. **Raw Literature Excerpt Partition (Governing C2):**
   - `quote-fidelity.py` is permanently locked to **heading-structured Markdown/HTML prose excerpts** under `.ufo/waves/` fixtures.
   - Superseding QUALITY #17 codifies a **not-submitted policy**: code members, commit objects, JSON, command outputs, and markup-spanning quotations require manual source checking under #1 and **must not be submitted** to raw quote machine grading.
   - The gate's raw UTF-8 behavior is preserved without adding an artificial "unsupported" exit-2 branch, and the boundary is demonstrated by synthetic limitation fixtures (`raw-accepted.json` exiting 0, `rendered-rejected.json` exiting 1).
3. **Adjacent Province Shielding:**
   - *Versus `chousa`:* Refuses automated citation chaining or markup parsing; keeps local quotation matching strictly dumb.
   - *Versus `tsukuroi` / Host:* Operates strictly read-only on installed typeinfo data.
   - *Versus `revenger` / REA targets:* Replaces dangerous carrier-replay temptations with safe, static structural inventory.

### Second-Order Effects & Explicit Contradictions

- **Contradiction Identified:**
  - In round 14, QUALITY #16 stated that the quote instrument "does not grade" markup-spanning quotations, code, and JSON. However, code inspection of `quote-fidelity.py` reveals that the tool *does* grade them: it computes raw UTF-8 substring containment and emits `quote_not_contiguous` (exit 1) when rendered text or formatted code diverges from raw file bytes.
  - Furthermore, S003 `Base-src.zip` is a zip archive containing Java source files, and installed snapshots are JSON files. If C1 attempted to use C2's gate to verify quotes from `GoRttiMapper.java` or `go1.25.0.json`, the gate would either fail on missing headings or fail on whitespace/syntax differences.
- **Resolution via Synthesis:**
  - The bifurcated partitioning contract directly resolves this contradiction without changing gate code.
  - By replacing "does not grade them" with an explicit **not-submitted prohibition** in QUALITY #17, the lane accurately describes gate behavior: the gate emits exit 0 or 1 on raw bytes; it lacks input-type classification; therefore, structured and rendered inputs must not be submitted to it.
  - C1's JSON inventory and Java source findings are validated via structural and manual checks (QUALITY #1), while C2's gate is restricted to raw Markdown prose, eliminating cross-contamination.

### Affected Axes

- **`depth` (Improved):**
  - Grounds C1 in reproducible, verified filesystem facts (11 base JSONs, 114 patch diffs, 0 in 1.26) and source control-flow reading (`GoApiSnapshot.java:125-132`, `GoRttiMapper.java:353-375`, `GoTypeManager.java:443-451`), cleanly discriminating missing base from patch diff and OS/architecture exclusion without relying on quotation gates.
- **`calibration` (Improved):**
  - Resolves routed defect 1 by correcting the virtual-dispatch mechanism in advisory documentation while qualifying the flawed pointer.
  - Resolves routed defect 2 by eliminating inaccurate "does not grade" claims and establishing an explicit not-submitted boundary supported by synthetic limitation controls (`BoundaryFixtures.md`), without score inflation or gate mutation.
- **No Harm to Other Axes:**
  - `coverage`: Unchanged (preserves held Go ground without claiming unheld Go 1.26 execution).
  - `operability`: Preserved (existing gate behavior and frozen fixtures remain 100% stable; new inventory script uses only Python stdlib).
  - `freshness`: Unchanged (anchors to installed Ghidra 12.1.4 and current registry).
  - `adjacency`: Preserved (zero encroachment on `chousa`, `tameshi`, `tsukuroi`, or `revenger`).

### Risks and Mitigations

| Risk | Severity | Mitigation in Round 15 |
|---|---|---|
| Inadvertent submission of `snapshot-inventory.py` JSON output to `quote-fidelity.py` | High | Codify the not-submitted prohibition in QUALITY #17; ensure L1 verification script runs inventory and quote checks in separate, isolated steps. |
| Confusion between installed JSON absence and historical target failure causality | High | Reiterate in C1 knowledge entry that historical 1Password failure cause is UNKNOWN; label snapshot selection as a source-supported diagnostic route, not historical proof. |
| Inadvertent edits to installed Ghidra typeinfo files | Critical | `snapshot-inventory.py` must use read-only file handles; enforce through L1 git status and filesystem permission checks. |
| Accidental gate modification | High | Pin `quote-fidelity.py` SHA-256 (`0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`) in measurement pins. |

---

## 5. Verification Recipe for Main Agent (L1)

The following checks must be executed by L1 once all seats finish. This seat has executed none of them:

1. **Verify No Substrate or Host Mutation (Git Worktree Cleanliness):**
   ```sh
   git -C /home/vgpnk/Projects/shokunin status --porcelain
   git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain
   ```
   *Expected:* No modified files in fleet root, sibling repos, or outside `.ufo/waves/round-15/` and assigned candidate paths.

2. **Verify Tool Immutability (Quote Gate Unchanged):**
   ```sh
   sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py
   ```
   *Expected:* Exactly `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`.

3. **Verify Existing Quote Gate Selftest & Frozen Regression:**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --selftest
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --frozen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json
   ```
   *Expected:* Selftest passes 28/28 with exit 0; frozen runs pass 7/7 with exit 0.

4. **Verify Boundary Limitation Fixtures (Demonstrating Raw vs Rendered Boundary):**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json
   # Expected: Exit 0, zero findings
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json
   # Expected: Exit 1, finding quote_not_contiguous@rendered-text
   ```

5. **Verify Installed Snapshot Inventory Tool Execution (Read-Only Census):**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py
   ```
   *Expected:* Exit 0; emits JSON with 11 base versions (1.15 to 1.25), 123 patch diffs (ending at `go1.24.6.json.diff`), and explicit absence of 1.26.

6. **Verify Immutable Git Measurement:**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py HEAD
   ```
   *Expected:* Exit 0; accurately registers presence of C1 knowledge entry, C1 inventory tool, C2 QUALITY row 17 with `must not be submitted` wording, and C2 lesson correction marker.

7. **Verify Shared Sources Census:**
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
   ```
   *Expected:* Exit 0 (`kaidoku ok .../corpus/SOURCES.md`).

---

## 6. Sources Opened & Exact Anchors

Every source below was opened and read on **2026-10-20**. Quotations are contiguous substrings $\le 25$ words:

1. **`chousa-shokunin/PROVINCE.md:3-8`**
   - *Quote:* “question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy;”
   - *Limit:* Governs deep-research method across fleet; establishes that general citation chaining belongs to `chousa`, not `kaidoku`.

2. **`tameshi-shokunin/PROVINCE.md:14-17`**
   - *Quote:* “Refuses: product domains — every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general).”
   - *Limit:* Confirms local gate code belongs to `kaidoku` and must not be exported or generalized without cross-lane evidence.

3. **`tsukuroi-shokunin/PROVINCE.md:25-28`**
   - *Quote:* “Refuses: endpoint/model serving health (→ kama), secrets (→ kagi), binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks state and health, not internals).”
   - *Limit:* Confirms host package health belongs to `tsukuroi` and binary RE belongs to `kaidoku`/`revenger`; prohibits `kaidoku` from modifying system packages.

4. **`kaidoku-shokunin/PROVINCE.md:108-113`**
   - *Quote:* “Installing engines, Python packages, or editing client configs — rea setup runs, registration refreshes ... all operator-owned. The lane documents the gap and the exact env key; it never runs the installer.”
   - *Limit:* Binds `kaidoku` to read-only observation of installed tools and providers; forbids modifying Ghidra's installed tree.

5. **`corpus/lessons/round-14-verifier-spotcheck.md:172-174`**
   - *Quote:* “Clarify that these inputs must not be submitted as machine-gradeable, or align the documented exit behavior and add an appropriate control.”
   - *Limit:* Official closure ruling defining routed defect 2 requirements.

6. **`Ghidra Base-src.zip:GoApiSnapshot.java:125-128`**
   - *Quote:* “GoVer baseVer = goVer.withPatch(0);\n\t\tFile jsonFile = getApiSnapshotFile(baseVer, "", "");\n\t\tif (jsonFile == null) {\n\t\t\treturn null;\n\t\t}”
   - *Limit:* Source observation of base file lookup; proves missing base version aborts snapshot loading before diff evaluation.

---

## 7. Tooling Directive Record

- **Tools installed or updated:** None. Standard system utilities and read-only Python 3 stdlib inspection tools were used exclusively.

---

## 8. Explicit Correction — Installed Patch Census & Unexecuted Gate Derivation

1. **Correction of Installed Patch Diff Census:**
   - *Erratum in initial draft:* Stated 114 `.diff` files extending up to `go1.25.7.json.diff`.
   - *Corrected fact (per `PatchLookup`, `ReviewPatchCases`, and L1 inventory):* The installed directory `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/` contains **exactly 123 `.diff` files**, covering Go 1.15 through 1.24 only:
     - Go 1.15: 15 diffs (`go1.15.1.json.diff` – `go1.15.15.json.diff`)
     - Go 1.16: 15 diffs (`go1.16.1.json.diff` – `go1.16.15.json.diff`)
     - Go 1.17: 13 diffs (`go1.17.1.json.diff` – `go1.17.13.json.diff`)
     - Go 1.18: 10 diffs (`go1.18.1.json.diff` – `go1.18.10.json.diff`)
     - Go 1.19: 13 diffs (`go1.19.1.json.diff` – `go1.19.13.json.diff`)
     - Go 1.20: 14 diffs (`go1.20.1.json.diff` – `go1.20.14.json.diff`)
     - Go 1.21: 13 diffs (`go1.21.1.json.diff` – `go1.21.13.json.diff`)
     - Go 1.22: 12 diffs (`go1.22.1.json.diff` – `go1.22.12.json.diff`)
     - Go 1.23: 12 diffs (`go1.23.1.json.diff` – `go1.23.12.json.diff`)
     - Go 1.24: 6 diffs (`go1.24.1.json.diff` – `go1.24.6.json.diff`)
     - Go 1.25: **0 diffs** (only base snapshot `go1.25.0.json` exists; zero patch diffs).
   - The patch diff sequence terminates at `go1.24.6.json.diff`. There are zero 1.25 diff names.

2. **Explicit Labeling of Unexecuted Gate Derivations:**
   - Exit codes for `raw-accepted.json` (exit 0) and `rendered-rejected.json` (exit 1 `quote_not_contiguous`) are strictly **`[INFERENCE from static code reading]`** derived from `quote-fidelity.py:250-258`.
   - Neither manifest was executed by this seat. In strict conformance with the leaf assignment contract, all test, build, lint, gate, and carrier executions are omitted and reserved exclusively for L1.
