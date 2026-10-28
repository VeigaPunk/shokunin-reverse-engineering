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
| REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `.ufo/waves/round-19/evidence/doctor/` (doctor-6.5.0.txt, doctor-6.7.0.txt); historical readiness probe 2026-10-13 |
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

- **PE subtypes** — x86-64 AND ARM64 both held (r3-08: cli-arm64.exe, 136 procedures via Ghidra). ARM64X synthetic exported-leaf native-view import/overview is now bounded Core (round 32, below);
  published hybrids, dual-view/EC recovery and internal-function analysis remain Frontier. The 91MB Godot ARM64 template is plain ARM64 and held (arc2-r7).
- **Recorded crashes >32 MiB** — mechanism held (Core), and a sub-cap organic
  core is now reachable (chrome_crashpad 17.6MB, probed exit 0); the huge
  organic cores still exceed the cap; no cap-raising knob exists. Retention decays oldest-first.
- **Alternate providers** — IDA (`REA_IDA_MCP_CONFIG` unset), Hopper (absent),
  JEB (unprobed). Engine installs are operator-owned.
- **macOS-only surfaces** — Mach-O/plist/LLDB/asset-catalog ops report
  `unsupported_host` on Linux; recorded so the lane never claims them.
- **EVM bytecode (extended)** — selectors held on synthetic dispatcher
  (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
  carrier (arc3-r4); names are labelled candidates from saved signature-DB lookups, never verified (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`).
  Round 28 (claim R28-C1 missed, 60 of 61 runs; Frontier status unchanged): on 187 held-out selectors the round-25 primary naming rule was observed at named 137, right 137, wrong 0 (`corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md`). openchain's `filtered` flag is set only for selectors on Sourcify's 36-key canonical list; it was re-observed on 10 of those keys, the deployed revision is not identified, and the test is not held out (`corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`).
  Round 29 (R29-C1 and R29-C2 targets met as measured; Frontier status unchanged): on 152 selectors absent from the lane at the base, from 15 of 16 fresh solcjs-0.8.37 stub carriers holding published function lists, the unchanged round-25 primary rule scored named 122, right 122, wrong 0, no name 30 against each carrier's compiler ABI, not a deployed contract (`corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`). The Sourcify `filtered` rule held on 178 never-fetched selectors, 0 mismatches of 252 entries (38 `true`, all under 19 of 26 canonical keys; 214 `false`), which supersedes the round-28 clause "the test is not held out"; the deployed revision is still not identified, and 6 of the list's 31 kept signatures belong to other selectors (`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`).

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
- **Tooling, dated 2026-10-26** — the 2026-10-19 operator directive
  (`/home/vgpnk/.omp/agent/RULES.md`) lets an agent install or upgrade the
  tooling its task needs through official channels only, with tool, version,
  channel and reason recorded (round 36: sasquatch 4.5.1, official onekey-sec
  deb, into `~/.local/bin`); `rea setup` runs and client-config edits
  (registration refreshes for `claude_code`/`codex`/`grok_build`/`opencode`/
  `pi`) stay **operator-owned** and lane-untouched. Full-system upgrades go through tsukuroi-shokunin's update-safety gate first (that ground is tsukuroi's), partial upgrades (`pacman -Sy <pkg>`) are never run, and pacman stays paused host-wide per the 2026-10-20 orchestrator ruling.


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
  covers the carved-image path today. [2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; big-endian/AVM stays here. Round 38: standard BE v4 measured through `sasquatch-v4be` (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`), not promoted — R38-C1 honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap. Round 39: standard BE v4 is Core — see `## Round-39 additions to Core` (`2026-10-26-r39-be-squashfs-v4-core`); AVM-BE and vendor-mangled stay here.]
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

### Round-20 additions to Core (verified 2026-10-20)

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| WASM interface inspect/compare | `REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin` (official release, S041; REA requires the exact banner of three WABT tools) | `inspect-wasm-artifact <module>`; `compare-wasm-interfaces <json>` with two inline inspect Evidence records | 4 shipped modules, 3 compare pairs (`corpus/knowledge/2026-10-20-r20-wasm-interfaces.md`) |
| Rizin command observation | `rizin` on PATH (`/usr/bin/rizin`), optional `REA_RIZIN_COMMAND`; REA runs `rizin -N -q -c <cmd> <path>` | `execute-rizin-command <path> iI` | jq, libjq, round-2 PE (`corpus/knowledge/2026-10-20-r20-rizin-command-observation.md`); unrestricted shell-capable surface — read-only info commands only |
| objdump target list | host GNU objdump; no artifact argument | `list-objdump-architectures` | equals host `objdump -i`, `subject: null` (`corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md`) |
| HarmonyOS application graph | none; input is `inspect-artifact` inventory Evidence | `project-harmony-application-graph <json>` | synthetic Stage/FA HAPs only (`corpus/knowledge/2026-10-20-r20-harmony-application-graph.md`) |

