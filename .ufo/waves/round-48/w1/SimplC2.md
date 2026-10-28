# SimplC2 — YAGNI/attack pass on `tools/round-48/record2.py` (R48-C2)

Seat: SimplC2, wave 1, round 48. Scope: the `quote` correction class, the `axes`
clause, the floor's per-section granularity, and the oracle delegation — verifying,
attacking and falsifying the frozen counter, and drafting landing evidence.

**Freeze caveat (read first).** The prompt named `dc73587` (A1) as the declared
freeze. The claims file is the rule: `git log --format=%H -1 --
plans/round-48-claims.md` at run time resolves the freeze to `c8d7da55` (A7 —
amendments A3–A7 landed while this pass ran). All frozen-bytes fixtures below were
run against `ac02a79` (A2, record2 identical to A1) and then re-verified against
`c8d7da55` where noted. `--freeze dc73587 --rev ac02a79` → exit 2
`frozen_path_changed` (`receipts/stale-freeze.json`), which also demonstrates the
freeze-integrity machinery working.

**Worktree caveat.** While this pass ran, `record2.py` was mutated in the worktree
(mtime 16:13, then committed as A7 at 16:09–16:13 timeline). Every fixture below
names the counter bytes it exercised. The A2-era battery result is genuine:
A7's own disclosure paragraph cites the identical red-before (`v2_green 4`,
`v3_green 3`, `ctl-c2-a7-before.json`), so this is an independent reproduction, not
a fork of L1's finding.

## Headline (pre-A7 frozen bytes, `ac02a79`): the battery could not score `v3_green 0`

On a faithful simulated landing (fixture clone `git clone` of the lane at the
freeze, `.ufo/waves/round-48/w1-dispatch.json` + `l1/scores/c2-sim48.json` +
`w1/SimplC2/evidence.json` committed, card appended with
`## Record corrections — round 48` + `## Round 48`), the A2-frozen counter scored:

- structural clauses all green, exit 0 (`receipts/sim2-no-battery.json`,
  `failing []`, `quotes_corrected` shows `exempted 2` corrected to `1`);
- full run exit 1, `battery v3_green 3 != 0` (`receipts/sim2-with-battery.json`);
  `v2_green 5` correct.

Three forgeries scored v3-green:

1. `quote-off-by-one` — `QUOTE.sub(..., count=1)` mutates the **first** match
   card-globally. On the real card that match sits at byte 5758 inside the
   Owned-axes calibration row (`corrections 2` → `corrections 3`), outside the
   two-section scope every clause examines → the mutation is invisible
   (`v3_failing []`). Proven: `receipts/sim2-with-battery.json` fixture
   `quote-off-by-one v3 0`, and the offset/context print in the transcript
   (`in last-two scope? False`).
2. `axes-score-cell-off` — **clause reads the wrong card.** `axis_scores(files)`
   called `files(CARD)` = the committed card at rev, not the `card` text under
   test. The forgery (`9.72 → 9.0`) scored green with `axis_score_bad []` while
   `axis_score_cells` still reported `(9.72, 10.0)` — it can never fail
   (dissect output in transcript; receipt `fixtures.json` epoch A2).
3. `axes-correction-forged` — appends a **second**
   `## Record corrections — round 48` heading; `corrections_section` split on the
   first occurrence, so the forged line was shadowed. `occurrences: 2`, parsed
   lines stayed 3, `corrections_bad []`, v3-green.

**This is the fourth instance of the defect class the round keeps hitting**
(A1: clause reads the wrong cell; A2: classifier rejects honest prose; now:
forgeries whose mutations land outside the scored surface). If any seat had
declared the claim under A2/A1 bytes it would have been unmeetable on the real
landing — the kill rule fires on the genuine artefact.

