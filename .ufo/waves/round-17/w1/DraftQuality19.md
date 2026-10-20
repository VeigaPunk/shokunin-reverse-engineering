# DraftQuality19 — report

Scope: draft QUALITY admission row 19 for R16-PROVENANCE. Draft: `.ufo/waves/round-17/w1/draft-quality-19.md`. No other file edited. No tool installed or updated. No REA analyze/search/decompile, no Ghidra, no carrier execution.

## Observations (verified by read or grep)

- `corpus/QUALITY.md:9-10` admission header; rows 1-18 at `:11-28`; row 18 is the last admission row (`:28`); blank `:29`. HEAD has 24 numbered rows (18 admission + 6 signal).
- Routed defects: R16-PROVENANCE at `corpus/lessons/round-16-verifier-spotcheck.md:183`; R16-INVOCATION at `:184`; routing sentence `:181`.
- `.ufo/waves/round-16/verification.json:419` `"pins_unchanged_during_run": true`; `:397-418` `producer_and_fixture_sha256` has 20 entries; `:4` a single `executed_at_utc` (`2026-10-20T08:36:33Z`). No before/after maps or timestamps.
- Temporal-stability sites found in the lane (grep: `unchanged during|remained unchanged during|stable throughout|pins_unchanged_during_run`, plus `during/across (the )?(execution|run)` variants):
  - `.ufo/waves/round-16/verification.json:419`
  - `corpus/lessons/round-16.md:154` ("All producer/fixture pins remained unchanged during execution.")
  - `LOG.md:2012` ("Producer/fixture hashes remain unchanged across execution.") — found only by the wider `across` variant; the sweep pattern in `contract.md:93` does not match it.
  - `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` ("Producer and fixture pins were unchanged during the run.")
- Outside the lane: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` ("Producer/input hashes stayed unchanged during execution.").
- `SCORECARD.md`: my patterns matched only `pin value unchanged` (config.toml) and table cells, none about r16 pins. The spotcheck's claim that the scorecard repeats the statement is therefore not confirmed by my search. Not resolved.
- Sweep scope gap: `contract.md:91-93` restricts sites to LOG.md, SCORECARD.md, `corpus/lessons/round-16.md`, SKILL.md and `verification.json`. That misses `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` (in-lane), and the sweep regex misses `LOG.md:2012` ("across execution").
- `contract.md:12-20`: pins.py proves only "same bytes at two instants", never "unchanged throughout". Row 19 follows that boundary.
- `.ufo/waves/round-17/pilot/README.txt:6`: "pre/post carrier pins were NOT recorded in the pilot."
- `corpus/lessons/round-17.md` does not exist on disk. `.ufo/waves/round-17/w1/` held only `swarm-registry.json` at draft time; r17 lesson drafts have not landed.

## Draft decision

Row 19 covers R16-PROVENANCE only. Criterion: any "unchanged during/across/throughout" claim needs retained pre/post records with an equality comparison. A boolean, a single timestamp, or a hash map matched to committed blobs does not qualify. The admissible fallback is the spotcheck's wording ("map matches committed source-revision blobs; temporal stability not evidenced"). Two-instant equality supports "identical at each recorded instant" only. "Throughout" needs a continuous change-notification record with a stated gap bound.

Why R16-INVOCATION is not in row 19: row 18 (`corpus/QUALITY.md:28`) already requires that future guidance match an exercised argv or "explicitly name an unexercised variant". Repeating it in row 19 would duplicate row 18. Alternative if L1 prefers: fold route 2 into row 18's `why` cell. Not done here.

## Calibration limits

- Row 19 is a rule, not evidence. It does not show that r16's pins changed or stayed fixed.
- "Throughout" is stated as inadmissible without continuous monitoring. I did not check whether this host has a usable inotify/fanotify path [INFERENCE: the rule is stated without that check].
- The `why` cell cites `corpus/lessons/round-17.md`, which is not on disk. If the r17 lesson uses a different class label or path, update the citation at integration.
- Scorecard occurrence unverified (see above); row 19 does not depend on it.

## Checks for L1 (not run by me)

- After integration: `corpus/QUALITY.md` rows 1-18 byte-identical to HEAD; row 19 present (controls.py / measure.py "QUALITY row 19" token).
- Confirm `corpus/lessons/round-17.md` path and Mistakes row wording match row 19's `why` cell.
- Route to TemporalSweepTool or L1: sweep file list omits `corpus/knowledge/2026-10-20-r16-go-selection-preview.md`, and the regex omits "across execution" (`LOG.md:2012`).

## Install / update record

None.