### Round-22 catalog dispositions

REA6.5.0, observed 2026-10-21. These rows calibrate gaps and adjacent ground;
they do not absorb revenger's contested runtime province. ADB rows are explicit
`REA_ADB_PATH=/usr/bin/false` unavailable-client controls, NOT observations of
device absence or of the real adb binary. No device operation was dispatched.
The Frida enumeration provider was available; the missing impossible PID
does not establish provider absence. No real process was attached or hooked.
Run files retain producing argv/stdout/stderr/exit. The five ADB overrides
are explicit; the manual missing-Cutter retry has no env_overrides member,
so its whole ambient environment is not claimed captured. The counter grades
only the stated observed field/code, not reason/placement semantics or all
enumeration contents. Those remain manual admission decisions; the final
suite separately compares receipts with run stdout/argv/exit and ADB overrides.

| verb | placement | probe | observed | receipt | reason |
|---|---|---|---|---|---|
| inspect-packet-fields | frontier-blocked | inspect-packet-fields | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-packet-fields.json | Explicit TShark configuration unavailable for this request; no field registrations examined |
| inspect-packet-capture | frontier-blocked | inspect-packet-capture | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-packet-capture.json | Supplied empty pcap not dissected because TShark configuration unavailable; not a traffic-absence claim |
| inspect-pcap-client | frontier-blocked | inspect-pcap-client | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-pcap-client.json | Selected tshark command ENOENT; capinfos availability not independently established |
| inspect-pcap-capture | frontier-blocked | inspect-pcap-capture | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-pcap-capture.json | Selected tshark command ENOENT; no packet summary capability acquired |
| list-cutter-sessions | frontier-blocked | list-cutter-sessions | ok-empty:sessions | .ufo/waves/round-22/evidence/c2/list-cutter-sessions.json | Empty discovered sessions at this instant only; security status not_checked |
| cutter-command | frontier-blocked | cutter-command | error:invalid_request | .ufo/waves/round-22/evidence/c2/cutter-command-missing.json | Well-formed nonexistent UUID/generation rejected; earlier malformed argument receipt retained separately |
| list-frida-devices | adjacent | list-frida-devices | ok-field:cleanup_error=null | .ufo/waves/round-22/evidence/c2/list-frida-devices.json | Provider successfully enumerated local descriptors; not provider absence, remote connection, or lane ownership |
| list-frida-processes | adjacent | list-frida-processes | ok-field:device_id="local" | .ufo/waves/round-22/evidence/c2/list-frida-processes.json | Provider returned local process names/PIDs; no command lines, hooking, or runtime ownership acquired |
| instrument-with-frida | adjacent | instrument-with-frida | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/instrument-with-frida.json | PID2147483647 is not a real selected process; missing-process refusal is not provider absence |
| inspect-adb-package | frontier-blocked | inspect-adb-package | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-adb-package.json | Explicit false-client control refused version inspection before device contact; real client/device unexamined |
| list-adb-services | frontier-blocked | list-adb-services | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/list-adb-services.json | Explicit false-client control only; no binder-service list observed |
| inspect-adb-window | frontier-blocked | inspect-adb-window | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/inspect-adb-window.json | Explicit false-client control only; no focused window observed |
| start-adb-activity | frontier-blocked | start-adb-activity | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/start-adb-activity.json | Explicit false-client version refusal; no activity start or device mutation |
| stop-adb-app | frontier-blocked | stop-adb-app | error:capability_unavailable | .ufo/waves/round-22/evidence/c2/stop-adb-app.json | Explicit false-client version refusal; no app stop or device mutation |

### Round-22 narrowly added static ground

`identify-flutter-build` parsed Godot as a negative and Saber as Flutter-positive
with **partial** coverage; both observations and target identities are in
`corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` and
`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md`.
`inspect-dart-aot` refused Saber's missing dynamic snapshot symbols and is not
held. Identification does not imply source recovery or runtime observation.

