# DartSaberRefusal — R22 Saber `inspect-dart-aot` refusal and ABI state

Seat: `KaidokuR23.DartSaberRefusal` (leaf scout, author-side only, not outside admission).
Lane HEAD: `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
Scope: read the retained R22 Saber `inspect-dart-aot` envelope/run, identify the
dynamic-symbol refusal reason, and state whether an alternate ABI was tried.
**No REA verb was re-run**; no debugger, Frida, process attach, device access or APK
execution occurred. The only new machine work is in-memory static ELF parsing of the
already-hash-verified carrier (no files written).

## Findings

### 1. The retained R22 run (observation)

Artifact: `/tmp/kd22probe/saber.apk`, 42,305,081 B, sha256
`de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720` (matches the
`artifact_sha256` field in the run record and the public F-Droid URL recorded there).

| field | observed value |
|---|---|
| record | `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json` sha256 `d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a` |
| envelope | `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.envelope.json` sha256 `2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145` (same `{ok:false,error}` JSON) |
| argv | `npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output` |
| exit | `1` |
| stderr | `""` (empty) |
| producer | `KaidokuR22R L1 recovery, not inherited W1` (L1-authored recovery probe, not an independent W1 executor run) |
| error | `ok:false`, `code:"unsupported_target"`, `category:"unsupported_target"`, `retryable:false`, `details.operation:"inspect_dart_aot"` |
| message/reason | `No recognizable Dart snapshot symbols were found:` then, for each of `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`: `symbol <name> is not in the dynamic symbol table` |
| meta | `{"command":"inspect-dart-aot","duration":"90ms"}` |

The run record carries no `env` member and no environment overrides; no override is
indicated. The record does not echo the selected ABI (the refusal fires after selection
and its message omits `abi`).

### 2. Why REA 6.5.0 refused (observation, installed source)

Installed dist: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`
(`rea-agents@6.5.0`; `FlutterBuildProvider.js` sha256 `2c00116a…d191`, `DartElf.js` sha256
`2f662427…2af8`).

1. `flutter/FlutterBuildProvider.js:543-551` — candidates are `lib/<abi>/libapp.so`
   libraries only; without `--abi` it sorts by preference
   `["arm64-v8a","x86_64","x86","armeabi-v7a"]` then ABI code points, and picks the first.
   `:553-557` is the separate earlier refusal `No libapp.so was found for ABI <abi>;
   available: …`.
2. `flutter/FlutterBuildProvider.js:595-602` — the recognized names are exactly the four
   legacy `_kDartVmSnapshot*` / `_kDartIsolateSnapshot*` symbols.
3. `flutter/DartElf.js:129-186,380` — `readElfSymbols` reads **only** `SHT_DYNSYM`
   (`.dynsym`) section(s) when section headers exist (`dynamicFallback` is true only at
   `DartElf.js:94` when `e_shoff==0 && e_shnum==0`), and on `dynamicFallback` uses
   `PT_DYNAMIC`/`DT_SYMTAB` — still the dynamic symbol table. `grep -c SHT_SYMTAB` in
   `DartElf.js` is `0`: there is **no static `.symtab` fallback at all**.
   Missing names produce `symbol <name> is not in the dynamic symbol table` (`:380`).
4. `flutter/FlutterBuildProvider.js:650` — `sections.length === 0` (no recognized symbol
   resolved) returns `AnalysisUnsupportedTargetError("inspect_dart_aot", path,
   "No recognizable Dart snapshot symbols were found: …")`, i.e. the observed envelope.

Therefore the refusal means precisely: none of the four legacy names resolved in the
selected `libapp.so`'s dynamic symbol table.

### 3. Why the four names are absent from Saber (observation, with inference)

Reproducible static check, run in memory against the hash-verified APK (no extraction to
disk; `python3 -c '…'` executed `zipfile` + `struct` over the local file, exit `0`,
printed `parse_ok`):

```
apk_sha256  de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720
libapp      lib/x86_64/libapp.so  16778120 B  sha256 b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb
ELF         class 2 (ELF64), e_type 3 (ET_DYN), e_machine 62 (x86-64), 7 phdrs, 11 shdrs
sections    '', .note.gnu.build-id, .dynstr, .dynsym, .hash, .rodata, .eh_frame, .text, .dynamic, .bss, .shstrtab
dynsym      96 B / 24 = 4 entries; dynstr 61 B = "\0_kDartSnapshotText\0_kDartSnapshotData\0_kDartSnapshotBuildId\0"
entry 1     _kDartSnapshotText       shndx 7 (.text)    value 0x6d0000  size 9609936
entry 2     _kDartSnapshotData       shndx 5 (.rodata)  value 0x2c0     size 7140976
entry 3     _kDartSnapshotBuildId    shndx 1 (.note)    value 0x1c8     size 32
symtab      absent (no SHT_SYMTAB section)
bytes_find  _kDartVmSnapshotData -1; _kDartVmSnapshotInstructions -1;
            _kDartIsolateSnapshotData -1; _kDartIsolateSnapshotInstructions -1
snapshot    magic f5f5dcdc at offset 704; header length 6098754; kind 2;
            hash at +20 = 0451907c2eaa8467e848c0067bfe8ed4
```

