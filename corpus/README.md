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
| REA service & connection | `2026-10-13-mcp-registrations`, `2026-10-13-doctor-taxonomy`, `2026-10-13-r2-doctor-reverify-r2` | held — 3/7 clients registered (devin/omp/kimi), Ghidra-only engine; zero drift across 3 re-verifications |
| REA CLI & self-docs | `2026-10-13-rea-cli-surface`, `2026-10-13-rea-self-documentation` | held — 127 commands, `--llms`/`--llms-full`/`--schema` tiers |
| REA skill contract (v37) | `2026-10-13-rea-skill-contract`, `2026-10-13-r2-skill-references-deep` | held — routing table, paging model, refusal rules, all 4 reference files extracted |
| Provider readiness | `2026-10-13-ghidra-install`, `2026-10-13-java-runtime` | held — Ghidra 12.1.4 8/8 checks, JDK 21.0.12.1 |
| Native ELF | `2026-10-13-elf-observation-jq`, `2026-10-13-rea-live-jq-e2e`, `2026-10-13-r2-libjq-engine`, `2026-10-13-r3-verb-coverage` | held — e2e on `/usr/bin/jq` + `libjq.so.1` (jq_next bytecode VM); xrefs/trace/read-bytes/function exercised |
| PE cross-format | `2026-10-13-pe-surface`, `2026-10-13-r2-pe-e2e-proof`, `2026-10-13-r3-pe-arm64` | held — x86-64 + ARM64 both e2e via Ghidra |
| Electron/ASAR/JS | `2026-10-13-asar-surface`, `2026-10-13-r2-asar-deep-obsidian`, `2026-10-13-r3-renderer-asar`, `2026-10-13-r3-typora-signal`, `2026-10-13-r3-node-addons` | held — obsidian app.asar (launcher) + obsidian.asar (real app: 45 ipcMain ops); N-API taxonomy; .jsc bytecode loader identified |
| Archives & packages | `2026-10-13-pacman-packages`, `2026-10-13-r3-apk-inventory`, `2026-10-13-r3-appimage` | held — signed corpus; APK content graph (120 nodes verified); AppImage = ELF+unaddressable payload segment |
| Managed assemblies | `2026-10-13-managed-assemblies` | surveyed — narrow; AnyCPU rejected by REA, no decompiler |
| Recorded crashes | `2026-10-13-crash-evidence`, `2026-10-13-r2-crash-inspect-probe` | mechanism held (32 MiB cap) — organic cores too big, coverage frontier |
| Cross-version diff | `2026-10-13-r2-version-diff-compare`, `2026-10-13-r3-mcp-session` | held — real `status:changed` verdict via record_pairs (requires ALL members paired) |
| Runtime observation | `2026-10-13-r3-runtime-observation` | held — CDP enumerate/inspect on self-launched chromium + electron; scenario capture ran |
| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
| Host anomaly triage | `2026-10-13-r2-jq-shadow-verdict`, `2026-10-13-r3-jq-provenance` | resolved — byte-identical upstream + provenance traced to kimi swarm bootstrap 2026-10-03 |
| Synthesized carriers | `2026-10-13-r3-keyed-archive-carriers` | held — keyed-archive/interface-builder/dylib-trace all work on Linux synths; recipes recorded |
| Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
| Provider/capability matrix | `2026-10-13-r2-provider-capability-matrix` | held — 18 ops, 8 available; per-op `available` is declared, provider `status` gates |
| Firmware | `2026-10-13-r2-firmware-probe`, `2026-10-13-r2-frontier-prereqs` | frontier — `REA_BINWALK_COMMAND` (3.1.x) + `REA_UNBLOB_COMMAND` (26.6.x) gates; GSP blobs are RISC-V ELF |

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
| `2026-10-13-r2-doctor-reverify-r2` | zero drift vs r1 registry values | `doctor --json` re-run | 2026-10-13 |
| `2026-10-13-r2-skill-references-deep` | android/js/runtime-obs/connection reference details | 4 skill reference files | 2026-10-13 |
| `2026-10-13-r2-libjq-engine` | libjq.so.1: 924 procs, .dynsym exports, +0x100000 rebase rule | `rea analyze`/`decompile jq_next` | 2026-10-13 |
| `2026-10-13-r3-runtime-observation` | CDP enumerate/inspect on self-launched chromium+electron; scenario capture | live CDP probes on :9222/:9223 | 2026-10-13 |
| `2026-10-13-r3-apk-inventory` | APK content-addressed graph; archive→native .so bridge; jadx/apktool refusals | `inspect-artifact` + `analyze` on Godot APK | 2026-10-13 |
| `2026-10-13-r3-evm-interface` | EVMole selector recovery; positional encoding; honest empty envelopes | synthetic hex carriers | 2026-10-13 |
| `2026-10-13-r3-pe-arm64` | ARM64 PE e2e (cli-arm64.exe, 136 procs); x64 cosmetic label noted | `rea analyze`/`decompile` | 2026-10-13 |
| `2026-10-13-r3-jq-provenance` | shadow jq install traced to kimi-code swarm agent-2, 2026-10-03 | shell history/session wire.jsonl/timestamps | 2026-10-13 |
| `2026-10-13-r3-renderer-asar` | obsidian.asar = real app: 45 ipcMain ops, permissive BrowserWindows w/ mitigations; 1GiB+8GiB heap wall | `analyze-javascript-application` 47.7MB ev bundle | 2026-10-13 |
| `2026-10-13-r3-node-addons` | .node N-API taxonomy (classic vs napi-rs); rebase rule holds on .node | `nm -D`/`rea analyze`/`decompile` on btime | 2026-10-13 |
| `2026-10-13-r3-appimage` | AppImage = ELF + unaddressable squashfs segment; payload via read-bytes | `inspect-artifact`/`analyze`/`--appimage-offset` | 2026-10-13 |
| `2026-10-13-r3-keyed-archive-carriers` | keyed-archive, interface-builder, dylib-trace all work on synth carriers | plistlib + hand-rolled Mach-O recipes | 2026-10-13 |
| `2026-10-13-r3-mcp-session` | retained-evidence paging; record_pairs changed-verdict; epoch-scoped retention w/ evidence_links pinning | live `rea` MCP session | 2026-10-13 |
| `2026-10-13-r3-verb-coverage` | xrefs/trace/read-bytes/addr-offset/function/instructions families; positional-arg pattern | live runs on libjq.so.1.0.4 | 2026-10-13 |
| `2026-10-13-r3-typora-signal` | typora app.asar = bytenode loader (99.4% .jsc); zero-finding ≠ parsed-empty | `analyze-javascript-application` | 2026-10-13 |

