# HistoricalSeatEvidence — R22 reportless recount (R23, author-side)

Seat: `KaidokuR23.HistoricalSeatEvidence`. Round 23, W1. Scope: independently recount the inherited claim "R22 102 reportless seats" from R22 receipts and inherited seat transcripts, and separate known terminal failures from per-seat unknowns. Read-only: no production file was edited, no git writes, no debugger/Frida/device/REA target execution. This is author-side evidence, not outside verification.

No REA probe was selected for this question, so there is no REA argv/target-sha256 to retain here; the whole recount is local artifact and transcript reading.

## Findings

### F1 — Recount: 102 reportless reproduces exactly as 93 (W1) + 9 (W2)

Observation. Independent recount from spec, dispatch, report paths and seat output files:

| Item | W1 | W2 | Total |
|---|---|---|---|
| Seats in wave spec | 93 | 64 | 157 |
| Spawn receipts (unique ids) | 93 | 64 | 157 |
| Expected report paths | 93 | 64 | 157 |
| Report files present | 0 | 55 | 55 |
| **Reportless** | **93** | **9** | **102** |

- W1 spec: `.ufo/waves/round-22/wave1-spec.json` `items` = 93 unique names. W2 spec: `wave2-spec.json` `items` = 64 unique names.
- W1 dispatch: `wave1-dispatch-result.txt` contains 93 unique `KaidokuR22.*` ids; `w1/swarm-registry.json` `members` = 93, all `kind: spawn`; id sets are equal, and equal to `final-wave-outcomes.json` `wave1.members` ids.
- W2 dispatch: `wave2-spawn-try6.json` spawn ack names 64 unique `KaidokuR22R.*-6` ids, equal to `final-wave-outcomes.json` `wave2.members` ids. W1/W2 id sets are disjoint; 93 + 64 = 157 = the top-level `round_seats` in `final-wave-outcomes.json` (the `wave2` block begins at line 1139).
- Expected report paths are explicit in the dispatch payloads (93 W1 paths, 64 W2 paths, names match spec exactly). `os.path.isfile` on each: W1 0/93 present; W2 55/64 present.
- W1 report dir contents: only `swarm-registry.json` (`ls .ufo/waves/round-22/w1/`); `find .ufo/waves/round-22 -name '*.md'` = 55 files, all under `w2/`.
- Seat output files under the inherited session dir: `KaidokuR22/*.md` = 93 files, **all 0 bytes**; `KaidokuR22R/*.md` = 64 files, 55 non-zero, **9 zero-byte**, and the 9 zero-byte stems are exactly the 9 absent report paths.
- `final-wave-outcomes.json`: W1 block `seats: 93`, `reports: 0` (lines 4–5); W2 block `seats: 64`, `reports: 55`, `reportless: 9` (lines 1140–1142). Arithmetic identical to this recount.
- Latest W2 report mtime is `2026-10-21T13:31:00Z` (`w2/CriticCausal.md`), before the final observation cutoff `2026-10-21T13:58:56.949274Z` (`final-wave-outcomes.json` `observation_cutoff_utc`). No `.md` appeared in `round-22/` after 13:31Z, so no late report changes the 55.
- W1 `late_report_sweep` in `final-wave-outcomes.json:8` records scope `kaidoku-shokunin/.ufo/waves/round-22/w1` with `fileCount: 1` and only `swarm-registry.json`. Rechecked at read time: unchanged.

### F2 — Known failures: 9, all W2, all with the cause text corroborated in the seat's own transcript

Observation. `final-wave-outcomes.json` marks all 9 W2 reportless as `status: terminal_provider_failure` with `terminal.authority: "automatic terminal notification"`. Provenance splits in two:

