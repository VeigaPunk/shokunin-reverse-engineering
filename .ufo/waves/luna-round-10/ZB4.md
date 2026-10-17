## CLAIM
Independently re-verify lane A's ancestry result (Y3) at the true current HEAD, plus the r1–r9 chain's structural integrity: linearity, authorship, refs, rewrite events.

## METHOD
`git log --format='%H %P' --reverse 6645585..HEAD` through an awk parent-link assert (each commit single-parent, parent = predecessor); `--count --merges`; `git for-each-ref`; identity scan; Y3's 19 IDs via `git merge-base --is-ancestor` against HEAD; `git fsck --unreachable --no-reflogs`; reflog scan (`amend|reset|rebase`); per-records-commit `--numstat` on LOG.md/SCORECARD.md plus sampled deleted lines; `git grep` for disclosure. Read-only; no probes.

## FINDINGS
- `6645585..c343939` = 25 commits, 0 merges, LINEAR_OK; all 25 author+committer `kaidoku-shokunin <kaidoku@shokunin.local>`; only refs `main=c343939`, `origin/main=6645585`; no tags/stash. The five 2026-10-15 `round-1:` commits (c265db9..a79945c), absent from Y3's range, are in-chain and lane-authored.
- Y3 holds: 19/19 cited IDs are ancestors of `c343939`. The brief's pin `6e83a20` is its direct parent; post-round-9 delta = exactly one commit, `c343939` (+16 LOG/+12 SCORECARD, 0 deletions, lane identity).
- Reflog: exactly 3 rewrite events, all `commit (amend)`, on r2/r4/r5 WORK commits: `24b0287→75af886` (PROVINCE.md 1/1), `35c81b5→6a71cd5` (corpus/README.md 7/7), `27886f4→7125dd4` (corpus/README.md 1/1). Each amend precedes its records commit (15:17:03<15:19:44; 16:18:30<16:20:53; 17:01:42<17:03:04). Originals exist, are not ancestors, and are the only unreachable commits under `--no-reflogs`. Disclosed: LOG.md:725,768; SCORECARD.md:307-308,390,435; reports r2:61, r4:22, r5:63.
- Records-commit numstat: LOG.md deletions 0 in all nine; SCORECARD.md deletions r1 −4, r2 −8, r3 −7, r4 −1, r7 −1; r5/r6/r8/r9 −0. `a4bd355` replaces the `| coverage |` row + 3 prose lines, so line-level "never rewritten" fails for SCORECARD in five records commits — r1 extends lane A's r2/r3/r4/r7 set.

## THREATS
Reflog/fsck are local metadata outside the published DAG; pre-records amends leave published-chain integrity intact but prove work-commit history was rewritten. Deletions are line counts, not semantic classes. Reachability ≠ content truth; r4's "eight wording tweaks" (LOG.md:725) vs 7 replaced lines unreconciled at sub-line granularity.

## VERDICT
FINDING: chain is linear, single-identity, 19/19 ancestry holds at `c343939` (one commit beyond the brief's pin); but three cited r2/r4/r5 work commits are `--amend` products (originals unreachable; disclosed pre-records), and SCORECARD deletions span five records commits, not four.
