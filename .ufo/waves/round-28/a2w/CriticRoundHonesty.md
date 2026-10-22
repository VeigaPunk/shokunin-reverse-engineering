# CriticRoundHonesty — round 28 report honesty given the R28-C1 miss

Seat: KaidokuR28a2.CriticRoundHonesty (critic, attempt 2, wave a2w). Attacked: the wording the round report, SCORECARD and LOG must carry, and the round-28 text already written at lane tip `9db24c9e10287d44d9f780d782ab608f3c84ff5a` plus the L1's uncommitted `PROVINCE.md` and `corpus/README.md` lines (working tree read 18:25:35Z; PROVINCE.md sha256 `219150b3…ea30`). Installs: none. No lane file written other than this report.

## Measurements (observation)

- `python3 -I -B tools/round-28/c1-heldout-naming.py --root <LANE> --rev 9db24c9e…` at 18:24:33Z, exit 1: `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1`; `FAIL h09: exit 1; operation differs; …`; `primary rule openchain_sole_unfiltered_args_consistent: named 137, right 137, wrong 0, no_name 50`.
- `python3 -I -B tools/round-28/c2-filtered-flag.py --root <LANE> --rev 9db24c9e…` at 18:24:35Z, exit 0: `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1`.
- Timing (`git log --format='%h %cI'`; `runs.tsv` line 10): h09 run `2026-10-22T17:17:34Z` exit 1; C2 freeze `86fa8526` at 17:21:55Z; C1 runs committed `ca4069a4` at 17:22:32Z. So R28-C2 was declared about four minutes after the h09 refusal was observable (also stated in `.ufo/waves/round-28/claims-c2.json:4`).
- `git grep -n -E 'round-27-verifier-spotcheck|rejected-honest-stop' 9db24c9e -- SCORECARD.md LOG.md` returns only the round-24 decision lines (SCORECARD.md:3049, LOG.md:2954) and the calibration row; no line records the round-27 outside decision.

## Rules applied

