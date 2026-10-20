# VerbCoverageTool — C2 implementation

## Delivery

**Observation.** Added `.ufo/waves/round-20/tools/verb-coverage.py` in the assigned clone; patch: `.ufo/waves/round-20/w1/patches/VerbCoverageTool.patch`. Diff stat: `1 file changed, 297 insertions(+)`. Base observed from clone: `14f0260ad319ecc26994381b2415d5a999003375`.

**Observation.** The CLI catalog is imported from `rea-agents@6.5.0` through Node; the counter reads tracked Git tree entries and blob content at the supplied revision, counts unique knowledge files per command, and applies the hyphen/underscore token-boundary rule (`tools/verb-coverage.py:23-39,65-105,152-193`). Default target names match C2 in `claims.json:26`; a target is `exercised` only when one naming entry has an `ev_<64 hex>` and a tracked existing C2 evidence path (`tools/verb-coverage.py:27-36,108-116,173-184`; contract `contract.md:71-75`).

## Baseline measurement

**Observation.** Command exit 0 at the assigned baseline; result: 128 mentioned out of 153 commands, 25 zero. `mentioned`, `cli_commands`, and `zero` below are copied from its JSON output. All five targets measured `entries: 0, exercised: false` at this revision.

Command (exit 0):
```text
python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --root /tmp/kr20-VerbCoverageTool --rev 14f0260ad319ecc26994381b2415d5a999003375
```

```json
{
  "cli_commands": [
    "inspect-packet-fields", "inspect-packet-capture", "inspect-signal-decoders", "decode-signal-recording", "compare-wasm-interfaces", "inspect-wasm-artifact", "inspect-sqlite-database", "inspect-evm-interface", "inspect-web-network-capture", "observe-web-execution", "inspect-web-event-listeners", "trace-web-source-location", "trace-web-module-imports", "analyze", "inspect", "decompile", "setup", "doctor", "uninstall", "update", "xrefs", "trace", "trace-native-ui-action", "inspect-native-dispatch-metadata", "capabilities", "providers", "function", "annotate-native-function", "inspect-native-api", "instructions", "search", "import-reference-source", "inspect-artifact", "extract-artifact", "decode-interface-builder", "inspect-keyed-archive", "trace-dylib-resolution", "inspect-native-data-type", "inspect-native-load-image", "read-bytes", "search-bytes", "address-to-file-offset", "trace-native-values", "inspect-native-instruction", "resolve-native-call-targets", "inspect-asset-catalog", "inspect-managed-artifact", "inspect-recorded-crash", "inspect-binary-layout", "list-cutter-sessions", "cutter-command", "inspect-with-objdump", "list-objdump-architectures", "execute-rizin-command", "debug-with-gdb", "debug-with-rizin", "inspect-go-binary", "inspect-rust-binary", "inspect-pe-resources", "inspect-analysis-view", "list-frida-devices", "list-frida-processes", "instrument-with-frida", "inspect-evidence-bundle", "inspect-firmware-regions", "extract-firmware", "inspect-android-package", "inspect-pcap-client", "inspect-pcap-capture", "identify-flutter-build", "inspect-dart-aot", "inspect-apktool-client", "decode-android-resources", "inspect-adb-client", "list-adb-devices", "inspect-adb-device", "list-adb-packages", "pull-adb-package", "read-adb-logcat", "inspect-adb-package", "pull-adb-file", "push-adb-file", "capture-adb-screen", "list-adb-processes", "list-adb-directory", "list-adb-features", "list-adb-services", "inspect-adb-display", "inspect-adb-window", "read-adb-setting", "collect-adb-bugreport", "resolve-adb-packages", "install-adb-package", "uninstall-adb-package", "start-adb-app", "start-adb-activity", "stop-adb-app", "search-android-classes", "inspect-android-class", "inspect-android-method", "trace-android-references", "inspect-jeb-client", "open-jeb-project", "list-jeb-units", "decompile-jeb-item", "inspect-managed-members", "inspect-managed-native-boundaries", "compare-managed-members", "verify-managed-native-boundaries", "import-managed-reconstruction", "project-managed-application-graph", "observe-native-ui", "observe-native-calls", "capture-native-ui-scenario", "inspect-macho", "inspect-signature", "list-architectures", "inspect-plist", "demangle-swift", "evidence-import", "evidence-export", "compare", "capture-process", "compare-process-captures", "list-browser-targets", "inspect-web-page", "analyze-web-bundle", "export-web-scripts", "recover-javascript-sources", "observe-web-session", "discover-webmcp-tools", "compare-web-captures", "capture-web-screenshot", "compare-web-screenshots", "capture-browser-scenario", "list-electron-targets", "inspect-electron-page", "inspect-electron-fuses", "capture-electron-scenario", "list-javascript-runtime-targets", "observe-javascript-runtime", "analyze-javascript-application", "reconcile-javascript-runtime", "trace-application-feature", "trace-javascript-semantics", "compare-application-versions", "compare-source-to-bundle", "compare-javascript-export-shapes", "build-reconstruction-obligation-ledger", "evaluate-reconstruction-coverage", "project-android-application-graph", "project-apple-application-graph", "project-harmony-application-graph"
  ],
  "mentioned": [
    "inspect-sqlite-database", "inspect-evm-interface", "inspect-web-network-capture", "observe-web-execution", "inspect-web-event-listeners", "trace-web-source-location", "trace-web-module-imports", "analyze", "inspect", "decompile", "setup", "doctor", "uninstall", "update", "xrefs", "trace", "trace-native-ui-action", "inspect-native-dispatch-metadata", "capabilities", "providers", "function", "annotate-native-function", "inspect-native-api", "instructions", "search", "import-reference-source", "inspect-artifact", "extract-artifact", "decode-interface-builder", "inspect-keyed-archive", "trace-dylib-resolution", "inspect-native-data-type", "inspect-native-load-image", "read-bytes", "search-bytes", "address-to-file-offset", "trace-native-values", "inspect-native-instruction", "resolve-native-call-targets", "inspect-asset-catalog", "inspect-managed-artifact", "inspect-recorded-crash", "inspect-binary-layout", "inspect-with-objdump", "inspect-go-binary", "inspect-rust-binary", "inspect-pe-resources", "inspect-analysis-view", "inspect-evidence-bundle", "inspect-firmware-regions", "extract-firmware", "inspect-android-package", "inspect-apktool-client", "decode-android-resources", "inspect-adb-client", "list-adb-devices", "inspect-adb-device", "list-adb-packages", "pull-adb-package", "read-adb-logcat", "pull-adb-file", "push-adb-file", "capture-adb-screen", "list-adb-processes", "list-adb-directory", "list-adb-features", "inspect-adb-display", "read-adb-setting", "collect-adb-bugreport", "resolve-adb-packages", "install-adb-package", "uninstall-adb-package", "start-adb-app", "search-android-classes", "inspect-android-class", "inspect-android-method", "trace-android-references", "inspect-jeb-client", "open-jeb-project", "list-jeb-units", "decompile-jeb-item", "inspect-managed-members", "inspect-managed-native-boundaries", "compare-managed-members", "verify-managed-native-boundaries", "import-managed-reconstruction", "project-managed-application-graph", "observe-native-ui", "observe-native-calls", "capture-native-ui-scenario", "inspect-macho", "inspect-signature", "list-architectures", "inspect-plist", "demangle-swift", "evidence-import", "evidence-export", "compare", "capture-process", "compare-process-captures", "list-browser-targets", "inspect-web-page", "analyze-web-bundle", "export-web-scripts", "recover-javascript-sources", "observe-web-session", "discover-webmcp-tools", "compare-web-captures", "capture-web-screenshot", "compare-web-screenshots", "capture-browser-scenario", "list-electron-targets", "inspect-electron-page", "inspect-electron-fuses", "capture-electron-scenario", "list-javascript-runtime-targets", "observe-javascript-runtime", "analyze-javascript-application", "reconcile-javascript-runtime", "trace-application-feature", "trace-javascript-semantics", "compare-application-versions", "compare-source-to-bundle", "compare-javascript-export-shapes", "build-reconstruction-obligation-ledger", "evaluate-reconstruction-coverage", "project-android-application-graph", "project-apple-application-graph"
  ],
  "zero": [
    "inspect-packet-fields", "inspect-packet-capture", "inspect-signal-decoders", "decode-signal-recording", "compare-wasm-interfaces", "inspect-wasm-artifact", "list-cutter-sessions", "cutter-command", "list-objdump-architectures", "execute-rizin-command", "debug-with-gdb", "debug-with-rizin", "list-frida-devices", "list-frida-processes", "instrument-with-frida", "inspect-pcap-client", "inspect-pcap-capture", "identify-flutter-build", "inspect-dart-aot", "inspect-adb-package", "list-adb-services", "inspect-adb-window", "start-adb-activity", "stop-adb-app", "project-harmony-application-graph"
  ]
}
```

