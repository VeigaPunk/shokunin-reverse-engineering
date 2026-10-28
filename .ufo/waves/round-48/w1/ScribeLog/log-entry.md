# Draft `LOG.md` entry — round 48

Drafted for the L1 before the landing is measured, in the format rounds 46–47 share
(`ScoutLog.md` surveyed the house format). `[fill: …]` marks the slots only the landing
measurement can supply; every other value below is already receipt-backed under
`.ufo/waves/round-48/`. Append after LOG.md line 3434 (a blank line, then this heading;
if a new `## 2026-10-28` date heading is opened for round 48, this entry sits under it as
rounds 46–47 do under round 45's).

---

### Round 48 — a binding is a meaning, and the record must name one seat, one path and one rev per round

Round 48 declared two claims on the two tied-lowest axes and landed both, each with its own
counter. `tools/round-48/meanings.py` (R48-C1, depth) scores craft rule block 25 — the
verdict-meaning table `<!-- verdict-meaning-table v1 -->` with rows keyed by routed id
(`R46-CL7` → `meaning`, `R47-CL10` → `floor`), a `mutations_sha256` over each mutation's name
and source body, an `interpreter_sha256` pin and ≥5 line-selected citations — plus every row
of the `<!-- instrument-registry v2 -->` section re-bound to `tools/round-48/census2.json`
so that each verdict map's 0/1/2 digits carry a success, a not-met and an unevaluable
meaning. `tools/round-48/record2.py` (R48-C2, calibration) re-derives `SCORECARD.md` from
committed bytes — the round-47 atom oracle executed from `--rev`, a completeness floor per
round section, every `## Record corrections — round 48` line re-derived, quoted receipt
numbers bound to their receipts and the Owned-axes score cell bound to its fraction. Frozen
at `plans/round-48-claims.md` + `tools/round-48/` (directory pathspec). Coverage gets no
claim: the round adds no domain surface, and `PROVINCE.md` is untouched (`w1/ScoutProvince.md`).

- **Freeze series, disclosed.** `7fe11332` (plan + counters) → A1 `dc73587a` (the
  `axis_scores` clause read the evidence cell; `ctl-c2-a1-before.json` red-before) → A2
  `ac02a79f` (the exit-0 classifier rejected `0=met with failing empty` prose on the
  legitimate `tools/round-47/exact.py` row) → A3 `f3a7afc4` (the census clause compared a
  derived object with the committed `paths` list; `ctl-c1-a3-simulation.json` red-before,
  found by wave 1 `C1Census`) → A4 `0f06251b` (two measured wave-1 attacks: `C1Gold`'s
  `0=not met` opposite-polarity map accepted as success, and `CritAxis`/`CritSeparability`'s
  `|  \`` leading-whitespace row skipped by the registry parser). **The declared freeze is
  A4 `0f06251bf6a3a6964c715f67243d4df12e854258`**; `git log --format=%H -1 --
  plans/round-48-claims.md` re-derives it. The wave's tasking text carried the A1 hash — the
  R47-CL11 stale-declared-freeze class recurring inside the round that routed it; a stale
  `--freeze dc73587a` at tip exits 2 `frozen_path_changed` (`w1/ExecMeasure/` receipts), so
  the freeze argument is part of the counted command.
- **Before → after, measured.** C1 at the freeze: exit 1, `marker_occurrences 0`,
  `rule_blocks 24`, battery skipped (`controls/ctl-c1-0-do-nothing.json`); at the base exit 2
  (`freeze is not an ancestor of rev`). C2 at the freeze: exit 1 — oracle green (44 atoms,
  `mismatches []`) but floor red (`round-47: no seat atom and no re-derived seats
  correction`), `corrections 0`, `exempted 2` quoted but unbacked (`quotes_bad 1`)
  (`controls/ctl-c2-0-do-nothing.json`); the ported v2 profile scores exit 0 on the same
  card — the hole this claim closes (`controls/ctl-c2-1-v2-profile.json`). Axis score cells
  read `coverage 9.72 → 10.0` over `138/138` and `depth 10.0 → 10.0` over `24/24`.
  `[fill: post-landing receipts for both counters at the measured revision, incl.
  battery forgeries_total/v2_green/v3_green/genuine_green/crash.]`
- **The record repaired, append-only.** `## Record corrections — round 48` carries [fill:
  exact landed lines; drafted values — a re-derived `seats` correction for round 47
  (`1 wave, 75 seats total` — `w1-dispatch.json` `counts.spawn 75`, no `w2-dispatch.json`)
  and a re-derived `quote` correction for round 47 (`exempted 1`, the value
  `.ufo/waves/round-47/l1/scores/c2-at-A7.json` states where the ledger row quotes
  `exempted 2 <= 3`)]. The `## Owned axes` head updates for this round
  [fill: new fractions and score cells].
- **What wave 1 found and routed.** Four amendments were forced before any verdict (above);
  the residual routed findings, all frozen-scope: a measured C2 blind spot —
  `axis_scores()` re-reads `files("SCORECARD.md")` and ignores the mutated card, so
  `axes-score-cell-off` is invisible to clause 5 and scores v3-green on a green landing
  card, tripping the kill rule until a further amendment lands
  (`w1/ScribeLog/c2-axes-blindspot.json`); the meaning classifier binds tokens, not code
  paths — the `0=met; actual exit 0 means the command failed` map survives, 16 of 40
  existing rows fail on honest vocabulary and four tools overload a digit or exit outside
  the 0/1/2 grammar (`w1/LabC1Meaning.md`, `w1/MutC1Rows.md`); correction-section laxity —
  malformed lines ignored, one quote correction can excuse multiple same-key wrong quotes,
  claim-id regex unbound to the round (`w1/RevC1.md`, `w1/MutC2Corr.md`); the round-46 gate
  imports from the worktree, not `--rev` (`w1/C2OracleLimit.md`); and a racy-clean
  `frozen_worktree_dirty` flap on `tools/round-48/meanings.py` (byte-identical; two
  receipts exited 2). Routed ids: [fill: L1 numbering.]
- **Waves:** wave 1 = 75 seats (executor 22, scribe 16, scout 9, reviewer 9, critic 6,
  mutation-tester 6, connector 2, revenger 2, simplifier 2, sentinel 1; bounded planning
  data-walks rode scout/connector/revenger seats because the validator rejects `planner`
  as a swarm role — recorded here per the round plan) [fill: settled/lost counts]; wave 2 =
  [fill: pending]. Per-seat output in `.ufo/waves/round-48/`. Tools installed this round:
  none (pacman transactions paused host-wide).

### Round 48 claim ledger

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R48-C1 | depth — `SKILL.md` craft rule block 25 (verdict-meaning table, two routed-id rows, both pins, ≥5 citations) and the registry re-bound to `census2.json` by meaning | exit 1 at the freeze: `marker_occurrences 0`, `block_present 0`, `rule_blocks 24`; v2 accepts all four forgeries | [fill] | `python3 -I -B tools/round-48/meanings.py --root . --freeze 0f06251b --rev <REV> --json-out <OUT>` | [fill] | [fill] |
| R48-C2 | calibration — `SCORECARD.md` re-derived from committed bytes (round-47 oracle from `--rev`, completeness floor, correction classes, quote binding, score-cell binding) | exit 1 at the freeze: oracle green but floor red (round-47 seats), `corrections 0`, `quotes_bad 1`; v2 exit 0 | [fill] | `python3 -I -B tools/round-48/record2.py --root . --freeze 0f06251b --rev <REV> --json-out <OUT>` | [fill] | [fill] |
