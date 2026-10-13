<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/06-apk-inventory.md. -->

# 06 — APK archive inventory + archive→native bridge (round 3)

Rounds 2–3 covered PE/ELF leaf binaries. This round exercises the container
frontier: `inspect-artifact` member inventory on a real 127 MB Godot export
APK, then bridges one extracted member into the native `analyze` path, then
records the typed refusals on the Android-decode providers (jadx/apktool)
that are not configured on this host.

## Candidates

### Candidate 1 — `inspect-artifact` on `android_debug.apk` (run)

- **claim:** `rea inspect-artifact` inventories a real APK as a
  content-addressed artifact graph (dedup'd nodes + path-bearing occurrences
  + `contains` edges), verifies every member hash, and surfaces the APK as
  `format: "apk"` without needing any Android tooling.
- **source:** `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_debug.apk`
  (Godot 4.7.2.stable Android debug export template; 127,260,725 bytes).
- **verify:**
  - Identity: `sha256sum` → `59e0073f0fa59f552684a861d8f4266b0b34b488a140d6657eac7dd70d1a0a0d`;
    `file` → `Android package (APK), with gradle app-metadata.properties`;
    `unzip -l` → 13 `classes*.dex`, 8 `.so` libs across arm64-v8a /
    armeabi-v7a / x86 / x86_64 (`libgodot_android.so` up to 91 MB), binary
    `AndroidManifest.xml`, `res/*`, `META-INF` gradle metadata.
  - Schema (`inspect-artifact --schema`): `args.path` required (positional
    on the CLI — `--path` is rejected as `Unknown flag`); sole option
    `integrityPolicy ∈ {fail, record-and-continue}`, default `fail`
    (`--integrity-policy` on CLI).
  - Result envelope: `evidence_id ev_5a05f956…`, provider `rea-artifact-graph`
    v1, `operation: inspect_artifact`, `authority: "shipped-artifact"`,
    `confidence: "observed"`. One substep `inventory_artifact` → `completed`.
  - Inventory structure: `manifest{manifest_id, root_artifact_id,
    root_sha256, root_format:"apk", graph_sha256, node_count:120,
    occurrence_count:130, edge_count:129}` — 130 ZIP central-directory
    occurrences dedup to 120 content nodes. `nodes[]` carry
    `artifact_id, format, sha256, size, media_type, architecture,
    content_state("embedded"), limitations[]`; `occurrences[]` carry
    `logical_path, entry_kind, artifact_kind, artifact_format,
    declared_size, compressed_size, executable, encrypted, hash_status`;
    `edges[]` carry `parent_artifact_id, relation:"contains", ordinal,
    occurrence_id`.
  - Node format histogram: `elf`×8 (the `.so` set), `file`×110 (dex, res,
    manifest — dex/xml get no format-specific detection), `zip`×1 (the root
    APK), `mach-o-universal`×1.
  - **All 130 occurrences `hash_status: "verified"`**;
    `integrity_contradictions: []`.
  - Quirk worth logging: the single `mach-o-universal` node is
    `DebugProbesKt.bin` (1,738 bytes) — Kotlin's debug-probe blob whose
    leading `0xCAFEBABE` collides with Mach-O fat magic. Format-sniffing
    false positive, not a real Mach-O.
  - Declared limitation (verbatim): "ZIP inventory lists central-directory
    entries only. Bytes after the central directory, including an APK
    Signing Block or a ZIP comment, are not occurrences." — i.e. the
    signature block is structurally invisible to this path.
- **verified-at:** 2026-10-13T15:45Z
- **suggested:** mark the archive-inventory path **held** for APK/ZIP-class
  containers. Frontier: archives with APK Signing Block vs
  `integrityPolicy: record-and-continue`, nested containers (AAP→AAB, zip-in-
  zip), and dex member semantics (currently `file`, no dex recognition).

### Candidate 2 — archive→native bridge: `analyze` on extracted member (run)

