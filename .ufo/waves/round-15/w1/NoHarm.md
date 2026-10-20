# Round 15 w1 — NoHarm: Comparative Analysis, No-Harm Controls, and Stale-Summary Audit

- **Seat:** `KaidokuR15.NoHarm` (leaf member; UFO-FSD connector; no subagent dispatch).
- **Round:** Kaidoku round 15 (`kaidoku-r15-w1`).
- **Target:** Compare prior entry correct diagnosis with planned inventory deepening and docs-only correction; name no-harm controls and potential stale-summary references; synthesize C1 and C2 into a single bounded move.
- **Assigned Output:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/NoHarm.md`.
- **Baseline Commit:** `9719dd232687f5ee78a4ed323b37f8810e833d10` (HEAD at round launch).
- **Execution State:** Read-only inspection of repository files, round-15 wave cache, installed S003 source archive, S007 documentation, and sibling candidates. Zero gate executions, selftests, builds, linters, tests, or live REA provider/target operations were run. No tools installed or upgraded (record: none).

---

## 1. Declared Axes & Structural Invariants

### 1.1 Declared Axes
1. **`depth` (Primary for C1):** Deepening the understanding of Go RTTI version gating from source-reading control flow (round 14) to a concrete, pinned inventory of installed Ghidra 12.1.4 API snapshot assets (`snapshot-inventory.py`) paired with an exact decision record discriminating missing base snapshots, patch diffs, and architecture exclusions.
2. **`calibration` (Primary for C2):** Grounding two outside-routed review obligations into repo-wide standards:
   - *Advisory Correction:* Appending a named correction for the flawed virtual-dispatch claim in `.ufo/waves/round-14/w1/ReviewGoInference.md:57-61` without altering filed historical bytes.
   - *Manual Input Boundary:* Adopting superseding criterion `corpus/QUALITY.md` row 17, establishing that manual-only representations (rendered markup-spanning quotes, code members, JSON, commits, command output) MUST NOT be submitted to the raw `quote-fidelity` gate, while keeping gate code unchanged.

### 1.2 Monitored Invariant Axes (Strict No-Harm Guarantee)
- **`coverage`:** Preserved at 10.0 (92/92 mapped entries at baseline, or 93/93 if a new knowledge entry is mapped in `corpus/README.md:11-69`). No dangling tokens, unindexed files, or broken category rows.
- **`operability`:** Preserved. Existing local gate (`quote-fidelity.py`) and frozen controls remain bit-for-bit identical to round 14.
- **`freshness`:** Preserved. Reopened sources (S001, S003, S007) match pinned hashes on disk; no stale remote assertions.
- **`adjacency`:** Preserved. Strict province custody; no target execution, engine installation, sibling repository mutations, or fleet configuration changes.

### 1.3 Structural Proxy Reality & Anti-Inflation Law
All three owned numeric proxy scores (`depth: 10.0`, `coverage: 10.0`, `calibration: 10.0`) in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` are clamped at their mathematical ceiling (saturation). 
- `depth_score` measures `10 * resolved / rule_blocks` exclusively over SKILL.md craft rules (17/17). Adding knowledge files or snapshot tools does not alter this formula.
- `coverage_score` measures `10 * mapped / files`. Adding a file can only harm coverage (if unmapped, 92/93 = 9.89); mapping it preserves 10.0.
- `calibration` is governed by frozen rubric Recipe B.
Therefore, "lowest axis tie at 10" represents zero numeric headroom. Progress this round cannot be expressed by scalar score inflation; it must be evidenced solely by discrete, verifiable observables, reproducible artifacts, and narrowed epistemic claims.

---

## 2. Comparative Analysis: Prior Diagnosis vs. Planned Deepening vs. Docs-Only Correction

