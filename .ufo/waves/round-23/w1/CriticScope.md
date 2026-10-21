# CriticScope — R23-C1 offline signal coverage: domain bleed and protocol decoding vs device control

Seat `KaidokuR23.CriticScope` (critic, read-only, author-side; not outside verification).
Frozen claim: `.ufo/waves/round-23/claims.json` (R23-C1, T1 includes `inspect-signal-decoders`
and `decode-signal-recording`). Lane HEAD read: `a3c92eb6bc70984e90ae5b895412de978840b2c5`.
No REA producer, debugger, Frida, attach, device, carrier or AppImage execution was run by this
seat. No build/test/lint.

Axes judged: coverage (R23-C1); calibration and depth only as harm checks.

## Verdict

**The device-control falsifier fails; the domain-bleed falsifier partly holds and needs a
wording correction.** It is not a reason for the canonical judge to reject the claim.

- **Device control:** REA 6.5.0's argument vectors cannot reach sigrok-cli 0.7.2's hardware
  scan or acquisition paths. Protocol decoding of a regular-file copy is structurally separate
  from device control. The residual gap is trust in the configured executable and the inherited
  environment, not the argv.
- **Domain bleed:** signal recordings are not named anywhere in MINT Core or Frontier, nor in
  QUALITY's domain line. A held REA *verb envelope* fits Core ("REA operation on this host").
  The claim becomes bleed only if the entry or PROVINCE presents it as held signal, hardware,
  UART or protocol-analysis ground.

## Finding 1 — REA argv never reaches device scan or acquisition (OBSERVED, source)

REA 6.5.0 is installed at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(`package.json` version 6.5.0). It builds exactly four argv shapes for sigrok:

- `dist/signals/SigrokRecordingProvider.js:139`, version gate: `["--version"]`.
- `:165`, catalog: `["--dont-scan", "--list-supported"]`.
- `:166`, one decoder's help: `["--dont-scan", "--protocol-decoders=<id>", "--show"]`.
- `:191-202`, decode:
  - `--dont-scan`
  - `--input-file=recording`
  - `--protocol-decoders=…`
  - `--protocol-decoder-samplenum`
  - optional `--input-format=…`
  - optional `--protocol-decoder-annotations=…`

The CLI bundle uses the same shapes: `dist/cli-runtime/cli.js:1319-1320,1352-1353` (sha256
`168cd322…e2204`).

- **No caller path to `-d`, `-c`, `--scan`, `--samples` or `--continuous`.**
  - The input schema `dist/domain/signals/signalRecording.js:10-34` is a `strictObject`
    containing only `path`, `decoders`, `input_format`, `annotations` and line paging.
  - Each selector becomes one argv element (`:4-9`: "single sigrok arguments, never shell
    fragments"; NUL rejected).
  - The CLI options are that schema minus `path` (`dist/cli/signalCommands.js:41-43`).
- **sigrok-cli 0.7.2 dispatch.** Source fetched 2026-10-21 from
  `https://raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/`. Branch order
  in `main.c:293-322`:
  - `opt_version` leads to `show_version`.
  - `opt_list_supported` leads to `show_supported`.
  - `opt_pds && opt_show` leads to `show_pd_detail` (`:310-311`).
  - `opt_input_file` without `--show` leads to `load_input_file(FALSE)` (`:315-316`).
  - Acquisition (`run_session`) is reached only through
    `opt_samples || opt_time || opt_frames || opt_continuous` (`:321-322`). REA can pass none of
    these.
- **Where scanning happens.** `device_scan()` (`device.c:31-64`) is called only from:
  - `main.c:169,214` (get/set options)
  - `session.c:732` (`run_session`)
  - `show.c:353,429` (device list and detail)

  None of these is on REA's four paths. `--dont-scan` (`device.c:43-45`; man page
  `doc/sigrok-cli.1:67-70`) is therefore a second barrier, not the only one.
- **Session (srzip) input binds the virtual session driver, not hardware.** libsigrok 0.5.2
  `src/session_file.c:177-184` sets `sdi->driver = &session_driver`. [INFERENCE] The AppImage's
  bundled libsigrok version is unconfirmed by this seat.
- **Device nodes and FIFOs are refused before sigrok runs.** `readStableArtifact.js:31-36` and
  `cli.js:327` require a regular non-symlink file. They open it `O_NOFOLLOW|O_NONBLOCK` and copy
  it into a private `recording` file (`SigrokRecordingProvider.js:184-189`). A `/dev/ttyUSB0`
  path cannot become `--input-file`. [INFERENCE from source; not executed.]
