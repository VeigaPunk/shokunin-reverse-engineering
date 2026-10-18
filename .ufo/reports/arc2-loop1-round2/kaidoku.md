# kaidoku arc2-loop1-round2 — calibration/freshness/operability: Kimi-pin reconciliation + label qualification + 5-path custody

Date: 2026-10-18. Wave: 64 seats on `devin/deepseek-v4-1-flash-max` (operator
directive of 2026-10-18), parent-integrated, no seat commits; 60 seat reports
delivered (4 non-completions recorded as a dispatch defect). Work commits:
`b3cd790` (content + receipts), `b21c0da` (wave artifacts) — lane identity;
this report lands after and cites them (lands-last). All in-place edits are
line-neutral (PROVINCE 162 / SCORECARD 701 / README 187 lines held) — chosen
after CR7 proved the wave's raw draft (+31/−13) would have shifted
`PROVINCE.md:114-116` and staled 7 landed citations in append-only files.

## Work performed

Claims (3, distinct axes, separability proved by C1/CR6 — C1 verifies
statically without battery artifacts; C3's gates never read C1's edits):

1. **C1 — calibration** (owned): reconcile every current-surface pin/version
   statement to 2026-10-18 live receipts, line-neutral, grade-ladder-enforced
   (CR1: configured → resolvable → available → held; the landed text claims
   configured/resolvable only — PROVINCE :44 "spawn"→"registers", no holding
   verbs). Acceptance: E22's census v9 with live-re-derived anchors.
