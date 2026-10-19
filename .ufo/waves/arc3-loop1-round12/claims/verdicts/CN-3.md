# CN-3 — R12 independent reconciliation verdict

**Revision checked:** `0436f4940283072db08e73c0117195847c50d31d` (named work revision `5ee13b358d0a1112d31808b9bae3d8ddd1b46875`).

This reconciles the available C1/C2/C3 drafts and the peer verdicts CN-2 and CN-4 against fresh checks. It is not a landing receipt: corpus/map, `SKILL.md`, gate/table, and expected-pin after-states remain unmeasured.

## C1 — admit one bounded fourth-family Unknown

**Verdict: ACCEPT the `inspect_go_binary` finding as the single C1 candidate; do not integrate competing C1 candidates in the same closure.** Six draft reports—EX-2, EX-4, EX-5, EX-6, CR-1, and CR-4—converge on REA 6.7.0 `inspect_go_binary` over `/usr/bin/docker` (`claims/c1/EX-2.md:13-21`; `EX-4.md:11-24`; `EX-5.md:13-29`; `EX-6.md:11-24`; `CR-1.md:12-24`; `CR-4.md:13-24`). EX-8 adds another measured derivation (`claims/c1/EX-8.md:13-25`). Their alternate-copy IDs differ because the copied paths differ and this operation hashes path-bearing semantic fields; that is expected, not a formula disagreement.

My four full envelopes are `/var/tmp/kaidoku-cn3-r12-go/{base1,base2,copy-a,copy-b}.json`, with same-byte copies at `/var/tmp/kaidoku-cn3-r12-go/copy-a/docker` and `copy-b/docker`; an independent projection/hash reconstruction produced:

```text
REA CLI version: 6.7.0
sha256sum (/usr/bin/docker, copy-a/docker, copy-b/docker):
  70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9 (all three)
size: 29327600 bytes (all three)
recomputed_ids=4/4
same_path_repeat_id_equal=true
copy_ids_differ=true
isolated_path_pointer_mutations_change_id=3/3
three_path_fields_only_reproduce_copy_a=true
display_subject_name_and_path_only_preserve_id=true
reported_ids:
  ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
  ev_87621921fc54a38ee60f85c9f81a47508dcdebd1c6f70569ec78da3a3a055dcd
  ev_6d91872d74b8e9af8ded93273855eee14040ad15e7d210d296c73d35137836c9
  ev_a9f0abe49949dedb7168eba96a7062aa5a8aba325bb18b92b217585163e8a8ff
```

The pinned source agrees with that derivation: REA's semantic projection keeps subject digest/format/architecture and semantic fields, excluding subject display `name`/`local_path` (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js:159-183`); the canonical digest hashes compact, sorted-key JSON with SHA-256 (`.../dist/domain/canonicalDigest.js:8-25,60-76`). For this operation, the selected path enters `parameters`, `normalized_result.artifact.path`, and an `artifact-path` location (`.../dist/application/go/GoBinaryService.js:54-76`; provider path at `.../dist/go/GoBinaryProvider.js:157-165`). These are static inspections; Docker was not executed, and observed build metadata is not compiler-authenticity, dependency-absence, or runtime evidence.

The alternative C1 drafts are not disproved: EX-1/EX-7/CR-2 measure bounded path-stable `analyze_function` cases (`claims/c1/EX-1.md:9-18`; `EX-7.md:15-29`; `CR-2.md:13-21`); EX-3 measures `search_bytes` (`claims/c1/EX-3.md:13-25`); CR-3 measures an internal nested `inventory_artifact` record (`claims/c1/CR-3.md:5-16`). The freeze asks for one Unknown (`claims-frozen.md:16-29`), and the fourth public operation family has the strongest convergence. CN-2:23-45 and CN-4:11-19 reach the same choice. Do not co-land all these alternatives as if they were one C1 claim.

