# CriticLifecycle — R23 W1 critic report (author-side, not outside verification)

Seat: `KaidokuR23.CriticLifecycle` (critic, read-only). Scope: R22's "unexplained" W1 and R23 W1 seat accounting.
Rule under test: instructions are not enforcement, and a missing report never becomes credited work.
Observation cutoff: 2026-10-21T14:38:29Z. No target execution, no device access, no REA probes, no builds or tests.
Session-store root used below: `S=~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22`.

## Findings

### F1. R22 W1 is not unexplained: per-seat transcripts were retained and never read (observation)

R22's records say the per-child cause is "unknown":
- `round-22/wave1-terminal-correction.json`: "per-child cause unknown".
- `round-22/final-wave-outcomes.json` `wave1.members[*].cause`: "unknown; parent provider error is not per-child terminal proof".
- `round-23/claims.json` `inherited`: "R22 102 reportless seats remain per-seat unknown where unknown".

The "tried" lists consulted only `agent://` reads, parent `proc://`, and a `w1/` glob. They never consulted `history://KaidokuR22.*`, even though R22 W2 rows do cite `history://`.

All 93 W1 transcripts exist at `$S/KaidokuR22/KaidokuR22.<Seat>-4.jsonl`. The set digest (`sha256sum *.jsonl | sha256sum`) is `b66c2f0c97aeb3df5f58358723b3feb148ca2c5c894afbafb13d18d3319b002f`. The 93 sibling `.md` output files total 0 bytes, which is why the `agent://` reads came back empty.

Each seat's terminal state, classified by a Python pass over every assistant message and `session_exit` record:

| Class | Seats | Observed transcript facts |
|---|---|---|
| Own terminal provider failure, before parent death | 13 Haiku scribes: ScribeMistakeAdb, ScribeSearchLog, ScribeSrcAndroidAbi, ScribeSrcDartVersion, ScribeSrcFdroidApi, ScribeSrcFlutterModes, ScribeSrcGdbCore, ScribeSrcGdbMi, ScribeSrcRizinDebug, ScribeSrcSigrokCli, ScribeSrcSigrokDumps, ScribeSrcSigrokPd, ScribeSrcTshark | `anthropic/claude-haiku-5-5` 429 rate_limit_error. The parent received an `async-result` notice `status="failed (exit 1)"` (duration 5.5–5.7 s) for exactly these 13 at `KaidokuR22.jsonl` lines 156 and 158 (11:57:36.162Z and 11:57:36.717Z). |
| Provider capacity, still in retry when disposed | 32 `openai-codex/gpt-6-luna` seats: all 8 Critic*, all Exec* except ExecDartAotX64, and both Sentinel* | 2× "Codex is at capacity (turn_rate_limit_exceeded)" each, between 11:57:35.867Z and 11:57:36.796Z. No terminal event, no abort. |
| Aborted in one shared instant | 48 seats: 42 glm-5.3-flash, 2 gpt-6.1-sol, 2 grok-composer, 1 gemini-3.8-flash, 1 luna (ExecDartAotX64) | The only non-error turn is `stopReason:"aborted"`, "Request was aborted", `completedAt` = 11:57:37.180Z for all 48 across five providers. |

Facts common to all 93 seats: 0 total tokens, 0 tool calls, 0 report writes. Every seat recorded `session_exit {reason:"dispose", kind:"normal"}` between 12:04:35.967Z and 12:04:37.897Z. The parent's own `session_exit` dispose follows at 12:04:37.911Z (`KaidokuR22.jsonl` line 160, sha256 `38e501dd807c9fedf5b78d65310f2f585f1252c9718ede5f7f3ea755d63cb8ba`).

The parent's last three turns are Anthropic 429s at 11:57:36.133Z, 11:57:36.724Z and 11:57:37.171Z (lines 155, 157, 159), with retry-after-ms=10344000 (about 2.9 h).

Inferences, marked as such:
- [INFERENCE] The 48 aborts were a single cancellation signal, not 48 provider events. Five providers stopped in the same millisecond, 9 ms after the parent's third 429. The mechanism (parent turn end cancelling in-flight child requests) is not observed in the harness code.
- [INFERENCE] The dispose of all 93 seats is coupled to the parent's teardown. They all exit inside a 1.93 s window that ends 14 ms before the parent's own dispose.

