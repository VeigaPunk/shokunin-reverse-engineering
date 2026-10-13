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
| Managed assemblies | `2026-10-13-managed-assemblies`, `2026-10-13-r4-11-managed-unlock`, `2026-10-13-r4u-04-dnfile-il` | held — REA verbs on `0x14c` IL-only (196 dlls accepted); dnfile/dncil covers all classes incl. `0xfd1d`; 64MiB budget + GENERICINST limits mapped |
| Recorded crashes | `2026-10-13-crash-evidence`, `2026-10-13-r2-crash-inspect-probe` | mechanism held (32 MiB cap) — organic cores too big, coverage frontier |
| Cross-version diff | `2026-10-13-r2-version-diff-compare`, `2026-10-13-r3-mcp-session` | held — real `status:changed` verdict via record_pairs (requires ALL members paired) |
| Runtime observation | `2026-10-13-r3-runtime-observation` | held — CDP enumerate/inspect on self-launched chromium + electron; scenario capture ran |
| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
| Host anomaly triage | `2026-10-13-r2-jq-shadow-verdict`, `2026-10-13-r3-jq-provenance` | resolved — byte-identical upstream + provenance traced to kimi swarm bootstrap 2026-10-03 |
| Synthesized carriers | `2026-10-13-r3-keyed-archive-carriers` | held — keyed-archive/interface-builder/dylib-trace all work on Linux synths; recipes recorded |
| Evidence model | `2026-10-13-r2-evidence-bundle-schema` | held — snapshot envelope vs inner bundle schema, content-addressed ev_ ids |
| Provider/capability matrix | `2026-10-13-r2-provider-capability-matrix` | held — 18 ops, 8 available; per-op `available` is declared, provider `status` gates |
| Firmware | `2026-10-13-r2-firmware-probe`, `2026-10-13-r2-frontier-prereqs`, `2026-10-13-r4u-01-firmware-deep`, `2026-10-13-r4u-03-unblob-extract` | held (partial) — binwalk regions + unblob extract exercised on GSP blobs; RISC-V `target_unavailable` is the deep-analysis wall |

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
| `2026-10-13-r3-typora-signal` | typora app.asar = bytenode loader (99.38% .jsc — corrected r4); zero-finding ≠ parsed-empty | `analyze-javascript-application` | 2026-10-13 |
| `2026-10-13-r4-06-1password-asar` | 1Password: hardened 423-file shell over 188MB Rust N-API core; 80 IPC channels behind one `file://` prefix gate; GraphQL/typed-command forward | `analyze-javascript-application` + `nm`/`rea` on index.node | 2026-10-13 |
| `2026-10-13-r4-07-jsc-bytecode` | `ELECTRON_RUN_AS_NODE=1` + version-matched electron (42.2.0/V8 14.8) accepts typora `.jsc`; `--print-bytecode` → 530KB Ignition disassembly, 116 function blocks | live electron run-as-node | 2026-10-13 |
| `2026-10-13-r4-08-observe-verbs` | `observe-web-session`/`observe-web-execution`/`observe-javascript-runtime`/`reconcile-javascript-runtime` held; `capture-electron-scenario` typed refusal (Playwright handshake); `node --inspect` needs real file target | live CDP + V8-inspector probes | 2026-10-13 |
| `2026-10-13-r4-09-js-export-compare` | `compare-javascript-export-shapes` e2e; CLI needs inline Evidence (retained refs MCP-only); obsidian cross-version diff landed | live compares on obsidian versions | 2026-10-13 |
| `2026-10-13-r4-11-managed-unlock` | managed surface mapped: `0x14c` IL-only accepted (196 dlls), refused = x64 R2R `0xfd1d`/x64 IL-only; dnfile+dncil covers all classes incl. refused | REA managed verbs + pip dnfile/dncil | 2026-10-13 |
| `2026-10-13-r4-12-godot-arm64-scale` | 91.6MB Godot ARM64 PE → `provider_timeout` at ~900s internal deadline (GhidraClient.js:607), still progressing at kill; not OOM; control re-run byte-identical | `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` live run | 2026-10-13 |
| `2026-10-13-r4-13-pwntools-persist` | `inspect-binary-layout` first-held: jq full RELRO observed; persistent venv `~/.local/share/kaidoku-pwnenv`; `coredumpctl dump` already-decompressed correction | live runs + venv persist | 2026-10-13 |
| `2026-10-13-r4-14-libsignal` | libsignal 188MB Rust N-API anatomy | `nm`/`file`/REA on signal-desktop `.node` | 2026-10-13 |
| `2026-10-13-r4-15-appimage-inner` | AppImage squashfs carved via unblob/7z; inner asar analyzes — "Grok Bot" = Anysphere/Cursor `sand` (715 members, full Electron surface) | unblob + 7z + `analyze-javascript-application` | 2026-10-13 |
| `2026-10-13-r4-16-frontier-rescan` | r5 roadmap: ~26 self-provisionable + ~45 env-gated ops; managed REA verbs proven in-lane | doctor/capabilities rescan | 2026-10-13 |
| `2026-10-13-r4u-01-firmware-deep` | GSP blobs = ELF64 RISC-V signature wrappers (56/156 regions); ucodes are stub containers (correct-empty); RISC-V `target_unavailable` REA-side | binwalk regions + unblob extract on 4 nvidia blobs | 2026-10-13 |
| `2026-10-13-r4u-02-jadx-decode` | Android surface fully open: package inspect, manifest decode, class search, real Java decompile; jadx mints per-run ev ids (mkdtemp) vs apktool deterministic | jadx-headless-mcp 0.7.1 + apktool 3.0.3 on Godot APKs | 2026-10-13 |
| `2026-10-13-r4u-03-unblob-extract` | `extract-firmware` live; pkg.tar.zst 100% carved (binwalk saw zero); squashfs needs sasquatch (7z fallback); per-run ev ids | unblob 26.6.4 on 3 candidates | 2026-10-13 |
| `2026-10-13-r4u-04-dnfile-il` | two-tool managed map: REA <64MiB on `0x14c`/`0x8664`; dnfile+dncil everything incl. `0xfd1d` (2,594/2,594 + 650/650 bodies) | pip dnfile/dncil + RVA shim recipe | 2026-10-13 |
| `2026-10-13-r4u-05-wakaru-oom` | wakaru spawn-OOM root-caused (prlimit --as=1GiB + node shim); FIX: bind `@wakaru/cli-linux-x64` ELF; verb takes FILE not dir | dist-source trace + live fix | 2026-10-13 |
| `2026-10-13-r4u-06-adb-surface` | adb 37.0.0 device-free: 2/24 serial-free verbs; dead-serial taxonomy; `collect-adb-bugreport` blocks ~10min; telemetry bug (daemon-start flag) | live verbs on dead serial emulator-5554 | 2026-10-13 |

