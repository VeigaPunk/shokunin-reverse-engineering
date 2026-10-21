# R23-C1 — inspect-dart-aot: CLI schema, exact four dynamic symbols, static-symtab eligibility

Seat: KaidokuR23.SchemaDart (read-only scout; leaf; author-side report, not outside verification).
Scope executed: `inspect-dart-aot --help` / `--schema`, installed REA 6.5.0 implementation, plus offline
static ELF reads and non-counting synthetic probes. No debugger/Frida, no device, no APK execution,
no MCP device, no network fetch. All claims below are observations from files/commands except where
explicitly marked **[INFERENCE]** or **[UNKNOWN]**.

## Findings

### 1. Command surface (observation)

Exact output of `npx -y rea-agents@6.5.0 inspect-dart-aot --help` (exit 0):

```
rea inspect-dart-aot — Inspect one ABI's Dart AOT snapshot: sections, headers, and the string pool

Usage: rea inspect-dart-aot <path> [options]

Arguments:
  path  Local APK carrying a Flutter payload

Options:
  --abi <string>  ABI under lib/ to inspect; defaults to the preferred one

Global Options:
  --filter-output <keys>   --format <toon|json|yaml|md|jsonl>   --full-output
  --help   --llms, --llms-full   --schema   --token-count   --token-limit <n>   --token-offset <n>
```

`--schema` (exit 0) is only the CLI projection:

```
args: {path: string(minLength 1)}
options: {abi: string(minLength 2, maxLength 16)}
additionalProperties: false
```

- `--abi` is the only command-local option. The documented preference order is
  `arm64-v8a, x86_64, x86, armeabi-v7a, then remaining ABIs alphabetically`
  (`dist/domain/flutter/flutterBuildAnalysis.js:15-22`).
- `detail: "complete"|"summary"` exists in the provider/MCP schema
  (`flutterBuildAnalysis.js:25-27`; contract inputSchema at `dist/contracts/flutter/flutterToolContracts.js:23-27`;
  consumed at `dist/application/flutter/DartAotInspection.js:11-25`) but is **not** wired into the CLI
  (`dist/cli/flutterCommands.js:21-43` omits it). Observed: `--detail summary` →
  `{"code":"UNKNOWN","message":"Unknown flag: --detail"}`, exit 1. So summary delivery is MCP-only in 6.5.0.
- The tool description itself is the contract headline: "the four snapshot symbols located through the
  **ELF dynamic symbol table** with their offsets, sizes, and section headers (magic, kind, length)"
  (`flutterToolContracts.js:25`).
- Output schema (`flutterBuildAnalysis.js:92-140`): `libapp.sections[] = {name, offset, size, magic_valid,
  kind, header_length}`, plus `snapshot_hash`, `snapshot_hash_candidates`, `snapshot_hash_sources`,
  `libapp.coverage`, `string_pool.*`, top-level `coverage`. `sections[]` is documented as "Snapshot symbols
  read from the dynamic symbol table" (`:113`).

### 2. Exact four dynamic symbols (observation)

Hardcoded list at `dist/flutter/FlutterBuildProvider.js:598-603`:

1. `_kDartVmSnapshotData`
2. `_kDartVmSnapshotInstructions`
3. `_kDartIsolateSnapshotData`
4. `_kDartIsolateSnapshotInstructions`

Matching is exact, case-sensitive Set membership (`dist/flutter/DartElf.js:328,349`); no prefix, wildcard,
or alias handling. The same four names are still hardcoded in the 6.7.0 cache copy
(`…/a1722018f28f9df2/.../FlutterBuildProvider.js:639-643`).

Acceptance semantics (observation from code + probes):
- **Zero** located → refusal: `unsupported_target`, message
  `No recognizable Dart snapshot symbols were found: symbol … is not in the dynamic symbol table; …`
  (`FlutterBuildProvider.js:649-650`). All four failures are listed, not just the first.
- **1–3** located → `ok:true` with `libapp.coverage:"partial"`; limitations carry each missing name's
  reason plus `Only k of 4 snapshot symbols were present` (`FlutterBuildProvider.js:604-660`, `691-703`).
