## CLAIM
Command-A guard 2: at HEAD `a280e07` the recipe reproduces the required invariant 79/79 knowledge files mapped, 9/9 citation-resolved rule blocks, coverage/depth 10.0/10.0, with the tracked tree clean, zero deletions, and `PROVINCE.md` byte-identical. One lane-A record defect found; hold maintained (no tracked writes).

## METHOD
Ran `SCORECARD.md:92-123` verbatim with `REV=a280e07133f52f719b0805fc73c0b997e77b5062` from the lane repo. Guards: `git status --porcelain=v1 --untracked-files=no`; `git diff --quiet HEAD --`; `git diff --name-status --diff-filter=D HEAD --`; `git rev-parse HEAD:PROVINCE.md` vs `git hash-object PROVINCE.md`. Independently reproduced lane A's README token-set guard (same regex/section split; G3.md:24) and recomputed its SHA-256 under two serializations. No probes, no network, no `/tmp`; only write is this file.

## FINDINGS
- Command A exact output: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}` — invariant met.
- Guards all pass: status empty; `diff --quiet` exit 0; no deleted paths listed; both PROVINCE hashes `8a1cec88b50f0e9aa928b0c042354a017217ad47`.
- README coverage-map token set: 79 occurrences, 79 unique, 0 repeats — consistent with G3.md:24.
- **Record defect (G3.md:24):** the recorded sorted-token-lines SHA-256 `bd70aa5f639b9d2240caa057658b702df2083344bd07bfb4e35fceebb79750c` is **63 hex chars — invalid SHA-256 length**. Raw-byte inspection shows one contiguous backticked token, no line wrap. My recomputation: `sha256('\n'.join(sorted(unique tokens)) + '\n')` = `...750c4` (64 chars); G3's string equals its first 63 chars. Without trailing newline: `bc971a10a50fa3128b485c13a412696bfd65966679cb2913af80bef534c84860`.

## THREATS
Point-in-time pre-integration snapshot: no source append has landed, so post-landing append-only and non-target byte-identity remain unverified. Command A is an index/citation-range proxy (`SCORECARD.md:126-129`), not semantic truth. The G3 defect is established as a one-character truncation by prefix match; origin beyond that is not determined. A verbatim comparison against G3's string will always mismatch.

## VERDICT
FINDING: guard invariant holds at `a280e07` (79/79, 9/9, 10.0/10.0; tracked tree clean; PROVINCE identical), but G3.md:24's token-set SHA-256 is 63 hex chars — one char short of the recomputed 64-char value — so it must not be used as a verbatim baseline target.
