# ScoutCatalogBytes — pinned CLI naming catalog

## Finding

The retained round-20 catalog records `rea-agents` **6.5.0**, revision `37e10c545a05cf8ede9a2da0e45d44eb13c7835f`, and **153 names / 153 unique** (`.ufo/waves/round-20/verify/round20/verb-coverage.json`; JSON fields `package_version`, `rev`, `cli_commands`). I read the retained JSON as data and confirmed its `cli_commands` array has length 153 and 153 unique values. The full ordered list below is copied from that retained array; the independent retained report also reproduces it in `CLI_COMMAND_NAMES` order.

Naming forms below distinguish:

- **CLI catalog**: the retained kebab-case command string.
- **Coverage token**: the exact matching alternative produced by the round-20 coverage counter; replace each `-` with `_`. For names with no hyphen, the forms are identical. These underscore forms are **counter matching forms**, not a claim that the CLI accepts underscore aliases.

The local source specifies this transformation at `.ufo/waves/round-20/tools/verb-coverage.py:99-105`; exact located quote from line 100 (10 words): `forms = sorted({name, name.replace("-", "_")}, key=len, reverse=True)`. The interface description at `.ufo/waves/round-20/contract.md:71-75` says: “per command the knowledge entries at REV naming it (hyphen or underscore form, token boundary)” (13 words).

## Catalog in retained order

