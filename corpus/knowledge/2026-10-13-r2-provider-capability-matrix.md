<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/11-caps-catalog.md. -->

# Round 2 — Provider & capability matrices (rea-agents 6.4.0 on linux/x64)

Host: `Linux plazir27 7.2.3-arch1-3`, node v24.21.0, invocation via `npx -y rea-agents@6.4.0` (npx cache `dea9475797100b20`).
Closes the r1-01 flag: "actual provider list on this host not yet captured".

## Candidate: `rea providers` and `rea capabilities` emit the SAME envelope — one payload, two verbs

- claim: `providers --format json` and `capabilities --format json` returned byte-identical JSON except for `server_identity.server.started_at` (run timestamp). The envelope has exactly 8 top-level keys: `open`, `capabilities` (18 host-scoped operations), `analysis_provider_binding`, `analysis_provider_candidates` (3 entries), `analysis_run`, `analysis_activity`, `provider_operation_health`, `server_identity`. There is no separate "providers" array — the provider list lives inside `analysis_provider_candidates`.
- source: `/tmp/rea-providers.json` vs `/tmp/rea-capabilities.json` (134,994 bytes each; `cmp` first diff at byte 76332 inside `started_at`; node diff confirms only that field).
- verify: `npx -y rea-agents@6.4.0 providers --format json > a.json; npx -y rea-agents@6.4.0 capabilities --format json > b.json; cmp a.json b.json`
- verified-at: 2026-10-13T15:19Z (both runs)
- suggested: admit — surprising but directly observed; consumers should read `analysis_provider_candidates`, not expect a flat list.

## Candidate: No-target state — binding/run/health are null, activity `not_observed`

- claim: With no target open, the envelope reports `open:false`, `analysis_provider_binding:null`, `analysis_run:null`, `provider_operation_health:null`, `analysis_activity:{"status":"not_observed","providers":[]}`. Every provider candidate reports `target_support.status:"unknown"` / `"No target is open."` and `selected:false` — no provider is pre-selected until a target binds.
- source: `/tmp/rea-providers.json` top-level scalars.
- verify: `npx -y rea-agents@6.4.0 capabilities --format json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const j=JSON.parse(s);console.log(j.open,j.analysis_provider_binding,j.analysis_run,j.provider_operation_health,JSON.stringify(j.analysis_activity))})'`
- verified-at: 2026-10-13T15:19Z
- suggested: admit — establishes baseline; `provider_operation_health` and `analysis_activity.providers[]` only populate after `open`.

## Candidate: Authoritative host operation matrix — 8 of 18 top-level operations available on linux/x64

- claim: The top-level `capabilities[]` (host-level, provider-independent operations) reports 18 operations. Exactly 8 are `available:true` (all with `availability_code:null`); the other 10 fail with `availability_code:"unsupported_host"` — 9 with reason "Native macOS utilities require macOS." and `inspect_asset_catalog` with "Apple asset catalogs require macOS assetutil." No operation is provider-gated at this level; the gate is purely the host OS.

| operation | available | availability_code | reason | effects (launches_process / may_write_fs / may_show_ui / may_net) | #limitations |
| --- | --- | --- | --- | --- | --- |
| capture_native_ui_scenario | false | unsupported_host | Native macOS utilities require macOS. | P / W / UI / NET | 1 |
| decode_interface_builder | **true** | — | — | – / – / – / – | 2 |
| demangle_swift | false | unsupported_host | Native macOS utilities require macOS. | P / – / – / – | 1 |
| extract_artifact | **true** | — | — | P / W / – / – | 2 |
| inspect_artifact | **true** | — | — | P / W / – / – | 2 |
| inspect_asset_catalog | false | unsupported_host | Apple asset catalogs require macOS assetutil. | P / – / – / – | 2 |
| inspect_keyed_archive | **true** | — | — | – / – / – / – | 2 |
| inspect_macho | false | unsupported_host | Native macOS utilities require macOS. | P / – / – / – | 1 |
| inspect_managed_artifact | **true** | — | — | – / – / – / – | 2 |
| inspect_managed_members | **true** | — | — | – / – / – / – | 2 |
| inspect_managed_native_boundaries | **true** | — | — | – / – / – / – | 2 |
| inspect_native_dispatch_metadata | false | unsupported_host | Native macOS utilities require macOS. | – / – / – / – | 1 |
| inspect_plist | false | unsupported_host | Native macOS utilities require macOS. | P / – / – / – | 1 |
| inspect_signature | false | unsupported_host | Native macOS utilities require macOS. | P / – / – / – | 1 |
| list_architectures | false | unsupported_host | Native macOS utilities require macOS. | P / – / – / – | 1 |
| observe_native_calls | false | unsupported_host | Native macOS utilities require macOS. | P / W / UI / NET | 1 |
| observe_native_ui | false | unsupported_host | Native macOS utilities require macOS. | – / W / – / – | 1 |
| trace_dylib_resolution | **true** | — | — | – / – / – / – | 2 |

