# SchemaSignalInventory — REA 6.5.0 `inspect-signal-decoders`

Seat: `KaidokuR23.SchemaSignalInventory` (scout, read-only lane member).
Date: 2026-10-21. Repo: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: CLI `--help`/`--schema`, installed REA 6.5.0 implementation, exact binary
override, version gate, and output fields. No recording decode, no hardware
acquisition, no device access, no debugger/Frida execution.

All source claims below are `[OBSERVED]` unless marked `[INFERENCE]` or
`[UNKNOWN]`. Command probes are listed with exit status; the success probes use
a caller-supplied extracted AppImage binary, not a host-installed `sigrok-cli`.

## Findings

### 1. CLI surface (observed)

`npx -y rea-agents@6.5.0 --version` -> stdout `6.5.0`, exit 0. The npx cache
copy used is `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(version 6.5.0; confirmed by `package.json` and by `capabilities`
`server_identity.package.root_path`).

`npx -y rea-agents@6.5.0 inspect-signal-decoders --help` -> exit 0:

```
Usage: rea inspect-signal-decoders [options]

Options:
  --decoder <string>  Exact installed decoder ID for help; null searches the decoder catalog (default: null)
  --query <string>    Case-insensitive literal substring in decoder ID/name or help lines; empty selects all (default: )
  --offset <number>   Number of matching decoders or help lines to skip; defaults to 0 (default: 0)
  --limit <number>    Maximum matching decoders or help lines to return; defaults to 50
  --all               Return all remaining matches
```

Global options include `--filter-output`, `--format <toon|json|yaml|md|jsonl>`,
`--full-output`, `--help`, `--llms`, `--llms-full`, `--schema`, `--token-count`,
`--token-limit`, `--token-offset`.

`npx -y rea-agents@6.5.0 inspect-signal-decoders --schema --format json` -> exit 0.
The CLI schema is **input-only** (no result/output schema) and contains:

| field | type | constraints | default |
|---|---|---|---|
| `decoder` | string or null | regex `^[a-zA-Z0-9_+\x2d]+$`, maxLength 256 | null |
| `query` | string | maxLength 8192 | `""` |
| `offset` | integer | min 0, max 9007199254740991 | 0 |
| `limit` | integer | exclusiveMinimum 0, max 9007199254740991 | CLI: optional |
| `all` | boolean | CLI-only | false |

`additionalProperties: false`. No field is required.

Two surfaces differ:

- Internal domain schema (`dist/domain/signals/signalDecoders.js:23-30`) makes
  `limit` nullable with default 50, where null means all remaining.
- The CLI (`dist/cli/signalCommands.js:16-35`) replaces `limit` with optional
  positive integer, adds `--all`, and rejects `--all` together with `--limit`
  as `VALIDATION_ERROR` exit 1 ("all and limit are mutually exclusive").
  `--limit 0` is also `VALIDATION_ERROR` exit 1. `--all` is converted to
  `{ limit: null }` before calling the service (`signalCommands.js:36`).

### 2. Installed implementation map

Package root:
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`

Relevant files and exact roles:

| path | lines | role |
|---|---|---|
| `dist/cli/signalCommands.js` | 11-37 | Registers the CLI command; CLI-only `limit`/`all`; mutual exclusion; `all` -> `limit:null`. |
| `dist/domain/signals/signalDecoders.js` | 3-31 | Input schema (`decoder`, `query`, `offset`, `limit`). |
| `dist/domain/signals/signalDecoders.js` | 32-69 | `signalDecodersSchema` result schema plus `superRefine` coverage invariants. |
| `dist/domain/signals/signalRecording.js` | 77-99 | Shared `tool`, `resource_limiter`, `limits`, `hardware_acquisition` shapes. |
| `dist/signals/parseDecoderDiscovery.js` | 5-65 | Parses `--list-supported` catalog and `--show` help; applies query/offset/limit. |
| `dist/signals/SigrokRecordingProvider.js` | 69-84 | Linux check, absolute env checks, realpath, X_OK, SHA-256, prlimit resolution. |
| `dist/signals/SigrokRecordingProvider.js` | 89-137 | Owned command wrapper, prlimit argv, captured output, post-run identity rechecks, nonzero-exit mapping. |
| `dist/signals/SigrokRecordingProvider.js` | 138-142 | `--version` invocation and exact version gate. |
| `dist/signals/SigrokRecordingProvider.js` | 143-161 | Builds `diagnostics`, `tool`, `resource_limiter`, `limits`, `hardware_acquisition`. |
| `dist/signals/SigrokRecordingProvider.js` | 162-181 | Catalog/help producer argv and result assembly. |
| `dist/application/signals/SignalRecordingService.js` | 47-66 | Input parse, provider call, output schema re-parse, selection/subject identity checks. |
| `dist/contracts/toolEffects.js` | 112-116 | Effects: `mutatesSession`, `launchesProcess`, `writesFilesystem`. |
| `dist/application/CapabilityInventory.js` | 285-291 | Optional-provider availability report for both signal verbs. |
| `dist/server/createServer.js` | 103-109 | MCP-time enable heuristic: Linux and absolute `REA_SIGROK_COMMAND`. |
| `dist/server/sessionAvailabilityPolicy.js` | 3-8 | Defaults signal availability to false unless configured. |
| `dist/process/LinuxResourceLimits.js` | 10-26 | Fixed producer limits and prlimit argv construction. |
| `dist/process/LinuxResourceLimits.js` | 28-49 | Clamps configured limits down to stricter inherited `/proc/self/limits`. |