- **claim:** a member listed by the artifact graph can be extracted,
  independently re-hashed, and fed to `rea analyze` — the artifact graph's
  `elf` typing and per-member sha256 give the bridge a verifiable handoff.
- **source:** `lib/arm64-v8a/libc++_shared.so` inside the APK
  (artifact_id `art_22eb01a8…`, declared_size 1,374,336,
  `hash_status: verified` per the graph).
- **verify:**
  - `unzip -o -j <apk> 'lib/arm64-v8a/libc++_shared.so' -d /tmp/kaidoku-r3-apk`
    → `sha256 c4c2fe5cbcb1fba0003a31fc7ab29a9bb12df6cc187ec45a806462540e83d93b`;
    `file` → `ELF 64-bit LSB shared object, ARM aarch64, for Android 21,
    built by NDK r28, stripped`.
  - `rea analyze <so> --format json` → success, evidence
    `ev_63bb52bd…`, provider chain `rea-workflow` → `ghidra` 12.1.4,
    `import_mode: ephemeral-source-immutable`, `architecture: arm64`
    (auto-from-header), document `target-c4c2fe5cbcb1.so`.
    Result: `segment_count: 32` (incl. `.note.android.ident`,
    `.dynsym`, `.text`, `__lcxx_override`), `procedure_count: 3009`,
    `string_count: 3332`. No typed failure; stripped binary still produced
    full procedure inventory via dynsym.
  - Cross-check: extracted-file sha256 matches the graph's node sha256 for
    that artifact_id — provenance chain closes end to end.
- **verified-at:** 2026-10-13T15:45Z
- **suggested:** archive→native bridge **held**. Note `analyze` accepted the
  raw `.so` directly; the CLI exposes no `open-binary` command — the MCP-side
  `open_binary` capability maps onto `analyze`/`inspect-*` surface. Frontier:
  `analyze` on `libgodot_android.so` arm64 (76 MB) for scale, or the
  armeabi-v7a/x86 sibling members for architecture coverage.

### Candidate 3 — `inspect-android-package` typed refusal (run, refused)

- **claim:** the Android-package inspection path fails closed with a typed,
  non-retryable refusal when its jadx provider is unconfigured — no partial
  decode, no silent fallback to `inspect-artifact`.
- **source:** same APK; `rea inspect-android-package --schema` then `--format json` run.
- **verify:**
  - Schema: `args.path` required ("Local standalone APK path"), no options.
  - Run → exit 1, `{"code":"capability_unavailable",
    "category":"unsupported_provider", "retryable":false}`;
    `details.provider_id: "jadx"`, `operation: "inspect_android_package"`,
    remediation: set `REA_JADX_MCP_JAR` to a caller-supplied
    `jadx-headless-mcp 0.7.1` JAR — "REA does not download or install it."
  - Sibling probe `rea decode-android-resources <apk>` → same shape,
    `provider_id: "apktool"`, `operation: "decode_android_resources"`,
    `retryable:false`, remediation: set `REA_APKTOOL_COMMAND` to an absolute
    apktool launcher.
- **verified-at:** 2026-10-13T15:45Z
- **suggested:** record jadx + apktool as **blocked-by-config** providers on
  this host (needs operator-supplied JAR/launcher). The manifest/dex/resource
  axis cannot advance until `REA_JADX_MCP_JAR` or `REA_APKTOOL_COMMAND` is
  provisioned; do not retry in-loop.

### Candidate 4 — `inspect-binary-layout` provider refusal (run, refused)

- **claim:** the lightweight ELF layout path (pwntools-elf) is also
  unconfigured — `analyze`/Ghidra is the only working native entry on this
  host.
- **source:** extracted `libc++_shared.so` (same as candidate 2).
- **verify:** `rea inspect-binary-layout <so>` → exit 1,
  `{"code":"provider_unavailable","category":"unavailable",
  "retryable":true}`; `candidate_ids:["pwntools-elf"]` rejected with
  `provider_unavailable` — needs `REA_PWNTOOLS_PYTHON` = python with
  pwntools 4.15.0 + pyelftools 0.33 + Unicorn 2.1.2.
