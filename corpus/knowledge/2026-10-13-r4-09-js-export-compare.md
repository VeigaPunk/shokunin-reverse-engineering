<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/09-js-export-compare.md. -->

# kaidoku-r4 · 09-js-export-compare — `compare-javascript-export-shapes` (r3's last unexercised compare verb)

Axes: **verb-coverage** (the 8th and last `compare-*` CLI verb now exercised end-to-end), **diff-taxonomy** (all four `change.status` values + `discriminant` pairing + JSON Pointer paths observed live), **selector-honesty** (`selected` / `missing` / `unavailable` outcomes all reproduced with typed reasons), **coverage-propagation** (graph `partial` → comparison `partial`; truncated upstream graphs surface as `missing`), **negative-space** (bogus selector, non-callable export, retained-ref on CLI — each fails closed with a typed envelope).

Targets: Obsidian `app.asar` 1.12.7 (`/var/cache/pacman/pkg/obsidian-1.12.7-3-…`, sha256 `a92d31a5…18e`, 73,056 B) vs 1.13.7 (`obsidian-1.13.7-2-…`, sha256 `8588f1fd…c52`, 480,052 B — byte-identical to `/usr/lib/obsidian/app.asar`), plus cross-file `obsidian.asar` 1.13.7 (r3 artifact `ev_e8a2c4ba…`, 47.66 MB Evidence reused from `/tmp/obsidian-renderer-analysis.json`), plus a controlled synthetic pair (`/tmp/mini-a` vs `/tmp/mini-b`, two-file CJS apps with literal-object returns).

## Candidate: input contract — `{left, right, left_module_path, left_export_name, right_module_path, right_export_name}`; `left`/`right` are full inline Evidence, identities must differ

- claim: `rea compare-javascript-export-shapes <inputJson>` takes one JSON arg (inline or file path). `compare-javascript-export-shapes '{}'` fails RC=1 with `invalid_request`/`invalid_input` listing all six missing fields and their types. `left`/`right` must be complete Evidence objects (validated against strict `evidenceSchema` — `subject`, `provider`, `predicate_type`, `confidence ∈ observed|derived|inferred`, `authority ∈ shipped-artifact|controlled-replay|historical-reference|external-service|analyst-inference`, etc. all required). `left.evidence_id === right.evidence_id` is rejected (`superRefine` in `dist/domain/javascript/javascriptExportShapeComparisonSchemas.js:52-59`). Selection semantics (`javascriptExportShapeSelection.js`): candidates = graph-node observations with `properties.semantic_role === "export-binding"` + `module_path` + `exported_name`; a `selected` result additionally requires authority `ast-static-analysis`, state `observed`, extractor `recover-module-export`, AND exactly one `export-return-shapes` observation matching module+export.
- source: live error envelopes (`{}` probe); `dist/server/registerApplicationTools/compareExportShapes.js`; `dist/domain/javascript/javascriptExportShapeComparison{,Schemas,Selection}.js`.
- verify: `npx -y rea-agents@6.4.0 compare-javascript-export-shapes '{}' ` → 6 `missing_argument` issues.
- verified-at: 2026-10-13
- suggested: admit — CLI accepts only full inline Evidence; ~24 MB input files are normal for real bundles (two app.asar Evidences → 23.7 MB request JSON).

## Candidate: REAL version diff — `type-utils.js:serialize` 1.12.7 vs 1.13.7 — 5 return variants per side, ZERO paired, all `unknown`

