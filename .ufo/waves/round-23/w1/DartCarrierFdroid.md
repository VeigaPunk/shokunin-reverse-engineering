# F-Droid Flutter carriers likely retaining legacy dynamic AOT symbols

Round 23, seat `KaidokuR23.DartCarrierFdroid`. Scope: static published metadata
only; no APK bytes were downloaded, no device/process access, no REA invocation,
no production-lane edits. All HTTP below is public F-Droid / Flutter / Dart
metadata; only `HEAD` was issued against APK URLs.

## Question

Find an older public F-Droid Flutter APK likely retaining the legacy four Dart
AOT symbols in `libapp.so`'s dynamic symbol table, justified from published
build/source metadata rather than filenames. Return at most three candidates.

## 1. Symbol-era boundary (observed from primary sources)

**Observation.** Dart SDK commit `d36adbacafee01d9852cf8e960cf2d8654d91e7e`,
author date `2026-05-18T18:35:03Z`, subject `[vm] Remove the VM isolate.`
Patch fetched with
`curl -sL https://github.com/dart-lang/sdk/commit/d36adbacafee01d9852cf8e960cf2d8654d91e7e.patch`
(HTTP 200). The patch removes the assembly symbol constants
`_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`,
`_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions` and replaces
them with `_kDartSnapshotData`, `_kDartSnapshotText`, `_kDartSnapshotBss`
(patch lines 200-209). It adds the four old names only as *transition aliases*
in the Mach-O writer (patch lines 344-347), not as the primary ELF symbol set.

**Observation.** Flutter official release metadata
(`https://storage.googleapis.com/flutter_infra_release/releases/releases_linux.json`,
fetched via `curl`, parsed with `python3`): Flutter `3.47.0`
(2026-08-12, stable) is the first stable release carrying Dart `3.13.0`; the
last stable before it is `3.44.9` (2026-08-06, Dart `3.12.2`). Beta `3.45.0-0.1.pre`
already carried Dart 3.13.0 on 2026-05-21, three days after the Dart commit.
Cross-check: Saber's `submodules/flutter` gitlink at tag `v1.36.1` is
`d3b14c876900e553bc736ca19295fc09e3853e8e` (GitHub contents API via
`curl .../contents/submodules/flutter?ref=v1.36.1`, HTTP 200), which equals the
`3.47.2` release hash `d3b14c876900`; Saber is the R22 carrier whose dynamic
symbol table held only `_kDartSnapshotText`, `_kDartSnapshotData`,
`_kDartSnapshotBuildId`.

**Observation.** Engine source at the Flutter 2.2.1 engine hash
`0fdb562ac8068ce3dda6b69aca3f355f4d1d2718`
(`https://raw.githubusercontent.com/flutter/engine/0fdb562ac8068ce3dda6b69aca3f355f4d1d2718/runtime/dart_snapshot.cc`,
HTTP 200) declares:

```
const char* DartSnapshot::kVMDataSymbol = "kDartVmSnapshotData";
const char* DartSnapshot::kVMInstructionsSymbol = "kDartVmSnapshotInstructions";
const char* DartSnapshot::kIsolateDataSymbol = "kDartIsolateSnapshotData";
const char* DartSnapshot::kIsolateInstructionsSymbol =
    "kDartIsolateSnapshotInstructions";
#define DART_SNAPSHOT_STATIC_LINK ((OS_WIN || OS_ANDROID) && FLUTTER_JIT_RUNTIME)
```

and, when not statically linked (Android **release/AOT**), resolves each buffer
through `SearchMapping(..., settings.application_library_path,
DartSnapshot::kVMDataSymbol, ...)` → `fml::SymbolMapping`, i.e. a dynamic symbol
lookup in `libapp.so`. Dart's own loader agrees: `runtime/bin/elf_loader.cc` at
Dart 2.13.0
(`https://raw.githubusercontent.com/dart-lang/sdk/2.13.0/runtime/bin/elf_loader.cc`,
HTTP 200) compares dynamic-symbol-table names against
`kVmSnapshotDataAsmSymbol`, `kVmSnapshotInstructionsAsmSymbol`,
`kIsolateSnapshotDataAsmSymbol`, `kIsolateSnapshotInstructionsAsmSymbol`
(lines 498-508), while `runtime/vm/elf.cc` (HTTP 200) adds dynamic symbols via
`AddDynamicSymbol` (lines 1074-1081).

