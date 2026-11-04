# Round 84 — claim metadata, mutation closure, and the nested container chain

Base: `043b89a25241710a68b45526c3287fb3c8d907c3`. Owned axes: coverage, depth, calibration,
freshness — all at 10 on their finite proxies (`SCORECARD.md` Saturation: line 10.0, window 10
lane-rounds). Round 83 landed calibration only; this round takes three claims on distinct
surfaces: calibration (claim metadata is mechanically bound to its counter), depth (the recorded
mutation-survivor set closes at its declared detectors), coverage (a Frontier edge class —
nested sub-images below depth 1 — becomes measured and governed). No stagnation waiver is
invoked: coverage/depth/calibration improvements are measured, not relabelled. L1 holds the
planner seat. Claims are causally separable: C1 reads claim containers, C2 reads tool selftests,
C3 runs REA on a fixture chain; none needs another's landing.

Round-83 outside review carried in (not rewritten): the full counter path belongs in claim
metadata before the freeze (C1); fixture identity and boundary cases must be pinned before the
next predicate (C2's declared cases are frozen in this plan); the 12-word git-diff quote is
corrected by an appended named correction in the lesson, not by rewriting the filed report.

## R84-C1 — calibration: a claim names its counter, the container pins it

Predicate: `tools/round-84/freeze-precheck.py` reports the round-83 container
`.ufo/waves/round-83/claims.json` FLAGGED with exactly `CLAIM_NO_COUNTER_PATH:R83-C1` and the
round-84 container `.ufo/waves/round-84/claims.json` CLEAN, each equal to its declared
`--expect`, with `mismatches []`, `refused_expected 1`, `accepted_expected 1`, and the
`--control instruments-only` rule accepting the round-83 container — the cheapest rule that
skips the per-claim work must not reach the target.

Counter: `tools/round-84/freeze-precheck.py` (full path; frozen by digest in
`.ufo/waves/round-84/claims.json`). The maintained post-hoc audit `tools/round-29/freeze-gate.py`
stays byte-unchanged: it reports round-83's freeze `FLAGGED INSTRUMENT_NONE` and exits 0 on the
disclosed ledger. This claim adds a prefreeze refusal; it does not rewrite the maintained gate,
the round-83 container, or any historical ledger row.

Before: at BASE the maintained audit audits 58 containers, flags `round-83`, and exits 0
(`.ufo/waves/round-84/pre/c1-maintained-gate-base.json`) — refusals 0/1. The cheap control
accepts the defective container (`pre/c1-precheck-at-base.json` `control.accepted true`).
After: refused 1/1, accepted 1/1, `met true`, exit 0.

Kill rule: any verdict/expectation mismatch; a round-84 container that is not CLEAN; a
round-83 container that is not FLAGGED with that exact finding; a control that fails to accept
the round-83 container (it must fire) or that also accepts the round-84 container as clean
without the per-claim check being exercised; a changed predicate or container set; a named
counter that is not a blob at the measured revision or is not pinned at its frozen digest.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-84/freeze-precheck.py --root . --rev $REV \
  --container .ufo/waves/round-83/claims.json --expect .ufo/waves/round-83/claims.json=FLAGGED \
  --container .ufo/waves/round-84/claims.json --expect .ufo/waves/round-84/claims.json=CLEAN \
  --control instruments-only --json-out $OUT
```
<!-- /counting-command -->

## R84-C2 — depth: the recorded mutation survivors close at declared cases

Predicate: `tools/round-84/mutation-closure.py` reports `killed 13`, `mutants 13`,
`survivors []`, `inconclusive []`, `pristine_failed []`, `ok true` and exit 0 for the frozen
mutant table `.ufo/waves/round-84/mutants.json` against the three target tools at the measured
revision, where every kill is bound to that mutant's declared selftest case; the same frozen
table at BASE reports `killed 4` and leaves 9 named survivors.

Targets: `tools/round-82/conjunction-gate.py`, `tools/round-82/printed-command.py`,
`tools/round-83/source-bind.py`. The table's declared cases that do not exist at BASE are the
work: `runtime-pin-mismatch-refused`, `static-defect-no-execution`,
`sourced-row-rejected-status`, `sourced-row-wrong-date`, `sourced-row-at-base`,
`sourced-plan-missing`, `sourced-entry-uncited`, `late-single-header`,
`duplicate-target-second`. The nine survivors are the recorded round-82 seven plus the
round-83 two; no survivor is redefined, and a kill requires the declared case to fail in the
mutant run while the pristine run is green (QUALITY 138).

Frozen mutant table (`mutants.json`, 13 rows, each edit anchored exactly once at BASE):
floor (2-edit pair; the floor is guarded twice), failure, binder, membership, pin-call,
static-refusal, source-mined, source-date, source-base, source-plan, source-entry,
sb-header-position, sb-duplicate-last.

Before: `.ufo/waves/round-84/pre/c2-base.json` — 4 killed, 9 survivors, exit 1.
After: 13 killed, 0 survivors, exit 0.

Kill rule: any survivor, inconclusive or red pristine target; a kill not bound to the declared
case (`declared_case_present false`); an anchor absent or occurring more than once; a table
edited after the freeze; a target digest differing from the frozen release pin without a
disclosed `instrument_supersessions` entry.

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-84/mutation-closure.py --root . --rev $REV \
  --mutants .ufo/waves/round-84/mutants.json --work $WORK --json-out $OUT
```
<!-- /counting-command -->

## R84-C3 — coverage: the nested container chain edge class

Predicate: `tools/round-84/nested-sqfs.py` reports A1–A9 true, the file-count control firing,
`met true` and exit 0 on a reproducible three-level chain of standard little-endian SquashFS v4
images (mksquashfs 4.7.5, gzip, `-repro-time 1760000000`) through REA 6.5.0 `extract-firmware`
(unblob 26.6.4): 8/8 oracle members published at exact paths with matching bytes at both
`--max-depth 3` and `--max-depth 4`; at depth 3 `coverage partial`, exactly one
`depth-limited` path at the deepest extract root, and the level-3 files carry
`analysis_depth null`; at depth 4 `coverage complete`, no gap, and the level-3 files carry
`analysis_depth 3`; unblob engine identity equal across both runs.

Counter: `tools/round-84/nested-sqfs.py` (full path). The oracle is the independent
`unsquashfs 4.7.5` extraction of each level, and the nested carriers' identity is checked
against the built image digests (`b_is_oracle_member`, `c_is_oracle_member`). Fixture identity
rests on S301 (`mksquashfs(1)` `-repro-time`, opened this round).

Before: the class is Frontier and unmeasured — `PROVINCE.md` and `corpus/README.md` each name
"nested sub-images below depth 1" as open, and `tools/round-84/nested-sqfs.py` does not exist at
BASE (`git show BASE:tools/round-84/nested-sqfs.py` fails), so 0/9 arms.
After: 9/9 arms, control fires, exit 0.

Kill rule: any arm false; the control not firing; an error envelope instead of an extraction;
fixture digests changing between the two depth runs; an engine identity difference; a
changing predicate, fixture recipe or depth pair.

<!-- counting-command: C3 -->
```sh
python3 -I -B tools/round-84/nested-sqfs.py --rev $REV --work $WORK --json-out $OUT
```
<!-- /counting-command -->

## Frontier step and standing duties

- `corpus/SOURCES.md`: two rows opened this round — S301 (mksquashfs(1) `-repro-time`; mined,
  tier A, grounds C3's fixture identity) and S302 (rejected: the REA npm tarball as an anchor
  for the `depth-limited` gap taxonomy — it duplicates a registry URL already held and is not a
  stable anchored document; flip condition recorded). Census before `205 rows,
  A187/B10/C8, mined 184/rejected 21`, measured at round start.
- Mistake mining: the round-83 routed word-count defect (13 vs 12) and this round's own
  mistakes into `corpus/lessons/round-84.md` `## Mistakes`, with captured-by and a fix shown
  able to fail.
- Lesson `## Gate`: URL, access date and a ≤25-word located quote for S301 and S302.
- Knowledge entry `corpus/knowledge/2026-11-04-r84-nested-container-chain.md` cites S301 and the
  round-84 receipts; it states the bounded class (lane-built LE v4 gzip chain, three levels),
  the not-covered classes, and that publication is not analysis.
- `PROVINCE.md` + `corpus/README.md`: the nested-chain edge class moves to Core for the bounded
  class; the round-50/67/68 "still frontier: nested sub-images below depth 1" line is
  superseded for this class only.
- Standing duties: registry rows for the three new tools under SKILL registry grammar v2;
  freeze-ledger row for round 84; disclosure consistency and receipt provenance sweeps; source
  census at round end; misroot sweep before the report; no considerthese directory in this lane
  (statement in the report); assimilation: none unless adopted.

## Wave plan

One v1 wave `r84-w1`, 14 seats (`ufo-wave-policy.json`, band 8–16): 5 executor (candidate
detector patches ×2, base-arm mutation reproduction, independent nested reproduction, gate
forgery attack), 2 scribe (knowledge entry draft, source curation draft), 1 scout (anchor
census + fixture identity), 2 reviewer (C1 semantics, C3 envelope/oracle), 1 critic (all three
claims), 1 mutation-tester (independent mutants beyond the frozen 13), 1 sentinel (write scope,
path containment, engine execution), 1 connector (sibling-overlap scan). Attack share 4/14 =
28.6 %; one connector. The L1 holds the planner seat (the validator rejects a planner role).