- **complete** requires all four, both `*Data` symbols carrying a valid complete header, exactly two data
  headers, one distinct hash with two sources, no aliasing/overlap
  (`FlutterBuildProvider.js:650-659`; `SYMBOL_PAIR_COUNT = 2` at `:40`). Header "complete" requires
  magic `f5f5dcdc`, `kind === 3` (documented as the Dart 2.14 FullAOT layout), a 32-hex hash at +20, and a
  declared length that fits the symbol (`DartElf.js:386-418`).

### 3. Which ELF table qualifies — static `.symtab` does not (observation: code + 4 probes)

- Only `SHT_DYNSYM` (type 11) is consumed: constant at `DartElf.js:43`; the section-header walk reads every
  section and `continue`s unless `sh_type === SHT_DYNSYM` (`DartElf.js:173-219`, filter at `:180`).
  There is **no** `SHT_SYMTAB` (type 2) branch anywhere in `dist/flutter/*`; the only `SHT_SYMTAB`
  occurrences in the package are unrelated native-layout **schema validators**
  (`dist/domain/native/binaryLayout.js:204,296`), which do not feed this verb.
- Alternate path is still the dynamic table: `dynamicFallback` is enabled only for
  `e_type === ET_DYN && e_shoff === 0 && e_shnum === 0` (`DartElf.js:94-98`); then PT_DYNAMIC tags
  `DT_SYMTAB/DT_STRTAB/DT_STRSZ/DT_SYMENT` plus `DT_HASH` or `DT_GNU_HASH` reconstruct `.dynsym`'s
  offset/count (`DartElf.js:220-326`). A stripped image without a hash table is refused
  (`Stripped ELF has no DT_HASH or DT_GNU_HASH symbol count`, `:314`). This is not a static-symbol path.
- Definition filter: `st_shndx == 0` (UND) is skipped, `0xfff1` (SHN_ABS) accepted, real section indices
  bounded by `e_shnum` unless the PT_DYNAMIC fallback is active (`DartElf.js:342-347`).
- Ambiguity: the same name appearing in multiple dynsym tables with different `(offset,size)` is dropped
  and reported as `conflicting definitions` (`DartElf.js:364-375`).

Probes (synthetic fixtures built in `/tmp/kd23fixture`; argv/env/stdout/exit retained here; target
sha256 given). These verify the reader's code paths only — they are fabricated ET_DYN images, not
original-envelope Flutter artifacts, and **cannot source R23-C1**.

| # | Target (sha256) | Shape | Observed result |
|---|---|---|---|
| A | `fx_dynsym.apk` `b92634fde6b223819b9499d3bf5cdf7da6f910b6f1fe2b129f14604c87ace2c1` | four names GLOBAL in `.dynsym`; both `*Data` symbols carry kind-3 headers, same hash | `ok:true`, exit 0, `libapp.coverage:"complete"`, `sections` = 4, `snapshot_hash_sources` = 2, hash `0123456789abcdef0123456789abcdef` |
| B | `fx_symtab_only.apk` `be03cfa078e846499902da44054fbb381d4c24bfdfb9cbb124e82cd1bbeafea8` | identical bytes except the four names are LOCAL and exist **only in `.symtab`**; `.dynsym` holds 5 unrelated UND entries | `unsupported_target`, exit 1, all four `… is not in the dynamic symbol table`, reason = "No recognizable Dart snapshot symbols were found: …" |
| C | `fx_noshdr.apk` `28f96195ac9cc83f33d7510bb54126ef135d0f182aaae9a7eb5bee72399c1957` | `.dynsym` intact, section headers removed (`e_shoff=0,e_shnum=0`) | `ok:true`, exit 0, `libapp.coverage:"complete"`, 4 sections, 2 sources (PT_DYNAMIC fallback) |
| D | `fx_half.apk` `51e9f16b9b7fdd25b5d915d33deff2fdf0e058ceb4bfb8232146ee5de5909bb3` | only VM data + VM instructions exported | `ok:true`, exit 0, `libapp.coverage:"partial"`, 2 sections, 1 source, limitation `Only 2 of 4 snapshot symbols were present` |

