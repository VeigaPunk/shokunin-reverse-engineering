<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/05-runtime-obs.md. -->

# 05 — Runtime-observation surface: self-launched CDP endpoints

r2 closed this axis as "viable via self-launched CDP" (14-frontier-scan.md:134)
with zero live endpoints — nothing was bindable. r3 launches its own Chromium
(:9222) and Electron 43 (:9223, under `xvfb-run`) instances and binds REA verbs
to them. All endpoints, pages, and app dirs were self-owned, loopback-only, and
removed after the run.

## Candidates

- claim: `rea list-browser-targets <endpoint>` enumerates HTTP(S) page targets
  on a caller-launched loopback CDP browser; `about:blank` and non-page targets
  are excluded with named reasons.
- source: `chromium --headless --remote-debugging-port=9222
  --user-data-dir=/tmp/kaidoku-chrome about:blank`; page target created via
  `PUT /json/new?http://127.0.0.1:8877/` (page served by self-owned
  `python3 -m http.server 8877 --bind 127.0.0.1`).
- verify: `npx -y rea-agents@6.4.0 list-browser-targets http://127.0.0.1:9222
  --format json` → `targets:[{target_id:"0E006FC629947859C164F1A080D4B3A0",
  title:"kaidoku-r3-probe",url:"http://127.0.0.1:8877/",origin:
  "http://127.0.0.1:8877",attached:false}]`, `excluded:{disallowed_origin:0,
  unsupported_url:1,non_page:2}`; predicate `rea.browser-target-list`,
  provider `rea-cdp-browser` v2, confidence `observed`. Browser product
  `Chrome/152.0.7977.82` (HeadlessChrome).
- verified-at: 2026-10-13.
- suggested: admit — the browser-target listing leg is now demonstrated, not
  just doc-derived. `about:blank` counts as `unsupported_url`; only HTTP(S)
  page targets list.

- claim: `--allowed-origins` filters the listing by exact origin; it takes a
  bare scalar per flag (repeatable), not a JSON-array string.
- source: same live endpoint.
- verify: `list-browser-targets http://127.0.0.1:9222 --allowed-origins
  http://example.invalid` → `targets:[]`, `excluded.disallowed_origin:1`,
  limitation "Only page targets whose current URL matches an explicitly
  requested exact origin are listed." Passing `'["http://example.invalid"]'`
  as one token → `invalid_request`/`invalid_input` (retryable).
- verified-at: 2026-10-13.
- suggested: admit — origin filter works and errs closed; CLI array flags want
  repeated scalars.

- claim: `rea inspect-web-page <endpoint> <targetId>` performs one bounded
  passive inspection (default `observationMs` 500) and self-scopes
  `allowed_origins` to the target's current origin.
- source: same endpoint and target.
- verify: `inspect-web-page http://127.0.0.1:9222
  0E006FC629947859C164F1A080D4B3A0` → predicate `rea.web-page-inspection`,
  `capture_window` 500 ms, `frames`/`dom` (7 nodes)/`accessibility` structure
  returned; `completeness.status:"policy_filtered"` with
  `attach_limited_sections:[console_events,metadata,network_requests,
  websocket_connections,websocket_frames]` and six `not_approved` sections
  gated behind the include* flags; `dropped_events.total:0`.
- verified-at: 2026-10-13.
- suggested: admit — first live passive page inspection in the corpus; the
  include* flag surface (console text, JSON/WS body shapes, script sources,
  storage keys/fingerprints, a11y text) is the opt-in depth dial.

- claim: `rea list-electron-targets <endpoint>` enumerates local `file://`
  page targets on a caller-launched Electron CDP endpoint with no file-root
  allowlist.
- source: `xvfb-run -a /usr/lib/electron43/electron /tmp/kaidoku-electron
  --remote-debugging-port=9223` (minimal self-owned app: package.json +
  main.js + index.html; `electron --version` → v43.6.0; xvfb needed — no
  display on this host).
- verify: `list-electron-targets http://127.0.0.1:9223` →
  `targets:[{target_id:"00E07DCB39602F33A607D8B0AAD10779",title:
  "kaidoku-electron-probe",file_path:"/tmp/kaidoku-electron/index.html",
  attached:false}]`, `excluded:{unsupported_url:0,non_page:0}`; predicate
  `rea.electron-target-list`, provider `rea-cdp-electron` v1. Endpoint
  reports `Chrome/150.0.7871.250 ... Electron/43.6.0`.
- verified-at: 2026-10-13.
- suggested: admit — the Electron leg of the r2 frontier note is now held.
  Electron 43 needs a display (hence `xvfb-run`) and synthesizes
  `--user-data-dir` under `~/.config/<appname>` — both now measured facts.

- claim: `rea inspect-electron-page <endpoint> <targetId>` performs one
  bounded passive file-page inspection (default `observationMs` 100).
- source: same Electron endpoint/target.
- verify: `inspect-electron-page http://127.0.0.1:9223
  00E07DCB39602F33A607D8B0AAD10779` → predicate `rea.electron-page-inspection`,
  `capture_window` 100 ms, DOM 7 nodes, `completeness.policy_filtered`;
  scripts excluded `out_of_target_scope`×1 + `unattributed_origin`×2.
- verified-at: 2026-10-13.
- suggested: admit — closes the loop `list → inspect` on the Electron leg.

- claim: `rea inspect-web-network-capture` is strictly offline — it requires a
  caller-supplied local capture file and never touches a live endpoint.
