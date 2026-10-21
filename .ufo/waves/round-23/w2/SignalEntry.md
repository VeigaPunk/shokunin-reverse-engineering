# SignalEntry: R23-C1 source review of the offline signal knowledge entry

Seat: KaidokuR23.SignalEntry (leaf source review; coverage of R23-C1 only).

## Target and method

- Target: `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` at candidate `2838351450ff1ee4baa620c962a1153450d53311`; baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. Entry sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35` (7153 bytes). Line numbers below refer to this blob.
- Read only candidate bytes (`git show <rev>:<path>`, `git cat-file -e`). Parsed committed JSON, the committed `.sr` zip (stdlib `zipfile`, read-only) and sha256 of committed blobs.
- Decoder emission order was checked against the uncommitted runtime file `uart/pd.py` (ignored runtime tree, read-only). Its sha256 `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` equals the pin in committed `tool-runtime-pins.json`.
- Not run: REA (`npx -y rea-agents@6.5.0`), sigrok, `count-c1.py`, `describe-signals.py`, npm, any device, network or remote access. Two scripts were read as source only.
- Scope items: (1) exact IDs, operations and paths; (2) literal versus inferred UART bytes; (3) rejection control; (4) hardware declaration limits.

## Verdict

Every evidence ID, operation, path and digest the entry cites matches committed bytes, and the literal UART output matches the envelopes. The defects are in what the entry leaves unsaid or overstates:

- an undisclosed end-of-recording annotation (F1);
- a round-status sentence that contradicts the lesson and the README (F2);
- provenance and retention wording that outruns its receipts (F3 to F6).

F1 and F2 should be fixed before L1 relies on the entry. Nothing here changes a count by itself; the count is not re-derived in this review.

## Verified (observed, exact match)

- V1 IDs, operations, paths. `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` is the `evidence_id` of `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`, operation `inspect_signal_decoders`. `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` is `decode-uart-hi.envelope.json` and `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` is `decode-official-uart.envelope.json`; both have operation `decode_signal_recording`. All three IDs in the entry match. Every `.ufo/waves/...` path the entry cites exists at the candidate.
- V2 digests. `uart-hi.bin` `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`. `hello_world_8n1_9600.sr` `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61` (58381 bytes; `official-download.json` records status 200 and the same size and digest). `sigrok-cli.sh` `50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902` (698 bytes). AppImage `49d2f597ec3ed3d71bfeb0465474ec2aac084fa1f66cbb132d996f7c9f50b614` appears in `sigrok-extraction.json` and as `EXPECTED` in `setup-sigrok.py`; the AppImage itself is not committed. sigrok-cli ELF `10fed05ae399d36a49ee9558440192023f842f3edbce0472a7f1ed15405ccebd` appears only in `tool-runtime-pins.json`; the ELF itself is not committed.
- V3 Inventory. 110 decoder records, no duplicate IDs, `uart` present, `signature` absent, `round23_nonexistent_decoder` absent. Output window: examined = matching = returned = 110, `has_more` false.
- V4 Signature diagnostic. `SyntaxError ... (pd.py, line 138)` for decoder `signature`, on the literal `0b0000_0010_1001_0001`. The entry's claim (underscore numeric literal rejected by Python 3.5.2) is accurate.
- V5 UART help. 81 lines, `has_more` false; "Required channels: None."; optional channels `rx` and `tx`.
- V6 Synthetic recording. Committed `generate-uart.run.json` bits reproduce by hand from `Hi` (0x48 and 0x69, LSB first, one start and one stop bit, 100 samples per bit). Decoder output is exactly `300-1100 uart-1: 48` and `1300-2100 uart-1: 69`. The entry labels this "Inference", which is the right label.
- V7 Official recording, literal output. 12885 lines, `has_more` false. First eight lines `BA, BD, C9, B1, 91, 85, 0D, 0A`. The first complete `Hello World!\r\n` runs from sample 5512 (`48`) to 13975 (`0A`). Spacing of 651 samples per byte matches 625 kHz / 9600 baud.
- V8 Recording metadata (committed `.sr`, stdlib zip read). `metadata`: `driver = chronovu-la8`, `unitsize = 1`, `samplerate = 625 kHz`, `total probes = 8`, `probe1 = TX`. Member `logic-1` is 8388608 bytes, so the recording has 8388608 samples, matching the README `--samples 8388608`.
- V9 Rejection control. `decode-invalid-decoder.envelope.json`: `ok` false, `error.code` `execution_failure`, `retryable` false, `details.operation` `decode_signal_recording`, `diagnostics.exit_code` 1. `decode-invalid-decoder.run.json` exit 1. stderr: `srd: ImportError: Failed to load decoder round23_nonexistent_decoder`. The entry's description is accurate.
- V10 Hardware argv. `tool.arguments` carry `--dont-scan` for inventory (`['--dont-scan', '--list-supported']`), uart-help (`['--dont-scan', '--protocol-decoders=uart', '--show']`), decode-uart-hi and decode-official-uart. `hardware_acquisition` is `not-performed` in all four successful envelopes.
- V11 Manual S058 (sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9`, 19180 bytes, matches the fetch receipt). Contains "Load input from a file instead of a hardware device." and documents `-i/--input-file`, `-P`, `-A`, `-I`, `-D/--dont-scan`, `--protocol-decoder-samplenum` (roff `\-` escapes; my first plain-text search missed them and was corrected). The S058 claim is supported.
- V12 Count binding (source reading only; not executed). `bind_new` in `count-c1.py` returns 1 for any top-level `ok` that is not `true`, so the invalid envelope cannot count. `ids` are taken from the entry text, so `uart-help` binds nothing because its evidence ID is not in the entry.

