<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/10-renderer-asar.md. -->

# kaidoku-r3 · 10-renderer-asar — `analyze-javascript-application` on Obsidian's 25 MB payload ASAR

Axes: **depth** (25,787,463 B / 380 entries vs r2's 480 KB / 54-entry launcher), **evidence-fidelity** (IPC channels, webPreferences, sender checks cross-verified against raw grep), **coverage-honesty** (resource-constraint partition mapped, not smoothed), **scaling-limits** (1 GiB default vs 8 GiB worker heap — two distinct walls), **tool-breadth** (`recover-javascript-sources`, `trace-application-feature` exercised). Target: `/usr/lib/obsidian/obsidian.asar`, `sha256 = a52a7daf1e2460bae03de80f2816604bd16a56cd374fbe5ce8d1a9ef5604059d`, Obsidian 1.13.7 (package.json `version`, matches r2's app.asar).

## Candidate: ASAR census — 380 entries: 274 lib/, 45 i18n/, 35 sandbox/, 12 public/, 14 root files

- claim: `npx @electron/asar list` yields exactly 380 paths. By extension: `bcmap` 168 (pdfjs CJK cmaps), `txt` 44 (i18n locales + mapping.txt), `md` 31 (sandbox vault), `js` 28, `woff` 23, `svg` 13, `pfb` 10, `ttf` 8, `.DS_Store` 5, `css` 4, `woff2` 3, `mjs` 3 (pdfjs), `html` 3 (index/help/starter), `wasm` 2 (openjpeg, qcms), `json` 2 (package.json, pdfjs version), `ts/png/icc` 1 each. Root scripts: `app.js` (3,876,459 B), `main.js` (199,730 B), `starter.js` (440,870 B), `help.js` (377,345 B), `worker.js` (239,283 B), `i18n.js` (133,013 B), `sim.js` (17,693 B), `enhance.js` (13,346 B). `package.json` declares `"main": "index.js"` — a file that does NOT exist in the archive.
- source: `sha256sum` (a52a7daf…59d, 25,787,463 B); `npx -y @electron/asar list` + awk census; per-file `extract-file` + `sha256sum` (app.js `8efbf581…9898`, main.js `25b0705d…c85f`).
- verify: re-run the asar list; diff against `/tmp/r3-asar-list.txt`.
- verified-at: 2026-10-13
- suggested: admit — measured.

## Candidate: `analyze-javascript-application` completes on the 25 MB renderer payload — RC=0, 47.66 MB Evidence

- claim: `timeout 900 npx -y rea-agents@6.4.0 analyze-javascript-application /usr/lib/obsidian/obsidian.asar --format json` exits 0 in ~3.5 min and writes a single 47,658,312-byte Evidence JSON on stdout plus a 50-line `rea_progress` JSONL stream on stderr (inventory → read → 37× parse → application graph → semantic graph → seal → hash). Evidence binds the artifact: `subject.digest.sha256` = `normalized_result.root_artifact_sha256` = `a52a7daf…59d`; `predicate_type = rea.javascript-application-analysis`, `provider.id = rea-javascript-application`, `confidence = derived`, `authority = shipped-artifact`, `parameters = {format: auto→asar, integrity_policy: fail}`, `integrity_contradictions: []`. Evidence ID `ev_e8a2c4ba61ff689cfe68b334714ff57b1b1cc392e5aa3e0509815d292a72b57e`.
- source: `/tmp/obsidian-renderer-analysis.json` + `/tmp/obsidian-renderer-progress.log` (terminal `sequence: 50`).
- verify: `python3 -c 'import json; d=json.load(open("/tmp/obsidian-renderer-analysis.json")); print(d["evidence_id"], d["subject"]["digest"]["sha256"])'`.
- verified-at: 2026-10-13
- suggested: admit — the tool scales to a real shipped 25 MB bundle within the default 1 GiB worker heap and 300 s per-source timeout, emitting partial-coverage limits instead of dying.

## Candidate: Graph census — 235-node application graph, 23,527-node semantic graph, 7,956 typed unknowns

