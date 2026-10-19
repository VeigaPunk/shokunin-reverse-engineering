# EX-3 — derive the `inspect-evm-interface` `ev_` ID domain

## Verdict

**REPRODUCED**, bounded to cached `rea-agents@6.4.0` and `@6.7.0` and the synthetic runtime / request variations retained under `EX-3/evidence/`. The named Unknown is the undetermined `ev_` ID formula for this verb family, cited at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`. That citation identifies the Unknown only; the reproduction evidence below was generated and recomputed for this claim.

## Work performed and evidence

- Probed one handcrafted 28-byte runtime through `inspect-evm-interface` in hex/raw form, with repeat, same-byte copied-path, and mutated-input variations at the two pinned package versions. Fixture bytes and eight full JSON envelopes are under `EX-3/evidence/fixtures/` and `EX-3/evidence/probes/`.
- Derived the identity projection from the cached package implementation: `EX-3/evidence/source-contract.txt` gives the package versions, source paths, line ranges, and projection; `source-hashes.txt` records source-file SHA-256 values.
- Independently recomputed IDs for all eight envelopes: `EX-3/evidence/recompute_evidence_ids.py` and `recompute-results.txt` show eight `match=True` results. Path-field deltas are recorded in `compare_paths.py` and `path-diff.txt`.

The observed formula is `ev_` + lowercase hexadecimal SHA-256 of the UTF-8 canonical JSON for the Evidence semantic projection. The package canonicalizer recursively sorts object keys in RFC 8785 UTF-16 code-unit order and emits compact JSON without extra separator whitespace. In `6.7.0` the projection includes `subject` (null or only `{digest, format, architecture}`), `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, and `evidence_links`. The `6.4.0` schema omits `relationship_coverage`. Neither schema includes the ID itself or subject `name`/`local_path`.

At `6.7.0`, same-path repeat IDs were both `ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`; same-byte, same-basename copies at different paths yielded `ev_6cbe1e3dfd0c345004eacb4369fef8f580f8766cd2b25ea0e629b1bf1c9a2917` and `ev_a633bebb47320f6815e8fab5884d5aea59b3c4c2509ed7e7ca676f1840d75afa`. The `6.4.0` base/copy pair likewise differed (`ev_36c9dd69420b7616e620527b817bb1b0682c73dd83daee212b1f86c3e8eb3bdc` vs `ev_e126868ef5a65750d8b8e038e2c152be474e28c2fc17cb35135b231f32be464f`). For the 6.7 copy pairs, `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` changed while carrier SHA, decoded runtime SHA, and function payload stayed equal. Display-only subject-name/local-path changes preserved the ID. The 28-byte fixture recovers selector `0xa9059cbb` at offset 19; decoded runtime SHA-256 is `53f39f7cfa290e524cd04a67a3a87a8778315e4711b8da06c7e9c4146b0eba41`.

## Command A measurement and map proposal

Fresh Command A baseline at HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804` is retained verbatim in `EX-3/evidence/command-A-before.txt`: `knowledge_files=85`, `mapped=85`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15`, `coverage_score=10.0`, `depth_score=10.0`. The proposed map token is `2026-10-19-arc3-r7-evm-evidence-id-domain`, to be appended to the EVM entry cell at `corpus/README.md:38` when the draft is integrated.

This seat was restricted to its own artifact paths, so this entry is staged only under `EX-3/entry-draft/`; neither `corpus/knowledge/` nor `corpus/README.md` was changed. Therefore the frozen 85 → 86 target and post-integration `missing=[]` / `dangling=[]` condition are **not yet measured**. The parent/integrator must land the draft and map token, then rerun Command A against that resulting tree. `EX-3/evidence/command-A-before.txt` is baseline evidence, not an after measurement.

## Recheck

The entry draft is `EX-3/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md`. Its recheck command uses the cached `6.7.0` CLI and `TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck`; the expected same-path ID is recorded there. The fixture is synthetic and the result is limited to this operation and the two named package versions; it does not generalize to all REA verbs, versions, or production EVM artifacts.
