# ConnectSignalFirmware — firmware bytes are not a protocol recording: a provenance ledger for the only admissible join

Seat `KaidokuR23.ConnectSignalFirmware` (connector, leaf, author-side). Round 23 w1, 2026-10-21.
Assignment: connect offline protocol-decoding to the current firmware blob scope without claiming hardware acquisition or sibling ownership.

Read set: `.ufo/waves/round-23/claims.json`; `wave1-spec.json`/`wave1-dispatch.json`; peer w1 reports `ReviewScope.md`, `CriticScope.md`, `SignalCarrierAlternatives.md`, `AppImageLibraries.md`; `evidence/c1/*.run.json` and `*.envelope.json`; `corpus/SOURCES.md`; `corpus/knowledge/2026-10-13-r2-firmware-probe.md`; `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md`; `PROVINCE.md`; installed `rea-agents@6.5.0` signal sources; official sigrok documentation and libsigrok source; the current `/usr/lib/firmware/nvidia` tree; the pacman package cache.

Lane bounds kept: leaf, no subagent, no background job, no MCP device, no device or remote target connection, no hardware, no debugger/Frida, no firmware/APK/carrier execution, no production-lane edit, no install. Six distinct REA CLI invocations were made: four discovery calls (`--help`/`--schema`) exited 0, and two verb attempts refused at the environment gate before any recording was read (probe table; each refusal was run twice with identical argv/exit/stdout and empty stderr to capture the streams separately). This report is author-side, not outside verification, and adds no held verb.

Tags: **OBS** = observed directly by a retained command, or read verbatim from a retained file named here; **INF** = inference from observed text; **UNK** = unknown.

## Axes named

- **coverage** — `claims.json:7` (10; tied-lowest working axis): count of frozen T1 verbs with retained, bound original-envelope evidence. This report contributes **0**.
- **depth** — `claims.json:8` (10): what a held verb's evidence actually binds — subject identity, tool identity, carrier class.
- **calibration** — `claims.json:9` (10): whether a claim's strength matches its evidence class (observed / refusal / derived / unknown).

## Findings

### F1 — The *current* firmware blob scope is `nvidia-utils 615.78.08-1`, not the corpus's `610.57.04` (OBS)

`pacman -Qi nvidia-utils` (exit 0) and `pacman -Si nvidia-utils` (exit 0): version `615.78.08-1`, repository `extra`, build date `Thu 08 Oct 2026 11:41:29 AM -03`, install date `Tue 20 Oct 2026 09:16:30 AM -03`. The four in-scope files are package-owned by that version (`pacman -Qo <file>` exit 0 for each):

| member | bytes | sha256 | owner |
|---|---:|---|---|
| `/usr/lib/firmware/nvidia/615.78.08/gsp_ga10x.bin` | 27,043,992 | `a20100cafd5a85e22b3e13188339730c6ced94bd5f654984dd2ed274ed58d584` | nvidia-utils 615.78.08-1 |
| `/usr/lib/firmware/nvidia/615.78.08/gsp_tu10x.bin` | 22,901,632 | `0c6124c11d59900a05ab5461e5fc7087fc6687a1badead49a7eeca6ed13eeb3b` | nvidia-utils 615.78.08-1 |
| `/usr/lib/firmware/nvidia/615.78.08/ucodes_ga10x.bin` | 58,215,936 | `eed53d76248582d71c629e8b6230aee48ce673c91d782301c94e98ac6a6db7aa` | nvidia-utils 615.78.08-1 |
| `/usr/lib/firmware/nvidia/615.78.08/ucodes_tu10x.bin` | 8,837,632 | `6027ab3736f733b5a06e6e61aaae957d1f990426a263849ebcfa8a49eeb4a5d0` | nvidia-utils 615.78.08-1 |

Durable scope key (survives the next upgrade): `/var/cache/pacman/pkg/nvidia-utils-615.78.08-1-x86_64.pkg.tar.zst`, 330,061,501 B, sha256 `c437ec64cfd4cfba5b8f51641553ec283ec111e14471f4f3a8927c2e3aee8673`. Streaming each member out of that archive (`tar --zstd -xOf <pkg> <member> | sha256sum`, exit 0, four runs) reproduces exactly the four installed digests above.