- **The catalog retains no hardware inventory.** `show.c:140` prints "Supported hardware
  drivers:" first, and protocol decoders come last (`:193`). The parser keeps only lines after
  "Supported protocol decoders:" (`parseDecoderDiscovery.js:19-33`). Driver names leave REA only
  inside `capturedOutput` on a failure. Listing a driver name is library metadata, not device
  contact.

**Counterexample tested: none found.** The strongest local construction was a decoder, format or
annotation string carrying `-d`/`--samples`. It fails: each is a single
`--protocol-decoders=` or `--input-format=` element (`signalRecording.js:4-9`; GLib string
option `options.c:134`).

## Finding 2 — `hardware_acquisition: "not-performed"` is a schema literal, not an observation (OBSERVED)

- `SigrokRecordingProvider.js:160` hard-codes it. `domain/signals/signalDecoders.js:51` and
  `signalRecording.js:99` type it as `z.literal("not-performed")`, so every success says this,
  whatever process actually ran.
- The tool is checked only for an absolute path, X_OK, sha256 capture and a version-banner regex
  (`/^sigrok-cli 0\.7\.2/` plus the substring `libsigrokdecode`, `:71-75,139-142`). A wrapper
  that prints that banner and then does anything else would still produce
  `"not-performed"`. [INFERENCE from source; not executed.]
- The child inherits the full host environment (`process/ProviderProcess.js:26-31`:
  `{...hostEnvironment, ...options.env}`). That includes `LD_LIBRARY_PATH` and
  `SIGROKDECODE_DIR`, and libsigrokdecode loads decoders from `SIGROKDECODE_DIR`
  (`round-23/w1/_uart/libsigrokdecode-0.5.3/srd.c:273`). Decoders are Python modules that REA
  states it trusts (`:231`).
- **False-provenance risk:** an entry that cites the field as observed "no hardware contact"
  overstates it. REA's own wording is "not requested" (`:178,231`).

**Impacted axes:** calibration (provenance grade), coverage (what "held" asserts).

## Finding 3 — domain placement: verb coverage is Core, signal analysis is undeclared (OBSERVED text, INFERENCE placement)

- MINT domain (`MINT.md:6-9`) and QUALITY's domain line (`corpus/QUALITY.md:3`) cover shipped
  artifacts, firmware images and recorded crashes. Neither mentions signal or logic recordings.
- MINT Core (`:30-32`) is "REA operation on this host — target routing, provider readiness …".
  MINT Frontier (`:34-36`) and Adjacent (`:38-39`) do not name signals either.
- `PROVINCE.md:217-218` (R22): "The sigrok verbs remain unexercised; no recording decode or
  hardware contact is claimed."
- **No sibling owner.** `rg -i -w` over `../*/MINT.md ../*/PROVINCE.md` excluding kaidoku found
  no match for `sigrok`, `logic analy[sz]er`, `pulseview`, `uart`, `i2c`, `hardware`,
  `embedded`, `electronics`, `oscilloscope` or `signal processing` (exit 0, empty output). This
  is not bleed into another lane. It would be an undeclared expansion of kaidoku's own province.
- A synthetic UART8N1 "Hi" carrier (BuildSignalRunner) or a sigrok-dumps fixture
  (SignalCarrierAlternatives) is not a shipped artifact. Synthesized carriers are an admitted
  precedent (QUALITY #10, #12; README "Synthesized carriers" row), but only as carriers for
  verbs.
- QUALITY rejection #5 (`QUALITY.md:52`) forbids "a recorded capture presented as live
  observation". Wording such as "device transmits Hi" or "UART traffic identified" would trip
  it. REA limits annotations to "the selected decoder's interpretation of the recorded samples
  and caller-selected settings" (`:229`). The baud rate, samplerate and channel count are
  caller-supplied on raw input, so a synthetic round-trip only shows that the envelope honours
  the caller's settings. It is not protocol recovery.
- **ConnectSignalFirmware bleed vector [INFERENCE].** Firmware Core covers image bytes (binwalk
  and unblob). A logic recording is a time-sampled bus capture. Treating a decode as firmware
  ground is bleed unless a recorded payload is itself shown to be firmware bytes, and none is.

## Finding 4 — inventory-only `inspect-signal-decoders` can raise k without any decode (OBSERVED source, INFERENCE count)

- The catalog path's subject is the sigrok executable itself:
  `subject: { path: command, sha256: tool.sha256, format: "file" }` (`SigrokRecordingProvider.js`,
  the `createAnalysisExecution` call that follows `:168-172`). No recording is read (`:178`).
- If k=2 is reached through `identify-flutter-build` plus this verb alone, "offline signal
  coverage" overstates it. What is held is provider-readiness and catalog inventory (Core:
  provider readiness), not signal decoding.