`debug-with-gdb` and `debug-with-rizin` remain **Adjacent and not held** in this
round; replacement work performed no debugger/target execution. Correct aliases in the
counter are grounded in REA6.5.0 source and synthetic controls only; they grant
no ownership or authorization to run a tracer. The sigrok verbs remain
unexercised; no recording decode or hardware contact is claimed.

### Round-23 offline envelope additions — 2026-10-21

This dated section supersedes the round-22 instant's statement that sigrok
verbs were unexercised, without rewriting that historical partition.
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` (current S059/S060/S062; S058 superseded)
holds REA6.5.0 decoder discovery on the local launcher and file-only UART
decode on one synthetic and one digest-pinned public recording. Discovery
is a tool-subject observation with a signature-module load failure; no
full-installation, hardware isolation or acquisition capability is claimed.
Offline recording envelopes fit artifact evidence; hardware acquisition and
device control remain Adjacent/unowned, not absorbed into this province.

`corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md` (current S063; S061 superseded)
holds static inspect-dart-aot on the exact archived Saber1330203 APK whose
libapp exports the supported four dynamic snapshot symbols. Its section/header
coverage is complete while overall and string-pool coverage are partial. R22's selected
Saber1360103 refusal stays valid and unchanged; no universal SDK/build,
decompilation or target execution claim follows.

The six-verb completeness denominator remains fixed. Both debugger verbs
remain unheld/Adjacent; kaidoku/revenger arbitration is still open.
No process attach, live device operation or general signal-analysis
ownership is earned by these offline observations.

### Round-23 current T1 readiness — explicit supersession after W2

This section supersedes the **current-readiness** statements in
`### Round-22 narrowly added static ground`, including both “unexercised”
and “no recording decode … is claimed”, and supersedes the earlier round-23
paragraph wherever it omits these limits. Round numbers and these named
sections, not the shared calendar date, identify the supersession. R22's
actual selected-carrier refusal and historical observations remain intact.

| Frozen T1 verb | Current bounded holding |
|---|---|
| identify-flutter-build | Held from R22; unchanged exact APK witnesses, not a new round-23 verb |
| inspect-dart-aot | Conditionally held on selected x86_64 Saber1330203, S063: supported four-symbol headers with complete libapp coverage; overall/string_pool partial. R22's refusal did not echo its selected ABI, so no causal SDK/ABI-boundary conclusion is made |
| debug-with-gdb | Not held; Adjacent, no permitted live debugger run |
| debug-with-rizin | Not held; Adjacent, no permitted live debugger run |
| inspect-signal-decoders | Held only as launcher-subject discovery/help; returned catalog excludes the failed signature module, not comprehensive decoder functionality |
| decode-signal-recording | Held on the exact synthetic/public offline recordings; literal annotations and diagnostics, not lossless traffic recovery, live acquisition or device execution |

The actual IDs and subject digests are now explicit in LOG's round-23
bound-holding table. The former R22 “Dart not held” readiness statement is
superseded only by this different selected four-symbol artifact; it does not
turn the original refusal into a success.

## Adjacent — round-23 explicit exclusion

- Hardware signal acquisition, live device control and general hardware
  protocol-analysis ownership remain unowned/Adjacent. Offline REA recording
  envelopes do not establish hardware isolation or resolve sibling ownership.
- Both live debugger verbs remain Adjacent/unheld; the kaidoku/revenger
  arbitration question remains open.

## Round-24 saved-capture holdings — 2026-10-21

This dated section supersedes the round-22 `frontier-blocked` placement of
`inspect-packet-fields`, `inspect-packet-capture`, `inspect-pcap-client` and
`inspect-pcap-capture` (table above) for the current host state, without
rewriting that table: the round-22 refusals were true when no TShark existed.
`corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md` (S064–S067) holds
all four verbs on public test captures from the signature-checked Wireshark
4.6.9 source tree and on the installed dissector registry, using the lane's
recorded local TShark/capinfos 4.6.9 build (`.ufo/waves/round-24/tool-pins.json`).

