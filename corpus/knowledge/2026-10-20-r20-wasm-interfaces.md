source: S041 (WABT 1.0.42 release identity), S042 (WebAssembly binary-format Modules: import/export entries), S040 (installed rea-agents@6.5.0 compiled source for the verb contracts); run evidence `.ufo/waves/round-20/evidence/c2/wasm-inspect/`, `.ufo/waves/round-20/evidence/c2/wasm-compare/`, `.ufo/waves/round-20/evidence/c2/wasm-refusals/` (receipts carry argv, cwd, REA_* env, UTC interval, exit, stdout/stderr sha256, carrier path+sha256).
verified-at: 2026-10-20 — REA CLI pinned `npx -y rea-agents@6.5.0`, `REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin` (official linux-x64 release, archive sha256 `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131`, installed by the round-20 L1 at 17:31 -03). Author-side runs by round-20 wave-1 seats WasmInspectLeg, WasmCompareLeg, WasmRefusalLeg; not outside verification.
recheck: `REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin npx -y rea-agents@6.5.0 inspect-wasm-artifact <carrier> --format json` and compare `evidence_id` with the receipt in the matching `evidence/c2/wasm-inspect/<label>/receipt.json`; for compare re-run the argv recorded in `evidence/c2/wasm-compare/compare-*.receipt.json`.

# WASM interface inspection and comparison (first held, round 20)

## What was exercised (observation)

`inspect-wasm-artifact` on four shipped modules, all exit 0, `interface_state: complete`, provider `wabt@1.0.42`, `confidence: observed`:

