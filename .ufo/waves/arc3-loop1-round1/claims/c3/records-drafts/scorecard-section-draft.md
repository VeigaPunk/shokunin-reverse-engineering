# SCORECARD.md round-section draft — C3 records (SC-7, arc3-loop1-round1)

Seat SC-7 · chain c3 · role scribe · 2026-10-19. **Draft for the PARENT;
SCORECARD.md was not touched.** Append at EOF (after the round-10 section,
`SCORECARD.md:1336`). Structure follows CN-2's records outline
(`claims/cross/records-outline.md` §4); `⟨…⟩` = parent-fill slots; the **C3
bullet, the C3 verdict row, the C3 learning sentence and the C3 carried-debt
line are complete and evidence-cited**.

**Pin-free discipline (measured, load-bearing):** the appended section must
carry no `rea-agents@` pin with a version, no bare `6.x.y` literal, and no
`~`//-absolute `path.json|toml|yaml:NNN` pointer in a block matching the
census REA_GATE — else the census reads UNDECLARED at the tail (SC-6 fixture
A1; SC-7 control). The C3 text below is pre-verified pin-free by simulation
(§3).

## Literal section text (append as-is; fill `⟨…⟩` slots first)

<!-- BEGIN LITERAL SECTION TEXT -->
## arc3-loop1-round1 — coverage + operability + freshness: ⟨PARENT-FILL: verdict phrase per CN-2 §4.1⟩, 2026-10-19

⟨PARENT-FILL: opening paragraph per CN-2 §4.2 — arc3 loop 1 round 1 (post-halt
restart); wave size/model; roster frozen pre-dispatch; delivery ⟨N⟩/64;
admission per chain⟩

- Wave: ⟨PARENT-FILL per CN-2 §4.3 — reports path, work/artifacts/records
  commits⟩.
- C1 coverage (owned) — ⟨PARENT-FILL from SC-3 per CN-2 §4.4⟩.
- C2 operability (fleet) — ⟨PARENT-FILL from SC-5 per CN-2 §4.5⟩.
- C3 freshness (fleet) — E22 (arc2-loop1-round3 carried debt,
  `SCORECARD.md:850-852`: "census scope-table drift (FAIL undeclared=2 at
  766-line HEAD vs PASS at 701-line `b21c0da` — re-key or retire next
  calibration round)") dispositioned by measurement at last — this bullet is
  the card-side closure of the debt line (the instrument header carries the
  instrument-side statement; CR-5 A4: record both, or the disposition is
  one-sided). Census v10 (instrument sha256 `36e96cd5…`) at HEAD `e845c2b` →
  **PASS 0/0/0/0** (`VERDICT: PASS  (stale=0 ambiguous=0
  undeclared=0 unresolved=0)`, exit 0, scope-errors [], G2 ok, G7 [], G11 []);
  capture sha `3b677b8e…`, four independent captures one digest
  (EX-26/SC-6/EX-30/RV-11). No scope row undeclared or stale at HEAD → the
  re-key branch is NOT taken; no row retired; the row-level history (rows
  added at `265e1aa`, shifted +1 at `6bc4c29` for the `:622` capability row)
  and the disposition are stated in the instrument's own header. The records
  append is pre-verified locus-free in the census unit: records-tree
  simulation → PASS 0/0/0/0, exit 0; planted tail locus → FAIL undeclared=1 —
  the PASS is a live detector result. Census at the records commit:
  ⟨PARENT-FILL: re-run quote⟩ (pre-verified to read PASS 0/0/0/0). No
  corpus/knowledge edit in this claim.
- Measured at the records commit: ⟨PARENT-FILL per CN-2 §4.7 — command A
  82/82, 13/13, 10.0/10.0, missing [], dangling []; probe selftest 13/13 +
  findings=0; census PASS 0/0/0/0; custody post-pair 5/5⟩.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage (owned) — C1 | ⟨PARENT-FILL from SC-3⟩ | ⟨PARENT-FILL⟩ |
| operability (fleet) — C2 | ⟨PARENT-FILL from SC-5⟩ | ⟨PARENT-FILL⟩ |
| freshness (fleet) — C3 | E22 finding undispositioned at HEAD → dispositioned by measurement: census v10 PASS 0/0/0/0 at `e845c2b` (the FAIL class unreproducible under v10; v9 stays red at HEAD by construction), no scope row undeclared/stale, no re-key, none retired; records append locus-free (simulation PASS 0/0/0/0; planted tail locus FAIL undeclared=1) | improved |
| depth | ⟨PARENT-FILL: 13/13 at the records commit, unchanged⟩ | unchanged |

Learning trends: ⟨PARENT-FILL per CN-2 §4.9; C3's sentence:⟩ the E22 carried
debt closed by measurement rather than another re-key, and the census's
fixed-bound posture is demonstrated with a live positive control — the records
append discipline (locus-free in the census unit) is checkable at every
records commit.

Planned: ⟨PARENT-FILL⟩. Carried debt (named): ⟨PARENT-FILL C1/C2 merges⟩; C3
adds none — E22 closed; the standing constraint (records appends stay
locus-free in the census unit or the bound re-keys in the same commit) is
restated in the instrument header. Retired: ⟨PARENT-FILL: none / list⟩.
<!-- END LITERAL SECTION TEXT -->

## Notes for the parent

- CN-2 §6.4 (C3's claim closes here): if the records append introduces an
  undeclared locus, the SCOPE table needs a new DATED row in the same commit.
  Measured for the drafted text: it does not (simulation below).
- The C3 bullet's "Census at the records commit" slot takes the verbatim
  re-run quote; the pre-verified reading is PASS 0/0/0/0, exit 0.

## 3. Records-tree simulation (SC-7, `/var/tmp/sc7` scratch)

- Tree A = the three census files at HEAD + the literal text above appended to
  `SCORECARD.md` → `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0
  unresolved=0)`, exit 0.
- Tree B = Tree A + a planted tail pin literal → `FAIL` with
  `UNDECLARED (1)`, exit 1 — the detector is live on the appended region (same
  class as SC-6 fixture A1).
- Commands, verbatim outputs and shas: `seats/SC-7.md` §3.
