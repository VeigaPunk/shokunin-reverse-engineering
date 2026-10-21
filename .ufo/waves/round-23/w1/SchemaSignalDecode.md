# SchemaSignalDecode — decode-signal-recording schema/source

Seat: read-only scout (leaf). Scope: REA 6.5.0 `decode-signal-recording` `--help`/`--schema`
plus installed implementation and the exact sigrok 0.7.2 producer contract it emits.
No recording was decoded, no sigrok binary was launched, no device/process was touched.
Author-side observations only; nothing here is outside verification.

## Probe ledger (actual argv / env / exit / stdout sha256)

All probes run from `/tmp/r23-signal` (scratch outside the lane; nothing written to the repo).

| # | argv | env override | exit | stdout |
|---|------|--------------|------|--------|
| 1 | `npx -y rea-agents@6.5.0 decode-signal-recording --help` | none | 0 | 25 lines, sha256 `6134b1b24508f23c12aeea0664ab7b919b9b024116bbfb5c04927c591001133d` |
| 2 | `npx -y rea-agents@6.5.0 decode-signal-recording --schema` | none | 0 | 1357 bytes, sha256 `3631c903bcee3d9f0c10ff10d70221fda28e0756b9c7ebd67f912e6a6ad85f61` |
| 3 | `npx -y rea-agents@6.5.0 decode-signal-recording /nonexistent-kaidoku-r23.bin --decoders 'uart:rx=0:baudrate=9600' --input-format 'binary:numchannels=1:samplerate=1000000' --format json --full-output` | `REA_SIGROK_COMMAND` unset | 1 | `{"ok":false,"error":{"code":"UNKNOWN","message":"Unknown flag: --input-format"}}`, 186 B, sha256 `cedb66628ce52ef190361a6669440950bcb4fc7e731197463f78d505eed428f0` |
| 4 | same as #3 with `--input_format` (underscore) | `REA_SIGROK_COMMAND` unset | 1 | `ok:false`, `error.code=capability_unavailable`, `category=unsupported_provider`, `retryable:false`, provider `sigrok-recording`, operation `decode_signal_recording`, 836 B, sha256 `f472029183b4fb8126bd35b115d5c6b4f73fa922c77e43dc789c647d9b36aca3` |
| 5 | `npx -y rea-agents@6.5.0 --version` | none | 0 | `6.5.0` |

Tool identity observed: package `rea-agents@6.5.0`, npm `dist.shasum`
`7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`, `dist.integrity`
`sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`,
bin `rea -> scripts/rea.mjs`. Installed/cached at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (package.json version `6.5.0`).
A second cache `a1722018f28f9df2` holds `rea-agents 6.7.0`; every probe above pinned `@6.5.0`,
so 6.7.0 was not used.

No `REA_SIGROK_COMMAND` exists in this shell: `env | cut -d= -f1 | grep '^REA_'` returned
`REA_ADB_PATH REA_APKTOOL_COMMAND REA_BINWALK_COMMAND REA_JADX_MCP_JAR REA_PWNTOOLS_PYTHON
REA_UNBLOB_COMMAND REA_WAKARU_COMMAND` (7 names, none sigrok). No values were read.

Peer coordination: `agent://KaidokuR23.BuildSignalRunner` (id taken from the parent-authored
`.ufo/waves/round-23/w1/swarm-registry.json`, seat `BuildSignalRunner`) was sent the flag-name,
raw-format/samplerate and channel-mapping facts. The write reported delivery, but that agent's
wake turn failed with `turn_rate_limit_exceeded` (no answer produced), so no acknowledgement
was received; the facts remain in this report rather than relying on the message.

## Observed findings

### 1. Exact CLI surface — underscore option names, one required decoder string

`--help` (probe 1) verbatim option block:

```
Usage: rea decode-signal-recording <path> [options]

Arguments:
  path  Local signal recording

Options:
  --decoders <string>      sigrok decoder stack, options and channel assignments, e.g. uart:rx=RX:baudrate=9600
  --input_format <string>  Explicit sigrok input format and options; omitted means autodetection (default: null)
  --annotations <string>   Optional annotation selection, e.g. uart=rx-data (default: null)
  --line_offset <number>   Skip this many literal LF-separated output lines; default 0 (default: 0)
  --line_limit <number>    Returned output lines per page; default 50
  --all_lines              Return all remaining output lines instead of a bounded page
```

- The REA flags are `--input_format`, `--line_offset`, `--line_limit`, `--all_lines`
  (underscores). The sigrok-style hyphen spelling `--input-format` is **rejected** by the
  wrapper: probe 3 exits 1 with `error.code=UNKNOWN`, `message=Unknown flag: --input-format`.
  This is the wrapper only; REA internally emits hyphenated sigrok flags (finding 3).
