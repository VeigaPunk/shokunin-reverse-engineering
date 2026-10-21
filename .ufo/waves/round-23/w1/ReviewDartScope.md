# ReviewDartScope — static Dart AOT boundary

Scope axes: **coverage** (whether a refusal is counted), **depth** (static metadata vs decompilation/execution), and **calibration** (what symbol declarations and one APK actually establish). Author-side review only.

## Findings

### Low — keep the Saber generation explanation explicitly inferential

No defect found in the inherited R22 refusal/count boundary. Keep the current `inspect-dart-aot` refusal and do not present the suspected Dart-generation mismatch as a verified property of Saber.

- **Observed, retained R22 run:** `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json:2-18` records `npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output`, exit **1**, empty stderr, target SHA-256 `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`, and the `unsupported_target` envelope. The error lists all four required names as absent from the **dynamic** symbol table. This is a refusal, not an `inspect_dart_aot` success.
- **Separate observed static result:** `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json` has the same target digest, `flutter_detected:true`, one `x86_64` ABI, a valid `libapp.so` ELF, one snapshot-hash source/candidate, and `coverage:"partial"` (normalized-result query). Thus the refusal does **not** establish that the APK lacks Dart/AOT content; it establishes that this REA invocation did not resolve the names its Dart reader requires. The inherited knowledge entry correctly keeps the two verbs separate (`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:11-23`).
- **Implementation boundary, observed in pinned REA 6.5.0:** `dist/flutter/FlutterBuildProvider.js:543-625,649-680` selects a packaged `libapp.so`, reads its bytes and checks only `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`, and `_kDartIsolateSnapshotInstructions`; zero matches returns the refusal. `dist/flutter/DartElf.js:173-219,220-326` reads `SHT_DYNSYM`, or reconstructs the dynamic table from `PT_DYNAMIC` when section headers are absent; it does not use static `.symtab`. The contract at `dist/contracts/flutter/flutterToolContracts.js:25` explicitly describes offsets, headers, hash, and bounded string-pool observations, says those strings are not deserialized cluster semantics and typed class/function recovery needs an SDK-specific parser, and ends **“No engine, no execution.”** `dist/application/flutter/DartAotInspection.js:7-25` delegates to that provider and optionally summarizes retained analysis; it is not a Dart decompiler or runtime. The provider does write/read a temporary `libapp.so` file (`FlutterBuildProvider.js:560-597`), so “static” should not be restated as “no filesystem effects.”
- **Calibration caution:** `DartSaberRefusal.md:96-112` labels a Dart-generation/layout mismatch as `[INFERENCE]` and separately says the exact Saber Dart/Flutter version is unknown. The observed facts sufficient to explain the pinned 6.5.0 refusal are the missing required names and the successful, partial identifier result. Do not promote the inferred generation/version explanation—or any SDK source declaration of a symbol—to evidence that Saber was built with a particular Dart SDK, that declarations are exported by this APK, or that source was recovered. Whether any other carrier would satisfy the reader remains unknown here.

### Diff scope

The scoped `jj diff --summary` over `root:corpus/SOURCES.md`, `root:corpus/knowledge`, and `root:corpus/lessons` returned only a modification to `corpus/SOURCES.md`; the detailed diff adds S058–S060 for offline signal work. No Dart/Flutter source row or knowledge change was present in that scoped diff at review time. The frozen claim still says `inspect-dart-aot` is static-only and APKs must never be executed (`.ufo/waves/round-23/claims.json:27-30`).

## Residual risk and verification gaps

- This review does not establish an `inspect-dart-aot` success; it intentionally does not repeat the R22 probe, run a debugger, access a device, or execute an APK. A symbol declaration is not proof of a target ELF’s dynamic exports.
- No LSP device/status route was available in the supplied tool inventory (and REA MCP use is prohibited for this wave); no LSP references/definition/diagnostics were run. Direct source reads and the original run records above are the evidence cited, not grep output presented as semantic proof.
- A scoped `jj diff` attempt using unrooted paths failed with “Invalid file pattern”; it was corrected to rooted paths before recording the diff result. No conclusion was drawn from the failed attempt.
- No packages/tools installed or updated. The current 6.5.0 result does not establish behavior of other REA versions or other Flutter/Dart builds.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewDartScope.md` — this report; SHA-256 is supplied in the final handoff (not embedded in itself).

## Installs

None.
