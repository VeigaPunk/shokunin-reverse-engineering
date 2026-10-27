# R43ConnRouted — Routed-Defect Ledger and Synthesis for Round 43, Wave 1

VERDICT: **DONE** — with 1 unassigned conformance defect flagged (`R42-V2`).

The round-43 routed-defect ledger into wave 1 is complete: `R42-CL1..CL3`, `R42-V1..V5`, and carried-open items `R40-CL2`, `R36-CL5`, `R40-CL7`, and `round-40 D2` are fully mapped against base commit `6b9e64fe7e0de202d9383baad5792fbfe039a743`. Each defect has its current state at the base recorded, its round-43 home identified (wave-1 seat, L1, wave 2, or open with reason), and the empirical observable that demonstrates it fixed. Defect `R42-V2` has no covering wave-1 seat in `w1-spec.json` and is explicitly flagged for L1 closure ownership.

---

## 1. UFO-FSD Connector Synthesis

### Evidence
1. **R43-C2 Path Contradiction**: `plans/round-43-claims.md` (:96-97, :103, :147) strictly binds `corpus/evidence/round-43/local-sources/` and dictates that `corpus/evidence/local-sources.json` bind each out-of-lane path to a copy under `round-43`. However, the prepared landing pack produced by `R43C2Land` (`.ufo/waves/round-43/w1/artifacts/R43C2Land/pack/`) staged files under `corpus/evidence/round-42/local-sources/` and emitted a `local-sources.json` where all 18 mapped entries point to `round-42`.
2. **Pre-File Gate Scope & Blind Spot**: In round 42, `tools/round-42/prefile-gate.py` condition (b) required `git status --porcelain` to be clean under `.ufo/waves/round-N/`, `corpus/evidence/round-N/`, `plans/`, and `tools/round-N/` (where `N=42`). For round 43 (`N=43`), if copies are committed under `corpus/evidence/round-42/local-sources/`, condition (b) will not sweep them, creating an unmonitored residue surface.
3. **Uncommitted Gate Run (R42-V2)**: Round-42 verifier spot-check defect D2 / `R42-V2` caught that "Pre-file gate GATE GREEN at af50af81" was claimed in the report without committed output (`git ls-tree` at `6b9e64fe` shows zero gate receipts for round 42). In round 43 wave 1, no seat in `w1-spec.json` is assigned to author `tools/round-43/prefile-gate.py` or commit its execution log.
4. **SOURCES Schema Strictness**: Seat `R43SrcLicense` confirmed that `scripts/sources-census.sh validate` rejects `kind: license` (exit 1, error E05), requiring `kind: docs`.

### Affected Axes
- **Coverage**: Directly affected by R43-C2. Moving 18 host-local SOURCES rows to resolvable in-lane copies improves coverage only if the landing map and files match Predicate P43-C2's path contract (`corpus/evidence/round-43/local-sources/`).
- **Depth**: Re-scoring the frozen v4 SquashFS triage table on fresh held-out carriers under QUALITY-85 refusal (R43-C1) must not be corrupted by path or tooling collisions.
- **Calibration**: Harms none; maintains honest reporting of gate outputs and exact revision receipts.

### Proposed Move
**Synthesize C2 path canonicalization with an L1 pre-file gate commit protocol:**
1. **L1 Landing Path Alignment**: At landing time, the L1 renames `R43C2Land`'s staged directory from `corpus/evidence/round-42/local-sources/` to `corpus/evidence/round-43/local-sources/` and rewrites all path strings in `corpus/evidence/local-sources.json` accordingly before committing.
2. **L1 Gate Execution Protocol (Discharging R42-V2)**: The L1 invokes `python3 -I -B tools/round-42/prefile-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 43 --json` after wave 2 settles, writes the output to `.ufo/waves/round-43/l1/prefile-gate.json`, and commits this file in the report-filing commit. This simultaneously discharges `R42-V2`, verifies `corpus/evidence/round-43/` under condition (b), and proves pre-file gate compliance.

### Risks
- **Path Substitution Inconsistency**: If `local-sources.json` is edited but a copy filename on disk does not match, `local-source-gate.py` will exit 1 with reason `missing-copy`. *Mitigation*: Run `local-source-gate.py --json` immediately after path transformation.
- **Premature Gate Invocation**: Invoking `prefile-gate.py` before wave 2 results are written will fail condition (a). *Mitigation*: The L1 must run the prefile gate strictly after all waves settle.

