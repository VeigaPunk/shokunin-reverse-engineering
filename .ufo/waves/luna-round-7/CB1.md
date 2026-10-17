## CLAIM
Overclaim audit of all six round-7 recommended entry texts: E1D+Z1 (01 go-binary), E2D+G2 (02 rust), E3D (03 fuses), G4 (04 sqlite, per ruling b), E5D (05 search-bytes), E6D (06 objdump). Question: does any claim exceed retained round-6 receipt bytes?

## METHOD
Read the six draft texts, E1V–E6V, G1–G6, Z1–Z6, F8; verified every hash, Evidence ID, offset, count, and limitation against `.ufo/waves/luna-round-6/receipts/leg-{3..8}.md`, `receipts-B/leg-{3..8}.md`, SC1–SC5, RV3.md, CB3.md, CC4/CC5, and `corpus/QUALITY.md`. No probes, network, or repo edits; only this file written.

## FINDINGS
- All substantive facts are receipt-backed. Spot-verified: docker `70f68a77…` / 29,327,600 B / header 28,873,984 (`receipts/leg-3.md:97,104`); rg `ev_9ea976…` (`receipts-B/leg-4.md:47`); Signal `ev_36045c…`, 9-state fingerprint, sentinel 35,260,752, 48/49 (`receipts/leg-5.md:8`); index.db `3701a7e3…`, `wal:null`, `rows:null`, `columns_completeness:not_requested` (`receipts-B/leg-6.md:35`); `searched.bytes 33668`, `0x100000`, `complete:true` (`receipts/leg-7.md:21`); jq `e8156675…`, `HAS_SYMS, DYNAMIC, D_PAGED`, `0x3cf0` (`receipts/leg-8.md:19`). No fabricated IDs, numbers, or capabilities.
- Two wording-level items. (1) `E5D.md:5` renders the recorded probecall as `search_bytes(pattern="7f 45 4c 46", limit=100)`; both lanes' request frames omit `limit` (`receipts/leg-7.md:9`; `receipts-B/leg-7.md:22`); 100 appears only as the response's effective parameter (`receipts/leg-7.md:21`) and lane B's "(default)" note (`receipts-B/leg-7.md:60`). (2) `E3D.md:8`/`G3.md:8` say lane B "independently matches/records"; BB5 derived its target from lane A's receipt (`receipts-B/leg-5.md:9`) and CC5 discloses a non-blind replay (`CC5.md:17`) — yet the matched Evidence ID/fingerprint themselves are receipt-backed (`receipts-B/leg-5.md:28,52`).
- Entry 4: G4's B-only text is fully receipt-backed (`receipts-B/leg-6.md:23-28,35,52-55`; `SC4.md:8-18`); E4D's combined text/rows still include the excluded lane-A synthetic RESULT (ruling b already applies).
- House metadata: only `E6D.md:12-14` carries `source:`/`verified-at:`/`recheck:`; E1D, E2D, E3D, G4, E5D lack them (grep `verified-at:` over round-7 drafts → E6D plus review seats only).

## THREATS
Receipt review only — no replay or re-hash. Receipt legs 3–8 are tracked at HEAD (`git ls-tree`), but SC1–SC6 are untracked (`??`), so scout pointers do not resolve at HEAD; every fact I checked is carried by tracked receipt lines. `E1D.md:26`'s pointer list omits the lines holding its input-schema claim (schema at `receipts/leg-3.md:20-50`) — claim itself is in-receipt. Z2:5/Z5:2-5 declare E2D/G2/E5D/G5 absent; all four exist (E2D predates Z2), so those absence verdicts are superseded.

## VERDICT
FINDING: no unsupported substantive claims in the six texts; before landing, reword E5D's `limit=100` (request frames omit it; effective default only) and E3D/G3's "independently" (disclosed non-blind compare), and add `source:`/`verified-at:`/`recheck:` to the five texts lacking them.
