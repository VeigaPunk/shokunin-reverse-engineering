# UartSemantics — official sigrok UART decoder source: 8N1 RX/baud options and exact annotation classes

Seat: `KaidokuR23.UartSemantics` (scout, leaf). Round-23 w1, claim R23-C1 coverage support.
Author-side source reading only: **no sigrok-cli, decoder, REA verb, debugger, Frida, device or
network target was executed**. This is not an outside admission and produces **zero T1 witnesses**;
it cannot change the 1/6 count by itself.

Pinned subject: **libsigrokdecode 0.5.3**, official release tarball, UART decoder
`decoders/uart/pd.py` (561 lines, sha256 `51a29d0e…e97da62`), byte-identical to git tag
`libsigrokdecode-0.5.3` (peeled commit `97991a3919da6a07c4c87308ae66fb441bd512e3`).

---

## 1. Pin and provenance (observation)

| item | observed value | how |
|---|---|---|
| Release page listing | `libsigrokdecode-0.5.3.tar.gz  2019-12-11 22:50  872K`; listing shows **no** `.sha256`/`.sig` sidecar and no later release | `curl -fsSL https://sigrok.org/download/source/libsigrokdecode/` exit 0 |
| Tarball | 892783 bytes, sha256 `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0` | `curl -fsSL -o … https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz` exit 0; `sha256sum` |
| Git tag | `refs/tags/libsigrokdecode-0.5.3` = tag object `1577c4354b4caba6fcb62d5919a1d4a196ae4512`, peeled commit `97991a3919da6a07c4c87308ae66fb441bd512e3` | `git ls-remote --tags https://github.com/sigrokproject/libsigrokdecode` exit 0 |
| Decoder file at tag | `https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/libsigrokdecode-0.5.3/decoders/uart/pd.py` sha256 `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` | `curl` exit 0; `cmp` against tarball copy → `IDENTICAL` |
| `decoders/uart/__init__.py` | sha256 `351098a23f5caa205068688550af53bd44a63776e1d02921ba32487ce720b92f`, 47 lines (docstring only, then `from .pd import Decoder`) | `sha256sum`, read |
| Host package context (not installed) | sync DB: `libsigrokdecode 0.5.3-10`, `sigrok-cli 0.7.2-3` (`Depends On: … libsigrokdecode`) | `pacman -Si libsigrokdecode sigrok-cli` exit 0 (read-only query; no transaction) |

**Boundary:** the release tarball and the git tag agree byte-for-byte on `pd.py`, so the decoder
semantics below are pinned twice. Whether Arch's `0.5.3-10` pkgrel patches this file is
**unknown** (not downloaded); the release source, not a distro package, is the authority here.

---

## 2. Decoder identity and the 8N1 configuration (observation, `pd.py` line cites)

`Decoder` class header, `pd.py:85-123`:

- `api_version = 3`; `id = 'uart'`; `name = 'UART'`; `longname = 'Universal Asynchronous Receiver/Transmitter'`; `desc = 'Asynchronous, serial bus.'`; `license = 'gplv2+'`; `inputs = ['logic']`; `outputs = ['uart']`; `tags = ['Embedded/industrial']`.
- Channels are **all optional** (`optional_channels`, `:95-101`), in declaration order:
  - index 0 `{'id': 'rx', 'name': 'RX', 'desc': 'UART receive line'}` (`:98`)
  - index 1 `{'id': 'tx', 'name': 'TX', 'desc': 'UART transmit line'}` (`:100`)
- There are **no required channels**. The decoder itself enforces "at least one direction":
  `pd.py:505-507` — `has_pin = [self.has_channel(ch) for ch in (RX, TX)]`; `if not True in has_pin:
  raise ChannelError('Need at least one of TX or RX pins.')`. Samplerate is likewise mandatory:
  `:502-503` `raise SamplerateError('Cannot decode without samplerate.')`.
- Default channel mapping is positional: libsigrokdecode `instance.c:376-378` states the default map
  comes "in the order in which the decoder class defined them", so the first trace of a one-channel
  recording maps to `rx` absent an explicit `rx=<n>` assignment.

Options (`pd.py:102-122`), with the release defaults:

| id | desc | default | values |
|---|---|---|---|
| `baudrate` | Baud rate | **115200** | (none declared — free integer) |
| `data_bits` | Data bits | **8** | 5, 6, 7, 8, 9 |
| `parity` | Parity | **`none`** | none, odd, even, zero, one, ignore |
| `stop_bits` | Stop bits | **1.0** | 0.0, 0.5, 1.0, 1.5 |
| `bit_order` | Bit order | **`lsb-first`** | lsb-first, msb-first |
| `format` | Data format | **`hex`** | ascii, dec, hex, oct, bin |
| `invert_rx` / `invert_tx` | Invert RX / TX | **`no`** | yes, no |
| `rx_packet_delim` / `tx_packet_delim` | Packet delimiter (decimal) | **-1** | free integer |
| `rx_packet_len` / `tx_packet_len` | Packet length | **-1** | free integer |

**8N1 is the default combination** — 8 data bits, no parity, 1.0 stop bit, LSB-first, 115200 baud,
hex rendering. The literal strings `8N1` / `8-N-1` **do not occur** in `pd.py` (`grep` exit 1), so
"8N1" is the conventional name for these defaults, not a declared mode. No presets exist.

Timing path (all observation):

- `metadata()` `:219-223`: on `SRD_CONF_SAMPLERATE`, `self.bit_width = float(samplerate) / float(self.options['baudrate'])`. `baudrate` is used **nowhere else**; it has no range/enum validation, so `baudrate=0` divides by zero (inference from `:223`).
- `get_sample_point()` `:225-235`: sample point = `frame_start + (bit_width - 1)/2 + bitnum*bit_width` — the middle sample of each bit slot.
- Frame start is the falling edge (`wait_for_start_bit()` `:236-241`); the start bit is then validated at its midpoint (`get_start_bit()` `:243-265`), which must be 0 or the frame is marked invalid (`:248-259`) with a frame-error annotation and an `INVALID STARTBIT` python packet.
- Bit numbering for `wait`: start=0, data=1…N, parity=N+1 (if enabled), first stop=N+1 without parity (`get_wait_cond()` `:419-436`). For 8N1 the single stop bit is sampled at **bit 9**.
- Frame length `decode()` `:515-521`: `frame_samples = 1 + data_bits + (parity != none) + stop_bits`, times `bit_width`, `ceil`ed. For 8N1 that is `ceil(10 * bit_width)`; the same value is the break threshold (`break_min_sample_count`, `:521`) and the idle-detector threshold (`:495`).
- `stop_bits` only changes that span arithmetic. The released decoder samples and validates **exactly one** stop bit: `get_stop_bits()` `:392-410`, preceded by the explicit comment `# TODO: Currently only supports 1 stop bit.` (`:391`). So `stop_bits=0.0`, `0.5`, `1.0` and `1.5` all read one stop slot at bit 9; the option does not add a second check (**observation from code; runtime consequence is inference**). Master later fixed this (§7).
- `format_value()` `:334-374`: `hex` pads to `(data_bits+4-1)//4` uppercase digits (**two digits for 8 bits**, no `0x`), `dec` unpadded, `oct`/`bin` zero-padded, `ascii` prints 32…126 literally and falls back to `[XX]` (`[XXX]` above 8 bits) otherwise.
- RX/TX inversion is applied at sample/edge/idle inspection (`:449-464`, `:466-480`, `:482-499`); `invert_rx=yes` flips the RX level (`inv[RX]` from `decode()` `:509-510`).

---

## 3. Exact output annotation classes (`pd.py:124-160`)

### 3.1 Declared classes — index order is the class number

Class index is the tuple position (sigrok-cli assigns it by iterating the list, `decode.c:350-356`).

