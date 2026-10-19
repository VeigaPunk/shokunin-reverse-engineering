# CR-5 — arc3-loop1-round12 claim reconciliation

**Verdict:** C1 — recommend one fourth-family `inspect_go_binary` Evidence-ID entry; the measurements reproduce, but the corpus/map landing and 91/91 count remain unverified. C2 — recommend one projection-local rule #17 with the `inspect_artifact` confounder preserved; the baseline is 16/16, and the post-landing 17/17 remains unverified. C3 — recommend three exact citation-drift rows plus a same-change table-digest refresh; the selected scratch patch is clean and catches all three seeded line faults, but the live table is unchanged.

## Inventory and measurement boundary

At the CR-5 pre-write inventory, all 36 top-level C1/C2/C3 reports were present: 12 C1, 12 C2, and 12 C3. EX-8 and PL-1 had appeared after CN-2's 16:53:13 inventory; CN-2's earlier 11/12, 12/12, 11/12 count is a valid snapshot, not the current report inventory (`claims/verdicts/CN-2.md:3-10`; current additions: `claims/c1/EX-8.md`, `claims/c3/PL-1.md`). The report directories also contain nested draft attachments, which are not additional seat reports.

I used the frozen Command A recipe at `SCORECARD.md:88-124` against both immutable revisions. I independently reproduced these results:

```text
HEAD  0436f4940283072db08e73c0117195847c50d31d: knowledge_files=90 mapped=90 missing=[] dangling=[] rule_blocks=16 citation_resolved_rules=16
work  5ee13b358d0a1112d31808b9bae3d8ddd1b46875: knowledge_files=90 mapped=90 missing=[] dangling=[] rule_blocks=16 citation_resolved_rules=16
```

These are pre-integration baselines only. They do not establish either proposed 91/91 coverage or a seventeenth landed rule.

### C1: independent Go-family recheck

I reran `claims/c1/CR-1/evidence/recheck.sh` against cached REA 6.7.0 and independently recomputed each returned ID from the full Evidence projection. `/usr/bin/docker` and both copies were 29,327,600 bytes with SHA-256 `70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9`. Two calls at `/usr/bin/docker` returned `ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd`; copies at distinct paths returned `ev_41902d401a87df87c2350852e8a3d84828755f89ac429f9f6ea61fe79efb9044` and `ev_83462cdf5077159097e5685794bc214198f904d9cb1578008bfe5b83941c9ad6`. All four recomputations matched, the repeat projections were equal, and changing only the subject display `name`/`local_path` preserved the ID. Substituting the selected path in `parameters.path`, `normalized_result.artifact.path`, and `locations[0].path` reproduced each copied-path ID (`claims/c1/CR-1.md:14-24`; projector: cached `rea-agents/dist/domain/evidence.js:159-183`; canonical digest: `dist/domain/canonicalDigest.js:8-25,60-76`). No target was executed.

The copied-path IDs in this fresh run differ from IDs recorded by EX-8 and other drafts because the absolute scratch paths differ; that is the expected result for the measured path-sensitive projection, not a disagreement (`claims/c1/EX-8.md:9,21-23`). This supports the bounded `inspect_go_binary` case, not a universal rule for all `ev_` operations.

### C2: independent projection replay

I ran `claims/c2/SC-1/rederive_projection_sensitivity.py` over the retained complete envelopes. It independently reproduced the EVM and Rust copy IDs and found direct projection deltas at `locations[0].path`, `normalized_result.artifact.path`, and `parameters.path`. For `inspect_artifact`, the outer projection differs at both `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`; a mutation of the nested path changes the outer ID, while top-level subject display mutations do not (`claims/c2/SC-1.md:27-45`; corroborating derivation: `claims/c2/EX-16.md:18-27`). This was a replay of retained records, not a new REA invocation.

### C3: independent gate and patch replay

The immutable HEAD pointer table contains 57 `entries`, 5 `quoted`, and 8 `exempt` records; its SHA-256 `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b` matches `expected.json:11-13`. No row's `file` or `target` references the three relevant corpus files. Their `recheck:` lines are at r7 line 5, r10 line 7, and r11 line 7. The unchanged strict probe returns `clean findings=0 exit=0`; that clean result does not grade unregistered lines.

I reconstructed PL-4's three exact rows at those line numbers, refreshed only a scratch `expected.json`, and ran the unchanged strict probe. The patch control returned no findings / exit 0. Replacing each respective scratch `recheck:` line with `recheck: SEEDED-FAULT` produced its corresponding `citation_dead` finding / strict exit 1 for r7, r10, and r11. All scratch was under `/var/tmp`; the helper logic overlaid source reads in memory and made no Git writes. The reconstructed PL-4 candidate digest is `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2` (60 entries, 5 quoted), matching `claims/c3/PL-4.md:63-69`.