**Post-A7 status: closed.** A7 re-freezes with `axis_scores(card)`, a
section-scoped `_m_quote_off` (last section), and `_m_axes_correction_forged`
inserting into the first corrections section (`CORR_HEAD` is now a regex).
Re-run on an identical simulated landing at `c8d7da55`:
`{forgeries_total 5, v2_green 5, v3_green 0, genuine_green 1, crash 0}`, exit 0
(`receipts/sim3-A7-with-battery.json`, `sim3-A7-no-battery.json`). The five
fixtures now fail on five distinct clauses — the battery discriminates.
`patched-validation.json` records the intermediate worktree patch scoring the
same `5/5/0/1/0` and `evaluate` correctly exiting 2 `frozen_path_changed`
(because the patch touched `tools/round-48/`).

## Residual findings on the A7 (current) frozen bytes

`receipts/residuals-A7.json` — all runs `record2.py@c8d7da55` inside the fixture.

- **P1 — a `quote` correction is vacuously satisfiable.** `_quote_correction`
  checks only that the stated value is backed by a cited receipt and not already
  quoted. `- corrects quote round-47: mismatches 0` — where the section quotes
  *no* `mismatches` — parses, re-derives, and counts toward `corrections 3`
  while correcting nothing (exit 0). Same inert-correction class R47-CL14
  complained about, one level down. Not load-bearing for the claim's stated
  purpose (the needed `exempted` correction is non-vacuous), but the clause text
  "every line re-derives" now includes lines that repair nothing.
- **P2 — positional scope shift.** "the last two `## Round N` sections" is
  positional: appending a re-derived `## Round 41` copy moves scope to
  `(48, 41)`. The *identical* card + lie (`-- tools/` in round-47's window)
  scored exit 1 in scope and **exit 0** shifted — `oracle_mismatches []`,
  `failing []` (`R6a`/`R6b`, and re-confirmed at A7). Every clause — oracle,
  floor, quotes, axes — examines the same positional window, so a lie pushed
  out of it is invisible to all of them. The claim text licenses the reading;
  it's a bounded-scope fact to record, not necessarily a defect — but it is the
  cheapest forgery shape the floor does not price.
- **P3 — a second corrections heading is still shadowed.** A card carrying a
  *genuine* `## Record corrections — round 48` section plus a later duplicate
  heading keeps the dup's lines unparsed (`residuals-A7` →
  `P3_second_heading_parsed_lines: 3`, unchanged from pre-A7). A7 fixed the
  *forgery* to insert into the first section, but the parser's first-occurrence
  split remains: any later same-named heading is dead text to the counter.
- **P4 — axes-clause edge states.** (a) A fraction-shaped score cell
  (`9/10 → 10.0`) is read by `SCORE_CELL` as `(10, 10.0)` and `FRAC` binds the
  *post-cell* `138/138` → green under the implementation, but the claim text
  binds "the first `n/d` fraction in that row" = `9/10` → wants `9.0`: a
  text-vs-implementation divergence, needs an exotic row so severity LOW.
  (b) A `coverage`/`depth` row with no `a → b` cell is skipped entirely →
  vacuous green (`axis_score_cells {}`) — clause is conditional on a parse that
  can silently not happen. (c) `calibration` is whitelisted out of both
  `AXIS_SCORE` and `collect_axes`; its row's fraction is unexamined. Licensed
  by the claim ("for the `coverage` and `depth` rows") — a disclosed gap.
- **P5 — floor's seats arm accepts a non-re-derived correction.**
  `corr_by_round` is built from *parsed* lines before re-derivation:
  `- corrects seats round-48: 1 waves, 99 seats total` (derived 75) sets
  `seats_via_correction: true`, satisfying the arm internally; the separate
  corrections clause is what actually catches it (card still exits 1). The
  claim says "a *re-derived* `seats` correction" — the floor's own
  `seats_via_correction` flag overclaims. Reporting-accuracy defect.
- **Oracle delegation is half-pinned (R47-CL1 partial).** `oracle()` execs the
  round-47 module's *committed* bytes, but its `import gate` resolves to the
  already-loaded worktree `gate` module (`ns["gate"].__file__` =
  `tools/round-46/../round-46/gate.py` — receipt `fixtures3.json`). Only the
  oracle's text is rev-pinned; `gate.show`/`git` plumbing (which every atom and
  record2 itself pipes through) is worktree-mutable, and `dirty()` watches only
  the round-48 frozen set, so a dirty `gate.py` is invisible to
  `frozen_worktree_dirty` under *this* claims file. A hostile `gate.py` would
  execute at oracle import time. Medium latent, needs worktree write access.