- R1 `/home/vgpnk/Projects/shokunin/AXES.md:34-36`: "A round is admitted only if every claim verifies and no axis is harmed … report every verdict and let the operator rule." Same rule: `templates/round-prompt.md:37-40` (fleet root).
- R2 `corpus/QUALITY.md:44` (row 34): "the original target decides the verdict"; a revised or replacement result "never substitutes"; SCORECARD and LOG record each outside closure decision "before the next round's claims are measured".
- R3 `.ufo/waves/round-28/claims.json:40`: target is the conjunction `runs_ok 61/61, rows_complete 187/187, tally_equal 1, entry_ok 1, exit 0`; `:41` H1 and H2 are "reported not target".
- R4 precedent `corpus/lessons/round-27-verifier-spotcheck.md:16-20` (one miss gives `rejected-honest-stop`), `:80-83` (not narrowed, no substitution; "this closure does not count it"), `:116` (missed claim's axis `unchanged`, "No harm"), `:156` ("Round 27's C1 stays a miss and is never re-scored").
- R5 SCORECARD.md:3090, :3096, :3101 and LOG.md:2972: round-27 heading carries "(honest stop, 15 of 16)", the claim row's verdict is "target missed: honest stop", and "The claim as frozen is not met, and this card does not count it."
- R6 `SKILL.md:395`: "Before any claim of "held"" needs a run this round with a cited evidence id; `corpus/README.md` uses "held narrowly" as the verified status (lines 70-75).

## Required statements (exact text; the L1 may fill the bracketed revision)

1. Round heading, SCORECARD and LOG: `Round 28 — held-out test of the round-25 EVM naming rule (honest stop, 60 of 61 runs) and openchain's filtered flag from Sourcify code` (R5).
2. R28-C1 claim row, verdict cell: `target missed: honest stop. runs_ok 60/61, rows_complete 186/187, tally_equal 1, entry_ok 1, exit 1 at 9db24c9e. REA 6.5.0 refused carrier h09 (invalid_format; unlinked-library placeholder, M28-1). The target is not narrowed, the counter is not changed, and h09 is not re-run or replaced.` (R2, R3, R4 :80-83, :156).
3. After the C1 row: `The claim as frozen is not met, and this card does not count it. The held-out triple (named 137, right 137, wrong 0, no name 50) and H1/H2 are observations, not the claim's result.` (R5 :3101, R3 :41).
4. R28-C2 claim row: `target met: responses_complete 230/230, entries 246, mismatches 0, predicted_true 59, entry_ok 1, exit 0 at <measured rev>.` Never "verified" or "admitted": verification is the outside closure's (R1; `templates/round-prompt.md:128-129` "Driver completion is not admission").
5. Declaration order: `R28-C2 was declared and frozen at 86fa8526 (17:21:55Z), after the R28-C1 run on h09 (17:17:34Z) was refused. It is a separate claim on the depth axis; it does not replace, offset or repair R28-C1.` (R2 "never substitutes").
6. Admission: `Round 28 does not meet the admission rule (AXES.md:34-36: every claim verifies): R28-C1 missed. The lane does not self-admit; the outside closure rules. Expected outside status, by the round-27 precedent: not admitted, rejected-honest-stop (inference).` (R1, R4 :16-20).
7. Axis verdicts table: coverage `unchanged` (R28-C1 missed; score 10 → 10; not harmed); depth `improved — lane self-assessment, R28-C2 target met; finite proxy 10 → 10, delta 0; outside closure rules`; calibration, operability, freshness, adjacency `unchanged — not claimed`. No axis harmed. (R4 :116; claims.json `not_claimed` says calibration is not claimed.)
8. Round-27 outside decision (missing at the tip; R2 ordering already missed): `Outside decision on round 27 (corpus/lessons/round-27-verifier-spotcheck.md:16-20): not admitted, rejected-honest-stop (R27-C1 missed at 15/16; R27-C2 met). Recorded late: round 28's claims were measured (ca4069a4, a2673116) before this line, so QUALITY row 34's ordering clause failed this round.` Same line in the LOG round-28 entry.
9. Recipe A count rising with the two new entries is reported as a count only, as round 27 did (SCORECARD.md:3098): `the coverage row keeps its round-26 measurement`.

## Forbidden phrasings (each presents C1 as met or partly met)

| phrasing | why forbidden |
|---|---|
| "C1 met on 60 valid carriers", "60/60", "186/186", "met except h09", "met with one disclosed exclusion" | changes the frozen denominator (R3 :40; R4 :80 "not narrowed") |
| "partly met", "mostly met", "98%", "4 of 5 target fields met", "tally_equal and entry_ok met" | the target is one conjunction ending in exit 0 (R3 :40); sub-fields are listed only under "target missed" (R5 :3096) |
| "substantively met", "met in spirit", "the rule held out of sample" as a claim verdict | H1 is reported, not a target (R3 :41); "held" is the verified status (R6) |
| "missed because of an REA limitation" or "REA defect" | REA's refusal is correct: the file holds `__$…$__`, not hex (S086 `:74`); the cause is the lane's freeze (M28-1, `corpus/lessons/round-28.md:42`) |
| "C1 met after linking h09" or any re-run, re-score or replacement envelope | R2 "never substitutes"; R4 :156 "never re-scored" |
| "one of two claims met, round partly admitted", "C2 carries the round" | no partial admission exists (R1) |
| "round 28 admitted" / "verified" in any lane file | the outside closure rules (R1; round-prompt :128-129) |
| "coverage improved" (from C1 or from recipe A 110 → 112) | missed claim gives `unchanged` (R4 :116); recipe A is index integrity only (SCORECARD.md:23) |
| "calibration improved" from the eight routed-defect fixes | hygiene, not a claim (claims.json `not_claimed`) |

## Attacks on text already written

- A1 fails: uncommitted `PROVINCE.md:94` reads "Round 28: the round-25 primary naming rule held out of sample at 0 wrong of 137 named (… claim missed at 60/61 runs …)". "held" is the lane's verified status word (R6), and it leads, with the miss in a parenthesis. Correction: `Round 28 (claim missed, 60 of 61 runs; Frontier status unchanged): on the held-out selectors the round-25 primary rule named 137, right 137, wrong 0, no name 50 (one snapshot, lane-invented names).` The same line's C2 clause "is set only for 36 canonical-list selectors" drops the limits that `corpus/README.md:78` keeps ("deployed revision assumed, one fetch instant"); add them.
- A2 holds: `corpus/lessons/round-28.md:13-15` ("**Missed:** … Honest stop") and the entry `…r28-evm-heldout-selector-naming.md:13`, `:22-23`, `:60` state the miss and say the numbers "do not make the claim met". Residual risk, not a defect: the entry title (`:5`) gives "named 137, right 137, wrong 0" with no miss; smallest correction: append "(claim missed, 60 of 61 runs)" to the title.
- A3 holds: uncommitted `corpus/README.md:77` uses "measured, claim missed", not "held narrowly". Counterexample not to copy: `corpus/README.md:76` (committed, round 27) labels the missed R27-C1 entry "held narrowly".
- A4 fails (observation): the round-27 outside decision is absent from SCORECARD.md and LOG.md at `9db24c9e` while round-28 data is measured; correction is statement 8.

## Verdict

Wording at the tip: holds for the lesson and the C1 entry; fails for PROVINCE.md:94 (uncommitted) and for the missing round-27 decision record. Impacted axes: calibration (self-assessment honesty), coverage (C1 verdict). Unknown: whether the outside closure treats the late round-27 record as a routed defect or a harm.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticRoundHonesty/`)

- `c1-heldout-naming-at-9db24c9e.txt` sha256 `dc4005462f8392e0744f5a323dc7a7edf3aa39bd8f8b9d45f51719edf180dede`
- `c2-filtered-flag-at-9db24c9e.txt` sha256 `ab150c68d925a023db484a359765be2a8dac52b84991f73afd62f6c1eef1c0a9`