Probe command shape (all four, REA 6.5.0 pinned; `--full-output` for A–C, plain for D):
`npx -y rea-agents@6.5.0 inspect-dart-aot <apk> --format json [--full-output]`.
Fixture provenance: `gcc -shared -fPIC -O0` over a generated C array with header bytes
`f5f5dcdc | u64 len=64 | u64 kind=3 | 32-hex hash`; B linked with `{ local: *; }` version script,
D with `{ global: _kDartVmSnapshotData; _kDartVmSnapshotInstructions; local: *; }`;
C produced with `objcopy --strip-section-headers`; each packaged via `zip -0` as `lib/x86_64/libapp.so`.

**Answer to the assignment:** the four dynamic symbols are exactly the `_kDartVmSnapshotData` /
`_kDartVmSnapshotInstructions` / `_kDartIsolateSnapshotData` / `_kDartIsolateSnapshotInstructions` set.
A static `.symtab` alternative does **not** qualify under any image shape — only `.dynsym`, whether found
through section headers or reconstructed through PT_DYNAMIC. A payload whose four names live only in a
static symbol table is refused with the same "not in the dynamic symbol table" text (probe B).

### 4. The pinned Saber APK: refusal cause is naming, not table kind (observation, one inference)

Target `/tmp/kd22probe/saber.apk`, sha256 `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`
(matches the R22 S055 receipt); member `lib/x86_64/libapp.so` sha256
`b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb`, 16,778,120 bytes
(recomputed from the zip member and from the pre-extracted copy — identical).

`readelf -SW` / `readelf -sW` observations:
- ELF64 DYN, **11 section headers**, section table present at `0x10000c8`; segments 7.
- `.dynstr` STRTAB, `.dynsym` DYNSYM (0x60 bytes = 4 entries), `.hash` HASH, `.rodata`, `.eh_frame`, `.text`,
  `.dynamic`, `.bss`, `.shstrtab`. **There is no `.symtab` at all** — so this artifact is not a
  static-symtab case; the static-symbol question is irrelevant to Saber's refusal.
- `.dynsym` entries: `_kDartSnapshotText` (value 0x6d0000, size 0x92a2d0, Ndx 7),
  `_kDartSnapshotData` (value 0x2c0, size 0x6cf670, Ndx 5), `_kDartSnapshotBuildId`
  (value 0x1c8, size 32, Ndx 1). None of the four required names is exported.
- At file offset 0x2c0 (`_kDartSnapshotData`): `f5f5dcdc`, declared length `0x5d0f42`, kind **2**,
  hash `0451907c2eaa8467e848c0067bfe8ed4`. Exactly **one** `f5f5dcdc` magic exists in the image.
- Cross-check with the existing `identify_flutter_build` envelope
  (`.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json`): `snapshot_hash_sources:1`,
  `snapshot_hash` = `0451907c2eaa8467e848c0067bfe8ed4`, `coverage: partial` — i.e. the byte scanner hashed the
  same header that `inspect_dart_aot` would have read for the isolate data symbol, had the name matched.

Fresh 6.5.0 probe (typed refusal, **non-counting**):
`npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output`
→ exit 1, stdout file sha256 `94d4b757015da88493a17de94300534a1ff16a59c94f8fa387349cf5abf39ea0`, stderr empty:
`{"ok":false,"error":{"code":"unsupported_target",…,"message":"… No recognizable Dart snapshot symbols
were found: symbol _kDartVmSnapshotData is not in the dynamic symbol table; symbol _kDartVmSnapshotInstructions
…; symbol _kDartIsolateSnapshotData …; symbol _kDartIsolateSnapshotInstructions …"}}`.

Interpretation:
- **Observation**: the refusal is caused by the exported names being the `_kDartSnapshotData` /
  `_kDartSnapshotText` / `_kDartSnapshotBuildId` trio while the tool requires the legacy four.
