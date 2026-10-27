# R43W2CrossClaims — cross-claim falsification

## Scope and measured revisions

Read-only cross-axis scan of the frozen claims, control receipts, and committed scoring receipts. Frozen plan: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. Lane HEAD when examined: `5856614ac4bf7f2363bbcd1956644474a82108e5` (working tree was dirty; pre-existing `w2.ready`, `SCORECARD.md`, `SHONEN.md`, `w2.ready.partial`, and `w2/` changes were left untouched). C1/C2 scorer receipts both evaluate full revision `77d196c66f4fea00d7d543728b190ebdfaf6d0f0`; the second C2 receipt additionally evaluates `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`. These are historical measured revisions, not HEAD. No published firmware or carved bytes were opened; no REA/extractor was run.

## Cross-claim scan result: no shared-input falsification found; C2 is honestly red

The frozen plan's separability section says C1 and C2 use separate data and that `S135` is a C1-only citation. The frontier step and final `SOURCES.md` content show S135–S137 appended. The measured base-to-revision `git diff --numstat` for `corpus/SOURCES.md` is `4 0`, while the C2 receipt explicitly requires exactly `3 0`; the three new registry rows are S135–S137, and the fourth added line is a blank separator (not a fourth registry row). Thus the current C2 failure is a discrepancy in the frozen *line-count* predicate against its intended three-row addition, not evidence of an unintended extra registry row or shared data use. This is a cross-claim boundary weakness worth correcting prospectively, but the explicit frozen C2 predicate must remain red this round.

C1's receipt at `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` independently reports `exit_code: 0`, `matched: 78`, `n: 78`, no false bindings, and identical `counter_sha256`/`counter_sha256_at_freeze` (`3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79`). Both committed C2 receipts (`77d196...` and `09ab56...`) explicitly report `sources_numstat_three_additions: false`, `checks_ok: false`, `exit_code: 1`. On the 77d receipt the other checks are true: clean clone, verifier 136 checks/0 failures, gate exit 0, 19 checked, 137 total, rows_failed empty, S126 preserved, map digest pinned, freeze ancestor, and score tool frozen. Consequently this is not a C1 score reused to certify C2: distinct counters/receipt schemas have distinct measured outcomes, and C2 honestly stops on its own bound check.

The exact count was reproduced against immutable objects:

```
git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..77d196c66f4fea00d7d543728b190ebdfaf6d0f0 -- corpus/SOURCES.md
4\t0\tcorpus/SOURCES.md

git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..09ab56b8fdc2efcc3b58b203644537d84dd5ac9e -- corpus/SOURCES.md
4\t0\tcorpus/SOURCES.md
```
Both exited 0. The full content diff shows the three row additions S135–S137 and a blank separator. No score was treated as green based only on a summary: C2 failure and C1 success fields were read directly from the JSON receipts.

## Axes and one bounded move

- **Coverage:** C2's copy/gate children are green, but its overall frozen predicate is false due to a count that includes a formatting separator. Coverage success is therefore not established by the overall receipt.
- **Calibration:** C1's measured score is green under its reported bindings. No cross-claim score reuse was observed.
- **Depth:** The count-vs-row distinction exposes a brittle interface between C2 and the shared registry file, although it does not establish claims sharing inputs.

**One bounded move:** for a future freeze, bind SOURCES changes by parsed appended row IDs/content (and separately constrain formatting if wanted), rather than raw added-line count; explicitly document the shared registry as a common interface while keeping claim data/predicates independent. Do not relax the frozen round-43 predicate post hoc; current C2 remains red. Risk: moving the predicate after seeing the result would destroy its freeze integrity, so only a subsequent freeze may adopt this change.

## Evidence inventory

Absolute paths and SHA-256 of principal files read:

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-43-claims.md` — `0326dff974d48df575486256dbd5a0b36593dbc84155d0d40560b64d3c20d83e`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json` — `13a495dbb6862d6cfbdd1f41e4a09460740f86bf93e8bb08e313b06d92b8a55c`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json` — `42f592aec7d6ffe082a257dba1142b1790857c53ddaab17b1bae1c8db09b76e6`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` — `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` — `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`

Commands executed: `git rev-parse HEAD`; `git status --short`; `df -h /fast/scratch /home/...`; `sha256sum` on the five paths above; Python JSON field extraction for C1; `git diff --numstat` for base→each C2 revision; `git diff` for base→77d SOURCES; bounded reads of the frozen plan and C2 receipt check fields; file discovery for C1 controls; targeted search of SOURCES rows. All completed commands exited 0. No scoring commands, tests, whole-repo checks, installs, commits, or VCS mutations were run. Disk observation: `/fast` 368G available (55% used), `/home` 590G available (35% used). RULES.md presence checked; no installation planned.

Limitations: this seat checked the cross-claim shared-path and score-reuse/dependency question against receipts and the SOURCES diff, not every C1/C2 predicate or the full wave-2 attack set. Receipt claims about scratch child processes were not independently rerun. Lane tip was `5856614...`; no claim is made that either scored revision equals that tip. No artifact beyond this report was needed.

Report: `.ufo/waves/round-43/w2/R43W2CrossClaims.md`