The digest depends on exact row bytes and serialization. I first tried `ensure_ascii=False`, which did not reproduce the committed table's bytes; a byte-for-byte baseline check showed the repository table matches Python's default `json.dumps(table, indent=2) + "\n"` ASCII escaping. Recomputing with that serialization yielded the matching PL-4 digest and clean/fault results above. A separate snapshot-redirected scratch table from this review hashed to `7a36e48ad5f093df484b6514b16e8b8ec321f2e2c333820f4379beaa2447cbe5`; that is not the PL-4 candidate or an integration digest. Do not mix one proposal's rows with another proposal's hash. Recompute against the final integrated bytes.

## Claim verdicts and integration recommendations

### C1 — choose one Unknown, not both

The current 12 reports split **7–5**: CR-1, CR-4, EX-2, EX-4, EX-5, EX-6, and EX-8 support the fourth-family `inspect_go_binary` Unknown; EX-1, EX-3, EX-7, CR-2, and CR-3 test a path-free projection. Both sides provide bounded, reproduced measurements; the path-free results are not refuted. The frozen C1 contract asks for one Unknown (`claims-frozen.md:16-29`), so I recommend the more convergent Go-family proposal and do not recommend landing both.

Keep one knowledge entry, preferably `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`, with one map token `2026-10-19-arc3-r12-go-evidence-id-domain`. Put the token in the **Evidence model** coverage row (`corpus/README.md:41`), which indexes the three existing operation-specific `ev_` findings. Do not put it in the separate Go build-metadata row at `corpus/README.md:62`: that row describes the existing r6 metadata observation, not the Evidence-ID domain. Several C1 drafts propose the Go row; the semantic mapping belongs with the Evidence model. Re-run Command A after both files land; 91 files / 91 mapped with no missing or dangling tokens is still **UNVERIFIABLE**.

### C2 — one rule #17, with causal attribution bounded

All 12 C2 reports converge on deriving sensitivity at the operation's semantic-projection boundary rather than treating `ev_` or a field name as a universal rule. Recommend one rule that pins package/version/call shape, recomputes full envelopes, records exact changed projection paths (including nested results), uses display-only fields as negative controls, and distinguishes a field that changes an ID from a field set that explains the whole alternate-call delta.

Do not say that each EVM or Rust path field alone caused the observed difference: the alternate-call projections changed at three path fields together. For `inspect_artifact`, the nested inventory `subject.local_path` mutation changes the outer ID but does not alone recreate the alternate-call ID because `normalized_result.inspection_id` also differs (`claims/c2/EX-16.md:18-27`). Preserve this distinction in rule text and leave untested operations, versions, and version/scope sensitivity unknown. The supporting measured ranges are `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:17-22`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-21`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-19`.

Treat the old corpus status sentences as stale, not as evidence against current mapping: `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:26` says unlanded although its token is in `corpus/README.md:38`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:1,24,30` calls the entry proposed although the tokens are listed at `corpus/README.md:41,63`; `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:23` says the baseline is pending although Command A independently reproduces 90/90. No corpus corrections were in scope here. The acceptance count `rule_blocks=17` and 17 citation-resolved rules remains **UNVERIFIABLE** until a rule is integrated and Command A is rerun.

### C3 — use one coherent table patch and matching digest

Recommend PL-4's exact rows at r7:5, r10:7, and r11:7, plus its matching expected-table digest in the same integration change (`claims/c3/PL-4.md:34-69`). The scratch clean/fault behavior is **REPRODUCED**. This is text-drift coverage only: it does not execute the three recipes or prove their caches/files remain live. The live 57-entry table and its expected digest remain unchanged; a post-integration strict run is **UNVERIFIABLE**.

### Gate identity and cross-check

The C1 census gate's SHA-256 is `6edde060b927af1adeb08b857989af62f54979288335eb12eade99e59039d694` at HEAD and `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573` at the named work revision. Their only source difference is the SCORECARD scope endpoint changing 1975 to 2027. The supplied older hash `d6b4deaa5973d3a29260b0e325620d87a3cc59464771688f97cb1c62d138fc80` identifies commit `9c1d1fef5595b55d65764626249f164e6816473a`, not either R12 revision. The current `python3 .ufo/gates/c1-census-v10.py --json` result is `PASS`, with 14 frontier rows and no frontier errors.

## Process and write-scope notes

One prior `TMPDIR=/var/tmp python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` run passed 13/13, but its builder runs `git init/add/commit` in disposable fixtures (`citation-drift-probe.py:347-368`). Those temporary repositories were cleaned and no project Git objects, refs, index, or source files were changed. Under a strict reading of the Git-read-only instruction, this was still a scratch Git mutation; I disclose it and do **not** rely on the self-test result as compliant evidence. The C3 verdict instead relies on the strict baseline and the scratch `run_check`/seeded-line measurements above. RV-3 and RV-4 also disclose earlier exploratory self-tests whose unset `TMPDIR` resolved to `/tmp`; their later `/var/tmp` reruns are separately recorded (`claims/c3/RV-3.md:33-38`, `RV-4.md:69-71`).

`AGENTS.md:4` requests a LOG entry for every change, but the CR-5 write boundary forbids changing `LOG.md`; it remains untouched. No corpus, gate, custody, SKILL, PROVINCE, SCORECARD, or other seat artifact was changed. The pre-existing modification `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched. The only CR-5 deliverable is this file; no integration or commit is claimed.
