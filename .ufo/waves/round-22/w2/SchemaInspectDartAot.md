# W2 SchemaInspectDartAot — REA 6.5.0 `inspect-dart-aot` schema authority review

Seat: `KaidokuR22R.SchemaInspectDartAot-6` (leaf scout, author-side only, not outside admission).
Scope: `--help` / `--schema` / `--llms` of `rea-agents@6.5.0 inspect-dart-aot` plus read-only package source, compared with frozen `.ufo/waves/round-22/claims.json` (R22-C1) and its counter. The target was not executed. No install, no device contact, no debug attach, no network beyond the npx package fetch (already cached).
Lane HEAD at review: `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` (baseline `7787fea4…` per claims).

## TL;DR

- **Admission boundary (observed):** the CLI takes one required positional `path` (a non-empty string) and one optional `--abi` (a string of 2–16 chars). Both schemas set `additionalProperties:false`. The CLI has **no `detail` option**. `detail: complete|summary` exists only on the MCP contract (`dartAotInspectionInputSchema`).
- **Operation binding (observed):** CLI `inspect-dart-aot` maps to operation `inspect_dart_aot`. That equals the R21 `bind` mapping `verb.replace('-','_')`, so a well-formed success record would bind under `count-c1.py`.
- **Prerequisites (observed):** Node/npx only. The provider is pure in-process parsing (`createFlutterBuildAnalysisProvider` says "needs no external tools", and `inspectAvailability()` always returns `available` with engine `static-apk-parsing`). It needs a writable `os.tmpdir()`, because the provider copies the APK to `rea-flutter-*/input.apk` and the selected library to `libapp.so`, then deletes them. No ADB, JEB, apktool, or Dart SDK is needed.
- **Carrier inventory (observed, full search):** the completed search found three APKs. The Godot 4.7.2 export templates (`android_release.apk`, `android_debug.apk`) are **not** Flutter carriers: their `lib/` holds only `libc++_shared.so` and `libgodot_android.so`, with no `libapp.so`. Source shows they would return typed refusal `unsupported_target`, which R21 `REFUSALS` and the R22-C1 falsifier "a typed refusal envelope counts" exclude. **`/tmp/kd22probe/saber.apk` is a Flutter carrier.** It is 42,305,081 B with sha256 `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`, which equals the expected F-Droid `com.adilhanney.saber_1360103.apk` hash in `.ufo/waves/round-22/gen-wave1.py`. It carries `lib/x86_64/libapp.so` (16,778,120 B) and `lib/x86_64/libflutter.so` (13,051,424 B), and **x86_64 is its only ABI**. It sits outside the lane in a prior agent's scratch dir (created 08:39 -0300), so it is not retained evidence. **[INFERENCE]** A held `inspect-dart-aot` run against Saber is the only route on this host to a bindable success record. The earlier "no Flutter carrier" blocker came from a search cut off at 120 s and is withdrawn.
- **Expected partial coverage (observed from prior identify output, inference for this verb):** `/tmp/kd22probe/fl.json` is a prior `identify-flutter-build` envelope (`ok:true`, `ev_f51ce1f05bfbf6acb3fd84533133be92c78a0fdeaa904410ddbbc5d0a66225b5`). It reports x86_64 `snapshot_hash_sources: 1`, hash `0451907c2eaa8467e848c0067bfe8ed4`, and `coverage: "partial"`, with the limitation "carries 1 snapshot section(s); a complete AOT payload carries two". **[INFERENCE]** `inspect-dart-aot` will probably also report `libapp.coverage:"partial"`. In R21 `bind`, `partial` is not a refusal (it is not in `REFUSALS` and is not an `error` member), so a partial success record should still bind. The knowledge entry must state the partial coverage and must not claim complete snapshot decoding.

## Commands, exits, outputs

