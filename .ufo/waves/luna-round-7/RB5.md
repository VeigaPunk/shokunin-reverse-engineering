## CLAIM
Independent simulation: with the six 6.5.0 entries landed under hyphenated stems plus their coverage-map/Knowledge rows, canonical command A (`SCORECARD.md:92-123`, unmodified) prints `knowledge_files=78, mapped=78, missing=[], dangling=[], 9/9 rules, coverage 10.0, depth 10.0`; each stem regex-matches the map token `[a-z0-9-]+` whole (no truncation); the 72 prior entries stay byte-identical.

## METHOD
Read-only; no probes/network. Pre-state canonical command A at real HEAD `411175e`: 72/72, 9/9, 10.0/10.0. Scratch `git archive HEAD | tar -x -C /tmp/rb5-sim`; wrote six stand-in bodies (condensed from E/Z/G drafts, with `source:`/`verified-at:`/`recheck:` headers per ruling d) named `2026-10-16-l7-01-inspect-go-binary.md`, `-l7-02-inspect-rust-binary.md`, `-l7-03-inspect-electron-fuses.md`, `-l7-04-inspect-sqlite-database.md`, `-l7-05-search-bytes.md`, `-l7-06-inspect-with-objdump.md`; appended six M1/M2-style map rows + six Knowledge rows (hyphenated tokens); commit `85772d7`; reran command A at REV=`85772d7`; separate checker did `re.fullmatch`/occurrence/truncation checks per stem; control commit `4e07c00` (underscore stems); prior blobs compared via `ls-tree` hashes vs real HEAD.

## FINDINGS
Post-state command A output (`/tmp/rb5-sim`, REV `85772d76efb02deeb250a7d62d0d5c48f51f7570`):
`{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 78, "mapped": 78, "missing": [], "rule_blocks": 9}`
Checker: all six stems `fullmatch=True`, map occurrences=1, truncated variants=[]; 78 unique tokens; no strict-prefix tokens. Prior tree: 73/73 paths (72 `.md` + `.gitkeep`) blob-identical to `411175e`.
Control (`4e07c00`, underscore stems): mapped=72, coverage 9.23, missing=6 underscore stems, dangling=[`2026-10-16-l7-01`…`-l7-06`] (truncation at `_`); widened `[a-z0-9_-]+` maps 78 — confirms ruling (a) and shows the hyphenated route needs no scorer change.

## THREATS
Simulation, not post-integration measurement; landing must use exactly these six hyphenated stems/tokens. Scratch bodies are stand-ins: command A reads only filenames, map tokens, and SKILL.md citations, so counts are body-invariant — but QUALITY.md conformance of real texts and real-world 72-blob identity remain integration checks. Scratch is /tmp-only, disposable.

## VERDICT
CLEAN — unmodified command A yields 78/78, 9/9, 10.0/10.0 with hyphenated names; underscore control fails as predicted.