| # | CLI catalog name | Coverage token form |
|---:|---|---|
| 1 | `inspect-packet-fields` | `inspect_packet_fields` |
| 2 | `inspect-packet-capture` | `inspect_packet_capture` |
| 3 | `inspect-signal-decoders` | `inspect_signal_decoders` |
| 4 | `decode-signal-recording` | `decode_signal_recording` |
| 5 | `compare-wasm-interfaces` | `compare_wasm_interfaces` |
| 6 | `inspect-wasm-artifact` | `inspect_wasm_artifact` |
| 7 | `inspect-sqlite-database` | `inspect_sqlite_database` |
| 8 | `inspect-evm-interface` | `inspect_evm_interface` |
| 9 | `inspect-web-network-capture` | `inspect_web_network_capture` |
| 10 | `observe-web-execution` | `observe_web_execution` |
| 11 | `inspect-web-event-listeners` | `inspect_web_event_listeners` |
| 12 | `trace-web-source-location` | `trace_web_source_location` |
| 13 | `trace-web-module-imports` | `trace_web_module_imports` |
| 14 | `analyze` | `analyze` |
| 15 | `inspect` | `inspect` |
| 16 | `decompile` | `decompile` |
| 17 | `setup` | `setup` |
| 18 | `doctor` | `doctor` |
| 19 | `uninstall` | `uninstall` |
| 20 | `update` | `update` |
| 21 | `xrefs` | `xrefs` |
| 22 | `trace` | `trace` |
| 23 | `trace-native-ui-action` | `trace_native_ui_action` |
| 24 | `inspect-native-dispatch-metadata` | `inspect_native_dispatch_metadata` |
| 25 | `capabilities` | `capabilities` |
| 26 | `providers` | `providers` |
| 27 | `function` | `function` |
| 28 | `annotate-native-function` | `annotate_native_function` |
| 29 | `inspect-native-api` | `inspect_native_api` |
| 30 | `instructions` | `instructions` |
| 31 | `search` | `search` |
| 32 | `import-reference-source` | `import_reference_source` |
| 33 | `inspect-artifact` | `inspect_artifact` |
| 34 | `extract-artifact` | `extract_artifact` |
| 35 | `decode-interface-builder` | `decode_interface_builder` |
| 36 | `inspect-keyed-archive` | `inspect_keyed_archive` |
| 37 | `trace-dylib-resolution` | `trace_dylib_resolution` |
| 38 | `inspect-native-data-type` | `inspect_native_data_type` |
| 39 | `inspect-native-load-image` | `inspect_native_load_image` |
| 40 | `read-bytes` | `read_bytes` |
| 41 | `search-bytes` | `search_bytes` |
| 42 | `address-to-file-offset` | `address_to_file_offset` |
| 43 | `trace-native-values` | `trace_native_values` |
| 44 | `inspect-native-instruction` | `inspect_native_instruction` |
| 45 | `resolve-native-call-targets` | `resolve_native_call_targets` |
| 46 | `inspect-asset-catalog` | `inspect_asset_catalog` |
| 47 | `inspect-managed-artifact` | `inspect_managed_artifact` |
| 48 | `inspect-recorded-crash` | `inspect_recorded_crash` |
| 49 | `inspect-binary-layout` | `inspect_binary_layout` |
| 50 | `list-cutter-sessions` | `list_cutter_sessions` |
| 51 | `cutter-command` | `cutter_command` |
| 52 | `inspect-with-objdump` | `inspect_with_objdump` |
| 53 | `list-objdump-architectures` | `list_objdump_architectures` |
| 54 | `execute-rizin-command` | `execute_rizin_command` |
| 55 | `debug-with-gdb` | `debug_with_gdb` |
| 56 | `debug-with-rizin` | `debug_with_rizin` |
| 57 | `inspect-go-binary` | `inspect_go_binary` |
| 58 | `inspect-rust-binary` | `inspect_rust_binary` |
| 59 | `inspect-pe-resources` | `inspect_pe_resources` |
| 60 | `inspect-analysis-view` | `inspect_analysis_view` |
| 61 | `list-frida-devices` | `list_frida_devices` |
| 62 | `list-frida-processes` | `list_frida_processes` |
| 63 | `instrument-with-frida` | `instrument_with_frida` |
| 64 | `inspect-evidence-bundle` | `inspect_evidence_bundle` |
| 65 | `inspect-firmware-regions` | `inspect_firmware_regions` |
| 66 | `extract-firmware` | `extract_firmware` |
| 67 | `inspect-android-package` | `inspect_android_package` |
| 68 | `inspect-pcap-client` | `inspect_pcap_client` |
| 69 | `inspect-pcap-capture` | `inspect_pcap_capture` |
| 70 | `identify-flutter-build` | `identify_flutter_build` |
| 71 | `inspect-dart-aot` | `inspect_dart_aot` |
| 72 | `inspect-apktool-client` | `inspect_apktool_client` |
| 73 | `decode-android-resources` | `decode_android_resources` |
| 74 | `inspect-adb-client` | `inspect_adb_client` |
| 75 | `list-adb-devices` | `list_adb_devices` |
| 76 | `inspect-adb-device` | `inspect_adb_device` |
| 77 | `list-adb-packages` | `list_adb_packages` |
| 78 | `pull-adb-package` | `pull_adb_package` |
| 79 | `read-adb-logcat` | `read_adb_logcat` |
| 80 | `inspect-adb-package` | `inspect_adb_package` |
| 81 | `pull-adb-file` | `pull_adb_file` |
| 82 | `push-adb-file` | `push_adb_file` |
| 83 | `capture-adb-screen` | `capture_adb_screen` |
| 84 | `list-adb-processes` | `list_adb_processes` |
| 85 | `list-adb-directory` | `list_adb_directory` |
| 86 | `list-adb-features` | `list_adb_features` |
| 87 | `list-adb-services` | `list_adb_services` |
| 88 | `inspect-adb-display` | `inspect_adb_display` |
| 89 | `inspect-adb-window` | `inspect_adb_window` |
| 90 | `read-adb-setting` | `read_adb_setting` |
| 91 | `collect-adb-bugreport` | `collect_adb_bugreport` |
| 92 | `resolve-adb-packages` | `resolve_adb_packages` |
| 93 | `install-adb-package` | `install_adb_package` |
| 94 | `uninstall-adb-package` | `uninstall_adb_package` |
| 95 | `start-adb-app` | `start_adb_app` |
| 96 | `start-adb-activity` | `start_adb_activity` |
| 97 | `stop-adb-app` | `stop_adb_app` |
| 98 | `search-android-classes` | `search_android_classes` |
| 99 | `inspect-android-class` | `inspect_android_class` |
| 100 | `inspect-android-method` | `inspect_android_method` |
| 101 | `trace-android-references` | `trace_android_references` |
| 102 | `inspect-jeb-client` | `inspect_jeb_client` |
| 103 | `open-jeb-project` | `open_jeb_project` |
| 104 | `list-jeb-units` | `list_jeb_units` |
| 105 | `decompile-jeb-item` | `decompile_jeb_item` |
| 106 | `inspect-managed-members` | `inspect_managed_members` |
| 107 | `inspect-managed-native-boundaries` | `inspect_managed_native_boundaries` |
| 108 | `compare-managed-members` | `compare_managed_members` |
| 109 | `verify-managed-native-boundaries` | `verify_managed_native_boundaries` |
| 110 | `import-managed-reconstruction` | `import_managed_reconstruction` |
| 111 | `project-managed-application-graph` | `project_managed_application_graph` |
| 112 | `observe-native-ui` | `observe_native_ui` |
| 113 | `observe-native-calls` | `observe_native_calls` |
| 114 | `capture-native-ui-scenario` | `capture_native_ui_scenario` |
| 115 | `inspect-macho` | `inspect_macho` |
| 116 | `inspect-signature` | `inspect_signature` |
| 117 | `list-architectures` | `list_architectures` |
| 118 | `inspect-plist` | `inspect_plist` |
| 119 | `demangle-swift` | `demangle_swift` |
| 120 | `evidence-import` | `evidence_import` |
| 121 | `evidence-export` | `evidence_export` |
| 122 | `compare` | `compare` |
| 123 | `capture-process` | `capture_process` |
| 124 | `compare-process-captures` | `compare_process_captures` |
| 125 | `list-browser-targets` | `list_browser_targets` |
| 126 | `inspect-web-page` | `inspect_web_page` |
| 127 | `analyze-web-bundle` | `analyze_web_bundle` |
| 128 | `export-web-scripts` | `export_web_scripts` |
| 129 | `recover-javascript-sources` | `recover_javascript_sources` |
| 130 | `observe-web-session` | `observe_web_session` |
| 131 | `discover-webmcp-tools` | `discover_webmcp_tools` |
| 132 | `compare-web-captures` | `compare_web_captures` |
| 133 | `capture-web-screenshot` | `capture_web_screenshot` |
| 134 | `compare-web-screenshots` | `compare_web_screenshots` |
| 135 | `capture-browser-scenario` | `capture_browser_scenario` |
| 136 | `list-electron-targets` | `list_electron_targets` |
| 137 | `inspect-electron-page` | `inspect_electron_page` |
| 138 | `inspect-electron-fuses` | `inspect_electron_fuses` |
| 139 | `capture-electron-scenario` | `capture_electron_scenario` |
| 140 | `list-javascript-runtime-targets` | `list_javascript_runtime_targets` |
| 141 | `observe-javascript-runtime` | `observe_javascript_runtime` |
| 142 | `analyze-javascript-application` | `analyze_javascript_application` |
| 143 | `reconcile-javascript-runtime` | `reconcile_javascript_runtime` |
| 144 | `trace-application-feature` | `trace_application_feature` |
| 145 | `trace-javascript-semantics` | `trace_javascript_semantics` |
| 146 | `compare-application-versions` | `compare_application_versions` |
| 147 | `compare-source-to-bundle` | `compare_source_to_bundle` |
| 148 | `compare-javascript-export-shapes` | `compare_javascript_export_shapes` |
| 149 | `build-reconstruction-obligation-ledger` | `build_reconstruction_obligation_ledger` |
| 150 | `evaluate-reconstruction-coverage` | `evaluate_reconstruction_coverage` |
| 151 | `project-android-application-graph` | `project_android_application_graph` |
| 152 | `project-apple-application-graph` | `project_apple_application_graph` |
| 153 | `project-harmony-application-graph` | `project_harmony_application_graph` |

