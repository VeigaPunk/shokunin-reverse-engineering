# SB4 — sentinel: format 2 (lane B, deepseek-v4.1-flash)

## CLAIM
Report-format sentinel (round-7 SB4 rerun), read-only 21:58–22:00 at HEAD `a280e07`: the frozen lane-A frame (66 reports) is format-clean — 16/16 sampled and 66/66 frame-wide pass the exact five-section sequence, ≤400-word cap, `^(CLEAN|FINDING)` verdict line, and single-line verdict sections; 16/16 sampled carry `path:line` evidence. No format defect found.

## METHOD
Frame = `ls -1 *.md | LC_ALL=C sort` at 21:58:13 in `.ufo/waves/luna-round-9/`, 66 files, no lane-B file present; list sha256 `3927e839df5d732e63e91c04d440ce4e5dcc2fde9c59c418e0856ae93047182b` (`/tmp/sb4r9-frame-2158-first66.txt`; `LC_ALL=C sort -c` passed; all 66 re-verified present at 22:00). Sample = ranks 4,8,…,64 (round-7 SB4 every-4th rule, 16 files): A4 B4 C4 D4 F2 G3 H2 P0 Q2 R2 R6 S3 X1 X5 Y4 Z4. Per file, read-only python: `## ` heading list == CLAIM/METHOD/FINDINGS/THREATS/VERDICT; whitespace word count; last non-blank line `^(CLEAN|FINDING)`; verdict-section non-blank line count; regex `\.md:\d+`; fenced-block presence. Corroboration: `git rev-parse HEAD` → `a280e07133f52f719b0805fc73c0b997e77b5062`; `git status --porcelain=v1 -uno` and `git diff HEAD` empty (PROVINCE untouched). Sole repo write: this receipt (scratch frame lists in /tmp).

## FINDINGS
- Sample 16/16 clean: exact sequence; wc ≤400 (max 307, `H2.md`); verdict single-line; each has ≥1 `path:line` (min `G3.md` 1, max `F2.md`/`X1.md` 11); `G3.md`/`Q2.md` also carry fenced command blocks.
- Frame 66/66 clean on sequence+wc+verdict+single-line (max wc 375, `F3.md`; 45 FINDING / 21 CLEAN; no lane-A title lines).
- Citation-form outliers (outside sample, allowed alternative): `S2.md`, `S4.md`, `T2.md`, `X3.md` have zero `.md:line` refs but present exact command+output — `S4.md:7-20` and `X3.md:10-16` fenced blocks; `S2.md:6-9` and `T2.md:5-9` inline with exact outputs (exit codes, hashes).
- Moving frame: directory grew 66→86 during the run (86 at 22:00:17); 20 lane-B arrivals (`CB1.md`…`YB2.md`), none lane-A-style.

## THREATS
Structural checks only, not semantics; citations counted, not resolved; lane-A stragglers after freeze unobserved (none by 22:00); word cap = whitespace split incl. headings; later lane-B sentinel reports outside frame. An alternative even-spacing sample (`S4.md:5` rule) would select different ranks.

## VERDICT
CLEAN — 16/16 sample and 66/66 lane-A frame are format-conformant; only lane-B growth occurred, outside the frame.
