# ScribeAxesRow — round 47 w1 report

Seat: ScribeAxesRow (leaf; no subagents). Scope: draft the replacement `coverage` and
`depth` cells of `SCORECARD.md` `## Owned axes` so each leading fraction equals the
observable at the round-47 landing, keep the historical chain, give every value its
counting command and revision, and verify the draft against the frozen counter.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base
`13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`; first landing `e856beb5`; round's measured
revision `a0753786`; lane head at hand-off `f7d6e58d` (24/24 and 138/138 re-measured
there, `receipts/measure-f7d6e58d.stdout.txt`); freeze re-derived at hand-off
`f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (A6). The lane moved under me during the
seat (six disclosed freeze amendments, a seven-commit series, all committed by the L1); every
number below is against a committed revision, not the worktree.

## Behavior

- Drafted both cells: head `138/138` and `24/24`, historical tails byte-identical.
  Full replacement rows: `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/cell_lines.txt`,
  sha256 `0d89e5433eb98a5494a65056a27f7c5f51290479f1049a6637a651d176d0be3e`.
  The exact head-clause delta and per-value provenance are in
  `.ufo/waves/round-47/w1/ScribeAxesRow/axes.md`.
- Measured both fractions two ways at every relevant revision: SCORECARD recipe A
  verbatim, and the frozen counter's `coverage_pair`/`depth_pair`.
- Validated the draft without writing the lane: SCORECARD at `a0753786` with rows 23–24
  substituted in memory, scored by `record.evaluate_text` → exit 0, `mismatches []`,
  `corrections_bad []`, `met_target true`, `verified 41`.
- Attacked the depth derivation with an isolated one-commit fixture.

## Gates (exact commands and outcomes)

| check | command (cwd = lane root) | exit | result |
|---|---|---|---|
| axes at base `13a9e9e1` | `python3 -I -B .ufo/waves/round-47/w1/ScribeAxesRow/receipts/measure_axes.py --root <lane> --rev 13a9e9e1` | 0 | 138/138, 23/23 both derivations |
| axes at `e856beb5` (first landing) | same, `--rev e856beb5` | 0 | 138/138; depth recipe A **23/24**, `depth_pair` **24/24** |
| axes at `07d2894e` (A5) | same, `--rev 07d2894e` | 0 | 138/138; depth 23/24 vs 24/24 |
| axes at `04469ee8`..`31b092d1` | same, `--rev 04469ee8` / `a0753786` / `31b092d1` | 0 | 138/138; depth **24/24 both** |
| counter C2 at measured revision | `python3 -I -B tools/round-47/record.py --root <lane> --rev a0753786` | 0 | `mismatches []`, `corrections 2`, `corrections_bad []`, `met_target true` |
| counter C2 at head | same, `--rev 31b092d1` | 0 | `mismatches []`, `met_target true` |
| counter C1 at measured revision | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze f54b3b6d --rev a0753786` | 0 | `v2_green 4`, `v3_green 0`, `genuine_green 1`, `crash 0`, `forgeries_total 4` |
| counter C1 at head | same, `--rev 31b092d1` | 0 | `met_target true`, `failing []` |
| C1 at first landing, then-declared freeze | `--freeze 9018c53b --rev e856beb5` | 1 | `arm cells not exact vocabulary tokens` (prose cells); battery skipped |
| stale freeze vs measured revision | `--freeze 07d2894e --rev a0753786` | 2 | `frozen_path_changed ["tools/round-47/", "tools/round-47/exact.py"]` |
| draft cells scored | `python3 -I -B .ufo/waves/round-47/w1/ScribeAxesRow/receipts/validate_draft.py --root <lane> --rev a0753786` | 0 | `mismatches []`, `met_target true` |
| self-citation fixture | `python3 -I -B .ufo/waves/round-47/w1/ScribeAxesRow/receipts/fixture_selfcite.py --scratch <scratch>` | 0 | `record_depth_pair (1,1)` vs `recipe_a 0/1`, `divergence true` |

