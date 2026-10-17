## CLAIM

L3 of the pre-registered battery reproduces on lane B: `inspect_go_binary` on the Lane-A carrier `/usr/bin/docker` (per SC1) returns a complete RESULT-class dossier, and the carrier identity matches SC1 byte-for-byte.

## METHOD

Carrier identity first (read-only): `file` + `sha256sum /usr/bin/docker` → `70f68a77…45c9`, identical to SC1.md. Probe from /tmp only: `cd /tmp/rea-bb3 && node probe-leg3.mjs` — a stdio MCP client spawning `npx -y rea-agents@6.5.0 --mcp`, sending initialize (protocolVersion 2025-03-26) → notifications/initialized → tools/call id=2 `inspect_go_binary {"path":"/usr/bin/docker"}`, then closing stdin to terminate; 240s budget, wall 1.804s. Full command, verbatim transcript, stderr, exit code, and stdout sha256 are in `receipts-B/leg-3.md`. The lane-A leg-3 receipt was deliberately not read.

## FINDINGS

- Probe: exit 0; stdout 12,904 B, sha256 `75b83edf…4d01`; stderr empty (sha256 `e3b0c442…b855`); graceful termination (`forced_termination=false`), no lingering processes. Server log: `status:"ok","durationMs":27.95`.
- Result (evidence `ev_671861638ed7fe54…a4b`): subject digest = carrier sha256; `go_version` `go1.26.5-X:nodwarf5`; module `github.com/docker/cli/cmd/docker`, `module.complete=true`; settings GOOS=linux, GOARCH=amd64, CGO_ENABLED=1; provider `go-build-info` v1; confidence `observed`; authority `shipped-artifact`; locations file-offset-range [28873984, 28874016].
- Outcome class RESULT → MATCH against the frozen L3 prediction (RESULT). No typed refusal, no unexpected error.

## THREATS

- Go attribution derives from embedded build metadata (observed file content), not runtime identity — REA's own stated limitation.
- Concurrent seats were active on this host during the probe (other seats' MCP servers and npx version probes visible in /tmp); no interference appears in this transcript, and their processes were not touched.
- npx resolved from local cache (server initialized in ~0.64s); this leg measures e2e operability, not network freshness (other legs' scope).
- The probe client is my own script; stdout was captured by redirection and sha256-pinned, so the receipt is independently verifiable.

## VERDICT

CLEAN — L3 reproduces as RESULT class on lane B; 1/1 predicted class matched; carrier hash identical to SC1.
