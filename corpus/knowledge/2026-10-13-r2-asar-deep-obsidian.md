<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/10-asar-deep.md. -->

# kaidoku-r2 · 10-asar-deep — `analyze-javascript-application` on Obsidian's real main-process bundle

Axes: **depth** (a real 54-entry application ASAR vs round 1's trivial stubs), **evidence-fidelity** (does REA's output survive independent checks — sha256, module paths, IPC literals), **paging-model** (summary→page→item chain through `inspect-analysis-view`), **failure-honesty** (typed refusals recorded, not smoothed over). Target: `/usr/lib/obsidian/app.asar`, `sha256 = 8588f1fd23c9f63d3507a9740d656252cf0fbe0538e00e5d8eb7660533416c52` (480,052 B), Obsidian 1.13.7 main-process bundle per r1.

## Candidate: `analyze-javascript-application` completes on the real Obsidian bundle — RC=0, 12.37 MB canonical Evidence

- claim: `timeout 900 npx -y rea-agents@6.4.0 analyze-javascript-application /usr/lib/obsidian/app.asar --format json` exits 0 and writes a single 12,367,708-byte Evidence JSON on stdout plus a 40-line `rea_progress` JSONL stream on stderr (inventory → read → 27× parse → application graph → semantic graph → seal → hash). Evidence binds the exact artifact: `subject.digest.sha256` and `normalized_result.root_artifact_sha256` both equal the independently measured `8588f1fd…52`; `predicate_type = rea.javascript-application-analysis`, `operation = analyze_javascript_application`, `provider.id = rea-javascript-application`, `confidence = derived`, `authority = shipped-artifact`, `parameters = {format: auto→detected asar, integrity_policy: fail}`, `integrity_contradictions: []`.
- source: run in `/tmp`, output at `/tmp/obsidian-app-analysis.json` (12,367,708 B) + stderr capture (6,969 B, 40 progress sequences, terminal `sequence: 40`); `sha256sum /usr/lib/obsidian/app.asar`.
- verify: `python3 -c 'import json; d=json.load(open("/tmp/obsidian-app-analysis.json")); print(d["evidence_id"], d["subject"]["digest"]["sha256"], d["normalized_result"]["statistics"])'`
- verified-at: 2026-10-13
- suggested: admit — round 1 only proved the verb exists; this is the first real end-to-end pass on a shipped app. Evidence ID `ev_039c8069b9bea1dc05e917047be39547cb8a89ff048857cef65924ce30fc5765` is the parent for every view below.

## Candidate: Graph census — 170-node application graph, 6,710-node semantic graph, 1,995 declared unknowns

- claim: `normalized_result.graph` (`schema: JavaScriptApplicationGraph`) holds 170 nodes / 221 edges — node kinds: `javascript-module` 90, `asar-entry` 27, `javascript-asset` 19, `ipc-channel` 15, `artifact` 7, `package` 5, `ipc-handler` 2, `native-export` 2, `native-addon` 2, `electron-main` 1; edge relations: `imports` 76, `contains` 53, `exposes` 46, `maps_to` 28, `sends` 13, `loads` 3, `handles` 2. `semantic_graph` holds 6,710 nodes (top kinds: `expression` 4,507, `call-site` 681, `property-slot` 384, `binding` 382, `parameter` 269, `return-site` 195, `function` 186) / 6,344 relations (top: `aliases` 1,978, `reads` 1,600, `defines` 762, `reads-property` 483, `captures` 451, `returns-to-call` 417, `argument-to-parameter` 293, `calls` 170), 184 fingerprints, 319 evidence contexts, and 1,995 explicit unknowns partitioned by family (object-flow 820, data-flow 637, call-flow 515, promise-ownership 17, event 6). Statistics: `relevant_files` 27, `parsed_javascript_files` 19, `visited_ast_nodes` 9,464, `text_bytes_read` 90,843, `parse_failures` 0, `invalid_utf8_files` 0, `findings` 135, `modules` 0.
- source: python census of `/tmp/obsidian-app-analysis.json` (`Counter` over `graph.nodes[].kind`, `graph.edges[].relation`, `semantic_graph.*`).
- verify: rerun the census; summary view (below) independently reports the same statistics block.
- verified-at: 2026-10-13
- suggested: admit — measured. Unknowns are first-class typed records (`jsrg_unknown_<sha256>`), not silent gaps — matches the "missing findings do not establish absence" limitation.

## Candidate: The entire observed IPC surface is `@electron/remote` internals; Obsidian's own main.js registers nothing statically

