# CN-2 — per-item reconciliation and verdict

**Wave:** `arc3-loop1-round12` · **Seat:** verdicts/convergence · **Inventory snapshot:** 2026-10-19 16:53:13 -03:00  
**Repository HEAD:** `0436f4940283072db08e73c0117195847c50d31d` · **Named work revision:** `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`

This is an evidence reconciliation, not a round-wide pass or a landing receipt. `VERIFIED` / `REPRODUCED` below describe the stated observations only. The corpus entries, rule, and instrument patch remain drafts until an integrator lands them and measures the resulting revision.

## Inventory and frozen baseline

At the snapshot, the 36 owned C1/C2/C3 claim reports were not all present: C1 had 11/12 (EX-8 unavailable), C2 12/12, and C3 11/12 (PL-1 unavailable), for 34 top-level reports. The two additional files under claims were nested C1 draft attachments, not extra seat reports. No peer verdict file was present; the other 11 verdict-seat reports (VZ-1..4, CN-1/CN-3/CN-4, CR-5..8) are unavailable at this snapshot. This is a bounded inventory, not a request to wait for late seats. Sources: `.ufo/waves/arc3-loop1-round12/claims-frozen.md:65-70`; `claims/c1/EX-8.md` and `claims/c3/PL-1.md` absent from the scan; `claims/verdicts/` had no report at inventory time.

The frozen source-derived Command A recipe (`SCORECARD.md:88-124`) was independently run on both immutable revisions. Exact results:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b358d0a1112d31808b9bae3d8ddd1b46875","rule_blocks":16}
```

These are pre-integration baselines, not before/after wins. Also verified: `python3 .ufo/gates/c1-census-v10.py --quiet` → `G21 14 rows, no scope/frontier errors; VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp` → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`.

## C1 — coverage: select one fourth-family `ev_` Unknown

**Verdict: RECOMMEND candidate (a), one bounded `inspect_go_binary` entry. Evidence is reproduced; corpus/map landing and 91/91 remain unverified.** Frozen C1 requires one Unknown, not a bundle of all the proposed candidates (`claims-frozen.md:16-29`).

### Convergent Go-binary result

EX-2, EX-4, EX-5, EX-6, CR-1 and CR-4 independently target the same `inspect_go_binary` / REA 6.7.0 finding on `/usr/bin/docker`. They agree on the same-path ID and formula, same-byte alternate paths producing different IDs, and the same three semantic path fields. CN-2 freshly repeated the static inspection at the original path and at two byte-identical `/var/tmp` paths. The bounded observations were:

```text
input: /usr/bin/docker; sha256=70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9; bytes=29327600
same-path repeat IDs: ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd / ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
byte-identical alternate-path IDs: ev_12687e016e177e587c9764087d73437494f7b2eda176255d894f0dc5dda12c3e / ev_c489735df7525cce822b13945aa26db4c6bed9388c67648a632a21ef848825ba
```

The package is 6.7.0 (`package.json:4`). Its projection and canonical digest are implemented at `dist/domain/evidence.js:159-183` and `dist/domain/canonicalDigest.js:8-25`; for this operation, `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` carry the path into the hashed projection. Independent recomputation from the four returned envelopes matched their IDs; substituting those three fields reproduces the alternate IDs, while changing top-level subject display `name`/`local_path` does not. See the matching retained first-hand records at `claims/c1/EX-6.md:11-24`, `claims/c1/EX-6/evidence/identity.txt:2-10`, `claims/c1/EX-6/evidence/probe-base1.json:1`, `probe-base2.json:1`, `probe-same-name-copy.json:1`, and `probe-other-name-copy.json:1`; corroborating claim derivations at `claims/c1/EX-2.md:17-21`, `EX-4.md:13-23`, `EX-5.md:23-26`, `CR-1.md:20-26`, and `CR-4.md:21-27`. Targets were inspected statically, not executed.

