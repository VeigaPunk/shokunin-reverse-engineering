<!-- DRAFT for integration only. Proposed corpus path: corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-forms.md. Proposed map token: 2026-10-19-arc3-r8-vyper-optimizer-forms (append once to the EVM row). Rerun Command A after actual landing; this seat did not modify corpus/ or corpus/README.md. -->

# Vyper 0.4.3 K8 optimizer forms — non-default dispatch byte-characterized; REA recovers 8/8 selectors

source: `.ufo/waves/arc3-loop1-round8/claims/c3/EX-7/evidence/` (the exact `K8.vy` source copy, compiler outputs, full REA JSON envelopes, and first-hand byte-walk/reconciliation outputs); original source `.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy`.
verified-at: 2026-10-19
recheck: from the lane root, run `B=/var/tmp/kaidoku-vyper-r8-recheck; V=.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper; SRC=.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy; mkdir -p "$B/tmp" && TMPDIR="$B/tmp" "$V" --no-optimize -f bytecode_runtime "$SRC" > "$B/noopt.hex" && TMPDIR="$B/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$B/noopt.hex" hex --format json && TMPDIR="$B/tmp" "$V" -O codesize -f bytecode_runtime "$SRC" > "$B/codesize.hex" && TMPDIR="$B/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$B/codesize.hex" hex --format json`. Full three-mode commands, tool identities, and raw outputs from this re-derivation are recorded in `.ufo/waves/arc3-loop1-round8/claims/c3/EX-7/evidence/rebuild-receipt.txt`.

## Observation — source, compiler, and recovered selectors

The input is a synthetic eight-function contract (`f0`–`f7`, each `view`, taking and returning `uint256`), not a deployed or shipped contract. The source bytes have SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. The compiler was re-identified at `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`: Vyper `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10` (`evidence/compiler/identity.txt`, `evidence/rebuild-receipt.txt`).

Fresh `bytecode_runtime` compilations, second-compiled byte-identical by `cmp`, yielded:

- `-O gas` control: 418 decoded bytes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`.
- `--no-optimize`: 617 decoded bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`; `-f settings` reports `optimize: none`.
- `-O codesize`: 360 decoded bytes, SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`; `-f settings` reports `optimize: codesize`.

The compiler ABI contains eight function signatures. A separate Keccak-256 derivation with PyCryptodome 3.24.1 agrees with the compiler's eight `method_identifiers`: `2ae1431c`, `364605a1`, `9adbf691`, `9b7c2962`, `bf3724af`, `cf35f823`, `d7531d91`, `d7b7913b` (`evidence/verify-final.txt`).

Three fresh `rea-agents@6.7.0 inspect-evm-interface <carrier> hex --format json` calls, provider `evmole-interface` / `evmole@0.9.3`, each return exactly those eight selectors, all `dispatch:"abi"`; the decoded bytecode length and SHA-256 match the freshly compiled runtime. Full envelopes and Evidence IDs:

- gas control: `ev_eaeb34c2e07ec78b266b285e63fc3075460c393be1ee61160c8d497c4838c0f3` (`evidence/probe/gas-6.7.0.json`).
- no-optimize: `ev_8d5c123382cd07af31bd0d8814ddd2e74be485bc502cc9937e5433863902d9c3` (`evidence/probe/noopt-6.7.0.json`).
- codesize: `ev_675503c5f19fe93f72c4a51e49783a597ed05eeceeed8d4dd08f60142e88bfbb` (`evidence/probe/codesize-6.7.0.json`).

The exact hex-carrier SHA-256 values (distinct from decoded runtime hashes) are respectively `b1f7fc882e44168156da34de403fa1573bcdfb0ebe8f9e501e94926c9b7c6b96`, `1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c`, and `c4af8ebcb724788f56c341c3dd0bfdb0d97aae74e1100e1c881d625f6c7ad68e` (`subject.digest.sha256` in the respective envelopes).

## Observation — distinct dispatcher forms and offset caveat

The independent opcode-boundary walk covers each complete decoded runtime (`evidence/characterize-final.txt`):

- The `-O gas` control has eight `PUSH4; DUP2; XOR; PUSH2; JUMPI` selector comparisons. Its eight REA offsets equal each selector `PUSH4` PC + 11.
- `--no-optimize` has eight opcode-boundary `PUSH4` selectors, each followed by `DUP2; EQ; ISZERO; PUSH2; JUMPI`. REA offsets are `31, 104, 177, 250, 323, 396, 469, 542`, each selector `PUSH4` PC + 12; every pointed-to byte is `0x34` (`CALLVALUE`). This is not the gas control's +11 offset convention.
- `-O codesize` has no opcode-boundary `PUSH4`, two `CODECOPY`s, one `MOD`, and one `EQ`. At runtime offset `0x12b`, the remaining tail is 61 bytes: a five-byte header followed by eight seven-byte selector/target/tag records. All eight selector records match the derived set; each target byte is a `JUMPDEST`, and each tag is `0x25`. The 27-byte sequence `01c3013008d7b7913b00a6259adbf6910074252ae1431c005b259b` is the first 27 bytes of that tail, not its full length. The analyzer reports offset 65 (`0x41`, `DUP1`) for all eight functions, not the table's eight distinct targets.

Inference: on this exact synthetic K8 source with Vyper 0.4.3, the two tested non-default settings produce different dispatcher encodings, while the pinned REA adapter recovers the same compiler/Keccak-cross-checked selectors from both. The packed codesize tail is data embedded in the runtime; this static byte walk does not establish execution of any target.

## Unknowns and scope

This closes the r4 entry's named byte-characterization Unknown (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`) only for this K8 source, Vyper `0.4.3+commit.bff19ea2`, and the explicitly tested `--no-optimize` and `-O codesize` options on this host. `-O none` was not compiled as a separate option (the `--no-optimize` settings output is `none`). Other Vyper releases, sources/selector counts, EVM targets, and optimizer settings remain unknown. The REA envelopes declare inferred results, `discovery_completeness:"unknown"`, and `runtime_execution:"not-performed"`; argument/mutability strings are not verified signatures. No deployment identity, runtime behavior, or chain/RPC state is claimed.