| idx | class id | description (declared) |
|---|---|---|
| 0 | `rx-data` | RX data |
| 1 | `tx-data` | TX data |
| 2 | `rx-start` | RX start bits |
| 3 | `tx-start` | TX start bits |
| 4 | `rx-parity-ok` | RX parity OK bits |
| 5 | `tx-parity-ok` | TX parity OK bits |
| 6 | `rx-parity-err` | RX parity error bits |
| 7 | `tx-parity-err` | TX parity error bits |
| 8 | `rx-stop` | RX stop bits |
| 9 | `tx-stop` | TX stop bits |
| 10 | `rx-warnings` | RX warnings |
| 11 | `tx-warnings` | TX warnings |
| 12 | `rx-data-bits` | RX data bits |
| 13 | `tx-data-bits` | TX data bits |
| 14 | `rx-break` | RX break |
| 15 | `tx-break` | TX break |
| 16 | `rx-packet` | RX packet |
| 17 | `tx-packet` | TX packet |

Rows (`annotation_rows`, `:144-155`), id → class indices:
`rx-data-bits`→(12) · `rx-data` ("RX")→(0,2,4,6,8) · `rx-warnings`→(10) · `rx-break`→(14) ·
`rx-packets`→(16) · `tx-data-bits`→(13) · `tx-data` ("TX")→(1,3,5,7,9) · `tx-warnings`→(11) ·
`tx-break`→(15) · `tx-packets`→(17).

Binary classes (`:156-160`): 0 `rx` "RX dump", 1 `tx` "TX dump", 2 `rxtx` "RX/TX dump".

### 3.2 Which classes are actually emitted on an 8N1 RX decode

| event | emission site | class used | text variants (longest first) |
|---|---|---|---|
| start bit OK | `:263` `putg` | 2 `rx-start` | `Start bit`, `Start`, `S` |
| each data bit level | `:296` `putg` | 12 `rx-data-bits` | `0` / `1` (single string, `'%d' % signal`) |
| completed byte value | `:318` `putx` | 0 `rx-data` | one string from `format_value()` — `41` for 0x41 at hex/8 bit |
| stop bit | `:402` `putg` | **4 `rx-parity-ok`** | `Stop bit`, `Stop`, `T` |
| stop-bit or start-bit violation | `:250`, `:398` `putg` | 10 `rx-warnings` | `Frame error`, `Frame err`, `FE` |
| break condition | `:415` `putgse` | 14 `rx-break` | `Break condition`, `Break`, `Brk`, `B` |
| packet (only if delim/len set) | `:288` `putx_packet` | 16 `rx-packet` | one string, values joined by space (non-ascii) or concatenated (ascii) |
| parity bit OK / error (only if parity ≠ none) | `:382` / `:386` | 4 / 6 | `Parity bit`,`Parity`,`P` / `Parity error`,`Parity err`,`PE` |

Two non-obvious, load-bearing observations:

1. **Class 8/9 (`rx-stop`/`tx-stop`) are declared but never emitted.** The stop bit is annotated under
   class 4/5 (`rxtx + 4`, `:402`) — the class *named* "parity OK". `grep` for `rxtx + 8`/`rxtx + 9`
   and for class indices 8/9 in emission calls returns nothing. Therefore `-A uart=rx-stop` selects
   an empty class in 0.5.3, while `-A uart=rx-parity-ok` also yields stop-bit text on 8N1 where no
   parity bit exists.
2. **`FRAME` and `IDLE` never become annotations.** They go only to `OUTPUT_PYTHON`
   (`putpse` at `:253`, `:405-407`, `:413`, `:498`). The annotation stream for a clean 8N1 RX frame is
   exactly: start-bit text, eight single-digit bit texts, one value text, one stop-bit text — plus
   warning/break/packet classes when their conditions occur.

Span semantics (helpers `:163-192`): a bit annotation spans `sample ± bit_width/2` around its
midpoint; the value annotation spans from the first data-bit midpoint minus half a bit to the last
data-bit midpoint plus half a bit; break spans frame start to the current sample; packet spans the
first frame's start minus half a bit to the delimiter/length sample plus half a bit.

### 3.3 Python-output classes and binary payloads (for completeness)

Docstring `pd.py:24-50` defines the python packet `[<ptype>, <rxtx>, <pdata>]` with
`rxtx` 0=RX, 1=TX and `ptype` ∈ `STARTBIT`, `DATA` (tuple: value 0…511, per-bit list),
`PARITYBIT`, `STOPBIT`, `INVALID STARTBIT`, `INVALID STOPBIT`, `PARITY ERROR` (expected, actual),
`BREAK` (data 0), `FRAME` (value, validity bool), `IDLE` (data 0).
Binary output (`:217`, `:321-322`): `bw = (data_bits + 7) // 8` (1 byte at 8 data bits);
each value is written `to_bytes(bw, 'big')` twice — once under class `rxtx` (0/1) and once under
class 2 (`rxtx` combined dump). At 8 data bits the byte equals the decoded value.

