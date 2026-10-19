# SC-2 — C2 depth: rule #17 draft and re-derivation

**Disposition:** proposed rule only; this seat did not edit `SKILL.md`, the corpus, gates, or other tracked files. The rule is earned by the three verb-family projection checks below and is not claimed as landed.

## Rule #17 draft

- **Measure Evidence-ID field sensitivity at the verb's pinned semantic-projection boundary; do not infer it from a field name or another verb.** For the exact operation and package version, inspect the operation's producer and the ID projection/canonicalizer. Compare complete envelopes from a same-path repeat and a same-byte alternate-path input with all other call options held constant; independently recompute each ID and list every changed projection path, including derived and nested values. Mutate top-level display-only fields as a negative control. Treat a value omitted by the outer projection as potentially identity-bearing when the verb embeds it inside a hashed nested result; distinguish the outer ID from any nested Evidence ID. State sensitivity only for the tested verb, package version, input identity, and call shape. Do not promote it to a universal REA rule. (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9-23`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-21`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-23`)

The draft targets the measured path-sensitivity differences: `inspect-evm-interface` and `inspect_rust_binary` carry paths at multiple direct projection paths; `inspect_artifact` carries the inventory Evidence inside `normalized_result`, so a nested `subject.local_path` and derived `inspection_id` affect the outer ID even though the outer subject's display fields are excluded. These are per-verb observations, not evidence that every path/version/scope field or every REA operation behaves alike.

## First-hand re-derivation

I read the retained complete envelopes and reimplemented the version-specific projection and canonical SHA-256 derivation in `claims/c2/SC-2/evidence/rederive-projections.mjs`. The implementation follows the installed package source, not the old seat recomputation scripts: REA 6.4.0's projection is `evidence.js:129-152`; REA 6.7.0's is `evidence.js:159-183`; canonical emission/hash is `canonicalDigest.js:8-25,27-83`. The replay is read-only and invokes no REA analysis.

Command: `node .ufo/waves/arc3-loop1-round12/claims/c2/SC-2/evidence/rederive-projections.mjs`

- **inspect-evm-interface — REPRODUCED.** Exact output fields: `envelope_count: 8`, `recomputed_id_matches: 8`; `v6_4_same_bytes_path_ids_differ: true`; `v6_7_same_path_repeat_stable: true`; `v6_7_same_bytes_copy_ids_differ: true`; `v6_7_projection_diff_paths: ["$.locations[0].path", "$.normalized_result.artifact.path", "$.parameters.path"]`; `v6_7_projection_differences_are_paths: true`; `v6_7_copy_rebuilt_from_base_projection: true`; `top_level_display_mutation_stable: true`. Direct producer evidence: 6.4.0 `EvmInterfaceService.js:55-65`; 6.7.0 `EvmInterfaceEvidence.js:3-10`. The complete eight re-derived IDs are in the command output; no prior seat's printed ID was used as the recomputation result.
- **inspect_rust_binary — REPRODUCED.** Exact output fields: `envelope_count: 4`, `recomputed_id_matches: 4`; `same_path_repeat_stable: true`; `same_byte_copy_ids_differ: true`; `projection_diff_paths: ["$.locations[0].path", "$.normalized_result.artifact.path", "$.parameters.path"]`; `projection_differences_are_paths: true`; `copy_rebuilt_from_base_projection: true`; `top_level_display_mutation_stable: true`. Producer: REA 6.7.0 `RustBinaryService.js:55-81` constructs the artifact path, parameters, and `artifact-path` location in the Evidence input.
- **inspect_artifact — REPRODUCED.** Exact output fields: `envelope_count: 4`, `recomputed_id_matches: 4`; `same_path_repeat_stable: true`; `same_name_same_bytes_other_path_changes_outer_id: true`; `projection_diff_paths: ["$.normalized_result.inspection_id", "$.normalized_result.substeps[0].evidence.subject.local_path"]`; `nested_inventory_id_count: 1`; `nested_local_path_change_changes_outer_id: true`; `top_level_display_mutation_stable: true`. Producer: REA 6.7.0 `artifactInspection.js:111-156,164-169` embeds the full `inventoryEvidence` under `normalized_result.substeps[0].evidence`, then derives `inspection_id`; outer Evidence hashing uses `evidence.js:159-183`.

The package identities/source hashes were freshly checked with Node `package.json` reads and `sha256sum`-equivalent hashing:

- REA 6.4.0 `package.json`: `1c6244e5689db5354fffc0e92f4ee0e0237c3a6d645de564ade2d8375fa570f9`; `dist/domain/evidence.js`: `690dc0355ce8dd64417b8ebb1ebd4a06c6b5ece648eeb7caf6978638b880de39`; `dist/domain/canonicalDigest.js`: `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; `dist/application/evm/EvmInterfaceService.js`: `23c5297efd17b002de67970d93e56a2319578848c5c3c04155529147b1e2b277`.
- REA 6.7.0 `package.json`: `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`; `dist/domain/evidence.js`: `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`; `dist/domain/canonicalDigest.js`: `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; `dist/application/evm/EvmInterfaceEvidence.js`: `0822b952444c30c25adfb6aefb9034fe718f0800eab4131778ff09702835f019`; `dist/application/rust/RustBinaryService.js`: `81c34f68609df323124f1c27f2525fc80ae2fcf4dccc02e711b7f477ce189c5d`; `dist/domain/artifactInspection.js`: `a2b71a1c75e55d46eecdc63cce5d939832d9391ef6298f202a9f3b990cc5991d`.

## Command-A baseline and citation check

**VERIFIED — frozen-HEAD baseline, not a post-landing result.** I reran the `SCORECARD.md:88-124` source-derived Command A against `git rev-parse HEAD`, which returned `0436f4940283072db08e73c0117195847c50d31d`. Exact JSON:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
```

The three proposed corpus citation ranges were checked against `git show <HEAD>:<path>` and Command A's `corpus/knowledge/…md(:line[-line])` pattern. Exact output:

```text
corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9-23 lines=26 in_bounds=True command_A_pattern=True
corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-21 lines=30 in_bounds=True command_A_pattern=True
corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-23 lines=24 in_bounds=True command_A_pattern=True
citation_refs=3 all_valid=True revision=0436f4940283072db08e73c0117195847c50d31d
```

**UNVERIFIABLE — post-draft acceptance.** No post-landing `rule_blocks=17`/17-resolved measurement is claimed: this is a seat draft and `SKILL.md` remains untouched. The parent must integrate the accepted text and rerun Command A on the landing revision before calling rule #17 landed.