**Integration correction:** use one corpus entry, preferably `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`, and one token `2026-10-19-arc3-r12-go-evidence-id-domain` on the **Evidence model** row at `corpus/README.md:41`. Do not place this Evidence-ID-domain token on the Go metadata row at `corpus/README.md:62` (suggested by some drafts), nor create duplicate Go entries/tokens. This matches the three prior operation-specific ID-domain entries and CN-2/CN-4's correction. The landing measurement remains **UNVERIFIABLE**: Command A at HEAD returned exactly:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":90,"mapped":90,"missing":[],"revision":"0436f4940283072db08e73c0117195847c50d31d","rule_blocks":16}
```

`91/91` is only the predicted count after co-landing exactly one entry and token.

## C2 — accept a projection-local rule #17 with a causal-isolation guard

**Verdict: ACCEPT one consolidated rule draft; the rule is not landed.** The C2 drafts converge on operation-specific semantic projection sensitivity. The meaningful refinement in EX-10/EX-16 and CN-2/CN-4 is to distinguish a field that contributes to an ID from a field mutation that explains the entire alternate-call delta.

Recommended text for integration (the fenced line is the exact raw bullet used in preflight):

```text
- **Measure Evidence-ID sensitivity at the exact semantic-projection pointer; never infer it from a field name, the `ev_` prefix, or another operation. Pin the package version, operation, request shape, and artifact bytes; independently recompute IDs from complete envelopes; compare a same-request repeat with a same-byte controlled path change. Enumerate every changed pointer in the outer semantic projection, including derived and nested result values. Attribute sensitivity to one pointer only when a one-pointer-only mutation changes the ID; attribute the entire alternate-call delta only when that mutation reproduces the alternate ID. Distinguish excluded outer subject display fields from same-named values nested in `normalized_result`, and limit conclusions to the measured operation, package version, input, and request shape; leave other fields and shapes unknown. Earned by `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:11-22`, `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:24-26`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15`, `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:19-21`, and `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:17-19`.
```

My Command-A-shaped in-memory preflight parsed the candidate as a seventeenth bullet and resolved all its corpus references against immutable HEAD:

```json
{"candidate_refs":[{"first":11,"in_bounds":true,"last":22,"lines":26,"path":"corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md"},{"first":24,"in_bounds":true,"last":26,"lines":26,"path":"corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md"},{"first":13,"in_bounds":true,"last":15,"lines":30,"path":"corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md"},{"first":19,"in_bounds":true,"last":21,"lines":30,"path":"corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md"},{"first":17,"in_bounds":true,"last":19,"lines":24,"path":"corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md"}],"citation_resolved_rules":17,"projected_rule_blocks":17,"revision":"0436f4940283072db08e73c0117195847c50d31d"}
```

This is a projection, not a post-landing count. The measured tree remains 16 blocks/16 resolved; an actual `17/17` requires integration and a fresh Command A run. R7/R10 path fields co-vary in the copied-path controls; report them as correlated unless separately isolated (`claims/c2/EX-10.md:7-9,22-40`). In R11, the alternate outer projection differs at `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`; an isolated nested-path mutation changes the outer ID but does **not** reproduce the alternate ID (`claims/c2/EX-16.md:20,27`). Do not overstate that nested path as the sole explanation.

## C3 — accept a revised, scratch-tested citation-drift table patch

**Verdict: gap VERIFIED; revised patch REPRODUCED on scratch; live integration UNVERIFIABLE.** At HEAD, R7 `:5`, R10 `:7`, and R11 `:7` each contain a `recheck:` line, and none has a grading row in the 57-entry table. The table has 5 `quoted` rows and 8 exemptions; its SHA-256 is `1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`, matching `expected.json:11-13`. The live strict baseline returned:

```text
CITATION_DRIFT_ROOT: .
CITATION_DRIFT_REVISION: 0436f4940283072db08e73c0117195847c50d31d
CITATION_DRIFT_TABLE: .ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

A clean baseline is not coverage of those unregistered fields. I recommend three no-line-pin `anchor` rows: retain relocatability, but make the command/recomputation signatures precise. This refines both CN-2's PL-4 recommendation and CN-4's original RV-6 recommendation; their hashes `7470c3f6…` and `2187f361…` belong to their own row bytes and must not be reused. The exact revised rows used in my scratch run are:

```json
[
  {
    "id": "r7-evm-entry-recheck",
    "kind": "anchor",
    "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
    "must_match": "^recheck: .*TMPDIR=/var/tmp/.*inspect-evm-interface .*--format json.*ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052.*disk-backed here\\.$",
    "note": "Grades the entry recheck command, its expected Evidence ID, and the host-specific disk-backed scratch requirement."
  },
  {
    "id": "r10-rust-entry-recheck",
    "kind": "anchor",
    "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
    "must_match": "^recheck: from the lane root, use the cached REA 6\\.7\\.0 command shown in `evidence/rederive-commands\\.txt`; then run `node \\.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids\\.mjs`\\.",
    "note": "Grades the recheck command source and the independent projection/path-field recomputation it names."
  },
  {
    "id": "r11-artifact-entry-recheck",
    "kind": "anchor",
    "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
    "must_match": "^recheck: .*identity\\.txt.*`TMPDIR` to a directory under `/var/tmp`, and run the four exact calls in `calls\\.txt`.*Then run `python3 \\.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids\\.py`\\. Do not use `/tmp` for scratch\\.$",
    "note": "Grades the pinned package identity, disk-backed scratch, recorded calls, ID recomputation, and /tmp exclusion."
  }
]
```

For the table formed from the frozen HEAD bytes plus exactly those rows, serialized with two-space JSON indentation, ASCII escaping, and a trailing newline, the measured candidate is `entries=60`, `quoted=5`, SHA-256 `d8e6a7d175a420be99f6ca2baaa0f4c344c687e2df5bf8b869a9c1e59b9f9586`. Set `expected.json:pointer_table.sha256` to that digest **only if** integration preserves these exact row bytes and serialization; otherwise recompute it.

I imported the unchanged gate module, ran its `run_check`/`report` against the scratch table and immutable HEAD, and overlaid each fault only in `git_show` memory. The clean candidate returned `clean findings=0 exit=0`; each baseline overlay was unobserved (`BASELINE_READS: 0`) and each candidate detected the fault (`PATCH_OVERLAY_APPLIED: true reads=1`):

```text
r7 :5 TMPDIR=/var/tmp/ -> /tmp/: citation_dead entry=r7-evm-entry-recheck; strict exit 1
r7 :5 expected ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052 -> ev_0000000000000000000000000000000000000000000000000000000000000000:
  citation_dead entry=r7-evm-entry-recheck; strict exit 1
r10 :7 recompute-ids.mjs -> missing-recompute-ids.mjs:
  citation_dead entry=r10-rust-entry-recheck; strict exit 1
r11 :7 directory under `/var/tmp` -> directory under `/tmp`:
  citation_dead entry=r11-artifact-entry-recheck; strict exit 1
```

The R10 needle is deliberately anchored to the complete recorded command/recomputation path; a weaker `recompute-ids.mjs` substring can falsely match `missing-recompute-ids.mjs`. The R11 needle explicitly includes the Markdown backticks around `TMPDIR` and `/var/tmp`, and passed the unmodified clean control. This is textual recheck-field coverage only; it does not execute REA or establish liveness of external caches/evidence. The scratch table and overlays were under `/var/tmp`; no project Git refs, index, source file, instrument, custody path, or expected pin were changed. I do not rely on citation-drift `--selftest` here: CN-2 notes it creates temporary Git repositories (`claims/verdicts/CN-2.md:71`); the in-memory overlays exercise the actual entry checker without that fixture behavior.

## Final per-claim boundary

- **C1 — ACCEPT as reproduced evidence, not integrated:** one `inspect_go_binary` entry/token; map row `corpus/README.md:41`. Predicted `91/91` remains unverified.
- **C2 — ACCEPT as a preflighted rule draft, not landed:** projected 17/17; actual tree remains 16/16.
- **C3 — ACCEPT as a scratch-validated patch proposal, not landed:** current 57-row table remains live; candidate 60-row table hash is `d8e6…`, with four seeded faults detected.

The latest inventory showed CN-2 and CN-4 verdicts; VZ-1..4 and CN-1 were not present in that scan. Only this CN-3 artifact is written by me. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched, as were all corpus, `SKILL.md`, gates, custody, scorecard, log, and province files.