| Verb | Current bounded holding |
|---|---|
| inspect-pcap-client | Held as tool-subject configuration report; no capture read |
| inspect-pcap-capture | Held on saved pcap/pcapng summaries (derived); embedded TLS secrets in a test capture are a property of that input |
| inspect-packet-fields | Held as installed-registry listing; not traffic |
| inspect-packet-capture | Held as TShark field output under prlimit on a saved capture; not protocol-semantics verification |

Missing or unrunnable TShark returns the round-22 refusal state; replacing
it or its libraries with another runnable installation need not be refused.
The recorded digests identify this build, not a full dependency lock.
The frozen R23 six-verb T1 is unchanged (4/6).

## Adjacent — round-24 explicit exclusion

- Live packet capture (`dumpcap`, interfaces, promiscuous mode), analyst-
  supplied decryption keys and network-forensics case ownership remain
  unowned/Adjacent; saved-capture envelopes do not absorb them.
- Live debugger verbs remain Adjacent/unheld; kaidoku/revenger arbitration is open.

## Round-27 renamed-copy identity and cross-pin attribution — 2026-10-22

Two dated additions to Core. Neither retires a Frontier bullet and neither rewrites the
Core table above: the Frontier list (PE subtypes, recorded crashes above 32 MiB, alternate
providers, macOS-only surfaces, EVM bytecode extended) is unchanged by this round.

- Native reader evidence-ID identity at `rea-agents@6.5.0` now rests on two carriers and a
  renamed copy: eight verbs on `/usr/bin/jq` (`0x103fa0`) and eight on `/usr/bin/tinyxxd`
  (`0x103d40`), each with a base run, a same-path repeat, and a byte-identical copy under
  another directory whose file name and extension also changed. 10 of 16 content-keyed, 6 rename-sensitive, 0 unstable. Against round 26, `analyze` and `inspect` turn rename-sensitive because the file extension reaches `normalized_result.document` (the Ghidra program name `target-<sha256[0:12]><suffix>`), the five address verbs stay content-keyed and `inspect-binary-layout` stays path-sensitive. Limits: one
  pin, one Ghidra build (12.1.4), one address per carrier, default parameters, and the copy
  moves directory, file name and extension together
  (`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`; table
  `corpus/evidence/round-27/c1/table.tsv`).
- Cross-pin attribution of a saved envelope is now a lane capability:
  `tools/round-27/xpin-attribute.mjs` attributes an envelope to the 6.5.0 rule, the 6.7.0
  rule, both or neither, from its bytes, using each installed package's own canonical
  digest code (package roots `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` and
  `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`). The 6.7.0 side is a rule fit
  over 6.5.0-produced evidence objects, not a 6.7.0 run.

Round-27 outcome note (appended after the falsify wave): R27-C1 missed its frozen target (15 of 16 rows under its counter; one genuine byte-identical repeat refused), and the identity lines above hold for the Ghidra provider on Linux with extensions that do not change the route; see the corrections section of `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`.

## Round-30 `inspect-rust-binary` positive class and refusal signatures — 2026-10-23

