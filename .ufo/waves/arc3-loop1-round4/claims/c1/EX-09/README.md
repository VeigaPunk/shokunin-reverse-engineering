# EX-09 artifacts — arc3-loop1-round4, chain c1 (controls)

Seat task: *controls: non-bytecode input; vyper creation/init bytecode;
wrong-encoding trap (raw over hex text); capture each envelope.*

Repo HEAD at work: `015e1bab914713568f339fd53999bc180459cc40` (no git mutations;
custody paths never read; scratch under `/var/tmp/ex09-r4`, never `/tmp`).

## Layout

| dir | contents |
|---|---|
| `carriers/` | every byte the probes read: Vyper runtime/creation (stripped, `0x`-prefixed, raw), the r3 solc control, the non-bytecode carriers, the encoding-trap carriers |
| `vyper/` | the three Vyper sources + their `bytecode` / `bytecode_runtime` / `abi` outputs |
| `planted/` | `planted-K.json` (Vyper-ABI-derived selector set, recorded **pre-probe**, two independent keccak impls agreeing) + the recording script |
| `probe/` | one sealed envelope (or one typed error object) per invocation |
| `analysis/` | the reconciliation harness and its outputs |

## Compiler

`vyper 0.4.3+commit.bff19ea2`, from the wave's one authorized install
(`.ufo/waves/arc3-loop1-round4/tools/vyper-venv/`, EX-02's receipt at
`claims/c1/EX-02/install.log` + `attest-output.txt`; wheel sha256
`3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd`). The same
sources were first compiled with EX-02's staged interpreter at
`/var/tmp/ex02/prep314/bin/vyper`; recompiling with the wave venv produced
**byte-identical** `creation.hex`, `runtime.hex` and `abi.json`.

## Envelope census

48 JSON files in `probe/`: 36 successful envelopes and 12 typed error objects.
Every success carries the provider block `evmole-interface` / "REA EVM interface
adapter" / `evmole@0.9.3`, `authority: shipped-artifact`,
`confidence: inferred`, `runtime_execution: not-performed`.

## Re-run

```bash
# reconciliation (reads sealed envelopes + carriers only; never invokes the probe)
python3 analysis/verify-ex09.py

# one leg, from scratch
mkdir -p /var/tmp/recheck && TMPDIR=/var/tmp/recheck \
  npx -y rea-agents@6.4.0 inspect-evm-interface carriers/Ex09Vault.runtime.hex hex --format json
```

`TMPDIR` must be disk-backed: a `/tmp`-defaulted run fails EDQUOT in the EVMole
worker (r3 entry, unchanged).
