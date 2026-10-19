# CR-5 (critic, chain c3) — attacks on the census scope-table re-key

Wave arc3-loop1-round1 · Seat CR-5 · 2026-10-19 · HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(no seat commits; all measurements read-only on the lane repo, scratch in `/dev/shm/cr5/`).

Task: attacks — (1) scope-creep re-key (widening to trivially PASS), (2)
adjudicated-not-edited laundering on dated rows, (3) instrument
self-certification (the census grading its own re-key). Verdicts below.

**Status: EX-28's edit LANDED at sha256
`6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (from
before-state `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`)
and was audited in full below.** The edit is a docstring disposition + one
range-neutral row re-key (PROVINCE.md 45-62: marker line 40 → 45, regex
`verified on this host 2026-10-13` → `2026-10-13`) + a new guard G18
(marker line must lie inside its own range). Headline verdicts: no creep
(differ flags empty, stdout byte-identical `3b677b8e…`); the re-key repairs a
real G15/G18 hole this seat had not tested; all detectors still fire after
the edit; the blind-instrument (G2) hole persists, patch still proposed.

## 1. Work performed (evidence pointers)

- **Before-state census at HEAD recorded verbatim**: `VERDICT: PASS (stale=0
  ambiguous=0 undeclared=0 unresolved=0)`, exit 0, anchors `devin 6.5.0 / omp
  6.5.0 / kimi 6.7.0`; counts PROVINCE.md 162 lines/6 loci, SCORECARD.md 1336
  lines/9 loci, SKILL.md 371 lines/2 loci. Receipt:
  `claims/c3/CR-5/receipts/census-at-HEAD-cr5.out` (identical in substance to
  EX-26/SC-6/RV-11 receipts, 4405 B).
- **Independent coverage re-derivation** (separate implementation, line-level,
  no REA_GATE gating — strictly broader than the census's UNDECLARED class):
  20 scope rows; **0 out-of-range occurrences** of the three needle classes;
  40 occurrences inside DATED rows (16 of them non-live values accepted as
  historical = the shelter surface). Tool + output:
  `claims/c3/CR-5/tools/independent-census.py`,
  `claims/c3/CR-5/receipts/independent-before.out`.
- **E22 finding reproduced on the archived tree**: recovered census v9
  (sha256 `213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c` —
  matches the v10 header's claimed predecessor) against `git show
  679af5d:*` (766-line SCORECARD) → **FAIL undeclared=2, exit 1**; the two
  undeclared loci identified: SCORECARD.md blocks 731-737 (round-2 records
  text) and 747-766 (`kimi=6.7.0`). Same instrument at `b21c0da` (701-line) →
  PASS 0/0/0/0, exit 0. Receipts: `receipts/v9-repro766.out`,
  `receipts/v9-repro701.out`.
- **Round-8 re-key necessity proven**: pre-r8 census (from `e87e507`) against
  the pre-r8 tree `e87e507` → PASS; against the post-insertion tree `6bc4c29`
  → **FAIL, 3 SCOPE-ERRORS** (markers absent at :635/:703/:768 — the +1 line
  insertion had shifted the round-record headers off the declared marker
  lines); post-re-key census at `6bc4c29` → PASS. So the r8 re-key was a
  genuine alignment repair, and its form is the clean form (pure +1 renumber,
  fixed bounds, no class flips — diff at `6bc4c29` shows exactly three rows
  shifted). Receipts: `receipts/v10-r7-at-e87e507.out`,
  `receipts/v10-r7-at-6bc4c29.out`, `receipts/v10-at-6bc4c29.out`.
- **Falsifiability suite on the before-instrument** (6 injections on
  /dev/shm copies of the three target files): false current pin → FAIL
  stale=1 exit 1; undeclared append → FAIL undeclared=1 exit 1; stripped
  DATED marker → 2 SCOPE-ERRORs exit 1; empty HOME → ANCHOR-FAIL exit 2;
  out-of-range pointer → UNDECLARED=1 exit 1. Receipts:
  `receipts/t1-*.out … receipts/t6-*.out`, harness
  `claims/c3/CR-5/tools/run-injections.py`.
- **Needle-free growth verified**: SCORECARD.md lines 856-1336 (beyond the
  last declared row, 769-855) contain **zero** `6.x.x` tokens and zero
  `rea-agents@` pins (plain grep + census run) — so the HEAD PASS is genuine,
  not a detection hole.
- **Current-state-language scan over every DATED row** (45 live-language hits
  across 13 rows, e.g. `:825 config.toml zero-drift claim is VOID`,
  `:699 live config now pins`): receipt
  `receipts/dated-live-language-scan.out`; tool
  `claims/c3/CR-5/tools/current-state-scan.py`.
- **Blind-instrument probe (self-certification hole, measured)**: with
  `PIN`/`VER`/`PTR` neutered to never match, the census reports `loci=0` on
  all three files, prints `G2 positive-assertion guard: ok`, and **PASSes**
  (exit 0) — the guard's second disjunct is vacuously true when nothing is
  found, so a blind instrument is indistinguishable from a clean one.
  Receipts: `receipts/census-blind-at-head.out`, `tools/census-blind.py`;
  patch-text proposal filed at
  `claims/c3/CR-5/proposed-g2-positive-floor.patch.md` (NOT applied).
- **DATED-class legitimacy spot check**: every one of the 13 DATED rows
  begins at a genuine era/round record (luna-round-2..8 sections at 273-326,
  417-466, 467-502, 503-533, 534-560; the Capabilities rows 619/620; the
  arc2-loop1-round1..3 sections at 636-702, 703-768, 769-855) with its
  content marker present (corroborated by EX-29's boundary audit) — the
  DATED class is not being abused in the before-state.
- **No line shift exists to re-key this round**: `git diff --stat
  9e9d6b1..HEAD -- PROVINCE.md SKILL.md SCORECARD.md` is empty, so any SCOPE
  bounds change by EX-28 would be a coverage decision, not an alignment
  repair (the r8 precedent was a necessary +1 repair — proven above).
- Custody: no custody path was modified by this seat; no installs; no git
  mutations; only reads (census anchor greps, `git show`).

## 1b. After-audit of EX-28's landed edit (final verdicts)

- **Diff audited in full** (`git diff`, final: 61 insertions / 4 deletions;
  copy of the after-instrument filed at `tools/census-after.py`, sha
  `6f1d19ff…`): docstring disposition (45 lines), the one SCOPE row re-key
  (marker 40→45 + regex narrowing), and G18 in `assert_markers()`
  (`s <= ml <= e` check appended before the G15 regex check). No needle
  regex, `REA_GATE`, or `classify()` change.
- **Creep verdict: CLEAN.** `tools/scope-diff.py` before-vs-after:
  `CHANGED (1) ~ PROVINCE.md 45-62 DATED -> 45-62 DATED (marker 40->45)`,
  `CREEP FLAGS: []` — range-neutral, no add/remove, no class flip, no
  widening, no open-ended bound. Receipt:
  `receipts/scope-diff-before-vs-after.txt`.
- **Behavioral identity: stdout sha256 `3b677b8e…` — byte-identical before
  and after the edit** (verified by this seat; matches PL-3's §6 requirement
  and the five prior captures). Locus-count invariance holds: PROVINCE 6 /
  SCORECARD 9 / SKILL 2 loci. EX-28's own receipt
  `claims/c3/EX-28/census-at-HEAD-after.txt` is byte-identical to my
  independent run (`receipts/census-at-HEAD-after-cr5.out`).
- **The re-key repairs a real hole this seat had NOT tested**: row 45-62
  named marker line 40 — inside row 40-43, i.e. the row dated itself by
  another row's intro line; G15 asserted only that the named line carried
  the marker, so the defect was invisible. EX-28 re-keyed the marker inside
  its own range (line 45 carries the row's own "(2026-10-13 receipt)" text)
  and added G18. My G18 falsification: reverting the marker to 40 →
  `SCOPE-ERROR ... (G18)`, FAIL exit 1 (`receipts/g18-revert-marker40.out`);
  marker beyond end (63) → G18 fires, FAIL exit 1
  (`receipts/g18-marker-beyond-end.out`); final state → `SCOPE-ERRORS: []`,
  PASS. Independent re-derivation of marker-in-range over all 13 DATED rows:
  `VIOLATIONS: []` (`receipts/marker-in-range-independent.txt`).
  Precision note for the parent (wording only): the docstring calls this
  "One stale row"; the row's *content* was not stale — its *marker
  declaration* was mis-anchored. The next sentence in the docstring explains
  it correctly.
- **Falsifiability suite re-run against the after-instrument**: t1 false pin
  → stale=1; t2 undeclared append → undeclared=1; t3 marker strip → 1
  SCOPE-ERROR (was 2 pre-edit — the shared-marker coupling is gone); t4
  anchor fail → exit 2; t6 ptr out-of-range → undeclared=1; t5 shelter
  unchanged (pre-existing design). Receipts: `receipts/t*-*.out` (after run
  overwrote the case outputs; both runs recorded in the transcript history
  and the before run preserved in the earlier receipts). All detectors
  intact.
- **Blind-instrument hole persists**: with all three needle regexes neutered,
  the after-instrument still prints `G2 positive-assertion guard: ok` →
  `VERDICT: PASS`, exit 0 (receipt `receipts/census-after-blind3.out`); the
  `g2_ok` line is unchanged at :453. The proposed patch
  (`proposed-g2-positive-floor.patch.md`) is orthogonal to EX-28's edit and
  still stands.

## 2. Proposed changes

**None landed** (critic seat; and EX-28's edit had not landed to audit).
Two patch-text recommendations if useful to the parent:

- If EX-28's header states the disposition, it should carry the causal chain
  measured here, not only the HEAD verdict: E22 real at the 766-line tree
  (undeclared=2, loci named) → r8 fixed-bound renumber was necessary
  (3 marker SCOPE-ERRORs without it) → v10 at `e845c2b` PASS 0/0/0/0. A
  disposition sentence without the 766-line reproduction risks the
  "adjudicated, not falsified" laundering class (the phrase already appears
  at SCORECARD.md:961 about an earlier census PASS).
- The records commit could pin the census sha256 before/after in the round
  section (the census has no external pin of its own SCOPE table; git history
  is currently the only audit trail). Parent-side decision.
- **`claims/c3/CR-5/proposed-g2-positive-floor.patch.md`** — patch text (NOT
  applied) closing the blind-instrument PASS: `g2_ok` must demand a positive
  assertion floor instead of passing vacuously when no loci are found.

## 3. Before → after measurement (c3 claim)

- **Before** (at HEAD `e845c2b`, census sha256 `36e96cd5…`):
  `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 —
  receipt `receipts/census-at-HEAD-cr5.out`.
