# kaidoku luna-round-4 — freshness debt-drain

Date: 2026-10-16. Axis: **freshness** (fleet axis, not a lane-owned proxy —
recording ruling in the SCORECARD section and below). One axis-move. Wave: 64
seats on `openai-codex/gpt-6-luna-max` (58 + 6 backfill — see Process).
Reports: `.ufo/waves/luna-round-4/`.

## Work performed

- Re-verified all 19 named drift findings against their knowledge files
  (V-pairs), drafted minimal repairs, adjudicated the two that were
  unsupported (asar row — V01a showed the round-1 finding was wrong; crash row
  — D01 showed the aggregate row is supported by the r2 entry).
- Merged conflicting drafts (B3: Firmware row split; B2: REA-service row final
  text; R07's correction folded into the firmware extraction wording).
- Applied 14 repair groups to `corpus/README.md` (map rows, Knowledge rows,
  Known gaps, lessons pointer). Knowledge files, lessons, LOG untouched by
  design; two knowledge-file debts named instead (r1 asar framing; r4u-01
  size decimals per C05's hex math).
- Eight wording tweaks post-dispatch, each reviewed as MORE faithful (e.g.
  "120 deduplicated content nodes", "3/3 probed … of 286 cataloged"), to
  satisfy the wave's own census matchers; work commit amended pre-records.

## Landed changes

- `corpus/README.md` — 14 repair groups — commit `6a71cd5` (lane identity).
- `LOG.md` + `SCORECARD.md` + this report — bookkeeping commit (below).

## Before → after measurements

- Command A at `6a71cd5`: mapped 72, missing [], dangling [], coverage 10.0,
  depth 10.0 (9/9 rules) — unchanged.
- Token set: 72/72 PASS (Firmware split + Frontier prerequisites reseat kept
  every token in the map section).
- Wave census at `6a71cd5`: 14/19 PASS; 5 ADJUDICATED-with-cause —
  F01 (census encodes removing "3/7", which V02a verified as the correct
  count; the repair added the registry clarification, which the census cannot
  express); F02 (census encodes the round-1 asar claim refuted by V01a);
  F05 (targets "content-addressed" in a row no seat flagged; the flagged
  universal lives in the knowledge file's historical r4 erratum — file debt,
  not map); F16 (replacement matcher encodes one specific per-leg wording;
  the stale-pattern absence is verified and the repair was R03-reviewed);
  F18 (z=1 line-count is structurally unsatisfiable while the
  `rea-skill-contract` map token exists; the stale v37 phrasing is verified
  absent). Census is instrument, not authority — its own disclaimer and this
  adjudication stand together.

## Findings & named debt (carried forward)

r1 asar knowledge-file framing (B1, round 5+); r4u-01 firmware `.fwimage`
size decimals (C05: 0x1c01dc8 = 29,367,752; 0x505b000 = 84,258,816 —
append-only correction, future round); README stale frontier summaries
(:160 content, :128 four-vs-two nits); PROVINCE conditional request-byte pin
for module-identity probes (C7, from round 3); r9-02 file's own later-summary
tension (:215-216 vs :82-84, V12b); knowledge-file re-verification debt from
C05's provenance inversion (files as authority were right this round; the
method deserves its own round).

## Process defects (recorded)

- SECOND short-count dispatch (58 vs 64; first was luna-round-2). Repaired
  both times with a 6-seat backfill before integration; root cause (parent
  item-array arithmetic) named in the fleet ledger. One more occurrence
  should trigger a dispatch checklist change.
- Seat defects: V11a wrote to V27.md (misnamed); R09's boundary review ran
  pre-integration by design (deferred); S1/S3 found pre-existing untracked
  `.ufo/interactive-sessions/` files and unattributable `/tmp/probe*.log`
  files (predate the wave; untouched).

## SHONEN

- [~] ×4 unchanged. K1: chousa/revenger boundaries clean. B6's recording
  question ruled as: fleet-axis freshness improvement with owned proxies
  unchanged (dissent shape recorded in SCORECARD.md).

## Verdicts

- freshness: **improved** (19 findings → 14 repaired + 5 adjudicated; 0 true
  debt remaining; census + command A measured).
- coverage / depth / calibration: **unchanged** (measured at the round commit).
- Learning: expansion unchanged; quality improved (summaries match sources;
  census overreach recorded as instrument debt); discernment improved locally.
- Admitted: yes — one axis improved, none harmed.
