# R23 DartSymbolSource — Dart SDK snapshot symbol declarations at pinned revisions

Author-side scout report. Read-only seat: no production edit other than this report; no APK opened,
no REA probe run, no debugger/Frida, no device or carrier execution. Target content (source) is
treated as data. **No source-recovery claim** is made or implied below.

## Pin (chosen, because round-23 carries no Dart-SDK revision pin)

`corpus/` and `.ufo/waves/round-23/` contain no Dart SDK revision/version pin; the Saber snapshot
hash `0451907c2eaa8467e848c0067bfe8ed4` is not a version and no lookup was attempted.

| Role | Tag | Annotated tag object | Peeled commit | Commit date (observed) |
|---|---|---|---|---|
| Current contract | `3.13.6` | `f00e9529cd7117fd4b556532208a49d8898e3e2e` | `0edc81df4fa2060ca4ca80bf2f91c4b5a2616004` | 2026-10-20T01:00:48-07:00 |
| Last stable with the four VM/isolate names | `3.12.0` | `3b675ba8536e5be310e520b57371c03aea9b8eaa` | `98116461144f4429ab873f8497023a5ec3b08127` | not fetched (tag→commit only) |
| Historical cross-check | `2.19.6` | `f52d73106ec9286233a7af41b1f7615d81949139` | `5b8936496673a285bf8f37472119bc2afb38a295` | 2023-03-28T13:41:04+00:00 |

`git ls-remote --tags https://github.com/dart-lang/sdk.git refs/tags/{3.13.6,3.13.0,3.12.0,2.19.6}{,^{}}`
exit 0 produced the table above (annotated tags are separate objects; `git clone --branch 3.13.6`
warns `refs/tags/3.13.6 f00e9529... is not a commit!`). Raw fetches were repeated at the peeled
commits and matched the tag-name fetches byte-for-byte (`dart_api.h` at `0edc81df…` and at `3.13.6`
both sha256 `d5009bb2…`; at `98116461…` and at `3.12.0` both `da42f9d2…`), so the pin holds.

Selection basis for `3.13.6`: newest bare stable tag found in 600 GitHub tag records plus direct
probes of `3.14.0`, `3.14.1`, `3.14.2`, `3.15.0` (`raw.githubusercontent.com` → HTTP 404 for
`runtime/include/dart_api.h`); `3.14.0-*`/`3.15.0-*` exist only as dev tags. This is an observation
of what the remote served on 2026-10-21, not a release-calendar claim.

## Findings — current pinned revision 3.13.6 (`0edc81df…`)

**Observation — declaration block.** `runtime/include/dart_api.h` (sha256
`d5009bb2dfa76dcdf3ed3c5bd427a74c4c820cea29f393a5909efa377291f713`, at commit and at tag):

- `:4019-4021` comment: Darwin `dlsym` adds `_`; use `...CSymbol` for `dlsym`, `...AsmSymbol` for
  the object names.
- `:4023-4031` `kSnapshot{BuildId,Data,Text,Bss}CSymbol`: Apple values drop the leading underscore
  (`"kDartSnapshotData"`), non-Apple values keep it (`"_kDartSnapshotData"`).
- `:4034-4037` `kSnapshot{BuildId,Data,Text,Bss}AsmSymbol`, all `"_kDart…"`.
- `:4081-4083` `Dart_CreateAppAOTSnapshotAsElf` documents exactly two ELF symbols:
  `_kDartSnapshotData`, `_kDartSnapshotText`.
- The legacy `kVmSnapshot*`/`kIsolateSnapshot*` macros are **absent**: `grep -c
  'kVmSnapshotDataCSymbol'` = 0; `grep -c 'kSnapshotDataCSymbol'` = 2.

**Observation — writer mapping.** `runtime/vm/image_snapshot.cc:702-713` `ImageWriter::SectionSymbol`:
`Text → _kDartSnapshotText`, `Data → _kDartSnapshotData`, `Bss → _kDartSnapshotBss`,
`BuildId → _kDartSnapshotBuildId`. Sections are `.text`, `.rodata`, `.bss`
(`runtime/vm/elf.h:89-91`). `BlobImageWriter::ExitSection` feeds those names into the ELF writer
(`image_snapshot.cc:1959-1967`); the assembly writer marks Text/Data `.globl`
(`image_snapshot.cc:1541-1558`).