## Findings

Severity is a judgement about impact on the entry's claims; "observed" means read from committed bytes, "inferred" means derived from them.

### F1. Medium. The final literal annotation is an end-of-recording partial frame, not disclosed (observed + inferred)

- Where: entry lines 76 to 79 ("retains 12885 literal display lines", "Thus the entire output is not described as a lossless Hello World payload"); last line of `decode-official-uart.envelope.json` `annotations_text`: `8388112-8388632 uart-1: 64`.
- Observed: the recording has 8388608 samples (V8), last index 8388607. The last annotation ends at 8388632, 25 samples past the recording.
- Source (runtime `pd.py`, sha256 matches the pin): `get_data_bits` (lines 291 to 332) emits `rx-data` through `putx` as soon as the eighth data bit is sampled. `putx` (lines 163 to 165) sets the annotation end to `samplenum + ceil(bit_width/2)`. Stop-bit inspection (`get_stop_bits`, lines 392 to 404) needs a later sample.
- Formula check: on the synthetic recording (bit width 100), the first data-bit sample 350 gives start 300 and the last data-bit sample 1050 gives end 1100, both matching the planted bits. On the official first frame, start 108 gives first sample 140 and end 628 gives last sample 595.
- Inferred: the official last data-bit sample is 8388632 − 33 = 8388599, inside the recording. Its stop-bit sample would be about 8388664, outside it. So byte `0x64` is emitted without a framing check. Nothing in the file pads past the end (the member is exactly 8388608 bytes). The synthetic recording does not share this; its last stop bit lies at samples 2100 to 2199 inside 2500 samples, followed by three idle bits.
- Impact: the "12885 literal lines" and "entire output" statements include one end-of-recording frame whose framing was never checked. The rest of the literal output is unaffected by this.
- Fix: label the final line as end-of-recording, with its stop bit outside the recorded samples and framing unvalidated.

### F2. Medium. Round-status sentence contradicts the lesson and README (observed + inferred)

- Entry line 117: "Dart parsing and both debugger verbs remain unheld".
- Lesson `corpus/lessons/round-23.md` line 90: "Cumulative T1 count 1/6→4/6 ... both debugger verbs remain unheld". Inferred composition of the 4: R22 `identify-flutter-build` + `inspect-signal-decoders` + `decode-signal-recording` + `inspect-dart-aot`. The only other T1 verbs are the two debugger verbs.
- `corpus/README.md` line 72 lists the Dart envelope as "held narrowly".
- Fix: "This entry does not hold `inspect-dart-aot` (see the Dart entry); both debugger verbs remain unheld."

