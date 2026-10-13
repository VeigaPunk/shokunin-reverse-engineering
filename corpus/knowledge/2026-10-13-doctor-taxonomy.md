<!-- corpus entry — kaidoku-shokunin round 1 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r1/03-rea-doctor.md. Each candidate's `suggested:` field is its curation verdict; `reject` rows are retained calibration entries. -->

# kaidoku-r1 — `rea doctor` taxonomy and host health state (rea-agents@6.4.0)

Probing method: `npx -y rea-agents@6.4.0 doctor --json` (exit 1) plus `doctor --help`,
default `--format toon` and `--format md` runs, and source reads of the installed
package at `~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/dist/application/
{Doctor,DoctorDiagnostics,DoctorScope,SetupSkill,SupportedClients,ClientRegistrationStatus}.js`.
`rea` does not resolve on this host's PATH (`which rea` → not found); the only
`rea` binary is the npx cache entry the doctor itself reports. The `rea doctor`
half of the task is therefore documented as N/A rather than run.

## Candidate: `rea` CLI is absent from PATH; npx is the only invocation route
- claim: `which rea` finds nothing in this host's PATH; `doctor` reports `identity.installations.paths = ["/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/.bin/rea"]` with `state: "single"` — i.e., the only installed `rea` executable is the npx cache shim, so `rea doctor` cannot be run directly and `npx -y rea-agents@6.4.0 doctor` is the canonical equivalent.
- source: `which rea` (exit 1); `npx -y rea-agents@6.4.0 doctor --json` → `.identity.installations`
- verify: `which rea; npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).identity.installations))'`
- verified-at: 2026-10-13
- suggested: admit — both halves observed directly on this host.

## Candidate: Doctor emits a fixed top-level envelope; `checks` and `scope_checks` are identical in audit-wide mode
- claim: `doctor --json` returns exactly 8 top-level keys — `healthy`, `environment_healthy`, `scope`, `scope_checks`, `informational_checks`, `providerInspections`, `checks`, `identity`. With no scope flags the scope is `{"mode":"audit-wide","clients":[],"providers":[],"skill":false,"target":null}`, `scope_checks` is byte-identical to `checks` (same 18-element array), and `informational_checks` is empty; scoping flags (`--client`, `--provider`, `--skill`, `--target`) would split checks into required (`scope_checks`) vs advisory (`informational_checks`) and recompute `healthy` against the selection only, while `environment_healthy` always reports the unscoped verdict.
- source: `npx -y rea-agents@6.4.0 doctor --json`; `dist/application/Doctor.js` `runDoctor` (`healthy: scope.mode === "audit-wide" ? environmentHealthy : scoped.healthy`); `doctor --help` option list
- verify: `npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log(Object.keys(j), JSON.stringify(j.checks)===JSON.stringify(j.scope_checks))})'`
- verified-at: 2026-10-13
- suggested: admit — structure observed in output and confirmed against `runDoctor` source.

## Candidate: Check classification taxonomy is a 5-class verdict label
- claim: Every check carries `name`, `ok`, and a `classification` drawn from `healthy | missing_dependency | unsupported_host | missing_analysis_engine | config_drift` (observed in source: `missing_dependency` for node, `unsupported_host` for host, `missing_analysis_engine` for hopper/ida engines, `config_drift` for skill/registrations and ghidra sub-checks). In `scope_checks` the classification describes the actual outcome; inside `providerInspections[].checks` the classification on a *passing* check instead names which failure class a failure would map to (all ghidra checks show `ok:true` yet carry `config_drift`/`unsupported_host` labels).
- source: `dist/application/DoctorDiagnostics.js` (check constructors); doctor `--json` `providerInspections[0].checks` (all `ok:true` with non-`healthy` classifications)
- verify: `npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log([...new Set(j.checks.map(c=>c.classification))]);console.log(j.providerInspections[0].checks.map(c=>c.ok+"/"+c.classification))})'`
- verified-at: 2026-10-13
- suggested: admit — the dual meaning of `classification` (outcome vs. would-be failure class) is directly visible in the ghidra block and explains an otherwise confusing field.