- claim: `normalized_result.graph` holds 235 nodes / 344 edges — node kinds: `endpoint` 50, `javascript-module` 43, `asar-entry` 37, `javascript-asset` 32, `unknown` 29, `storage` 23, `worker` 8, `artifact` 6, `electron-renderer` 3, `source-map`/`package`/`electron-main`/`electron-preload` 1 each; edge relations: `contains` 91, `persists_to` 69, `calls` 69, `maps_to` 43, `loads` 32, `imports` 29, `exposes` 11. `semantic_graph` holds 23,527 nodes (top: `expression` 16,527, `call-site` 2,060, `property-slot` 1,731, `binding` 1,059) / 33,119 relations (top: `aliases` 18,085, `reads` 6,451, `defines` 2,338) / 589 fingerprints / 401 evidence contexts / 7,956 unknowns (object-flow 4,129, data-flow 1,896, call-flow 1,696, plus event/timer/boundary/child-process/configuration/request/promise-ownership/closure/resource-lifecycle). Statistics: `relevant_files` 37, `parsed_javascript_files` 32, `visited_ast_nodes` 4,247,312, `text_bytes_read` 16,070,215, `findings` 1,492, `modules` 0, `parse_failures` 0.
- source: python `Counter` census of `/tmp/obsidian-renderer-analysis.json`.
- verify: rerun the census; same counters reproduce.
- verified-at: 2026-10-13
- suggested: admit — measured; note endpoint labels are noisy (moment.js internals `months`/`seconds`, mathjax `\df@tag`, plus real URLs like `https://www.youtube.com/youtubei/v1/next` via `call:fetch`).

## Candidate: obsidian.asar is the REAL application — 45 literal `ipcMain` operations live in its `main.js`, not in r2's launcher

- claim: `summary.ipc` reports 45 operations — 45 literal channels, 0 dynamic, 45 `main_handlers`, 0 renderer transmissions. The detail lives on the `main.js` file node's `static_analysis.electron.ipc` (45 records, `side: "main"`, `handler_kind: "inline-function"`, each with a handler source range): 44× `ipcMain.on("<channel>")` — `terms, is-quitting, is-closing, desktop-dir, documents-dir, resources, version, policy, set-language, file-url, relaunch, update, check-update, disable-update, copy-asar, disable-gpu, insider-build, cli, frame, adblock-lists, adblock-frequency, print-to-pdf, vault, vault-list, vault-remove, vault-move, vault-open, vault-message, starter, help, sandbox, context-menu, request-url, open-url, trash, get-documents-path, get-sandbox-vault-path, get-default-vault-path, set-menu, update-menu-items, render-menu, set-icon, get-icon, create-browser-session` — plus 1× `ipcMain.handle("register-cli")`. Independent grep of extracted `main.js` reproduces all 45 literals 1:1. Cross-checks r2 exactly: the outer `app.asar` registers nothing itself (only `@electron/remote` channels) — it is a thin launcher; this 25 MB payload carries the entire privileged surface. Renderer side: `app.js` holds 64 `ipcRenderer` refs, `starter.js` 8, `help.js` 5 (grep).
- source: `graph.nodes[126].observations[0].properties.static_analysis.electron.ipc` in `/tmp/obsidian-renderer-analysis.json`; `grep -oE 'ipcMain\.(handle|on)\("' /tmp/main.js`.
- verify: `python3` dump of the electron block; `grep -c 'ipcMain' /tmp/main.js` → 45.
- verified-at: 2026-10-13
- suggested: admit — the "renderer asar" label understates it: this archive holds main.js (privileged) + app.js/worker.js (renderer) + 3 HTML entrypoints. Any audit of Obsidian's IPC must target obsidian.asar, not app.asar.

## Candidate: Two BrowserWindows, both `web_preferences_status: "dynamic"` — so `explicit_web_preferences: 0` while grep proves `contextIsolation:false, nodeIntegration:true, webviewTag:true`

