## CLAIM
Lane-B final QUALITY gate for entry 5 (`search_bytes`, leg 7): the now-present E5D and G5 converge with Z5's substance on one bounded RESULT-class observation, but the entry as drafted is not landable — it omits the required corpus opener `source:`/`verified-at:`/`recheck:` (CORPUS.md:17-19; parent ruling d). Z5.md:2,5 and Q5.md:7 "E5D/G5 absent" are timing artifacts; both files exist now.

## METHOD
Read-only: Z5/E5D/G5/E5V/G3/Q5/K4/M2/C1, `corpus/QUALITY.md:11-24`, `/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:17-19`, both leg-7 receipts, SC5, `SCORECARD.md:92-123`. Ran Command A verbatim at pinned `REV=411175e337c0725ae9bee3fd478ae9bf05bedf3f` (git objects only); regex-checked the proposed stem; `git status --porcelain -uno` → empty. No probes/network. Only this receipt written.

## FINDINGS
- Timing: mtimes E5D 19:59:19, G5 19:59:18, Z5 19:59:38, Q5 19:58:42 — absence claims reflect reads before the writes; actual files verified present.
- Convergence: all three fix the same carrier SHA-256 `8bc9a73a…002d`, Evidence `ev_4b0badc6…`, one hit `0x100000`/file_offset 0, 33,668 bytes searched, `complete:true`, no cursor (`.ufo/waves/luna-round-6/receipts/leg-7.md:21`; `receipts-B/leg-7.md:58-60`); lane-B stdout byte-identical, hash `3492d27d…9a8` (`receipts-B/leg-7.md:66-67`). C1.md:12 and E5V.md:8-13 agree.
- Ruling (a): stem `2026-10-16-l7-05-search-bytes` matches Command A's `[a-z0-9-]+`; M2.md:11 token identical. But K4.md:11's Knowledge row still reads `…-search_bytes` (underscore) — normalize at landing.
- Command A now: `knowledge_files=72, mapped=72, missing=[], dangling=[], citation_resolved_rules=9, coverage_score=10.0` (run above); 78/78 remains post-integration.
- QUALITY substance passes: absolute path+SHA-256 (4), Evidence ID (6), observation/inference/unknown labels (5), stated limitations (7); RESULT non-promotion stated (E5D.md:11; G5.md:14).
- Gaps: E5D contains no `source:`/`verified-at:`/`recheck:` (grep → none); only E6D of the six drafts carries them (E6D.md:12-14). Precision: the provider-version/auto-analysis anchor is `leg-7.md:13` / `receipts-B/leg-7.md:32`, one line outside E5D's cited 3-12 and 21-25; `limit=100` is the recorded default, not a passed argument (`receipts-B/leg-7.md:22` vs `:60`).

## THREATS
Receipt review, not replay; one carrier/pattern only. Command A maps stems, not semantics; prior-72 byte-identity is not re-measured here (baseline digest: N2.md:8). The 78-file/79-row count story (K4.md:14) is an integration concern.

## VERDICT
FINDING: entry 5's substance converges (E5D/G5/Z5) and passes QUALITY, but before landing add the missing `source:`/`verified-at:`/`recheck:` opener and hyphenate K4's 05 row token.
