<!-- corpus entry — kaidoku-shokunin round 4 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4/06-1password-asar.md. -->

# 06 — 1Password `app.asar` (40.7 MB) — first analysis

Target: `/opt/1Password/resources/app.asar` — 1Password for Linux `8.12.42-32.BETA`
(package `@1password/oph`, `main: ./main.js`, Electron + Rust N-API core).
Tooling: `@electron/asar` (list/extract) + `rea-agents@6.4.0 analyze-javascript-application`
(`--format json --max-heap-mb 8192`), manual grep on extracted tree `/tmp/op-asar`.

---

## Candidates

### C1 — Bundle census

- **claim:** asar holds 423 inventory files: 415 `.js` (≈16.17 MB of JS text), 6 `.html`,
  5 `.css`, 3 `.woff2`, 22 `.svg`, 20 `.png`, 6 `.ico`, `package.json`,
  `vendors.js.LICENSE.txt`, `index.node` (stored unpacked). JS is one flat webpack-5
  bundle family (`webpackChunk_1password_oph`, 1,311 modules, 277 chunks): `main.js`
  (236,724 B), `preload.js` (2,994 B), `vendors.js` (2,433,386 B) + 5 renderer bundles
  (`primaryRenderer.js` 5,633,453 B / `secondaryRenderer.js` 2,709,230 B /
  `quickAccessRenderer.js` 503,134 B / `passkeyPromptRenderer.js` 502,707 B /
  `authPromptRenderer.js` 539,298 B) + ~400 numbered lazy chunks.
- **source:** `npx @electron/asar list` (486 lines incl. dirs); REA `statistics`
  {relevant_files:423, parsed_javascript_files:415, visited_ast_nodes:1,712,317,
  findings:3997, modules:1311, parse_failures:0, text_bytes_read:16,168,007}.
- **verify:** `sha256sum` on the asar; REA per-entry `entry_sha256` agrees for every
  sampled file (`index.node` sha256 matches `app.asar.unpacked/index.node` byte-for-byte).
- **verified-at:** 2026-10-13T16:5xZ, host sha256 `app.asar=769e0962…31e2d21`.
- **suggested:** none — baseline established; per-file sha256 table retained in Evidence
  `ev_40214dabc8444cedaa82d815e836ba7cfb8e677e723891c0fef112439d15c9c4`.

### C2 — Native core is the real application; JS is a thin shell

- **claim:** all vault/crypto/network logic lives in `index.node` (188 MB unpacked Rust
  N-API addon) + sibling `libop_sdk_lib_core.so` / `libop_sdk_ipc_client.so` in
  `/opt/1Password/`. `main.js` wraps it via `require` of the addon (webpack module 939 →
  `a().gql_invoke / gql_create_channel / gql_subscription_send / complete_future /
  localize / get_resource / webauthnSign / protect_process_memory / should_disable_seccomp /
  dev_tools_enabled / send_crash_reports …`). ≥59 distinct `core.invoke({type:…})`
  commands observed: `Lock, AuthPrompt, SystemUnlock, SilentUnlock, SecureCopy,
  CheckForOnlineUpdate, SyncAll, MigrateDataUsingImport, ImportSshKey,
  ApiGetUnlockedAccounts, GrantBrokeredAccess, CommitSigning, DesktopFill,
  AutoFillFromShortcut, OpenLogsDirectory, FeatureFlags, Sso*, Totp, TelemetryEvent,
  FrontendEvent, FrontendInitialized, ClientSettings, AppUrlFromEmergencyKit, …`
- **source:** `main.js` grep of `invoke({type:"…"` (59 unique), `a().*` native calls;
  `nm -D` on index.node.
- **verify:** `nm -D --defined-only index.node` → only 27 exported dynsyms incl.
  `napi_register_module_v1`, `rust_u2f_mgr_register`; ELF 64-bit LSB `DYN`, x86-64,
  **not stripped** (BuildID `ac08c3a1…b43`, ~150k symbol strings embedded).
