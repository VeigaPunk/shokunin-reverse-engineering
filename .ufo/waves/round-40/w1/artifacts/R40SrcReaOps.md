DONE — R40SrcReaOps: SOURCES candidate for the R40-C2 domain guard. S119 does NOT cover the needed files, so one new 11-column row (S123) is drafted; the draft row passes `sources-census.sh validate` (no E-code except the E11 copy artefact; W04 12 -> 13).

Artifacts: `.ufo/waves/round-40/w1/artifacts/R40SrcReaOps/` — `S123-row.md` (the row), `envelopes/` (5 success envelopes + 1 error + 1 full-output regions envelope), `rea-6.5.0-help.txt`, `rea-6.5.0-capabilities.json`, `rea-6.5.0-operations-toolEffects.txt`, `probe.py`, `rebuild-dev.sh`. Dir hashes are not claimed; the paths above are what the L1 freezes.

## 1. Package identity and S119 scope check

- Re-downloaded `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` (curl, 5634033 B): sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` = the S119/S080 value. `diff -rq <extracted>/package/dist <installed>/dist` → empty (`DIST-IDENTICAL`), 1574 files; `package.json` identical. All line numbers below are from the installed copy = tarball.
- S119 (`corpus/SOURCES.md:125`) scope: "extraction-gap kinds, the `dependencies` field, `unpublished_entries` and how unblob reports reach `diagnostics`". Anchor files: `firmwareAnalysis.js:84-91,:100`, `FirmwarePublication.js:68-75,301-308` (+ `FirmwareReports.js`, per the knowledge note). None of `FirmwareAnalysisService.js`, `FirmwareProvider.js`, `FirmwareRelease.js`, `evidence.js`, `cliCommandNames.js`, `ReverseEngineeringService.js` is anchored, and the scope excludes envelope operation/provider and other operations. A used-by/scope edit would also rewrite S119's anchor/teaches (S083 precedent, `SOURCES.md` search-log 2026-10-22 round 27: same package, new row because an existing row's cells cannot change in place). => new row S123 (next free id; S122 is the highest).
- Census (run `scripts/sources-census.sh validate --file <copy with S123 inserted after S122> --today 2026-10-26`): 11 columns; only findings are E11 for every used-by path (the copy lives outside the lane, so relative paths do not resolve; the real row's `plans/round-40-claims.md` exists on disk) and W04 on S123's reused tarball URL (13 W04 vs 12 now; the same cost S119 paid). Unchanged lane file: exit 0, 12×W04.

## 2. Where `operation` and the provider id are set (file:line, quotes <=25 words)

| fact | where | quote |
|---|---|---|
| CLI verbs -> operation strings | `dist/cli/firmwareCommands.js:29` ; `:50` | `execute(CLI_COMMANDS.inspectFirmwareRegions, "inspect_firmware_regions",` ; `execute(CLI_COMMANDS.extractFirmware, "extract_firmware", {` |
| the envelope's `operation` is the string the verb passed | `dist/application/firmware/FirmwareAnalysisService.js:28-29` | `return ok(createEvidence(execution.subject, execution.provider, { operation,` |
| field is copied verbatim into the envelope | `dist/domain/evidence.js:281` (schema `:105` `operation: z.string().min(1)`) | `operation: observation.operation,` |
| `provider` copied from the execution | `dist/domain/evidence.js:274-278` (schema `:102`) | `provider: { id: provider.id, name: provider.name, version: provider.version,` |
| provider chosen by operation | `dist/firmware/FirmwareProvider.js:141` | `const engineName = request.operation === "inspect_firmware_regions" ? "binwalk" : "unblob";` |
| catalog identity attached | `dist/firmware/FirmwareProvider.js:281-284` | `const catalog = engineName === "binwalk" ? BINWALK_PROVIDER_IDENTITY : UNBLOB_PROVIDER_IDENTITY;` |
| ids | `dist/firmware/FirmwareRelease.js:15-18`, `:21-24` | `id: "binwalk", name: "Binwalk"` ; `id: "unblob", name: "Unblob"` (version from the observed banner via `{ ...catalog, version: admitted.version }`) |
| the operation literal is also a schema discriminant | `dist/domain/firmware/firmwareAnalysis.js:54,58` | `operation: z.literal("extract_firmware"),` |
| other ops, same mechanism | `dist/application/reverse/ReverseEngineeringService.js:103,111` ; ids `dist/rizin/RizinCommand.js:3`, `dist/objdump/ObjdumpCommand.js:3`, `dist/evm/EvmoleRelease.js:3` | `this.#observe("execute_rizin_command", command, input.path, ...)` ; `id: "rizin"` / `"gnu.objdump"` / `"evmole-interface"` |
| firmware verbs gated by env vars | `dist/firmware/FirmwareCommand.js:18` ; `dist/application/CapabilityInventory.js:315-318` | `const variable = engine === "binwalk" ? "REA_BINWALK_COMMAND" : "REA_UNBLOB_COMMAND";` |

Observed on a real run (below) the committed R39 receipts agree: `corpus/evidence/round-39/c1/K1/after.json` has `operation: extract_firmware`, `provider: {id: unblob, name: Unblob, version: 26.6.4}`.

## 3. Operation surface

- CLI: `npx -y rea-agents@6.5.0 --help` (exit 0) lists 155 commands (`rea-6.5.0-help.txt`). Operation catalog: `Object.keys(TOOL_EFFECTS)` from `dist/contracts/toolEffects.js` = 207 names (`rea-6.5.0-operations-toolEffects.txt`; the file has 207 lines, the 208 in my grep counted a non-key line). CLI verb -> operation aliases: `dist/cliCommandNames.js:162-182` (`analyze`/`inspect` -> `binary_overview`, `search` -> `search_strings`+`search_procedures`, `"execute-rizin-command": ["execute_rizin_command"]` at `:176`, `"inspect-with-objdump"` at `:174`); every other verb is its snake_case.
- Firmware operations are exactly two (`firmwareAnalysis.js:54,58`): `inspect_firmware_regions` (provider `binwalk`) and `extract_firmware` (provider `unblob`).
- `rea capabilities` (even with `REA_UNBLOB_COMMAND` set) lists 19 operations over 4 providers (`native-macos`, `rea-artifact-graph`, `rea-dotnet-static`, `sqlite`) and neither firmware operation (`rea-6.5.0-capabilities.json`); the gating exists at `CapabilityInventory.js:315`, but `capabilities` is not a way to enumerate firmware ops [observed].

## 4. Which operations accept a SquashFS file — probe matrix (development input only)

Input: `dev.sqfs`, 361 B, built with `python3 tools/round-39/gen-squashfs.py tree dev.sqfs --endian le --comp gzip` from {a/x.txt, y.txt, lnk->y.txt}; sha256 `7494b3d7634e76868a6c8bf3b5609cd9f3bb6c60e08a4b305ad66eed01f951b3`. Not a carrier. `cd $S; REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 <verb> dev.sqfs ... --format json`; `probe.py` summarises. Rebuild: `rebuild-dev.sh`.

Exit 0 with an Evidence envelope (accept the file):

| CLI verb | `operation` | `provider.id` | subject.format | what it says about the file |
|---|---|---|---|---|
| `extract-firmware dev.sqfs OUT` | `extract_firmware` | `unblob` (26.6.4) | `file` | chunks, gaps, files (the C2 domain) |
| `inspect-firmware-regions dev.sqfs` | `inspect_firmware_regions` | `binwalk` (3.1.0) | `file` | `coverage: signature_scan`, region `signature: squashfs`, "SquashFS file system, little endian, version: 4.0 ..." |
| `execute-rizin-command dev.sqfs i` | `execute_rizin_command` | `rizin` (version null) | `unknown` | stdout `type  Squashfs filesystem, little endian, version 4.0 ...` |
| `inspect-with-objdump dev.sqfs file_headers` | `inspect_with_objdump` | `gnu.objdump` | `unknown` | raw objdump text |
| `inspect-evm-interface dev.sqfs raw` | `inspect_evm_interface` | `evmole-interface` | `file` | treats the bytes as EVM bytecode |

Exit 1 with an error object, no `operation`/`provider` (reject the file): `inspect-artifact`, `extract-artifact`, `analyze`, `inspect`, `inspect-binary-layout` (`invalid_format`, "does not contain an ELF header"), `inspect-android-package`, `inspect-managed-artifact`, `inspect-managed-members`, `inspect-plist`, `inspect-signature`, `inspect-macho`, `list-architectures`, `inspect-keyed-archive` (all `target_unavailable`/"unsupported binary format", from `dist/domain/binaryTarget.js:24`, reached after the ELF, MZ, Mach-O and FAT checks at `:11-23`); `inspect-go-binary`, `inspect-rust-binary`, `inspect-electron-fuses`, `analyze-javascript-application` (`unsupported_target`); `inspect-sqlite-database`, `inspect-pe-resources`, `inspect-recorded-crash`, `inspect-dart-aot`, `identify-flutter-build` (`invalid_request`/`invalid_format`); `decode-android-resources` (apktool exception); `import-reference-source` ("not a directory"). Env-blocked, not tested for acceptance: `inspect-wasm-artifact` (`REA_WABT_BIN_DIRECTORY`), `inspect-pcap-capture` (no tshark). Needs other args: `inspect-packet-capture`, `recover-javascript-sources`. `dist/artifacts/` readers are Zip/Asar/Directory/NativeDmg/MachOSlice only; `grep -il squash` over `dist` finds nothing (the shipped code has no SquashFS reader).
- Error envelope shape: bare `{error?, code, category, message, retryable, remediation, details}`; with `--full-output` `{ok:false, error, meta}`. A `details.operation` exists for `invalid_request` errors (e.g. `inspect_binary_layout`) — a guard must read the top-level `operation`, never `details.operation`.
- `--full-output` success shape: `{ok:true, data:<evidence>, meta:{command, duration}}`; `data.operation` / `data.provider.id` carry the domain keys (`envelopes/full-regions.json`).

## 5. Finding that bears on the C2 claim (R39-CL1, now observed)

Running the frozen v1 interpreter (`python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json <envelope>`) on four non-`extract_firmware` envelopes of the SquashFS file: `inspect_firmware_regions` (bare and `{ok,data,meta}`), `execute_rizin_command`, `inspect_with_objdump`, `inspect_evm_interface` each print label `no-squashfs-chunk` (features `H=[] G=[] P=0`, `row[1]=none` handler), exit 0 — even though binwalk and rizin both report a SquashFS. The error envelope (`full-err.json`) exits 2 ("no normalized_result"). So v1 has no domain guard: an out-of-domain envelope of a SquashFS is silently mislabelled, not `unclassified`. The v2 `operation`/`provider` columns fix this; the draft's out-of-domain class ("a non-`extract-firmware` REA operation on a SquashFS carrier") has a real, one-command generator: `inspect-firmware-regions CARRIER` (provider `binwalk`, exit 0, region text names SquashFS) or `execute-rizin-command CARRIER i`. Nothing was run on a C2 held-out carrier.

Note for the table grammar [INFERENCE]: `inspect_firmware_regions` envelopes have no `extraction_gaps`/`chunks`, so any column cell that is `*` on handler/gap would match them; only the `operation` + `provider` columns separate them, and `provider.version` is per-run (observed banner), so the guard should key on `provider.id`, not name+version.

## 6. Draft SOURCES row (copy of `S123-row.md`; insert after S122 at `corpus/SOURCES.md:128`)

| S123 | rea-agents 6.5.0 published package, envelope `operation`/provider assignment and operation surface — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz | code | A | which REA 6.5.0 code sets an Evidence envelope's `operation` and `provider.id`, the `extract_firmware`→`unblob` and `inspect_firmware_regions`→`binwalk` pairing, the operation catalog and CLI command map, and which commands read a SquashFS file; not gap kinds, `dependencies` or `unpublished_entries` (S119), not unblob's own behaviour, not other REA versions | tarball sha256 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699 re-downloaded 2026-10-26, equal to S119/S080; all 1574 `dist` files and `package.json` equal the installed copy; `dist/application/firmware/FirmwareAnalysisService.js:28-29` `createEvidence(execution.subject, execution.provider, { operation,`; `dist/firmware/FirmwareProvider.js:141` engine chosen by `request.operation`, `:281-284` catalog identity; `dist/firmware/FirmwareRelease.js:15-24` ids `binwalk`, `unblob`; `dist/domain/evidence.js:274-281`; `dist/cliCommandNames.js:162-182` CLI→operation aliases; `dist/domain/binaryTarget.js:11-24` | Gate a result on the envelope's own `operation` and `provider.id` before reading any firmware field: `extract_firmware`/`unblob` is the only pair that carries gaps and diagnostics, while `inspect_firmware_regions`/`binwalk`, `execute_rizin_command`/`rizin`, `inspect_with_objdump`/`gnu.objdump` and `inspect_evm_interface`/`evmole-interface` also exit 0 on a SquashFS file and carry none | mined | 2026-10-26 | on-release | plans/round-40-claims.md |

Search-log entry (draft, to add under `## Search log`): `- 2026-10-26 UTC, round 40 wave 1 (S123) — Question: which rea-agents 6.5.0 code sets an envelope's operation and provider id, what operations the CLI exposes, and which accept a SquashFS file. Where searched: the 6.5.0 tarball re-downloaded and diffed with the installed copy (one family, same package as S079/S080/S083/S119), plus CLI probes on a development SquashFS. Identified 7 files, screened 7, included 1 row (S123), because S119's anchor and scope cover only gap kinds, dependencies and unpublished entries. Excluded 0.`

## 7. Limits, tools, state

- No tool installed or upgraded. No REA/unblob run on any C1 carrier or any C2 held-out carrier; every REA call used `dev.sqfs` (own tree). unblob wrote nothing outside `$S`; REA outdirs `ex1`/`ex3` are in scratch. `inspect-with-objdump`, `inspect-evm-interface` and `execute-rizin-command` were run only on `dev.sqfs`.
- Not tested: whether `inspect-firmware-regions` and `execute-rizin-command` work on a genuine-AVM-layout image (no carrier touched) — the generator claim is established only for the lane-format LE image.
- Scratch `/fast/scratch/hyaku/kaidoku-r40/R40SrcReaOps` removed before yielding; no VCS command beyond read-only `git log/status`.
