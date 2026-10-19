# CR-3 — C2 coverage: Vyper no-optimize alias

## Verdicts

- **REPRODUCED — selected Unknown:** for this exact K8 fixture and Vyper build, `--no-optimize` and `-O none` produce identical runtime text and decoded runtime bytes. No residual byte-level distinction was measured within this boundary.
- **REPRODUCED — REA comparison:** both independently probed input files return the same eight inferred function rows and decoded-bytecode identity.
- **VERIFIED — current Command A baseline:** at `947091d6b6f52684faf9ca53adf94ff8a0f6b006`, the source-derived baseline is 87 knowledge files / 87 mapped, with no missing or dangling tokens.
- **UNVERIFIABLE — post-landing count:** this seat only drafts the corpus entry and token; it does not modify `corpus/` or `corpus/README.md`. The 88/88 result below is a source-derived projection, not an after-landing Command A run.

## First-hand re-derivation

The tested input is the exact source copy at `kaidoku-shokunin/.ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/K8.vy` (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`). Compiler executable: `kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version output `0.4.3+commit.bff19ea2` (`evidence/rederive.log:1-9`). These source and compiler identities were freshly hashed for this seat; previous-round measurements are not used as evidence.

With scratch and `TMPDIR` under `/var/tmp`, the compiler emitted each non-optimized runtime twice. The exact outputs passed repeat `cmp`; the two option forms passed cross-mode `cmp`. Their settings JSON, ABI JSON, and method-identifier JSON also passed `cmp`. Exact measurements are in `evidence/rederive.log:10-29`:

- `--no-optimize`: 617 decoded bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`; compiler settings `{"experimental_codegen":false,"optimize":"none"}`.
- `-O none`: 617 decoded bytes, the same SHA-256 and compiler settings.
- Runtime hex stdout files also match byte-for-byte: each is SHA-256 `1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c` (`evidence/compile/noopt.runtime.hex` and `none.runtime.hex`).
- Positive control `-O gas`: 418 decoded bytes, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`, settings `optimize:"gas"`; its output differs from the non-optimized outputs.
- Both non-optimized variants produce eight ABI entries and eight method identifiers.

REA was run through `npx -y rea-agents@6.7.0`; the provider in both envelopes is `evmole-interface` / `evmole@0.9.3`. The two calls and exit codes are recorded at `evidence/probe/rea-run.txt:9-14`; full output is in `evidence/probe/noopt.json:1` and `evidence/probe/none.json:1`:

- `inspect-evm-interface` on `noopt.runtime.hex`: Evidence ID `ev_c66e9cc955e596bb3274f4e05fcc6e5485a1436f3e470fdb88efad5627ad22d3`.
- `inspect-evm-interface` on `none.runtime.hex`: Evidence ID `ev_66d04e37dbeb49549e763585c63a8856f46b3f455af02ebb499cc0f65651d88f`.
- Each returns eight raw and eight normalized rows, all `dispatch:"abi"`. The sorted selector list is identical: `2ae1431c`, `364605a1`, `9adbf691`, `9b7c2962`, `bf3724af`, `cf35f823`, `d7531d91`, `d7b7913b`. Each decoded bytecode is 617 bytes with SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. Direct JSON comparison yielded `{"decoded_bytecode_bytes_identical":true,"decoded_bytecode_sha_identical":true,"normalized_functions_identical":true,"raw_functions_identical":true}`.

## Proposed corpus entry (draft only; not landed)

<!-- Proposed destination: corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-alias.md. Proposed EVM-map token: 2026-10-19-arc3-r9-vyper-noopt-alias. -->

# Vyper 0.4.3 K8: `--no-optimize` and `-O none` produce identical output for this fixture

verified-at: 2026-10-19

**Observation — input and tool identity.** The synthetic K8 source is the exact byte sequence at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/K8.vy` (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`). It was compiled with `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version `0.4.3+commit.bff19ea2`. Exact generated runtime files and JSON outputs are retained under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/compile/`.

