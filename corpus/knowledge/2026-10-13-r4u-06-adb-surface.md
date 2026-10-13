<!-- corpus entry — kaidoku-shokunin round 4 unlock wave (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r4u/06-adb-surface.md. -->

# kaidoku-r4u / 06 — ADB surface: client present, zero devices

Re-probe of the adb frontier after `android-tools 37.0.0` landed at
`/usr/bin/adb` (r2 `11-caps-catalog.md` had both probed verbs at
`capability_unavailable`: "The selected adb binary was not found: adb").
Answer: the adb surface is **bound and partially live** — 2 of 24 verbs are
device-free and now return real evidence; the other 22 all demand a `<serial>`
up front and fail `unsupported_target` against a device-less server, with three
divergent edge behaviors (one false-positive refusal, one silent daemon-start,
one 10-minute block).

## Candidate: adb capability unlocks with `REA_ADB_PATH` — and without it
- claim: `export REA_ADB_PATH=/usr/bin/adb; npx -y rea-agents@6.4.0
  inspect-adb-client` succeeds — `provider adb 37.0.0-android-tools`,
  `client.binary_path:/usr/bin/adb`, `path_source:"environment"`,
  `contacted_adb_server:false`. With `REA_ADB_PATH` unset it STILL succeeds
  (`path_source:"path"`, `binary_path:"adb"`): unset falls back to a PATH
  exec lookup (`resolveAdbBinary`, AdbConfiguration.js:13-21), so the env var
  is an override, not a requirement — r2's refusal was `adb` absent from PATH,
  not the missing variable. If set, it must be an absolute path or the
  provider throws `AdbConfigurationFailure("not_absolute")`.
- source: live runs above → evidence `ev_d850ccd0ada3e7b6d44a980b606a4842930413142ddfb933145a49a436f803e2`
  (env set) and `ev_519f16a2d4d27145fbc07a0ffcb18c080a405f0427ae225258ee16bcacb7055c`
  (env unset); `adb --version` → `Android Debug Bridge version 1.0.41 /
  37.0.0-android-tools / Installed as /usr/bin/adb`.
- verify: `REA_ADB_PATH=/usr/bin/adb npx -y rea-agents@6.4.0 inspect-adb-client
  --format json` and `env -u REA_ADB_PATH npx -y rea-agents@6.4.0
  inspect-adb-client --format json`; compare `normalized_result.client`.
- verified-at: 2026-10-13
- suggested: admit — `inspect-adb-client` is a pure client probe (runs
  `adb version`, 10 s / 64 KiB bound, documented "never starts the adb
  server", AdbConfiguration.js:44-46). Both path_source modes verified.

## Candidate: `list-adb-devices` returns an empty list, not a refusal
- claim: with the daemon already up, `list-adb-devices` → `devices:[]`,
  `may_have_started_adb_server:false`, exit 0 — an honest empty list matching
  `adb devices -l` ground truth (`List of devices attached` + nothing). The
  evidence_id is deterministic: identical `ev_d4d8cc77c3950870012fa3d41a0e810e1c569db0aad32e22cdef8b9f66e281db`
  across repeat runs. It executes real `adb devices -l` and parses serial /
  state / transport / kind per line (`parseAdbDevicesOutput`,
  AdbDeviceOutput.js:32-79; kind inference limited to `emulator-\d+` serials
  and `usb:` metadata — stated in the result's own `limitations`).
- source: live run (evidence id above); `adb devices -l` ground truth
  immediately prior → empty, exit 0.
- verify: `adb devices -l` then `REA_ADB_PATH=/usr/bin/adb npx -y
  rea-agents@6.4.0 list-adb-devices --format json`.
- verified-at: 2026-10-13
- suggested: admit — first live adb-surface evidence on this host.

## Candidate: `list-adb-devices` DOES start the daemon but reports it didn't
- claim: with the daemon killed (`ss` shows :5037 free), `list-adb-devices`
  returns `devices:[]` with `may_have_started_adb_server:false` — yet a fresh
  `adb -L tcp:5037 fork-server server` process is listening afterward. The
  flag is a false negative on android-tools 37.0.0: this adb prints
  `* daemon not running; starting now at tcp:5037` / `* daemon started
  successfully` to **stderr**, while `parseAdbDevicesOutput(ran.value.stdout)`
  scans **stdout only** (AdbProvider.js:357). The parser explicitly handles
  `* daemon` lines (sets `daemonStarted`, AdbDeviceOutput.js:~44) — upstream
  intent exists, the bytes just arrive on the wrong stream.
- source: sequence — `adb kill-server` → `ss` 5037 closed → REA
  `list-adb-devices` → `may_have_started:false` → `ss` shows
  `127.0.0.1:5037 LISTEN` + `pgrep` → `adb -L tcp:5037 fork-server server`;
  raw `adb devices -l 2>/dev/null` (stdout) lacks daemon lines, `2>&1
  1>/dev/null` (stderr) has both.
- verify: `adb kill-server; sleep 1; npx -y rea-agents@6.4.0 list-adb-devices
  --format json; ss -tln | grep 5037`.
- verified-at: 2026-10-13
- suggested: admit — behavioral note: any adb verb may spawn the host daemon
  as a side effect; the `may_have_started_adb_server` telemetry cannot be
  trusted on android-tools ≥37 stderr layout.

## Candidate: the 22 serial-bound verbs — `unsupported_target`, three ways to differ
- claim: exactly 2 of the 24 adb CLI verbs are serial-free
  (`inspect-adb-client`, `list-adb-devices` — the only `args: z.object({})`
  schemas, cli/adbCommands.js:30,35). All 22 others require `<serial>` and,
  on a device-less host:
  - **no serial** → `VALIDATION_ERROR` (zod `invalid_type` on `serial`),
    exit 0, adb never invoked.
  - **dead serial** → `unsupported_target` (`AnalysisUnsupportedTargetError`,
    `adb: device 'emulator-5554' not found`), `retryable:false`, exit 0,
    instant. Verified on 14 verbs spanning every family: inspect-adb-device,
    inspect-adb-display, list-adb-packages, list-adb-processes,
    list-adb-directory, read-adb-logcat, read-adb-setting,
    resolve-adb-packages, start-adb-app, uninstall-adb-package,
    install-adb-package, pull-adb-file, pull-adb-package, list-adb-features
    (the last at VALIDATION boundary; same runner past it). Classifier is
    stderr-regex driven (AdbProvider.js:91-106): `unauthorized`,
    `device not found|offline|still authorizing|more than one device`,
    `No such file|Permission denied` → `unsupported_target`; killed child →
    `timeout`; >maxOutputBytes → `resource_constraint`; else protocol error.
  - `capture-adb-screen` → **`unreadable_output`**, not
    `unsupported_target`: it runs through `runAdbBinary` (raw PNG stdout
    path, AdbProvider.js:113-141) which maps any exec failure to
    `AnalysisProtocolError` with NO stderr classification. Raw truth:
    `adb -s emulator-5554 exec-out screencap -p` → exit 255, empty stdout,
    stderr `error: device 'emulator-5554' not found`. Protocol and Output
    errors both project to `unreadable_output`
    (analysisErrorProjection.js:130-131).
  - `push-adb-file` **without `--overwrite`** → **`unreadable_output`** with
    `details.reason:"The device path already exists and overwrite was not
    requested"` — a FALSE exists-verdict: the `shell test -e` probe's
    `AnalysisUnsupportedTargetError` falls through to `deviceExists=true`
    ("authorization/refusal states surface on push instead",
    AdbProvider.js:895-912), emitting a bogus path-exists refusal. Re-run
    with `--overwrite` → reaches real `adb push` → `unsupported_target`
    (`failed to get feature set: device 'emulator-5554' not found`).
  - `collect-adb-bugreport` → **blocks**: raw `adb -s emulator-5554
    bugreport <dir>` prints `- waiting for device -` and parks
    (wait-for-device semantics), observed >70 s with the child
    `/usr/bin/adb -s emulator-5554 bugreport /tmp` confirmed waiting. REA
    bounds it at `BUGREPORT_TIMEOUT_MS = 600_000` (10 min,
    AdbProvider.js:46-47) → terminal code would be `timeout`
    (AnalysisTimeoutError → `"timeout"`, analysisErrorPresentation.js:122).
- source: live runs above; AdbProvider.js:91-106 (classifier), :113-141
  (binary path), :46 (bugreport bound), :895-914 (push exists-probe);
  analysisErrorProjection.js:130-131; analysisErrorPresentation.js:122.
- verify: `npx -y rea-agents@6.4.0 <verb> emulator-5554 --format json` per
  verb; `timeout 10 adb -s emulator-5554 bugreport /tmp/x` reproduces the
  park; `push-adb-file … /sdcard/fake --format json --full-output` shows the
  hidden `details.reason`.
- verified-at: 2026-10-13
- suggested: admit — `unsupported_target` is the stable dead-device code for
  19/22 verbs; treat `unreadable_output` on push/screen and the bugreport
  park as known-divergent edges, not capability gaps.

## Candidate: REA exposes zero host-side adb provisioning verbs
- claim: the entire REA adb vocabulary is the 24 ops enumerated in
  AdbProvider.js (`inspect_adb_client`, `list_adb_devices`, + 22 serial-bound
  device ops). There is no `keygen`, `pair`, `connect`, or `start-server`
  wrapper — device-free *provisioning* is out of surface. The substrate
  supports it anyway: raw `adb keygen /tmp/rea-testkey` succeeded
  device-free (OpenSSH private key 1704 B + `.pub` 715 B, now deleted). And
  `rea doctor` never inspects adb: `providerInspections` covers only the
  ghidra+ida analysis engines (doctor JSON at /tmp/rea-doctor-r4u.json); adb
  appears solely as 24 `adb-provider` entries in `identity.catalog.tools[]`
  — the unlock is invisible to the doctor verdict.
- source: op-name enumeration `grep -o '"[a-z_]*adb[a-z_]*"'
  dist/adb/AdbProvider.js` (24 ops); `adb keygen /tmp/rea-testkey` run +
  `file` → `OpenSSH private key`; doctor JSON top keys `healthy, …,
  providerInspections, checks, identity` with adb only under
  `identity.catalog.tools`.
- verify: same greps; `npx -y rea-agents@6.4.0 doctor --format json |
  jq '.providerInspections[].id'` → `ghidra`, `ida` only.
- verified-at: 2026-10-13
- suggested: admit — "adb surface live" means *client + server ops only*;
  any adb provisioning (keygen/pair/connect/emulator bring-up) is raw-adb
  territory outside REA. Doctor stays silent on adb health; the two
  serial-free verbs are the only readiness probes.

## Run log
- `adb --version` → 1.0.41 / 37.0.0-android-tools at /usr/bin/adb.
- `adb devices -l` → daemon autostart (`* daemon …` on stderr), empty list,
  :5037 LISTEN (pid 187846). Ground truth: no devices.
- `inspect-adb-client` (env set) → ev_d850ccd0…, path_source environment,
  contacted_adb_server false; (env unset) → ev_519f16a2…, path_source path —
  both succeed.
- `list-adb-devices` → ev_d4d8cc77…, `devices:[]`; deterministic id across
  runs. Daemon-start flag false-negative proven by kill→run→LISTEN cycle.
- Serial-free schema check: only 2 `args: z.object({})` commands
  (adbCommands.js:30,35); all other 22 declare `serial`.
- Dead-serial probes (serial `emulator-5554`): 14 verbs →
  `unsupported_target`, retryable false, exit 0; push without `--overwrite`
  → `unreadable_output` (false "path already exists"); with `--overwrite` →
  `unsupported_target`; capture-adb-screen → `unreadable_output`;
  collect-adb-bugreport → blocked >70 s on `- waiting for device -`,
  SIGKILLed via shell teardown (REA bound: 600 s → `timeout`).
- Raw adb cross-checks: `exec-out screencap` → exit 255 + stderr
  `error: device … not found`; `shell` → exit 1 + `adb: device … not found`;
  `bugreport` → `- waiting for device -` park; `keygen /tmp/rea-testkey` →
  OpenSSH keypair written (deleted after).
- `rea doctor --format json` → providerInspections = ghidra+ida only; adb
  presence only in `identity.catalog.tools` (saved /tmp/rea-doctor-r4u.json).
- Source reads: `~/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/dist/
  adb/{AdbProvider,AdbDeviceOutput,AdbConfiguration}.js`,
  `dist/cli/adbCommands.js`, `dist/domain/analysisError{Projection,
  Presentation}.js`.
- Cleanup: `adb kill-server` → `pgrep -a adb` empty, :5037 closed; scratch
  keys/bins removed; other lanes' rea mcp/ghidra processes observed but
  untouched (one self-inflicted `pkill -f` matched the wrapper — shell died,
  no harm; kills redone by pid/pattern-safe commands).

## Summary
adb is **bound**: `inspect-adb-client` and `list-adb-devices` both return
live evidence (provider 37.0.0-android-tools; honest empty device list),
`REA_ADB_PATH` is now optional since `adb` resolves on PATH. The device-less
taxonomy is: missing `serial` → `VALIDATION_ERROR`; dead serial →
`unsupported_target` (retryable:false, exit 0) on 19 of 22 verbs; divergent
edges = `unreadable_output` for `capture-adb-screen` (binary path skips
stderr classification) and no-`--overwrite` `push-adb-file` (dead-serial
exists-probe degrades to a false "path already exists"), plus
`collect-adb-bugreport` which parks on adb's `- waiting for device -` until
the hardcoded 600 s bound ends it as `timeout`. Two telemetry caveats:
`may_have_started_adb_server` false-negatives on android-tools 37 (daemon
notices moved to stderr, parser reads stdout), and `rea doctor` does not
inspect adb at all — these two verbs are the only readiness probes. REA
offers no host-side provisioning (keygen/pair/connect): the next frontier
atom is a live target — an emulator or `adb connect`-able endpoint is what
unlocks the remaining 22 verbs.