- claim: `summary.ipc` reports 15 operations: 2 literal channels + 13 dynamic-channel operations, 13 renderer transmissions, 1 renderer listener, 1 main handler, 0 paired, 2 unpaired literal renderer transmissions. Both literals sit in `node_modules/@electron/remote/dist/src/renderer/remote.js` — `REMOTE_BROWSER_DEREFERENCE` (renderer `send`, line 16) and `REMOTE_BROWSER_WRONG_CONTEXT_ERROR` (send, line 339). All 13 dynamics are `@electron/remote`'s `command`/`channel` parameter expressions (renderer `send`/`send-sync`, plus one main-side `on` listener at `dist/src/main/server.js:313`). Obsidian's own `main.js` contributes zero ipc-channel/ipc-handler nodes — consistent with r1's finding that Obsidian initializes `@electron/remote` (generic privileged dispatch) rather than declaring channels. `browser_windows` 0, `explicit_web_preferences` 0, `preload_entrypoints` 0, `context_bridge_apis` 0 — the renderer payload lives in sibling `obsidian.asar`.
- source: `normalized_result.summary.ipc`; per-node dump of `ipc-channel`/`ipc-handler` observation properties + `evidence.location.value` source ranges.
- verify: `python3` filter of `graph.nodes` where `kind in (ipc-channel, ipc-handler)` printing `properties` + location — 17 rows, all under `node_modules/@electron/remote/`.
- verified-at: 2026-10-13
- suggested: admit — every claim is a verbatim observation with a source range; the "main.js registers nothing" half is correctly framed as absence-of-observation inside recorded partial coverage, not proof of absence.

## Candidate: Both native addon bindings resolve inside the archive — btime and get-fonts, matching r1's `.unpacked` survey

- claim: `summary.native_addon_bindings: 2`, `resolved_native_addon_bindings: 2`. The two `native-addon` nodes name `node_modules/btime/binding.node` (50,896 B, `art_5e78dfed1d1b42df0aaa25142f5bb4b5fc82f085892c68cd3e2e7bcd90ea…`) and `node_modules/get-fonts/binding.node` (52,160 B, `art_768d2a0253b9f7a04e61efba06b99177d8abe489a94bda39e053d420…`), each with a `native-export` `./binding.node` request edge — the same two ELF natives round 1 found in `app.asar.unpacked/`. REA's ASAR inventory sees them as archive members; per its own limitation, "requested .node member is not a verified native export."
- source: `graph.nodes` where `kind == native-addon`, observation properties + `inventory_artifact_id`.
- verify: `python3` dump of native-addon/native-export nodes; cross-check `find /usr/lib/obsidian/app.asar.unpacked -name binding.node` (r1 evidence).
- verified-at: 2026-10-13
- suggested: admit — independent confirmation across two probes (r1 filesystem survey, r2 static analysis).

## Candidate: `inspect-analysis-view` delivers the documented summary→page→item paging chain on real output

- claim: With `{"source":{"kind":"inline","evidence":<12.37 MB bundle>},"view":…}` passed as a JSON file path, three projections succeed, each minting a NEW Evidence record linked by `parent_evidence_id` to `ev_039c8069…`:
  - `{kind:"summary"}` → `ev_547a4a64aa47151b48494179fac83f3707ada6c27bf72cb8d526228765c54646` (12 KB): statistics + electron summary + per-family coverage + `view_digest` `21d2c48f…`; coverage `complete-within-view` examined 109 / total 170.
  - `{kind:"page",collection:"modules",offset:0,limit:16}` → `ev_d857d5444009312684fcd35a5f6b639499c736d3259cc1ed4029fff359643315`: 16 identity rows (`node_id`, `kind`, `path` only — exactly the "pages return only identities" contract), `coverage:{status:"page",examined:16,total:109,next_offset:16,exhausted:false}`. Reissuing at `offset:16` → `ev_eed765cd37993b0e5d10ebd7d83e3e8dc55c3042345425c5faa007bfffefefcd`, `next_offset:32` — the cursor walks.
  - `{kind:"item",collection:"modules",selector:{node_id:"jag_node_6bc874…"}}` → `ev_9c5c51e95ef15b743236966186c832985d857abb537d2cd9527b937b591a9571`: the real `main.js` source-module node (identity key `8588f1fd…:main.js`, `semantic_role: source-module`), and `…selector:{node_id:"jag_node_081367…"}` → `ev_bcbbd13f…` (an unresolved `external:path` reference anchored to main.js).
