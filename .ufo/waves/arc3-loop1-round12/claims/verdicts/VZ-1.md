# VZ-1 — independent reconciliation, arc3-loop1-round12

## Disposition

- **C1 — RECOMMEND one bounded fourth-family Unknown:** `inspect_go_binary` in `rea-agents@6.7.0`. The stored records and projection mutation controls reproduce; do not also land the path-free candidate in this C1 slot. The 91/91 after-state is **UNVERIFIABLE** until an entry and one map token are co-landed and Command A is rerun.
- **C2 — RECOMMEND one rule #17 using EX-16's causal-isolation caveat.** Its cited measurement ranges pass Command A's citation pattern and bounds; actual `rule_blocks=17` remains **UNVERIFIABLE** until integration.
- **C3 — RECOMMEND PL-4's exact three rows and its matching table digest.** I independently reproduced the clean scratch control and all three seeded failures. Integration and the resulting live gate identity remain **UNVERIFIABLE**.

These recommendations choose one candidate per frozen claim; they are not a landing receipt or a round-wide pass.

## Frozen baselines and controls

Revision checks: `HEAD=0436f4940283072db08e73c0117195847c50d31d`; named work revision `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`.

I reran SCORECARD Command A (`SCORECARD.md:88-124`) against both immutable Git revisions. Exact results:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"5ee13b358d0a1112d31808b9bae3d8ddd1b46875","rule_blocks":16}
```

These are baseline measurements only. No corpus, map, `SKILL.md`, gate, table, expected pin, custody path, `LOG.md`, or other seat artifact was edited. All analysis inputs below are retained evidence; no new REA analysis target was run or executed.

## C1 — one Unknown selected

**VERIFIED / REPRODUCED — `inspect_go_binary` in REA 6.7.0.** I recursively loaded every retained JSON record under `.ufo/waves/arc3-loop1-round12/claims/c1/`, selected `operation == "inspect_go_binary"`, rebuilt the projection, and called the cached package's `digestCanonicalValue` from `dist/domain/canonicalDigest.js`. All **27/27** stored IDs matched. The seven evidence bundles—EX-2, EX-4, EX-5, EX-6, EX-8, CR-1, and CR-4—each also had a stable `/usr/bin/docker` repeat; changing only `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` in memory reproduced every alternate-path ID; changing only top-level subject display `name`/`local_path` did not change the ID.

The controlled target identity was `/usr/bin/docker`, 29,327,600 bytes, SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`. The repeated original-path ID is `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`; byte-identical copies at different paths produced different IDs. For example, CR-4's two copies yielded `ev_01c99c5db77c3546a879e7cf570f9d8b0f79950f174b48b2b9d1b87d0c08ff6d` and `ev_4a5922f1f6de19f0d2156e6c22239ae5ff35a6fbf52fd0040dddbdc4dc969e67` (`claims/c1/CR-4.md:21-24`). The measured package projection is `ev_` plus SHA-256 of canonical semantic Evidence; it excludes outer display name/path but includes the three operation-specific path fields (`rea-agents/dist/domain/evidence.js:159-183`; `dist/domain/canonicalDigest.js:8-25,60-76`; Go producer: `dist/application/go/GoBinaryService.js:54-77`). These are bounded successful static inspections, not runtime, compiler-authenticity, or dependency-absence claims.

**Selection and peer reconciliation.** CN-2 and CN-4 both recommend the same fourth-family result and one Evidence-model map token. I recommend one corpus entry, using CR-4 as the integration draft and EX-6 as the closest corroborating bundle; do not land duplicate Go entries from the seven convergent bundles. Proposed destination: `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`. Proposed token: `2026-10-19-arc3-r12-go-evidence-id-domain` on the Evidence-model row (`corpus/README.md:41`), not a second token on the Go metadata row.

**VERIFIED / NOT SELECTED — path-free `search_bytes` is a genuine competing candidate, not a disproved claim.** I independently recomputed EX-3's three full envelopes with the package canonical digest. All three report/recompute to `ev_4b9f570ed7503ebe3946a9458e9ae61b9fce0b3ca6605ae88b1d836da096d754`; the same-byte alternate at `/var/tmp/kaidoku-arc3-r12-ex3/jq-copy` has the same target digest (`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) as `/usr/bin/jq`, and all three semantic projections compare equal. The outer display path/name changes, but recursive scans find no path-key in the semantic projection or its raw/normalized result. Scope is exactly `search_bytes`, REA 6.7.0, query `48 83 ec`, limit 5 and the captured provider/profile. Its result is page-limited (`complete:false`); it is not a full-search claim. EX-1/EX-7/CR-2 provide other `analyze_function` variants, while CR-3's `inventory_artifact` is nested inside public `inspect_artifact`, not an independent CLI command (`claims/c1/CR-3.md:5-8`). I choose Go because frozen C1 allows one Unknown and the fourth-family coverage has the strongest cross-seat convergence; candidate (d) remains open. Do not claim both Unknowns closed.

**UNVERIFIABLE — C1 after-state.** The actual source remains at 90/90. `91/91` is only the prediction if exactly one entry and its matching token land together.

## C2 — rule #17

