## CLAIM
Replayed L3–L5 on REA 6.4.0 MCP: all three matched the frozen TYPED-REFUSAL predictions. Their 6.5.0 comparison calls were RESULTs.

## METHOD
From `/tmp`, used a separate REA 6.4.0 MCP session per leg with a 240-second limit; each initialized protocol `2024-11-05`, sent `notifications/initialized`, then its assigned `tools/call` and carrier. Closed stdin; each server exited 0. Receipts preserve each invocation, full stdout/stderr, exit and stdout SHA-256; extracted stdout hashes recomputed to the recorded values.

## FINDINGS
- L3 `/usr/bin/docker`: JSON-RPC `-32602`, `Tool inspect_go_binary not found` — TYPED-REFUSAL (`receipts/leg-3.md:21-23`). 6.5.0 returned RESULT on the same carrier, Evidence `ev_671861638ed7fe544cce229c3d4a9258766337a5e72dcf79f107af713b596a4b` (`.ufo/waves/luna-round-6/receipts-B/leg-3.md:41-42`).
- L4 `/usr/bin/rg`: `-32602`, `Tool inspect_rust_binary not found` — TYPED-REFUSAL (`receipts/leg-4.md:12-13`). 6.5.0 returned RESULT on the same carrier, Evidence `ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2` (`.ufo/waves/luna-round-6/receipts-B/leg-4.md:46-47`).
- L5 Signal: `-32602`, `Tool inspect_electron_fuses not found` — TYPED-REFUSAL (`receipts/leg-5.md:8-9`). 6.5.0 returned RESULT on the same carrier, Evidence `ev_36045c43ecbed14e3eb3b77a720c24c115cc2377737d2ed2fe8acce76a4288ed` (`.ufo/waves/luna-round-6/receipts-B/leg-5.md:27-28`).

## THREATS
Unknown-tool errors precede carrier analysis, so these replays show version-specific MCP dispatch/catalog behavior, not artifact readability. No other legs, config drift, command A or token checks were assigned here.

## VERDICT
CLEAN