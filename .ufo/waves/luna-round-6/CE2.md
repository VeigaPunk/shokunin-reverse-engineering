## CLAIM
Command A at HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f` produced and froze its source-derived control output.

## METHOD
Confirmed `git rev-parse HEAD` → `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f`. Ran the unchanged Python recipe in `SCORECARD.md:92-123` with `REV` set to that full hash; it reads immutable Git objects. Exit code 0; no stderr output. Initial `git status --short` showed only untracked `.ufo/interactive-sessions/` and `.ufo/waves/`.

## FINDINGS
Held stdout:
```json
{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "f0e8cdecb216d71cf7df974675c0f6b16ba4f82f", "rule_blocks": 9}
```
The measured controls are 72/72 files mapped, empty missing/dangling sets, 9/9 citation-resolved rules, and coverage/depth scores of 10.0.

## THREATS
Command A checks source-derived map and citation-range controls; it does not establish semantic correctness or live REA behavior. The initial untracked `.ufo` paths predated this report.

## VERDICT
CLEAN