## Lessons

| entry | round | gist |
|---|---|---|
| `2026-10-13-round-1` | 1 | rejects-as-calibration; `--schema`>`--help`; doctor healthy≠usable; ASAR/extract-file/tmpdir gotchas; snapshot≠DB cache; verify-then-disassemble |
| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign |
| `2026-10-13-round-3` | 3 | r2 survives audit (2 errata + 1 mechanism fix); positional-arg pattern; rebase rule generalizes to .node; evidence ids content-addressed across sessions; partial pairing→unknown; zero-findings≠inventory exclusion |

## Frontier

- `inspect_recorded_crash` on cores >32 MiB — mechanism held, organic coverage blocked by cap.
- `inspect_firmware_regions` — blocked on `REA_BINWALK_COMMAND` (Binwalk 3.1.x, operator-owned).
- APK decode route (`inspect-android-package`/`decode-android-resources`) — typed refusals on `REA_JADX_MCP_JAR`/`REA_APKTOOL_COMMAND` (operator-owned).
- Bytecode `.jsc` (bytenode) decompile — typora's real app surface; no REA verb yet.
- `recover-javascript-sources` — needs `REA_WAKARU_COMMAND` (Wakaru binary).
- JS bundles >3.9MB single-file — worker OOM even at 8GiB heap; per-file `--artifact-format directory` is the workaround.
- PE reserve: 91MB Godot ARM64 template, ARM64X hybrids.
- Managed AnyCPU still REA-rejected; precompiled ilspy/Cecil harness is the cheapest unlock.
- Runtime-obs extended: `observe-web-session`/`observe-javascript-runtime`/`capture-electron-scenario` unexercised.
- Blocked-on-operator: `inspect_binary_layout` (pwntools — uv recipe documented, not persisted), `extract_firmware` (Unblob 26.6.x), IDA/Hopper/JEB (absent), signal/1Password asar scale (needs raised heap + filter-output).

## Known gaps

- `record_pairs` exercised via MCP session r3 (14-mcp-session) — `changed` needs ALL members paired; remaining: `compare_javascript_export_shapes` unexercised.
- Organic cores exceed the 32 MiB inspect cap — no deep runtime-evidence coverage yet.
- Skill `v37` flagged `stale` by doctor — per-client destination absence, not content drift; healing is operator-owned.
- LOG.md discipline during parallel waves: a lane's dispatch scope overrides ambient append rules — encode explicitly in future wave prompts.
- Criterion-5 (observation/inference labels) is not uniformly applied in round-1 entries — violations recorded as errata; applies to all future entries at write time.