## Candidate: This host's `environment_healthy=false` is caused by exactly 6 core `config_drift` checks — not by the missing engines
- claim: `doctorHealthy` (`dist/application/DoctorDiagnostics.js`) computes environment health as: all non-provider checks ok AND all checks belonging to *configured* providers ok AND at least one deep-analysis provider available (`hopperAvailable || providerInspections.some(available)`). On this host the `hopper` and `ida-registration` failures are excluded from the verdict because neither provider is configured, and ghidra satisfies the ≥1-available rule — so the unhealthy verdict comes solely from `skill:identity` plus `registration:{claude_code, codex, grok_build, opencode, pi}` (6 `config_drift` core checks). Provider check names match via `name === id || name.startsWith(id+"-")`.
- source: `dist/application/DoctorDiagnostics.js` lines 33-51 (`doctorHealthy`) and 153 (`providerCheckName`); doctor `--json` (`hopper`/`ida-registration` ok=false while ghidra `available:true`)
- verify: `npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log(j.checks.filter(c=>!c.ok).map(c=>c.name+":"+c.classification))})'`
- verified-at: 2026-10-13
- suggested: admit — mechanism confirmed in source; explains why two `missing_analysis_engine` failures do not dominate the verdict.

## Candidate: Full 18-check list on this host — 10 pass, 8 fail
- claim: Audit-wide `checks` on this host, in order: `node` ok (24.21.0); `host` ok ("arch unknown"); `hopper` FAIL missing_analysis_engine; `ghidra` ok (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`); `ghidra-platform` ok (linux); `ghidra-architecture` ok (x64); `ghidra-installation` ok (`Ghidra/application.properties`); `ghidra-version` ok (12.1.4); `ghidra-headless` ok (`support/analyzeHeadless`); `ghidra-native_decompiler` ok (`Ghidra/Features/Decompiler/os/linux_x86_64/decompile` reports elf x86_64 matching linux/x64); `ghidra-java` ok (21.0.12.1, 64-bit JDK, `/usr/lib/jvm/java-21-openjdk`, "accepted a 64-bit full JDK 21 or newer"); `ida-registration` FAIL missing_analysis_engine; `skill:identity` FAIL config_drift; `registration:claude_code` FAIL (`~/.claude.json`); `registration:codex` FAIL (`~/.codex/config.toml`); `registration:grok_build` FAIL (`~/.grok/config.toml`); `registration:opencode` FAIL (`~/.config/opencode/opencode.json`); `registration:pi` FAIL (`~/.pi/agent/mcp.json`) — all registration failures are `config_drift` with remediation "Run rea setup to refresh this registration, then restart the client."
- source: `npx -y rea-agents@6.4.0 doctor --json` → `.checks` (also `--format md` table)
- verify: `npx -y rea-agents@6.4.0 doctor --format md | sed -n '/## scope_checks/,/## informational_checks/p'`
- verified-at: 2026-10-13
- suggested: admit — verbatim enumeration of the 18-check output on this host.

## Candidate: Ghidra provider passes all 8 deep inspections — the host's one ready analysis engine
- claim: `providerInspections[0]` (id `ghidra`) reports `configured:true, available:true, providerVersion:"12.1.4"`, registration env `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` and `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`, and 8/8 checks ok: `configuration` (install dir resolves), `platform` (linux), `architecture` (x64), `installation` (`application.properties` present → real install, not a bare dir), `version` (12.1.4), `headless` (`support/analyzeHeadless` executable present), `native_decompiler` (`decompile` binary self-reports `elf x86_64` matching host linux/x64), `java` (JDK 21.0.12.1 64-bit accepted; requirement is "64-bit full JDK 21 or newer").
- source: doctor `--json` → `.providerInspections[0]`; `dist/application/DoctorDiagnostics.js` ghidra check construction
- verify: `test -x /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/support/analyzeHeadless && /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/linux_x86_64/decompile -v 2>&1 | head -3; $JAVA_HOME/bin/java -version 2>&1 | head -2`
- verified-at: 2026-10-13
- suggested: admit — all eight sub-checks green; Ghidra is the only configured+available provider, which is what keeps the ≥1-engine floor satisfied.

## Candidate: Hopper check fails as `missing_analysis_engine`; three probe paths plus env override
- claim: `hopper` check fails with remediation "Run rea setup to install Hopper, or set HOPPER_LAUNCHER_PATH." Source shows the search order when `HOPPER_LAUNCHER_PATH` is unset: macOS default `/Applications/Hopper Disassembler.app/Contents/MacOS/hopper`, system Linux `/opt/hopper/bin/Hopper`, a per-user launcher path, then manual paths — none exist on this host. Because hopper is unconfigured its failure is excluded from `environment_healthy` (candidate above); on Linux a found hopper would additionally trigger `hopper-version` (supported-build check, class `config_drift`) and a `hopper-demo` check.
- source: `dist/application/DoctorDiagnostics.js` lines 3-9, 75-131 (`DEFAULT_HOPPER`, `SYSTEM_LINUX_HOPPER`, `linuxHopperLauncherPath`, `optionalHopperVersionCheck`, `optionalHopperDemoCheck`)
- verify: `ls /opt/hopper/bin/Hopper ~/Applications 2>&1; echo "$HOPPER_LAUNCHER_PATH"; npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).checks.find(c=>c.name==="hopper")))'`
- verified-at: 2026-10-13
- suggested: admit — absence confirmed on host; conditional sub-checks documented from source (they cannot fire here).