- `--schema` (probe 2) confirms `args.required = [path]`, `options.required = [decoders]`,
  `additionalProperties: false`; `decoders`, `input_format`, `annotations` are each
  `string minLength 1 maxLength 8192` (nullable only for the latter two), and the three
  strings plus their flag prefixes share a 32768-byte budget
  (`.../dist/domain/signals/signalRecording.js:10-51`).
- `path` is resolved by the CLI (`.../dist/cli/signalCommands.js:68 resolve(args.path)`), then
  the shared service rejects non-absolute values
  (`.../dist/application/signals/SignalRecordingService.js:26-33`,
  `reason=invalid_format`, `message=Expected an absolute local path.`). CLI callers may pass a
  relative path; direct service/MCP callers must pass absolute.

### 2. Exact producer argv REA builds for sigrok-cli

`.../dist/signals/SigrokRecordingProvider.js:191-202` (verbatim array, in order):

```js
const args = [
  "--dont-scan",
  "--input-file=recording",
  `--protocol-decoders=${input.decoders}`,
  "--protocol-decoder-samplenum",
  ...(input.input_format === null ? [] : [`--input-format=${input.input_format}`]),
  ...(input.annotations === null ? [] : [`--protocol-decoder-annotations=${input.annotations}`]),
];
```

- The selected file is first copied into a private runtime dir as `recording`
  (`SigrokRecordingProvider.js:88`, `:184-189`, mode 0400, `flag:"wx"`), and sigrok runs with
  that dir as cwd, so `--input-file=recording` is always a relative name inside the workspace.
  The copy has **no extension**.
- REA never passes `--channels`, `--config`, `-d`, or any samplerate switch of its own.
  `samplerate` is not a REA parameter anywhere in schema or source; it can only ride inside
  `input_format` (or the container format).
- `--protocol-decoder-samplenum` is unconditional for recordings
  (`SigrokRecordingProvider.js:195`).
- Execution is wrapped by util-linux prlimit (`REA_SIGROK_PRLIMIT_COMMAND`, default
  `/usr/bin/prlimit`) with `--as=1GiB:1GiB --fsize=64MiB:64MiB --cpu=30:30 --core=0:0 --`
  (`.../dist/process/LinuxResourceLimits.js:10-26`); resident input ≤32 MiB, output ≤4 MiB,
  wall clock 30 s, concurrent decodes = 1 (`SigrokRecordingProvider.js:40-47`).
- Version gate before any decode: stdout of `--version` must match
  `/^sigrok-cli 0\.7\.2(?:\r?\n|$)/u` **and** contain the literal `libsigrokdecode`
  (`SigrokRecordingProvider.js:138-142`).

### 3. Raw input mapping — explicit `binary` format, numeric samplerate

sigrok-cli 0.7.2 input module options are colon-separated `key=value` after the module id
(`sigrok-cli-0.7.2/input.c:44-56`; parser `parsers.c:337-376` splits on `:` then `=`; no
escaping, no colons inside values). REA forwards the string unchanged.

The `binary` input module exposes exactly two options
(`libsigrok-0.5.2/src/input/binary.c:158-170`): `numchannels` (default 8) and `samplerate`
(default 0 Hz). Channels are auto-created and enabled, named by decimal index
`"0".."N-1"` (`binary.c:59-62`); sample byte width is `unitsize = ceil(numchannels/8)`
(`binary.c:64`; `struct sr_datafeed_logic { uint64_t length; uint16_t unitsize; ... }`
`libsigrok-0.5.2.h:493-497`).

