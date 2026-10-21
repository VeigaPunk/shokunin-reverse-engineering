source: S054 https://developer.android.com/ndk/guides/abis (Native code in app packages), S055 `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json` and `inspect-dart-aot-saber.envelope.json`
verified-at: 2026-10-21, round22 L1 recovery; rea-agents@6.5.0
recheck: download https://f-droid.org/repo/com.adilhanney.saber_1360103.apk to a new directory, require SHA-256 de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720, then run the two exact REA commands in the retained run records; compare content digest and fields, not path-sensitive Evidence ids

# Flutter identification can succeed partially while Dart AOT inspection refuses

## Trigger → action → outcome

**Observation:** W2 SchemaInspectDartAot located the already-selected Saber carrier at `/tmp/kd22probe/saber.apk`. L1 independently required its full SHA-256 before either new probe: `sha256sum /tmp/kd22probe/saber.apk` returned `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`. The exact public version URL above and digest reproduce the carrier after temporary files disappear; no older adjacent `fl.json` result was reused or credited. APK size is 42305081 bytes, from the normalized target field and the same reproducing inspection.

**Observation:** `npx -y rea-agents@6.5.0 identify-flutter-build /tmp/kd22probe/saber.apk --format json --full-output` exited0 with `ok:true`, operation `identify_flutter_build`, Evidence `ev_6a84742a9749692a3c6b59678c83d50b4741761f996c723995fa799b1bbca0b6`. It reports `flutter_detected:true` and one ABI record (`abis` contains x86_64), but **coverage is partial**, not complete. Record: `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json`; argv, exit, stderr and explicit L1 attribution: adjacent `identify-flutter-build-saber.run.json`.

The libapp record reports size16778120, SHA-256 `b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb`, valid ELF header, one snapshot-hash source and candidate `0451907c2eaa8467e848c0067bfe8ed4`. The engine record reports size13051424, SHA-256 `bf332effcc407a658cb477b94417f83ce8df11b1676a06ee42ff754817b4197a`, build id `132bfb8e399a170c02e5f577474dd0eed81ed2c3`, and `dart_version:null`. These are provider-reported static fields, not independently authenticated compiler/runtime identity. Counting/recheck command is the exact identify invocation above; the sizes are its normalized_result.abis fields.

**Observation:** `npx -y rea-agents@6.5.0 inspect-dart-aot /tmp/kd22probe/saber.apk --format json --full-output` exited1 with `ok:false`, `unsupported_target`. The refusal says none of four recognizable snapshot symbols was found in the dynamic symbol table: `_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`. Record and actual argv/stderr/exit are `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.envelope.json` and adjacent `inspect-dart-aot-saber.run.json`. This operation is **not held or counted**, even though the preceding identifier succeeded.

## Inference and limits

**Inference:** snapshot-magic identification and symbol-based AOT inspection have different acceptance conditions. A Flutter-positive result cannot predict a successful symbol walk. W2's pre-run expectation of a partial Dart result was disproved by this retained actual refusal; it is not silently promoted into a success.

**Unknown/not examined:** no Dart version lookup, source reconstruction, snapshot completeness, original program behavior, device installation, debugging or execution. The snapshot hash is not a mapped Dart SDK version; REA explicitly performs no external mapping lookup. The lack of a labeled Dart version string does not establish absence of Dart. S054 supports the packaging convention only, not these provider fields. Full provider limitations remain in the retained successful Evidence record.

C1 can count `identify-flutter-build` from the original successful CLI envelope only; derived bare records cannot erase a producer refusal. `inspect-dart-aot` is mention-level catalog coverage here, not exercised success. The same verb already counted on the non-Flutter control, so this positive does not manufacture a second exercised verb or a six-of-six pass.

Public bootstrap actually re-exercised by L1:
`.ufo/waves/round-22/evidence/sources/saber-download.json` records curl exit0,
HTTP200, 42305081 bytes and the exact declared SHA-256. The download was
removed after hashing, never executed. This provides a versioned, exercised
reproducer instead of relying on continued existence of the temporary carrier.
