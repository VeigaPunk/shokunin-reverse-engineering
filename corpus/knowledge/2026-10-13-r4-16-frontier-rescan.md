<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/16-frontier-rescan.md. -->

# 16 — Frontier rescan + unexercised-verb census (round 4)

Axes: **drift-detection** (did anything move since r3?) / **census-completeness** (every
never-exercised op named with its real gate) / **cheap-closure** (ops with no gate get
exercised in-lane, not queued) / **boundary-honesty** (refusal vs success path kept
distinct). All probes read-only; new evidence bundles live in rea-managed dirs and `/tmp`.

## Candidate: `capabilities` matrix re-verified — zero drift vs the r2 baseline, byte-pinned by catalog digests

- claim: `capabilities --format json` (134,994 B envelope, 8 top-level keys) still
  reports the identical 18-op host matrix r2 recorded: **8 `available:true`**
  (`decode_interface_builder`, `extract_artifact`, `inspect_artifact`,
  `inspect_keyed_archive`, `inspect_managed_artifact`, `inspect_managed_members`,
  `inspect_managed_native_boundaries`, `trace_dylib_resolution`) and **10
  `unsupported_host`** (all macOS/`assetutil`-gated). Provider candidates unchanged:
  `ghidra` available 28 ops, `hopper` `executable_missing` 36, `ida` `not_configured`
  12. Catalog counts 127 CLI / 170 MCP / 6 prompts; identity digests
  `tools_sha256:25802f6d…0116`, `prompts_sha256:5296f030…c7a2`,
  `combined_sha256:85d80276…d72a` — byte-identical to `r2-doctor-reverify` values.
- source: `/tmp/r4-caps.json` (npx cache `dea9475797100b20`, same as r2).
- verify: `npx -y rea-agents@6.4.0 capabilities --format json | python3 -c "import
  json,sys; c=json.load(sys.stdin)['capabilities']; print(len(c));
  [print(x['operation'],x['available']) for x in c]"`
- verified-at: 2026-10-13T16:45Z
- suggested: admit — the catalog digest invariance is the strong claim: same
  127-verb surface, same gates; every "never exercised" tag below is coverage debt,
  not surface drift.

## Candidate: `rea doctor` re-verify — zero drift; 4th consecutive identical verdict

- claim: `doctor --format json` (68,124 B) returns the same 18-check array as r1/r2:
  10 pass (`node` 24.21.0, `host` "arch unknown", ghidra + 7 sub-checks incl. JDK
  21.0.12.1 `/usr/lib/jvm/java-21-openjdk`), 8 fail — `hopper`
  `missing_analysis_engine`, `ida-registration` `missing_analysis_engine`,
  `skill:identity` `config_drift` (still v37/170-tools `stale` via the
  `~/.claude/skills` destination gap, not content drift), and the same five
  `registration:*` `config_drift` (claude_code, codex, grok_build, opencode, pi).
  `devin` + `omp` still `aligned`; `grok_bot` still `manual`-exempt. `healthy:false`
  / `environment_healthy:false` → exit 1. kimi remains correctly absent from
  doctor's SupportedClients registry; its live registration at
  `~/.kimi-code/config.toml:1284-1292` (`[mcp_servers.rea]`, npx
  `rea-agents@6.4.0 mcp`, same env pair) verified intact by hand — 3/7 surfaces
  (devin/omp/kimi) still registered.
- source: `/tmp/r4-doctor.json`; `~/.kimi-code/config.toml` sed dump.
- verify: `npx -y rea-agents@6.4.0 doctor --format json | python3 -c "import
  json,sys; d=json.load(sys.stdin); print([c['name'] for c in d['checks'] if not
  c['ok']])"` → the same 8 names.
- verified-at: 2026-10-13T16:46Z
- suggested: admit — fourth identical verdict; the 6 `config_drift` failures are
  standing operator-owned state, not new drift.

## Candidate: artifact + package rescan — zero new targets since r3; `pacman -Q` first baseline 1174

- claim: `find /usr/lib /opt ~/Applications ~/.local/share -newermt '2026-10-13'`
  over `*.asar|*.node|*.exe|*.apk|*.AppImage` returns **zero** files — nothing new
  has landed on the watched surface since the r3 sweep (same calendar day).
  `pacman -Q | wc -l` = **1174**; no prior round recorded an installed-package
  count, so 1174 is the first baseline, not a delta. The two counts r1 did record
  still hold exactly: package cache 1556 `.pkg.tar.zst` (was 1556) and `pacman
  -Qm` foreign set 14 (was 14) — consistent with a no-drift host.
