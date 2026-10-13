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
| Native PE via Ghidra | `rea analyze/search/decompile <pe>` — pure-Java `PeLoader`, wine-independent | `rea analyze <pe>` → segments/procedures | `cli-64.exe` (sha256 `bbb3de57…`): 8 segments, 142 procedures, `entry` decompiled; deterministic re-run (r2-05) |
| Cross-version compare | `rea function --procedure` + `compare_functions` (8 typed dims, CLI); `rea compare` membership diff; `record_pairs` verdicts are MCP-only | function-level diff on two versions | expac 10-12↔10-13 `entry`/`main` compared; `REA_GHIDRA_STARTUP_TIMEOUT_MS` needed past ~40MB targets (r2-08) |
| Recorded crashes (mechanism) | `inspect_recorded_crash <elf-core>` — caller must `coredumpctl dump`/`zstd -d` first; **32 MiB decompressed cap**; `REA_PWNTOOLS_PYTHON` + optional `REA_PWNDBG_GDBINIT` | live run on a ≤32MiB core | crash-godot core → `ev_3686f9…`, 27 regs × threads, notes retained (r2-06) |
| Evidence discipline | `detail:"summary"` + `parent_evidence_id` paging; `get_evidence_bundle` filters; `inspect-evidence-bundle`; `--snapshot <path>` JSON bundle | every Core probe emits `evidence_id` + `limitations[]`/`unknowns[]` | snapshot is evidence persistence, not a Ghidra DB cache (timed) |
| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |

Cross-lane registry this lane maintains: the REA surface map — per-client
registration state, provider availability, provider env keys, and the on-host
artifact inventory — kept in `corpus/knowledge/`, refreshed by `rea doctor`
each round.

## Frontier

Claimed in MINT.md, not yet held. Each moves to Core by a `LOG.md` entry citing
the corpus entries that earned it.

- **PE subtypes** — native x86-64 held (Core); ARM64 and managed-arch PE not
  yet exercised end-to-end.
- **Managed PE/CLI assemblies** — `inspect_managed_artifact` family reports
  `available:true` but rejected a real AnyCPU `Microsoft.*.dll` as
  `unsupported PE architecture`; no SDK/`ilspycmd`/Mono on host (Pinta's
  Mono.Cecil is a reader substrate but no compiler to build a harness).
- **Firmware images** — `inspect-firmware-regions` probed r2: requires
  `REA_BINWALK_COMMAND` (Binwalk 3.1.x, version-gated) — NOT Binwalk-free as
  catalog prose suggested; `extract-firmware` needs `REA_UNBLOB_COMMAND`
  (Unblob 26.6.x). Targets ready (`ucodes_tu10x.bin` 12KB, GSP blobs are ELF64
  RISC-V). REA's `analyze` refuses all firmware bytes — no fallback path.
- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
  intake — neither exists. Retention decays oldest-first.
- **Offline ELF layout** — `inspect-binary-layout` still gated on
  `REA_PWNTOOLS_PYTHON`; the uv-venv provisioning recipe is documented
  (r2 lessons) but not persisted — operator-owned.
- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
  JEB (unprobed). Engine installs are operator-owned.
- **Android APK** — 2 real APKs exist (Godot export templates); decode route
  needs `REA_JADX_MCP_JAR` (jadx-headless-mcp 0.7.1, absent) — archive
  inventory of an APK is already Core via `inspect_artifact`.
- **Runtime observation** — substrate present (system chromium, playwright
  1.64, electron39/43 binaries) but zero debug ports currently bound; next
  probe: self-launch `chromium --remote-debugging-port=9222` →
  `list_browser_targets` (electron targets default :9223).
- **Cross-version diffing** — `compare_application_versions`,
  `compare_bundles`, `compare_javascript_export_shapes`: catalog-listed; needs
  a two-version artifact pair (pacman cache already retains multi-version
  archives — e.g. `1password-cli` 2.34.1-1 + 2.40.0-2).
- **macOS-only surfaces** — Mach-O/plist/LLDB/asset-catalog ops report
  `unsupported_host` on Linux; recorded so the lane never claims them.
- **EVM bytecode** — unblocked: 6.4.0 bundles EVMole 0.9.3/WASM (r1's
  "needs pwntools" belief corrected); needs only a synthetic hex carrier.

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
