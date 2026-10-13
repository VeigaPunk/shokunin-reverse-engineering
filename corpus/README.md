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
| PE cross-format | `2026-10-13-pe-surface`, `2026-10-13-r2-pe-e2e-proof` | held — Ghidra PE import proven e2e (cli-64.exe, 142 procedures) |
| Electron/ASAR/JS | `2026-10-13-asar-surface`, `2026-10-13-r2-asar-deep-obsidian` | held — obsidian app.asar full graph, summary→page→item paging demonstrated |
| Archives & packages | `2026-10-13-pacman-packages` | held — signed corpus, verify-then-disassemble baseline |
| Managed assemblies | `2026-10-13-managed-assemblies` | surveyed — narrow; AnyCPU rejected by REA, no decompiler |
| Recorded crashes | `2026-10-13-crash-evidence`, `2026-10-13-r2-crash-inspect-probe` | mechanism held (32 MiB cap) — organic cores too big, coverage frontier |
| Cross-version diff | `2026-10-13-r2-version-diff-compare` | machinery held — 8-dim function compare on CLI; `record_pairs` MCP-only |
| Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
| Provider/capability matrix | `2026-10-13-r2-provider-capability-matrix` | held — 18 ops, 8 available; per-op `available` is declared, provider `status` gates |
| Firmware / APK / runtime-obs | `2026-10-13-r2-firmware-probe`, `2026-10-13-r2-frontier-prereqs` | frontier — firmware needs Binwalk env; 2 APKs exist, no decode tooling; nothing bindable for runtime-obs |
| EVM | `2026-10-13-r2-frontier-prereqs` | unblocked (EVMole WASM bundled) — no carrier probed |

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
| `2026-10-13-r2-pe-e2e-proof` | Ghidra PE import proven, deterministic | `rea analyze` on cli-64.exe | 2026-10-13 |
| `2026-10-13-r2-crash-inspect-probe` | inspect_recorded_crash e2e, 32MiB cap, provider env keys | live run on crash-godot core | 2026-10-13 |
| `2026-10-13-r2-jq-shadow-verdict` | `~/.local/bin/jq` = byte-identical upstream jq-1.8.2 release — benign | rea analyze + upstream sha256 match | 2026-10-13 |
| `2026-10-13-r2-version-diff-compare` | compare_functions 8 dims; record_pairs MCP-only; 330s timeout bound | live compares on expac/bwrap pairs | 2026-10-13 |
| `2026-10-13-r2-firmware-probe` | inspect-firmware-regions needs `REA_BINWALK_COMMAND`; doctor blind spot | live refusals + source | 2026-10-13 |
| `2026-10-13-r2-asar-deep-obsidian` | obsidian app.asar: 170-node graph, IPC surface, paging model | `analyze-javascript-application` e2e | 2026-10-13 |
| `2026-10-13-r2-provider-capability-matrix` | 18-op matrix, 7 provider ids, env-key contracts | `providers`/`capabilities` JSON | 2026-10-13 |
| `2026-10-13-r2-evidence-bundle-schema` | snapshot envelope vs evidence_bundle; ev_ content-addressed; replay | live snapshot + bundle verbs | 2026-10-13 |
| `2026-10-13-r2-frontier-prereqs` | APK/runtime-obs/EVM/JEB prerequisite state | command -v sweeps, ports | 2026-10-13 |
| `2026-10-13-r2-doctor-reverify` | zero drift vs r1 registry values | `doctor --json` re-run | 2026-10-13 |
| `2026-10-13-r2-skill-references-deep` | android/js/runtime-obs/connection reference details | 4 skill reference files | 2026-10-13 |
| `2026-10-13-r2-libjq-engine` | libjq.so.1: 924 procs, .dynsym exports, +0x100000 rebase rule | `rea analyze`/`decompile jq_next` | 2026-10-13 |

## Lessons

| entry | round | gist |
|---|---|---|
| `2026-10-13-round-1` | 1 | rejects-as-calibration; `--schema`>`--help`; doctor healthy≠usable; ASAR/extract-file/tmpdir gotchas; snapshot≠DB cache; verify-then-disassemble |
| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign |

## Frontier

- `inspect_recorded_crash` on cores >32 MiB — mechanism held, organic coverage blocked by cap.
- `inspect_firmware_regions` — blocked on `REA_BINWALK_COMMAND` (Binwalk 3.1.x, operator-owned).
- APK decode route (`inspect_android_package`) — 2 Godot APKs exist; apktool/jadx absent.
- Runtime observation — substrate present (chromium/electron binaries, playwright) but nothing currently bindable; needs a launched debug port.
- PE subtypes: ARM64 and managed assemblies not yet exercised end-to-end.
- Managed AnyCPU still REA-rejected; precompiled ilspy/Cecil harness is the cheapest unlock.
- EVM `inspect_evm_interface` — unblocked (bundled WASM), needs a synthetic hex carrier.
- Blocked-on-operator: `inspect_binary_layout` (pwntools — uv recipe documented), `extract_firmware` (Unblob 26.6.x), IDA/Hopper/JEB (absent).

## Known gaps

- `record_pairs` verdict path exercised only via bundled domain calls — no MCP-session compare yet.
- Organic cores exceed the 32 MiB inspect cap — no deep runtime-evidence coverage yet.
- Skill `v37` flagged `stale` by doctor — per-client destination absence, not content drift; healing is operator-owned.
- LOG.md discipline during parallel waves: a lane's dispatch scope overrides ambient append rules — encode explicitly in future wave prompts.
- Criterion-5 (observation/inference labels) is not uniformly applied in round-1 entries — violations recorded as errata; applies to all future entries at write time.
