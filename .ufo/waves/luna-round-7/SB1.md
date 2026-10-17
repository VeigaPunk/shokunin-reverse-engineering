# SB1 — luna-round-7 LANE B | scope sentinel, git status LAST

## CLAIM
Round-7 writes are confined to `.ufo/waves/luna-round-7/`; the tracked tree at HEAD 411175e has zero modifications, and `git status` — run last (20:10:52) — shows untracked content only under `.ufo/`. Verdict: CLEAN.

## METHOD
Read-only, repo root, no probes/network. Window = first wave file (`E1V.md` 19:56:45) to snapshot. Commands: `git rev-parse HEAD`; `git status --porcelain=v1 [-uall]`; `git hash-object` vs `git rev-parse HEAD:<path>`; `find . -path ./.git -prune -o -type f -newermt '2026-10-16 19:56:00' -print` (round-7 dir excluded); `find .ufo/waves/luna-round-7 -type f`; `git status --porcelain=v1 -- corpus/`. Git-status block executed last, after all other evidence.

## FINDINGS
- Confinement: the post-19:56 scan outside the wave dir returned zero files. Wave dir: 65 files — 64 seat reports + `receipts/census-pre.txt`; no other non-`.md`, no underscore-named file.
- Pre-round tail (19:50–19:53): `LOG.md` and `SCORECARD.md` (both 19:52:35) and `.ufo/reports/luna-round-6/kaidoku.md` (19:53:10) have fresh mtimes, but `git hash-object` equals `git rev-parse HEAD:<path>` for each — byte-identical, no drift; `.ufo/waves/luna-round-6/BC6.md` (19:50:23) is the untracked round-6 census. All predate round-7 start ⇒ round-6 tail, not escapes.
- Corpus untouched both ways: `git status --porcelain=v1 -- corpus/` empty; 72 tracked `corpus/knowledge/*.md` (+`.gitkeep`), zero `l7-*` on disk — integration still pending, as expected.
- GIT STATUS LAST (2026-10-16T20:10:52-03:00): HEAD `411175e337c0725ae9bee3fd478ae9bf05bedf3f`; `## main...origin/main [ahead 17]`; non-untracked porcelain lines = 0; `--untracked-files=no` empty; `-uall` prefixes: `.ufo/waves` 607, `.ufo/interactive-sessions` 4.
- Supplementary: no round-7-labelled `/tmp` entry; `cc3-luna6`, `kaidoku-luna-round-6[B]-npm-cache` are round-6 residue (round-6 SB1), untouched here.

## THREATS
- Snapshot, not close: `TB1.md` landed 20:10:50 between my two counts (606→607); re-sweep warranted at wave close.
- mtime window assumes clock sanity; same-second pre-round writes not excluded, not observed.
- Scope audited = worktree + `/tmp` names; homedir configs and other repos not audited (outside this seat).

## VERDICT
CLEAN: round-7 writes confined to the wave dir; tracked tree and corpus byte-clean at HEAD; git status last shows only expected untracked `.ufo/` content.
