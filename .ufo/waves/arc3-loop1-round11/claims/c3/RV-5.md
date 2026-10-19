# RV-5 — C3 availability re-probe

## Verdict

- `inspect_artifact` — **REPRODUCED**: the fresh `rea-agents@6.7.0` CLI capability response lists it in an `available:true` group.
- `extract_artifact` — **REPRODUCED**: the same response lists it in that `available:true` group.
- Already-running agent MCP session — **UNVERIFIABLE**: this is a live capability result from the CLI server started by the command, not a `binary_session {}` response from that separate session. Do not promote it to proof about that session.

## First-hand measurement

Command: `npx -y rea-agents@6.7.0 capabilities --format json`

Selected exact stdout fields:

```json
{"provider":{"id":"rea-artifact-graph","name":"REA safe artifact graph provider","version":"1"},"groups":[{"operations":["decode_interface_builder","inspect_keyed_archive","trace_dylib_resolution"],"effects":[],"limitations":[],"available":true,"reason":null,"availability_code":null},{"operations":["extract_artifact","inspect_artifact"],"effects":["launches_process","may_write_filesystem"],"limitations":[],"available":true,"reason":null,"availability_code":null},{"operations":["inspect_asset_catalog"],"effects":["launches_process"],"limitations":[],"available":false,"reason":"Apple asset catalogs require macOS assetutil.","availability_code":"unsupported_host"}]}
```

The same stdout identifies `server_identity.package.name=rea-agents`, `package.version=6.7.0`, `server.version=6.7.0`, and `server.started_at=2026-10-19T19:22:30.032Z`; top-level `open=false` (no artifact open). The command completed successfully.

## Active-session boundary

A separate `npx -y rea-agents@6.7.0 doctor --client kimi --format json` returned exit 1. Its stdout reports `scope_checks` entry `registration:kimi` with `ok=false`, `classification=config_drift`, `detail=/home/vgpnk/.kimi-code/mcp.json`; `live_server.state=unknown`, with remediation “Call binary_session in the active client to inspect the running server identity.” Thus this doctor run does not establish the current agent's tool availability. No `binary_session` tool was exposed in this seat's tool list, so the original active-session claim remains **UNVERIFIABLE** here.

## Claim disposition

`PROVINCE.md:50`'s `inspect_artifact`/`extract_artifact` `available:true` class is **reproduced for a fresh 6.7.0 CLI capability session**, independently measured above. Whether those operations remain `available:true` in the already-running client session is **unverified**; the doctor output explicitly leaves the live server unknown. No configuration or custody path was changed.
