# C2 WASM refusal/limit observations

All five envelopes are the exact captured CLI stdout in the sibling case directory; each `receipt.json` records argv, cwd, REA_* environment, UTC start/end, exit, carrier identity, and stdout/stderr hashes. Outer stderr was empty in all five runs. The command was `npx -y rea-agents@6.5.0 inspect-wasm-artifact <path> --format json`; case E additionally used the literal `--glue_paths <path>` option.

## Input identities

- Real carrier: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/evmole/dist/evmole_bg.wasm`, 480,805 bytes, SHA-256 `542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884`.
- Adjacent JS glue: `.../evmole/dist/evmole.mjs`, 16,174 bytes, SHA-256 `19715500c7344202b10783f314ee99d41c9259fbe522f43477c9708515807b14`.

## A — WABT env unset

- Carrier: real WASM above; `env_REA` is empty; exit 1.
- Envelope: `capability_unavailable` / `unsupported_provider`; message: `REA_WABT_BIN_DIRECTORY must be an absolute tool directory. Supply WABT 1.0.42 via absolute REA_WABT_BIN_DIRECTORY; REA does not install tools.`
- Evidence record: none (no Evidence ID in the returned envelope).
- Captures: `a-unset-wabt/receipt.json`; `a-unset-wabt/stdout.txt`.

## B — fake wasm-objdump version

- Carrier: real WASM above; env points to `/tmp/kr20-wasm-refusal-1od9iqo1/fake-wabt`; fake `wasm-objdump` SHA-256 `d89a6b340c53059841d84d9bc82655ba010f3f8df8c962d07975f9e4cf24b61d`; the other configured tools resolve to the 1.0.42 directory; exit 1.
- Envelope: `capability_unavailable` / `unsupported_provider`; message: `Unsupported wasm-objdump version banner; expected 1.0.42. Supply WABT 1.0.42 via absolute REA_WABT_BIN_DIRECTORY; REA does not install tools.` The fake executable was configured to print `1.0.41`.
- Evidence record: none (no Evidence ID in the returned envelope).
- Captures: `b-wrong-wabt-version/receipt.json`; `b-wrong-wabt-version/stdout.txt`.

## C — first 1,000 bytes of real WASM

- Carrier: `/tmp/kr20-wasm-refusal-1od9iqo1/truncated-first-1000.wasm`, 1,000 bytes, SHA-256 `5e73730c09d757d5e475b5c3deb47cb614144d739707344ba051cd268cff00a3`; WABT directory is the installed 1.0.42 directory; exit 1.
- Envelope: `invalid_request` / `invalid_input`; message: `Analysis input is invalid. Check the arguments and try again.` Issue: `invalid_format`; captured WABT stderr: `0000120: error: invalid section size: extends past end`.
- Evidence record: yes, partial observation `ev_b7b2bfab2f057e6d9e83abd33463199d82f89c8d63d03518f81d7e13919ebda2`; subject SHA-256 matches the 1,000-byte carrier. Limitation: WABT rejected these exact bytes with `--enable-all`; no complete inspection or target execution occurred.
- Captures: `c-truncated-1000/receipt.json`; `c-truncated-1000/stdout.txt`.

## D — non-WASM JavaScript file

- Carrier: adjacent `evmole.mjs`, 16,174 bytes, SHA-256 `19715500c7344202b10783f314ee99d41c9259fbe522f43477c9708515807b14`; WABT directory is the installed 1.0.42 directory; exit 1.
- Envelope: `invalid_request` / `invalid_input`; message: `Analysis input is invalid. Check the arguments and try again.` Issue: `invalid_format`; captured WABT stderr: `0000004: error: bad magic value`.
- Evidence record: yes, partial observation `ev_ac55ab0535b9eea69fbac08b46dcbfcdad921987e634c5e68b729d38a18aafc3`; subject SHA-256 matches the JS carrier. Limitation: WABT rejected these exact bytes with `--enable-all`; no complete inspection or target execution occurred.
- Captures: `d-non-wasm-js/receipt.json`; `d-non-wasm-js/stdout.txt`.

## E — adjacent JS glue selected with --glue_paths

- Carrier: real WASM above; glue: adjacent `evmole.mjs` above; WABT directory is installed 1.0.42; exit 0.
- Envelope: success, Evidence ID `ev_f3d0de4d02721ece46d1c3e469d3f527709840b080b330e97f650e5b6a1f7501`; subject SHA-256 is the real WASM hash; provider `wabt-artifact`, version `wabt@1.0.42`; validation `valid`; 12 sections, 30 imports, 21 exports.
- Glue result: parse status `complete`; two AST-observed static literals `evmole_bg.wasm` (glue lines 434 and 447), each associated as `local-path-candidate` with the selected WASM path. The result records runtime execution and network fetch as `not-performed`.
- Limitations recorded in the Evidence: WAT is decoded representation, not source or proof of runtime behavior; it does not prove original layout or round-trip byte identity; imports/exports preserve top-level WAT forms and names remain escaped producer text; glue references are static literals and associations, not proven data flow, URL-to-file identity, or runtime loading (computed references/aliases are unresolved); no target execution/implicit fetch; caller-supplied WABT tools are trusted and hashes identify bytes, not publisher authenticity, and no OS memory sandbox is claimed; each subprocess has a 30-second deadline and 32 MiB combined-output budget and oversized output fails rather than succeeding truncated.
- Raw stdout was 13,955,029 bytes (SHA-256 `014b02b28f8dce9c872347225505859786cac297fa2146cf05f53305bfcbd501`) and is retained as XZ, 434,820 bytes (SHA-256 `e292853d6596b06f67f1e9b7eb6f04d4f132254ad3f00fb94bdfba565a565554`); see `e-glue-paths/receipt.json` and `e-glue-paths/stdout.xz.part000`.

## Taxonomy

- Configuration/provider unavailability (A, B): capability-level refusal, exit 1, no Evidence.
- Input-format rejection (C, D): `invalid_request`, exit 1, partial observed Evidence returned with WABT diagnostics.
- Valid inspection plus selected glue analysis (E): exit 0 and complete observed Evidence; static literal association only, not execution or runtime-loading proof.