Addition to Core (the Core table above is not rewritten; the Frontier list is unchanged by this round):

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| Rust dependency metadata (cargo-auditable `.dep-v0`) via `inspect-rust-binary` | none (REA's own container and zlib/JSON reader, provider-free); `rea-agents@6.5.0` | `inspect-rust-binary <image> --format json --full-output` on an image carrying one `.dep-v0` section (ELF, PE, thin Mach-O; `__DATA,.dep-v0` on Mach-O) | 16 of 16 uv 0.13.0 PyPI wheel members (ELF x86_64/aarch64/riscv64, PE x86_64/arm64, Mach-O x86_64/arm64): package multiset, edges, root, kind, section offset and size equal an independent decode (`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`, ids in its Results table); 19 of 19 code-predicted accept/refuse signatures on ELF mutants (`corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`; decision table in SKILL.md) |

Before round 30 the lane held only `auditable_metadata: null` runs of `inspect-rust-binary` (no section). Limits: one producer (5 distinct package lists and 7 distinct dependency documents, one per wheel, across 16 carriers), one pin, Linux host; the embedded list is file content and is not authenticated by REA.

Correction (R29-C1 carrier provenance, round 30, routed defect 5 of `corpus/lessons/round-29-verifier-spotcheck.md`): only carrier n04 rests on an opened source (S088); the other 15 lists were written from the L1's knowledge of the standards and are author-selected names, not opened published interfaces.


## Round-31 additions to Core (verified 2026-10-23)

Addition to Core for REA's SQLite reader (the Core table above is not rewritten; the Frontier list is unchanged by this round). The lane's one earlier run of this operation (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`, scope `inventory`, one pnpm index copy) had not entered PROVINCE.

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| Offline SQLite schema via `inspect-sqlite-database` (`inspect_sqlite_database`) | none (REA's own snapshot copy plus an owned node:sqlite worker, SQLite 3.53.4 in node v24.21.0; provider-free); `rea-agents@6.5.0` | `inspect-sqlite-database <file> --schema-scope database --format json --full-output` on a quiescent database file with no hot journal | 12 of 12 published files (5 PROJ `proj.db` from pyproj wheels, 2 Chinook v1.4.5 databases, 5 GeoPackages with R*Tree virtual and shadow tables): every table, column, index, view and trigger equals an independent reader (`corpus/knowledge/2026-10-23-r31-sqlite-positive.md`, evidence ids in its Carriers table); refusal and edge table in SKILL.md (`corpus/knowledge/2026-10-23-r31-sqlite-refusals.md`) |

Limits: three schema families, one pin, Linux host, all files UTF-8 without WAL. The reader reports SQLite's own catalog; it is not an integrity check, it never executes views or triggers, and its row sample has unspecified order. Input above 256 MiB (database plus WAL), a non-empty journal with a nonzero header, and symlinked database or journal paths are refused (SKILL.md table).

## Round-32 additions to Core (verified 2026-10-23)

| Surface | Verified holding | Entry |
|---|---|---|
| ARM64X hybrid PE through REA 6.5.0 `inspect` | Native-view `binary_overview` on twelve pinned, author-built exported-leaf DLLs; raw COFF 0xAA64 plus CHPE ARM64/ARM64EC ranges; ordered segments and native-view procedure counts checked against the frozen byte oracle and predictions. Not dual-view recovery, decompilation or execution | `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` |

The frozen carriers and original envelopes are in `corpus/evidence/round-32/c1/`; source definitions/input provenance are S099/S098. The fixture builder is not a general PE build tool or a claim to PE-format maintenance. Published hybrids, internal functions and the EC view remain unverified Frontier scope.

## Round-36 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| sasquatch squashfs recursion | no new REA key — unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` runs `sasquatch` from `PATH` (`sasquatch-v4be` is its big-endian sibling, unmeasured); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); sasquatch 4.5.1, official onekey-sec deb, at `~/.local/bin/sasquatch` (sha256 `ad02d27a…`) | `extract-firmware` on the four frozen carriers — K1/K2 synthetic LE v4 squashfs (xz; gzip 4 KiB blocks, nested dirs, a symlink), K3/K4 neovim v0.12.6 `nvim-linux-{x86_64,arm64}.appimage` — against the frozen `/usr/bin/unsquashfs` 4.7.5 regular-file oracle | carriers `corpus/evidence/round-36/c1/carriers.json`; receipts `corpus/evidence/round-36/c1/` (oracle 3, 4, 2,130, 2,130 regular files, all published after, none before; every `after.json` carries zero `missing-extractor-dependency` gaps against one `dependencies: ["sasquatch"]` gap in the paired `before.json`, the only remaining after-gaps being `unpublished-entry` 0/1/2/2 for symlinks); `tools/round-36/c1-counter.py`; entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |

Frontier note, 2026-10-26: the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)` (`PROVINCE.md:156-157`; `PROVINCE.md:149-150` before this round's 7-line Adjacent addition) is superseded for little-endian SquashFS v4 as measured above; its "(AUR-only)" was wrong as a route statement — unblob's own README documents the Debian-package install (`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`). Big-endian/AVM and vendor-mangled images stay Frontier.

Round-38 note, 2026-10-26: the row's aside "`sasquatch-v4be` … unmeasured" is history as of round 38 — standard big-endian v4 was measured through `sasquatch-v4be` on four frozen carriers (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`) and **not promoted**: R38-C1 stopped under its first-freeze counter on K2's `unpublished-entry` symlink gap. Big-endian SquashFS stays Frontier. Round 39: superseded for standard big-endian v4 by `## Round-39 additions to Core` below (`2026-10-26-r39-be-squashfs-v4-core`).

