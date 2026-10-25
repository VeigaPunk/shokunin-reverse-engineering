# R35ConnectorOverlap — Cross-Axis & Sibling Pattern Scan for C1/C2 (Wave 1)

**Seat:** `R35ConnectorOverlap` (UFO-FSD connector)  
**Lane root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`  
**Milestone:** Build evidence and first falsifications  
**Target:** Kaidoku round 35, wave one (`plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`)  
**Frozen Claims:** C1 (Coverage: `.jsc -> source mapping` via S125/S129); C2 (Calibration: round-34 record defects D-1..D-4).  
**Mode:** Advisory evidence and cross-axis synthesis only; read-only inspection of lane repository; write confined strictly to this assigned report path.

---

## 1. Evidence Base (Repository & Current Wave Cache)

Across the wave-1 sibling reports (`R35CriticClaims`, `R35SentinelScope`, `R35Audit07`, `R35Audit08`, `R35Audit10`, `R35Audit16`, `R35Audit24`, `R35Audit31`, `R35Audit32`, `R35Audit33`, `R35Audit35`, `R35ExecC1`, `R35ExecC2`), several structural patterns and second-order dependencies across C1 and C2 were identified and confirmed:

1. **Cross-Claim Temporal Coupling (C2 D-1 ↔ C1 SOURCES Append):**
   - In `tools/round-35/c2-calibration-counter.py:71-77`, D-1 evaluates `fc = first_change_time(root, base, rev, "corpus/SOURCES.md")`. If no post-base commit modifies `corpus/SOURCES.md`, `fc` is `None` and the counter appends `D1_no_sources_change_after_base`, failing C2.
   - In Round 35, only Claim C1's data landing modifies `corpus/SOURCES.md` (by adding rows S125 and S129). None of C2's defect closures (D-1 receipt, D-2 lesson/settles, D-3 r34b trio, D-4 SKILL.md tables) touch `corpus/SOURCES.md`.
   - Consequently, C2 cannot pass in isolation or if measured before C1's registry append is committed.

2. **ID Space Collision vs Citation Overlap (S106 ↔ S125/S129):**
   - `corpus/SOURCES.md` at base ends at `S106` (106 rows, `rows=106`, `duplicate_ids=0`). S106 is the exact authority row cited by C2 defect D-3 on `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`.
   - `.ufo/waves/round-35/assimilation/staged-ids` spans `S106..S237`. The intersection with `reg-ids` is `{'S106'}` (documented in `assimilation/collisions`).
   - If C1's row addition blindly appends from the start of the staged list, S106 will be duplicated in `corpus/SOURCES.md`, destroying census validity (`duplicate_ids != 0`), failing census validation, and invalidating the D-1 baseline premise.

3. **D-4 Heading Literal Mismatch & Unbounded Table Over-Coverage:**
   - In `tools/round-35/c2-calibration-counter.py:130-153`, the counter checks sections listed in `EIGHT_CELL_SECTIONS`:
     - Section 1: `### Round-32 instrument registry`
     - Section 2: `### Round-34 run-6 instrument registry`
   - In `SKILL.md:1209`, the heading is `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)`. Exact-match `l.rstrip() == sec` fails, throwing `D4_section_missing`.
   - In `SKILL.md:1064-1086`, the counter scans every line starting with `|` until the next `##` or `###` heading. At line 1081 sits the archived 4-cell "Residual witness registry" table. Because line 1079 (`Residual witness registry...`) is unheaded plain text, the counter scans lines 1081–1084 and throws `D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4`. The actual Round-32 instrument registry rows (lines 1066–1073) are already 100% 8-cell compliant.

4. **README House Style Divergence for C1:**
   - In `corpus/README.md` (Coverage map lines 15–88), all existing entries list filenames without the `.md` extension.
   - However, `tools/round-35/c1-coverage-counter.py:139` explicitly asserts `p.rsplit("/", 1)[1] not in readme`, requiring `2026-10-25-r35-jsc2js-mapper-contract.md` and `2026-10-25-r35-jsc2js-release-inventory.md` with `.md`. An implementer following repository house style fails C1 with `readme_missing`.

5. **Settle JSON Schema Shift for C2 D-2:**
   - `c2-calibration-counter.py:89-108` asserts integer keys `spawned`, `settled`, `dead` across `.ufo/waves/round-35/w1-settle.json` and `w2-settle.json`. Reusing prior rounds' templates (`completed`/`cancelled`) fails with `D2_settle_missing_field`. Settle files must be committed before measurement.