- claim: `static_analysis.electron.browser_windows` holds 2 windows (main.js line 53 col 3078 `options_status: "dynamic"`, line 53 col 4419 `object-literal` options but `web_preferences_status: "dynamic"` both); `preload_path: null`. Summary therefore counts `explicit_web_preferences: 0` — NOT absence: the `webPreferences` objects sit inside spread-computed options (`...pe(g)`), which the analyzer honestly marks dynamic. Ground truth by grep: window 1 `{contextIsolation:!1, nodeIntegration:!0, nodeIntegrationInWorker:!0, spellcheck:!0, webviewTag:!0, affinity:"main-window"}`; window 2 `{contextIsolation:!1, nodeIntegration:!0}` — the maximally-privileged renderer posture, consistent with app.js needing Node. Mitigations also verified in source: `setWindowOpenHandler` → `{action:"deny"}` then re-opens with `sandbox:!0, nodeIntegration:!1, nodeIntegrationInWorker/SubFrames:!1, webSecurity:!0, plugins:!1, experimentalFeatures:!1, webviewTag:!1`; `will-navigate`/`will-frame-navigate` restricted to `^https?://`; a `will-attach-webview → preventDefault()`; and the main window's `attach-webview` handler deletes `preload`/`preloadURL` and forces `p.sandbox=!0`. One `sender_validations` record: `subject: "process-id"`, `mechanism: "comparison:==="`, `expected: dynamic "f.processId"`, `enforcement: "unknown"` (main.js line 69 col 1864).
- source: electron block on `main.js` node; `grep -oE 'webPreferences.{0,220}|will-navigate[^;]*|setWindowOpenHandler[^;]*|attach-webview[^;]*' /tmp/main.js`.
- verify: `python3` dump of `browser_windows`/`sender_validations`; grep literals as above.
- verified-at: 2026-10-13
- suggested: admit — read `explicit_web_preferences: 0` as "0 statically resolved", not "0 present"; the same caveat applies wherever `options_status` is `dynamic`.

## Candidate: Coverage partition is explicit — ~20 files kept inventory/static facts only; `app.js` OOM'd the 1 GiB worker

- claim: `limitations` carries ~24 `Resource constraint` records split into two classes: (a) "Owned JavaScript worker exhausted its heap" — `app.js`, `help.js`, `worker.js`, `starter.js`, `lib/defuddle.full.js`, `lib/pdfjs/wasm/openjpeg_nowasm_fallback.js` (during semantic phase); (b) "exceeds the parent's result budget" / "parent reserved its remaining result capacity" — `main.js`, `sim.js`, `lib/codemirror/*` (3), `lib/mathjax/*` (2), `lib/mermaid.min.js`, `lib/moment.min.js`, `lib/pdfjs/*` (4), `lib/pixi.min.js`, `lib/prism.min.js`, `lib/readability.js`, `lib/reveal/reveal.js`, `lib/scrypt.js`, `lib/turndown.js`. Each OOM file is recorded as an `unknown`-kind "parse scope" node; expanded files keep `static_analysis` (parse_status + references) on their `javascript-asset` node. app.js — the actual renderer — therefore contributed ZERO `ipcRenderer`/storage/endpoint detail to this Evidence beyond inventory.
- source: `normalized_result.limitations`; per-node `static_analysis`/`unknown` census.
- verify: `python3` count of limitation strings + node-kind filter.
- verified-at: 2026-10-13
- suggested: admit — this is the honest-coverage contract working at scale; but any claim about app.js internals needs either per-file analysis or a bigger budget (see next candidate).

## Candidate: `--max-heap-mb 8192` rerun shifts coverage but hits BOTH walls anyway — 8 GiB worker still OOM'd on app.js; the parent result budget is a separate, untunable cap