| Seat | Cause class (final receipt) | Transcript last error (UTC) | Session exit (UTC) | In `wave2-terminal-initial.json` |
|---|---|---|---|---|
| RecoverReceipts | Codex capacity, retry budget exhausted (5) | 13:03:01.143Z | 13:10:01.165Z | yes |
| RecoverFlutter | Codex capacity, retry budget exhausted (5) | 13:03:01.625Z | 13:10:01.672Z | yes |
| CounterSelfInvocation | Codex capacity, retry budget exhausted (5) | 13:02:59.783Z | 13:09:59.832Z | yes |
| SourceGateDraft | Anthropic 429 `rate_limit_error`, `retry-after-ms=6423000` | 13:02:56.432Z | 13:09:56.461Z | yes |
| SchemaInspectSignalDecoders | Cursor RESOURCE_EXHAUSTED | 13:03:23.163Z | 13:10:23.195Z | no |
| PrimaryDart | Cursor RESOURCE_EXHAUSTED | 13:03:27.708Z | 13:10:27.728Z | no |
| CriticLowest | Cursor RESOURCE_EXHAUSTED | 13:03:23.178Z | 13:10:23.208Z | no |
| C1Split | Devin `resource_exhausted` free-model rate limit | 13:15:20.492Z | 13:22:20.511Z | no |
| C1Partial | Devin `resource_exhausted` free-model rate limit | 13:14:47.836Z | 13:21:47.853Z | no |

- The 4 retained entries are in `wave2-terminal-initial.json:2,8,14,20`, file mtime `2026-10-21T13:03:26.937Z`. The 5 remaining causes appear only in `final-wave-outcomes.json` (written `13:58:56.951Z`). `wave2-missing-causes.json` lists all 9 ids (lines 4, 33, 62, 91, 120, 149, 178, 207, 236) with empty `agent://` reads.
- Each of the 9 `KaidokuR22R.<Name>-6.jsonl` transcripts contains the matching `errorMessage` text: Codex capacity (RecoverReceipts/RecoverFlutter/CounterSelfInvocation), Anthropic 429 with `retry-after-ms=6423000` (SourceGateDraft), `Cursor RESOURCE_EXHAUSTED` (SchemaInspectSignalDecoders/PrimaryDart/CriticLowest), `Devin stream error resource_exhausted: Reached free model rate limit` (C1Split/C1Partial). This corroborates the cause text, not the notification-receipt chain for the 5.
- Note as observation only: three Cursor errors are timestamped `13:03:23Z`, three seconds before `wave2-terminal-initial.json` was written at `13:03:26.937Z`, yet they are not in that file. No explanation is asserted.
- `wave2-terminal-initial.json` records SourceGateDraft as `429 rate_limit_error ... retry-after-ms=6433000`; the transcript holds two such messages (`retry-after-ms=6433000` and `6423000`). The final receipt keeps `6433000`.

### F3 — Unknown W1: 93 per-seat unknowns; superseded per-seat causal records, no retained per-seat notification receipts

Observation and match to the correction.

- `wave1-terminal-correction.json:7` `dispatched: 93`; `:8` `initial_reports: 0`; `:9` `93 treated dead/reportless; no live KaidokuR22 seats observed`; `:10` `per-child cause unknown; predecessor parent Anthropic429 is observed, automatic child termination is not established`.
- `final-wave-outcomes.json:6` `not_live_at_parent_and_final_observation: 93`; `:7` same cause statement; every one of the 93 members carries `cause: "unknown; parent provider error is not per-child terminal proof"` (first at line 25, repeated per member).
- `wave1-terminal.json` (mtime `12:39:07Z`, sha above) does contain 93 per-seat entries, each `status: dead_parent_provider_death`, `cause: "parent KaidokuR22 Anthropic429 terminated child session"`, `report: null`. These are coordinator-authored global-assertion records, not retained per-seat terminal notifications, and their causal assertion is what the correction supersedes.
- `recovery-authority.json` repeated "all children terminated with KaidokuR22 coordinator Anthropic429". `wave1-terminal-correction.json:2` lists `wave1-terminal.json` and `recovery-authority.json` under `supersedes_causal_assertion_in`, authority "parent Main correction: children do not necessarily die with parent". Both original files remain on disk; nothing was deleted or rewritten by this seat.
- Under the corrected record, this recount classifies **W1 known failures = 0, unknown = 93**. Zero retained per-seat terminal notification receipts exist for W1; the 93 per-seat causes in `wave1-terminal.json` are superseded assertions and are not counted as known failures.

### F4 — W1 transcript activity: observed, and deliberately not promoted to cause

Observation (activity evidence only):