All commands were run from `/tmp`. `npx -y rea-agents@6.5.0 --version` printed `6.5.0` (exit 0). The resolved package is `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (`package.json` version 6.5.0). A separate cache holds 6.7.0 (`a1722018f28f9df2`) and was **not** used.

| argv | exit | stdout | stderr |
|---|---|---|---|
| `npx -y rea-agents@6.5.0 inspect-dart-aot --help` | 0 | help text (below) | empty |
| `npx -y rea-agents@6.5.0 inspect-dart-aot --schema` | 0 | 400 B TOON, sha256 `c9f9f8cf…3a9f` | 0 B |
| `npx -y rea-agents@6.5.0 inspect-dart-aot --schema --format json` | 0 | 560 B JSON, sha256 `7e9c604f…bee6` | 0 B |
| `npx -y rea-agents@6.5.0 inspect-dart-aot --llms` | 0 | 320 B manifest, sha256 `411e11a4…37a4` | 0 B |
| `unzip -Z1 <godot android_release.apk> \| grep '^lib/'` | 0 | 8 entries, no `libapp.so`/`libflutter.so` | — |
| `unzip -Z1 <godot android_debug.apk> \| grep '^lib/'` | 0 | 8 entries, no `libapp.so`/`libflutter.so` | — |
| `timeout 120 find /home /opt /usr/share /tmp -type f \( -name '*.apk' -o -name '*.aab' -o -name '*.xapk' -o -name 'libapp.so' \) -size +10k` | killed at the 120 s timeout (wall 120.03 s), so the walk is **incomplete** | only the two Godot templates before the cutoff | — |
| `timeout 1200 find /home /opt /usr/share /tmp /srv /mnt /media …` (same predicates, stderr discarded) | find exit 1 (not the timeout's 124; most likely unreadable dirs), wall 242.16 s, walk completed | 2 Godot templates + `/tmp/kd22probe/saber.apk` | discarded |
| `sha256sum /tmp/kd22probe/saber.apk` | 0 | `de4813f9…b720` (matches `gen-wave1.py` expected) | — |
| `unzip -Z1 /tmp/kd22probe/saber.apk \| grep '^lib/'` | 0 | 6 entries, all `lib/x86_64/`, including `libapp.so` and `libflutter.so` | — |

`--help` stdout (verbatim core):

```
rea inspect-dart-aot — Inspect one ABI's Dart AOT snapshot: sections, headers, and the string pool
Usage: rea inspect-dart-aot <path> [options]
Arguments:
  path  Local APK carrying a Flutter payload
Options:
  --abi <string>  ABI under lib/ to inspect; defaults to the preferred one
Global Options: --filter-output --format <toon|json|yaml|md|jsonl> --full-output --help --llms/--llms-full --schema --token-count --token-limit --token-offset
```

`--schema --format json` stdout (verbatim):

```json
{"args":{"type":"object","properties":{"path":{"type":"string","minLength":1,"description":"Local APK carrying a Flutter payload"}},"required":["path"],"additionalProperties":false},
 "options":{"type":"object","properties":{"abi":{"description":"ABI under lib/ to inspect; defaults to the preferred one","type":"string","minLength":2,"maxLength":16}},"additionalProperties":false}}
