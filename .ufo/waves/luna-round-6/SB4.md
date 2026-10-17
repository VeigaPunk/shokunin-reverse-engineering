# SB4 — sentinel: git status (lane B, deepseek-v4.1-flash)

## CLAIM
After lane-A delivery and in-flight lane-B writes, `git status` should show: HEAD pinned at f0e8cde, zero modifications to tracked files, and no new untracked content outside `.ufo/waves/luna-round-6/`.

## METHOD
Read-only, repo root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, 2026-10-16T22:01:27Z:
- `git rev-parse HEAD`; `git log -1 --format='%H %cI %s'`
- `git status --porcelain=v1 --untracked-files=all > /tmp/sb4-status.txt`
- tracked-change detectors: `git diff --stat`, `git diff --cached --stat`, `git status --porcelain=v1 | grep -v '^??' | wc -l`
- untracked entries grouped by 3-level prefix
- wave-write window detector (18:16:42 = earliest round-6 artifact mtime, `.ufo/waves/luna-round-6/EX1.md`):
  `find . -path ./.git -prune -o -type f -newermt "2026-10-16 18:16:42" -print | grep -v '^\./\.ufo/waves/luna-round-6/'`
- Baseline read for protocol only (not expected output): `.ufo/waves/luna-round-6/receipts/census-pre.txt:3-4` — at round start: HEAD f0e8cde, no tracked changes, untracked = `.ufo/interactive-sessions/` + `.ufo/waves/`.

## FINDINGS
- HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f` = pinned f0e8cde; last commit 2026-10-16T17:03:04-03:00 ("luna-round-5: records…"). No commit during this wave.
- Tracked changes: 0 — both `diff --stat` outputs empty, 0 non-`??` porcelain lines. No config drift.
- Untracked at snapshot: 492 entries; listing sha256 `3555566e4b290075b25ac44151a147d85461a5e25d69f0aece5c4852fda25e37` (moving target — seats writing concurrently). Breakdown: round-1 64, round-2 91, round-3 64, round-4 65, round-5 130, round-6 74, interactive-sessions 4.
- Out-of-scope writes during the wave: 0 — no file outside `.ufo/waves/luna-round-6/` has mtime after 18:16:42. Newest non-round-6 mtimes: round-5 wave 16:57:21, interactive-sessions 2026-10-15 02:16–02:43.
- Literal reading of "only luna-round-6 untracked" is false: rounds 1–5 and interactive-sessions are untracked too. These are pre-round residue documented at round start (`census-pre.txt:4`) and untouched during the wave; interpreting the expectation as "no new out-of-dir untracked content from this wave", it holds exactly.

## THREATS
- Counts/hashes are a one-moment snapshot; concurrent lane-B seats add files (e.g. `receipts-B/leg-1.md` at 19:00, `SB2.md` at 19:00:36).
- mtime is not authorship: a wave write preserving mtime would be invisible to this check; no such mechanism observed.
- Scope is working-tree git state only; receipt content integrity is other seats' remit. Command A/token set not re-verified here.

## VERDICT
CLEAN: HEAD pinned, zero tracked-file changes, zero out-of-dir writes during the wave; only caveat is pre-existing untracked rounds 1–5 + interactive-sessions, documented at round start.
