# ScribeLesson — round-48 lesson draft

## Behavior

Read `plans/round-48-claims.md` in full before any command. Drafted
`corpus/lessons/round-48.md` at `.ufo/waves/round-48/w1/ScribeLesson/lesson.md`,
merge-compatible with the L1's staged skeleton (`corpus/lessons/round-48.md`
untracked in the worktree: same header, `## Gate`, `## Mistakes`,
`## Freeze series (disclosed)`, `## Routed defects (for round 49)`), upgraded with
every landed wave-1 report, the six committed controls and the L1 scores dir.

- `## Mistakes`: three rows. M48-1 `vacuous-clause` (the spec-named candidate: A1's
  `axis_scores()` read the evidence cell, green over zero rows — same class shape as
  round-47's A2/A5 no-op forgeries); M48-2 `type-confusion-equality` (A3's
  dict-vs-list census comparison, unreachable by construction); M48-3
  `false-green-class-pair` (A4's two demonstrated accept-what-it-rejects holes).
  Each row carries class, evidence pointer, captured-by (`none` for A1–A3;
  adversarial wave seats for A4 — the 16-case selftest passed while both A4 holes
  were open) and fix-with-red-before.
- `## Routed defects (for round 49)`: seven new R48-CL items plus the inherited
  still-open list, plus the landing-gate list distilled from measured reds.
- `## Gate`: six rows covering the L1's staged S145/S146 (unmodified), ScribeSources'
  filed S147/S148 and ScoutSources' pair — provisional S149 (`argparse` admit,
  scoped to `ArgumentParser.error`) and S150 (FreeBSD `sysexits`, a second scoped
  rejection: `EX_USAGE` is 64, falsifying the registry's `2=usage` mapping).
- `## Freeze series (disclosed)`: `7fe11332` → A1 → A2 → A3 → A4 with defect class
  and red-before each; the prompt-declared `dc73587a` (A1) is superseded — the
  claims file's own derivation resolves A4 — routed as R48-CL5 (R47-CL11 recurrence).

## Gates / evidence exercised
- `## Gate` revision (post-review): ScoutSources-4 corrected the draft — the FreeBSD
  /OpenBSD `sysexits` captures are a separate rejected row (provisional S150), not a
  merge into S146: quoting `EX_USAGE` returns 64, which falsifies S146's flip rather
  than satisfying it. S146 is unmodified; S149 is marked provisional-and-scoped to
  `ArgumentParser.error` only (status `queued` until the landed lesson cites it).
  ScribeSources-2 verified S147's redirect note after correction.

- `git log`/`git show`/`git status` read-only over base `61b87d74`, freeze series
  `7fe11332`/`dc73587a`/`ac02a79f`/`f3a7afc4`/`0f06251b` and tip `663f30ee`.
  Verified `tools/round-48/meanings.py` sha256: A2 `74b8da35…`, A4 `cd4dbad8…`,
  worktree `00f768c5…` (equals A4 per `git status` post-A4 commit).
- Classifier probe (executed, not reviewed): extracted the A4 `meanings.py`,
  `census2.py`, `gate.py` into scratch, imported `meaning_classes` over seven
  verdict maps. Output retained at `w1/ScribeLesson/classifier-probe.json`:
  `0=not clean`, `0=never passed`, `1=not failed`, `2=no error` all classify green —
  the A4 `NEGATED` guard covers only `not met`/`no verdict` on digit 0. Basis of
  routed R48-CL1. Receipt: `.ufo/waves/round-48/w1/ScribeLesson/classifier-probe.json`.
- Source fetches for Gate candidates (curl, 2026-10-28T18:51:57Z, all HTTP 200):
  argparse `521adff647…` (334,734 B), sys `867b5a26…` (280,618 B, screened),
  OpenBSD sysexits `4cf3eb9d…` (12,147 B). Receipt:
  `.ufo/waves/round-48/w1/ScribeLesson/gate-sources.txt`. Reconciled with
  ScoutSources-4 (pin its `3.14` URL+digest `896dc9a8…`, not mine) and
  ScribeSources-2 (its S147/S148 appended; my pair renumbered to provisional
  S149/S150).
- Read all 25 `w1/*.md` reports + `C1IdsArms`, `C1Struct-2`, `C2Gold`, `C2Quote`,
  `l1/block25.md`, `l1/scores/probe-record47.json`, all six `controls/*.json`,
  `w1/ScribeSources/sources.md`, staged `corpus/SOURCES.md` rows S145/S146 and the
  untracked lesson skeleton.
- `disk-guard.sh status` run before the heavy pass (`/fast/scratch/hyaku` ~32%).

## Key findings returned to the L1

1. **R48-CL1 (HIGH, measured):** residual classifier false-greens at A4 — four
   negated/out-of-vocabulary maps classify green (`classifier-probe.json`).
2. **R48-CL2 (MEDIUM, measured):** A3 binds only `derived["paths"]`; the `named`
   map may drift (`ExecCensus`: 5-vs-4 round-48 names, equal path set, different
   doc sha).
3. **R48-CL3 (MEDIUM, measured):** every battery skips on a non-green genuine card;
   kill rules unexercised pre-landing; claimed `ctl-c1-1-v2-profile.json` absent.
4. **R48-CL4 (HIGH):** R47-CL1 closed for the oracle, open for `gate.py` (worktree
   `sys.path` import; `C2OracleLimit`) and for the counter scripts themselves.
5. **R48-CL5 (HIGH):** freeze-as-series — all wave receipts are at A1 while the
   derivation resolves A4; pin `74b8da35…` in `l1/block25.md` is the A2 bytes, not
   A4 `cd4dbad8…`; R47-CL8/CL11 recur.
6. **R48-CL6 (MEDIUM):** forced three-class partition invents verdicts for
   probes/libraries (`C1Semantic`).
7. **R48-CL7 (LOW):** `--json-out` lane-root policy couples receipts to the tree.
8. Landing must include: a re-derived `seats` correction for round 47, a
   `corrects quote round-47: exempted 1` line (proven to re-derive by
   `C2Quote/misquote-repaired.json`), backed quoted numbers, and the C1 pin taken at
   the landing revision.

## Touched surfaces

Only `.ufo/waves/round-48/w1/ScribeLesson.md`,
`.ufo/waves/round-48/w1/ScribeLesson/{lesson.md, classifier-probe.json,
gate-sources.txt}`. No product/frozen bytes modified; no git mutation; no installs.

## Out of scope / not run

No full `meanings.py`/`record2.py` counter run by this seat (other seats' receipts
cited, each named). `sources-census.sh validate` not run (L1 lands the rows).
`ScoutAssim`/`CritAssim` reports absent at draft time; assimilation recorded as
"none taken in this draft" per the staged skeleton. Scratch
`/fast/scratch/hyaku/kaidoku-r48/ScribeLesson` removed after receipts copied in.
