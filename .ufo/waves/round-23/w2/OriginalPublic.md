# R23-C1 source review — OriginalPublic (decode-official-uart envelope/run pair + public .sr)

Candidate commit: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Scope: `decode-official-uart.envelope.json`, `decode-official-uart.run.json`, `hello_world_8n1_9600.sr`. Targets: selected channel TX, source digest, leading anomalous bytes, exhausted display window, unretained or unbound claimed fields.

Method: all candidate bytes read with `git show <commit>:<path>` into `runtime/OriginalPublic/`. Producer, `sigrok-cli`, `rea-agents`, `count-c1.py`, and any counting command were NOT run. One read-only analysis script (`independent-decode.py`) was run once over the committed `.sr` and envelope (exit 0). Current-state runtime digests were compared against committed source. No worktree bytes were read.

## Summary

- **Source digest: bound.** The `.sr` at the commit is 58381 bytes, sha256 `01b72610…900b61`, matching `subject.digest`, `artifact.sha256`, and `official-download.json`.
- **Channel TX: bound by reproduction, not by retained fields.** Only bit 0 toggles; bits 1–7 are constant. The envelope retains only the string `rx=TX`. Samplerate, probe map, and sample count appear only in the `.sr`.
- **Annotation text: independently reproduced.** My decode of the committed bytes reproduces all 12,885 `annotations_text` lines (start, end, byte) with 0 mismatches.
- **Leading anomalous bytes: under-reported.** Of the 6 bytes before the first CRLF, `BA` and `85` are framing errors (stop bit = 0). Their `Frame error` annotations are computed by the decoder but excluded by `--annotations uart=rx-data`. Nothing retained in the envelope or run flags them.
- **Exhausted window: frame-exhausted, recording-truncated, undisclosed.** The display window is exhausted (`has_more:false`). The recording is exhausted at the 8,388,608-sample buffer boundary. The final byte `64` (`d`) has no stop bit in the file, and its annotation ends 24 samples past EOF.

## Findings

### F1 — Framing-error annotations are computed then discarded; leading bytes appear as valid data (observed; mechanism from source)
- Observed in the `.sr` (my decode, `independent-decode.out.json` field `frame_error_frames`):
  - Index 0, `BA`, `s0=42`: stop sample 660 = 0. Line stays low 628–692, rises at 693, then BD starts at 758.
  - Index 5, `85`, `s0=3363`: stop sample 3981 = 0. Line stays low 3949–4078 (stop bit plus one extra low bit time), rises at 4079, then `0D` starts at 4144.
  - The remaining 12,882 frames have stop = 1; the final frame has no stop sample (F2).
- Decoder source (committed `w1/_uart/libsigrokdecode-0.5.3/decoders/uart/pd.py`; runtime copy digest-identical, sha256 `51a29d0e…97da62`):
  - L398: `get_stop_bits` emits `putg([rxtx + 10, ['Frame error', …]])`.
  - L147: annotation class 10 is `rx-warnings`. L146: `rx-data` is classes (0, 2, 4, 6, 8).
  - L312–L318: the `DATA` / `rx-data` output is emitted at the 8th data bit, before the stop-bit check.
- Run argv (`decode-official-uart.run.json`, `argv[7]`/`argv[8]`): `--annotations`, `uart=rx-data`. The envelope's `annotations_text` contains only `uart-1: XX` lines; no `Start`, `Stop`, or `Frame error` lines.
- Inferred: sigrok emitted `Frame error` for indices 0 and 5 and the class filter removed them. The direct emission is not observed (no run was performed).
- Consequence: the envelope presents `BA` and `85` as ordinary `rx-data`. No field records them as anomalous.
- Unknown: cause of the stop-bit low (device boot transient, line glitch, or framing). Not determinable from retained evidence.