- **verified-at:** 2026-10-13.
- **suggested:** JS-side analysis is done; the remaining risk frontier is `index.node`
  (explicitly inventoried only, per task scope — do NOT deep-analyze here).

### C3 — `index.node` + `app.asar.unpacked/` inventory

- **claim:** unpacked dir = `index.node` (187,997,016 B) + `CREDITS.html` (593,734 B);
  no other native payloads in the asar tree.
- **source:** `ls -laR`, `file`, `sha256sum`.
- **verify:** `index.node` sha256 `1cb3e361…fa7778` (matches asar `entry_sha256`);
  `CREDITS.html` sha256 `6ef045b5…d2ad4`; `file` → `ELF 64-bit LSB shared object,
  x86-64, dynamically linked, not stripped`.
- **verified-at:** 2026-10-13.
- **suggested:** inventory-only per instructions; candidates for later lanes —
  `nm`/`readelf` symbol census, `strings` for Rust crate versions/panic paths.

### C4 — Renderer hardening is strong and uniform

- **claim:** all 5 app windows share `webPreferences {preload: preload.js,
  nodeIntegration:false, contextIsolation:true, sandbox:true,
  disableBlinkFeatures:"Auxclick", devTools: a().dev_tools_enabled()}` inside class `Ha`;
  `Mr.app.enableSandbox()` is called globally at startup (sandbox cannot be opted out
  per-window). Every shipped HTML has
  `CSP: default-src 'none'; connect-src data: 'self'; base-uri 'none'; form-action 'none';
  img-src data: blob: 'self'; style-src 'self' 'unsafe-inline'; font-src 'self';
  script-src 'self'` — no remote script/connect, no `unsafe-eval`.
- **source:** `grep -oE` webPreferences keys in `main.js`; `<meta http-equiv=CSP>` in
  `primary/secondary/quickAccess/authPrompt/passkeyPrompt.html`.
- **verify:** identical CSP in all 5 HTML files; only `contextIsolation`, `sandbox`,
  `nodeIntegration`, `disableBlinkFeatures` appear as webPreference keys — no
  `webSecurity`, `allowRunningInsecureContent`, `webviewTag` overrides anywhere.
- **verified-at:** 2026-10-13.
- **suggested:** devtools flag is native-side (`dev_tools_enabled()`) — worth checking
  whether beta builds ship it on.

### C5 — Zero renderer network access by construction

- **claim:** `Mr.protocol.handle` and `persist:1password`-partition `n.protocol.handle`
  register `http`, `https`, `ws`, `wss` → `() => new Response` (empty 200) on BOTH the
  default session and the app partition; `resource` + `file-icon` are the only custom
  privileged schemes (`bypassCSP:true, supportFetchAPI:true, standard:true`), served from
  the native core (`fetchResource → core.get_resource`). `session.fromPartition(
  "persist:1password",{cache:!1})` — cache disabled. Renderer cannot fetch anything
  remote; all egress rides the Rust core's GraphQL channel.
- **source:** `main.js` (`Mr.protocol.handle("http…"`, `n.protocol.handle("wss…"`).
- **verify:** 4 schemes × 2 sessions enumerated by grep; `resource` handler logs a
  deprecation warning at runtime.
- **verified-at:** 2026-10-13.
- **suggested:** this collapses the exfil question onto IPC/graphql channels — prioritize
  those over DOM/network bugs.

### C6 — IPC surface: one contextBridge key, ~84-method allowlist, 2 multiplexers

