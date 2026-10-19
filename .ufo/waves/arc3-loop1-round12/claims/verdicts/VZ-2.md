# VZ-2 — Independent C1–C3 adjudication

**Scope:** reconcile the frozen claims and submitted round-12 evidence; independently re-derive representative reported values; provide a per-seat verdict. This is not a landing receipt. No C1 corpus entry/map token, C2 rule, or C3 instrument patch is present in the measured revisions.

## Overall verdict

- **C1 — ACCEPT one bounded `inspect_go_binary` entry (candidate a).** The Go result is independently reproducible and has the strongest convergence across the claim reports. Use one canonical corpus entry and one Evidence-model map token; do not bundle the competing path-free result as a second C1 closure. `91/91` remains unverified.
- **C2 — ACCEPT EX-16’s rule-17 draft, with its causal-scope caveat.** It correctly says that co-varying projected fields must not be treated as a single-field explanation, and it identifies the `inspect_artifact` confounder. The proposed rule passes an in-memory citation preflight, but the live count remains `16/16`.
- **C3 — ACCEPT RV-6’s exact three-anchor patch as the canonical scratch candidate.** I reran its harness: the candidate is clean and each of the three seeded faults yields `citation_dead` / strict exit 1. Use RV-6’s exact rows and its matching table digest together. The live instrument remains unchanged.

CN-2 and CN-4 converge on Go for C1 and EX-16 for C2. Their C3 patch choices differ (RV-4 versus RV-6); the row bytes and table hashes are not interchangeable. I independently reran RV-6’s full seeded harness and recommend its line-pinned `anchor` rows. All three frozen acceptance boundaries remain post-integration work.

## Frozen baselines and independent checks

The source-derived Command A recipe (`SCORECARD.md:88-124`) was run against both immutable revisions:

```text
HEAD 0436f4940283072db08e73c0117195847c50d31d:
knowledge_files=90 mapped=90 missing=[] dangling=[] rule_blocks=16 citation_resolved_rules=16

work 5ee13b358d0a1112d31808b9bae3d8ddd1b46875:
knowledge_files=90 mapped=90 missing=[] dangling=[] rule_blocks=16 citation_resolved_rules=16
```

These are baselines, not after-state wins. The EX-16 bullet, tested in memory against the frozen Command A splitter, projects to `rule_blocks=17` and `citation_resolved_rules=17`; this does not change the live `SKILL.md` count.

At HEAD the citation-drift table has 57 `entries`, 5 `quoted` rows, and 8 exemptions; its SHA-256 is `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, matching `expected.json`. The three `recheck:` lines are present at r7 `:5`, r10 `:7`, and r11 `:7`, with zero table rows grading them. The live strict probe reports `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`; that clean result does not cover unregistered lines.

The census instrument identity was also corrected: both the worktree file and `git show HEAD:.ufo/gates/c1-census-v10.py` hash to `6edde060b927af1adeb08b857989af62f54979288335eb12eade99e59039d694`. The previously supplied `d6b4deaa…` value does not describe this checkout.

## C1 — choose one Unknown

### Re-derived finding and selection

For the cached `rea-agents@6.7.0` package, `inspect_go_binary` computes `ev_` plus SHA-256 over the canonical semantic Evidence projection (`dist/domain/evidence.js:159-183`; `dist/domain/canonicalDigest.js:8-25,60-76`). Its projection excludes top-level subject display `name` and `local_path`, but this operation includes the selected path at `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path`.

I independently reran EX-8’s stored-envelope projection checker. `/usr/bin/docker` and the same-basename copy have SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9` and size 29,327,600 bytes. The two `/usr/bin/docker` calls both yield `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`; the byte-identical copy yields `ev_eb31c985b48ce12c69c82ad62f9f86f8927e48f44db801b3ad7ba66632ddf029`. All three recompute. The projection diff is exactly the three path leaves above; substituting those three fields reproduces the copy ID, while changing only display fields does not (`claims/c1/EX-8/evidence/go-recompute-results.txt`). This is a bounded static inspection, not target execution or a universal REA formula.

The independently measured EX-3 `search_bytes` result is a valid competing closure of frozen candidate (d): all three IDs recompute to `ev_4b9f570ed7503ebe3946a9458e9ae61b9fce0b3ca6605ae88b1d836da096d754`, and the semantic projections are identical across same-path repeats and a byte-identical alternate path. The captured projection has no path fields; it is bounded to REA 6.7.0, the exact `/usr/bin/jq` bytes, query `48 83 ec`, limit 5, provider, and profile (`claims/c1/EX-3/evidence/recompute-output.json`). The result is a five-match page with `complete:false`, not a full search. CR-3 likewise reproduces a path-stable nested `inventory_artifact` ID while its parent `inspect_artifact` ID changes; that substep is internal, not a distinct CLI operation (`claims/c1/CR-3.md:5-16`; `claims/c1/CR-3/entry-draft/2026-10-19-arc3-r12-inventory-artifact-evidence-id-domain.md:7,23-25`). These findings are not contradictions: they show distinct operation projections.

