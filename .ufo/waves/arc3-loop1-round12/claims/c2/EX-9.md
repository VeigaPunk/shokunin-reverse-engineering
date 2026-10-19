# EX-9 — C2 depth: projection-local Evidence-ID sensitivity

**Deliverable:** draft queue-drain craft rule #17 and citation list. This seat did not edit `SKILL.md`; it is not yet a landed rule. The three corpus citations below are the precedents that earn the rule. All measured outputs and identities reported here were freshly re-derived by EX-9, not copied from a prior seat's measurements.

## Proposed rule #17 (draft)

- **Measure identity-field sensitivity in the exact operation's semantic Evidence projection; do not generalize it from the `ev_` prefix or another verb.** Pin the REA package and request shape. Re-run the same request at the same path, then inspect byte-identical input at a different path while holding its basename fixed. Compare the returned full Evidence records, list every changed leaf that enters the parent semantic projection (including nested Evidence under `normalized_result`), and independently recompute each `ev_` digest. Treat a top-level display-only subject field separately from the same field nested in a hashed result. Say that a field is identity-bearing only for the measured operation, package, and request shape; leave unmeasured operations and releases unknown. Earned by `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-22`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-21`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-19`.

## First-hand derivation

### Frozen baseline

**VERIFIED — Command A at frozen HEAD and the named work commit**, using the recipe at `SCORECARD.md:88-124`, returned:

