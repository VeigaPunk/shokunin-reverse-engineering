# ZB — six-entry manifest (final convergence read of Z1–Z6)

## CLAIM
Parent-ready manifest for the six round-7 knowledge entries: final text location, open conditions, hyphenated filename, map-row and table-row sources. Nothing landed; no tracked file touched.

## METHOD
Read Z1–Z6 and every input they reference (E1D–E6D, E1V–E6V, G1–G6, M1/M2, K3/K4), `corpus/QUALITY.md:11-25`, `CORPUS.md:17-19`. Command A (SCORECARD.md:93-123) at HEAD `411175e337c0725ae9bee3fd478ae9bf05bedf3f` → `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "knowledge_files": 72, "mapped": 72, "missing": []}`. Read-only simulation of the post-landing map: hyphen rows + hyphen stems → 78/78, no missing/dangling; underscore rows → 72 mapped, 6 missing, 6 dangling (`2026-10-16-l7-01-inspect`, …). Only this file written.

## FINDINGS
Paths relative to `.ufo/waves/luna-round-7/`. Fields: final text — open conditions — filename — map row — table row.

1. **inspect_go_binary** — Z1.md:11-23 (alt E1D.md:13-26) — add `source:/verified-at:/recheck:` header (CORPUS.md:17-19); keep captured-description vs tested split — `2026-10-16-l7-01-inspect-go-binary.md` — M1.md:11, underscore→hyphen token; K3.md:8, hyphenate.
2. **inspect_rust_binary** — no Z text; Z2 absence claim stale (E2D/G2 exist). Primary E2D.md:10-17 (both carriers, distinct identities); narrower alt G2.md:11-24 — add header; scope per ruling (c); preserve A-fallback + inferred-hash labels (E2V.md:8-10) — `2026-10-16-l7-02-inspect-rust-binary.md` — M1.md:12, hyphenate — K3.md:9, hyphenate.
3. **inspect_electron_fuses** — no Z text; E3D.md:8 — add header (G3.md:10); G3's `E3D.md:12-26` pointer stale (file ends :14; Z3.md:8) — `2026-10-16-l7-03-inspect-electron-fuses.md` — M1.md:13, hyphenate — K3.md:10, hyphenate.
4. **inspect_sqlite_database** — G4.md:11-22 (B-only per ruling b); exclude lane-A synthetic (QUALITY.md:22) — add header; E4V.md:13-19 "receipts untracked" stale: HEAD has leg-6 receipts both lanes; only SC1–SC6 untracked — `2026-10-16-l7-04-inspect-sqlite-database.md` — M2.md:10 (alt E4D.md:11) — K4.md:10, hyphenate (alt M2.md:15).
5. **search_bytes** — no converged text; Z5 absence claim stale (E5D/G5 exist). Compose from E5D.md:2-13 + G5.md:8-11 + E5V.md:8-13 — add header; keep `complete:true`=loaded-blocks caveat — `2026-10-16-l7-05-search-bytes.md` — M2.md:11 — K4.md:11, hyphenate (alt M2.md:16).
6. **inspect_with_objdump** — E6D.md:10-19 (already has all three metadata fields) — none — `2026-10-16-l7-06-inspect-with-objdump.md` — M2.md:12 (alt E6D.md:21) — K4.md:12, hyphenate (alt E6D.md:23 / M2.md:17).

## THREATS
Z2.md:5,11 and Z5.md:3,6 absence verdicts are tool/race artifacts; entries 2 and 5 drafts were read directly. Command A needs hyphenated README map tokens and filenames: M1's rows and K3/K4 tokens still carry `_`; K-table rows sit outside command A's scan but normalize for consistency. Untested here: merged texts' QUALITY conformance, 72 prior files byte-identical, post-landing 9/9 rules.

## VERDICT
FINDING: manifest complete; hyphen-normalize M1/K3/K4 tokens, add metadata headers to entries 1–5, compose entry 5 text; Z2/Z5 absence and E4V untracked claims stale.