## Candidate: IDA provider is unconfigured (`REA_IDA_MCP_CONFIG` unset); single registration check
- claim: `providerInspections[1]` (id `ida`) reports `configured:false, available:false` with one check `registration` failing `code:"not_configured"`, `missing_analysis_engine`; remediation points to env var `REA_IDA_MCP_CONFIG` holding an upstream IDA MCP registration JSON (`docs/ida-provider.md`). This surfaces in the flat list as `ida-registration`.
- source: doctor `--json` → `.providerInspections[1]` and `.checks` `ida-registration`
- verify: `echo "REA_IDA_MCP_CONFIG=$REA_IDA_MCP_CONFIG"; npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).providerInspections[1]))'`
- verified-at: 2026-10-13
- suggested: admit — env var unset and check output observed.

## Candidate: Registration matrix — 8 known clients; `devin` and `omp` aligned, `grok_bot` manual-exempt, 5 missing
- claim: `identity.registrations` lists 8 clients. `devin` (`~/.config/devin/mcp_config.json`) and `omp` (`~/.omp/agent/mcp.json`) are `state:"aligned"` with command `["npx","-y","rea-agents@6.4.0","mcp"]`. `grok_bot` is `state:"manual"` — connectors live in the signed-in hosted account, setup cannot write it, and manual-state registrations are exempted from the failing-check list (`registration.state !== "aligned" && !== "manual"` filter in `collectDoctorIdentity`). The other five are `state:"missing"` and each produces a `registration:<client>` config_drift check.
- source: doctor `--json` → `.identity.registrations`; `dist/application/Doctor.js` `collectDoctorIdentity` filter
- verify: `node -e 'const fs=require("fs");for(const p of ["/home/vgpnk/.config/devin/mcp_config.json","/home/vgpnk/.omp/agent/mcp.json"]){try{console.log(p,fs.readFileSync(p,"utf8").includes("rea-agents"))}catch(e){console.log(p,"unreadable")}}'`
- verified-at: 2026-10-13
- suggested: admit — both aligned entries verified against the actual client config paths.

## Candidate: `skill:identity` is `stale` despite a byte-identical installed skill — the gap is the claude_code destination, not content drift
- claim: `identity.skill` reports `installed_version:"37"`, `installed_tool_count:170`, `state:"stale"`. Yet `diff -r` shows the installed `~/.agents/skills/reverse-engineer-anything/` is byte-identical to the bundled `skills/reverse-engineer-anything/` in rea-agents@6.4.0 (all 7 managed files). Alignment requires `version===expected && toolCount===170 && canonical`; `canonical` is computed across *every registered client's* skill destination — clients without a `skillPath` fall back to shared `~/.agents/skills`, but `claude_code` maps to `~/.claude/skills`, where `reverse-engineer-anything/` is absent on this host. One missing per-client copy flips `canonical` to false → `stale`, even though the readable skill content is current.
- source: `dist/application/Doctor.js` (`skillIdentityAligned`), `SetupSkill.js` (`MANAGED_SKILL_FILES`, `canonicalSkillNeedsInstall`), `SupportedClients.js` (`clientSkillDirectories`: claude_code → `~/.claude/skills`, others → `~/.agents/skills`); `diff -rq ~/.agents/skills/reverse-engineer-anything <pkg>/skills/reverse-engineer-anything` (no output); `ls ~/.claude/skills/` (only `omarchy` symlink)
- verify: `diff -rq ~/.agents/skills/reverse-engineer-anything ~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/skills/reverse-engineer-anything; ls ~/.claude/skills/reverse-engineer-anything 2>&1`
- verified-at: 2026-10-13
- suggested: admit — the `stale`-despite-identical-content result is counterintuitive and fully explained by the per-client destination scan; high-value correction to the naive reading.

## Candidate: `healthy=false` ⇒ exit code 1; `--json` is a supported global format, not a doctor-specific flag
- claim: `npx -y rea-agents@6.4.0 doctor` exits 1 whenever `healthy` is false (both default toon and `--format md` runs exited 1 on this host); JSON output is obtained via `--json` shorthand or `--format json` from the universal global-option set (`toon|json|yaml|md|jsonl`). Doctor-specific options are only the four scoping flags: `--target`, `--client` (repeatable), `--provider` (repeatable, ids in `hopper|ghidra|ida` per `DOCTOR_PROVIDER_IDS`), `--skill`.
- source: `npx -y rea-agents@6.4.0 doctor > /dev/null; echo $?` → 1; `doctor --help`; `dist/application/Doctor.js` `DOCTOR_PROVIDER_IDS`
- verify: `npx -y rea-agents@6.4.0 doctor >/dev/null 2>&1; echo $?; npx -y rea-agents@6.4.0 doctor --help | sed -n '/^Options:/,/Global Options/p'`
- verified-at: 2026-10-13
- suggested: admit — exit code observed directly; scripting note: a failing doctor is still a successful diagnostic.

