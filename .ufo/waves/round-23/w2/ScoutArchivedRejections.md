# R23-C1 archived refusal and invalid-decoder findings

Candidate source: `2838351450ff1ee4baa620c962a1153450d53311`; frozen baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`. Candidate source bytes were read with `git show <candidate>:<path>`, not from the moving worktree.

## Findings

- **[OBSERVED — frozen denominator and boundary]** Candidate `.ufo/waves/round-23/claims.json:14-29` fixes the same six T1 verbs, `before: 1`, `total: 6`, improvement target `>=2/6`, and completeness only at `6/6`; it explicitly forbids counting a refusal. Candidate `corpus/lessons/round-23.md:33-36` explicitly retains the invalid-decoder `execution_failure` and the prior Dart refusal as rejected held witnesses. The candidate lesson's recorded initial measurement says cumulative `1/6→4/6` and both original R22 counters remain `1/6` at `:90-96`; I did not run a counter or treat that report as independent admission.

- **[OBSERVED — R22 Dart refusal retained verbatim]** `.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.run.json:2-17` records `inspect-dart-aot`, exit `1`, stderr empty, producer `KaidokuR22R L1 recovery, not inherited W1`, and artifact SHA-256 `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`. Its stdout and paired `inspect-dart-aot-saber.envelope.json:1` report `unsupported_target` / `No recognizable Dart snapshot symbols`, listing the four absent legacy dynamic symbols (`_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`, `_kDartIsolateSnapshotInstructions`). The archived run JSON SHA-256 is `d1eaa23f96ec4a9695af4f373051da8ad3e87fc3dff3bbee083eed5eaf2eb34a`; envelope SHA-256 is `2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145`.

- **[OBSERVED — R23 invalid-decoder attempt retained verbatim, not a positive]** `.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.run.json:2-24` records `decode-signal-recording` against `uart-hi.bin`, decoder `round23_nonexistent_decoder`, explicit binary input format, `REA_SIGROK_COMMAND` wrapper, and exit `1`. Paired `decode-invalid-decoder.envelope.json:1` returns `execution_failure` for `decode_signal_recording`, with provider diagnostics including Python prefix warnings and `No module named 'round23_nonexistent_decoder'` / `Failed to load protocol decoder`. This is an observed failed request, **not** proof of an `invalid_request` validation branch or missing-provider behavior. Candidate lesson `corpus/lessons/round-23.md:24-26` also says the newer upstream `invalid_request` description cannot replace this 6.5.0 observation; candidate knowledge `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:84-88` marks it a rejected held witness. Run JSON SHA-256: `518181aa69dfc844601dbec60f7b8794bbde769d27a075e428398a214e45262c`; envelope SHA-256: `04697e72e9cabc9dae1385731ea3f2becf8a4bb94dc2334f067180b3b1008292`.

- **[OBSERVED — exact receipt pairing]** For each pair, `jq -rj .stdout <run.json | sha256sum` equals the paired envelope's `sha256sum` exactly (R22: `2b13cb8...c5c145`; R23: `04697e72...008292`). Raw stdout and envelope byte counts also match (1121 R22; 991 R23). This confirms the retained envelope bytes are the exact captured stdout, not a re-rendered substitute.

- **[OBSERVED / INFERENCE boundary — source generation]** The pinned synthetic fixture generator `.ufo/waves/round-23/tools/make-uart.py` is explicit at candidate lines `2-7,17-27`: it forms ASCII `Hi` frames with two leading idle bits, 100 samples/bit at 960 kHz, 9600 baud, LSB-first data and three final idle bits; its recorded run `.ufo/waves/round-23/evidence/c1/generate-uart.run.json:2-11` reports the fixture digest and `acquisition: synthetic; no hardware`. The candidate knowledge entry labels the claim that REA's two hex annotations agree with the planted payload under those settings as **inference** (`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:37-60`).

  For the **third-party** `hello_world_8n1_9600.sr`, the retained S059 README (`.ufo/waves/round-23/evidence/sources/uart-README.txt:5-11,22-27`) attributes repeated “Hello World” traffic to an Olimex STM32-H103/libopencm3 example on TX and describes the analyzer/sample-rate setup. This is source-author attribution, not this lane observing the hardware or acquisition (candidate knowledge `:64-82`; candidate lesson `corpus/lessons/round-23.md:16-17,29-36`). The actual decode begins `BA,BD,C9,B1,91,85,0D,0A` before the first matching “Hello World” sequence at sample 5512 (candidate knowledge `:72-82`). **[INFERENCE / UNKNOWN]** The cause of those leading annotations and a complete, independently evidenced explanation of this recording's generation/acquisition remain unresolved; the text prediction was recorded as false, not explained away.

- **[OBSERVED — candidate source identity]** `git show 2838351450ff1ee4baa620c962a1153450d53311:corpus/lessons/round-23.md` yielded the cited candidate lesson (SHA-256 `8327a21fbae3c976af820e10063d973f1862a945a041d4b02a90906700a70723`). Pinned `tools/make-uart.py` content SHA-256: `8720ee4e5afdfd66630fe4f357aec1a574b1fe2ff7bb367c5284079ff1ab6c3c`.

## Verification boundary and open risks

- No counter, REA replay, target execution, test/build/lint/format command, hardware/device/process access, or external access was performed. The candidate's reported counts above are cited as source assertions only.
- The LSP device is unavailable (`read xd://lsp` returned “No such tool”; the mounted-tool inventory contains no LSP route). This scoped evidence is Markdown/JSON rather than a source-level exported code contract, so no LSP definition/reference result is claimed; grep results were used only to locate relevant sections.
- Outside admission remains unclaimed; the R23 author-side status and unresolved source-generation/acquisition attribution remain open.

## Produced files and hashes

- This report: `.ufo/waves/round-23/w2/ScoutArchivedRejections.md` — SHA-256 is reported in the handoff (not embedded to avoid self-reference).

## Installs

- None.