- **[INFERENCE]** this trio plus a single magic and `kind 2` is the newer Flutter single-snapshot
  `libapp.so` layout; the tool's four-name list and `kind === 3` rule encode the older two-snapshot
  (Dart 2.14 FullAOT) layout. Not confirmed here against an engine/SDK source.
- Even with a name alias, this artifact would remain `partial`: one data header (pair count 1 of 2) and
  header `kind 2` ≠ 3 both fail the completeness conjunction.
- **Claim consequence**: Saber is a typed refusal and cannot be counted for `inspect-dart-aot`; the
  successful `identify_flutter_build` on the same APK is a different verb and cannot substitute
  (double-count falsifier). A countable original-envelope `inspect_dart_aot` success needs an APK whose
  `libapp.so` exports all four legacy names in `.dynsym` with kind-3 data headers — a target-discovery
  question, not a parsing one. Whether such an APK is available on the pinned source lane is **[UNKNOWN]**
  to this seat; no live download/device probing was performed.

### 5. Version drift (observation, not a claim)

- Pinned install used: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json`
  `"version": "6.5.0"` (sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`);
  `npx -y rea-agents@6.5.0 --version` → `6.5.0`.
- A second cache copy at `…/a1722018f28f9df2/…` is 6.7.0. Same four names; `DartElf.js` adds
  `SHF_ALLOC` PT_LOAD-consistency validation of dynsym/dynstr (new `sectionMappingFailure`). On Saber it
  still refuses, but the CLI returns exit **0** with the error envelope (6.5.0 returned exit 1), and on
  fixture A it still succeeds. Do not infer provider behavior over time from this; the wave explicitly
  disclaims that.

### 6. Acceptance summary

- **Exact names**: the four listed in §2, matched literally in `.dynsym`.
- **Exact table**: `SHT_DYNSYM` or its PT_DYNAMIC reconstruction only; `.symtab` never qualifies.
- **Partial vs refusal**: zero → refusal; 1–3 → successful partial; complete needs 4 symbols, 2 complete
  kind-3 data headers, one hash from 2 non-aliased sources.
