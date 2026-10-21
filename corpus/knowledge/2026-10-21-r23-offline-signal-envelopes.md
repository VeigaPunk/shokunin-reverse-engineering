source: S058 sigrok-cli0.7.2 manual; S059 sigrok-dumps c8fad0528648ba58ceddbda9e34e4dfcd293a6b0 UART README; S060 original REA6.5.0 envelopes in .ufo/waves/round-23/evidence/c1/
verified-at: 2026-10-21, round23; exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files
recheck: python3 -I -B .ufo/waves/round-23/tools/describe-signals.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <MEASURED-COMMIT>; real replay uses the retained run argv and explicit REA_SIGROK_COMMAND after reproducing the pinned extraction

# Offline signal REA envelopes, not hardware ownership

Coverage-map ground: offline recording envelopes and decoder discovery, added in
round23. This entry holds two REA verbs within the frozen six-verb T1 list; it
claims neither general signal-analysis expertise nor hardware acquisition.

## Discovery is a tool-subject observation

**Observation:** REA6.5.0 `inspect-signal-decoders --all` returned original
success envelope `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`,
`ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0`,
operation `inspect_signal_decoders`. The subject is the launcher, not a recording.
Its output window reports110 examined/matching/returned decoder records and
`has_more:false`; the field count and counting command are retained by the
`recheck:` producer. This is installed catalog discovery only, not device
scan results or110 independently verified decoders.
The diagnostics explicitly report a `signature` decoder load failure:
Python3.5.2 rejects an underscore-separated binary numeric literal at its
`pd.py:138`. That module is excluded from the returned catalog; an exhausted
window does not mean every installed module loaded or every decoder works.
UART help/selected decoding succeed separately. No repair of the unrelated
signature decoder or warning suppression is claimed.

The separate UART help envelope
`.ufo/waves/round-23/evidence/c1/uart-help.envelope.json` retains the selected
installed module's literal help. RX is optional because TX is another supported
direction; at least one actual direction is still required. `rx-data` selects
one annotation class, not an assertion that every frame is losslessly recovered.
The returned Python-prefix diagnostics remain visible; exit0 did not erase them.

## Exact synthetic round trip

**Observation:** `.ufo/waves/round-23/tools/make-uart.py` generates the committed
`.ufo/waves/round-23/evidence/c1/uart-hi.bin`: SHA256
`4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`.
This is an inert synthetic recording, not data acquired from any device.
It places channel0 in bit0,100 samples per bit at960000Hz, baud9600, one start,
eight LSB-first data and one stop bit. Payload is ASCII Hi (`4869`). Exact bits,
size and generator argv/output are retained in `generate-uart.run.json`.

REA `decode-signal-recording` used explicit
`--input_format binary:numchannels=1:samplerate=960000`,
`--decoders uart:rx=0:baudrate=9600`, `--annotations uart=rx-data`, `--all_lines`.
Original envelope:
`.ufo/waves/round-23/evidence/c1/decode-uart-hi.envelope.json`,
`ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e`,
operation `decode_signal_recording`. The literal output is:

```text
300-1100 uart-1: 48
1300-2100 uart-1: 69
```

**Inference:** those two producer annotations agree with the planted payload
under the declared settings. They are sample ranges and displayed hex bytes,
not timestamps, source code, execution of a device or proof of every UART mode.

## Selected third-party acquired recording

The public version-pinned source is
https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad0528648ba58ceddbda9e34e4dfcd293a6b0/uart/hello_world/8n1/hello_world_8n1_9600.sr .
Committed copy `.ufo/waves/round-23/evidence/c1/hello_world_8n1_9600.sr` has
SHA256 `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`;
HTTP200/size/digest receipt is `official-download.json`. S059's author describes
one-way UART from an Olimex board,625kHz at9600baud and TX channel. That is
**source attribution**, not this lane observing that board or its acquisition.

**Observation:** the exact `uart:rx=TX:baudrate=9600` request, with
`uart=rx-data`, succeeded. Original envelope
`.ufo/waves/round-23/evidence/c1/decode-official-uart.envelope.json`,
`ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c`,
operation `decode_signal_recording`, retains12885 literal display lines with
`has_more:false` (same recheck producer). Initial annotations are BA,BD,C9,B1,
91,85,0D,0A; the first matching Hello World sequence begins at sample5512.
Thus the entire output is **not** described as a lossless Hello World payload.
The initial `predictions.json` expected textual Hello World; output is hex
annotation text, so that literal-string prediction is not met. Decoding and
inferred interpretation are distinct; no false-clean prediction is claimed.

The invalid-decoder control is an actual `execution_failure`, exit1, in
`.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.envelope.json`.
It is a rejected held witness, never a third held verb or an absent-provider
claim. The current upstream guide's newer `invalid_request` description is not
substituted for this6.5.0 observation.

## Tool identity, resource and scope boundaries