**Observation — exported vs internal.** `runtime/vm/elf.cc:1197-1221`: a *portion* symbol name is
emitted `STB_GLOBAL`/`STT_OBJECT` into the dynamic symbol table (comment: "Global dynamic symbols …
always a single structured element"); per-object/static symbols are emitted `STB_LOCAL` only for the
non-dynamic table (comment cites dartbug.com/41783: dynamic symbols are also placed in `.symtab` when
present). `runtime/vm/elf.cc:1231-1253`: `.dynstr`/`.dynsym` are created unconditionally; `.strtab`/
`.symtab` only `if (!IsStripped())`, where stripped means "no DWARF" (`runtime/vm/so_writer.h:57-58`).
`runtime/vm/elf.cc:1174-1181`: the BSS symbol is deliberately added as a **local** `STT_SECTION`
static-table symbol ("these addresses are only used for relocation"). `runtime/vm/elf.cc:1755-1758`:
the build-id note portion carries `_kDartSnapshotBuildId` as a portion symbol (therefore global).

**Observation — the SDK's own loader accepts only the dynamic table.**
`runtime/bin/elf_loader.cc:344-360` requires `.dynstr` and `.dynsym` (checks fail otherwise);
`:363-383` walks `dynamic_symbol_table_` for `_kDartSnapshotData`/`_kDartSnapshotText` and errors if
not found. So in the pinned SDK's own contract, a usable AOT snapshot symbol is an **exported
`.dynsym` global**, not a `.symtab` internal.

**Observation — residual legacy strings are labels, not declarations.**
`runtime/vm/analyze_snapshot_api_impl.cc:285,295,353` still print the strings
`_kDartVmSnapshotInstructions` / `_kDartIsolateSnapshotInstructions` as JSON `"section"` labels.
A whole-tree grep of the pinned sparse checkout (runtime, tools, pkg/vm_snapshot_analysis) for the
four legacy names returns exactly those 3 lines. These are analysis-output labels; they do not
declare or generate ELF symbols.

### Mapping table — pinned 3.13.6

| Semantic role | Object symbol (`...AsmSymbol`, non-Apple `...CSymbol`) | Apple `dlsym` name | ELF section | Binding/type (writer) | `.dynsym` | `.symtab` |
|---|---|---|---|---|---|---|
| snapshot data (read-only image) | `_kDartSnapshotData` | `kDartSnapshotData` | `.rodata` | GLOBAL OBJECT | yes | unstripped only |
| snapshot instructions | `_kDartSnapshotText` | `kDartSnapshotText` | `.text` | GLOBAL OBJECT | yes | unstripped only |
| snapshot BSS | `_kDartSnapshotBss` | `kDartSnapshotBss` | `.bss` | LOCAL SECTION (relocation only) | **no** | unstripped only |
| build id | `_kDartSnapshotBuildId` | `kDartSnapshotBuildId` | `.note.gnu.build-id` portion | GLOBAL OBJECT | yes | unstripped only |

There is **no** VM-vs-isolate split at this revision: one snapshot per isolate group.

## Findings — legacy four-name contract (stable ≤ 3.12.0)

**Observation — 3.12.0 `runtime/include/dart_api.h`** (sha256 `da42f9d2…`, tag and commit
`98116461…`): `:4026-4038` define `kVmSnapshotDataCSymbol`, `kVmSnapshotInstructionsCSymbol`,
`kIsolateSnapshotDataCSymbol`, `kIsolateSnapshotInstructionsCSymbol` (Darwin no-underscore and
non-Darwin underscore forms); `:4043-4047` define the matching AsmSymbols; `:4095-4099` document the
ELF output as defining exactly `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`,
`_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`.

**Observation — 3.12.0 writer.** `runtime/vm/image_snapshot.cc:701-712`
`SectionSymbol(section, bool vm)` returns VM vs isolate names for Text/Data/Bss. 3.12.0
`runtime/vm/elf.cc` (sha256 `3fe477c9…`) `:1219-1236` has the same global-portion / local-static
split; the BSS names are `SymbolData` locals. 3.12.0 `runtime/bin/elf_loader.cc` (sha256
`ead06d1e…`) `:352-361` requires `.dynsym`; `:379-385` looks up **all four** legacy names in the
dynamic symbol table.

**Observation — 2.19.6 origin.** `runtime/include/dart_api.h:3948-3961` CSymbols, `:3965-3971`
AsmSymbols, `:4016-4020` documents the four ELF symbols. `runtime/vm/image_snapshot.cc:631-643`
same VM/isolate switch; assembly `.globl` at `:1375-1381`; BSS at `:1360-1364` is `.bss` with no
`.globl`. `runtime/vm/elf.cc:1336-1348` (global portion → `.dynsym`, local static-only symbols),
`:1368,1386` (dynsym always / symtab when unstripped). `runtime/bin/elf_loader.cc:455-500` reads
`.dynstr`/`.dynsym` and resolves the four names, checking isolate data/instructions are non-null.
`runtime/vm/dart_api_impl.cc:6751-6770` is the `Dart_CreateAppAOTSnapshotAsElf` API path.

**Peer sampling (not re-run by this seat).** `KaidokuR23.CriticSource` independently reports the
legacy defines present at 3.0.0, 3.5.0, 3.8.0, 3.9.0, 3.10.0, 3.11.0 and 3.12.0; this seat's own
fetches covered 3.0.0, 3.2.0, 3.4.0, 3.6.0, 3.8.0, 3.10.0, 3.11.0, 3.12.0 with the same result.

### Mapping table — stable ≤ 3.12.0

| Semantic role | Object/dynamic symbol | ELF section | Binding/type (writer) | `.dynsym` | `.symtab` |
|---|---|---|---|---|---|
| VM snapshot data | `_kDartVmSnapshotData` | `.rodata` | GLOBAL OBJECT | yes | unstripped only |
| VM snapshot instructions | `_kDartVmSnapshotInstructions` | `.text` | GLOBAL OBJECT | yes | unstripped only |
| isolate snapshot data | `_kDartIsolateSnapshotData` | `.rodata` | GLOBAL OBJECT | yes | unstripped only |
| isolate snapshot instructions | `_kDartIsolateSnapshotInstructions` | `.text` | GLOBAL OBJECT | yes | unstripped only |
| VM BSS | `_kDartVmSnapshotBss` | `.bss` | LOCAL SECTION | **no** | unstripped only |
| isolate BSS | `_kDartIsolateSnapshotBss` | `.bss` | LOCAL SECTION | **no** | unstripped only |

REA's four-name probe set is exactly the exported subset; the BSS names were never exported and are
correctly omitted.

## Transition boundary (observed)

- Commit `d36adbacafee01d9852cf8e960cf2d8654d91e7e`, titled `[vm] Remove the VM isolate.`, authored
  2026-05-18 (GitHub commit page, read 2026-10-21): the message states "The snapshot symbols are
  renamed to kDartSnapshotData and kDartSnapshotText… Aliases with the old names are added to ease
  migration."
- At that commit, `runtime/include/dart_api.h:4019-4033` keeps the six legacy CSymbols under a
  `/* TRANSITION */` comment; the assembly writer emits aliases
  `_kDartVmSnapshotInstructions = _kDartSnapshotText`, `_kDartIsolateSnapshotInstructions =
  _kDartSnapshotText`, `_kDartVmSnapshotData = _kDartSnapshotData`,
  `_kDartIsolateSnapshotData = _kDartSnapshotData` (`image_snapshot.cc` at that commit, 1652-1667);
  the ELF writer adds the same four legacy names as global alias symbols next to the merged portion
  symbols (`elf.cc` at that commit, 1224-1240).
- By stable **3.13.0** (`da6595cd6bb5d4c0a185d759a025e879ff06e631`) the aliases and the legacy
  macros are gone: raw `dart_api.h` at 3.13.0 and 3.13.6 both `d5009bb2…` with 0 legacy defines;
  `image_snapshot.cc` at 3.13.0 and 3.13.6 both `12aa43e3…`; `elf.cc` at 3.13.0 and 3.13.6 both
  `d0cd8da7…`, with 0 occurrences of the legacy names. **The writer sources at stable tags ≥ 3.13.0
  define/emit only the merged set.** The alias window is therefore dev-channel (`d36adbac` until an
  unidentified removal commit before 3.13.0); whether any shipped Flutter release used a dev SDK in
  that window is [UNKNOWN] here.

## Consumer linkage (why this matters for R23-C1) — observed

Installed `rea-agents@6.5.0`:

- `.../node_modules/rea-agents/dist/flutter/FlutterBuildProvider.js`
  (sha256 `2c00116a02ee3e9a483886a14ec84d7f224899c8807c84c999bcca49b043d191`), `:599-602`
  hardcodes the probe array `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`,
  `_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`; `:623` special-cases
  `_kDartIsolateSnapshotData` for the snapshot header.
- `.../dist/cli-runtime/cli.js` (sha256
  `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204`), `:18851` declares
  `SHT_DYNSYM`, `PT_DYNAMIC`, `DT_SYMTAB`; `:18926` `readElfSymbols` reads `SHT_DYNSYM` (with a
  `PT_DYNAMIC` fallback) only — never `.symtab`; `:19750` is the inventory call with the four names.
  The R22 refusal text itself says "is not in the dynamic symbol table" (S055 evidence).

**Peer corroboration (not re-run by this seat).** `KaidokuR23.CriticSource` reported via IRC a
readelf (exit 0) of the Saber `libapp.so` (sha256 `b54b19d2…`) whose `.dynsym` contains
`_kDartSnapshotText`, `_kDartSnapshotData`, `_kDartSnapshotBuildId` and none of the legacy four.

**Inference (explicitly not verified here).** `gen_snapshot` at stable ≥ 3.13 emits the merged
names, so a `libapp.so` built from such a toolchain is expected to export them unless post-processed;
the four names REA checks are those declared by SDK ≤ 3.12 (plus the brief dev alias window), while
REA 6.5.0 itself declares no Dart version range. The R22 Saber `unsupported_target` refusal is
consistent with a symbol-set/version gap, not with absence of a snapshot. Writer source identifies
what `gen_snapshot` emits at a tag; it does not establish what any given APK exports. This report
does not establish which Dart/Flutter version built Saber, does not open the APK, and does not claim
source recovery. The four-name set remains a valid reader for older builds.

## Command / exit record (key)

- `git clone --filter=blob:none --no-checkout --depth 1 --branch 3.13.6 https://github.com/dart-lang/sdk.git dartsdk` → exit 0 (tag-object warning as above); `git rev-parse HEAD` → `0edc81df4fa2060ca4ca80bf2f91c4b5a2616004`; `git sparse-checkout set runtime tools` + `git checkout` → exit 0, 72 MB.
- `git clone … --branch 2.19.6 …` → exit 0; `HEAD` = `5b8936496673a285bf8f37472119bc2afb38a295`.
- `grep -rn '<four legacy names>' . --exclude-dir=.git | wc -l` → 3 (all `analyze_snapshot_api_impl.cc`).
- `curl https://raw.githubusercontent.com/dart-lang/sdk/<tag>/runtime/include/dart_api.h` → HTTP 200 for 3.0.0, 3.2.0, 3.4.0, 3.6.0, 3.8.0, 3.10.0, 3.11.0, 3.12.0, 3.13.0, 3.13.6; legacy defines present through 3.12.0 (2 lines) and 0 at 3.13.0/3.13.6; merged defines 2 at 3.13.0/3.13.6.
- `curl https://api.github.com/repos/dart-lang/sdk/commits?path=runtime/include/dart_api.h&sha=3.13.0` → **HTTP 403, API rate limit exceeded** (retained failure; not used for any claim).
- `read https://github.com/dart-lang/sdk/commit/d36adbac` → 200, commit subject/description as quoted.
- No REA CLI invocation was selected or run in this seat; no target execution of any kind.

## Fetched working copies (host temp, not wave evidence)

All under `/tmp/kd23-dartsym/`:

| Path | sha256 |
|---|---|
| `dartsdk/runtime/include/dart_api.h` (3.13.6) | `d5009bb2dfa76dcdf3ed3c5bd427a74c4c820cea29f393a5909efa377291f713` |
| `dartsdk/runtime/vm/elf.cc` (3.13.6) | `d0cd8da7024f64cecd7595bcf274bb56e0f6a7601267b6252447d916392b0f26` |
| `dartsdk/runtime/vm/image_snapshot.cc` (3.13.6) | `12aa43e3c90f7cc5fae2116906f2e28165e7c054e716353d10186625d40e88af` |
| `dartsdk/runtime/vm/analyze_snapshot_api_impl.cc` (3.13.6) | `82f7b0e3be11b8707346b0d0a40d9e91205848ac4c4cb760cbca0e74ed515c13` |
| `dartsdk/runtime/bin/elf_loader.cc` (3.13.6) | `01c93d79b3d1124039ffaa126feb5d7c524257c00741c6abe9cf98db94d4df47` |
| `dartsdk/runtime/vm/so_writer.h` (3.13.6) | `e4cf25b47b4b981729571496b764ef7002bae7b3314a2c6153e98d7b86548cce` |
| `api_3.12.0.h` / `dart_api_9811646.h` | `da42f9d2691a41dfec4a7c53101399d5e65480de0661d4cefdb338f11acbd506` |
| `is_3.12.0.cc` (`image_snapshot.cc` 3.12.0) | `41ef33b3d546a498f25516b2b18353e378651d8968de45a62e7a69c9ae0366ea` |
| `elf_3.12.0.cc` | `3fe477c978320f43884d459589df86762d82ab4f34ba63dc55445d0de59a2378` |
| `elf_loader_3.12.0.cc` | `ead06d1eee6c97876b1ee645f0855b2c6bba8b4d69b8ca26ffbf57a1bcd9dca0` |
| `is_3.13.0.cc` / `elf_3.13.0.cc` / `api_3.13.0.h` | `12aa43e3…` / `d0cd8da7…` / `d5009bb2…` (identical to 3.13.6 counterparts) |
| `dart_api_d36adbac.h` (transition commit) | `f1cdd9922da2389f8b8bdbdf79c6c3d0dd3015cf44b9720ba3a7aead7a2674eb` |
| `image_snapshot_d36adbac.cc` | `a7112a5fc923680bce68e97204df6471444845808e04f16c06929f002616c6b2` |
| `elf_d36adbac.cc` | `3870cba451de34f6331d61ef300bcc17a762e4960056ae64c7e3fe3b9b5c56c1` |
| `tags_lsremote.txt` (tag→commit evidence) | `sha256` not computed (small text; re-runnable command above) |

Report output: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/DartSymbolSource.md`
(its own sha256 is reported in the final message, since a file cannot contain its own digest).

## Installs

None. No pacman/uv/npm/cargo transaction occurred; `git` and `curl` were already present. No global
config or host service was touched.

## Open risks / unknowns

1. **No wave-level Dart pin.** 3.13.6 was chosen as the newest stable tag observable; the Saber
   build's actual SDK version is not derivable from its snapshot hash and was not established here.
2. **APK-side claim is peer-supplied.** The Saber `.dynsym` content comes from CriticSource, not from
   an artifact opened by this seat; no download/readelf was repeated.
3. **External post-link stripping is unexamined.** The SDK writer always emits `.dynsym` and only
   drops `.symtab` when stripped; whether Flutter's build or a downstream `strip`/`objcopy` further
   alters exports is not established by source reading.
4. **Flutter engine pipeline not opened.** Whether Flutter invokes `app-aot-elf` with `strip=1` and
   how it consumes the returned symbols is outside this seat (source-side only).
5. **Alias lifetime in dev only.** Stable 3.13.0+ has no legacy aliases; the exact dev tag that
   removed them was not pinned, so any dev-channel Flutter engine build between 2026-05-18 and 3.13.0
   could export either set.
6. **GitHub API limit.** Commit-list queries returned HTTP 403 (rate limit); the transition commit
   was confirmed from its public commit page and raw files, not from the commits API.
7. **`analyze_snapshot_api_impl.cc` legacy labels** are output-schema strings. Do not cite them as
   generation or export evidence.
8. No source recovery, runtime behavior, authentication, or dynamic-debugger ownership is claimed;
   dynamic ownership remains adjacent and unresolved per the wave contract.
