<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/08-observe-verbs.md. -->

# 08 — Runtime-obs surface: observe/reconcile verbs (r4)

r3-05 held enumerate/inspect/capture (`list-browser-targets`, `inspect-web-page`,
`list-electron-targets`, `inspect-electron-page`, `capture-browser-scenario`,
`inspect-web-network-capture` schema). This lane exercises the remaining
runtime-obs verbs from that file's "remaining frontier" list against two
self-owned loopback endpoints:

- `chromium --headless --remote-debugging-port=9222
  --user-data-dir=/tmp/kaidoku-r4-chrome` → `Chrome/152.0.7977.82`
  (HeadlessChrome, CDP protocol 1.3); page target
  `4FD99778D7FFAB5ED8DC9F222D7BAEB4` opened via
  `PUT /json/new?http://127.0.0.1:8878/` on a self-owned
  `python3 -m http.server 8878 --bind 127.0.0.1`.
- `node --inspect=0.0.0.0:9229 /tmp/kaidoku-r4-app/main.js` →
  `node.js/v24.21.0` (Inspector protocol 1.1); target
  `4ea0636d-1b5a-4f83-a315-32b46559ed89`. All REA calls used loopback only.

Exact names confirmed via `rea --llms`: `observe-web-session`,
`observe-web-execution`, `list-javascript-runtime-targets`,
`observe-javascript-runtime`, `capture-electron-scenario`,
`reconcile-javascript-runtime` (the dispatch's `list-javascript-runtime` /
`list-observe-javascript-runtime` guesses do not exist).

## Candidates

- claim: `rea observe-web-session <endpoint> <targetId>` records a bounded
  passive navigation-session timeline; it auto-scopes `allowed_origins` to the
  target's current origin when the caller passes none.
- source: `--schema` → args `{endpoint, targetId}` required; options
  `allowedOrigins[]` (exact-origin filter), `observationMs` (default 10000).
- verify: `--observation-ms 2500 --format json` → `ev_ac51acb0…`,
  predicate `rea.web-observation-session`, provider `rea-cdp-browser` v2.
  Echoed parameters show `allowed_origins:["http://127.0.0.1:8878"]` — the
  verb self-scoped (contrast `observe-web-execution` below). `window`
  armed 16:49:54.817Z → ended 16:49:57.321Z, `requested_ms:2500`,
  `end_reason:"window_elapsed"`; timeline = 5 lifecycle events
  (commit, domcontentloaded, load, networkalmostidle, networkidle) on the
  initial loader; `completeness.status:"attach_limited"` with
  `attach_limited_sections:["timeline"]`; `dropped_events.total:0`.
  Limitation verbatim: "An out-of-policy destination ends collection
  immediately and is recorded without its URL."
- verified-at: 2026-10-13.
- suggested: admit — session-observation leg held; the origin self-scoping
  and out-of-policy destination gate are now measured behavior, not doc text.

- claim: `rea observe-web-execution <endpoint> <targetId>` runs a bounded
  precise-coverage window: it resets V8 execution counters and disables
  optimized execution for the window, takes one resetting sample, never
  executes page code, and does NOT auto-scope `allowed_origins`.
- source: `--schema` → same arg/option shape as observe-web-session.
- verify: `--observation-ms 2500 --format json` → `ev_990bff76…`,
  predicate `rea.observe-web-execution`, provider `rea-cdp-browser` v2.
  Echoed `allowed_origins:[]` (no self-scoping — recorded asymmetry).
  `window` 2500 ms, `end_reason:"window_elapsed"`, producer start/sampled
  timestamps retained; `coverage.state:"captured"`, `offset_units:
  "utf16-code-units"`, `end_offset:"exclusive"`, `scripts:[]` — the probe
  page ships zero scripts, so the sample is empty by content, not failure;
  `script_inventory.main_document_scripts:0`, `coverage_absence:"unknown"`.
  `instrumentation` verbatim: `{resets_execution_counters:true,
  disables_optimized_execution:true, takes_one_resetting_sample:true,
  executes_selected_code:false, cleanup:"confirmed",
  page_ownership:"external"}`. Limitations flag the perturbation
  ("Timing and JIT behavior are affected") and the non-summing rule for
  nested ranges. Progress events (`rea_progress` 1/2→2/2) emit on stderr.
- verified-at: 2026-10-13.
- suggested: admit — instrumentation contract is verbatim-measured:
  passive-but-perturbing (counter reset + deopt) vs
  inspect-web-page's passive-nonperturbing. Empty coverage on a
  script-less page returns `captured`, not an error.

