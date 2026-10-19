# RV-1 — C3 availability re-probe

## Claim and measurement

`PROVINCE.md:50` records `inspect_artifact` / `extract_artifact` as `available:true` in a live session. I attempted a fresh REA capability check with:

```text
npx -y rea-agents@6.7.0 doctor --json
```

There is no `rea` executable on this shell's PATH, so this used the package-pinned CLI. The exact relevant output fragments were:

```text
"live_server":{"state":"unknown","remediation":"Call binary_session in the active client to inspect the running server identity."}
{"client":"kimi","config_path":"/home/vgpnk/.kimi-code/mcp.json","command":[],"state":"missing","remediation":"Run rea setup to refresh this registration, then restart the client."}
```

The command exited with status 1 (`healthy:false`). The current agent's exposed tools do not include `binary_session`, and the doctor output provides no per-tool availability entries for `inspect_artifact` or `extract_artifact`.

## Verdict

**UNVERIFIABLE** — this probe did not establish either current availability or unavailability of the two session tools. It establishes only that REA's doctor could not identify a live server (`live_server.state = unknown`) and diagnosed the Kimi MCP registration as missing. I made no registration/configuration changes; a `binary_session {}` result from a connected REA session is still required to resolve the original claim.
