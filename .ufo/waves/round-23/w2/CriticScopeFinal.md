# CriticScopeFinal — R23-C1 target/hardware/debugger claim falsification

Seat: `KaidokuR23.CriticScopeFinal`, a leaf, source-review-only seat.
Candidate `C=2838351450ff1ee4baa620c962a1153450d53311`, baseline `B=aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Every byte below was read with `git show C:PATH` (no worktree reads). I did not contact a device, run a producer, run a counter or any test, or execute any target.
The only local computations were `jq`/`grep`/`sha256sum`/`unzip -l|-p` over committed blobs, plus an inline re-derivation of the `make-uart.py` bit list, run through `python3 -I -B -c` (it writes nothing).

Scope: the target, hardware and debugger claims in the committed `PROVINCE.md` §Round-23, `SKILL.md` §round 23, `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`, `corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md`, `corpus/SOURCES.md` S058–S061, and `corpus/lessons/round-23.md`.

## Verdict

No counterexample reduces the coverage count. I found no rejecting defect. There are four fixable calibration/depth defects (F1–F4) and one advisory (A1).
The debugger claims hold: no debugger verb is held, and none can be held at C.

## Findings

### Claims confirmed against recorded bytes (observed)

| Claim (location at C) | Recorded bytes | Result |
|---|---|---|
| Discovery returned 110 records, `has_more:false` (signal entry l.17–18) | `inventory.envelope.json` `.data.normalized_result.output_window` = 110/110/110, false; 110 unique ids | holds |
| The `signature` decoder failed at `pd.py:138` with an underscore literal under Python 3.5.2, and is excluded (l.21–24) | The diagnostics contain `invalid syntax (pd.py, line 138)` and `0b0000_0010_1001_0001`; `signature` is absent from `decoders[].id`; the banner says Python 3.5.2 | holds |
| The synthetic `uart-hi.bin` has SHA-256 `4a2e…1727`, is 2500 bytes, 100 samples/bit at 960000 Hz, payload `4869` (l.37–43) | The blob sha256 matches. Re-deriving the `make-uart.py` bit list gives the same digest and length. 960000/9600 = 100 | holds |
| The literal annotations are `300-1100 …48` and `1300-2100 …69` (l.53–56) | `decode-uart-hi.envelope.json` `annotations_text` is identical. The frame arithmetic (2 idle + start bits put data at 300–1100; stop + start put data at 1300–2100) agrees | holds |
| The public `.sr` has SHA-256 `01b7…0b61`; 625 kHz, 9600 baud, TX (l.66–69, S059) | Blob sha256 matches. Archive `metadata`: `samplerate = 625 kHz`, `probe1 = TX`, `driver = chronovu-la8`. `uart-README.txt` gives 625 kHz for 9600–1200 and probe TX | holds |
| 12885 lines; leading BA,BD,C9,B1,91,85,0D,0A; first `48` at sample 5512 (l.76–78) | `total_lines:12885`, `has_more:false`; the first nine lines match exactly. There are 919 complete `48 65 6C 6C 6F 20 57 6F 72 6C 64 21 0D 0A` runs, and the tail is truncated at the end of the 8388608-sample buffer | holds; "not lossless" is correctly worded |
| The invalid-decoder control is `execution_failure`, exit 1 (l.84–86) | Envelope `ok:false`, `code:execution_failure`, stderr `No module named 'round23_nonexistent_decoder'`; `run.json` `exit:1` | holds; it is a refusal, and the counter's `bind_new` rejects `ok≠true` |
| prlimit settings 1 GiB / 64 MiB / 30 s CPU / core 0, 30 s deadline, 4 MiB output (l.111–112) | `resource_limiter.arguments` and `limits` match (the 32 MiB input cap is also present but not mentioned) | holds |
| The launcher digest `50fe…0902` is the subject, not the installation; ELF `10fe…ebd` (l.101–106) | `tool.sha256`/`subject.digest` = `50fe…`; `tool-runtime-pins.json` sigrok-cli = `10fed05ae399…` | holds |
| Banner shows sigrok-cli 0.7.2, libsigrok 0.5.2, libsigrokdecode 0.5.3 (l.107–108) | `version_banner` matches | holds; see F2 for what it also shows |
| `hardware_acquisition:not-performed` is only a provider declaration (l.114–116; SKILL l.727) | The field is present in all three ok envelopes. The provider adds `--dont-scan` and `--input-file=recording` to sigrok, and passes no `-d` driver | holds; the hedge is correct (see A1) |
| Dart: x86_64, libapp `f82a…38a8`; offsets/sizes/magic/kind/length of all four symbols; hash `78da…3f3f` with 2 sources; `string_pool` partial (Dart entry l.33–51) | `inspect-dart-legacy-saber.envelope.json` `normalized_result` matches every table cell. `run.json` argv/exit 0/empty stderr and APK sha256 match `legacy-saber-download.json` | holds |
| Both debugger verbs are unheld/Adjacent (PROVINCE l.239–242; SKILL l.722; Dart l.66; signal l.117) | `git ls-tree -r C -- round-23/evidence round-22/evidence` has no gdb/rizin/debug entry. In `count-c1.py` l.111–124, a new witness requires a cited round-23 `.json` blob holding the evidence id and passing `bind_new`/`r22.bind_cli`, and a mention alone adds only to `catalog_mentioned_count` | holds; the falsifiers "mere mention counts" and "refusal counted" are not triggered for the debugger verbs |

### F1 — the "bundled libraries" wording hides a host-resolved runtime, and libusb is unpinned (observed; calibration and depth)

- **Counterexample:** the signal entry (l.97–98) says `tools/sigrok-cli.sh` "selects bundled libraries … but preloads the host's matching libgmodule". Lessons (l.63–66) says the extraction "installs a lane-local ignored runtime only: sigrok-cli0.7.2, libsigrok0.5.2, libsigrokdecode0.5.3, Python3.5.2". The S060 row says "pinned local sigrok0.7.2 wrapper".
- **Evidence:**
  - The `sigrok-extraction.json` stdout lists no `libglib-2.0`, `libgio-2.0`, `libgobject-2.0` or `libusb-1.0` under `usr/lib` (grep count 0).
  - The recorded banner shows `glib 2.48.2 (rt: 2.90.1/9001:1)` and `libusb-1.0 1.0.30.12037`. Runtime glib is the host's 2.90.1, and the libusb version cannot come from a 2019 bundle, so it is host-resolved. [INFERENCE: libsigrok formats the libusb field from runtime `libusb_get_version()`.]
  - `tool-runtime-pins.json` pins host glib, gio and gmodule (`/usr/lib/lib*-2.0.so.0.9000.1`) but has no libusb or gobject entry (grep count 0).
- **Impact:** the executed tool is a hybrid of the 2019 bundle and moving host libraries. Its one hardware-capable library (libusb) is unpinned, and a host glib or libusb upgrade silently changes the "pinned" runtime. This does not change k.
- **Smallest safe correction:** one sentence in the signal entry (and, optionally, the lessons tooling paragraph) stating that glib/gio/gobject and libusb-1.0 resolve from the host, with the banner runtime versions. Either append host libusb and gobject digests to a new dated pins file, or state that they are unpinned. Do not rewrite the existing pins file.

### F2 — the SKILL decision row presents one fixture's sample rate as the generic recipe (observed; calibration)

- **Counterexample:** `SKILL.md` l.719, row "Existing raw UART sample file", prescribes `samplerate=960000` and `baudrate=9600` as the decision for any raw UART file.
- **Evidence:** 960000 Hz and 9600 baud are the planted parameters of the synthetic `uart-hi.bin` (from `make-uart.py`). The public recording runs at 625 kHz (`.sr` metadata). A raw binary file carries no rate, so copying the row to another capture mis-times every frame.
- **Smallest safe correction:** write `binary:numchannels=<n>:samplerate=<recording's actual Hz>` and `uart:rx=<ch>:baudrate=<declared baud>`, and label 960000/9600 as the exercised synthetic example.