- claim: RC=0, `ev_c9b2fcdf6b3d34e61a5fa8eac38e3108205232018bef54ee6e995bcdc4e60f27`, `jesc_72edc740…`. Both selectors `selected` (1 exact candidate each). `property_inventories`: 10 rows, `paired:false` all — every `static_return_shapes[]` entry on both sides has `value_status:"unknown"` (dynamic deserialization returns), so **no unique exact literal discriminant exists and the engine refuses positional pairing** — `paired_variants:0`, `unpaired_left:5`, `unpaired_right:5`, `summary:{added:0,removed:0,changed:0,unknown:10}`, `coverage.status:"partial"` (both `graph_status:"partial"` propagate). Each change row carries availability `unknown` + reason (`"No left return variant was uniquely paired with this right variant."` / mirror), null discriminant, `presence:{unknown-coverage,unknown-coverage}`, one-sided `source_range`.
- source: `/tmp/cmp-serialize-out.json` (14,320 B); inputs `/tmp/app-1127-analysis.json` (ev `a29ab2a0…`, 10.5 MB) + `/tmp/app-1137-analysis.json` (ev `4c3202c9…`, 12.0 MB).
- verify: rerun compare on the two Evidence files; `python3` recount `summary`/`coverage`.
- verified-at: 2026-10-13
- suggested: admit — the verb's headline behavior on real shipped code is *refusing to guess*: `unknown` dominates when return values are dynamic. Pairing is discriminant-only, "never by source order" (verbatim limitation).

## Candidate: REAL version diff — `get-electron-binding.js:getElectronBinding` — literal discriminant pairs exactly 1 of 3 variants; the pair emits ZERO change rows

- claim: RC=0, `ev_b9ad0fe7ca18cd1b347d24514b23dfc735232600ce4972c9eda8215ee6e8545b`, `jesc_0275ec62…`. Each side has 3 return variants (source lines 6/9/12); only the line-12 variant carries a discriminant `{path:"", value:null}` (the bare `return`/null literal) → `paired:true` on both sides, `paired_variants:1`, unpaired 2+2, `summary:{unknown:4}`. The paired variant produced **no change row at all** — identical empty property sets on both sides means nothing to report (`unchanged` is not a status; absence = identical-within-observability). Coverage `partial` despite complete per-side shape coverage, driven by unpaired variants + partial graphs.
- source: `/tmp/cmp-geteb-out.json` (8,858 B).
- verify: `python3` inspect `property_inventories` (paired flags, discriminants) and `changes[]` reasons.
- verified-at: 2026-10-13
- suggested: admit — documents that "paired but unchanged" is silent; consumers diff `changes[]` only.

## Candidate: non-callable export — `module-names.js:browserModuleNames` → selector `unavailable` on BOTH sides

- claim: RC=0, `ev_f45fc64e53984494d2b0aaf8707353ad7e55d2ad9e82a06a4af943b679a5f672`, `jesc_2c306d29…`. The export-**binding** exists (1 candidate each, `matches_requested_*:true`) but no `export-return-shapes` observation was ever projected — `browserModuleNames` is an exported constant array, and return-shape projection requires a callable link (`callable_kind ∈ function|class|method`). Result: `status:"unavailable"` both sides, one synthetic `unknown` change at path `""` with reasons `"Left/Right export selection is unavailable."` + change-level limitation `"Both selectors must resolve one exact export with trusted static return shapes before comparison."`; limitation `"No exact static return-shape observation is available for the selected export."` Honest negative — a literal array's *contents* are out of this verb's scope.
- source: `/tmp/cmp-modnames-out.json` (5,312 B).
- verify: rerun; recount candidates/status.
- verified-at: 2026-10-13
- suggested: admit — documents the callable-only boundary; const exports are knowable via `export-binding` but never comparable here.

## Candidate: nonexistent selector — `no/such/module.js:nope` → `missing`, full candidate census returned

- claim: RC=0, `ev_cdc468c35d1eb5143b933a4799d33a42a60b02113febf483639829ab8809ecfd`, `jesc_0c0864b7…`. Left selector `status:"missing"`, `selected_node_id:null`, `candidates` = all 24 export bindings in the left graph (0 match flags — enumeration is a discovery aid), `omitted_candidates:0`. Right still `selected`. One `unknown` change with per-side reasons `"Left export selection is missing."` / `"Right export selection is selected."`; limitation `"No exact export binding matched no/such/module.js:nope."`
- source: `/tmp/cmp-bogus-out.json` (11,880 B).
- verify: rerun; same census.
- verified-at: 2026-10-13
- suggested: admit — `missing` vs `unavailable` is a meaningful distinction (no binding vs binding-without-shapes); candidate lists make selector typos cheap to fix.