The freeze permits one Unknown. Given the seven convergent Go reports and the independently reproduced same-path/copy result, select candidate (a), not both (a) and (d). Use a single Go entry, preferably CR-4’s fuller draft, with EX-6/CR-1 and the remaining Go reports as corroboration. Proposed destination: `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`; proposed token: `2026-10-19-arc3-r12-go-evidence-id-domain` on the **Evidence model** row (`corpus/README.md:41`), not an additional Go metadata token at `:62`. Do not land duplicate entries for one operation. The actual after-state `91/91` has not been measured.

### C1 per-item verdicts

- **EX-1 — SUPPORTED, alternate candidate (d):** path-stable `analyze_function` sample; not the selected C1 entry.
- **EX-2 — CORROBORATES candidate (a):** `inspect_go_binary` same-byte path variants and projection recomputation agree with the other Go captures.
- **EX-3 — REPRODUCED, alternate candidate (d):** three `search_bytes` IDs and identical path-free projections independently checked; not selected.
- **EX-4 — CORROBORATES candidate (a):** Go same-path repeat, same-byte alternate paths, and path-field reconstruction.
- **EX-5 — CORROBORATES candidate (a):** Go same-basename and different-basename copies; no competing formula claim.
- **EX-6 — CORROBORATES candidate (a):** Go same-path repeat and two path variants; strong second bundle.
- **EX-7 — SUPPORTED, alternate candidate (d):** path-stable `analyze_function` call shape; not selected.
- **EX-8 — REPRODUCED, candidate (a):** all three retained IDs match; the three semantic path leaves explain the copied-path result.
- **CR-1 — CORROBORATES candidate (a):** Go operation and semantic path fields agree with EX-2/4/5/6/8.
- **CR-2 — SUPPORTED, alternate candidate (d):** path-stable `analyze_function` call shape; not selected.
- **CR-3 — REPRODUCED, alternate candidate (d):** nested inventory ID remains constant across paths while outer wrapper IDs differ. Its re-derivation script requires the evidence-directory argument; the correct invocation is `node …/rederive.mjs .ufo/waves/arc3-loop1-round12/claims/c1/CR-3/evidence`.
- **CR-4 — RECOMMENDED canonical draft for candidate (a):** its controlled Go copies, formula and bounded scope are consistent with my re-derivation and peer convergence.

## C2 — rule #17

All proposals target the same earned rule: identity-field sensitivity belongs to the exact emitted projection, not to the `ev_` prefix or an assumed domain-wide rule. EX-16 is the best draft because it requires complete-envelope recomputation, same-path and same-byte alternate-path controls, exact projected pointers, and a field-or-field-set mutation; crucially, if the mutation does not reproduce the alternate-call ID, the remaining differences must be reported rather than attributed to that field (`claims/c2/EX-16.md:6-9,18-27`). Its citation ranges are in bounds at frozen HEAD (r7 26 lines, r10 30, r11 24), and the in-memory rule-count preflight is 17/17. No rule landed, so 17/17 is not a measured after-state.

I independently replayed EX-14’s retained envelope re-derivations: all reported outer IDs match; same-path repeats are stable; alternate paths change the outer ID for EVM, Rust, and artifact inspection. For EVM/Rust, `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` co-vary. For `inspect_artifact`, the full outer-projection diff includes both `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`. Mutating the nested path alone changes the outer ID but does **not** reproduce the copied-path ID; it is therefore a contributing pointer, not a complete explanation of that live delta. This is the material confounder that EX-16 handles correctly.

The prior-round corpus measurement passages support the rule, but several status sentences are stale at HEAD: r7 says its corpus/map token is not landed at `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:26` although the token is on `corpus/README.md:38`; r10 calls its entry/token proposed at `:1,24,30` although it appears at README `:41,63`; r11 says its 90/90 Command A result is pending at `:23`, while the measured HEAD baseline is 90/90. Use measurement passages, not these status claims. No corpus edit is authorized here.

### C2 per-item verdicts

- **EX-9 — SUPPORTED DRAFT:** per-projection rule and fresh operation measurements; after-count unverified.
- **EX-10 — SUPPORTED DRAFT:** strongest explicit exact-pointer and correlated-field caveat; after-count unverified.
- **EX-11 — SUPPORTED DRAFT:** citations and in-memory 17/17 preflight; actual rule remains at 16.
- **EX-12 — SUPPORTED DRAFT:** version-bounded projection reconstruction; preserve the wrapper-field confounder.
- **EX-13 — SUPPORTED DRAFT:** per-operation rule and independently reported envelope checks; no landing claim.
- **EX-14 — REPRODUCED FROM RETAINED ENVELOPES:** all three operation sets recompute and support projection-local sensitivity; no landing claim.
- **EX-15 — SUPPORTED DRAFT:** sound rule/citation preflight; describe the EVM/Rust path leaves as co-varying unless individually isolated.
- **EX-16 — RECOMMENDED:** best causal-scope wording; correctly says nested-path-only mutation does not reproduce the full artifact-copy ID.
- **SC-1 — SUPPORTED DRAFT:** correct gap and independent projections; its report also identifies the stale status text verified above.
- **SC-2 — SUPPORTED DRAFT:** version-aware projection reconstruction; do not generalize across releases.
- **SC-3 — SUPPORTED DRAFT:** fresh path probes and bounded operation results; keep the wrapper confounder explicit.
- **SC-4 — SUPPORTED DRAFT:** accurate projection-local formulation and citations; not a landed change.

