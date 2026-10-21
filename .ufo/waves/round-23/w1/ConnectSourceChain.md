# ConnectSourceChain — exact source hierarchy for raw UART bytes, sigrok annotations, REA envelope and own-work source

Seat: `KaidokuR23.ConnectSourceChain` (connector, leaf). Author-side report; not outside
verification or admission. Lane HEAD read: `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
Cutoff for every observation below: **2026-10-21 ~14:52 UTC** (`11:52 -0300`). The source
table and counter moved while this seat read them; both states are recorded in §10. This
report proposes a hierarchy; it does not claim a final count, a held verb, or another seat's
result as verified.

No production file, registry row, knowledge entry, counter or evidence file was edited. The
only file written is this report. Two transient files were created and immediately removed
(disclosed in §2): `/tmp/pd_upstream_053.py` and `runtime/squashfs-root/err.txt`. Neither was
used as retained evidence. No device, APK, debugger, Frida or target carrier was executed or
attached. The local `sigrok-cli` behaviour probes in §2 ran against the already-extracted
AppImage and, for the error-path probe, against the decoder's own `pd.py` file as a regular
input file. Those are tool-behaviour probes, not signal claims.

## 1. The hierarchy in one table

Each layer is a different authority. The right-hand column is the fact that layer **must not**
be cited for. `[OBS]` = observed in a retained envelope/run or by a command recorded here;
`[INF]` = inference from pinned source; `[UNK]` = not established by this seat.

| Layer | What it alone establishes | Pinned authority (path / commit / sha256) | Evidence record | Must not be cited for |
|---|---|---|---|---|
| **L0 raw carrier** | The exact bytes/samples and their declared rate: synthetic `uart-hi.bin` (2,500 B, `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`, 960,000 Hz, 100 samples/bit, payload `4869`) and official `hello_world_8n1_9600.sr` (58,381 B, `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; zip member `metadata`: `driver = chronovu-la8`, `unitsize = 1`, `samplerate = 625 kHz`, `probe1 = TX`; `logic-1` = 8,388,608 samples) | Synthetic: `tools/make-uart.py` (`8720ee4e…` at cutoff; run-time hash not retained) + `generate-uart.run.json` (`1190f3dc…`). Official: `official-download.json` (`42648310…`) + `.sr` metadata read in memory | `decode-uart-hi.*`, `decode-official-uart.*` | UART framing, annotation meaning, decoder success, tool identity, external acquisition truth |
| **L1 raw-format mapping** | How bytes become samples/channels: `numchannels`/`samplerate` options, channel names `"0"…"N-1"`, `unitsize = ceil(N/8)`, channel index → bit index, samplerate metadata only when non-zero, binary never autodetected (no `format_match`/metadata, extensionless private copy) | libsigrok 0.5.2, commit `a6b07d7e28fe445afccf36922ef7d20e63e54fe6`; `src/input/binary.c` `fa037abe…` `:33-34,47-51,59-64,83-87,101-106,174-184`; `include/libsigrok/libsigrok.h` `:492-497,596-600`; `src/input/input.c:499-501`; output writers `vcd.c:240-243`, `ascii.c:185-187` | Synthetic envelope `selection.input_format = binary:numchannels=1:samplerate=960000`; official uses `input_format:null` and is **not** this layer | UART semantics, annotation rendering, REA fields |
| **L2 decoder semantics** | What `uart` means: optional `rx`/`tx` decoder channels, 8N1 framing (`start 0`, 5–9 data LSB-first, optional parity, 1+ stop), defaults (`baudrate 115200`, `data_bits 8`, `parity none`, `stop_bits 1.0`, `bit_order lsb-first`, `format hex`), annotation classes/rows, `SamplerateError` and `ChannelError` | libsigrokdecode 0.5.3, tag commit `97991a3919da6a07c4c87308ae66fb441bd512e3`; tarball `c50814aa…`; `decoders/uart/pd.py` `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62`, `:95-152,218-223,334-360,501-507` | Both decode envelopes, through the observed `annotations_text` | That a decode ran, CLI display format, REA field semantics |
| **L2′ CLI rendering** | How the decoder text is produced/displayed: `-I` colon grammar + `strtoul(...,10)`, `-P` stack and **literal channel-name** matching for the first decoder only, `-A` class-before-row lookup, `--protocol-decoder-samplenum` prefix `"start-end "`, `--version` banner, exit 0 on a decoder session error (only `srd_session_send` failure stops the session) | sigrok-cli 0.7.2, tag commit `b584f959edb788f1731d5a304badf241ac21bf65`; tarball `71d0443f…`; `parsers.c:36,224,337-376,429-479`; `decode.c:184,314-397,677,721`; `input.c:53-54`; `session.c:417-419`; `main.c:339`; `show.c:72` | Envelope `tool.arguments` and `annotations_text`; observed error-path probe (§2) | Decoder internals; REA envelope contract |
| **L3 REA envelope** | The producer contract and observed producer run: exact sigrok argv, version gate, wrapper realpath/hash, `artifact`/`selection`/`annotations_text`/`output_window`/`diagnostics`/`tool`/`resource_limiter`/`limits`/`hardware_acquisition`, line-window semantics, exit-code-only refusal, provider limitations (annotations not independently verified; not a lossless byte stream) | installed `rea-agents@6.5.0`: `dist/signals/SigrokRecordingProvider.js` `7979bafb…` `:128-142,192-202,229-231`; `dist/domain/signals/signalRecording.js` `0ef15149…` `:56-115`; `dist/domain/signals/annotationTextWindow.js` `11f176ad…`; `dist/contracts/signals/signalToolContracts.js` `61553044…`; `dist/application/signals/SignalRecordingService.js` `97a5ffcf…` | All `.envelope.json`/`.run.json` pairs | Sigrok semantics, decoder identity, “decode succeeded”, payload truth |
| **L4 own-work observation** | The exact run: argv, `REA_SIGROK_COMMAND`, cwd, exit, stdout/stderr, ev id, annotations text, window, diagnostics; plus the generator receipt and pinned carriers | `evidence/c1/{decode-uart-hi,decode-official-uart,decode-invalid-decoder,inventory,uart-help}.{envelope,run}.json`; `generate-uart.run.json`; `official-download.json`; `tool-runtime-pins.json` `02ef8379…`; `sigrok-extraction.json` `2b84f466…` | itself | External protocol semantics, acquisition truth, publisher authenticity, temporal custody |
| **L5 tool identity** (bridge) | Which files actually executed: AppImage `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`; wrapper `50fe4359…`; ELF `10fed05a…`; `libsigrok.so.4` `0861b03c…`; `libsigrokdecode.so.4` `4bfe11a3…`; `uart/pd.py` `51a29d0e…`; host `libgmodule`/`libglib`/`libgio` at one instant | `sigrok-extraction.json` (argv/exit/appimage sha) + `tool-runtime-pins.json` (paths/sha/size, `captured_at 2026-10-21T14:42:59Z`, limit “one named instant; selected files only”) + envelope `version_banner` | `tool.sha256` in every envelope = wrapper only | Publisher authentication, continuous custody, wrapper behaviour |

