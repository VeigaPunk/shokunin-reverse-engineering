# SC-3 — C2 depth: proposed queue-drain rule #17

Status: **draft for integration only**. No `SKILL.md`, corpus, gate, custody, scorecard, or log file was changed.

## Proposed rule #17

- **Establish `ev_` path sensitivity per operation by inspecting its semantic projection; never infer a domain-wide path rule.** For each verb, package version, and call shape, inspect the Evidence producer and projection, compare a same-path repeat with a same-byte, same-basename copy at another path, then recompute IDs from complete envelopes and mutate candidate projected path fields one at a time. State the tested scope and leave other shapes unknown. In REA 6.7.0, `inspect_evm_interface` and `inspect_rust_binary` change IDs when each of `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` changes. `inspect_artifact` excludes top-level subject display fields but includes nested inventory Evidence under `normalized_result`; mutating that nested `subject.local_path` changes the outer ID. The three operation-specific results are bounded to their cited inputs and calls: `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:11` and `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-26`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15` and `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:19-22`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-23`.

## First-hand measurements

### Command A baseline

Ran the source-derived Command A recipe at `SCORECARD.md:88-124` against both frozen HEAD and the supplied work commit. Exact outputs:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b358d0a1112d31808b9bae3d8ddd1b46875","rule_blocks":16}
```

The proposed draft is not in `SKILL.md`; its post-integration `rule_blocks=17` and citation-resolution check are **UNVERIFIABLE** until integration and a fresh Command A run.

### Fresh static REA probes and independent ID recomputation

Ran REA 6.7.0 from `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs`. All copies and `TMPDIR`s were under `/var/tmp/kaidoku-sc3-r12-rechecks`; original inputs were read-only. The EVM fixture, `/usr/bin/rustc`, and `/usr/bin/jq` plus their scratch copies were independently hashed before probing:

```text
EVM fixture: 8b5ae958c9d78fc1788b0886e44e54dce8f39ca9b98e2013ee7430d1d7f730df (base and both copies)
Rust binary: c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136 (original and both copies)
Artifact: e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 (original and copy)
```

Exact invocation shapes were `inspect-evm-interface <path> hex --format json`, `inspect-rust-binary <path> --format json --full-output`, and `inspect-artifact <path> --format json --full-output`. Each operation had two same-path calls and same-byte copies at distinct paths with the same basename. All calls exited 0 with zero stderr; stdout byte counts were EVM base1/base2 5065/5065 and copyA/copyB 4785/4785; Rust base1/base2 2676/2676 and copyA/copyB 2820/2820; artifact base1/base2 5613/5613 and copy 5703.

Then independently recomputed the outer `ev_` ID from each complete fresh envelope using the inspected semantic projection and canonical JSON rules (`python3 /var/tmp/kaidoku-sc3-r12-recompute.py`). Exact output:

```text
fresh_live_probes=3 operation_families; envelopes=11; recomputed_ids=11/11
inspect_evm_interface: base1=ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052, base2=ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052, copyA=ev_33b372e883a528a7b444344a47a9ef580042da383443fd3b33d82e30a6119994, copyB=ev_ea382d5f20eced165d6225a6219981e3727f69422ea26afbc015110f3db2becc
inspect_rust_binary: base1=ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256, base2=ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256, copyA=ev_a35b384663a0b36f6330ff4841361462d40ea36b1352496a676f9a5d20b0f646, copyB=ev_7ef692060bd5170335e4bfb439ba9866a19112320078547f1d5a0e14d603058b
inspect_artifact: base1=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca, base2=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca, copy=ev_bfc78d4a6ae21d815da0354e4fb9df0e9b464ddb2884d37aa5040672bea1ebeb
inspect_evm_interface: same_path_repeat=True; same_sha_other_path=True; id_changes_on_path_copy=True; single_path_field_mutations_change_id=3/3
inspect_rust_binary: same_path_repeat=True; same_sha_other_path=True; id_changes_on_path_copy=True; single_path_field_mutations_change_id=3/3
inspect_artifact: same_path_repeat=True; same_sha_other_path=True; id_changes_on_path_copy=True; top_level_display_only_same_id=True; nested_inventory_local_path_changes_id=True
```

### Verdicts

- **VERIFIED — baseline:** Command A independently measured 16 rule blocks and 16 citation-resolved rules at both revisions above.
- **REPRODUCED — `inspect_evm_interface`:** two same-path IDs matched; both same-byte/same-name path copies changed the ID. Each of the three isolated projected path-field mutations changed the recomputed ID.
- **REPRODUCED — `inspect_rust_binary`:** same repeat/copy result and 3/3 isolated path-field mutations changed the recomputed ID.
- **REPRODUCED — `inspect_artifact`:** same repeat/copy result; changing only outer subject display name/path preserved the ID, while changing only nested inventory Evidence `subject.local_path` changed it.
- **UNVERIFIABLE — landed rule #17:** this seat is artifact-only; no SKILL edit or post-integration measurement was made. These probes are static inspections; no target was executed.

## Source and citation record

Verified the cached package version and source identities directly: `rea.mjs --version` → `6.7.0`; `package.json` SHA-256 `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`; `dist/domain/evidence.js` `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`; `dist/domain/canonicalDigest.js` `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; `dist/application/evm/EvmInterfaceEvidence.js` `0822b952444c30c25adfb6aefb9034fe718f0800eab4131778ff09702835f019`; `dist/application/rust/RustBinaryService.js` `81c34f68609df323124f1c27f2525fc80ae2fcf4dccc02e711b7f477ce189c5d`; `dist/domain/artifactInspection.js` `a2b71a1c75e55d46eecdc63cce5d939832d9391ef6298f202a9f3b990cc5991d`.

Source locations: shared projection `dist/domain/evidence.js:159-183`; canonical hashing `dist/domain/canonicalDigest.js:8-25,60-76`; EVM producer `dist/application/evm/EvmInterfaceEvidence.js:3-10`; Rust path-bearing evidence construction `dist/application/rust/RustBinaryService.js:55-81`; nested artifact-inspection result `dist/domain/artifactInspection.js:111-156`. The rule's corpus citations and line ranges are listed in the proposed text above.
