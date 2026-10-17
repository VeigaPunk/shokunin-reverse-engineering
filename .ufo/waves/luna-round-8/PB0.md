## CLAIM
Verify lane A's 6.4.0 symmetry battery at HEAD 6e2ee8f: receipts present and hash-valid; 10/10 vs frozen predictions; leg-3 display-hash defect status and repair plan; stale-verdict adjudication.

## METHOD
Read-only. `sha256sum receipts/leg-*.md` vs `receipts/MANIFEST.txt`; Python byte-extraction of every leg's fenced stdout block vs its in-file claim; `cmp` leg-3 block vs `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`; re-hashed surviving /tmp artifacts (rv1 leg1/leg2, ex7, leg10, leg-6 sqlite); `wc -l`/`sort -u`/`grep -cFx` on `leg-2-tools.txt`; `sha256sum /usr/bin/jq`; `head -n 59 receipts/leg-10.md | sha256sum`. No probes; no writes besides this file.

## FINDINGS
All ten canonical legs plus `leg-2-tools.txt`, MANIFEST, census-pre, 3 RV3 replays present; legs 1–9 recompute to MANIFEST exactly. `leg-10.md` (mtime 21:14) hashes `6cd389e9`; `head -n 59` = `c89eea7a` (MANIFEST value, 27655 B) — append-only EX10 supersession, no byte loss; internal claims `61450b92`/`6abdf805` and original raw stdout `23e94d0b` recompute.
10/10 independently: L1 6-byte `6.4.0\n` = `3754366908ac` (equals `/tmp/kaidoku-luna-round8-rv1/leg1.stdout`); L2 `leg-2-tools.txt` = 170 lines, 170 unique, block = `0bbe6bc75c8f` (= rv1 leg2.stdout); L3–L8 in frozen order return `-32602 Tool <name> not found`, exit 0; L9 my `grep -cFx` = 0 for all six names; L10 jq `inspect_binary_layout` RESULT, artifact digest `e815667571d0` = actual `/usr/bin/jq` re-hash.
leg-3 defect: the census-era file (1430 B `d641e3d3`, reconstructed hash-identical via `/tmp/zb3-broken-sim.md`) displayed `"prompts":{}` where raw bytes have `"prompts":{"listChanged":true}` — block 605 B `ac7470f9` vs claimed `5c682099`. Delivered `leg-3.md` (1448 B `1be7e4f9`, mtime 20:59:03, pre-MANIFEST) block is 623 B, byte-equal to claim and to the /tmp artifact → defect already repaired; plan = none, retire the note. census-pre leg-3/leg-4 rows are that pre-repair snapshot, not delivered bytes.
Stale verdicts (pre-delivery reads superseded by landed receipts, CA6 10/10 census 21:07, FB2 audit, and this check): PS1, PS2, PS3, PR1, PR2, RE2, RE6, RV8, CA3, CA7, CA8.

## THREATS
No re-execution (rules). L4/L5/L6/L8 lack surviving raw stdout; blocks verify only against receipt-side claims (L5/L6 carriers and hashes re-verified). Protocol echo varies (`2024-11-05` vs planned `2025-03-26` on some legs) — outcome classes unaffected. Config-drift zero still lacks a true before/after pair (CA6). MANIFEST/census-pre rows need annotation, not reconciliation.

## VERDICT
FINDING: battery verified 10/10 at delivered revisions; leg-3 defect existed only in the pre-repair generation (already fixed); leg-10/MANIFEST and census-pre staleness is supersession, not corruption; 11 early absent/unscored verdicts superseded.