| Carrier (owner) | Bytes; SHA-256 | Evidence ID | sections / imports / exports |
|---|---|---|---|
| `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/evmole/dist/evmole_bg.wasm` (npm `evmole@0.9.3`) | 480805; `542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884` | `ev_16a0be885adf3dee8f857604b91d409f4113a97e198b5875e0416f678e356d89` | 12 / 30 / 21 |
| `.../@zip.js/zip.js/dist/zip-module.wasm` (npm `@zip.js/zip.js@2.15.0`) | 55126; `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | `ev_629d4ec0f9bedf3a4b7781c3f8c7625ce41eeeffa8fe6284daa535236fd6d3e7` | 9 / 0 / 32 |
| `/opt/ZCode/resources/glm/packages/pdf-plugin/dist/ui/pdfjs/wasm/qcms_bg.wasm` (pacman `zcode 3.16.2-1`) | 94519; `6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26` | `ev_4b405f45646e4f950cd835ac59af82e32c556f998ef1bd3a2628d998ea5f0225` | 13 / 5 / 23 |
| `/opt/ZCode/.../pdfjs/wasm/openjpeg.wasm` (pacman `zcode 3.16.2-1`) | 250009; `67b8e2b162da472e98cb48d3d32e3e38fff481b9b32ff4818e78bb248af88ab2` | `ev_b2156cd077af18e5e500ecd927eb439fd2527655f62136b6ae52cef3c3ece0ba` | 11 / 17 / 6 |

A repeated evmole call returned the same Evidence ID and the same uncompressed stdout SHA-256 (content+params-keyed for this verb on these inputs).

`compare-wasm-interfaces` (inputs: two inline `inspect_wasm_artifact` Evidence records) returned, with every compare exit 0:

| Pair | Scope | added / removed / changed / unchanged / unknown | Evidence ID |
|---|---|---|---|
| Synthetic v1→v2 WAT modules built with WABT `wat2wasm` (recipe and bytes in `evidence/c2/wasm-compare/synth/`) | both | 1 / 1 / 1 / 1 / 0 | `ev_2529e50816c83bb2f37c596678299e223a27ccca696672596a847397ada43351` |
| `qcms_bg.wasm` vs `openjpeg.wasm` (distinct real modules) | both | 23 / 28 / 0 / 0 / 0 | `ev_38716779400ae692129c94bd6d0af9627a4f511cc401977979429e4874eeaaf7` |
| Two package releases shipping byte-identical `zxing_reader.wasm` (sha256 `0e8d688d71932ebb6b8b33f700d43d3cb997f59ed9cab3c05102d7f10288a392`) | both | 0 / 0 / 0 / 98 / 0 | `ev_ca8b59b0c4763f0842ba684a50800fc7da5d9450e174c6ea9df2e85e1b1f34b9` |

The synthetic pair is the only case that exercised `changed` (one import signature) and the add/remove pair of named exports; the
real-module pair shows a different-module diff, not a version regression. No same-module, different-bytes version pair exists on this
host (wave-1 `ScoutWasmCarriers.md`: every repeated filename is byte-identical).

## Refusals and limits (observation)

- `REA_WABT_BIN_DIRECTORY` unset, or pointing at a fake `wasm-objdump` with another banner → `capability_unavailable`, no Evidence (`evidence/c2/wasm-refusals/`). REA gates on an absolute directory and the exact `1.0.42` banner of three tools (S040; wave-1 `ScoutWasmSchema.md`, `RevWasmVerb.md`).
- A 1000-byte truncation and a non-WASM file → exit 1 `invalid_request`/`invalid_input`, with partial observed Evidence (`ev_b7b2bfab…`, `ev_ac55ab05…`) carrying WABT's diagnostic (`invalid section size: extends past end`; `bad magic value`). An error exit can still mint an Evidence ID: an `ev_` id alone is not proof of a successful inspection.
- `--glue_paths` with evmole's adjacent JS → complete Evidence `ev_f3d0de4d02721ece46d1c3e469d3f527709840b080b330e97f650e5b6a1f7501`; glue associations are static string-literal matches, not execution.
- CLI has no `--detail` flag (MCP-only); full WAT is returned inline, so larger modules produce multi-MB stdout (retained xz-compressed where >8 MiB).

## Interpretation (inference, bounded)

Per S042 an import entry is module name + field name + external type, an export entry is a name + external index with no type: export
"signatures" in REA's comparison are resolved through the index spaces by WABT, not read from the export entry. A `changed` verdict is
therefore a type change at the same name; renames appear as add+remove. Interface equality does not establish ABI or runtime
compatibility (REA's own limitations). Not examined: modules >8 MiB (REA input cap), non-function import kinds beyond those present,
`interface.state: partial` paths, MCP `detail: "summary"`.

## Erratum — round-20 wave 2 (2026-10-21, appended; text above unchanged)

- **Source identity.** The `source:` line's `S040` is the Harmony-only installed-source row. The non-Harmony implementation source for
  the WASM verbs is **S048** (installed `rea-agents@6.5.0` CLI/service: `reverseEngineeringCommands.js`, `ReverseEngineeringService.js`,
  `domain/reverseEngineering.js`, `contracts/reverseEngineeringToolContracts.js`; retained extract
  `.ufo/waves/round-20/evidence/c2/rizin-pe/rea-cli-source-notes.md`). S041 (WABT release identity) and S042 (module grammar) stand.
- **Scope of the absent-pair statement.** "No same-module, different-bytes version pair exists on this host" holds for the scanned roots
  (`/usr/lib`, `/opt`, `/home/vgpnk/.npm/_npx`, `-xdev`) only; other mounts were not scanned (w1 `ScoutWasmCarriers.md:95-103,135-136`).
- **Install attribution.** The archive digest and extracted bytes are supported; the "installed by the round-20 L1 at 17:31 -03" instant is
  the L1's recorded action and has no retained install-event receipt. Treat it as a recorded action, not an observed event.
- **Replay.** A compare replay must regenerate `input_json` from the retained inspection Evidence; the receipt's temporary input path is
  not retained, so `argv` alone is not self-contained.
- **WABT signature resolution.** The export-signature explanation remains inference (S042 grammar; WABT not instrumented for that claim).
