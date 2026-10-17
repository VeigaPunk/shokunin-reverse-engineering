# PB2 — divergence ledger (lane A luna / lane B deepseek-v4.1-flash)

## CLAIM
Ledger of every lane divergence at snapshot 2026-10-16T22:04Z: receipt classes, seat contradictions, XA items — each with disposition. No execution and no promotion claim.

## METHOD
Read-only: all 54 lane-A seat reports, XA.md, `receipts/` (10 legs, MANIFEST, census-pre); lane-B arrivals through snapshot (BB1–BB10 seats, SB2/SB4; `receipts-B/` all 10 legs); XA citations rechecked line-by-line (`sed`). No probes, no MCP, no config edits.

## FINDINGS
|Item|Evidence|Disposition|
|Cross-lane classes|all 10 legs class-agree A↔B (BB1–BB10; `receipts/` vs `receipts-B/`)|10/10 agreement; byte-identical stdout L1/2/7/8/10 only|
|L9 cross-lane|B `2a20c456…` vs A `2b596b31…`(frame)/`1ff84c06…`(raw) (`receipts-B/leg-9.md:54`; `receipts/leg-9.md`)|B captured pretty-printed 772B frame, not wire bytes; refusal fields identical; no byte agreement|
|L6 receipt collision|canonical `leg-6.md`=RV3 replay on generated /tmp db; EX6 transcript replaced (`EX6.md:15`; `RV3.md:5`); B re-ran on SC4's db (`receipts-B/leg-6.md:4`)|RESULT both; parent reconciliation; EX6 raw only in /tmp|
|L6 digest|RE1 found receipt-vs-bytes mismatch (`RE1.md:10`); current leg-6 recomputes matching|Superseded capture; XA cites `EX8.md:10` — EX8 has no L6 (miscite)|
|L4 carrier|A `leg-4.md`=Signal `.node` fallback (`EX4.md`; `RV2.md:9`) vs B `leg-4.md`=SC2's `/usr/bin/rg` (`SC2.md:10`; `receipts-B/leg-4.md`)|RESULT both; B complied with SC2's carrier, A's assigned-target compliance unverified; hashes differ by design|
|L10 route|canonical Wasm-prereq refusal (`leg-10.md`; `EX10.md:8`) vs RV4 harmony refusal (`RV4.md:6,10`)|Both typed refusals; `compare_wasm_interfaces` never ran; XA cites `RV2.md:6,10` — wrong file; credit flagged (`BB10.md`)|
|Stale snapshots|PS1–3, RE1–3, RV5–8, CA7, XG1/2 predate receipts|Not mismatches; superseded; final lane-A classes match 10/10|
|Hygiene|live MCP leftovers (`SE3.md`; `RV1.md`); 4 receipts lack 240s evidence (`RE1.md:9`); BB9 saw concurrent seats' processes|Open cleanup gap; no class impact|
|Scope|no drift post-L1 (`SE2.md`); HEAD pinned, 0 tracked/out-of-dir writes (`SB4.md`); census-pre only; literal zero-`/tmp` needs carve-out (`CA4.md`; `RE3.md`)|Post-state census absent (`CE1.md`); command-A/map unchanged = pre-state|
|XA items|MANIFEST lists leg-1 only; L9 raw-process digest not recomputable from receipt|Manifest incomplete; digest replay-verified (RV7 `1ff84c06…`), not self-contained|

## THREATS
Lane B closed all 10 receipts mid-write; classes agree 10/10, but byte-identity covers only L1/2/7/8/10 (L3 capture, L5 CLI-vs-MCP, L9 serialization, L4/L6 carriers differ). Lane-B seats read lane-A receipts for routes (allowed) — not blind. Snapshot 22:04Z; files still moving. XA miscites (2) show citations need spot-checks. EX9's batch attempt would be ERROR-UNEXPECTED if scored; exclusion rule parent-owned. Lane-A seat-file count 54 vs stated 64 — roster unverifiable.

## VERDICT
FINDING: classes agree across lanes on all 10 legs; L6 collision, L4/L6 carrier splits, L10 dual route, XA miscites, and byte-comparability limits remain open.
