# Source059 — S059 row, pinned README, and Gate (R23-C1 source review)

Seat: `KaidokuR23.Source059` (spec item `Source059`). Candidate: `2838351450ff1ee4baa620c962a1153450d53311`. Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
Method: committed bytes only, read via `git show`, `git grep`, `git ls-tree`, `git cat-file`, and `git hash-object` (no `-w`). The retained README and the 0.7.2 manual were staged into the ignored runtime directory. No REA, sigrok, or npx execution. No count-tool run (`count-c1.py` was read only). No network access. No installs.

## Verdict
- **Identity and pins: PASS.** The URL, commit `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0`, README sha256 `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66`, and size 1277 B agree across `corpus/SOURCES.md:65`, `.ufo/waves/round-23/evidence/sources/fetches.json`, and the retained bytes.
- **One-way acquisition provenance: PASS as attribution.** The row scope, the Gate decision, and knowledge line 70 all attribute capture to the dataset author. None claims lane acquisition or lane execution.
- **Exact TX and samplerate facts: NOT SUPPORTED as written.** The README gives a baud-band rate table and a TX probe name. It does not assign 625 kHz or 9600 baud to `hello_world_8n1_9600.sr`. The Gate locates only the one-way sentence. The README spells the TX channel two incompatible ways. The recorded decode uses the decoder's `rx` role for the device TX line.

## Findings

Severity: H, M, or L. Status: **observed** (read from bytes), **inferred** (reasoned, not observed), or **unknown**.

### F1 · M · observed (text) + inferred (file mapping) — baud and sample rate attributed to the recording
- Row `corpus/SOURCES.md:65`, teaches cell: "The supplied third-party recording documents one-way UART, TX channel and625kHz at9600baud". Knowledge `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:68–69`: "S059's author describes one-way UART from an Olimex board,625kHz at9600baud and TX channel."
- Retained README `.ufo/waves/round-23/evidence/sources/uart-README.txt` (sha256 `7af1c784…f66`), lines 22–23, is a band table: "sample rate of 5MHz (for baud rates 921600 - 230400), 1MHz (115200 - 19200), and 625kHz (9600 - 1200)". Line 35 is a template, `-d 0:samplerate=<hz>`. The retained bytes contain no `hello_world_8n1` and no `8n1/`. `9600` appears once, at line 23.
- The README never names the recording and never assigns it a baud. The 9600 and the 8n1 come from the filename `uart/hello_world/8n1/hello_world_8n1_9600.sr` (knowledge line 65), not from S059.
- The row says the recording "documents" these facts. Only the README can document them. The scope's "UART settings" is likewise just the README's example list (line 7: "such as 8n1, 8o1, 8e1, 7o1, 7e1, etc.").
- Re-evaluated stale W1 claim: `w1/CriticSource.md:64` ("captured at 625 kHz") makes the same overreach.
- Suggested wording: "README lines 22–23 give 625kHz for 9600–1200 baud; the 9600 of hello_world_8n1_9600.sr comes from its filename."

### F2 · M · observed — the Gate does not locate the TX or rate facts
- `corpus/lessons/round-23.md:17` locates one quote for S059: README line 5, "This is a collection of example UART communication (only in one direction)." It is byte-exact, 12 words, admitted as "dataset provenance/selection facts."
- The row's anchor cites "introduction and Logic analyzer setup" (`SOURCES.md:65`). The row's teaches cell and knowledge lines 68–69 assert TX and 625 kHz at 9600. None of those is located in the Gate.
- Gate rule (`corpus/lessons/round-23.md:8–11`): "Quotes are contiguous, located…". Byte-verified contiguous candidates: `625kHz (9600 - 1200):` (README line 23), `  0 (green)   TX` (line 27, three spaces), and `-p '1=TX'` (line 35).