## Candidate: `host` check passes with detail "arch unknown" — Arch Linux supported despite missing VERSION_ID
- claim: The `host` check detail string is `${distribution.id} ${distribution.versionId ?? "unknown"}`; this host is Arch (`os-release` ID=arch, no VERSION_ID) → "arch unknown". Support verdict comes from `linuxDistribution.supported === true` (supported set per remediation: macOS 12+, Ubuntu 24.04+, Fedora 41+, Nobara 44+, 64-bit Arch, CachyOS, Omarchy, experimental Windows x64 Ghidra P0 boundary).
- source: `dist/application/DoctorDiagnostics.js` `hostCheck` (lines ~57-70); doctor `--json` `host` detail "arch unknown"; host is Omarchy/Arch (`~/.local/share/omarchy` present, PATH contains omarchy bin)
- verify: `cat /etc/os-release | head -4; npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).checks.find(c=>c.name==="host")))'`
- verified-at: 2026-10-13
- suggested: admit — explains the odd "arch unknown" detail string as a formatting artifact, not a failed probe.

## Candidate: `identity` block pins version/catalog fingerprints for drift detection
- claim: `identity` carries `cli_package_version:"6.4.0"`, `expected_skill_version:37`, `sdk:{server,client_test,core}:"2.3.1"`, `catalog.counts:{cli_commands:127, mcp_tools:170, mcp_prompts:6}`, `catalog.digests` (tools_sha256 `25802f6d…`, prompts_sha256 `5296f030…`, combined `85d80276…`), `live_server.state:"unknown"` (CLI cannot see a running MCP server; remediation says call `binary_session` in the active client), and `installations.state:"single"`. Digests + skill metadata give agents a tamper/staleness fingerprint independent of version strings.
- source: doctor `--json` → `.identity`; `dist/application/Doctor.js` `collectDoctorIdentity`
- verify: `npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const i=JSON.parse(s).identity;console.log(i.cli_package_version,i.expected_skill_version,i.catalog.counts,i.catalog.digests.combined_sha256)})'`
- verified-at: 2026-10-13
- suggested: admit — verbatim values; combined digest is the version-pinned fingerprint worth citing in later rounds.

## Candidate (rejected reading): "`rea` can be invoked directly / doctor must be run via a global install"
- claim: `rea doctor` is runnable on this host because the doctor reports an installation path.
- source: `identity.installations.paths` vs `which rea`
- verify: `which rea || echo NOT-ON-PATH; ls -la /home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/.bin/rea`
- verified-at: 2026-10-13
- suggested: reject — the reported path is the npx cache `.bin` shim, not a PATH member; `which rea` fails. The installation record proves the package ran, not that a global CLI exists.

## Candidate (rejected reading): "The missing Hopper/IDA engines are what make the host unhealthy"
- claim: `environment_healthy:false` is caused by the `missing_analysis_engine` failures.
- source: `dist/application/DoctorDiagnostics.js` `doctorHealthy`; doctor `--json`
- verify: `npx -y rea-agents@6.4.0 doctor --json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log(j.checks.filter(c=>!c.ok&&c.classification!=="missing_analysis_engine").length,"non-engine failures")})'`
- verified-at: 2026-10-13
- suggested: reject — unconfigured-provider checks are excluded from the verdict; the 6 `config_drift` core checks (skill + 5 registrations) are the actual cause, and ghidra alone satisfies the engine floor.

## Summary
`rea doctor` on this host: healthy=false / environment_healthy=false (exit 1), driven solely by 6 core `config_drift` checks — a stale-flagged skill identity (actually a missing `~/.claude/skills` destination; the shared `~/.agents/skills` copy is byte-identical v37/170) and 5 missing client registrations — while Ghidra 12.1.4 + JDK 21 passes all 8 provider inspections as the sole ready analysis engine, Hopper and IDA are absent-but-unconfigured, and devin/omp registrations are aligned.

## Errata (round 2)

- Verify line `decompile -v` emits no output (exit 1); the native-decompiler fact is
  confirmed via `file` on the binary instead — replace that verify command. (audit-A)
