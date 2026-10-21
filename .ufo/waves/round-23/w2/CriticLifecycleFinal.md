# CriticLifecycleFinal — R23 W2 critic (author-side, not outside verification)

Seat `KaidokuR23.CriticLifecycleFinal`, critic, source review only. Candidate `C=2838351450ff1ee4baa620c962a1153450d53311`, B=`aa1450b8…`.
Objects attacked: `wave1-outcomes.json` at C (sha256 `b88db5f6…6a96`), the R22 receipt `w1/CriticLifecycle-r22w1-receipt.json` at C (`0ef557fe…00eb`), and the LOG, SCORECARD and lesson text that summarizes both.
Everything was read with `git show C:PATH`, plus read-only parsing of the retained seat transcripts under
`S=~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22`.
No suite, counter, producer, REA, target, device, or network was run. No tool was installed.

## Bottom line

R23-C1 is not affected. The count uses only L1 envelopes. No knowledge entry at C cites `connect-dart-symbols/` with the full evidence prefix, and no source was borrowed from a W1 seat.

The record and its prose overclaim on all three attacked axes:
- **Dead seats.** Two dead seats were resumed by peer messages, and one of them is recorded with the wrong terminal error.
- **Known error vs unexplained mechanism.** In R22, 32 seats are called "capacity-retrying", but they had stopped retrying. They belong with the 48 aborts as unexplained stops. Only 13 seats are known own terminal failures.
- **Scope deviations.** The record names only ConnectDartSymbols. The committed candidate also carries 337 third-party files and counter outputs written by read-only seats, and none of it is marked as a deviation. One seat describes its deviation as compliance.

## Findings

### F1. "No dead-seat replacement" holds; "not resumed" does not (observed)

What holds:
- The parent made no respawn. Its only agent-message writes are `KaidokuR23.jsonl` line 254 (to CriticLifecycle, receipt request), line 328 (ConnectDartSymbols stop), and line 423 (a six-seat close message at 14:52:30Z, none of them dead seats).
- The 128 transcripts under `$S/KaidokuR23/` are exactly the 64 W1 names plus the 64 W2 names.
- The only suffixed id is `CoverageMap-2`. It is the W2 seat named CoverageMap, not a W1 respawn. The W1 CoverageMap reported.
- `replacements: 0` is correct for spawns.

What does not hold. Two seats that were terminal at the `wave1-terminal-2.json` cutoff (14:36:43Z) received peer messages and ran again:

| Dead seat | Woken by | Then |
|---|---|---|
| `SourceDartSnapshots` (transcript sha256 `687817f8…c258`) | IRC from `KaidokuR23.CriticSource` at 14:40:10.282Z (line 11) | `model_change role:fallback` to `openai-codex/gpt-6-luna` (line 12), four Codex capacity errors, then "Retry budget exhausted after 5 retries" at 14:40:26.361Z (line 21) |
| `BuildSignalRunner` (`a6073ed5…6d29`) | IRC from `KaidokuR23.SchemaSignalDecode` at 14:42:53.505Z, permitted by that seat's prompt in `gen-wave1.py` | A second full Luna retry ladder, ending exhausted at 14:43:06.106Z |

Neither seat produced output, so no credit leaked. But the mechanism that would have leaked credit is visible: a sibling message can restart a dead seat on a fallback model. If that seat had then written `w1/<Seat>.md`, it would have been counted `reported` under `replacements: 0`. The record has no field that can tell such a seat apart.

Contradicted text:
- Lesson line 61: "Dead seats are not resumed or replaced".
- Lesson line 61: "all eight scribes died with Anthropic429". Seven did. SourceDartSnapshots' final failure is Codex capacity.

### F2. A recorded "known error" is stale and names the wrong provider (observed)

`wave1-outcomes.json` at C gives `SourceDartSnapshots.terminal.last_error` as `[anthropic/claude-haiku-5-5] 429 …`. That text was copied from the 14:36:43Z snapshot, but the outcomes cutoff is 14:58:05Z. The transcript's actual last error is the Luna retry exhaustion at 14:40:26Z, and the answering identity changed in between.