```

## Exact input limits (observed: CLI schema vs. source)

| Limit | CLI `--schema` | Source authority (6.5.0 dist) |
|---|---|---|
| `path` | string, minLength 1, required | `localPathStringSchema` in `domain/flutter/flutterBuildAnalysis.js` (strictObject) |
| `abi` | string, 2..16 | additionally `regex /^[a-z0-9_\x2d]+$/u` in the domain schema. **The CLI JSON Schema does not show this regex**, so the CLI schema understates the admission rule. |
| `detail` | **absent** | Only in `dartAotInspectionInputSchema` (MCP). The CLI routes `FlutterBuildAnalysisService.execute` → `flutterRequestSchema`, which uses `flutterInputSchemas.inspect_dart_aot` without `detail`. CLI output is therefore always the complete observation. |
| Default ABI order | "preferred one" | `arm64-v8a, x86_64, x86, armeabi-v7a`, then the remaining ABIs alphabetically (`FlutterBuildProvider.js` L547–551) |
| APK size | — | `APK_MAX_BYTES` = 2 GiB → `resource_constraint`/`file-size` |
| ZIP metadata read | — | `APK_METADATA_READ_MAX_BYTES` = 8 MiB → `resource_constraint`/`memory` |
| libapp.so size | — | `LIBRARY_MAX_BYTES` = 256 MiB, checked on declared size and again while streaming. If the declared size is missing, it is treated as over budget. |
| ABI count | — | `MAX_FLUTTER_ABIS` = 32. Library path ≤ 1024 bytes. |
| String pool | — | `package_uris` ≤ 500 and `dart_uris` ≤ 500 are reported, and `class_like_tokens` ≤ 2000. Collection stops at 2× each bound; a run cap of 1024 bytes applies. Counts are `*_count_at_least` lower bounds. |
| ELF | — | Little-endian only (32-bit and 64-bit headers). Types ET_REL/ET_EXEC/ET_DYN. Symbols come from the dynamic symbol table: `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`. |
| Complete header decoding | — | Only kind 3 (the source comment calls it "Dart 2.14 FullAOT layout"). Other kinds are observed with `coverage:"partial"`. |

## Effects (observed: `contracts/toolEffects.js` L249–252)

`inspect_dart_aot: effects({ mutatesSession: true, writesFilesystem: true })`. Every other flag stays at its default false: `launchesProcess`, `accessesNetwork`, `executesForeignCode`, `mutatesDevice`, `mutatesTarget`, `changesUiState`, `mayDiscardData`. `idempotent` is true. `writesFilesystem` is the provider-owned temp snapshot (`mkdtemp(tmpdir(),"rea-flutter-")`, chmod 0400, removed in `discardRoot`). If cleanup fails on `close()`, the CLI projects an `AnalysisError`, so a cleanup failure becomes a refused envelope. The original APK is opened read-only, and its identity is revalidated after the copy (`artifact_changed` on mismatch).

## Output and operation binding (observed)

- CLI spec: `operation: "inspect_dart_aot"`, `toInput` = `{path, abi?}` (`cli/flutterCommands.js` L22–43).
- Provider identity: `{id:"flutter", name:"Flutter build identification", version:null}`. Subject is `{path, format:"apk", sha256}` and location is `artifact-path`.
- Success `normalized_result` schema (`flutterResultSchemas.inspect_dart_aot`): `target{path,bytes,sha256}`, `abi`, `libapp{coverage,bytes,sha256,snapshot_hash,snapshot_hash_candidates,snapshot_hash_sources,sections[{name,offset,size,magic_valid,kind,header_length}]}`, `string_pool{coverage,package_uris,package_uri_count_at_least,dart_uris,dart_uri_count_at_least,class_like_tokens,class_like_token_count_at_least,printable_run_count}`, `coverage`.
- Typed refusals in the source: `unsupported_target` (no libapp.so; ABI not present, with the available list; no recognizable snapshot symbols), `resource_constraint` (the size and count budgets above), `invalid_input` (schema), `access_denied`, `artifact_changed`, `cancelled`, `protocol`.

## Comparison to R22-C1 and the counter mapping

1. **Verb and operation match (observed).** `count-c1.py` T1 includes `inspect-dart-aot`. R21 `bind` derives `inspect_dart_aot`, which equals the CLI spec operation.
2. **Carrier shape (observed).** `--format json --full-output` emits `{ok,data,meta}`. R21 `records()` only descends `evidence/evidences/records/result`, so the raw envelope does **not** bind. The `data` member must be extracted unchanged into a bare record file, as was done for `identify-godot.evidence.json`. The record must carry `ev_<64hex>` (`HEX64` requires the `ev_` prefix) and `operation:"inspect_dart_aot"`.
3. **Refusal exclusion (observed).** `unsupported_target` and `resource_constraint`-class codes are in R21 `REFUSALS` or are carried in `error` members. A Godot run would be a refused record, which the claim's falsifiers exclude.
4. **Source gate (observed).** Counted entries must cite a mined S051+ row dated 2026-10-21 whose used-by names the entry. Existing `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` cites S051/S052/S053 and covers only `identify-flutter-build` as a negative. It states that "Dart snapshot parsing … not established".
5. **Frozen and working counter divergence (observed, relevant to the authority chain).** `frozen/count-c1.py` sha256 `d7f67075…04aa` differs from `tools/count-c1.py` sha256 `5fbc6868…dd61`. `tools/` adds the S051+/mined/2026-10-21 source-row eligibility gate and `--selftest`, and makes `--root/--rev` optional. The frozen version lacks the source gate. **[INFERENCE]** The two counters can disagree on an entry that binds evidence but fails the source gate. L1 should state which one is authoritative for R22-C1 `counting_command` (claims.json names `.ufo/waves/round-22/tools/count-c1.py`).
6. **Claim calibration and path to counting.** Until a held run is retained, `inspect-dart-aot` stays not exercised, and "k/6 reported exactly as measured" covers that. **[INFERENCE]** The route to counting it, for the execution seat and not this one:
   1. Copy or verify Saber (sha256 `de4813f9…b720`) into lane scratch.
   2. Run `npx -y rea-agents@6.5.0 inspect-dart-aot saber.apk --format json --full-output`. `--abi x86_64` is redundant because it is the only ABI.
   3. Retain the argv, exit and envelope under `.ufo/waves/round-22/evidence/c1/`, and extract `data` unchanged to a bare record.
   4. Cite the `ev_` id and the file path from a new `corpus/knowledge/2026-10-21-r22-*.md` whose `source:` line names a mined S051+ row dated 2026-10-21 that lists the entry in used-by.

   `libapp` is 16,778,120 B and the APK is 42,305,081 B, both well under the 256 MiB and 2 GiB budgets, so no `resource_constraint` is expected.

## Source paths (6.5.0, `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`)

| File | sha256 |
|---|---|
| `cli/flutterCommands.js` | `8354ba86bc42c73a785c3ed9b99f0f8a702d1b0be5fe6d798b76d6ee35da0d18` |
| `flutter/FlutterBuildProvider.js` | `2c00116a02ee3e9a483886a14ec84d7f224899c8807c84c999bcca49b043d191` |
| `domain/flutter/flutterBuildAnalysis.js` | `c8cac80550d266e1741142bfd9e88a87381fc0fd25485b4ea6ed0db25538ddf2` |
| `application/flutter/DartAotInspection.js` (MCP only) | `e8c2904eeaee5ad917d61a7c13a72ac53244617879509b41b8d824690a7cd1c9` |
| `contracts/flutter/flutterToolContracts.js` | `8150d522e7dc4fec43cfe0d93aa4ef06ca7d4bd61fd45f3c72e6cb89de130d3e` |
| `contracts/toolEffects.js` | `1d12ce7f0ab94c1f2e1caf3903008da318f5dbccb04d102bdc4e8efa3e2814f8` |
| `flutter/DartElf.js` | `2f66242747848e36ca91e9ea56e94e632911f0fa351f80439eda4f0bf4d52af8` |

Other relevant files: `composition/flutter.js`, `server/registerFlutterTools.js`, `domain/analysisErrorProjection.js` (L146 `unsupported_target`, L150 `resource_constraint`).

## Observed / inference / unknown

- **Observed:** everything cited in the tables above, including help, schema, argv, exits, source lines, hashes, and the APK `lib/` inventories.
- **Inference:** a Godot input yields an `unsupported_target` refusal; the frozen and working counters may disagree; a Saber run would probably succeed with `coverage:"partial"` and still bind.
- **Unknown:** paths outside the searched roots (`/home /opt /usr/share /tmp /srv /mnt /media`) and any dirs `find` could not read (exit 1, stderr discarded). Actual CLI rejection text for an `--abi` value that violates the regex or for an unknown `--detail` flag (not probed, help/schema only). Actual `inspect-dart-aot` output on Saber (not run). Whether the kind-3 "Dart 2.14" decoding matches Saber's snapshot kind.

## Tooling

No installs or updates. `rea-agents@6.5.0` was already in the npx cache. No pacman transaction was made.