The rows above are **authorities, not a count**. A fact is admitted only by the lowest layer
that owns it; higher layers preserve but never upgrade it.

## 2. Probe ledger (actual argv/env/exit; only what this seat ran)

All `sigrok-cli` runs used the extracted runtime under
`.ufo/waves/round-23/runtime/squashfs-root` with
`LD_PRELOAD=/usr/lib/libgmodule-2.0.so.0`,
`LD_LIBRARY_PATH=<runtime>/usr/lib:<runtime>/usr/lib64`,
`PYTHONHOME=<runtime>/usr`, `PYTHONPATH=<runtime>/usr/share/pyshared`,
`LC_ALL=C.UTF-8`, `SIGROKDECODE_DIR=<runtime>/usr/share/libsigrokdecode/decoders`.
This differs from `tools/sigrok-cli.sh` (which omits `PYTHONHOME`/`LC_ALL`); the wrapper's own
env is in that file, and the retained envelopes show the same producer banner.

| # | argv | exit | observation |
|---|---|---|---|
| 1 | `sha256sum /home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` | 0 | `49d2f597…9f50b614`; matches `sigrok-extraction.json` and `setup-sigrok.py` `EXPECTED` |
| 2 | `sigrok-cli --version` (same extracted runtime) | 0 | first line `sigrok-cli 0.7.2`; banner reports `libsigrok 0.5.2`, `libsigrokdecode 0.5.3`, Python `3.5.2`, glib `2.48.2 (rt: 2.90.1)`; matches envelope `tool.version_banner` |
| 3 | `sigrok-cli --dont-scan --protocol-decoders=uart --show` | 0 | `ID: uart`; optional channels `rx`/`tx`; options `baudrate`, `data_bits 5..9 default 8`, `parity none…`, `stop_bits 1.0`, `bit_order lsb-first`, `format hex`; annotation classes `rx-data` …; content agrees with the 81-line help window in `uart-help.envelope.json` (exact byte comparison not run) |
| 4 | `sigrok-cli --dont-scan -i <runtime>/usr/share/libsigrokdecode/decoders/uart/pd.py --input-format=binary:numchannels=1 --protocol-decoders=uart:rx=0:baudrate=9600 --protocol-decoder-annotations=uart=rx-data --protocol-decoder-samplenum` (stderr captured to a file, then removed) | **0** | stdout empty; stderr carries `srd: SamplerateError: … Cannot decode without samplerate.` with traceback at `pd.py:503`. This is the calibration counterexample: **exit 0 does not mean a decode happened** |
| 5 | same as #4 with `samplerate=1000000`, `format=ascii` | 0 (pipeline to `head`) | display lines observed as `106-940 uart-1: [D9]`, `1153-1987 uart-1: J`, `2250-3084 uart-1: Y`; confirms the samplenum prefix format from `decode.c:721` and the `format=ascii` rendering from `pd.py:345`. Run on the decoder's own file — behaviour probe, not a signal claim |
| 6 | `python3 -I -B` `zipfile` read of `hello_world_8n1_9600.sr` | 0 | members `version`, `logic-1` (8,388,608 B), `metadata` (150 B); metadata quoted in §1 L0 |
| 7 | `python3 -I -B` parse of official `annotations_text` | 0 | 12,885 lines; first `108-628 uart-1: BA`; last `8388112-8388632 uart-1: 64`; max end 8,388,632 > `logic-1` length 8,388,608 by 24 samples |
| 8 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | **1** at 11:47 local | three `E11` for `S058`/`S059`/`S060` citing missing `corpus/lessons/round-23.md` |
| 9 | same census at 11:50 local | **0** | W04 only; live table 61 rows (S061 now a Dart own-work row). Both outputs retained here; the change is L1's, not this seat's |
| 10 | `sha256sum tools/make-uart.py` at 11:44 and 11:47 local | 0 | `e22a8f1f…` → `8720ee4e…`; mtime 11:45:20; docstring-only edit (“the actual pinned fixture is retained; this recipe alone is not a measured cross-run byte-equality claim”). In-memory recomputation of the current bit logic yields `4a2e729f…`, the retained fixture hash. The run record does **not** pin the generator hash or a timestamp |

