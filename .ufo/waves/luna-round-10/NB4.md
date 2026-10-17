# NB4 — sentinel: format 2 | Sample 16 (lane B, deepseek-v4.1-flash)

## CLAIM
Report-format sentinel (round-7/9 SB4 lineage, `.ufo/waves/luna-round-9/SB4.md:7`): the round-10 lane-A frame (57 reports, frozen 22:45–22:46) is format-clean — 57/57 exact five-section sequence, ≤400-word cap (max 370, `X2.md`), one-line verdicts first-token only (8 CLEAN / 49 FINDING), no title lines; the 16-file even-spaced sample passes all checks, and every zero-`.md:line` file uses a resolving allowed alternative. No format defect found.

## METHOD
Frame = lane-A stems in `.ufo/waves/luna-round-10/` (exclude `^[A-Z]B[0-9]+\.md` lane-B arrivals), `LC_ALL=C sort`; list sha256 `faead5cb760c52989be8d0ea421bd1718a0eace79245d248dbc18200ae9a29fc`; per-file hashes in `/tmp/nb4-frame-sha256.txt` (cat sha256 `f91190f7…`), byte-stable at 22:46. Sample: ranks `round(i·57/16)`, i=1..16 → `4,7,11,14,18,21,25,29,32,36,39,43,46,50,53,57` → `A4 C1 D1 D4 F2 N2 P1 R3 R6 S2 S5 W3 W6 X1 X4 Y4`. Per-file read-only Python (fence-aware): five-heading sequence; whitespace word count; last non-blank `^(CLEAN|FINDING)`; VERDICT non-blank lines = 1; `\.md:\d+`, stem shorthand, fences. Zero-cite files re-read; `../MANIFEST.json:2751-2754,2791-2794` resolved at `/home/vgpnk/Projects/shokunin/MANIFEST.json` (2868 lines; `:2791` = C3's quoted string, `C3.md:12,22`). `git rev-parse HEAD` → `c343939`; `git status -uno`, `git diff HEAD` empty. Sole repo write: this file; /tmp scratch disclosed.

## FINDINGS
- Frame 57/57 clean on all four checks; sample 16/16 clean (wc 133–352; `.md:line` cites 2–35, except N2/Y4).
- Eight files carry no `*.md:line`: C2 C3 D6 N2 R8 X2 Y1 Y4. R8/X2 use wave-local stem shorthand (`R8.md:11` `C1:5–17`; `X2.md:11` `r6:25-29`); C3 cites `../MANIFEST.json:…`; C2 D6 N2 Y1 Y4 give exact command+output (`C2.md:5`; `D6.md:5`; `Y1.md:7`; sampled N2 `N2.md:7,9`; Y4 `Y4.md:8,10,12`). All satisfy "path:line or exact command+output".

## THREATS
Structural only; semantics and citation resolution beyond C3's anchor unchecked. Frame is lane-A-only: 18 lane-B reports existed at 22:46 and grow. HEAD moved `6e83a20`→`c343939` at 22:42:01 (47 commits; N2's 46 predates it, `N2.md:9`), so "HEAD" outputs are time-indexed. Word cap = whitespace split incl. headings. Rounds 1–9 format is prior-wave seats' remit, not re-audited.

## VERDICT
CLEAN
