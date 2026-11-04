# Round 85 — a claim container refuses a counter named only outside its predicate; the r84 surviving-mutant probe becomes a frozen 21-row table

Base: `b3084c8c2036db966ce4750b4039bddaa84cc760` (lane `main`, clean, pushed). Attempt 1 (`watchdog.log`:
`launch kaidoku round=85 … attempt=1`; no earlier `lane-dead-no-report` line; dispatch evidence
`74b9b44f`). Round 84 closed admitted (`MANIFEST` rounds ledger; `corpus/lessons/round-84-verifier-spotcheck.md`).

Owned axes (lane prompt §1): coverage, depth, calibration. All at the saturation line 10.0 on their finite
proxies (`SCORECARD.md`, Owned axes table). Round 84 entered three capability rows, so the stagnation window
restarts and the nudge is not invoked. Calibration and depth are the two claimed axes; coverage is not claimed.

Claims are causally separable: C1 reads claim containers only; C2 reads mutant-table targets only.
Neither needs the other to land. Two claims, two distinct axes. Declaration is committed before any data:
the counters below are the frozen predicates; the pre-declaration BASE receipts (`pre/`) are the do-nothing
controls.

## Routed r84 items carried into this round (spot-check `corpus/lessons/round-84-verifier-spotcheck.md` §9)

- R1 (S302 durable pointer) — snapshot of `FirmwarePublication.js` (sha256 `bb4f3246…`) committed under
  `.ufo/waves/round-85/l1/sources/`, byte-equal to the npx-cache file. Not a claim; an evidence repair.
- R2 (S303 reason, "five scopes") — corrected by an appended lesson correction naming the seven rows
  S079, S080, S083, S090, S092, S119, S123 (counted, not asserted; `grep -c -F`). No in-place rewrite.
- R3 (M84-5 pointer prefix) and R4 (M84-4 no evidence pointer) — appended corrections in the round-85 lesson.
- R5 (planner seat) — the L1 holds the planner seat again; recorded as a deviation in the report.
- R6 (C2 kill binding is name-level) — partially addressed by C2 below: each kill must be the declared case
  failing under the mutant and passing on pristine. Still name-level for case *semantics*; disclosed.
- R7 (C1 naming-lint limit, C3 fixture pins, A3/A9) — C1 addressed below. C3 fixture pins and A3/A9 are
  **not claimed** this round and remain carried debt.

## R85-C1 — calibration: a claim's counter is named in its predicate, not only in its kill rule

Gap (measured at r84 landing, lesson `round-84.md` Limits): the prefreeze gate `tools/round-84/freeze-precheck.py`
accepts a counter path anywhere in a claim's strings, so a counter path that appears only in `kill_rule`,
or only inside a negated sentence, satisfies it.

Counter (new, built in this round): `tools/round-85/predicate-bind.py`, run as
`python3 -I -B tools/round-85/predicate-bind.py --root . --rev $REV --container <json> --expect <json>=<CLEAN|FLAGGED> … --control instruments-only --json-out <receipt>`.