- **claim:** `preload.js` runs `contextBridge.exposeInMainWorld("op", …)` ONLY when
  `window.location.protocol === "file:"`, exposing ~84 invoke wrappers +
  `{on,invoke,executeGql,executeGqlSubscriptionRequest/Response,send,sendPendingEvent,
  coreLog,pathFromFile(webUtils.getPathForFile)}`. Main side: class `Ca`/`ba` registers
  **80 literal `rpc.handle` channels** + `invoke` + `executeGql`; every handler wrapped in
  `if (e.senderFrame?.url.startsWith("file://")) … else throw 'unknown RPC user'`.
  REA: `context_bridge_apis:1 (api_key "op", world main, api_status dynamic)`,
  `ipc.operations:10` (invoke×3, send×4, on×3 — literal channels `invoke`, `executeGql`,
  `gqlSubscriptionRequest`, `gqlSubscriptionResponse`, `SendPendingEvent`, `CoreLog`),
  `sender_validation_observations:1` (`sender-url startsWith "file://"`, enforcement
  "unknown"). Main→renderer: ~40 event channels (`gqlSubscriptionResponse`,
  `SendPendingEvent`, `UnlockWithSso`, `ShowToastNotification`, `InitialAuthPromptData`,
  `InitialPasskeyPromptData`, `ImportLoginSso`, `DuoMfaTimeout`, `EmbeddedAuthFallback`,…).
- **source:** `preload.js` verbatim (read in full, 2,994 B); `main.js` grep of
  `this.rpc.handle("…"` (80 unique); REA electron observations on `preload.js` node.
- **verify:** preload/mains sha256 `7e7a6888…` / `b4b5d16f…` (REA `entry_sha256`).
- **verified-at:** 2026-10-13.
- **suggested:** the file:// guard is the ONLY per-message check observed — no
  `senderFrame.url` allowlist beyond the scheme prefix, no `webContents` identity check
  in the wrapper itself (some handlers then `BrowserWindow.fromWebContents(e.sender)`).

### C7 — `invoke` is an unrestricted typed-command bridge (headline surface)

- **claim:** `rpc.handle("invoke", (e,t,n) => this.core.invoke({type:t, content:n}))` —
  the renderer supplies BOTH the command type and payload; the preload `op.invoke(type,
  …args)` forwards verbatim. Likewise `executeGql` → `core.executeGql(t)` (full GraphQL
  to core) and `gqlSubscriptionRequest/Response`. Therefore any script execution inside a
  `file://` renderer (XSS in primary/secondary/quickAccess/authPrompt/passkeyPrompt) can
  drive the complete privileged command surface — `SecureCopy`, `SystemUnlock`,
  `SilentUnlock`, `AuthPrompt{unlock,approve}`, `ImportSshKey`, `ApiGetUnlockedAccounts`,
  `CheckForOnlineUpdate`, `MigrateDataUsingImport`, etc. — subject only to the core's own
  authorization (in index.node, unanalyzed).
- **source:** `main.js` (`handle("invoke"` handler body).
- **verify:** cross-checked against preload: `invoke:(n,…t)=>ipcRenderer.invoke("invoke",
  n,…t)` — no allowlist on type.
- **verified-at:** 2026-10-13.
- **suggested:** severity hinges on whether `index.node` re-authorizes per command;
  flag for native-side follow-up. Also note `secureCopy` → `core.invoke({type:"SecureCopy"})`
  is ALSO reachable directly (defense-in-depth duplication).

### C8 — Navigation + window-open lockdown

- **claim:** `will-attach-webview` → `preventDefault()`; `will-navigate` →
  `preventDefault()` + `urlService.openUrlInBrowser(t)`; `setWindowOpenHandler` →
  `{action:"deny"}` + bounce URL to the system browser. In-app navigation to any remote
  origin is impossible by construction.
- **source:** `main.js` session/webContents wiring.
- **verify:** grep hits confirm all three hooks on the app session.
- **verified-at:** 2026-10-13.
- **suggested:** none — this is the correct pattern.

### C9 — `shell.openExternal` protocol allowlist

