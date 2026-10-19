# PL-3 — chain c3, planner — plan for the census v10 scope-table re-key at HEAD

Wave arc3-loop1-round1 · 2026-10-19 · HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(no seat commits; all PL-3 work read-only + in-memory, zero scratch writes).
Task: plan C3 (census v10 scope-table re-key at HEAD): measurement-first design —
run at HEAD, capture verdict, classify scope rows current/stale-bound/dated,
re-key or retire-with-cause per row, with the r4 laundering-refusal and r3
adjudicated-not-edited precedents as constraints.

**Status: COMPLETE.** Artifact: `claims/c3/PL-3/plan.md` (14.4 KB).

## 1. Work performed (each bullet with an evidence pointer)

- Read the frozen claims + rules: `.ufo/waves/arc3-loop1-round1/claims-frozen.md`
  (C3 claim, cross-cutting rules, roster).
- **Measured the census at HEAD**: `python3 .ufo/gates/c1-census-v10.py` →
  `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0,
  stdout sha256 `3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418`
  (re-hashed by PL-3; byte-identical to EX-26 ×2 / EX-29 / SC-6 / RV-11 captures —
  five independent runs, one digest).
- **Row classification, all 20 SCOPE rows** (method + result in plan.md §2):
  7 CURRENT + 13 DATED aligned; **0 stale-bound; 0 retire-candidates**; markers all
  present (`SCOPE-ERRORS: []`). Evidence: PL-3 in-memory classifier
  (`importlib` load of the instrument + its own `classify()`/`assert_markers()`);
  corroborated by `claims/c3/EX-26/scope-alignment.txt`,
  `claims/c3/EX-29/{scope-audit,row-locus-counts}.txt` ("Blocks NOT attributed to
  any row: (empty)") and CR-5's independent re-derivation (0 out-of-range).
- **E22 reproduction (the debt's own tree)**: recovered v9 (RV-11,
  `scratch/c1-census-v9-recovered.py`, sha256 `213fe679…` matching E22's claim) —
  `679af5d` (766-line card) → **FAIL undeclared=2** at blocks 731-737 / 747-766
  (round-2's records append past the 701 bound); `b21c0da` (701-line) → PASS.
  Re-ran the same recovered v9 against HEAD first-hand: **FAIL, exit 1** —
  `SCOPE-ERRORS: ["SCORECARD.md:635 marker '2026-10-18' absent from ''"]` +
  undeclared=2 (blocks 732-738 / 748-767). So the r4 v10 re-key + r8 +1 shift are
  **load-bearing**; the frozen "FAIL at HEAD" framing is not v10's state.
- **Tail scan**: undeclared tails PROVINCE 132-162 (31 lines), SKILL 21-371 (351),
  SCORECARD 856-1336 (481) — **0 gated loci** at HEAD (EX-26 §4.1 classify probe +
  raw grep; CR-5 same; PL-3 attacks A2/A5c independently).
- **Precedent reads** (constraints): `git show 6bc4c29 -- .ufo/gates/c1-census-v10.py`
  (r8 re-key = pure +1 bound/marker shift of three DATED rows, "SCOPE +1");
  `git show 265e1aa` (v10 birth = "two fixed-bound DATED rows + RECEIPT widening");
  Z1 arc2-loop1-round4 §4d ("the commit that appends the round-4 records section is
  the commit that moves the bound"); r4 laundering measurements (E14 §3.6, E15,
  P3:45, P4:204, Z1:40,301) and SCORECARD.md:908 ("fixed-bound re-key; laundering
  path refused"); r3 "Dated records adjudicated, not edited" (SCORECARD.md:789-791).
- **Wrote the plan** `claims/c3/PL-3/plan.md`: measurement procedure M1-M5 (with
  status), row table, tail table, records-commit decision tree + re-key template,
  attack table, EX-28 header edit spec + verification, constraints, remaining work.
  §9 addendum folds in CR-5 / SC-6 / RV-11 landings (see §4 below).

## 2. Proposed changes

- **None applied by this seat.** The plan's §6 specifies EX-28's header-disposition
  edit (base: `claims/c3/EX-26/proposed-census-header-disposition.patch.md`,
  extend with the E22-tree reproduction + v9@HEAD flip + r8-necessity + the CR-5
  self-certification caveat); §4(ii) carries the records-commit re-key template as
  text (fixed-bound DATED row, marker = heading line, receipt language in each
  locus block). The census write target belongs to EX-28 alone; no patch was
  applied and no repo file was modified by PL-3.

## 3. Before→after measurement (chain c3)

- **Frozen "before"** ("census FAIL undeclared=2 at HEAD"): **not reproducible with
  v10 at HEAD** — measured PASS 0/0/0/0, exit 0 (sha `3b677b8e…`).
- **Reproduced where it is real**: v9@679af5d FAIL undeclared=2, exit 1 (the E22
  finding verbatim); v9@b21c0da PASS; v9@HEAD FAIL, exit 1 (marker@635 +
  undeclared=2) — PL-3 re-ran all three against RV-11's recovered instrument.
- **Discriminating before→after on one tree**: **v9@HEAD FAIL → v10@HEAD PASS**
  (treatment = the r4/r8 re-keys, proven load-bearing). PASS→PASS without the flip
  would be a no-op disposition; the plan records the flip as the falsifiable unit.
- **Command A unchanged** (T0): EX-30 `recipeA-t0.txt` → 81/81, 13/13, 10.0/10.0;
  `git status --porcelain -- corpus/` empty (EX-30 `gitstatus-corpus-t0.txt`).
  T1 pending EX-28.
- **M5 (records commit)**: pending by construction — the template + coupling rule
  are in plan §4 for the parent.

## 4. Attacks / refutations run or attempted, with verdicts

PL-3 in-memory harness (instrument's own functions, files deep-copied; zero fs
writes) — full table in plan §5:

- A1 marker stripped at SCORECARD:636 → **FAIL** SCOPE-ERROR (G15 fires).
- A2 records append carrying `rea-agents@6.5.0` in the undeclared tail → **FAIL**
  UNDECLARED=1 (fail-closed holds — the live records-commit hazard, simulated).
- A3 same append tagged inline `historical, superseded` → **still FAIL**: G16
  re-labels the live-equal value `current-ok` (c1-census-v10.py:336-338) before the
  inline-marker branch (:344-345) can excuse it — the escape hatch is narrower than
  its name (refutes "tag it historical and it passes").
- A4 one blank line inserted at SCORECARD:636 → **FAIL**, 3 SCOPE-ERRORs
  (markers 636/704/769 missed) — shift drift is caught.
- A5 re-key simulation (new fixed-bound DATED row [1338,1340]) → **FAIL on G11
  alone** (`g11=['SCORECARD.md:1340']`): live-equal values read current-ok inside
  DATED rows and the block needs receipt language; A5b (+ receipt language) →
  **PASS** (the template); A5c token-free append, no new row → **PASS** (preferred
  form).
- A6 overshoot bound 768→10**9 (the r4-refused path) + fresh stale claim at EOF →
  **PASS — laundering reproduced first-hand** (the claim reads `historical (dated
  scope)`); A7 modest overshoot (769→900) → FAIL (only launders up to its bound).
- A8 baseline restored → PASS (harness side-effect-free).
- Cross-seat: CR-5's self-certification attack (widened row → census still PASS;
  SCOPE is both object and oracle) — folded into plan §6/§9 as a certificate
  requirement; SC-6's A1-A4 fixtures agree with my A1/A2/A4 verdicts.

## 5. Blockers / environment

- **`/tmp` EDQUOT for this user** (standing hazard, SCORECARD.md:990-991): even a
  tiny write failed (`cat: write error: Disk quota exceeded`). PL-3 therefore ran
  the entire harness **in memory** (no scratch files anywhere); `/tmp/pl3` was
  created once and removed. EX-30/CR-5 relocated scratch to `/dev/shm` with cause.
- `.ufo/gates/__pycache__/` recreated by module-import audits (mine and others') —
  removed by PL-3 at close (07:06); concurrent seats' imports may recreate it; the
  class is recorded in EX-26/CR-5/SC-6 reports.
- **EX-28 had not landed** (census sha256 unchanged `36e96cd5…`); the header edit
  and the records-commit re-key decision are open. **M5 (records-commit PASS)** is
  parent-side. Gap named, not blocked on.
- **Post-report landings (checked before close, ~07:12Z)**: RV-10 (reviewer) landed
  **CONFIRMED — no laundering**: no landed instrument version carries an
  open-ended/overshooting bound (max declared end 855); the synthetic stale append
  reads UNDECLARED under the fixed bound and is swallowed under both relaxed
  variants — this independently validates the plan's §4/§7 refusal spec. SC-7
  landed the records drafts (census-header draft, LOG entry, SCORECARD section).
  VZ-3's report file was still empty at close.
