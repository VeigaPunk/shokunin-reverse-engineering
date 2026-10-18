# kaidoku arc2-loop1-round5 — verification: the calibration audit that caught a parent defect

Date: 2026-10-18. Wave: 60 seat items (the declaration said 64 — the audit
caught the slip; see C2), `openai-codex/gpt-6-luna-max`, one batched call,
60/60 delivery. Work commits: `9ce9ff9` (lesson + receipts), `3f4a685` (wave
artifacts). P2's mid-wave LOG append rides in this commit's LOG changes
(content accurate; deviation recorded).

**Round admitted: all three claims verify** — because the audit found real
discrepancies and dispositioned every one.

## Work performed

Claims (3, distinct axes; verification-round shape per schedule):

1. **C1 — calibration** (owned): audit every falsifiable before→after
   recorded in rounds 1-4, re-derived at its cited commit from `git archive`
   trees (fidelity independently verified: 1,458 paths byte-identical, V4).
2. **C2 — operability** (fleet): identify the cross-round "60/64" defect
   class and land a mitigation.
3. **C3 — freshness** (fleet): disposition the R1–R4 missed-item register
   per item.

The audit matrix (C1 connector, 20 rows): **13 confirmed, 7 dispositioned.**
Confirmed highlights: command A at all four work commits; r4's probe and
census; r3's scoped 6→0; r1's receipts, prefixes, and battery hashes; r4's
SHONEN refresh; archive methodology. Dispositions (all named in the SCORECARD
section): the arc's own dispatch-count records (C2), r2's 5+1 restatement,
receipt-scoping adjudications, the probe's --rev handling (named debt), CR4's
axis-honesty point, and the r3 honest-stop affirmations (E15).

The C2 investigation is the round's signature: reconstructing the roster
from round 1's complete 64-name set against the archived wave trees
(`b21c0da`, `dbba2dd`, `fc8e53c`) proved rounds 2-5 each dispatched 60 items
— the "4 non-completions" in three round sections were fictional, and the
real defect was the parent's count. Mitigation: the
`2026-10-18-wave-dispatch-counting` lesson (roster-freeze protocol;
count-the-items-array rule; re-dispatch protocol for true shortfalls).

Cross-domain evidence: none absorbed; the config surface stayed quiet after
the r4 post-pair (SC2: no custody-path churn).

## Landed changes

- `corpus/lessons/2026-10-18-wave-dispatch-counting.md` — the counting-slip
  case + standing rules + re-dispatch protocol. LOG: this entry; commit
  `9ce9ff9`. (README index row deliberately deferred — insertion would shift
  `corpus/README.md:177`, staling a landed pointer; caught pre-commit,
  reverted, named debt.)
- Receipts (post-pair 5/5 + MANIFEST) at `9ce9ff9`; wave reports at
  `3f4a685`.
- NOT landed (by audit verdict): zero unsafe source edits — the drifted-
  citation trio adjudicated (lessons:37 baseline-valid; LOG:685 dated;
  rubric.json:61 frozen), append-only corrections recorded in this round's
  section instead of rewrites.
- SCORECARD round section + this report: this commit.

## Before → after measurements

- **C1** — audit matrix: 20 audited / 13 confirmed at cited commits / 7
  dispositioned with named evidence (P1/P2/S2/E5-E15/C1-connector/R1-R8/
  CR1-CR8/V1-V6; Z1 convergence: 113 citations resolved, 0 unresolved).
  Independent sample re-derivation (V1, 4/4 rows) matched.
- **C2** — defect class: parent dispatch-count slip (declared 64, dispatched
  60, 60/60 completion in four consecutive waves). Correction convention:
  this entry + the round section name the superseded r2/r3/r4 lines.
- **C3** — register disposition count: every R1-R4 carried item now carries
  one of {adjudicated-NO-CHANGE, closed, named-debt, operator-owned}.
- **Side-harm check** — command A at `3f4a685`: 79/79, 11/11, 10.0/10.0
  (the lesson is corpus/lessons — outside the denominator); probe findings=0
  at HEAD; census v10 PASS at the records state.

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists: 11 rules + custody SOP +
  2-row registry + the counting lesson; command A 11/11 at `3f4a685`; no
  outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task: the verification audit itself (20-row matrix re-derived
  from archived trees) + the r4 battery precedents; receipts + this LOG
  entry; no outside verifier (`SHONEN.md:7-8`).
- [~] Executable without oral context: the audit commands replay from the
  matrix; the roster-freeze protocol is a standalone lesson;
  documentation-level only (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: operator surfaces recorded not touched; seat
  deviations (P2's LOG append) recorded with process notes; no complete
  outside audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

Stale-lane duty: single parent session; no live probes; all seat processes
closed; custody pair captured at both ends.

## Verdicts

- calibration: **improved** — the self-assessment record now matches
  re-derived state; the discrepancies are named corrections, not drift.
- operability: **improved** — the counting-slip class is identified, the
  protocol is standing craft, and the fictional-defect records are corrected.
- freshness: **improved** — the register is fully dispositioned with zero
  unsafe edits.
- depth / coverage: **unchanged** (command A at `3f4a685`).

Stagnation window 5/10. Regimen continues to round 6 — 128 seats on
`xai-oauth/grok-4.7-fast`.
