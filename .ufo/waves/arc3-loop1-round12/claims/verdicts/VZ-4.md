# VZ-4 — Convergence verdict

**Revision basis:** `HEAD=0436f4940283072db08e73c0117195847c50d31d`; work revision `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`. This is the verdict seat’s only deliverable. I changed no corpus, map, `SKILL.md`, scorecard, log, province, gate, custody, or other peer artifact. All temporary probe data was kept under `/var/tmp` and cleaned.

## Convergence decision

- **C1 — recommend one closure only:** frozen candidate (a), the `inspect_go_binary` Evidence-ID domain, using EX-5’s bounded draft and proposed Evidence-model token `2026-10-19-arc3-r12-inspect-go-binary-evidence-id-domain`. Do not co-land the competing C1 operation drafts as additional closures: the frozen claim says “Pick ONE” (`claims-frozen.md:16-29`).
- **C2 — recommend one synthesized rule #17:** projection-local sensitivity, with EX-16’s “diff residual projected fields” safeguard and EX-10’s pointer-level / correlated-field caution. Proposed wording and citations are below. The measured r11 confounder is material; do not say the nested path alone accounts for the alternate-call ID.
- **C3 — recommend PL-4’s exact three-row citation-drift patch text** and its matching hash `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`. Its clean control and all three seeded faults pass through the real gate logic on scratch. The live instrument is unchanged. If C1’s R12 corpus draft is integrated in the same batch, decide whether to add its new `recheck:` line as a fourth table row and refresh the hash too; PL-4 covers the three already-present r7/r10/r11 lines only.

## C1 — fourth `ev_` family: `inspect_go_binary`

