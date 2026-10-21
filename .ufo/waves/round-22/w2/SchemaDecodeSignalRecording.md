# SchemaDecodeSignalRecording — REA 6.5.0 `decode-signal-recording` schema authority review

Seat: `KaidokuR22R.SchemaDecodeSignalRecording-6` (scout, leaf). Recovery evidence/review wave; this is a schema review, not a held execution. Author-side only, not outside admission.

## Verdict (TL;DR)

- **Counter binding matches.** `count-c1.py` gets the operation to match by turning `decode-signal-recording` into `decode_signal_recording` (`verb.replace('-', '_')` in `.ufo/waves/round-21/tools/verb-coverage.py:85`). That string is exactly the provider constant `OPERATION = "decode_signal_recording"` (`dist/signals/SigrokRecordingProvider.js:21`) and the Evidence `operation` field written at `:245`. There is no special case for this verb.
- **Cannot be held on this host as it is today.** `sigrok-cli` is not installed (`exit 127`, `pacman -Qi` exit 1). `libsigrokdecode` is not installed (`pacman -Qi` exit 1). `REA_SIGROK_COMMAND` is unset. Any run would fail in the `configuration` phase with `AnalysisCapabilityUnavailableError`, which is projected as `capability_unavailable`. Both the `error` key and that code are in the counter's `REFUSALS`, so the result would be `evidence_refused` and would not count. This is in line with the claim's falsifier "a typed refusal envelope counts". `[INFERENCE: not executed, derived from source]`
- **claims.json has no input or effect limits for this verb.** It only lists the verb in `R22-C1.t1` (line 17) and the counting and falsifier rules. There is nothing in it to compare against REA's limits. The limits below are REA's own authority, taken from `--schema` and the source.
- **Calibration gap (new).** A successful run that exits 0 with **empty output** (`output_window.total_lines: 0`) is a bound, non-refused record, so the counter would count it. REA's own limitation text says "Empty output does not establish absence of traffic." None of the four C1 falsifiers excludes this case.

## Commands and observed exits

