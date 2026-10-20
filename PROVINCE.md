# kaidoku-shokunin — Province

**Domain:** reverse engineering of shipped artifacts with REA on this Linux
host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript
bundles, archives and packages; evidence-first static analysis that keeps
observation, inference and unknowns separate.

Surface summary: the `rea` package requests in the client config files: Devin, OMP
and Kimi all pin `rea-agents@6.7.0` (207 MCP tools + 153 CLI commands;
catalog tools_sha256 `af39310c…`, the package's compiled, recorded identity;
re-read 2026-10-20, round 19, `.ufo/waves/round-19/evidence/rea-catalog.json`). These are configured requests, not running-server versions; the doctor checks a separate Kimi JSON registration, not the live TOML pin.
Round carrier runs pin the CLI explicitly to the superseded client pin `rea-agents@6.5.0` (same 207/153 counts; tools_sha256 `805433f1…`). Historical: Kimi resolved `rea-agents@6.4.0` (historical 170 MCP tools + 127 CLI commands; historical catalog tools_sha256 `25802f6d…`) before 2026-10-18; its npx cache is gone (historical, absent 2026-10-20). The Ghidra provider is at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`;
host binutils as non-REA fallback readers.

Drift-prone values: reverified 2026-10-20 (round 19) — configured REA MCP pins are Devin
`rea-agents@6.7.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`), OMP
`rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:8`), and Kimi
`rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126`); Devin/OMP were rewritten 2026-10-20 13:35:56 -03 outside the lane (they carried the superseded 6.5.0 pin before). The operator disabled the OMP rea entry for the hyaku phase (10:12 -03); that rewrite dropped the `enabled: false` key, so the live OMP file no longer records the disable (round-19 w1 `LiveConfigPins.md`). Cache/catalog The `17:55:49Z receipt` and its old line-number pointers are historical, not current registration evidence.
identities (re-derived 2026-10-20, round 19): 6.7.0 at `/home/vgpnk/.npm/_npx/a1722018f28f9df2` — 153 CLI
commands, 207 MCP tools, `tools_sha256=af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639`; 6.5.0 at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` — 153 CLI commands, 207 MCP tools, `tools_sha256=805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded`; historical 6.4.0 in npx cache directory
`dea9475797100b20` (historical: directory absent 2026-10-20) — 127 CLI commands, 170 MCP tools,
`tools_sha256=25802f6de8c14ba736dc61ff1cbc7c5cd738fd74426aa01338f2dd03e0911166` (historical pin)
(L12 receipt, SHA-256 above). Installed shared REA skill is v42/207 tools; since 2026-10-20 13:35:56 -03 it is byte-identical to the 6.7.0 bundled skill (installed sha256 `fbcd39d6…`; the prior `c8639823…` variant survives only as a `.rea.backup` recovery file; round-19 w1 `SourcesRowAudit.md`). Doctor: the 6.7.0 doctor reports no Devin/OMP registration finding, the 6.5.0 doctor reports those registrations request 6.7.0 (`.ufo/waves/round-19/evidence/doctor/`); 6.4.0 expected v37 (historical L10 receipts).
Reverified Ghidra/JDK 2026-10-20: `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`, `application.version=12.1.4` (build `2026-Sep-21 1613 UTC`); `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`, Java `21.0.12.1` (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties:17`, `/home/vgpnk/.bashrc:28-29` (were `:23-24` before the 2026-10-19 `.bashrc` edit); `java -version 2>&1 | head -n 1` returned `openjdk version "21.0.12.1" 2026-08-18`).
Provider-key inventory re-probed 2026-10-20 (round 19, names only, w1 `ProviderKeysRecheck.md`): `.bashrc:63-69` exports `REA_PWNTOOLS_PYTHON`, `REA_BINWALK_COMMAND`, `REA_UNBLOB_COMMAND`, `REA_APKTOOL_COMMAND`, `REA_ADB_PATH`, `REA_WAKARU_COMMAND` (bind the `@wakaru/cli-linux-x64` ELF, not node shim) and `REA_JADX_MCP_JAR`, all resolving to existing paths; these exports sit below the interactive guard (`.bashrc:34`), so a non-interactive shell does not see them; `REA_IDA_MCP_CONFIG` and `HOPPER_LAUNCHER_PATH` are unset. The r5-audit C8 correction was for REA 6.4.0 (historical): `APKTOOL_COMMAND_ENV=REA_APKTOOL_COMMAND`, now `.bashrc:66` (was `:61`) → `/usr/bin/apktool`.

Probe/reconciliation conventions: `rea doctor` is the environment verdict;
`binary_session {}` is the live-server verdict (`result.tool_availability` +
provider candidates); a catalog-listed tool is *available*, not *held* —
ground moves to Core only after an end-to-end probe lands a `LOG.md` entry
citing its `evidence_id` and subject sha256. When module identity matters
for an `analyze_function` probe, pin request bytes (or re-derive the
dossier); the evidence ID alone does not authenticate module attribution
carried in `subject` (`corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`).
The domain is a frontier, not a fence: it grows by evidence (LEARNING.md).

## Core

Surfaces owned now — each verified on this host 2026-10-13.

| Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |
|---|---|---|---|
| REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `evidence/doctor/`; historical readiness probe 2026-10-13 |
| `rea` CLI | npx cache `~/.npm/_npx/*/node_modules/rea-agents` — no `rea` on PATH; 153 commands on the 6.5.0/6.7.0 pins, 127 on 6.4.0 (historical) | `npx -y rea-agents@6.4.0 --version` → `6.4.0` (2026-10-13 receipt) | wave 01/02/03 catalogs |
| Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 34 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
| JDK 21 substrate | `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`, exported in `.bashrc:29` + `.profile:4` (re-read 2026-10-20, w1 `GhidraJdkRecheck`); sole Java on host | `java -version` → 21.0.12.1 full JDK | meets Ghidra `java.min=21` exactly; single-Java fragility noted |
| Native ELF via Ghidra | `rea analyze/search/decompile <path>`; sessions `mkdtemp /tmp/rea-ghidra-*`, `-readOnly -deleteProject`, self-cleaning | `rea analyze <elf>` → overview + procedure inventory | `/usr/bin/jq`: 30 segments, 167 procedures, 190 strings, ~5.5s; `decompile 0x103fa0` recovered `process()` loop |
| Electron/ASAR/JavaScript | `analyze_javascript_application` on `.asar` or extracted tree; `inspect_analysis_view` paging; asar archives pinned on host (12 live): obsidian ×2 + a config-dir copy, signal, 1Password, electron39/43 stubs, typora ×3 (r1 sweep missed them), chatgpt, zcode squashfs-root | `analyze_javascript_application` `detail:"summary"` on a small asar | `default_app.asar` (electron43) → 5 files, 41 findings, evidence `ev_2628de89…`; 1Password 480-file asar (count per the r4-06 erratum) + 188MB Rust N-API core (r4-06); AppImage inner asar via unblob/7z carve (r4-15) |
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in the live session as recorded for the 2026-10-13 host survey); pacman `.pkg.tar.zst` cache: 1,556 signed archives (2026-10-13 snapshot); current cache: 1,350 archive files, each with a matching `.sig` sidecar (arc3-loop1-round9 recount; −206 vs snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md` erratum); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member (re-verified arc3-loop1-round9) |
| Native PE via Ghidra | `rea analyze/search/decompile <pe>` — pure-Java `PeLoader`, wine-independent | `rea analyze <pe>` → segments/procedures | `cli-64.exe` (sha256 `bbb3de57…`): 8 segments, 142 procedures, `entry` decompiled; deterministic re-run (r2-05) |
| Cross-version compare | `rea function --procedure`; `compare_functions`/`compareFunctions` (8 typed dims — domain API or MCP only, **no CLI verb**); `rea compare` membership diff; `record_pairs` verdicts are MCP-session-only (changed verdict requires ALL members paired — r3); `compare-javascript-export-shapes` CLI-held (needs inline Evidence objects — retained refs are MCP-only) | function-level diff on two versions | expac 10-12↔10-13 `entry`/`main` compared; obsidian export-shape diff across versions (r4-09); real-version pair `op` 2.34.1→2.40.0 (41–43MB Go ELF): historical builds go1.25.7→go1.26.8 yielded provider inventories 33,060→11,595 procs (11,588 `FUN_*`) — symbol-keyed pairing unsafe across these builds; pair by explicit evidence/ELF role (r4-10) [r5-audit C1]; precise old cause remains unknown, source-bootstrap diagnosis `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`; current `op` 2.41.0-1 (go1.26.8) observed missing-base bootstrap failure with a bound retained log, a different binary from the historical pair (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`); `REA_GHIDRA_STARTUP_TIMEOUT_MS` needed past ~40MB targets (r2-08) |
| Runtime observation (CDP) | self-launched targets: `chromium --headless --remote-debugging-port=9222`, `xvfb-run electron --remote-debugging-port=9223`; `list_browser_targets`, `inspect-web-page`, `list_electron_targets`, `inspect-electron-page`, `capture-browser-scenario` | `list-browser-targets http://127.0.0.1:9222` on own instance | both legs held r3 (05): CDP enumerate+inspect verified, connect-mode scenario capture ran |
| EVM interface | `rea inspect-evm-interface <file> <raw|hex>` — encoding is POSITIONAL (no `--encoding` flag despite schema); bundled EVMole 0.9.3/WASM | synthetic hex carrier → selector extraction | hand-assembled 81-byte dispatcher recovered all 3 planted ERC-20 selectors; `dispatch:"abi"` (r3-07) |
| Carrierless-macOS surface via synth carriers | `inspect-keyed-archive <plist> [archive]` (archive positional), `decode-interface-builder` (needs `CFBundleExecutable` in Info.plist), `trace-dylib-resolution` (8-aligned cmdsize) | synth carriers (plistlib, hand-rolled Mach-O) — recipes in r3-13 | all three WORK on Linux; `inspect-plist` alone hard-gates macOS |
| APK surface (full) | `rea inspect-artifact` content graph; `inspect-android-package` (jadx-headless-mcp 0.7.1); `decode-android-resources` (apktool 3.0.3); `search-android-classes`/`inspect-android-class`/`inspect-android-method` → real Java decompile; `.so` members extract→`analyze` | `inspect-android-package` on a real APK | Godot `android_debug.apk`: 120 nodes verified (r3-06); 1,925 classes + full manifest decode (r4u-02); `libc++_shared.so` → 3,009 procedures |
| `.node` native addons | ELF shared objects in `*.asar.unpacked`; N-API taxonomy: `nm -D | grep -c ' U napi'` >0 = classic, =0 = napi-rs/Neon | `rea analyze` on a `.node` | btime/get-fonts decompiled; +0x100000 rebase rule holds on `.node` too (r3-11) |
| MCP retained-evidence session | `binary_session`→`open_binary`→`inspect_analysis_view` paging (`parent_evidence_id`, coverage cursors) — CLI-inexpressible; retention epoch-scoped, `evidence_links` pin | live `rea` MCP tools | `record_pairs`→`status:changed` demonstrated r3-14; view gate: only inspect_binary_layout/analyze_js/analyze_function parents pageable |
| Verb families | `xrefs` (inbound-only, GOT+DWARF decomp), `trace` (literal feature, no from/to), `read-bytes`, `address-to-file-offset`, `function` dossier, `instructions` — address is POSITIONAL on all | `rea xrefs <path> <addr>` on libjq | exercised r3-15: read-bytes byte-exact vs objdump; addr→file-offset confirms rebase |
| Recorded crashes (mechanism) | `inspect_recorded_crash <elf-core>` — `coredumpctl dump` output is already decompressed ELF (no `zstd -d`); **32 MiB decompressed cap**; `REA_PWNTOOLS_PYTHON` persistent venv `~/.local/share/kaidoku-pwnenv` | live run on a ≤32MiB core | crash-godot core → `ev_3686f9…`, 27 regs × threads, notes retained (r2-06); `inspect-binary-layout` first-held r4-13 (jq full RELRO observed) |
| Evidence discipline | `detail:"summary"` + `parent_evidence_id` paging; `get_evidence_bundle` filters; `inspect-evidence-bundle`; `--snapshot <path>` JSON bundle | every Core probe emits `evidence_id` + `limitations[]`/`unknowns[]` | snapshot is evidence persistence, not a Ghidra DB cache (timed) |
| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx, `7z`, `xxd`, `radare2`, `strace`, `upx`, `rizin`; pacman-contrib package installed (rechecked 2026-10-20, round-19 w1 `FallbackReaders.md`, not installed by this round) | `command -v <tool>`; `pacman -Q pacman-contrib` | absent: `cabextract`, `ltrace`; historical 2026-10-13 list omitted the subsequently installed rizin and pacman-contrib |

Cross-lane registry this lane maintains: the REA surface map — per-client
registration state, provider availability, provider env keys, and the on-host
artifact inventory — kept in `corpus/knowledge/`, refreshed by `rea doctor`
each round. Map entries are live state only: a version drift past the historical Kimi 6.4.0 pin
is refreshed here, never re-bases a sibling lane's frozen receipt command
or historical artifact path, and never stands for that lane's current
runtime capability (routing:
`../revenger-shokunin/reports/round-1/connector.md:25,33-36`).

## Frontier

Claimed in MINT.md, not yet held. Each moves to Core by a `LOG.md` entry citing
the corpus entries that earned it. [r5-audit C1: six stale pre-round-4 bullets
pruned from this section — managed PE/CLI, firmware, offline ELF layout,
Android decode, runtime-obs extended, cross-version extended — each now held
in "Round-4 additions to Core" below; reconciliation follows the r4-16
frontier rescan]

- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136
  procedures via Ghidra). Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7).
- **Recorded crashes >32 MiB** — mechanism held (Core), and a sub-cap organic
  core is now reachable (chrome_crashpad 17.6MB, probed exit 0); the huge
  organic cores still exceed the cap; no cap-raising knob exists. Retention decays oldest-first.
- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
  JEB (unprobed). Engine installs are operator-owned.
- **macOS-only surfaces** — Mach-O/plist/LLDB/asset-catalog ops report
  `unsupported_host` on Linux; recorded so the lane never claims them.
- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
  carrier (arc3-r4); selectors stay bare hashes (no signature DB → no name resolution).

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


### Round-4 additions to Core (verified 2026-10-13)

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| Firmware regions + extract | `REA_BINWALK_COMMAND=/usr/bin/binwalk` (3.1.0), `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4) | `inspect-firmware-regions`, `extract-firmware` | GSP blobs: 56/156 regions mapped (`ev_0388cb9a…`, `ev_4009f834…`); nvidia ucodes correct-empty stubs; pkg.tar.zst 100% carved (r4u-01/03) |
| JavaScript source recovery | `REA_WAKARU_COMMAND` → `@wakaru/cli-linux-x64` ELF (**not** the node shim — REA wraps providers in `prlimit --as=1GiB` which V8 isolate init cannot survive) | `recover-javascript-sources <file> <outdir>` (file arg, not dir) | `ev_5cb1856a…` on lodash.min.js → deobfuscated modules + provenance map (r4u-05, fix applied .bashrc:63; **round-12 audit correction** — this cell cited `ev_4898906e…`, an id that appears nowhere in the corpus; r4u-05's recorded success id is `ev_5cb1856a…`) |
| Android deep analysis | `REA_JADX_MCP_JAR` (jadx-headless-mcp 0.7.1-all, sha256 `6e5eacf5…`), `REA_APKTOOL_COMMAND` [r5-audit C8: key name corrected to the one REA 6.4.0 actually reads — exported at `.bashrc:61` → `/usr/bin/apktool`] | `inspect-android-package`, `decode-android-resources`, `inspect-android-method` | Godot APK: 1,925 classes, decoded manifest, real Java decompile `ev_ec92f4d1…` (r4u-02) |
| Managed IL (two-tool map) | `REA_DOTNET*` keys unset — REA managed verbs are provider-free; `dnfile 0.18.0`+`dncil 1.0.2` pip pkgs + RVA shim over `dnPE.get_data` | `inspect-managed-artifact`, `inspect-managed-members`; dnfile+dncil decode | Pinta.dll `ev_471d085b…`; Pinta.Core 2,594/2,594 + Pinta.dll 650/650 method bodies via dnfile/dncil incl. REA-refused `0xfd1d` class (r4-11, r4u-04) |
| `.jsc` V8 bytecode | `ELECTRON_RUN_AS_NODE=1` + electron version matching the target's V8 (typora = V8 14.8 → electron 42.2.0); host node 24/V8 13.6 REJECTS cached data | `electron --print-bytecode <jsc>` under run-as-node | typora `atom.compiled.dist.jsc` → 530KB Ignition disassembly, 116 function blocks (r4-07) |
| Runtime observation verbs | self-launched CDP/V8-inspector targets (r3 recipe); `node --inspect` needs a real file target (bare `file://` → `unsupported_location`) | `observe-web-session`, `observe-web-execution`, `observe-javascript-runtime`, `reconcile-javascript-runtime` | all held r4-08; `capture-electron-scenario` remains typed refusal (Playwright handshake, not app launch) |
| Binary layout | `REA_PWNTOOLS_PYTHON` persistent venv `~/.local/share/kaidoku-pwnenv` | `inspect-binary-layout <elf>` | `/usr/bin/jq` full RELRO + canary/NX **observed** (r4-13) |
| ADB client (device-free) | `REA_ADB_PATH` optional — PATH fallback works | `inspect-adb-client`, `list-adb-devices` | provider adb 37.0.0, honest `devices:[]`; only 2/24 verbs are serial-free; dead-serial taxonomy mapped (r4u-06) |
| AppImage inner payload | unblob carve at `--appimage-offset` or `7z` on carved squashfs; then `analyze-javascript-application` on inner asar | extract → asar analyze | Grok_Bot AppImage = Anysphere/Cursor `sand`, 715-member asar fully mapped (r4-15) |

### Round-4 frontier (post-unlock)

- **RISC-V analysis** — `target_unavailable` gate pinned (`binaryTarget.js:105`
  ELF e_machine allowlist), bypassed via e_machine patch + language override
  (r5-01: `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md`); full 29 MB EXEC
  via direct `analyzeHeadless` (10,766 functions @900 s cap).
- **>90 MB PE scale wall** — CLOSED (arc2-r7: the same 91.6 MB Godot ARM64 PE
  held, 75,218 procedures, 7.9G/9G peak, zero OOM, three validated analyzers
  disabled; arc2-r8's no-disable control OOM-killed at 9G in 4m42.945s; not
  OOM at this cap, RSS ~2.36GB vs -Xmx2G headroom). Residual: rerun id-stability
  UNKNOWN; no natural unmitigated hold exists at this cap. The pre-r7 "Next:"
  remediation is superseded by the validated analyzer-disable recipe.
- **`.jsc` → source mapping** — Ignition disassembly held; a View8/jsc2js-style
  bytecode-to-source mapper is the next frontier for typora's real app.
- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback
  covers the carved-image path today.
- **adb device surface** — 22/24 verbs need a live device/emulator;
  `collect-adb-bugreport` blocks ~10min on dead serial.
- **Signal/1Password-scale asar analysis** — 1Password's 40.7MB asar + 188MB
  native core are mapped (r4-06); signal's 38.5MB asar (1,866 entries) mapped
  via a scoped `--artifact-format directory` run past three honest walls, and
  its stripped Rust `.node` addons recovered down to the neon registration
  surface (r4-05, r4-14) [r5-audit C1: lane landed — stale pending-status
  wording removed].
- **Cross-version residuals** — `compare-application-versions` EXERCISED on all
  three input classes (r12-02: JS + managed; r14-01: runtime-reconcile, `ev_8f0ac46c…`);
  multi-version pacman pairs beyond expac exercised (r4-10: op 2.34.1→2.40.0, qpdf control)
  [r5-audit C1: merged from the pruned Frontier bullet — its `compare_javascript_export_shapes` item is now held (Core, r4-09)].
- **Operator-gated, still absent**: IDA (`REA_IDA_MCP_CONFIG`), Hopper
  (`HOPPER_LAUNCHER_PATH`), JEB.