**Inference (high confidence).** On Android AOT releases *before* the 2026-05-18
rename, `libapp.so` must export the four legacy snapshot symbols in `.dynsym`;
otherwise the release engine cannot locate its snapshots. Flutter ≤ 3.44.9
stable (Dart ≤ 3.12.2) is therefore the legacy-symbol era; Flutter ≥ 3.47.0
(Dart ≥ 3.13.0) is the renamed era. The exact leading-underscore spelling in
the dynamic table (`_kDart…` asm constants vs `kDart…` C names) is not
separately observed here; the 2026 alias constants use `_kDartVmSnapshotData`
etc., matching the spellings REA reports.

## 2. Candidate selection method

**Observed command.** `curl -s https://f-droid.org/repo/index-v2.json | python3 -c ...`
(HTTP 200, `content-length: 66480070`, `last-modified: Mon, 19 Oct 2026 11:13:13 GMT`).
Parsed in memory: 4766 packages. The same kernel scanned the official
fdroiddata metadata archive
(`https://gitlab.com/fdroid/fdroiddata/-/archive/master/fdroiddata-master.tar.gz?path=metadata`,
HTTP 200, streamed, not written to disk): 7129 YAML files, 61,338,299 bytes;
583 mention `flutter`, 516 of which are still present in the current index; 184
of those have a current published version added before 2026-01-01.

Selection required, per candidate: (a) fdroiddata `srclibs: - flutter@<version>`
for the still-published `versionCode`; (b) F-Droid build log whose downloaded
engine hash equals `bin/internal/engine.version` of that exact Flutter tag;
(c) APK still served by `f-droid.org/repo` (HEAD 200) with index-recorded
sha256/size. All three below resolve to Flutter ≤ 3.3.7, years inside the
legacy-symbol era.

## 3. Candidates (three, strongest chain first)

### C1 — `io.librehealth.toolkit.cost_of_care` 1.0.2 (versionCode 3)

- Published source/build metadata: `metadata/io.librehealth.toolkit.cost_of_care.yml`
  (`https://gitlab.com/fdroid/fdroiddata/-/raw/master/metadata/io.librehealth.toolkit.cost_of_care.yml`, HTTP 200):
  entry `versionName: 1.0.2` / `versionCode: 3` / `commit: v1.0.2` /
  `output: build/app/outputs/apk/release/app-release.apk`, `srclibs: - flutter@1.22.5`,
  build `$$flutter$$/bin/flutter build apk` (recipe lines 39-50).
- Build log: `https://f-droid.org/repo/io.librehealth.toolkit.cost_of_care_3.log.gz`
  HTTP 200; line 54 `Downloading Dart SDK from Flutter engine ae90085a8437c0ae94d6b5ad2741739ebc742cb4...`.
  `https://raw.githubusercontent.com/flutter/flutter/1.22.5/bin/internal/engine.version`
  is exactly `ae90085a8437c0ae94d6b5ad2741739ebc742cb4` (HTTP 200). The log dates
  the build 2021-06-05.
- Published APK: `HEAD https://f-droid.org/repo/io.librehealth.toolkit.cost_of_care_3.apk`
  → HTTP/2 200, `content-length: 24531834`,
  `last-modified: Mon, 07 Jun 2021 14:41:00 GMT`.