**Disclosure of read-only-seat violations.** The error-path probe (#4) wrote `err.txt` inside
`runtime/squashfs-root` to capture stderr; it was deleted immediately. The upstream decoder
comparison wrote `/tmp/pd_upstream_053.py`; it was deleted immediately. Neither survives or is
cited as retained evidence. The contract says read-only seats write only their report; these
were transient and are reported rather than hidden.

## 3. Exact namespace separation (the non-obvious part)

The same word is not the same object across layers. Every mapping below needs its own authority:

| Name in the chain | Synthetic `.bin` | Official `.sr` | Authority |
|---|---|---|---|
| REA option name | `input_format` | `input_format` | REA schema (`signalRecording.js`) |
| Producer flag | `--input-format=…` | omitted (`null`) | REA provider argv (`SigrokRecordingProvider.js:192-202`) |
| Input format | `binary:numchannels=1:samplerate=960000` | autodetected srzip | libsigrok binary module / `.sr` metadata |
| Carrier channel name | `"0"` (libsigrok binary names by index) | `"TX"` (`.sr` metadata `probe1 = TX`) | L1 for binary; carrier metadata/README for srzip |
| Decoder channel id | `rx` | `rx` | `uart/pd.py:95-100` |
| Decoder selection | `uart:rx=0:baudrate=9600` | `uart:rx=TX:baudrate=9600` | combination of the two rows above; **not** a universal recipe |
| Annotation class | `rx-data` (class 0) | `rx-data` (class 0) | `uart/pd.py:124-152` + sigrok-cli class-first lookup (`decode.c:314-397`) |
| Annotation text | `48`, `69` (hex default) | `BA`, `BD`, … `64` (hex) | `pd.py:111,334-360`; `decode.c:721` |
| Payload interpretation | ASCII `Hi` (`4869`) | “Hello World!\r\n” per README | generator receipt / README, **not** the annotation text |

Two concrete traps follow:

1. REA's own contract example is `uart:rx=RX:baudrate=9600`
   (`signalToolContracts.js`). That resolves only for an input whose channel is literally
   `RX`; it does **not** resolve for `binary`, whose channels are `0…N-1`, and it does not
   resolve for the official `.sr`, whose channel is `TX`. The successful runs use `0` and
   `TX` respectively. The decoder-side id `rx` is constant; the input-side name is not.
2. `uart=rx-data` is both a class id (index 0, “RX data”) and a row id (classes
   `0,2,4,6,8`). sigrok-cli looks up the class first, so the observed two-line synthetic
   output contains only data annotations, not start/stop. A claim that the row was selected
   would be a different, unsupported claim.

## 4. Two carriers, one verb — the counting consequence

The retained records are two `decode-signal-recording` runs over different carriers:

| Fact | Synthetic `uart-hi.bin` | Official `hello_world_8n1_9600.sr` |
|---|---|---|
| carrier sha256 | `4a2e729f…861727` | `01b72610…900b61` |
| rate | 960,000 Hz (`input_format`) | 625 kHz (`.sr` metadata; README) |
| channel mapping | `uart:rx=0` | `uart:rx=TX` |
| acquisition | `synthetic; no hardware` (generator receipt) | third-party Olimex STM32-H103 / ChronoVu LA8 per README (source attribution, not our observation) |
| envelope / run | `a40c947c…`, `2c1984eb…` | `7d5e07cc…`, `0bdd0026…` |
| ev id | `ev_bcadf773…bd3e` | `ev_1d361f25…7e5c` |
| output window | 2/2, `has_more:false` | 12,885/12,885, `has_more:false` |
| literal text | `300-1100 uart-1: 48` / `1300-2100 uart-1: 69` | head `108-628 uart-1: BA …`; includes `0D 0A` then `48 65 6C 6C 6F…`; last range ends past `logic-1` |
| tool hash | wrapper `50fe4359…` | same wrapper |

These are **two witnesses for one verb**, not two coverage increments. The frozen counter
reduces each verb to a boolean (`exercised`); two `decode-signal-recording` envelopes add
corroboration and depth, not a second unit. Presenting them as two held verbs would hit the
`same verb double counted` falsifier.

With the historical `identify-flutter-build` witness plus `inspect-signal-decoders`
(`inventory.envelope.json` `5f802187…`, `ev_940cf7bb…`; `uart-help.envelope.json`
`462bc694…`, `ev_4be13793…`), the **conditional projection** for this entry is `k=3/6`:
`identify-flutter-build` (historical), `inspect-signal-decoders`, `decode-signal-recording`.
That is a projection from the counter's source, not a measured final count; the entry was
untracked/being edited at this seat's cutoff and the counter file changed during the wave
(§10). `debug-with-gdb`, `debug-with-rizin` and `inspect-dart-aot` are not in this chain; the
refusal envelope is not a witness.

## 5. No source substitutes for another — ten rules with counterexamples

1. **Documentation cannot supply decoder semantics.** The live `S058` manual documents
   `-I`/`-P`/`-A`; it does not define UART optional channels, framing, defaults or
   annotation classes. The entry's sentences “RX is optional because TX is another supported
   direction” and “`rx-data` selects one annotation class” need `uart/pd.py:95-100,124-152,501-507`,
   not the manual. Counterexample: cite `S058` alone for those sentences and the source scope
   is unsupported.
2. **The REA envelope cannot supply signal semantics.** The provider itself says annotations
   are “not independently verified protocol semantics” and not “a lossless byte stream”
   (`SigrokRecordingProvider.js:229-230`). The envelope can quote the text; it cannot say what
   a UART frame is.
3. **Raw bytes cannot supply framing.** `uart-hi.bin` is 2,500 bytes of `00`/`01`; without
   `binary.c` and `pd.py` the bytes do not say “8N1, channel 0, 9600”. Conversely, `pd.py`
   cannot produce the exact bytes; the generator receipt and fixture hash do.
4. **Decoder source cannot prove the run.** `pd.py` and `sigrok-cli` source establish what
   would happen; only the `.envelope.json`/`.run.json` pair establishes that it did, with
   argv/env/exit and the literal text.
5. **Own-work evidence cannot supply external provenance.** The synthetic generator's
   `acquisition: synthetic; no hardware` is an own-work declaration; the official README's
   Olimex/ChronoVu claim is the dataset author's declaration. Neither is verified by the
   other, and neither is verified by this seat.
6. **The envelope's `tool.sha256` is the wrapper, not the decoder.** Every retained envelope
   reports `tools/sigrok-cli.sh` / `50fe4359…`; the executed ELF is `10fed05a…`, the decoder
   module is `51a29d0e…`. Only `tool-runtime-pins.json` bridges this, and it is a
   post-run single instant (`captured_at 14:42:59Z`; decode runs at `14:38:57Z`/`14:38:58Z`).
   Citing the envelope hash as “the sigrok/decoder identity” is a false bind.
7. **Two carriers are not two verbs.** See §4.
8. **Hex annotation text is not the ASCII payload.** The synthetic output is `48`/`69`, not
   `H`/`i`; the official output is hex, not literal `Hello World!`. The `predictions.json`
   `expected_text: "Hello World!"` is not met as literal producer text; converting hex to
   ASCII is our inference and must be labelled as such. The entry already records this
   mismatch; do not “fix” it by quoting the README as if it were the output.
9. **`rx=0`, `rx=TX`, `rx=RX` are three namespaces.** The input-format layer supplies the
   right-hand name; the decoder layer supplies `rx`; the REA/CLI layer joins them. No single
   example is universal.
10. **The catalog is not a decoder inventory.** `inventory.envelope.json` reports 110
    examined/matching/returned with `has_more:false`, but the installed tree has 112 entries:
    `common` is a helper, and `signature` fails to import under Python 3.5.2
    (`0b…_…` numeric literal at `pd.py:138`, visible only in `diagnostics`). The 110 is a
    parsed `--list-supported` count, not all installed modules. This is the
    `inspect-signal-decoders` chain, not the decode semantics chain. (Peer-observed in two
    seats; this seat did not re-run the catalog probe.)

## 6. Contradictions and limits stated as contradictions

- **Assigned 1 MHz vs retained 960 kHz.** The seat prompt says “1MHz”; the generator, its
  receipt and the envelope all say `960000 Hz`, `100 samples/bit`. The artifact wins. If L1
  requires 1 MHz, the fixture and all sample ranges/expectations must be regenerated; the
  current envelope is not a 1 MHz witness. Do not write “1 MHz” beside `4a2e729f…`.
- **`ok:true` vs decode success.** Observed locally at the sigrok-cli layer: missing
  `samplerate` gives exit 0, empty stdout, and a `SamplerateError` traceback in stderr. The
  provider refuses only on `exitCode !== 0` (`SigrokRecordingProvider.js:128`), so the REA
  envelope would be `ok:true` with empty `annotations_text` `[INF from source]`; the counter
  binds `ok:true` plus command/operation, not annotation content. A chain-complete `ok:true` with empty/partial
  annotations is possible. Manual admission must require the literal expectation (non-empty,
  matching hex/ranges) or state a negative; the counter alone cannot.
- **Official README payload vs annotation text.** The `.sr` starts with `BA BD C9 B1 91 85`,
  then `0D 0A`, then repeated `Hello World` hex, with a truncated tail. The README's
  “repeatedly transmitted `Hello World!\r\n`” is the author's description, not a line-for-line
  match.
- **Annotation end beyond recording length.** The last official annotation ends at sample
  8,388,632; `logic-1` holds 8,388,608 samples. The range is decoder-computed; it is not a
  valid byte index and must not be presented as one.
- **Generator changed after the run.** `make-uart.py` was edited at 11:45:20 local, after the
  11:38:40 fixture/run. The edit is docstring-only; the current bit logic reproduces
  `4a2e729f…` in memory. But the run record lacks the generator hash and timestamp, so
  “generator G produced fixture F” is not bound by the run record; the fixture hash is the
  durable anchor, and byte-exactness is claimed for the retained bytes, not for re-synthesis
  (QUALITY #12).
- **Pins are a single instant.** `tool-runtime-pins.json` is one `captured_at` after the
  runs; it is not continuous custody. It is consistent with the envelope's wrapper hash and
  version banner, but a change between run and pin capture would not be detected. State it as
  “selected files at 14:42:59Z”, never “stable during the run” (QUALITY #19).
- **Mixed-ABI runtime.** The wrapper preloads host `libgmodule` to satisfy host `libgio`
  against the 2019 bundle; the banner reports bundled glib 2.48.2 running with host 2.90.1.
  The pins include host `libgmodule`/`libglib`/`libgio`. This is a composite runtime, not the
  stock AppImage; do not call it “the official 0.7.2 binary” without that qualifier.
- **Unsigned AppImage.** `AppImageLibraries` reports zeroed `.sha256_sig`/`.sig_key`; the
  pinned sha256 is identity, not publisher authentication.
- **Live integration state moved under this seat.** The table went 57 → 60 → 61 rows while
  reading; the earlier census exited 1 on three `E11` (missing `corpus/lessons/round-23.md`),
  the later one exited 0. `tools/count-c1.py` also changed (`99259c82…` → `7c356b97…` →
  `76b039ba…` at my read). These are L1's states; this report does not freeze them.

## 7. Bounded move: layer-split the source rows, bridge the tool hash

**Proposed move.** Keep the live `S058` (manual), `S059` (README) and `S060` (own-work
envelopes) rows. Add five layer rows, allocated after the live frontier (`S061` was a Dart
own-work row at cutoff; next free `S062` — L1 must re-check before allocating):

| Proposed id | kind/tier | Authority | Scope it alone owns | Scope it must not own |
|---|---|---|---|---|
| `S062` | code/A | libsigrok 0.5.2 `binary.c` + `libsigrok.h` + output writers + `input.c` (commit `a6b07d7e…`) | byte→sample/channel mapping; `unitsize`; channel names; samplerate metadata; no autodetect | UART framing; CLI display; REA fields |
| `S063` | code/A | libsigrokdecode 0.5.3 `uart/pd.py` (tarball `c50814aa…`; tag commit `97991a39…`; `pd.py` `51a29d0e…`) | optional `rx`/`tx`; 8N1 framing; option defaults; annotation classes/rows; `SamplerateError`/`ChannelError` | that a run happened; CLI class/row resolution; REA envelope |
| `S064` | code/A | sigrok-cli 0.7.2 code (tarball `71d0443f…`; tag commit `b584f959…`) | `-I`/`-P` grammar; literal channel matching; class-first `-A`; samplenum format; exit 0 on decoder session error | decoder internals; REA contract |
| `S065` | code/A | installed `rea-agents@6.5.0` signal provider/schema/window/contract/service (`7979bafb…`/`0ef15149…`/`11f176ad…`/`61553044…`/`97a5ffcf…`) | envelope fields; producer argv; version gate; wrapper hash; exit-code-only refusal; line window; limits; limitations | sigrok semantics; decoder identity; success of decode |
| `S066` | tool/A | AppImage `49d2f597…` + `sigrok-extraction.json` + `tool-runtime-pins.json` (`02ef8379…`) | one-instant identity chain wrapper→ELF→libsigrok→libsigrokdecode→`uart/pd.py`; version banner | publisher authentication; continuous custody; wrapper behaviour |
| `S067` (conditional) | docs/A | sigrok wiki `File_format:Binary` rev 13665 (2018-09-17; raw sha `2d81a085…`) | documented `numchannels`/`samplerate` names/defaults and example | packing, bit order, channel names, autodetect, `1mhz` parsing |

Every new row's `used-by` must name the exact live entry path
`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` literally (no backticks, no
spaces inside a path), and the entry's `source:` first line must cite the rows. The current
three rows also list `corpus/lessons/round-23.md`; at the 11:47 census that path was missing
(E11). Either create a real lesson file or drop the path from `used-by` — do not add a
placeholder.

**Axes affected.**
- **Coverage:** the `decode-signal-recording` witness becomes source-supported (not only
  envelope-bound), enabling the conditional `k=3/6` projection with the historical identify
  and the catalog verb. No new verb is claimed; the refusal is excluded.
- **Calibration:** the manual no longer stands in for decoder semantics; the envelope hash no
  longer stands in for the decoder; `ok:true` no longer stands in for success; two carriers
  no longer stand in for two verbs; hex text no longer stands in for ASCII payload.
- **Depth:** the synthetic exact-byte control and the official acquired carrier remain
  separate, with their own rates, channels and output windows.

**Risks.**
- Row inflation/duplication: `S058` manual vs `S064` code are the same release, different
  documents; scopes must say “docs surface” vs “executed parser”. `S062`/`S063` are different
  repositories; no URL collision. The census compares only the first URL, so content
  duplication is a manual review.
- E11/commit coupling: rows and the entry must land in one commit; `used-by` paths are checked
  at the same revision. The entry was untracked at this seat's cutoff.
- Counter churn: the counter changed during the wave; its docstring admits source relevance
  is manual. Do not treat a green count as semantic admission.
- The official dataset README is a third-party declaration; it cannot become our observation.
- The pins manifest is post-run and single-instant; the generator's run-time hash is not
  retained.
- If L1 regenerates at 1 MHz, the current envelope becomes historical; all ranges/expectations
  must be recomputed.

**Verification for L1 (not run here; not verified).**
1. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` →
   exit 0; no E11; W04 only.
2. `python3 -I -B .ufo/waves/round-23/tools/describe-signals.py --root <lane> --rev <rev>` →
   expected `synthetic_exact:true`, `stdout_byte_equal:true`, subject/carrier digests equal,
   official `output_window {12885,12885,false}`.
3. `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <lane> --rev <rev>` → exact
   JSON; expected `t1_exercised_count=3` only if the entry cites the four signal envelopes and
   their ids; `decode-invalid-decoder` must not bind. Record actual output, not this
   projection.
4. Red substitution test A: remove `S063` (decoder source) and re-review the entry's
   “RX optional / `rx-data` class” sentences; they should become unsupported. This
   demonstrates the move's necessity.
5. Red substitution test B: cite only the envelope `tool.sha256` as decoder identity; the
   pin chain (`50fe4359…` wrapper vs `10fed05a…` ELF vs `51a29d0e…` `pd.py`) should reject it.
6. Red calibration test: a missing-`samplerate` run (exit 0, traceback in `diagnostics`) must
   not be admitted as a successful decode merely because the envelope is `ok:true`.

## 8. Live integration state at cutoff (recorded, not judged)

- `corpus/SOURCES.md`: 61 rows at 11:50 local. `S058` = sigrok-cli 0.7.2 manual; `S059` =
  sigrok-dumps README; `S060` = round-23 offline signal envelopes (own-work); `S061` = round-23
  L1 legacy-layout Saber Dart AOT (own-work, outside this chain and not evaluated here).
- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`: present at 11:43 local,
  sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`, 7,153 B. Its
  `source:` line cites S058/S059/S060; it cites the exact signal envelopes/ids, records the
  synthetic 960 kHz round trip and the official 625 kHz/TX run, and explicitly marks the
  invalid decoder as a rejected witness. Whether it is tracked/committed is L1's state.
- Earlier census (11:47) exited 1 with `E11 S058/S059/S060 missing used-by
  corpus/lessons/round-23.md`; later census (11:50) exited 0 with W04 only. Both are actual
  outputs; the later state is not a claim about the final commit.
- `tools/count-c1.py` at my read `76b039ba…`: eligibility is first-line `source:` plus any
  `S058+` A/B mined row opened `2026-10-21` whose `used-by` contains the entry path; credit is
  per verb mentioned, with an envelope id binding. Source relevance remains manual. The file
  changed during the wave (peers saw `99259c82…`, `7c356b97…`); re-read at the measured
  revision.

## 9. Produced files

| path | note |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ConnectSourceChain.md` | this report; sha256 reported in the seat's final message (embedding it here would change the digest) |

No other file survives. The two transient files in §2 were deleted; no evidence or production
file was written.

## 10. Installs

None. No pacman/uv/npx install, no global or host configuration change. The `npx -y
rea-agents@6.5.0` cache was pre-existing; this seat ran no REA verb. The extracted sigrok
runtime and AppImage pre-existed in the lane.

## 11. Open risks

- The hierarchy is a **proposal**; L1 has not adopted the rows and W2 has not reviewed it.
- The synthetic carrier is 960 kHz, not the prompt's 1 MHz; the official carrier is 625 kHz.
  Any “1 MHz” statement beside these artifacts is false.
- `ok:true` + exit 0 can coexist with a decoder exception; counter binding is not semantic
  admission.
- The wrapper is the envelope's tool identity; the decoder module is outside that hash, and
  the pins are one post-run instant.
- The generator edit after the run means the run record does not bind the generator hash; the
  fixture hash is the durable anchor.
- The official `.sr` is third-party data; its README declares the acquisition, which this seat
  did not verify. The final annotation range exceeds the recorded sample count.
- The counter and source table were moving at cutoff; final numbers must be measured at the
  shipping revision, not read from this report.
