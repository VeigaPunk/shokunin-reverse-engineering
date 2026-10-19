# CR-6 — Independent verdict and convergence

**Frozen source HEAD:** `0436f4940283072db08e73c0117195847c50d31d`  
**Named work revision:** `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`

This is a verdict on the delivered claims, not a landing receipt. The frozen contract allows one C1 Unknown, one C2 rule-17 draft, and C3 patch text plus a seeded scratch measurement (`claims-frozen.md:16-63`). None of those after-states is integrated in the frozen source tree.

## Baseline and controls

I independently reran the source-derived Command A in `SCORECARD.md:88-124` on both immutable revisions. Both outputs were:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b358d0a1112d31808b9bae3d8ddd1b46875","rule_blocks":16}
```

`python3 .ufo/gates/c1-census-v10.py --json` returned `verdict=PASS`, `frontier_rows=14`, no frontier errors, and no stale/ambiguous/undeclared/unresolved/scope errors. `python3 .ufo/gates/custody-pair/custody-pair.py selftest` ended `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (scratch under `/dev/shm`).

## C1 — one bounded corpus Unknown

**VERIFIED — baseline.** Command A is still 90 files / 90 mapped, with no missing or dangling tokens, at both revisions above. Therefore 91/91 is not an observed after-state.

**REPRODUCED — fourth verb-family candidate, `inspect_go_binary`.** I made four fresh static REA 6.7.0 calls and independently reconstructed the Evidence projection/digest. `/usr/bin/docker` and both copies were 29,327,600 bytes with SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c`. Results:

```text
/usr/bin/docker repeat: ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
/var/tmp/kaidoku-arc3-r12-ex6/same-name/docker: ev_ebf691e2857e55fadff95ee9d09f4e9196c0f4c83adb8c0bcad674000fe1e966
/var/tmp/kaidoku-arc3-r12-ex6/other-name/docker-copy: ev_ee5e4cbb2c8ce91e647562a16b201772506f6f9c2ab1cec6dd578da9fb586d17
repeat_id_equal=true alternate_ids_differ=true same_basename=true all_four_ids_recomputed=true
```

Changing only the outer subject display `name`/`local_path` preserves the ID; substituting the three semantic path fields `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` reproduces the copied-path IDs. The pinned implementation defines the semantic projection in cached REA 6.7.0 `dist/domain/evidence.js:159-183`, canonical hashing in `dist/domain/canonicalDigest.js:8-25,60-76`, and supplies those Go path fields in `dist/application/go/GoBinaryService.js:54-77`. This is bounded to the tested successful operation/version/input/call shape; the target was statically inspected, not executed.

**REPRODUCED — competing pathless observations, not selected as a second C1 move.** Replaying the full-envelope recomputations produced the same `ev_4b9f570e…` for EX-3's `search_bytes` base/base-repeat/byte-identical alternate (`EX-3.md:15-21`; its result is explicitly `complete:false`). EX-7 and CR-2 also reproduce path-stable `analyze_function` records (`EX-7.md:15-21`; `CR-2.md:12-22`). The general `analyze_function` behavior is already recorded at `corpus/QUALITY.md:25` and `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`. CR-3 measures the nested `inventory_artifact` substep, not a distinct public CLI family (`CR-3.md:5-8`). These bounded results are not disproved, but they do not justify bundling several C1 candidates or making a universal path-stability claim.

**DISCREPANCY — historical status prose.** Current map/source state contradicts old status sentences: r7 says its entry/token are unlanded at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:26`, while its token is present at `corpus/README.md:38`; r10 has similar “proposed/not landed” text at `...r10-rust-evidence-id-domain.md:1,24,30`, while its entry and token exist (`corpus/README.md:41,63`); r11 says the 90/90 baseline is pending at `...r11-inspect-artifact-evidence-id-domain.md:23`, while Command A above measures 90/90. Treat those statements as stale, not as technical evidence.

**UNVERIFIABLE — C1 integration.** No R12 corpus entry or map token is landed, so the frozen 91/91 acceptance condition remains unmeasured. EX-2/EX-4/EX-5/EX-6/CR-1/CR-4 converge on the Go result. CN-2 prefers EX-6/CR-1's evidence bundle; CN-4 prefers CR-4's draft. I find no substantive measurement disagreement: integrate exactly one entry at `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`, with one token `2026-10-19-arc3-r12-go-evidence-id-domain` on the Evidence model row (`corpus/README.md:41`). Do not add duplicate Go entries/tokens or also land the pathless alternatives as this C1 move.

## C2 — depth rule #17

**VERIFIED — current count.** The immutable baseline is 16 rules and 16 citation-resolved rules (Command A above).

**CORRECTED — `inspect_artifact` causal scope.** In the stored R11 pair, changing only the nested inventory subject path changes the outer ID but does not reproduce the alternate-call ID; the projection diff also includes `normalized_result.inspection_id` (`claims/c2/EX-16.md:20,27`; `claims/c1/CR-2.md:20`). I confirmed this with a fresh same-byte `/usr/bin/jq` copy while preserving file mode (`0755` on both inputs). All three reported IDs recomputed; base/base-repeat IDs were `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca`, and the alternate ID was `ev_6feb801bac83b41ca1d7c309b47873858ad35537ce4b017f446b848e98dfb9d7`. The nested inventory ID stayed equal across all three.