**Convergence decision:** retain exactly one draft entry, using the EX-6/CR-1 evidence bundle as the clearest canonical bundle; do not land six duplicate entries or map tokens for one operation. Recommended destination: `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`. Recommended single map token: `2026-10-19-arc3-r12-go-evidence-id-domain` on the Evidence model row (`corpus/README.md:41`), where the three prior operation-specific formula entries are indexed. Some drafts suggest a Go-binary row instead; this is an Evidence-ID-domain result, so the Evidence-model destination is the better semantic fit. Do not also add a second token beside the general Go metadata entry (`corpus/README.md:147`).

### Other C1 proposals and boundary

The pathless-projection candidate (d) also has reproducible, operation-bounded evidence: EX-1/EX-7/CR-2 tested `analyze_function`, EX-3 tested `search_bytes`, and CR-3 tested the nested `inventory_artifact` record. For example, EX-3 reports the same `ev_4b9f570e…` on two `/usr/bin/jq` calls and a byte-identical alternate path (`claims/c1/EX-3.md:15-21`); CR-3 reports nested `inventory_artifact` ID `ev_bd06f056…` stable across four inspected paths, while the parent `inspect_artifact` ID changes (`claims/c1/CR-3.md:11-17,23-25`). These are valid bounded measurements, not disproved claims. They are **not selected** because C1 allows one Unknown and the fourth-family Go result has the clearest convergence. Do not conflate the several `analyze_function` variants or turn any of these results into a universal path-stability rule. EX-8 is unavailable.

Several existing corpus status sentences are stale and must be corrected in a later authorized corpus pass; do not use them to adjudicate the technical evidence: r7 says its entry/token remain unlanded at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:26` although the token is listed at `corpus/README.md:38`; r10 still calls its entry/token proposed at `...r10-rust-evidence-id-domain.md:1,24,30` although the token is listed at `corpus/README.md:41,63`; r11 says the 90/90 Command A result is pending at `...r11-inspect-artifact-evidence-id-domain.md:23`, while the measured baseline above is 90/90. This is correction debt only; CN-2 did not edit those out-of-scope files.

**Acceptance boundary:** 91 knowledge files / 91 mapped is a prediction only if exactly one new entry and its token co-land. No post-integration count was measured; it remains `UNVERIFIABLE`.

## C2 — depth: converge on one projection-local rule #17

**Verdict: RECOMMEND one rule #17, incorporating EX-10/EX-16's isolation caveat. Draft and citation preflight are supported; landing is unverified.** All twelve C2 claim seats are present, and their proposals converge on the per-operation semantic-projection principle. The best final text must be more precise than a bare “path-sensitive” label:

> **Derive Evidence-ID field sensitivity at the exact operation's semantic-projection boundary, not from a field name or the `ev_` prefix.** Pin the package version and call shape; inspect the producer and complete projection; recompute IDs from full envelopes; compare a same-path repeat with a controlled same-byte alternate path; and isolate a candidate pointer when attributing causality. Record the exact changed projection paths, including nested `normalized_result` values, and use excluded top-level display fields as a negative control. If a one-field mutation changes an ID but does not reproduce the alternate-call ID, report the other projection differences instead of attributing the whole delta to that field. Bound each conclusion to the measured operation, version, input and call shape; leave untested cases unknown.

This adjudicates the meaningful disagreement. For the EVM and Rust alternate-path envelopes, `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` co-vary; unless the exact one-pointer controls are reported, describe those as correlated changes, not sole causes (`claims/c2/EX-10.md:7-9,47-63`; `claims/c2/EX-16.md:18-20`). For `inspect_artifact`, the outer projection differs at both `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`. Mutating only the nested path changes the outer ID but does **not** reproduce the full alternate-call ID (`claims/c2/EX-16.md:20,27`; independently corroborated by `claims/c2/EX-10.md:42-50` and `SC-2.md:19`). This is why the rule must distinguish field contribution from explaining the entire observed ID delta.

Proposed citations should point to the measured passages, e.g. r7 `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-22`, r10 `...r10-rust-evidence-id-domain.md:13-21`, and r11 `...r11-inspect-artifact-evidence-id-domain.md:17-21`—not the stale “draft/not landed” status sentences noted above. EX-15's in-memory Command A-style citation preflight projects 17 resolved rules (`claims/c2/EX-15.md:111-121`), and multiple seats report the same baseline 16/16; neither is a live landed result. The measured baseline remains `rule_blocks=16`, `citation_resolved_rules=16` at both revisions above. `rule_blocks=17` and 17 citation-resolved rules are **UNVERIFIABLE** until the text is integrated and Command A runs on that commit.

## C3 — operability: choose one citation-drift table patch

**Verdict: RECOMMEND PL-4's three exact rows as the canonical patch text. Scratch clean and seeded-fault behavior are reproduced; the gate/table/digest remain unlanded.** At frozen HEAD, `.ufo/gates/citation-drift/pointer-table.json` has 57 `entries`, 5 `quoted`, 8 `exempt`, SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, pinned by `expected.json:11-13`. The table has no row for any of the three source recheck lines: r7 `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, r10 `...r10-rust-evidence-id-domain.md:7`, and r11 `...r11-inspect-artifact-evidence-id-domain.md:7`. The live strict baseline is `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`: clean is not evidence that those unregistered lines were graded (`claims/c3/PL-4.md:7-30`; also PL-2/PL-3 and RV-1..RV-8).

