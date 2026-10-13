<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/14-frontier-scan.md. -->

# kaidoku-r2 lane 14 — Frontier prerequisite scan (READ ONLY)

Axes: prerequisite-truth (what the host actually holds) / probe-readiness
(smallest viable round-3 move) / boundary-honesty (absence recorded as
absence). Read-only survey; nothing installed, nothing launched, no config
touched.

## Candidate: Android APK surface

- claim: All decode tooling is absent; the APK *corpus* is present.
  `apktool`, `jadx`, `adb`, `aapt`, `aapt2`, `apkanalyzer`, `baksmali`,
  `dex2jar`, `smali`, `fastboot`, `sdkmanager`, `emulator` — none on PATH,
  no `~/Android/Sdk` or `/opt/android*` dirs, port 5037 (adb) closed. But
  two real APKs exist: `~/.local/share/godot/export_templates/4.7.2.stable/
  android_debug.apk` + `android_release.apk` (Godot 4.7.2 export templates).
- source: REA pins its Android engines externally —
  `rea-agents/dist/android/JadxRelease.js`: `REA_JADX_MCP_JAR` must point at
  a caller-supplied `jadx-headless-mcp-0.7.1-all.jar` (sha256
  `6e5eacf500b6…`, "REA does not download or install it"); JDK 21.0.12.1
  present satisfies the "full JDK" leg. Apktool leg wants
  `REA_APKTOOL_COMMAND` (abs) or `apktool` on PATH — both absent
  (`dist/contracts/apktool/apktoolToolContracts.js`). adb verbs need
  caller-supplied adb.
- verify: `command -v apktool jadx adb aapt fastboot` (all absent);
  `find /usr /opt ~ -maxdepth 6 -name '*.apk'` → the 2 Godot APKs;
  `grep REA_JADX` → zero hits in `~/.config/devin/mcp_config.json`,
  `~/.omp/agent/mcp.json`.
- verified-at: 2026-10-13T12:23-03:00
- suggested: round-3 probe needs no engine: `inspect_artifact` /
  `open_binary` (both `available:true`) on
  `android_debug.apk` as a ZIP/APK inventory (manifest, DEX count, native
  `.so` arch list — Godot templates ship arm32/arm64/x86_64 libs). Then a
  typed `inspect_android_package` attempt records `executable_missing`
  (`REA_JADX_MCP_JAR` unset) — a clean refusal datum, not a failure.

## Candidate: Runtime observation (CDP / Electron)

- claim: Nothing bindable right now — zero CDP listeners and no process
  carrying `--remote-debugging-port`. The *substrate* to self-provision a
  target is fully present: `/usr/bin/chromium` (running user instance PID
  25784 has no debug flag — cannot attach), `playwright` 1.64.0 global +
  `~/.cache/ms-playwright/chromium-1248` + `chromium_headless_shell-1248`,
  `agent-browser` 0.38.2 global, a stale `~/.local/share/burnerchrome/`
  profile whose `chrome.log` shows a prior `DevTools listening on
  ws://127.0.0.1:9222/` run (script now points at a missing
  `~/.agent-browser/browsers/chrome-154…/chrome`). Electron side:
  `/usr/lib/electron39/electron` + `/usr/lib/electron43/electron` binaries;
  1Password is Electron 42.11.1 running without debug port.
- source: `dist/browser/CdpEndpoint.js` — `list_browser_targets` fetches
  `/json/version` + `/json/list` from a caller-supplied `cdp_endpoint`
  (default `http://127.0.0.1:9222` per `browserToolContracts.js`);
  `electronToolContracts.js` defaults Electron CDP to `:9223` and counts
  only `file://` page targets; passive path = `list_electron_targets` →
  `inspect_electron_page`, active path = provider-owned run with
  caller-defined actions.
- verify: `ss -tln` shows no `:9222|:9223|:9229|:5858` listeners;
  `pgrep -af remote-debugging` empty; `pgrep -af electron` only 1Password
  helpers without the flag. So `list_browser_targets` /
  `list_electron_targets` would return an endpoint-unreachable/empty
  result today.
- verified-at: 2026-10-13T12:23-03:00
- suggested (smallest viable r3): launch
  `chromium --headless --remote-debugging-port=9222
  --user-data-dir=$(mktemp -d) about:blank`, then `list_browser_targets`
  on `http://127.0.0.1:9222` — exercises `/json/list` target enumeration
  end-to-end. Electron leg: `/usr/lib/electron43/electron
  --remote-debugging-port=9223 <tiny app with a file:// page>` →
  `list_electron_targets` — both legs self-owned, no operator installs.

## Candidate: Mach-O / macOS surface