## Round-39 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| standard big-endian SquashFS v4 recursion (`squashfs_v4_be`) | no new REA key — unblob 26.6.4 runs `sasquatch-v4be -be` from the child `PATH` for big-endian v4 (AVM marker excepted); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1 at `~/.local/bin/sasquatch-v4be` | `extract-firmware` (rea-agents 6.5.0) on six frozen carriers — K1/K2 round-37 synthetic BE gzip, K3/K4 the unblob 26.6.4 BE fixtures, K5 round-39 BE gzip (UTF-8 names, 2 in-tree + 1 escaping link), K6 round-39 BE xz (compression id 4) — against independent regular-file oracles and frozen symlink tables | entry `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`; carriers `.ufo/waves/round-39/c1/carriers.json`; receipts `corpus/evidence/round-39/c1/K{1..6}/after.json`: every oracle file published (5, 3, 4, 4, 10, 8), no failed chunk, gaps exactly one `unpublished-entry` per in-tree link (0, 1, 0, 0, 2, 1), escaping links removed; claim R39-C1 (`plans/round-39-claims.md`) |

Round-39 frontier note, 2026-10-26: the big-endian part of the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)` (`PROVINCE.md:156-157`) and the round-38 note above are superseded for standard big-endian SquashFS v4 by the row above (`2026-10-26-r39-be-squashfs-v4-core`). AVM-BE bodies and vendor-mangled images stay Frontier. The little-endian part of the same bullet was superseded in round 36 by `2026-10-26-r36-sasquatch-squashfs-recursion` (routed defect R36-CL2: the earlier pointer named only the Core heading).

## Round-40 measured, not promoted (R40-C1 honest stop)

Recorded 2026-10-26 after scoring: the frozen counter `tools/round-40/c1-counter.py` at `42c10a58` matched 3 of 4 carriers (exit 1). L2 failed only `nonregular_unpublished_ok`, a suffix false positive (the regular file `usr/bin/busy` ends with the symlink path `bin/busy`); its receipt publishes no symlink path (`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`). The row below is a measurement record, not a Core promotion; promotion waits for a re-frozen counter.

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`, AVM layout: big-endian fields, little-endian metadata block lengths, `mkfs_time == bytes_used`) | no new REA key — unblob 26.6.4 runs `sasquatch-v4be` without `-be` when the AVM marker holds; `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1; `extract-firmware --max-depth 1` (a vendor member exceeds the 10000-entry staging budget at the default depth) | `extract-firmware` (rea-agents 6.5.0) on four frozen carriers — V1 FRITZ!Box 6490 Cable FRITZ!OS 07.57 member, V2 FRITZ!Box 6820v1 LTE FRITZ!OS 07.30 member (vendor bytes fetched by `tools/round-40/fetch-vendor.py`, never committed), L1/L2 lane-built AVM layout xz/gzip | every oracle regular file published (697, 8, 7, 6), one `unpublished-entry` gap per symlink plus one `depth-limited`, no failed chunk; receipts `corpus/evidence/round-40/c1/`; counter `tools/round-40/c1-counter.py` with a rerun binding; entry `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` |

Round-40 frontier note, 2026-10-26: AVM-BE is **measured, not promoted** — the genuine AVM layout extracted with every oracle file on two vendor members and two lane-built images (`2026-10-26-r40-avm-be-squashfs-core`), but R40-C1 stopped at 3/4 on a counter false negative, so the round-39 note's AVM sentence still stands until a re-frozen counter scores it. Still Frontier: AVM-BE bodies (this measurement included), LE AVM members (`hsqs`), nested `filesystem_core` images below depth 1, other vendor-mangled images.

## Round-41 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`) | no new REA key — unblob 26.6.4 appends `-be` to `sasquatch-v4be` only when the AVM marker `mkfs_time == bytes_used` is false (S112 lines 44-50), so a genuine AVM body runs `sasquatch-v4be` WITHOUT `-be` (S121 lines 664-669, 4389-4400); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1; `extract-firmware --max-depth 1` (a vendor member exceeds the 10 000-entry staging budget at the default depth) | `extract-firmware` (rea-agents 6.5.0) on four frozen carriers no extractor touched before the freeze — V3 FRITZ!Box 5490 FRITZ!OS 07.31 member `./var/tmp/filesystem.image`, V4 FRITZ!Box 5491 FRITZ!OS 07.31 the nested `filesystem_core.squashfs` carved to its own `bytes_used` (32 720 860 B), L3 lane-built AVM layout xz and L4 lane-built AVM layout gzip (both carrying in-tree and absolute symlinks and both-direction path collisions) — against the frozen reader oracle; vendor bytes fetched by `tools/round-41/fetch-vendor.py` (url -> image sha256 -> member sha256 -> carve -> pin), never committed | entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`; every oracle regular file published at its exact path relative to the chunk extract root with the same sha256 V3 8, V4 6349, L3 13, L4 14 files published, no regular file at a non-regular entry's exact path, gaps one `unpublished-entry` per retained symlink plus one `depth-limited`, no failed chunk, `plus-extractor` projection reproduced by the counter's own rerun; counter `tools/round-41/c1-counter.py` `carriers_matched scored after this commit` exit see `.ufo/waves/round-41/l1/scores/` at `the commit that adds this text`; receipts `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` |

The row above supersedes the status of the block below for the genuine AVM layout only: the layout was
correctly measured in round 40, and the block's own status line was a counter false negative. A standard
big-endian body whose AVM marker was stripped stays governed by `## Round-39 additions to Core`, and
LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1 and other vendor-mangled
images stay Frontier.