- No capability mutates the artifact (`mutates_artifact:false` on all 18), none needs root, none changes permissions.
- Two shared limitation texts recur: (a) "Availability and textual formats depend on the installed macOS/Xcode toolchain." on every macOS-gated op; (b) the DMG/ASAR pair ("DMG child inventory automatically uses a read-only native macOS mount; PKG remains root-hash-only." + "ASAR files discovered in filesystem-backed inventories are expanded without bulk extraction…") on 7 of the 8 available ops — the managed-* trio carries its own PE/CLI pair instead ("never loads the target assembly, resolves dependencies through a CLR, decompiles C#, or executes target code").
- source: `/tmp/rea-providers.json` `.capabilities[]`
- verify: `npx -y rea-agents@6.4.0 capabilities --format json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>JSON.parse(s).capabilities.forEach(c=>console.log(c.operation,c.available,c.availability_code)))'`
- verified-at: 2026-10-13T15:19Z
- suggested: admit — this is the authoritative on-host matrix for the 18 host-scoped operations. Note several nominally-Apple ops (decode_interface_builder, inspect_keyed_archive, trace_dylib_resolution, inspect_artifact/extract_artifact DMG handling) ARE available on Linux because they are pure-parser, not native-tool, implementations.

## Candidate: Provider registry — exactly 3 analysis-provider candidates; only `ghidra` is usable on this host

- claim: `analysis_provider_candidates` has exactly 3 entries. The gate is each candidate's `availability.status`, NOT the per-operation `available` flag (see next candidate).

| provider id | name | declared version | availability.status | code | gate / remediation | ops declared | diagnostics highlights |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ghidra | Ghidra | null (diag: 12.1.4) | **available** | — | — | 28 | install `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`; headless `support/analyzeHeadless`; native decompiler `linux_x86_64/decompile` self-reports elf x86_64; java `/usr/lib/jvm/java-21-openjdk` 21.0.12.1 64-bit JDK; all 8 checks ok (configuration, platform, architecture, installation, version, headless, native_decompiler, java) |
| hopper | Hopper Disassembler | null | unavailable | executable_missing | launcher missing/not executable: `/opt/hopper/bin/Hopper` | 36 | `launcher_path` probed, absent |
| ida | IDA Pro MCP adapter | "1" | unavailable | not_configured | set `REA_IDA_MCP_CONFIG` to an upstream IDA MCP JSON registration; see `docs/ida-provider.md` | 12 | `configured:false`, `live_connection_probed:false` |

- Provider-gated (non-analysis) engines surface separately via typed failures on their client verbs — see next-but-one candidate.
- source: `/tmp/rea-providers.json` `.analysis_provider_candidates[]`
- verify: `npx -y rea-agents@6.4.0 providers --format json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>JSON.parse(s).analysis_provider_candidates.forEach(c=>console.log(c.provider.id,c.availability.status,c.availability.code,c.capabilities.length)))'`
- verified-at: 2026-10-13T15:19Z
- suggested: admit — matches r1 doctor findings (ghidra 12.1.4 sole engine; hopper `executable_missing`; ida `not_configured`); adds exact declared op counts and probe paths.

## Candidate: Per-provider operation matrix — 41-op union; per-op `available:true` is a DECLARED capability, not host availability

- claim: Inside each candidate, every listed operation carries `available:true` even for unavailable providers (hopper's 36 and ida's 12 ops all say `available:true`). The field means "this provider implements this op when bound"; actual usability requires the provider-level `availability.status:"available"`. Effective on-host coverage = ghidra's 28 ops only.

| operation set | count | operations |
| --- | --- | --- |
| all three providers (core) | 12 | analyze_function, list_procedures, list_strings, procedure_address, procedure_assembly, procedure_callees, procedure_callers, procedure_pseudo_code, read_function_instructions, search_procedures, search_strings, xrefs |
| ghidra + hopper only | 11 | address_name, address_to_file_offset, list_documents, list_names, list_segments, procedure_info, procedure_references, read_bytes, resolve_containing_procedure, set_address_name, set_addresses_names |
| ghidra only | 5 | annotate_native_function, inspect_native_data_type, inspect_native_instruction, inspect_native_load_image, resolve_native_call_targets |
| hopper only | 13 | comment, current_address, current_document, current_procedure, goto_address, inline_comment, list_bookmarks, next_address, prev_address, set_bookmark, set_comment, set_inline_comment, unset_bookmark |
| ida only | 0 | — |

