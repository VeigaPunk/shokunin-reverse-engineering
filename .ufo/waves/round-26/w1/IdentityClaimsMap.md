# R26-C1 prior-statement map — what the lane already says about evidence-ID identity

Seat KaidokuR26.IdentityClaimsMap (leaf, read-only). Lane revision read:
`c27f445e70cedbaf5300b2fd0a53e821d9b659a9` (`git rev-parse HEAD`, 2026-10-22T12:13:57Z, exit 0).
No REA call and no measurement in this file is mine; every measurement cited below is the
lane's own. Nothing in the lane was written except this file.

## Evidence of commands (all 2026-10-22, all exit 0)

Raw output retained at `/fast/scratch/hyaku/kaidoku-r26/seats/IdentityClaimsMap/raw-lane-statements.txt`
(3,666 B, 46 lines, sha256 `942043420b1e71dd53de25bc5020908fdcf5566f80fb006cc2e099713a0390aa`,
re-hashed 2026-10-22T12:15:32Z, exit 0).
Each row of Table 1 was produced by `sed -n '<range>p' <path>` at the lane root (exit 0) and by
`grep -rn "<term>" --include=*.md .` for discovery; the 6.5.0 package facts are from
`grep -n` / `sed -n` on the installed package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` (exit 0, 12:14:09Z).

- E1 `sed -n '203p' corpus/README.md` → "Evidence-id identity is verb-family-specific, not universal: revenger-verifier ids are path-sensitive … while `analyze`/`inspect` and `analyze_function` ids are content+params-keyed".
- E2 `sed -n '24,25p' corpus/QUALITY.md` → rule 14 "`f(content, path, params)` — 'content-addressed' alone is inadmissible"; rule 15 "per verb family with its corpus citation — never a universal formula".
- E3 `sed -n '407,419p' SKILL.md` → same verdict as E1, with r5-01 cited.
- E4 `sed -n '28,33p' PROVINCE.md` → "the evidence ID alone does not authenticate module attribution carried in `subject`".
- E5 `sed -n '61,67p;327,352p' SCORECARD.md` → "`analyze`/`inspect`/`analyze_function` content+params-keyed per r5-01/r9-02"; luna-round-3 "no live probes by design", universal hits 3 → 0.
- E6 `dist/cliCommandNames.js:162-167` → `analyze: ["binary_overview"]`, `inspect: ["binary_overview"]`, `decompile: ["procedure_pseudo_code"]`, `function: ["analyze_function"]`, `instructions: ["read_function_instructions"]` (sha256 `41963156…5dd3`).
- E7 `dist/cli-runtime/cli.js:10347,10355` → both `runDirectAnalysis(args.path, "binary_overview", {}, …)`; `:10371` decompile `{ procedure }`, `:10398` xrefs `{ address }`, `:10432` function `{ procedure }`, `:10447` instructions `{ procedure }`, `:10524` read-bytes `{ address, length }` (sha256 `168cd322…e2204`).
- E8 `dist/domain/evidence.js:156-177` → projection keeps `parameters`, `normalized_result`, `locations`; subject keeps only `digest`, `format`, `architecture` (sha256 `f992d93e…dcff`).

## Table 1 — statements (path:line, pin, verb, stated verdict, pointer)

| # | path:line | pin | verbs / family | stated verdict | evidence pointer | class |
|---|---|---|---|---|---|---|
| 1 | `corpus/README.md:203` | none stated (cites 6.4.0-era entries) | revenger-verifier family; `analyze`, `inspect`, `analyze_function` | family-specific; revenger-verifier path-sensitive; those three content+params-keyed; `subject` unauthenticated | r2:244-250; r9-02:146-169 (r5-01:83-85 absent) | summary, second-hand |
| 2 | `corpus/QUALITY.md:25` (rule 15) | none stated | same as #1 | same as #1; binding, supersedes 14 | r9-02:146-169; r2:244-250 (r5-01 absent) | binding rule |
| 3 | `corpus/QUALITY.md:24` (rule 14) | none stated | universal | ids are `f(content, path, params)`, path-sensitive | r4 three-lane corroboration | retained superseded universal |
| 4 | `SKILL.md:407-419` | none stated | same as #1 | same as #1 | r2:244-250; r5-01:83-85; r9-02:146-169 | summary, fullest pointers |
| 5 | `SCORECARD.md:61-67` | 6.4.0 lineage | same as #1 | "authority contradiction closed"; no family beyond the recorded ones claimed | r5-01, r9-02, r2 | self-assessment record |
| 6 | `SCORECARD.md:327-352` | 6.4.0 lineage | same as #1 | luna-round-3 measured textual scope only: universal hits 3 → 0, no live probes | same three | self-assessment record |
| 7 | `PROVINCE.md:28-33` | 6.4.0 lineage | `analyze_function` | id does not authenticate module; pin request bytes | r9-02:146-169 | operating convention |
| 8 | `corpus/knowledge/2026-10-13-r2-evidence-bundle-schema.md:244-250`; duplicate `2026-10-13-r3-mcp-session.md:150-158` | 6.4.0 | revenger verifier (jadx, apktool, trace-application-feature) | ids path-sensitive; universal formula `f(content, path, params)` | `ev_8efa2368…` vs `ev_50038b96…`; jadx mkdtemp; apktool deterministic | first-hand, written as universal |
| 9 | `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md:83-85` | 6.4.0 | `analyze`, `inspect` | identical ids at two paths, byte-identical content → tracked content, not path; scope labeled UNKNOWN | `ev_e9a735a2…`, `ev_73581d6b…`; `/tmp` scratch only | first-hand; only measurement on these two verbs |
| 10 | `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-183` | unstated for these runs (only `:67` says 6.4.0, different candidate) | `analyze_function` | same id across two paths; subject-only rewrite bit-identical → `f(content, params)` | `/tmp/r9-fn-libc.json` etc. (scratch) | first-hand |
| 11 | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:117-119` | 6.5.0 | `analyze` (Ghidra) | 7/8 ids repeat across passes, attributed to content-keyed; aether differs with `string_count` | two passes, retained runs | first-hand, same-path only |
| 12 | `corpus/knowledge/2026-10-20-r20-wasm-interfaces.md:18` | 6.5.0 | `inspect-wasm-artifact` | repeat returned same id, content+params-keyed for these inputs | retained envelope | first-hand, other verb |
| 13 | `corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:3` | 6.5.0 | `identify-flutter-build`, `inspect-dart-aot` | replay guidance: compare digests and fields, "not path-sensitive Evidence ids" | two retained envelopes | operating guidance, implicit universal |
| 14 | `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:13,19` | 6.7.0 | `inspect_artifact` on `/usr/bin/jq` (same carrier) | same-path stable; alternate path, even same basename, changes the outer id | four committed envelopes + recompute | first-hand, different verb from frozen `inspect` |
| 15 | `corpus/knowledge/2026-10-19-arc3-r7-…:9,17-22,26`; `arc3-r10-…:13-15,28`; `arc3-r12-…:1,15`; `arc3-r3-evm-optimizer-shapes.md:19,30`; `arc3-r4-evm-vyper-leg.md:26` | 6.4.0 and 6.7.0 | `inspect-evm-interface`, `inspect_rust_binary`, `inspect_go_binary` | path-sensitive through named semantic path fields; explicitly "not a universal rule" | committed envelopes, package source lines | first-hand, per operation |
| 16 | `corpus/knowledge/2026-10-13-r3-appimage.md:65-66,87` | 6.4.0 | `inspect_binary_layout` | `provider_unavailable` without pwntools — availability, not identity | run log | first-hand, availability only |
| 17 | `corpus/knowledge/2026-10-13-r3-verb-coverage.md:88-91,145,190` | 6.4.0 | `read-bytes`, `instructions`, `xrefs` | single-run id records only; no identity verdict | `/tmp/r3-*.json` | context, no verdict |

