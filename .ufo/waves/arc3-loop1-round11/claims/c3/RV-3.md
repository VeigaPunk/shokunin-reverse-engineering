# RV-3 — c3 availability re-probe

Date: 2026-10-19  
Verdict: **UNVERIFIABLE** for the session-scoped `inspect_artifact` / `extract_artifact` availability claim.

## Target and method

The claim to re-derive is the `available:true` class in `PROVINCE.md:50`; the frozen c3 requirement calls for a live `binary_session {}` or `rea doctor`/capability result (`.ufo/waves/arc3-loop1-round11/claims-frozen.md:43-54`). No `binary_session` REA tool was exposed in this seat's tool set, and `rea` was not on `PATH`; `npx` was available. I therefore ran the pinned CLI doctor without changing registrations or configuration:

```text
$ npx -y rea-agents@6.7.0 doctor --client codex --json
exit status: 1
```

Exact relevant output fields:

```json
{
  "scope": {"mode":"explicit","clients":["codex"],"providers":[],"skill":false,"target":null},
  "scope_checks": [
    {"name":"node","ok":true,"classification":"healthy","detail":"26.12.0","details":{"runtime":"node","version":"26.12.0"}},
    {"name":"registration:codex","ok":false,"classification":"config_drift","detail":"/home/vgpnk/.codex/config.toml","remediation":"Run rea setup to refresh this registration, then restart the client."}
  ],
  "live_server": {
    "state":"unknown",
    "remediation":"Call binary_session in the active client to inspect the running server identity."
  },
  "identity": {
    "cli_package_version":"6.7.0",
    "catalog":{"counts":{"cli_commands":153,"mcp_tools":207,"mcp_prompts":6}}
  }
}
```

## Finding

The doctor re-probed the local Codex registration and reports it as `config_drift`; it cannot identify the active REA server (`live_server.state` is `unknown`). The package-wide count of 207 MCP tools is not an operation-level availability result and does not show whether `inspect_artifact` or `extract_artifact` is available in the live session. Therefore this run neither reproduces nor falsifies the prior session's `available:true` value: the calibration target remains **UNVERIFIABLE**. A live `binary_session {}` result from the connected client is still required.

No REA setup, registration edit, restart, or custody-file modification was performed. This note records the measured diagnostic and its boundary; it is not a claim that the earlier session did not have those capabilities.