The historical path is **gone**: `ls -d /usr/lib/firmware/nvidia/610*` → exit 2, `No such file or directory`. The historical package is retained in cache: `/var/cache/pacman/pkg/nvidia-utils-610.57.04-1-x86_64.pkg.tar.zst`, 315,337,340 B, sha256 `2ea5a57afc5104edd40dc4f4b1160f067f09ff1dad7e1bc588408087d1f7c0d0`. Streaming its four members (exit 0) gives exactly the digests recorded in `corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:9-14`:

| 610.57.04 member | streamed sha256 | corpus row |
|---|---|---|
| `ucodes_tu10x.bin` (12,032 B) | `dcbdf512ab09b7f6d946e7f415bcfbc9137f5db1cf0c3c576f4b34b5275acb38` | `:10` |
| `ucodes_ga10x.bin` (31,744 B) | `3a36ceb211c20694f3d2e33ade2bbd2c3ae0b61ba2f28eaff4362aac547a632c` | `:11` |
| `gsp_tu10x.bin` (29,381,504 B) | `d157e3b7dd5da2ca8d1ccb6ca98958f9e35d10a9ef7326277ebac133e4b0d1a7` | `:12` |
| `gsp_ga10x.bin` (84,310,168 B) | `c0156954f3e048d56011524e0c2ae2881bb6db8173b53f9b2f4eb94197f02999` | `:13` |