### Verification
- `python3 -I -B tools/round-41/local-source-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --json` exits 0 with `rows_failed: []` and `rows_total >= 129`.
- `python3 -I -B tools/round-42/prefile-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --round 43 --json` exits 0, and `.ufo/waves/round-43/l1/prefile-gate.json` is committed in git HEAD.

---

## 2. Routed-Defect Ledger (One Table)

Base revision: `6b9e64fe7e0de202d9383baad5792fbfe039a743` (lane `main`).

| id | origin | current state at base `6b9e64fe` | round-43 home (wave-1 seat, L1, wave 2, or open — reason) | observable that shows it fixed |
|---|---|---|---|---|
| **R42-CL1** | `corpus/lessons/round-42.md` `## Routed defects into round 43`; mistake M42-2: generator predicted tuple without measuring; combo C02 declared `{extractor-failure, unpublished-entry}` while REA observed `{depth-limited, extractor-failure, unpublished-entry}` | unfixed in frozen tools — `tools/round-42/heldout-gen-v4.py` predicts declared tuple from factors; C02 in round-42 held-out set lacks `depth-limited`; stop receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` binds `observed_features_match_declared=false`, exit 1 | **R43C1Gen**, **R43MutGen**, **R43LabTuple**, **R43RevRevenger**, **R43C1Controls** (wave 1); **the L1 itself** (post-freeze data run) | `heldout-gen-v4r43.py` exits 3 (`declared_tuple_unobserved`) on tuple mismatch and writes no manifest (CTL-C1-2 red receipt); round-43 held-out manifest records `generator.tuple_check` all equal; `tools/round-43/c1-counter.py` binding `observed_features_match_declared` is `true`, exit 0 |
| **R42-CL2** | `corpus/lessons/round-42.md` `## Routed defects into round 43`: no wave 2 attacked the round-42 landing (mirrors round-42 verifier spot-check §1 D1 and §5 R42-V1) | open from round 42 — round 42 concluded with only wave 1 (43 seats), below run-9 floor of 64; no wave 2 falsification wave was dispatched | **wave 2** (falsification wave attacking R43-C1 and R43-C2 landings; rerun of round-42 C1 counter against fresh carrier cache); managed by **the L1 itself**; wave-1 preparation by `R43Mistake` and `plans/round-43-claims.md:17-18` | `.ufo/waves/round-43/r43-w2-results.json` committed with settling reports; wave 2 reports include adversarial falsification attacks on C1/C2 landings; total round seats across w1 and w2 ≥ 64 |
| **R42-CL3** | `corpus/lessons/round-42.md` `## Routed defects into round 43`; carries R41-CL3: 18 host-local SOURCES rows resolvable with in-lane copies prepared by `R42LocalSrc` but never landed in lane | unfixed at base — `tools/round-41/local-source-gate.py` at `6b9e64fe` exits 1 with 18 failed rows (S001, S002, S003, S006, S007, S023, S035, S040, S048, S056, S066, S070, S079, S081, S082, S083, S090, S092); only S126 resolved | **R43C2Land**, **R43C2Pin**, **R43RevLocalsrc**, **R43CritC2** (wave 1); **the L1 itself** (commits landing under `corpus/evidence/round-43/local-sources/` and `corpus/evidence/local-sources.json`) | `python3 -I -B tools/round-41/local-source-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>` exits 0 with `rows_failed []` and `rows_total >= 129` |
| **R42-V1** | `corpus/lessons/round-42-verifier-spotcheck.md` §1 D1 and §5 R42-V1: round total 43 < run-9 floor 64; no wave 2 attacked the C1 landing (mirrors R42-CL2) | carried from round-42 non-author closure | **wave 2** (and **the L1 itself** for sizing wave 2 with ≥ 32 seats so total seats across round-43 ≥ 64) | `.ufo/waves/round-43/r43-w2-results.json` committed; total seats in round-43 ≥ 64; wave 2 reports include falsification runs against C1/C2 landings |
| **R42-V2** | `corpus/lessons/round-42-verifier-spotcheck.md` §1 D2 and §5 R42-V2: pre-file gate GREEN at `af50af81` asserted without committed output in git tree | unfixed in tree — no committed gate run output for `af50af81` exists in git history (`git ls-tree 6b9e64fe` yields 0 run receipts) | **the L1 itself** [FLAG: NO WAVE-1 ITEM COVERS IT] (filing responsibility: L1 must run prefile-gate and commit receipt before filing) | committed file `.ufo/waves/round-43/l1/prefile-gate.log` (or `.json`) at measured tip revision showing exit 0, command line, timestamp, and conditions (a)-(d) passing |
| **R42-V3** | `corpus/lessons/round-42-verifier-spotcheck.md` §5 R42-V3: `SKILL.md` rule blocks 20 and 21 carry no in-SKILL claim status, while block 20 reads "Superseded" and both claims stopped | unfixed at base — `SKILL.md:438` (block 20) and `SKILL.md:521` (block 21) have no claim status marker or stop notice | **R43SkillMark** (authors status sentence diffs), **R43ScoutTable** (verifies placement outside frozen table byte region); landed by **the L1 itself** | `SKILL.md` block 20 carries explicit status line (v3 stopped, superseded by v4) and block 21 carries explicit status line (matched evaluator 78/78, R42-C2 stopped on `observed_features_match_declared`, re-scored under P43-C1); table bytes between `<!-- sqfs-triage-table v4 -->` and markdown table end remain byte-identical to `d1681696` |
| **R42-V4** | `corpus/lessons/round-42-verifier-spotcheck.md` §5 R42-V4: generator declares tuples it did not observe; combo C02 (mirrors R42-CL1 / QUALITY 85) | unfixed in frozen tools at base | **R43C1Gen**, **R43MutGen**, **R43LabTuple**, **R43C1Controls**, **R43RevRevenger** (wave 1); **the L1 itself** (post-freeze data run) | `heldout-gen-v4r43.py` refuses to emit manifest if declared != observed (exit 3); fresh held-out set manifests declare observed tuple including `depth-limited`; `observed_features_match_declared` evaluates `true` in `tools/round-43/c1-counter.py` |
| **R42-V5** | `corpus/lessons/round-42-verifier-spotcheck.md` §5 R42-V5: `2026-10-26-r42-squashfs-v3-core.md` opens with `status:` before provenance trio `source:`/`verified-at:`/`recheck:`, violating CORPUS §Additional corpus rules | present at base — `2026-10-26-r42-squashfs-v3-core.md` line 3 has `status:` before `source:` at line 5 | **R43RevEntry** (verifies schema ordering), **R43ScribeEntry** (drafts `2026-10-27-r43-sqfs-triage-v4-scored.md` with correct order), **R43ScribeAssim** (drafts `2026-10-27-sasquatch-release-matrix.md` with correct order); landed by **the L1 itself** | all newly committed `corpus/knowledge/2026-10-27-*.md` files have `source:`, `verified-at:`, `recheck:` occurring before `status:` in front matter (verified by `grep -n`) |
| **R40-CL2** | `corpus/lessons/round-40.md` `## Routed defects`: rerun binding proves carrier consistency through pinned toolchain, not receipt provenance; oracle-only fabrication passes (carried in r41, r42) | open (disclosed limit) — inherent limitation of carrier rerun binding; disclosed in round-41, round-42, and round-43 claims | **open — reason: inherent provenance limit** (disclosed in `plans/round-43-claims.md` `## R43-C1 Disclosed limits`; defended by CTL-C1-2 and `R43C1Counter` / `R43SentProv`, but cannot be closed without cryptographic provenance infrastructure) | disclosed in `plans/round-43-claims.md` and round-43 report; CTL-C1 controls verify fabricated/relabeled manifests are rejected (exit non-zero) |
| **R36-CL5** | `corpus/lessons/round-36-verifier-spotcheck.md:209-210`: campaign instruments fail QUALITY rows 33, 39, 45, 58, 60, 68 (carried in r38–r42) | open — instruments lack machine-readable pin map (Q33), per-call `package.json`-sha logging (Q39), row IDs named in claims (Q45), predicates read directly from claims file (Q68) | **open — reason: out of round-43 claim scope** (round-43 claims focus on R43-C1 depth and R43-C2 coverage; none of the 32 wave-1 seats binds QUALITY 33/39/45/58/60/68 into counter predicates) | machine-readable `instruments` map in claims file, per-call sha logged in receipts, and counter dynamically parsing predicate clauses from `plans/round-N-claims.md` |
| **R40-CL7** | `corpus/lessons/round-40.md`: vendor terms purport to forbid analysis; round publishes derived metadata only | open (operator) — operator directed RE training on public firmware; lane publishes derived metadata only | **open — reason: operator-owned policy** (hygiene maintained by `R43SentProv` licence sweep) | no third-party image bytes committed in lane; carrier rows cite URL + sha256 + rebuild command only |
| **round-40 D2** | `corpus/lessons/round-40.md`: seven AVM vendor texts remain reachable in git history at `7fce3086` | open (operator) — history not rewritten | **open — reason: operator-owned policy** (no lane history rewrite) | operator ruling / historical branch retirement |

