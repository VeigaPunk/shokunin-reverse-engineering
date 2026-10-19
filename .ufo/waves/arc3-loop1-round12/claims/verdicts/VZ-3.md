# VZ-3 — Arc3 loop1 round 12 verdict

Measurement revision: `0436f4940283072db08e73c0117195847c50d31d` (work revision `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`). I reviewed the frozen claim set and the delivered C1, C2, and C3 artifacts, including late-arriving C1 `EX-8` and C3 `PL-1` / `RV-1`. This verdict and the two VZ-3 verification scripts under `claims/verdicts/VZ-3/` are the only files this seat wrote, all within its artifact paths; the gates, corpus, coverage map, `SKILL.md`, custody paths, and other tracked files remain untouched. Scratch was confined to `/var/tmp` or `/dev/shm`; no Git mutation was used in the independent measurements below.

## Per-claim verdicts

- **C1 — UNVERIFIABLE as a completed coverage move.** The proposed fourth `ev_` verb-family candidate, `inspect_go_binary`, is independently reproduced below and fits frozen candidate (a). But no corpus entry or coverage-map token is landed, so Command A remains 90/90 and the required 91/91 after-state is not measured. Recommend one Go-family entry only; do not co-land the duplicate drafts.
- **C2 — UNVERIFIABLE as a completed depth move.** `EX-16` is the strongest rule-17 draft: its six R7/R10/R11 citations resolve and the proposed projection is 17/17. No rule is in `SKILL.md`; therefore the actual 17-rule after-state remains unverified. `EX-16` also correctly handles the R11 two-field confounder that weaker drafts omit.
- **C3 — VERIFIED against the frozen scratch-deliverable contract.** The gap is present at HEAD, and the selected three-row citation-drift patch passes on the control while each seeded fault is caught by the unchanged probe. C3 explicitly asks for patch text plus a seeded scratch measurement, not a live instrument edit. The patch remains unapplied; its post-integration live result is not claimed.

These are independent claim verdicts, not a combined score.

## Shared baselines and revision corrections