- **verified-at:** 2026-10-13T15:45Z
- **suggested:** retryable in principle (env-var provisioning only), but
  redundant while Ghidra covers ELF layout; low priority.

## Run log

- `ls -la` + `sha256sum` + `file` on target APK → exists, 127,260,725 B,
  sha256 `59e0073f…`, "Android package (APK)".
- `unzip -l <apk> | head` → 134 total lines; 13 dex, 8 `.so` across 4 ABIs,
  binary manifest.
- `npx -y rea-agents@6.4.0 inspect-artifact --schema` → args `{path}`, opts
  `{integrityPolicy}`; `inspect-android-package --schema` → args `{path}` only.
- `inspect-artifact --path <apk>` → `UNKNOWN / Unknown flag: --path` (flags
  are positional; retried `<apk>` positional → success).
- `inspect-artifact <apk> --format json` → evidence `ev_5a05f956…`;
  manifest 120 nodes / 130 occurrences / 129 edges; all occurrences
  `hash_status: verified`; `integrity_contradictions: []`; ELF×8,
  `mach-o-universal` false-positive on `DebugProbesKt.bin`.
- `unzip -o -j <apk> 'lib/arm64-v8a/libc++_shared.so' -d /tmp/kaidoku-r3-apk`
  → sha256 `c4c2fe5c…`; `file` → ELF aarch64 Android NDK r28 stripped.
- `analyze /tmp/kaidoku-r3-apk/libc++_shared.so --format json` → evidence
  `ev_63bb52bd…`, Ghidra 12.1.4 upstream; 32 segments / 3,009 procedures /
  3,332 strings.
- `inspect-android-package <apk>` → `capability_unavailable` /
  `unsupported_provider` / provider `jadx` / `retryable:false` (needs
  `REA_JADX_MCP_JAR`).
- `decode-android-resources <apk>` → `capability_unavailable` / provider
  `apktool` / `retryable:false` (needs `REA_APKTOOL_COMMAND`).
- `inspect-binary-layout <so>` → `provider_unavailable` / `pwntools-elf` /
  `retryable:true` (needs `REA_PWNTOOLS_PYTHON`).
- `doctor --format json` → `healthy:false`: ghidra 12.1.4 + java 21 + node
  24.21.0 healthy; `hopper` and `ida-registration` `missing_analysis_engine`;
  `skill:identity` + 5 MCP registrations `config_drift`. jadx/apktool/
  pwntools are not doctor-scope checks — they surface only at call time.
- Cleanup: `rm -rf /tmp/kaidoku-r3-apk` and all `kaidoku-r3-{inspect-artifact,
  analyze-so*,doctor}.json` scratch files. `/tmp/rea-ghidra-*` untouched.
  Other `/tmp/kaidoku-r3-*` files belong to sibling lanes — left alone.

## Summary

**Archive-inventory path held; archive→native bridge held; Android-decode
providers refused cleanly.** `inspect-artifact` turned the 127 MB Godot APK
into a verified content-addressed graph — 130 occurrences dedup'd to 120
sha256-keyed nodes, all hash-verified, ELF members correctly typed — with an
explicit structural limitation (APK Signing Block invisible). One extracted
arm64 member re-hashed byte-identical to its graph node and completed full
Ghidra analysis (3,009 procedures on a stripped NDK lib), closing the
container→native provenance loop. `inspect-android-package` and
`decode-android-resources` both fail closed `retryable:false` pending
operator-supplied jadx/apktool; `inspect-binary-layout` needs pwntools and is
redundant while Ghidra stands. Frontier: dex/manifest semantics (blocked on
jadx/apktool), signing-block integrity policy behavior, and the 76–91 MB
`libgodot_android.so` members as an analyze-scale probe.
