# SB4 — sentinel: git status (lane B, deepseek-v4.1-flash)

## CLAIM
After lane-A delivery and in-flight lane-B writes, `git status` should show: HEAD pinned at `6e2ee8f`; zero tracked-file modifications; all untracked content inside `.ufo/`, with this round's writes adding no new untracked entry outside `.ufo/waves/luna-round-8/`.

## METHOD
Read-only, repo root, snapshot 2026-10-16T21:23:42-03:00. `git rev-parse HEAD`; `git log -1`; `git status --porcelain=v1` (count, sorted-listing sha256); `-uall`; `git diff [--cached]`; `git stash list`; per-dir tracked/untracked counts; wave-window stat-loop vs earliest round-8 mtime (`EX1.md` 20:52:40). Baseline `receipts/census-pre.txt:86-87`. Fence-byte re-hash of `leg-3.md`. Paths below relative to `.ufo/waves/luna-round-8/`.

## FINDINGS
- HEAD `6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4` = pinned; last commit 20:50:20 ("luna-round-7: records…"); no commit during the wave.
- Tracked changes 0: both diffs empty, 0 non-`??` porcelain lines, stash empty.
- Untracked: 135 entries, all `??`, sorted-listing sha256 `1786a8a62d89266056f6bba6d078bbefc83fd2e7ace6cd54788a6a586b2dbe95` (identical at 21:22:59 and 21:23:42), all under `.ufo/`. Expected-untracked list = 8 collapsed dirs (`.ufo/interactive-sessions/`; `luna-round-1..5,7,8`) + `luna-round-6` expanded to 127 entries (26 tracked files there force descent) = 135 ✓ (census-pre: 135 untracked / 0 dirty, `:86-87`). `-uall`: 771 files (64/91/64/65/130/127/130/96/4).
- Out-of-scope writes since wave start (20:52:40): 0 files outside `luna-round-8/` newer; newest outside file `.ufo/reports/luna-round-7/kaidoku.md` 20:50:03.
- Round-8 payload at snapshot: 80 reports + 16 receipts = 96 files; SB1–SB3 landed, lane B still writing.
- Receipts: census-pre's leg-3/leg-4 rows (`:97`; `d641e3d3`/1430 B, `8f04ac26`/1233 B) are stale; current `1be7e4f9`/1448 B and `aa4aa7a3`/1200 B match `MANIFEST.txt:3-4` ≡ `CA6.md:10`. leg-3 display defect not reproducible: fenced block+LF = 623 B = `5c682099…` = claim (`leg-3.md:6`) = /tmp raw. `leg-10.md` rewritten 21:14 (post-MANIFEST 21:02, post-census): current `6cd389e9` ≠ `MANIFEST.txt:10`/`CA6.md:10` `c89eea7a`; its internal stdout claims recompute.

## THREATS
One-moment snapshot of a moving target (lane-B files landing inside the collapsed dir keep the count at 135). mtime is not authorship. Receipt-binding drift reported, not adjudicated (parent-side).

## VERDICT
CLEAN: HEAD pinned, 0 tracked changes, 0 out-of-scope writes, untracked exactly matches the expected list; caveats: leg-10.md ≠ MANIFEST binding; census-pre leg-3/leg-4 rows stale; leg-3 display defect already repaired.