### F3 · M · observed + inferred — TX channel spelled two ways; the README command is not 0.7.2 syntax
- README line 27 (probe table): `0 (green)   TX`. README line 35 (command): `-p '1=TX'`.
- Retained 0.7.2 manual `.ufo/waves/round-23/evidence/sources/sigrok-cli.1` (sha256 `e3f06dfe…5f9`; matches `fetches.json`):
  - `-C, --channels <channellist>` at line 191.
  - "sigrok always names the channels according to how they're shown on the enclosure of the hardware. If your logic analyzer numbers the channels 0\-15, that's how you must specify them" at lines 194–196.
  - Example `--channels 1=CLK,2\-4,7` at line 210.
  - A search for `\-p` and for `probe`/`probes` returns no hits.
- The README's `-d 0:samplerate=…` is also not the manual's syntax. The manual has `-d, --driver <drivername>` at line 36 and `-c, --config samplerate=…` at line 72, with examples at lines 89–99.
- Observed: under the manual's enclosure-numbering rule, `1=TX` and `0 (green)` disagree.
- Inferred: `-p 1=TX` used 1-based probe numbering from an older sigrok. That would reconcile lines 27 and 35 for that older version only. Unverified here.
- Consequence: "TX channel" as a name is safe in the row. Any numeric TX index is unresolved by S059.

### F4 · M · observed (label mismatch) + inferred (impact) — the recorded decode uses the decoder's RX role for the device TX line
- README line 11: "The USART1 (USART1.TX pin) is used." The recorded line is the device's transmit line.
- Retained decoder help `.ufo/waves/round-23/evidence/c1/uart-help.envelope.json`, `.data.normalized_result.help_lines[46]` = "Optional channels:", `[47]` = "- rx (RX): UART receive line", `[48]` = "- tx (TX): UART transmit line".
- Official decode `.ufo/waves/round-23/evidence/c1/decode-official-uart.run.json`: argv contains `--decoders 'uart:rx=TX:baudrate=9600' --annotations 'uart=rx-data'`; exit 0. Knowledge lines 72–73 call this the "exact … request … succeeded." No line in the knowledge entry or in S059 gives a reason for the `rx` role. Knowledge lines 30–31 say TX is "another supported direction."
- Inferred: the framing decode is probably role-agnostic, so the decoded bytes are probably unaffected. The RX label and role still contradict the S059 TX fact and the decoder's own TX role. The decoder source is not retained, so this is unverified. Route to the SignalEntry item to justify or correct. Not re-run here.

### F5 · L–M · observed — the "Release commit" and "Official" labels have no retained receipt
- `SOURCES.md:65` anchor: "Release commit c8fad0528648ba58ceddbda9e34e4dfcd293a6b0". Source: "Official sigrok-dumps UART dataset README".
- The retained README contains neither "official", "release", nor "tag" (byte search: all absent).
- `fetches.json` holds two entries only, for sigrok-cli.1 and the README. There is no tags or commit API receipt.
- The only support is `w1/SignalCarrierAlternatives.md:17–19`: "official tag `sigrok-dumps-0.1.0` → commit c8fad05… Observed via GitHub tags API and commit API." That is narrative, not a retained receipt. Lines 13–16 cite a root README at a different commit, `6bf0de22…`.
- Fix: retain the tag and commit receipts, or relabel the anchor "pinned commit (URL path)" and drop "Official".

### F6 · L–M · observed — tier "A" is not defined in the retained docs
- `SOURCES.md:65` tier cell = `A`. Searches of candidate `corpus/README.md`, `corpus/SOURCES.md`, and `corpus/*.md` found no A/B definition.
- `.ufo/waves/round-23/tools/count-c1.py:107` admits only `row[4] in ('A','B')`. Cells are stripped at `:87`. As coded, S059 passes: tier A, status mined, opened 2026-10-21, and used-by contains the knowledge path. This is observed by reading; the counter was not run.
- Risk: a tier label alone satisfies the eligibility gate for a third-party dataset README.