- F-Droid index entry: sha256
  `0be7f7d506d15d69ba9b1f1cea3eab8a25b36c00608d68abce21a7c30cbe9b7b`,
  size 24531834, versionName 1.0.2, versionCode 3, `added` 1623024000000
  (2021-06-07 UTC), nativecode `[arm64-v8a, armeabi-v7a, x86_64]`.

### C2 — `net.redsolver.noteless` 1.4.6 (versionCode 146)

- Recipe `metadata/net.redsolver.noteless.yml` (HTTP 200): `versionName: 1.4.6` /
  `versionCode: 146` / `commit: v1.4.6` /
  `output: build/app/outputs/flutter-apk/app-release.apk`, `srclibs: - flutter@2.2.1`,
  build `$$flutter$$/bin/flutter build apk`, `ndk: r22` (recipe lines 30-39).
- Build log `.../net.redsolver.noteless_146.log.gz` HTTP 200; line 58
  `Downloading Dart SDK from Flutter engine 0fdb562ac8068ce3dda6b69aca3f355f4d1d2718...`.
  `.../flutter/2.2.1/bin/internal/engine.version` is exactly that hash. Release
  metadata pairs Flutter 2.2.1 (2021-05-27, stable) with Dart 2.13.1.
- APK HEAD 200, `content-length: 21894454`,
  `last-modified: Thu, 10 Jun 2021 15:26:09 GMT`.
- Index: sha256
  `e3c940175801e47e9bf7daad6ab4daf728d5df9fcdfb6a874304c3c0d8e6c7e2`,
  size 21894454, `added` 1623369600000 (2021-06-11), nativecode
  `[arm64-v8a, armeabi-v7a, x86_64]`.

### C3 — `ca.hamaluik.timecop` 1.8.1 (versionCode 45)

- Recipe `metadata/ca.hamaluik.timecop.yml` (HTTP 200): entry `versionName: 1.8.1` /
  `versionCode: 45` / `commit: b42c5d6e59dab381b9510635405a71d797c5af6c` /
  `output: build/app/outputs/flutter-apk/app-release.apk`,
  `srclibs: - flutter@3.3.7`, build
  `$$flutter$$/bin/flutter build apk` (recipe lines 63-76).
- Build log `.../ca.hamaluik.timecop_45.log.gz` HTTP 200; line 59
  `Downloading Linux x64 Dart SDK from Flutter engine 857bd6b74c5eb56151bfafe91e7fa6a82b6fee25...`.
  `.../flutter/3.3.7/bin/internal/engine.version` is exactly that hash. Release
  metadata pairs Flutter 3.3.7 (2022-11-02, stable) with Dart 2.18.4.
- APK HEAD 200, `content-length: 23940825`,
  `last-modified: Thu, 24 Nov 2022 12:44:00 GMT`.
- Index: sha256
  `ac0beb01168754028a1ce9814495b891bf240aa8098d904e2f73347052595cb3`,
  size 23940825, `added` 1669300152000 (2022-11-24), nativecode
  `[arm64-v8a, armeabi-v7a, x86_64]`.

**Also observed, not counted** (full chain exists, kept out to respect the
three-candidate cap): `com.enjoyingfoss.feeel` 2.4.1/vc4241, `flutter@3.3.7`,
engine `857bd6b7…`, sha256 `0e706395a9e3620d9323392b7a7a494c0ac502aa6f5b9d875d40bf3b7857ad81`;
`com.enjoyingfoss.parlera` 3.0.5/vc12, `flutter@3.10.5`, engine `45f6e009…`,
sha256 `3798719857f194d9757e123e4fca58821ff6664fbfcb9e5af972794b7c826c76`.

## 4. Why these are "likely", not verified

- The dynamic symbol tables themselves were **not** inspected: no APK bytes were
  downloaded (lane rule). The claim is toolchain-era inference plus the engine/
  loader source requirement above, not observed `.dynsym` membership.
- F-Droid's published log binds the *toolchain* (exact engine hash) to the
  versionCode build; it does not by itself authenticate that the currently
  served APK bytes are the artifacts of that exact run. The index sha256/size
  are the only byte-level identity retained here.
