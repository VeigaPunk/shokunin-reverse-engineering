## CLAIM
Answer: is PS1–PS4 + RE2 scoring consistent with the frozen predictions and raw lane-A receipts? Independent recount performed from receipts only.

## METHOD
Read PS1–PS4.md, RE2.md; `stat` birth/mtimes to test each seat's snapshot; recomputed every declared stdout hash (sha256 of extracted blocks); re-parsed leg-2 JSON with json.loads; checked current receipts against PS3's cited lines. No probes executed.

## FINDINGS
- Snapshot coherence holds. PS1 (written 18:18:41) and RE2 (18:18:32) correctly saw only leg-1 (leg-2 born 18:19:00). PS2 (18:19:03) correctly reports L6–L10 absent (earliest birth 18:21:04). PS3 (18:22:44–18:23:10) saw legs 4/6/8/9 (born 18:21:04–18:22:47) and correctly lacked 3/7/10 (born 18:24:22/18:28:03/18:28:04). Receipt mtimes 18:25–18:28 looked paradoxical against PS3; birth times resolve it.
- 10/10 declared stdout hashes reproduce byte-exact: leg-1 3eb8e06c…, leg-2 38d44bf8…, leg-3 fb47bd53…, leg-4 bc4902f7…, leg-5 afebe903…, leg-6 9a1445b4…, leg-7 3492d27d…, leg-8 e0b2d505…, leg-9 2b596b31…, leg-10 e4cf0833…. leg-2 tools array = 207 via my parse; MANIFEST's 24bfd90f… = sha256(leg-1.md).
- Current classes: L1–L2 exact; L3–L8 RESULT (exit 0, Evidence IDs); L9 typed invalid_request/invalid_input; L10 structured capability_unavailable, exit 0. So 9 clean matches. L10's preregistered compare_wasm_interfaces branch was never sent; it matches only under a class-shape reading, while PS3.md:19 / PS4.md:8 quote "RESULT if wasm carriers exist". Parent must rule this slot.
- Drift: PS3.md:17-18 cites leg-8.md:26-28 and leg-9.md:14-26,47; these files were rewritten at 18:28 (now 25 and 13 lines) — class content survives, line cites don't. PS4.md:5 “No matches found” is contradicted by leg-1's birth 18:16:42 if literal; immaterial to its prereg verdict. MANIFEST.txt (18:18:38) covers only leg-1.

## THREATS
Receipts were mutated mid-wave; I verified current revisions, not those seats read. My recount adds no execution evidence. L10's class depends on the parent's reading of the frozen dispatch.

## VERDICT
FINDING: PS scoring is snapshot-consistent and all 10 stdout hashes reproduce; only L10 awaits a class ruling (9 vs 10 match).
