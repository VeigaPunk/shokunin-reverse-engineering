## CLAIM
Recompute seat X2's six-row arc census (`.ufo/waves/luna-round-10/X2.md`) from raw sources only and adjudicate every numeric cell.

## METHOD
Re-ran X2's commands; ran SCORECARD.md recipe A (git-object reader) at `411175e`/`6e83a20`/`c343939`; counted `corpus/knowledge` `.md` files per tree (`git ls-tree`); extracted all nine reports' verdict sections programmatically; recomputed at X2's HEAD (`6e83a20`) and at current HEAD (`c343939`).

## FINDINGS
Exact recomputes:
- Row 1: 4×64+5×128=896 ✓; all nine cited spans land on the claimed text; R6 127 distinct ✓ (r6:47-50). "895 distinct" is assumption-labeled (896−1); premise unverifiable (r9:56 records VB3 absent — delivery gap, not dispatch count).
- Row 2: command reproduces `[0, 27, 0, 1, 4, 26, 3, 17, 2] 80` verbatim. Composition: 30 battery legs (r6 20 + r8 10), 27 r2 probe receipts, 16 censuses, 3 MANIFESTs, 4 r8 auxiliaries = 80; "not 80 test legs" ✓. Minor cite gap: "10 per lane" is r6:15-17, not cited :35-43 (the 20/20 hash line r6:43 is in span).
- Row 3: tree counts `411175e`=72 → `1cfd2a3`=78 → `18dc397d`=79 → `c343939`=79; recipe A at `6e83a20` returns r9's JSON verbatim: `{"citation_resolved_rules": 9, "coverage_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 9, "depth_score": 10.0}`.
- Row 5: 36 axis-verdicts recomputed = 9 improved + 27 unchanged + 0 harmed + 0 unprovable-but-better; "Admitted: yes" ×9; verdict headings at claimed lines (r1:85, r2:80, r3:77, r4:76, r5:75, r6:76, r7:63, r8:57, r9:62).
- Row 6 short-counts: 5/9 ✓ (r2:57-59, r4:61-64, r5:60-62, r6:47-50, r7:3-4).
Drift found:
- Row 4: at `6e83a20` the window was 19 luna-round-* + `a79945c` (round-1 erratum), count 20 ✓. Current HEAD is `c343939` (protocol-conformance, committed 22:42:01, after X2.md's 22:31 mtime): same command still prints 20, but now 19 luna-round-* + `c343939`; `a79945c` aged out. "HEAD 6e83a20" is stale.
- Row 6 "backfills recorded": explicit only for R2/R4 (6-seat) and R7 (5-seat); R5 says "Repaired" (no backfill term); R6 records none — closed repair-less at 127.

## THREATS
X2's MANIFEST threat verified: `git ls-files '*MANIFEST*'` = 3 receipt MANIFEST.txt, zero MANIFEST.json. Receipt corpus is 43/80 tracked (r6+r8 only); the 80-count includes untracked working-tree files. Lane A's SCORECARD-rewrite item is not this seat — not adjudicated here.

## VERDICT
FINDING: all printed numbers recompute exactly at X2's snapshot; row 4 is stale under current HEAD `c343939` and row 6's "backfills recorded" holds for only 4/5 rounds.