Receipts: `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/runs.jsonl` (exact argv, cwd,
UTC, exit, stdout sha256 per run) and the matching `*.stdout.txt` files.

## Findings

1. **Depth derivation ≠ command A (calibration).** `record.py:116` says `depth_pair` reads
   "exactly as command A reads them"; `record.py:42` uses
   `(?:corpus|plans|tools)/…` while recipe A (`SCORECARD.md:105`) matches only
   `corpus/knowledge/…`. At `e856beb5`, `1e2c3102` and `07d2894e` that meant
   `depth_pair (24,24)` vs recipe A `citation_resolved_rules 23` / `rule_blocks 24`; the
   landed correction lines (`SCORECARD.md:3677-3678`) claimed command A reads 24, which
   was false at those revisions. `04469ee8` added a `corpus/knowledge/...:40-66` citation
   to block 24, and from that commit both derivations read 24/24. The frozen claims row
   `plans/round-47-claims.md:154` still describes the atom as "command A's
   citation-resolution count", which misdescribes the frozen scorer. Fixture shows a block
   citing only `tools/round-47/exact.py` scores `1/1` under `depth_pair`, `0/1` under
   recipe A — the axis is movable by a non-domain citation.
2. **C1 failed at the first landing.** `exact.py` exit 1 at `e856beb5` because the four
   v3-arm cells were prose (`symbol: …`), not the exact token; fixed at `62e33f7d` (A2).
   Passes at the measured revision with the full battery.
3. **Freeze drift.** The seat prompt's freeze `5017e1f` is stale: the claims file declares
   a seven-commit series and the `## Round 47` section now declares A6 `f54b3b6d`;
   `exact.py`/`record.py` changed at A6, so a run against an earlier freeze exits 2
   `frozen_path_changed`. The counter's freeze must be re-derived with
   `git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/`.
4. **Evidence text.** The landed cells and the axes correction lines cite the directory
   `.ufo/waves/round-47/l1/scores/` (empty at 14:52Z, populated later) and embed a literal
   `<rev>` placeholder in the `git ls-tree` command; my draft cites the actual receipt at
   the measured revision and replaces `<rev>`.

## Touched surfaces

- Written: `.ufo/waves/round-47/w1/ScribeAxesRow/` (deliverable + receipts + report
  inputs) and this file `.ufo/waves/round-47/w1/ScribeAxesRow.md`.
- Not written: `SKILL.md`, `SCORECARD.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, the
  fleet repo, `.ufo/state/`, other seats. Verified at hand-off:
  `git status --porcelain -- SKILL.md SCORECARD.md plans tools` prints nothing.
- No git/jj mutation ran anywhere; read-only commands only (`log`, `show`, `rev-parse`,
  `status`, `diff`, `cat-file`, `ls-tree`). Fixture commits ran only inside
  `$HYAKU_SCRATCH` with `git -C "$D"` after asserting the toplevel.
- No installs. No use of `/tmp`. `$S` removed after the receipts were copied here.

## Out of scope / not run

- No landing, no counter repair, no frozen-byte change; the two claims are L1's
  instruments and remain as committed.
- Not run: `exact.py --selftest`, `record.py --selftest`; a standalone v2-profile control;
  mutation of the coverage map. Not claimed as passed.
- The fixture repo was deleted with the scratch root after its receipt (content sha256
  `68b43eee…` is recorded in `receipts/fixture-selfcite.stdout.txt`).

## Artifacts

- `.ufo/waves/round-47/w1/ScribeAxesRow/axes.md` — exact cell text, provenance, findings.
- `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/cell_lines.txt` — byte-exact replacement rows.
- `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/{measure_axes,validate_draft,fixture_selfcite}.py`.
- `.ufo/waves/round-47/w1/ScribeAxesRow/receipts/runs.jsonl` + `*.stdout.txt`.
