# Round 92 — frozen claims (declaration)

Base `73a882712907606eba074377b536c6dd82517e25` (lane tip at declaration). Machine record:
`.ufo/waves/round-92/claims.json` (instrument sha256 pins, control summary). Controls and
receipts: `.ufo/waves/round-92/pre/` and `.ufo/waves/round-92/controls/`. Predicates,
counters, kill rules and targets below are frozen at this declaration; no later edit may change
them (a changed rule is a new claim, not this one).

Round-start census (frontier step §2b): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku` → exit 0, `ok`, 221 registry rows, 29 W04 duplicate-URL
warnings (`.ufo/waves/round-92/census-before.txt`).

Axes: the lane owns coverage, depth, calibration, freshness; all four are at 10.0 on their
finite proxies (SCORECARD `## Saturation`, line 10.0; the lowest-axis obligation is therefore a
tie across all four, and both claims below sit on tied-lowest axes, coverage and calibration).
Stagnation nudge: not applicable — a capability entered in round 91 within the window of 10.

## R92-C1 — coverage (capability): a last-block stop-boundary tamper is repaired inside a declared window

- **Surface moved.** The round-91 class `T7-chain-stop-boundary` (packed UPX 5.2.0 `--best`
  little-endian ELF; the last block before the chain stop has `sz_cpr` moved by -7 or +7) is
  refused in Core today (R91-C1). R92-C1 adds a repair path for the declared window
  `|delta| <= 16`: the candidate tries every `v` in `stored-16 .. stored+16` (in range
  `0 < v <= sz_unc`), decides each by the packer's own verdict (`upx -t` on a private copy), and
  writes output only when exactly one value is green, the output differs from the input only in
  the four-byte window, and the output is green. Zero or two-plus green values → typed refusal
  (rc 2, no output). An intact input is returned byte-identical (rc 0), as in round 91.
- **Candidate.** `tools/round-92/upx-stop-boundary-search-repair.py` — built in the round-92 wave;
  it does not exist at declaration and is not measured here.
- **Counter (frozen).** `tools/round-92/stop-boundary-repair-battery.py` (imports
  `tools/round-92/stop-boundary-battery-v2.py` by path; both sha256 pinned in `claims.json`).
  Five carriers: jq, xxd, libz, docker-init, and the unseen `/usr/bin/xz` (named in no round-91
  table). Ten near cells (±7), ten far cells (±40, the negative control), five intact controls.
- **Frozen label.** `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`,
  exit 0. Command: see `claims.json` `frozen_command`.
- **Before (do-nothing control, scored by the frozen counter at base).**
  `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met False, exit 1
  (`.ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json`, revision `73a882712`,
  command `tools/round-91/upx-stop-boundary-repair.py`). The target is unreachable by the
  do-nothing control.
- **Kill rule.** Any of `repaired < 10`, `wrong > 0`, `unsafe > 0`, `intact < 5`, `far-refused < 10`,
  a missing receipt, or a counter sha256 that differs from the pin → the claim is not verified,
  no axis credit, and the round-91 refusal row is not superseded.
- **Declared limits (not claimed).** Window `±16` is the tool's own bound; `±7` is the battery
  class. A counterfeit that embeds the pinned packed images of all five carriers would pass
  `repaired` and is not excluded by this counter; the unseen carrier is one carrier, not a proof.

## R92-C2 — calibration: the refusal label stops admitting counterfeit refusals

- **Surface moved.** The round-91 frozen label `refused 8 of 8; unsafe 0; intact 4 of 4` (the
  `refused` arm = rc != 0 with no output) admits three declared counterfeit refusals: CHEAT-A
  carrier-read (reads four pinned carriers), CHEAT-B hash-table (sha256 of four pinned packed
  images), CHEAT-C exit-1 (the typed rc-2 refusal exits 1). Round 91 recorded this as D-91-4 /
  ATTACK-2 / ATTACK-3 and routed the rc-2 assertion and the cheat arms to round 92 as a new counter.
- **Measure.** Count of the three declared counterfeits that the counter labels `met_target true`.
- **Counter (frozen).** `tools/round-92/stop-boundary-battery-v2.py` (new; `tools/round-91/`
  unchanged). Same class, five carriers (the four round-91 carriers plus unseen `xz`), 10 tampered
  cells and 5 intact controls. A refusal counts only when rc is 2 AND the last stdout line is a
  JSON object with a `refused` key (`typed`).
- **Frozen label.** `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5`, exit 0.
- **Before (the round-91 counter, label unchanged, scoring the three counterfeits at base).**
  Admitted 3 of 3 (`pre/c2-do-nothing-v1-counterfeit-{A,B,C}.json`, all `met_target true`).
- **After (v2, at the measured commit).** Admitted must be 0 of 3 (`pre/c2-counterfeit-{A,B,C}-v2.json`,
  base: all three `met_target false`: A and B `intact 4 of 5` (the unseen carrier), C `typed 0`).
  Positive control: the round-91 refusal tool under v2 must be `met_target true` (pre/base:
  `pre/c2-positive-v2-round91.json`, `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5`).
- **Kill rule.** The after admitted count is nonzero; or the positive control is not met at the
  measured commit; or any counterfeit receipt is missing.
- **Declared limits.** The counterfeits are the round-91 CriticClaims definitions, reproduced here;
  CHEAT-B's table was recomputed from freshly packed carriers (not copied from round 91). Other
  counterfeits (an unseen-carrier table, a fresh-pack oracle) are not in this claim.

## Not claimed

- Calibration numeric score: unchanged at 10.0 (saturated finite proxy); the verdict is carried
  by the counterfeit count, not by a new number.
- R91-C1 frozen label and R91-C2 depth predicate: historical, not re-scored, not edited.
- `tools/round-91/` instruments: unchanged.
- Exploratory claims: none this round.