---

## 3. Flags: Defects With No Wave-1 Item Covering Them

1. **`R42-V2` (Pre-file gate output uncommitted at closure)**:
   - **Finding**: None of the 32 wave-1 seats in `w1-spec.json` is assigned to author or execute `prefile-gate.py` for round 43 or commit its run receipt.
   - **Remedy**: This defect belongs to **the L1 itself** as a strict pre-filing gate requirement. The L1 must run `tools/round-42/prefile-gate.py --round 43` and commit `.ufo/waves/round-43/l1/prefile-gate.json` before filing the round report.
2. **`R40-CL2` (Carrier consistency vs receipt provenance)**:
   - **Finding**: Inherent limit of re-execution architectures without cryptographic tracing; disclosed in claims and bounded by negative controls (CTL-C1-1, CTL-C1-2). Marked `open — reason: inherent provenance limit`.
3. **`R36-CL5` (Instrument QUALITY bar: rows 33, 39, 45, 58, 60, 68)**:
   - **Finding**: Out of scope for round 43's two declared claims (R43-C1 depth, R43-C2 coverage). Marked `open — reason: out of round-43 claim scope`.
4. **`R40-CL7` & `round-40 D2` (Vendor analysis terms and historical AVM blobs)**:
   - **Finding**: Operator-owned governance questions outside lane scope. Fences maintained by `R43SentProv`. Marked `open — reason: operator-owned policy`.

