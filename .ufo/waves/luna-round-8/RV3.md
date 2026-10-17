## CLAIM
L6–L8 replay on REA 6.4.0 matched all three frozen TYPED-REFUSAL predictions.

## METHOD
From `/tmp`, launched one `npx -y rea-agents@6.4.0 mcp` process per leg with a 240-second response deadline, MCP 2024-11-05 initialize, stdin close, and normal server exit. For L7, waited for `open_binary` before calling `search_bytes`. Complete requests, stdout/stderr, exits, and hashes: `receipts/leg-6-RV3-replay.md`, `leg-7-RV3-replay.md`, `leg-8-RV3-replay.md`.

## FINDINGS
- L6: `inspect_sqlite_database` returned JSON-RPC `-32602`, “Tool inspect_sqlite_database not found” on the 16 KiB pnpm SQLite carrier; TYPED-REFUSAL.
- L7: `open_binary` succeeded on `/usr/bin/true` (SHA-256 `8bc9a73a…`); `search_bytes` returned `-32602`, “Tool search_bytes not found”; TYPED-REFUSAL.
- L8: `inspect_with_objdump` returned `-32602`, “Tool inspect_with_objdump not found” on `/usr/bin/jq`; TYPED-REFUSAL.
- All initializes identified REA `6.4.0`; all MCP servers exited 0.

## THREATS
Unknown-tool refusals establish dispatch/version behavior, not analysis of carrier contents or 6.5.0 behavior. This seat did not verify the other seven legs, config drift, Command A, or token-set invariance. Canonical `leg-6.md`–`leg-8.md` receipts already existed for EX6–EX8; they were preserved and these replay captures use RV3-suffixed names.

## VERDICT
CLEAN — all three assigned predictions matched; no full-battery score or promotion inferred.