## Smallest safe corrections (for L1; this seat edits nothing)

1. **Entry and PROVINCE wording.** Use "REA verb envelope held on an offline regular-file
   carrier; protocol decoding only (sigrok `-i` path); hardware discovery, acquisition and device
   control not requested by argv (cite `SigrokRecordingProvider.js:165-166,191-202` and
   sigrok-cli `main.c:293-322`, `device.c:31-64`). No signal, hardware, UART or bus-analysis
   domain ownership is claimed."
2. **The `hardware_acquisition` field.** Cite it as "REA schema literal (declared)", never as an
   observation. Record the `tool.sha256` from the envelope and match it against the sha256 of the
   extracted official AppImage binary. Record every env override (`LD_LIBRARY_PATH`,
   `SIGROKDECODE_DIR`, `REA_SIGROK_*`) with the run.
3. **Per-verb scope.** Report each verb separately: `inspect-signal-decoders` = catalog/help
   inventory of the configured tool, and `decode-signal-recording` = decode of a named carrier.
   k must say which signal verb contributed.
4. **Carrier wording.** Label it synthetic (own-work, recipe and bytes retained) or third-party
   dump (cite URL and sha only). Make no acquisition or live-device statement, and say
   "decoder output under caller-selected settings".
5. **Province.** If any signal ground is to be named, add one append-only PROVINCE line placing
   offline decode of caller-supplied recordings as REA-verb Core coverage. Place hardware
   acquisition and device control as **Adjacent `(unowned)`**. Do not extend MINT Frontier
   implicitly.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CriticScope.md`: this
  report. sha256 is not self-computable in-file.

**Contract deviation (disclosed).** Upstream sources were fetched with `curl` into scratch
`/tmp/criticscope-r23/`, which is outside the round-23 tree. The directory was removed after
use. The fetched files can be reproduced from these URLs and sha256 values:

| file | URL | sha256 |
|---|---|---|
| sigrok-cli 0.7.2 `main.c` | `raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/main.c` | `941b65aee47d5c156f0aec8d331c0e374fc3f0c6d45fc50893243ebdfd294c48` |
| `show.c` | same tag, `/show.c` | `ae9d8c1ca9f05f3abfc7192a6cc02ae93ff15e77185ae8c43bc1e8544244ac9f` |
| `device.c` | same tag, `/device.c` | `33f0269a8edc2c5d6e35952bb05cc5b085964480b7b03f4a04e54254bad3b563` |
| `options.c` | same tag, `/options.c` | `a063e09d9511ffcd0aa061088ebbd700a59cacf9d7d17d4dffd7f756cdc3bf3b` |
| `input.c` | same tag, `/input.c` | `894aa07fc2ce29e9fed159c459060915aa83c8e1528621a4b67910782691dc5d` |
| `session.c` | same tag, `/session.c` | `b25e05e37ce2e4684c3e5866f819413ce1f9c794b75054bc8cf7f919a9216d70` |
| `doc/sigrok-cli.1` | same tag | `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9` |
| libsigrok 0.5.2 `src/session_file.c` | `raw.githubusercontent.com/sigrokproject/libsigrok/libsigrok-0.5.2/src/session_file.c` | `c1a9de46f71f4f9ec8792cbf13320269afddfc54af24008083b7296c25c45495` |

Local REA 6.5.0 files cited:

| file | sha256 |
|---|---|
| `SigrokRecordingProvider.js` | `7979bafb…2dced7` |
| `parseDecoderDiscovery.js` | `2fa74a0b…69097e` |
| `signalRecording.js` | `0ef15149…040171` |
| `signalDecoders.js` | `cb052ebc…0040d5` |
| `ProviderProcess.js` | `cb5e0869…14ae4` |
| `readStableArtifact.js` | `06a23746…2d2707` |
| `signalCommands.js` | `f033461c…1b3eef` |

The AppImage at `/home/vgpnk/.local/opt/sigrok-cli-0.7.2-x86_64.AppImage` was hashed only and
matches the expected value: `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`.

## Installs

None.

## Open risks

- Findings 1, 2 and 4 come from reading source. No REA signal run was observed by this seat,
  because the provider launch is BuildSigrok's job.
- Whether the AppImage's bundled libsigrok and libsigrokdecode match the 0.5.2 and 0.5.3 sources
  cited here is UNKNOWN.
- A peer's decoder-dir or `LD_LIBRARY_PATH` workaround would change what runs under the same
  `tool.sha256`. Only recorded env overrides can bound this.
- Dynamic-debugger ownership (gdb/rizin) stays Adjacent and unresolved and is untouched here.