**Observation — no-optimize boundary.** Two fresh `--no-optimize` runtime compilations and two fresh `-O none` runtime compilations each reproduce byte-identically. Cross-mode output compares equal with `cmp`; `-f settings`, `-f abi`, and `-f method_identifiers` output also compare equal. The decoded runtime is 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`; both settings records say `optimize:"none"`. A `-O gas` control produces a distinct 418-byte runtime, SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`, with `optimize:"gas"` (`.ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/rederive.log:10-29`). Thus the two tested spellings have no residual byte-level distinction for this source, this compiler build, and the runtime/ABI/method-identifier outputs examined.

**Observation — REA static inspection.** `npx -y rea-agents@6.7.0 inspect-evm-interface <runtime-hex-file> hex --format json` was run separately on both runtime files. The provider is `evmole-interface` / `evmole@0.9.3`; Evidence IDs are `ev_c66e9cc955e596bb3274f4e05fcc6e5485a1436f3e470fdb88efad5627ad22d3` (no-optimize) and `ev_66d04e37dbeb49549e763585c63a8856f46b3f455af02ebb499cc0f65651d88f` (`-O none`). Both envelopes return eight rows, all `dispatch:"abi"`, and the same selector set and decoded-bytecode SHA-256. Full envelopes are preserved in `.ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/probe/`.

**Inference and scope.** This establishes equivalence only for the exact K8 source bytes, Vyper `0.4.3+commit.bff19ea2`, and the compiler outputs named above. It does not prove a language-wide alias across other Vyper releases, sources, settings, or EVM targets. REA's selector/argument/mutability fields are upstream inferences (`confidence:"inferred"`); `discovery_completeness` is `unknown`, runtime execution was not performed, and no deployment identity, chain lookup, or runtime behavior is asserted. This is a synthetic compiler fixture, not evidence about a deployed contract.

**Recheck.** From the lane root, set `VYPER=.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` and `RUN=$(mktemp -d /var/tmp/vyper-noopt-check.XXXXXX); mkdir -p "$RUN/tmp"`; run `env TMPDIR="$RUN/tmp" "$VYPER" --no-optimize -f bytecode_runtime .ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/K8.vy > "$RUN/noopt.hex"` and `env TMPDIR="$RUN/tmp" "$VYPER" -O none -f bytecode_runtime .ufo/waves/arc3-loop1-round9/claims/c2/CR-3/evidence/K8.vy > "$RUN/none.hex"`; `cmp "$RUN/noopt.hex" "$RUN/none.hex"` must succeed. The recorded calls used `/var/tmp`; do not use `/tmp` on this host.

This closes only the fixture-scoped residual byte-level question raised by the Vyper optimizer-form entry. The prior record identifies the question (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:11,17`); all measurements above were re-derived in this seat.

## Coverage-map token and Command A

Proposed token to append to the EVM row at `corpus/README.md:38`: `2026-10-19-arc3-r9-vyper-noopt-alias`. Proposed entry filename: `2026-10-19-arc3-r9-vyper-noopt-alias.md`.

Command A (`SCORECARD.md:88-124`) was independently run against immutable HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. Exact baseline output:

```json
{"command_a_baseline":{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15},"hypothetical_single_entry_plus_map_token":{"dangling":[],"hypothetical_token":"2026-10-19-arc3-r9-vyper-noopt-alias","knowledge_files":88,"mapped":88,"missing":[]}}
```

The first object is a measured HEAD baseline. The second is a set projection for one matching proposed filename/token, not a post-landing gate result. Parent integration must land the entry and EVM-row token and run Command A at that revision to verify 87 → 88, mapped 88, missing `[]`, dangling `[]`. This seat made no changes to `corpus/`, `corpus/README.md`, or any tracked source file.

## Evidence files

- `CR-3/evidence/K8.vy` — exact tested source copy.
- `CR-3/evidence/rederive.log` — source/compiler identities, commands, `cmp` results and measured runtime hashes/sizes.
- `CR-3/evidence/compile/` — both repeat outputs, cross-mode outputs, settings, ABI and method identifiers, plus the gas control.
- `CR-3/evidence/probe/rea-run.txt` and `*.json` — exact REA invocations and complete JSON envelopes.
