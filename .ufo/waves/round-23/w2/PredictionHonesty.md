# KaidokuR23.PredictionHonesty — predictions.json vs actual official annotations

Candidate source commit `2838351450ff1ee4baa620c962a1153450d53311` (candidate blob hash `predictions.json` = `f230addbddf6e1951ccfc5eacd40362e05847329`; git-show bytes sha256 `2ec069ad63616f95076a993e89198100438d30f806d167152d211d4d7efc4817`). Worktree copy of `predictions.json` is byte-identical (same sha256), single commit `2b40aec` touched it (11:33:00 -03). Baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.

All findings below are **observed** from `git show <candidate>:PATH` bytes plus local re-analysis of those bytes in `/tmp`; no producer replay, no live tool run, no REA invocation. `.sr` and envelope parsing was offline reading of committed bytes (python3, stdlib only).

## Findings

### F1 — MEDIUM (prediction false, confirmed): `official.expected_text` is not met, literally or even as containment

- `predictions.json` `official` block: `"expected_text": "Hello World!"`, `"expected_exit": 0`, decoder `uart:rx=TX:baudrate=9600`, `source_sha256 01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61` (matches committed `hello_world_8n1_9600.sr` byte digest and `official-download.json` receipt — observed).
- Actual retained decode (`decode-official-uart.envelope.json`, `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c`, `normalized_result.annotations_text`, 12885 lines, `has_more:false`) re-parsed offline:
  - Leading annotations are **not** "Hello": `BA BD C9 B1 91 85 0D 0A` (rows starting at sample 108), i.e. 6 garbage bytes plus `\r\n` before the first `H` at sample 5512.
  - Byte histogram over the 12885 displayed hex values: `6C×2760, 6F×1840, 48/65/20/57/72/64/0D/0A ×920 each, 21×919, BA/BD/C9/B1/91/85 ×1 each` (observed counts).
  - Reconstructed ASCII (labelled inference from hex): `\xBA\xBD\xC9\xB1\x91\x85` + `\r\n` + 919× `"Hello World!\r\n"` + a final truncated `Hello World` **without** the closing `!` (the last annotation row is `8388112-8388632 uart-1: 64`; 12885 bytes total = 6 + 920×14 + 11 + 1).
  - Therefore the literal substring `"Hello World!"` is **absent** from `annotations_text` even before hex conversion: producer text is `<ranges> uart-1: <HEX>` lines. `contains_literal_Hello_World` recomputed by the committed `describe-signals.py` is `false` for `decode-official-uart` (observed in retained `verify/initial/signal-records.json`, measured at rev `6615aeae642aec36959180e7ea940b2794c7f1cb`; candidate did not change `describe-signals.py` semantics).

### F2 — LOW (disclosure honest; no forecast rewrite, no lossless claim): the false prediction is disclosed in the corpus entry

- `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` (blob sha256 `7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35`) states: "Initial annotations are BA,BD,C9,B1,91,85,0D,0A; the first matching Hello World sequence begins at sample5512. Thus the entire output is **not** described as a lossless Hello World payload. The initial `predictions.json` expected textual Hello World; output is hex annotation text, so that literal-string prediction is not met. Decoding and inferred interpretation are distinct; no false-clean prediction is claimed." (observed; all quoted facts verified against the envelope above).
- `predictions.json` was committed in `2b40aec` and **never rewritten** at candidate — forecast left standing as initially written (observed blob history: single commit, unchanged bytes at candidate; identical to worktree).
- Envelope `limitations` also preserve verbatim-text/no-lossless semantics: "Sample-number ranges and display text are preserved verbatim, not converted to timestamps or parsed as a lossless byte stream. All producer stderr is retained, including warnings on exit zero." (observed). No code consumer of `predictions.json` exists (`git grep expected_text|expected_rx_hex|predictions.json` at candidate hits only the file itself and the seat spec `gen-wave2.py:52`), so the false expectation cannot be silently converted into a pass by any committed check.

### F3 — LOW (prediction hygiene): the remaining `predictions.json` fields all match retained observations

- `synthetic`: `expected_exit 0`, `expected_rx_hex ["48","69"]`, `binary:numchannels=1:samplerate=960000`, `uart:rx=0:baudrate=9600` — matches `decode-uart-hi.envelope.json` annotations exactly: `300-1100 uart-1: 48\n1300-2100 uart-1: 69\n`, exit 0 (observed).
- `refusal`: `expected_exit 1`, `round23_nonexistent_decoder` — matches `decode-invalid-decoder` actual `execution_failure` exit 1 (observed).
- `official.expected_exit 0` and decoder/selection string `uart:rx=TX:baudrate=9600` match the retained run argv exactly (observed; `.sr` metadata declares `probe1 = TX`, 8 probes, samplerate `625 kHz`, so the decoder-layer pin binds correctly).

### F4 — LOW (disclosure completeness gap, inferred): the entry's non-lossless wording does not surface two observable envelope facts

1. The trailing truncation: the annotated stream ends `... Hello World` with no `!` (final row `8388112-8388632 uart-1: 64`), and the byte histogram shows `!` (0x21) at 919 vs 920 for every other payload byte. The entry says "not lossless" but never mentions the tail cut.
2. Annotation sample ranges exceed the recorded capture: `.sr` `metadata` declares `capturefile = logic-1`, `unitsize = 1`, 8.388.608-byte `logic-1` member at `samplerate = 625 kHz` ≈ 8.388.608 samples, yet the final annotation end sample 8388632 is 24 samples beyond, and `--all_lines` output is described as exhausted (`has_more:false`). Nominal overhang only; flagged as an unexplained producer detail, not a defect of the envelopes.
Both are covered only loosely by the entry's blanket "not lossless" sentence; no downstream check encodes them.

## Severity summary

| ID | Severity | Character |
|---|---|---|
| F1 | MEDIUM | Confirmed false prediction vs retained actual output |
| F2 | LOW | Honest disclosure; forecast unrewritten; no lossless treatment |
| F3 | LOW | All other prediction fields verified accurate |
| F4 | LOW | Disclosure gaps: tail truncation + range/capture overhang not stated |

## Produced files and hashes

- `.ufo/waves/round-23/w2/PredictionHonesty.md` (this report; path relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`).
- Scratch reads only in `/tmp` (`/tmp/off-env.json`, `/tmp/hw.sr`) — outside the lane write scope for permanent artifacts, used transiently to parse committed bytes; no lane file modified.

## Installs

None.

## Open risks

- `predictions.json` has no self-verdict field and no consumer; a reader could treat `official.expected_text` as if it had been met. Truth survives only in the entry prose and in recomputed `contains_literal_Hello_World:false`; unknown whether L1 intends a future verdict field (out of my scope to add).
- F4 items are described as producer-observable facts I derived offline from committed bytes; I did not rerun any decoder (prohibited), so the semantic cause of the truncation/overhang is unknown.
- W1 counterpart: `w1/ConnectSourceChain.md` item 8 ("Hex annotation text is not the ASCII payload", lines 153–157) already flagged hex-vs-literal; my finding confirms it still holds at the candidate commit — not a stale proposal, retained accurate.
