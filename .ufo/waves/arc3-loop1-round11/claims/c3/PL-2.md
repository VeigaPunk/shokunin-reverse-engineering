# PL-2 — C3 availability re-probe

**Verdict: REPRODUCED for the REA CLI capability scope; the attached Kimi MCP session remains unverified.**

## First-hand measurement

Ran the pinned REA CLI capability call:

```sh
npx -y rea-agents@6.7.0 capabilities --format json
```

The output identifies provider `rea-artifact-graph` (`REA safe artifact graph provider`, version `1`). Verbatim operation-group object from its `capabilities` array:

```json
{"operations":["extract_artifact","inspect_artifact"],"effects":["launches_process","may_write_filesystem"],"limitations":[],"available":true,"reason":null,"availability_code":null}
```

The same output's server identity reports package/server version `6.7.0`, `started_at` `2026-10-19T19:23:05.726Z`, and `client: null`. This is a positive, first-hand capability result for both operations from the CLI-created REA server context; neither operation itself was invoked.

## Session-scope limitation

Also ran `npx -y rea-agents@6.7.0 doctor --client kimi --json` (exit 1; health false). Its output reports `registration:kimi` as `ok:false`, `classification:"config_drift"`, at `/home/vgpnk/.kimi-code/mcp.json`, and reports `live_server.state:"unknown"` with remediation `Call binary_session in the active client to inspect the running server identity.` No `binary_session` tool was exposed in this seat. Therefore the CLI capability result reproduces `available:true`, but it does not establish that the current attached Kimi MCP session is connected or has the same advertised availability. I did not run setup or modify client configuration.

## Source and scope

The frozen C3 asks for a first-hand availability re-probe of `inspect_artifact`/`extract_artifact` (`.ufo/waves/arc3-loop1-round11/claims-frozen.md:43-54`). The recorded claim being checked is `.ufo/waves/arc3-loop1-round11`'s cited `PROVINCE.md:50` entry. No prior seat or round value was used as measurement evidence.