---

## 4. How those classes reach the caller: sigrok-cli 0.7.2 (supporting source)

Pinned: tarball `https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz`, sha256
`71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8`; git tag `sigrok-cli-0.7.2`
→ peeled commit `b584f959edb788f1731d5a304badf241ac21bf65`; embedded `doc/sigrok-cli.1` sha256
`e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` (identical to the raw file at the tag).

- **`-A` / `--protocol-decoder-annotations` matching** (`decode.c:314-411`): the token is
  `decoder[=name[:name…]]`. Each name is compared first against annotation-class **id**
  (`ann_descr[0]`, `:351-356`), then against annotation-row **id** (`row_desc->id`, `:366-370`);
  class wins when both match. `canon_cmp` (`parsers.c:481-510`) lowercases and deletes every
  character except `[a-z0-9]`, so `rx-data`, `RX_Data`, `rx data` and `rxdata` are the same key.
  No match → `g_critical("Annotation '%s' not found …")` and non-zero return (`:392-396`).
  Consequence: the decoder's `rx-data` **class** shadows the identically named `rx-data` **row**;
  `-A uart=rx-data` selects only index 0 (byte values), not the row's (0,2,4,6,8).
- **Output line shape** (`decode.c:664-709`): default loglevel is `SR_LOG_WARN`
  (`options.c:27`). With `--protocol-decoder-samplenum` and no `-l`, `show_snum` is true and
  `show_class`/`show_quotes`/`show_abbrev` are false, so each line is exactly
  `printf("%" PRIu64 "-%" PRIu64 " ", start, end)` + `printf("%s: ", proto_id)` + **the longest
  text only** (`pda->ann_text[0]`). `proto_id` defaults to the decoder instance id
  (`libsigrokdecode type_decoder.c:480-481`), and an instance without an explicit `id` is named
  `<decoder_id>-<n>` with `n` starting at 1 (`instance.c:345, 368-373`). So a one-decoder uart run
  emits lines like `1234-1298 uart-1: 41`, not `uart: 41`. At `-l 4`+ the class id and all text
  variants are also printed (`:697-706`).
- **`--show` inventory** (`show.c:856-940`; annotation block `:907-930`) prints `Annotation classes:` as `- <id>: <desc>` in
  declaration order, then `Annotation rows: - <row id> (<desc>): <class ids…>`, then
  `Binary classes:`, `Optional channels:`, and `Options: - <id>: <desc> (…, default <v>)`.
  This is the observable form of §2–§3 for `inspect-signal-decoders`; it derives from the same
  `pd.py` declarations, so a tool listing and this source must agree id-for-id.