### F3. Medium-low. Uncited external-source claim (observed)

- Entry line 87: "The current upstream guide's newer `invalid_request` description is not substituted for this 6.5.0 observation." No source row, URL, fetch receipt or retained bytes exist for that guide. `fetches.json` lists only `sigrok-cli.1` and `uart-README.txt`. The lesson records the guide as a lead excluded from rows.
- Fix: remove the sentence, or add a row with URL and retained bytes.

### F4. Low-medium. Retention overclaimed: "environment" (observed)

- Entry line 2: "exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files".
- The run records keep `argv`, `cwd`, `env_overrides` (only `REA_SIGROK_COMMAND`), `exit`, `stdout`, `stderr` and `captured_at`. The full environment is not retained.
- Fix: "argv, cwd, env overrides, exit, stdout, stderr".

### F5. Low-medium. Producer identity pinned only by name@version; install-on-use unrecorded (observed)

- Every REA run argv begins `npx -y rea-agents@6.5.0` (for example `inventory.run.json` and `decode-uart-hi.run.json`). The envelopes' `provider.version` is `sigrok-cli@0.7.2`, not the REA package.
- The entry gives no package integrity, npm channel or cache location, or fetch record for `rea-agents@6.5.0`. The tooling directive requires channel, version and reason to be recorded for tool installs; an `npx -y` fetch-and-run is an install-on-use. I did not query npm.
- Fix: record the npm `dist.integrity` (or the cache path and its integrity) and the channel, or state that producer identity is name@version only.

### F6. Low-medium. Tool provenance outruns its receipts (observed)

- (a) Entry line 92: "The local official-release AppImage SHA256 is 49d2f5...". No committed URL or receipt covers the AppImage. `tools/setup-sigrok.py` names a "historical official URL" (`https://sigrok.org/download/binary/sigrok-cli/sigrok-cli-0.7.2-x86_64.AppImage`) and says "Digest identity is not publisher authentication". The lesson calls the file "pre-existing". Acquisition channel and date are unknown.
- (b) Entry line 94: "The exercised extraction command and output are in `sigrok-extraction.json`." That file (`.ufo/waves/round-23/sigrok-extraction.json`, sha256 `2b84f466e5a81e99c447554863bc01e0108aec29b3279cbeef6476b04c39e5e2`, 127744 bytes) has exactly the six keys of `setup-sigrok.py`'s stdout (`argv`, `cwd`, `appimage_sha256`, `exit`, `stdout`, `stderr`). It has no producer, no `captured_at` and no comparison result. "Exercised" rests on the file's own say-so.
- (c) Section "Tool identity, resource and scope boundaries": "No host package transaction or global configuration was changed." No receipt in committed evidence; this is an author-asserted negative.
- Fix: state the digest-only basis and that acquisition is not receipt-backed; add producer and timestamp to the extraction record, or label it accordingly.

### F7. Low. Recheck placeholder; no commit anchor (observed)

- Entry line 3: `recheck: ... --rev <MEASURED-COMMIT>`. Line 2 gives only a date. The measured commit is not recorded anywhere in the entry.
- `describe-signals.py` resolves `--rev` with `git rev-parse --verify --end-of-options <rev>^{commit}` and exits 2 on failure. Source reading; not run. The literal placeholder would fail.
- Fix: record the measured commit (`2838351450ff1ee4baa620c962a1153450d53311`, or whichever commit was measured).

### F8. Low. Ambiguous artifact paths (observed)

- Entry line 94 cites `sigrok-extraction.json` and entry line 103 cites `tool-runtime-pins.json` with no directory. Both live at `.ufo/waves/round-23/`, not `evidence/c1/`.
- Fix: write the full paths.

### F9. Low. Hardware-limit evidence under-cited; time order and rejection posture unrecorded (observed)