- source: `--schema` (npx cache `rea-agents@6.4.0`).
- verify: `inspect-web-network-capture --schema` → required args
  `{capturePath:"Absolute local capture path", format: enum [har, mitmproxy]}`;
  options `record` (ordinal select) and `sensitiveValue` (literal redaction
  list). No endpoint parameter exists.
- verified-at: 2026-10-13.
- suggested: admit — confirms r2's read; the verb pairs with retained
  captures, not live observation.

- claim: `rea capture-browser-scenario <inputJson>` runs an explicit Playwright
  scenario; `browser.mode:"connect"` attaches to a supplied loopback CDP
  endpoint+target, executes declared actions, and disconnects without owning
  the process.
- source: schema walk of
  `dist/domain/browserScenario.js`/`browserScenarioValues.js` in the npx
  package: input is strictObject `{browser: launch{executable_path,headless} |
  connect{cdp_endpoint,target_id}, start_url{url,query[]}, actions[min 1],
  environment?, storage?, secrets?, capture?}`; actions = goto|click|fill|
  press|select_option|check|uncheck|wait_for|wait_for_timeout.
- verify: scenario `{mode:"connect",cdp_endpoint:"http://127.0.0.1:9222",
  target_id:"0E006FC…", start_url:"http://127.0.0.1:8877/",
  actions:[{step_id:"wait-1",action:"wait_for_timeout",duration_ms:250}]}` →
  predicate `rea.browser-scenario-capture`, provider
  `rea-playwright-browser-scenario` v1, `browser.process_ownership:
  "external"`, `cleanup:"disconnected-external"`, steps `goto_start`+`wait-1`,
  `duration_ms:288`, `scenario_sha256` recorded. Playwright core +
  chromium-1248/headless-shell cache present on this host.
- verified-at: 2026-10-13.
- suggested: admit — active scenario capture is demonstrated end-to-end in
  connect mode; `launch` mode (owned temp profile, `executable_path`) is
  schema-admitted but unexercised here.

## Run log

1. `mkdir -p /tmp/kaidoku-chrome`; `chromium --headless
   --remote-debugging-port=9222 --user-data-dir=/tmp/kaidoku-chrome
   about:blank &` → `/json/version` answers `Chrome/152.0.7977.82`,
   HeadlessChrome UA. (System chromium also auto-injected
   `--ozone-platform=headless` + omarchy default flags; harmless.)
2. `/json/list` showed only `about:blank` + browser_ui/service_worker targets;
   first `list-browser-targets` → `targets:[]`, `unsupported_url:1`,
   `non_page:3`.
3. `python3 -m http.server 8877 --bind 127.0.0.1` in `/tmp/kaidoku-www` serving
   a one-line probe page; `curl -X PUT /json/new?http://127.0.0.1:8877/` opened
   the page target.
4. `list-browser-targets` re-run → http page enumerated (see candidate 1);
   `--allowed-origins` filter check both ways (see candidate 2).
5. `inspect-web-page` on the target, defaults only (see candidate 3).
6. `xvfb-run -a /usr/lib/electron43/electron /tmp/kaidoku-electron
   --remote-debugging-port=9223` → `/json/version` answers
   `Electron/43.6.0`/`Chrome/150.0.7871.250`; `list-electron-targets` and
   `inspect-electron-page` verified (candidates 4–5).
7. `capture-browser-scenario` connect-mode scenario, one 250 ms
   `wait_for_timeout` action, loopback-only (candidate 7).
8. Cleanup: killed only the launched chromium tree (PIDs ~68819+children
   sharing `--user-data-dir=/tmp/kaidoku-chrome`), electron tree
   (`--remote-debugging-port=9223` + xvfb-run wrapper), and the http.server
   (PID 71424). Ports 9222/9223/8877 verified closed; no stray Xvfb. Removed
   `/tmp/kaidoku-chrome`, `/tmp/kaidoku-electron`, `/tmp/kaidoku-www`,
   `/tmp/kaidoku-scenario.json`, three launch logs, and electron's
   `~/.config/kaidoku-probe` user-data dir. A sibling lane's
   `/tmp/kaidoku-r3-*` artifacts and its libjq search process were left
   untouched.
9. Note for future lanes: `pkill -f` on a literal flag string self-matches the
   calling shell — bracket one character or kill by PID.

## Summary

Runtime observation is **held**, no longer frontier. The r2 blocker (zero live
CDP endpoints) was self-imposed — every verb bound on first contact against
self-launched loopback instances:

- Browser leg: `list-browser-targets` (enumerate + origin filter),
  `inspect-web-page` (passive, policy-filtered depth dial) — confirmed.
- Electron leg: `list-electron-targets` + `inspect-electron-page` on
  electron43 via xvfb — confirmed; `capture-electron-scenario` exists and is
  the obvious next probe.
- Active leg: `capture-browser-scenario` connect-mode — confirmed end-to-end
  (`disconnected-external` cleanup); `launch` mode untested.
- Offline leg: `inspect-web-network-capture` — schema-confirmed HAR/mitmproxy
  intake only.

Remaining frontier within this axis: `observe-web-session`,
`observe-web-execution`, `list-javascript-runtime-targets` /
`observe-javascript-runtime` (V8 inspector — needs `--inspect` on a Node or
electron main process), `capture-electron-scenario`, `capture-web-screenshot`,
and `reconcile_javascript_runtime` (needs static + runtime evidence pair).
All are now executable: the binding recipe is `--remote-debugging-port` (+
`xvfb-run` for electron) against a self-owned instance.
