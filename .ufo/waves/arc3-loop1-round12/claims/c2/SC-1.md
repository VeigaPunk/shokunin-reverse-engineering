# SC-1 — C2 queue-drain rule #17 draft

**Disposition:** rule #17 proposal only. This seat did not edit `SKILL.md`, corpus entries, the coverage map, or any gate.

## Proposed rule #17

- **Evidence-ID sensitivity is projection-local, not a domain constant.** Derive it for the exact verb, operation, and package version from the full Evidence projection; test a same-byte controlled copy that varies the candidate field and independently recompute the IDs. Record the precise projected field paths. Do not transfer a “path-sensitive” or “display-only” result to another verb or to a same-named field at another nesting depth. The three measured families show why: EVM and Rust include path-bearing request/result/location fields, while `inspect_artifact` excludes top-level display fields but includes a nested inventory path through its result (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,22`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15,21,28`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19`).

## Citation list and boundaries

- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:9,22` — bounds the finding to the measured `inspect-evm-interface` operation and identifies the changed projected fields: `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path`.
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15,21,28` — identifies the Rust projection and independently recomputed same-byte path-copy outcome; scope remains that operation/package and measured input class.
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19` — distinguishes excluded top-level subject display fields from the nested `normalized_result.substeps[0].evidence.subject.local_path` whose mutation changes the outer ID.

These are citations to measured envelope/projection conclusions, not a claim that any one field has universal sensitivity. The proposed rule is scoped to Evidence-ID projection reasoning; it does not imply runtime execution or behavior outside the cited operations and package versions.

## First-hand re-derivation and verdicts

**VERIFIED — queue-drain baseline.** I ran Command A from `SCORECARD.md:88-124` with `REV=$(git rev-parse HEAD)`. `git rev-parse HEAD` returned `0436f4940283072db08e73c0117195847c50d31d`. Exact Command A output:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "0436f4940283072db08e73c0117195847c50d31d", "rule_blocks": 16}
```

The current craft section therefore has 16 rule blocks; this draft is not a landed seventeenth rule.

**REPRODUCED — per-projection sensitivity.** I independently parsed the retained full Evidence envelopes, reconstructed the semantic projection, recomputed SHA-256 Evidence IDs, and applied display-field / nested-path mutations with the read-only script `claims/c2/SC-1/rederive_projection_sensitivity.py`. Run from the lane root as:

```text
python3 .ufo/waves/arc3-loop1-round12/claims/c2/SC-1/rederive_projection_sensitivity.py
```

Exact output:

```text
inspect-evm-interface: recompute_base_matches=True; recompute_copy_matches=True; same_subject_digest=True; observed_ids_differ=True; projection_deltas=['locations[0].path', 'normalized_result.artifact.path', 'parameters.path']
inspect_rust_binary: recompute_base_matches=True; recompute_copy_matches=True; same_subject_digest=True; observed_ids_differ=True; projection_deltas=['locations[0].path', 'normalized_result.artifact.path', 'parameters.path']
inspect_artifact: recompute_base_matches=True; recompute_copy_matches=True; same_subject_digest=True; observed_ids_differ=True; projection_deltas=['normalized_result.inspection_id', 'normalized_result.substeps[0].evidence.subject.local_path']
inspect_rust_binary: top_level_display_mutation_preserves_id=True
inspect_artifact: top_level_display_mutation_preserves_id=True; nested_inventory_path_mutation_changes_id=True
```

The source envelopes read were `...round7/claims/c2/EX-3/evidence/probes/{67-base1,67-copyA}.json`, `...round10/claims/c1/EX-4/evidence/{probe-base1,probe-copyA}.json`, and `...round11/claims/c1/CR-2/evidence/{inspect-artifact-base-1,inspect-artifact-same-name-other-path}.json`. This re-derives the recorded results from full envelopes; it is not a fresh REA invocation.

**DISCREPANCY — stale integration-status text in cited entries.** The measurement passages cited above are supported by the independent recomputation, but some later status statements in those same corpus files conflict with the current source tree: r7 says its corpus file/map token are “not ... landed” at `:26`, while the token is present at `corpus/README.md:38`; r10 retains “proposed” / “not been landed” markers at `:1,24,30`, while the entries are listed at `corpus/README.md:41,63`; r11 says the 90/90 Command A result is pending at `:23`, while the direct Command A output above is 90/90. I did not use those status statements as evidence for the rule and did not edit the out-of-scope corpus or map.

**UNVERIFIABLE — landed rule count.** No SKILL edit was authorized for this seat artifact, so a post-change `rule_blocks=17` result is not claimed. Re-run Command A after any authorized integration.