- source: find run (empty output), `pacman -Q|wc -l`, `ls
  /var/cache/pacman/pkg/*.pkg.tar.zst|wc -l` = 1556, `pacman -Qm|wc -l` = 14.
- verify: same four commands; corpus `2026-10-13-pacman-packages` for the
  1556/14 baselines.
- verified-at: 2026-10-13T16:46Z
- suggested: admit — frontier movement must come from the verb census, not new
  artifacts; note the corpus now has a `pacman -Q` baseline to diff against.

## Candidate: managed-assembly boundary INVERTED vs the r1 record — `inspect_managed_*` works on 0x14c IL-only assemblies; **x86-64 (R2R) is the refused class**

- claim: r1 recorded "`inspect_managed_artifact` … AnyCPU assembly class is
  rejected" after a probe on `Microsoft.CSharp.dll`. Re-run this round shows the
  boundary is the machine field, and it cuts the other way than r1's wording
  implies: `Microsoft.CSharp.dll` is `pei-x86-64` (objdump) — a
  crossgen/R2R-class assembly — and `System.Private.CoreLib.dll` (also
  pei-x86-64; **92/172** of `Microsoft.NETCore.App/10.0.11` DLLs are x86-64 vs 80
  i386) refuses identically: `{"code":"target_unavailable","reason":"unsupported
  PE architecture","retryable":false}`. Meanwhile `/usr/lib/pinta/Pinta.dll`
  (`pei-i386`, machine `0x014c`, `il-only`, `ready_to_run_signature:false`)
  **succeeds**: ev_471d085b…, provider `rea-dotnet-static`, full artifact
  envelope (3 sections, CLI header, 32 references, 913 attributes, TFM list).
  All 36 Pinta DLLs are `pei-i386` → the whole app corpus is in the accepted
  class.
- source: `objdump -f` on the three DLLs; `/tmp/r4-managed-corelib.json` (refusal)
  and `/tmp/r4-managed-pinta.json` (success envelope).
- verify: `npx -y rea-agents@6.4.0 inspect-managed-artifact
  /usr/lib/pinta/Pinta.dll --format json` → ev_ id; same command on
  `System.Private.CoreLib.dll` → typed refusal.
- verified-at: 2026-10-13T17:0xZ (this round)
- suggested: admit + **erratum for `2026-10-13-r1` / PROVINCE**: "AnyCPU rejected"
  mislabels the class — accepted = `machine 0x014c` IL-only PE32 (which is what
  most AnyCPU assemblies, incl. all of Pinta, actually are); refused = x86-64
  R2R/crossgen'd (`0x8664`, `ready_to_run` class). Framework R2R inventory: 92
  x86-64 vs 80 i386 in 10.0.11.

## Candidate: managed trio + `compare-managed-members` now exercised end-to-end on Pinta — members decode, P/Invoke boundary resolves, compare degrades honestly to `unknown`

