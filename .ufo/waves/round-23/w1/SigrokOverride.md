# R23-C1 — `REA_SIGROK_COMMAND` selection and `prlimit` limits in installed rea-agents 6.5.0

Seat: `KaidokuR23.SigrokOverride` (scout, leaf, read-only; author-side report, not outside verification).
Round 23, W1. Scope: source trace of the installed REA 6.5.0 package plus non-counting CLI configuration
probes. No debugger/Frida, no process attach, no device access, no APK or carrier execution, no MCP device,
no network target, no credential/config probing.

- Probe date: 2026-10-21. Host: Linux 7.2.11-arch1-1 x86_64. Node `v24.21.0`, npx `11.19.0`.
- Probe cwd: `/tmp` (the repo cwd was not used for probe outputs).
- Package under trace: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
  (`package.json` version `6.5.0`, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`).
  The only 6.5.0 npx cache; the other resolvable cache is 6.7.0 (`a1722018f28f9df2`). `npx ... --version`
  printed `6.5.0` (6 bytes, sha256 `3eb8e06c…95b00`), so this is the package exercised.
- No artifact target exists for these probes. The subject is the installed package; configured-tool hashes
  are listed where a probe reached an executable. Every probe is a typed refusal except `--version`/`--help`;
  none is evidence for any T1 verb.

## Verdict

1. `REA_SIGROK_COMMAND` is the only selector for the sigrok executable. It must be one **absolute path** to
   an existing, executable regular file. There is no default value, no PATH lookup, no shell/argument
   splitting, no CLI flag, and no config-file key. Absence and a relative value collapse to the same
   configuration refusal.
2. `REA_SIGROK_PRLIMIT_COMMAND` is the only other sigrok-scoped environment key. It defaults to the literal
   `/usr/bin/prlimit` when unset or null; an empty string is not defaulted (`??`, not `||`).
3. Resource limits are compile-time constants (`BOUNDED_PRODUCER_LIMITS`), not environment-configurable.
   `prlimit` is invoked with an exact five-part prefix that pins address space, file size, CPU and core
   limits, and the kernel's inherited soft/hard ceilings can only lower them.
4. MCP/CLI tool registration is unconditional. The `signalRecordingEnabled` availability field is a cheap
   `isAbsolute()` predicate used only by capability inventory/reporting, not a registration gate and not a
   probe of existence/version.

## Findings

### 1. Selection chain (observation)

CLI path:

| Step | Location | Behavior |
|---|---|---|
| Dispatcher | `scripts/rea.mjs:84-96` | `createCli(process.env, resultOutput)`; the compiled CLI bundle is loaded (`scripts/rea.mjs:43-47`). |
| CLI build | `dist/cli.js:61-62` | `createCli(selectedEnvironment = process.env)` then `snapshotEnvironment(selectedEnvironment)` (frozen shallow copy; `dist/process/snapshotEnvironment.js:2-13`). |
| Register | `dist/cli.js:85` | `registerSignalCommands(cli, logger, environment)`. |
| Service default | `dist/cli/signalCommands.js:10` | `service = createSignalRecordingService(environment)` evaluated at registration. |
| Composition | `dist/composition/signals.js:3` | `new SignalRecordingService(new SigrokRecordingProvider(environment))`. |
| Provider fields | `dist/signals/SigrokRecordingProvider.js:36-47` | stores `this.environment`, `this.platform`; no env read in the constructor. |

MCP path:

| Step | Location | Behavior |
|---|---|---|
| Runtime env | `dist/main.js:17-18,42-43` | `env: process.env` → `snapshotEnvironment(dependencies.env)`. |
| Server env | `dist/main/transport.js:40-50` | passes `serverContext.environment` into `createServer`. |
| Server snapshot | `dist/server/createServer.js:164-169` | `snapshotEnvironment(options.environment ?? process.env)`. |
| Service creation | `dist/server/createServer.js:209` | `options.signalRecording ?? createSignalRecordingService(environment)`. |
| Tool registration | `dist/server/createServer.js:309`, `dist/server/registerSignalTools.js:5-12` | `registerSignalTools(...)` is called unconditionally. |

Per-request read (both adapters): `SigrokRecordingProvider.decode` (`:48-50`) and
`inspectDecoders` (`:51-53`) call `#executeRequest` (`:57`); the environment key is read inside that method
at `:71`. The object is a frozen startup snapshot, so this is a per-request read of a fixed value, not a
live `process.env` lookup. The provider is constructed once per CLI invocation or MCP server lifetime.

Runtime bundles duplicate this code: CLI bundle `dist/cli-runtime/cli.js:1234-1246` (loaded by
`scripts/rea.mjs:44`) and MCP bundle `dist/mcp/main-kBXHZ8S5.js:18046-18058` (loaded by
`scripts/rea.mjs:40`). They are line-for-line equivalent to the source module for the selection block.

### 2. Exact gate order and line numbers (observation)

`dist/signals/SigrokRecordingProvider.js`, `#executeRequest` (starts `:57`; `phase = "configuration"` at
`:59` and again at `:138`):

| Order | Line(s) | Check | Failure result |
|---|---|---|---|
| 1 | `:66-67` | caller signal already aborted → `AnalysisCancelledError` | cancelled |
| 2 | `:68` | `#resources.release()` drains earlier work | cleanup failure, if any |
| 3 | `:69-70` | `this.platform !== "linux"` | configuration refusal |
| 4 | `:71` | `const configured = this.environment.REA_SIGROK_COMMAND ?? ""` | — |
| 5 | `:72-73` | `!isAbsolute(configured)` → "Supply absolute REA_SIGROK_COMMAND…" | `capability_unavailable` |
| 6 | `:74` | `await realpath(configured)` — resolves symlinks; ENOENT/EACCES propagate | `capability_unavailable` |
| 7 | `:75` | `await access(command, constants.X_OK)` | `capability_unavailable` |
| 8 | `:76` | read resolved executable with 64 MiB cap, hash it (`readStableArtifact` requires a regular file, no symlink) | `capability_unavailable` |
| 9 | `:77` | `const configuredLimiter = this.environment.REA_SIGROK_PRLIMIT_COMMAND ?? "/usr/bin/prlimit"` | — |
| 10 | `:78-79` | `!isAbsolute(configuredLimiter)` → "REA_SIGROK_PRLIMIT_COMMAND must be absolute." | `capability_unavailable` |
| 11 | `:80-82` | `realpath`, `X_OK`, read/hash limiter with 64 MiB cap | `capability_unavailable` |
| 12 | `:83` | `effectiveLimits = await this.#resources.readLimits(LIMITS)` (see §5) | `capability_unavailable` on unreadable/invalid kernel report |
| 13 | `:84` | `limitArguments = prlimitArgumentVector(effectiveLimits, command)` | — |
| 14 | `:85-88` | create private runtime (`PrivateRuntimeRoot`, prefix `rea-sigrok-`), retain it | workspace failure |
| 15 | `:138-142` | `execute(["--version"])`; banner gate | `capability_unavailable` on generic mismatch |

Consequences visible in the gates:

- No value in the environment and a relative value both fail at `:72-73` with the same message and the same
  response bytes. Observed: unset and `REA_SIGROK_COMMAND=relative/sigrok-cli` produced byte-identical
  stdout (both 836 bytes, sha256 `d24b0a56bee07de14be77d48f5abcf2d6635a3739993bebec675a93103567dee`).
- The value is not a command line. `REA_SIGROK_COMMAND="/usr/bin/prlimit --version"` fails at `realpath`
  with ENOENT on the whole string (observed, 821 bytes, sha256 `4c6f408b…204b10`).
- PATH resolution is impossible because the absolute-path check precedes `realpath`; no `PATH` search exists.
- Symlinks are resolved by `realpath`; the resolved path is what is executed and hashed. The metadata records
  both `configured_path` and resolved `path` (`:143-151`).
- A readable but non-executable file fails at `access(..., X_OK)`; observed `/etc/hostname` →
  `EACCES: permission denied, access '/etc/hostname'` (752 bytes, sha256 `dbb59259…a3822`).
- A missing limiter fails before any execution; observed `/nonexistent/prlimit` → ENOENT on realpath
  (803 bytes, sha256 `feeb6ba8…73fa8`).
- Empty `REA_SIGROK_PRLIMIT_COMMAND=` is not defaulted; observed "must be absolute" (737 bytes, sha256
  `2b5737af…b8406`, identical to the relative-limiter probe).
- `REA_SIGROK_PRLIMIT_COMMAND=/usr/bin/prlimit` is the default actually used when unset: with
  `REA_SIGROK_COMMAND=/usr/bin/prlimit`, the run reached and executed the limiter and then failed the
  version banner (observed `captured_output.stdout = "prlimit from util-linux 2.42.4\n"`, exit 0,
  974 bytes, sha256 `0fa86cc5…c792`).

### 3. Version binding (observation)

- Provider identity pins `version: "sigrok-cli@0.7.2"` (`:22-26`).
- `execute(["--version"])` runs through the limiter first (`:138-139`). The check at `:140-142` is a
  banner test only: stdout must match `/^sigrok-cli 0\.7\.2(?:\r?\n|$)/u` **and** contain the literal
  substring `libsigrokdecode`. Anything else throws a plain `Error` in the `configuration` phase.
- A valid banner does not prove a specific build or library ABI; it is a caller-trusted string test.
  Each request repeats the probe; there is no cached tool identity across calls.
- The banner check itself runs as a subprocess under the same prlimit prefix, so `--cpu`/`--as`/`--fsize`
  limits apply to the version probe too.

### 4. Command construction (observation)

`execute` (`:89-137`) always launches the **limiter**, not the configured tool directly:

```
command: limiter
arguments: [...limitArguments, ...args]
cwd: private runtime path            // :94
runId: `rea-sigrok-${randomUUID()}`  // :96
hostEnvironment: this.environment    // :97
timeoutMs: LIMITS.command_timeout_ms // :99
diagnosticBytes: LIMITS.output_bytes // :100
acceptNonZeroExit: true              // :101
```

Operation arguments:

- `inspect-signal-decoders`: `--dont-scan --list-supported` when `decoder === null`; otherwise
  `--dont-scan --protocol-decoders=<decoder> --show` (`:164-166`).
- `decode-signal-recording`: `--dont-scan --input-file=recording --protocol-decoders=<stack>
  --protocol-decoder-samplenum [--input-format=…] [--protocol-decoder-annotations=…]` (`:191-201`).
  The input is first copied to `<runtime>/recording` with mode `0o400` (`:184-189`) and decoded from the
  private cwd; after the run the copy is re-read and its sha256 compared (`:204-208`).
- After every `execute`, the resolved tool and limiter are re-read at 64 MiB each and their sha256 compared
  to the pre-run identities (`:119-125`). A changed executable or limiter is `artifact_changed`.
- Non-zero producer exit throws `ProviderAdapterError` with `exit_code`, stdout and stderr (`:128-135`),
  which projects as `execution_failure` (`dist/domain/analysisErrorProjection.js:157`), not
  `capability_unavailable`.

The child environment is the full frozen host snapshot plus `REA_PROCESS_RUN_ID`:
`dist/process/ProviderProcess.js:26-31` (`{...hostEnvironment, ...options.env, REA_PROCESS_RUN_ID: runId}`).
No credential filtering is applied by this provider; the caller-supplied executable and limiter are
trusted (`:231-232` limitations text).

### 5. Limits and prlimit (observation, exact)

`dist/process/LinuxResourceLimits.js`:

| Item | Line(s) | Exact value / behavior |
|---|---|---|
| `BOUNDED_PRODUCER_LIMITS` | `:10-17` | `input_bytes: 33554432` (32 MiB), `output_bytes: 4194304` (4 MiB), `command_timeout_ms: 30000`, `address_space_bytes: 1073741824` (1 GiB), `file_bytes: 67108864` (64 MiB), `cpu_seconds: 30` |
| `prlimitArgumentVector` | `:19-26` | `["--as=1073741824:1073741824","--fsize=67108864:67108864","--cpu=30:30","--core=0:0","--", command]` |
| `clampLinuxResourceLimits` | `:28-50` | reads `Max address space`, `Max file size`, `Max cpu time`; requires exactly one matching line and exactly 3 whitespace-separated fields; `unlimited` is skipped; effective = min(configured, inherited soft, inherited hard); malformed/missing/duplicate → `Cannot establish inherited Linux limit: …` / `Invalid inherited Linux limit: …` |
| `readLinuxResourceLimits` | `:52-80` | opens `/proc/self/limits`, allocates 16 KiB (`Buffer.alloc(16*1024)`), fails if `bytesRead === buffer.length` ("Inherited Linux limits exceed the report budget"), then clamps; handle is released through the artifact resource scope |

Enforcement points in the provider:

| Limit | Line(s) | Mechanism |
|---|---|---|
| 1 GiB AS / 64 MiB file / 30 s CPU / no core | `:84`, `:91-107` | exact prlimit prefix; `prlimit` is the launched process and the tool is its trailing command after `--` |
| 30 s wall clock | `:99`; `dist/process/ProviderDeadline.js:30-52` | absolute monotonic deadline; both timer and caller signal abort; on interruption `OwnedCommand` throws reason `timeout`/`cancelled` |
| 4 MiB combined output | `:100`; `dist/process/ProviderProcess.js:341-363` | retention budget is `maxDiagnosticBytes - stdout.bytes - stderr.bytes` (combined, not per stream); once exceeded, `OwnedCommand` raises `output-limit` (`dist/process/OwnedCommand.js:85-86,99-100`) |
| 32 MiB recording input | `:184`, `:206` | `readStableArtifact` hard limit (`dist/artifacts/readStableArtifact.js:29-73`); also checks regular-file/identity stability |
| 64 MiB tool/limiter read | `:76`, `:82`, `:119`, `:121` | hash identity capture and post-run re-check |
| concurrency 1 | `:43-46`; `dist/process/ArtifactAnalysisResources.js:33-51` | second concurrent request returns `resource_constraint` with `max_concurrent_decodes: 1` |
| private workspace | `:85-88`, `:186-189` | `mkdtemp` under OS tmpdir (`dist/process/PrivateRuntimeRoot.js:27-38`), recording copy `0o400` |
| stop sequence | `dist/process/ProviderProcess.js:289-294` | SIGTERM, 250 ms grace, SIGKILL, 1 s grace |

Effective limits are reported in the result metadata as `{...LIMITS, ...effectiveLimits}` (`:159`), together
with both configured and resolved tool/limiter paths and argv (`:143-158`).

Error mapping for bounded-command failures (`dist/process/ArtifactAnalysisResources.js:127-152`):

- `cancelled` → `AnalysisCancelledError`
- `timeout` → `AnalysisTimeoutError(operation, 30000)` → `provider_timeout`
- `output-limit` → `AnalysisResourceConstraintError(..., {output_bytes: 4194304})` → `resource_constraint`
- snapshot signal `SIGXFSZ` → `file-size` constraint; `SIGXCPU` → `cpu` constraint
- other process failures → `AnalysisOutputError` → `unreadable_output`
- configuration-phase generic failures → `AnalysisCapabilityUnavailableError` → `capability_unavailable`
  (`dist/signals/SigrokRecordingProvider.js:305-313`)

Direct function checks (installed module imported, no target):

- `prlimitArgumentVector(BOUNDED_PRODUCER_LIMITS, "/opt/sigrok-cli")` returned exactly
  `["--as=1073741824:1073741824","--fsize=67108864:67108864","--cpu=30:30","--core=0:0","--","/opt/sigrok-cli"]`.
- `clampLinuxResourceLimits` with a synthetic inherited report of `536870912` AS, `1048576` fsize and `10`
  CPU returned `536870912` / `1048576` / `10`; with `unlimited` it returned the configured 1 GiB / 64 MiB /
  30 s; a duplicated `Max cpu time` line threw `Cannot establish inherited Linux limit: Max cpu time`.
- Host kernel report currently shows all three rows `unlimited`, so on this host the constants are used
  unchanged. Running the exact argv directly produced the kernel view
  `Max address space 1073741824`, `Max file size 67108864`, `Max cpu time 30`, `Max core file size 0`
  (exit 0).

Host tool facts: `/usr/bin/prlimit` is util-linux `2.42.4` sha256
`092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96`, size 27320. `sigrok-cli` is not on
PATH (`command -v` exit 1); `pacman -Q sigrok-cli libsigrokdecode` exit 1 with both packages not found.
No successful sigrok execution is possible on this host as configured.

### 6. Availability reporting vs registration (observation + one inference)

- `dist/server/createServer.js:103-129` builds `signalRecordingEnabled` as
  `options.signalRecording !== undefined || (linux && isAbsolute(environment.REA_SIGROK_COMMAND ?? ""))`.
- `dist/server/createServer.js:254` wraps it in `installSessionToolAvailability`; `:317-323` passes the
  resulting `policy` to the session status tool.
- `dist/server/registerSessionStatusTool.js:35-44` feeds that policy into `buildCapabilityInventory`;
  `dist/application/CapabilityInventory.js:285-291` maps `decode_signal_recording` /
  `inspect_signal_decoders` to `available` or `provider_missing` with remediation text.
- `dist/server/createServer.js:309` registers both tools regardless of that flag.
- The CLI registers the two commands unconditionally (`dist/cli/signalCommands.js:10-11,38-40`) and the
  dispatcher lists them in `--help` even with both env keys unset (observed: 17408-byte help output,
  sha256 `80df1883…04b10`, exit 0, lines 34 and 91 list both commands).

`[INFERENCE]` Because the predicate is only `isAbsolute`, an absolute but nonexistent, non-executable, or
wrong-version path makes capability inventory say `available` while every actual call refuses at `:74-75` or
`:140-142`. This is a reporting probe of string shape, not of the installation.

### 7. Environment-key census (observation; no invented keys)

Package-wide grep for `(REA_)?SIGROK[A-Z_]*` over `dist`, `skills`, and `README.md` yields exactly two
environment keys plus one JavaScript symbol:

- `REA_SIGROK_COMMAND` — selector for the sigrok executable (`dist/signals/SigrokRecordingProvider.js:71`;
  also bundle copies at `dist/cli-runtime/cli.js:1235` and `dist/mcp/main-kBXHZ8S5.js:18047`).
- `REA_SIGROK_PRLIMIT_COMMAND` — limiter override, default `/usr/bin/prlimit`
  (`dist/signals/SigrokRecordingProvider.js:77`).
- `SIGROK_PROVIDER_IDENTITY` — a module constant (`:22`), not an environment key.

There is no `REA_SIGROK_VERSION`, `REA_SIGROK_TIMEOUT`, `REA_SIGROK_MAX_*`, `SIGROK_COMMAND`,
`REA_SIGROK_PATH`, or shell-command variant. `parseConfig` has no sigrok key (`dist/config/*.js`). The
skill text names only `REA_SIGROK_COMMAND` (`skills/reverse-engineer-anything/SKILL.md:146-148`), and the
provider remediation text names both keys (`:311`).

### 8. Observation vs inference vs unknown

Observed:

- Exact source lines and bundle duplicates in §1-§7; file hashes in §Produced files.
- Nine CLI configuration probes with exact argv/env/exit/stdout/stderr (§Probes below).
- Host `/usr/bin/prlimit` version and the exact limits produced by REA's argv.
- Direct invocation of `prlimitArgumentVector` and `clampLinuxResourceLimits` from the installed module.
- `sigrok-cli`/`libsigrokdecode` absent; no system package installed.

`[INFERENCE]`:

- Availability inventory can claim `available` for a bad absolute path (only `isAbsolute` is checked).
- An address-space violation (`--as`) is likely projected as `execution_failure`/OOM exit, not
  `resource_constraint`, because only `SIGXFSZ`/`SIGXCPU` receive precise mappings.
- At `--cpu=30:30` and a 30 s wall deadline that starts before exec, the wall timeout will usually win the
  race; `SIGXCPU` classification may therefore be rare in practice.
- A path containing spaces is not split by REA (it is passed as one path); it would work only if the file
  name itself is that literal path. No such probe was run.

`[UNKNOWN]`:

- No successful `inspect_signal_decoders`/`decode_signal_recording` execution exists here; the host lacks
  sigrok-cli 0.7.2. Therefore nothing about decoder output, real limit reporting, or a held T1 verb is
  established by this seat.
- MCP `tools/list` and `binary_session` inventory output were not probed live; registration/inventory
  claims are source-read only.
- The behavior of sigrok-cli 0.7.2 under `--as=1 GiB` for large recordings is not exercised.

### 9. Probes (observation; non-counting)

Probes 2-10 used `npx -y rea-agents@6.5.0 <command> --format json --full-output`; probe 1 used
`--version` and probe 11 used `--help` without those flags. All ran with cwd `/tmp`; stderr was empty
(0 bytes, sha256 `e3b0c442…b855`) for every probe. Env overrides are exact; `-u` means unset. No target
artifact; where a probe reached an executable, its sha256 is given.

| # | argv / overrides | exit | observation | stdout bytes / sha256 |
|---|---|---|---|---|
| 1 | `--version`, both sigrok keys unset | 0 | `6.5.0` | 6 / `3eb8e06c…95b00` |
| 2 | `inspect-signal-decoders`, both keys unset | 1 | `capability_unavailable`; reason "Supply absolute REA_SIGROK_COMMAND…" | 836 / `d24b0a56…67dee` |
| 3 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=relative/sigrok-cli`, limiter unset | 1 | same code and byte-identical message as #2 | 836 / `d24b0a56…67dee` |
| 4 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/nonexistent/sigrok-cli`, limiter unset | 1 | `capability_unavailable`; realpath ENOENT | 812 / `2ca506cb…9e34f` |
| 5 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/usr/bin/prlimit`, `REA_SIGROK_PRLIMIT_COMMAND=prlimit` | 1 | limiter absolute check; "REA_SIGROK_PRLIMIT_COMMAND must be absolute." | 737 / `2b5737af…b8406` |
| 6 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/usr/bin/prlimit`, limiter unset | 1 | default limiter ran (`captured_output.stdout = "prlimit from util-linux 2.42.4\n"`, exit 0); version banner gate failed | 974 / `0fa86cc5…c792` |
| 7 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/usr/bin/prlimit`, `REA_SIGROK_PRLIMIT_COMMAND=/nonexistent/prlimit` | 1 | realpath ENOENT on limiter | 803 / `feeb6ba8…73fa8` |
| 8 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/usr/bin/prlimit`, `REA_SIGROK_PRLIMIT_COMMAND=` (empty) | 1 | "must be absolute" (empty is not defaulted) | 737 / `2b5737af…b8406` |
| 9 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND="/usr/bin/prlimit --version"` | 1 | realpath ENOENT on the whole string (no argument splitting) | 821 / `4c6f408b…204b10` |
| 10 | `inspect-signal-decoders`, `REA_SIGROK_COMMAND=/etc/hostname` | 1 | `EACCES` at the `X_OK` gate | 752 / `dbb59259…a3822` |
| 11 | `--help`, both keys unset | 0 | both signal commands listed; no preflight env gate | 17408 / `80df1883…04b10` |

The configured-tool hash reached in probes 5-8 is `/usr/bin/prlimit`
`092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96` (27320 bytes). Probe 10's rejected
path `/etc/hostname` hashes `694cd433b4212f7ed2f6b1bb23c8ef980056bf36de62d37e9f0a01c04f6fa194`. The
direct prlimit argv check used `/bin/sh` (`c14c8f49…3358d`) only to print `/proc/self/limits`.

## Coverage position

Nothing in this report counts toward R23-C1. All nine sigrok configuration probes (`#2-#10`) are typed
`capability_unavailable` refusals; `#1`/`#11` are version/help output. Refusals are explicitly non-counting. No
`inspect_signal_decoders` or `decode_signal_recording` evidence record was produced, and no T1 verb is
claimed held. This is an author-side source trace only.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SigrokOverride.md` — this report
  (only seat-written file; sha256 printed in the final handoff message).
- Ephemeral `/tmp` probe outputs (disposable, hashes inlined above): `sigrok-probe-version.out`
  `3eb8e06c…95b00`, `sigrok-probe-unset.out` `d24b0a56…67dee`, `sigrok-probe-relative.out`
  `d24b0a56…67dee`, `sigrok-probe-missing.out` `2ca506cb…9e34f`, `sigrok-probe-limiter-relative.out`
  `2b5737af…b8406`, `sigrok-probe-limiter-empty.out` `2b5737af…b8406`, `sigrok-probe-limiter-run.out`
  `0fa86cc5…c792`, `sigrok-probe-limiter-missing.out` `feeb6ba8…73fa8`, `sigrok-probe-args.out`
  `4c6f408b…204b10`, `sigrok-probe-noexec.out` `dbb59259…a3822`, `sigrok-probe-help.out`
  `80df1883…04b10`; every `.err` is 0 bytes `e3b0c442…b855`.
- Read-only installed inputs hashed: `package.json` `a5003023…050a6c`;
  `dist/signals/SigrokRecordingProvider.js` `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`
  (339 lines); `dist/process/LinuxResourceLimits.js`
  `00980570c40ed7d911e9e71bf4aa064d244187d19a805e2db241a319e214bbd6` (80 lines);
  `dist/process/ProviderProcess.js` `cb5e0869…d14ae4`;
  `dist/process/snapshotEnvironment.js` `bfccdd7f…4c5540`;
  `dist/process/ArtifactAnalysisResources.js` `a23fd673…0188df`;
  `dist/process/ProviderDeadline.js` `226b6e83…33964`;
  `dist/composition/signals.js` `5f102dc9…a62ce`;
  `dist/cli/signalCommands.js` `f033461c…b3eef`;
  `dist/application/signals/SignalRecordingService.js` `97a5ffcf…93aa8`;
  `dist/contracts/signals/signalToolContracts.js` `61553044…1f80`;
  `dist/server/createServer.js` `c5357924…80d56`;
  `dist/application/CapabilityInventory.js` `7e455299…9fd6`;
  `dist/cli-runtime/cli.js` `168cd322…e2204` (41847 lines);
  `dist/mcp/main-kBXHZ8S5.js` `12a70d8a…fe82e` (69389 lines).

## Installs

None. No pacman/uv/npm/cargo installs, no config edits, no host-service changes. `npx -y rea-agents@6.5.0`
used the already-present cached 6.5.0 package (cache mtime 2026-10-18); no package-manager transaction was
run. Pacman was not invoked; the `pacman -Q` queries were read-only and failed for absent packages.

## Open risks

- The availability flag (`createServer.js:108-109`) checks only `isAbsolute`; operators can see
  `available` for a missing or wrong-version binary until the first call refuses. Not fixed or probed here.
- Both executable and limiter are fully trusted; `REA_SIGROK_PRLIMIT_COMMAND` can name any executable and
  receives REA's fixed argv. The child also inherits the complete REA environment snapshot plus
  `REA_PROCESS_RUN_ID` (`ProviderProcess.js:26-31`), so unrelated environment values are visible to the
  caller-supplied tool. This is documented trust, not a sandbox.
- Limits are constants; there is no operator override for 1 GiB AS, 64 MiB fsize, 30 s CPU, 30 s wall,
  4 MiB output, or 32 MiB input. A legitimate large recording or decoder catalog above those bounds cannot
  be processed by configuration alone.
- The 30 s CPU soft/hard limit and 30 s wall deadline are equal and start at different moments (deadline
  before spawn); the observed classification of a CPU-limit hit is not exercised. `SIGXFSZ`/`SIGXCPU` are
  the only precisely mapped signals; AS exhaustion falls through to a generic execution failure.
- No live sigrok 0.7.2 exists on the host, so the version banner, `--dont-scan` behavior, and actual
  `prlimit` limit reporting on a real run remain unverified here. Source-only trace cannot establish
  provider behavior over time.
- Runtime bundles (`cli-runtime/cli.js`, `mcp/main-kBXHZ8S5.js`) duplicate the provider source; a future
  build could drift. This trace checked the selection block line-for-line but not the whole 339-line file.