---

## 4. Evidence (Exact Commands, Outputs, Exit Codes)

### A. Local Source Gate at Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`
```bash
python3 -I -B tools/round-41/local-source-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 6b9e64fe7e0de202d9383baad5792fbfe039a743 --json
```
- **Exit Code**: `1`
- **Output JSON excerpt**:
  ```json
  {
    "exit": 1,
    "map": "corpus/evidence/local-sources.json",
    "map_present": true,
    "rows_checked": 19,
    "rows_failed": [
      "S001", "S002", "S003", "S006", "S007", "S023", "S035", "S040",
      "S048", "S056", "S066", "S070", "S079", "S081", "S082", "S083",
      "S090", "S092"
    ],
    "rows_total": 134
  }
  ```
- Corroborates base state for **R42-CL3**.

### B. SKILL.md Status Markers at Base `6b9e64fe`
```bash
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 6b9e64fe7e0de202d9383baad5792fbfe039a743:SKILL.md | grep -n -C 3 "sqfs-triage-table v[34]"
```
- Line 438: `<!-- sqfs-triage-table v3 -->` (no status sentence before marker or after table).
- Line 521: `<!-- sqfs-triage-table v4 -->` (no claim status or R42-C2 stop explanation).
- Corroborates base state for **R42-V3**.

### C. Knowledge Entry Front-Matter at Base `6b9e64fe`
```bash
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 6b9e64fe7e0de202d9383baad5792fbfe039a743:corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md | head -n 8
```
- Line 3: `status: R42-C1 — scored by tools/round-42/c1-counter.py ...`
- Line 5: `source: S112 ...`
- Line 6: `source: S116 ...`
- `status:` precedes provenance trio, violating CORPUS rules. Corroborates base state for **R42-V5**.

### D. Audit of Staged C2 Pack vs Round-43 Plan Contract
- Staged pack in `.ufo/waves/round-43/w1/artifacts/R43C2Land/pack/corpus/evidence/local-sources.json` contains:
  ```json
  "copy": "corpus/evidence/round-42/local-sources/S001/SKILL.md"
  ```
- Target in `plans/round-43-claims.md:103` states:
  `corpus/evidence/round-43/local-sources/`
- Audit file generated: `artifacts/R43ConnRouted/c2-path-audit.txt`.

---

## 5. Seat Hygiene & Tooling Record

- **Tooling authorization (operator, 2026-10-19)**: No tools installed or upgraded. Zero pacman calls, zero pip/npx/cargo operations.
- **VCS Mutation**: Zero git or jj mutations executed in lane or fleet repository. All inspections performed via read-only git queries and python stdlib scripts.
- **Scratch Directory**: Scratch created at `/fast/scratch/hyaku/kaidoku-r43/w1-R43ConnRouted` and cleaned up upon task completion.
- **Committed Artifacts**:
  - `.ufo/waves/round-43/w1/artifacts/R43ConnRouted/ledger.json`: Structured JSON ledger of all defects.
  - `.ufo/waves/round-43/w1/artifacts/R43ConnRouted/base-checks.json`: Machine-readable results of base state audits.
  - `.ufo/waves/round-43/w1/artifacts/R43ConnRouted/c2-path-audit.txt`: Textual breakdown of C2 path discrepancy and remediation steps.