- **After**: EX-28's edit not landed within the poll window; no after-state to
  measure. The claim's "records commit" run is parent-side and, given the
  before-state already PASSes, the honest minimal edit is a header
  disposition with no SCOPE change; the records-commit PASS then depends on
  the parent's new round-section text staying needle-free (rounds 4-10 did
  this: 856-1336 has 29 live-language lines but zero version tokens).

## 4. Attacks / refutations attempted, with verdicts

**A1 — scope-creep re-key (widening to trivially PASS).** Detector armed and
proven: `tools/scope-diff.py` flags open-ended bounds, wide added DATED rows,
CURRENT→DATED flips, DATED end-widening, and widen-by-add/remove. Proof it
catches the exact attack shape: on a scratch copy I widened the last row
(769-855 → 769-1336) and the differ flagged both "wide added DATED row (568
lines)" and "widen-by-add/remove". Verdict on the *actual* edit: **pending
EX-28**; on the before-state, no creep exists (table unchanged since r8), and
there is **no line shift to repair** this round (targets byte-identical to
`9e9d6b1`), so a bounds change would be a coverage decision, not a re-key.
Note the r8 precedent (measured above) is the clean form — a future re-key
matching it is acceptable; any coverage *expansion* is not.

**A2 — adjudicated-not-edited laundering on dated rows.** Two parts.
(a) Is the finding real? Yes — reproduced at the 766-line tree
(undeclared=2, exit 1) and not reproducible at the 701-line tree (PASS); so a
disposition that says "no drift" or closes E22 without naming the re-key
would be refuted by `receipts/v9-repro766.out`. (b) Is the DATED class being
used as an escape hatch? The shelter surface is real and pre-existing: a
false-current statement planted inside a DATED row (markers intact) is
swallowed → PASS exit 0 (`receipts/t5-dated-shelter.out`), and 16 of 40
DATED occurrences are non-live values. The r8 re-key did not grow this
surface (three rows renumbered, same bounds). Spot check (corroborating
EX-29/PL-3): all 13 DATED rows begin at genuine era/round records with their
content markers present — no abuse in the before-state. Verdict: acceptable
*iff* EX-28's edit does not add/extend DATED coverage over text that carries
current-state claims (the 45-hit scan quantifies where that text is); the
PL-3 plan's rule (never extend a row past its section; never rewrite dated
text; overshoot bounds refused) is the correct boundary.
**Pending EX-28**; no laundering in the before-state.

