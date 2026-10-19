<!-- corpus entry DRAFT — kaidoku-shokunin arc3-loop1-round7, seat EX-6 (c2).
     LAND-MOVE: copy this file to corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md
     and append `2026-10-19-arc3-r7-evm-evidence-id-domain` to the EVM coverage-map row
     in corpus/README.md (patch text and the 85→86 overlay projection are in EX-6.md).
     The post-landing Command A run is intentionally left to the integrator. Evidence JSON
     and the compact matrix are retained under `.ufo/waves/arc3-loop1-round7/claims/c2/EX-6/`. -->

# `inspect-evm-interface` evidence IDs — bounded path/canonicalization characterization

source: `.ufo/waves/arc3-loop1-round7/claims/c2/EX-6/evidence/` (six complete REA JSON envelopes + `matrix-summary.txt`); read-only carrier `.ufo/waves/arc3-loop1-round6/claims/c2/EX-7/out/viair-opt200/runtime.bin`.
verified-at: 2026-10-19
REA pin: `rea-agents@6.7.0`; envelopes identify provider `evmole-interface`, EVMole `evmole@0.9.3`.

## Question and boundary

The open `ev_` id-domain item is named in `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`, `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`, and carried as open in `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`. This entry adds a bounded first-hand characterization for one `inspect_evm_interface` request shape. It does **not** derive the full Evidence-ID formula, and does not generalize to other verbs, REA pins, carriers, or request parameters.

## Observation — exact bounded matrix

The source carrier and both scratch copies were re-hashed this round: 1,517 bytes; SHA-256 `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`. Each run used `raw` encoding and returned 15 normalized functions. For every response, the input and decoded-byte SHA-256 matched that digest, and the canonical JSON SHA-256 of `normalized_result.functions` was `3394626e1e49bdb2714faf1fbc942f20dfcbd2a35547a2de18e3c2005adbe1ce`.

- Same absolute path, same request, run twice: both IDs were `ev_a84a565969defaa739ab2567e8da826a284b4a8c4ee1564ec472ab1703b6a09c`; full response envelopes were byte-identical.
- Same absolute path and request, but `TMPDIR` changed from `A/tmp` to `B/tmp`: same ID and byte-identical envelope.
- Same resolved file supplied relatively (`A/carrier.bin`, from the scratch-root working directory) versus absolutely: CLI evidence normalized `parameters.path` to the same absolute path; same ID and byte-identical envelope.
- Same bytes and same directory, only basename changed to `renamed.bin`: ID `ev_a19a232f0589027e2b528a7fc5ad68ad95034faee95e3ff7ec98281d130f4912`.
- Same bytes and basename, only parent directory changed to `B/`: ID `ev_4634efd77db0fc4d9df111ea38e333651a992c004ccb6a5b5f0361de43843b79`.

All six complete envelopes are retained in the source directory above; `matrix-summary.txt` records their full IDs, envelope hashes, and paths. Directly observed: changing the resolved path's basename or parent changed the ID while the decoded bytes and function payload stayed identical; changing only `TMPDIR` or relative/absolute spelling of the same resolved path did not change the envelope. This supports path-sensitive identity for this bounded invocation, but does not reveal the hash inputs or algorithm.

## Bounded inference and remaining unknown

For `inspect_evm_interface` at REA 6.7.0 / EVMole 0.9.3, the tested `ev_` ID is repeatable for an identical resolved path/request, varies with the resolved file path, and is invariant here to `TMPDIR` and the spelling of a path that resolves to the same absolute path. This closes that finite path/canonicalization question only. The complete ID formula, other operation families, pins, encodings, and request shapes remain unknown. Compare cross-path results by decoded-byte SHA-256 plus the normalized function payload, not by `ev_` ID.

The envelopes label the result `confidence: inferred`, `authority: shipped-artifact`, and `runtime_execution: not-performed`. This measurement concerns envelope identity and output equality; selector, argument, and mutability claims remain REA/EVMole inferences, not verified ABI or runtime behavior. It makes no deployment, chain, or source-authenticity claim.

## Recheck recipe

Use a disk-backed scratch directory (not `/tmp`), create identical copies at two paths, and run the same pinned command twice at path A, once at path B, and with a second TMPDIR at path A. IDs are path-specific; compare the relation and decoded/function digests, not these run-specific IDs:

```bash
S=/var/tmp/evm-id-domain-recheck
mkdir -p "$S/A/tmp" "$S/B/tmp"
cp .ufo/waves/arc3-loop1-round6/claims/c2/EX-7/out/viair-opt200/runtime.bin "$S/A/carrier.bin"
cp "$S/A/carrier.bin" "$S/B/carrier.bin"
TMPDIR="$S/A/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$S/A/carrier.bin" raw --format json
TMPDIR="$S/A/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$S/A/carrier.bin" raw --format json
TMPDIR="$S/B/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$S/A/carrier.bin" raw --format json
TMPDIR="$S/B/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$S/B/carrier.bin" raw --format json
```

This is a RESULT-class bounded characterization, not source-level formula derivation or a universal statement about REA Evidence IDs.
