# GB4 — M-row review (faithful one-liners?)

## CLAIM
Reviewed M1's three coverage-map rows and M2's three map + three Knowledge rows against the entry texts they summarize (E1D–E6D, with G1–G6/Z1–Z6 as second opinions), plus parent rulings (a)–(c). Read-only; only this receipt was written.

## METHOD
Read M1, M2, E1D–E6D, G1–G6, Z1–Z6, K3/K4, `corpus/QUALITY.md:11-24`, `corpus/README.md:11-15,59-66`, `SCORECARD.md:92-105`. Spot-verified every hash/offset/id in the rows against round-6 receipts `leg-3…leg-8` (both lanes). Ran the `SCORECARD.md:102` map regex `2026-10-\d{2}-[a-z0-9-]+` over M1.md/M2.md (read-only python). No probes, no network, no tracked-file edits.

## FINDINGS
1. Facts check out: docker `70f68a77…` / `go1.26.5-X:nodwarf5` / module (leg-3:67,106,119); rg `d006acfe…`, no `.dep-v0`, `rustc_commit:null` (leg-4-B:69); Signal `.node` `1b44ed53…` inferred rustc hash (leg-4-A:28); fuse sentinel offset 35260752, nine states, complete (leg-5:8); true `8bc9a73a…`, hit 0x100000/file_offset 0, 33,668 bytes, complete (leg-7:21; B:58-68); jq `e8156675…`, exit 0, complete (leg-8:12). M1 rows 1/3 and M2 row 05 are faithful; M2 row 04 and M2 row 06 carry the defects below.
2. M1 rows 1–3 use underscore stems (`l7-01-inspect_go_binary`…). Command A's regex truncates these — output: `['2026-10-16-l7-01-inspect','2026-10-16-l7-02-inspect','2026-10-16-l7-03-inspect']`, vs the hyphenated stems in E1D:8/E2D:2/E3D:2. Integrated verbatim: 3 missing files + 3 dangling tokens, so `mapped=78, missing=[], dangling=[]` fails. Fix: hyphenate. M2's rows are already hyphenated (regex returns its three full tokens).
3. M2 row 04 keeps the excluded half: map cell "SQLite selected-table sample vs inventory-only schema" and Knowledge cell "Selected-table schema/sample and inventory response", source "L6 receipts A/B". Ruling (b)/Z4/G4 admit lane-B only (lane-A fixture has no retained bytes/recipe; QUALITY:22). Row must be B-only (path-only inventory, columns not requested, `rows:null`) citing `receipts-B/leg-6.md` + SC4.
4. M2 row 06 says "on jq" (floating name, G6 warning) and drops E6D:21's "two pinned jq ELF inputs; other operations untested". Minor: M1 row 2 compresses rg's observed "no `.dep-v0`" into "unknown".
5. Carriers stay distinct (ruling c) in M1 row 2 and M2 row 06; no row claims Core promotion.

## THREATS
Draft/receipt review, no replay; SC4–SC6 are worktree-only, so their line cites are unverifiable at HEAD. The regex run is a token-level check, not a full post-integration command A run.

## VERDICT
FINDING: M1 tokens must be hyphenated and M2 row 04 must drop the lane-A half, else the rows misstate the admitted entries and block command A's 78/78.
