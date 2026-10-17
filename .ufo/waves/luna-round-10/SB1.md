# SB1 — SHONEN box 1, independent fresh read (Box 1)

## CLAIM
Box 1's `[~]` is correct at HEAD: the claimed SKILL.md contents exist and the queue-drain citations resolve, but the box cannot close — no named non-author verifier exists.

## METHOD
Read at HEAD `c343939`: `SHONEN.md:5-6`, all of `SKILL.md`, `SCORECARD.md:18-31,86-124,543-575,606-625`, `LOG.md:445-456`, fleet `PROTOCOL.md:61-73`; `git diff 6e83a20 c343939`. Re-ran command A (`SCORECARD.md:92-123`) over Git objects at `6e83a20` and `c343939`; spot-checked four citation ranges via `git show`. Read-only; independent of lane A's S1.

## FINDINGS
- Command A at both revisions: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "6e83a20", "rule_blocks": 9}` (identical with `"revision": "c343939"`).
- Fresh read: decision table `SKILL.md:42-66` (25 rows), error patterns `:68-79` (8), checklists `:197-205`, queue-drain craft `:81-195` = 9 rule blocks.
- Spot checks resolve (all `corpus/knowledge/`): `2026-10-13-r5-02-call-targets-jq.md:144-146` (+0x100000 law); `2026-10-14-r12-01-queue-b-ready.md:11` (byte-exact id); `2026-10-14-r10-01-queue-ops.md:166-173` ("Recorded URLs are never fetched"); `2026-10-14-r12-02-queue-b-ledger.md:131-133` (mkdtemp per-run id).
- Linkage gap: `PROTOCOL.md:69-70` wants the table, error list and checklist "each citing a resolvable source"; none of the three does (`SKILL.md:204` "typora lesson" is prose, not a pointer). Citations concentrate in queue-drain; asserted range `SKILL.md:77-191` omits `:42-66` and `:197-205`.
- No verifier: `SHONEN.md:6` disclaims; `LOG.md:445-450,456`; `SCORECARD.md:49`; `PROTOCOL.md:63-68` needs a named non-author `<id>`; nothing in `evidence/` or `c343939` supplies one.
- Brief vs repo: real HEAD is `c343939` (additive-only: +12 SCORECARD stub lines, +16 LOG; pure additions), not `6e83a20`; box-1 inputs untouched.

## THREATS
Command A is range resolution, not semantics (the row itself says so); my four spot checks are samples. The no-verifier finding is scoped to this checkout's artifacts. Even read loosely, the linkage bar leaves `[x]` unreachable without a non-author verifier. Peripheral: coverage row `SCORECARD.md:23` reads 78/78 (measured `3395b6d`) while rounds 8-9 measured 79/79 (`:543-544,573`).

## VERDICT
FINDING: keep Box 1 `[~]` — content and 9/9 queue-drain citations independently verified; no named non-author verifier; the table/error/checklist components cite no resolvable source.
