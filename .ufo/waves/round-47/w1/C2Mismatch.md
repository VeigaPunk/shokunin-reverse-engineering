# R47-C2 before-state: verification of the four mismatches, and six defects in the frozen clause

Seat `C2Mismatch`, wave 1, lane `kaidoku` round 47. Base `13a9e9e`; freeze `5017e1f`.
Full report and every receipt: `.ufo/waves/round-47/w1/C2Mismatch/` (`report.md`, `receipt.json`,
`derive/`, `probe*.{py,out,utc}`). Lane tree read-only; nothing written outside this directory pair;
scratch removed; no installs; no commits.

## The four before-mismatches are all real (no false mismatch)

Counter run (exit **1**, stdout sha256 `53d81a3d…4d7e36`, `2026-10-28T17:55:59Z`,
`atoms 50 / verified 46`, `failing ["mismatches 4 != 0", "corrections 0 < 2"]`).

| # | atom | recorded | truth by my own command | verdict |
|---|---|---|---|---|
| 1 | round-45 seats `Wave 1: 40 seats; wave 2: 32 seats` | 40 / 32 | **40 / 36** — `w2-dispatch.json` `counts.spawn 36`; `r45-w2-results.json` `seats 36`, 36 results; the `32` is `policy.waveMinLanes` from the same dispatch file | counter right; the record is **false**, against its own cited source |
| 2 | round-46 window `0425224..<tip> -- tools/round-46 plans/round-46-claims.md` "is empty at every measurement above" | empty | **unverifiable** (literal `<tip>`) **and false**: `git log 0425224..13a9e9e` over that pathspec prints `M tools/round-46/attest.py`, `M tools/round-46/gate.py` (commit `332f4884`, which the same section declares the measured freeze) | counter right, for a weaker reason than the truth |
| 3 | `coverage` row head `133/133` | 133/133 | **138/138** at `--rev` (138 knowledge files, 138 map tokens, `dangling []`, `missing []`); 133 was true at its own cited `e1c83313` | counter right at `--rev`; defect is staleness, and the card then carries two incompatible current values (row head vs the round-45/46 sections' `138/138`) |
| 4 | `depth` row head `20/20` | 20/20 | **23/23** at `--rev` (23 craft blocks, 23/23 citations resolve); 20 at `e1c83313` | same staleness class; counter right |

## Frozen-clause defects (attack findings — do not repair frozen bytes)

- **C2M-1 (HIGH) `CORR` omits `axes`.** `record.py:50` matches `(seats|window|path|rev)` only, so a
  documented `- corrects axes …: <resolved>/<total>` line is silently dropped: not counted, not
  exempted, never `corrections_bad`, although `corrects()` implements the branch. Live at the
  landing: four `- corrects` lines, **two parsed** (`probe6.out`, rev `f54b3b6d`, exit 0); a
  fabricated `- corrects axes depth: 99/99` also exits 0. The SCORECARD sentence that every
  `corrects` line is re-derived by the counter is false for the two `axes` lines.
- **C2M-2 (HIGH) deleting an axis row is a valid repair.** Remove the `| coverage |` row and the
  card is met (`probe2.out`, exit 0, `axes 1`): the `classes` clause only fails at zero atoms.
- **C2M-3 (HIGH) a `window` atom goes green on a pathspec nobody touched, or on a reversed window.**
  `0425224..13a9e9e -- tools/round-46x …` → exit 0; `13a9e9e..7bf33e31 -- tools/round-46 …` →
  exit 0 (`probe.out`). The battery carries neither class.
- **C2M-4 (MEDIUM) `path` corrections ignore their statement.** `corrects()` returns
  `files(key) is not None`; two inert or fabricated `- corrects path …` lines satisfy
  `corrections >= 2` with `exempted []` (`probe4.out` exit 0; `probe6.out` `fabricated-path-statement`
  exit 0). A fabricated `seats` total *is* caught.
- **C2M-5 (MEDIUM) `Wave 1/Wave 2` binds only two waves.** With a synthetic third dispatch the pair
  atom stays green and no atom names wave 3, while the sum shape counts it (`85` green, `76` red).
  Latent at this base: no round has three dispatches.
- **C2M-6 (MEDIUM) the before-state battery passes by erroring.** With no corrections section all
  three fixtures report `error: "no corrections section"` → `forgeries 3 / green 0` with zero
  mutations. The before cell's clause-6 numbers evidence nothing.

## What the landing must say (measured)

- **depth `24/24` at the landing revision**, and block 24 must be written `- **24. …`: as a
  `### 24.` heading the block is invisible (`(23,23)`), and as `**24. …` it folds into block 23 and
  breaks *its* resolution (`(22,23)`). A block whose citations do not all resolve reads `(23,24)`.
- **coverage stays `138/138`** (the freeze adds no `corpus/knowledge` file).
- **the axes rows must be edited in place**; the two `- corrects axes …` lines do nothing (C2M-1).
- the two parseable corrections currently landed are both true and I reproduced them:
  `2 waves, 76 seats total` (dispatch `[40,36]`) and
  `empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` (0 bytes).

At `f54b3b6d` the counter is met (exit 0, `mismatches []`); the only visible defect is C2M-1.
