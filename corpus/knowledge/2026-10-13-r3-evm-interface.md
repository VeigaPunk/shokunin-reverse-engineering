<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/07-evm.md. -->

# 07 — EVM interface inspection (round 3)

Round 2 discovered the EVM surface is unblocked — `inspect-evm-interface` ships
with EVMole 0.9.3 (WASM, bundled in rea-agents@6.4.0, no external deps) — but
never executed it. This round synthesizes local bytecode carriers and runs the
command for real.

## Candidates

### Candidate 1 — minimal arithmetic snippet `6001600101` (run)

- **claim:** a 5-byte hex carrier (`PUSH1 1, PUSH1 1, ADD`) decodes cleanly and
  returns a valid Evidence envelope with an empty function list.
- **source:** `/tmp/evm-carrier-1.hex`, written by this lane (printf; 10 ASCII
  hex chars = 5 bytecode bytes; sha256 `27dc8217…a87c3`; decoded bytecode
  sha256 `b20db086…e54fb`).
- **verify:** `rea inspect-evm-interface /tmp/evm-carrier-1.hex hex --format json`
  → success. Provider `evmole-interface` / "REA EVM interface adapter",
  `version: evmole@0.9.3`. `raw_result.functions: []`,
  `normalized_result.functions: []`, `evidence_kind: "inferred"`,
  `runtime_execution: "not-performed"`, `discovery_completeness: "unknown"`.
  Bytecode kind/hardfork/deployment_authenticity all `"unknown"` — honest, no
  dispatch exists in 5 bytes.
- **verified-at:** 2026-10-13T15:43Z
- **suggested:** correct baseline: tool runs, decodes, reports empty without
  fabricating selectors.

### Candidate 2 — minimal contract blob (creation+runtime, 42 bytes) (run)

- **claim:** a realistic `60806040…a164736f6c6343` creation blob with an
  all-REVERT runtime decodes but yields no selectors.
- **source:** `/tmp/evm-carrier-2.hex` (task-supplied minimal contract; 84 hex
  chars = 42 bytes; carrier sha256 `c8c64f44…75ab`; bytecode sha256
  `c4826075…2dbf`).
- **verify:** `rea inspect-evm-interface /tmp/evm-carrier-2.hex hex --format json`
  → success. `functions: []`, and notably `bytecode.kind: "unknown"` —
  EVMole does NOT classify this as creation/deploy code even though the
  `…f3fe…` RETURN+metadata pattern is present. Runtime stub contains only
  REVERT, so empty selectors are expected; the unclassified `kind` is an
  honest "no inference made" rather than a failure.
- **verified-at:** 2026-10-13T15:43Z
- **suggested:** treat `kind: "unknown"` as the default floor; classification
  appears to need richer bytecode (real solc output) to engage.

### Candidate 3 — hand-assembled dispatcher with real ERC-20 selectors (run)

- **claim:** an 81-byte runtime with a Solidity-style selector dispatch
  (`CALLDATALOAD; SHR 0xe0; EQ/JUMPI` per selector) yields recovered
  function selectors with bytecode offsets.
- **source:** `/tmp/evm-carrier-3.hex`, hand-assembled by this lane. Dispatch
  chain: `0x63a9059cbb` → `transfer(address,uint256)`, `0x6370a08231` →
  `balanceOf(address)`, `0x63095ea7b3` → `approve(address,uint256)`; bodies
  are minimal ADD/MUL/SUB stubs. Bytecode sha256
  `3e2fd6ca…fe67`.
- **verify:**
  - `rea inspect-evm-interface /tmp/evm-carrier-3.hex hex --format json` →
    success. `raw_result.functions` recovered all 3 selectors:
    `a9059cbb` @ offset 62, `70a08231` @ 68, `095ea7b3` @ 74 — every
    dispatched selector found, zero false positives, offsets point at the
    PUSH4 sites. `dispatch: "abi"` for all three.
  - `inferred_arguments: ""` — expected: stub bodies never decode calldata,
    so EVMole honestly reports no argument tuple rather than guessing
    `(address,uint256)`.
  - `inferred_state_mutability: "pure"` for all three — inference artifact:
    stubs contain no SLOAD/SSTORE/CALL, consistent with the shipped
    limitation "recovered selectors … are upstream inferences, not verified
    ABI signatures or names".
  - `raw`-encoding twin: `/tmp/evm-carrier-3.bin` (same 81 bytes, written via
    node Buffer) → identical selector set and identical bytecode sha256 —
    `raw` and `hex` paths converge on the same decoded bytes.
- **verified-at:** 2026-10-13T15:44Z
- **suggested:** mark selector recovery **held**. Frontier: real solc-compiled
  runtime bytecode where `inferred_arguments`/`stateMutability` have actual
  signal to infer from, plus creation-code `kind` classification.

### Candidate 4 — input-validation edges (run)

- **claim:** the command fails closed with typed refusals on bad input.
- **source:** synthesized by this lane: nonexistent path, `zzzznothex`
  carrier, `0x`-prefixed hex carrier.