## Lessons

| entry | round | gist |
|---|---|---|
| `2026-10-13-round-1` | 1 | rejects-as-calibration; `--schema`>`--help`; doctor healthy≠usable; ASAR/extract-file/tmpdir gotchas; snapshot≠DB cache; verify-then-disassemble |
| `2026-10-13-round-2` | 2 | r1 survives audit (1 erratum); catalog≠provider≠held; doctor aux-blind; 32MiB crash cap; MCP-session-scoped ev_ids; shadow-binary verdict benign |
| `2026-10-13-round-3` | 3 | r2 survives audit (2 errata + 1 mechanism fix); positional-arg pattern; rebase rule generalizes to .node; evidence ids content-addressed across sessions; partial pairing→unknown; zero-findings≠inventory exclusion |
| `2026-10-13-round-4` | 4+4u | r3 survives audit (10+ errata appended); provider-gate diagnosis = find the spawn wrapper (prlimit); ev_ids = f(content,path,params); `grep -o|wc -l` not `grep -c` on minified; synth carriers ≠ byte-reproducible; env keys unlock 6 surfaces; 900s internal deadline vs outer timeout |

## Frontier

- `inspect_recorded_crash` on cores >32 MiB — mechanism held, organic coverage blocked by cap (`invalid_request`/`out_of_range` on oversize).
- RISC-V deep analysis — `target_unavailable` REA-side on outer REL + carved EXEC; Ghidra ships the module. Next: direct analyzeHeadless on `.fwimage`.
- `.jsc` → source mapping — Ignition disassembly held (r4-07); View8/jsc2js-style mapper is next for typora's real app.
- >90MB PE scale — 91.6MB Godot ARM64 hits the ~900s internal session deadline; raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`≈3.6M + `GHIDRA_HEADLESS_MAXMEM=6-8G`, or bisect 2-5MB.
- `capture-electron-scenario` — typed refusal (Playwright handshake) despite same app launching manually.
- sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today.
- adb device surface — 22/24 verbs need a live device/emulator.
- PE reserve: ARM64X hybrids; signal-desktop 38.5MB asar lane in flight.
- Runtime-obs extended: process-capture, managed `verify`/`project` ops, native call-target resolution (per r4-16 rescan: ~26 self-provisionable).
- Blocked-on-operator: IDA (`REA_IDA_MCP_CONFIG`), Hopper (`HOPPER_LAUNCHER_PATH`), JEB — all absent.

## Known gaps

- `record_pairs` exercised via MCP session r3 — `changed` needs ALL members paired. `compare_javascript_export_shapes` exercised r4-09 (inline-Evidence required on CLI).
- Organic cores exceed the 32 MiB inspect cap — no deep runtime-evidence coverage yet.
- Evidence ids are `f(content, path, params)` — path-sensitive, three-lane corroboration r4; cite `subject.digest.sha256` for cross-path identity.
- Skill `v37` flagged `stale` by doctor — per-client destination absence, not content drift; healing is operator-owned.
- LOG.md discipline during parallel waves: a lane's dispatch scope overrides ambient append rules — encode explicitly in future wave prompts.
- Criterion-5 (observation/inference labels) is not uniformly applied in round-1 entries — violations recorded as errata; applies to all future entries at write time.