- Every ghidra op's `effects` block: `launches_process:true`, `may_write_filesystem:true`, all others false — uniform because each op spawns an ephemeral Ghidra headless session. Shared limitations across ghidra ops: session serves results only after Ghidra auto-analysis completes (no partial results); imported Program + temp project are ephemeral and deleted on close (annotations edit session DB metadata, never original bytes); cancelling terminates the ephemeral DB; default-space addresses are lowercase `0x`-hex, other spaces `<percent-encoded>:0x<hex>`.
- source: `/tmp/rea-providers.json` `.analysis_provider_candidates[].capabilities[]`
- verify: `node -e 'const p=JSON.parse(require("fs").readFileSync("/tmp/rea-providers.json")); for(const c of p.analysis_provider_candidates) console.log(c.provider.id, c.capabilities.filter(o=>o.available).length, "of", c.capabilities.length)'`
- verified-at: 2026-10-13T15:19Z
- suggested: admit — corrects a likely misreading: op-level `available` is declared-surface, provider-level `availability` is the binding gate. The 17 ops we lose vs hopper (13 hopper-only + GUI-driven workflow) are unreachable without a Hopper install; ida adds nothing unique (its 12 ops are the shared core).

## Candidate: Non-analysis providers exist outside `analysis_provider_candidates` — 4 more provider ids observed via typed failures

- claim: `list-*`/`inspect-*-client` verbs bind additional providers that never appear in `analysis_provider_candidates`. Probed on-host:

| verb | result | provider_id | code / category | gate |
| --- | --- | --- | --- | --- |
| `rea list-adb-devices` | fail (exit 0) | `adb` | `capability_unavailable` / `unsupported_provider` | "The selected adb binary was not found: adb — Set REA_ADB_PATH to an absolute path to an existing adb binary" |
| `rea inspect-adb-client` | fail (exit 0) | `adb` | same | same `REA_ADB_PATH` remediation |
| `rea inspect-apktool-client` | fail (exit 0) | `apktool` | `capability_unavailable` / `unsupported_provider` | set `REA_APKTOOL_COMMAND` to an absolute apktool launcher (upstream wrapper or `java -jar` script) |
| `rea inspect-jeb-client` | fail (exit 0) | `jeb` | `capability_unavailable` / `unsupported_provider` | start a JEB client serving MCP (default `http://127.0.0.1:8425/mcp`) or set `REA_JEB_MCP_URL`; live probe `fetch failed` |
| `rea inspect-binary-layout /usr/bin/jq` | fail (exit **1**) | `pwntools-elf` (sole candidate) | `provider_unavailable` / `unavailable`, `retryable:true` | set `REA_PWNTOOLS_PYTHON` to a caller-supplied Python with pwntools 4.15.0 + pyelftools 0.33 + Unicorn 2.1.2; "REA never installs Python or packages"; `candidate_ids:["pwntools-elf"]` shows per-op provider pinning |
| `rea list-browser-targets` | VALIDATION_ERROR | — | input validation | `--endpoint <string>` required (CDP endpoint); no default loopback scan |

- Failure taxonomy nuance: `capability_unavailable`/`unsupported_provider` exits 0; `provider_unavailable` exits 1 and marks `retryable:true`. Total provider ids observed: **7** — ghidra, hopper, ida, adb, apktool, jeb, pwntools-elf. On this host only `ghidra` is bound-and-available.
- source: live runs above (stderr captured, JSON on stdout); r1-10 for corroboration of the pwntools-elf triple-requirement.
- verify: `npx -y rea-agents@6.4.0 inspect-adb-client --format json; npx -y rea-agents@6.4.0 inspect-jeb-client --format json; npx -y rea-agents@6.4.0 inspect-binary-layout /usr/bin/jq --format json; echo $?`
- verified-at: 2026-10-13T15:21Z
- suggested: admit — completes the provider inventory r1 doctor only partially covered (doctor inspects hopper/ghidra/ida only; `DOCTOR_PROVIDER_IDS` = `hopper|ghidra|ida`).

## Candidate: Server identity — catalog fingerprints and surface histogram pin the 6.4.0 tool inventory

