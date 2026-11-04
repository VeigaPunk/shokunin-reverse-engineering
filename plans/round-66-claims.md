# Round 66 claims — kaidoku-shokunin (attempt 1)

Base: `311079d869f068bc083a8d180977e49634120fdf` (lane tip at round start; `jj-lane.sh state` →
local = remote, ahead 0). Owned axes: coverage, depth, calibration — all at 10.0 on saturated
finite proxies (SCORECARD `## Saturation`). The stagnation nudge is **not** fired: the window is
N = 10 lane-rounds and a capability row entered the table in round 65; the lowest-axis obligation
is therefore live and is met by **calibration** (C2), one of the three tied-at-10.0 axes.

This round executes the two freezes the round-65 non-author closure routed (its routed defects 1
and 2) — the lane's own counter defects, mined as M65-2/M65-4 and M65-5. Two claims, distinct
axes, causally separable (different counters, different files, each verifiable without the other).
No fresh-start binding: of the last three closures, r63 was admitted, r64 and r65 each stopped
honestly on their own predicates, and no closure was rejected three times in a row.

Instruments were committed **before** this file at `78fa9666` (the QUALITY #33 order) with their
do-nothing controls; the carry-in LOG entry is `b5b02e1f`, an ancestor of this freeze commit
(QUALITY #34 and the M65-3 order check). Both were dry-run end to end at the base before the
freeze (QUALITY #83/#84): `l1/pre/dryrun-c1-verify.json` (5/5 arms, exit 0) and
`l1/pre/dryrun-c2-selfcheck-at-base.json` (equivalent true, hidden 3, mismatches 1, exit 1). Each
clause of both predicates is traced to the counter line that evaluates it (QUALITY #87), and the
predicate sentence is byte-identical in this file, `.ufo/waves/round-66/claims.json`, the
counter's `PREDICATE` constant and every receipt (QUALITY #68).

## R66-C1 — depth, counter repair: the closure counter's two boundaries and the skip-run claim

Round 65's closure routed M65-5: (C1-F1) the closure check ran **before** the setup probe, so a
cache written by that probe was invisible and the before-census absorbed it; (C1-F2) the entry
count was emitted but never asserted, so a truncated manifest passed; (Q5) `--skip-run` emitted a
synthetic `closure.ok: true` for a run that never happened. This claim is the NEW freeze that
repairs all three in a new counter, with the r65 bytes left frozen.

**Predicate** (byte-identical in this file, `claims.json`, `PREDICATE` in the counter, every
receipt):

> R66-C1 is verified iff the repaired closure counter passes all five of its boundary arms: a1 the guarded fixture probe leaves closure.ok true with an empty cache; a2 the same probe without -B or the bytecode env makes closure.ok false and names a .pyc path; a3 the frozen 30-entry toolchain manifest verifies with count_ok true; a4 a manifest one entry short reports entries 29 != 30 and closure.ok false; a5 --skip-run emits no closure object claiming ok.

Counter: `tools/round-66/closure-boundary.py --verify --repo <lane> --out <receipt>`
(`sha256 3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b`).
Exit 0 verified (5/5) / 1 not verified (each false arm named) / 2 could-not-evaluate.

Clause → line trace (QUALITY #87): a1 → `run_verify` arm block calling `closure_state` with
`fixture_probe(..., guarded=True)` and the `ok is True and cache_present == [] and count_ok`
condition; a2 → the same block with `guarded=False` and the `named_pyc` condition; a3 → the
`closure_state` call on `mod.CLOSURE` with `COUNT` and the `count_ok is True and entries == COUNT`
condition; a4 → the truncated-manifest call plus the `count 29 != 30` finding string; a5 →
`skip_run_receipt`, which returns `closure: None, closure_claimed: False`.

Kill rule: any arm false, an arm that could not be evaluated, a drifted or absent r65 instrument
(the `V1_PIN` check), an edit to the counter after this freeze, or a run that needs the counter's
predicate changed → the claim is **not verified**; the stop is reported, never re-predicted or
repaired in place.

Before-arm (do-nothing control, committed): `.ufo/waves/round-66/l1/controls/c1-do-nothing.json`
— the r65 instrument's own order and claims scored with the five frozen arm conditions:
**1/5** (a1 only). a2 fails because the pre-probe scan sees an empty cache while the `.pyc`
appears afterwards; a3 fails because r65 has no `count_ok` line; a4 fails because a scratch copy
of the r65 instrument with one `CLOSURE` entry deleted runs `--manifest` exit 0 with
`entries 29, ok true, findings []`; a5 fails because `--skip-run` emits `closure.ok true`.
After-arm: `--verify` at the freeze, 5/5 exit 0 (dry run already green at the base).

## R66-C2 — calibration, counter repair: recipe A verbatim, the hidden names, the atom count

Round 65's closure routed M65-2/M65-4: the r65 "date" arm was declared the superseded recipe but
was a different recipe (it filtered the population and emitted `population_dropped` as an
integer), the frozen "naming the files it hides" clause had no implementing line, and no counter
carried the predicate. At this base recipe A verbatim reports `knowledge_files 145`, `mapped 142`,
`missing` the three non-October names, `coverage_score 9.79`, `depth_score 10.0` (27/27 rule
blocks). The `## Owned axes` coverage row's head cites the round-53 `142/142` — stale against the
145 files at this base.

**Predicate** (byte-identical in this file, `claims.json`, `PREDICATE` in the counter, every
receipt):

> R66-C2 is verified iff the coverage self-check counter at the measured revision reports recipe_a_equivalent true, a non-empty recipe_a_hidden list, and mismatches 0 across its two self-assessment atoms, where at the base revision the same counter reports the cited fraction atom as a mismatch.

Counter: `tools/round-66/coverage-selfcheck.py --selfcheck --rev <rev> --out <receipt>`
(`sha256 1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`).
Exit 0 verified / 1 not verified / 2 could-not-evaluate.

Atoms (emitted): A1 `head-score` — the coverage row's head score equals the stem recipe's score at
the same revision; A2 `cited-fraction` — the row's cited `<mapped>/<files> knowledge files` equals
the stem recipe's `mapped`/`knowledge_files`. `mismatches` = the number of false atoms.
`recipe_a_equivalent` comes from `--equiv`'s extraction of the committed SCORECARD recipe-A block
at the same revision and a field-for-field comparison of its nine keys with `--recipe a`.
`recipe_a_hidden` is the explicit sorted list of knowledge stems recipe A's date-token numerator
cannot map.

Clause → line trace (QUALITY #87): `recipe_a_equivalent` → `recipe_a_equivalence`'s `diffs` over
`RECIPE_A_KEYS`; `recipe_a_hidden` → `recipe_hidden`, whose result is the emitted list tested for
non-emptiness in `selfcheck`'s `ok`; `mismatches` → `selfcheck`'s `sum(1 for a in atoms if not
a["ok"])`; the base arm → the same counter at `--rev <base>`, whose A2 atom is false.

Kill rule: an equivalence difference, an empty hidden list, any false atom at the measured
revision, an Owned-axes row whose declared shape cannot be parsed, a post-freeze counter edit, or
a counter whose atom list is not the two declared above → **not verified**; reported, never
narrowed.

Before-arm (do-nothing control, committed): `.ufo/waves/round-66/l1/controls/c2-do-nothing.json`
— the r65 instrument's date mode scored with the three frozen conditions: **0/3**.
After-arm: this round repairs the `## Owned axes` coverage row (head sentence re-derived at the
landing with the repaired stem recipe and the `recipe_a_hidden` list recorded) and scores
`--selfcheck` at the landing → `mismatches 0`, exit 0.

## Frontier step (not a third claim)

- `corpus/SOURCES.md`: one row opened this round — the CPython `sys.dont_write_bytecode` page,
  re-opened under **its own** scope (the environment variable sets the flag that `-B` sets), which
  round 65 rejected only as the *S266 anchor* for the switch's effect. Gate records URL, access
  date, located quote and the tier category. The C1 knowledge entry cites the row (**sourced
  claim**).
- One mistake mined into `corpus/lessons/round-66.md` `## Mistakes` with a red demonstration.
- Assimilation: none this round — the `merge/kaidoku/` jsc theme was adopted in round 64 and no
  remaining staged theme fits these two counter repairs; `considerthese/` remains absent
  (measured, `ls` at the base).
- The r65 knowledge-entry erratum and the report/LOG accuracy corrections (the closure's routed
  defects 3 and 4) land this round as work items, not claims.

## Round shape

One v1 wave, 12 seats (policy band 8–16): 3 executors, 1 reviewer, 1 critic, 2 mutation-testers,
1 sentinel, 1 scout, 1 connector, 2 scribes. Attack seats = reviewer + critic + 2 mutation-testers
= 4/12 = 33 % ≥ 25 %. One connector seat. The L1 holds the canonical planner seat (the validator
rejects a `planner` role). Seat outputs land under `.ufo/waves/round-66/w1/<seat>/`; the L1
integrates and lands. No residual call is planned.
