# Round 75 — declared claims (frozen; no amendments after this file's container commit)

Base `3c15a156239af06114e1ece8d1044a0d8205379b` (the round-74 lane tip: the record, the
report and the round-74 non-author spot-check lesson; the lane tree is clean and pushed).
Two claims on two distinct axes, causally separable — each is scored by its own instrument and
none reads the other's result. Both are capability acquisitions in the AXES sense: the
instrument runs, its output verifies, and its row enters the SCORECARD capabilities table in the
same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies and are tied; the stagnation nudge's waiver condition is *not* met
(capability rows entered in rounds 72–74, inside the 10-round window), so no waiver is claimed.
**`lowest-axis: calibration`** — R75-C2 works a tied-lowest axis. The round-74 closure admitted
the same tie and worked two axes; a tie has no unique lowest member.

The round-74 non-author spot-check routed eight defects to this round
(`corpus/lessons/round-74-verifier-spotcheck.md` §6) and the round-74 record's `planned` list
carried items (a)–(e). This round's work is that queue, resolved as follows:

- routed defects 3 and 4a (the cross-binding and the three A12 survivors) + item (a) → **R75-C1**;
- routed defects 1, 2, 4b, 5, 6 and 7 (the `--validate` evidence, the S275 re-log, the four
  cosmetic atom passes, the D14/D15 coverage limits, the SentinelScope code items, the
  retrospective-row convention) → **R75-C2**;
- routed defect 8 (a report rounding: 4/15 printed as 27%) is cosmetic and is corrected in the
  report, not atomised; **D20** records that reason.

## R75-C1 — operability: the A12 case set becomes independent, and its three survivors close

**Type.** Capability acquisition. The round-74 wave found three A12 selftest survivors outside
the frozen class set and one cross-binding: `home_under`/`tmpdir_under` are compared with
`is True` while every fixture feeds a real boolean; `_name_samples` keeps one sample per shim
name, so a last-wins (or first-wins) mutation hides a dirty launch behind a clean one;
`lie_clean`'s exact key list can be replaced by a superset test; and deleting the
`canary_present` field also failed `a12-kernel-multiple-samples`, so the canary-field case was
not the sole detector its row claimed.

**Falsifiable before → after.** At the base, the fourteen-class patch set `r75base` applied to
`tools/round-74/seam-probe.py` scores ten killed and **four survivors**
(`d-home-under-truthy, d-tmpdir-under-truthy, d-name-samples-last-wins, d-lie-clean-superset`),
pristine 20 cases green, and `b-drop-canary-field` fails two cases
(`a12-kernel-multiple-samples`, `a12-kernel-canary-field`) — the cross-binding. At the landing,
the fifteen-class `r75probe` applied to `tools/round-75/seam-probe.py` scores **zero survivors**,
every mutant killed by its declared case, and `b-drop-canary-field` fails exactly its one case.

**Predicate (one sentence, frozen).** R75-C1 is verified iff the frozen battery
`tools/round-75/probe-mutation.py`, run at the measured revision as
`python3 -I -B tools/round-75/probe-mutation.py --root . --rev <measured> --tool
tools/round-75/seam-probe.py --patch-set r75probe --work <scratch> --expect-survivors 0
--expect-target-sha256 <the r75 probe's sha256 at <measured>> --expect-sole
b-drop-canary-field --json-out <receipt>`, exits 0 with `survivor_count 0`, every mutant
`killed` with its `expect_case` in its `failed` list, `sole_detector["b-drop-canary-field"]`
true with `failed == ["a12-kernel-canary-field"]`, `pristine {cases 25, failed [], rc 0}` and
`target_pin {matched true, pinned_before_exec true}` — while the same battery with
`--patch-set r75base --tool tools/round-74/seam-probe.py --expect-survivors 4
--expect-survivor-names d-home-under-truthy,d-tmpdir-under-truthy,d-name-samples-last-wins,d-lie-clean-superset`
exits 0 reporting exactly those four survivors and `b-drop-canary-field` not sole.

**Counting command.** The two battery commands above; `survivor_count` is the counter.

**Kill rule.** A survivor; a mutant killed by a case other than its declared one
(`killed_wrong_case`); a pristine selftest that is not green or shorter than 25 cases; an
unpinned target or a pin compared after execution; a base arm that does not name all four
survivors or that makes the canary field sole → not verified, reported, never narrowed.

