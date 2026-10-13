# kaidoku-shokunin corpus — index

Proprietary memory for reverse engineering of shipped artifacts with REA on
this Linux host — native ELF/PE through the Ghidra 12.1.4 provider,
Electron/ASAR/JavaScript bundles, archives and packages, managed assemblies,
firmware images and recorded crashes; evidence-first static analysis that keeps
observation, inference and unknowns separate. Every entry cites its source.
Coverage map, frontier and open gaps grow with rounds (CORPUS.md, LEARNING.md).
A row is written when its file exists, never before.

## Coverage map

| section | entries | state |
|---|---|---|
| REA service & connection | `2026-10-13-mcp-registrations`, `2026-10-13-doctor-taxonomy` | held — 3/7 clients registered (devin/omp/kimi), Ghidra-only engine |
| REA CLI & self-docs | `2026-10-13-rea-cli-surface`, `2026-10-13-rea-self-documentation` | held — 127 commands, `--llms`/`--llms-full`/`--schema` tiers |
| REA skill contract (v37) | `2026-10-13-rea-skill-contract` | held — routing table, paging model, refusal rules |
| Provider readiness | `2026-10-13-ghidra-install`, `2026-10-13-java-runtime` | held — Ghidra 12.1.4 8/8 checks, JDK 21.0.12.1 |
| Native ELF | `2026-10-13-elf-observation-jq`, `2026-10-13-rea-live-jq-e2e` | held — end-to-end analyze/search/decompile on `/usr/bin/jq` |
| PE cross-format | `2026-10-13-pe-surface` | surveyed — 413 local PEs, Ghidra import unprobed |
| Electron/ASAR/JS | `2026-10-13-asar-surface` | surveyed — 6 archives, `analyze_javascript_application` e2e via wave 16 |
| Archives & packages | `2026-10-13-pacman-packages` | held — signed corpus, verify-then-disassemble baseline |
| Managed assemblies | `2026-10-13-managed-assemblies` | surveyed — narrow; AnyCPU rejected by REA, no decompiler |
| Recorded crashes | `2026-10-13-crash-evidence` | surveyed — 174 zstd cores, `inspect_recorded_crash` unprobed |
| Firmware / APK / runtime-obs / EVM | — | frontier — catalog-listed, unprobed or prerequisite-gated |

## Knowledge

| entry | topic | source | verified-at |
|---|---|---|---|
| `2026-10-13-rea-cli-surface` | 127-command CLI inventory, global options, argument shapes | `npx rea-agents@6.4.0 --help` ×16 | 2026-10-13 |
| `2026-10-13-rea-self-documentation` | `--llms`/`--llms-full`/`--schema` doc tiers, README matrix | live CLI output | 2026-10-13 |
| `2026-10-13-doctor-taxonomy` | doctor check classes, health verdict mechanics, registrations | `doctor --json` + `dist/application/` source | 2026-10-13 |
| `2026-10-13-mcp-registrations` | per-client config dialects, npx-shim fragility | client config files | 2026-10-13 |
| `2026-10-13-rea-skill-contract` | routing table, evidence paging, refusals | `~/.agents/skills/reverse-engineer-anything/` | 2026-10-13 |
| `2026-10-13-pe-surface` | 413 local PEs, wine absent, objdump/llvm coverage | find/file/readelf/objdump | 2026-10-13 |
| `2026-10-13-ghidra-install` | install layout, 39 processors, decompiler binary | filesystem inventory | 2026-10-13 |
| `2026-10-13-java-runtime` | JDK 21 wiring, JAVA_HOME dual export, single-Java risk | java/readlink/grep | 2026-10-13 |
| `2026-10-13-elf-observation-jq` | observation-vs-inference worked example on `/usr/bin/jq` | file/readelf/strings/jq --version | 2026-10-13 |
| `2026-10-13-rea-live-jq-e2e` | live analyze/search/decompile run, session lifecycle, snapshot semantics | timed `rea` runs on `/usr/bin/jq` | 2026-10-13 |
| `2026-10-13-asar-surface` | 6 asar archives, enumeration gotchas, `.unpacked` natives | find/asar-list/file | 2026-10-13 |
| `2026-10-13-pacman-packages` | ownership oracle, signed corpus, `.MTREE` digests, `~/.local/bin/jq` shadow | pacman/tar/gpg/sha256sum | 2026-10-13 |
| `2026-10-13-managed-assemblies` | dotnet host, ~341 framework DLLs, Pinta+Mono.Cecil, tooling absent | dotnet/file/pacman | 2026-10-13 |
| `2026-10-13-crash-evidence` | systemd-coredump corpus, ACL reach, gdb path, decay | coredumpctl/journalctl/getfacl | 2026-10-13 |

## Lessons

| entry | round | gist |
|---|---|---|
| `2026-10-13-round-1` | 1 | rejects-as-calibration; `--schema`>`--help`; doctor healthy≠usable; ASAR/extract-file/tmpdir gotchas; snapshot≠DB cache; verify-then-disassemble |

## Frontier

- PE end-to-end via Ghidra (`open_binary` on a Godot template) — inferred, unprobed.
- `inspect_recorded_crash` on a retained core (waybar/godot) — catalog-listed.
- `inspect_firmware_regions` on nvidia GSP blobs — catalog-listed.
- Cross-version diffing on cached pacman archive pairs — catalog-listed.
- `~/.local/bin/jq` impostor analysis — unowned static ELF shadowing packaged jq (highest-value live target).
- Blocked-on-operator: `inspect_binary_layout` (pwntools), `extract_firmware` (Binwalk/Unblob), managed AnyCPU (REA rejects), IDA/Hopper (absent).

## Known gaps

- No two-version artifact diff has been run — compare verbs are catalog knowledge only.
- MCP `binary_session` tool_availability recorded only via wave 16's live probe; no full catalog dump retained in corpus.
- Skill `v37` flagged `stale` by doctor — per-client destination absence, not content drift; whether this needs healing is operator-owned.
- LOG.md discipline during parallel waves: a lane's dispatch scope overrides ambient append rules — encode explicitly in future wave prompts.
