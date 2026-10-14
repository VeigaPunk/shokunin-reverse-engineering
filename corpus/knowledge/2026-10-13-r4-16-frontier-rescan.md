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

## Errata (round-6 expand lane, r5-02)

- **Queue A row 1 discharged (r5-02):** `resolve-native-call-targets` ran
  live on `/usr/bin/jq` — the one-arg form as queued refuses typed-and-fast
  (`VALIDATION_ERROR`, required second positional `address`, exit 1, 0.7 s);
  the two-arg form resolved 3/3 probed GOT-indirect call sites to Ghidra
  `EXTERNAL` thunks (ev_db50c389…, ev_4e3303af…, ev_c9fcea3d…; `0x109110`
  == `<EXTERNAL>::jq_init` by independent search evidence), returns honest
  `not-call`/0-target non-verdicts off call sites (ev_b0238bea…), and
  `sha256sum /usr/bin/jq` is byte-identical before/after. "Self-provisionable
  NOW (ghidra)" holds. Row 1 moves from queued to exercised; the table body
  above is left as recorded. Detail:
  `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md`.

- **Queue A rows 2+3 discharged (r7-01):** `inspect-native-api` and
  `inspect-native-data-type` ran live on `/usr/lib/libjq.so.1.0.4` (350,384 B
  shared object, sha256 `7e8bcc…8b6b`, byte-identical before/after — the
  "libjq" these rows name). API: `jq_next` resolves by NAME and by `0x117070`
  to the same composed-workflow dossier (ev_85486b39…, ev_7ed3e243…; re-run
  byte-identical → ev ids reproducible); the row-4 hint address `0x117070` is
  jq_next's entry in Ghidra space (dynsym file vaddr `0x17070` + base
  `0x100000`); boundary is decompiler-inferred (`undefined1[16]` return, 1
  param, confidence `low`, 85-entry jump table @ `0x143eec` typed into 47
  case mappings, 2 residual unknowns). Data-type: bare and both-args forms
  refuse pre-analysis in 0.7 s ("Supply exactly one of type or address" — a
  second, distinct error family vs r5-02's `VALIDATION_ERROR`); `--type
  /string` and `--address 0x13f000` succeed (`available` `/string`; ev_3fed2e41…,
  ev_6445bef7…), `--type /` and `--type undefined1` are honest
  `unavailable` non-verdicts (ev_d1fb4eb6…, ev_81d4694a…); +0x100000
  Ghidra base re-confirmed on a second artifact kind. Both rows move from
  queued to exercised; the table body above is left as recorded. Detail:
  `corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md`.

## Errata (round-7 expand lane, r7-02)

- **Queue A rows 4–5 — the 3rd and 4th still-unexercised rows (table lines 168–169) — discharged (r7-02)**; census
  address convention fixed:** `inspect-native-instruction` on
  `/usr/lib/libjq.so.1.0.4` decodes the queued `libjq 0x117070` as
  **`jq_next`'s entry instruction** (`ENDBR64`, bytes `f30f1efa`,
  ev_b73334e9…) — `0x117070` is the **Ghidra image-space** address (image
  base `0x100000`, confirmed by ev_f0221f0a… `observations.image_base`);
  the file-space address is `0x17070` (`nm -D`), and probing that raw form
  returns a typed `outside-memory` at exit 0 (ev_961a7a55…) — ELF DYN/PIE
  addresses must be pre-shifted +`0x100000` (extends r5-02's PIE pitfall to
  shared objects). `inspect-native-load-image` on ELF degrades honestly:
  `status "unsupported"` — "Independent load-image verification currently
  supports DOS MZ and explicit DOS COM targets only." (ev_f0221f0a… libjq,
  ev_bdecdf21… jq) — while still emitting the full observation payload
  (base `0x100000`; 29 mappings / 729 applied relocations / 185 entry
  points for libjq). Cross-run: r5-02's verify re-reproduces today
  (`resolved-indirect 0x109110` at site `0x1020a3`; instruction decode
  `CALL qword ptr [0x107ea8]`, ev_65a06e0c…). Rows move queued → exercised;
  the table body above is left as recorded. Detail:
  `corpus/knowledge/2026-10-13-r7-02-queue-a-ops-2.md`.

## Errata (round-8 expand lane, r8-01)

- **Queue A rows 6+8 — the 5th and 6th still-unexercised rows (table lines
  170, 172) — discharged (r8-01)**; **row 7 (table line 171) closed as a
  census defect, not re-run**: `annotate-native-function` on
  `/usr/lib/libjq.so.1.0.4` wrote the queued `jq_next` rename (ev_d6b85107…)
  and the provider states the row's own gate as output — `effects
  {scope:"session-analysis-database", source_bytes_modified:false,
  persists_after_close:false}`; a fresh-invocation `inspect-native-api jq_next`
  read-back re-derived r7-01's ev_85486b39… byte-identically with the original
  name (non-persistence proven empirically, plus cross-round id
  reproduction); interior addresses snap to the containing function's entry
  (ev_11449635…: `0x117080` → annotated `0x117070`), unknown names refuse
  typed but post-analysis (405 B after a full 14.2 s import), and the
  annotated dossier keeps r7-01's inference-grade signature. All jq/libjq
  digests byte-identical before/after. `trace-javascript-semantics` ran on the
  queued `obsidian.asar ev` (ev_e8a2c4ba…, 47.66 MB, 6.3 s): `found` at
  degree-0, 13 relevant unknowns (ev_1b5805c1…); on the app.asar 1.13.7 graph
  three statuses observed live — `found`-with-zero-caller-edges on
  `serialize` (ev_e027acb5…), `ambiguous` returning the 4-node `error`-event
  collision set (ev_46ef7954…), and a zero-match property seed reporting
  status `partial`, NOT the schema-enumerated `no-match` (ev_c83a02dc…) —
  emptiness must be tested via `total_seed_matches`. For row 7:
  `compare-javascript-export-shapes` was already exercised end-to-end by
  round-4 wave entry r4-09
  (`2026-10-13-r4-09-js-export-compare.md`, 16 runs) before this census's
  exercised-set union was written — the census listed neither that verb nor
  its evidences; this lane re-derived r4-09's recorded
  `ev_ec6d721d…` byte-exact from its own verify input today. Rows 6+8 move
  queued → exercised; row 7 moves queued → exercised-by-r4-09; the table body
  above is left as recorded. Detail:
  `corpus/knowledge/2026-10-13-r8-01-queue-a-ops.md`.

## Errata (round-8 expand lane, r8-02)

- **Queue A rows 8+9 — table lines 172–173 — discharged (r8-02)**; row 8 was
  discharged concurrently and complementarily by r8-01 (bullet above — line
  172 carries both lanes' evidences; line 173 is solely this lane's).
  `trace-javascript-semantics` (inputJson `{application, query}`) re-ran on
  the r3 renderer Evidence (ev_e8a2c4ba…, 47.66 MB, reused unchanged, sha
  95eb1948…): three seed kinds → three typed statuses — `ambiguous`
  (event `refresh`, the 6 `cm-addons.js` sites, ev_8aa311c3…), `found`
  (function fingerprint bc93a7e9…, 0 retained callers, coverage `partial`,
  ev_318cc2d7…), and `partial` — NOT the schema-enumerated `no-match` — for a
  0-match `endpoint` seed on the budget-truncated graph (ev_8904a82d…): the
  status machine (cache `javascriptSemanticQueryAssessment.js:13-30`) refuses
  absence claims on partial graphs, independently reproduced by r8-01's
  zero-match property seed the same night. Result envelopes label themselves
  `analyst-inference`/`inferred` with `evidence_links` lineage; a re-run is
  byte-identical with the same id (ev_8aa311c3…) — content-addressed evidence
  ids extend to the application-workflow verbs.
  `compare-source-to-bundle` (strict `{reference, application}`) succeeds
  from held artifacts alone: `import-reference-source /tmp/sig-core`
  (Queue-A row 12's verb consumed as PROVISIONING ONLY — its gates stay
  unprobed for their owner) → 31-entry `HistoricalSourceGraph` (root
  a5949039…, caller-invented commitments rejected), then vs ev_f9b4493a… →
  stbc_1d2e0820… (ev_524f714f…): **19/19 retained sources
  `unchanged`/`exact` via `exact-source-digest`** (the held extraction proven
  still byte-identical to the analyzed tree; 229 application nodes honestly
  unmapped). The row's "typora `.jsc` vs recovered?" resolves: vs
  ev_184ef0ac… the loader `launch.dist.js` maps `unchanged/exact`
  (stbc_c0d3e8f7…, ev_a2680e34…) while the `.jsc` — reference-classified
  `unknown`, node-less in the bundle graph — is structurally incomparable at
  BOTH layers (`retained_source_files` 1/3): the wall is the data model's,
  not a missing tool. All nine live runs exit 0, stderr 0 B, 0.7–11.3 s, no
  operator env; all eight input digests (incl. the `/usr/lib/obsidian/
  obsidian.asar` a52a7daf… and `/usr/share/typora/resources/app.asar`
  7ac791ca… pins) byte-identical before/after. Rows 8+9 move queued →
  exercised; the table body above is left as recorded. Detail:
  `corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md`.

## Errata (round-9 expand lane, r9-02)

- **Queue A rows 13+14 — the 4th and 5th still-unexercised rows (table lines
  177–178) — discharged (r9-02)**; sibling r9-01 had not landed when this
  lane's runs finished (git clean at the 04:22Z check → the assignment's
  4th+5th fallback applied); r9-01 landed mid-write (~04:24Z) claiming rows
  10+11 (table lines 174–175) — zero row overlap; line 176 was skipped by
  both lanes (r8-02 leaves its gates with their owner).
  `verify-managed-native-boundaries` ran live on the queued pairing
  (boundaries `ev_082020a6…` + a libgtk native evidence) with a gate
  refinement: the native side accepts only `inspect_macho` or
  `analyze_function` Evidence — one symbol per function dossier
  (`managedNativeVerificationMatch.js:17,:32`), so "a libgtk native ev" is a
  104.0 s `rea function` dossier (`ev_6ac0c9af…`, `gtk_button_new`
  `0x1d8380` = `nm -D` `0xd8380` + `0x100000`), not an analysis inventory.
  The pairing answers honestly and negatively: 39/39 `unresolved`/
  `no-native-candidate` at coverage `complete-within-inputs`
  (`mnv_f7ed4e2e…`) — Pinta.dll's module_refs are macOS-only (Carbon /
  CoreFoundation / ApplicationServices / `libsystem_c.dylib`, per
  `ev_082020a6…`), and the result's own limitation states unresolved ≠
  absence. Module identity is enforced and basename-normalized: a glibc
  `setenv` dossier (`ev_2262ac05…`, `0x144bd0` = dynsym `0x44bd0` +
  `0x100000` — the PIE rule re-confirmed on glibc) is `contradicted`/
  `module-mismatch` against the declared `/usr/lib/system/libsystem_c.dylib`
  scope (`mnv_1a2d59ec…`), while the same bytes analyzed as
  `/tmp/libsystem_c.so` flip that import to `verified`/`exact-function-name`/
  `observed` (`mnv_af96af7d…`) — calibration rename, labeled as such;
  `libc.so.6` never strips because the lib-variant only fires for names
  ending `.dylib`/`.so`. Wrong-kind native Evidence (the members bundle) →
  accepted 0 / unsupported 1, 39 `unresolved`/`unsupported-native-evidence`,
  coverage `partial` (`mnv_0c8a9a8c…`); boundaries offered as their own
  native observation refuse typed (`invalid_request`/`invalid_input` with
  `issues[]` — a third distinct managed-domain refusal family). NEW
  authentication datum: `analyze_function` evidence ids are f(content,
  params) — the renamed-path dossier carries the SAME id `ev_2262ac05…` with
  a byte-different `subject`, and a subject-only rewrite (no re-analysis)
  yields a request byte-identical to the honest rename (both `125cb2a9…`) →
  identical envelope `ev_d7d2efa2…`/`mnv_af96af7d…`: module attribution is
  caller-attested, not id-authenticated (refines the r2 "path-sensitive"
  evidence-id note for this verb family; consumers must pin request bytes).
  `project-managed-application-graph` discharged twice: members-only as
  queued (`ev_f382333b…` → `ev_4d2b732d…`/`magp_8d35cc89…`, 1,545 nodes/1,544
  edges, 1 link) and the three-evidence union (`ev_471d085b…` + `ev_f382333b…`
  + `ev_082020a6…` → `ev_75927c55…`/`magp_b0495613…`, 1,636 nodes, 3 links,
  +1 assembly/+39 pinvoke/+51 native-impl nodes) — both project into the
  `JavaScriptApplicationGraph` data model, both `analyst-inference`/
  `partial`. Census cost note: "chained, cheap" holds for the workflow verbs
  (0.68–0.84 s verify, 1.23–1.29 s project) but the native-evidence leg is
  minutes-class (36.8 s glibc / 104.0 s libgtk dossiers). All nine input
  digests byte-identical before/after; both re-run verifications
  byte-identical (same ids `ev_6f495c63…`, `ev_2262ac05…`). Rows 13+14 move
  queued → exercised; the table body above is left as recorded. Detail:
  `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md`.

## Errata (round-9 expand lane, r9-01)

- **Queue A rows 10+11 — the next still-unexercised rows after the r5–r8
  drain (table lines 174–175) — discharged (r9-01)**:
  `build-reconstruction-obligation-ledger` and
  `evaluate-reconstruction-coverage` ran live on the held obsidian renderer
  Evidence (ev_e8a2c4ba…, 47,658,312 B, sha 95eb1948… — byte-identical
  before/after; `/usr/lib/obsidian/obsidian.asar` still a52a7daf…). Input
  shape finding first: both verbs consume an Evidence **bundle**
  (`records[]` + derived manifests) and refuse hand-wrapped bundles typed
  and verbatim — "Evidence bundle manifests are not canonical" — so the
  census's "obsidian.asar ev" target is reachable only after canonical
  wrapping (the package's own `createEvidenceBundle` produces the accepted
  form; a lane holding only ev_ ids must first materialize envelopes via
  the already-exercised `evidence-export`). Ledger success: ev_e249a865… /
  `rol_c68008b9…` (390,597 B, 8.4 s, analyst-inference) — **171
  obligations** (169 generated from the real graph by the node-kind policy
  map + 2 authored reviewed), **status `unknown`, 0 of 171 verified, all
  171 `static-only`**; a manifest-bound reviewer reaches `implemented`
  (fixture+verifier diagnostics honest), a blocked reviewer stays
  `blocked`; 29 unresolved-node limitations propagate from the r3 graph
  verbatim; re-run byte-identical with the same id (content-addressing
  extends to this verb). Refusals: dangling review-evidence id refuses
  (`unreadable_output`, non-retryable — CLI masks the cause; recovered
  verbatim via direct module repro: "Reviewed obligation Evidence is
  missing: ev_000…0", single-diff attributed). Coverage success: bare,
  timestamp-free closure, no Evidence envelope — `partial` with exactly one
  named reason (`package-proof-missing`) plus the verb's own recommended
  probe (`verify_reconstruction_package`), flipping to `ready` when that
  named proof lands; verifier contracts are tamper-checked (canonical-JSON
  digest recomputed; flip → verbatim "Verifier contract digest is
  invalid:…"), unknown boundaries refuse verbatim; re-run byte-identical.
  Cross-verb asymmetry recorded: the ledger projects referential TypeErrors
  as non-retryable `unreadable_output`, coverage as retryable
  `invalid_request`. All runs exit 0/1 as designed, longest 8.4 s, no
  operator env. Rows 10+11 move queued → exercised; the table body above is
  left as recorded. Detail:
  `corpus/knowledge/2026-10-14-r9-01-queue-a-ops.md`.

## Errata (round-10 expand lane, r10-01)

- **Queue A rows 15+16 — the next still-unexercised rows after the r5–r9
  drain (table lines 179–180) — discharged (r10-01)**; line 176 skipped per
  convention (gates stay with their owner); git clean at lane start and
  final write — no sibling overlap. `compare-managed-members` (round-2):
  the verb takes `{leftPath, rightPath}` only and re-decodes both sides
  internally (no evidence-id input), so the gate "decode both sides first"
  is a selection rule — pick metadata-complete IL-only assemblies; with
  Pinta.dll vs Pinta.Effects.dll (both `pei-i386`, decodes
  `metadata_status:"complete"`; the Effects decode is new evidence
  `ev_92faacb3…`, 1,671 methods/704 fields, `coverage.issues[]` empty) the
  verb returns its first real differentiated verdict on this host:
  `ev_cbf4acfb…`/`mmc_0d5f6e8b…` summary `{unchanged 2, changed 14,
  added 1241, removed 1047, unknown 588}` vs round-1's all-unknown
  `{unknown: 1382}` at right `unavailable` — the coverage ladder is keyed
  on `metadata_status` (right `unavailable` → `partial`), NOT on the
  members `coverage.state`, which stays `partial` with empty issues even on
  complete decodes. Semantics pinned live: pairing is identity-keyed,
  names alone never a basis (`matching` exact_il_signature 2 /
  exact_signature 9 / structural_method_shape 20 / field_signature 24 /
  ambiguous 39 / unmatched 2837); the 588 unknowns are honest non-verdicts
  ("Multiple managed methods share the same non-name identity key; REA did
  not guess a token remap."); reversed order swaps added/removed exactly
  (1047/1241) with distinct direction-sensitive ids (`ev_eea2312b…`/
  `mmc_7765bc45…`); re-run byte-identical (same `ev_cbf4acfb…`). New
  authentication nuance (extends r9-02's f(content, params)): the compare's
  internally-minted member evidence ids (`ev_0b4eeaa7…`,
  `ev_701d5d1b…`) differ from CLI-minted ids for identical bytes and mvids
  (`ev_f382333b…`, `ev_92faacb3…`), yet the left internal id is identical
  to r4's held round-1 link — one stable id per invocation shape;
  consumers must never substitute ids across invocation shapes.
  `inspect-web-network-capture`: args `{capturePath, format:
  har|mitmproxy}` + `--record`/`--sensitive-value`; the census's first
  hint is REFUTED — a real 1,310-event chromium `--log-net-log` capture
  refuses typed (`invalid_request`/`invalid_format`, "HAR schema validation
  failed: required.", retryable, exit 1): the operative gate is
  har-schema validity, and the path that works is playwright 1.64.0
  `recordHar` over self-launched `/usr/bin/chromium` 152 against a
  localhost fixture (9,942 B HAR, 5 real 200 entries, 1.4 s provisioning;
  mitmproxy absent on host — that format leg stays unexercised). Success:
  `ev_be4c0e79…` (0.86 s) decodes 5/5 records losslessly under
  `har-schema/lossless-json`, labeled `authority:"historical-reference"`/
  `confidence:"observed"` (a third authority grade alongside
  `shipped-artifact` and `analyst-inference`), `runtime_attribution`
  literal `"unknown"`, "Recorded URLs are never fetched"; record anatomy
  preserves producer representations (the 70-byte PNG as
  `retained`/`har-base64-content`; float literals like
  `1.1520000000000001` survive verbatim); `--record 4` still decodes all
  5 then filters (`ev_9282326c…`); `--sensitive-value` redacts the
  affected record at three pointers (`/request/url`,
  `/request/queryString/0/value`, `/response/content/text`) with zero
  envelope leakage, the capture sha256 intact, and only
  `sensitive_value_count` persisted (declaration strings never persisted —
  verified live; fixture token, secrets shape-only); re-run
  byte-identical. Cross-verb id re-verification: three byte-identical
  re-runs this lane (`ev_f382333b…` members, `ev_cbf4acfb…` compare,
  `ev_be4c0e79…` capture). All probes 0.85–1.1 s, zero operator env; both
  Pinta DLLs + four r4 evidence files + all 7 provisions byte-identical
  before/after. Rows 15+16 move queued → exercised; the table body above
  is left as recorded. Detail:
  `corpus/knowledge/2026-10-14-r10-01-queue-ops.md`.

## Errata (round-10 expand lane, r10-02)

- **Queue A rows 18+19 — the 4th and 5th still-unexercised rows at this
  lane's take (table lines 182–183) — closed as CENSUS DEFECTS, the row-7
  class again, and rows 20+21 (lines 184–185) discharged in their place
  (r10-02)**; sibling r10-01 landed mid-write claiming rows 15+16 (lines
  179–180, bullet above) — zero row overlap by construction; line 176
  untouched (owner convention). **The defect**: r4-08 held lines 182–183
  end-to-end on 2026-10-13 — `reconcile-javascript-runtime` (its
  `ev_032f373f…`), `observe-web-session` (`ev_ac51acb0…`),
  `observe-web-execution` (`ev_990bff76…`) — but the census's exercised
  set was written concurrently with r4-08 and lists only the r3 CDP verbs.
  **Lines 181 (`capture-electron-scenario`, r4-08's deterministic typed
  refusal, re-verified by the r5 audit) and 187
  (`observe-javascript-runtime` / `list-javascript-runtime-targets`, both
  r4-08-held) carry the same defect** and move queued →
  exercised-by-r4-08 on the r4-08 entry's strength. **Fresh re-verification
  (not trust)**: this lane re-ran all four involved verbs on new
  loopback-only self-launched endpoints (chromium 152 headless :9222,
  node v24.21.0 :9229 — the same stack versions r4-08 recorded): session
  auto-scopes `allowed_origins` while execution echoes `[]`
  (`ev_375855d9…` vs `ev_38a61fd8…`; instrumentation block verbatim to
  r4-08); the `file://`-must-stat rule holds both ways (`-e` control →
  `excluded:{unsupported_location:1}`, `ev_a4d15055…`; real-file target →
  listed, `ev_a7961441…`); `observe-javascript-runtime` reproduces the 81
  builtin + 1 file split with the file script's `cdp_hash` EQUAL to the
  pinned main.js sha256 (`ev_bee56f0e…`); the reconcile join lands
  r4-08's exact buckets `matched:1/unmatched:1/unknown:81` at
  `runtime_scripts:82` with `resident-in-loaded-asset` load states
  (`ev_7943e598…` over a fresh static layer `ev_f867295d…`), and BOTH
  deterministic legs re-ran byte-identical (analyze ×2 → same
  `ev_f867295d…`; reconcile on the fixed input ×2 → same
  `ev_7943e598…`). Honest limit recorded: r4-08's own session-scoped ids
  are NOT byte-re-derivable (window timestamps + target ids + their app
  tree deleted by their cleanup) — the close rests on behavioral
  reproduction + fresh content-addressed evidence. Rows 18+19 (and 17, 23)
  move queued → exercised-by-r4-08. **Rows 20+21 discharged live** to keep
  the drain: `capture-web-screenshot` ×3 (`ev_469b8340…`, `ev_fb99d599…`,
  `ev_1bf3535e…`) — artifacts are self-verifying `{sha256, bytes,
  media_type, data_base64}` PNG blocks and a static page's captures are
  byte-deterministic (A/A2 identical artifact sha256 `6746f742…` while the
  envelopes' ids differ: `captured_at` is in the id, the bytes are not);
  `compare-web-screenshots` consumes the artifact block only (envelope
  form → typed `invalid_request` with per-path issues[]) — A vs B
  `different` 384540/384540 px maxΔ246 (`ev_f77738ef…`), A vs A2
  `identical` 0 (`ev_11191731…`); `compare-web-captures` wants SNAPSHOT
  files `{inspection: <complete inspect_web_page normalized_result>,
  webmcp: <discover_webmcp_tools normalized_result|null>}` — the CLI
  composes `{before, after}` itself (`webCaptureDiffSchemas.js:3-13`,
  `browserAdvancedCommands.js:69-76`; raw envelopes refuse opaque
  `invalid_input`) — same-snapshot compare returns overall **`unknown`**
  (incomplete dimensions stay `unknown`, never `unchanged` — absence is
  not proof, `ev_e465f5d4…`), A vs B overall `changed` across
  dom/scripts/resources/metadata/accessibility (`ev_fdfc038c…`);
  `analyze-web-bundle` (`ev_0b903a99…`) chunk digest self-verifies against
  the page's extracted inline-script text (sha256 `75e1da85…`, 146 B,
  recomputed match); `inspect-web-event-listeners "#go"` (`ev_42b8fd4f…`)
  pins one click listener to `index.html:7:74` via `script_id`;
  `discover-webmcp-tools` honest `tools:{total:0}` (`ev_82dbdf0e…`). Cross
  -verb join: script identity `scr_5469de86…` is shared by the
  capture-diff and bundle verbs. All runs 0.7–3.2 s, zero operator env,
  loopback-only; four fixture digests byte-identical before/after; ports
  9222/9229/9230/8878 verified closed and the chromium profile removed.
  Rows 20+21 move queued → exercised; the table body above is left as
  recorded. Detail:
  `corpus/knowledge/2026-10-14-r10-02-queue-ops-2.md`.
