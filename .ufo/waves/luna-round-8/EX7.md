## CLAIM
Frozen L7 predicted `search_bytes` on `/usr/bin/true` after `open_binary` via REA 6.4.0 would yield TYPED-REFUSAL (unknown tool). Observed result matches; this is a fleet OPERABILITY symmetry measurement, not a promotion.

## METHOD
From `/tmp`, ran `npx -y rea-agents@6.4.0 --mcp` in a bounded stdio MCP session; initialized protocol 2025-03-26, called `open_binary` on `/usr/bin/true`, then `search_bytes` for `7f 45 4c 46`, and closed stdin. Full command, request frames, stdout/stderr, exit, and digest: `receipts/leg-7.md:3-32`.

## FINDINGS
`open_binary` returned ELF x86-64 and carrier SHA-256 `8bc9a73afd7d85061160857536e093ded799dae7a2f0cf5758c4553f2f83002d`. `search_bytes` returned JSON-RPC `-32602`, `Tool search_bytes not found`: TYPED-REFUSAL, prediction matched. Server reported REA 6.4.0, exited 0, and no REA MCP process remained (`receipts/leg-7.md:12-21,26-31`). Raw stdout SHA-256: `866f8b5827c750b5216fd125c2b7253429a2f9937ae5f978eb5484e6cb21bb6b` (`:15`).

## THREATS
One package-pin run and one carrier only; no general tool-capability claim. Registry/network activity and fleet-wide config drift were not independently measured.

## VERDICT
CLEAN