## Selftest and command record

**Observation.** The first required fixture run exposed three fixture/matcher defects; I corrected the matcher boundary and substring-trap fixture, then the final invocation reported exactly `SELFTEST: CLEAN cases=7`, exit 0. Fixture coverage includes hyphen form, underscore form, absent name, `inspect-artifact-x` substring decoy, existing evidence path plus ID, split ID/path entries, and missing path (`tools/verb-coverage.py:202-266`).

Commands and observed exits:
```text
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-VerbCoverageTool && git -C /tmp/kr20-VerbCoverageTool checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-VerbCoverageTool rev-parse HEAD
exit: 0; stdout: 14f0260ad319ecc26994381b2415d5a999003375

mkdir -p /tmp/kr20-VerbCoverageTool/.ufo/waves/round-20/tools
exit: 0

python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --selftest
exit: 1; exact output: SELFTEST: FAILED not_mentioned_is_zero,substring_trap_rejected,evidence_id_and_existing_path_exercise cases=7 fails=3

python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --selftest
exit: 0; exact output: SELFTEST: CLEAN cases=7

python3 -I -B .ufo/waves/round-20/tools/verb-coverage.py --root /tmp/kr20-VerbCoverageTool --rev 14f0260ad319ecc26994381b2415d5a999003375
exit: 0

git -C /tmp/kr20-VerbCoverageTool add -A && git -C /tmp/kr20-VerbCoverageTool diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375
exit: 0; stdout:  .ufo/waves/round-20/tools/verb-coverage.py | 297 +++++++++++++++++++++++++++++
 1 file changed, 297 insertions(+)

git -C /tmp/kr20-VerbCoverageTool diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/VerbCoverageTool.patch
exit: 0
```

## Risks and blockers

**Inference / limit.** This is mention-level coverage, not proof of mastery or source/evidence authenticity, matching `claims.json:29`; `exercised` enforces the specified syntactic ID + same-entry existing-path test, not a semantic relationship between those artifacts. No blocker. No tool installed or updated.
