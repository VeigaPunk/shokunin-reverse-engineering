# kaidoku-shokunin — Province

**Domain:** reverse engineering of shipped artifacts with REA on this Linux
host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript
bundles, archives and packages; evidence-first static analysis that keeps
observation, inference and unknowns separate.

Surface summary: the `rea` MCP server (stdio, `npx -y rea-agents@6.4.0 mcp`,
170 MCP tools + 127 CLI commands, catalog tools_sha256 `25802f6d…`) plus its
`rea` CLI; the Ghidra provider at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`;
host binutils as non-REA fallback readers.

Drift-prone values: `GHIDRA_INSTALL_DIR` and `JAVA_HOME` in
`~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json`, and
`~/.kimi-code/config.toml`; the pinned `rea-agents@6.4.0` version; the installed
REA skill version (v37 — `rea doctor` reports `skill: stale` because the
per-client `claude_code` destination `~/.claude/skills/` is absent, not because
the shared copy drifted); Ghidra's own `application.version`; unset provider
env keys (`REA_IDA_MCP_CONFIG`, `REA_PWNTOOLS_PYTHON`, `HOPPER_LAUNCHER_PATH`).

Probe/reconciliation conventions: `rea doctor` is the environment verdict;
`binary_session {}` is the live-server verdict (`result.tool_availability` +
provider candidates); a catalog-listed tool is *available*, not *held* —
ground moves to Core only after an end-to-end probe lands a `LOG.md` entry
citing its `evidence_id` and subject sha256. The domain is a frontier, not a
fence: it grows by evidence (LEARNING.md).

## Core

Surfaces owned now — each verified on this host 2026-10-13.

| Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |
|---|---|---|---|
| REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml:1285` — all spawn `npx -y rea-agents@6.4.0 mcp` with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` in an attached client → `analysis_provider_candidates` + `capabilities[]`; CLI: `rea doctor` (devin `aligned`, omp `aligned`) | doctor run 2026-10-13; wave 04 file-level verification |
| `rea` CLI | npx cache `~/.npm/_npx/*/node_modules/rea-agents` — no `rea` on PATH; 127 commands | `npx -y rea-agents@6.4.0 --version` → `6.4.0` | wave 01/02/03 catalogs |
| Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 35 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
| JDK 21 substrate | `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`, exported in `.bashrc:24` + `.profile:4`; sole Java on host | `java -version` → 21.0.12.1 full JDK | meets Ghidra `java.min=21` exactly; single-Java fragility noted |
| Native ELF via Ghidra | `rea analyze/search/decompile <path>`; sessions `mkdtemp /tmp/rea-ghidra-*`, `-readOnly -deleteProject`, self-cleaning | `rea analyze <elf>` → overview + procedure inventory | `/usr/bin/jq`: 30 segments, 167 procedures, 190 strings, ~5.5s; `decompile 0x103fa0` recovered `process()` loop |
| Electron/ASAR/JavaScript | `analyze_javascript_application` on `.asar` or extracted tree; `inspect_analysis_view` paging; 6 asar archives on host (obsidian ×2, signal, 1Password, electron39/43 stubs) | `analyze_javascript_application` `detail:"summary"` on a small asar | `default_app.asar` (electron43) → 5 files, 41 findings, evidence `ev_2628de89…` |
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
| Evidence discipline | `detail:"summary"` + `parent_evidence_id` paging; `get_evidence_bundle` filters; `inspect-evidence-bundle`; `--snapshot <path>` JSON bundle | every Core probe emits `evidence_id` + `limitations[]`/`unknowns[]` | snapshot is evidence persistence, not a Ghidra DB cache (timed) |
| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |

Cross-lane registry this lane maintains: the REA surface map — per-client
registration state, provider availability, provider env keys, and the on-host
artifact inventory — kept in `corpus/knowledge/`, refreshed by `rea doctor`
each round.

## Frontier

Claimed in MINT.md, not yet held. Each moves to Core by a `LOG.md` entry citing
the corpus entries that earned it.

- **PE binaries under this Linux host** — 413 PE files exist locally (Godot
  export templates, setuptools launchers, dotnet assemblies); Ghidra's
  `PeLoader` is pure-Java (wine-independent by construction — end-to-end
  import INFERRED, unprobed). First move: `open_binary` + overview on a real
  PE, e.g. a Godot `windows_release_x86_64.exe`.
- **Managed PE/CLI assemblies** — `inspect_managed_artifact` family reports
  `available:true` but rejected a real AnyCPU `Microsoft.*.dll` as
  `unsupported PE architecture`; no SDK/`ilspycmd`/Mono on host (Pinta's
  Mono.Cecil is a reader substrate but no compiler to build a harness).
- **Firmware images** — `inspect_firmware_regions` catalog-listed; real
  targets `/usr/lib/firmware/nvidia/610.57.04/*.bin`; `extract_firmware` needs
  absent Binwalk/Unblob (operator-owned prerequisite).
- **Recorded crashes** — `inspect_recorded_crash` catalog-listed, unprobed;
  174 zstd cores retained via `coredumpctl` (3 organic: godot, waybar,
  localsearch) with unprivileged ACL read + gdb/`eu-stack` path confirmed;
  retention decays oldest-first.
- **Offline ELF layout** — `inspect-binary-layout` fails
  `provider_unavailable`: needs `REA_PWNTOOLS_PYTHON` (pwntools 4.15.0 +
  pyelftools 0.33 + Unicorn 2.1.2); REA never installs Python.
- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
  JEB (unprobed). Engine installs are operator-owned.
- **Android APK** — `inspect_android_package` + adb family catalog-listed;
  apktool/jadx/adb presence and APK corpus unprobed.
- **Runtime observation** — `list_browser_targets`, `list_electron_targets`,
  `observe_javascript_runtime`, `capture_*_scenario`, HAR inspection:
  catalog-listed, need user-owned targets or caller-supplied captures.
- **Cross-version diffing** — `compare_application_versions`,
  `compare_bundles`, `compare_javascript_export_shapes`: catalog-listed; needs
  a two-version artifact pair (pacman cache already retains multi-version
  archives — e.g. `1password-cli` 2.34.1-1 + 2.40.0-2).
- **macOS-only surfaces** — Mach-O/plist/LLDB/asset-catalog ops report
  `unsupported_host` on Linux; recorded so the lane never claims them.
- **EVM bytecode** — `inspect_evm_interface` catalog-listed; no carrier probed.

## Adjacent

Ground the lane refuses or defers — reported to the orchestrator, never
absorbed.

- **Malware triage at scale** — verdict pipelines, sandbox detonation, bulk
  classification `(unowned)`. The lane analyzes declared, caller-supplied
  artifacts; it does not run a triage queue or label samples malicious/benign.
- **Non-REA dynamic analysis** — gdb scripting, strace/ltrace, unpacking by
  execution, Frida-style hooking `(unowned)`. gdb stays a fallback reader for
  supplied cores, not a lane-run tracer.
- **Source-available reconstruction of ordinary repositories** — REA's own
  anti-trigger `(unowned)`.
- **Installing engines, Python packages, or editing client configs** —
  `rea setup` runs, registration refreshes for `claude_code`/`codex`/
  `grok_build`/`opencode`/`pi` (all `missing` per doctor), installing
  Hopper/IDA/JADX/Binwalk/Unblob/pwntools/ilspycmd/.NET SDK — all
  **operator-owned**. The lane documents the gap and the exact env key; it
  never runs the installer.
- **Quality/safety verdicts on findings** — the lane answers "what does this
  shipped artifact do, per evidence id X" — never "is it safe, trustworthy, or
  licensed for reuse" `(unowned)`.