**A3 — instrument self-certification (the census grading its own re-key).**
Demonstrated empirically: with the widened row, the census still reports
**PASS 0/0/0/0** (receipt `receipts/census-widened-at-head.out`) — the
instrument cannot detect its own widening, because the SCOPE table is both
the object and the oracle. Paired demonstration on one fixture (false-current
claim at SCORECARD:1000): widened instrument → PASS exit 0
(`receipts/widen-swallow.out`); un-widened instrument → FAIL undeclared=1
exit 1 (`receipts/before-swallow.out`). Verdict: **the census's PASS cannot
certify the re-key; the external diff audit (A1) + the independent checker
(A1/tools) + the historical reproductions (A2) are the only certificates.**
For this round the external re-derivation confirms the before-state PASS
(independent checker: 0 out-of-range) — the instrument's claim survives an
external check today, but nothing about the mechanism prevents a future
edit from making PASS trivial, which is why the edit diff must be audited.
**Second hole, measured**: a *blind* instrument (all needle regexes neutered)
reports `loci=0` everywhere and still PASSes — `G2 positive-assertion guard:
ok` (receipt `receipts/census-blind-at-head.out`; patch text
`claims/c3/CR-5/proposed-g2-positive-floor.patch.md`, NOT applied). So the
instrument can certify neither its own scope nor its own detection; the
audit must re-check locus-count invariance across the edit (before: PROVINCE
6 / SCORECARD 9 / SKILL 2 loci; current-ok loci 10) in addition to the diff.

