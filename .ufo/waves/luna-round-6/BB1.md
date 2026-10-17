# BB1 — leg 1 independent re-run (lane B)

## CLAIM
Lane-B independent re-run of leg 1 reproduces lane A exactly: `rea-agents@6.5.0 --version` prints `6.5.0`, exit 0, byte-identical stdout. Pre-registered L1 class RESULT → MATCH, cross-lane agreement confirmed at hash level.

## METHOD
Command: `cd /tmp/rea-bb1 && npx -y rea-agents@6.5.0 --version` (npx/MCP from /tmp per probe rules; 240s budget; wall ~0.6s, cache hit). stdout/stderr redirected to separate files; exit captured to file; `sha256sum` on stdout; `xxd` to pin exact bytes. npx = `/home/vgpnk/.local/share/mise/installs/node/latest/bin/npx`, node v26.12.0, cwd `/tmp`. Lane A's leg-1 receipt was read only AFTER my own run and hash were recorded.

## FINDINGS
- Exit 0; stdout exactly `6.5.0\n` (bytes `36 2e 35 2e 30 0a`); stderr empty (0 bytes).
- stdout sha256 `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00` — identical to lane A's leg-1 stdout hash (`.ufo/waves/luna-round-6/receipts/leg-1.md:11` vs my receipt).
- Frozen prediction L1 (version 6.5.0, exit 0) → observed RESULT class. MATCH.
- `--version` starts no MCP server; `pgrep -fa rea-agents` shows no orphan (only the check's own shell, plus unrelated pre-existing host process PID 3018 cli-agents-mcp).
- Receipt written: `.ufo/waves/luna-round-6/receipts-B/leg-1.md`.

## THREATS
- Sub-second npx run indicates a warm npx/npm cache (almost certainly populated by lane A). This validates the cached artifact, not a cold fetch; a cold-fetch rerun was not assigned and cache cleaning would touch shared state.
- Both lanes share host, node runtime, and npx install → common-mode risk; hash equality proves reproducibility of output, not independence of the toolchain.
- Only `--version` exercised; runtime behavior beyond version reporting untested here.

## VERDICT
CLEAN — leg 1 independently reproduced, byte-identical stdout hash, RESULT class matched, receipt filed.
