# RV-6 — C3 availability re-probe

**Verdict: REPRODUCED at provider-capability scope; qualified at tool/session scope.** I re-derived the availability in a fresh local REA MCP stdio session; this was not an attached session of the current Kimi agent.

## First-hand measurement (2026-10-19)

Started the installed REA CLI at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/.bin/rea mcp`, initialized MCP protocol `2025-03-26` as `rv6-live-probe`, called `tools/list`, then `tools/call` with `name: "binary_session"` and `arguments: {}`. The returned server identity was REA `6.7.0`, started at `2026-10-19T19:23:35.192Z`; the session reported `open:false`, `cleanup_pending:false`. No target was opened and no extraction was run.

Exact selected output values from that response:

```text
tools/list: {"binary_session":true,"count":207,"extract_artifact":true,"inspect_artifact":true}
provider capability: {"group":{"availability_code":null,"available":true,"effects":["launches_process","may_write_filesystem"],"limitations":[],"operations":["extract_artifact","inspect_artifact"],"reason":null},"provider":{"id":"rea-artifact-graph","name":"REA safe artifact graph provider","version":"1"}}
per-tool availability: [{"annotations":["open_world"],"available":false,"effects":["mutatesSession","writesFilesystem","launchesProcess"],"names":["extract_artifact"],"reason":"target_required","remediation":"Call open_binary with a supported local target.","surface":"artifact-provider"},{"annotations":["idempotent","open_world"],"available":false,"effects":["mutatesSession","writesFilesystem","launchesProcess","idempotent"],"names":["inspect_artifact"],"reason":"target_required","remediation":"Call open_binary with a supported local target.","surface":"artifact-provider"}]
```

## Disposition

- The `rea-artifact-graph` capability group containing `inspect_artifact` and `extract_artifact` reports `available:true`, reproducing the dated provider-capability value in `PROVINCE.md:50` (whose survey scope is dated at `PROVINCE.md:40`).
- The same `binary_session {}` reports both exact tools as `available:false` in `tool_availability`, with `reason:"target_required"`; the capability group and per-tool readiness are different scopes. Neither tool is callable against a target until `open_binary` selects one. Thus the unqualified phrase `available:true` is not an accurate description of per-tool availability in this targetless session.
- The active Kimi-agent connection remains **UNVERIFIABLE**: `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/.bin/rea doctor --client kimi --json` returned `registration:kimi` `ok:false`, `classification:"config_drift"`, detail `/home/vgpnk/.kimi-code/mcp.json`; its `live_server.state` is `unknown`. I did not repair registration or claim the separate stdio probe was the active agent's server.

No REA Evidence ID is produced by this capability query. No configuration, corpus, or other wave artifact was changed.