The patch reports propose different row kinds, line pinning, regex scopes, and serialized bytes; their expected hashes are not interchangeable (examples: PL-2 `78d86b55…`, PL-3 `075db60f…`, RV-2 `8a97f595…`, PL-4 `7470c3f6…`). I independently rebuilt the exact PL-4 three-row table from the current baseline, confirmed current-table JSON round-trips byte-identically, and re-derived candidate SHA-256 `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2` (60 entries + 5 quoted). Its rows test the existing recheck lines at the exact pinned line numbers, including r7's command/expected ID, r10's command source and recomputation helper, and r11's identity/calls/recompute plus `/tmp` exclusion. The unchanged real probe's scratch control was clean. Replacing each targeted scratch line with `recheck: SEEDED-FAULT` yielded the matching `citation_dead` entry and strict exit 1; cumulative findings were 1, then 2, then 3. Exact candidate and retained output are in `claims/c3/PL-4.md:34-69,71-98`.

**Integration instruction:** use PL-4's exact row bytes and its matching digest together; do not combine rows from another proposal with the `7470…` hash. This extends text-drift grading only. It does not execute the three recheck recipes or prove their files/caches are live. PL-1 is unavailable. The alternative custody-pair stanza-count debt is not the selected gap; the bounded self-test result above reports 28/28 passing, so no duplicate custody patch is recommended.

**Acceptance boundary:** the proposed table and `expected.json` pin are scratch-only. No post-landing citation-drift run or integrated table digest exists; C3 improvement remains **UNVERIFIABLE as landed**.

## Process limits and final scope check

No corpus, `SKILL.md`, gate, custody file, scorecard, log, province, or other seat's artifact was changed. Only this CN-2 verdict artifact is written by this seat. Static REA calls inspected targets; none were executed. Probe copies and scratch were under `/var/tmp`, and no `/tmp` scratch was used.

One citation-drift `--selftest` run under `TMPDIR=/var/tmp` printed `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`, but the self-test constructs temporary Git repositories and runs `git init/add/commit` (disclosed at `claims/c1/PL-2.md:29,31,114-118`). I exclude that result as policy-inadmissible under the Git-read-only constraint; the independent live baseline and scratch `run_check`/seeded-fault path above are the relevant evidence. No project repository Git refs/index were changed. The pre-existing worktree modification `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched.