- **claim:** `openUrlInBrowser` validates `new URL(e).protocol ∈ {https:, http:,
  onepassword:, onepassword8:, mailto:, x-safari-https:}` else throws
  "URL does not have a valid protocol"; then `shell.openExternal`. `openLink`/`openCustomUrl`
  IPC routes through it. No `file:`/`javascript:`/`data:` — good. `onepassword:`/
  `onepassword8:` are dispatched to the OS → re-enter this app via deep-link handling
  (see C10).
- **source:** `main.js` `openUrlInBrowser`.
- **verify:** literal protocol list grep.
- **verified-at:** 2026-10-13.
- **suggested:** `x-safari-https:` is a safari-extension scheme — dead on Linux but live
  in shared code; `mailto:` bodies are renderer-influenced (search link builds
  `?q=selectionText`).

### C10 — Deep-link / instance entry points

- **claim:** `onepassword://` ingestion has 4 doors: macOS `app.on("open-url")`,
  `second-instance` argv, first-instance `commander` CLI (`nc()`: `[url]`,
  `--disable-gpu`, `--lock`, `--silent`), `app.on("open-file")` (Emergency Kit). All flow
  to `urlService.captureUrl` → `core.invoke ClassifyAppUrl` → classification switch
  (`OpenRoute`, `AddAccount`, `SignIn`, `OpenUrl` → openUrlInBrowser allowlist). Also
  `captureUrlFromClipboard`.
- **source:** `main.js` app event wiring + `nc()` commander setup.
- **verify:** grep of `captureUrl`, `open-url`, `second-instance`, `new tc.Command`.
- **verified-at:** 2026-10-13.
- **suggested:** URL strings are core-classified — injection surface sits inside
  `index.node` (route dispatch / emergency-kit parser), not in JS.

### C11 — Permission policy is minimal

- **claim:** `session.setPermissionRequestHandler` grants ONLY `media` and ONLY when the
  requesting URL equals the app's own `file://…primary.html`; `setPermissionCheckHandler`
  allows `video` mediaType under the same condition (QR/TOTP camera). `getCameraAccessStatus`
  returns `"granted"` unconditionally (combined with the URL gate this is consistent).
- **source:** `main.js`.
- **verify:** literal handler bodies grep.
- **verified-at:** 2026-10-13.
- **suggested:** none.

### C12 — Hidden offscreen windows render renderer-supplied `data:` HTML

- **claim:** `downloadHtmlAsImage` builds `new BrowserWindow({show:false,
  webPreferences:{contextIsolation:true}})` (no explicit preload/session — inherits
  default session where http/https are already neutered; global `enableSandbox()` still
  applies), `loadURL("data:text/html;charset=utf-8,"+encodeURI(t))` where `t` is the
  renderer's argument, then `capturePage()` → writes `~/Downloads/wifiQrCode.png` and
  destroys. A second `data:<pre>` hidden window backs `print`/`hasPrinter`
  (`new BrowserWindow({show:!1})`, default prefs).
- **source:** `main.js` handler bodies.
- **verify:** grep of `downloadHtmlAsImage`, `hasPrinter`, `print` handlers.
- **verified-at:** 2026-10-13.
- **suggested:** renderer-controlled HTML executes in a sandboxed, non-preloaded,
  net-blocked window — worst case is pixel exfil via capturePage to a FIXED filename;
  still worth noting `writeFileSync`-class sink `wifiQrCode.png` overwrite semantics.

### C13 — File-write dialogs are user-gated but auto-opened

- **claim:** `saveContentToFile(content=t, filename=n, appPath=o)` →
  `dialog.showSaveDialog` (defaultPath `app.getPath(o)/n`; `o` is a renderer-chosen
  `app.getPath` key like `downloads`) → `writeFileSync(a,t)` → `shell.openPath(a)`
  (auto-opens the written file). `profile` → save dialog `profile.pb`; `showInFileBrowser`
  → `shell.showItemInFolder(renderer-supplied path)`; `selectDotEnvFileMountPath` /
  `getDotEnvFilePath` expose dotenv file UX.
