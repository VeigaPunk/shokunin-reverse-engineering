## CLAIM
Seat RB2 (lane B, citation verifier 3-4): every citation in the round-7 landing material for entries 3 (`inspect-electron-fuses`) and 4 (`inspect-sqlite-database`) — E3D, E4D, E3V, E4V, and the proposed map/Knowledge rows — resolves at HEAD `411175e` and matches the cited round-6 records.

## METHOD
Read-only review of E3D/E4D/E3V/E4V, SC3/SC4, CC5, RV3, CB3, both lanes' leg-5/leg-6 receipts, `corpus/QUALITY.md`, `SCORECARD.md:92-123` (Command A), `CORPUS.md:17-19`. Extracted every `path:line(-line)` from the four drafts and validated existence/range in Python; grepped each cited hash/Evidence ID in its receipts; ran Command A's token regex (`SCORECARD.md:102`) on the drafted stems; `git ls-tree`/`git status --short` for HEAD durability. No probes, MCP call, or network.

## FINDINGS
- 31/31 cited ranges valid after expanding round-local shorthands (e.g. E4V's `QUALITY.md:22` → `corpus/QUALITY.md:22` = criterion 12); no missing files or out-of-range lines; content matches. Spot checks: `ev_36045c43…`+`f7a9b441…` in both leg-5 receipts; `ev_e0eb446a…`+`71ac0b8e…` in leg-6A; `ev_7572e622…`+`3701a7e3…`+`package_index`/`rows:null`/`columns_completeness=not_requested` in leg-6B and `SC4.md:8-18`; nine fuse states, sentinel offset 35,260,752, `order:"unspecified"`, and both calls' parameters match the cited lines.
- Entry 4: E4D's lane-A citations (`receipts/leg-6.md:3,8-13,19`; `RV3.md:5`) resolve, but ruling (b)/`QUALITY.md:22` excludes that carrier; the B-only text (G4) cites resolvable lines (`receipts-B/leg-6.md:10,20,23-28,34-35,50-55`; `SC4.md:8-21`; `CB3.md:12`).
- Entry 3: E3D's cited filename is hyphenated, but M1:13's proposed map stem `2026-10-16-l7-03-inspect_electron_fuses` truncates under `SCORECARD.md:102` (underscore halts `[a-z0-9-]+`): `findall` → `['2026-10-16-l7-03-inspect']` — the hyphenated file stem cannot map. Entry-4 stems (E4D:11, M2:10,15) map. K3:10/K4:10 Knowledge rows are unscanned: Command A reads only `## Coverage map` (`SCORECARD.md:101`).
- Durability: leg-5/leg-6 receipts (both lanes) tracked at HEAD; SC3/SC4/CC5/RV3/CB3 untracked (`??`). E4V:13-19's claim that the leg-6 receipts are untracked is not reproducible at `411175e` — stale lane-checkout evidence.
- Both entry bodies lack `source:`/`verified-at:`/`recheck:` (`CORPUS.md:17-19`); required at integration, as are expanded shorthands (F4).

## THREATS
Documentary only — no re-run or re-hash; entries are absent, so the post-integration pointer audit remains. Untracked auxiliary reports may change. Scope: entries 3-4 only.

## VERDICT
FINDING: all entry-3/4 citations resolve and match; before landing, hyphenate entry-3's map-row stem (M1:13), add house metadata to both bodies, keep entry 4 B-only, and discard E4V's stale untracked claim.