### F7 · L · observed bytes — missing spaces in the S059 row and the knowledge entry
- `SOURCES.md:65` anchor: `opened2026-10-21`. Teaches cell: `and625kHz at9600baud`. The bytes are ASCII. The only non-ASCII character in the row is U+2014, at character index 51, so no hidden whitespace is involved.
- Knowledge line 69: `board,625kHz at9600baud`. Knowledge line 41: `baud9600`, `at960000Hz`.
- Impact: word-boundary matches fail (`\b625kHz\b` and `\b9600\b` do not match inside `and625kHz` or `at9600baud`). count-c1 reads only cells 4, 8, 9, and 11, so there is no count effect. Observed by reading.

### F8 · L · observed — "still require their own retained run" is stale
- `SOURCES.md:65`: "decoded annotations still require their own retained run." The run exists in this round: `evidence/c1/decode-official-uart.run.json` (exit 0) and envelope `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` (knowledge lines 72–73).
- Suggested wording: "S059 supplies no decoded annotations; decoding is the lane's own retained run."

### F9 · L · wording risk — the "acquired" heading
- `knowledge:62` "## Selected third-party acquired recording". Read alone, "acquired" suggests lane acquisition. Lines 69–70 disclaim that. Suggest "third-party-captured recording". No claim changes.

## Pass checks (observed)
- P1 Identity: `SOURCES.md:65` URL = `fetches.json` URL (status 200; size 1277; sha256 `7af1…f66`; accessed `2026-10-21T14:41:40.337220+00:00`). The retained blob `57365d63825e30abfdc19362d0c8c1da03312535` is reproduced by `git hash-object` (no `-w`).
- P2 Gate quote: `corpus/lessons/round-23.md:17` equals README line 5 byte-for-byte; 12 words against a limit of 25.
- P3 Attribution: `SOURCES.md:65` scope ("Dataset author's declared origin … not independently observed hardware acquisition or lossless decoding"), `lesson:17` decision, and `knowledge:70`.
- P4 Used-by: both `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` and `corpus/lessons/round-23.md` exist at candidate and name S059 (`knowledge:1`, `lesson:17`).
- P5 W1 consistency: `w1/SourceRegistry.md:58` and `w1/PlannerDataWalk.md:53` match the README sha256 and retained path.
- P6 Paraphrase: "one-way" (README line 5) and "Olimex" (README line 9, "Olimex STM32-H103 eval kit") are faithful in knowledge line 69.

## Produced files and hashes
- `.ufo/waves/round-23/runtime/Source059/README.bytes` (ignored via `.ufo/waves/round-23/.gitignore:1`): sha256 `7af1c7841a603eb1f6dfecbe1402acd980e175e7e31cd62daf2fe2a0caed6f66`, 1277 B.
- `.ufo/waves/round-23/runtime/Source059/sigrok-cli.1.manual` (ignored): sha256 `e3f06dfef230760a012dc1e5d37e049fe8ba4e6bdb718b8230b28da7ca64a5f9`, 19180 B.
- `.ufo/waves/round-23/w2/Source059.md`: this report.

## Installs or none
None. No package, tool, or runtime was installed or updated. Only `python3 -I -B` stdlib reads and read-only git plumbing were used.

## Open risks
1. The upstream identity of commit `c8fad05…` rests on the lane's fetch receipt. It was not re-fetched, because network access is excluded by contract.
2. Recording-level sample rate, probe name, and baud are not established by S059. They need the committed `.sr` metadata, which is the PublicDownload item. W1 `w1/PlannerDataWalk.md:80` claims "probe1 = TX, 625 kHz, 8n1"; that is unverified here.
3. The F4 impact is inferred, and the decoder source is not retained.
4. The tier-A policy is undefined in the retained docs (F6).
5. Stale W1 S059 claims remain committed: `w1/CriticSource.md:64`, `w1/CoverageMap.md:259`, `w1/ConnectOutsideDebt.md:85`, and `w1/SignalCarrierAlternatives.md:17–19`. They were not edited, because peer reports are read-only for this seat.