- claim: Closed, per `npx -y rea-agents@6.4.0 capabilities --format json`
  (this host): `inspect_macho`, `inspect_plist`, `inspect_asset_catalog`,
  `demangle_swift`, `capture_native_ui_scenario`, `observe_native_ui`,
  `observe_native_calls`, `inspect_signature`,
  `inspect_native_dispatch_metadata`, `list_architectures` —
  `available:false, availability_code:"unsupported_host"`. Note
  `list_architectures` is also macOS-bound (LLDB). Counter-samples:
  `inspect_keyed_archive`, `decode_interface_builder`,
  `trace_dylib_resolution` report `available:true` (pure-JS paths) —
  probeable if a `.dmg`/`.pkg`/nib carrier ever lands, none on host now.
- source: live CLI output this round; matches r1 `03-rea-doctor.md` and
  PROVINCE frontier line.
- verify: `capabilities --format json | jq` table above; re-run is
  deterministic (catalog sha256-pinned).
- verified-at: 2026-10-13T12:23-03:00
- suggested: none — keep recorded as `unsupported_host` boundary. Do not
  spend a round-3 lane here.

## Candidate: EVM bytecode

- claim: No on-host carrier and no chain tooling: zero `.evm` /
  `foundry.toml` / `hardhat.config.*` / `.sol` files; `forge cast anvil
  hardhat solc geth hevm` all absent; `*.bin` sweep returns devin-cli
  cache protobufs + a 64-byte ASCII `burner.bin` — no bytecode.
  **However** `inspect_evm_interface` is self-contained: contract states
  "unchanged bundled EVMole 0.9.3/WASM in a bounded owned worker" — no
  pwntools/python needed (the r1 README note claiming otherwise is stale
  vs the shipped contract).
- source: `dist/contracts/evm/evmToolContracts.js` — input
  `{path, encoding: "hex"|"raw"}`, infers dispatch selectors / argument
  strings / mutability without chain/RPC; `EvmInterfaceService.js` shows
  no external spawn; EOF-style `EF00` containers explicitly unsupported.
- verify: `command -v forge cast anvil solc` absent; `find ~
  -maxdepth 6 -name 'foundry.toml' …` empty; contract file read directly.
- verified-at: 2026-10-13T12:23-03:00
- suggested (smallest viable r3): synthesize a minimal honest carrier —
  write a standard solc-style runtime hex (e.g. `6080604052348015600e…`
  PUSH/arithmetic sequence) to `/tmp/probe.hex`, call
  `inspect_evm_interface {path, encoding:"hex"}`. Selector-inference on a
  synthetic-but-valid carrier proves the WASM pipeline end-to-end; log
  that the carrier is synthetic, never a found artifact.

## Candidate: JEB provider

- claim: Fully absent. `REA_JEB_MCP_URL` unset; no JEB install under
  `/opt`, `/usr/local`, `~` (maxdepth 5); nothing on default endpoint
  `http://127.0.0.1:8425/mcp` (port closed); no `REA_*` env keys in either
  client MCP config.
- source: `dist/jeb/JebProvider.js` + `CapabilityInventory.js` — "Start a
  JEB client serving MCP … point REA_JEB_MCP_URL at it (default
  http://127.0.0.1:8425/mcp). REA does not install or launch JEB."
- verify: `echo $REA_JEB_MCP_URL` unset; `find -iname '*jeb*'` empty;
  `ss -tln` no `:8425`.
- verified-at: 2026-10-13T12:23-03:00
- suggested: none — operator-owned engine install. Record the gap +
  exact env key; spend nothing further.

## Summary

| Frontier | Prerequisites on host | Disposition | Round-3 move |
|---|---|---|---|
| Android APK | 2 real APKs (Godot 4.7.2); jadx-jar/apktool/adb absent; JDK 21 ok | **partial — inventory leg open now, decode leg operator-owned** | `inspect_artifact`/`open_binary` on `android_debug.apk`; record jadx `executable_missing` |
| Runtime observation | chromium + playwright cache + electron39/43 binaries; zero live CDP endpoints | **viable via self-launched CDP** | chromium `--remote-debugging-port=9222` → `list_browser_targets`; electron43 `:9223` file:// page → `list_electron_targets` |
| Mach-O/macOS | n/a | **closed — `unsupported_host` ×10 ops confirmed live** | none |
| EVM | no carrier/tooling, but bundled EVMole WASM needs nothing external | **viable with synthetic hex carrier** | `inspect_evm_interface` on `/tmp/probe.hex` (`encoding:"hex"`) |
| JEB | env unset, no install, port 8425 closed | **absent — operator-owned** | none; log gap + `REA_JEB_MCP_URL` key |

Corrections to prior beliefs (data, not instructions): r1/README claimed
EVM needs caller-supplied pwntools — the shipped 6.4.0 contract shows
bundled EVMole 0.9.3/WASM instead. `list_electron_targets` defaults to
CDP `:9223`, not the browser `:9222`.