File digests (SHA-256) of the exact cached implementation read:

```
168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204  dist/cli-runtime/cli.js
cb052ebc2ffe3ac5931179b5e137bcf8c8c7c94cb2cdc3c5ae500b29c63040d5  dist/domain/signals/signalDecoders.js
7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7  dist/signals/SigrokRecordingProvider.js
```

### 3. Exact binary override and version gate

Binary override is environment-only; there is no CLI flag for the binary.

- `REA_SIGROK_COMMAND` (`SigrokRecordingProvider.js:71`): must be an absolute
  path. If unset or relative, the call fails before spawn with
  `capability_unavailable` / `unsupported_provider` / `retryable:false`
  (lines 72-73, mapped through the `configuration` phase).
- The path is `realpath`-resolved (line 74), checked `X_OK` (line 75), read up
  to 64 MiB, and SHA-256 hashed (line 76). `tool.configured_path` keeps the
  literal env value; `tool.path` and `tool.sha256` describe the resolved file.
- The resolved executable is hashed again after every production command; any
  change fails with `AnalysisArtifactChangedError` (lines 119-125).
- `REA_SIGROK_PRLIMIT_COMMAND` (`SigrokRecordingProvider.js:77`): defaults to
  `/usr/bin/prlimit`; must be absolute; same realpath/X_OK/hash and post-run
  recheck (lines 78-82, 120-123).
- Platform gate: `this.platform !== "linux"` fails at line 69. This host is
  Linux/x64, so the platform gate was not exercised as a refusal.
- Every invocation, including `--version`, runs as
  `prlimit <limit-args> -- <command> <producer-args>` (lines 89-107). The full
  host environment is passed to the child (`hostEnvironment: this.environment`,
  line 97). This is why library/Python env workarounds below reached sigrok.
- Fixed limits (`LinuxResourceLimits.js:10-17`) and observed prlimit argv:

```
--as=1073741824:1073741824
--fsize=67108864:67108864
--cpu=30:30
--core=0:0
--
<resolved command path>
```

- Effective limits are the configured values clamped downward by inherited
  soft/hard limits read from `/proc/self/limits` (lines 28-61). On this host the
  observed effective limits equal the configured values: input 33554432 B,
  output 4194304 B, timeout 30000 ms, address space 1073741824 B, file
  67108864 B, CPU 30 s.

Version gate (`SigrokRecordingProvider.js:138-142`):

1. Run `<command> --version` through the same prlimit wrapper.
2. Accept only if stdout matches `/^sigrok-cli 0\.7\.2(?:\r?\n|$)/u` **and**
   stdout contains the literal `libsigrokdecode`.
3. Otherwise fail with message
   `Expected sigrok-cli 0.7.2 with libsigrokdecode; inspect the selected installation.`
   in the `configuration` phase, i.e. `capability_unavailable` /
   `unsupported_provider` / `retryable:false`, with captured stdout/stderr/exit
   in `details.captured_output` when available.

Consequences observed from source and probes: the gate is stdout-only, exact
`0.7.2`, and can be satisfied by any executable that prints the expected banner
and contains the substring. Provenance is only the SHA-256 of the configured
file; a wrapper script is hashed as a wrapper, and its inner binary and decoder
modules are not fingerprinted (also stated in the result limitations).