- (a) Entry line 114 cites only the provider declaration `hardware_acquisition:not-performed`. The `--dont-scan` argv in V10 is a file-anchored control that the entry does not cite.
- (b) `tool-runtime-pins.json` `captured_at` is `2026-10-21T14:42:59Z`. The decode runs were at `14:38:58Z` (official) and `14:38:59Z` (invalid), so the pins were captured about four minutes after the runs. Entry line 103 says "at one instant" without relating the pins to the runs.
- (c) `decode-invalid-decoder.envelope.json` `error.details` has only `exit_code`, `stdout` and `stderr`. The rejection control's sigrok argv and hardware declaration are therefore not recorded. The entry does not claim them, but it should state the limit.
- Fix: cite the `--dont-scan` argv; state the pin-to-run order; state the rejection control's missing posture.

### F10. Low. Unlabelled inference (observed)

- Entry line 31: "at least one actual direction is still required." The help envelope says "Required channels: None." The requirement comes from `pd.py` lines 505 to 507 (`if not True in has_pin: raise ChannelError('Need at least one of TX or RX pins.')`).
- Fix: cite `pd.py` or label the sentence as inferred.

### F11. Low. Linkage gaps for the two verbs (observed)

- `uart-help` (`ev_4be13793b8a767184ddcfb301b3f0e06c1333e12e533347c68eb1b53d169e94a`, operation `inspect_signal_decoders`, decoder `uart`) is cited by path only, with neither ID nor operation.
- `decode-invalid-decoder` is cited by path only and is absent from S060's enumerated artifact list, which names three envelopes.
- Counting is unaffected (see V12), but the linkage is incomplete.
- Fix: enumerate these envelopes in S060, or label them as unlinked witnesses.

### F12. Info. S059 internal inconsistency; committed file corroborates the declared settings (observed)

- S059 README: the probe table says "0 (green) TX" while its command says `-p '1=TX'` (0-based versus 1-based). The committed `.sr` names the channel `probe1 = TX`, `samplerate = 625 kHz`, driver `chronovu-la8` (V8), which corroborates S059's declared TX and 625 kHz. The decode resolves `TX` by name, so the result is unaffected.
- Optional fix: cite the metadata as observed corroboration; the entry currently treats these facts as only declared.

### F13. Info. Wording and unstated defaults (observed)

- Entry line 86 "rejected held witness" is ambiguous jargon.
- Entry line 113 "declared/measured provider settings": the prlimit values are declared in the envelope `limits` and `resource_limiter`; "measured" is unsupported.
- Entry line 109 ".pyc files" claim rests on the ignored runtime tree, not on committed evidence.
- The official decode relies on decoder defaults (8 data bits, no parity, one stop bit) that are not passed explicitly. This is consistent with the 8N1 filename but is not stated.

## Produced files and hashes

- Report: `.ufo/waves/round-23/w2/SignalEntry.md` (this file; its own sha256 is given in the final message).
- No other file was written. No git write, no index change, no runtime change.

Candidate blobs read (sha256 of content at `2838351450ff1ee4baa620c962a1153450d53311`):

- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` 7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35
- `corpus/lessons/round-23.md` 8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723
- `corpus/SOURCES.md` 736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525
- `corpus/README.md` 795466e5be2ac7341014a30a1a793a1aea17cdbb1f0d3451abc305085a62b57c
- `.ufo/waves/round-23/evidence/c1/inventory.envelope.json` 5f80218747c3f7c3308adef59216dea9559cada8c93a1ff543ebea6134a43d35
- `.ufo/waves/round-23/evidence/c1/uart-help.envelope.json` 462bc694a020c6b6eb9eeb171c5d7bfcf48c30a733ffe07c7df186b9d58c4d90
- `.ufo/waves/round-23/evidence/c1/decode-uart-hi.envelope.json` a40c947cf337319411b55c43e8e0270437e29324038a67bacb17232b9311a884
- `.ufo/waves/round-23/evidence/c1/decode-official-uart.envelope.json` 7d5e07cca64ba60aa66ae25b8402ffe70a1bfc49bcce5c9a16f67826f768358e
- `.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.envelope.json` 04697e72e9cabc9dae1385731ea3f2becf8a4bb94dc2334f067180b3b1008292
- `.ufo/waves/round-23/evidence/c1/inventory.run.json` df20226c269680c91c76bfa85386073d69257876c23e63e91176f7c0c5faae76
- `.ufo/waves/round-23/evidence/c1/uart-help.run.json` 20819612158048e687df0a59fab58b4d10bd71c238fc4bb0afa309bd846e4b17
- `.ufo/waves/round-23/evidence/c1/decode-uart-hi.run.json` 2c1984eba0171f62dd9dd63549789daa591e4084bec51f2f3e3fa3b1487e5985
- `.ufo/waves/round-23/evidence/c1/decode-official-uart.run.json` 0bdd002604176b2852d3400709951b1e34f5807645c23013e8b27e73cda4b62b
- `.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.run.json` 518181aa69dfc844601dbec60f7b8794bbde769d27a075e428398a214e45262c
- `.ufo/waves/round-23/evidence/c1/generate-uart.run.json` 1190f3dce3a155796569e84c3fddfb468bc868b890629f20667007a4c0538bbb
- `.ufo/waves/round-23/evidence/c1/uart-hi.bin` 4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727
- `.ufo/waves/round-23/evidence/c1/hello_world_8n1_9600.sr` 01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61
- `.ufo/waves/round-23/evidence/c1/official-download.json` 426483100c0df544f2bf4a8d61293f759f3a49103b3ed239e2088f2a695685d8 (329 bytes)
- `.ufo/waves/round-23/evidence/sources/fetches.json` bd4310a82f8b844d66568a7ae419ba199c626a2b72cb18a0439d63bf6a50538d
- `.ufo/waves/round-23/evidence/sources/sigrok-cli.1` e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9
- `.ufo/waves/round-23/evidence/sources/uart-README.txt` 7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66
- `.ufo/waves/round-23/sigrok-extraction.json` 2b84f466e5a81e99c447554863bc01e0108aec29b3279cbeef6476b04c39e5e2
- `.ufo/waves/round-23/tool-runtime-pins.json` 02ef8379734f3bf9d25b893b7170e36aaab32805c542c613e399307490a68f73
- `.ufo/waves/round-23/predictions.json` 2ec069ad63616f95076a993e89198100438d30f806d167152d211d4d7efc4817
- `.ufo/waves/round-23/tools/sigrok-cli.sh` 50fe43590a7b8f88f285f788ff6cb3bead8a3fe11be6a8b3c59f39f1f3470902
- `.ufo/waves/round-23/tools/setup-sigrok.py` a6e46c7a907682b85a423589cc19c6043ce42220f5f3c2c329fdb130f4d9bef7
- `.ufo/waves/round-23/tools/make-uart.py` 8720ee4e5afdfd66630fe4f357aec1a574b1fe2ff7bb367c5284079ff1ab6c3c
- `.ufo/waves/round-23/tools/describe-signals.py` a669607c12fd2be84dd28c80d4826b415c21bae06ec28aa78b22f6fc564078c3
- `.ufo/waves/round-23/tools/count-c1.py` f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2 (source read only; not executed)
- Runtime (uncommitted, ignored): `.ufo/waves/round-23/runtime/squashfs-root/usr/share/libsigrokdecode/decoders/uart/pd.py` 51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62 (equals pin)

## Installs or none

None. I installed, updated or fetched nothing. I did not run `npx`, npm, sigrok or REA. The only executions were read-only `git` queries, stdlib Python parsing and hashing of committed or read-only files.

## Open risks

- Nothing was re-executed. Every result above rests on committed envelopes and source reading. The sigrok binaries, the AppImage and the REA producer were not re-run or re-verified.
- The runtime `pd.py` hash matched its pin only at my read time. The runtime tree is ignored and not part of the commit, so it has no custody record.
- The runtime pins were captured about four minutes after the decode runs (F9b).
- The 4/6 cumulative count asserted in the lesson was not re-derived here. `count-c1.py` was not run because this seat is not a designated Run seat.
- The official recording's provenance is S059's declaration plus a digest match to a public URL. The entry already disclaims acquisition, but the final-byte framing gap (F1) means the literal output is not fully framing-validated.
- Only the `rx-data` annotation class is selected in the literal outputs, so framing or warning annotations would not appear there even if present. The entry says this in part; the consequence for the last byte is not stated.
