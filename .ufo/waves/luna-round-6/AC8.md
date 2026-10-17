## CLAIM
Command A at frozen HEAD `f0e8cdecb216d71cf7df974675c0f6b16ba4f82f` passes; the coverage-map token set contains 72 entries and equals the tracked knowledge-file stem set. Baseline captured for post-integration comparison.

## METHOD
Ran `SCORECARD.md:92-123` from the repository root with `REV=$(git rev-parse HEAD)`; the recipe reads Git objects. Held its JSON stdout and computed its SHA-256. Independently extracted the sorted, unique coverage-map tokens and `corpus/knowledge/*.md` stems from the same HEAD objects; checked count, exact-set equality, and the newline-delimited token digest. No live probes or tracked-file writes.

For the post-integration check, pin the final integration commit as `REV`, rerun the same recipe against that Git object, then repeat the token extraction/equality check at that `REV`. Compare Command A fields other than `revision` with this baseline, and compare the exact sorted token set (or its digest) to the pre-integration set. Do not use the raw JSON stdout hash across revisions because the JSON embeds `revision`.

## FINDINGS
Command A exit 0; stdout: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "revision": "f0e8cdecb216d71cf7df974675c0f6b16ba4f82f", "rule_blocks": 9}`. Stdout SHA-256: `258dc8695e0fa3809a9aceb289077b0e0c66a5c1b7d020cfb32b4db7d5567b45`. Token count 72; exact-set equality true; sorted token-set SHA-256 `c538284bd40fec6c039b6c2f18e7202f6390e0ca1ce92ea8a0c50e20a58651a0`.

## THREATS
This is a Git-object scope/count check, not validation of map descriptions or semantic correctness. It does not establish post-integration state until run at the final integration commit.

## VERDICT
CLEAN — command A and the 72-token exact-set guard reproduce at frozen HEAD; post-integration comparison procedure is specified above.
