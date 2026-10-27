# R43ConnSib — Sibling-Overlap Scan & Connector Synthesis (Pre-Freeze Recon)

**Verdict: DONE** — Sibling-overlap scan complete across all 20 sibling lanes and 10 round-43 fleet reports. Zero claim collisions exist with round-43 declared claims. One substantive sibling holds ground on the same toolchain (`revenger-shokunin`, REA + unblob + firmware province label), with an established and arbitrated boundary. Sibling defect patterns from `tsukuroi`, `kengaku`, and `kake` directly illuminate blind spots in the round-43 draft. One non-obvious connector move is synthesized to calibrate substrate attribution, unify landing paths, and secure census validity across C1 and C2.

---

## 1. Scope and Method

- **Lanes Scanned (read-only)**: All 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kaidoku-shokunin` itself).
- **Files Inspected**: `PROVINCE.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/` (specifically the last 3–5 rounds of each lane), `tools/`, and `plans/`.
- **Target Sweeps**:
  1. `SquashFS triage tables` / `sqfs-triage` / `indep-eval` / `interpreter` patterns.
  2. `generator-declared-vs-observed` defect class / `declared_features` / refusal checks (especially `kumitate`, `tsukuroi`, `kengaku`, `kake`).
  3. `SOURCES` local-source resolution / in-lane copy maps / `local-source-gate.py` (all lanes).
  4. `REA held-out regen with seed=freeze` (especially `kengaku`, `revenger`).
  5. Fleet repo `.ufo/reports/round-43/*.md` for all 10 sibling reports filed this round.
- **Rules Followed**: No git mutations, no writes outside the seat report and artifact directory, scratch bound to `/fast/scratch/hyaku/kaidoku-r43/w1-R43ConnSib` and cleaned up.

---

## 2. Sibling Overlaps Found

| Lane | Path:Line | What | Contested? |
|---|---|---|---|
| `revenger-shokunin` | `PROVINCE.md:3-6` | Core owns "reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, **firmware**, browser/Electron runtime evidence — using the REA skill and its toolset" | Province label shared ("firmware") |
| `revenger-shokunin` | `corpus/README.md:47` (C07 row) | Firmware images held **only** as manual byte-derived readout of one authored fixture (`fixtures/firmware-r63/firmware-r63.bin`); explicit disclaimer "no general firmware-format, **extraction/execution**, provider-completeness or authenticity claim" | No — deliberately narrower than kaidoku R43-C1 |
| `revenger-shokunin` | `corpus/README.md:75-78` | REA `inspect_firmware_regions` / `extract_firmware` need caller-supplied Binwalk 3.1.x and Unblob 26.6.x (host has binwalk 3.1.0, unblob 26.6.4, sasquatch 4.5.1) | No — shared toolchain engine inventory |
| `revenger-shokunin` | `SKILL.md:431-442` | Firmware oracle: authored bytes vs saved REA record | No — authored fixture testing only |
| `revenger-shokunin` | `corpus/lessons/round-70.md:98-106` | Staged unadopted unblob SOURCES rows S054/S099/S152 quarantined; renumber map ready | Collision risk if kaidoku stages unblob documentation rows (kaidoku S135 is the raw MIT LICENSE file, not a doc row) |
| `tsukuroi-shokunin` | `PROVINCE.md:50-51` (ADJ-06) | "Driver/firmware/package mechanism requires shipped-artifact RE beyond health inventory ... protocol integrator — **kaidoku/revenger ownership unresolved**" | **Recorded open arbitration** |
| `tsukuroi-shokunin` | `PROVINCE.md:149-152` (OUT-009) | "Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff" | **Recorded open arbitration** |
| `tsukuroi-shokunin` | `corpus/lessons/round-40.md:77` | `R40-HOSTCELL-UNANCHORED`: host cell stated `/tmp` is a tmpfs from memory, while live state was xfs on `/dev/nvme1n1p1`; repeated `R39-HOSTCELL-INFERRED-AS-SEEN` | Method defect pattern: unanchored host-fact statements |
| `tsukuroi-shokunin` | `corpus/lessons/round-43.md:124-127` | `R42-VERDICT-FORM`: C2 counter binding counted one declared form but unanchored parser admitted padded or contradictory fields | Method defect pattern: counter token parsing must be anchored |
| `kengaku-shokunin` | `corpus/lessons/round-42.md:11` | Mistake M1: "A declared direction copied from a table instead of re-derived from the run — XO5 and XO6 are rc-mirror ... near-variant table labels both rc-silence" | Method defect pattern: declared properties copied from static expectation rather than observed from live run (direct peer of R42-CL1 / M42-2) |
| `kengaku-shokunin` | `corpus/lessons/round-46.md:18` | Mistake M2: "A ## Predictor presented as the grader's exact rule that diverges on lone CR ... generator never built a lone-CR state" | Method defect pattern: generator blind spot where declared predictor diverges on untested states |
| `kengaku-shokunin` | `plans/round45_c2_verify.py:23,432` | State generator seeded with `Random(45)` over 16 kinds, 48 states | Method pattern: seed-based test state generation (uses stdlib random, not REA or freeze-hash seed) |
| `kake-shokunin` | `.ufo/waves/round-43/w1/CtlPrefixCache.md:44-55` | Generator `cut = rng.randint(36, 44)` capped shared prefixes at 44 cp; blind to >= 45 cp | Method defect pattern: generator ceilings create blind spots |
| `kake-shokunin` | `.ufo/waves/round-43/w1/CtlHeadTail.md:22-25` | "No generated value carries a long port and a defect... every long-port value is built from a clean base" | Method defect pattern: combinatorial generators building from clean bases miss cross-feature interactions (direct peer of combo C02 missing `depth-limited`) |
| `kama-shokunin` | `tools/round43-registry-audit.py:14-32` | Audits `SKILL.md` instrument registry tables using regex matching | Table-reading tool checks presence of registry rows; does not interpret decision tables into executable actions |

### Negative Search Results (Definitive Across All Sibling Lanes)
1. **SquashFS Triage Tables**: ZERO sibling lanes hold SquashFS triage tables. The table `<!-- sqfs-triage-table v4 -->` is unique to `kaidoku-shokunin/SKILL.md:522`.
2. **SOURCES Local-Source Resolution / In-Lane Copy Maps**: ZERO sibling lanes use `local-sources.json` or `local-source-gate.py`. Sibling lanes cite public HTTP(S) URLs or lane-relative repository paths, avoiding host-local absolute paths.
3. **REA Held-Out Generation with `seed=freeze`**: ZERO sibling lanes run REA held-out generation seeded by a freeze commit hash. Kengaku's domain is LLM benchmark evaluation (bwrap, Python, pytest), not REA. Revenger uses REA but has no held-out generator. This pattern is unique to `kaidoku-shokunin`.
4. **Executable Markdown Decision-Table Interpreter (v4-interpreter-pattern)**: ZERO sibling lanes execute domain triage directly from markdown decision tables via an interpreter like `tools/round-42/sqfs-triage-v4.py`. Sibling tools that read markdown files only perform regex schema checks on registry rows.

---

## 3. Contested Scope & Adjacency

### A. The "Firmware" Province Label (revenger vs kaidoku)
- **Status**: Tsukuroi's `PROVINCE.md` (`ADJ-06` line 50 and `OUT-009` line 149) records an open, unresolved arbitration between `kaidoku` and `revenger` regarding shipped-artifact reverse engineering of firmware mechanisms.
- **Empirical Ground Division**:
  - `revenger-shokunin` owns static binary analysis of native/managed/APK/Electron artifacts using REA. Its firmware capability (`corpus/README.md:47`, C07) is restricted to manual byte readouts of one authored fixture (`fixtures/firmware-r63/firmware-r63.bin`), with an explicit disclaimer excluding general firmware extraction, formats, and execution.
  - `kaidoku-shokunin` owns firmware format unpacking, multi-version SquashFS recursion (v1–v4, LE/BE/AVM layout), and executable outcome triage of REA `extract-firmware` runs.
- **Adjacency Requirement**: In `kaidoku-shokunin/PROVINCE.md`, keep the established boundary note affirming that kaidoku's firmware scope is extraction recursion and outcome triage on compound images, leaving single-binary artifact reverse engineering and interactive debugger control to revenger, consistent with revenger's C07 disclaimer and tsukuroi's ADJ-06 routing.

### B. Upstream Toolchain Facts
Both `kaidoku` and `revenger` cite identical host toolchain facts: REA 6.5.0, Binwalk 3.1.0, Unblob 26.6.4, Sasquatch 4.5.1. Sourced claims and knowledge entries in kaidoku should cite the installed receipt or row-pinned package records rather than restating toolchain availability as an ungrounded novel finding.

---

## 4. Defect Patterns Siblings Recorded That Round-43 Tools Could Repeat

1. **Unanchored Host-Fact Statements (`tsukuroi` R40-HOSTCELL-UNANCHORED, `kengaku` M3, `revenger` Q16)**:
   - *Sibling Evidence*: In tsukuroi `round-40.md:77`, the L1 wrote from memory that `/tmp` was tmpfs, whereas live host inspection showed xfs. In kengaku `round-40.md:41`, the L1 wrote an unobserved exit code.
   - *Repeat Risk in Kaidoku R43-C2*: Draft claim `plans/round-43-claims.md:107-108` asserts: `"every copy's digest re-verifies against the live host object it copies (fresh row-pin audit, this round)"`.
   - *Empirical Defect*: Seats `R43C2Land` and `R43C2Pin` verified today that the npx cache path `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/` (covering S040, S048, S056, S066, S070, S079, S083, S090, S092) and the Go directories `/home/vgpnk/.local/opt/go-1.25.0` (S035) **no longer exist on this host**. Freezing line 107 as written would commit an unanchored, false host-state assertion. The claim text must be calibrated to state re-verification against surviving host paths (Ghidra, tinyxxd) and against row-pinned package archives for transient caches.
2. **Generator Blind Spots and Factor-Predicted Tuples (`kengaku` M1/M2, `kake` CtlPrefixCache/CtlHeadTail)**:
   - *Sibling Evidence*: Kengaku M1 (`round-42.md:11`) caught declared directions copied from tables instead of measured from runs. Kake `CtlHeadTail.md:24` caught that generators building clean bases missed cross-feature defect combinations.
   - *Application to Kaidoku R43-C1*: This is the exact root of routed defect `R42-CL1` / mistake `M42-2`: combo C02 was predicted as `{extractor-failure, unpublished-entry}`, but REA `--run` generated a sibling that hit the depth ceiling, minting `{depth-limited, extractor-failure, unpublished-entry}`. QUALITY 85 enforces that the generator refuses to write the manifest if declared != observed. Pre-freeze controls (CTL-C1-2) must test this refusal red/green.
3. **Unanchored Verdict Parsing (`tsukuroi` R42-VERDICT-FORM)**:
   - *Sibling Evidence*: Tsukuroi `round-43.md:124` found that a counter parsing loose verdict lines admitted contradictory JSON fields or blank-prefixed lines.
   - *Application to Kaidoku C1 Counter*: `tools/round-43/c1-counter.py` must strictly anchor `observed_features_match_declared` and refuse malformed or multi-valued boolean tokens.
4. **Controls Failing for the Wrong Reason (`tsukuroi` R40-CONTROL-OWN-BASELINE / R41-LABEL-SUFFIX)**:
   - *Sibling Evidence*: Pre-data controls must violate *exactly one* parameter. In CTL-C1-1 and CTL-C1-2, receipts must prove failure specifically via the refusal exit (exit 3 `declared_tuple_unobserved` or seed mismatch), not via missing fixtures, scratch paths, or unhandled exceptions.

---

## 5. Fleet Round-43 Reports Scan (`.ufo/reports/round-43/`)

All 10 reports filed for round 43 across the fleet were audited against kaidoku round-43 claims:

| Report | Lane | Declared Claims | Collision with Kaidoku R43? |
|---|---|---|---|
| `tsukuroi.md` | `tsukuroi` | C1 boot-chain-audit.sh under pipefail (operability); C2 btrfs-scrub-record-r43.md (depth) | **None** |
| `kengaku.md` | `kengaku` | C1 anchor/order digest verification (calibration); C2 TB2 feal differential cryptanalysis (coverage) | **None** |
| `mado.md` | `mado` | C1 mado-geometry.py windowrule join (operability); C2 hyprland-gkeep-geometry-r43.md (coverage) | **None** |
| `kama.md` | `kama` | C1 instrument registry audit (calibration); C2 hexrun-census (operability); C3 assimilation (coverage) | **None** |
| `tameshi.md` | `tameshi` | Mutation-testing verification of census gates | **None** |
| `mori.md` | `mori` | C1S successor operability counter; calibration repair | **None** |
| `chousa.md` | `chousa` | C1 absent-split.py (operability) | **None** |
| `kake.md` | `kake` | C1 sitemap URL scanner counter v4 across three independent seeds (operability) | **None** |
| `kumitate.md` | `kumitate` | Dispatch evidence and latch synchronization operability | **None** |
| `kotodama.md` | `kotodama` | Honest stop on operability and calibration | **None** |

**Conclusion**: Zero claim collisions. No other lane is claiming SquashFS recursion, outcome triage tables, unblob/sasquatch assets, or host-local source copy gates.

---

## 6. UFO-FSD Connector Synthesis: Bounded Proposal

### Evidence
1. **Contract Path Discrepancy (C2)**: `plans/round-43-claims.md` (:96-97, :103, :147) strictly binds in-lane copies under `corpus/evidence/round-43/local-sources/`. However, `R43C2Land` staged its landing pack under `corpus/evidence/round-42/local-sources/` with `local-sources.json` pointing to `round-42`. Committing under `round-42` would cause Predicate P43-C2 clause `"under corpus/evidence/round-43/local-sources/"` to fail.
2. **Substrate Drift Contradiction (C2)**: Draft claim line 107 asserts `"every copy's digest re-verifies against the live host object it copies (fresh row-pin audit, this round)"`. Empirical re-audit by `R43C2Land` and `R43C2Pin` confirms that 11 of the 18 host paths (npx `rea-agents@6.5.0` and Go toolchains) have drifted off the host filesystem. Their byte authority rests on row-pinned package tarballs (npm, Go releases), not live host files.
3. **Census Validator Schema Rejection (Frontier S135)**: Seat `R43SrcLicense` proved that setting `kind: license` on row S135 causes `scripts/sources-census.sh validate` to fail with `E05 kind=license` (exit 1). `scripts/sources-census.sh` only allows `(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)`. S135 must be `kind: docs` to green the census.
4. **Refusal Mechanism Alignment (C1)**: `R43RevRevenger`'s `tuple-check-proto.py` and `R43C1Gen` verify that comparing `observed_features(envelope)` from REA `--run` against `declared_features` accurately refuses discrepant factor combinations (exit 3 on C02).

### Affected Axes
- **Calibration (Owned, Tied at 10)**: Prevents an ungrounded overclaim in the claims document (claiming live host re-verification for files no longer on disk) and ensures truthful substrate attribution.
- **Coverage (Owned, Worked by C2)**: Ensures that `local-sources.json` and in-lane copies strictly satisfy Predicate P43-C2's path requirement (`round-43/local-sources/`), allowing `local-source-gate.py` to exit 0 without contract-path failure.
- **Depth (Owned, Worked by C1)**: Ensures S135 passes `sources-census.sh validate`, preventing a census failure from blocking the round-43 depth knowledge note.

### Proposed Move
**Synthesize Substrate Calibration, Path Canonicalization, and Census Conformance into a Single Pre-Freeze Claims Harmonization:**
1. **Calibrate Substrate Attribution in `plans/round-43-claims.md:107-108`**:
   Replace the unanchored assertion with:
   `"every copy's digest re-verifies against its authoritative origin bytes: surviving live host objects for local installs (Ghidra, tinyxxd) and row-pinned upstream package archives for drifted transient caches (npm rea-agents@6.5.0/6.7.0, Go source archives), with live-vs-upstream provenance recorded in local-sources.json notes."`
2. **Canonicalize Landing Path to `round-43`**:
   At integration time, ensure `local-sources.json` and the 17 staged copy directories are placed under `corpus/evidence/round-43/local-sources/`, updating `LANE_TREE` from `round-42` to `round-43` to perfectly match Predicate P43-C2.
3. **Adopt Valid Census Schema for S135**:
   Commit S135 with `kind: docs` as validated by `R43SrcLicense`, ensuring `sources-census.sh validate` exits 0.

### Risks
- If path strings in `local-sources.json` do not match copy directory paths on disk, `local-source-gate.py` will exit 1 with `missing-copy`. *Mitigation*: Run `python3 -I -B tools/round-41/local-source-gate.py --root . --rev <REV>` in a sandbox clone before freeze.
- Upstream package tarballs must match the exact sha256 pinned in the SOURCES rows. *Mitigation*: `R43C2Land` and `R43C2Pin` have verified that npm registry tarballs match row-pinned digests byte-for-byte.

### Verification
1. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 (clean census, no E05).
2. `python3 -I -B tools/round-41/local-source-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` exits 0 with `rows_failed: []` and all copies residing under `corpus/evidence/round-43/local-sources/`.
3. Pre-data refusal control CTL-C1-2 exits 3 (`declared_tuple_unobserved`) on round-42 C02 and writes no manifest, while passing on observed tuples.

---

## 7. Artifacts

- Hit table with line context: `.ufo/waves/round-43/w1/artifacts/R43ConnSib/sibling-overlap-hits.tsv`