HEAD `0436f4940283072db08e73c0117195847c50d31d`:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
```

Work `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "5ee13b358d0a1112d31808b9bae3d8ddd1b46875", "rule_blocks": 16}
```

Both measured source revisions baseline to 16/16 citation-resolved rule blocks. This artifact only proposes rule #17; the post-integration `rule_blocks=17` result is **UNVERIFIABLE** until the parent lands the rule and reruns Command A.

### Package and method

`node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs --version` printed `6.7.0`. The package identity and relevant source hashes were re-measured with `sha256sum`:

- `package.json`: `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`
- `dist/domain/evidence.js`: `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`
- `dist/domain/canonicalDigest.js`: `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`
- `dist/application/evm/EvmInterfaceEvidence.js`: `0822b952444c30c25adfb6aefb9034fe718f0800eab4131778ff09702835f019`
- `dist/application/rust/RustBinaryService.js`: `81c34f68609df323124f1c27f2525fc80ae2fcf4dccc02e711b7f477ce189c5d`
- `dist/domain/artifactInspection.js`: `a2b71a1c75e55d46eecdc63cce5d939832d9391ef6298f202a9f3b990cc5991d`
- `dist/application/DirectAnalysis.js`: `188f1d412fe2682d10921282126a4c1b7968a4eb88ed4dca1ee76d247223bed0`

Source references below are relative to the pinned package root `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents`. The common projection selects the subject's `digest`, `format`, and `architecture`, then hashes semantic fields including `parameters`, `raw_result`, `normalized_result`, and `locations` (`dist/domain/evidence.js:159-183`); the digest is SHA-256 over canonical JSON (`dist/domain/canonicalDigest.js:8-25,60-76`). The EVM adapter supplies the input, result, and locations (`dist/application/evm/EvmInterfaceEvidence.js:3-10`); the Rust evidence constructor uses the selected path in its parameters, artifact result, and artifact-path location (`dist/application/rust/RustBinaryService.js:55-81`). Artifact inspection puts the full inventory Evidence object inside its semantic `substeps` (`dist/domain/artifactInspection.js:111-128`), and `DirectAnalysis` puts that inspection result into the outer `normalized_result` (`dist/application/DirectAnalysis.js:293-311`). These source paths explain why the measured path-bearing leaves differ by projection.

### Fresh controlled probes

All nine REA CLI invocations exited `0` with empty stderr. Full raw envelopes are retained in `evidence/{evm-base-1,evm-base-2,evm-copy,rust-base-1,rust-base-2,rust-copy,artifact-base-1,artifact-base-2,artifact-copy}.json`; the EVM input is `evidence/evm-selector.hex`. Scratch and each call's `TMPDIR` were under `/var/tmp/kaidoku-ex9-R6i0j2`.

- **REPRODUCED — `inspect_evm_interface`.** Command shape: `TMPDIR="$ROOT" node "$REA/scripts/rea.mjs" inspect-evm-interface "$PATH" hex --format json --full-output`. The two fixture paths had the same measured SHA-256, `773adfc0e8612a1d38fde458df16ac6a97a7bbb73ff7c28de433797cc7a39797`. Same-path outputs both reported `ev_3e33b8ba100122b35b5ce60d7296bdaacf24c7610f0fa27495ee29d87f47ba5e`; the same-name copy reported `ev_3900cb87debc95214a6dedbe7a1623d110c7cf3abc52d99d3aac1728c95999bb`. Recomputed projection leaves that changed: `parameters.path`, `normalized_result.artifact.path`, `locations[0].path`.
- **REPRODUCED — `inspect_rust_binary`.** Command shape: `TMPDIR="$ROOT" node "$REA/scripts/rea.mjs" inspect-rust-binary "$PATH" --format json --full-output`. `/usr/bin/rustc` and its same-byte copy both measured SHA-256 `c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136`. Same-path outputs both reported `ev_96443401784f756a931b32301b2dc0225f66682b0bc2bb8e389267410d7cf256`; the copy reported `ev_81f8fa1de4528374a30976754d7e7274cb70f85324d719aafe516cba32646cf1`. Recomputed changed leaves: `parameters.path`, `normalized_result.artifact.path`, `locations[0].path`.
- **REPRODUCED — `inspect_artifact`.** Command shape: `TMPDIR="$ROOT" node "$REA/scripts/rea.mjs" inspect-artifact "$PATH" --format json --full-output`. `/usr/bin/jq` and the same-basename copy both measured SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. Same-path outputs both reported `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca`; the copy reported `ev_6ccd8b68b3115c9c6bd38b58d9508be03ed3c4d1966ed888c30452b9babc5fac`. The nested `inventory_artifact` ID stayed `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435`; changed outer-projection leaves were `normalized_result.substeps[0].evidence.subject.local_path` and the derived `normalized_result.inspection_id`.

Independent Python recomputation on the retained envelopes (`evidence/recompute_projection_ids.py`) printed:

```text
inspect_evm_interface: base_match=True repeat_match=True copy_match=True same_path_repeat=True relocated_id_changed=True
  projection_diff=$.locations[0].path,$.normalized_result.artifact.path,$.parameters.path
  top_subject_display_only_ignored=True
inspect_rust_binary: base_match=True repeat_match=True copy_match=True same_path_repeat=True relocated_id_changed=True
  projection_diff=$.locations[0].path,$.normalized_result.artifact.path,$.parameters.path
  top_subject_display_only_ignored=True
inspect_artifact: base_match=True repeat_match=True copy_match=True same_path_repeat=True relocated_id_changed=True
  projection_diff=$.normalized_result.inspection_id,$.normalized_result.substeps[0].evidence.subject.local_path
  top_subject_display_only_ignored=True
```

### Scope and disposition

**VERIFIED** for the pinned REA 6.7.0 package and these three measured call shapes: each `ev_` digest independently recomputed from its returned envelope; each same-path repeat matched; each controlled relocation changed the outer ID. The different projection leaves make the proposed rule operationally useful. This does not establish sensitivity for every Evidence field, operation, package version, or request shape; probes were static and did not execute the analyzed files. The corpus entries in the citation list are citations for the craft rule, not the source of the fresh numerical measurements above.

**UNVERIFIABLE — landed rule count:** no `SKILL.md` change was permitted or made by this seat. Parent integration must co-land the rule and its citations, then rerun Command A to establish `rule_blocks=17` and citation resolution.