Producer argv (`SigrokRecordingProvider.js:162-166`):

- Catalog (`decoder: null`): `--dont-scan --list-supported`
- Help (`decoder: <id>`): `--dont-scan --protocol-decoders=<id> --show`

Both are prefixed by the prlimit vector; the producer cwd is a private runtime
workspace, although catalog/help do not read or write a recording. The result
always reports `hardware_acquisition: "not-performed"`.

Failure classes observed:

- Missing/relative binary: `capability_unavailable`, exit 1.
- Banner mismatch (`/bin/true`): `capability_unavailable`, exit 1, captured
  stdout was GNU true 9.12, `exit_code: 0`.
- Invalid decoder ID syntax (`uart!`): CLI `VALIDATION_ERROR`, exit 1, before
  any spawn.
- Valid-syntax but unavailable decoder (`nope`, `signature`): producer exits 1,
  mapped to `execution_failure`, exit 1, with `details.diagnostics` containing
  `exit_code`, `stdout`, and `stderr`. This is a producer failure, not a
  capability refusal.

### 4. Output fields

Success envelope (`--format json --full-output`): `{ ok: true, data: <Evidence>, meta: { command, duration } }`.

`data` fields observed:

```
evidence_id
subject: { name, digest: { sha256 }, local_path, format, architecture }
provider: { id: "sigrok-recording", name: "REA sigrok recording adapter", version: "sigrok-cli@0.7.2" }
analysis_profile: null
predicate_type: "rea.analysis"
operation: "inspect_signal_decoders"
parameters: <normalized input>
raw_result: null
normalized_result: <signalDecodersSchema result>
confidence: "observed"
authority: "shipped-artifact"
environment: null
limitations: [ ... ]
relationship_coverage: null
locations: []
evidence_links: []
```

`normalized_result` fields (`signalDecoders.js:32-69`):

```
selection: {
  decoder: string|null,
  query: string,
  offset: integer,
  limit: integer|null
}
decoders: [ { id: string, name: string } ]      // catalog mode only
help_lines: [ { line_number: integer>=1, text: string } ]  // help mode only
output_window: {
  unit: "decoders" | "help-lines",
  examined: integer,
  matching: integer,
  returned: integer,
  has_more: boolean
}
diagnostics: string        // selected producer command's stderr
tool: {
  configured_path: string,
  path: string,
  sha256: string,
  version_banner: string,  // full stdout of `--version`
  version_diagnostics: string,  // stderr of `--version`
  arguments: string[]      // producer args only, no prlimit prefix
}
resource_limiter: {
  configured_path: string,
  path: string,
  sha256: string,
  arguments: string[]      // limit flags + "--" + command path
}
limits: {
  input_bytes, output_bytes, command_timeout_ms,
  address_space_bytes, file_bytes, cpu_seconds
}
hardware_acquisition: "not-performed"
```

Coverage invariants enforced by `superRefine`:
`unit` matches the selected mode, `matching <= examined`,
`returned == min(max(0, matching-offset), limit ?? remaining)`, only the
selected array is populated, and `has_more == remaining > returned`.

Parsing details (`parseDecoderDiscovery.js:5-65`):

- Catalog: find the exact line `Supported protocol decoders:`; every nonempty
  line after it must match `^ {2}([a-zA-Z0-9_+-]+) +(.+)$` and be unique. A
  missing heading, malformed line, duplicate ID, or empty catalog fails the
  whole request. The hardware-driver section before the heading is ignored.
- Help: line 1 must be exactly `ID: <decoder>`. All remaining lines become
  `help_lines` with 1-based line numbers. A trailing final newline is dropped;
  internal blank lines are retained.
- More than 65,535 LF separators raises `DecoderDiscoveryBudgetError`, mapped
  to an `AnalysisResourceConstraintError` with `{ line_budget: 65536 }`.
- `query` is a case-insensitive literal substring (`.toLowerCase().includes`).
  In catalog mode it matches only `` `${id} ${name}` ``; in help mode it
  matches every literal help line. `offset` is clamped to the matching length;
  `limit:null` returns all remaining.
- Strings are copied through a UTF-16LE round trip; this is an identity copy
  for valid JS strings, not normalization.

Observed result examples (all with the target below):