The local official-release AppImage SHA256 is
`49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614`.
The exercised extraction command and output are in `sigrok-extraction.json`;
`tools/setup-sigrok.py` is the explicit digest-checking reproduction recipe,
not a claim that this wrapper script itself was exercised during extraction.
`tools/sigrok-cli.sh` selects bundled libraries/Python modules but preloads the
host's matching libgmodule to avoid the old bundled gmodule/new host gio mismatch.
No host package transaction or global configuration was changed.

The original envelopes' `tool.sha256` identifies the **launcher**, SHA256
`50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902`,
not the complete installation. Separate `tool-runtime-pins.json` identifies
selected actual executable/library/module files at one instant, including
sigrok-cli ELF SHA256
`10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd`.
The banner reports sigrok-cli0.7.2, libsigrok0.5.2, libsigrokdecode0.5.3 and
Python3.5.2; decoder modules/libraries remain trusted, not fully authenticated.
Generated `.pyc` files mean the extracted runtime is not a pristine tree.

The provider records prlimit ceilings1GiB address space,64MiB file size,
30CPU seconds and no core dumps, plus a30s command deadline and4MiB output cap.
Those are declared/measured provider settings, not an OS sandbox or aggregate
quota. `hardware_acquisition:not-performed` is a provider declaration; no
independent syscall/device-contact monitor was run. No target/device execution,
attach, hardware acquisition or debugger ownership is claimed or credited.
Dart parsing and both debugger verbs remain unheld; prior R22 identify remains
one verb regardless of how many success envelopes cite it.

## Round-23 W2 correction — source attribution and current holding

This dated correction supersedes only the statements named here; original
envelopes, predictions and earlier committed prose are retained.

- The final paragraph's “Dart parsing … remain unheld” statement predates
  the independently retained four-symbol Saber result. It is superseded by
  `2026-10-21-r23-dart-legacy-layout-boundary.md`: inspect-dart-aot is now held
  on that exact selected x86_64 carrier, not generally. Both debugger verbs
  remain unheld/Adjacent.
- S062 supersedes S058's overly broad sampling-attribution wording.
  `samplerate=960000` is explicit only in the synthetic binary call. The
  public `.sr` call has input_format:null and uses its recording metadata;
  decoder/channel selections are explicit in both. This does not change
  any observed result or interpret the manual as REA output authority.
- The sentence “at least one actual direction is still required” was not
  established by the retained help alone (which lists required channels:
  none). Withdraw that global assertion here; only the selected RX settings
  were exercised. No universal channel-validation rule is admitted.
- Host glib/gio/gobject/libusb/expat resolve outside the extracted bundle.
  The one-instant manifest pins selected gmodule/glib/gio files, not host
  gobject/libusb/expat. Those other host dependencies remain unpinned; the
  banner is version text, not complete dependency attestation or isolation.
- The otherwise-unlocated “current upstream guide” sentence refers to
  https://raw.githubusercontent.com/morluto/rea/main/docs/signal-recordings.md .
  Retained lead copy `evidence/sources/rea-signal-guide-main.md` and
  `guide-fetch.json` under round23 record a new same-round access and SHA256
  `8997ec52c2f432bb1722aa1d3a27301a4e4c6c0553bb7bbbcb75b6ed59765fa9`.
  It is unversioned main, excluded as6.5.0 authority, not a source row or
  grounds to rewrite the actual execution_failure.

The original acquisition/non-contact labels remain provider declarations;
no independent monitor or full hardware-isolation proof was added.

Further W2 precision: the raw carrier contains no absolute sampling-rate
metadata;960000Hz is a **caller-declared interpretation**, while the pinned
bytes establish100 samples per planted bit. The provenance header's
“environment” means retained explicit env_overrides only; ambient environment
was not captured. The reported prlimit arguments/limits are requested or
provider-declared values, not a retained kernel readback of effective ceilings.
Accordingly, the earlier “declared/measured provider settings” wording is
superseded on “measured”; no stronger enforcement claim is made.

W2 PredictionHonesty also records tail truncation and an annotation-range
overhang in the public recording output. Their causes remain unknown; the
entry's non-lossless qualification applies to both the leading and trailing
anomalies. No absent-traffic, complete-frame or acquisition claim follows.

The requested `uart=rx-data` annotation filter excludes warning classes.
W2 OriginalPublic's retained independent bit-analysis program/output under
`.ufo/waves/round-23/w2/retained-runs/OriginalPublic/` reports leading framing errors and an
incomplete trailing frame. This is separate source analysis, not a new REA
run or a proof that every data annotation is a valid framed byte. The
admitted result remains the selected literal annotation view. Producer
warnings outside that requested class are not “parsed-and-empty”.

**Current source authority:** S062 replaces S058's attribution wording;
S059 supplies the dataset author's provenance and S060 supplies the original
local observations. The original source header is retained as historical
provenance under the append-only correction rule. Semantic admission follows
this explicit supersession, not the counter's lexical first-line eligibility.