So the historical firmware claims remain byte-reconstructible from the package cache, but **not from their cited installed path**, and their producer envelopes are gone: the r4u staging report cites `/tmp/r4u-ifr-*.json`, `/tmp/r4u-ef-*.json`, etc. (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaidoku-r4u/01-firmware-deep.md:16,32,56`), and `ls /tmp/r4u-*` → exit 2. The evidence IDs survive only as text in that staging report, later corpus entries that quote them, and `PROVINCE.md:123`.

Scope breadth: `/usr/lib/firmware/nvidia` currently holds **276 regular files** (`find … -type f | wc -l` exit 0). Four are the nvidia-utils members above; the other 272 are per-chip firmware directories (e.g. `/usr/lib/firmware/nvidia/ga102/gsp/booter_load-535.113.01.bin.zst`, `pacman -Qo` exit 0 → `linux-firmware-nvidia 20260916-1`; other chip directories were not individually re-owned). [INF: the tree is broader than the lane's four-file scope; the spot check establishes the package split for one chip family, not for all 272.]

Provider readiness (OBS env; INF gate): this shell has `REA_BINWALK_COMMAND=/usr/bin/binwalk` (3.1.0) and `REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob` (26.6.4), the same tool versions as the r4u run. A firmware-region/extract verb could therefore run on the 615 bytes without any install (the version gates were not re-probed here) — but those are firmware verbs, not T1 verbs, and the historical 56/156 region counts at `PROVINCE.md:123` are 610-only. No firmware verb was run here.

### F2 — The current blobs are not the historical blobs: GSP shape persists, ucodes are no longer stubs (OBS)

`file` (exit 0): both `gsp_*.bin` are `ELF 64-bit LSB relocatable, UCB RISC-V, soft-float ABI, not stripped`; both `ucodes_*.bin` are `data`.

`readelf -h`, `readelf -SW`, and `readelf -x .fwversion` on `gsp_tu10x.bin` (exit 0): `Type: REL`, `Machine: RISC-V`, `e_shoff = 22,900,992`, 10 sections; `.fwimage` PROGBITS at file offset `0x40`, size `0x15d3dc8` (22,887,880 B); `.note.gnu.build-id`; `.fwversion` 10 B = ASCII `615.78.08`; three 0x1000-B `.fwsignature_ga100` / `_tu11x` / `_tu10x`; `.symtab`, `.strtab`, `.shstrtab`. `readelf -x .fwversion` on `gsp_ga10x.bin` also reads `615.78.08`. Build IDs: `gsp_tu10x` `4c2b93ff78c815828bdf2bb36cbf3b17c9f0e41b`; `gsp_ga10x` `bae8003ffd51fd740c5a1e4776d6e52e50582125` (`file` output). The GSP wrapper shape described in the r4u entry (`:39-41`) persists for `gsp_tu10x` (sections read here); `gsp_ga10x` is likewise REL RISC-V with `.fwversion` `615.78.08`, but its sections were not re-read in this probe. The bytes and the version string differ from 610.57.04.

The ucodes do **not** persist in kind. `struct.unpack('<8sII8s', d[:24])` (exit 0):

| file | magic | u32 #1 | u32 #2 | 8-byte tag | nonzero bytes / size |
|---|---|---:|---:|---|---|
| `ucodes_tu10x.bin` | `NVUCODES` | 1 | 496 | `2bae986bab90198d` | 7,188,666 / 8,837,632 |
| `ucodes_ga10x.bin` | `NVUCODES` | 1 | 1,293 | `a603b7cdfebe382d` | 52,962,356 / 58,215,936 |

The historical r4u candidate "both `ucodes_*.bin` are STUB containers — 24 nonzero bytes … then zero-padding to EOF" (`corpus/knowledge/2026-10-13-r4u-01-firmware-deep.md:23-26`) is true only of the 610.57.04 bytes. The current files carry large payloads: first dense 8 KiB window at offset 139,264 (0.996 nonzero, 7.975 bits/byte Shannon entropy); the first 4,096 bytes are sparse (entropy 0.313). [OBS for counts/entropy; INF that the density change makes the old "correct empty" reasoning inapplicable to 615.]

### F3 — The signal lane's current evidence already separates three carrier classes (OBS, from retained wave records)

| evidence | subject | subject sha256 | envelope | exit | result shape |
|---|---|---|---|---:|---|
| `evidence/c1/decode-uart-hi.run.json` | `uart-hi.bin` (2,500 B) | `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727` | `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` | 0 | 2 lines: `300-1100 uart-1: 48`, `1300-2100 uart-1: 69` |
| `evidence/c1/decode-official-uart.run.json` | `hello_world_8n1_9600.sr` (58,381 B) | `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61` | `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` | 0 | 12,885 lines; starts `108-628 uart-1: BA` … `0D`, `0A`, `48 65 6C 6C 6F 20` (`\r\nHello `) |
| `evidence/c1/inventory.run.json` | `tools/sigrok-cli.sh` | `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902` | `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` | 0 | 110 examined / 110 matching / 110 returned, `has_more:false` |
| `evidence/c1/decode-invalid-decoder.run.json` | `uart-hi.bin` | same as row 1 | none (`execution_failure`) | 1 | stderr `ImportError: … No module named 'round23_nonexistent_decoder'` |

All three successful normalized results carry the literal `hardware_acquisition: "not-performed"` (envelope key; schema literal at `dist/domain/signals/signalRecording.js:99`). Each successful run record sets `env_overrides.REA_SIGROK_COMMAND` to the lane wrapper `tools/sigrok-cli.sh`; this seat's shell has no such variable (probe P5), which is why its own verb attempts refused (P6/P7) rather than reproducing the sibling runs. The synthetic carrier's generator record (`evidence/c1/generate-uart.run.json`) states `"acquisition": "synthetic; no hardware"`, size 2,500, samplerate 960,000 Hz, baud 9,600, 100 samples/bit, payload hex `4869` (`Hi`).

The official fixture is a **third-party device capture**, not ours: `evidence/c1/official-download.json` records URL `https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad0528648ba58ceddbda9e34e4dfcd293a6b0/uart/hello_world/8n1/hello_world_8n1_9600.sr`, HTTP 200, sha256 `01b72610…`, captured `2026-10-21T14:38:57Z`. The pinned README (retained at `evidence/sources/uart-README.txt:1-26`) says the sender is an Olimex STM32-H103 (STM32 USART1.TX, libopencm3 example), the analyzer a ChronoVu LA8 at 625 kHz for 9,600 baud, probe 0 = TX, payload "Hello World!\r\n" (one direction). `SignalCarrierAlternatives.md:16-19` pins the release tag `sigrok-dumps-0.1.0` → commit `c8fad052…` (2012-05-18).

The invalid-decoder probe is a **producer failure**, not a held verb and not a capability refusal; it is correctly retained with stderr and exit 1.

### F4 — The byte→sample mapping is caller-chosen; a decode is a function of settings, not of the source bytes (OBS source)

Official `binary` input module: `https://sigrok.org/wiki/File_format:Binary` (oldid 13665, last edited 2018-09-17, fetched 2026-10-21) documents only two options — `numchannels` (default 8) and `samplerate` (default 0) — for "Raw binary logic data". libsigrok at tag `libsigrok-0.5.2` (`src/input/binary.c`, fetched 2026-10-21): `:33-34` defaults 8 / 0; `:48` reads `numchannels`; `:60` names channels `"%d"` (0,1,…); `:64` `unitsize = (channels + 7) / 8`; `:175` module id `"binary"`. There is no header, magic, or embedded sample-rate declaration: the file is raw bytes and the packing is whatever the caller passed.

REA 6.5.0 `dist/signals/SigrokRecordingProvider.js` (sha256 `7979bafb84b463d0fc3040d3643e08362326d67fd4543ee690679dc88b2dced7`) passes the caller string verbatim as `--input-format=<value>` (`:193-198`), requires `decoders` (schema `dist/domain/signals/signalRecording.js:12`), and binds the Evidence subject to the recording file's path + sha256 (`signalRecording.js:58-63`; service cross-check `dist/application/signals/SignalRecordingService.js:39-43`). Limits: 32 MiB input (`dist/process/LinuxResourceLimits.js:11`), 4 MiB combined output (`:12`), 30 s wall (`:13`), 1 GiB address space, 64 MiB per file, 30 CPU s (`:14-16`); over-limit files are a typed `limit` failure and symlinks are rejected (`dist/artifacts/readStableArtifact.js:33,35`). Autodetection is used only when `input_format` is null (`SigrokRecordingProvider.js:196-198`).

Consequence [INF]: for a headerless byte source, `numchannels` alone changes the sample stream (1 channel = 8 one-bit samples per byte; 8 channels = 1 eight-channel sample per byte), and `samplerate` changes samples-per-bit at a fixed baud. Neither parameter is a property of the source. REA's own limitation says annotations are "the selected decoder's interpretation of the recorded samples and caller-selected settings, not independently verified protocol semantics. Empty output does not establish absence of traffic." (`SigrokRecordingProvider.js:229`).

### F5 — The decode Evidence's tool identity stops at the wrapper, not the decoder binaries (OBS)

The successful inventory envelope's `normalized_result.tool` is `{configured_path: .ufo/waves/round-23/tools/sigrok-cli.sh, path: same, sha256: 50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902, version_banner: "sigrok-cli 0.7.2 …"}`. The wrapper (`tools/sigrok-cli.sh:1-15`) is a bash script that sets `LD_LIBRARY_PATH`/`LD_PRELOAD`/`PYTHONPATH`/`SIGROKDECODE_DIR` and `exec`s `runtime/squashfs-root/usr/bin/sigrok-cli`. Bytes outside the envelope (observed by `sha256sum`, exit 0):

| component | bytes | sha256 |
|---|---:|---|
| AppImage `~/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` | 49,558,848 | `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` |
| extracted `runtime/squashfs-root/usr/bin/sigrok-cli` | — | `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd` |
| `runtime/squashfs-root/usr/lib/libsigrok.so.4.1.1` | — | `0861b03cb9755fb5b94f6fb44e7334f7acb775bd03579397dbbaf5183b05df3f` |
| `runtime/squashfs-root/usr/lib/libsigrokdecode.so.4` | — | `4bfe11a3b76fee2c6847a9638fff82f1b8078ed56d8a9b182f78cba0f28b80b3` |

The AppImage digest equals `setup-sigrok.py:14`'s `EXPECTED` gate [OBS text]; the extraction step was not re-run here [UNK for byte-level derivation, but the digest gate and the extracted files are both retained]. The version banner reports libsigrok 0.5.2 and libsigrokdecode 0.5.3 with Python 3.5.2; the same banner lists SCPI backends TCP/RPC/serial/USBTMC and libusb/libserialport — capabilities, not contact; the adapter ran `--dont-scan` and file/list operations only (`SigrokRecordingProvider.js:166,192-198`). [INF: the envelope's tool hash is a wrapper identity; decoder-binary identity requires the ledger in the proposal.]