- **`-P` option syntax** (`doc/sigrok-cli.1`, `-P` section): `uart:key=value:…`, comma separates
  decoder stacks. The manpage's own example is `-P uart:baudrate=115200:parity_type=odd`, but the
  0.5.3 decoder declares **`parity`**, not `parity_type` (observation: `pd.py:107` vs manpage line
  ~293). Per the same manpage ("options … not actually supported … will be interpreted as being
  channel name/number assignments") and `decode.c:160-173`, an unmatched key survives option and
  channel extraction, triggers `g_critical("Unknown option or channel …")`, and `register_pd` breaks
  **without setting its error return** (`:167-173`); `main.c:263` only aborts on non-zero. Inference:
  a misspelled option can leave the uart instance uncreated while the process continues to decode
  with empty annotation output — consistent with REA's own limitation text "Empty output does not
  establish absence of traffic" (`SigrokRecordingProvider.js`, sha256 `7979bafb…2dced7`, lines 229-230).
  Not executed; the control flow is observed, the runtime outcome is not.
- REA 6.5.0 constructs the producer argv as `--dont-scan --input-file=recording
  --protocol-decoders=<decoders> --protocol-decoder-samplenum [--input-format=…]
  [--protocol-decoder-annotations=…]` (`SigrokRecordingProvider.js:191-202`, hash above). It passes
  **no** `-c`/`-l` and no `-B`, so the caller's baud/data/parity/stop choices can only travel inside
  the `--decoders` stack string, and output is the default-loglevel annotation text described above.

---

## 5. Release vs git master (calibration boundary)

`pd.py` at `master` now sha256 `67655f53162c531bc6eb77d9d29b384edec80a2dd5bd741897b4aa2afc52ffcc`;
`diff -u` against 0.5.3 shows the decoder is **not** interchangeable:

- class ids 10/11 renamed `rx-warnings`/`tx-warnings` → `rx-warning`/`tx-warning`, 12/13
  `rx-data-bits`/`tx-data-bits` → `rx-data-bit`/`tx-data-bit`;
- row ids renamed (`rx-data`→`rx-data-vals`, `rx-break`→`rx-breaks`);
- stop bits moved to their own class (`Ann.RX_STOP`, 8/9) and **multiple** stop bits are now read
  (`stopbits` list, loop until `stop_bits` reached), removing the 0.5.3 one-stop-bit TODO;
- new `sample_point` option (default 50) replaces the hard-coded midpoint;
- `stop_bits` enum gains `2.0`; state handling refactored into `advance_state()`.

Any claim grounded in 0.5.3 (`-A uart=rx-warnings`, stop bits under class 4, midpoint sampling) must
not be carried to a decoder tree that is git master or a distro build carrying those changes.
libsigrokdecode 0.5.3 is the newest release on the official download page (2019-12-11); master is
tagged only `libsigrokdecode-unreleased` (`git ls-remote` above).

---

## 6. Bearing on R23-C1 (no credit claimed)

- For `inspect-signal-decoders`: this pins what the decoder inventory for `uart` must contain —
  id `uart`, the exact option ids/defaults in §2, the 18 class ids with their descriptions, the ten
  rows and three binary classes. A tool listing that diverges from these ids is a different
  decoder revision, not a formatting quirk.
- For `decode-signal-recording`: this pins what a uart 8N1 RX decode can put in
  `annotations_text` — start/bit/value/stop lines under classes 2/12/0/4, warnings under 10,
  break under 14, packets under 16, `FRAME`/`IDLE` absent from annotations, line prefix
  `uart-1: `. It also names a concrete empty-output cause (misspelled option) that is not
  "no traffic".
- It is **source evidence only**: no REA envelope, no `ev_…` Evidence id, no non-refused record,
  and no recording was decoded. It must not be counted as a T1 witness, and it does not touch
  dynamic/debugger ownership, which stays unresolved.

---

## 7. Draft registry rows (L1 assigns ids; highest existing row is S057)

The claim requires new knowledge to cite opened/mined **S058+**. Two draft rows follow; ids are
**not** assigned here, and sibling round-23 seats may be drafting into the same range — L1 must
allocate and dedupe. Both are `mined` (opened and read) with today's date.

```
| S0xx | libsigrokdecode 0.5.3 UART decoder — https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz (extracted `decoders/uart/pd.py`); git tag `libsigrokdecode-0.5.3` → commit `97991a3919da6a07c4c87308ae66fb441bd512e3` | code | A | The released UART decoder's declared channels, options, annotation classes/rows, binary classes and 8N1 sampling/stop-bit behaviour; not any runtime decode, not git master, not sigrok-cli's option syntax | Tarball sha256 `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0` (892783 bytes, 2019-12-11); `pd.py` sha256 `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62`, byte-identical to `raw.githubusercontent.com/sigrokproject/libsigrokdecode/libsigrokdecode-0.5.3/decoders/uart/pd.py`; anchors `:95-123` channels/options, `:124-160` annotations/rows/binary, `:219-235` bit width and sample point, `:391-407` one-stop-bit path, `:515-521` frame length | Defaults are 8 data bits, parity none, 1.0 stop bit, 115200 baud, LSB-first, hex; class 8/9 `rx-stop`/`tx-stop` are declared but never emitted because stop bits use class 4/5; `FRAME`/`IDLE` are python-only. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/UartSemantics.md |
| S0xx | sigrok-cli 0.7.2 annotation selection and rendering — https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz (`decode.c`, `show.c`, `parsers.c`, `doc/sigrok-cli.1`); git tag `sigrok-cli-0.7.2` → commit `b584f959edb788f1731d5a304badf241ac21bf65` | code | A | How `-A` resolves class vs row names, how `--protocol-decoder-samplenum` shapes stdout, and how `--show` lists a decoder; not decoder internals and not any executed decode | Tarball sha256 `71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8`; `decode.c` sha256 `f2fc8af880cabc7e83574c626f8e3ca10eff4c658db5bd9e42fd192aacae53a1` (`:314-411` matching, `:664-709` rendering); `parsers.c` sha256 `0d2cffb62f3e1162126f3e17955b09832c60c37c98210844b8b33493c9a19b7e` (`:481-510` `canon_cmp`); `show.c` sha256 `ae9d8c1ca9f05f3abfc7192a6cc02ae93ff15e77185ae8c43bc1e8544244ac9f` (`:861-940`); manpage sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` | Annotation names are matched on the decoder's class id first, then row id, canonically (case/separator-insensitive); default output with sample numbers is `<start>-<end> <instance-id>: <longest text>`, with instance id `uart-1` for one instance. | mined | 2026-10-21 | on-release | .ufo/waves/round-23/w1/UartSemantics.md |
```

If L1 admits only one row, the first is the load-bearing one; the second is the caller-side mapping.

---

## 8. Commands, exits, retained failures

| argv (cwd) | exit | observed |
|---|---|---|
| `curl -fsSL -o libsigrokdecode-0.5.3.tar.gz https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz` (`…/w1/_uart`) | 0 | 892783 bytes, sha256 `c50814aa…` |
| `tar xzf libsigrokdecode-0.5.3.tar.gz` | 0 | `decoders/uart/{__init__.py,pd.py}`, 561-line `pd.py` |
| `curl -fsSL https://sigrok.org/download/source/libsigrokdecode/` | 0 | newest entry `libsigrokdecode-0.5.3.tar.gz 2019-12-11 22:50 872K`; no digest sidecar |
| `curl -fsSL -o pd-tag.py https://raw.githubusercontent.com/sigrokproject/libsigrokdecode/libsigrokdecode-0.5.3/decoders/uart/pd.py` | 0 | sha256 `51a29d0e…`; `cmp pd-tag.py …/pd.py` → `IDENTICAL` |
| `git ls-remote --tags https://github.com/sigrokproject/libsigrokdecode` | 0 | tag object `1577c435…`, peeled `97991a39…` |
| `curl -fsSL -o pd-master.py …/master/decoders/uart/pd.py`; `diff -u` | 0 | sha256 `67655f53…`; class/row renames, stop-bit and sample-point changes (§5) |
| `grep -n '8N1\|8-N-1' pd.py` | 1 | no match (literal absent) |
| `grep -n 'rxtx + 8\|rxtx + 9' pd.py` | 1 | no match (classes 8/9 never emitted) |
| `curl -fsSL -o sigrok-cli-0.7.2.tar.gz https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz`; `tar xzf` | 0 | sha256 `71d0443f…`; `decode.c`, `show.c`, `parsers.c`, `doc/sigrok-cli.1` present |
| `curl -fsSL -o cli-man.1 https://raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1`; `cmp` with tarball copy | 0 | sha256 `e3f06dfe…`; `IDENTICAL` |
| `git ls-remote https://github.com/sigrokproject/sigrok-cli refs/tags/sigrok-cli-0.7.2{,\^{}}` | 0 | tag object `2f342b4d…`, peeled `b584f959…` |
| `pacman -Si libsigrokdecode sigrok-cli` | 0 | `0.5.3-10` / `0.7.2-3`; read-only sync query only |
| `python3` AST probe of `pd.py` annotations | 1 | helper errored on `ast.List.args` after printing the annotations/binary tuples; superseded by direct line reads, no conclusion rested on it |
| `sha256sum` on all retained files | 0 | values in §1, §9 |

No `sigrok-cli`, decoder, `sigrok-cli --version`, REA CLI, MCP device, `prlimit`, debugger, Frida,
ADB or recording was run. No target binary or APK was opened.

---

## 9. Produced files

| absolute path | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/UartSemantics.md` | in adjacent `UartSemantics.md.sha256` (computed after the final edit, so this file needs no self-reference) |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/_uart/libsigrokdecode-0.5.3.tar.gz` | `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0` |
| `…/w1/_uart/libsigrokdecode-0.5.3/decoders/uart/pd.py` (extracted) | `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` |
| `…/w1/_uart/libsigrokdecode-0.5.3/decoders/uart/__init__.py` | `351098a23f5caa205068688550af53bd44a63776e1d02921ba32487ce720b92f` |
| `…/w1/_uart/libsigrokdecode-0.5.3/instance.c` | `9f744bddd6a6d5db388899d11c0b9d94dce1b0b9d19afaffb0f78f0a0eb43784` |
| `…/w1/_uart/libsigrokdecode-0.5.3/type_decoder.c` | `6753e1ef23885b6af4a4db92c345cf5c93a51a0c3e81210b40eb7c99e3f4142f` |
| `…/w1/_uart/pd-tag.py` (raw tag copy) | `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` |
| `…/w1/_uart/pd-master.py` (comparison only) | `67655f53162c531bc6eb77d9d29b384edec80a2dd5bd741897b4aa2afc52ffcc` |
| `…/w1/_uart/sigrok-cli-0.7.2.tar.gz` | `71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8` |
| `…/w1/_uart/cli-man.1` | `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` |
| `…/w1/_uart/sigrok-cli-0.7.2/decode.c` | `f2fc8af880cabc7e83574c626f8e3ca10eff4c658db5bd9e42fd192aacae53a1` |
| `…/w1/_uart/sigrok-cli-0.7.2/show.c` | `ae9d8c1ca9f05f3abfc7192a6cc02ae93ff15e77185ae8c43bc1e8544244ac9f` |
| `…/w1/_uart/sigrok-cli-0.7.2/parsers.c` | `0d2cffb62f3e1162126f3e17955b09832c60c37c98210844b8b33493c9a19b7e` |
| `…/w1/_uart/sigrok-cli-0.7.2/doc/sigrok-cli.1` | `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` |

All writes are inside `.ufo/waves/round-23/w1/`; no production lane, corpus, MANIFEST, jj or
sibling-repo file was touched.

---

## 10. Installs

None. No pacman transaction, no `uv`/`npx`/cargo/npm install, no config edit. Host state unchanged.
(`pacman -Si` is a read-only sync-database query; pacman transactions are paused host-wide.)

---

## 11. Open risks and unknowns

1. **No execution.** Nothing here is a decoder run. The line shape `uart-1: …`, the empty-output
   consequence of a misspelled option, and the `-A` precedence are read from source; they were not
   observed with a real `sigrok-cli` and recording.
2. **Which libsigrokdecode a future REA run links.** Accumulated knowledge here is release 0.5.3;
   REA only checks the version banner contains `libsigrokdecode`, so a host build against
   master/unreleased would change class ids (§5) and invalidate id-keyed selection. Unknown.
3. **Distro patching.** Arch ships `libsigrokdecode 0.5.3-10`; whether pkgrel patches alter
   `decoders/uart/pd.py` is unverified. The release tarball is the pinned authority.
4. **Channel mapping.** Positional default mapping and explicit `rx=<n>` were read from
   `instance.c`/the manpage; no `.sr` recording was opened, so the actual channel order of any lane
   fixture remains unknown.
5. **`-A` with a row name that collides with a class id** (`rx-data`, `rx-warnings`) silently means
   "class only". A caller expecting the row's full set is not warned. This is source-observed, not
   a documented caveat.
6. **Registry ids.** Draft rows in §7 use `S0xx`; ids and `mined` status belong to L1, and sibling
   round-23 seats may target the same range.
7. **Claim impact.** Zero T1 witnesses from this seat. R23-C1's k stays whatever L1 measures; this
   report only supplies held source semantics, not a held verb record.

Report: `.ufo/waves/round-23/w1/UartSemantics.md`
