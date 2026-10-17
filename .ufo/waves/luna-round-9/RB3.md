## CLAIM
Item-3 final gate: the `/tmp`-dependence audit is substantiated at current scope, and the hygiene proposal is conservative/operator-owned; residuals (historical `/tmp`-citing recipes, untested cold-cache) must be recorded as known limits, not closure claims.

## METHOD
Static review at HEAD `a280e07133f52f719b0805fc73c0b997e77b5062`; only write is this file. Re-checked primary sources behind Z3/Q3/C1/C2/C4/H: `PROVINCE.md:48`, `SKILL.md:39-40,242-251`, `.ufo/rounds/interactive-r1/verify-recovery.py:120-128`, `.ufo/rounds/interactive-r1/expected.json:70-79`, `PROTOCOL.md:341-343`, the four `recheck:` lines (`l7-01:5`, `l7-03:5`, `l7-05:5`, `l8-01:5`), `corpus/knowledge/2026-10-13-r3-renderer-asar.md:11,19`, `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:40-42`. Command A at HEAD → `{"mapped":79,"knowledge_files":79,"citation_resolved_rules":9,"rule_blocks":9,"coverage_score":10.0,"depth_score":10.0}`. `git status --porcelain` has no tracked modification; no round-9 artifact authorizes or reports a `/tmp` deletion.

## FINDINGS
1. No current lane instruction, registered gate, or landed `recheck:` requires pre-existing `/tmp` contents: `PROVINCE.md:48` session self-cleans, `SKILL.md:39-40` shared-ephemeral plus never clean another session, gate fixture under repo `HERE` (`verify-recovery.py:123`), snapshots repo-relative (`expected.json:70-79`), tmpfs refused as evidence (`PROTOCOL.md:341-343`). The four rechecks need only transient `/tmp` cwd; L7-01's npm-cache pre-existence is untested (no probe allowed).
2. Q3's residual stands but is archival: `r3-renderer-asar.md:11,19` and `r12-01:40-42` cite prior `/tmp` outputs not recreated by their own commands. Provenance debt in retained records — already non-conformant under `PROTOCOL.md:341-343` — not a current dependency. Label it; no corpus edit this round (item 3 lands audit + proposal).
3. Hygiene proposal (C2, gated CLEAN by C4) is conservative: two-snapshot attribution, tracked receipts, operator-manual exact-path deletion after close review; no lane cleanup, no glob, no janitor. r6 ~1.2 GB/43 entries and r7 59/~1.21 GiB are point-in-time floors.
4. Command A 79/79 + 9/9 and PROVINCE-untouched hold at my snapshot.

## THREATS
VB3 absent at 21:58 (no `.ufo/waves/luna-round-9/VB3.md`; round-5 DB3 precedent) → no third-seat review. No live `/tmp` inventory; current size/ownership unverified. Q3's recipes and L7-01 cold-cache were not replayed. Residuals stay open if SCORECARD omits them.

## VERDICT
FINDING: item 3 disposition = audit CLEAN at current scope plus two labeled known limits (historical `/tmp`-citing recipes; untested cold-cache), hygiene operator-owned per C2, no deletions authorized or performed, and no freshness-improvement claim from item 3 alone.
