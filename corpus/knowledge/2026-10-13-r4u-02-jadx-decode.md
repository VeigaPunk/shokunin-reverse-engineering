<!-- corpus entry — kaidoku-shokunin round 4 unlock wave (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4u/02-jadx-decode.md. -->

# kaidoku-r4u / 02 — First real APK decode: jadx + apktool unblocked

r3-06 recorded `capability_unavailable`/`retryable:false` on both Android
providers. With `REA_JADX_MCP_JAR` (sha256 `6e5eacf5…`, verified) and
`REA_APKTOOL_COMMAND=/usr/bin/apktool` (3.0.3) now provisioned, this lane ran
the full decode surface on the Godot 4.7.2 export templates: debug
(`android_debug.apk`, 127 260 725 B, sha256 `59e0073f…`, 13 dex) and release
(`android_release.apk`, 104 803 333 B, sha256 `6d1bb2cf…`, 1 dex). All runs
exit 0, `rea-agents@6.4.0`, JDK 21.0.12.1.

## Candidate 1 — `inspect-android-package` decodes manifest + census, decompiles nothing

- claim: on the 127 MB / 13-dex debug APK the verb succeeds in ~8 s and its
  `normalized_result` is declarations-only: `engine` (jadx-headless-mcp 0.7.1,
  artifact_sha256 `6e5eacf5…`, source_revision `5844800a…`, worker 1, heap
  7748 MiB), `package_name com.godot.game`, `version_name 1.0` /
  `version_code 1`, `min_sdk 24`, `target_sdk 36`, `permissions []` (empty —
  the template declares none), `manifest {status:"complete", text: full
  decoded XML}`, `class_count 1925`, `resource_count 129`,
  `signature_verification:"not_performed"`. The bridge transcript shows
  exactly four calls — `rea_jvm_status`, `load_apk` (3 285 ms,
  `metadata_scope:"parsed_members"`, `decompile_timeout_ms:90 000`,
  `code_cache_size:64`), `get_app_info`, `get_android_manifest` — so jadx
  *parses* all 13 dex into a merged 1925-class census but emits no decompiled
  code. There is no per-dex attribution anywhere: the "which of the 13 dex
  fit the budget" question is moot — no decompile budget is consumed at this
  scope, and dex-level granularity is not exposed by this verb.
- source: `npx -y rea-agents@6.4.0 inspect-android-package
  /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_debug.apk
  --format json` → evidence `ev_d760cc5cbda1030285b1879fb0819ca5b1c586ef53ef23d40660819d1e2b8a52`,
  `confidence:"observed"`, `authority:"shipped-artifact"`, bridge
  `rea-jadx-bridge` v1, bridge_sha256 `5a5a4e32…`. Manifest content:
  `android:debuggable="true"`, activity `com.godot.game.GodotApp`
  (singleInstancePerTask, landscape, PiP) + exported `activity-alias`
  `GodotAppLauncher` (MAIN/LAUNCHER), `org.godotengine.godot.utils.
  ProcessPhoenix` on `:phoenix`, androidx `FileProvider`,
  `InitializationProvider`, `ProfileInstallReceiver`; meta-data
  `org.godotengine.library.version=4.7.2.stable`; glEsVersion 0x30000.
- verify: rerun the command; `jq '.raw_result.calls[].operation'` shows the
  4-call transcript; `jq '.normalized_result.manifest.status'` → `complete`.
- verified-at: 2026-10-13
- suggested: admit — this is the APK declaration surface, held. Note the verb
  is census+manifest only; per-class/member/decompile live on sibling verbs
  (candidate 4).

## Candidate 2 — `decode-android-resources` decodes arsc + strings + manifest; deterministic evidence id

- claim: apktool 3.0.3 leg succeeds in ~6 s, `coverage:"complete"`,
  `decoded_file_count:232`. `normalized_result` carries `client{command:
  /usr/bin/apktool, command_source:"environment"}`, `target{path, bytes,
  sha256}` (identity is inside normalized_result, not the envelope),
  `metadata{package,version_code,sdk}`, `manifest` = full decoded XML in
  apktool's own serialization (attributes alphabetized, same semantics as
  jadx's render), `strings` = 11 default-locale entries
  (`godot_project_name_string="godot-project-name"`, `gabe_connection_*`,
  `error_engine_setup_message`, `dialog_*`, …), `locales` = 92 declared
  locales (`af…zu` incl. `b+sr+Latn`, `en-rXC`), `locale:null`. Two quirks:
  `subject:null` and `raw_result:null` — the envelope carries no artifact
  identity object (limitation: "Artifact identity is unavailable for this
  observation") and no transcript. Smali is deliberately skipped:
  "Decoding skips smali (--no-src); Java-source recovery belongs to the JADX
  family". Evidence id `ev_a78193a3…` is byte-identical to the parent's
  smoke-run id — this verb's evidence is content-deterministic.
- source: `npx -y rea-agents@6.4.0 decode-android-resources <debug.apk>
  --format json` → `ev_a78193a347b799e7defa658c0a5a9c8abb593b6fef13c777c6608bc6ee9a1265`.
  Schema: args `{path}`; options `locale` (2–16 chars, BCP-47-ish pattern)
  and `no-strings`.
- verify: rerun → identical evidence id; `jq '.normalized_result.strings |
  length'` → 11, `.decoded_file_count` → 232.
- verified-at: 2026-10-13
- suggested: admit — held. Frontier: `--locale <xx>` projections (92
  available) and `project-android-application-graph` over this evidence.

## Candidate 3 — debug-vs-release delta is exactly `debuggable`, dex count, and 5 kotlin shims; NEITHER apk is signed

- claim: `inspect-android-package` on `android_release.apk` succeeds with the
  same shape (`ev_f05731d561f7b20b4dacdca77f9d72e934f7cdb8724084fdedb474c43842164f`),
  `class_count 1920`, `resource_count 121`. The decoded manifests `diff` to
  exactly one line: debug carries `android:debuggable="true"`, release omits
  it — same package/version/sdk/permission set/component tree otherwise.
  Zip census: debug 129 entries / 13 dex, release 121 entries / 1 dex
  (`classes.dex`); release-only members `assets/dexopt/baseline.prof` +
  `.profm` and `META-INF/version-control-info.textproto`.
  `search-android-classes` on release (ev `ev_edb28274…`, 1920) diffed
  against debug's 1925: the delta is exactly
  `kotlin.UByte$$ExternalSyntheticBackport1..5` — D8 desugar shims, not app
  code. Signing: `signature_verification:"not_performed"` on both, and the
  gap is real — neither APK has v1 entries (no `META-INF/*.SF|.RSA|.DSA`)
  nor a v2+ block (`APK Sig Block 42` magic absent in both files, counted
  byte-wise). These are unsigned base templates; "signed vs debug" produces
  no signature-axis difference here — only the manifest flag, multidex, and
  build-metadata members differ.
- source: diff of both `normalized_result.manifest.text` payloads → `25d24
  < android:debuggable="true"`; `unzip -l` on both; class-list diff of the
  two `search-android-classes ""` inventories.
- verify: commands above; `grep -c 'APK Sig Block 42'` / python byte count →
  0 on both APKs.
- verified-at: 2026-10-13
- suggested: admit — held. The signing axis stays unobservable through this
  provider even when signatures exist (`not_performed` is declared
  limitation); apksigner/keytool are outside the REA surface.

## Candidate 4 — the decompile axis lives on class/method verbs, all working

- claim: the sibling jadx verbs (same env, ~8 s each — every CLI call spawns
  a fresh JVM and re-loads the full 127 MB APK, `load_duration_ms` ~3.3–3.9 s;
  no session reuse across invocations):
  - `search-android-classes <apk> ""` → `ev_a89cefe1d91afc95f85e922a2a3972bbd9fe5309b2a0329fb90aeb3129cb8193`,
    `total_classes:1925`, `coverage:"complete"`, `matches[]` = all 1925 names
    (androidx/kotlinx bulk + the `org.godotengine.godot.*` tree incl.
    `editor.utils.EditorUtils`/`GameMenuUtils` — editor classes ship in the
    debug template dex).
  - `inspect-android-class <apk> com.godot.game.GodotApp` → `ev_3dd127618d95b436fb3e6ac4e6eaebabfc501b1a3f336581f8c307cfae29b70c`,
    member inventory: 1 field (`updateWindowAppearance: Runnable`), 10
    methods with `reported_signature` display types, `dex_descriptor:null`
    throughout, `is_constructor`/`overload_index` per member.
  - `inspect-android-method <apk> com.godot.game.GodotApp onCreate` →
    `ev_ec92f4d14b1433d5222765353d712cdc904e8034c1b348b7cf898c98aebee02e`,
    `representation:"java"`, `body_status:"available"`, `fell_back:false`,
    `overload_count:1`, and real decompiled source —
    `public void onCreate(Bundle)` body with `SplashScreen.installSplashScreen`,
    `EdgeToEdge.enable`, `getGodot().getDisableGodotSplash()` guard, and the
    `GodotApp$$ExternalSyntheticLambda0` keep-on-screen shim. Bridge calls:
    `rea_jvm_status, load_apk, get_class_summary, get_method_body`.
- source: the four commands above under the same env; schemas: class verb
  args `{path,className}`, method verb `{path,className,methodName}` +
  `--overload-index` (required when ambiguous).
- verify: rerun each; `.normalized_result.source.text` on the method verb.
- verified-at: 2026-10-13
- suggested: admit — held. This completes the dex axis r3 left blocked:
  inventory → members → Java bodies all reachable. Cost note for future
  waves: budget ~8 s + one full APK reload per CLI call, so batch class
  selection deliberately rather than per-class probing at scale.

## Candidate 5 — evidence-id determinism differs per provider (jadx per-run, apktool content-stable)

- claim: jadx-family verbs mint a fresh `evidence_id` every invocation on
  identical input: three runs of `inspect-android-package` on the same debug
  APK produced `ev_e774f2bb…` (parent smoke), `ev_d760cc5c…`,
  `ev_a5eebe8f…` — while `normalized_result` diffs byte-identical across
  runs. Cause is structural: `raw_result` embeds the per-invocation mkdtemp
  staging path (`/tmp/rea-android-{kuhLd2,xEWTq8,bRe4fH}/target.apk`) plus
  `load_duration_ms`, so the hashed envelope is never run-stable. The
  apktool verb carries `subject:null`/`raw_result:null` and reproduces the
  parent's smoke id exactly (`ev_a78193a3…` == `ev_a78193a3…`).
- source: rerun command + `jq '.evidence_id, .raw_result.loaded.apk_path'`;
  `diff` of `.normalized_result` across two runs → identical.
- verify: rerun `inspect-android-package` twice and compare ids vs
  normalized payload.
- verified-at: 2026-10-13
- suggested: admit — evidence ids for jadx runs are per-invocation receipts,
  not artifact keys; cite `subject.digest.sha256` + normalized content when
  cross-referencing evidence, and expect dedup-by-evidence-id to fail for
  this provider family.

## Typed refusals / coverage limits observed

- None on any of the 7 runs — every call returned exit 0 with
  `confidence:"observed"`. The r3 `capability_unavailable` refusals were
  purely config-gated; both env keys satisfy them.
- Declared limitation block (all jadx verbs, verbatim): static-only, no
  runtime behavior; provider display types, no DEX descriptors/offsets,
  engine-local overload indices; parsed-metadata inventories may include
  synthetic members absent from decompiled source; APK signatures, split
  APKs, native libraries and runtime capture are NOT verified.
- decode-android-resources: `subject:null` + `raw_result:null` (no
  envelope-level artifact identity, no transcript); smali skipped by design;
  `decoded_file_count` is a count only — the 232 decoded files are not
  enumerated in the result; strings default-locale unless `--locale` given.
- inspect-android-package: no per-dex breakdown — `class_count` is a merged
  census across all dex members; no method-level or code content at all.
- `.so` members (8×, incl. 91 MB `libgodot_android.so`) are untouched by
  both verbs — they remain `analyze`/`inspect-artifact` territory per r3-06.

## Run log

- `export REA_JADX_MCP_JAR=~/.local/opt/jadx-headless-mcp/jadx-headless-mcp-0.7.1-all.jar
  REA_APKTOOL_COMMAND=/usr/bin/apktool`; jar sha256 re-verified
  `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75`;
  `apktool --version` → 3.0.3; `java -version` → 21.0.12.1.
- `inspect-android-package --schema` → args `{path}` only;
  `decode-android-resources --schema` → args `{path}` + options
  `{locale, no-strings}`; `search-android-classes` `{path,query}`;
  `inspect-android-class` `{path,className}`; `inspect-android-method`
  `{path,className,methodName}` + `--overload-index`.
- `inspect-android-package <debug>` → exit 0, ~8.1 s, `ev_d760cc5c…`,
  load 3 285 ms, 1925 classes / 129 resources, manifest complete,
  `signature_verification:not_performed`.
- `decode-android-resources <debug>` → exit 0, ~5.7 s, `ev_a78193a3…`
  (== parent smoke id), apktool 3.0.3, 232 files, 11 strings, 92 locales,
  coverage complete, `subject:null`, `raw_result:null`.
- `inspect-android-package <release>` → exit 0, ~8.0 s, `ev_f05731d5…`,
  1920 classes / 121 resources; manifest diff vs debug = `-debuggable` only.
- `search-android-classes <debug> ""` → `ev_a89cefe1…`, 1925 matches,
  complete; `<release> ""` → `ev_edb28274…`, 1920; diff = 5
  `kotlin.UByte$$ExternalSyntheticBackport*` debug-only.
- `inspect-android-class <debug> com.godot.game.GodotApp` →
  `ev_3dd12761…`, 1 field + 10 methods, `dex_descriptor` null everywhere.
- `inspect-android-method <debug> com.godot.game.GodotApp onCreate` →
  `ev_ec92f4d1…`, java source returned, `fell_back:false`.
- `inspect-android-package <debug>` re-run → `ev_a5eebe8f…`,
  staging `/tmp/rea-android-bRe4fH/target.apk`; normalized_result identical
  to first run → per-run evidence ids confirmed.
- `unzip -l` census: debug 129 entries/13 dex/8 so; release 121/1 dex/8 so;
  release-only `assets/dexopt/baseline.prof{,m}`,
  `META-INF/version-control-info.textproto`.
- Signing check: no `META-INF/*.SF/.RSA` in either APK; python byte-count of
  `APK Sig Block 42` → 0 in both → both templates unsigned.
- Scratch under `/tmp/kaidoku-r4u-*`, `/tmp/mf-{debug,release}.xml`,
  `/tmp/nr{1,2}.json`, `/tmp/classes-{debug,release}.txt`; engine staging
  dirs `/tmp/rea-android-*` are provider-owned mkdtemp scratch.

## Summary

The Android-decode axis is **held end to end**. `inspect-android-package`
(jadx 0.7.1) delivers the declaration surface — complete decoded manifest,
package/version/sdk metadata, merged class+resource census — and
`decode-android-resources` (apktool 3.0.3) delivers the resource surface —
decoded manifest, 11 default strings, 92 locales, 232 files — both in
seconds on a 127 MB 13-dex APK with zero refusals. The 13-dex budget worry
was misplaced at this scope: the verb decompiles nothing; real Java bodies
live on `inspect-android-method` (verified: `GodotApp.onCreate` decompiled
clean, `representation:"java"`), with `search-android-classes` and
`inspect-android-class` covering inventory and members. Debug-vs-release
delta is precisely `android:debuggable`, multidex (13→1), 5 kotlin desugar
shims, and build-metadata members — neither template is signed and the
provider never checks (`not_performed` is honest). Watch-items: jadx
evidence ids are per-run (mkdtemp path in `raw_result`), apktool emits
`subject:null` envelopes, every CLI call pays a fresh ~3.5 s full-APK load,
and `.so`/signature/split-APK axes remain outside both providers.