Counterexamples to the round-22 and round-23 positions:
- **`wave1-terminal.json` overclaimed.** It labels all 93 `dead_parent_provider_death`, but 13 seats failed on their own terminal provider error, and the parent was notified of each before it died.
- **The correction and R23 underclaim.** "Per-child unknown" and "automatic child termination is not established" are contradicted for this event. A per-child cause is observable for all 93, and parent-coupled dispose is observed at the timestamp level.
- **The R23 plan pre-commits the verdict.** `round-23/gen-wave1.py:61` instructs ReviewReportless to "reject R22 parent-death automatic cancellation explanation using retained correction". `gen-wave1.py:86` instructs DraftMistake "unknown causes stay unknown". A seat told the answer is an instruction, not evidence. Both lines can certify a conclusion that the retained transcripts contradict.
- **"102 per-seat unknown" double-counts the unknowns.** All 9 R22 W2 reportless rows already carry a known terminal provider cause in `final-wave-outcomes.json` `wave2.members` (4 Luna/Haiku, 3 Cursor RESOURCE_EXHAUSTED, 2 Devin rate limit). The defensible inherited unknown is narrower: the abort mechanism for 48 seats and the dispose mechanism for 93.

What does not change: credit. Every R22 W1 seat produced 0 tokens and 0 reports, so the crediting conclusion "0 completed" is correct. Explaining these seats must never credit them, and calling them unknown must never erase the per-seat evidence.

### F2. R22 W1 dispatch: the admission gate was not the enforcement point (observation)

- `KaidokuR22.jsonl` line 145: `wave-slot.sh acquire` answered "granted … seats=93 live=125 pending=0 cap=240".
- Line 148, 106 ms later, the harness refused all 93: "Background job limit reached (100)".
- `wave1-dispatch-attempts.json` records tries 1–3 as refused 93 and try 4 as `refused:0`, with no `spawned` field. The spawn count of 93 exists only in `wave1-dispatch-result.txt`.

The slot ledger counts admissions it cannot enforce, and the real ceiling is the harness job cap. Seat counts must be taken from the spawn result, never from the slot grant. `final-wave-outcomes.json` does this correctly: `round_seats` = 157 = 93 + 64, and the refused batches count zero seats.

### F3. R23 W1 accounting at cutoff (observation)

There are 64 registry members (`round-23/w1/swarm-registry.json`), and 64 transcripts exist under `$S/KaidokuR23/`.

- **One report is present:** `w1/SignalCarrierAlternatives.md` (7038 bytes, sha256 `a8923e73d6f3f1431ed056af0e767384567e8ae6fae27a3b899933339192702f`). Its final turn is `stopReason:"stop"` at 14:38:13.841Z.
- **12 seats are terminally failed with 0 tokens and no report**, matching `round-23/wave1-terminal-2.json` (sha256 `82c37e79…a23c2`): 8 Haiku 429 and 4 Luna "Retry budget exhausted". My live peer roster still lists several of these as "running" (SourceSigrokUart, DraftMistake, BuildSigrok). Roster liveness is not evidence of work.
- **The answering identity changed for 30 DeepSeek seats.** Every `commandcode/deepseek/deepseek-v4.1-flash` seat got "429 You've reached your weekly usage limit … resets at 2026-10-27". Each then logged `model_change {role:"fallback", resolvedModelIsFallback:true}` to `opencode-go/deepseek-v4.1-flash`, and all later turns ran there.
- **The answering identity changed for 13 of 16 Devin reviewers.** These `devin/swe-2` seats hit "Reached free model rate limit" and continued on `openai-codex/gpt-6-luna`. That is the same provider whose capacity errors killed all 4 Luna-routed seats. At an earlier sample 3 Devin seats had no successful turn after their error; by the later sample all had recovered.
- **6 `cursor/default` critics show no assistant turns in their transcripts, including this seat, which is visibly working.** The session store does not record this provider's turns, so transcript activity cannot be a credit or liveness signal for these seats.

Consequence: none of the three available signals is safe to credit on its own. Roster "running" was wrong for at least 3 failed seats. Transcript activity is blind for 6 seats. Registry route ≠ answering model for 43 seats. The routing written in `recovery-authority.json` ("reviewer": "m_swe") does not describe who answered.

### F4. The collector's "present" test can credit work that was never done (observation from source)

`ufo-fsd-alpha/scripts/ufo-swarm-collect.mjs` (sha256 `841e3c7f…e5f1`):
- Line 602 sets `entry.reportPresent = reportFilePresent(join(ROOT, reportDir, name + ".md"))`.
- Lines 474–480 test only `lstatSync(path).isFile()`.
- Lines 725–729 build `reportSummary.present` and `missing` from that boolean alone.

There is no size check, no `mtime` versus dispatch-time check, no check that the seat wrote the file, and no check of the seat's terminal status. No test in `ufo-swarm-collect.test.mjs` covers empty or stale reports (grep for empty/zero/size near `reportPresent`: 0 matches).