### F3 — "at least one actual direction is still required" is not in the recorded help (observed absence; calibration)

- **Counterexample:** signal entry l.30–32.
- **Evidence:** `uart-help.envelope.json` `help_lines` says `Required channels:` / `None.` and `Optional channels: rx, tx`. The documentation lines say only "It can be run on one signal line (RX or TX) only, or on two lines". The uart `pd.py` is digest-pinned (`51a29d0e51f9…`) but its text is not committed, so the "required" rule has no recorded-byte source. [INFERENCE: upstream `pd.py` may raise when neither channel is given, but that is unobserved here.]
- **Smallest safe correction:** mark that clause **Inference**, or retain and cite the exact `pd.py` line.

### F4 — the Dart carrier contrast is ABI-asymmetric and unrecorded on the R22 side (observed; calibration)

- **Counterexample:** the Dart entry (l.57–60) says "this selected carrier exposes the four names the reader supports, whereas the retained R22 carrier did not". PROVINCE l.234 says "APK whose libapp exports the supported four dynamic snapshot symbols".
- **Evidence:** the R23 success names `abi:"x86_64"` and has no ABI-candidate field. The R22 refusal (`round-22/evidence/c1/inspect-dart-aot-saber.envelope.json`) has `details:{operation,path}` and a reason, and names no ABI at all (grep for ABI tokens returns empty).
  So the observed contrast is between "the reader's selection on carrier 1330203 (x86_64)" and "the reader's unrecorded selection on carrier 1360103". It is not a same-ABI layout comparison, and the other ABIs of 1330203 are unobserved.