## Table 2 — statements a per-verb 6.5.0 table would refine or contradict

| statement | refines if | contradicts if |
|---|---|---|
| #1, #2, #4 (`analyze`/`inspect`/`analyze_function` content+params) | all three rows label content-keyed: the table adds the missing 6.5.0 pin, committed envelopes and 8-verb scope | any of those three rows labels path-sensitive or unstable at 6.5.0 |
| #1, #2, #4 unit of claim, "verb family" | `analyze` and `inspect` rows differ, or they agree while another DirectAnalysis verb differs: the unit becomes CLI verb or invocation shape, not operation | nothing — a stable unit change is a refinement, not a factual refutation |
| #3 (universal) | any of the eight rows is content-keyed (expected; confirms supersession already recorded) | only if the C1 entry itself restates a universal; the table cannot revive #3 |
| #5, #6 (closure claims) | verdicts agree: closure stays textual, table adds empirical rows at a new pin | `analyze`, `inspect` or `function` flips at 6.5.0: "closed" holds only for the 6.4.0 citations, so the closure needs a pin qualifier |
| #8 (r2 universal errata) | corroborated as historical, pin-scoped | restated as current if C1 prose generalizes |
| #9 (r5-01) | same verbs, new pin, third run, explicit verdict label; extends 6.4.0 to 6.5.0 | `analyze` or `inspect` row is path-sensitive or unstable at 6.5.0 → r5-01 becomes pin- or parameter-bounded |
| #10 (r9-02) | `function` row content-keyed: supplies the version pin r9-02 never states | `function` row path-sensitive or unstable |
| #11 (r17) | `analyze` base equals repeat: same test shape at the same pin, now with a committed envelope | `analyze` repeat differs at 6.5.0 on identical bytes, undercutting r17's content attribution |
| #12 (r20) | scope widens from one wasm verb to eight native verbs at the same pin | no contradiction path (different verb) |
| #13 (r22 guidance) | guidance narrows to the verbs actually measured content-keyed | not contradicted; conservative advice stays safe |
| #14 (r11, `inspect_artifact`) | nothing to refine | only prose that equates the frozen `inspect` with `inspect_artifact`; the rows themselves cannot contradict it |
| #15 (arc3 per-operation) | agrees with a per-verb unit and supplies native reader verbs | only if C1 generalizes beyond its carrier, pin and address |
| #7 (PROVINCE) | list of which verbs' ids are content-keyed replaces the single `analyze_function` example | nothing |
| #2 governance (QUALITY never-rewrite) | if any prose must change, the lane's own pattern (#15 superseding #14) is a new rule row, not an edit of #15 | not applicable — design constraint on the L1, not a truth claim |

