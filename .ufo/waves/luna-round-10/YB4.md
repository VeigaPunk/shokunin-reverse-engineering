## CLAIM
The arc's frozen surfaces hold at the current HEAD: (a) PROVINCE.md byte-frozen since the round-5 pin (7125dd4); (b) every tracked file at HEAD is byte-identical to lane A's pin commit 6e83a20 except the labelled pure-append protocol-conformance addition.

## METHOD
Read-only Git-object checks: `git rev-parse HEAD` → `c343939236d95f6027a67db6034920d06c83ac25` (HEAD moved past the parent's/lane A's 6e83a20 at 22:42). `git show REV:PROVINCE.md | sha256sum` across revs; Python `bytes.startswith` prefix comparison of blobs; `git diff --numstat/--check`; worktree `git status --porcelain` and `sha256sum`. No network, no live probes, no writes outside this file.

## FINDINGS
- PROVINCE freeze: `git log --format='%h %s' 2abd30f5^..HEAD -- PROVINCE.md` lists only 75af886 (r2) and 7125dd4 (r5); `git log 7125dd4..HEAD -- PROVINCE.md` → empty (all-time last touch is also 7125dd4). SHA-256 identical, `fe7f3f61c6beb6d601bf6780194ad10f8641c402c2501067d6a93f29c3b37c1c`, at 7125dd4, a280e07, 40162fc, 6e83a20, c343939, and the worktree — confirming W9.md:22's `fe7f3f61…` and extending it to current HEAD.
- `git diff --numstat 6e83a20 c343939` → `16 0 LOG.md` / `12 0 SCORECARD.md`; `git diff --check` clean; therefore every other tracked file is byte-identical between lane A's pin and HEAD.
- Prefix identity 6e83a20→c343939: LOG.md `True` (+963 B), SCORECARD.md `True` (+468 B); PROVINCE.md, SKILL.md, SHONEN.md delta 0 (byte-identical).
- Round-9 errata raw_equal at HEAD vs 40162fc: `2026-10-13-r2-jq-shadow-verdict.md` 17,220 B (`d7699268…` worktree), `2026-10-13-r4-16-frontier-rescan.md` 64,625 B (`ec0f221a…` worktree).
- c343939 author=committer `kaidoku-shokunin <kaidoku@shokunin.local>`; worktree has no tracked or staged drift (236 untracked `.ufo` wave artifacts only).

## THREATS
Git-local only: verifies bytes, not the semantic accuracy of PROVINCE claims (S4/S5 box-4 boundary debt remains). Untracked wave artifacts are outside tracked byte-identity. Sibling checkouts untouched.

## VERDICT
CLEAN — PROVINCE byte-frozen at `fe7f3f61…` through HEAD c343939; tracked-file byte-identity holds, with the new HEAD differing only by pure-append LOG/SCORECARD protocol-conformance rows.