- `srclibs: flutter@X` resolution to `github.com/flutter/flutter` was not
  inspected in fdroiddata's srclib definitions; the engine-hash equality is
  independent corroboration that the official Flutter toolchain at tag X was
  used.
- Flutter 1.22.5's release JSON entry publishes `dart_sdk_version: null`; no
  Dart version is asserted for C1. The pre-rename argument does not depend on
  it.
- Pre-1.0 Flutter recipes exist in the same corpus (e.g.
  `com.nikhiljha.lobstersapp`, `flutter@v0.8.2`, 2018) but its build log URL
  returned HTTP 404 and its ELF/AOT packaging era is less certain; rejected.
- F-Droid may later remove these versions from the repo (archive only), and
  index metadata is a moving public artifact (snapshot observed 2026-10-21).

## 5. Command/exit record (observed)

| Command (abridged) | Observed result |
|---|---|
| `curl -sI https://f-droid.org/repo/index-v2.json` | HTTP/2 200, length 66480070, LM 2026-10-19 |
| `curl -s https://f-droid.org/repo/index-v2.json \| python3 …` | parsed 4766 packages |
| `curl -s https://gitlab.com/fdroid/fdroiddata/-/archive/master/…?path=metadata \| tarfile stream` | 7129 YAML, 61338299 bytes, 583 flutter recipes |
| `curl -s …/metadata/<pkg>.yml` (×3) | HTTP 200, blocks quoted above |
| `curl -sI https://f-droid.org/repo/<pkg>_<vc>.apk` (×3) | HTTP/2 200 + lengths above |
| `curl -s …/<pkg>_<vc>.log.gz \| gzip -dc \| grep -i 'Downloading…'` | engine hashes above; HTTP 200 |
| `curl -s https://raw.githubusercontent.com/flutter/flutter/<tag>/bin/internal/engine.version` | hashes equal to log lines |
| `curl -sL https://github.com/dart-lang/sdk/commit/d36adbacaf….patch` | HTTP 200, rename hunks quoted |
| `curl -s https://raw.githubusercontent.com/flutter/engine/0fdb562a…/runtime/dart_snapshot.cc` | HTTP 200, symbol constants quoted |
| `curl -s https://raw.githubusercontent.com/dart-lang/sdk/2.13.0/runtime/bin/elf_loader.cc` | HTTP 200, dynsym name checks lines 498-508 |

Curl exit statuses were not separately captured beyond HTTP codes shown; the
GitHub REST API returned `401 Unauthorized`/rate-limit for two attempted
lookups (GitLab blob search `scope=blobs` → `401 Unauthorized`; GitHub contents
API → `API rate limit exceeded`), which is why discovery used the fdroiddata
archive and raw.githubusercontent.com instead. No payload was downloaded,
executed, unpacked, or installed.

## 6. Installs

None. No packages, tools, or configs were installed or modified; all work used
`curl`, `gzip`, and Python from the host.

## 7. Open risks

1. **Unverified dynsym**: the cryptographic identity of the APKs is known from
   the index, but their `.dynsym` was never read in this lane; only the era
   argument supports symbol retention.
2. **Builder-vs-served bytes**: F-Droid logs and served APKs are not
   independently tied byte-for-byte here.
3. **Symbol spelling**: `_kDart…` vs `kDart…` in the dynamic table is unresolved
   from metadata alone; a later static probe should check both spellings and
   all four names.
4. **ABI coverage**: presence is argued for the AOT ELF (`libapp.so`); x86_64/
   arm64 slices are the expected carriers, but per-ABI contents are unobserved.
5. **Index mutability**: `index-v2.json` and per-app logs are live public files;
   the hashes/sizes above are as observed 2026-10-21 and may disappear later.
6. **No claim of success**: these are candidates for fresh W2 static review, not
   demonstrated `inspect-dart-aot` successes; dynamic/debugger ownership remains
   untouched.
