# ScribeQualityRow — QUALITY row draft (the A1 vacuous-clause defect)

Report: `.ufo/waves/round-48/w1/ScribeQualityRow.md` (seat file; no subdirectory needed, no heavy receipts — evidence is short and quoted inline).

## Draft — appended-bullet section, house style (`corpus/QUALITY.md` tail)

- **Row 88 added after the round (a clause that scores nothing is not a clause).**
  `record2.axis_scores()` at the first freeze read the *evidence* cell where it meant the
  *score* cell — `SCORE_CELL.search(cell[1])`, corrected to `cell[0]` by A1 — so clause 5
  went green over `axis_score_cells {}` with `axis_score_bad []`: consistency over zero
  rows, the same "measures consistency, never completeness" class the claim exists to
  close (`plans/round-48-claims.md` `## Freeze amendment A1`; red-before
  `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` at `7fe11332` showing
  `axis_score_cells {}`, vs the populated `coverage`/`depth` cells in
  `ctl-c2-0-do-nothing.json` at `dc73587a`). The rule the next round applies: the
  pre-freeze do-nothing run must publish, per clause, the card fields that prove a
  non-empty input set was evaluated — cell counts, row lists, matched ids — and a clause
  whose scored population is empty at the freeze is a defect to amend before data, never
  a green.

Two sentences, matching the `**Row N added after the round (theme).**` bullet convention of rows 75–78.

## Numbering decision (deviation, stated)

The seat asked for "row 79 (or the next free number)". **79 is not free**: the admission-criteria table already carries `| 79 |` (round-38 freeze-drift row, committed `3b960fe5`), and table rows run through 87. The appended bullets re-used 75–78, colliding with table rows 77/78. I drafted **row 88**, the first number free in both sequences. If the integrator intends the bullets' own local counter, the same text renumbers to "Row 79" on landing — the body carries no number dependency.

## Verified facts behind the draft (read-only git)

- `git diff 7fe11332..dc73587a -- tools/round-48/record2.py`: one line — `SCORE_CELL.search(cell[1])` → `SCORE_CELL.search(cell[0])` in `axis_scores()`; matches the A1 paragraph verbatim.
- `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` (worktree, controls are not frozen): `freeze=rev=7fe11332…`, `axis_score_cells {}`, `axis_score_bad []`, `failing` names floor/quote clauses only — the green-over-zero-rows receipt.
- `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json`: `freeze=rev=dc73587a…`, `axis_score_cells` populated (`coverage` fraction 138/138 score [9.72,10.0]; `depth` 24/24 [10.0,10.0]) — post-A1 cells are bound. (The claims file names this file as A1's red-before "(`axis_score_cells {}`)"; at HEAD it is populated. The receipt that *at HEAD* shows the vacuous state is `ctl-c2-a1-before.json`; I cite both so the pointer resolves for a reader at the landing revision.)
- Numbering: `grep -n '^| 7[0-9] |\|^| 8[0-9] |' corpus/QUALITY.md` → table rows 70–74, 77–87; bullets 75–78 appended (`git log` shows bullets 77/78 landed `49e6cac4`/`caafeffa` after table rows 77/78 landed `01a44dbf` — a known collision).
- Controls directory `.ufo/waves/round-48/` is entirely **untracked** at HEAD (`git status --porcelain`: `?? .ufo/waves/round-48/`); the control receipts named in the claims file exist in the worktree but are not committed yet — expected, controls are "committed as wave evidence" at landing.

## Frozen-state note for the L1 (observed, not acted on)

My prompt declared freeze `dc73587a8b9c…` (A1). The committed claims file at HEAD
`f3a7afc4` carries `## Freeze amendment A3` (census `derived["paths"]` comparison) whose
text declares the freeze to be "the commit that carries this paragraph" — i.e.
`f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`, two commits past the prompt's freeze.
`tools/round-48/` at HEAD thus differs from the prompt-declared freeze. Scribe scope was
the A1 row only, so no action taken; flagging because any report citing `dc73587a` as the
freeze is one amendment stale.

## Commands run (all read-only)

- `git diff 7fe11332..dc73587a -- tools/round-48/record2.py plans/round-48-claims.md`
- `git show 7fe11332:tools/round-48/record2.py | grep -n axis_score`; same at `f3a7afc4`
- `git log --format='%h %cI %s' -- corpus/QUALITY.md`; `git log -- <controls path>` (empty — untracked)
- `python3 -c` JSON dumps of three committed/worktree control receipts (quoted above)
- `scripts/hyaku/disk-guard.sh status` — `/fast/scratch/hyaku` 32% used, 546.8 GiB free.

Installs: none. Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeQualityRow` created, unused, removed before yield. No mutations to lane, frozen paths, or fixtures; no git mutations anywhere.
