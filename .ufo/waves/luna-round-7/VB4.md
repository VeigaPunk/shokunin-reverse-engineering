# VB4 — receipt-at-HEAD audit (E4V/S1 "untracked" claim)

## CLAIM
Independent audit at HEAD `411175e`: do the leg-6 receipts resolve in the HEAD tree? E4V.md:13–22 claims they are "untracked / not yet durable at HEAD". Result: claim is false; both receipts are tracked, clean, and byte-identical to their HEAD blobs.

## METHOD
Read-only; no probes/network. Reproduced E4V's exact commands at HEAD from repo root and from `.ufo/waves/luna-round-6`; cross-checked `git ls-tree`/`git status`/`git ls-files`/`git hash-object`; compared bc91424 vs HEAD file sets; checked mtimes for the evidence timeline.

## FINDINGS
- From cwd `.ufo/waves/luna-round-6`, exact `git ls-tree HEAD -- receipts/leg-6.md receipts-B/leg-6.md` → exit 0:
  `100644 blob 372c8a8e…  receipts-B/leg-6.md`
  `100644 blob 8b47efa7…  receipts/leg-6.md`
  The `:/` top-relative form resolves from both cwds; the bare form from repo root matches nothing (no top-level `receipts/`) — cwd-relative semantics, not durability.
- `git hash-object` of the worktree receipts equals those blob ids; `git status --porcelain` over receipts/ + receipts-B/ → 0 lines; 26 files tracked at bc91424 and HEAD, sets IDENTICAL (diff empty).
- E4V.md:13–19's quoted evidence does not reproduce at HEAD: root-cwd rerun of its status command prints only `?? .ufo/waves/luna-round-6/SC4.md` (genuinely untracked wave-report); its ls-tree rerun lists both receipts. The wave-dir rerun prints a "could not open directory" warning and no `??` lines. Its three-line `??` block matches only the pre-bc91424 working state (receipt mtimes 18:27:56/19:03:27, SC4 18:17:35; bc91424 landed 19:52:00; E4V.md mtime 19:58:40 — drafted ~5 min after tracking).
- Seat-misread class: (1) empty pathspec output (exit 0) read as "not in tree" — subdirectory cwd + repo-root-relative paths silently no-match (`ls-files --error-unmatch` from the wave dir likewise exits 1 "did not match any file(s) known to git"); (2) pre-integration snapshot quoted as "current checkout". Guard: root cwd or `:/` pathspec; trust output plus exit code, not absence.

## THREATS
Cannot reconstruct E4V's exact shell state; its status block is stale-or-composite, provable only by non-reproduction. S1.md itself contains no untracked-receipts text (its sweep was deferred to its handoff); the written claim lives in E4V.md — F8.md:10 already contradicted it. My audit certifies only the HEAD tree, not future commits.

## VERDICT
FINDING: E4V's "untracked / not durable at HEAD" claim is false at 411175e — both leg-6 receipts resolve, tracked, clean, byte-identical; misread class = empty-pathspec-output + stale-snapshot-as-HEAD (cwd-sensitive pathspecs).