### F2 — Exhausted display window vs truncated recording; truncation undisclosed (observed)
- `output_window`: `total_lines=12885`, `returned_lines=12885`, `has_more=false`. The line count matches my independent frame count (12,885). The display window is exhausted with no decoder-side truncation.
- `logic-1` is 8,388,608 bytes (unitsize 1, so 8,388,608 samples; `metadata`: `samplerate = 625 kHz`, `probe1 = TX`). The committed `uart-README.txt` says: "We capture as many samples as fit into the 8MByte buffer" and gives `--samples 8388608 -p '1=TX'`.
- Final annotation `8388112-8388632 uart-1: 64` is frame index 12884, `s0=8388046`:
  - Data bit 7 sample point 8388599 is inside the file.
  - Stop sample point 8388664 is outside the file (≥ 8388608), so the stop bit is never checked.
  - The annotation end 8388632 is 24 samples past EOF.
- The decoded text ends `…Hello World`, with no `!\r\n`. The recording is cut mid-message.
- The envelope has no field for sample count, samplerate, truncation, or incomplete final frame. `limitations` does not mention truncation. `has_more:false` reads as completeness but means only "no more frames".

### F3 — Channel TX binding is observational only (observed)
- `runs_per_bit`: bit 0 = 79,154 runs; bits 1–7 = 1 run each (constant 0 over all 8,388,608 samples). Only probe 1 (`TX`) carries traffic.
- Reproduction (annotation match) at bit 0, 625 kHz, 9600 baud confirms the channel binding empirically.
- The README's probe table ("0 (green) TX") and `-p '1=TX'` are consistent with 1-based probe naming. That naming convention is INFERENCE; the reproduction is the observed binding.
- Not retained in the envelope: probe map, samplerate, unitsize, sample count. Option defaults not recorded: `data_bits=8`, `parity=none`, `stop_bits=1.0`, `bit_order=lsb-first`, `format=hex` (committed `pd.py` option table). `8n1` in the filename is therefore unbound by the envelope, though consistent with the output.

### F4 — Source linkage and authority label not evidenced in the evidence graph (observed)
- Envelope: `evidence_links: []`, `relationship_coverage: null`. The `.sr` provenance receipt is a standalone file, not linked.
- `official-download.json`: status 200, size 58381, sha256 matching the `.sr`, `captured_at 2026-10-21T14:38:57.638074+00:00`. No command, headers, or ETag.
- `fetches.json` lists only `sigrok-cli.1` and `uart-README.txt`. It has no `.sr` entry.
- The README (sha256 `7af1c784…6f66`, matches its fetches entry) was accessed 14:41:40, about 2 min 42 s after the decode run (`captured_at 14:38:58.876480`). The capture-parameter source postdates the decode.
- `authority: "shipped-artifact"`: no retained provenance supports "shipped". The artifact is a third-party community capture pinned by URL to commit `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0`. Upstream content is not verifiable offline (U).

### F5 — Claimed executables and adapter partly unbound (observed)
- Bound: wrapper `tools/sigrok-cli.sh` sha256 `50fe4359…3470902` (envelope `tool.sha256`) equals the committed script. The wrapper sets `LD_LIBRARY_PATH`, `LD_PRELOAD`, `PYTHONPATH`, `SIGROKDECODE_DIR`, so those are bound through the wrapper digest.
- Bound: `resource_limiter.sha256` (`/usr/bin/prlimit`, `092bb6db…fff96`) equals the current host binary. Capture-time equality is INFERENCE.
- Not retained: executed `runtime/squashfs-root/usr/bin/sigrok-cli` (sha256 `10fed05a…ccebd`); `libsigrokdecode.so.4.2.1` (`4bfe11a3…80b3`); host preload `/usr/lib/libgmodule-2.0.so.0`.
- Adapter identity `rea-agents@6.5.0` (via `npx -y`) appears only in run argv. `provider.version` names `sigrok-cli@0.7.2`, not the adapter. No integrity hash. Unbound (U).

### F6 — "Effective limits are reported" overstated (observed; low)
- `limitations` says the prlimit ceilings preserve stricter inherited limits and that effective limits are reported.
- Retained values (`limits`, `resource_limiter.arguments`) are the requested constants (e.g. `--as=1073741824:1073741824`). Post-min effective values and inherited limits are not recorded.
- No limit was approached (input 58 KB, 0.66 s, stdout 362 KB). No effect on this output.

