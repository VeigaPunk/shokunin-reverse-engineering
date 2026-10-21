# OriginalSynthetic: source review of decode-uart-hi envelope/run pair and uart-hi.bin

Seat: `KaidokuR23.OriginalSynthetic` (leaf reviewer, round-23 w2, R23-C1 coverage).
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` (B=`aa1450b82f9ede35aada63efe8a34e01c6e02f72`).
Scope: exact SHA, 960 kHz / 100 samples per bit, two literal annotations, no acquired-device assertion.

Method and bounds: every candidate byte was read with `git show 2838351450ff…:<path>`. No REA producer replay, no sigrok-cli or decoder execution, no `count-c1.py`, no device, process, or network access. Independent checks were reads and recomputation over committed bytes: a pure-Python bit-level decode of the committed `uart-hi.bin`, and regeneration of the generator's bit list from the `make-uart.py` source logic in memory. The generator script itself was not executed. Copies live only under the ignored `runtime/OriginalSynthetic/`.

## Verdict

- **Bound:** exact SHA and size of `uart-hi.bin`; the run stdout equals the envelope; both literal annotations reproduce exactly from the committed bytes under the decoder defaults that the producer ran; 100 samples per bit is a byte property.
- **Declared only, not bound to the bytes:** 960 kHz. The decode output does not identify the absolute sample rate (F1).
- **Retained-field overclaims:** "environment" in the knowledge note (F2); "effective limits" in the envelope (F8).
- **Bound by provenance and argv, not by envelope fields:** "no acquired-device". The envelope's `hardware_acquisition`/`authority` values are adapter constants (F3).
- **Version or post-run identity only:** producer `rea-agents@6.5.0` (F6) and the sigrok-cli executable (F7).
- No field in the pair asserts an acquired device.

## Findings (severity order)

**F1 — MEDIUM — "960 kHz" is declared, not bound to the bytes.**
- Observed: `uart-hi.bin` is headerless raw logic (2500 bytes, byte values {0,1}, no rate field). The only 960000 Hz statements are `decode-uart-hi.envelope.json` `data.parameters.input_format = "binary:numchannels=1:samplerate=960000"`, the generator constant `samplerate_hz: 960000` in `generate-uart.run.json` stdout, and knowledge note line 41.
- Observed (source): `uart-pd.py` (committed as `w1/_uart/libsigrokdecode-0.5.3/decoders/uart/pd.py`, sha256 `51a29d0e…`) line 223: `self.bit_width = float(self.samplerate) / float(self.options['baudrate'])`. Annotation values are sample indices (pd.py:164–165, 299–300).
- Inferred (arithmetic, not executed): output depends on samplerate and baud only through their ratio, 100 samples/bit. A different pair with the same ratio would give identical annotation text.
- Required wording: "declared input rate 960000 Hz; the decode identifies 100 samples per bit."

**F2 — MEDIUM — "environment" retention is overclaimed.** Knowledge note line 2: "exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files".
- Observed: `decode-uart-hi.run.json` keys are exactly `[argv, captured_at, cwd, env_overrides, exit, stderr, stdout]`. `env_overrides` holds only `REA_SIGROK_COMMAND`. Ambient environment is not retained.
- Observed and retained: argv, stdout (equal to envelope), stderr `""`, exit `0`.
- Not retained: launcher-exported `LD_LIBRARY_PATH`, `LD_PRELOAD`, `PYTHONPATH`, `SIGROKDECODE_DIR` (derivable from committed `tools/sigrok-cli.sh`, blob `3a806cbb…`, not recorded per run).

**F3 — LOW-MEDIUM — "no acquired-device" is bound by provenance and argv, not by the envelope's acquisition fields.**
- Observed constants: `normalized_result.hardware_acquisition = "not-performed"`, `authority = "shipped-artifact"`, `confidence = "observed"`, `subject.format = "file"` are identical in `decode-uart-hi`, `decode-official-uart` (a third-party recording), `uart-help`, and `inventory` (no recording subject). These are adapter constants, not per-run observations.
- Observed per-run evidence: `normalized_result.tool.arguments` contains `--dont-scan` and `--input-file=recording`. Subject is a file, `input_format` is binary.
- Observed linkage: `evidence_links: []` and `relationship_coverage: null`. The link to the generator exists only by digest equality (`uart-hi.bin` sha256 `4a2e729f…` = `generate-uart.run.json` stdout `sha256`), plus knowledge note line 40 ("not data acquired from any device").
- Inferred: `authority = "shipped-artifact"` does not describe a self-generated fixture if read literally. Its taxonomy is not defined in retained evidence.
- Frozen falsifier "source linkage absent" applies at envelope level. The note supplies path-level linkage; I did not check its S058–S060 rows.

**F4 — LOW — 100 samples/bit is byte-bound but absent as a literal from the decode pair.**
- Observed: no `samples_per_bit` key in the decode envelope or run. The literal exists only in `generate-uart.run.json` stdout (`samples_per_bit: 100`) and in `make-uart.py`.
- Observed (bytes): 2500 bytes = 25 aligned blocks of 100 bytes, each block constant, values {0,1}. The 100-sample bit period is therefore a byte property.

**F5 — LOW — 8N1 and LSB-first framing are not stated in the decode argv or envelope; they come from decoder defaults.**
- Observed: argv and `tool.arguments` carry only `uart:rx=0:baudrate=9600`. No data_bits, parity, stop_bits, or bit_order option is passed.
- Observed (source, pd.py lines 101–111): defaults `data_bits` 8, `parity` none, `stop_bits` 1.0, `bit_order` lsb-first, `format` hex (explains "48"/"69"). `baudrate` default 115200 is overridden to 9600.
- Observed (pin): `tool-runtime-pins.json` records runtime `usr/share/libsigrokdecode/decoders/uart/pd.py` sha256 `51a29d0e…`, identical to the committed copy. The runtime therefore has the same defaults. The pin was captured 14:42:59.166503, about 4 min after the run at 14:38:40.850488.
- Verdict: bound via source plus post-run hash equality. Not retained in the decode record.

**F6 — LOW-MEDIUM — producer identity is a version string only.**
- Observed: run argv begins `npx -y rea-agents@6.5.0 decode-signal-recording`. No tarball digest, lockfile, or integrity value is retained. Envelope `provider.version` is `sigrok-cli@0.7.2`, not the REA version.
- Observed: W1 `w1/UartSemantics.md` lines 191–192 cite `SigrokRecordingProvider.js` sha256 `7979bafb…2dced7` (lines 229–230). That digest appears in no field of the decode pair. I did not fetch the npm package.
- Verdict: "REA6.5.0 envelopes" is bound by argv string only.

**F7 — LOW-MEDIUM — sigrok-cli executable identity is bound only by a post-run pin the envelope does not reference.**
- Observed: `tool.sha256` (launcher `tools/sigrok-cli.sh`, `50fe4359…`) equals the committed blob and the pin entry. The launcher execs `runtime/squashfs-root/usr/bin/sigrok-cli`, which is in the ignored runtime and not committed.
- Observed: committed `.ufo/waves/round-23/tool-runtime-pins.json` (sha256 `02ef8379…`) records sigrok-cli ELF `10fed05a…` (77728 bytes), `libsigrok.so.4` `0861b03c…`, `libsigrokdecode.so.4` `4bfe11a3…`, and the decoder `pd.py`. Its `limit` field reads "one named instant; selected files only, not complete installation or continuous custody".
- Observed: the envelope carries no pin reference. The link is knowledge note lines 101–106 only. `prlimit` (`resource_limiter.sha256` `092bb6db…`) is not among the pins.
- Unknown: whether the executable at 14:38:40 equals the one pinned at 14:42:59. No custody record exists.

**F8 — LOW — "Effective limits are reported" overstates; "measured" (knowledge note line 113) is unsupported.**
- Observed: envelope `data.limitations[3]` says "Effective limits are reported." Retained values are requested prlimit arguments (`--as=1073741824:1073741824`, `--fsize=67108864:67108864`, `--cpu=30:30`, `--core=0:0`), not post-application effective values. No measurement is retained.
- Unknown: the producer's min(inherited, requested) logic is not in the pair.

**F9 — LOW — "literal output" is the adapter-normalized field, not a separately retained raw sigrok stdout.**
- Observed: run stdout is the REA JSON envelope. `normalized_result.annotations_text` is adapter-rendered, and `output_window` counts are adapter-computed. Raw sigrok-cli stdout is not stored separately.
- Inferred: the text matches sigrok's `start-end row: value` format, so passthrough is likely. It cannot be excluded from the pair.

**F10 — INFO — `evidence_id` is opaque to independent recomputation.**
- Observed: `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e`. I tried sha256 over 16 JSON serializations (data, whole envelope, normalized_result, data minus evidence_id; sorted and unsorted; compact and spaced). None matched. Canonicalization is not retained.

## Claim-by-claim binding (the five named claims)

| Claim | Retained in pair | Independently bound | Verdict |
|---|---|---|---|
| Exact SHA of uart-hi.bin | envelope `subject.digest.sha256`, `normalized_result.artifact.sha256`/`bytes`; run stdout | candidate blob recomputed: sha256 `4a2e729f…`, 2500 B; generator stdout `sha256`; generator logic regenerated in memory | BOUND |
| 960 kHz | `parameters.input_format` samplerate=960000 (declared) | No: headerless bytes; output depends only on ratio (F1) | DECLARED ONLY |
| 100 samples per bit | no literal in decode pair; literal in `generate-uart.run.json` only | Yes: 25 constant 100-byte blocks | BOUND by bytes (F4) |
| Two literal annotations | `normalized_result.annotations_text`; run stdout; knowledge note lines 53–56 | Reproduced byte-exact from committed bytes with 8N1 LSB-first 100 samples/bit; spans match pd.py arithmetic | BOUND (round trip; F5, F9) |
| No acquired-device assertion | argv `--dont-scan`, `--input-file=recording`; file subject; generator provenance | Digest equality with generator output; generator logic. `hardware_acquisition` is an adapter constant (F3) | SUPPORTED, not by envelope fields |

## Positive confirmations (observed)

- `git show 2838351…:.ufo/waves/round-23/evidence/c1/uart-hi.bin | sha256sum` → `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`; `wc -c` → 2500.
- Parsed `decode-uart-hi.run.json` `stdout` equals parsed `decode-uart-hi.envelope.json` (object equality True). Run `exit` 0, `stderr` `""`.
- Bit-level decode of committed bytes: bits `[1,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1]`. Frames: (300–1100, 0x48 `H`, stop 1) and (1300–2100, 0x69 `i`, stop 1). Rebuilt text `300-1100 uart-1: 48\n1300-2100 uart-1: 69\n` equals retained `annotations_text`.
- `generate-uart.run.json` stdout: sha256 `4a2e729f…`, size 2500, `samplerate_hz` 960000, `baud` 9600, `samples_per_bit` 100, `payload_hex` `4869`, bits identical to the regenerated list, exit 0.
- Span arithmetic: with bit_width 100, pd.py:164–165 (`s - floor(halfbit)` to `samplenum + ceil(halfbit)`) and pd.py:299–300 reproduce 300/1100 and 1300/2100.
- W1 `UartSemantics.md` lines 137–140 (span semantics) and 194–198 (argv construction, no `-c`/`-l`/`-B`) match the committed pd.py and the envelope `tool.arguments`.

## Produced files and hashes

Under `runtime/OriginalSynthetic/` (ignored; git-blob IDs are at `2838351…`):

| File | sha256 | Bytes | Blob |
|---|---|---|---|
| `decode-uart-hi.envelope.json` | `a40c947cf337319411b55c43e8e0270437e29324038a67bacb17232b9311a884` | 4821 | `6dceda21…` |
| `decode-uart-hi.run.json` | `2c1984eba0171f62dd9dd63549789daa591e4084bec51f2f3e3fa3b1487e5985` | 5819 | `a0a40b58…` |
| `uart-hi.bin` | `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727` | 2500 | `295d0ebc…` |
| `uart-pd.py` | `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62` | n/a | `w1/_uart/…/decoders/uart/pd.py` |
| `tool-runtime-pins.json` | `02ef8379734f3bf9d25b893b7170e36aaab32805c542c613e399307490a68f73` | 2833 | n/a |
| `UartSemantics.md` (read-only W1 copy) | `f5a43e2250697a57c3edd44dd7461683a3eb24857426f0af51f921c4deae9b0b` | 26234 | n/a |
| `knowledge-note.md` | `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35` | n/a | `6c14cce6…` |
| `round23-tree.txt` (`ls-tree` snapshot, 479 entries) | `367ea64e1d73993264ff2881c5e7b73226f50b77a9e56d394a0d06cb29ff546b` | n/a | n/a |

This report: `.ufo/waves/round-23/w2/OriginalSynthetic.md`. Its hash is recorded in the hand-off message, not here.

## Installs or none

None. No pacman, uv, npm, cargo, or download. Tools used: `git` (read-only), `sha256sum`, `wc`, and the existing eval kernel for in-memory parsing. No config, global, or sibling file was touched.

## Open risks and unknowns

- Producer code (`rea-agents@6.5.0`, `SigrokRecordingProvider.js`) was not reviewed. Its identity is unpinned in the pair (F6).
- The runtime (`squashfs-root`) is not committed. Pins are post-run and "not continuous custody" (F7).
- The decode is a self-consistency round trip against the author's generator. It establishes nothing about real UART semantics or any device. Knowledge note line 32 disclaims this.
- Binding uses candidate bytes only. The worktree paths in the envelope (`local_path`, `parameters.path`) were deliberately not read.
- Re-evaluation of W1 proposal findings was limited to the lines that bear on this pair (listed above). The rest of W1 is outside this item and unexamined.
- R23-C1 counting (`count-c1.py`) was not run. That is a designated Run seat command.