Autodetection cannot select `binary`: the module sets `.exts = NULL` and leaves the
zero-initialised `metadata[8]` empty (`binary.c:178`; field contract
`src/libsigrok-internal.h:404-424`, "Can be all-zero, if the
module cannot identify streams at all, i.e. has to be forced into use"). `sr_input_scan_file`
skips modules with `!imod->metadata[0]` (`libsigrok-0.5.2/src/input/input.c:498-501`). REA's
extensionless `recording` copy removes even filename-extension hints. Therefore for a raw
recording `input_format` is mandatory, e.g.

```
binary:numchannels=1:samplerate=1000000
```

`samplerate` must be **decimal digits**. sigrok-cli converts input-module options by GVariant
type and for UINT64 uses `strtoul(s, NULL, 10)`
(`sigrok-cli-0.7.2/parsers.c:450-453`), so `samplerate=1mhz` parses as `1`, not 1 MHz
(despite the man-page example at `doc/sigrok-cli.1:141-145`). Use `1000000`.

Samplerate is not optional for UART decoding: the uart decoder raises
`SamplerateError('Cannot decode without samplerate.')` when the metadata is absent/zero
(`libsigrokdecode-0.5.3/decoders/uart/pd.py:501-503`), and `binary`'s default is 0
(`binary.c:33-34`).

### 4. Channel and decoder mapping — literal channel name, first decoder only

REA passes the whole `decoders` value as one `--protocol-decoders=` element
(`SigrokRecordingProvider.js:194`). sigrok-cli 0.7.2 then splits that value on commas into a
decoder stack, splits each token on colons into `decoder_id` + `option=value` pairs, and
extracts channel assignments for the **first decoder only** ("stacked decoders don't get
channels") (`sigrok-cli-0.7.2/decode.c:140-214`).

Channel assignment token form is `<decoder_channel_id>=<target_channel_name>`:

- `uart` declares optional channels `rx` (`RX`) and `tx` (`TX`)
  (`uart/pd.py:95-100`); the decoder needs at least one of them or raises
  `ChannelError('Need at least one of TX or RX pins.')` (`uart/pd.py:505-507`).
- The target is matched by **literal channel name**, `strcmp(ch->name, channelname)`
  (`sigrok-cli-0.7.2/parsers.c:28-42`, used at `decode.c:281-289`); a numeric string is not an
  index, it is a name. `binary` names its channels `"0"`, `"1"`, … (`binary.c:59-62`), so the
  raw-channel mapping is `uart:rx=0`. The schema example `uart:rx=RX` only resolves when the
  input format itself yields a channel literally named `RX` (e.g. VCD/srzip); it does **not**
  resolve for the `binary` module.
- Stacked decoders are comma-separated (e.g. `uart:rx=0:baudrate=9600,<upper>`); options are
  colon-separated, so no `:`/`,` may appear inside a value.

Exact raw UART8N1 decoder string for channel 0 at 9600 baud:

```
uart:rx=0:baudrate=9600
```

Defaults that make this 8N1 without extra options: `data_bits=8`, `parity=none`,
`stop_bits=1.0`, `bit_order=lsb-first`, `format=hex`, `invert_rx=no`
(`uart/pd.py:101-123`). `format=ascii` is an available option value (`pd.py:108`) if printable
payload text is wanted in the annotation instead of hex; that switch is inference from the
option enum (no successful decode was executed here).

### 5. Annotation mapping

`--annotations` becomes `--protocol-decoder-annotations=<string>`
(`SigrokRecordingProvider.js:199-201`). sigrok-cli splits that on commas, then each entry on
`=` into exactly two fields: `decoder_id` and a `:`-separated list of annotation class ids or
annotation-row ids (`sigrok-cli-0.7.2/decode.c:314-395`). Class lookup runs before row lookup,
and an unknown id aborts the run with `Annotation '<id>' not found for protocol decoder '<id>'`
(`decode.c:386-397`). An entry with no `=` shows all classes (`decode.c:398-400`).

For the UART decoder, `rx-data` is both an annotation class (index 0, `'RX data'`) and a row
id that also contains start/parity/stop classes (`uart/pd.py:124-152`). Because class lookup
is attempted first, `uart=rx-data` selects **class 0 only** — the decoded RX data bytes — not
the row. That is the mapping the REA help example implies.

### 6. Output and evidence boundary (decode success vs refusal)

- `annotations_text` is the producer's raw stdout paginated by literal LF lines; the window
  logic never reinterprets annotations (`.../dist/domain/signals/annotationTextWindow.js:1-30`;
  page fields `signalRecording.js:64-75`). Default page is 50 lines; `--all_lines` maps to
  `line_limit:null` (`signalCommands.js:50-53,64-68`); `--all_lines` and `--line_limit` are
  mutually exclusive.
- The report is a strict object containing `artifact {path, sha256, bytes}`,
  `selection` (echo of all inputs including defaults), `annotations_text`,
  `output_window {total_lines, returned_lines, has_more}`, `diagnostics`, `tool {configured_path,
  path, sha256, version_banner, version_diagnostics, arguments}`, `resource_limiter`, `limits`,
  and literal `hardware_acquisition: "not-performed"` (`signalRecording.js:56-115`).
  `tool.arguments` is the exact post-prlimit argv REA executed (finding 2), so the producer
  invocation is self-evidencing.
- Success requires exit 0 **and** a schema-valid report whose `artifact.path`/subject sha256
  match the selected file and whose `selection` deep-equals the parsed input
  (`SignalRecordingService.js:34-44`). A successful run with empty `annotations_text` is still
  a decode result; the provider's own limitation text says empty output does not establish
  absence of traffic (`SigrokRecordingProvider.js:229-231`).
- Refusal (not coverage): missing/non-absolute `REA_SIGROK_COMMAND` yields probe 4's
  `capability_unavailable` envelope before the file is even read; a non-zero producer exit is
  converted to `ProviderAdapterError` with `exit_code/stdout/stderr` diagnostics
  (`SigrokRecordingProvider.js:128-135`); non-Linux fails the same capability path
  (`:69-70`). All are `ok:false` + exit 1 from the CLI, i.e. typed refusals.
- Version/identity can be read back from `data.tool.version_banner` (`--version` prints
  `sigrok-cli <ver>` plus a "Libraries and features" block, `sigrok-cli-0.7.2/show.c:63-76`),
  which is the only way to observe the actually bundled libsigrok/libsigrokdecode versions.

## Inferred end-to-end recipe for BuildSignalRunner (UNVERIFIED — not executed)

Given the assigned generator (1 channel, 1 MHz, 9600 8N1, ASCII `Hi`):

```sh
REA_SIGROK_COMMAND=/abs/sandbox/sigrok-cli \
npx -y rea-agents@6.5.0 decode-signal-recording /abs/output/uart.bin \
  --input_format 'binary:numchannels=1:samplerate=1000000' \
  --decoders 'uart:rx=0:baudrate=9600' \
  --annotations 'uart=rx-data' \
  --all_lines --format json --full-output
```

Expected `data.tool.arguments` (order fixed by source):

```
["--dont-scan","--input-file=recording",
 "--protocol-decoders=uart:rx=0:baudrate=9600",
 "--protocol-decoder-samplenum",
 "--input-format=binary:numchannels=1:samplerate=1000000",
 "--protocol-decoder-annotations=uart=rx-data"]
```

Raw byte layout implied by source: with `numchannels=1`, `unitsize=1`, so **one file byte is
one sample** (bit 0 carries channel 0's level; bits 1-7 of each byte are ignored by the logic
feed). A 9600-baud 8N1 character spans 10 bit times at 1 MHz ≈ 1042 samples ≈ 1042 file
bytes, not one byte per character. This arithmetic is inference from `binary.c:64` and the
`length`/`unitsize` fields, not from an executed decode.

## Unknowns / not observed

- No successful decode was executed: `REA_SIGROK_COMMAND` is unset in this shell and the
  AppImage launcher is a separate seat's work. End-to-end `annotations_text` content,
  sample-number formatting with `--protocol-decoder-samplenum`, and exit-0 behavior remain
  unverified by this seat.
- The AppImage's bundled libsigrok version was not observed. I analyzed the `binary` module at
  tag `libsigrok-0.5.2` (source sha256 `fa037abe…`), which matches master on option ids and
  channel naming (`snprintf("%d")`), but the runtime version must be read from
  `version_banner`.
- `strtoul` behavior for `samplerate=1mhz` is source-derived; not executed against the binary.
- UART decode tolerance for the runner's quantisation (1,000,000/9,600 = 104.1667 samples per
  bit) was not tested; the decoder uses the float ratio (`uart/pd.py:218-223`) so exact
  104/105-sample spacing is a runner design question, not a REA contract question.
- This seat does not establish any R23-C1 count; a refusal (probe 3/4) is explicitly excluded
  from coverage, and the decode verb remains uncounted until an executor produces an
  `ok:true` envelope bound to a hashed recording.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SchemaSignalDecode.md`
  (this report), sha256 recorded in the seat's final message after write; no other lane files
  written.
- Probe scratch (outside lane, not deliverables): `/tmp/r23-signal/{help.txt,schema.txt,refusal.json,refusal2.json}`
  with sha256 `6134b1b2…`, `3631c903…`, `cedb6662…`, `f4720291…`.

## Installs

None. No pacman/uv/npx install beyond the ordinary `npx -y rea-agents@6.5.0` cache fetch
already present on host; no global install, no config edit, no pacman transaction.

## Open risks

- Flag spelling is a live trap: `--input-format` is rejected (`UNKNOWN`), so any runner that
  copies sigrok's spelling will fail before reading the file.
- `samplerate=1mhz` silently becomes 1 Hz (strtoul base 10), producing a UART failure that
  looks like carrier corruption.
- `uart:rx=RX` from the help example cannot resolve against `binary` channels (`0`, `1`, …);
  it needs an input format that names channels `RX`.
- Autodetection is unusable for raw data here: the private copy is extensionless and `binary`
  declares no matching metadata; omitting `input_format` yields a producer failure, not
  evidence.
- `--protocol-decoder-samplenum` is always on, so output text is sample-range prefixed; any
  expectation of bare `Hi` text needs `format=ascii` plus tolerant parsing.
- Empty output on a successful decode is not absence of traffic; count only `ok:true`
  envelopes with recorded `artifact.sha256`, and never count probes 3/4.