**REPRODUCED — bounded operation result.** I independently invoked the cached `rea-agents@6.7.0` CLI (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs`) four times with `inspect-go-binary <path> --format json --full-output`, with `TMPDIR` under `/var/tmp`: twice on `/usr/bin/docker`, then on same-byte copies at distinct paths. `/usr/bin/docker` and both copies were 29,327,600 bytes and had SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`.

Fresh call IDs and independent recomputation from each full envelope:

```text
base-1: ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd match=true
base-2: ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd match=true
same-name copy: ev_d28d3c06d8a11024695161d363d4761cf9922b50fbbae898d89baa57f01f6eb8 match=true
other-name copy: ev_cfd3dde029f1dc922969aa5fa7834677f33406756c88123f08b4ce6677779025 match=true
same_path_repeat=true
display_only_subject_mutation_preserves_id=true
three_semantic_path_fields_only_reproduce_each_copy_id=true
```

This independently supports EX-5’s mechanism for this exact operation, version, byte identity, and call shape. In the installed package’s `dist/domain/evidence.js:159-183`, subject display fields are excluded while semantic Evidence fields—including `parameters`, `normalized_result`, and `locations`—are projected; `dist/domain/canonicalDigest.js:8-25,58-76` hashes canonical compact JSON with SHA-256. The selected input path appears in the three tested semantic pointers: `parameters.path`, `normalized_result.artifact.path`, and the `artifact-path` location. Substituting that three-field set reproduced each alternate-path ID; changing only outer subject `name`/`local_path` did not. No inspected Docker code was executed.

**VERIFIED — baseline; UNVERIFIABLE — after-state.** I reran Command A from `SCORECARD.md:88-124` against both immutable revisions:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b358d0a1112d31808b9bae3d8ddd1b46875","rule_blocks":16}
```

No corpus entry or map token was landed by this seat. The predicted 91/91 result remains **UNVERIFIABLE** until both are co-landed and Command A is rerun. The other C1 drafts propose distinct candidate-(d) tests (`search_bytes`, `analyze_function`, and nested `inventory_artifact`); I did not independently reprobe those alternatives here. They are not additive to the one selected C1 closure.

## C2 — synthesized rule #17

**REPRODUCED — archived projection measurements.** I ran `node .ufo/waves/arc3-loop1-round12/claims/c2/SC-4/evidence/recompute-projections.mjs`; the source reconstructs the semantic projection and recomputes IDs from retained envelopes. Exact output:

```text
r7: digest_matches=8/8; same_path_repeat=true; same_bytes_altpath_pairs=3/3; display_only_stable=true
r10: digest_matches=4/4; same_path_repeat=true; same_bytes_altpath_copies=2/2; path_fields_only_reproduce_copy=true; display_only_stable=true
r11: digest_matches=4/4; same_path_repeat=true; same_name_same_bytes_altpath_differs=true; outer_display_only_stable=true; nested_inventory_path_changes_outer_id=true
```

I separately recomputed the r11 base/copy IDs and diffed their semantic projections. The copy differs at both `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`. Mutating only the nested path changes the ID, but does **not** reproduce the alternate-call ID. This is why EX-16’s residual-diff caution must be retained; EX-10 correctly warns that co-varying fields are correlated until isolated. The top-level subject display mutation remains distinct from a nested Evidence path.

**Recommended synthesis (draft only):**

> Evidence-ID field sensitivity is local to the measured semantic projection, not a domain-wide property. For each operation, package version, and call shape, derive the projection and compare same-path repeats with byte-identical alternate-path calls. Claim a pointer-level cause only after changing that projection pointer alone and reproducing the observed digest; if projected pointers co-vary or one mutation does not reproduce the copy ID, name the correlation and diff the remaining projected fields. Distinguish outer display metadata from nested Evidence inside `normalized_result`; do not transfer a sensitivity result across operations or versions. (`corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-22`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:19-22`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:19-23`)

All three cited ranges resolve against immutable HEAD. Command A baseline is 16 rule blocks and 16 citation-resolved rules. Injecting the proposed rule and these citations into the parsed craft section gives `projected_rule_blocks=17 projected_citation_resolved_rules=17`. That is a projection check only: no `SKILL.md` change was made, so the landed `17/17` after-state remains **UNVERIFIABLE** until integration and a fresh Command A run.

## C3 — citation-drift pointer-table patch

**VERIFIED — current gap and live baseline.** I independently measured `.ufo/gates/citation-drift/pointer-table.json`: 57 `entries`, 5 `quoted`, SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, matching `expected.json:11-13`. There are zero `file` or `target` references for the three current `recheck:` lines: r7 `:5`, r10 `:7`, r11 `:7`. The strict live command at frozen HEAD returned:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

That clean result does not grade the three absent pointers.

**REPRODUCED — PL-4 exact scratch patch.** I parsed the three JSON objects printed in `claims/c3/PL-4.md:32-69`, appended them to the current table, and serialized using the table’s current `json.dumps(..., indent=2) + "\\n"` convention. This reproduced 60 entries / 5 quoted and the proposed digest `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`. Using the real `citation-drift-probe.py` `run_check` with a scratch table/expected pin and line overlays under `/var/tmp` gave:

```text
CONTROL: findings=0 strict_exit=0
SEEDED pl4-r7-recheck: citation_dead entry=pl4-r7-recheck strict_exit=1
SEEDED pl4-r10-recheck: citation_dead entry=pl4-r10-recheck strict_exit=1
SEEDED pl4-r11-recheck: citation_dead entry=pl4-r11-recheck strict_exit=1
```

The live tool self-test also passed: `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`. This validates the PL-4 patch text against the three current recheck lines, not command execution or REA runtime rechecks. The post-integration live table/hash and strict result remain **UNVERIFIABLE** because the instrument was not edited.

**DISCREPANCY — RV-4 helper’s serialization scope.** I reran `python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py`; its control passed and each of its three seeded faults yielded the expected `citation_dead` / strict exit 1. However, the helper serializes its distinct scratch proposal with `ensure_ascii=False` (`seeded-measurement.py:39`) and computes a matching scratch expected pin from those bytes. For RV-4’s own payload, default serialization hashes to `7f54fc2650fe1c63467a292a9154f005cfe3794c6e5eb095cc55a56d92335078`, while `ensure_ascii=False` hashes to `b3156b0a89c8b2e67ba4ca372e3dd179dab6d5e1ef78312938b028f784374d40`. Thus its seed test exercises the real matcher but does not validate a normal-format on-disk patch hash; use the exact PL-4 text/hash pair or recompute the pin from the actual integrated bytes.

## Cross-check / unresolved fingerprint discrepancy

The prompt’s `c1-census-v10.py` fingerprint prefix `d6b4deaa…` was not reproduced at either supplied revision. The file at HEAD hashes to `6edde060b927af1adeb08b857989af62f54979288335eb12eade99e59039d694`; `git show 5ee13b3:.ufo/gates/c1-census-v10.py | sha256sum` gives `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573`. Its worktree path is clean. The checked-in source does contain the described G21/frontier and unregistered-bullet logic (`.ufo/gates/c1-census-v10.py:95-112,279-290,427-468`), so the mismatch is a fingerprint discrepancy, not evidence that the described feature is absent. `PROVINCE.md:18` records the Kimi pointer at `~/.kimi-code/config.toml:4126`; I did not inspect the operator custody file, so that live pointer was not independently verified.