**A4 — "the whole claim is a no-op" (PASS→PASS disposition).** Attempted
against the frozen claim: its falsifiable before→after is "verdict at HEAD
before the re-key (recorded verbatim) → PASS 0/0/0/0 at the records commit".
At HEAD the verdict is already PASS, so the measured movement is PASS→PASS
and the "re-key" branch of the claim does not fire (0 stale-bound, 0
retire-candidates — my re-derivation + PL-3 §2). Verdict: the charge lands
*partially* — the round's freshness movement cannot rest on a manufactured
FAIL→PASS; it rests on (a) the instrument-revision flip on one tree
(v9@HEAD FAIL undeclared=2 → v10@HEAD PASS, both measured), (b) the E22
reproduction at its own tree, and (c) the *accuracy* of the header
disposition (my A2 receipts adjudicate it). Residual risk to flag to the
parent: if the round records do not append an E22 disposition sentence
(the debt line at SCORECARD.md:850-852 still reads "re-key or retire next
calibration round"), the debt stays nominally open in the card while the
instrument header says discharged — record both, or the disposition is
one-sided.

## 5. Blockers

- **EX-28 had not landed** at report-write time (~20 min into the wave; 25
  polls). If it lands, re-run: `tools/scope-diff.py` before/after, the
  falsifiability suite against the after-instrument, `tools/independent-census.py`,
  and a shelter injection inside any new DATED region.
- **/tmp is EDQUOT** for this user (13 G/16 G tmpfs by other seats' scratch;
  even a 5-byte write fails while 3.1 G shows free). Scratch relocated to
  `/dev/shm/cr5/` (same tmpfs semantics, different mount, works); noted as a
  deviation from the "scratch under /tmp" rule with cause.
- `.ufo/gates/__pycache__/` (untracked) appeared during the wave — not
  written by this seat (my runs execute the census as a script, which does
  not byte-compile it); flagged as a hygiene item for the parent.