- claim: `inspect-managed-members Pinta.dll` → ev_f382333b…, 3.56 MB envelope:
  **types 161, fields 671, methods 711, member_refs 1122, call_edges 4422,
  field_accesses 2265**, `coverage.issues[]` empty. `inspect-managed-native-boundaries
  Pinta.dll` → ev_082020a6…, `coverage.complete`: **39 pinvoke_imports** (e.g.
  `AECreateDesc` → `/System/Library/Frameworks/Carbon.framework/…/Carbon`), **4
  module_refs** (Carbon, CoreFoundation, ApplicationServices, libsystem_c.dylib —
  Pinta's macOS-compat declarations), 51 native_implementations; verification
  honestly `managed-declaration-only`. `compare-managed-members Pinta.dll
  Pinta.Core.dll` → ev_f5e2dbc1…: machinery works (algorithm
  `rea-managed-member-comparison`, exact-IL→signature→shape pairing, both sides
  evidence-linked) but right side decoded `metadata_status:"partial"`, 0 methods →
  `summary {unknown:1382}` — an honest non-verdict, not a fabricated diff.
  Boundary op on `Gtk-4.0.dll` (2.3 MB GirCore binding) hits a typed budget:
  `coverage.state:"unavailable"` — "Managed metadata exceeds the 67108864 byte
  representation budget" at offset 597814.
- source: `/tmp/r4-mem-pinta.json`, `/tmp/r4-bnd-pinta.json`,
  `/tmp/r4-cmm.json`, `/tmp/r4-bnd-gtk.json`.
- verify: the three commands verbatim; member counts via the run-log python.
- verified-at: 2026-10-13T17:0xZ
- suggested: admit — the managed-provider surface is real and decode-faithful on
  IL-only assemblies; honest ceilings observed (64 MiB representation budget on
  GirCore; `partial` right side → all-`unknown` compare, never guessed).

## Candidate: `extract_artifact` success path proven — APK materializes to a REA-managed root; no destination arg exists

- claim: `extract-artifact ~/.local/share/godot/export_templates/4.7.2.stable/
  android_debug.apk` → ev_a39de6b5…, provider `rea-artifact-graph`,
  `root_format:"apk"`, real file tree materialized under
  `/tmp/rea-extracted-d927f6ef-…/` (`AndroidManifest.xml`, `classes2.dex` …
  `classes13.dex` visible). Limitation: "All regular files in the active
  artifact were materialized; nested archive contents remain represented by
  their containing file." `--schema` shows args `{path}` + option
  `integrityPolicy` **only** — no output-directory parameter exists; a second
  positional (as r3's AppImage row used) is accepted-and-silently-unused and
  the extraction root is always `/tmp/rea-extracted-<uuid>`. Success-path status
  by format: APK ✓; ELF refused r3 (`unsupported_target`, no elf reader).
- source: `/tmp/r4-extract-apk.json`; `ls` of the managed root; `--schema` dump.
- verify: `npx -y rea-agents@6.4.0 extract-artifact --schema --format json` (arg
  set) + the APK run.
- verified-at: 2026-10-13T17:0xZ
- suggested: admit — upgrades `extract_artifact` from refusal-only to exercised;
  record the no-destination-arg pitfall (contrast `extract-firmware` which
  *requires* `<path> <outputDirectory>`).

## Candidate: definitive unexercised-ops census → the r5 frontier queue

Exercised set (union of r1–r3 waves + this lane): analyze/inspect, search,
decompile, compare, function, instructions, xrefs, trace, read-bytes,
address-to-file-offset, analyze-javascript-application, trace-application-feature,
inspect-artifact, **extract-artifact ✓(new)**, inspect-evidence-bundle,
evidence-export, evidence-import, inspect-analysis-view, inspect-recorded-crash,
inspect-evm-interface, inspect-pe-resources, inspect-keyed-archive,
decode-interface-builder, trace-dylib-resolution, **inspect-managed-artifact /
inspect-managed-members / inspect-managed-native-boundaries /
compare-managed-members ✓(new)**, list-browser-targets, inspect-web-page,
list-electron-targets, inspect-electron-page, capture-browser-scenario,
inspect-web-network-capture (schema), compare-application-versions (refusal),
record_pairs + open/close/export/get_evidence_bundle/binary_session (MCP r3).
Meta: doctor, providers, capabilities, setup, mcp.

**Queue A — self-provisionable NOW (provider available, targets on disk, no operator
key):**

| op (CLI verb) | gate | cheap first target |
|---|---|---|
| `resolve-native-call-targets` | ghidra | libjq GOT-indirect calls (r3 xrefs left these unresolved) |
| `inspect-native-api` | ghidra | `jq_next` signature (function dossier already carries `native_api`) |
| `inspect-native-data-type` | ghidra | libjq `--type`/`--address` |
| `inspect-native-instruction` | ghidra | libjq `0x117070` |
| `inspect-native-load-image` | ghidra | libjq |
| `annotate-native-function` | ghidra (ephemeral session metadata) | libjq `jq_next` rename |
| `compare-javascript-export-shapes` | application; needs 2 JS-graph evidences | obsidian.asar ev vs typora app.asar ev (both held) |
| `trace-javascript-semantics` | application; JS evidence | obsidian.asar ev |
| `compare-source-to-bundle` | application; JS evidence + source dir | typora `.jsc` vs recovered? |
| `build-reconstruction-obligation-ledger` | application; evidence input | obsidian.asar ev |
| `evaluate-reconstruction-coverage` | application; evidence input | obsidian.asar ev |
| `import-reference-source` | pure import; `{root}` dir | jq/pinta source tree (fetch or local) |
| `verify-managed-native-boundaries` | needs boundary+native evidences | **ev_082020a6 + a libgtk native ev** (chained, cheap) |
| `project-managed-application-graph` | needs managed evidence | **ev_f382333b (Pinta members)** (chained) |
| `compare-managed-members` round-2 | decode both sides first | two complete-decode assemblies (Pinta vs Pinta.Effects) |
| `inspect-web-network-capture` | needs a HAR file — self-provisionable | chromium `--log-net-log` or mitmproxy HAR |
| `capture-electron-scenario` | electron CDP :9223 self-launch (r3 pattern) | electron43 + xvfb |
| `reconcile-javascript-runtime` | runtime+static evidence | follow capture-electron-scenario |
| `observe-web-session` / `observe-web-execution` | CDP endpoint :9222 self-launch | chromium headless |
| `capture-web-screenshot` / `compare-web-screenshots` / `compare-web-captures` | CDP + prior captures | chromium headless |
| `analyze-web-bundle` / `inspect-web-event-listeners` / `discover-webmcp-tools` | CDP target | same endpoint |
| `export-web-scripts` → `trace-web-module-imports` → `trace-web-source-location` | chained on a saved capture | capture JSON from browser-scenario run |
| `list-javascript-runtime-targets` / `observe-javascript-runtime` | V8 Inspector endpoint | `node --inspect` self-launch |
| `capture-process` / `compare-process-captures` | launches local process, scenario JSON | small scripted scenario |
| `project-apple-application-graph` | inputJson; needs Apple-graph evidence | maybe feedable by keyed-archive/IB evs — probe with typed refusal as datum |

**Queue B — exercised-as-refusal, success path operator-gated (boundary held; r5 can only re-confirm):**

| op | gate (env key / requirement) |
|---|---|
| `inspect-binary-layout` | `REA_PWNTOOLS_PYTHON` — caller Python w/ pwntools 4.15.0+pyelftools 0.33+Unicorn 2.1.2 (uv recipe documented r1) |
| `inspect-firmware-regions` | `REA_BINWALK_COMMAND` — Binwalk 3.1.x |
| `extract-firmware` | `REA_UNBLOB_COMMAND` — Unblob 26.6.x |
| `recover-javascript-sources` | `REA_WAKARU_COMMAND` — Wakaru ^1.13.0 |
| `inspect-android-package` + `inspect-android-class` / `inspect-android-method` / `search-android-classes` / `trace-android-references` / `project-android-application-graph` | `REA_JADX_MCP_JAR` — jadx-headless-mcp-0.7.1 (sha256-pinned jar) |
| `decode-android-resources`, `inspect-apktool-client` | `REA_APKTOOL_COMMAND` |
| `inspect-jeb-client`, `list-jeb-units`, `open-jeb-project`, `decompile-jeb-item` | `REA_JEB_MCP_URL` (live MCP at :8425) |
| adb surface (22 verbs; only `list-adb-devices`+`inspect-adb-client` refusal-probed) | `REA_ADB_PATH` + a device |
| `compare-application-versions` success path | two JS-graph/managed evidences — **now self-provisionable**; only the refusal datum is held |
| `import-managed-reconstruction` | external decompiler output (ilspy/dnSpy absent; no SDK) — operator or hand-crafted JSON |
| ida provider's 12 MCP ops | `REA_IDA_MCP_CONFIG` |
| hopper's 13 unique ops | `/opt/hopper/bin/Hopper` (executable_missing) |

**Queue C — host-gated, never invoked (macOS `unsupported_host`; cheapest move is a
refusal-datum per op, value low):** `inspect-macho`, `inspect-signature`,
`demangle-swift`, `capture-native-ui-scenario`, `observe-native-calls`,
`observe-native-ui`, `inspect-asset-catalog`, `inspect-native-dispatch-metadata`.
(`list-architectures`, `inspect-plist` already refusal-probed.)

**Queue D — MCP-session-only ops not yet exercised** (need a session lane like r3-14;
gates shown as surface): `build_call_path`, `compare_artifacts`,
`compare_process_captures`(MCP), `correlate_static_and_runtime`,
`find_changed_behavior`, `get_navigation_context`, `inspect_address_context`,
`list_unknowns`, `record_unknown`, `update_unknown`, `verify_reconstruction`,
`verify_unknown_resolution` (session surface, open target needed) — and
official-proxy ops never invoked standalone though subsumed by CLI dossier verbs:
`address_name`, `set_address_name`, `set_addresses_names` (session-mutating,
ephemeral), `list_documents`, `list_names`, `list_segments`, `procedure_address`,
`resolve_containing_procedure`, `procedure_references`.

## Run log

| # | command | result |
|---|---|---|
| 1 | `capabilities --format json` → `/tmp/r4-caps.json` | 134,994 B; 18 ops, 8 available; ghidra 28/hopper 36/ida 12 — identical matrix + digests to r2 |
| 2 | `doctor --format json` → `/tmp/r4-doctor.json` | exit 1; same 8 failures as r1/r2; devin+omp aligned, grok_bot manual; digests identical |
| 3 | `find /usr/lib /opt ~/Applications ~/.local/share -newermt '2026-10-13' \( -name '*.asar' -o … \)` | **zero** new artifacts since r3 |
| 4 | `pacman -Q\|wc -l`; `ls /var/cache/pacman/pkg/*.pkg.tar.zst\|wc -l`; `pacman -Qm\|wc -l` | 1174 (first baseline); 1556 cache (== r1); 14 foreign (== r1) |
| 5 | `sed -n '1283,1294p' ~/.kimi-code/config.toml` | kimi `[mcp_servers.rea]` registration intact (doctor-blind client) |
| 6 | `objdump -f` CoreLib/CSharp/Pinta/Gtk-4.0/Mono.Cecil + 10.0.11 census | refused class = `pei-x86-64` (92/172 in 10.0.11); accepted = `pei-i386` (all 36 Pinta DLLs) |
| 7 | `inspect-managed-artifact System.Private.CoreLib.dll` | exit 1 `target_unavailable`/"unsupported PE architecture" — R2R class refused |
| 8 | `inspect-managed-artifact /usr/lib/pinta/Pinta.dll` | **ev_471d085b…** rea-dotnet-static — machine 0x014c il-only, 32 refs, 913 attrs |
| 9 | `inspect-managed-members /usr/lib/pinta/Pinta.dll` | **ev_f382333b…** 3.56 MB — 161 types/671 fields/711 methods/4422 call_edges; 0 coverage issues |
| 10 | `inspect-managed-native-boundaries /usr/lib/pinta/{Pinta,Gtk-4.0}.dll` | Pinta **ev_082020a6…** complete — 39 pinvokes/4 module_refs (macOS shims)/51 native_impl; Gtk-4.0 → `unavailable` 64 MiB representation budget |
| 11 | `compare-managed-members Pinta.dll Pinta.Core.dll` | **ev_f5e2dbc1…** — right `partial`/0 methods → summary `unknown:1382`, honest non-verdict |
| 12 | `extract-artifact android_debug.apk` + `--schema` | **ev_a39de6b5…** rea-artifact-graph — dex/manifest materialized under `/tmp/rea-extracted-<uuid>`; schema proves no destination arg exists |
| 13 | `--schema` on ~35 unexercised verbs | arg shapes captured; gates tabulated in Queue A/B/C/D |
| 14 | grep exercised-set census across `waves/kaidoku-r{1,2,3}` + corpus | managed ops had **zero** prior invocations; `inspect_managed_artifact`'s only prior run was the r1 Microsoft.CSharp refusal |

Scratch (reproducibility, `/tmp`): `r4-{caps,doctor,caps.err,doctor.err}`,
`r4-managed-{corelib,pinta}.{json,err}`, `r4-mem-pinta.json`, `r4-bnd-{pinta,gtk}.json`,
`r4-cmm.json`, `r4-extract-apk.json`, `r4-verbs.txt`; extracted APK tree at
`/tmp/rea-extracted-d927f6ef-1ad2-48cf-8130-32a48609f688`.

## Summary

Zero drift on every axis — capability matrix, doctor verdict, catalog digests,
provider set, watched-artifact filesystem, package cache (1556) and foreign set
(14) all identical to r1–r3 records; `pacman -Q` 1174 is a first baseline. The
census closed the **managed** frontier in-lane instead of queueing it: r1's
"AnyCPU rejected" was a mislabel — accepted class is `pei-i386` IL-only, refused
class is x86-64 R2R (92/172 of the 10.0.11 framework). All three
`inspect_managed_*` ops plus `compare_managed_members` now carry live evidence
(Pinta: 711 methods, 39 P/Invokes to macOS shims), and `extract_artifact`
succeeded on the Godot APK. Honest ceilings found: 64 MiB managed-metadata
representation budget (Gtk-4.0), `partial` decodes → all-`unknown` compares.

**r5 queue:** 26 self-provisionable CLI ops (Queue A, headed by
`resolve-native-call-targets` on libjq's GOT-indirect sites, the held-evidence
application verbs, and the CDP/V8 self-launch family), ~45 operator-env-gated
ops (Queue B), 8 terminal macOS-gated (C), 12 MCP-session + 7 standalone
official-proxy ops (D).