Predicate (frozen sentence; the same sentence is the counter's rule): for every container, each claim's
`predicate` string names at least one lane-relative script path (`tools/|corpus/|.ufo/` + `.py/.sh/.mjs/.js`)
that is (a) a blob at `$REV`, (b) pinned in the container's `instruments`/`loaded_by_counter`/`producers_not_counters`
at its blob digest, and (c) not negated: no negation token (`not`, `no`, `never`, `without`, `neither`, `nor`,
`cannot`, `none` as a predicate qualifier — list frozen in the counter's source) appears in the same sentence
as that path. A path in `kill_rule` alone does not satisfy the predicate.

Fixtures (committed before this declaration as `.ufo/waves/round-85/pre/c1/`):
- `F1.json` — predicate names no counter; `kill_rule` names `tools/round-84/freeze-precheck.py`.
- `F2.json` — predicate names the counter inside a negated sentence ("… does not score this container …").
- Positive control: `.ufo/waves/round-84/claims.json` (the round-84 container; its three claims name counters
  in their predicates and nowhere negated).

Before (measured at the declaration revision with the frozen r84 gate `tools/round-84/freeze-precheck.py`):
F1 CLEAN, F2 CLEAN, positive CLEAN → forgeries refused 0/2. Receipt: `pre/c1/base-freeze-precheck.json`.

After (target): forgeries refused 2/2 (`F1`, `F2` FLAGGED with `PB_NO_PREDICATE_PATH:R85-F1` and `PB_PREDICATE_NEGATED:R85-F2`
respectively, exact findings); the positive control CLEAN; `mismatches []`; `control instruments-only` accepts
F1 and F2 (the cheap rule fires on them, so the target is failable and not satisfied by container shape).

Target (one predicate): `predicate-bind.py` reports F1 FLAGGED with exactly `PB_NO_PREDICATE_PATH:R85-F1`,
F2 FLAGGED with exactly `PB_PREDICATE_NEGATED:R85-F2`, the round-84 container CLEAN, each equal to its
`--expect`, `mismatches []`, `refused_expected 2`, `accepted_expected 1`, `control.fires true`, exit 0.
A do-nothing control (the unchanged r84 gate) scores `refused_expected 0`, so it cannot reach the target.

Kill rule: any verdict or expectation mismatch; a positive control not CLEAN; F1 or F2 not FLAGGED with its
exact finding; the control not firing on F1 and F2; a counter path in the predicate that is not a blob or not
pinned at its digest; a changed fixture, expectation, or the predicate sentence after the declaration.

Limit (declared in advance): a naming-and-negation lint. A predicate that names the counter in an affirmative
but meaningless sentence still passes. This is a limit on what the claim measures, not a retirement.

## R85-C2 — depth: the r84 probe's surviving mutants close at declared cases

Gap (measured at r84, `.ufo/waves/round-84/w1/MutationTester.md`, 24-row probe at `fa92d34`): 22 of 24
probe mutants survived the frozen detectors; 15 are genuine gaps with no covering case. The frozen r84 table
(13 rows) is closed and stays frozen.

Table (frozen by this declaration): `.ufo/waves/round-85/mutants.json`, 21 rows = the 24 probe rows minus three
verdict-neutral rows (`pc-pin-traversal-basename`, `pc-token-unbound-maxlen`, `pc-battery-verdict-drop-sourced`,
excluded with reasons in the table). Each row carries its target (`tools/round-82/printed-command.py`,
`tools/round-83/source-bind.py`, `tools/round-82/conjunction-gate.py`), its find/replace, and its declared case.
Declared cases for the 15 genuine gaps, two conditional rows and the BASE-covered rows are new names unless the
BASE measurement shows them present.

Counter (unchanged, frozen r84 instrument): `tools/round-84/mutation-closure.py`:
`python3 -I -B tools/round-84/mutation-closure.py --root . --rev $REV --mutants .ufo/waves/round-85/mutants.json --work $HYAKU_SCRATCH/kaidoku-r85/L1/c2 --json-out <receipt>`.
Its kill binding: the declared case must appear in the mutant's failing-case list and in the pristine
inventory; pristine must be green.

Before (measured at the declaration revision, the do-nothing control): see `pre/c2/base-mutation-closure.json`.
Declared target is fixed now and not moved after data: **killed ≥ 16 of 21**, with pristine green for all three
targets. A do-nothing control (no tool edits) kills the BASE count shown in the receipt; if that count already
reaches 16, the target is wrong and is fixed before any wave data (r84 rule).

After (target): killed ≥ 16 of 21 at the measured revision; pristine green for `tools/round-82/printed-command.py`,
`tools/round-83/source-bind.py`, `tools/round-82/conjunction-gate.py`; and the frozen r84 table
(`.ufo/waves/round-84/mutants.json`, 13 rows) still kills 13 of 13 at the measured revision (regression arm,
same counter).

Kill rule: any pristine red target; any kill not bound to its declared case; any frozen-13 regression; an anchor
count ≠ 1 for any row at the measured revision; a table edited after the declaration (its sha256 is pinned in the
container's `fixtures`); a changed target instrument without an `instrument_supersessions` entry naming the reason;
a removed or weakened existing case in the three targets.

Limit (declared in advance): a kill still binds a case *name* to a failing run. A fabricated case that asserts
the declared failure would also score; semantic certification of each case is not claimed (routed R6, carried).

Sourced claim (CORPUS.md §SOURCES rule 1; §2b item 4): the round-85 knowledge entry on mutant-kill binding cites
`S304` (Papadakis et al., "Mutation Testing Advances: An Analysis and Survey", Advances in Computers 112, 2019,
DOI 10.1016/bs.adcom.2018.03.015), opened this round by the scribe seat with its own access date and a
≤25-word located quote recorded in the lesson's `## Gate`. The entry's claim is that a mutant counts as killed
only by an observed behavioural difference, which is what the declared-case binding measures.

## Frontier step (§2b, every child-lane round)

1. `corpus/SOURCES.md`: one new row `S304` (opened this round), tier **B** (survey), scope mutation-testing
   survey. Census before→after with `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
   (exit 0 at round start: `kaidoku ok …/corpus/SOURCES.md`, 27 W04 warnings) and the frozen manual census.
2. Mistake mined (`corpus/lessons/round-85.md ## Mistakes`): M85-1 — the r84 spot-check's routed R2/R3 errors
   (a count "five scopes" for a seven-row URL; a `l1/waves/round-84/` pointer that does not resolve). Captured-by:
   none. Fix: a pointer-resolution sweep over the lesson that must show red on the r84 wording and green after the
   appended correction.
3. Assimilation: `Assimilation: none` — this round's claim budget is C1 + C2; `considerthese/` does not exist for
   kaidoku (one report line says so); `merge/kaidoku/` is not drawn on this round.

## Wave (declared before dispatch)

One v1 wave, `r85-w1`, 11 seats, within the 8–16 band: executor ×3 (ExecPredBind: C1 counter; ExecPrintedCmd:
the 15 `printed-command.py` rows; ExecSourceBind: the 4 `source-bind.py` and 2 `conjunction-gate.py` rows);
scribe ×2 (ScribeSource: S304 row and knowledge entry draft; ScribeLesson: round-85 lesson, Gate, Mistakes, appended
corrections R2–R4); scout ×1 (ScoutSurface, read-only insertion-point map); reviewer ×2 (ReviewerC1, ReviewerC2);
critic ×1 (CriticClaims); mutation-tester ×1 (MutationRemeasure); connector ×1 (sibling-overlap scan). Attack seats
are reviewer 2 + critic 1 + mutation-tester 1 = 4 of 11 (36 %). One connector seat. The L1 holds the planner seat
(the validator excludes `planner`; R5). Seats write only under `.ufo/waves/round-85/w1/<seat>/`; the L1 is the sole
integrator into the lane tree.
