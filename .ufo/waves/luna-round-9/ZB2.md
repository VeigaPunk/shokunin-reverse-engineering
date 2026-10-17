## CLAIM
On-disk round-9 report counts under the round-8 lane convention (seat-ID second character `B` ⇒ lane B): lane A = 66 (static), lane B = 38 (mid-landing, lower bound), total 104, at 22:01:55 -0300. Both counts reported for parent reconciliation; the convention is stated so the parent can re-split if its roster differs.

## METHOD
At HEAD `a280e07133f52f719b0805fc73c0b997e77b5062` (tracked tree clean: non-`??` status lines = 0; `git diff HEAD` empty; `PROVINCE.md` blob `8a1cec88…` = HEAD). Counted top-level `.ufo/waves/luna-round-9/*.md` via stdin Python (no files written), lane B = second name character `B` (precedent `.ufo/waves/luna-round-8/ZB4.md:5-8`; validated by round-9 IDs `HB2`, `ZB2` = this seat). Four timestamped snapshots with sorted-name SHA-256 digests. Read `X3.md`, round-8 `ZB4.md`/`ZB2.md`.

## FINDINGS
- Progression (time / total / lane A / lane B): 22:00:22 → 87/66/21; 22:01:12 → 101/66/35; 22:01:38 → 104/66/38; 22:01:55 → 104/66/38.
- Lane A static: 66 files, digest `1337a56a9a10d506`, families A:4 B:4 C:4 D:4 E:2 F:3 G:4 H:5 K:1 P:3 Q:4 R:7 S:4 T:2 X:5 Y:4 Z:6.
- Lane B digest moved twice (`31c72279…` → `f65af47a…` → `eb822cfa…`), then paused; 38 files across CB, DB, FB, GB, HB, KB, PB, QB, RB, SB, TB, VB, YB, ZB.
- `X3.md`'s "4 lane-A reports" reproduces only as the narrow glob `A*.md` = 4 (A1–A4); that is not the lane-A total (`X3.md:2,5-12`).
- Round-8 context: the wave claim "Lane A 64 + lane B 64 = 128" (`.ufo/waves/luna-round-8/ZB4.md:2`) was never reproduced on disk (52+39=91 at its cutoff); here lane A already exceeds 64. `receipts/` = 2 files (`census-pre.txt`, `census-laneB-pre.txt`).
- This report adds 1 lane-B file after the snapshots; post-write recount 22:02:17 (after it landed): total 113 / lane A 66 (digest unchanged) / lane B 47 (`e9ffd631…`) — lane B resumed (~9 files/22 s).

## THREATS
Point-in-time; lane B rose 21→38 in the preceding ~90 s, so 38 is a lower bound, not a final count. No on-disk dispatch roster exists, so membership rests on the convention plus seat IDs; a different parent roster (e.g. prefix sets) changes the split. Lane A exceeding 64 is measured, not adjudicated. Untracked concurrent writes only; no tracked file was touched.

## VERDICT
FINDING: lane A = 66 (static, digest `1337a56a…`); lane B = 38 and previously climbing at 22:01:55 -0300 (total 104); `X3.md`'s "4" is a narrow-glob artifact.