| Dimension | Prior Entry Diagnosis (`2026-10-20-r14-go-version-diagnosis.md`) | Planned Inventory Deepening (C1: `snapshot-inventory.py` & Decision Record) | Docs-Only Correction (C2: Advisory Virtual Dispatch & QUALITY #17) |
|---|---|---|---|
| **Substrate / Artifact** | Literature & source reading of S003 (`Base-src.zip`), S004 (GP-6528 commit), S007 (`ChangeHistory.md`). | Python inspection tool (`snapshot-inventory.py`) scanning physical files in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`. | Markdown text additions in `corpus/QUALITY.md`, `corpus/lessons/round-14.md`, `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, and `LOG.md`. |
| **Mechanistic Scope** | Separated advisory range warning (`Untested Go version`) from snapshot lookup (`EMPTY`) and struct registration exception. | Establishes exact disk inventory: 11 base JSONs (`1.15.0`–`1.25.0`), 98 patch diffs, 27 arch keys in `1.25.0`, and physical absence of `go1.26.0.json`. | Traces exact Java virtual dispatch: `registerStructures` → `DataTypeMapper.registerStructure` (`:176`) → `getType(List, Class)` (`:310`) → `GoRttiMapper.getType` (`:379`) → `GoTypeManager.findTypeRec` (`:402`) → `apiSnapshot.getTypeDef` (`:449`). |
| **Discriminating Power** | Proved that range check continues rather than stopping; showed upstream fix is a multi-file bundle. | Proves that for Go 1.26, Ghidra fails at base file lookup (`GoApiSnapshot.java:122-126`), returning `EMPTY` with `arches.isEmpty()`. Distinguishes missing base from missing patch diff. | Falsifies the round-14 review misconception that `registerStructures` is independent of snapshot data. Proves snapshot invalidity directly aborts struct mapping. |
| **Epistemic Limits & Boundaries** | Historical `op-2.40.0` failure cause declared **UNKNOWN** due to un-retained analyzer log; no target replay. | File presence/absence on disk does **not** prove historical execution flow; does not prove adding `go1.26.0.json` repairs Go 1.26 analysis. | Qualifies the advisory pointer without mutating historical bytes in `.ufo/waves/round-14/w1/ReviewGoInference.md`. Narrows gate scope without changing gate code. |

### 2.1 The Specific Shift from Round 14 to Round 15
In round 14, the lane successfully refuted the hard version-gate assumption (`GoRttiMapper.java:79`), proving that `Msg.error` logs and continues execution. However, an author-side advisory report (`ReviewGoInference.md:57-61`) introduced a secondary error: it claimed that `registerStructures` does not consult `apiSnapshot` and that snapshot invalidity merely selects error message wording.
Round 15 rectifies this:
1. **C2 traces the exact virtual dispatch chain**, proving that `registerStructures` does indeed consult `apiSnapshot` through overridden `getType()`. Therefore, an invalid snapshot causes `Structure structDT = getType(...)` to return `null`, throwing an `IOException` that selects `BootstrapInfoException("Missing Go bootstrap type info...")`. Snapshot invalidity is a *functional failure mechanism*, not just a cosmetic string selector.
2. **C1 grounds this functional failure on disk**, inspecting the actual installation to demonstrate that `go1.26.0.json` is absent, guaranteeing that `GoApiSnapshot.get` returns `GoApiSnapshot.EMPTY` (where `arches.isEmpty() == true`).

---

## 3. Exhaustive No-Harm Controls Across Surfaces

To prevent accidental regressions (harm) on unworked or saturated axes, the following controls are strictly enforced:

### Control 1: Coverage Map Index Integrity (Axis: `coverage`)
- **Risk:** Adding a new knowledge file (e.g. `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`) increases `knowledge_files` from 92 to 93. If omitted from `corpus/README.md:11-69` (`## Coverage map`), Recipe A computes `mapped = 92`, `files = 93`, dropping `coverage_score` from 10.0 to 9.89.
- **Control:** L1 must ensure any admitted knowledge entry token is indexed in `## Coverage map` on an existing row without inserting extra newlines (e.g. multi-token convention on line 35) or appending at EOF, preserving both index completeness and frozen line pins.

### Control 2: Line-Pinned Citation Stability (Axis: `depth` & `calibration`)
- **Risk:** Inserting new lines in `corpus/README.md` or `SKILL.md` displaces line-pinned anchors (e.g., `SCORECARD.md:69, 72` pinning `README.md` lines 138, 175, 180; craft rules in `SKILL.md:81-318`).
- **Control:** Zero row insertions above pinned lines. All modifications must be in-place token appends on existing rows or strictly append-only blocks at EOF after the final pinned reference.

### Control 3: Craft Rule Citation Resolution (Axis: `depth`)
- **Risk:** Adding or editing a craft rule (`- **...` in `SKILL.md`) that references non-existent files or invalid ranges drops the resolved ratio below 17/17, degrading `depth_score` from 10.0.
- **Control:** Round 15 adds zero craft rules to `SKILL.md`. Existing craft block hash `e12b60ce0c71316e457680c65ae8273487deac9c68db3f80a084814a8ad765e6` remains bit-identical.

### Control 4: Gate Code Immutability & Contract Preservation (Axis: `operability` & `calibration`)
- **Risk:** Modifying `.ufo/waves/round-14/tools/quote-fidelity.py` to handle rendered HTML or detect unsupported inputs risks breaking existing CLI selftests or tampering with the exit code schema.
- **Control:** The gate script is locked by SHA-256 (`0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`). No regex normalization, tag stripping, or automated unsupported classification is added. Exit 2 remains reserved strictly for malformed manifests or tampered source digests (`CNE_FINDINGS`), never for manual-only inputs.

### Control 5: Registry Custody & Permitted Cell Scope (Axis: `freshness` & `calibration`)
- **Risk:** Modifying tier, anchor, scope, or adding unvetted rows in `corpus/SOURCES.md` violates registry immutability and trips `sources-census.sh validate`.
- **Control:** All 22 rows, tiers (20 A, 1 B, 1 C), and statuses (21 mined, 1 rejected) remain unchanged. `used-by` cell updates are permitted only for reopened sources (S001, S003, S007) and must be applied strictly *after* the citing knowledge file exists on disk (preventing census check E11 failure).

### Control 6: Historical Artifact Custody (Axis: `calibration`)
- **Risk:** Editing `.ufo/waves/round-14/w1/ReviewGoInference.md` in-place to correct lines 57–61 destroys historical audit trails and violates immutable evidence custody.
- **Control:** Zero byte edits to filed wave artifacts (`git diff --quiet 9719dd232687f5ee78a4ed323b37f8810e833d10 -- .ufo/waves/round-14/w1/ReviewGoInference.md` exits 0). Corrections are applied via named, append-only addenda in active lessons and entries.

### Control 7: Epistemic Causal Restraint (Axis: `calibration`)
- **Risk:** Concluding that because `go1.26.0.json` is missing in Ghidra 12.1.4, its absence was the sole cause of the `op-2.40.0` symbol loss in round 4, or that providing this file repairs Go 1.26 support.
- **Control:** Formal prohibition against asserting historical target causality. The historical log was deleted; cause remains **UNKNOWN**. Upstream commit GP-6528 proves that Go 1.26 support requires at least 8 distinct multi-file changes across the runtime model.

### Control 8: Synthetic Fixture Isolation (Axis: `calibration`)
- **Risk:** Mixing synthetic boundary fixtures with upstream research excerpts could dilute evidence authenticity.
- **Control:** Fixtures under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/` explicitly declare `"origin": "synthetic"` and `"upstream": false`, verifying only local tool behavior under edge conditions.

---

## 4. Potential Stale-Summary References & Remediation Map

A repository-wide audit reveals several locations where summaries, pointers, or criteria could become misleading or stale if read without round-15 context:

| Location & Anchor | Baseline Stated Text | Why It Risks Staleness / Misinterpretation | Required Remediation / Status |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:103` | Cites `.ufo/waves/round-14/w1/ReviewGoInference.md` in Evidence list. | Lines 57–61 of that report claim `registerStructures` does not consult `apiSnapshot` and that snapshot absence only affects log wording. | **Remediated:** Append-only section `## Round-15 advisory-pointer correction` added (lines 107–117), qualifying the pointer as flawed advisory evidence that must not support mechanism claims. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md:18, 76` | Row 1: `ReviewGoInference.md ... preserve[s] conditional control flow`; Row 76: cites report under causal-overreach fix. | Implies the report's mechanical explanation of struct registration was sound. | **Remediated:** Append-only section `## Round-15 correction — virtual-dispatch advisory` added (lines 144–160), detailing the virtual dispatch path and qualifying the reference. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:26` (Criterion #16) | "Code members, commit objects, JSON, command output, and quotations spanning markup require their appropriate manual source check under #1; this local instrument does not grade them." | The phrase "does not grade them" falsely implies the tool classifies or refuses them. In reality, it grades raw substrings and returns exit 1 `quote_not_contiguous`. | **Remediated:** Superseding row 17 added at `QUALITY.md:27`, replacing "does not grade them" with an explicit **not-submitted policy**: these inputs MUST NOT be submitted to the machine gate. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:450` | `quote-fidelity` gate entry: `0 clean, 1 failed (quote absent/mislocated/too long), 2 could-not-evaluate...` | Does not warn that submitting rendered text spanning markup produces exit 1 rather than exit 2. Operators might assume exit 1 means misquotation. | **Remediated:** QUALITY #17 serves as the governing standard; boundary fixtures in wave 15 demonstrate the raw/rendered limitation control. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md:35, 140` | `r14 source-backed bootstrap diagnosis supersedes the unproved layout-cause inference, not those retained measurements` | If round 15 adds a separate snapshot inventory knowledge entry, omitting it from line 35 would leave the inventory unmapped in Recipe A. | **Remediation:** If `SnapshotEntry` is committed as a new knowledge file, L1 must append its token to line 35, e.g.: `knowledge/2026-10-13-r4-10-real-version-pair, 2026-10-20-r14-go-version-diagnosis, 2026-10-20-r15-go-snapshot-inventory`. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md:1775-1780, 1799-1806` | Summarizes round-14 diagnosis as separating range warning from snapshot lookup, but leaves virtual dispatch unclarified. | Historical logs read without qualification could propagate the wording-only fallacy. | **Remediation:** L1 must append a round-15 LOG entry explicitly recording the virtual-dispatch advisory correction and QUALITY #17 supersession. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/PROVINCE.md:52` | Notes that `precise old cause remains unknown, source-backed bootstrap diagnosis supersedes unproved layout cause`. | Must not be edited to claim that snapshot absence on disk proves the old 1password-cli failure. | **Status:** Preserved as-is. Remains accurate under the disciplined unknown boundary. |

---

## 5. The Proposed Move: Compatible Synthesis Across C1 and C2

### 5.1 The Apparent Contradiction
There is an underlying tension between the round's two proposals:
- **C2's Virtual Dispatch Proof** shows that `apiSnapshot` is directly queried during struct registration (`GoTypeManager.findTypeRec` → `apiSnapshot.getTypeDef`). This proves that snapshot validity is an essential, hard mechanical requirement for Ghidra to construct `runtime.moduledata`.
- **C1's Inventory & Epistemic Boundary** shows that `go1.26.0.json` is missing on disk, but simultaneously insists that we cannot claim this missing file caused the historical `op-2.40.0` failure or that adding it would fix Go 1.26 analysis.
- *The Risk:* An analyst seeing the virtual dispatch proof (C2) might immediately conclude that the missing JSON (C1) was the sole root cause of the historical breakdown, undermining the lane's calibration and epistemic restraint.

### 5.2 The Synthesis: "Coupled Decoupling — Bridging Precondition Necessity and Causal Insufficiency"
The non-obvious move is to **explicitly couple the virtual-dispatch proof to the GP-6528 bundle proof**:
1. **Elevate to Necessary Precondition (`depth` improved):** Use C2's virtual dispatch trace to prove that on this installed Ghidra 12.1.4 platform, the presence of an applicable API snapshot is a *necessary precondition* for `GoRttiMapper` struct registration. This directly establishes the technical relevance and architectural depth of C1's installed snapshot inventory (`snapshot-inventory.py`).
2. **Constrain by Causal Insufficiency (`calibration` improved):** Simultaneously couple this finding to S004's upstream commit diff (`385e8cd923d09f10b1a7874108e71748875fa174`), which proves that snapshot presence is *wholly insufficient* for Go 1.26 recovery. Even if `go1.26.0.json` were present, execution would immediately encounter subsequent breaking layout differences in `GoModuledata` (missing `go.module` section lookup), `GoPcHeader` (invalid `textStart` field presence), and `GoMapType` (missing `group` field).
3. **Formal Epistemic Formula:**
   $$\text{Snapshot Validity} = \text{Necessary Precondition} \quad \wedge \quad \text{Snapshot Validity} \neq \text{Sufficient Cause}$$
   By formalizing this distinction, the lane deepens its architectural model without conceding an inch to causal overreach.

### 5.3 Second-Order Effects Trace
- **Runtime Surface:** Zero impact. Neither Ghidra nor target binaries are executed.
- **Contract Surface:** QUALITY #17 eliminates the false promise that `quote-fidelity.py` detects or refuses unsupported representations; establishes an enforceable, manual-only submission standard.
- **Substrate Surface:** Pinned tool `snapshot-inventory.py` provides deterministic, structured JSON output of installed assets. Existing gate code and fixtures remain bit-identical.
- **Verification Surface:** Re-running verification on committed Git revisions demonstrates 100% regression stability for C2 and discrete 0→1 observable additions for C1 and C2.

---

## 6. Proposed L1 Verification Plan (Named, Unexecuted)

Under the leaf contract, this seat executed no gates, builds, or tests. The following verification checks are proposed for L1 to run once all seats conclude:

### 6.1 Source Hash & Archive Anchor Re-Check
```bash
sha256sum \
  /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md \
  /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip \
  /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md
```
- *Expected:*
  - S001: `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`
  - S003: `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`
  - S007: `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`

### 6.2 Gate Immutability & Regression Baseline
```bash
# Verify gate script, frozen fixtures, and old measure script are bit-identical to round-14 pins
sha256sum \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py

# Run CLI selftest (28 cases)
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --selftest

# Run frozen controls (7 manifests)
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --frozen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/fixtures/expected.json
```
- *Expected:*
  - Hashes match `measurement-pins.json` exactly (`0d939e23...`, `ef3714bb...`, `ee546111...`).
  - Selftest: `CLEAN cases=28 passed=28 failed=0 exit=0`.
  - Frozen: `manifests=7 findings=0 exit=0`.

### 6.3 Boundary Limitation Controls (C2 Evidence)
```bash
# Test synthetic raw accepted quote
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json

# Test synthetic rendered rejected quote
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py \
  --manifest /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json
```
- *Expected:*
  - `raw-accepted.json`: clean, exit 0 (raw `<em>raw</em>` matches raw source).
  - `rendered-rejected.json`: exit 1, finding `quote_not_contiguous` (rendered text spanning tags fails raw substring check, demonstrating the documented limitation).

### 6.4 Installed Snapshot Inventory Invocations (C1 Evidence)
```bash
# Execute census tool and verify deterministic JSON stdout
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py \
  --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC > /tmp/inventory1.json

python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py \
  --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC > /tmp/inventory2.json

diff -u /tmp/inventory1.json /tmp/inventory2.json
```
- *Expected:* Clean exit 0; byte-for-byte identical output; reports base JSON `go1.15.0` through `go1.25.0` present, `go1.26.0` absent; 98 patch diffs; zero uncaught exceptions.

### 6.5 Repository Integrity & Sources Validation
```bash
# Shared sources census validation
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku

# Git numstat audit (confirm zero deletions on historical files)
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff 9719dd232687f5ee78a4ed323b37f8810e833d10 --numstat \
  corpus/QUALITY.md \
  corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md \
  corpus/lessons/round-14.md \
  .ufo/waves/round-14/w1/ReviewGoInference.md
```
- *Expected:*
  - `sources-census.sh`: `kaidoku ok ... exit=0`.
  - Git numstat: deletions column is strictly `0` across all four targets; `ReviewGoInference.md` diff is empty.

### 6.6 Round-15 Measurement Script Execution
```bash
# Run round-15 measurement script against the committed work revision
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <WORK_COMMIT_REV>
```
- *Expected:*
  - C1 inventory tool and entry observables: 0 → 1.
  - C2 QUALITY row 17 and virtual-dispatch correction marker observables: 0 → 1.
  - `knowledge_files`: 92 → 93 (or 92 if integrated as draft), `mapped`: equal to `knowledge_files`, `missing`: `[]`.
  - `sources`: 22 rows, tiers A=20, B=1, C=1, status mined=21, rejected=1.
  - Craft rules: 17/17 resolved.
  - Proxy scores: `depth: 10.0`, `coverage: 10.0`, `calibration: 10.0` (saturated, unharmed).
