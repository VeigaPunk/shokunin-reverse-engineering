# Draft — `inspect-evm-interface` evidence ID derivation and path-sensitive identity

source: `.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/source-contract.txt`, `source-hashes.txt`, `probes/{64-base,64-copyA,67-base1,67-base2,67-copyA,67-copyB,67-mutated,67-raw}.json`, `recompute_evidence_ids.py`, `recompute-results.txt`, `compare_paths.py`, `path-diff.txt`, and `fixtures/`; the prior Unknown is named in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` (that citation identifies the Unknown, not this entry's probe evidence).
verified-at: 2026-10-19
recheck: `mkdir -p /var/tmp/kaidoku-ex3-r7-recheck && TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-evm-interface "$PWD/.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/fixtures/base/selector.hex" hex --format json` → on this host's cached `rea-agents@6.7.0`, expect `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`; `TMPDIR` must be disk-backed here.

## Result

The previously named Unknown is the `ev_` Evidence-ID formula for the `inspect-evm-interface` verb family: path sensitivity had been measured, but the formula had not been derived. This draft closes it narrowly for `rea-agents@6.4.0` and `@6.7.0` on the synthetic runtime fixture and requests exercised here. It does not establish a universal formula for other REA verbs, packages, or operations.

In both inspected package versions, the ID is `ev_` followed by the lowercase hexadecimal SHA-256 of the UTF-8 canonical JSON for a semantic projection of the Evidence object. The package canonicalizer recursively sorts object keys in RFC 8785 UTF-16 code-unit order and emits compact JSON without extra separator whitespace. In `6.7.0`, the projection is `{subject, provider, analysis_profile, predicate_type, operation, parameters, raw_result, normalized_result, confidence, authority, environment, limitations, relationship_coverage, locations, evidence_links}`. `subject` is `null` or `{digest, format, architecture}`. The `6.4.0` Evidence schema and projection have the same fields except that `relationship_coverage` is absent. Neither projection hashes the ID itself or the subject's display-only `name` and `local_path`. The cached package source locations, hashes, and line references are recorded in `evidence/source-contract.txt` and `evidence/source-hashes.txt`.

## Reproduced evidence

The fixture is a handcrafted 28-byte EVM runtime (`60003560e01c8063a9059cbb146013575f80fd5b60005260206000f3`), not a deployed contract or a production corpus sample. Both hex and raw probes recover selector `0xa9059cbb` at offset 19; the decoded runtime SHA-256 is `53f39f7cfa290e524cd04a67a3a87a8778315e4711b8da06c7e9c4146b0eba41`.

- At `6.7.0`, two same-path/same-request runs returned the same ID: base1 and base2 `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`.
- Same bytes and same basename copied to different paths returned distinct IDs: copyA `ev_6cbe1e3dfd0c345004eacb4369fef8f580f8766cd2b25ea0e629b1bf1c9a2917`; copyB `ev_a633bebb47320f6815e8fab5884d5aea59b3c4c2509ed7e7ca676f1840d75afa`.
- At `6.4.0`, base `ev_36c9dd69420b7616e620527b817bb1b0682c73dd83daee212b1f86c3e8eb3bdc` and its same-byte copyA `ev_e126868ef5a65750d8b8e038e2c152be474e28c2fc17cb35135b231f32be464f` also differ.
- The `6.7.0` mutated-input and raw-input runs returned `ev_c0fd3a49f3226bd1458373a8935e670cc948577f23f60f4e18e3a246ff54f75c` and `ev_75387f5c7467f1b6ab6b894a0444ef900ff0ab70fe23dcd1dc0d878b7c286b07`, respectively.

Independent recomputation from each of the eight full envelopes matches all eight claimed IDs (`evidence/recompute-results.txt`). Same-byte copy comparisons show equal carrier SHA, decoded runtime SHA, function payloads, and subject basename, while `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` change; these path-bearing semantic fields account for the observed ID change (`evidence/path-diff.txt`). Altering only `subject.name`/`subject.local_path` leaves the computed ID unchanged. Thus, for this operation, paths affect the ID because they are present in the semantic projection, not because the subject's display labels are hashed.

## Scope and limitations

This is a bounded characterization of the two pinned package versions using one synthetic runtime under `inspect-evm-interface`, with hex/raw and same-byte path-copy variations. It does not test all projection field types, missing/null combinations, all operations, or other package versions; it makes no claim about chain behavior or deployed code. The package source hashes bind the inspected implementation, while the full probe envelopes and fixture hashes are retained alongside this draft. This remains a draft: the corpus file and EVM map token have not been landed.