Command A, rerun from the `SCORECARD.md:88-124` recipe against immutable HEAD:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 90, "mapped": 90, "missing": [], "revision": "0436f4940283072db08e73c0117195847c50d31d", "rule_blocks": 16}
```

The live C1 census gate also passes:

```text
python3 .ufo/gates/c1-census-v10.py --json
verdict=PASS frontier_rows=14 frontier_errors=[] stale=[] ambiguous=[] undeclared=[] unresolved=[] scope_errors=[] g2_ok=true
```

Digest correction: the `d6b4deaa5973d3a29260b0e325620d87a3cc59464771688f97cb1c62d138fc80` key corresponds to the gate at historical commit `9c1d1fef5595b55d65764626249f164e6816473a`, not the current R12 measurement revision. The gate SHA-256 is `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573` at work commit `5ee13b3…` and `6edde060b927af1adeb08b857989af62f54979288335eb12eade99e59039d694` at HEAD `0436f49…`. Current gate still contains G21 and the unregistered-frontier-bullet check (`.ufo/gates/c1-census-v10.py:216-227,427-470`); the live pin pointer is recorded at `SCORECARD.md:1833-1839`. Do not treat the historical digest as the current-file hash.

The cited REA projection verifier was rerun from the VZ-3 evidence directory:

```text
r7 inspect_evm_interface: envelope_ids=8/8, same_path_repeat=true, 6.7_path_controls=2, 6.4_path_control=true, bytes/decoded/functions_equal=true, semantic_path_fields_changed=3
r10 inspect_rust_binary: envelope_ids=4/4, same_path_repeat=true, byte-identical_path_controls=2, artifact_digest_equal=true, semantic_path_fields_changed=3
r11 inspect_artifact: envelope_ids=4/4, same_path_repeat=true, byte-identical_path_controls=2, nested_inventory_digest_equal=true, outer_display_only_same_id=true, nested_path_only_changes_outer_id=true, alternate_id_reproduced_after_inspection_id_update=true
```

This is the key C2 qualification: R11's base-to-alternate `normalized_result` diff contains exactly `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`. Recomputing after changing only the nested path changes the outer ID but does **not** reproduce the alternate ID; updating both correlated fields does reproduce it. This was re-derived directly from the retained R11 envelopes at HEAD. It is evidence about this projection only, not a universal rule for `ev_` IDs.

## C1 — selected coverage candidate

The frozen Unknown allows a fourth `ev_` verb family (claims-frozen `:16-29`). The C1 drafts divide between that candidate and other projection questions; multiple drafts independently propose `inspect_go_binary`. I select the Go family because it directly closes frozen candidate (a), and freshly reran CR-1's complete evidence recipe rather than relying on its reported numbers. `EX-8` is a duplicate Go-family draft, not a second entry to land. Use a single bounded Go entry with a single map token; CR-1 contains the independently rechecked evidence and full draft (`claims/c1/CR-1.md:5-26`, `claims/c1/CR-1/evidence/recheck.sh:1-22`).

Command, run from the lane root:

```text
bash .ufo/waves/arc3-loop1-round12/claims/c1/CR-1/evidence/recheck.sh
```

The script made byte-identical `/var/tmp` copies of `/usr/bin/docker`, made two fresh same-path calls and one call per copy through the cached REA 6.7.0 `inspect-go-binary` CLI, and independently recomputed IDs. Exact recheck results:

```text
/usr/bin/docker and both copies: sha256=70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9
all three: 29327600 bytes, mode=755
base1 ID = base2 ID = ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
copyA ID = ev_ef525acb4244c7da5611e805b2121d56305ec4c35c2d14f08cce6533084bff0c
copyB ID = ev_854ee6fcbac6c57c8b57767eda551e224d5fcff939f62500b6ebb55d8664727f
same_path_repeat.ids_equal=true
same_path_repeat.semantic_projection_equal=true
byte_identity.all_three_inputs_match=true
display_only_subject_mutation.equals_base_id=true
substituted_semantic_path_fields: parameters.path, normalized_result.artifact.path, locations[0].path
verification=PASS
```

All four observed IDs matched the independent projection reconstruction. Updating those three included path fields alone reproduced each copy ID. This is static Go metadata inspection; it did not execute `/usr/bin/docker`. The source-level account in the draft identifies those fields in `GoBinaryService.js` and the Go report schema. The scratch paths were removed at script exit.

**Limit:** this verifies the named verb/version/input shape, not all Go artifacts or all REA operations. No C1 integration occurred: the live source map still has 90 knowledge files mapped 90/90 with no missing or dangling tokens, so the frozen 90→91 after-count remains **UNVERIFIABLE**.

## C2 — rule-17 adjudication

All rule drafts are projections only. I recommend `EX-16` (`claims/c2/EX-16.md:6-8,18-22,30-34`): it requires testing field sensitivity per operation and, crucially, instructs the reader to diff remaining projection fields when a one-field mutation fails to reproduce the alternate ID. That matches R11's independently re-derived `inspection_id` confounder. `EX-13`'s exact-match attribution criterion does not characterize the whole R11 alternate-ID delta; `EX-15` describes the nested path effect but omits the correlated `inspection_id` field. Keep that distinction in the integration wording.

A read-only equivalent of the VZ-3 citation projection checked the six R7/R10/R11 ranges in the EX-16 rule against immutable HEAD, the coverage map, and actual source line counts:

```json
{"EX-16_all_refs_in_bounds_and_mapped": true, "EX-16_citation_resolved_rules": 17, "EX-16_projected_rule_blocks": 17, "EX-16_proposal_refs": 6, "baseline_citation_resolved_rules": 16, "baseline_knowledge_files": 90, "baseline_rule_blocks": 16, "dangling": [], "mapped": 90, "missing": [], "ref_ranges": [{"file":"2026-10-19-arc3-r7-evm-evidence-id-domain.md","start":11,"end":11,"source_lines":26,"in_bounds":true},{"file":"2026-10-19-arc3-r7-evm-evidence-id-domain.md","start":17,"end":22,"source_lines":26,"in_bounds":true},{"file":"2026-10-19-arc3-r10-rust-evidence-id-domain.md","start":13,"end":15,"source_lines":30,"in_bounds":true},{"file":"2026-10-19-arc3-r10-rust-evidence-id-domain.md","start":19,"end":22,"source_lines":30,"in_bounds":true},{"file":"2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md","start":11,"end":15,"source_lines":24,"in_bounds":true},{"file":"2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md","start":19,"end":23,"source_lines":24,"in_bounds":true}], "revision":"0436f4940283072db08e73c0117195847c50d31d"}
```

The 17/17 value is a draft projection only. No `SKILL.md` rule was landed, so post-integration `rule_blocks=17` is **UNVERIFIABLE**. The current Command A result remains 16 blocks / 16 resolved rules.

## C3 — selected operability candidate

The live citation-drift table at HEAD has 57 `entries`, 5 `quoted` rows, and 8 exemptions. Its Git-object SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` matches `expected.json`. Each named `recheck:` field exists once and has zero existing table rows: R7 at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, R10 at `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`, and R11 at `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`. The unchanged strict probe returns `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; that clean result is not coverage of fields the table does not name.

The peer proposals converge on this same gap, not a dozen separate moves. I recommend the three exact rows in `claims/c3/RV-4/proposed-entries.json`: IDs `arc3r7-evm-recheck`, `arc3r10-rust-recheck`, `arc3r11-artifact-recheck`. I reran its scratch measurement with the unchanged gate and a read-only Git-show overlay:

```text
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py
CONTROL: no findings; strict_exit=0
SEEDED arc3r7-evm-recheck: citation_dead entry=arc3r7-evm-recheck; strict_exit=1
SEEDED arc3r10-rust-recheck: citation_dead entry=arc3r10-rust-recheck; strict_exit=1
SEEDED arc3r11-artifact-recheck: citation_dead entry=arc3r11-artifact-recheck; strict_exit=1
SCRATCH: /var/tmp only; no Git writes; live instrument/table/expected unchanged
```

I independently serialized the exact RV-4 rows over the immutable HEAD table using the helper's JSON formatting. The candidate is 60 `entries` / 5 `quoted`, SHA-256 `b3156b0a89c8b2e67ba4ca372e3dd179dab6d5e1ef78312938b028f784374d40`. **CORRECTED:** `RV-4.md:63-67` reports `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`, which does not hash the exact `proposed-entries.json` payload. The helper computes and pins the table it actually tests in scratch, so its clean/fault results reproduce; integration must recompute `expected.json` from the final table bytes rather than copy RV-4's printed digest.

The custody alternative (candidate b) is not a current gap: the existing implementation counts distinct resolved paths (`.ufo/gates/custody-pair/custody-pair.py:637-651`) and has duplicate-stanza rejection plus a distinct-five control (`:1157-1193`). I reran `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch <fresh /dev/shm dir>`; result: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`. No custody path was written. Thus the citation-drift recheck gap is the stronger live C3 candidate.

**Process qualification:** the citation-drift probe's own self-test constructs temporary Git repositories and runs `git init`, `git add`, and `git commit` (`.ufo/gates/citation-drift/citation-drift-probe.py:347-367`). Those reported 13/13 self-test runs are not counted here as compliant evidence under the frozen Git-read-only rule; PL-2 explicitly discloses this deviation (`claims/c3/PL-2.md:29`). The selected RV-4 scratch harness avoids that self-test path and performed no Git writes. The patch only grades text on the three `recheck:` lines; it does not execute REA or establish that referenced caches/files remain live.

## Integration boundary

- C1: co-land one Go-family corpus entry and one map token; rerun Command A at that commit to establish 91/91.
- C2: land the EX-16 rule with the R11 two-field caveat; rerun Command A to establish the actual 17-rule result.
- C3: if integrating the selected RV-4 rows, recalculate the table digest from final bytes, update the expected pin in the same change, then rerun the strict probe. The scratch deliverable already verifies clean-control and fault detection, but no live table change was made here.

No commit was made.