- **source:** `main.js`.
- **verify:** handler bodies grep.
- **verified-at:** 2026-10-13.
- **suggested:** write requires user pick — but `shell.openPath` auto-launch after save
  is the interesting edge (handler=content-controlled file, OS-opened).

### C14 — Conditional Chromium sandbox weakening

- **claim:** `a().should_disable_seccomp()` (native core) gates
  `app.commandLine.appendArgument("--disable-seccomp-filter-sandbox")` before
  `enableSandbox()` — the ONLY command-line override found. When the core returns true
  (compat environments), the seccomp layer is off while Chromium sandbox stays on.
- **source:** `main.js` startup `gc()`.
- **verify:** grep — single `appendArgument`, no `appendSwitch` hits elsewhere.
- **verified-at:** 2026-10-13.
- **suggested:** environmental; verify whether beta on this host actually triggers it
  (would need runtime check — out of scope).

### C15 — Memory protection + misc hardening hooks

- **claim:** `core.protectProcessMemory(0)` for main at boot and
  `core.protectProcessMemory(this.osPid)` on every window `did-finish-load` — native
  memory-protection applied per renderer. `setCurrentProcessAumid()`, crashReporter to
  `app.setPath("crashDumps")` dir under userData, core-gated `send_crash_reports`.
  `setSecureInput` IPC → windowManager (macOS secure-input equivalent). Beta expiry:
  `AppExpired` core error → "Expiration Notice" dialog.
- **source:** `main.js`.
- **verify:** grep.
- **verified-at:** 2026-10-13.
- **suggested:** `protectProcessMemory` semantics live in index.node — candidate for
  native lane (what does it actually do on Linux — prctl/madvise?).

### C16 — REA coverage honesty note

- **claim:** REA completed but `coverage.status="partial"`: parent result budget
  (~2 GB) exhausted; semantic analysis skipped for `main.js`, `preload.js`, all 5
  renderer bundles, `vendors.js` (worker heap-exhausted at 8 GiB) and ~500 numbered
  chunks — "static facts were retained". `integrity_contradictions: []`, `limitations[]`
  ≈ 560 budget entries + 1 async-chunk self-edge + 4 honesty boilerplate. Graph recovered:
  3,059 nodes / 6,135+ edges; semantic graph 24,254 nodes / 26,867 relations
  (dominated by aliases/reads). REA's `browser_windows:0`/`main_handlers:0` are FALSE
  NEGATIVES caused by the custom `rpc.handle` wrapper + skipped semantic pass — my
  manual grep above corrects them (80 channels, real prefs).
- **source:** `/tmp/rea-op-full.json` (59 MB Evidence JSON,
  `ev_40214dabc8444cedaa82d815e836ba7cfb8e677e723891c0fef112439d15c9c4`).
- **verify:** jq queries enumerated above.
- **verified-at:** 2026-10-13.
- **suggested:** for future runs on this target: per-file `--analysis-timeout-ms` won't
  help — the bottleneck is the parent result budget, not time; analyze `main.js` +
  `preload.js` as a directory subset to get complete semantic coverage of the boundary.

### C17 — Dependencies / supply-chain snapshot

- **claim:** `package.json` declares React 19.1, Apollo Client 3.13, graphql, redux,
  immer, react-router-dom 6.23, jsqr, @lingui, motion, dnd-kit, commander 7.2,
  lexical-editor + `@1password/*` workspace deps; `vendors.js` = shared vendor chunk.
- **source:** `/tmp/op-asar/package.json` (sha256 `9ef1fe85…aedd`).
- **verify:** REA `package` node `@1password/oph@8.12.42-32.BETA` agrees.
- **verified-at:** 2026-10-13.
- **suggested:** run a dependency-CVE pass on vendors.js chunk map in a dedicated lane.

---

## Run log

