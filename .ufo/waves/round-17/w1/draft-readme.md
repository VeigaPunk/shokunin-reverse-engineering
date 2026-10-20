# Draft: corpus/README.md edits for the round-17 Go carrier row (w1, DraftReadmeRow)

Status: DRAFT, NOT APPLIED. Apply only in the landing commit that also adds
`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`. README rule
(`corpus/README.md:8-9`): a row is written when its file exists, never before.

Baseline: `corpus/README.md` clean in the worktree at HEAD `b563c79`
(`git diff --stat HEAD -- corpus/README.md` empty). Line numbers below are HEAD numbers.
`.ufo/gates/citation-drift/pointer-table.json` is NOT edited (sha256 `7994eec7…789d1`, matches `expected.json` `pointer_table`).

## Pinned README lines (must not move)

| pin id | citing location | README line held | content that must survive |
|---|---|---|---|
| readme22-r7range / readme22-r8range | pointer-table.json:170, :182 | `corpus/README.md:22` | r7 range `…pe-wall.md:(\d+)-(\d+)` |
| readme175-sc1217 / -r7range / -r8e2 | pointer-table.json:208, :219, :231 | `corpus/README.md:175` | `SCORECARD.md:(\d+)`, `pe-wall.md:(\d+)-(\d+)`, `round8/E2.md:(\d+)-(\d+)` |
| sc69-readme-177 | SCORECARD.md:69 → pattern pointer-table.json:57 | `corpus/README.md:180` | `held, not frontier` |
| sc72-readme-nitrow | SCORECARD.md:72 → pattern pointer-table.json:68 | `corpus/README.md:138` | `4 nits: 2 fixes applied at integration` |
| readme38-arc3r1-token | pointer-table.json:407 (anchor, line unpinned) | token anywhere | `2026-10-19-arc3-r1-evm-real-solc` |

Rule for this draft: no line in 1-181 changes its line number. Only in-place text
edits on line 35, and one insertion after line 181 (shifts 182+, which no pin references).

## Edit 1 — coverage-map Go row, IN PLACE on line 35 (no line added)

Line 35 is the Go row (cell 1 tokens | cell 2 summary | cell 3 sources). Three substitutions on
the existing line; every other character stays as it is at HEAD.

S1 (cell 1, token):
- old: `` `2026-10-20-r16-go-selection-preview` | full compare ``
- new: `` `2026-10-20-r16-go-selection-preview`, `2026-10-20-r17-go-carrier-diagnostics` | full compare ``

S2 (cell 2, clause appended before the cell 2/3 separator):
- old: `` source-model only | historical r4-10 commands ``
- new: `` source-model only; r17: <R17-VERDICT> | historical r4-10 commands ``
- `<R17-VERDICT>` = that sentence copied verbatim from the landed entry's verdict line.
  Do NOT write it before the entry exists. It must state observed results only.

S3 (cell 3, receipt):
- old: `` in `.ufo/waves/round-16/verification.json` | ``
- new: `` in `.ufo/waves/round-16/verification.json`; r17: <R17-RECEIPT> | ``
- `<R17-RECEIPT>` = the committed path of the retained run receipt (`W/runs/*/receipt.json`,
  committed in the landing commit). Not the untracked `.ufo/waves/round-17/` path.

Why this placement (see DraftReadmeRow.md for the simulation):
- A new coverage-map row inserted after line 35 shifts pinned lines 138, 175 and 180 (3 pins fail in simulation: readme175 citing line, sc69, sc72).
- A Knowledge-table row inserted anywhere above line 180 shifts pins 138/175/180. r14–r16 Go entries have no Knowledge-table row (precedent); do not add one for r17.

## Edit 2 — Frontier: one appended bullet after line 181 (`## Frontier` ends at 181)

Insert as new line 182 (before the blank line that precedes `## Known gaps`). Lines 170-181 are
unchanged, so `held, not frontier` stays at :180 and the :175 bullet is untouched.

```
- Go analyzer bootstrap on real carriers — r14–r16 hold source-backed and source-model analysis (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md`) with no retained Ghidra analyzer log for a Go carrier; retained-log capture on a pinned out-of-range carrier and in-range carriers stays open until the r17 entry lands. On that landing this bullet is rewritten to the residual, or removed if none remains.
```

Gate: this bullet is the only text change in the Frontier section. Do NOT edit lines 170-181
(`:175` and `:180` are pinned; the lesson `corpus/lessons/round-12.md:20` records the same failure).

## Apply and verify (L1, at landing)

1. Apply Edit 1 (S1-S3, with placeholders filled from the landed entry) and Edit 2 in one README commit.
2. `python3 -I .ufo/gates/citation-drift/citation-drift-probe.py --root <repo> --rev <new HEAD>`
   expect `findings=0 exit=0` (pointer table digest unchanged, no pins moved).
3. `measure.py` README-token check: token `2026-10-20-r17-go-carrier-diagnostics` must match the landed filename.
4. Confirm `corpus/README.md:22`, `:138`, `:175`, `:180` unchanged by `sed -n` at new HEAD.

No stubs: S2/S3 placeholders are the only open fields and are filled only from the landed
entry and receipt. If the r17 entry does not land, do NOT apply Edit 1 or Edit 2 in any form.
