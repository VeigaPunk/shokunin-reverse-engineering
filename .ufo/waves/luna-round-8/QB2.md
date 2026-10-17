## CLAIM
RB6's planned consolidated-entry filename and map token — `2026-10-16-l8-01-6p4-symmetry-battery` (RB6.md:4,16-17; corroborated QB1.md:2, RB8.md:4) — are hyphenated and regex-passing; landing them (79 files) yields knowledge_files=79, mapped=79, missing/dangling empty, 9/9 rule citations, coverage/depth 10.0. (RB5 itself never landed — RB6.md:21.)

## METHOD
Read-only in-repo; scratch Git store `/tmp/qb2-sim` only; no REA/MCP probes; no tracked file touched. Command A extracted verbatim from `SCORECARD.md:92-124` (1530 B, sha256 `6cc5081894f7f4aee2ff9c894b12d5cec5c38883a9341c0d9b9ed62f15cb4804`). Real HEAD `6e2ee8f` baseline: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 78, "mapped": 78, "missing": [], "revision": "6e2ee8fadc4ab328ce7c8d4d82cceb9b326b94c4", "rule_blocks": 9}` = census-pre.txt:90 field-for-field. Scratch base `4bb7b82` (78 copied `.md` + README + SKILL); added stand-in entry file plus RB6.md:16-17's two rows verbatim (map row before `## Knowledge` = after `README.md:67`; Knowledge row before `## Lessons` = after `:151`); commit `236baa5`; re-ran command A and a fullmatch/occurrence/set checker.

## FINDINGS
- Command A at `236baa5`: `knowledge_files=79, mapped=79, missing=[], dangling=[], citation_resolved_rules=9, rule_blocks=9, coverage_score=10.0, depth_score=10.0` — exactly the expected outcome.
- Checker: stem fullmatch `[a-z0-9-]+` True; token fullmatch `2026-10-\d{2}-[a-z0-9-]+` True; no `_`, no `.`; citation regex `corpus/knowledge/([a-z0-9-]+\.md)` matches; map-token occurrences=1; 79 stems == 79 tokens; no dup/prefix collisions.
- Controls: dotted `2026-10-16-luna-r8-6.4-symmetry` (CA5.md:9's shape) truncates to `2026-10-16-luna-r8-6`; underscore variant truncates to `2026-10-16-l8-01-6p4` — either would break mapped=79.
- Prior 78 `.md` blobs byte-identical to `6e2ee8f`.

## THREATS
Checked plan is RB6's slug, not RB5 prose (RB5 absent at write time). Scratch body is a declared stand-in (QB1.md:2 notes it); command A reads only filenames, map tokens, SKILL citations — counts are body-invariant, QUALITY conformance of the real text unmeasured. Simulation ≠ post-integration measurement. If CA5.md:9's dotted slug lands instead, expect mapped=78, coverage 9.87, truncated dangling token.

## VERDICT
CLEAN — planned filename+token hyphenated and regex-passing; unmodified command A at sim `236baa5` gives 79/79, 9/9, 10.0/10.0; dotted/underscore controls fail as predicted.
