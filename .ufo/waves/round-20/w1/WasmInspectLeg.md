# WasmInspectLeg — C2 inspect-wasm-artifact

## Observations

- Used the assigned clone `/tmp/kr20-WasmInspectLeg-2` at baseline `14f0260ad319ecc26994381b2415d5a999003375`. Ran the exact `npx -y rea-agents@6.5.0 inspect-wasm-artifact <carrier> --format json` argv on four shipped WASM carriers and repeated evmole; each receipt records argv, cwd, REA environment, UTC start/end, exit, stdout/stderr paths and hashes. All five REA calls exited 0. The `REA_WABT_BIN_DIRECTORY` value was `/home/vgpnk/.local/opt/wabt-1.0.42/bin` for each run.

| Carrier / owner | Bytes; subject SHA-256 | Evidence ID | Status; sections / imports / exports | Retained receipt pointers |
|---|---:|---|---|---|
| `evmole_bg.wasm`; npm `evmole@0.9.3` | 480805; `542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884` | `ev_16a0be885adf3dee8f857604b91d409f4113a97e198b5875e0416f678e356d89` | valid; 12 / 30 / 21 | `evidence/c2/wasm-inspect/evmole/receipt.json:33-47,62-78` |
| `zip-module.wasm`; npm `@zip.js/zip.js@2.15.0` | 55126; `1ebaf6e62f247a005189493097f460bc9050f248755c55ecba34fd54257a6bb2` | `ev_629d4ec0f9bedf3a4b7781c3f8c7625ce41eeeffa8fe6284daa535236fd6d3e7` | valid; 9 / 0 / 32 | `evidence/c2/wasm-inspect/zip-js/receipt.json:29-43,55-71` |
| `qcms_bg.wasm`; pacman owner `zcode 3.16.2-1` | 94519; `6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26` | `ev_4b405f45646e4f950cd835ac59af82e32c556f998ef1bd3a2628d998ea5f0225` | valid; 13 / 5 / 23 | `evidence/c2/wasm-inspect/qcms/receipt.json:29-43,58-74` |
| `openjpeg.wasm`; pacman owner `zcode 3.16.2-1` | 250009; `67b8e2b162da472e98cb48d3d32e3e38fff481b9b32ff4818e78bb248af88ab2` | `ev_b2156cd077af18e5e500ecd927eb439fd2527655f62136b6ae52cef3c3ece0ba` | valid; 11 / 17 / 6 | `evidence/c2/wasm-inspect/openjpeg/receipt.json:29-43,57-73` |

- Every call reported `interface_state: complete`, zero interface issues, `confidence: observed`, provider `wabt@1.0.42`, and the same five limitations: WAT is decoded form rather than original source/layout or runtime proof; import/export names are escaped WAT forms; JavaScript links are static literal candidates only; no target execution, implicit fetch, publisher-authenticity claim, or OS memory sandbox; each subprocess is limited to 30 seconds and 32 MiB combined output. These limitations are retained verbatim in each receipt (for example `evmole/receipt.json:64-78`).
- Determinism check: the repeat on the same evmole carrier returned the same Evidence ID and the same uncompressed stdout SHA-256 (`418cc183c91cd358175afea784ff20fb4093466f48eb6aa080a80f93d7394c65`); compressed stdout hashes also match. Compare `evmole/receipt.json:19-26,39-41` with `evmole-repeat/receipt.json:19-26,39-41`.
- WABT version banner: `/home/vgpnk/.local/opt/wabt-1.0.42/bin/wasm-validate --version` exited 0 and printed `1.0.42`; retained at `evidence/c2/wasm-inspect/wabt-version.stdout.txt:1` with command receipt `wabt-version.receipt.json:2-19`.
- The evmole raw stdout (13,954,282 bytes) exceeded the per-file 8 MiB ceiling and was xz-compressed to 434,600 bytes; pre- and post-compression SHA-256 values are in its receipt. Other stdout files are each below 8 MiB; stderr files are empty. No tools were installed or updated.

## Inference / limits

These runs demonstrate successful structural inspections on four shipped artifacts from three package identities, not general mastery or runtime correctness. The retained REA limitations prevent treating WAT, listed exports/imports, or candidate JavaScript references as proof of original source, loading behavior, or execution semantics.

## Delivery / blockers

Patch: `.ufo/waves/round-20/w1/patches/WasmInspectLeg-2.patch` (18 evidence files; staged diff stat: 18 files, 408 insertions). No blockers.