### F6 — The current GSP images do not carry a printable UART protocol token (OBS, bounded)

`grep -a -o -i -E 'uart|16550|baudrate|ns16550|serial'` (exit 0) over all four 615 blobs, followed by `strings -n 5 | grep -i -E 'uart|serial'` (exit 0): the 14 case-insensitive `uart` substrings in each `gsp_*.bin` resolve to `RmVgpcSkylineQuarter*` / `RmVgpcSkylineMiniQuarter*` tokens; the `serial` hits resolve to `serialNumber`, `id-at-serialNumber`, `Serial number`, `OverdrivePanelSerialNo0`, `OverDriveDataSerialNo0`. No `16550`, `ns16550`, or `baudrate` token appears in any of the four. Both `ucodes_*.bin` produce no matches.

Bounded reading: this is a printable-token scan of non-compressed regions; it does not cover the high-entropy `.fwimage` interior and absence of a token is not absence of a UART. It is enough to falsify any claim that *these bytes as packaged* name a UART protocol.

## Contradictions (stated, not smoothed)

1. **Semantic vs byte join.** A logic recording is time-sampled bus data; a firmware image is code/data bytes. The only shared representation is "bytes the caller may interpret as samples". A decode over firmware bytes (if one is ever run) is a statement about the caller's packing, samplerate, and decoder settings — not about firmware I/O. This is exactly the bleed vector `CriticScope.md:126-128` flags; it is not resolved by the decode succeeding.
2. **Current vs historical firmware identity.** The corpus's 610.57.04 rows are true of the cached archive and false of the installed path (F1). The r4u producer envelopes are gone. Any new knowledge entry that cites the r4u IDs as *current* firmware observations, or that reuses the "ucodes are stubs" conclusion for 615, would be wrong on the bytes (F2).
3. **Tool identity vs version banner.** The Evidence's `tool.sha256` covers a lane-authored bash wrapper, not the AppImage, `sigrok-cli`, `libsigrok`, or `libsigrokdecode` (F5). A claim that "the decode tool is sigrok-cli 0.7.2" is supported by producer text, not by the subject hash. This is a calibration gap, not a failure: the wrapper is deterministic and its exec target is a fixed path.
4. **Source relevance.** Under `claims.json:28`, a new source must be cited with exact used-by and must be relevant. A sigrok format/tool source can source the decode verb; a firmware package source cannot (citing it as the decode's used-by would trip the `new source relevance or ownership unsupported` falsifier). The firmware identity belongs in a separate scope stanza, never in the decode envelope's used-by.
5. **Three senses of "firmware".** (a) NVIDIA vendor firmware images — the lane's firmware surface (`PROVINCE.md:123`); (b) device firmware bundled inside the sigrok AppImage — 21 files per `AppImageLibraries.md:20`, tool payload, [single-witness OBS]; (c) the round's phrase "current firmware blob scope" — sense (a). The official `.sr` fixture's README also names STM32 *firmware* (libopencm3 example): a fourth, source-device sense that is not a target. Equivocating these would silently import claims.

## Proposed move (one, bounded, not performed here)

**A carrier-provenance ledger entry keyed by the firmware package archive digest, plus exactly one firmware-slice negative control.** This is a compatible synthesis of the round's existing proposals: `SignalRawFormat` supplies the headerless `binary` format options; `SchemaSignalDecode` supplies the exact arg mapping; `SignalCarrierAlternatives` supplies the third-party device capture; `BuildSignalRunner` supplies the regenerable synthetic positive; `AppImageLibraries`/`SigrokOverride` supply the tool chain; the firmware surface supplies the static byte source.

Ledger entry (a lane artifact under `round-23/evidence/c1/`, not an REA schema field):

```json
{
  "carrier_class": "lane-derived-from-static-blob",
  "package": {"name": "nvidia-utils", "version": "615.78.08-1", "repo": "extra",
               "archive_sha256": "c437ec64cfd4cfba5b8f51641553ec283ec111e14471f4f3a8927c2e3aee8673"},
  "member": {"path": "/usr/lib/firmware/nvidia/615.78.08/ucodes_tu10x.bin",
              "sha256": "6027ab3736f733b5a06e6e61aaae957d1f990426a263849ebcfa8a49eeb4a5d0",
              "bytes": 8837632},
  "slice": {"offset": 139264, "length": 8192,
             "sha256": "f8f3e4c9343ff7b0519e8c893c8d0a689ded457fa6290b93ec6a3b31a339949e"},
  "input_format": "binary:numchannels=1:samplerate=960000",
  "decoders": "uart:rx=0:baudrate=9600",
  "annotations": "uart=rx-data",
  "rea_envelope": "<evidence_id>",
  "tool_chain": {"wrapper_sha256": "50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902",
                  "appimage_sha256": "49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614",
                  "sigrok_cli_sha256": "10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd"},
  "hardware_acquisition": "not-performed"
}
```

The slice is the first dense 8 KiB window of `ucodes_tu10x.bin` (0.996 nonzero, 7.975 bits/byte): a worst-case byte source chosen for its lack of printable structure, not a protocol sample. It is not executed, mapped, or loaded; only its bytes are copied into a regular recording file (REA rejects symlinks and caps input at 32 MiB, so the 58 MB `ucodes_ga10x.bin` cannot be used whole).

The control: decode that one slice twice with the existing wrapper, identical in every argument except samplerate —

1. `--input_format binary:numchannels=1:samplerate=960000 --decoders uart:rx=0:baudrate=9600 --annotations uart=rx-data --all_lines`
2. `--input_format binary:numchannels=1:samplerate=1920000 --decoders uart:rx=0:baudrate=9600 --annotations uart=rx-data --all_lines`

Both rates give integer samples-per-bit at 9,600 baud (100 and 200). The falsifier: the *same bytes* under a changed packing rate must not yield the same decoded message; if annotations differ (or one side is empty), the message is a function of caller settings, not of the firmware. If they are identical, that is itself a finding about the decoder's treatment of samplerate and must be retained, not smoothed.

What the move does and does not do:
- Improves **depth** (a carrier-class/provenance record and a worst-case control for the held decode verb) and **calibration** (the settings-dependence falsifier plus the durable package key).
- Does **not** change coverage: it is the same `decode-signal-recording` verb, so it must be counted once. If L1 reaches k=2 via `inspect-signal-decoders`, that verb's evidence stands on its own envelope; this control does not add to it.
- Does **not** claim the firmware contains or lacks UART, does **not** execute the blob, does **not** acquire hardware, and does **not** touch the sibling-owned wrapper/runtime beyond citing their digests.
- Is non-obvious because the naive bridge ("decode the blob to learn its protocol") is replaced by a *negative* control; the join is byte derivation plus a package digest, not semantics, and it survives the next `nvidia-utils` upgrade that already erased the 610 path.

## Open risks

1. **Empty/decoder-error control.** The slice may yield no annotations or a decoder error. Both are legitimate outcomes; retain them verbatim and do not convert them into "no UART in firmware" (F6 bound; REA limitation `:229`).
2. **Slice arbitrariness.** A different offset/length yields different annotations. The ledger records offset/length/sha and labels the choice illustrative; it is not a survey of the blob.
3. **Output cap.** A noisy decode can exceed the 4 MiB combined output and fail with `output_bytes`; reduce the slice to 2 KiB or filter annotations, and retain the failure if it happens.
4. **Runtime fragility.** The banner reports Python 3.5.2 and the inventory already shows `srd: SyntaxError … signature/pd.py:138`; other old decoders may fail. The `binary` module itself is in libsigrok 0.5.2 [INF from source + banner], but a failure must be retained as a typed refusal, not substituted.
5. **Tool-chain drift.** If the wrapper, AppImage, or runtime changes, the digests in the ledger are stale. Regenerate the chain; never reuse a stale ledger entry silently. The envelope alone will not reveal the change (F5).
6. **Cache pruning.** `pacman -Sc` would destroy the 610 reproducibility. The 615 archive digest is recorded now; its cache copy is not guaranteed either.
7. **Source-relevance tripwire.** If the firmware stanza is spliced into the decode evidence's used-by, the counter's "new source relevance" falsifier may fire. Keep the firmware identity in the scope stanza (or a separate corpus entry), and cite only sigrok/REA sources for the decode verb.
8. **Equivocation.** "Firmware" in the AppImage (21 bundled files) and in the STM32 fixture README is not the NVIDIA blob scope. Do not let a future entry import one as the other.
9. **Historical evidence custody.** The r4u envelopes are gone; only the staging text and `PROVINCE.md:123` remain. The cached 610 archive reproduces the bytes but not the provider observations. Do not describe the old IDs as re-verified.

## Verification (for L1; not run by this seat, and not claimed verified)

Static identity:

```bash
sha256sum /usr/lib/firmware/nvidia/615.78.08/*.bin            # four digests as in F1
pacman -Qo /usr/lib/firmware/nvidia/615.78.08/*.bin          # nvidia-utils 615.78.08-1
sha256sum /var/cache/pacman/pkg/nvidia-utils-615.78.08-1-x86_64.pkg.tar.zst
for f in gsp_ga10x.bin gsp_tu10x.bin ucodes_ga10x.bin ucodes_tu10x.bin; do
  tar --zstd -xOf /var/cache/pacman/pkg/nvidia-utils-615.78.08-1-x86_64.pkg.tar.zst \
    "usr/lib/firmware/nvidia/615.78.08/$f" | sha256sum
done
readelf -h -S -W -x .fwversion /usr/lib/firmware/nvidia/615.78.08/gsp_tu10x.bin
```

Negative control (proposed; requires a regular slice file under `round-23/evidence/c1/` with sha256 `f8f3e4…`, and the existing wrapper):

```bash
REA_SIGROK_COMMAND=<repo>/.ufo/waves/round-23/tools/sigrok-cli.sh \
npx -y rea-agents@6.5.0 decode-signal-recording <slice> \
  --input_format binary:numchannels=1:samplerate=960000 \
  --decoders 'uart:rx=0:baudrate=9600' --annotations uart=rx-data \
  --all_lines --format json --full-output
```

Assert for each run: `exit == 0` (or a retained typed refusal, never a silent substitution); `data.normalized_result.artifact.sha256 == f8f3e4…`; `hardware_acquisition == "not-performed"`; `tool.version_banner` starts `sigrok-cli 0.7.2`; compare the two `annotations_text` values. Re-run with `samplerate=1920000` and compare. Do not compare against the synthetic `uart-hi.bin` message as if it were the same carrier.

Counter: neither control run changes k. If the round counts `inspect-signal-decoders` and `decode-signal-recording`, verify each against its own original envelope and its own subject hash (`inventory` → wrapper `50fe43…`; decode → recording sha). The firmware ledger is not a counter input.

## Probes retained

| # | argv (env noted) | exit | captured |
|---|---|---:|---|
| P1 | `npx -y rea-agents@6.5.0 decode-signal-recording --help` | 0 | usage: `<path>`, options `--decoders`, `--input_format`, `--annotations`, `--line_offset`, `--line_limit`, `--all_lines` |
| P2 | `npx -y rea-agents@6.5.0 decode-signal-recording --schema` | 0 | required `decoders`; `input_format` string-or-null default null; `additionalProperties:false` |
| P3 | `npx -y rea-agents@6.5.0 inspect-signal-decoders --help` | 0 | `--decoder`, `--query`, `--offset`, `--limit`, `--all` |
| P4 | `npx -y rea-agents@6.5.0 inspect-signal-decoders --schema` | 0 | decoder pattern `^[a-zA-Z0-9_+\x2d]+$`; max 256 |
| P5 | `env | grep -E '^REA_'` | 0 | 7 `REA_*` vars; **no** `REA_SIGROK_COMMAND`; includes `REA_BINWALK_COMMAND=/usr/bin/binwalk`, `REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob` |
| P6 | `npx -y rea-agents@6.5.0 inspect-signal-decoders --format json --full-output` (no env override) | 1 | stdout `capability_unavailable` / `unsupported_provider`; message demands absolute `REA_SIGROK_COMMAND`; stderr empty |
| P7 | `npx -y rea-agents@6.5.0 decode-signal-recording /usr/lib/firmware/nvidia/615.78.08/ucodes_tu10x.bin --decoders uart:rx=0:baudrate=9600 --input_format binary:numchannels=1:samplerate=1000000 --format json --full-output` (no env override) | 1 | same typed refusal before any artifact read; stderr empty. **Refusal; does not count** |
| P8 | `sha256sum /usr/lib/firmware/nvidia/615.78.08/*` | 0 | four digests (F1) |
| P9 | `stat -c '%n %s' /usr/lib/firmware/nvidia/615.78.08/*` | 0 | sizes (F1) |
| P10 | `pacman -Qo /usr/lib/firmware/nvidia/615.78.08/*.bin` | 0 | `nvidia-utils 615.78.08-1` for each |
| P11 | `pacman -Qi nvidia-utils`; `pacman -Si nvidia-utils` | 0 | version, repo `extra`, build/install dates |
| P12 | `tar --zstd -xOf <615 pkg> <member> \| sha256sum` ×4 | 0 | digests equal installed members |
| P13 | `tar --zstd -xOf <610 pkg> <member> \| sha256sum` ×4 | 0 | digests equal r4u corpus rows |
| P14 | `ls -d /usr/lib/firmware/nvidia/610*` | 2 | `No such file or directory` |
| P15 | `ls /tmp/r4u-*` | 2 | no historical envelopes |
| P16 | `file`, `readelf -h/-SW/-x`, `xxd`, `strings`, `grep -a -o` on the 615 blobs | 0 | F2/F6 |
| P17 | `find /usr/lib/firmware/nvidia -type f \| wc -l`; `pacman -Qo` spot check | 0 | 276 files total; 4 `nvidia-utils` 615.78.08; `ga102/gsp` spot check `linux-firmware-nvidia` (not all 272 individually owned) |
| P18 | `sha256sum` on AppImage, wrapper, runtime `sigrok-cli`, libsiglrok/libsigrokdecode | 0 | F5 digests |
| P19 | `curl -fsSL https://raw.githubusercontent.com/sigrokproject/libsigrok/libsigrok-0.5.2/src/input/binary.c \| grep -n …` | 0 | line anchors in F4 |
| P20 | `python3` (inline, read-only) slice digests/nonzero/entropy | 0 | F2, proposal slice `f8f3e4…` |
| P21 | `sha256sum evidence/c1/{uart-hi.bin,hello_world_8n1_9600.sr,*.envelope.json}` | 0 | F3 digests |

External reads (no target contact): `https://sigrok.org/wiki/File_format:Binary` (oldid 13665, last edited 2018-09-17; fetched 2026-10-21), `https://raw.githubusercontent.com/sigrokproject/libsigrok/libsigrok-0.5.2/src/input/binary.c` (fetched 2026-10-21). `https://man.archlinux.org/man/sigrok-cli.1.en` and `https://archlinux.org/packages/extra/x86_64/nvidia-utils/` both failed with ECONNRESET from this host; package facts were taken from the local pacman database/package archive instead. That fetch failure is retained, not papered over.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ConnectSignalFirmware.md` — this report. Its sha256 is reported in the seat's completion message (self-reference excluded).

No other file was created or edited. No sandbox clone was made (read/connector seat; all outputs are in this report).

## Installs

None. No tool was installed, upgraded, or configured. `binwalk 3.1.0` and `unblob 26.6.4` were already present and are only reported; `sigrok-cli 0.7.2` exists as the AppImage/wrapper already created by sibling seats and was not launched by this seat. No pacman transaction was attempted (host-wide pause respected).