- source: three `inspect-analysis-view` invocations (workflow files `/tmp/view-{summary,modules-p0,modules-p1,item-node,item-mainjs}.json`); outputs captured.
- verify: `rea inspect-analysis-view /tmp/view-summary.json --format json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["evidence_id"], d["normalized_result"]["parent_evidence_id"])'`
- verified-at: 2026-10-13
- suggested: admit — this is the SKILL.md "Work summary-first" doctrine (`detail:"summary"` → `parent_evidence_id` → `inspect_analysis_view`) exercised end-to-end on CLI, the missing r1 piece.

## Candidate: Item selection by `path` fails typed-and-useful on ambiguity — `main.js` anchors 19 module nodes

- claim: `selector:{"path":"main.js"}` returns `{"error":"Application workflow failed","code":"invalid_request","category":"invalid_input","retryable":true}` whose `details.issues[0]` says `Multiple modules have path "main.js"; select one by node_id.` and supplies an `expected` array of candidate `node_id`s. The census explains why: 19 `javascript-module` nodes carry `path: main.js` — one `source-module` (keyed `<root sha256>:main.js`) plus 18 unresolved-import reference nodes (`unresolved-reference` keys like `require:electron`, `require:fs`, `require:require(main)`, `dynamic-import:electron`; `unresolved-semantic-module` keys like `external:path`, `external:zlib`). The interesting fingerprint: Obsidian's main.js really does `require("require(main)")` — the self re-require bootstrap — and a dynamic `import("electron")`.
- source: error JSON from `/tmp/view-item-path.json` run; namespace census of main.js module nodes in the parent graph.
- verify: re-run item view with `selector.path:"main.js"` → same typed error; `python3` filter `identity.namespace` for nodes with path main.js → 19 rows.
- verified-at: 2026-10-13
- suggested: admit — proves the reference doc's "use selector.path only when uniqueness is established; on ambiguity select the matching node ID from the page or the error's candidates" is enforced behavior, and yields a real Obsidian bootstrap observation as a side effect.

## Candidate: `retained-evidence` references are session-scoped — they fail closed across CLI invocations

- claim: `{"source":{"kind":"retained-evidence","evidence_id":"ev_039c8069…"}}` fails `{"code":"evidence_integrity_mismatch","category":"integrity_mismatch","retryable":false,"message":"Evidence ev_039c8069… is not retained in this session. Supply complete inline Evidence, re-run its producer, or import its bundle before using this reference."}` — each CLI call is a fresh session with an empty retention store. The paging model on CLI therefore costs the full parent Evidence inline per call (12 MB JSON file input is accepted); retained IDs are an MCP-connection optimization only. The schema itself (`dist/domain/analysisView/analysisView.js:98-107`) admits exactly two source forms: `retained-evidence` (`ev`-prefixed digest) or `inline` (full `evidenceSchema`).
- source: run of `/tmp/view-retained.json` → RC 1 typed error; installed package source at `/home/vgpnk/.npm/_npx/af752b90495482d7/node_modules/rea-agents/dist/domain/analysisView/analysisView.js`.
- verify: `rea inspect-analysis-view /tmp/view-retained.json --format json` → same error; `grep -n 'retained-evidence\|inline' dist/domain/analysisView/analysisView.js`.
- verified-at: 2026-10-13
- suggested: admit — honest negative that shapes the CLI playbook: analyze once, save the bundle, then view-page by file. Also records where the schema truth lives for future lanes.

## Candidate: Interpretation caveats — `modules: 0`, `findings: 135`, and every view mints its own Evidence ID