All commands ran in `/tmp`. Package resolved from npx cache `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version `6.5.0`. `npx -y rea-agents@6.5.0 --version` printed `6.5.0`.

| argv | exit | output |
|---|---|---|
| `npx -y rea-agents@6.5.0 decode-signal-recording --help` | 0 | stdout sha256 `6134b1b24508f23c12aeea0664ab7b919b9b024116bbfb5c04927c591001133d`; stderr empty |
| `npx -y rea-agents@6.5.0 decode-signal-recording --schema` | 0 | stdout (toon) sha256 `3631c903bcee3d9f0c10ff10d70221fda28e0756b9c7ebd67f912e6a6ad85f61` |
| `npx -y rea-agents@6.5.0 decode-signal-recording --schema --format json > /tmp/dsr-schema.json` | 0 | sha256 `baf2134dfe90d819b3fee2158c87add7ebe5e90b045350f26d33506c65fdbc8c` (scratch, not retained in lane) |
| `npx -y rea-agents@6.5.0 --llms-full` (section extracted) | 0 | same option table as `--help`; `--input_format` and `--annotations` typed `unknown` (nullable) |
| `sigrok-cli --version` | 127 | `error: command not found: sigrok-cli` |
| `prlimit --version` | 0 | `prlimit from util-linux 2.42.4`; `/usr/bin/prlimit` sha256 `092bb6db10a743ecccfc7d6e72055007064abf8910c85d736832fb53697fff96` |
| `pacman -Qi sigrok-cli` / `pacman -Qi libsigrokdecode` | 1 / 1 | not installed |
| `pacman -Si sigrok-cli` (read-only sync-DB query, no transaction) | 0 | `Repository: extra`, `Version: 0.7.2-3` |
| env presence test `REA_SIGROK_COMMAND`, `REA_SIGROK_PRLIMIT_COMMAND` | — | both `unset` (presence only, values not read) |
| host | — | `Linux x86_64`, `node v24.21.0` |

Not executed: the target command itself, any recording decode, any `sigrok-cli` invocation, and any input-validation probe. The scope was `--help`/`--schema` only.

## Source paths (REA 6.5.0, npx cache root `…/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`)

| file | sha256 | role |
|---|---|---|
| `dist/cli/signalCommands.js` | `f033461c4c136296b4abeb3315e8572438a5654bc7615283626abf0b671b3eef` | CLI registration; `path` → `resolve(args.path)`; `--all_lines` → `line_limit: null`; `all_lines`/`line_limit` mutually exclusive |
| `dist/domain/signals/signalRecording.js` | `0ef15149da472d82559d907bef4bbeabedd19c6de953978f6a04af48f4040171` | input schema, 32 KiB selector budget, output `signalRecordingSchema` |
| `dist/signals/SigrokRecordingProvider.js` | `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7` | provider, prerequisites, argv, limits, error mapping, Evidence creation |
| `dist/process/LinuxResourceLimits.js` | not hashed | `BOUNDED_PRODUCER_LIMITS`, prlimit argv |
| `dist/contracts/signals/signalToolContracts.js` | not hashed | MCP contract description/example |
| `dist/contracts/toolEffects.js:117` | not hashed | effect audit |
| `dist/application/CapabilityInventory.js:285-291` | not hashed | `provider_missing` remediation text |
| `dist/domain/analysisErrorProjection.js:142-157` | not hashed | error class → code projection |

## Exact input limits (REA authority)

| field | `--schema` (CLI) | runtime domain schema (`signalRecording.js`) |
|---|---|---|
| `path` (positional) | `string`, required | `localPathStringSchema` (absolute). The CLI pre-resolves relative paths with `resolve()`. |
| `--decoders` | required, `string`, `minLength 1`, `maxLength 8192` | same, **plus `refine: no NUL`** |
| `--input_format` | `string 1..8192 \| null`, default `null` (= sigrok autodetect) | same, plus no-NUL |
| `--annotations` | `string 1..8192 \| null`, default `null` | same, plus no-NUL |
| `--line_offset` | `integer`, `0..9007199254740991`, default `0` | `int ≥ 0`, default `0` |
| `--line_limit` | `integer`, `exclusiveMinimum 0`, max `2^53-1`, **no default shown** | `int > 0 \| null`, **default `50`**; `null` = all remaining lines |
| `--all_lines` | `boolean`, default `false` | CLI-only; mapped to `line_limit: null`; error if combined with `--line_limit` |
| combined selectors | **not shown in `--schema`** | `Σ(byteLength(prefix)+byteLength(value)+9) ≤ 32768` over `--protocol-decoders=`, `--input-format=`, `--protocol-decoder-annotations=` |
| extra keys | `additionalProperties: false` | `strictObject` |

Gaps between `--schema` and runtime, i.e. places where `--schema` shows less than is enforced:

1. The NUL-character refinement is not visible.
2. The 32 KiB UTF-8 byte budget across all selectors is not visible. A set of selectors that passes `--schema` can still be rejected.
3. `maxLength 8192` counts UTF-16 code units, while the budget counts UTF-8 bytes.
4. The default of 50 for `line_limit` appears only in the description text, not as a schema `default`.

## Runtime resource and effect limits

From `BOUNDED_PRODUCER_LIMITS`, enforced through `prlimit` with soft and hard limits pinned together. Stricter inherited limits are kept and reported in the result as `limits`.

- `input_bytes` 32 MiB: a larger recording fails with `resource_constraint` (`file-size`).
- `output_bytes` 4 MiB of combined output: overflow fails.
- `command_timeout_ms` 30 000 per command.
- `--as=1073741824:1073741824` (1 GiB address space), `--fsize=67108864:67108864` (64 MiB), `--cpu=30:30`, `--core=0:0`.
- Concurrency: `max_concurrent_decodes: 1`. A second active operation is rejected.
- Effects (`toolEffects.js:117`): `mutatesSession: true`, `launchesProcess: true`, `writesFilesystem: true`, everything else at the default (`mutatesTarget`, `accessesNetwork`, `changesUiState`, `mayDiscardData`, `executesForeignCode`, `mutatesDevice` all `false`), `idempotent: true`. Derived MCP annotations: `readOnlyHint: false`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: true`.
- Filesystem write: a private runtime root with prefix `rea-sigrok-`. It holds one copy of the recording named `recording` (`flag wx`, `mode 0400`), which is used as the producer's working directory. The original file is never handed to sigrok.
- Integrity checks after the run: the sha256 values of the sigrok executable and the limiter are re-read and compared (a change gives `AnalysisArtifactChangedError`), and so is the sha256 of the private copy.
- Not performed: hardware. The run passes `--dont-scan`, and the result carries `hardware_acquisition: "not-performed"` as a literal.
- `executesForeignCode: false` is REA's classification. It treats the caller-supplied sigrok-cli and its Python decoder modules as trusted tools, not as target code. The source says "not an OS sandbox".

## Required host and provider prerequisites (in check order, `configuration` phase)

