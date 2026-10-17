## CLAIM

Frozen L4 prediction: `inspect_rust_binary` called through REA 6.4.0 on `/usr/bin/rg` returns `TYPED-REFUSAL`. Observed class matches.

## METHOD

From `/tmp`, ran the 6.4.0 stdio MCP server (`npx -y rea-agents@6.4.0 --mcp`), initialized protocol `2024-11-05`, then called `inspect_rust_binary` with `{"path":"/usr/bin/rg"}`. Target was ELF x86-64, 4,377,936 bytes, SHA-256 `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`. Closed client stdin; server exited 0. Full exchange and digest: `.ufo/waves/luna-round-8/receipts/leg-4.md:1-14`.

## FINDINGS

Server reported version `6.4.0`; response id 2 was JSON-RPC `-32602`, `Tool inspect_rust_binary not found`. This is the predicted `TYPED-REFUSAL`. Raw MCP stdout was 625 bytes, SHA-256 `0fbd3bd0d3095c7c5fe6b2605618dfb88cc3b5f4268cfd9f7d18c683f7030d5f`; stderr was empty; exit code 0.

## THREATS

Evidence establishes only this pinned call and carrier; no `tools/list` census or other-version behavior is inferred. No config edits were made; configuration drift was not independently audited.

## VERDICT

CLEAN