- claim: `server_identity` reports package `rea-agents@6.4.0`, server `rea 6.4.0`, sdk `{server,client_test,core}=2.3.1`, skill `reverse-engineer-anything` expected_version "37", `build_commit:null`. `catalog.counts` = `{cli_commands:127, mcp_tools:170, mcp_prompts:6}` with digests `tools_sha256:25802f6d…0116`, `prompts_sha256:5296f030…c7a2`, `combined_sha256:85d80276…d72a`. The embedded `catalog.tools[]` (170 entries) tags each MCP tool with a `surface`; histogram: `official-proxy` 40, `adb-provider` 24, `session` 21, `application` 18, `enhanced` 14, `browser-provider` 12, `native-provider` 11, `artifact-provider` 7, `electron-provider` 5, `android-provider` 5, `jeb-provider` 4, `managed-provider` 3, `firmware-provider` 2, `apktool-provider` 2, `runtime-provider` 2 (sums to 170). 44 tools carry a mutating-ish effect (`mutatesTarget|writesFilesystem|mayDiscardData|destructive`), concentrated in adb package/file verbs, Hopper bookmark/comment setters, scenario capture, and artifact extraction.
- source: `/tmp/rea-providers.json` `.server_identity`
- verify: `npx -y rea-agents@6.4.0 capabilities --format json | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{const c=JSON.parse(s).server_identity.catalog;console.log(c.counts,Object.keys(c.tools).length)})'`
- verified-at: 2026-10-13T15:19Z
- suggested: admit — the sha256 digests are the drift-detection anchors for cross-host/version comparison; surface names corroborate the 7 provider ids (adb/apktool/jeb/electron/browser/native/firmware/managed/runtime/android surfaces vs the analysis trio).

## Summary

- **One envelope, two verbs**: `providers` and `capabilities` return the identical 8-key payload (only `started_at` differs). Provider truth lives in `analysis_provider_candidates`; host-level op truth in `capabilities`.
- **Host matrix (18 ops)**: 8 available — `decode_interface_builder`, `extract_artifact`, `inspect_artifact`, `inspect_keyed_archive`, `inspect_managed_artifact`, `inspect_managed_members`, `inspect_managed_native_boundaries`, `trace_dylib_resolution`; 10 `unsupported_host` (all macOS-gated). Nothing mutates the artifact; nothing needs root.
- **Provider matrix (7 ids)**: analysis trio = `ghidra` **available** 12.1.4 (8/8 checks, ephemeral headless sessions), `hopper` `executable_missing` at `/opt/hopper/bin/Hopper`, `ida` `not_configured` (`REA_IDA_MCP_CONFIG`); aux providers = `adb` (`REA_ADB_PATH`), `apktool` (`REA_APKTOOL_COMMAND`), `jeb` (`REA_JEB_MCP_URL`, probes `127.0.0.1:8425/mcp`), `pwntools-elf` (`REA_PWNTOOLS_PYTHON` pinned versions; sole candidate for `inspect_binary_layout`).
- **Op coverage**: 41-op union across providers; effective on-host = ghidra's 28. 12-op common core across all three; 5 ghidra-only; 13 hopper-only (GUI-navigation + annotation ops unreachable here); 0 ida-only.
- **Key semantics**: per-op `available` inside a candidate is *declared* capability — the real gate is provider-level `availability.status`. `capability_unavailable` exits 0; `provider_unavailable` exits 1 with `retryable:true`.
- **Drift anchors**: catalog counts 127 CLI / 170 MCP tools / 6 prompts; `tools_sha256:25802f6d…`, `combined_sha256:85d80276…`; skill expected_version 37.
- Open thread for later rounds: `provider_operation_health`, `analysis_provider_binding`, `analysis_run`, `analysis_activity.providers[]` are only observable after a target `open` — an open-target rerun would capture the bound-provider view.

## Errata (round 3)

- **"`capability_unavailable` exits 0" is WRONG (r3 audit-B, verified 2026-10-13):** verbatim
  re-runs of `list-adb-devices`, `inspect-adb-client`, `inspect-jeb-client` all exit **1** —
  identical to `provider_unavailable`. The real differentiator between the two failure kinds
  is the `retryable` field (`false` vs `true`), not the exit code. Rows in the table above
  recording "fail (exit 0)" reflect the report's misreading of pipe-masked exit status.
- **`record_pairs` confirmed MCP-only (r3 audit-B):** `grep -rn record_pairs dist/` hits only
  `dist/domain/bundleComparison.js` + `dist/server/registerBundleComparisonTool.js` — zero
  under `dist/cli/`. `rea compare --schema` exposes only `left`/`right`.