Cross-check of the same payload via the retained identify record
(`.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.run.json` sha256
`6b2c24d9…068f`): one ABI (`x86_64`), libapp size/sha equal to the above,
`snapshot_hash_sources:1`, candidate `0451907c2eaa8467e848c0067bfe8ed4`, overall
`coverage:"partial"`; libflutter sha `bf332eff…197a`, build id
`132bfb8e399a170c02e5f577474dd0eed81ed2c3`, `dart_version:null`.

**Observation → conclusion:** the carrier is not missing a symbol table and is not
"stripped to no exports"; it exports exactly the **single-snapshot** symbol set
`_kDartSnapshotText` / `_kDartSnapshotData` / `_kDartSnapshotBuildId`. The four names REA
requires do not exist anywhere in the file (not in `.dynsym`, no `.symtab`, no byte
occurrence), so no table-selection change inside 6.5.0 could have resolved them.

**[INFERENCE]** the refusal is a Dart snapshot-ABI generation mismatch, not a corrupt or
unreadable ELF: REA 6.5.0 models the older VM+isolate four-symbol layout (its own
limitation string, `FlutterBuildProvider.js:694`, calls kind 3 "the Dart 2.14 FullAOT
layout"), while Saber's payload matches the symbol contract of a current Dart SDK. Read-only
corroboration from another seat's scratch clone
`/tmp/kd23-dartsym/dartsdk` (HEAD `0edc81df4fa2060ca4ca80bf2f91c4b5a2616004`,
"Version 3.13.6", origin `https://github.com/dart-lang/sdk.git`, `dart_api.h` sha256
`d5009bb2…f713`): `runtime/include/dart_api.h:4028-4036` defines
`kSnapshotBuildIdCSymbol "_kDartSnapshotBuildId"`, `kSnapshotDataCSymbol
"_kDartSnapshotData"`, `kSnapshotTextCSymbol "_kDartSnapshotText"`, and
`grep -rl _kDartVmSnapshotData\|_kDartIsolateSnapshotData` over that tree returns no file.
The exact Dart/Flutter version used to build Saber is **[UNKNOWN]** (`dart_version:null`;
REA performs no external mapping lookup).

Also observed: Saber's data-snapshot header has `kind:2`, not the `kind:3` that 6.5.0
treats as complete/decodable (`DartElf.js:415`). Even with matching symbol names, 6.5.0
would report this payload as partial, not complete.

### 4. Was an alternate ABI tried? (answer: no — and none exists in this carrier)

- **Observed:** `unzip -Z1 /tmp/kd22probe/saber.apk | grep '^lib/'` (exit 0) lists six
  entries, all `lib/x86_64/`: `libapp.so`, `libdatastore_shared_counter.so`,
  `libflutter.so`, `libirondash_engine_context_native.so`, `libpdfium.so`,
  `libsuper_native_extensions_native.so`. `identify-flutter-build`'s `abis` array contains
  exactly one entry, `x86_64`.
- **Observed:** the retained run's argv has **no `--abi`**. With the source preference order
  (`FlutterBuildProvider.js:547`) and a single libapp candidate, the default selection is
  `x86_64`. **[INFERENCE, deterministic]** this is the ABI that produced the refusal; the
  error JSON does not echo it.
- **Observed:** R22's W1 assignments did include ABI-specific seats —
  `ExecDartAotX64-4` (`--abi x86_64`), `ExecDartAotDefault-4` (default plus each other ABI),
  `ExecDartAotRefusal-4` (Godot template, and Saber `--abi mips`). All three are recorded in
  `.ufo/waves/round-22/wave1-terminal.json` as `status:"dead_parent_provider_death"`,
  `report:null` (cause: `parent KaidokuR22 Anthropic429 terminated child session`), and in
  `final-wave-outcomes.json` as reportless. No outputs from them exist.
- **Observed:** `.ufo/waves/round-22/evidence/c1/` contains exactly one `inspect-dart-aot`
  run (the L1 recovery probe above); there is no `dart-aot-saber-x86_64.json`, no
  `dart-aot-saber-<other-abi>.json` and no `--abi mips` record. A bounded search
  (`timeout 60 rg -l --max-filesize 2M "No libapp.so was found for ABI|inspect-dart-aot"
  /tmp`) matched only unpacked REA package sources, no run output.
- **Therefore:** the alternate-ABI route was **never exercised** — not for another ABI in
  this APK (none exists) and not the `--abi mips` negative probe. An explicit other-ABI run
  would have refused earlier at `FlutterBuildProvider.js:553-557` with
  `No libapp.so was found for ABI <abi>; available: x86_64` **[INFERENCE, not observed]**.
  **[INFERENCE]** changing ABI would not help here in any case: the missing names are a
  Dart SDK symbol convention, not a per-CPU artifact, and this carrier holds only x86_64
  libraries.

### 5. Count disposition (observation; relevant to R23-C1)

- `.ufo/waves/round-22/verify/final/after-c1.json` (count-c1.py, rev
  `e9db7e2d…c1bb`): `t1_exercised:["identify-flutter-build"]`,
  `t1_exercised_count:1`, and `targets["inspect-dart-aot"] =
  {"entries":1,"exercised":false,"bound_evidence":[],"unsupported_candidates":[]}`.
  The refusal was seen but **not bound or counted**.
- `.ufo/waves/round-22/tools/count-c1.py:76-77` (envelope level) and `:92` (nested
  nodes): an envelope with `ok is not True` or a recognized refusal returns the
  non-counting binding result before any record binding, so a typed refusal cannot satisfy
  R23-C1's `refusal counted` falsifier.
- Corner for L1: `catalog_zero` at `after-c1` no longer lists `inspect-dart-aot` (18 vs 19
  at baseline) while `t1_exercised_count` stays 1. That field is a mention metric; the
  knowledge entry `corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md`
  (sha256 `417482ef…7dd8`) states the verb is "mention-level catalog coverage here, not
  exercised success … not held or counted". Do not read the `catalog_zero` movement as
  coverage.
- The R22 refusal is historical witness only. Any R23-C1 count of this verb would need a
  new R23-held non-refused record under `round-23/evidence/c1`; this envelope cannot supply
  one, and no repeated probe was made by this seat.

### Observed / inferred / unknown

- **Observed:** the run record bytes, argv/exit/stderr, error JSON, the four names/line
  numbers in installed REA 6.5.0 source, Saber's `.dynsym` contents and absent `.symtab`,
  the single-ABI APK inventory, the dead ABI-seat records, and the R22 counter's
  non-counting disposition.
- **Inferred:** default ABI selection = `x86_64` (single candidate + source order); the
  refusal is a Dart-3-era single-snapshot vs Dart-2.14 four-symbol layout mismatch; the
  exact other-ABI refusal text (not executed).
- **Unknown:** exact Dart/Flutter version that produced `libapp.so`; engine build id's
  upstream meaning; whether an older or differently built Saber/Flutter carrier exists
  (adjacent seats' scope); any environment override (none retained).

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/DartSaberRefusal.md`
  — this report, the only file written by this seat. Its sha256 cannot be embedded in
  itself; the delivered digest is reported to Main (`sha256sum` after write).
- No other files created, no sandbox clone needed (read-only seat), no extraction:
  the 16,778,120-byte `libapp.so` was parsed entirely in memory.
- Inputs read, with sha256: `inspect-dart-aot-saber.run.json` `d1eaa23f…b34a`;
  `inspect-dart-aot-saber.envelope.json` `2b13cb8f…c145`;
  `identify-flutter-build-saber.run.json` `6b2c24d9…068f`;
  `identify-flutter-build-saber.envelope.json` `143af76e…904b`;
  carrier `/tmp/kd22probe/saber.apk` `de4813f9…b720`;
  REA `FlutterBuildProvider.js` `2c00116a…d191`, `DartElf.js` `2f662427…2af8`;
  Dart SDK `dart_api.h` `d5009bb2…f713`.

## Installs

None. No package manager, uv, npx install, or config change. `rea-agents@6.5.0` was already
present in the npx cache and was **not** invoked; the Dart SDK tree was read from another
seat's existing scratch clone (read-only).

## Open risks

1. **ABI is inferred, not echoed.** The refusal JSON omits `abi`; the single-candidate
   argument is deterministic against 6.5.0 source, but no retained field states `x86_64`.
2. **Carrier location is ephemeral.** `/tmp/kd22probe/saber.apk` could disappear; the
   static parse is reproducible only by re-fetching the public URL and checking
   `de4813f9…b720` (as `saber-download.json` documents).
3. **SDK corroboration provenance.** `/tmp/kd23-dartsym/dartsdk` belongs to another seat's
   scratch; it is read-only, at HEAD `0edc81df…`, remote `dart-lang/sdk`, but its fetch
   history was not independently verified. The Saber-side observation (three modern names,
   no legacy names) stands without it.
4. **Version drift.** `rea-agents` 6.7.0 also exists in the npx cache and was not used or
   compared; if R23 pins a different version its symbol set may differ. Nothing here claims
   6.7.0 behavior.
5. **No re-probe, by design.** This report cannot certify that the refusal would reproduce
   today; it certifies only what the retained run and the installed 6.5.0 source say.
6. **Failed/low-yield checks retained:** a Python query of
   `.ufo/waves/round-22/final-wave-outcomes.json` assumed per-seat objects and raised
   `AttributeError` on string entries; it was unnecessary because `wave1-terminal.json`
   already carries the three dead Dart seats verbatim. The `/tmp` search was bounded
   (`--max-filesize 2M`, 60 s timeout), so absence of other ABI artifacts outside that
   bound is not proven — but every retained R22 evidence file was enumerated directly.
7. **No coverage advance.** This seat adds a causal explanation and an ABI answer only;
   `inspect-dart-aot` remains k-incomplete for R23-C1 and this refusal must not be counted.