Counterexamples, each currently credited as present:
- A 0-byte `<Seat>.md`. The R22 W1 agent outputs were all 0 bytes; only their location differed.
- A file another seat or the coordinator wrote at that path. The rule "do not edit other seats' reports" is prompt text only.
- A stale file from an earlier wave that shares the `reportDir`.
- A file written by a seat whose transcript ends in a terminal failure.

The same applies to the R22 `late_report_rule` ("Any fresh late W1 report is counted completed"): "fresh" is not defined or checked anywhere.

## Impacted axes

- **Calibration:** the R23 `inherited` statement and the `gen-wave1.py:61` and `:86` instructions assert conclusions that the retained evidence contradicts.
- **Coverage (R23-C1):** not changed by this report. It depends on seat credit, which F4 shows can be inflated.
- **Provenance:** 43 of 64 R23 seats answered on a model other than their routed one.
- **No-harm:** the R22 "C1=1/6" figure is unaffected, because W1 produced nothing either way.

## Smallest safe corrections (for L1; this seat edits nothing)

1. Append an R22 W1 reclassification without deleting or replacing the existing records. Use per-seat classes from the transcripts: 13 `own_terminal_provider_failure`, 32 `provider_capacity_retrying_at_dispose`, 48 `aborted_single_instant_unexplained_mechanism`. Keep `completed=0`. Narrow "unknown" to the abort and dispose mechanisms only. Cite the `history://` paths and the transcript-set digest above.
2. Correct `round-23/claims.json` `inherited`. "102 per-seat unknown" should become: 93 W1 seats with an observed per-seat cause, 9 W2 seats with a known terminal cause, and an unknown mechanism only for the 48 aborts and the 93 parent-coupled disposes.
3. Do not count the ReviewReportless and DraftMistake outputs as independent evidence on the parent-death question. Their prompts dictated the conclusion (`gen-wave1.py:61`, `:86`).
4. When crediting R23 W1, require all of the following per seat: the report file exists, is non-empty, and has `mtime` later than that seat's spawn; the seat's transcript shows a write to its own path, or a non-transcript provider is explicitly noted; and the seat has no terminal failure, or the report predates that failure. Record the actual answering provider and model for each seat, separate from its route. Report the exact count of seats that fail these checks; never fold them into "completed".
5. Collector, as a follow-on outside this lane: `reportFilePresent` should at least reject 0-byte files and expose `size` and `mtime` so the judge can apply item 4. That code lives in `ufo-fsd-alpha`, so this is recorded as a risk, not a change.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CriticLifecycle.md` (this report; no other writes). Scratch analysis files `/tmp/r22w1.json` and `/tmp/r23w1.json` are outside the lane and non-authoritative.

## Installs

None. Pacman is paused host-wide, and no tool was needed.

## Open risks

- The abort and dispose mechanisms are inferred from timestamps only. Harness source for parent cancellation and disposal was not read.
- R23 seat states are a snapshot taken at 14:38:29Z. The DeepSeek and Devin fallbacks and the counts above will drift.
- Transcripts are append-only JSONL in the user session store, not cryptographically authenticated. Digests are pinned above for later recheck.
- This is author-side critique, not verification.

## Addendum 2026-10-21T14:4xZ (coordinator request; append-only, no credit change)

- Per-seat receipt: `.ufo/waves/round-23/w1/CriticLifecycle-r22w1-receipt.json` (sha256 `0ef557fe8883a1ac98b3bfc7a7a18641375cc5b6e5026abd25e058bc596500eb`). It has 93 rows. Each row gives the seat id, model, observed class, every assistant event (1-based JSONL line, stopReason, error text, completedAt), the parent terminal notice if one exists (parent line and timestamp), the `session_exit` line and time, tokens, tool calls, the `history://` id, the transcript path, and the transcript sha256. Credit is `none` for every row.
- Class counts (observed): 13 `observed_own_terminal_failure_notified_to_parent`, 48 `observed_request_aborted`, 32 `observed_provider_errors_no_terminal_event_before_dispose`.
- Inference is kept separate: the mechanism behind the 48 same-instant aborts and the 93 clustered disposes is not established. There is no claim of universal parent causation, because 45 seats show their own provider failures, independent of the parent.
- Correction to F1. `round-23/claims.json` says the 102 reportless seats "remain per-seat unknown **where unknown**". That does not assert all 102 are unknown, and my "double-counts" wording mischaracterized it. The distinction it draws should stand. The receipt only moves R22 W1 per-seat observations from unknown to observed, and leaves the mechanisms marked unknown.
- Correction to line citations. The `KaidokuR22.jsonl` line numbers in F1 and F2 were 0-based. The 1-based lines are: spawn result 155; parent 429s 156, 158 and 160; terminal notices 157 and 159; parent dispose 161; slot grant 146; job-limit refusal 149. The receipt uses 1-based lines.
