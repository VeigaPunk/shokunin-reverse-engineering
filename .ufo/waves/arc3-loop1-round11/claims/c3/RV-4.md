# RV-4 — C3 availability re-probe

## Claim and boundary
Re-probe the session-scoped `available:true` class recorded at `PROVINCE.md:50` for `inspect_artifact` / `extract_artifact`. This is a local REA CLI capability-session measurement, not proof that this agent's active MCP connection is healthy.

## First-hand measurement
The active seat exposed no `binary_session` MCP tool. `rea` was not on `PATH`; I used the already-cached REA 6.7.0 executable at `/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/.bin/rea` (no package acquisition).

Command:
```sh
"$HOME/.npm/_npx/9b9809298fe40d2c/node_modules/.bin/rea" capabilities --format json
```

Output excerpt (from the command result):
```json
{"open":false,"cleanup_pending":false,"capabilities":[{"provider":{"id":"rea-artifact-graph","name":"REA safe artifact graph provider","version":"1"},"shared_limitations":["DMG child inventory automatically uses a read-only native macOS mount; PKG remains root-hash-only.","ASAR files discovered in filesystem-backed inventories are expanded without bulk extraction; other nested containers remain recorded only."],"groups":[{"operations":["decode_interface_builder","inspect_keyed_archive","trace_dylib_resolution"],"effects":[],"limitations":[],"available":true,"reason":null,"availability_code":null},{"operations":["extract_artifact","inspect_artifact"],"effects":["launches_process","may_write_filesystem"],"limitations":[],"available":true,"reason":null,"availability_code":null},{"operations":["inspect_asset_catalog"],"effects":["launches_process"],"limitations":[],"available":false,"reason":"Apple asset catalogs require macOS assetutil.","availability_code":"unsupported_host"}]
```

REA capability result identified package/server `6.7.0`; the result had `open:false` (no target opened). The operation group reports both names `available:true`, with `reason:null` and `availability_code:null`.

## Doctor / active-client qualification
I also ran `"$HOME/.npm/_npx/9b9809298fe40d2c/node_modules/.bin/rea" doctor --json`; it exited 1 because its audit result was `healthy:false`. Relevant exact output excerpts:
```json
"live_server":{"state":"unknown","remediation":"Call binary_session in the active client to inspect the running server identity."}
{"client":"kimi","config_path":"/home/vgpnk/.kimi-code/mcp.json","command":[],"state":"missing","remediation":"Run rea setup to refresh this registration, then restart the client."}
```

## Verdicts
- `inspect_artifact` availability — **VERIFIED** for the measured REA 6.7.0 CLI capability session (`rea-artifact-graph` group above).
- `extract_artifact` availability — **VERIFIED** for the same measured session.
- Active Kimi MCP server identity/availability — **UNVERIFIABLE** from this seat: no `binary_session` tool was exposed, and doctor reported `live_server.state:"unknown"` plus a missing Kimi registration. Do not infer active-agent MCP availability from the CLI result.

No target was opened or extracted. No REA/client configuration or tracked project file was changed; this report is the seat artifact only.
