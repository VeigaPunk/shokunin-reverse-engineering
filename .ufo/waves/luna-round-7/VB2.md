## CLAIM
Evidence re-verify for round-7 entries 3–4: every anchor cited by E3D/E4D resolves at the stated lines; all retained hashes, Evidence IDs and stdout digests recompute on live state; entry 4's lane-A exclusion is justified. Landing still pending (corpus 72 files, 0 l7).

## METHOD
Read-only: E3D/E4D, SC3/SC4, leg-5/leg-6 receipts (both lanes), CC5, RV3, G3/G4, K3/K4, QUALITY.md, SCORECARD.md:92-123; recomputed SHA-256 of the carriers, retained /tmp captures and receipt-embedded stdout blocks; replayed command A from a temp `git archive HEAD` copy. No probes, MCP, network; no tracked file touched.

## FINDINGS
- Entry 3: `/usr/lib/signal-desktop/signal-desktop` re-hashes `f7a9b441…c85a`, 223,513,856 B = `SC3.md:10` = `receipts/leg-5.md:5` = `receipts-B/leg-5.md:8`. Block `receipts/leg-5.md:8` (3,771 B) → `afebe903…` = recorded `:12`; `/tmp/rea-bb5/call.stdout` → `14ef0f1c…` = recorded `receipts-B/leg-5.md:24,44`; line hashes `5a4a91b6`/`83f9d564` reproduce. Both lanes carry Evidence `ev_36045c43…`; sentinel 35260752, wire v1, length 9, complete; raw bytes 48,49,48,48,48,49,48,49,49 — E3D:8 matches (six names abbreviated, see `DB3.md:13`). Receipt file hashes `52741f00…`/`57ac0124…` = `CC5.md:8`, `BB5.md:2`.
- Entry 4: host `…/pnpm/package-manager-store/v11/index.db` re-hashes `3701a7e3…`, 16,384 B, mtime 1792051409 unchanged; `/tmp/bb6-leg-6/sc4-index.db` identical on disk; `/tmp/bb6-leg-6/mcp-stdout.raw` 9,763 B → `a3c0bc10…` = `receipts-B/leg-6.md:30-31`; stderr 186 B → `df3311d1…` = `:39`; embedded block `:34-35` reproduces `a3c0bc10…`. E4D:8's B-observation transcribes `:35` exactly.
- Lane A: `/tmp/luna-round-6-leg-6.sqlite` gone; no recipe in repo or /tmp; `receipts/leg-6.md:10-11` keeps only size+hash; `RV3.md:5` says generated → QUALITY criterion 12 (`QUALITY.md:22`, outside E4D:5's 11-19 range) exclusion stands (ruling b). Its recorded block `:18-19` does reproduce `9a1445b4…`.
- Anchors: leg-5/6 receipts are in HEAD `411175e`; SC3/SC4/CC5/RV3 untracked (auxiliary only). Command A at HEAD replayed: `knowledge_files=72, mapped=72, missing=[], dangling=[], citation_resolved_rules=9, coverage_score=10.0`.

## THREATS
Static records only — round-6 executions not observed. Lane-A fixture bytes unrecoverable. E3D/E4D lack `source:`/`verified-at:`/`recheck:` (ruling d); G3's `E3D.md:12-26` pointer is stale (file has 14 lines). Underscore stems persist for entries 3–4 in `K3.md:10`, `K4.md:10`, `M1.md:13`, `P1.md:16`; E4D:11-12 is hyphenated — land hyphenated per ruling (a); regex `[a-z0-9-]+` at `SCORECARD.md:102`. Post-landing 78/78 and prior-72 byte identity are not verifiable pre-integration (other seats).

## VERDICT
CLEAN — entries 3–4 evidence re-verifies end-to-end; residual items are integration-side metadata/stem hygiene already covered by rulings.
