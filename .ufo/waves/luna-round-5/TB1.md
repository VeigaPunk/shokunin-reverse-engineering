# TB1 — command-A guard (Lane B)

## CLAIM
Command A (SCORECARD.md:92-123) at HEAD=cfc84c2 yields the pre-integration baseline: 72/72 knowledge files mapped, 9/9 rule blocks citation-resolved, coverage/depth 10.0/10.0, no missing/dangling tokens. Output frozen here for post-integration diff.

## METHOD
- `git rev-parse HEAD` → `cfc84c226bb8755c15fcdc342e27de7654c6fcb8`; `git status --porcelain` → only untracked `.ufo/` paths (tracked tree clean).
- Ran recipe A verbatim (SCORECARD.md:92-123) with `REV=cfc84c2`, twice. Identical output; sha256 of the JSON line: `cc1d4ecc4f80514e0715251c42ce80529fb2d38f4a15200e36701f0175697e89`.
- Also ran recipe A with both `result.json` source commits for disambiguation.

## FINDINGS
- REV=cfc84c2 (verbatim): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "cfc84c226bb8755c15fcdc342e27de7654c6fcb8", "rule_blocks": 9}`
- Determinism: two independent runs byte-identical.
- Disambiguation for the parent: at the two frozen `evidence/round-1-2026-10-15/result.json` revisions (baseline `6645585…`, measured `c265db9…`) command A returns mapped=70/72 with missing `["2026-10-14-r14-01-queue-b-residual", "2026-10-14-r14-02-final-sweep"]`, rules 9/9. The "72/72, 9/9" invariant therefore holds at HEAD, not at those older revisions. Post-integration comparison must re-run with REV=new HEAD, not with result.json revisions.
- Scope caveat: `mapped` is computed from README.md's `## Coverage map` section only (HEAD README.md:11; Frontier is a separate section at :153). The planned README frontier edit must not remove coverage-map tokens, or `mapped` will move.

## THREATS
- Recipe A reads Git objects (`git show REV:path`), not the worktree; comparison is only meaningful after integrated edits are committed.
- If integration rewrites/rebases history the revision string changes — compare the JSON payload fields, not the `revision` value or raw line.
- No post-integration run exists yet in this wave; the actual pre/post diff remains open and is the parent's step.

## VERDICT
CLEAN — command A reproduced 72/72 and 9/9 at HEAD; baseline held for post-integration comparison.