| t (UTC) | action | result |
| --- | --- | --- |
| 16:1x | `sha256sum app.asar`, `ls resources/` | `769e0962f9092909ebba96a2c406bd859427a0777fc3b7156f4c19f3d31e2d21`, 40,708,328 B; unpacked dir = `index.node`+`CREDITS.html` |
| 16:1x | `file`/`sha256sum`/`nm -D` `index.node` | ELF DYN x86-64 not stripped, 187,997,016 B, `1cb3e361…`, 27 dynsyms (`napi_register_module_v1`, `rust_u2f_mgr_register`) |
| 16:1x | `/opt/1Password/1password --version` | `8.12.42-32.BETA` |
| 16:2x | `@electron/asar list` → `/tmp/asar-list.txt` | 486 entries, 415 `.js`, ext census above |
| 16:2x | `rea analyze-javascript-application --help` + `--schema` + `--llms-full` | learned `--filter-output`/`--max-heap-mb`/`--integrity-policy`; output schema is Evidence envelope (`normalized_result.graph/semantic_graph/statistics/summary/limitations`) |
| 16:2x | `@electron/asar extract` → `/tmp/op-asar` | clean extract, 220 MB on disk (188 MB is index.node); `package.json` read |
| 16:2x→16:4x | `timeout 1200 npx rea-agents@6.4.0 analyze-javascript-application … --format json --max-heap-mb 8192` | EXIT=0 in ~20 min window; 59,181,596 B JSON Evidence; all 423 files parsed, 0 parse failures; coverage `partial` (result-budget, see C16) |
| 16:4x | jq census of Evidence (statistics/summary/graph/limitations; per-entry sha256; ipc/contextBridge/sender-validation observations) | numbers in C1/C6/C16 |
| 16:4x–16:5x | manual grep pass on `main.js`/`preload.js`/HTMLs (IPC handlers, webPreferences, CSP, protocol handlers, permission handlers, navigation lockdown, openExternal allowlist, dialogs, commander CLI, core.invoke type census, main→renderer events) | findings C2–C15 |

Failures/gaps (honest): `asar extract-file package.json` produced no stdout (worked
around via full extract); REA semantic coverage partial (C16) — corrected by manual grep;
`index.node` intentionally not analyzed; `nc()` body not fully decompiled (commander CLI
options enumerated from call sites); could not run 1Password itself (headless lane), so
`dev_tools_enabled()`/`should_disable_seccomp()` runtime values unknown.

## Summary

1Password 8.12.42-32.BETA is a **thin Electron shell around a 188 MB Rust N-API core**.
JS surface ≈ 16 MB across 423 files: `main.js` (236 KB router), a 3 KB `preload.js`, and
5 renderer bundles under a strict `script-src 'self'` / `connect-src data: 'self'` CSP.
Hardening is unusually thorough: global `enableSandbox()`, `contextIsolation+sandbox` on
every window, http/https/ws/wss neutered on both sessions (empty `Response`), navigation
and window-open denied and bounced to the OS browser, media permission gated to the
app's own file URL, openExternal protocol allowlist, memory-protection calls per window.

The trust boundary is therefore concentrated and binary: **one `file://` senderFrame
check guards 80 IPC channels**, and the `invoke`/`executeGql` multiplexers forward
arbitrary typed commands and GraphQL to the native core. Renderer compromise ⇒ the full
59+ command surface (unlock, secure-copy, import, update-check) — the only remaining
gate is whatever re-authorization lives inside `index.node`. Secondary sinks worth
noting: renderer-supplied `data:` HTML in hidden capture windows (net-blocked, fixed
output path), user-gated `saveContentToFile` that auto-`openPath`s, renderer-controlled
`showItemInFolder` paths, and a conditional `--disable-seccomp-filter-sandbox`.

REA ran clean (0 parse failures, integrity contradictions none) but hit its result
budget on every large bundle — treat its `browser_windows:0`/`main_handlers:0` as false
negatives; the manual grep pass above is the corrected boundary record.