- **Saber**: refuses for name/layout reasons even though `.dynsym` is intact and un-stripped.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaDart.md` — this report
  (only file written inside round-23; sha256 printed in the final message).
- Ephemeral `/tmp` scratch (disposable, not a seat deliverable; contents/hashes inlined above):
  `/tmp/kd23fixture/fx_dynsym.apk` `b92634fd…`, `fx_symtab_only.apk` `be03cfa0…`, `fx_noshdr.apk`
  `28f96195…`, `fx_half.apk` `51e9f16b…`, corresponding `libapp_*.so` (`0bda55a4…`, `a56c9064…`,
  `7bfe0481…`, `7225510d…`), `/tmp/kd23_schema_probe.out.json` `94d4b757…` (Saber refusal, exit 1).
- Read-only inputs hashed: installed impl `DartElf.js` `2f66242747848e36ca91e9ea56e94e632911f0fa351f80439eda4f0bf4d52af8`,
  `FlutterBuildProvider.js` `2c00116a02ee3e9a483886a14ec84d7f224899c8807c84c999bcca49b043d191`,
  `flutterBuildAnalysis.js` `c8cac80550d266e1741142bfd9e88a87381fc0fd25485b4ea6ed0db25538ddf2`,
  `flutterCommands.js` `8354ba86bc42c73a785c3ed9b99f0f8a702d1b0be5fe6d798b76d6ee35da0d18`,
  `flutterToolContracts.js` `8150d522e7dc4fec43cfe0d93aa4ef06ca7d4bd61fd45f3c72e6cb89de130d3e`,
  `DartAotInspection.js` `e8c2904eeaee5ad917d61a7c13a72ac53244617879509b41b8d824690a7cd1c9`.

## Installs

None. No pacman/uv/npm global installs, no config edits. `npx` used the already-present cached
`rea-agents@6.5.0` (pinned) and, for one cross-check only, cached `rea-agents@6.7.0`; no package manager
transaction was run and nothing was persisted outside the npm cache.

## Open risks

- Probes A–D are synthetic ET_DYN images. They establish the reader's accept/refuse contract, not Flutter
  SDK behavior, and cannot source R23-C1 or count as any verb's held evidence.
- The modern-naming inference in §4 is drawn from this one artifact; no Flutter engine/SDK source was read.
  `kind 2` is reported by the tool as a raw field; its SDK meaning is uninterpreted by the tool.
- Not probed: multiple `.dynsym` sections carrying conflicting definitions, SHN_ABS symbols, deflate-stored
  `libapp.so` inside the zip (fixtures were stored with `zip -0`; compressed entry handling is code-read
  only, `openEntrySafely` + streaming in `FlutterBuildProvider.js:564-590`).
- The 6.7.0 exit-code difference (0 on typed refusal vs 6.5.0's 1) is a single observation; it is not a
  contract claim and the wave pins 6.5.0.
- `/tmp` scratch is not durable; hashes and decisive outputs are inlined here so the finding survives
  cleanup.

## Appendix — probe receipts (observed)

Environment: no env overrides; shell `/tmp`; REA 6.5.0 via npx. stderr empty for all four probes.

### A. `fx_dynsym.apk` — argv: `npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd23fixture/fx_dynsym.apk --format json --full-output`; exit 0

```json
{"ok":true,"data":{"evidence_id":"ev_4000bb2cdccc9f63cea9d989888d9ee9ab32e45f4e47649f5c425a449cf65ce9","subject":{"name":"fx_dynsym.apk","digest":{"sha256":"b92634fde6b223819b9499d3bf5cdf7da6f910b6f1fe2b129f14604c87ace2c1"},"local_path":"/tmp/kd23fixture/fx_dynsym.apk","format":"apk","architecture":null},"provider":{"id":"flutter","name":"Flutter build identification","version":null},"analysis_profile":null,"predicate_type":"rea.analysis","operation":"inspect_dart_aot","parameters":{"path":"/tmp/kd23fixture/fx_dynsym.apk"},"raw_result":null,"normalized_result":{"target":{"path":"/tmp/kd23fixture/fx_dynsym.apk","bytes":23654,"sha256":"b92634fde6b223819b9499d3bf5cdf7da6f910b6f1fe2b129f14604c87ace2c1"},"abi":"x86_64","libapp":{"coverage":"complete","bytes":23464,"sha256":"0bda55a456ad55831e3cfa229650756533fb8027e9f8e97dcfc631dc43f7c096","snapshot_hash":"0123456789abcdef0123456789abcdef","snapshot_hash_candidates":["0123456789abcdef0123456789abcdef"],"snapshot_hash_sources":2,"sections":[{"name":"_kDartIsolateSnapshotData","offset":12544,"size":4096,"magic_valid":true,"kind":3,"header_length":64},{"name":"_kDartIsolateSnapshotInstructions","offset":16640,"size":256,"magic_valid":false,"kind":null,"header_length":null},{"name":"_kDartVmSnapshotData","offset":8192,"size":4096,"magic_valid":true,"kind":3,"header_length":64},{"name":"_kDartVmSnapshotInstructions","offset":12288,"size":256,"magic_valid":false,"kind":null,"header_length":null}]},"string_pool":{"coverage":"complete","package_uris":[],"package_uri_count_at_least":0,"dart_uris":[],"dart_uri_count_at_least":0,"class_like_tokens":[],"class_like_token_count_at_least":0,"printable_run_count":1},"coverage":"complete"},"confidence":"observed","authority":"shipped-artifact","environment":null,"limitations":["The APK is read through an owned read-only snapshot; concurrent changes to the original cannot mix into this observation","Snapshot sections are located through the ELF dynamic symbol table; a payload without exported snapshot symbols is refused rather than guessed","Snapshot hash sources are the headers at the start of the VM and isolate data symbols; complete decoding supports kind 3 (the Dart 2.14 FullAOT layout), a valid hash and a declared length that fits its symbol, including the four magic bytes; other kind values remain observed with partial coverage","String-pool entries are byte-pattern observations from the isolate data section, not deserialized cluster semantics; typed class and function recovery needs an SDK-specific parser","class_like_tokens are identifier-shaped runs and include incidental matches","string-pool counts are lower bounds: collection stops at twice each projection bound, and any value beyond that is counted only through the capped flag"],"relationship_coverage":null,"locations":[{"kind":"artifact-path","path":"/tmp/kd23fixture/fx_dynsym.apk"}],"evidence_links":[]},"meta":{"command":"inspect-dart-aot","duration":"15ms"}}
```

### B. `fx_symtab_only.apk` — same argv with `fx_symtab_only.apk`; exit 1

```json
{"ok":false,"error":{"code":"unsupported_target","category":"unsupported_target","message":"Unsupported target for inspect_dart_aot at /tmp/kd23fixture/fx_symtab_only.apk: No recognizable Dart snapshot symbols were found: symbol _kDartVmSnapshotData is not in the dynamic symbol table; symbol _kDartVmSnapshotInstructions is not in the dynamic symbol table; symbol _kDartIsolateSnapshotData is not in the dynamic symbol table; symbol _kDartIsolateSnapshotInstructions is not in the dynamic symbol table","retryable":false,"remediation":{"action":"Select a target supported by this operation or choose an operation supporting the reported target format."},"details":{"operation":"inspect_dart_aot","path":"/tmp/kd23fixture/fx_symtab_only.apk","reason":"No recognizable Dart snapshot symbols were found: symbol _kDartVmSnapshotData is not in the dynamic symbol table; symbol _kDartVmSnapshotInstructions is not in the dynamic symbol table; symbol _kDartIsolateSnapshotData is not in the dynamic symbol table; symbol _kDartIsolateSnapshotInstructions is not in the dynamic symbol table"}},"meta":{"command":"inspect-dart-aot","duration":"15ms"}}
```

### C. `fx_noshdr.apk` — same argv with `fx_noshdr.apk --format json --full-output`; exit 0

Decisive `normalized_result`: `abi:"x86_64"`, `libapp.coverage:"complete"`, `bytes:20488`,
`sha256:"7bfe04817777106c30f2c4c17907f661b6ae59fa1ea3858363cef61b0c8dc98f"`,
`snapshot_hash:"0123456789abcdef0123456789abcdef"`, `snapshot_hash_sources:2`, `sections` identical in
substance to A (four names; offsets 12544, 16640, 8192, 12288; both `*Data` `magic_valid:true`,
`kind:3`, `header_length:64`), `string_pool.coverage:"complete"`, top-level `coverage:"complete"`,
`evidence_id:"ev_354e792e76aaaca7eb8afe54bf53a339d65f0707c0a11fe0f3c6d2581d5a84a0"`.

### D. `fx_half.apk` — same argv with `fx_half.apk --format json`; exit 0

Decisive `normalized_result`: `libapp.coverage:"partial"`, `snapshot_hash_sources:1`,
`sections` = [`_kDartVmSnapshotInstructions` (offset 12288, size 256, magic_valid false),
`_kDartVmSnapshotData` (offset 8192, size 4096, magic_valid true, kind 3, header_length 64)],
`string_pool.coverage:"partial"`, top-level `coverage:"partial"`; limitations include the two missing
names' "not in the dynamic symbol table" reasons and `Only 2 of 4 snapshot symbols were present`;
`evidence_id:"ev_89d34f5e3c3e3f196798fba9799d9ef898ec876fb8ded00691fb0ceab6145269"`.

### Saber refusal (typed, non-counting)

argv: `npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output`;
exit 1; stderr empty; stdout sha256 `94d4b757015da88493a17de94300534a1ff16a59c94f8fa387349cf5abf39ea0`; body is the
same `unsupported_target` shape as B with the four names and path `/tmp/kd22probe/saber.apk`.

### Toolchain observation used for the CLI-detail check

`npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --abi x86_64 --detail summary --format json`
→ exit 1, stdout `{"code": "UNKNOWN", "message": "Unknown flag: --detail"}` (formatted JSON, two-space
indent), confirming `detail` is not part of the CLI option schema.
