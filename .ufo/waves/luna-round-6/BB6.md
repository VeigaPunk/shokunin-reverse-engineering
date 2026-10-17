## CLAIM
Round-6 leg-6 re-run (BB6): `inspect_sqlite_database` on SC4's database returns outcome class RESULT, matching the frozen L6 prediction; evidence is my own hashed receipt `receipts-B/leg-6.md`.

## METHOD
Protocol read from lane-A seat reports (not receipts): `P0.md:9` (L6 line, `/tmp`, ≤240s), `EX6.md:7`, `RV3.md:5` (MCP framing). Tool input schema confirmed from the cached 6.5.0 contract (`cutterToolContracts-TZH9EHr5.js:778-779`: strictObject, required absolute `path`), read-only. Took SC4's carrier (`SC4.md:8,17`) and copied it to `/tmp/bb6-leg-6/sc4-index.db` (hashes equal; no `-wal` sibling). One MCP session from `/tmp` — `npx -y rea-agents@6.5.0 mcp`, npm cache + TMPDIR under `/tmp` — frames initialize → notifications/initialized → tools/call, awaited id=2, closed stdin; 230s driver self-deadline under `timeout 240`. Server exited 0 in 0.70s; no leftover process. Receipt: `receipts-B/leg-6.md`.

## FINDINGS
- Initialize response: serverInfo `rea` 6.5.0, protocol 2025-03-26 (receipt stdout line 1).
- tools/call: typed Evidence `ev_7572e622…`, subject sha256 `3701a7e3…` = input hash; provider SQLite 3.54.0; `wal: null`; schema inventory complete: one ordinary table `package_index` (root page 2, without_rowid, 2 columns), no indexes/views/triggers → class RESULT, frozen L6 matched.
- Cross-check: `sqlite3 /tmp/bb6-leg-6/sc4-index.db "SELECT name,type,rootpage FROM sqlite_master ORDER BY rootpage;"` → `package_index|table|2`.
- stdout 9,763 bytes sha256 `a3c0bc10…`; stderr 186 bytes `"status":"ok"`; exit 0; host DB and snapshot hashes unchanged post-run.
- Lane-A seat reports record L6 RESULT too (`EX6.md:3`, `RV3.md:8`) — class agreement; carriers differ (theirs: generated `/tmp/luna-round-6-leg-6.sqlite`).
- No config edits; HEAD `f0e8cde` unchanged; `git status` only pre-existing untracked `.ufo/`.

## THREATS
SC4's DB is live pnpm state (`SC4.md:21`); I probed a byte copy, quiescent at copy time but not an atomic snapshot (engine limitation recorded in the result). npx ran with an isolated `/tmp` cache; the host npm cache was only read to confirm the schema. Command A/token-set controls are round-level, not run by this seat. Driver meta re-logs the id=1 line during its second pump scan; raw capture is ground truth (2 lines verified). Cross-lane class agreement here is same-tool-same-class, not same-carrier.

## VERDICT
CLEAN — L6 re-run returns RESULT, matching the frozen prediction; hashed receipt at `receipts-B/leg-6.md`.