SCORECARD line 2844 says "12 named provider failures". That number counts correctly but names one of them wrongly.

The record also has no answering-model field. At C, 46 of the 52 reporting seats finished on a model other than the one they were routed to:
- 30 seats routed to `commandcode/deepseek` finished on `opencode-go/deepseek`.
- 14 seats routed to `devin/swe-2` finished on `openai-codex/gpt-6-luna`.
- 2 seats routed to `devin/swe-2` finished on `zai/glm-5.3-flash`.

No claim depends on the answering model, so this is a provenance gap and not a credit error.

### F3. R22: the 32 "capacity-retrying" seats were not retrying; the unexplained set is 80, not 48 (observed counterexample, mechanism unknown)

First, the receipt reproduces:
- All 93 transcript sha256 values match, and the parent `KaidokuR22.jsonl` still hashes to `38e501dd…b8ba`.
- An independent reclassification gives 48 seats with `stopReason:aborted`.
- The 13 parent-notified seats are exactly the 13 `<task-result … status="failed (exit 1)">` ids at parent lines 157 and 159.
- The remaining 32 seats have errors only.

The counterexample for those 32 `openai-codex/gpt-6-luna` seats:
- **R22 behaviour.** Each has exactly two capacity errors, 0.48–0.87 s apart. The last one falls between 11:57:35.9 and 11:57:36.797Z. After that there is no event for about 7 minutes, until the dispose.
- **R23 behaviour on the same runtime.** Runtime 18.12.5 is recorded on every line in both rounds. Here the Luna retry ladder runs at gaps of 0.53–0.64, 0.86–1.04, 1.6–2.1, 4.0–4.4 and 6.2–7.2 s, then reports "Retry budget exhausted" within about 15 s. This holds for all four R23 Luna seats.
- **Timing.** The shared abort instant, 11:57:37.180Z, falls 0.383–0.819 s after each of the 32 seats' last error. That is inside their next backoff window, and none of them attempted again.
- **Direct witness.** `KaidokuR22.ExecDartAotX64-4` (`22fc533f…fe9b`) is a Luna seat with one capacity error at 11:57:36.636Z, then `aborted` "Request was aborted" at 11:57:37.180Z. A seat that was mid-ladder was cut at the shared instant.

Consequences:
- The receipt's per-row facts are accurate.
- Its inference line "32 seats observed provider capacity errors independent of parent" is not accurate, and neither is its addendum claim "45 seats show their own provider failures, independent of the parent". The capacity errors were not terminal. What ended these seats is unobserved, just as for the 48.
- LOG line 2630 "32 capacity-retrying seats" and lesson line 51 "32 retrying-capacity seats" present an unobserved state as observed.
- The defensible split is:
  - 13 known own terminal failures (Haiku 429, with the parent notified).
  - 80 seats whose stop mechanism is unexplained. In 48 of them it was recorded as an abort. The other 32 show a halted retry ladder with no recorded event.
  - All 93 have the dispose mechanism unexplained.
- [INFERENCE] One cancellation at 11:57:37.180Z stopped both groups. It was recorded as an abort only for requests that were in flight. This is not established from harness code.
- Credit is unchanged: all 93 seats have 0 tokens and 0 reports.

### F4. Two committed W1 authorities disagree on R22 per-seat evidence (observed)

`w1/recount-102.json` at C (sha256 `f0f34ece…cda8`, the digest pinned by `HistoricalSeatEvidence.sha256`) has:
- `per_seat_terminal_notification_receipts: 0`
- `unknown_per_child_w1: 93`
- the note "W1 has no per-seat terminal notification"

This is falsified by parent lines 157 and 159, which carry 13 per-seat failed notices.

Lesson row 51 cites both the receipt and the "HistoricalSeatEvidence recount" as evidence, without saying which one supersedes the other. The recount's `generated_at_utc` is also a hand-typed literal: the transcript shows `sed -i` changing `14:40:00Z` to `14:40:48Z` in `recount-102.py` at 14:40:51.960Z. It is an authored value, not a clock observation.