2. **C2 — freshness** (fleet): qualify README :90,:160 (E10 COMPACT in-cell
   form — the appended-note form was measured to fail the round's own probe)
   and reword SCORECARD:68-72 (R2's 5-for-5; both named debts discharged at
   `7125dd4` — a bare re-point would have landed false sentences).
3. **C3 — operability** (fleet; capability acquisition): 5-path custody
   (E15's queued extension — `.bashrc`/`~/.profile` enter at THIS round's
   pre-pair) bracketing a 2-leg 6.7.0 battery; SOP amended 3→5 paths (the
   landed 3-path SOP would have voided this round's own 6-line receipt —
   CR4/R4's necessity proof); capability row entered (replaces the r1 row).

Work items (pointers): live pin re-verification (E1/SC2/V2 — Kimi 6.7.0 at
`config.toml:2940`, `:1478` = `model = "kimi-k3"`, both .baks carry 6.7.0);
cache inventory (E2/V4 — 6.7.0 `a1722018f28f9df2`, package.json sha256
`3f6c47fb…`, offline npx resolution reproduced); the C1 acceptance census
(instrument v9 — before-values at HEAD: stale=5 hard + ambiguous reads; after:
**PASS 0/0/0/0** at the work tree); README byte-certification (whole-file
`ba7265eb…` equals R2's certified prediction); battery legs E13 (doctor exit 1,
27 checks, `af39310c…`) and E14 (census PASS, 207 names byte-identical to
6.5.0, clean close, server exit 0); hygiene E16 (zero residue); post-pair E15
(17:08:57Z, self-hash `3157624e…`, hash column cmp-identical to the pre-pair);
the wave's adversarial record (CR1 grade-ladder + wire-log finding; CR2
in-cell form; CR3 carrier bounds; CR4 SOP necessity; CR5 completeness; CR6
separability; CR7 shift-harm catch; CR8 provenance — all dispositioned from
evidence).

Cross-domain evidence (routed, not absorbed): the Kimi wire-log finding —
0/2195 tool-logs declare `mcp__rea__*`, so 6.7.0 is configured-but-not-held on
Kimi (a future live-probe candidate, not a claim); grok/codex rea registrations
sit outside the 5-path custody set (zero-drift scoped to the five named
paths). No sibling repo touched.

## Landed changes

- `PROVINCE.md` — surface summary + drift-prone values + Core cells :44/:45
  (line-neutral, 16 lines for 16). LOG: this round's entry; commit `b3cd790`.
- `SKILL.md` — inventory paragraph (:18-20) + custody SOP 5-path amendment
  (:217-256 → 64 lines; craft section byte-identical). LOG: this entry;
  commit `b3cd790`.
- `SCORECARD.md` — Version-drift supersession (:56-61), :68-72 reword (5-for-5),
  capability row (5-path custody, replaces the r1 row), this round's section.
  Commit: this report's commit.
- `corpus/README.md` — :90,:160 in-cell qualification (2 lines for 2;
  certified hash `ba7265eb…`). Commit `b3cd790`.
- Receipts `.ufo/waves/arc2-loop1-round2/receipts/` committed TRACKED at
  `b3cd790`: 5-path pre/post-pair (zero drift 0/5 in-window), 6.7.0 leg
  artifacts + census client, `MANIFEST.txt`, and the post-window drift record.
  Wave seat reports at `b21c0da`. No config edits (the drifted config was not
  restored), no pushes.

## Before → after measurements

- **C1 census** — stale 6 + contradicted 1 + ambiguous 1 → **0/0/0/0**
  (instrument v9, anchors re-derived live each run; measured at the work tree,
  exit 0). Counting command: `python3 c1-census-v9.py` (scope table per E22,
  session-preserved at `/tmp/arc2-l2r2-Z1-sim/c1-census-v9.py`).
- **C2 labels** — unqualified safety-label loci in editable corpus files
  **2 → 0** (README :90,:160; marker-aware instrument per E23/CR5's fixed
  form; r3 file clean since round 1). **C2 pointers** — drifted README
  pointers inside the SCORECARD:68 bullet **2 → 0** (:160→:177, :128→:138;
  both debts discharged at `7125dd4`).
- **C3 custody** — pre-pair 2026-10-18T16:57:35Z / post-pair 17:08:57Z,
  in-window drift **0/5** (five captures, aggregate-matching; `sha256sum -c`
  rc 0 at capture). Before: 3-path custody, SOP voiding its own 6-line
  receipt. Capability row entered (AXES.md §Capabilities conditions met).
- **Side-harm checks** — command A at `b21c0da`: 79/79, 10/10 rules, 10.0/10.0
  (identical to `165057e`); PROVINCE 162 / SCORECARD 701 / README 187 lines
  (anchors `## Saturation :625`, `## Capabilities :615`, round-1 section :635
  unmoved); census G7 configured≠held warnings: none.
- **Post-window drift (recorded, not a claim input)** — config.toml rewritten
  17:32:20Z: receipt `3546e033…` → live `f10b01e9…`; pure additions; pin value
  unchanged at :3227. Full record: `receipts/drift-config-toml-20261018T173220Z.txt`.

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists, cited sources: ten queue-drain
  rules + custody SOP (5-path) at `SKILL.md:81-206` / `:208-281`; command A
  10/10 at `b21c0da`; no semantic audit, no outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task executed and logged: the 6.7.0 battery (doctor + census,
  sessions closed) and the 5-path custody pair end-to-end; receipts + this
  LOG entry; the 2026-10-15 libjq smoke remains at
  `evidence/round-1-2026-10-15/rea-bundle.json`; no outside verifier
  (`SHONEN.md:7-8`).
- [~] Executable without oral context: the custody SOP + census instruments
  replay from the record (`SKILL.md` SOP section; instrument copies in the
  wave); documentation-level only (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: boundary `PROVINCE.md:88-116` enforced (safety
  labels qualified, never verdicted); the not-held Kimi finding is routed as
  debt, not absorbed; no complete outside audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

Stale-lane duty: no mission exceeded two driver ticks (parent-integrated
batch, single session); all sessions closed; wave complete except 4 seat
reports noted above.

## Verdicts

- calibration: **improved** — census PASS 0/0/0/0 at the work commit; 8
  defective/disputed loci reconciled receipt-backed; zero citation harm.
- freshness: **improved** — labels 2→0; :68-bullet drifted pointers 2→0.
- operability: **improved** — 5-path custody capability entered; 6.7.0
  surface probed (counts live, digest build-recorded); detector's first live
  catch recorded verbatim.
- coverage / depth / calibration-proxy: **unchanged** (command A at `b21c0da`).

Round admitted: all three claims verified at the landed commits, no axis
harmed; the post-window drift is recorded debt, not a trade. Stagnation
window 2/10.