### F7 — Stderr retention unverifiable (observed; low)
- `diagnostics` holds three Python PYTHONHOME warnings. The run JSON `stderr` is `""`. Whether the adapter captured all producer stderr is unverifiable from retained data.

### F8 — `evidence_id` not recomputed (unknown; low)
- `ev_1d361f25…c67e5c`. Four canonical JSON forms of `data` and the whole file were tried; none matched. The canonicalization is not in the committed lane sources, so the id is unverified.

### F9 — Private copy and locator fields (observed; low)
- `limitations` states "only a private copy of the selected file is decoded". No copy path or digest is retained.
- `subject.local_path`, `parameters.path`, `artifact.path`, and `locations` all point at the moving worktree. They are locators, not content bindings. The digest is the binding.

### F10 — Verified, no defect (observed)
- `run.stdout` (362,104 bytes) is byte-identical to the envelope file (sha256 `7d5e07cc…8358e`).
- `ok:true`, `exit 0`, `hardware_acquisition: not-performed` (consistent with argv; no device access).
- `limits` values are arithmetically consistent with `resource_limiter.arguments`.
- `annotations_text` line count and `output_window.total_lines` both equal 12,885.

## Claimed-field binding table

Status: **B** bound by my re-derivation; **R** retained, not independently bound; **N** not retained; **U** unverifiable offline; **X** overstated or mislabelled.

| Field / claim | Status | Evidence |
|---|---|---|
| `subject.digest.sha256`, `artifact.sha256`, `artifact.bytes` | B | `.sr` sha256 `01b726…900b61`, 58381 bytes (git show) |
| `parameters.decoders` `rx=TX` (channel TX) | B (by reproduction) / N (map) | bit 0 only active; reproduction 12885/12885; probe map not retained (F3) |
| `annotations_text` (12885 lines) | B | 0 mismatches vs independent decode (`independent-decode.out.json`) |
| `parameters.annotations` `uart=rx-data` (FE hidden) | N for FE | class 10 excluded; run argv[8] (F1) |
| `output_window` `has_more:false` as recording completeness | X | recording truncated at 8388608 samples; final frame incomplete (F2) |
| `limitations`: truncation, incomplete frames | N | not mentioned anywhere in envelope |
| `tool.sha256` (wrapper) | B | `50fe4359…3470902` = committed `tools/sigrok-cli.sh` |
| `tool.version_banner` / `provider.version` | R (text); N (binary sha) | runtime `sigrok-cli` `10fed05a…` not retained (F5) |
| decoder module identity (libsigrokdecode 0.5.3) | B now / N in envelope | runtime `pd.py` `51a29d0e…` = committed source |
| `resource_limiter.sha256` (prlimit) | B now | host `092bb6db…` = retained digest |
| `resource_limiter` / `limits` "effective limits reported" | R, X-lite | requested values only (F6) |
| `provider` adapter (rea-agents@6.5.0) | U / N in envelope | argv only; no integrity (F5) |
| `diagnostics` = "all producer stderr" | U | run `stderr: ""`; no raw capture (F7) |
| `authority: shipped-artifact` | X / U | third-party community capture; receipt self-attested (F4) |
| `evidence_links`, `relationship_coverage` | N | `[]`, `null`; `fetches.json` omits `.sr` (F4) |
| `evidence_id` | U | 4 canonical forms, no match (F8) |
| `meta.duration`, `captured_at` | U | no independent timing receipt |
| "only a private copy decoded" | N | no copy path/digest (F9) |
| `subject.name` "8n1" framing | N (options) | `data_bits/parity/stop` not retained; defaults 8/none/1; consistent with output (F3) |

## Leading-byte timeline (observed; `independent-decode.out.json` `leading8`)