## Findings

F1 (observation, E1/E2/E4) `corpus/README.md:203` and `corpus/QUALITY.md:25` cite only r2 and
r9-02 for their content-keying clause; the first-hand support for the `analyze`/`inspect` half is
`r5-01:83-85`, which both omit while `SKILL.md:407-419` and `SCORECARD.md:339-346` do cite it. The
omitted pointer is the only measurement covering two of the eight frozen verbs.

F2 (observation, E6/E7) Name collision: frozen verb `inspect` calls `binary_overview`, while
`inspect-artifact` calls `inspect_artifact`. The lane's only 6.7.0 measurement on carrier
`/usr/bin/jq` is `inspect_artifact` (r11) and it is path-sensitive. The r11 envelopes therefore
say nothing about the `inspect` row; the C1 entry must keep the two names apart.

F3 (observation, E7) `analyze` and `inspect` are literally one call:
`runDirectAnalysis(args.path, "binary_overview", {})` at cli.js:10347 and :10355, after a
JavaScript-lane branch that does not trigger on `/usr/bin/jq`. [INFERENCE] Their base ids on the
same path should be equal and their verdicts identical; if they differ, the difference lies
outside the operation and needs explaining, and if they agree, two rows carry one measurement.

F4 (observation, E8 + E7) At 6.5.0 the id hashes `parameters`, `normalized_result` and
`locations`, and none of the six DirectAnalysis argv sets carries a path (parameters are `{}`,
`{procedure}`, `{address}` or `{address, length}`). [INFERENCE] Path can enter only through
`normalized_result` or `locations`, so content-keyed is the expected verdict for six verbs;
`inspect-binary-layout` is the exception candidate because its service input is `{ path }`
(cli.js:8413).

F5 (observation, Table 1 rows 9-17) Five of the eight frozen verbs — `decompile`, `xrefs`,
`read-bytes`, `instructions`, `inspect-binary-layout` — have no identity statement anywhere in
the lane; their corpus presence is single-run id records. For those five the table is new
evidence, not a correction of anything.

F6 (observation, E1/E5) The prior "path-sensitive" statements all target verbs outside the frozen
eight (jadx, apktool, trace-feature, the three arc3 inspection verbs). No existing statement
claims path sensitivity for any of the eight, so the table cannot confirm one; its only
falsifiable targets are the content-keying claims on `analyze`, `inspect`, `function` and the
generalizations in #3 and #13.

F7 (observation, claims.json) `no-id` is possible for a host-config reason: r3-appimage recorded
`inspect-binary-layout` as `provider_unavailable` at 6.4.0, while the round-26 pre-freeze probe at
6.5.0 returned `ok: true` with `ev_294a449c…`. The frozen rule already scopes the label to the
invocation; the entry should say so next to that row.

## Unknowns

- No committed envelope backs r5-01 or r9-02 (both cite `/tmp` scratch); I did not test whether
  those files still exist, so neither statement's raw bytes were re-read by me.
- I did not run REA; verdict labels for the eight verbs remain unmeasured and this map asserts no
  verdict.
