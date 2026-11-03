# ScribeLesson — round 65 w1

Seat: ScribeLesson (scribe, leaf). Scope: draft the round-65 lesson's `## Mistakes` rows and one
QUALITY candidate from evidence already on disk; read-only to the lane. No scratch dir was
created, no clone, no matrix run, no install.

## Behavior

Read the base revision `c99e907cb5576c13a7b22755d776b356fdfc1752` and the round-65 evidence
already written by L1 and by the ExecControls/ExecCoverage seats, then drafted:

- two Mistakes rows (M65-1 process/scope, M65-2 number-drift/stale-premise) in the lane's
  `id | class | evidence pointer | captured-by | fix` form;
- one QUALITY candidate criterion;
- for each row, the exact command that resolves its evidence pointer.

Draft: `.ufo/waves/round-65/w1/ScribeLesson/draft.md`.

## Gates

- QUALITY #33 order: the two instruments' sha256 recomputed at the base are the frozen ones —
  `9434888e…fcf83995a6` (`coverage-recipe.py`), `79a4dca4…77ff922c6` (`jsc-closure-matrix.py`);
  they match `claims.json` `instruments`.
- R65-C1 evidence used: `l1/probe/dryrun-matrix.json` (closure `entries` 30, `cache_present` [],
  `ok` true, census `equal` true, 18/18, exit 0) and the ExecControls red/green cache arm
  (`cache-present.json` ok false with 2 named entries, exit 2; `cache-clean.json` ok true,
  30 entries, exit 0).
- R65-C2 evidence used: `l1/c2-before-date.json` (144 → 142, `population_dropped` 2,
  `mismatches` 2, exit 1) and `l1/c2-after-stem-at-base.json` (144/144, `mismatches` 0, exit 0).
- Cache-free state re-checked read-only at this write: `find … -name '__pycache__' -type d` → 0,
  `find … -name '*.pyc'` → 0.

## Touched surfaces

- wrote `.ufo/waves/round-65/w1/ScribeLesson/draft.md`
- wrote `.ufo/waves/round-65/w1/ScribeLesson.md` (this report)
- nothing else; no edit to `corpus/lessons/round-64.md`, `corpus/QUALITY.md`, `SCORECARD.md`,
  `tools/`, or the toolchain.

## Findings

1. **F-1 — the assigned QUALITY number collides.** The seat spec says the highest criterion is 93
   and the next free is 94. At the base the table stops at 93 but the appended correction bullets
   already carry rows 94–101 (`corpus/QUALITY.md:151` in the base blob is row 94). The next free
   number is 102; the drafted row is numbered 102 and carries the number-conflict block verbatim.
   Filing it as #94 would duplicate a live criterion.
2. **F-2 — the frozen C2 receipt counts the hidden files, it does not name them.**
   `coverage-recipe.py:104` computes `dropped = len(files) - len(population)` and `:108` emits it
   as an integer; `missing` and `dangling` are empty on the date arm. The predicate clause
   "`population_dropped` naming the files it hides" is therefore not discharged by
   `c2-before-date.json` alone. The two names are `jsc-mapper-cli-contract` and
   `jsc-mapper-release-inventory`, produced by a separate read-only `git ls-tree` command (in the
   draft) and asserted in plan prose (`plans/round-65-claims.md:90`). Any filing that cites the
   receipt for the naming half is citing prose, not instrument output.
3. **F-3 — M65-1's captured-by is not "none".** r64 ReviewerMatrix `review.md:24` F2 is the
   committed observation (blocking, `cwd=view8_dir` writes `__pycache__` into the frozen tree).
   What was absent in r64 was a criterion and a predicate clause, not the observation; the row
   records the capture and names the gap.
4. **F-4 — the stale premise is revision-dependent.** On `df727606` both recipes report 142/142,
   `population_dropped` 0, exit 0 (`w1/ExecCoverage/c2-ctrl-date-df727606.json`). The date
   recipe is observably wrong only once a non-dated entry exists; the lesson must not claim it
   was always red.
5. **F-5 — M65-1's red arm is synthetic.** `x.pyc` is planted in a scratch copy, so the arm
   exercises the refusal, not the round-64 file set; the prep receipt states the 15 filenames
   were not retained. No draft sentence asserts those bytes.

## Out of scope (not done here)

- No verification of R65-C1 or R65-C2 — no matrix run, no counter re-run; this seat reports only
  receipts already committed by L1 and the executor seats.
- No `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` or lesson file edit (host guard and seat spec).
- No mutation, closure review, provenance or sources work (other seats).
- No judge of the number conflict beyond stating it; the canonical Rust judge decides.

## Artifact paths

- `.ufo/waves/round-65/w1/ScribeLesson/draft.md` (rows, QUALITY row, resolving commands, findings)
- `.ufo/waves/round-65/w1/ScribeLesson.md` (this report)
