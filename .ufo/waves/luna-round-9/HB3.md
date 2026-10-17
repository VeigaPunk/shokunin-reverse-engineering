## CLAIM
Simulated the round-9 landing in memory (no repo writes): after the drafted appends, command A still yields 79/79 knowledge files mapped, 9/9 citation-resolved rules, 10.0/10.0 coverage and depth.

## METHOD
Extracted the exact fenced recipe (`SCORECARD.md:94-122`) and executed it twice at `REV=a280e07133f52f719b0805fc73c0b997e77b5062`, wrapping `subprocess.check_output` only to intercept `git show`: run 1 unmodified (independent baseline reproduction); run 2 with the drafted landing texts appended in memory to `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` (A2 draft, `.ufo/waves/luna-round-9/A2.md:9-10`) and `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md` (D2 draft, `.ufo/waves/luna-round-9/D2.md:10`). Script ran from stdin; no file written. Baseline hashes match T2 (`.ufo/waves/luna-round-9/T2.md:8-9`). Post-run: `git status --porcelain --untracked-files=no` and `git diff --stat` empty; HEAD unchanged.

## FINDINGS
Both runs printed byte-identical JSON:
`{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "revision": "a280e07133f52f719b0805fc73c0b997e77b5062", "rule_blocks": 9}` → equal=True. Two mechanisms confirm this is not coincidence: (a) command A fetched 16 paths — `corpus/README.md`, `SKILL.md`, 14 cited knowledge files; `SCORECARD.md` and `corpus/QUALITY.md` were never fetched, so the census-limits home (X4's open ruling) cannot affect command A; (b) neither append target is cited by any of the 9 queue-drain rules, and appends only raise line counts (925→928, 242→244), which cannot break `start<=end<=count`.

## THREATS
Simulated appends are the A2/D2 drafts, not integrator-final wording. A landing that edits README's coverage-map section or SKILL's queue-drain section is outside this simulation. The guard remains an exact post-landing rerun at the landed revision (P0's invariant, `.ufo/waves/luna-round-9/P0.md:14`); no /tmp state was read or written.

## VERDICT
CLEAN — landing simulation holds command A at 79/79, 9/9, 10.0/10.0 (unmodified recipe, in-memory interception, zero tracked writes).
