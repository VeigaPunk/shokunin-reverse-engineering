# ZB4 — wave count audit

## CLAIM
Verify the frozen wave claim "Lane A 64 + lane B 64 = 128" against on-disk seat files for luna-round-8.

## METHOD
Read-only; no probes. Timestamped snapshots of `.ufo/waves/luna-round-8/` (`ls -1 *.md | wc -l`, `find -maxdepth 1 -type f`) at 21:11, 21:18:20, 21:20:10, 21:21:15, 21:24:30, 21:25:04, 21:25:18, 21:26:04 ART; all files are `.md` at maxdepth 1. Lane split by seat-ID convention (second character `B` ⇒ lane B), validated against self-IDs: `TB1.md:1` "command-A guard 2 (lane B)"; round-6 `.ufo/waves/luna-round-6/receipts-B/leg-1.md:3` "Seat: BB1 (lane B, deepseek-v4.1-flash)"; independent lane-B split count `ZB2.md:4` "lane A (52 reports)". Receipts dir counted separately; repo mtime sweep `find . -newermt '2026-10-16 20:45' | grep -v luna-round-8` for off-directory output.

## FINDINGS
- Progression (lane A / lane B / total): 52/0/52 (~21:11) → 52/3/55 (21:18:20) → 52/11/63 (21:20:10) → 52/12/64 (21:21:15) → 52/35/87 (21:25:18) → 52/39/91 (21:26:04). Lane B still landing (~5–7 files/min).
- Lane A: 52 seat files at every snapshot; membership unchanged ≥15 min (sorted-name digest `56bbef55…`); never 64. `ZB2.md:4` independently counts the same 52.
- Lane B at 21:26:04: 39 files (families CB, DB, FB, HB, KB, PB, QB, RB, SB, TB, VB, ZB); roster mid-flight.
- Total 91/128 — 128 unreached; total coincided with 64 (52+12) at 21:21:15.
- Receipts dir: 17 files, incl. `receipts/census-laneB-pre.txt` (landed 21:22–21:25), whose own census records the moving count (WAVE_REPORT_COUNT 74→76→81; `:9,:288,:295`).
- No lane-A artifact outside the wave dir (sweep found only 20:50 round-7 landing files); no commit past `6e2ee8f`.

## THREATS
Point-in-time; lane B still filing, so its count is a lower bound — lane A's 52 was stable across the whole 15-min window. No roster/dispatch manifest exists on disk (searched repo, `.ufo`, /tmp), so lane membership rests on the name convention plus self-IDs. The claimed 64 lane-A reports reproduce as no on-disk set found (52 seat files; 128 unreached); if "64" counts seat completions rather than files, disk cannot verify it.

## VERDICT
FINDING: disk does not reproduce 64+64=128 — lane A = 52 files (static ≥15 min, 12 short of 64), lane B = 39 and climbing, total 91/128 at 21:26:04 ART.