**REPRODUCED — recommend EX-16's projection-local rule with its isolation language.** The useful rule is: pin operation, package version, call shape and bytes; inspect the producer and full semantic projection; recompute IDs from full envelopes; compare same-path repeats with controlled same-byte alternate-path calls; name exact changed projection pointers, including nested `normalized_result`; use outer display fields as a negative control; and isolate a field or field set before attributing causality. If a single-field mutation changes the ID but does not reproduce the alternate-call ID, diff the remaining projection instead of attributing the entire delta to that field. Bound every result to the measured operation/version/input/call shape.

I independently re-derived R7 EVM and R10 Rust with the package canonical digest: all three selected envelopes per family matched; same-path IDs matched; the alternate-path IDs differed; and the three-field path substitution reproduced the copy ID. The three fields co-vary in each live copy pair, so that demonstrates a field-set explanation, not sole causality for each field.

For R11 `inspect_artifact`, four-envelope recomputation is also in the retained run, and I independently checked the key confounder using the base/repeat/same-name-copy envelopes. Base and copy IDs are `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca` and `ev_38cc43f4175331e53c7cd1bcefea9736028dc596bf84315d75b3a86505c9613c`. Mutating only nested `normalized_result.substeps[0].evidence.subject.local_path` recomputes to `ev_8b031a55bb0ee2716710e3a19e87d39bd43363f55e69415696e32c91ec03bea9`, **not** the live copy ID. Mutating that nested path and `normalized_result.inspection_id` together reproduces the copy ID. Top-level display-only mutation is ignored. This corrects drafts that imply the nested path alone explains the whole wrapper delta; EX-16 records the distinction (`claims/c2/EX-16.md:18-27`).

I checked EX-16's six corpus citation references with Command A's exact citation regex and immutable HEAD line counts: r7 file has 26 lines, r10 30, r11 24; all six ranges resolve and are in bounds. Appending the candidate bullet in memory projects 17 rule blocks, but actual HEAD remains 16 blocks / 16 resolved. **UNVERIFIABLE — landed 17/17.**

## C3 — citation-drift coverage

**VERIFIED — live gap.** At HEAD, `pointer-table.json` has 57 `entries`, 5 `quoted`, 8 `exempt`; raw SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` matches `expected.json:11-13`. No row grades the three current `recheck:` fields: r7 `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`, r10 `...r10-rust-evidence-id-domain.md:7`, r11 `...r11-inspect-artifact-evidence-id-domain.md:7`. The live strict command returns `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; because those lines have no rows, clean is not evidence they are covered.

**REPRODUCED — recommend PL-4's exact rows and its matching digest.** I extracted the three exact JSON objects from `.ufo/waves/arc3-loop1-round12/claims/c3/PL-4.md:34-69`, appended them to the scratch table, and ran the unmodified gate. The proposed table has 60 entries, 5 quoted, 8 exempt, and SHA-256 `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`; this matches PL-4. The actual strict scratch control was clean, exit 0. With one `recheck:`-line mutation at a time, each matching row produced exactly one `citation_dead` and strict exit 1:

- `pl4-r7-recheck` — disk-backed `/var/tmp` changed to `/tmp`.
- `pl4-r10-recheck` — recorded command-list path changed to a missing filename.
- `pl4-r11-recheck` — recomputation script name changed.

The seeded overlays were supplied in memory to the gate's `git_show`; Git objects/refs/index and live instrument files were read-only. Scratch was under `/var/tmp`. These rows grade recorded text only; they do not execute the recheck recipes or prove their referenced files/caches remain live. Use PL-4's exact rows and `7470…` pin together; hashes from PL-2/PL-3/RV proposals describe different row text and are not interchangeable. CN-2 independently recommends PL-4; CN-4 recommends RV-6, another valid but different row set.

**CORRECTED — serialization in my first PL-4 hash attempt.** I initially used `ensure_ascii=False`, yielding `ec7636cff59cf42bc75cc9110aa89622a64b9d4d4a4a1410730cbec24f361ed2`, which was not PL-4's candidate byte stream. The live table round-trips byte-identically with Python's default ASCII-escaped `json.dumps(table, indent=2) + newline`; using that exact serializer reproduces PL-4's `7470…` digest and all results above. Do not use the initial `ec7636…` value.

**REPRODUCED — RV-4 helper status recheck.** The current `seeded-measurement.py` also passes its clean control and all three named seeds. The earlier-noted unique-needle failure did not recur on the current helper/source; no current failure is claimed. Its candidate bytes are a separate proposal and must not be paired with PL-4's digest.

**UNVERIFIABLE — C3 landing.** No instrument/table/pin patch is applied; a post-integration strict probe remains for the integrator.

## Write boundary

This verdict is based on immutable Git objects, package source, retained envelopes, in-memory mutation controls, and `/var/tmp` scratch. No live corpus, map, skill, instrument, custody path, Git ref/index, or other seat artifact was changed. `AGENTS.md` asks for a `LOG.md` append on changes; the explicit artifact-only boundary controls here, so no LOG edit was made. The only intended repository write from this seat is this `claims/verdicts/VZ-1.md` file.
