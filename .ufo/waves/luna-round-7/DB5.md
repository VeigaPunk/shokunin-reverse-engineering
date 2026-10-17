## CLAIM
Entry-5 content (E5D.md → `corpus/knowledge/2026-10-16-l7-05-search-bytes.md`) is derivable from the leg-7 receipts; two citation precisions and the missing house metadata header must be fixed at landing.

## METHOD
Read-only review, no live probes/MCP/network: E5D/E5V, `receipts/leg-7.md`, `receipts-B/leg-7.md`, SC5, M2/K4; line checks via grep/sed. First-hand Command A (body `SCORECARD.md:93-123`, REV `411175e337c0725ae9bee3fd478ae9bf05bedf3f`): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9}`. `git ls-tree ... -- corpus/knowledge | grep -c l7-0` → 0; l7 tokens under `## Coverage map` → 0. No tracked file modified.

## FINDINGS
- Each E5D assertion traces to receipts: carrier/hash/Evidence ID/pattern (`.ufo/waves/luna-round-6/receipts/leg-7.md:8-14,21`); requests (`receipts/leg-7.md:8-9`; `receipts-B/leg-7.md:21-22`); resolve to `/usr/bin/true` (`receipts-B/leg-7.md:25`); hit `0x100000`/`segment_2.1`/file offset 0/procedure null, 33,668 bytes, complete, no cursor (`receipts-B/leg-7.md:58-60`); byte-identical stdout (`receipts-B/leg-7.md:66-68`); block-scope limits (`receipts/leg-7.md:21`; `receipts-B/leg-7.md:32`). Assertions are labeled observation/inference/unknown; RESULT-class (`receipts/leg-7.md:13`), no Core promotion.
- Precision 1: `limit=100` is not in the recorded requests (`receipts/leg-7.md:9`; `receipts-B/leg-7.md:22`); it is the effective parameter (`receipts/leg-7.md:21`; `receipts-B/leg-7.md:32`) labeled "(default)" (`receipts-B/leg-7.md:60`). Land as "effective limit 100 (default)".
- Precision 2: METHOD cites `leg-7.md:3-12` and `receipts-B/leg-7.md:21-25` for "Ghidra 12.1.4, default auto-analysis"; those facts sit at `receipts/leg-7.md:13,21` and `receipts-B/leg-7.md:32`. Add those cites.
- Admission: `grep -n "source:\|verified-at:\|recheck:" E5D.md` → no output. CORPUS.md:17 requires entries to open with these fields; E6D.md:12-14 shows the pattern. Landing material exists (E5D.md:2,5,8,11; M2.md:21) with the hyphenated stem of parent ruling (a).
- Cross-check: K4.md:11 Knowledge-row stem is `2026-10-16-l7-05-search_bytes` (underscore); landed rows must use the hyphenated stem to match the file stem (`SCORECARD.md:102` token regex `[a-z0-9-]+`).

## THREATS
Documentary review of retained records only; no replay. Entries absent at HEAD (72 files; 0 l7), so 78/78 and map/table integration remain unverified here. SC5 is worktree-only (`git cat-file -e HEAD:.ufo/waves/luna-round-6/SC5.md` → "not in HEAD"), so it must not anchor the entry alone. E5D may change after this snapshot.

## VERDICT
FINDING: all entry-5 claims are derivable; before admission add `source:`/`verified-at:`/`recheck:` (absent from E5D) and the two citation fixes (effective-default limit; provider/auto-analysis lines).
