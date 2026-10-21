# SignalRawFormat — official sigrok binary/raw input: channel count, samplerate, bit order, accepted parameters

Seat: `KaidokuR23.SignalRawFormat` (leaf scout, round-23 w1). Author-side report; not outside verification or admission. Opened 2026-10-21. Lane bounds kept: no REA invocation, no device, no debugger/Frida, no target execution, no installs, no lane writes other than this report.

## Verdict (bounded)

- The official sigrok wiki page for the binary input format is reachable and states exactly two parameters and their compiled defaults: `numchannels` (default 8), `samplerate` (default 0 Hz). It does **not** state sample packing, unit size, channel naming, bit order, autodetection behavior, or partial-sample handling.
- Packing and bit order are established by the version-bound libsigrok input/output implementation: a sample is `ceil(numchannels/8)` bytes; logic channel `i` is bit `i % 8` of byte `i / 8` of that sample (channel 0 = LSB of the first byte; higher channels continue into later bytes, low bit first). This is the shape both the ASCII and VCD output writers consume.
- sigrok-cli 0.7.2 parses `-I` format options as colon-separated `key=value` with `strtoul(s, NULL, 10)` for `numchannels`/`samplerate`: **plain decimal only**. The man page's own example `-I binary:numchannels=4:samplerate=1mhz` therefore yields samplerate **1 Hz**, not 1 MHz, on this code path. Suffix forms (`1m`, `24m`) are documented for device `--config samplerate=`, a different parser, not for `-I`.
- Raw binary has no extension list and all-zero identification metadata, so it is skipped by `sr_input_scan_file`/`sr_input_scan_buffer`; `-I binary` (or REA's `--input_format=binary:...`) must be supplied explicitly.
- **No T1 credit.** No sigrok-cli was installed or run and no REA operation produced a non-refused bound record. This report supplies source linkage only; R23-C1 k is unchanged by it.

## Findings

### 1. Official wiki page — exactly what it says

- URL: `https://sigrok.org/wiki/File_format:Binary` (HTTP 200, 13,661-byte HTML; raw wikitext 335 bytes, sha256 `2d81a085ad13ac0bf859629728549130fc7d8fa401c7950d5a8281757be222c4`).
- Revision `13665` (`wgRevisionId` = `wgCurRevisionId`); latest **and only** edit 2018-09-17 02:56 by `Crackwitz`; 1 edit, 1 author (action=info).
- Full informative content, verbatim (`sigrok.org/w/index.php?title=File_format:Binary&action=raw`):

```
$ sigrok-cli -I binary --show
ID: binary
Name: Binary
Description: Raw binary logic data
Options:
  numchannels: The number of (logic) channels in the data (default 8)
  samplerate: The sample rate of the (logic) data in Hz (default 0)
```

  followed by the example `sigrok-cli -I binary:numchannels=8:samplerate=1000000 -i SOMEFILE ...`.
- The companion page `https://sigrok.org/wiki/Input_output_formats` (revision `16565`, last edited 2023-07-12 19:27, 59 edits) lists `Binary` as **input: supported** and **output: supported**, described as "Raw binary data output without any metadata attached" (raw wikitext line 22–25). "No metadata" is the page's phrase for the format, not a statement about `samplerate` option propagation.
- The wiki page says nothing about bit order, unit size, channel names, channel-index mapping, autodetection, or trailing bytes. Any such statement attributed to this page would be unsourced. (Matches `KaidokuR23.CriticSource`'s scope note in IRC.)

### 2. Channel count and packing — version-bound source

Source: libsigrok tag `libsigrok-0.5.2`, annotated tag object `48ceaf1b0920ca09189cdca32b05488c00536d83` → commit `a6b07d7e28fe445afccf36922ef7d20e63e54fe6` (tagger 2019-12-25T20:28:46Z). File `src/input/binary.c` sha256 `fa037abe4beaf00ff35470f4a78989c2237663edad79b9fd53af6375e72dd9d1`, 184 lines (scratch `/tmp/binary_old.c`).

| Point | Location | Observation |
|---|---|---|
| compiled defaults | `:33-34` | `DEFAULT_NUM_CHANNELS 8`, `DEFAULT_SAMPLERATE 0` |
| option types | `:167-168` | defaults registered as `int32` (numchannels) and `uint64` (samplerate) |
| minimum | `:47-51` | `num_channels < 1` → `sr_err("Invalid value for numchannels: must be at least 1.")`, returns `SR_ERR_ARG` |
| channel names | `:59-61` | channels created with index `i`, type `SR_CHANNEL_LOGIC`, enabled `TRUE`, name `"%d"` → `0 … N-1` |
| sample unit | `:64` | `unitsize = (channel_count + 7) / 8` bytes |
| samplerate metadata | `:83-87` | only sent when `inc->samplerate` is non-zero (`SR_CONF_SAMPLERATE` via `SR_DF_META`) |
| stream chunking | `:101-106` | input truncated to a whole multiple of `unitsize` per buffer; `logic.length = chunk` |
| tail handling | `:131-145` (`end` → `process_buffer`, then free) | remaining bytes fewer than one unit are never processed and disappear silently |
| identification | `:174-184` | `.exts = NULL`; no `.metadata` initializer → all-zero metadata |
| high bits | `:64`, `:94-110` | not masked or validated; bits at positions ≥ `numchannels` simply never map to a channel |

For the current upstream (master, fetched 2026-10-21; NOT version-bound to REA) `src/input/binary.c` sha256 `10f3d73eee53a9681f7b64bc3ada64f543b95c001b9169643d4ef7879b2db934`, 179 lines: same defaults/minimum/unitsize at `:33-34`, `:49`, `:64`, `.exts = NULL` at `:173`; difference at `:95-101` — the chunk length is rounded down to a multiple of `unitsize` before sending (`chunk /= unitsize; chunk *= unitsize`). In 0.5.2 it is not (`:105-106`), so for a `unitsize` that does not divide the 4 MiB internal chunk size (e.g. 3 bytes for 17–24 channels) a `SR_DF_LOGIC` packet can end mid-sample. `[INFERENCE from source diff; not executed]`

### 3. Bit ordering — the mapping the writers consume

The official page does not define it; the libsigrok output modules do, identically across 0.5.2 and master:

- `libsigrok-0.5.2 src/output/vcd.c:240-243`: `curbit = ((unsigned)sample[index / 8] >> (index % 8)) & 1;` where `sample = logic->data + i` and `i` advances by `logic->unitsize` (`:224-225`, `:267`).
- `libsigrok-0.5.2 src/output/ascii.c:185-187`: `p = logic->data + i + idx / 8; curbit = *p & (1 << (idx % 8));`.
- master `src/output/vcd.c:1067-1068` and `src/output/ascii.c:225-226` use the same `index / 8` + `1 << (index % 8)` split.

Therefore, for `numchannels = N` and a raw file:

```
sample s (0-based)     : bytes [s*U, s*U + U),  U = ceil(N/8)
channel c (0 <= c < N) : bit (c % 8) of byte (s*U + c/8)   [LSB = bit 0]
1..8 channels   -> U=1: ch0=bit0 ... ch7=bit7 of each byte
9..16 channels  -> U=2: ch8=bit0 of the 2nd byte, ch15=bit7 of the 2nd byte
```

So the packing is little-endian by channel group: lower channel indices occupy earlier bytes and lower bits. File byte order is the sample byte order as stored; there is no endianness/wordsize option for this module.

Caveat observed in `vcd.c:228-238` (0.5.2): the writer carries a TODO that the data image is assumed dense over *enabled* channels. For the binary input module all N channels are created enabled, so index == channel number and the mapping above holds. `[INFERENCE: dense-packing caveat matters for hardware drivers, not for this input module]`

### 4. Accepted format parameters and value conversion — sigrok-cli 0.7.2

Source: sigrok-cli tag `sigrok-cli-0.7.2`, annotated tag object `2f342b4d7bf211207af718d4d0c27f6c6d84ea79` → commit `b584f959edb788f1731d5a304badf241ac21bf65` (tagger 2021-03-01T22:38:51Z). `configure.ac:92` requires `libsigrok >= 0.5.0`; Arch `extra` currently ships `libsigrok 0.5.2-26` (`pacman -Si libsigrok`, read-only, exit 0), so the 0.5.2 module above is the plausible linked implementation for a 0.7.2 CLI. `[INFERENCE: not observed in a running sigrok-cli]`

| Point | Location (file sha256) | Observation |
|---|---|---|
| `-I` entry | `options.c:117` (`a063e09d9511ffcd0aa061088ebbd700a59cacf9d7d17d4dffd7f756cdc3bf3b`) | `--input-format/-I` stored verbatim; only one occurrence allowed (`CHECK_ONCE`) |
| argument parse | `input.c:54` (`894aa07fc2ce29e9fed159c459060915aa83c8e1528621a4b67910782691dc5d`) | `parse_generic_arg(opt_input_format, TRUE, NULL)`; first colon token is the format id (`sigrok_key`) |
| grammar | `parsers.c:337-376` (`0d2cffb62f3e1162126f3e17955b09832c60c37c98210844b8b33493c9a19b7e`) | split on `:`; each item split at the **first** `=` (`:282-306`); `key` with no `=` yields NULL value |
| conversion | `parsers.c:429-479` | `int32`/`uint32`/`uint64` options all via `strtoul(s, NULL, 10)` (`:443,:447,:451`); no `endptr` check, no suffix handling |
| unknown keys | `input.c:67-68` | `warn_unknown_keys(...)` only warns ("Unknown keyword: X."); the run continues |
| missing value | `parsers.c:440-441` | a key without `=` is skipped entirely, so the compiled default applies |
| runtime types | `binary.c:47,57` | `numchannels` read as int32, `samplerate` as uint64 |
| man page | `doc/sigrok-cli.1:129-145` (sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9`) | `-I <format>[:key=value]...`; example `-I binary:numchannels=4:samplerate=1mhz` |

Consequences (source-derived, one libc probe):

- Accepted parameters for this module are exactly `numchannels` and `samplerate`; no `format`, `wordsize`, `endianness`, `unitsize`, or `channel` option exists.
- `numchannels` and `samplerate` must be plain decimal integers for this path. `strtoul("1mhz", NULL, 10) == 1`, `strtoul("24m", NULL, 10) == 24`, `strtoul("4x", NULL, 10) == 4`, `strtoul("", NULL, 10) == 0`, `strtoul("-1", NULL, 10) == 18446744073709551615` (host glibc 2.44, ctypes call; standard semantics per `man 3 strtoul`). So the man page's `samplerate=1mhz` example silently decodes as **1 Hz**. `[OBSERVED for strtoul; INFERENCE for sigrok-cli because generic_arg_to_opt calls it]`
- The suffix behaviour (`1m`, `24m`, `"1 MHz"`) documented at `doc/sigrok-cli.1:86-99` belongs to device `--config samplerate=...`, a separate parser/option namespace, not to `-I` format options.
- Because `g_hash_table_insert` is used while walking the colon list, a duplicated key keeps the last value. `[INFERENCE from GLib API semantics; not executed]`
- `numchannels=0` (or any value that converts below 1) is rejected by the module with the "must be at least 1" error; there is no documented upper bound, and `unitsize` is `uint16_t`, so counts above 524,280 would overflow the unit size. `[INFERENCE from `:64` arithmetic]`

### 5. Samplerate semantics

`samplerate` is `uint64` Hz with default 0 (`binary.c:34,57,167-168`). Zero is not a valid rate: `process_buffer` sends `SR_DF_META`/`SR_CONF_SAMPLERATE` only when non-zero (`:83-87`). Decoders that need timing (e.g. UART baud reconstruction, protocol timing annotations) therefore receive no samplerate unless the caller supplies one. This matters for REA: a successful exit with empty annotations can follow from a missing samplerate, not only from a wrong channel count.

### 6. File identification — binary is never autodetected

`sr_input_scan_file` and `sr_input_scan_buffer` skip every module whose `metadata[0]` is zero ("Module has no metadata for matching so will take any input. No point in letting it try to match") — `libsigrok-0.5.2 src/input/input.c:498-502` and `:376-382`; `struct sr_input_module` metadata docs at `src/libsigrok-internal.h:411-421` say all-zero means "has to be forced into use". `input_binary` sets `.exts = NULL` and no metadata (`binary.c:174-184`). So sigrok-cli without `-I` falls to `sr_input_scan_file`; if no other module claims the bytes, it errors "Error: no input module found for this file." (`input.c:113`). Explicit format selection is required for raw binary, and is what REA does.

### 7. Relation to REA 6.5.0 / this round (not a run)

- REA's `decode-signal-recording` provider passes `--input-format=<fmt>` verbatim (prior retained source observation, R22 `SchemaDecodeSignalRecording.md`; not re-read this seat). With this documentation, the REA caller's `<fmt>` must be `binary:numchannels=<N>:samplerate=<Hz>` for raw captures; REA does not add either key.
- Defaults `8`/`0` apply when a key is omitted or malformed: an 8-channel default misreads any file packed with `N != 8`, and samplerate 0 removes timing metadata. Unknown keys only warn, so `numchannel=4` (typo) leaves 8.
- REA's input cap is 32 MiB; the 0.5.2 chunk-length difference (section 2) can split a sample between `SR_DF_LOGIC` packets only for non-power-of-two `unitsize` and inputs crossing a 4 MiB internal chunk boundary. Master fixes it. Whether the packaged 0.5.2-26 binary is affected is unverified (distro patches not inspected).
- Bit order for REA decoders: channel 0 = bit 0 of the first byte of each sample; `N>8` continues at bit 0 of the second byte. This is the mapping a decoder stack must assume for a correctly specified raw file.

### 8. Version binding summary

| Object | Identity | Date |
|---|---|---|
| wiki `File_format:Binary` | revision 13665 (only edit) | 2018-09-17 02:56 |
| wiki `Input_output_formats` | revision 16565 | 2023-07-12 19:27 |
| libsigrok tag `libsigrok-0.5.2` | tag obj `48ceaf1b…`, commit `a6b07d7e28fe445afccf36922ef7d20e63e54fe6` | tagger 2019-12-25T20:28:46Z |
| sigrok-cli tag `sigrok-cli-0.7.2` | tag obj `2f342b4d…`, commit `b584f959edb788f1731d5a304badf241ac21bf65` | tagger 2021-03-01T22:38:51Z |
| REA pin | `sigrok-cli@0.7.2` (provider constant, prior retained reading) | — |
| host repo candidate | Arch `extra` `sigrok-cli 0.7.2-3`, `libsigrok 0.5.2-26` (read-only `pacman -Si`) | package DB as of 2026-10-21 |

`[INFERENCE]` The 0.7.2 CLI against the 0.5.2 module is the configuration REA would exercise if a binary were supplied; nothing was installed or run here, and host pacman transactions are paused.

## Drafted source rows (L1 assigns ids; current registry max observed is S057, and no sigrok row exists in `corpus/SOURCES.md`)

`S0xx` — docs — A — scope: exactly the two parameters and defaults on the official binary-format page, plus the page's own example; **not** packing, bit order, channel naming, autodetection, or partial-sample handling (those are S0yy/source).

```
| S0xx | sigrok wiki, File format:Binary — https://sigrok.org/wiki/File_format:Binary | docs | A | The official page's complete binary input option listing and its 8-channel/1 MHz example; it defines no packing or bit order | Revision 13665, only edit 2018-09-17 02:56 by Crackwitz; raw wikitext sha256 2d81a085ad13ac0bf859629728549130fc7d8fa401c7950d5a8281757be222c4; sections `Options` and `Example` | `numchannels` (default 8) and `samplerate` Hz (default 0) are the only binary input options; the page is not evidence for unit size or bit order. | mined | 2026-10-21 | 365d | .ufo/waves/round-23/w1/SignalRawFormat.md |
```

`S0yy` — code — A — scope: version-bound libsigrok 0.5.2 binary input module and sigrok-cli 0.7.2 `-I` argument conversion; REA's own pin is sigrok-cli 0.7.2, satisfying "same producer or explicit supersession" only for the CLI layer; the libsigrok 0.5.2 link is inferred from `>= 0.5.0` + Arch packaging.

```
| S0yy | libsigrok 0.5.2 `src/input/binary.c` + `src/output/{vcd,ascii}.c`, sigrok-cli 0.7.2 `parsers.c`/`input.c`/`doc/sigrok-cli.1` — https://github.com/sigrokproject/libsigrok/tree/libsigrok-0.5.2 , https://github.com/sigrokproject/sigrok-cli/tree/sigrok-cli-0.7.2 | code | A | How raw binary samples are sized and mapped to channel bits, and how `-I` key=value options are converted before the module sees them | commits `a6b07d7e28fe445afccf36922ef7d20e63e54fe6` (2019-12-25) and `b584f959edb788f1731d5a304badf241ac21bf65` (2021-03-01); `binary.c` sha256 fa037abe…7e72dd9d1 `:33-34,47-51,59-64,83-87,101-106,174-184`; `vcd.c:240-243`; `ascii.c:185-187`; `parsers.c:282-306,337-376,429-479`; `input.c:54,67-68`; man `:129-145` | Unit size is ceil(N/8) bytes; channel i is bit i%8 of byte i/8; samplerate 0 sends no metadata; `-I` values are decimal `strtoul` only (suffix truncates, e.g. `1mhz`→1), unknown keys only warn, binary is never autodetected. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/SignalRawFormat.md |
```

Both rows are scoped so neither can be cited as proof of an executed decode. If L1 folds them into `corpus/knowledge/2026-10-21-r23-signal-raw-format.md`, that path must replace/add to `used-by`.

## Commands, exits, observations (all 2026-10-21, cwd `/tmp` or `/tmp/sigrok-doc`)

| argv | exit | observation |
|---|---|---|
| `curl -sS -L -o bin-wiki.html -w '%{http_code} %{url_effective} %{size_download}\n' https://sigrok.org/wiki/File_format:Binary` | 0 | `200 https://sigrok.org/wiki/File_format:Binary 13661`; html sha256 `b4ceb8226bab54fb923a3d0bec9e1b415814a108caab13402b2b9959a6101846` |
| `curl … 'https://sigrok.org/w/index.php?title=File_format:Binary&action=raw'` | 0 | `200 335`; sha256 `2d81a085…be222c4`; 11 lines |
| `curl … '…&action=info'` | 0 | `200 16075`; revision 13665; latest/only edit 02:56, 17 Sep 2018; 1 edit, 1 author (Crackwitz) |
| `curl … https://sigrok.org/wiki/Input_output_formats` and `…&action=raw` | 0 | `200 24292` / `200 6342`; revision 16565, last edited 2023-07-12 19:27, 59 edits; raw lines 22-25 Binary input+output |
| `curl … https://manpages.debian.org/testing/sigrok-cli/sigrok-cli.1.en.html` | 0 | `200 43562`; contains the same `binary:numchannels=4:samplerate=1mhz` example (mirror copy; page names only "sigrok-cli 0.7", no minor version — not relied on) |
| `curl … raw.githubusercontent.com/sigrokproject/libsigrok/libsigrok-0.5.2/src/input/binary.c` | 0 | 200, 4,394 bytes, sha256 `fa037abe…7e72dd9d1`, 184 lines |
| `curl … libsigrok-0.5.2/src/output/vcd.c` / `ascii.c` / `src/input/input.c` / `src/libsigrok-internal.h` | 0 | sha256 `11282775…71c423` / `79947085…23e8d` / `27fa63e4…619b2b` / `59af065b…077c1ca8`; input.c 1,607 lines, internal.h 66,252 bytes |
| `curl … libsigrok/master/src/input/binary.c` and master vcd/ascii | 0 | 200, 179 lines, sha256 `10f3d73e…b2db934`; master vcd `:1067-1068`, ascii `:225-226` same mapping |
| `curl … sigrok-cli/sigrok-cli-0.7.2/{parsers.c,input.c,options.c,doc/sigrok-cli.1,configure.ac}` | 0 | sha256 `0d2cffb6…19b7e` / `894aa07f…91dc5d` / `a063e09d…c3bf3b` / `e3f06dfe…64a5f9`; configure requires `libsigrok >= 0.5.0` |
| `curl https://api.github.com/repos/sigrokproject/{libsigrok,sigrok-cli}/git/ref/tags/…` and `/git/tags/<obj>` | 0 | libsigrok tag obj `48ceaf1b…` → commit `a6b07d7e…` (2019-12-25T20:28:46Z); sigrok-cli tag obj `2f342b4d…` → commit `b584f959…` (2021-03-01T22:38:51Z) |
| `pacman -Si sigrok-cli` / `pacman -Si libsigrok` | 0 / 0 | `0.7.2-3` / `0.5.2-26`, repository `extra`; read-only query, no transaction |
| `MANWIDTH=100 man 3 strtoul \| col -b` | 0 | "stopping at the first character which is not a valid digit in the given base"; optional sign; no endptr here |
| ctypes `strtoul(s, NULL, 10)` on host glibc 2.44 | 0 | `1mhz`→1, `1m`→1, `24m`→24, `4x`→4, `""`→0, `-1`→18446744073709551615 |
| `sigrok-cli --version` | not run | binary absent from host (prior R22 observation; not rechecked here); no install attempted |

## Produced files

| path | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SignalRawFormat.md` | digest is reported in the seat's final message; embedding it here would change the digest |

Scratch fetches under `/tmp/sigrok-doc/` and `/tmp/*.c|h` are ephemeral citation anchors, not lane outputs; their digests are listed above and in this file. No other lane file was created or edited.

## Installs

None. No pacman transaction, no uv/npx install, no config edit. The only executable probes were `curl`, `pacman -Si` (read-only), `man`, and a Python `ctypes` libc call.

## Open risks / unresolved gaps

- No sigrok-cli execution: the parser conclusion (`1mhz`→1 Hz) is source + libc `strtoul`, not an observed sigrok-cli run. A packaged 0.7.2-3 banner and `-I binary --show` output were not observed.
- The libsigrok 0.5.2 ↔ sigrok-cli 0.7.2 link is inferred from `configure.ac` `>= 0.5.0` and Arch's pairing (`libsigrok 0.5.2-26`); distro patches to either package were not inspected.
- Bit order is proven by two output writers consuming `SR_DF_LOGIC`, not by an end-to-end decode; a protocol decoder could in principle re-map channels, though the sdi channel index convention is shared.
- The 0.5.2 chunk-boundary difference is a source-level diff; whether it produces a visible decode artifact for 17–24-channel raw files was not exercised.
- `numchannels` upper bound and `unitsize` overflow are arithmetic inferences; no validation in source was observed beyond `< 1`.
- Wiki pages are mutable; revision ids/hashes above are the durable anchors. The 2018 page predates the 0.7.2 CLI, so the page's option text is stable but not a versioned API contract.
- REA's exact `--input-format=` assembly was not re-opened this seat; it is taken from the prior retained R22 provider reading and should be re-confirmed by whoever executes a probe.
- No T1 verb was held: this report is documentation/source linkage only, and must not be counted as `inspect-signal-decoders`, `decode-signal-recording`, or any other verb evidence.
