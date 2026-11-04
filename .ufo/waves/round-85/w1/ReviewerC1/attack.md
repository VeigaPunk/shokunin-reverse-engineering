# ReviewerC1 — attack on R85-C1 (predicate-bind calibration)

Candidate: `.ufo/waves/round-85/w1/ExecPredBind/candidate/tools/round-85/predicate-bind.py`, sha256 `a99f8f18c071d7496b07ea65795057484d10904e0501ad47ae6b9190dbfa9b12` (ExecPredBind's own DONE was present when I started). Plan: `plans/round-85-claims.md` at 91eeb72f. No candidate bytes were copied, edited, or moved; no lane tree writes; no git writes in the lane.

Verdict key: HOLDS = the candidate withstood the attack (refused the forgery, or accepted a case the plan text also accepts). FALSIFIED = a forgery was accepted, or the candidate's verdict contradicts the frozen plan text. UNTESTED = not run.

## 1. Independent re-measurement of the BASE do-nothing control (step 1)

Command: `python3 -I -B tools/round-84/freeze-precheck.py --root <lane> --rev 91eeb72f… --container pre/c1/F1.json --container pre/c1/F2.json --container round-84/claims.json --expect F1=FLAGGED --expect F2=FLAGGED --expect round-84=CLEAN --control instruments-only`.

- Re-run: F1 CLEAN, F2 CLEAN, round-84 CLEAN; `refused_expected 0`, `accepted_expected 1`, `control_fired true`, `met false`, `mismatches [F1:CLEAN, F2:CLEAN]`, exit 1.
- Disk receipt `pre/c1/base-freeze-precheck.json`: identical on every field except the expectation fields I did not copy. **Agree.** The do-nothing control misses both forgeries (refused 0/2), so it cannot reach the target. Re-run receipt: `receipts/base-recheck-rerun.json`.

## 2. Plan vs rule vs code (step 2): drift findings

The frozen sentence (plan §R85-C1, "Predicate") and the candidate's docstring/code disagree on four points.

- **D1 — `none` (decisive).** Plan: negation tokens are `not, no, never, without, neither, nor, cannot, none as a predicate qualifier`. Candidate: `none` "is deliberately NOT a token: the round-84 predicates read 'mismatches none'" (`NEGATION_RE` lacks `none`). The round-84 positive control `R84-C1` ("…with mismatches none…") and `R84-C2` ("…with survivors none, inconclusive none, pristine_failed none…") both have `none` in the same sentence as their counter path. Diagnostic (in-memory only, not a verdict; `receipts/out/diag-none.txt`): with `none` in the list as the plan writes it, the candidate's own check returns **FLAGGED** on the positive control (`PB_PREDICATE_NEGATED:R84-C1`, `…:R84-C2`), so the "round-84 container CLEAN" half of the target is unreachable under the literal plan list. The candidate reaches the target only by dropping a token the plan names. The kill rule's "a changed predicate … after the declaration" is therefore arguably triggered. The plan's phrase "`none` as a predicate qualifier" does not say whether that qualifier use counts; L1 must adjudicate.
- **D2 — "any" vs "at least one".** Plan: each claim's predicate "names at least one" path that satisfies (a)(b)(c). Candidate: "a claim is refused if ANY predicate path is negated", and it claims this is "Decision (declared with the plan)". The plan contains no such declaration; the claim is unverifiable against the plan. Observed effect: A01 and A02 are refused by the candidate and would pass the plan's literal "at least one" text.
- **D3 — "sentence" undefined in plan.** Candidate splits on `.`, `;` and newline. Plan says only "the same sentence". Observed: A04 (`not` in an earlier `;`-clause) is accepted (CLEAN).
- **D4 — empty claims and case.** Plan is silent on `claims: []` (its universal sentence is vacuously CLEAN) and on case (its token list is lowercase in prose). Candidate refuses empty claims (`CONTAINER_NO_CLAIMS`) and matches tokens case-sensitively.
- **D5 — exit code vs docstring.** Docstring: exit 0 "without --expect: every container CLEAN". Code: `met` requires `refused ≥ 1`, so an all-CLEAN run without `--expect` exits 1 (observed on A03, A04, … with `CLEAN []`). Observed: docstring/code mismatch.
- **D6 — the selftest encodes D1.** `none-token-is-not-negation` is a passing selftest case (21/21 pass), so the drift is pinned as correct behaviour.

## 3. Attack table (step 3)

Predicted verdicts were written to `receipts/predictions-before-run.tsv` before the first run. Attack fixtures are in sandbox commits `32304da6` (A01–A14) and `1d58b6f3` (A15–A16) of a scratch clone; copies in `receipts/attacks/`. Each row's evidence is `receipts/out/<id>.json`.

| id | attack | predicted | observed | verdict | evidence |
|---|---|---|---|---|---|
| A01 | (a) affirmative sentence 1, negated pinned path sentence 2 | CLEAN | FLAGGED `PB_PREDICATE_NEGATED:ATK-A01` (prediction wrong) | HOLDS (refused; D2) | out/A01-… |
| A02 | (a) as A01, negated path unpinned | CLEAN | FLAGGED `PB_PREDICATE_NEGATED:ATK-A02` (prediction wrong) | HOLDS (refused; D2) | out/A02-… |
| A03 | (b) `NOT` uppercase: "This container is NOT scored by …" | CLEAN | CLEAN | FALSIFIED: forgery accepted | out/A03-… |
| A04 | (c) `not` in quoted label, earlier `;`-clause | FLAGGED | CLEAN (prediction wrong; no over-refusal) | HOLDS (D3) | out/A04-… |
| A05 | (c) `not` in quoted label, earlier sentence | CLEAN | CLEAN | HOLDS | out/A05-… |
| A06 | (d) path pinned only under `producers_not_counters`, digest matches | CLEAN | CLEAN | FALSIFIED: a producer passes as counter (plan-admitted limit) | out/A06-… |
| A07 | (e) only path is `corpus/evidence/round-37/…/run.sh` | CLEAN | CLEAN | FALSIFIED: a non-counter script passes (plan-admitted limit) | out/A07-… |
| A08 | (f) `claims: []` with pinned instruments | CLEAN | FLAGGED `CONTAINER_NO_CLAIMS` (prediction wrong) | HOLDS (D4) | out/A08-… |
| A09 | second claim names no path | FLAGGED | FLAGGED `PB_NO_PREDICATE_PATH:ATK-A09b` | HOLDS | out/A09-… |
| A10 | predicate path pinned with zero digest | FLAGGED | FLAGGED `PB_PIN_MISMATCH:tools/round-84/freeze-precheck.py` | HOLDS | out/A10-… |
| A11 | `none` as qualifier only: "reports mismatches none" | FLAGGED | CLEAN | FALSIFIED against plan list (D1) | out/A11-… |
| A12 | `never` in the path's sentence | FLAGGED | FLAGGED `PB_PREDICATE_NEGATED:ATK-A12` | HOLDS | out/A12-… |
| A13 | "Known counter …" (substring `no`) | CLEAN | CLEAN | HOLDS (word boundary correct) | out/A13-… |
| A14 | path only in `kill_rule` (F1 variant) | FLAGGED | FLAGGED `PB_NO_PREDICATE_PATH:ATK-A14` | HOLDS | out/A14-… |
| A15 | "Counter … doesn't score this container." (contraction) | not predicted | CLEAN | FALSIFIED: negation not recognised | out/A15-… |
| A16 | "Counter … scores nothing for this container." | not predicted | CLEAN | FALSIFIED: negation not recognised | out/A16-… |

Predicted-verdict misses: A01, A02, A04, A08, and the `none` case A11 (I predicted FLAGGED from the plan list; the candidate drops `none`). A15 and A16 were not predicted and are added as extra probes.

## 4. Target check (C1)

Command (receipt `receipts/out/target.json`): candidate on F1, F2, round-84 with `--expect F1=FLAGGED --expect F2=FLAGGED --expect round-84=CLEAN --control instruments-only`, exit 0.

- F1: FLAGGED `PB_NO_PREDICATE_PATH:R85-F1` (exact match).
- F2: FLAGGED `PB_PREDICATE_NEGATED:R85-F2` (exact match).
- round-84: CLEAN, no findings.
- `refused_expected 2`, `accepted_expected 1`, `control_fired true`, `mismatches []`, `met true`, exit 0.
- The do-nothing control scores `refused_expected 0` (§1).

**Verdict:** the candidate reaches the C1 target as written in its receipt. It does so only because it removed `none` from the plan's negation list (D1); with the literal list the positive control is FLAGGED and the target is unreachable. The do-nothing control misses the target (refused 0/2). Target status: reached by the candidate, but not by the plan's frozen predicate text. The plan's own kill rule (a changed predicate) is arguably triggered; L1 must adjudicate.

Selftest of the candidate (`receipts/out/selftest.json`): 21 cases, 0 failures (this selftest pins D1 as correct).

## 5. Limits demonstrated

1. Case-sensitive token list: `NOT` / any capitalised negator is ignored (A03 accepted).
2. Closed token list: contractions and non-listed negators are ignored (A15 `doesn't`, A16 `nothing` accepted).
3. Counter-or-not: a path pinned as `producers_not_counters` (A06) or any `corpus/…/*.sh` (A07) satisfies the predicate. The plan admits both (its (b) and regex); the claim measures "named and pinned", not "is a counter".
4. Token `none` excluded (D1): a predicate "reports mismatches none" is accepted (A11). This is the same deviation that makes the positive control CLEAN.
5. Exit 1 on an all-CLEAN run without `--expect` (D5).
6. Declared in advance and not tested: a meaningless affirmative sentence ("X is a counter") still passes. UNTESTED.

## 6. Install / tooling

None. Python 3 stdlib only; no packages installed or upgraded.

## 7. Blockers

None for the attack. The C1 verdict depends on L1 deciding D1 (plan's literal `none` vs the candidate's omission).
