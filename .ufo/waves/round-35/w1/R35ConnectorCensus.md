# R35ConnectorCensus — Connector Report: Census, Collision, and C1 Row Selection

**Seat**: `R35ConnectorCensus` (UFO-FSD connector)  
**Lane Root**: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`  
**Milestone**: Build evidence and first falsifications (Round 35, Wave 1)  
**Report Target**: `.ufo/waves/round-35/w1/R35ConnectorCensus.md`  

---

## 1. Executive Summary & Scope

Per the UFO-FSD connector mandate, this report identifies one non-obvious move — a compatible synthesis across Wave 1 findings — that connects the three focal elements of Round 35's assimilation substrate:
1. **Census**: The base registry census (`rows=106`, 9 W04 warnings, committed in `d2729cba`) and its role in Claim C2 Defect D-1.
2. **Collision**: The recorded collision `S106` (`assimilation/collisions`), its boundary origin in Round 34, and the 0–3 space leading indentation guard.
3. **C1 Row Selection**: The selection of `S125` and `S129` from `merge/kaidoku/` (and `shokuknow`) for the `.jsc -> source mapping` frontier, resulting in a sparse ID sequence (`S106` -> `S125` -> `S129`).

We examine the second-order coupling among these surfaces, expose critical contradictions across verification and contract layers, and present a single bounded proposal: the **Isolated-Staged Atomic Landing (ISAL) Envelope**.

---

## 2. Local Evidence

### 2.1 Census Evidence
- **Base Registry State (`aa04633a`)**: `corpus/SOURCES.md` contains exactly 106 rows (`S001` through `S106`). `scripts/sources-census.sh validate` exits 0 with 9 pre-existing `W04` warnings (duplicate URL across scopes).
- **Frozen Census Start Receipt**: `.ufo/waves/round-35/assimilation/census-start.txt` was committed in `d2729cba` (first commit post-base, committer timestamp `2026-10-25T16:05:46-03:00`). It records `rows=106`, `malformed=0`, `tiers A=100 B=5 C=1`, `status mined=102 rejected=4`, `duplicate_ids=0`, `EXIT=0`.
- **Frozen Input Pin**: Pinned in `.ufo/waves/round-35/claims-canonical.json` under `frozen_inputs` with SHA-256 `b6ce2b1773c60af4e3f5b14b7a63ba9743cae1eeec121b1ada50178a3d7af10a`.
- **C2 D-1 Requirement & Counter Mechanism**: `tools/round-35/c2-calibration-counter.py:64-78`:
  - Retrieves `ct = commit_time(root, rev, CENSUS_PATH)` via `git log --format=%cI -1 rev -- CENSUS_PATH`.
  - Retrieves `fc = first_change_time(root, base, rev, "corpus/SOURCES.md")` via `lines[-1]` of `git log --format=%cI base..rev -- corpus/SOURCES.md`.
  - Asserts `"rows=106" in census and "EXIT=0" in census and "W04" in census`.
  - Asserts `fc is not None` (`D1_no_sources_change_after_base` if absent) and `parse_iso(ct) <= parse_iso(fc)` (`D1_census_after_first_sources_change` if `ct > fc`).

### 2.2 Collision Evidence
- **Collision Record**: `.ufo/waves/round-35/assimilation/collisions` contains exactly one line: `S106`.
- **Set Derivation**:
  - `assimilation/reg-ids` (106 items): `S001`..`S106`.
  - `assimilation/staged-ids` (132 items): `S106`..`S237`.
  - Intersection: `set(reg-ids) & set(staged-ids) = {'S106'}`.
- **Root Cause of Collision**: Row `S106` was admitted and mined in Round 34 (commit `66b84027`, GNU binutils `readelf.c` version-needs reader, line 112 of `corpus/SOURCES.md`). When `staged-ids` was carried over into Round 35, `S106` was not pruned from line 1 of the staged list.
- **C2 D-3 Direct Reference**: Claim C2 Defect D-3 explicitly requires: `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` must carry an appended provenance trio citing `S106`. Thus `S106` is not an unadmitted candidate; it is an active registered source.
- **Indentation Guard**: `.ufo/waves/round-35/assimilation/id-guard-proof/` confirms that `scripts/sources-census.sh` accepts 0–3 leading spaces before `|` rows (`^ {0,3}\|`), catching indented collisions (e.g. `S002` in fixture). However, `c1-coverage-counter.py:22-25` `ROW_RE` uses `(?m)^\|\s*(S\d{3,})\s*\|` (column 0 only).

### 2.3 C1 Row Selection Evidence
- **Origin in `merge/kaidoku/`**: In `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md`, the expansion campaign staged rows sequentially (`S106`..`S132`). Rows `S125` (`xqy2006/jsc2js` upstream README) and `S129` (`xqy2006/jsc2js` GitHub Releases API) were mapped to candidate knowledge entries `jsc-mapper-cli-contract.md` and `jsc-mapper-release-inventory.md`.
- **Round 35 Selection**: `plans/round-35-claims.md:10-14` selected only the `.jsc -> source mapping` frontier for Claim C1 (coverage) because S125 and S129 cite external fetched sources, avoiding own-work execution debt.
- **Quarantine Outcome**: `assimilation/quarantine-verdicts.md` evaluated 5 staged rows: S150 was refused (fabrication class), while S113, S117, S136, S147 were not adopted. Conclusion: "No row is appended; adoption stays closed to the admitted jsc2js entries (S125/S129)."
- **Sparse Allocation**: Admitting S125 and S129 skips S107..S124 and S126..S128, creating a non-contiguous registry index: `S001..S106`, `S125`, `S129`.
- **C1 Counter Validation**: `tools/round-35/c1-coverage-counter.py` specifically requires `rows["S125"]` and `rows["S129"]` with `status == "mined"`, `opened.startswith("2026-10-25")`, and `used-by` naming the corresponding `corpus/knowledge/` paths.

---

## 3. Explicit Contradictions Identified

1. **Cross-Claim Coupling vs. Claim Severability**:
   - C2 claims to be an independent calibration claim ("round-34 verifier-routed record defects closed").
   - However, C2 D-1 requires a post-base commit to `corpus/SOURCES.md` (`fc is not None`).
   - In Round 35, only C1 writes to `corpus/SOURCES.md`. If C1 is stalled, partitioned, or fails, C2 D-1 fails with `D1_no_sources_change_after_base`. C2 is functionally coupled to C1.
2. **Collision False-Alarm vs. Registry Integrity**:
   - `assimilation/collisions` flags `S106` as a collision.
   - However, `S106` is not a colliding candidate; it is the vital base row needed by C2 D-3.
   - If an automated script attempts to resolve `collisions` by re-allocating or re-appending the staged block starting at `S106`, `corpus/SOURCES.md` gets a duplicate ID, triggering `E03 duplicate id` in `sources-census.sh validate`.
   - If an implementer attempts to close the ID gap by sequentially renumbering S125/S129 into S107/S108, Claim C1 immediately fails on `registry_row_missing:S125` and predicate mismatch.
3. **Start-Census Witness Immutability vs. Post-Landing Census Drift**:
   - Base census is 106 rows; post-C1 landing registry will have 108 rows.
   - If a downstream seat attempts to update `census-start.txt` with the 108-row census post-landing:
     - `commit_time(census-start.txt)` will be later than `first_change_time(SOURCES.md)`, triggering `D1_census_after_first_sources_change`.
     - `rows=106` substring check will fail (`D1_census_content_missing`).
     - `frozen_inputs` SHA-256 pin will break.
4. **Registry Used-By Validation vs. Commit Atomicity**:
   - `scripts/sources-census.sh validate:566-568` checks `if [ ! -e "$dir/$path" ]; then printf '...E11 missing used-by %s\n'; fi`.
   - If `corpus/SOURCES.md` is modified before the two C1 knowledge entry files exist on disk, `validate` fails with `E11`.

---

## 4. Second-Order Effects Across Surfaces

| Surface | Mechanism | Consequence / Interaction |
|---|---|---|
| **Runtime** | `c2-calibration-counter.py` commit-time parsing (`%cI`) | Strict string comparison `parse_iso(ct) > parse_iso(fc)`. Equal-second commits pass, but any later touch to `census-start.txt` flips the inequality and causes false failure. |
| **Contract** | Frozen predicates `P35-c1` and `P35-c2` | Fixed tokens (`S125`, `S129`, `rows=106`, `S106`) prevent ID shifting or renumbering. |
| **Substrate** | `scripts/sources-census.sh validate` | Enforces `E01` (NF=13), `E02` (`S\d{3,}`), `E03` (unique ID), and `E11` (used-by exists). Does **not** enforce contiguous sequential numbering. |
| **Verification** | Frozen input hash `b6ce2b17...` | Locks `census-start.txt` byte-for-byte; file must remain untouched through all subsequent waves. |

---

## 5. Affected Axes

- **Calibration (C2)**: Direct improvement. Eliminates the false-failure risks of D-1 timestamp inversion, census content corruption, and missing SOURCES change.
- **Coverage (C1)**: Direct improvement. Ensures seamless assimilation of S125/S129 into Core without violating census constraints or triggering `E11` dangling used-by errors.
- **Depth**: Harmed on zero fronts (remains tied at base level 10).

---

## 6. Proposed Move: Isolated-Staged Atomic Landing (ISAL) Envelope

We propose a unified, four-point operational envelope for executing Round 35 data landing:

1. **Formally Prune Staged Range to `[S107..S237] \ {S106}`**:
   Treat `assimilation/collisions: S106` as a closed, historical artifact of Round 34's landing of S106. Retain S106 exclusively for C2 D-3 provenance trio citation. Prohibit any script or seat from appending S106 or treating it as an available candidate ID.
2. **Authorize Sparse Monotonic Registry Allocation**:
   Commit S125 and S129 directly to `corpus/SOURCES.md` without filling or renumbering the intervening IDs (S107..S124, S126..S128). This preserves C1's frozen predicate, avoids introducing unmined/quarantined entries into the registry, and conforms cleanly to `sources-census.sh validate` (which permits non-contiguous IDs).
3. **Atomic Co-Landing Commit for C1**:
   The post-base modification to `corpus/SOURCES.md` (adding S125 and S129) MUST be co-committed in the identical git commit as:
   - `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md`
   - `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md`
   - `PROVINCE.md` (Core-addition table row)
   - `corpus/README.md` (coverage map entries)  
   *Second-order effect*: This guarantees that `first_change_time(SOURCES.md)` postdates `census-start.txt` (`d2729cba`), unblocking C2 D-1, while simultaneously preventing `sources-census.sh validate` from throwing `E11 missing used-by`.
4. **Strict Immutability of `census-start.txt` & Separate End-Census Capture**:
   Enforce that `.ufo/waves/round-35/assimilation/census-start.txt` is NEVER edited or re-committed. Any post-landing census (recording 108 rows) must be written exclusively to `.ufo/waves/round-35/assimilation/census-end.txt` (or documented in `corpus/lessons/round-35.md`), maintaining the integrity of C2 D-1 and the frozen input hash.

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Premature SOURCES Edit** | A commit touches `corpus/SOURCES.md` before knowledge files are written, causing `E11 missing used-by`. | Enforce single atomic commit for all C1 artifacts. |
| **Accidental Overwrite of `census-start.txt`** | Executor updates start receipt with 108 rows, breaking D-1 ordering and content checks. | Lock `census-start.txt`; route post-landing counts strictly to `census-end.txt`. |
| **Clock Skew / Equal Timestamp** | C1 commit committer time matches prep commit (`16:05:46`), causing ambiguous ordering. | Standard git execution: current timestamp (>16:20) is strictly greater than prep time (`16:05:46`). `parse_iso(ct) <= parse_iso(fc)` holds. |
| **Quarantine Contamination** | An agent tries to fill S107..S124 with quarantined rows from `staged-ids`. | `quarantine-verdicts.md` explicitly seals adoption; counter strictly requires only S125/S129. |

---

## 8. Verification Plan

1. **Pre-Landing Invariant Check (Current HEAD `3ecf4298`)**:
   - `c1-coverage-counter.py`: Exits 1 with 8 expected pre-data failures (verified).
   - `c2-calibration-counter.py`: Exits 1 with D1 (`no_sources_change_after_base`) and D2-D4 failures (verified).
   - `census-start.txt`: SHA-256 matches `b6ce2b17...` pin (verified).
2. **Post-Landing Verification**:
   - Run `sources-census.sh validate kaidoku`: Verify exit 0, exactly 108 rows, no E-codes, 9 W04 warnings.
   - Run `python3 -I -B tools/round-35/c1-coverage-counter.py --root . --freeze 2323d197... --rev <measured-rev>`: Verify exit 0 (`C1_CLEAN`).
   - Run `python3 -I -B tools/round-35/c2-calibration-counter.py --root . --base aa04633a... --freeze 2323d197... --rev <measured-rev>`: Verify D-1 passes cleanly (`parse_iso(ct) <= parse_iso(fc)` and content matched), and verify D-2..D-4 closure.