- **Inherited oracle defects (record.py@c8d7da55, not frozen but load-bearing
  via delegation).** (a) `corrects()` lines 292–299: a second `cls == "axes"`
  branch that is unreachable dead code and references `atom` (undefined in that
  scope — would `NameError` if reached). (b) `evaluate_text` line 328:
  `known_pairs` assigned, never read — dead store. (c) `exempt()` exempts a
  pair-less `window` atom under *any* window correction regardless of key:
  receipted live — `sim-no-battery.json` (A2 epoch) shows a window atom keyed
  `48` exempted by `corrects window round-46`; a stray `is empty` line in the
  landed section would be silently forgiven. record2 inherits all three via
  delegation.
- **Dead weight in record2.py (YAGNI hits).** (a) `score()`'s
  `elif key in fixed and int(val) != fixed[key] and any(quote_value(r,key) ==
  fixed[key] ...)` — the last two conjuncts are provably dead: `fixed[key]` is
  populated only when `value not in quoted` and `backed`, which imply both
  invariants (proof in report body; `elif key in fixed:` suffices). (b)
  `len(secs) != 2` in `score()` duplicates the oracle's identical check one
  call deeper — reachable only because it runs first; pure duplication of
  `sections()` (itself a copy of the oracle's `sections`). (c) `import shutil`
  is used only in `selftest` — keep or inline.
- **Spec/impl tightness notes.** `RECEIPT` admits only `l1/scores/*.json`
  receipts (controls can't back a quote — stricter than spec, fine);
  `CLAIM_ID = R\d\d-C\d` can't match a two-digit claim id (`R48-C10` fails on
  `\b`) — latent; "a quoted number" in the claim reads card-wide but the clause
  checks section-scoped quotes only (the A7-forgery fix now matches the clause's
  own scope); a bare directory `.ufo/waves/round-N/w1/` is a valid `path` atom
  (`git show` on a tree succeeds) — trivially satisfiable but claim-conformant;
  `run_battery` marks a no-op mutation `v2_green` without ever scoring it v3 —
  `v3_green 0` can be met by five unexercised forgeries (A7's fixes make all
  five land today, so latent); `crash` counts only pre-clause exit-2s — a
  forgery that crashes mid-clause propagates to `main_guard` exit 2 without
  incrementing `battery.crash`.

## Per-element verdict (the four named YAGNI targets)

- **`quote` correction class: KEEP — load-bearing.** The genuine landing
  *requires* it: round-47 quotes `exempted 2`, the committed receipt exempts 1,
  so clause 4 can only be green via a re-derived quote correction — verified
  working (`sim3-A7-no-battery.json`, `quotes_corrected`). It also earns its
  keep negatively: `gold-tautology`'s v3 red includes "corrections that do not
  re-derive: 1" (the forged section cites no receipts). Deletable weight: the
  two dead conjuncts in the `elif key in fixed` escape; recommended tightening:
  require `value` to differ from *some* quoted value or require a quoted key
  match — i.e. forbid vacuous corrections (P1).
- **`axes` clause: KEEP — now correct.** A7's `axis_scores(card)` is the right
  fix (clause must read the text under test). Residual: P4a text-vs-impl
  fraction binding, P4b vacuous skip, P4c calibration blind (licensed). No
  dead weight found in the clause itself.
- **Floor per-section granularity: KEEP — with two reporting fixes.** The
  granularity (seat/path/rev/claims per section + cross-section claim-id
  uniqueness) is exactly the R47-CL10 closure the claim needs; `gold-tautology`
  and `seats-moved` both die on it. Defects: P5 (`seats_via_correction` doesn't
  wait for re-derivation) and P2 (positional window — record, maybe document).
  `section_bodies` duplicates oracle `sections` — collapse to `mod["sections"]`
  (identical contract) and drop the redundant `len(secs) != 2` pre-check if
  kept. Deleting either is safe: both produce identical `(rnd, body)` pairs —
  verified by construction; the duplicated code is what would silently diverge.
- **Oracle delegation: KEEP — the rev-pin is the point of the claim.** Six
  entry points all present at `c8d7da55` (`evaluate_text`, `collect`,
  `collect_axes`, `corrects`, `axis_pairs`, `dispatch_counts`). Weight to shed:
  the dead `axes` branch and `known_pairs` in the oracle (inherited, not
  frozen — L1's call whether to repair round-47 bytes; the freeze union would
  flag `tools/round-47/` only if a *future* claims file freezes it, so touching
  it is mechanically safe but historically odd). The `gate` half-pin is the
  honest residual of "executed from --rev".

## Landing evidence notes for L1

- At `c8d7da55` do-nothing is red exactly as claimed:
  `['round-47: no seat atom and no re-derived seats correction',
  'no \`## Record corrections — round 48\` line re-derived',
  'quoted numbers with no backing receipt: 1']`
  (`receipts/ctl-do-nothing-A7.json`, exit 1). The single unbacked quote is
  `exempted 2` — the thing the mandatory quote correction repairs.
- Landing must commit `.ufo/waves/round-48/w1-dispatch.json` (untracked at
  freeze) or no round-48 seat atom/correction can re-derive; the w1 report dir
  must be committed or `gold-tautology`'s `.ufo/waves/round-48/w1/` path atom
  mismatches and `v2_green` drops to 4 (proven: `sim-with-battery.json` vs
  `sim-with-battery-2.json`).
- Keep stray `is empty` phrases off their own lines in the landed section —
  they collect as pair-less window atoms which any window correction exempts
  (receipted, A2 epoch). Pair the `A..B` on the same line.
- The simulation card that scored the A7 counter `5/5/0/1/0` is fixture commit
  `db364b15` (clone at `/fast/scratch/…/fixture`, removed after reporting);
  `sim3-A7-*.json` are the receipts to cite.

## Installs

None. `python3 -I -B`, `git`, `sha256sum` only. Pacman paused per directive.

## Method note

`lsp` device is not mounted in this session → deletion-candidate caller checks
used text-grep + import-graph reading (declared per role fallback). Fixture repo:
`git clone` of the lane at `$S/fixture`, `rev-parse --show-toplevel` asserted
before every mutation; all commits under `simplc2@fixture.local` inside the
clone only. Lane tree: zero writes outside this report dir (verified:
`git status --porcelain` shows only pre-existing sibling modifications plus my
`?? .ufo/waves/round-48/w1/SimplC2/`).

## Peer note

Received `DISALLOWED` from `C2Floor` mid-run with no question or content;
treated as a stray/broadcast artifact, no action taken.

## Receipt index (`receipts/`, sha256-16)

| file | epoch | what it proves |
|---|---|---|
| `stale-freeze.json` | real lane | prompt's `dc73587` freeze → exit 2 `frozen_path_changed` at `ac02a79` |
| `freeze-rev.json` | real lane | `frozen_worktree_dirty` while L1's patch sat uncommitted |
| `ctl-do-nothing-A7.json` | real lane | do-nothing red, exact three failing clauses at `c8d7da55` |
| `sim-no-battery.json` / `sim-with-battery{,-2}.json` | A2 fixture | green struct + `v3_green 3` kill trip; stray window-atom exemption |
| `sim2-*.json` | A2 fixture (clean card) | `v2 5 / v3 3 / genuine 1 / crash 0` — the unmeetable battery |
| `patched-validation.json` | A7 worktree patch | patch scores `5/5/0/1/0`; `evaluate` → `frozen_path_changed`; heading-shadow residual |
| `sim3-A7-*.json` | A7 fixture | frozen counter fully discriminating on simulated landing |
| `fixtures*.json` | A2 fixture | vacuity, scope-shift, axes divergence, delegation audit |
| `residuals-A7.json` | A7 fixture | P1–P5 residual defects on current frozen bytes |