- **verify:**
  - Missing file → `code: invalid_request`, `category: invalid_input`,
    `retryable: true`, issue detail `path: "Selected bytecode carrier could
    not be read (ENOENT)"`. Real process exit code **1** (verified without a
    pipe — earlier piped runs masked it behind `head`).
  - Malformed hex → typed refusal: "Hex carrier requires complete
    hexadecimal byte pairs, an optional 0x prefix and outer ASCII
    whitespace; interior separators are invalid." — precise, actionable.
  - `0x6001600101` hex carrier → accepted; decoded to the same bytecode
    sha256 (`b20db086…`) as the unprefixed carrier 1 — `0x` prefix honored.
  - CLI shape: encoding is a POSITIONAL arg (`rea inspect-evm-interface
    <path> <raw|hex>`), NOT a flag — `--encoding hex` returns
    `Unknown flag: --encoding` (exit 1). `--schema` advertises it as a
    property; the dispatch protocol differs from flag-shaped commands.
- **verified-at:** 2026-10-13T15:44Z
- **suggested:** record the positional-arg quirk in the lane's command
  cookbook; schema shape and CLI shape diverge here.

## Run log

- `printf '6001600101' > /tmp/evm-carrier-1.hex`; `printf '60806040…6c6343'
  > /tmp/evm-carrier-2.hex` — carriers 1–2 synthesized.
- `npx -y rea-agents@6.4.0 inspect-evm-interface --schema` → args `{path,
  encoding enum[raw,hex]}`, both required.
- `inspect-evm-interface <file> --encoding hex` → `Unknown flag: --encoding`
  (exit 1) — flag form rejected.
- `inspect-evm-interface --help` → usage `rea inspect-evm-interface <path>
  <raw|hex>` — encoding is positional.
- `inspect-evm-interface /tmp/evm-carrier-1.hex hex` → evidence
  `ev_6159275a…`, provider `evmole@0.9.3`, `functions: []`.
- `inspect-evm-interface /tmp/evm-carrier-2.hex hex` → evidence
  `ev_6cc06a1e…`, `functions: []`, `kind: "unknown"`.
- `grep -i 'evm|selector|abi|bytecode' --help` → `inspect-evm-interface` is
  the ONLY EVM command in the surface (no decompiler/disassembler sibling).
- Carrier 3 assembled (81 bytes, 3 selectors, PUSH4 offsets 62/68/74);
  `inspect-evm-interface … hex` → evidence `ev_a428ec89…`, all 3 selectors
  recovered, `dispatch: "abi"`, `stateMutability: "pure"`, empty args.
- `node -e` wrote `/tmp/evm-carrier-3.bin`; `inspect-evm-interface … raw` →
  identical selectors + bytecode sha256 (`raw` ≡ `hex` decode path). Note:
  `xxd` absent on this host; node used instead.
- Failure probes: ENOENT → typed `invalid_request` exit 1; `zzzznothex` →
  typed format refusal; `0x`-prefixed hex → accepted, same decode.
- Worker limits disclosed in envelope limitations: 256 MiB JS heap, 3 GiB
  address space, 30 s deadline, 16 MiB file cap; `confidence: inferred`,
  `authority: shipped-artifact`; explicit caveat that SHA-256 ≠ Ethereum
  Keccak code hash and no chain/RPC lookup is performed.
- `rm -f /tmp/evm-*` — scratch cleaned, nothing left behind.

## Summary

**EVM held.** `inspect-evm-interface` (EVMole 0.9.3, WASM-bundled, zero
external deps) executes for real in round 3: it decoded three synthesized
carriers, recovered all three planted ERC-20 selectors (`a9059cbb`,
`70a08231`, `095ea7b3`) with exact PUSH4 bytecode offsets and
`dispatch: "abi"`, emitted honest empty results on dispatch-less bytecode,
and failed closed with typed `invalid_request` refusals on missing files and
malformed hex. Both `hex` (with optional `0x` prefix) and `raw` encodings
work and converge. Two caveats worth carrying: (a) encoding is a positional
arg, not `--encoding`; (b) recovered fields are upstream inferences —
selectors stay as bare hashes (no signature DB → no name resolution),
`inferred_arguments` only populates when bodies actually decode calldata,
and `bytecode.kind` stayed `unknown` even on a creation-code blob. Remaining
EVM frontier: real solc/vyper-compiled bytecode (argument + mutability
inference with real signal, `kind` classification), larger dispatch tables,
and Vyper-style selector layouts vs Solidity's.

## Errata (round 4)

- **`bytecodeOffset` semantics corrected (r4 audit-A, verified 2026-10-13):** the selector
  findings' `bytecodeOffset` records the **JUMPDEST dispatch-target position**, not the
  PUSH4 comparison site. Carrier 3's recorded offsets (62/68/74) sit at jump destinations.
  The selector→push-site mapping is still derivable from the disassembly but is not what
  the field emits.