**Do-nothing control.** `tools/round-75/controls.py` arm `c1_base_world` (the round-74 blob:
four survivors and the canary cross-binding) and arm `c1_no_declared_cases` (the round-75 probe
with the seven closed case names renamed, assertions unchanged: those mutants are
`killed_wrong_case` and no kill — a red selftest alone does not satisfy the claim).

## R75-C2 — calibration: the record audit's atom grammar becomes exact

**Type.** Capability acquisition. The round-74 audit's D9–D12 passed on four cosmetic
constructions the wave demonstrated (a used-by cell that negates the path it names, a
search-log line carrying only the tokens, an erratum that reverses the two values, a rejected
row with an empty flip), and its D14/D15 did not reach the routed receipt or the plan's tool
set. Round 75 replaces those predicates with exact grammars (parsed cells, required fields,
typed integer counts, receipt-bound values), adds a self-validation block to its own receipt,
and widens the binding atoms.

**Falsifiable before → after.** At base `3c15a156` the audit exits 1 with `mismatch_count 8`
naming `D16`–`D23`; at the landing revision it exits 0 with `mismatch_count 0` over the same
eight atoms and a defect-free `validate` block.

**Predicate (one sentence, frozen).** R75-C2 is verified iff the frozen audit
`tools/round-75/record-audit.py`, run at the measured revision as
`python3 -I -B tools/round-75/record-audit.py --root . --rev <measured> --json-out <receipt>`,
exits 0 with `mismatch_count 0` over its eight atoms `D16`–`D23`, every atom row `ok true`, and
`validate {defects [], atoms 8}` — while the same command at base `3c15a156` exits 1 with
`mismatch_count 8` naming exactly those eight atoms, and a committed
`--validate` receipt names the landing receipt with `defects []`.

**Counting command.** The audit command above; `mismatch_count` is the counter.

**Kill rule.** An atom true at base for a reason its routed defect names; an atom false at the
landing; a `validate` defect; an atom added, removed or re-worded after this freeze; a receipt
whose `validate` block is absent → not verified, reported.

**Do-nothing control.** `tools/round-75/controls.py` arm `c2_do_nothing` (the audit at base
`3c15a156`: all eight atoms false there) and arm `c2_red_fixtures` (each strengthened grammar
rejects its red fixture, so the four cosmetic passes are shown detectable).

**Instruments.** The five round-75 instruments the freeze pins are `tools/round-75/seam-probe.py`,
`tools/round-75/probe-mutation.py`, `tools/round-75/record-audit.py`, `tools/round-75/controls.py`
and `tools/round-75/freeze-pins.py` (the containment-hardened pin checker, routed defect 6).

## Frontier step (inside the claim cap, no extra claim)

- **SOURCES.md.** Two pages opened this round on **2026-11-04**: `proc_pid_cmdline(5)` admitted
  (`mined`, docs/A) — the leaf page round 73 mislabelled and round 74 rejected its umbrella for,
  now opened directly; and `environ(7)` rejected (it defines the C-level `environ` array, not
  the `/proc/<pid>/cmdline` interface). Both rows carry the round's own Gate quote and digest.
- **Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
  start: exit 0, 189 rows, 23 W04 warnings (receipt `.ufo/waves/round-75/l1/census-start.txt`).
- **Mistake mined.** Round 74 recorded `b-drop-canary-field` as the canary-field case's mutant
  while the multi-sample case also read that field, and the round-74 audit's D9–D12 accepted
  four cosmetic constructions. Both are the same class: *a predicate that tests for the
  presence of a token instead of the shape the token must have*. Captured by: the new
  `sole_detector` field and the four grammar red fixtures (`D20`).
- **Assimilation.** `merge/kaidoku/` does not serve these claims → `Assimilation: none`.
  `considerthese/` is absent in this lane (no directory).
- **Sourced claim.** R75-C1 cites S283 through
  `corpus/knowledge/2026-11-04-r75-a12-case-independence.md`.

## Waves

One v1 wave `r75-w1`, 14 seats: 5 executor, 2 scribe, 2 reviewer, 1 critic, 1 mutation-tester,
1 sentinel, 1 scout, 1 connector. Attack roles (reviewer/critic/mutation-tester) 4 of 14 = 29%.
One connector. The L1 holds the planner seat. No residual call.
