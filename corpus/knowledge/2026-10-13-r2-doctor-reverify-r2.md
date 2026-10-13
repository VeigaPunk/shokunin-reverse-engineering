<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/15-doctor-fresh.md. -->

# kaidoku-r2 — freshness re-verification of r1 drift-sensitive pins (rea-agents@6.4.0)

Registry refresh: every value below was re-probed live on 2026-10-13 against the
r1 records (`kaidoku-r1/03-rea-doctor.md`, `04-mcp-config.md`, `10-rea-live.md`,
`corpus/lessons/2026-10-13-round-1.md`). Probe: `npx -y rea-agents@6.4.0 doctor
--json` (full output captured to scratch `/tmp/r2-doctor.json` and field-parsed).

## Check: doctor JSON envelope
- expected (r1): 8 top-level keys (`healthy`, `environment_healthy`, `scope`, `scope_checks`, `informational_checks`, `providerInspections`, `checks`, `identity`); audit-wide scope; `scope_checks` byte-identical to `checks`; `informational_checks` empty.
- observed (r2): identical — same 8 keys, `scope.mode:"audit-wide"`, `scope_checks===checks` true, `informational_checks` length 0.
- verdict: unchanged

## Check: check roster, count, and classifications
- expected (r1): exactly 18 checks, 10 pass / 8 fail; failures `hopper:missing_analysis_engine`, `ida-registration:missing_analysis_engine`, `skill:identity:config_drift`, `registration:{claude_code,codex,grok_build,opencode,pi}:config_drift`.
- observed (r2): 18 checks, identical order, identical `ok` flags, identical classification strings and remediation text; same 8 failures.
- verdict: unchanged

## Check: catalog digests + counts (the pinned fingerprint)
- expected (r1): `tools_sha256 25802f6d…`, `prompts_sha256 5296f030…`, `combined_sha256 85d80276…`; counts `{cli_commands:127, mcp_tools:170, mcp_prompts:6}`.
- observed (r2): `tools_sha256 25802f6de8c14ba736dc61ff1cbc7c5cd738fd74426aa01338f2dd03e0911166`, `prompts_sha256 5296f0301566cadaf89243e774512011f11045af36d48405f76a3ff9a8947ac2`, `combined_sha256 85d80276ecacf937bf3e803b7a31748ae1a8286f556fa5cf734eef768cc7d72a`; counts `{127,170,6}`.
- verdict: unchanged

## Check: identity versions and installation state
- expected (r1): `cli_package_version 6.4.0`, `expected_skill_version 37`, `sdk {server,client_test,core}: 2.3.1`, `live_server.state:"unknown"`, `installations.state:"single"` at `~/.npm/_npx/dea9475797100b20/…/.bin/rea`.
- observed (r2): all identical, same single npx-cache installation path.
- verdict: unchanged

## Check: skill identity state
- expected (r1): `installed_version:"37"`, `installed_tool_count:170`, `state:"stale"` (stale = missing `~/.claude/skills` destination, not content drift).
- observed (r2): identical triple `37/170/stale` with same remediation.
- verdict: unchanged

## Check: registration matrix (devin/omp alignment)
- expected (r1): 8 clients — `devin` + `omp` `state:"aligned"` with command `["npx","-y","rea-agents@6.4.0","mcp"]`; `grok_bot` `manual`; `claude_code`, `codex`, `grok_build`, `opencode`, `pi` `missing`.
- observed (r2): identical — devin and omp still aligned on the pinned npx command; same 5 missing + 1 manual.
- verdict: unchanged

## Check: provider inspections and health verdict
- expected (r1): ghidra `configured:true, available:true, providerVersion:"12.1.4"`, 8/8 sub-checks ok; ida unconfigured (`not_configured`); `healthy:false`/`environment_healthy:false` → exit 1; node `24.21.0`; host `arch unknown`; ghidra-java `21.0.12.1`.
- observed (r2): identical on every field, including all detail strings.
- verdict: unchanged

## Check: env wiring in client registrations
- expected (r1): `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` + `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` present in `~/.config/devin/mcp_config.json` (lines 11-12), `~/.omp/agent/mcp.json` (lines 12-13), `~/.kimi-code/config.toml` (lines 1290-1291).
- observed (r2): `grep -rn` hits the same two vars at the same paths — devin lines 11-12, omp lines 12-13, kimi TOML lines 1290-1291; values identical.
- verdict: unchanged

## Check: package version and npx caches
- expected (r1): `npm view rea-agents version` → `6.4.0`; two npx caches `af752b90495482d7` (`@latest` key) and `dea9475797100b20` (`@6.4.0` key), both materialized at 6.4.0.
- observed (r2): `npm view` → `6.4.0`; same two cache dirs both at 6.4.0; no third cache appeared despite this round's `npx` run.
- verdict: unchanged

## Check: `/tmp/rea-ghidra-*` session dirs (orphans)
- expected (r1): zero orphaned session dirs post-wave (`corpus/lessons/2026-10-13-round-1.md`: shared namespace; a concurrent `rea mcp` held live dir `rea-ghidra-RqxIxo` during r1).
- observed (r2): zero orphans, but active churn — three snapshots ~60s apart caught `2ryngu` → `tf9qMo` → `kfMwyc`/`tf9qMo`/`rSmZL0` rotating; every inspected dir has fresh `session.json`/`ownership.json` (created_at within the minute, `ownership_kind:"posix-process-group"`) and a live owner (PID 42863 = `analyzeHeadless` bound to `rea-ghidra-kfMwyc`). A persistent `rea mcp` server (PIDs 4474/4495, up since 11:10) plus sibling-lane analyses are the source; distinct `target_sha256` per session.
- verdict: unchanged (orphan count still 0; live-session presence is expected concurrent use, recorded not cleaned)

## Summary
No drift on any pinned value: the doctor envelope, all 18 checks with their
classifications, both catalog digests (`combined_sha256 85d80276…` intact), skill
identity (`37/170/stale`), the 8-client registration matrix (devin+omp aligned),
all three env-wiring sites, the 6.4.0 version pin (registry + both npx caches),
and the zero-orphan session state are byte-for-byte identical to round 1.

DRIFT entries: none.

Observational note (not drift): `/tmp/rea-ghidra-*` is actively churning right
now — live `analyzeHeadless` sessions from the persistent `rea mcp` server
(PID 4495) and/or sibling round-2 lanes. Dirs are owned (posix-process-group,
fresh mtimes) and self-clean on close; none qualify as orphans. Shared
namespace — recorded only, untouched.