## Evidence, scope, and limits

- `.ufo/waves/round-20/verify/round20/verb-coverage.json` — retained array and its `package_version` / `rev`; this is the directly read source of the list here.
- `.ufo/waves/round-20/w1/ScoutVerbZeroOracle.md:9-12,20,206-367` — retained original source identity (`rea-agents@6.5.0`, `dist/cliCommandNames.js`, SHA-256 `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3`), distinct count, and ordered 153-name table.
- `corpus/lessons/round-20-verifier-spotcheck.md:92-95` — 2026-10-21 retained closure says the installed `dist/cliCommandNames.js` was read as text (not run as REA), and its 153 distinct names matched the retained catalog; it also records that source-file SHA-256.
- `.ufo/waves/round-20/contract.md:71-75` — package/version provenance and underscore/hyphen token-counting rule.
- `.ufo/waves/round-20/tools/verb-coverage.py:99-105,169-199` — literal matcher transformation and the tool's package-version / module-loading implementation. This research did not execute `load_cli_commands`, import Node code, or run that tool.

No external URL was opened for this assignment (no external URL/date applies). I did not access the host-local npm cache path: the package source/hash details above are from retained reports, not a fresh byte/hash check. No LSP device was exposed in the available tool inventory; the findings are direct reads of retained text/JSON and do not claim semantic call-graph proof. No tests, builds, REA commands, providers, or source-row edits were run.

## Parent checks

Read-only check, if desired: compare all 153 ordered pairs to `verb-coverage.json` and independently compare the kebab-case column to `ScoutVerbZeroOracle.md:213-367`. Do not treat underscore tokens as user-facing CLI aliases. No code tests/builds are applicable to this report-only change; parent owns any broader final suite.