- claim: Second run `timeout 900 rea analyze-javascript-application … --max-heap-mb 8192` exits 0 → `ev_6cf34bde1dc26f90bbbbf757a10b789856c5b2e608d768263444fd88f2c60f47` (47,777,337 B). Diff vs default run: identical `statistics` (findings 1,492, visited_ast_nodes 4,247,312 — deterministic parse), identical security surface (ipc 45/45 literal, browser_windows 2, sender_validations 1), but graph grows to 285 nodes / 391 edges (`javascript-module` 43→84, `endpoint` 50→61, `imports` edges 29→71) while the semantic graph shrinks slightly (23,486 vs 23,527 nodes; unknowns 7,967 vs 7,956) and resource-limit entries grow to 33. `app.js`, `help.js`, `defuddle.full.js` STILL exhausted the worker at 8 GiB — pathological single-scope minified bundles — and "parent's remaining result capacity" dropped even more expansions (pixi, reveal, starter, sim now listed). Conclusion: worker heap is one wall (`--max-heap-mb`, 128–16384), the parent's aggregate result budget is a second wall with no CLI knob; raising heap redistributes WHICH facts survive rather than monotonically increasing coverage.
- source: `/tmp/obsidian-renderer-analysis-h8.json` + `/tmp/obsidian-renderer-progress-h8.log` (50 sequences); python diff of both bundles.
- verify: `python3` census of h8 bundle; `grep -c 'Resource constraint' ` on limitations.
- verified-at: 2026-10-13
- suggested: admit — operationally important: bigger heap ≠ more coverage, and the security surface (ipc/bw/sv counts) is the deterministic part. A per-file `analyze-javascript-application --artifact-format directory` pass on extracted app.js is the remaining escape hatch.

## Candidate: `recover-javascript-sources` fails closed with a typed capability error — external Wakaru binary required

- claim: `npx rea-agents@6.4.0 recover-javascript-sources /tmp/app.js /tmp/recovered-app --format json` → RC=1 `{"code":"capability_unavailable","category":"unsupported_provider","provider_id":"wakaru","retryable":false}` — message: provide an absolute `REA_WAKARU_COMMAND` pointing to a Wakaru ^1.13.0 Linux x64 binary (verified with 1.14.0); REA installs no recovery tool itself; remediation names `docs/javascript-recovery.md#install-wakaru`. Schema confirmed beforehand: args `{path (JS file), outputDirectory (must be absent)}`, options `extractionMode: structural|heuristic|inspection`, `rewriteLevel: minimal|standard|aggressive`.
- source: `/tmp/recover-app.json` (770 B error envelope), `/tmp/recover-app.err`.
- verify: rerun; same typed envelope.
- verified-at: 2026-10-13
- suggested: admit — honest negative; the verb is a provider shell. Unblocks only after installing Wakaru — flag to L0 if source recovery becomes a lane goal.

## Candidate: `trace-application-feature` works on this Evidence — module seed traces the whole graph; `channel` seed types an honest `no-match` because channel facts live on file nodes, not graph nodes