Round-41 frontier note, 2026-10-26: for the genuine AVM layout the block `## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); its `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not from the images, and this note also supersedes the AVM sentence of the round-39 note. Still Frontier: LE AVM members (`hsqs`), AVM kernel images, nested `filesystem_core` images below depth 1, other vendor-mangled images.

## Round-42 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| `squashfs_v3` and `squashfs_v3_ddwrt` (SquashFS v3, LZMA bodies, both byte orders) | no new REA key — unblob 26.6.4 runs plain `sasquatch -le`/`-be` for every v3 chunk (S112 :39-54; logged on each carrier); `REA_UNBLOB_COMMAND` = unblob 26.6.4 through `tools/round-42/unblob-logtee.sh`; `extract-firmware --max-depth 1` | `tools/round-42/c1-counter.py` against the freeze `d1681696`; oracle backhand-cli 0.25.5 (v3_lzma) + 7-Zip 26.04 | four published images (OpenWrt 8.09.2 atheros BE, OpenWrt 8.09 x86 LE, DD-WRT v24 mega LE, DD-WRT v24 Fonera BE): every oracle regular file published at its exact path, one `unpublished-entry` per symlink, one `depth-limited`; entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` (SquashFS v3) |

Round-42 frontier note, 2026-10-26: SquashFS v3 (`squashfs_v3`, `squashfs_v3_ddwrt`) moved Frontier → Core with `2026-10-26-r42-squashfs-v3-core`; the producer statement `2026-10-26-unblob-format-matrix` stays as written. Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, LE AVM members, AVM kernels, nested sub-images below depth 1.

Round-43 frontier note, 2026-10-27: the published sasquatch package inventory is now grounded in
`2026-10-27-sasquatch-release-matrix` (8 tags, three Debian architectures from `v1.0.1`; `v1.0` is
amd64-only). This is packaging availability, not an extraction/compatibility result; no sasquatch release asset was
downloaded or run this round. The round-36 "AUR-only" route wording remains superseded by the round-36 note above,
and vendor-mangled packages/images remain Frontier.

## Round-44 measured, not promoted (R44-C1 honest stop)

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| `squashfs_v1` and `squashfs_v2` (SquashFS v1/v2, four standard fixtures) | no new REA key — unblob 26.6.4 names the handlers and selects `sasquatch -le`/`-be` by byte order (S108 :24-26, :51-54, :101-102, :158-159; S110) | REA 6.5.0 `extract-firmware` and the independent `unsquashfs` 4.7.5 oracle on four committed MIT fixtures | The counter matched 4/4 and published every oracle file, but the frozen R44-C1 claim and counter disagree about `parameters.output_directory`: the claim required the committed evidence path, while the counter accepts only the `/kaidoku-r44/` scratch provenance. The score therefore does not satisfy the frozen predicate; no Core promotion is claimed. |

Round-44 frontier note, 2026-10-28: SquashFS v1/v2 were measured on four standard fixtures (`squashfs_v1`, `squashfs_v2`; counter 4/4), but R44-C1 is not promoted: the frozen claim's output-directory clause disagreed with the counter's `/kaidoku-r44/` provenance binding. SquashFS v1/v2 remain Frontier pending a new pre-data freeze that aligns the predicate and instrument. Still Frontier: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.
