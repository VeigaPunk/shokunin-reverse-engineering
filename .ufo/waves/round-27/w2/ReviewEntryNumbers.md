# ReviewEntryNumbers: numbers and pointers in the round 27 renamed-copy entry

Scope: every id, hash, time, count and line pointer in `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`, checked against committed bytes (lane HEAD 4084d8975b684a8837b1c858eea0008ce9ab49e0; entry blob 340747377cbc6d31f770d1b1273220db573816afaa7e0e822d6f3f6be9ec0adc), plus host and installed-package bytes. All times UTC, 2026-10-22. Read-only; no REA call; no lane write except this report.

## 1. Verdict
- Two checks fail, both on pointer wording: B2, the call window end "14:57:40Z" (entry line 3); F2, a quoted phrase not in the cited entry (line 75).
- Everything else holds: the 48 envelope hashes, the 48 evidence ids (recomputed), the 16 verdicts, the document names, the layout paths, the counterfactual id, the carrier and package hashes, the counts, and the two named call times.
- Not evaluated: the live REA recheck (outside this item) and the 6.7.0 pin (the entry excludes it).

## 2. Failed checks
- B2 (line 3). Command: `python3 -I -B entry_checks.py <clone>`, check B2; shell check S17. Output: `latest call end 2026-10-22T14:56:43Z (RunJqA jq inspect renamed)`; `RunTxC.md line 64 ... after the last call (2026-10-22T14:57:40Z)`. Exit 0 (the checker prints failed IDs and still exits 0). UTC 15:41:51Z and 15:44:53Z. Verdict: fails as a call window. 14:57:40Z is RunTxC's post-run carrier digest, not a call end; calls end by 14:56:43Z. Suggested wording: "calls 14:54:51Z–14:56:43Z; post-run digest 14:57:40Z".
- F2 (line 75). Command: `python3 -I -B extra_checks.py <clone>`, check X4. Output: `verbatim 'seven content-keyed verbs' in round-26 entry: False`; `'seven keep their id' in round-26 entry: True`. Exit 0. UTC 15:44Z. Verdict: fails as a quotation. The count "seven" holds (round-26 entry lines 7 and 64). The exact phrase is not in the round-26 entry. It appears in wave-1 seat text (`.ufo/waves/round-27/w1/ProvinceMap.md` line 62) and in the round-27 entry itself (line 75). The round-26 entry says "seven keep their id" (line 7) and "the other seven verbs" (line 64); `corpus/README.md` line 75 and the round-26 lesson line 93 say "seven content-keyed" without "verbs".