## Candidate: CROSS-FILE — `app.asar`(1.13.7) vs `obsidian.asar`(1.13.7) same selector → left `selected`, right `missing` (only 8 export bindings survive the 25 MB budget truncation)

- claim: RC=0, `ev_99b42bc21158ad8ec87cc54c604d74133ca52da829ac80381d2b0cbe773b689d`, `jesc_92c905ea…` (63 MB request JSON). The r3 obsidian.asar Evidence — where parent result-budget truncation killed most module expansion — exposes exactly **8 export-binding candidates**: `lib/{codemirror/codemirror,i18next.min,moment.min,prism.min,readability,reveal/reveal,scrypt}.js:default` + `lib/readability.d.ts:Readability`. `serialize` matches none → right `missing`, one `unknown` change, coverage `partial`, both `graph_status:"partial"`. Cross-file same-version compare is mechanically supported (distinct evidence_id is the only identity rule) but degenerates to selector diagnostics when one side's export surface was budget-truncated.
- source: `/tmp/cmp-crossfile-out.json` (7,595 B); `/tmp/obsidian-renderer-analysis.json` (r3 artifact).
- verify: rerun compare; enumerate `right.candidates`.
- verified-at: 2026-10-13
- suggested: admit — honest negative; records that budget-truncated bundles (r3's 1 GiB wall) leave too few export bindings for meaningful cross-artifact shape diffs. Same-version cross-file pairs need per-file/directory analysis first.

## Candidate: SYNTHETIC literal fixture — full diff taxonomy observed: `changed` + `added` + `removed` with literal values, JSON Pointer paths, discriminant `/nested/flag=true`, array path `/2`

- claim: `/tmp/mini-a`/`/tmp/mini-b` = two 4-line CJS apps (`exports.config = function(){ return {…literals…} }`, `exports.tags` returning `["a","b"]` vs `["a","b","c"]`). Analyses: `ev_6e6e173b…`(a) / `ev_f36db5b9…`(b), 46 KB each. Forward compare `index.js:config` → `ev_ec6d721d…`, `jesc_15f0e3fc…`: `coverage:"complete-within-inputs"`, `paired_variants:1` via discriminant `{path:"/nested/flag", value:true}`, `summary:{added:2,removed:0,changed:1,unknown:0}` — `changed /mode` (literal `"dark"`→`"light"`), `added /extra` (`"new-field"`), `added /nested/second` (`2`); each change carries `presence:{left,right}`, `availability` (`literal`+value vs `absent`), both source ranges, `evidence_links:[leftEv,rightEv]`. `tags` → `ev_71ed7485…`, `jesc_56cc9dd0…`: `added /2` — **array elements are JSON-Pointer-indexed properties**; discriminant `{path:"/0",value:"a"}`. REVERSED compare (b→a) → `ev_c330884f…`, `jesc_915955f3…`: `removed:2, changed:1` symmetric. `property_inventories` list every observed property path + per-level `property_coverage {complete}`.
- source: `/tmp/cmp-mini-{config,tags,rev}-out.json`; fixture files `/tmp/mini-{a,b}/index.js`.
- verify: rerun any of the three compares; identical summaries.
- verified-at: 2026-10-13
- suggested: admit — the ONLY run producing non-`unknown` statuses; proves the added/removed/changed machinery works end-to-end and that failure to pair in the real runs is data-driven, not engine-broken. Fixture caveat recorded honestly: synthetic literals were authored to exercise the taxonomy.

## Candidate: fixture gotcha — `module.exports = {config, tags}` yields `default` binding only, NO return shapes; `exports.X = function` yields both

- claim: first mini iteration used shorthand `module.exports = {config, tags}` → exactly one `export-binding` (`index.js:default`), zero `export-return-shapes` observations (the shorthand object export has `exportedName` but `callableId:null` in the module-relationship IR — see `javascriptExportReturnShapeProjection.js:6`). Rewriting to `exports.config = function config(){…}` produced per-export bindings AND shape projections. Selector on `default` would land `unavailable`.
- source: `/tmp/mini-a-ev.json` before (ev `de3385f9…`, 46,200 B) vs after (ev `6e6e173b…`).
- verify: diff the two mini Evidence files' `semantic_role` census.
- verified-at: 2026-10-13
- suggested: admit — playbook note: export *shape* coverage depends on export *form*; `module.exports = {…}` aggregates are invisible to this verb beyond `default`.

## Candidate: retained-evidence references are an MCP-session affordance — CLI rejects `{"kind":"retained-evidence","evidence_id":"ev_…(64hex)"}` at input validation

- claim: RC=1, `invalid_request`/`invalid_input`: strict `evidenceSchema` rejects the `{"kind":…}` object — all Evidence fields `missing_argument`, `kind` flagged `unknown_argument` (probe ran with a full-length 64-hex `ev_6e6e173b…` id; an earlier truncated-id probe additionally flagged `invalid_format`). The docs' `retained-evidence` form (`references/javascript-applications.md`) resolves via `evidenceById` — a per-MCP-connection store; each CLI invocation is a fresh process with no retained table, so the resolver never sees a valid reference. Every CLI call must carry full inline Evidence.
- source: `/tmp/cmp-mini-ref2-out.json` error envelope; `EvidenceInputResolver.js` usage in `compareExportShapes.js:14`.
- verify: rerun `/tmp/cmp-mini-ref2-in.json`; same typed envelope.
- verified-at: 2026-10-13
- suggested: admit — honest negative; budget ~2× input Evidence size per CLI compare request.

## Run log

| # | command | RC | output bytes | evidence / notes |
|---|---------|----|--------------|------------------|
| 1 | `npx -y rea-agents@6.4.0 --llms \| grep -i 'export\|compare'` | 0 | — | exact CLI name `compare-javascript-export-shapes`; `--schema` shows only `{inputJson: string}` (inline JSON or file path) |
| 2 | `compare-javascript-export-shapes '{}'` | 1 | ~600 | typed `invalid_input` revealing the 6-field input contract |
| 3 | `tar -xf obsidian-{1.12.7-3,1.13.7-2}.pkg.tar.zst usr/lib/obsidian/{app,obsidian}.asar` → `/tmp/obs-{1127,1137}` | 0 | — | pacman cache holds both versions; 1.13.7 asars sha256-identical to `/usr/lib/obsidian/*` |
| 4 | `analyze-javascript-application /tmp/obs-1137/…/app.asar` | 0 | 11,993,834 | `ev_4c3202c9…`; 34 progress sequences; graph `partial`; 25 unique export bindings, 16 return-shape obs |
| 5 | `analyze-javascript-application /tmp/obs-1127/…/app.asar` | 0 | 10,541,236 | `ev_a29ab2a0…`; 24 unique bindings (adds nothing; 1.13.7 adds `node-addon-api/index.js:default`), 16 shape obs |
| 6 | `compare-javascript-export-shapes /tmp/cmp-serialize-in.json` (23.76 MB) | 0 | 14,320 | `ev_c9b2fcdf…` — 5v5 variants, 0 paired, 10 `unknown` |
| 7 | `compare-javascript-export-shapes /tmp/cmp-geteb-in.json` | 0 | 8,858 | `ev_b9ad0fe7…` — 1 literal-discriminant pair (silent), 4 `unknown` |
| 8 | `compare-javascript-export-shapes /tmp/cmp-modnames-in.json` | 0 | 5,312 | `ev_f45fc64e…` — `unavailable` ×2 (const export, no callable link) |
| 9 | `compare-javascript-export-shapes /tmp/cmp-bogus-in.json` | 0 | 11,880 | `ev_cdc468c3…` — `missing`, 24-candidate census returned |
| 10 | `compare-javascript-export-shapes /tmp/cmp-crossfile-in.json` (62.98 MB: app.asar + obsidian.asar Evidences) | 0 | 7,595 | `ev_99b42bc2…` — left `selected`, right `missing` (8 bindings only) |
| 11 | `analyze-javascript-application /tmp/mini-{a,b}` (v1 `module.exports={…}`) | 0 | ~46 KB ea | `default` binding only, no shape obs — fixture revised |
| 12 | `analyze-javascript-application /tmp/mini-{a,b}` (v2 `exports.X=function`) | 0 | 54,771 / 55,031 | `ev_6e6e173b…` / `ev_f36db5b9…`; bindings+shapes for `config`,`tags` |
| 13 | `compare-javascript-export-shapes /tmp/cmp-mini-config-in.json` | 0 | 6,549 | `ev_ec6d721d…` — `complete-within-inputs`: `changed /mode`, `added /extra`, `added /nested/second` |
| 14 | `compare-javascript-export-shapes /tmp/cmp-mini-tags-in.json` | 0 | 5,009 | `ev_71ed7485…` — `added /2` (array index as JSON Pointer) |
| 15 | `compare-javascript-export-shapes /tmp/cmp-mini-rev-in.json` (b→a) | 0 | 6,553 | `ev_c330884f…` — `removed:2, changed:1` symmetric |
| 16 | `compare-javascript-export-shapes /tmp/cmp-mini-ref2-in.json` (`{"kind":"retained-evidence"}` + full 64-hex ids) | 1 | 2,933 | `invalid_input` — retained-ref form rejected on CLI (MCP-session only) |

Failures/negatives, all recorded as evidence: (a) `browserModuleNames` selector `unavailable` — const exports never get return shapes; (b) bogus selector `missing` — candidate census is the recovery path; (c) cross-file compare degraded to `missing` on the budget-truncated 25 MB bundle; (d) retained-ref CLI rejection; (e) first fixture form produced no shape observations. No silent failures; every negative carried a typed reason.

## Summary

`compare-javascript-export-shapes` (CLI `rea compare-javascript-export-shapes`, operation `compare_javascript_export_shapes`, predicate `rea.javascript-export-shape-comparison`, provider `rea-javascript-application-workflows`) is exercised end-to-end — the last unexercised compare verb from the r3 coverage map. Shape taxonomy observed: `value_status ∈ {literal, union, object, array, unknown, ambiguous, cycle}` per projected return shape; field `state ∈ {literal, union, unknown}` with `presence ∈ {present, absent, unknown-coverage}`; change `status ∈ {added, removed, changed, unknown}` keyed by JSON Pointer (array indices included: `/2`); per-change `evidence_links` bind both source Evidences; `coverage.status ∈ {complete-within-inputs, partial, truncated}`; selector `status ∈ {selected, missing, ambiguous, unavailable}`. Diff classification observed live: `changed` (literal→literal), `added`/`removed` (literal↔absent), `unknown` (unpaired variants / unresolved selectors). Core semantics, all verified: **variant pairing requires a unique exact literal discriminant — never source order** (5v5 `serialize` variants paired ZERO despite same arity); paired-but-identical variants emit no row (`unchanged` isn't a status); `partial` upstream graph coverage forces comparison `partial`; selector `missing` returns the full binding census while `unavailable` means binding-without-shape-observation (const/non-callable exports). Practical gates discovered: CLI takes only full inline Evidence (retained-ref is MCP-only; real-bundle requests run 24–63 MB); `export-return-shapes` exist only for callable exports reached via `recover-module-export` links — `module.exports = {…}` shorthand and const exports are out of scope; and budget-truncated bundles (obsidian.asar's 8 surviving bindings) can't feed meaningful cross-artifact diffs. All eight compare verbs in the family are now exercised.
