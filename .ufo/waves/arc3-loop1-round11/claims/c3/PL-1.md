# PL-1 — C3 live availability re-probe

**Conclusion: REPRODUCED at provider-capability scope; DISCREPANCY at empty-session tool-readiness scope.** The artifact provider reports `available:true` for `inspect_artifact`/`extract_artifact`, while the same `binary_session {}` response marks each tool `available:false` with `reason:"target_required"` because no binary is open. The distinction is material: the provider is present, but neither operation is ready to run until a supported target is opened.

## First-hand measurement

- At `2026-10-19T16:25:45-03:00`, launched the public REA 6.7.0 stdio executable (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/.bin/rea mcp`) with the MCP SDK `Client`/`StdioClientTransport` and called `binary_session` with `arguments: {}`. Server identity in the returned response: `rea@6.7.0`; the response had `open:false` and `cleanup_pending:false`.
- Selected raw response values are in [PL-1/binary-session-excerpt.json](PL-1/binary-session-excerpt.json). The original command-output log SHA-256 is `852a0257eb5e1265a5d831d76f592246da57d2582c400919ed53c648af174b0a`; relevant raw output lines: provider group `79-114`, `extract_artifact` tool gate `1678-1694`, and `inspect_artifact` tool gate `1947-1965` (raw log: `/home/vgpnk/.kimi-code/sessions/wd_shokunin_8c4a99c6228c/session_f33b1f06-8ec4-4bf9-9726-28a5a61545d1/agents/agent-811/tasks/bash-2kiwx979/output.log`).
- Exact provider group fields: `operations:["extract_artifact","inspect_artifact"]`, `available:true`, `reason:null`, `availability_code:null`.
- Exact per-tool availability for both names: `available:false`, `reason:"target_required"`, remediation `Call open_binary with a supported local target.` No target was supplied/opened, and neither artifact operation was invoked.

## Cross-checks and scope

- `npx -y rea-agents@6.7.0 mcp doctor --json --full-output` returned `healthy:true`, `adapter:"production-stdio"`, server `rea@6.7.0`, tool inventory `expected:207, observed:207, missing:[], unexpected:[], duplicates:[]`, and `request_flow:{tool:"binary_session",ok:true}`. This validates the fresh server/request path; it does not expose the tool-level availability fields, so the direct response above is the measurement.
- `npx -y rea-agents@6.7.0 doctor --client zcode --format json --full-output` exited 1: `registration:zcode` was `ok:false`, classification `config_drift`, detail `/home/vgpnk/.zcode/cli/config.json`; `live_server.state` was `unknown` with remediation to call `binary_session` in the active client. Thus this measurement is a directly launched REA 6.7.0 session, not proof that the parent Kimi/ZCode client is currently attached to REA. Active-client availability remains **UNVERIFIABLE**.
- No REA registration/configuration was repaired or edited. No artifact target was opened; the `extract_artifact` operation's filesystem effects were not exercised.

## Per-item verdicts

- **Provider capability (`inspect_artifact` + `extract_artifact`): REPRODUCED** — returned `available:true` for the shared `rea-artifact-graph` provider group.
- **Tool readiness in `binary_session {}` with no target: DISCREPANCY** with an unqualified reading of “available:true” — both tool entries are target-gated (`available:false`, `target_required`). This does not show provider failure; it shows the current session has no open artifact.
- **Parent Kimi/ZCode live-client session: UNVERIFIABLE** — ZCode registration missing/config-drift and doctor reports live server unknown.

**Disposition:** preserve the provider-level `available:true`, but qualify it as provider capability, not targetless tool-call readiness. To establish per-tool readiness for an actual artifact, a separately scoped `open_binary` on the intended supported target would be required; none was selected for this seat.