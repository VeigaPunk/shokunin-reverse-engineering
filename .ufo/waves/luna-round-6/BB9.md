# BB9 — lane B, leg 9 re-run

## CLAIM

Independent re-run of leg 9 reproduces the frozen outcome class: `identify_flutter_build` on `/usr/bin/jq` via REA 6.5.0 MCP returns a structured TYPED-REFUSAL, with a hashed receipt, graceful server termination, and zero config edits.

## METHOD

- Fresh run; lane-A receipts were not read. Only protocol/method inputs used: the round's probe rules and the tool's own input schema from the cached 6.5.0 package (`identify_flutter_build` = strictObject `{path}`).
- Command: `cd /tmp/rea-bb9 && timeout 240 node probe.mjs`; the harness spawns `npx -y rea-agents@6.5.0 mcp` (cwd `/tmp/rea-bb9`) and sends JSON-RPC `initialize` (protocol `2025-03-26`), `notifications/initialized`, then `tools/call {"name":"identify_flutter_build","arguments":{"path":"/usr/bin/jq"}}`.
- Receipt: `.ufo/waves/luna-round-6/receipts-B/leg-9.md` (command, full stdout, stderr, exit, stdout sha256).

## FINDINGS

- Response (receipt §Stdout; 772 bytes; sha256 `2a20c456d5cccebbe1b84f86582f774001f93527fedf88b1d5fbd1c332e747bd`): `isError: true` carrying a structured error `invalid_request` / `invalid_input` / `invalid_format` — "The APK could not be read as a package: /usr/bin/jq: ZIP archive is malformed". Typed refusal → class TYPED-REFUSAL; matches frozen L9 prediction.
- Server identity: serverInfo `{"name":"rea","version":"6.5.0"}`, negotiated protocol `2025-03-26`.
- Exit 0; MCP server exited code 0 gracefully on stdin EOF; post-run scan found no node/npx process with cwd `/tmp/rea-bb9`.
- Input identity: `/usr/bin/jq` ELF x86-64, jq-1.8.2, sha256 `e8156675…` (not an APK/Flutter artifact).

## THREATS

- Independence caveat: a pre-run repo-wide grep for the tool name surfaced fragments of lane-A seat reports (EX9/RV4) describing the same refusal shape; lane-A receipts were not read and the run is a fresh execution, but the caveat stands.
- TYPED-REFUSAL vs ERROR-UNEXPECTED is a judgment on payload structure; here the error is structured, categorized, and input-bound, so refusal. `isError:true` alone does not decide the class.
- A broad pgrep matched concurrent seats' processes (not mine); my tree's exit code 0 is the evidence. Config drift, command A / map-token invariance, and the other nine legs were not audited by this seat. Network use (npx cache hit) not proven either way.

## VERDICT

CLEAN