- claim: Three readings that would mislead if taken naively. (a) `statistics.modules: 0` does NOT mean "no modules": the counter tracks bundler-recovered modules (the limitations note "Webpack/Rspack factories were recovered from AST literals") and this is a plain CommonJS archive — the graph still holds 90 `javascript-module` nodes. (b) `findings: 135` has no inline array to enumerate; total app-graph observations sum to 204, so `findings` is a distinct graded-observation counter — treat it as a scalar statistic, not a list. (c) Every `inspect-analysis-view` projection is itself a sealed Evidence record (`predicate_type: rea.analysis-view`, provider `rea-analysis-view`) with a fresh `evidence_id` + `view_digest`; lineage flows through `parent_evidence_id`/`parent_digest`, never ID reuse. Also honest negative: the CLI verb has no `--detail summary` flag — `detail` is an MCP-schema option; on CLI the parent always returns inline in full, and `inspect-analysis-view` is the only pager.
- source: `statistics` block vs graph census; `--help`/`--schema` for both verbs (no `detail` option anywhere); view-output envelope inspection.
- verify: `rea analyze-javascript-application --schema` (args: path only; no detail); `rea inspect-analysis-view --schema` (args: inputJson only).
- verified-at: 2026-10-13
- suggested: admit — prevents three specific misreadings future lanes would otherwise repeat.

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `sha256sum /usr/lib/obsidian/app.asar` | `8588f1fd23c9f63d3507a9740d656252cf0fbe0538e00e5d8eb7660533416c52`, 480,052 B |
| 2 | `rea analyze-javascript-application --help` / `--schema` | args: `<path>`; opts `--max-heap-mb` (128–16384, def 1024), `--analysis-timeout-ms` (def 300000), `--artifact-format auto|asar|directory`, `--integrity-policy fail|record-and-continue` (def fail) |
| 3 | `timeout 900 rea analyze-javascript-application /usr/lib/obsidian/app.asar --format json` | RC=0 within the 280 s tool window; stdout 12,367,708 B Evidence; stderr 6,969 B = 40 `rea_progress` JSONL lines (27 sources parsed, 0 failures) |
| 4 | python census of parent Evidence | 170 nodes / 221 edges app graph; 6,710 nodes / 6,344 relations / 1,995 unknowns semantic graph; statistics `findings:135, modules:0, parsed_javascript_files:19` |
| 5 | `rea inspect-analysis-view /tmp/view-retained.json` (retained-evidence source) | RC=1 `evidence_integrity_mismatch` — not retained in fresh session; remediation names inline/bundle path |
| 6 | `rea inspect-analysis-view /tmp/view-summary.json` (inline + `{kind:"summary"}`) | RC=0 → `ev_547a4a64…`, parent `ev_039c8069…`, coverage complete-within-view 109/170 |
| 7 | `rea inspect-analysis-view /tmp/view-modules-p0.json` (page modules off 0 lim 16) | RC=0 → `ev_d857d544…`, `next_offset:16`, 16 identity rows |
| 8 | `rea inspect-analysis-view /tmp/view-modules-p1.json` (off 16 lim 16) | RC=0 → `ev_eed765cd…`, `next_offset:32` |
| 9 | `rea inspect-analysis-view /tmp/view-item-path.json` (`selector.path:"main.js"`) | RC=1 `invalid_request`/`invalid_input` — ambiguity error with 19 candidate node_ids in `expected` |
| 10 | `rea inspect-analysis-view /tmp/view-item-node.json` (`node_id jag_node_081367…`) | RC=0 → `ev_bcbbd13f…` — `external:path` unresolved-reference module item |
| 11 | `rea inspect-analysis-view /tmp/view-item-mainjs.json` (`node_id jag_node_6bc874…`) | RC=0 → `ev_9c5c51e9…` — real `main.js` source-module item (identity `8588f1fd…:main.js`) |
| 12 | `grep`/`read` of installed `dist/domain/analysisView/analysisView.js` + `cli/analysisViewCommands.js` | source schema = `retained-evidence` | `inline` discriminated union; views = summary | facet | item | page | native; collections sections|symbols|modules |

## Summary

The JS/ASAR analysis surface is proven end-to-end on a real shipped application: `rea-agents@6.4.0 analyze-javascript-application` digests Obsidian 1.13.7's 54-entry main-process `app.asar` into a 12.37 MB sealed Evidence bundle (`ev_039c8069…`, sha256-pinned to the artifact) containing a 170-node application graph plus a 6,710-node semantic graph with 1,995 explicitly typed unknowns. The reconstructed security surface is coherent and cross-confirms round 1: the only IPC channels observed are `@electron/remote` internals (2 literal `REMOTE_BROWSER_*` sends + 13 dynamic `command` dispatches, one main-side listener), zero BrowserWindow/preload/contextBridge observations in this bundle, and both native addons (btime, get-fonts binding.node) resolve. `inspect-analysis-view` supplies real summary→page→item paging over inline Evidence with `next_offset` cursors and typed ambiguity refusals — but `retained-evidence` IDs are session-scoped and fail closed on the per-invocation CLI, so the CLI playbook is: analyze once → save bundle → feed the file back for each view. Caveats recorded: `modules:0` counts bundler modules not graph nodes, `findings:135` is a scalar not a list, and each view mints a fresh Evidence ID chained by `parent_evidence_id`. No failures beyond the two honest typed refusals (missing retention, ambiguous path selector) — both of which encode correct operator guidance.
