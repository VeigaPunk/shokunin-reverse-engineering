# C2Axes — Owned-axes score-cell probe

## Axes

- **Coverage:** calibration of the scorecell parser against the adjacent score column and its fraction.
- **Depth:** adversarially test frozen clause 5 for stale-score acceptance.
- **Calibration:** preserve exact observed counter output, including the genuine artifact's independent failing clauses.

## Retained evidence

Frozen specification: `plans/round-48-claims.md` at declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`, clause 5 (lines 96–98) requires the second number of coverage/depth score cell equal `round(10*n/d,2)` for the first fraction in that row. A1 notes the former `axis_score_cells {}` vacuity and parser change to `cell[0]` (lines 133–145).

Control evidence read: `.ufo/waves/round-48/controls/ctl-c2-a1-before.json` records `axis_score_cells: {}`, `axis_score_bad: []`, and `met_target: false`; it also identifies first freeze `7fe11332781356ec3d5b0b314698de27dd25b50d`, not the declared A1 freeze.

Counter source at freeze: `tools/round-48/record2.py` lines 140–156 parses `score` from `cell[0]`, fraction from the remaining cells; lines 303–315 compares score's second value to rounded fraction. Lines 443–471 show mutation battery only runs on a structurally green card.

Command actually run (exit **1**):

```sh
S=/fast/scratch/hyaku/kaidoku-r48/C2Axes
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
export TMPDIR="$S" HYAKU_SCRATCH="$S"
python3 -I -B "$R/tools/round-48/record2.py" --root "$R" --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out "$R/.ufo/waves/round-48/w1/C2Axes/receipt.json"
```

Stdout JSON is retained verbatim at `.ufo/waves/round-48/w1/C2Axes/receipt.json`; stdout SHA-256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`; UTC `2026-10-28T18:47:54Z`.

Observed exact `axis_score_cells`: coverage fraction `[138,138]`, score `[9.72,10.0]`; depth fraction `[24,24]`, score `[10.0,10.0]`; `axis_score_bad: []`. This demonstrates the A1 parser no longer returns an empty set and correctly interprets coverage's score cell as distinct from the evidence fraction. It does **not** prove stale-score rejection: at this revision both score cells currently equal their derived values.

The counter output reports `met_target:false`, oracle `mismatches:[]`, and failures: round-47 lacks seat atom/correction; no round-48 corrections re-derived; one quoted number lacks backing receipt. Battery was skipped due to structural failure. Thus no claim that battery passed or that the whole C2 predicate passed.

## Stale score attack status

Not run. This seat contract permits writing only this report path; clause requires modifying a committed card fixture/revision or mutating a copy of frozen tools, and no permitted fixture workspace or scratch receipt path was available within the scoped path restriction. Do not infer stale-score rejection from the genuine score values; the probe shows parser coverage, not adversarial clause behavior.

## Evidence integrity / limitations

No receipt wrapper with command/exit/stdout-hash/UTC fields was produced by the counter command itself; command and exit are documented here and the stdout JSON is retained. Disk guard status was run before work; it reported `/fast/scratch/hyaku` 32% use. No installs. No build, test, lint, or formatter run. No source-tree or frozen-file edits.