| probe | parameters | output_window | notes |
|---|---|---|---|
| catalog default | `{decoder:null,query:"",offset:0,limit:50}` | `{unit:"decoders",examined:110,matching:110,returned:50,has_more:true}` | first 50 decoders, `ac97` ... `jtag_stm32`; non-empty `diagnostics`. |
| help `uart` | `{decoder:"uart",query:"",offset:0,limit:50}` | `{unit:"help-lines",examined:81,matching:81,returned:50,has_more:true}` | `help_lines` 1-50, beginning `ID: uart`, `Name: UART`, options follow beyond page 50. |
| catalog query page | `{decoder:null,query:"uart",offset:1,limit:3}` | `{unit:"decoders",examined:110,matching:1,returned:0,has_more:false}` | `query:"uart"` matched only decoder id `uart`; offset 1 skipped the sole match. |
| catalog query all | `{decoder:null,query:"uart",offset:0,limit:null}` | `{unit:"decoders",examined:110,matching:1,returned:1,has_more:false}` | `selection.limit` is null; decoder `{id:"uart",name:"Universal Asynchronous Receiver/Transmitter"}`. |
| catalog query `signature` | `{decoder:null,query:"signature",offset:0,limit:null}` | `{unit:"decoders",examined:110,matching:0,returned:0,has_more:false}` | `signature` is absent from the 110-entry catalog but its load failure is in `diagnostics`. |
| help `signature` | `{decoder:"signature",...}` | n/a (`execution_failure`) | exit 1, producer stderr shows the Python 3.5 syntax error. |

`arguments` observed:
catalog `["--dont-scan","--list-supported"]`;
help `["--dont-scan","--protocol-decoders=uart","--show"]`.
`resource_limiter.arguments` observed includes the four limit flags, `--`, and
the resolved command path, but not the producer args.

### 5. Installed target used for the positive probes

The host has no `sigrok-cli` on `PATH` and no pacman package (R22 observation;
rechecked here: `which sigrok-cli` returned nothing). The pre-existing
caller-supplied artifact is:

```
/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage
size 49,558,848 bytes
sha256 49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614
```

Running the AppImage directly, or its `AppRun`, fails:

```
sigrok-cli: symbol lookup error: /usr/lib/libgio-2.0.so.0: undefined symbol: g_module_open_full
exit 127
```

`[INFERENCE]` The bundled `libgmodule` 2.48.2 is found before host `libgmodule`
2.90.1 while host `libgio` 2.90.1 expects `g_module_open_full`. Two workarounds
worked observably for `--version`:

```
LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0
LD_LIBRARY_PATH=/usr/lib:<extract>/usr/lib
```

For the REA probes the second form was used. The extracted binary and decoder
runtime need:

```
REA_SIGROK_COMMAND=<extract>/usr/bin/sigrok-cli
LD_LIBRARY_PATH=/usr/lib:<extract>/usr/lib
PYTHONHOME=<extract>/usr
PYTHONPATH=<extract>/usr/share/pyshared
SIGROKDECODE_DIR=<extract>/usr/share/libsigrokdecode/decoders
```

Observed identities:

```
10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd  <extract>/usr/bin/sigrok-cli
4bfe11a3b76fee2c6847a9638fff82f1b8078ed56d8a9b182f78cba0f28b80b3  <extract>/usr/lib/libsigrokdecode.so.4.2.1
092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96  /usr/bin/prlimit
```