```text
projection_diff_paths=["$.normalized_result.inspection_id","$.normalized_result.substeps[0].evidence.subject.local_path"]
nested_path_only_id=ev_dfa00affb9f6ff1785e98666b7aa57dfd3801ec0df62582293e423d62d22617e matches_alternate=false
nested_path_plus_inspection_id_matches_alternate=true
```

An initial scratch attempt used `shutil.copyfile`, which left the copy mode at `0644` instead of the source's `0755` and consequently changed additional manifest fields. I excluded that confounded attempt and reran with `shutil.copy2`; the mode/hash control and two-field diff above are from the corrected run. This distinction matters: a path-only mutation can affect the ID without explaining the full live delta.

**REPRODUCED — rule projection, not a landed count.** EX-16's operational rule says to pin the operation/version/call shape, recompute full envelopes, record exact projection fields, and diff remaining fields whenever an isolated mutation does not reproduce the alternate ID (`claims/c2/EX-16.md:6-9`). I inserted that exact bullet only into an in-memory Command A projection against the frozen revision; the six cited ranges were in bounds (r7: 26 lines; r10: 30; r11: 24):

```text
revision=0436f4940283072db08e73c0117195847c50d31d projected_rule_blocks=17 projected_citation_resolved_rules=17
```

This is the strongest draft because it directly covers the R11 confounder and avoids transferring path behavior across operations. The R7/R10 path fields co-vary in their copy controls; rule text should describe them as correlated unless a single-field mutation establishes attribution (`EX-10.md:7-9,47-63`; `EX-16.md:18-20`).

**UNVERIFIABLE — C2 integration.** `SKILL.md` remains at 16/16; there is no actual `rule_blocks=17` after-state. Land one rule with these resolved citations, then rerun Command A at that commit.

## C3 — citation-drift coverage

**VERIFIED — measured gap.** At HEAD, the pointer table has 57 `entries`, 5 `quoted`, SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, matching the frozen pin. It has zero rows for r7 `:5`, r10 `:7`, and r11 `:7`. The live strict probe returned `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; clean does not mean these three lines were graded.

**REPRODUCED — RV-4 scratch patch.** I reran `.ufo/waves/arc3-loop1-round12/claims/c3/RV-4/seeded-measurement.py` against the unmodified probe and exact three proposed rows. Output:

```text
CONTROL: no findings; strict_exit=0
SEEDED arc3r7-evm-recheck: citation_dead entry=arc3r7-evm-recheck; strict_exit=1
SEEDED arc3r10-rust-recheck: citation_dead entry=arc3r10-rust-recheck; strict_exit=1
SEEDED arc3r11-artifact-recheck: citation_dead entry=arc3r11-artifact-recheck; strict_exit=1
SCRATCH: /var/tmp only; no Git writes; live instrument/table/expected unchanged
```

I also re-derived the exact candidate table digest for RV-4's JSON rows appended to the frozen table: 60 entries, 5 quoted, SHA-256 `b3156b0a89c8b2e67ba4ca372e3dd179dab6d5e1ef78312938b028f784374d40`. Its r7 matcher is at `claims/c3/RV-4/proposed-entries.json:3-8`; it pins the expected ID, its closing backtick, and the rest of the required sentence through end-of-line.

**DISCREPANCY — patch precision.** CN-2 prefers PL-4 and CN-4 prefers RV-6; their clean and seeded controls do reproduce, but their r7 matchers leave blind spots. The live gate uses `re.search` for exact rows (`.ufo/gates/citation-drift/citation-drift-probe.py:206-210`). Testing the current r7 line and three mutations gives:

```text
matcher   live  matches-wrong-ID  matches-missing-ID-delimiter  matches-junk-after-ID
PL-4      yes   no                yes                           yes
RV-6      yes   yes               yes                           yes
RV-4      yes   no                no                            no
```

PL-4's matcher stops at the expected hash without requiring its Markdown closing delimiter; RV-6 accepts any syntactically valid `ev_` hash. RV-4 rejects both faults while retaining the same measured three-fault catch. I therefore recommend RV-4's exact rows and matching recomputed table pin, not combining any proposal's rows with another proposal's hash.

**UNVERIFIABLE — C3 integration.** The live table and expected pin were not changed. Re-run the strict probe against the landed table and pin; the scratch pass is not an integrated result.

## Peer convergence, process limits, and write boundary

At the latest inventory, the visible verdict reports are CN-2 and CN-4; no VZ, CN-1/CN-3, or CR-5/CR-7/CR-8 report was present. EX-8 and PL-1 claim reports are also absent. CN-2 and CN-4 agree on the single Go C1 entry and the EX-16-style C2 caveat; they differ on C3 patch choice, addressed above.

**Operational deviation — citation-drift self-test excluded.** I invoked `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` twice during this seat's work; it printed 13/13. On source inspection, `.ufo/gates/citation-drift/citation-drift-probe.py:347-367` shows that each test constructs a temporary Git repository with `git init`, `git add`, and `git commit`; `:464-466` removes the fixture. Because the task's Git constraint is read-only, I exclude that self-test output from accepted evidence. Its temporary fixtures were under `/var/tmp` and removed; no project Git ref/index change is observed. The strict live probe and RV-4 seeded helper are the admissible C3 evidence.

Only this verdict file is written. I left the pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification untouched and changed no corpus, `SKILL.md`, gate, table, expected pin, custody file, `LOG.md`, or peer artifact. The general `AGENTS.md:4` LOG request is outside this wave artifact's explicit write scope.