---

## 2. Contradictions Identified

1. **Separability vs Implementation Coupling:**  
   The round claims C1 (coverage) and C2 (calibration) are independent claims on separate axes. In reality, C2 D-1 has an implicit hard dependency on C1's `corpus/SOURCES.md` modifications.
2. **Historical Fidelity vs Parser Cell-Count Enforcing:**  
   Re-piping the round-32 residual witness table from 4 columns to 8 columns would alter archived historical evidence, corrupting calibration integrity to satisfy a naive line scanner.
3. **Convention vs Literal Token Matching:**  
   `corpus/README.md` convention omits `.md`, whereas the frozen C1 counter strictly enforces `.md`.

---

## 3. Affected Axes

- **Calibration (C2):** Directly resolved from guaranteed failure (`D1_no_sources_change_after_base`, `D4_section_missing`, `D4_not_eight_cells`) to evaluable and passing.
- **Coverage (C1):** Protected against convention-based failure (`readme_missing`) and ID-collision corruption.
- **Depth:** Unaffected and unharmed (retains 10/10 level; no depth regression).

---

## 4. Proposed Move: Boundary-Insulated Co-Landing Sequence

Synthesize the landing of C1 and C2 in Wave 2 under a single coordinated execution contract:

1. **Atomic or Sequenced Commit Order (C1 → C2):**  
   Commit C1's addition of rows S125 and S129 to `corpus/SOURCES.md` either in the same commit as C2 or immediately prior to it. This produces `fc` strictly after `ct` (`d2729cba`, `16:05:46`), clearing `D1_no_sources_change_after_base` without altering frozen counter logic.
2. **S106 Exclusion in C1 Allocation:**  
   Explicitly allocate C1 rows only at `S107+` (`S125` and `S129`). Do not adopt or re-insert `S106` from `staged-ids`, ensuring `S106` remains solely attached to C2 D-3's r34b entry citation, maintaining `duplicate_ids=0`.
3. **Heading Insulation in `SKILL.md` (Preserving Historical Data):**  
   - Insert `### Residual witness registry` at line 1079 above the 4-cell table. This halts the C2 D-4 while-loop before line 1081, satisfying the Round-32 check without modifying a single cell of archived witness records.
   - Normalize line 1209 to `### Round-34 run-6 instrument registry` (removing the suffix) and pad the five run-6 instrument rows to 8 columns.
4. **README Literal Inclusion:**  
   In `corpus/README.md`, add both entries with explicit `.md` extensions in the Coverage map table, satisfying `c1-coverage-counter.py`. In `PROVINCE.md`, add the bare stems to the Round-35 Core-addition table.
5. **Exact Settle Schema Emission:**  
   Commit `w1-settle.json` and `w2-settle.json` with keys `{"spawned": ..., "settled": ..., "dead": ...}` prior to running the C2 counter, and match the exact sum line in `corpus/lessons/round-35.md`.

---

## 5. Risks and Mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| C1 and C2 separated across branches | C2 fails D-1 with `D1_no_sources_change_after_base` | Enforce single-branch co-landing in wave 2 |
| Accidental ingestion of S106 from staged range | ID collision in `corpus/SOURCES.md`, breaks census | Filter out S106 in row append scripts |
| Suffix omission in README coverage map | C1 fails `readme_missing` | Pre-commit check verifying `.md` in README rows |
| Rewriting residual witness columns | Historical evidence mutation | Use `###` heading insulation instead |

---

## 6. Verification

Verify the proposed move by running both frozen counters against the measured commit in a temporary clone:

```bash
FZ="2323d197456f1328459d9420aff025cffbcb3e27"
BASE="aa04633a686d49756763b1feed4be6830d5bb479"

# C1 verification
python3 -I -B tools/round-35/c1-coverage-counter.py --root <lane> --freeze $FZ --rev <measured-rev>
# Expected: exit 0 (C1_CLEAN)

# C2 verification
python3 -I -B tools/round-35/c2-calibration-counter.py --root <lane> --base $BASE --freeze $FZ --rev <measured-rev>
# Expected: exit 0 (C2_CLEAN)
```

Report: .ufo/waves/round-35/w1/R35ConnectorOverlap.md
