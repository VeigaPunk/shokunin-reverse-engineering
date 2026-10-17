## CLAIM
At 2026-10-16 20:59:42 -0300, all ten canonical receipts are present and their recorded outcomes match the frozen predictions. Protocol evidence has one integrity finding: L3's displayed stdout does not match its recorded SHA-256. No live REA/MCP process was detected.

## METHOD
Inventoried `receipts/leg-1.md` through `leg-10.md`; checked L2's 170-line `leg-2-tools.txt` and searched for all six predicted 6.5-only names. Recomputed SHA-256 over available stdout blocks and compared L3 with `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`. Checked `pgrep -a -f 'rea-agents|rea-mcp|MCP'`, `/tmp` residue, and `git status --short --untracked-files=no`.

## FINDINGS
- Ten canonical receipts are present. L2 lists exactly 170 tools; none of the six frozen names occur in the list, consistent with L9. The ten recorded result classes match the predictions.
- L1, L2, L4-L8, and L10 displayed stdout hashes recompute correctly. L3 does not: receipt `leg-3.md:21-22` shows `prompts:{}`; its displayed block hashes to `ac7470f9…2223`, not the claimed `5c682099…a569`. The preserved raw `/tmp` stdout hashes to the claimed digest and has `prompts:{"listChanged":true}`. Its receipt block is therefore not byte-exact.
- Receipts place probes in `/tmp` and report 240-second bounds. L4-L6, L8, and L10 assert a ceiling/deadline but omit the exact timeout-wrapped invocation; enforcement is not independently reproducible from those receipts. Server exits are recorded as 0.
- The process scan returned only its own `pgrep` shell, no REA/MCP server. Round-named outputs, the SQLite fixture, npm caches, L7 harness files, and L10 logs remain in `/tmp`. Tracked worktree status was empty.

## THREATS
This is a snapshot, not a global config-drift or command/token-set audit. The process scan is name-filtered. I did not clean shared `/tmp` artifacts because the seat permits only the RE1 report write.

## VERDICT
FINDING: all ten outcomes are recorded and server cleanup is evidenced, but L3's stdout receipt is not hash-consistent and several timeout bounds are only asserted.