## 3. Checks that hold (IDs are mine; raw logs carry the same IDs with a UTC stamp per row: entry_checks 15:41:51Z, shell S-rows 15:44:53Z, extra X-rows 15:44Z, counter and recompute 15:40Z; exit 0 on every check except the counter runs, which exit 1 by their own rule)
Pins and commits
- P1 (line 3): S03, `git show HEAD:<entry> | sha256sum` = 340747377cbc…ec0adc. Holds at HEAD (worktree now differs; see 4.1).
- P2 (recheck paragraph): S04–S06. Counter commit a4f674b3 committed 11:51:23-03:00 = 14:51:23Z, before the first call (14:54:51Z); it is an ancestor of data commit 9dca26df (`merge-base --is-ancestor`, exit 0); only commit touching the counter. Holds.
- P3 (lines 1, 3): S13, package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c; version 6.5.0. Holds.
- P4 (lines 1, 47): S13, GhidraTargetSnapshot.js sha256 a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b. Holds. Re-open 2026-10-22 recorded in corpus/lessons/round-27.md lines 40–41. Holds.
- P5 (lines 1, 21): S09 pacman jq 1.8.2-1 and tinyxxd 1.3.17-1; S11 pacman mtree `./usr/bin/tinyxxd ... size=38928 sha256digest=7b1e…ae65`. Holds. S082 row (corpus/SOURCES.md line 88) and log (line 155) say opened 2026-10-22. Holds.
Carriers and addresses
- C1 (line 20): S07 `sha256sum /usr/bin/jq` = e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806. Holds.
- C2 (line 21): S07 `sha256sum /usr/bin/tinyxxd` = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65. Holds.
- C3 (lines 20–21): S08 renamed copies have the same hashes; sizes 30800 and 38928 bytes. Holds.
- C4 (lines 20–21): S10 `pacman -Qkk`: jq 25 files, tinyxxd 12 files, 0 altered. Holds.
- C5 (line 20): runs.tsv argv and function envelope `procedure.address` = 0x103fa0 (X2, FUN_00103fa0). Holds as "a function start".
- C6 (line 20): S12 readelf jq entry 0x3cf0; python gives 0x100000+0x3cf0 = 0x103cf0 ≠ 0x103fa0. Holds as "not the entry".
- C7 (line 21): S12 tinyxxd entry 0x3d40; python 0x100000+0x3d40 = 0x103d40 (the entry's address). Holds.
- C8 (line 21): X3 tinyxxd-analyze-base.json `image_base` = 0x100000 (committed bytes). Holds.
Runs and times
- R1 (lines 3, 36): A1–A3, A8, S15: 48 run rows, 48 envelope files, 16 table rows, 16 carrier-verb pairs with 3 runs each; 8 seats (RunJqA–D, RunTxA–D), 8 Run*.md files. Holds.
- R2 (lines 1, 3): A5–A7: pkg_version 6.5.0 and package.json sha256 on all 48 calls; exit 0 on all. Holds (the "read after every call" wording is a process claim; only the recorded hash is checkable).
- R3 (line 3): B1 first start 2026-10-22T14:54:51Z. Holds.
- R4 (line 89): B3 layout base starts 14:55:49Z, repeat 14:55:50Z. Holds.
- R5 (line 90): B4 meta.duration 132ms for both. Holds. S14 `cmp` base and repeat: byte-identical; the only shared envelope sha256. Holds.
- R6 (lines 1–3): C1 48/48 files match runs.tsv sha256; C3 48/48 evidence_id, command, ok and subject sha256 agree. Holds.
- R7 (line 88): counter at 9dca26df: `rows_complete=15/16 ... rev=9dca26df`, tinyxxd layout INCOMPLETE (shared sha), exit 1. Holds. At HEAD: 15/16, entry_ok=1, exit 1.
- R8 (recheck paragraph): recompute tool, 48 envelopes: `recomputed ids: 48 match of 48 total`, exit 0. Holds.
Ids and verdicts
- I1 (lines 37–38): D checks: each of the four truncated ids matches exactly one run id. Holds.
- I2 (line 36): C5, base equals repeat in 16 of 16 pairs. Holds.
- I3 (table lines 20–21): C4 table ids equal runs ids; C6 16 verdicts equal table, recomputed rule, and entry table. Holds.
- I4 (lines 20–21): C7 five address verbs keep ids on both carriers (10 cells). Holds. C8 analyze and inspect give the same id on each path. Holds.
- I5 (lines 37–38): G1–G4. Round-26 analyze-base id recomputes; document .bin changed to .dat gives ev_a60580a9…3cd2 (full id matched). Holds.
Mechanism pointers
- M1 (line 47): GhidraTargetSnapshot.js lines 13–14 build `target-${sha.slice(0,12)}${suffix}` (read tool). Holds.
- M2 (line 47): lines 76–78 `safeExtension`, regex `^\.[A-Za-z0-9]{1,12}$`, fallback `.bin` (read tool). Holds.
- M3 (line 50): evidence.js 156–180 projection hashes subject digest, format and architecture only; 181–182 id rule (read tool). Holds.
- M4 (line 47): E-doc, 12 cells: document `target-e815667571d0.bin/.dat` and `target-7b1e5d0c970a.bin/.dat`; prefixes equal the first 12 hex of each sha256. Holds.
- M5: E-op, analyze and inspect `operation` = binary_overview. Holds.
- M6 (lines 47–48): E-layout, 4 cells, and F: layout projected diffs are only parameters.path, artifact.path and locations[0].path. Holds.
- M7 (line 48): F: analyze and inspect projected diff is only document; address verbs have no projected diff, and non-projected diffs are only subject.name, subject.local_path, meta.duration. Holds.
- M8 (decision table): X1 `subject.digest.sha256` exists. Holds.
Scouts and limits
- S-1 (line 63): "8 of 8": PredictWholeFile.md (3 rename-sensitive) and PredictAddressVerbs.md (5 content-keyed) exist and are tracked (S18); table matches all 8 (C6). Holds.
- S-2 (line 83): no 6.7.0 run in runs.tsv (A5). Holds.
- S-3 (pin text): S16, claims.json frozen at a4f674b3 contains "npx -y rea-agents@6.5.0" 2 times. Holds.
- S-4 (line 92): corpus/lessons/round-27.md line 68 (M27-2) records the shared-sha refusal. Holds.
- S-5 (recheck paragraph): counter flags `--root` and `--rev` run as written; recompute tool tracked (S18). Holds.

## 4. Residual risks and notes
- 4.1 Working copy moved during my run. At 15:37:30Z the entry matched HEAD. By 15:44:53Z the status and the entry hash showed a change, and `git diff` at 15:45:02Z shows 30 lines appended after line 92 ("## Corrections after the falsify wave", lines 93–122), plus uncommitted edits to SKILL.md, PROVINCE.md, corpus/README.md and an r17 entry. I did not make these edits. Lines 1–92 are unchanged, so B2 and F2 also apply to the working copy. The appended section has new ids, hashes and times (for example binary-BVOr2mgE.js sha256 64c07dae…c00df, lines :5261, :5318, :293, "15:37Z"), and cites 97358f75. Not checked here (not committed bytes); they need the same check before commit.
- 4.2 Scout timing. PredictAddressVerbs.md lines 7–8 say "prediction made before that data exists"; PredictWholeFile.md lines 3–4 say "before any round-27 envelope was read or produced". runs.tsv shows all calls ended by 14:56:43Z, and the scouts' observations start at 14:55Z (PredictAddressVerbs.md line 10) and 15:00:40Z (PredictWholeFile.md O1). The entry's own words, "before reading any round-27 envelope", hold; "before the data existed" does not. Scout transcripts were not opened, so their reads are unverified.
- 4.3 Counter at the data commit: entry_ok is 0 at 9dca26df because the entry was added later (c6d619a3); it is 1 at HEAD. Rows 15/16 hold at both.
- 4.4 The npx cache directory ~/.npm/_npx/ad9a3fdbcad992c6 had its mtime change at 15:37:48Z. I made no npx call before 15:44:06Z; cause not established (possibly a sibling seat). Package hashes re-read at 15:44:53Z (S13) match the 15:37:30Z values.

## 5. Side effects and tools
- My mistake: a helper bug in my first shell script ran `npx pin text in claims frozen at a4f674b3` at 15:44:06Z. The npm log (/home/vgpnk/.npm/_logs/2026-10-22T15_44_06_850Z-debug-0.log) shows one registry metadata GET for `pin` (200) and exit 1 "could not determine executable to run". `find ~/.npm/_npx -maxdepth 3 -name pin` found nothing, so no install. The same bug ran other description lines as commands (exit 127, or tinyxxd usage with exit 1); nothing was written, and the scratch listing shows no stray files. The corrected rerun replaced the first run's raw log.
- No tool installed or upgraded. Used: python3, readelf, pacman -Q and -Qkk (query only), sha256sum, cmp, stat, git (read-only, plus a clone into the sandbox).

## 6. Artifacts (scratch: /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewEntryNumbers/)
- entry_checks.py 1202e8459ca1d5c334b647b1f200bd1d34e6a70118a8e9820657cde8f6c6b059; entry-checks-raw.txt c4db8c7fb28473d6c73f2358d43938c45dccbc37bb7290b2c4ec7c6ef38b32b6
- extra_checks.py 0bc62508a1387f40e0284f6b591f1439f0e63499d7f0a2cbd1766067045f6636; extra-checks-raw.txt 18813cfba3245b375a9f8ee723c8a00f27dabcee6524fa4f1d7d19f61e501fd0
- shell_checks.sh 913903336a813cc2ecfd849b154ed098d19f469c922a78d64b93b2a1ce4dd27c; shell-checks-raw.txt 2186af5a1a3cde95106f133f77c52c46a59262fb03ee85eeda536a0c877021d8
- counter-at-9dca26df.txt 2f8842285e86565fb2349522164ea9966ebc95c474b99708c3134ed857ab6882; counter-at-HEAD.txt a02047192099a8546be7162dbff293fd108e8357be225be30f67fa0e463ccfb8
- recompute-r27-48.txt 071427e5049ffcc8b63cf8c72c1eb994b25989d4b75d925886fc0a67d8b33e86
- clone/: sandbox checkout at 4084d897, clean (S19).

## 7. Not evaluated and gaps
- Live REA recheck (copy with a .dat name, `analyze` on both): not run; REA is outside this item.
- 6.7.0 numbers: not checked; the entry excludes them.
- Scout transcripts: not opened; their claimed reads are unverified.
- The appended uncommitted section: not checked (see 4.1).
- lsp device: not used; the pointers are text and byte checks, and the entry makes no caller or definition claim.