- claim: Input `{application:<Evidence>, native_observations:[], seed:{...}}` via JSON file. (a) `seed {kind:"channel", value:"open-url", match:"exact"}` → RC=0, `ev_a2e93f37b6c59fde57695bbb423c487336460f02d01780320d5e547fbcc241b3`, `coverage.status:"no-match"`, `matched_seeds:0`, limitation "No graph entity matched the literal seed; this is not evidence that the feature is absent" — correct behavior: this bundle records IPC inside `static_analysis.electron.ipc` on the main.js file node (parent-budget cut meant channel nodes were never projected into `graph.nodes`), so the graph-level seed misses what the file-level observation knows. (b) `seed {kind:"module", value:"app.js", match:"exact"}` → RC=0, `ev_3d267786f29d93e779196ba803f183206d70ed1cf897ec0b71c309cbd9cb1901`, `trace_id jatr_de8c7efeeda0…`, `source_evidence_id` = parent `ev_e8a2c4ba…`, `source_graph_id jag_b87d2d5d…`: 1 seed match (javascript-asset node by label basis), traced 235 nodes / 344 edges / 102 terminal paths (all seed→X single-edge, e.g. →endpoint), `observed_facts` 378, `inferred_facts` 262, `unavailable_facts` 29, `coverage:"partial"`.
- source: `/tmp/trace-openurl{,-out}.json`, `/tmp/trace-appjs{,-out}.json`; workflow schema from `dist/domain/javascript/javascriptFeatureTraceSchemas.js` (seed kinds: node-id|route|string|api|channel|module|native-export).
- verify: rerun either trace; `python3` print `normalized_result.summary`/`coverage`.
- verified-at: 2026-10-13
- suggested: admit — both outcomes are evidence (typed no-match IS a result, minted with lineage). Playbook note: for budget-truncated bundles, seed `module`/`node-id`/`string` — `channel` seeds only work where IPC survived into graph nodes (r2's small app.asar did project ipc-channel nodes; this one did not).

## Candidate: Entrypoint topology — `package.json:main → index.js` NOT-FOUND; preload specifier `metadata` unresolved-external; 3 HTML renderer entrypoints

- claim: The single `electron-main` node records `package.json` declaring `"main": "index.js"` → `resolution_status: "not-found"` ("No extension, directory package, or index candidate exists in the inventoried artifact container") — obsidian.asar is not launched via its own package entry; the outer app.asar launcher must load it by path (consistent with r2: app.asar's main.js bootstraps it). The single `electron-preload` node records `declared_path: "metadata"` via `module-specifier` → `resolution_status: "external"` ("No matching bare package was inventoried"). Three `electron-renderer` nodes resolve cleanly: `index.html`, `help.html`, `starter.html` (`mechanism: html-script-entrypoint`). Workers: `worker.js` + `/sim.js` specifiers observed among 8 worker nodes. Storage: 23 nodes — `local-storage`/`indexed-db` with Obsidian keys (`mobile-selected-vault`, `obsidian-vault-path`, `most-recently-installed-version`, `local-themes`, `communityPluginSortOrder`, `spellcheck-languages`, `vim`, `site-theme`). One `source-map` node (a sourcemap reference exists somewhere in the bundle — detail on the file node).
- source: `graph.nodes` filtered by kind; observation properties verbatim.
- verify: `python3` kind-filter dump.
- verified-at: 2026-10-13
- suggested: admit — the missing index.js is a real topology fact, not a bug: this asar is a payload, not a launchable package.

## Run log

| # | command | result |
|---|---------|--------|
| 1 | `sha256sum /usr/lib/obsidian/obsidian.asar` | `a52a7daf1e2460bae03de80f2816604bd16a56cd374fbe5ce8d1a9ef5604059d`, 25,787,463 B |
| 2 | `npx @electron/asar list` + awk census | 380 entries; 274 lib / 45 i18n / 35 sandbox / 12 public / 14 root; ext histogram (bcmap 168, txt 44, md 31, js 28, …) |
| 3 | `npx @electron/asar extract-file` ×8 + sha256 | app.js 3,876,459 B `8efbf581…`; main.js 199,730 B `25b0705d…`; worker/starter/help/i18n/sim/enhance digests recorded; package.json → version 1.13.7, `"main":"index.js"` |
| 4 | `rea analyze-javascript-application --schema` / `recover-javascript-sources --schema` / `trace-application-feature --schema` | schemas captured (path-only arg; maxHeapMb 128–16384 def 1024; analysisTimeoutMs def 300000; integrityPolicy fail|record-and-continue) |
| 5 | `timeout 900 rea analyze-javascript-application /usr/lib/obsidian/obsidian.asar --format json` | RC=0 ≈3.5 min; stdout 47,658,312 B Evidence `ev_e8a2c4ba…`; stderr 50 `rea_progress` sequences, 37 sources parsed, 0 parse failures |
| 6 | python census | 235n/344e app graph; 23,527n/33,119r semantic; 7,956 unknowns; findings 1,492; ipc summary 45 literal main_handlers |
| 7 | python electron-block dump (main.js node) | 45 ipc records (44 `on` + `handle register-cli`), 2 browser_windows (options/webprefs `dynamic`), 1 sender_validation (`process-id`, `===`, `f.processId`, enforcement unknown) |
| 8 | `grep` verification of `/tmp/main.js` | 45 `ipcMain` refs — channel literals match REA 1:1; `webPreferences{contextIsolation:!1,nodeIntegration:!0,nodeIntegrationInWorker:!0,webviewTag:!0}`; deny+locked windowOpen handler; https-only will-navigate; attach-webview strips preload/sandbox |
| 9 | `grep` verification of `/tmp/app.js` | 64 `ipcRenderer` refs — renderer side confirmed |
| 10 | `timeout 600 rea recover-javascript-sources /tmp/app.js /tmp/recovered-app` | RC=1 `capability_unavailable`/`unsupported_provider` — needs `REA_WAKARU_COMMAND` (Wakaru ^1.13.0 x64); no bundled tool |
| 11 | `rea trace-application-feature /tmp/trace-openurl.json` (channel seed) | RC=0 `ev_a2e93f37…` — `no-match`, 0 seeds (channels sit in file-node static_analysis, not graph nodes); honest "not evidence of absence" limitation |
| 12 | `rea trace-application-feature /tmp/trace-appjs.json` (module seed) | RC=0 `ev_3d267786…` — 1 match, 235n/344e traced, 102 terminal paths, 378 observed/262 inferred/29 unavailable facts, coverage partial |
| 13 | `timeout 900 rea analyze-javascript-application … --max-heap-mb 8192` | RC=0 `ev_6cf34bde…` (47,777,337 B); same statistics+security surface; graph 285n/391e; app.js/help.js/defuddle STILL heap-OOM at 8 GiB; parent result-budget entries grew to 33 |

## Summary

The 25 MB `obsidian.asar` is the real Obsidian application — the 480 KB `app.asar` analyzed in r2 is only its launcher. `rea-agents@6.4.0 analyze-javascript-application` digests it end-to-end in ~3.5 min into a 47.66 MB sealed Evidence bundle (`ev_e8a2c4ba…`, sha256-pinned): a 235-node application graph + 23,527-node semantic graph with 7,956 typed unknowns, `findings` 1,492, zero parse failures. The headline reconstruction: **45 literal `ipcMain` operations in `main.js`** (44 `on` channels — vault-*, open-url, request-url, print-to-pdf, copy-asar, register-cli `handle`, create-browser-session, trash, update machinery — each with a source range) verified 1:1 against grep, plus **2 BrowserWindows** whose `webPreferences` are honestly flagged `dynamic` but grep proves `contextIsolation:false, nodeIntegration:true, nodeIntegrationInWorker:true, webviewTag:true` — the classic Obsidian fully-privileged renderer, mitigated in-source by a deny-and-relock `setWindowOpenHandler` (sandbox:true, nodeIntegration:false, webviewTag:false), https-only `will-navigate`, `will-attach-webview` prevention, and preload-stripping webview attach. Exactly **1 sender validation** was observed (`process-id === f.processId`, enforcement unknown) against 45 handlers — the remaining 44 handlers show no static sender check in this Evidence. Coverage is honestly partitioned: ~20 large minified files hit resource limits — `app.js` (3.9 MB) OOM'd the analyzer worker even at `--max-heap-mb 8192`, and a second untunable "parent result budget" caps expanded relations; a rerun at 8 GiB produced a *different* coverage partition (285 vs 235 graph nodes) but an identical security surface, proving the surface deterministic and the budget the variable. Deeper tools: `recover-javascript-sources` fails closed typed (`capability_unavailable` — external Wakaru binary required, nothing bundled); `trace-application-feature` succeeds and mints lineage-chained Evidence — a `module` seed on `app.js` traces all 235 nodes / 102 terminal paths (378 observed facts), while a `channel` seed returns typed `no-match` because this bundle's IPC facts live on file nodes, not graph channel nodes. Next-round frontier: per-file analysis of extracted `app.js` via `--artifact-format directory`, or a Wakaru install, to crack open the renderer internals the 8 GiB worker still could not hold.

## Errata (round 4)

- **Verify-recipe defect (r4 audit-B, verified 2026-10-13):** `grep -c 'ipcMain'
  /tmp/main.js` counts matching LINES — on the 69-line minified file it yields 1, not 45.
  Correct recipe: `grep -o 'ipcMain' | wc -l` → 45 (44 `on` + 1 `handle` confirmed).
  Same defect in the renderer-side checks (`grep -c ipcRenderer` → 1 vs `grep -o|wc -l` →
  64/8/5). Claims all reproduce; the recorded verify commands were wrong as written.
- **Resource-constraint census (r4 audit-B):** exactly **29** `Resource constraint`
  records (6 heap-exhaustion + 22 named budget + 1 generic), not "~24". The hedge covered
  the direction and partition; the exact count is 29.
- **`inspect` ≡ `analyze` proven (r4 audit-B):** `rea inspect` produced an evidence_id
  byte-identical to `rea analyze` on the same input — normalized bundle → same evidence
  hash. The two commands are the same analysis.
