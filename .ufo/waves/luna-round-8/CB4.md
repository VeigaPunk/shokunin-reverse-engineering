# CB4 — scope 2: tracked-file freeze check (git status)

## CLAIM
At check time the tracked tree of kaidoku-shokunin is frozen at HEAD 6e2ee8f: zero tracked-file modifications, staged changes, or deletions. Every new artifact present is an untracked addition under `.ufo/` (lane-A evidence), which the freeze contract allows.

## METHOD
Read-only git inspection from repo root, re-verified twice (21:13–21:17 ART):
- `git status --porcelain=v1` and `--untracked-files=no` / `=all`
- `git diff --quiet` (worktree vs index), `git diff --cached --quiet` (index vs HEAD), `git diff --quiet HEAD` (worktree vs HEAD)
- `git ls-files -v | grep -vc '^H '` (masking flags)
- `git stash list`; porcelain code histogram via awk
- newest tracked-file mtime (`stat -c %Y` over `git ls-files -z`) vs commit epoch

## FINDINGS
- `git rev-parse HEAD` → `6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4` (branch `main`) — matches frozen 6e2ee8f exactly. `git log -1`: `6e2ee8f... 2026-10-16 20:50:20 -0300 luna-round-7: records (LOG + SCORECARD + report; command A 78/78 at work commit 3395b6d)`.
- `git status --porcelain=v1 --untracked-files=no` → empty output, exit 0. No non-`??` lines in full porcelain (grep found none).
- `git diff --quiet` → exit 0; `git diff --cached --quiet` → exit 0; `git diff --quiet HEAD` → exit 0. 151 tracked files, none dirty.
- No staged, deleted, renamed, or copied entries: porcelain histogram = `135 ??` and nothing else. Validation not masked: `git ls-files -v` shows all 151 as clean `H` (0 assume-unchanged/skip-worktree bits). `git stash list` empty.
- All 135 untracked entries are under `.ufo/` (luna-round-1..8, interactive-sessions); with `-uall`, 0 untracked paths outside `.ufo/`. `.ufo` itself holds 49 tracked files, all unchanged.
- Mtime corroboration: newest tracked-file mtime = 1792194603 (20:50:03), 17 s before commit epoch 1792194620 — no tracked file rewritten after the round-7 commit.

## THREATS
- Point-in-time proof only: two git snapshots cannot exclude a modify-then-restore between them, and git status could never show that. The mtime skew makes it unlikely but mtimes are user-settable.
- A writer active after 21:17 would invalidate this; parent should re-run `git status --porcelain -uno` before integrating.
- The late lane-A receipts arrived as untracked files — consistent with the contract, but their presence means "all new files are evidence", not "tree untouched since round 7".
- Round-6 wave files also show as untracked; that predates this round and is out of scope-2's remit.

## VERDICT
CLEAN