- 93 `KaidokuR22/*.jsonl` transcripts exist (85 KB–98 KB each). 93/93 end in `session_exit` `reason: dispose`, `kind: normal`.
- Exit window `2026-10-21T12:04:35.967Z`–`12:04:37.897Z` (1.93 s). Parent `KaidokuR22.jsonl` exit `12:04:37.911Z`, 14 ms after the last child. Parent transcript contains 3 `errorMessage` events: Anthropic `429 {"type":"error","error":{"type":"rate_limit_error",...}} retry-after-ms=10343000`.
- Last-error-text class per seat transcript, by role (classification of the last `errorMessage` string; not a terminal proof):

| Role | Codex capacity retry-exhausted | 429 rate limit | Request aborted | Total |
|---|---|---|---|---|
| scout | 0 | 0 | 24 | 24 |
| executor | 23 | 0 | 0 | 23 |
| reviewer | 0 | 0 | 14 | 14 |
| scribe | 0 | 13 | 0 | 13 |
| critic | 8 | 0 | 0 | 8 |
| revenger | 0 | 0 | 4 | 4 |
| sentinel | 2 | 0 | 0 | 2 |
| mutation-tester | 0 | 0 | 2 | 2 |
| simplifier | 0 | 0 | 2 | 2 |
| connector | 0 | 0 | 1 | 1 |
| **Total** | **33** | **13** | **47** | **93** |

- Inference (labeled): a 1.93 s common exit window ending 14 ms before the parent's own dispose is consistent with parent-driven disposal. It does **not** establish that the parent's Anthropic 429 caused child termination, and the correction says the same. Per-child cause remains unknown.
- Unknown: whether any W1 seat would have produced a report absent disposal. No W1 report exists and no per-seat terminal notification receipt was retained; the 93 per-seat causes in `wave1-terminal.json` are superseded assertions (F3).
- `reportless` is an output-status classification, not an execution-status classification: all 102 reportless seats have transcripts, 5 of the 9 W2 transcripts are 155–301 KB (C1Split, C1Partial, CriticLowest, SchemaInspectSignalDecoders, PrimaryDart), and all 93 W1 transcripts are 85–98 KB.

### F5 — Classification totals

- Known terminal provider failures: **9** (all W2; 4 with retained intermediate notification, 5 final-summary-only but transcript-corroborated).
- Unknown per-seat: **93** (all W1).
- Total reportless: **102 = 9 known + 93 unknown**.
- The inherited line `R23 claims.json:63` ("R22 102 reportless seats remain per-seat unknown where unknown") is consistent with this recount: it does not claim all 102 are unknown; 9 have known terminal causes.

## Commands and observed exits

All runs used `python3 -I -B`; stderr empty; exit shown.

| # | Command (abbreviated) | Exit | Key output |
|---|---|---|---|
| 1 | `python3 -I -B .ufo/waves/round-23/w1/recount-102.py` | 0 | `w1_reportless 93`, `w2_reportless 9`, `total_reportless 102`, `known_terminal_failures 9`, `unknown_per_child 93`, both identity checks `true` |
| 2 | `find .ufo/waves/round-22 -name '*.md' \| wc -l` | 0 | `55` |
| 3 | `ls .ufo/waves/round-22/w1/` | 0 | `swarm-registry.json` only |
| 4 | `sha256sum` over the 13 R22 source files | 0 | hashes below |
| 5 | transcript scan of 93 `KaidokuR22/*.jsonl` (exists, size, `session_exit`, `errorMessage`) | 0 | 93 files; 93 `dispose/normal`; 93 with an error message; window and role table above |
| 6 | transcript scan of 64 `KaidokuR22R/*.jsonl` | 0 | 64 files; 64 `dispose/normal`; 9 reportless each with matching `errorMessage` |
| 7 | `os.path.isfile` over 93 W1 + 64 W2 exact expected report paths | 0 | 0/93 and 55/64 present |
| 8 | `os.listdir`/`stat` of inherited session `.md` outputs | 0 | W1 93 files, 0 non-zero; W2 64 files, 55 non-zero |

No T1 REA verb probe was run for this seat; no target was opened, so no target sha256 exists to report.

## Source hashes (sha256, read at 2026-10-21)