### F5. Scope deviations committed at C are not marked as deviations (observed; detection partly heuristic)

The W1 contract (`gen-wave1.py` context at C) says: "Read-only seats write only their own report", "All seat-written paths MUST be inside …/round-23/", "Skip all builds/tests … unless explicitly assigned", and sandbox clones are for executors only.

All 52 reporting seats wrote their own report path in their own transcript, so no report is borrowed. The non-report writes and runs at or around C are below. LOG, SCORECARD, the lesson and `wave1-outcomes.json` mention none of them (`git grep` for `_uart|tmp-counter|recount-102|worktrees/AppImageLibraries` returns no lines).

| Seat (role) | Deviation | Committed at C? | Seat's own report |
|---|---|---|---|
| UartSemantics (scout) | `curl` fetch and extract into `w1/_uart/`: **337 files, 5,639,996 bytes** of third-party tarballs and source trees | yes (in `6615aea`) | lists files and hashes; no deviation label |
| CoverageMap (scout) | created `w1/.tmp-counter/` and ran the R22 and R23 `count-c1.py` (3 runs) | yes, 5 files | lists them as "Raw outputs"; no deviation label |
| HistoricalSeatEvidence (scout) | wrote and ran `w1/recount-102.py`, `.json` and `HistoricalSeatEvidence.sha256` | yes | not labelled a deviation |
| CounterRefusals (scout) | `CounterRefusals.md.sha256` sidecar; ran the R22 counter | yes (sidecar) | sidecar disclosed |
| AppImageLibraries (scout) | `git clone --shared` sandbox under `worktrees/AppImageLibraries` (executor-only privilege); payload extraction | ignored, not committed | says **"Lane bounds kept … no repo or production-lane writes"**, which describes the deviation as compliance |
| PlannerDataWalk (scout) | ran the AppImage `--appimage-extract` in `/tmp`; `curl` into `/tmp`; ran the R23 counter into `/tmp` | no | no `/tmp` mention |
| ConnectCounters (connector) | ran the R22 counter (3 runs) | no | — |
| ConnectDartSymbols (connector) | `evidence/c1/connect-dart-symbols/` (committed in `2b40aec`) | yes | disclosed |
| about 20 seats in total, including critics and connectors | writes under `/tmp` (for example SchemaDart's `gcc` fixture build in `/tmp/kd23fixture`) | no | mostly mentioned as "scratch"; HistoricalSeatEvidence and PlannerDataWalk do not mention `/tmp` |

Further observations:
- **ConnectDartSymbols timing.** L1's stop was written at 14:45:09.342Z, but it reached the seat at 14:45:26.962Z (its transcript line 229). The seat wrote `connect-dart-symbols/README.md` at 14:45:26.960Z, 17.6 s after the stop was sent and 2 ms before it arrived. "Before L1's stop" (LOG line 2635, lesson line 52) is true only if the stop is measured at delivery. This is a further case of an instruction not being enforcement.
- **Counter exposure.** `.ufo/waves/round-22/tools/count-c1.py:110` builds `CITED` as `re.escape(EVIDENCE_PREFIX) + r"[A-Za-z0-9._/-]*"`, and the R23 `ROOTS` include `.ufo/waves/round-23/evidence/c1/`. A single full-path citation to `connect-dart-symbols/*.envelope.json` would make the deviating envelopes countable. Today only a relative mention exists (Dart entry line 31). Nothing structurally excludes them.
- **The receipt's extra-file write was authorized.** It came from parent line 254 at 14:41:18Z, but the record does not note that contract amendment.
- **Lesson line 52 undercounts.** "Several scouts used outside-lane temporary scratch or unassigned probes" leaves out the in-lane committed deviations (`_uart`, `.tmp-counter`, `recount-102.*`), the deviations by critics and connectors, and AppImageLibraries' self-certified compliance.

### F6. Re-evaluating the earlier W1 CriticLifecycle findings against C

- **F3 cursor claim is stale.** "6 cursor/default critics show no assistant turns" was a snapshot artifact. At C each has 1–4 recorded turns with tool calls and an own-report write.
- **F4 empty-file concern is resolved.** The record now counts only nonempty files and pins byte counts and sha256. I re-hashed all 52 `report_sha256` values against C and against the worktree: 0 mismatches.
- **F4 binding gap remains.** There is still no per-row author binding or terminal-status binding. It is resolved in fact at this cutoff, because every report was written by its own seat, but not in the record's schema.

## Impacted axes

- **Calibration:** affected by F3, F4 and the F1 wording. Statements that are not observed are presented as observed.
- **Provenance:** affected by F2, the answering-model gap, and F5's unmarked deviations committed at C.
- **No-harm:** prior files unchanged. The 337 added third-party files are additive and outside the 1138-file baseline. Recorded as a risk, not a regression.
- **Coverage, R23-C1 4/6:** unaffected on current evidence.

## Smallest safe corrections (for L1; append-only, no credit change)

1. **Outcomes addendum.** Append a `wave1-outcomes-2.json` (or an addendum) that adds these per-seat fields and leaves every count unchanged:
   - `post_terminal_wakes`: SourceDartSnapshots (CriticSource, 14:40:10Z) and BuildSignalRunner (SchemaSignalDecode, 14:42:53Z).
   - SourceDartSnapshots `final_error`: Luna "Retry budget exhausted" at 14:40:26Z, after fallback.
   - `answering_models`.
   - `scope_deviations[]`, enumerated from F5.
2. **Lesson and LOG wording.**
   - Replace "Dead seats are not resumed" with: "L1 neither resumed nor replaced dead seats; two peer messages woke two dead seats, both re-failed with no output."
   - Correct "eight scribes died with Anthropic429" to seven, plus SourceDartSnapshots, which finally failed on Codex capacity after a fallback.
   - Replace "32 capacity-retrying" with "32 with non-terminal capacity errors whose retry ladder halted. The stop mechanism is unexplained, as for the 48 aborts."
   - The only known own terminal failures are 13. The unexplained-stop set is 80.
3. **Supersession marker.** Mark `recount-102.json`'s `per_seat_terminal_notification_receipts: 0` and `unknown_per_child_w1: 93` as superseded by parent lines 157 and 159 for the 13 notified seats. Do not edit the file.
4. **Lesson row 52.** Enumerate the committed in-lane deviations (`_uart`, `.tmp-counter`, `recount-102.*`, sidecars), and state that AppImageLibraries' "lane bounds kept" is a scope deviation, not compliance. Do not delete history.
5. **Risk note for the counter.** Record that the evidence-citation regex admits `connect-dart-symbols/` subpaths. Any later full-path citation of those files must fail admission, for example through a negative control. This seat makes no change.

## Produced files and hashes

- `.ufo/waves/round-23/w2/CriticLifecycleFinal.md`: this report.
- `.ufo/waves/round-23/runtime/CriticLifecycleFinal/scan_w1.py`: sha256 `ceaf017e32d35dd7cad7bfcae911afe1ac7fdaee6b2c7305bbc7b8087509ba76`. A read-only transcript scanner. It ran once with `python3 -I -B scan_w1.py scan_w1.json` and exited 0.
- `.ufo/waves/round-23/runtime/CriticLifecycleFinal/scan_w1.json`: sha256 `3577dc288d199f9b3eb295ec84690fb3463844d417fc1dabcad4ddac825b375b`. Per-seat models, turns, and write candidates. The bash write classification is regex-heuristic and contains false positives (for example `=0` targets). F5 cites only items confirmed by reading the exact transcript commands.
- All other analysis was inline read-only Python. Nothing else was written.

## Installs

None. The pacman pause was respected.

## Open risks

- Transcripts are append-only JSONL in the user session store and are not authenticated. Digests are pinned above. The W1 seats that are still idle could append more, though no W1 report differs from C at this time.
- The `/tmp` count of about 20 seats and the AppImage and `gcc` hits are regex-derived. The rows in the F5 table were confirmed individually, but the long tail was not.
- The R22 "single cancellation" explanation is still only inferred. No harness source was read.
- This review is author-side. It is not independent admission.