| idx | byte | start sample `s0` | envelope annotation | stop bit | note |
|---|---|---|---|---|---|
| 0 | BA | 42 | 108-628 | **0 (FE)** | stop low 628–692, idle 693–757 |
| 1 | BD | 758 | 824-1344 | 1 | 1 idle bit before (gap 11) |
| 2 | C9 | 1410 | 1476-1996 | 1 | |
| 3 | B1 | 2061 | 2127-2647 | 1 | |
| 4 | 91 | 2712 | 2778-3298 | 1 | |
| 5 | 85 | 3363 | 3429-3949 | **0 (FE)** | low 3949–4078 (extra low bit) |
| 6 | 0D | 4144 | 4210-4730 | 1 | gap 12 before |
| 7 | 0A | 4795 | 4861-5381 | 1 | |

- Timing is on the exact 9600-baud grid: max edge residual 0.96 samples across the whole stream and 0.96 across idx 0–7. The FE is a bit-value anomaly, not timing drift.
- The two non-10-bit gaps in the stream (`gap_bit_times_counter`: 10→12882, 11→1, 12→1) both lie in the leading group.
- From idx 8 on, the stream is 919 exact repeats of `Hello World!\r\n` plus a final `Hello World` (11 bytes), per `tail_exact_repeats` and `tail_remainder`.

## Produced files and hashes

- `.ufo/waves/round-23/w2/OriginalPublic.md` — this report.
- `runtime/OriginalPublic/independent-decode.py` — `7cff8dd94f56e944dc824bc8a20a28f787f49065f87e033ae470e871d9ae1392`. Read-only analysis; run once: `python3 -I -B independent-decode.py hello_world_8n1_9600.sr decode-official-uart.envelope.json`, exit 0.
- `runtime/OriginalPublic/independent-decode.out.json` — `242801ad347db9bf4ed95cfbf6cf2c23d606c42965897175b9ba7af0b57a6f39`.
- Committed-byte copies (git show, sha verified):
  - `hello_world_8n1_9600.sr` `01b72610…900b61`
  - `decode-official-uart.envelope.json` `7d5e07cc…8358e`
  - `decode-official-uart.run.json` `0bdd0026…4b62b`
  - `uart-pd.py` (committed w1 source) `51a29d0e…97da62`
  - `sigrok-cli.sh` `50fe4359…3470902`
  - Other scratch copies (not analyzed): `count-c1.py`, `make-uart.py`, `describe-signals.py`, `setup-sigrok.py`, `uart-README.txt`, `fetches.json`, `official-download.json`, `generate-uart.run.json`, `decode-invalid-decoder.*`, `decode-uart-hi.*`, `uart-help.*`.
- No production, peer, jj, index, or fleet file was modified.

## Installs or none

None. Used `git` (read-only: `show`, `ls-tree`, `rev-parse`, `check-ignore`), `sha256sum`, `python3`, and `/usr/bin/prlimit` hash only. No pacman, npm, uv, or cargo activity.

## Open risks and verification gaps

1. Upstream `sigrok-dumps` content at `c8fad05…` is not re-fetched (offline contract). Provenance rests on the self-attested receipt and digest equality.
2. Runtime digests (`sigrok-cli`, `libsigrokdecode`, `pd.py`, `prlimit`) are current-state, not capture-time. Equality is observed now; capture-time equality is INFERENCE.
3. Cause of the leading FE stop bits (BA, 85) is unknown. No hardware re-acquisition is permitted.
4. Counting consequence for L1: the 12,885 `rx-data` annotations include two framing-error bytes and one incomplete final byte. Whether these count as clean sourced bytes is a judgement for L1. The envelope itself carries no marker for them.
5. The worktree copy at `evidence/c1/` was not compared to the committed blob (contract forbids reading worktree bytes as candidate).
6. `evidence_id` canonicalization not located; id unverified.
7. Not run: `count-c1.py`, producer replay, tests, builds, linters. Only the read-only analysis script above was executed.
8. W1 proposal findings are outside this seat's assignment and were not re-evaluated against `2838351450…`.

Report: .ufo/waves/round-23/w2/OriginalPublic.md