- claim: `rea list-javascript-runtime-targets <endpoint>` enumerates V8
  Inspector targets, but a Node target is bindable only when its reported
  `file://` URL resolves to a real on-disk file — `node --inspect -e …`
  reports bare `file://` and is excluded `unsupported_location`.
- source: `--schema` → args `{endpoint}` only ("Literal-loopback Inspector
  endpoint"); gating logic read in npx cache
  `dist/inspector/JavaScriptRuntimeScope.js` +
  `dist/browser/ElectronFileScope.js` (`authorizeRuntimeTargetLocation` →
  `authorizedElectronFile` = stat + realpath of the file URL, or `.asar`
  member resolution).
- verify: on the dispatched `node --inspect=0.0.0.0:9229 -e
  'setInterval(()=>{},60000)'` (target `url:"file://"`) → `ev_c5de5bef…`,
  `targets:[]`, `excluded:{unsupported_location:1,unconnectable:0}`.
  After relaunch on `/tmp/kaidoku-r4-app/main.js` → `ev_8ec03b37…`,
  `targets:[{target_id:"4ea0636d-…",protocol_type:"node",attached:false,
  location:{kind:"file",file_path:"/tmp/kaidoku-r4-app/main.js"}}]`,
  excluded all-zero. Runtime header `product:"node.js/v24.21.0"`,
  `protocol_version:"1.1"`; provider `rea-v8-inspector` v1.
- verified-at: 2026-10-13.
- suggested: admit — the `file://`-must-stat rule is the binding contract
  for this verb family; the dispatch's `-e` target is inherently
  unobservable. Documented for future lanes: run `--inspect` on a real
  file.

- claim: `rea observe-javascript-runtime <endpoint> <targetId>` performs a
  bounded passive V8 capture (Runtime.enable + Debugger.enable only); the
  caller-declared `runtime_kind` is echoed as
  `caller-declared-unverified`.
- source: `--schema` → options `runtimeKind` enum
  `[node|electron-main|electron-preload|electron-renderer]`,
  `observationMs` (default 100).
- verify: `--runtime-kind node --observation-ms 500 --format json` →
  `ev_9d0db442…`, predicate `rea.javascript-runtime-observation`,
  provider `rea-v8-inspector` v1. `target.runtime_kind:"node"`,
  `runtime_kind_authority:"caller-declared-unverified"`. `capture`:
  `events_observed:83`, `events_retained:83`, `events_dropped:0`,
  `metadata_bytes_retained:62210`, `truncated:false`. `scripts.items`: 82
  — 81 `node:` builtins (`location.kind:"builtin"`, each with `cdp_hash` +
  `length`, `status:"observed-loaded"`) + `main.js` (`kind:"file"`).
  `execution_contexts:[{name:"node[113122]",state:"created"}]`;
  `directly_observed` names only scriptParsed/context-lifecycle;
  `unavailable_without_instrumentation` lists require/import edges,
  EventEmitter, Electron IPC, unload events.
- verified-at: 2026-10-13.
- suggested: admit — first V8-inspector capture in the corpus; the
  builtin-vs-file location split and the unverified-runtime-kind marker
  are the reconciliation inputs this verb exists to produce.

- claim: `rea reconcile-javascript-runtime <inputJson>` reconciles
  caller-supplied Evidence objects (not evidence store lookups):
  `{static_layers:[{role, analysis:<Evidence>, runtime_mappings[]}],
  runtime_observations:[<Evidence>]}`, requiring exactly one
  `role:"application"` layer and unique evidence ids.
- source: `--schema` shows only `{inputJson}`; inner schema read in npx
  cache `dist/domain/javascript/javascriptRuntimeReconciliationSchemas.js`
  (strictObject; `runtime_mappings` = `file-root{root,artifact_prefix}` |
  `url-prefix{prefix,artifact_prefix}`; capture parsing accepts
  `inspect_web_page`, `inspect_electron_page`,
  `observe_javascript_runtime`, `capture_electron_scenario` Evidence).
- verify: built `static_layers:[{role:"application",
  analysis:<ev_93b0f984…>}]` — produced live by
  `analyze-javascript-application /tmp/kaidoku-r4-app` (directory format,
  6 graph nodes, `root_artifact_sha256:f2e5f4ce…`) — plus
  `runtime_mappings:[{kind:"file-root",root:"/tmp/kaidoku-r4-app",
  artifact_prefix:""}]`; `runtime_observations:[<ev_9d0db442…>]`. →
  `ev_032f373f…`, predicate `rea.javascript-runtime-reconciliation`,
  provider `rea-javascript-runtime-reconciliation` v1.
  `summary:{runtime_targets:1, runtime_scripts:82, matched:1,
  ambiguous:0, unmatched:1, unknown:81, static_loaded:1,
  static_resident:1}`. The `main.js` runtime script → `status:"matched"`,
  `basis:"artifact-path"`, `reason:"unique-location-match"`,
  `confidence:"medium"` onto the static `javascript-asset` node; the
  runtime target entity → `unmatched`/`no-static-content-match`; the 81
  builtins → `unknown`/`no-authorized-location-mapping` (mappings are
  caller-declared authority, not inferred). `static_load_states`: asset
  `loaded` (`runtime-script-correspondence`), contained module
  `resident-in-loaded-asset` (`containing-asset-was-loaded`).
  `coverage.status:"partial"`, zero omitted items.
- verified-at: 2026-10-13.
- suggested: admit — the static↔runtime join is demonstrated end-to-end
  on live evidence; load-state semantics (loaded ≠ executed) and the
  explicit unknown bucket are exactly the discipline the province wants.

- claim: `rea capture-electron-scenario <inputJson>` takes
  `{executable_path, application_path, application_root?, args?,
  actions[]}` (strictObject; actions = click(selector), wait(duration_ms),
  renderer-reload, renderer-crash, deep-link) and launches an OWNED
  Electron via Playwright `_electron.launch` (executablePath + cwd +
  `-r electron-active-hook.cjs` + app path).
- source: `--schema` (`{inputJson}`) + npx cache
  `dist/domain/javascript/electronActiveObservation.js` (input schema) and
  `dist/browser/PlaywrightElectronActiveProvider.js` (launch mechanics,
  60 s startup bound, lineage-verified cleanup).
- verify: minimal self-owned app (`/tmp/kaidoku-r4-electron`:
  package.json + main.js BrowserWindow + index.html) against
  `/usr/lib/electron43/electron` v43.6.0 under `xvfb-run -a`, action list
  `[{step_id:"w1",kind:"wait",duration_ms:500}]`. Two bounded attempts —
  default args, then `args:["--no-sandbox","--disable-gpu"]` — both exit 1
  with the IDENTICAL typed refusal (verbatim):
  `{"error":"Electron analysis failed","code":"cleanup_incomplete",
  "category":"execution_failure","message":"Electron cleanup could not be
  verified: owned Electron lineage was unavailable; helper cleanup was not
  proven. Capture also failed: Provider rea-playwright-electron-active
  adapter failed during capture_electron_scenario. Inspect the reported
  process resources before launching another capture.","retryable":false,
  "details":{"operation":"capture_electron_scenario","reason":
  "cleanup_failed","cleanup":"incomplete","resources":
  ["owned_process_group","run:<uuid>","process-group:<pid>"],
  "cleanup_reason":"owned Electron lineage was unavailable; helper
  cleanup was not proven","execution_failure":"unreadable_output"}}`.
  Control probe: `xvfb-run -a electron /tmp/kaidoku-r4-electron
  --no-sandbox --disable-gpu` launches silently and stays up → the app and
  electron binary are fine; the failure is inside the provider's
  capture/lineage path (`unreadable_output` projects
  AnalysisProtocol/OutputError in `analysisErrorProjection.js`), so the
  unverified lineage correctly refuses `cleanup_incomplete` rather than
  reporting success. No stray electron/Xvfb processes after either
  attempt.
- verified-at: 2026-10-13.
- suggested: hold-as-refused — verb exercised, deterministic typed refusal
  recorded verbatim on this host's distro Electron 43. The error is
  `retryable:false` and names its owned-process-group resources; nothing
  leaked. Worth one retry probe only if a future lane has a packaged
  Electron app (`.asar`/dist build) rather than a source dir, since
  Playwright's electron driver handshake may behave differently there.

## Run log

1. `mkdir -p /tmp/kaidoku-r4-chrome /tmp/kaidoku-r4-www`; launched
   `chromium --headless --remote-debugging-port=9222
   --user-data-dir=/tmp/kaidoku-r4-chrome about:blank` →
   `Chrome/152.0.7977.82`; `node --inspect=0.0.0.0:9229 -e
   'setInterval(()=>{},60000)'` → inspector answered `node.js/v24.21.0`.
2. `rea --llms | grep` → exact verb names (see header note).
3. `--schema` on all six verbs; `capture-electron-scenario` and
   `reconcile-javascript-runtime` expose only `inputJson` — inner shapes
   recovered from npx cache `dist/domain/javascript/
   electronActiveObservation.js` and
   `javascriptRuntimeReconciliationSchemas.js`.
4. `python3 -m http.server 8878 --bind 127.0.0.1` (PID 104053) serving
   `/tmp/kaidoku-r4-www`; `PUT /json/new?http://127.0.0.1:8878/` → page
   target `4FD99778D7FFAB5ED8DC9F222D7BAEB4`.
5. `list-javascript-runtime-targets http://127.0.0.1:9229` → `targets:[]`,
   `unsupported_location:1` — the `-e` target reports bare `file://`.
   Read `JavaScriptRuntimeScope.js`: a Node `file://` location must
   stat+realpath to a regular file. Killed only my `-e` node (PID
   102307), relaunched `--inspect=0.0.0.0:9229
   /tmp/kaidoku-r4-app/main.js` (PID 113122) — 0.0.0.0 kept per dispatch,
   all REA access stayed loopback. Re-list → file-location target.
6. `observe-web-session` / `observe-web-execution` /
   `observe-javascript-runtime`, all bounded (2500/2500/500 ms), all
   exit 0 with `observed` confidence (candidates 1, 2, 4).
7. `analyze-javascript-application /tmp/kaidoku-r4-app` → static layer
   `ev_93b0f984…`; assembled reconcile input in /tmp;
   `reconcile-javascript-runtime` → `ev_032f373f…` (candidate 5).
8. `capture-electron-scenario` under `xvfb-run -a`, minimal owned app →
   typed refusal `cleanup_incomplete`/`unreadable_output`, reproduced
   identically with `--no-sandbox --disable-gpu` passthrough (candidate
   6). Manual xvfb electron launch of the same app succeeded →
   provider-path failure, not app failure.
9. Sibling-lane traffic observed and left untouched: PID 127612 (a
   `/tmp` schema-probe loop), PIDs 113304/113305
   (`/tmp/kaidoku-appimg` → `/tmp/kaidoku-r4-aja-full.*` —
   sibling r4 outputs sharing the `/tmp/kaidoku-r4-` prefix; NOT
   removed). `/tmp/.X0-lock` is the pre-existing host display.
10. Cleanup: killed only my processes — chromium parent PID 102293
    (whole tree, `--user-data-dir=/tmp/kaidoku-r4-chrome`), node
    inspector PID 113122, http.server PID 104053; ports
    9222/9229/8878 verified closed; no stray electron/Xvfb from my runs.
    Removed exactly my artifacts: `/tmp/kaidoku-r4-chrome`,
    `/tmp/kaidoku-r4-www`, `/tmp/kaidoku-r4-app`,
    `/tmp/kaidoku-r4-electron`, `~/.config/kaidoku-r4-electron`
    (electron-synthesized user-data), and my
    `/tmp/kaidoku-r4-{chromium,node,http,electron-manual}.log` +
    `{websession,webexec,jsrt,static,reconcile,reconcile-out,
    electron-cap,electron-cap2}{.json,.err}` files. Sibling files
    `/tmp/kaidoku-r4-aja-full.*` preserved.

## Summary

The runtime-observation frontier r3-05 left is now closed on the
observe/reconcile legs:

- **Held (live evidence):** `observe-web-session` (auto-scoped origin
  gate, lifecycle timeline, `attach_limited`), `observe-web-execution`
  (precise-coverage window, perturbation contract verbatim, no origin
  self-scope), `list-javascript-runtime-targets`,
  `observe-javascript-runtime` (82-script passive V8 capture,
  `caller-declared-unverified` runtime kind), and
  `reconcile-javascript-runtime` end-to-end — static `ev_93b0f984…` +
  runtime `ev_9d0db442…` → `ev_032f373f…` with `matched:1 /
  unmatched:1 / unknown:81` and loaded≠resident≠executed load states.
- **Binding rule discovered:** Node Inspector targets are observable only
  when their `file://` discovery URL resolves to a real file on disk;
  `node --inspect -e` is structurally unobservable
  (`unsupported_location`).
- **Held-as-refused:** `capture-electron-scenario` — deterministic typed
  refusal `cleanup_incomplete` + `execution_failure:unreadable_output`
  on distro electron43 under xvfb, reproduced with/without sandbox flags;
  app+binary proven healthy by control launch. No process leakage.
- **Asymmetries worth keeping:** session self-scopes `allowed_origins`,
  execution does not; runtime_kind is accepted but tagged unverified;
  reconcile treats caller `runtime_mappings` as declared authority and
  buckets everything unmapped as `unknown` rather than guessing.

Every verb in the r3-05 "remaining frontier" list is now either held by
evidence or held by a recorded typed refusal. Remaining adjacent
unexercised surface on this axis: `capture-web-screenshot` (named in
r3-05), `capture-native-ui-scenario` / `observe-native-ui` /
`observe-native-calls` (native-UI leg, different provider family).