1. `process.platform === "linux"`. Met.
2. `REA_SIGROK_COMMAND` must be an **absolute** path. It must resolve through `realpath`, pass `X_OK`, and be readable at ≤64 MiB. **Not met: unset.**
3. `REA_SIGROK_PRLIMIT_COMMAND`, default `/usr/bin/prlimit`, must be absolute, executable, and readable. Met (util-linux 2.42.4).
4. Linux resource limits must be readable.
5. The `--version` probe runs the configured sigrok under prlimit. Its stdout must match `^sigrok-cli 0\.7\.2(\r?\n|$)` and contain `libsigrokdecode`. **Not met: binary absent.** This step runs the caller-supplied sigrok binary *before* the recording is read.
6. A local recording file of ≤32 MiB. No existing lane fixture for this verb was found: `.ufo/waves/round-22/evidence/c1/` holds only `identify-godot*` files.

Install path: `sigrok-cli 0.7.2-3` exists in Arch `extra` according to the sync DB. pacman transactions are paused host-wide, though, and "no tool install expected". **No install performed.** `[INFERENCE]` An official sigrok release binary might be an alternative channel; I did not verify it.

## Output and operation binding

The produced argv is `<prlimit> --as=… --fsize=… --cpu=… --core=0:0 -- <sigrok> --dont-scan --input-file=recording --protocol-decoders=<decoders> --protocol-decoder-samplenum [--input-format=<fmt>] [--protocol-decoder-annotations=<ann>]`. Each selector is passed as one argv element, never through a shell.

Evidence fields (`SigrokRecordingProvider.js:244-251`, `:221-234`):

- `operation: "decode_signal_recording"`
- provider `{id: "sigrok-recording", name: "REA sigrok recording adapter", version: "sigrok-cli@0.7.2"}`
- `confidence: "observed"`
- `parameters`: the full input
- `subject {path, sha256, format: "file"}`
- `locations [{kind: "artifact-path", path}]`
- four `limitations` strings

The result is a `signalRecordingSchema` strict object:

- `artifact {path, sha256, bytes}`
- `selection`
- `annotations_text` (verbatim display lines, sample ranges preserved)
- `output_window {total_lines, returned_lines, has_more}`, checked with a superRefine for consistency with the offset and limit
- `diagnostics` (all stderr, including warnings on exit 0)
- `tool {configured_path, path, sha256, version_banner, version_diagnostics, arguments}`
- `resource_limiter {configured_path, path, sha256, arguments}`
- `limits {input_bytes, output_bytes, command_timeout_ms, address_space_bytes, file_bytes, cpu_seconds}`
- `hardware_acquisition: "not-performed"`

## Counter mapping (R22-C1)

- `count-c1.py` T1 includes `decode-signal-recording`. A record binds when `record.operation == "decode_signal_recording"` and its `evidence_id` (`ev_` followed by 64 hex characters) appears in an eligible knowledge entry and in a cited file under `.ufo/waves/round-22/evidence/c1/`.
- How each failure path projects, and what the counter does with it:

| failure | projected code | counter result |
|---|---|---|
| missing sigrok, wrong version, missing `REA_SIGROK_COMMAND` | `capability_unavailable` | refused |
| non-zero sigrok exit (`ProviderAdapterError`, diagnostics carry `exit_code`) | `execution_failure` | refused |
| bad input | `AnalysisInputError` → `invalid_request` | refused |
| oversized recording | `resource_constraint` (`file-size`) | `[INFERENCE]` not in `REFUSALS`, but the envelope's `error` key → refused |

- The success record carries no top-level `exit_code`, so `refused()` lets a real success through. Correct.
- **Gap:** an exit-0 empty decode (`total_lines: 0`, `annotations_text: ""`) also binds. This happens, for example, with a wrong channel or baud rate. If L1 wants calibration to survive scrutiny, the knowledge entry should state `total_lines > 0`, or the claim should name this limitation. This is a recommendation; the frozen claim was not edited.

## Observed lane state

- Lane `HEAD` = `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`. This differs from the claim baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`. I observed this only; the lineage was not checked.
- `decode-signal-recording` appears in `.ufo/waves/round-20/verify/round20/verb-coverage.json` as a catalog verb. A grep found no mention in `corpus/` or `PROVINCE.md`, which is consistent with "zero-mention at baseline".

## Unknowns

- Whether the CLI's refusal envelope for this verb carries a top-level `evidence_id`+`operation`. Either way the counter returns refused or unbound.
- Behaviour of a real sigrok-cli 0.7.2 against the `--version` regex. The Arch `0.7.2-3` banner was not observed.
- Whether a provider-owned recording fixture (for example a synthesized VCD) would be accepted as "uncovered coverage-map ground" by L1.

## Tooling record

No installs or updates. No pacman transaction. No MCP device use; REA was used only through `npx -y rea-agents@6.5.0`, already cached. No ADB, device, network, or debugger contact.