- **Impact:** an ABI-selection difference is not excluded as the explanation. The entry already disclaims the causal SDK boundary, and the count is not affected.
- **Smallest safe correction:** say "selected x86_64 libapp" in PROVINCE l.234, and add to Dart l.57–60 that the R22 refusal records no ABI selection, so the contrast is per-reader-selection.

### A1 — advisory: "not requested" versus "not performed" for hardware (inferred; no edit required)

- The provider passes `--dont-scan` and file input (observed), which suppresses sigrok driver scans only.
- [INFERENCE from upstream libsigrok/libusb behaviour, not recorded bytes] `sr_init` calls `libusb_init`, and on Linux that may enumerate USB devices via udev/sysfs whatever the CLI flags. Host-resolved libusb 1.0.30 (F1) is in-process.
- The committed text already calls `not-performed` a provider declaration and denies running a syscall/device-contact monitor (signal l.114–116; SKILL l.727–728; PROVINCE l.225–229). That is correct calibration.
- Any future wording such as "no device contact" or "hardware isolated" would be an overclaim. Optionally, cite `--dont-scan` as the observed request scope.

## Impacted axes

- **Coverage:** none. 4/6 is unaffected: the two debugger verbs have no bindable envelope, and the signal and Dart witnesses bind to `ok:true` original envelopes.
- **Calibration:** F1, F2, F3, F4.
- **Depth:** F1 (tool identity and provenance).

None of these is a tradeoff the canonical judge must reject. All are wording or pin-supplement fixes, and none touches the claim, the denominator or the counter.

## Produced files and hashes

- `.ufo/waves/round-23/w2/CriticScopeFinal.md` — this file. The sha256 is in the handoff, because the file cannot contain its own digest.
- I wrote nothing else in the lane. Outside the lane I created two scratch files, `/tmp/off.txt` and `/tmp/hw.sr` (copies of committed blob content), which I did not delete. The contract only allows writes under `w2/` or `runtime/<SeatName>/`, so this is a scope deviation and they should be removed.

## Installs

None. No pacman, uv, cargo or npm transaction, and no config edit.

## Open risks

- The host-library drift in F1 persists until a pins supplement or a disclosure lands.
- The A1 USB-enumeration question is unresolved without a syscall monitor, which is out of scope for this wave.
- The R22 ABI selection in F4 is unrecoverable from the retained bytes without replaying the producer, which is disallowed.
- Author-side review only; this is not independent outside admission.
