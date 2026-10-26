# R41W2C1AxisFit — is R41-C1 a coverage move (Frontier → Core) or re-scoring held ground?

**Verdict: CONFIRMED — R41-C1 is a genuine coverage move, not re-scoring held ground.** The
surface it moves (genuine AVM-layout BE SquashFS v4, Frontier → Core) was **not governed** at
the freeze: R40-C1 was not met (3/4, honest stop), the round-40 closure recorded coverage
**unchanged**, and PROVINCE still carried `## Round-40 measured, not promoted`. The frozen C1
rests on four carriers no extractor touched before the freeze, including a new edge class (V4,
the first full vendor AVM rootfs, 6349 regular files), and the kill-rule control CTL-C1-1
(round-40 receipts relabelled) scores 0/4 — the round-41 score cannot be manufactured from
round-40 data. What was attacked: the draft critique's claim (w1/R41CritC1Draft.md) that the
claim re-scored round-40 ground and was quality/calibration, never coverage.

## 1. The axis test (AXES.md + prompt §6 item 9)

AXES.md defines **coverage** as the fraction of the domain's real surfaces the skill *governs*;
its signal is "PROVINCE.md lists every surface; none unexplored without reason." Prompt §6 item 9
(The run-9 prompt, lines 464–486) says: *"Name the axis by the surface the round changes, not by
the number it produces … Re-scoring a rule the lane already holds on new inputs … is quality work,
never coverage or depth. A coverage claim names the surface it moves (frontier → core, a new tool,
operation or edge class) and the command that would show it unmoved."*

R41-C1 satisfies the positive test literally:

- **Names the surface it moves:** "coverage: genuine AVM-layout big-endian SquashFS v4 moves from
  Frontier to Core" (plans/round-41-claims.md §R41-C1); the moved records are named: PROVINCE
  `## Round-40 measured, not promoted (R40-C1 honest stop)`, the round-39 frontier note's AVM
  sentence, and the `corpus/README.md` `## Frontier` sasquatch-v4be line.
- **Names the command that shows it unmoved:** "the C1 counter at the freeze exits 1 (no round-41
  receipts, no `## Round-41 additions to Core`)". Verified: CTL-C1-0 at freeze `d764389e` →
  `{"carriers_matched":0,"exit_code":1,"met_target":false}` with `province_core_section:false`
  (`.ufo/waves/round-41/controls/c1/ctl-c1-0-do-nothing.json`).

The negative test fails: the rule was **not already held**. R40-C1 ended 3/4 (not met), its
closure verdict reads "Coverage axis: **unchanged** (the Frontier → Core move did not land; nothing
regressed)" (corpus/lessons/round-40-verifier-spotcheck.md §2). At the freeze, PROVINCE still had
no `## Round-41 additions to Core` section (`province-freeze-vs-tip.json`: freeze has
measured-not-promoted, no round-41 Core; tip has round-41 Core + frontier note). A surface that is
"measured, not promoted" is explored but **not governed**; moving it to Core increases the governed
fraction — that is the coverage move, not a replay.

## 2. The strongest counterexample and why the frozen claim defeats it

The draft critique (w1/R41CritC1Draft.md, verdict DEFECTS FOUND) argued: round 40's stop was an
*instrument* defect, not a capability miss — V1/V2/L1 matched every clause, the wave-2 sandbox
exact-match counter scored the same round-40 receipts 4/4 (R40W2C1Refreeze.md), so "promoting a
measured record after fixing the instrument changes the record, not the surface the lane governs:
that is calibration plus quality." The frozen claim neutralises each leg of that attack, with
committed evidence:

1. **Freshness is now a scored, binding clause.** `carrier_fresh_ok` rejects any pin present in
   `prior_pins` (round-40 `carriers.json`) — counter source `tools/round-41/c1-counter.py:91-92,321,1545`.
   CTL-C1-1 (round-40 receipts copied to round-41 paths, re-minted) scores **0/4**: all four
   carriers show `subject_pin_ok:false` — subject digests cannot equal the round-41 pins
   (`ctl-c1-1-relabel-r40-summary.json`). So the score cannot be reached by re-scoring held data.
2. **Carriers are fresh bytes, and one is a new edge class.** The four round-41 carriers (V3
   FRITZ!Box 5490 07.31 member, V4 5491 nested `filesystem_core` rootfs, L3/L4 lane-built with
   both-direction collisions) were reserved; the wave-1 reservation scan reported 0 red — no REA or
   unblob run touched them before the freeze (claims §R41-C1 reservation; V3/V4/L3/L4 seat reports
   state no REA/unblob runs). V4 is the **first full vendor AVM rootfs the lane has measured**:
   6349 regular files + 1017 non-regular entries, 7367 staged entries against REA's 10000-entry
   budget (`carrier-scope-comparison.json`: round-40 max measured oracle = 697 regular rows (V1),
   round-41 V4 = 6349). This is a new surface/edge class — a full rootfs under REA's staging budget
   — not a re-run of the 697-file or 8-file members round 40 scored.
3. **The counter is new, not the same rule.** Exact extract-root path matching (R40-CL1 fix),
   fetch chain with `member_sha256`/`nested.sha256` (R40-CL6 fix), single-chunk oracle-set equality,
   and the freshness clause are all new bindings; the counter's selftest  both collision directions.
4. **Sourced-new binding.** The round-41 entry cites S127/S128, opened this round (`opened_source_rows
   ["S127","S128"]` in the score receipt); `c1-extra.py` met with `sourced_new:true`.

## 3. Measured score at the landing (evidence)

`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json` (revision `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4`):
`carriers_matched 4/4`, exit 0, `met_target true`; per carrier all clause keys true (published ==
oracle: V3 8/8, V4 6349/6349, L3 13/13, L4 14/14; `gaps_ok`, `carrier_fresh_ok`,
`receipt_fresh`, `subject_pin_ok`, `layout_ok`, `handler_ok` all true); top-level bindings true
(`province_core_row`, `province_core_section`, `coverage_map_row`, `entry_present`, `sourced`,
`frontier_note`). `c1-extra-at-e9a24d07.json`: met, exit 0, `sourced_new true`.
(`c1-score-e9a24d07-summary.json`.)

## 4. Impacted axes and residual note

- **coverage: improved** — a surface that stood as "measured, not promoted" (governed fraction
  unchanged after round 40) is now a Core row, backed by fresh measurements including a new edge
  class (full vendor rootfs).
- **depth/calibration: un-harmed** — the counter repair (R40-CL1/CL6) is quality work riding the
  claim, but the axis is named by the surface the round changes (promotion with new data), per §6
  item 9. The honest-stop record itself is superseded, not hidden.
- Residual caveat (calibration): the promotion record's own prose is careful — it states the round-40
  stop was a counter false negative "not from the images" (PROVINCE round-41 frontier note). That is
  accurate and does not weaken the coverage move: the *governing* state changed with *new* evidence.

## 5. Evidence / artifact inventory

Artifacts: `.ufo/waves/round-41/w2/artifacts/R41W2C1AxisFit/` — `c1-score-e9a24d07-summary.json`,
`ctl-c1-0-do-nothing-summary.json`, `ctl-c1-1-relabel-r40-summary.json`,
`province-freeze-vs-tip.json`, `carrier-scope-comparison.json`, `round40-closure-quote.json`.
Commands run: `git show` of freeze/tip PROVINCE and round-40 oracle.tsv row counts (read-only);
`python3` extraction of committed score/control receipts (identical to committed bytes). No tool
installed; no VCS mutation; no REA/unblob run; no vendor bytes copied (pins only). Scratch
`S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1AxisFit` created empty and removed at finish.