| Path | sha256 |
|---|---|
| `.ufo/waves/round-22/final-wave-outcomes.json` | `093311163a45fea0c6c000331e68c098340b6b4a96c7d6bcd5c4a17ff4c77fa6` |
| `.ufo/waves/round-22/wave1-terminal-correction.json` | `4914c0e5757481a0215fde85cb8d4efb75afac54c644c8dcebc2f697f01074e9` |
| `.ufo/waves/round-22/wave1-terminal.json` | `67d1ebb80514554db6054ca54cd322ef15c21207143de4fed848d422b67222a1` |
| `.ufo/waves/round-22/wave2-terminal-initial.json` | `9679ecc6468fa7fbc8e26d2983af29fa3a9fd67d61c4b19358e8a868e0cf453a` |
| `.ufo/waves/round-22/wave2-missing-causes.json` | `73dc9ab6269aca6d812cba74950c422976ebc7e7d403abcc4832dad2ca257fa4` |
| `.ufo/waves/round-22/recovery-authority.json` | `e7a08c7cab4e391c14c3f6c92a530cc5c32d64e094ad47ec045f088eb415ef0f` |
| `.ufo/waves/round-22/w1/swarm-registry.json` | `621a7c2751243acd3992b3ea172e81c28715bbe6562857be77551ed8035b889c` |
| `.ufo/waves/round-22/wave1-spec.json` | `2e3b72c0ee273da53a63bf2bef27948eb6ce6549a0697748046edb4e3838b632` |
| `.ufo/waves/round-22/wave2-spec.json` | `e6d6674fa81f85dd4218ef975ee9d96633bfd64e1e1acd03f4a923063e280dc7` |
| `.ufo/waves/round-22/wave1-dispatch-attempts.json` | `d38c1b41777204abc32df54dc2cd0b7351d9ee5c797b66801a53c319b30a58b0` |

`recount-102.json` carries the same hashes for 13 R22 source files (including `wave1-dispatch.json`, `wave2-dispatch.json`, `wave2-spawn-try6.json`).

## Produced files

| Absolute path | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/HistoricalSeatEvidence.md` | see `HistoricalSeatEvidence.sha256` (computed after final write) |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/recount-102.py` | see `HistoricalSeatEvidence.sha256` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/recount-102.json` | see `HistoricalSeatEvidence.sha256` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/HistoricalSeatEvidence.sha256` | manifest of the three files above |

The manifest is the authoritative hash record for this seat's outputs; it is written after the last content edit so the report hash is self-consistent.

## Installs

None. No package, tool, model or config was installed or changed.

## Open risks

1. **Five W2 causes rest on one retained summary.** For SchemaInspectSignalDecoders, PrimaryDart, CriticLowest, C1Split and C1Partial, the claim `terminal.authority: "automatic terminal notification"` has no retained intermediate notification file; only `final-wave-outcomes.json` plus matching transcript error text. If the summary's authority chain is contested, these five should be treated as transcript-corroborated terminal errors rather than receipt-retained notifications.
2. **W1 causality stays open.** 93 per-seat causes remain unknown. The common 1.93 s disposal window and the parent's Anthropic 429 are observations; this recount does not establish parent-to-child termination. The 33 Codex-capacity / 13 429 / 47 aborted transcript error texts must not be promoted to per-seat terminal causes.
3. **Late report rule is open.** `wave1-terminal-correction.json:16` says any fresh W1 report counts completed and reclassification is appended. A single late W1 report would move the count from 102 to 101; this recount is a point-in-time snapshot.
4. **Reportless ≠ unexecuted.** All 102 have transcripts; 5 of the W2 nine show 155–301 KB of tool activity. Any downstream statement equating reportless with "did nothing" or "never ran" is unsupported by this evidence.
5. **Hashes cover working-tree bytes, not a git revision.** The R22 files were read from the working tree; the recorded sha256 pins what was read. No cryptographic authentication of the artifacts is claimed.
6. **W2 report content quality is out of scope.** The 55 present reports were counted by path and non-zero size only; this seat did not assess their content, and R22's C1/C2 outcomes are not re-judged here.
7. **Arithmetic depends on the declared per-wave report directory.** Both dispatch payloads name the report path per seat; the recount uses those exact paths. Any report written elsewhere would be invisible to this count — a scan of `round-22/` found no other `.md` files.