## C3 — citation-drift table coverage

The live gap is verified: r7 `:5`, r10 `:7`, and r11 `:7` each contain a `recheck:` recipe, and the current pointer table has no row for any of them. I independently ran the live strict baseline (clean, zero findings), then ran RV-6’s scratch harness from `claims/c3/RV-6/seeded-fault.py`. It produced a 60-entry candidate table with SHA-256 `2187f361403c9c13d861b41c210ab2e8c123c77203020c53c64aa2a55d7f0602`; the candidate control is clean, and each separate fault—r7 `/var/tmp` to `/tmp`, r10 command-list rename, r11 `/var/tmp` to `/tmp`—produces exactly its corresponding `citation_dead`, strict exit 1. The baseline reads none of the three lines; the patch reads each targeted line. Scratch is under `/var/tmp`; the harness uses an in-memory Git-object overlay and makes no Git writes.

Recommend RV-6’s exact rows (`claims/c3/RV-6.md:56-93`) and that exact digest together. Its existing `anchor` + `pin_line` behavior can distinguish moved text (`citation_moved`) from missing text (`citation_dead`) (`citation-drift-probe.py:180-189`). Do not copy a table digest from RV-4, PL-4, or another draft: different row text/serialization produces a different SHA. The patch grades text, not command execution, file liveness, or REA results. The instrument, table, and expected pin are unmodified; integration remains unverified.

The citation-drift `--selftest` results reported by some peers are excluded as policy-inadmissible: the test builder creates temporary Git repositories with `git init`, `git add`, and `git commit` (`citation-drift-probe.py:347-368`). Setting `TMPDIR=/var/tmp` does not make those Git mutations admissible. The direct live baseline and the scratch overlay harness are the relevant evidence. RV-4 additionally disclosed an initial self-test invocation that used `/tmp`; its later seeded harness is a separate compliant measurement.

The alternative custody-pair stanza-count candidate is already covered at this HEAD. I independently ran its self-test with scratch under `/var/tmp`: `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`; cases reject five duplicate stanzas as only 1/5 distinct paths and accept five distinct paths. Source counts resolved distinct paths (`custody-pair.py:637-651,1157-1193`), so no duplicate custody patch is recommended.

### C3 per-item verdicts

- **PL-1 — REPRODUCED SCRATCH PATCH:** baseline gap, clean candidate and seeded r11 failure; exclude its citation-drift self-test result.
- **PL-2 — REPRODUCED SCRATCH PATCH:** gap and seeded r10 fault; its report correctly excludes the Git-mutating self-test.
- **PL-3 — REPRODUCED SCRATCH PATCH:** candidate clean and three seeded line faults detected; exclude the self-test result.
- **PL-4 — REPRODUCED SCRATCH PATCH:** three exact rows and cumulative seeded findings; its proposed table hash is a distinct alternative, not RV-6’s pin; exclude the self-test result.
- **RV-1 — SUPPORTED:** citation-table gap and seeded r11 fault; its custody alternative is already closed by current behavior.
- **RV-2 — REPRODUCED SCRATCH PATCH:** clean candidate and seeded stale-line detection; custody alternative is not a live gap.
- **RV-3 — REPRODUCED SCRATCH PATCH:** current gap and seeded r11 fault; exclude citation-drift self-test result.
- **RV-4 — REPRODUCED SCRATCH PATCH:** independently valid three-fault candidate; do not combine its bytes/hash with RV-6. Initial `/tmp` self-test and later self-test results are not relied on.
- **RV-5 — REPRODUCED SCRATCH PATCH:** clean candidate and seeded r7 ID drift; candidate hash applies only to its rows.
- **RV-6 — RECOMMENDED:** independently rerun here; clean control, all three exact seeded mutations caught, no Git writes.
- **RV-7 — REPRODUCED SCRATCH PATCH:** clean candidate and seeded r11 scratch-path fault; candidate hash applies only to its rows.
- **RV-8 — PARTIAL / SEED INADMISSIBLE:** baseline gap is supported, but its seeded fixture creates and commits a temporary Git repository, contrary to the read-only rule; do not use that seed as C3 verification.

## Write boundary and acceptance limits

Only this `claims/verdicts/VZ-2.md` artifact is written by this seat. The pre-existing modification `.ufo/waves/arc2-loop1-round10/C3.md` remains untouched. No corpus, map, `SKILL.md`, gate, expected pin, custody file, scorecard, province, or log was changed. C1 `91/91`, C2 `17/17`, and an integrated C3 strict run remain unverified until the selected exact proposals are landed together and measured at the landing revision.