Version banner observed from the extracted binary (and captured in every
successful result's `tool.version_banner`):

```
sigrok-cli 0.7.2

Libraries and features:
- libsigrok 0.5.2/5:1:1 (rt: 0.5.2/5:1:1).
 - glib 2.48.2 (rt: 2.90.1/9001:1)
 - libzip 1.0.1
 - libserialport 0.1.1/1:0:1 (rt: 0.1.1/1:0:1)
 - libusb-1.0 1.0.30.12037 API 0x01000104
 - hidapi 0.8.0-rc1
 - bluez 5.37
 - libftdi 1.2
 - Host: x86_64-pc-linux-gnu, little-endian.
 - SCPI backends: TCP, RPC, serial, USBTMC.
- libsigrokdecode 0.5.3/6:1:2 (rt: 0.5.3/6:1:2).
 - glib 2.48.2 (rt: 2.90.1/9001:1)
 - Python 3.5.2 / 0x30502f0 (API 1013, ABI 3)
 - Host: x86_64-pc-linux-gnu, little-endian.
```

The bundled decoder directory contains 112 entries. The catalog returned 110:
`common` is a shared support package (`plugtrx`, `sdcard`, `srdhelper`) and not
a decoder record, while `signature` fails to load because it uses a Python 3.6+
int-literal underscore (`0b0000_0010_1001_0001`) in
`decoders/signature/pd.py:138`, which the bundled Python 3.5.2 rejects. The
failure is surfaced verbatim in `normalized_result.diagnostics` on otherwise
successful catalog calls; it does not prevent the 110 valid records from being
parsed. `--decoder signature --show` instead fails as `execution_failure`.

### 6. Probe log (argv, env, exit)

Working directory `/tmp` for all probes. `npx` resolved to the cached 6.5.0
package. Where `--format` is shown, `--full-output` was also passed.

1. `npx -y rea-agents@6.5.0 --version` -> exit 0, stdout `6.5.0`.
2. `npx -y rea-agents@6.5.0 inspect-signal-decoders --help` -> exit 0.
3. `npx -y rea-agents@6.5.0 inspect-signal-decoders --schema --format json`
   -> exit 0, input-only JSON schema above.
4. `env -u REA_SIGROK_COMMAND -u REA_SIGROK_PRLIMIT_COMMAND \
   npx -y rea-agents@6.5.0 inspect-signal-decoders --format json --full-output`
   -> exit 1, `capability_unavailable`, reason
   `Supply absolute REA_SIGROK_COMMAND for sigrok-cli 0.7.2 with libsigrokdecode.`
5. Same as (4) with `REA_SIGROK_COMMAND=sigrok-cli` (relative) -> exit 1,
   same capability refusal.
6. `REA_SIGROK_COMMAND=/bin/true npx -y ... inspect-signal-decoders ...`
   -> exit 1, `capability_unavailable`, reason begins
   `Expected sigrok-cli 0.7.2 with libsigrokdecode`; `captured_output` contains
   GNU true 9.12 stdout, empty stderr, `exit_code:0`.
7. Success env (once per probe):
   `REA_SIGROK_COMMAND`, `LD_LIBRARY_PATH`, `PYTHONHOME`, `PYTHONPATH`,
   `SIGROKDECODE_DIR` as in section 5, then
   `npx -y rea-agents@6.5.0 inspect-signal-decoders ... --format json --full-output`:
   - default -> exit 0, `ok:true`, evidence
     `ev_18bf084c8afece5613184b4489e167c0fa100ea7e0b474cfd7a422fc83cd936b`,
     `examined:110`, duration 279 ms.
   - `--decoder uart` -> exit 0, evidence
     `ev_5904588a553178488605bf9ebfa43f0b9cde62575192c79ac209e90ff85a6f41`,
     `examined:81`, duration 110 ms.
   - `--query uart --offset 1 --limit 3` -> exit 0, evidence
     `ev_17118125e00ba4fb56460872ca3952564985feb5200a744a5fcf928f1766627e`,
     `matching:1`, `returned:0`, duration 186 ms.
   - `--query uart --all` -> exit 0, evidence
     `ev_418e59a924f2445af52543c062af2a883cec3e91a3acba4929c89f3096b48af8`,
     `limit:null`, `returned:1`, duration 181 ms.
   - `--query signature --all` -> exit 0, evidence
     `ev_8be39f104450cea4b7060c50e2e9061afe9e61607dd3552245c66693b9233113`,
     `matching:0`, `returned:0`, duration 179 ms.
8. `--decoder nope` with the success env -> exit 1, `execution_failure`,
   diagnostics `exit_code:1`, stderr
   `srd: ImportError: Failed to load decoder nope...`.
9. `--decoder 'uart!'` -> exit 1, CLI `VALIDATION_ERROR`
   (regex `^[a-zA-Z0-9_+\x2d]+$`).
10. `--all --limit 5` -> exit 1, `VALIDATION_ERROR`
    (`all and limit are mutually exclusive`); `--limit 0` -> exit 1,
    `VALIDATION_ERROR` (`Too small: expected number to be >0`).
11. `npx -y rea-agents@6.5.0 capabilities --format json --full-output` exited
    0 with and without `REA_SIGROK_COMMAND` and reported `ok:true`. Neither
    that output nor `doctor --format json --full-output` (exit 1 with and
    without `REA_SIGROK_COMMAND`; `ok:false` because Hopper is missing, an
    unrelated check) printed a `sigrok`/signal capability group or check in
    either state. `[UNKNOWN]` whether the CLI capability/doctor projections
    intentionally omit optional signal providers; the source availability path
    exists at `CapabilityInventory.js:285-291` and is wired for MCP policy at
    `createServer.js:103-109`.

Every success result carried `confidence:"observed"`,
`authority:"shipped-artifact"`, `hardware_acquisition` literal
`"not-performed"`, and limitations stating no hardware discovery, recording
read, or acquisition was requested. `subject.sha256` equaled the extracted
binary SHA-256; `resource_limiter.sha256` equaled the `/usr/bin/prlimit`
SHA-256.

### 7. Coverage relevance and limits

This is an inventory-only probe. It does not decode any recording and does not
exercise hardware discovery or acquisition. It produced `ok:true` Evidence for
`inspect_signal_decoders` against a caller-supplied sigrok-cli 0.7.2 binary,
with the selected binary and prlimit identities bound inline. It does not
demonstrate `decode_signal_recording`, and it does not establish dynamic or
device ownership. Whether this evidence supports R23-C1, and how to bind it
into the lane, is L1's call; this report is author-side, not outside
verification.

Observed text-vs-behavior caveats:

- The CLI `--schema` exposes only inputs, not the result schema. Consumers must
  take the output shape from `signalDecodersSchema`/`signalRecordingSchema` or
  from the actual Evidence.
- A successful catalog call can still carry nonempty `diagnostics` (the
  `signature` load failure). `hardware_acquisition:"not-performed"` is a
  declared result field, not an independent syscall audit of `--dont-scan`.
- `query:"uart"` matched only the single decoder id `uart`, because catalog
  matching is against `id + " " + name`; it is not a fuzzy/prefix search.
- The version gate is stdout banner matching, not signature/provenance
  verification. A wrapper satisfies it while hiding the inner executable, and
  decoder modules/libraries are not fully fingerprinted (stated by REA's own
  limitations).
- The positive probe depended on host-library ordering and Python/decoder path
  environment; the stock AppImage/AppRun does not launch on this host. This is
  not a clean installed sigrok. Any lane-bound rerun should use the
  BuildSigrok launcher and record the wrapper and inner binary identities
  separately.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaSignalInventory.md`
  (this report; post-write SHA-256 reported in the final message because a
  self-referential digest cannot be embedded stably).
- No lane evidence, production file, or other authored output was written.
- Temporary scratch used only to read/run the pre-existing AppImage:
  `/tmp/sigrok-extract/` (extracted with the AppImage's
  `--appimage-extract`). It is outside the lane and is not a deliverable;
  no repo, fleet, MANIFEST, runtime, or operator configuration was touched.

## Installs

None. No pacman, uv, npm global, cargo, or release-binary install/upgrade was
performed. The npx cache already contained rea-agents 6.5.0; the AppImage was
pre-existing and was not installed or moved into `PATH`. Host pacman
transactions remain paused.

## Open risks

1. The successful probes are author-side and depend on a temporary extracted
   AppImage plus host-first library ordering. They are not lane-bound evidence
   and must be rerun through the BuildSigrok launcher for any retained claim.
2. The bundled decoder runtime is Python 3.5.2; at least `signature` fails to
   load, so `examined:110` is 110 catalog rows, not proof that every shipped
   decoder module is loadable. `--decoder signature` fails at execution time.
3. The AppImage banner reports glib built 2.48.2 against runtime 2.90.1; this
   ABI mismatch is the cause of the direct-launch failure. A wrapper that fixes
   it may mask further ABI issues in individual decoders.
4. `--dont-scan` and `hardware_acquisition:"not-performed"` are REA-declared
   behavior; no independent audit of device syscalls was performed, and this
   report makes no such claim.
5. CLI `capabilities`/`doctor` did not surface the signal provider in either
   env state. The reason is unknown; do not infer availability from those
   commands without rerunning and inspecting the MCP policy path.
6. `[UNKNOWN]` Whether `inspect-signal-decoders` on a wrapper's inner binary
   will rehash or detect changes to libraries loaded at runtime; source only
   rehashes the configured wrapper file. Decoder module changes are explicitly
   not fingerprinted.
