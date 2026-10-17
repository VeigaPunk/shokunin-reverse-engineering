## CLAIM
Audit M1/M2 coverage-map rows and K3/K4 Knowledge-table rows for cell shape, hyphenated tokens, dates, and insertion points; test whether integration as drafted can produce Command A's claimed `mapped=78, missing=[], dangling=[]`.

## METHOD
Read `M1.md`, `M2.md`, `K3.md`, `K4.md`, `corpus/README.md:59-67,129-141`, `SCORECARD.md:92-123`, `P0.md:8`, `N1.md:5,16`, `receipts/census-pre.txt`. Ran Command A verbatim at HEAD `411175e337c0725ae9bee3fd478ae9bf05bedf3f` (output: 72/72, missing/dangling `[]`, 9/9 rules, coverage 10.0). Parsed every candidate row (cell counts) and re-ran Command A's stem/map logic (`SCORECARD.md:100-102,118`) in memory with the six rows inserted after the r14-02 line under three token policies. Spot-checked `receipts/leg-4.md:28-43` and `receipts-B/leg-4.md:37-71`. No tracked-file writes.

## FINDINGS
- Shapes/dates conform: M1:11-13 and M2:10-12 are 3-cell map rows; M2:15-17, K3:8-10, K4:10-12 are 4-cell Knowledge rows; no stray pipes; all date cells `2026-10-16`. Map anchor after r14-02 (`README.md:61`), before `## Knowledge` (`:63`), is stated by M1:2/M2:8; the Knowledge anchor after `README.md:139`, before `## Lessons` (`:141`), is pinned only by P0:8, not by M2/K3/K4.
- Blocker: M1:11-13, K3:8-10, K4:10-12 carry underscore stems; ruling (a) and N1:16 prescribe hyphenated IDs. Simulation "hyphenated files + drafts as-written": `{"mapped": 75, "missing": [3 stems 01-03], "dangling": ["2026-10-16-l7-01-inspect", "2026-10-16-l7-02-inspect", "2026-10-16-l7-03-inspect"], "coverage_score": 9.62}`. All-hyphenated variant: `{"mapped": 78, "missing": [], "dangling": [], "coverage_score": 10.0}` — the current matcher suffices; K4's regex-widening is moot under ruling (a). Only cell-1 stems need hyphenation; underscores in prose/verb references do not affect the matcher.
- Duplicates: M2:15-17 and K4:10-12 draft the same rows 04-06; integrate exactly one (hyphenated) set, else N1's one-row-each gate fails.
- Ruling (b) alignment: row-04 topic text (M2:10, M2:15, K4:10) still summarizes both carriers; the admitted entry is lane-B-only, so narrow it to the lane-B inventory result.
- Row texts make no Core/promotion claim; M1:12 labels the `rg` run RESULT. K3 row 02's claims match both spot-checked receipts.

## THREATS
The all-hyphenated variant is an in-memory projection, not a post-integration measurement; rerun Command A after landing. Citations were boundary-checked with one row content-spot-checked per lane, not fully adjudicated. This audit assumes ruling (a); stem choice is the parent's.

## VERDICT
FINDING: shapes, dates, anchors conform, but M1/K3/K4 underscore tokens must become hyphenated (as-written: mapped=75, missing=3, dangling=3) and M2/K4 rows 04-06 must be de-duplicated to one set.
