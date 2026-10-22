# Round 27 wave 2: review of the hygiene bullets (ReviewHygieneLanded)

Seat: KaidokuR27.ReviewHygieneLanded, leaf reviewer. Scope: the 11 bullets under "### Round-27 hygiene corrections (not a claim)" in SCORECARD.md. Checked against the wave 1 reference `.ufo/waves/round-27/w1/ReviewHygieneTargets.md` (used as a checklist only; every point re-run), against the lane itself, and for append-only status.

## Summary
- Verdicts: 8 fail (bullets 1, 2, 3, 7, 8, 9, 10, 11). 3 hold with minor cite or wording defects (4, 5, 6). None could not be evaluated.
- Append-only: pass. No old line was removed or rewritten. One mid-table insertion shifts later line numbers by one.
- Inference items 1, 8 and 9 all overstate. Bullet 9 is worst: a false present-tense span, and rows from three separate tables called "the same table".
- The lane tip moved during the run. `main` is now `c4ec7a2e` (15:47:19Z). The 11 bullets are unchanged there. An appended note (SCORECARD 3123-3129) discloses some errors below, not all.

## Tips and timing (UTC)
- Assigned tip `4084d8975b684a8837b1c858eea0008ce9ab49e0`: checked in full.
- New tip `c4ec7a2e04889ed3a07fa1bd03550fbf467e0c19` ("round-27: falsify-wave corrections"), committed 2026-10-22T15:47:19Z. Working tree clean. SCORECARD lines 1-3119 identical at both tips (N8).
- Runs: earlier batches 15:36-15:46; replay.log 15:47:34; replay-moved.log 15:47:56; replay-new-tip.log 15:48:23; replay-extra.log 15:50:42. Fleet HEAD check at 15:49:22: `git -C /home/vgpnk/Projects/shokunin show HEAD:AXES.md | sha256sum` gave 04ea5c9e…, exit 0 (fleet HEAD c58b7e7).
- Each check ID below (A2, D05, E3 and so on) names one block in those logs, with command, output excerpt, exit code and UTC time.
- Git used read-only only, with GIT_OPTIONAL_LOCKS=0. No jj. No REA calls, web sources, sudo or installs; no tool installed or updated. Lane write: this file only.

## Append-only (question 2)
- cd32264f to 4084d897: `git diff --numstat` gives `34 0` (A2). Hunks `@@ -620,6 +620,7 @@` (one capability row at line 623, from 97358f75) and `@@ -3085,3 +3086,36 @@` (33 appended lines). Removed content lines: 0 (A3b). PASS.
- cd32264f to c4ec7a2e: `42 0` (M6). Eight more lines appended after line 3119 (N1, N2). PASS.
- Old text of all 11 bullets is unchanged (N8).
- Caveat: the row at 623 sits inside the line-addressed `## Capabilities` table, so every later line moved down by one. Bullets 7, 8, 9 and 11, the 681 cite in bullet 4 and the 2941 cite in bullet 1 all quote pre-shift numbers.

## Verdicts (questions 1 and 3)
| # | Bullet, cite as written | What the tip shows (check IDs) | Verdict |
|---|---|---|---|
| 1 | L12, calibration is the lowest axis [inference item 1] | Quote at 11-12 (D01, D02). Rows 23-25 end at 10.0, 10 and 10 (C1). Cite 2941-2942 is really 2942-2943 (D03, D04). The "current card reads calibration as tied-lowest" comes from a round-25 sentence under the 2938 heading, which says "at this prospective phase" (X6). | FAILS: overstated inference; stale cite; "tied-lowest ... not lowest" contradicts itself |
| 2 | L46, map is 70/72 | Quote right (D05). The bullet's "at main 109/109" is the a4f674b3 run (B1). At 4084d897 recipe A gives 110/110, missing [] (B2; N4 at c4ec7a2e). The card's own line 3099 also says 110/110 (K1). | FAILS: counterexample B2 |
| 3 | L55, 70/70 is not current 72/72 | Quote right (D06). The 72/72 point is stale, as claimed. "Current map 109/109" is false at main (B2). | FAILS on the count; the 72/72 point holds |
| 4 | L77-80, correction debt; PROVINCE 107-109 pointer | Quote at 80 (D07). Scope notes present: r2 line 244, r3 line 141 (X1, X2). The r2 note came from 40162fc7 (X3). Refusal block hash 78f40919 matches at baseline 107-109 and at 114-116 (F5, F6, N5). Cite 681 is line 682 (D08). "Discharged" is a judgement. | HOLDS, one stale cite |
| 5 | L81-83, EVM and PE items | Quote at 81-82 (D09, D10). PROVINCE 84-86, 87-88, 91-93, 139-144, 145-146, 149-150 say what the bullet says (N6). Line 622 unchanged. PROVINCE 103-104 is the non-REA dynamic-analysis scope line, not a runtime-capture limit; SKILL:61 is the on-point line (N7). | HOLDS, one loose cite |
| 6 | L152-154, planned reconcile; L56 says closed | Quote at 152 (D11); line 56 (D12). PROVINCE:45 gives the 6.4.0 receipt, with "(historical)" in the same row (F2). SKILL:12 names 6.4.0 under "Owned surfaces", and the same line says "historical" (F3, F4). Old/new-name search exits 1 (F1). | HOLDS, bullet omits "historical" on SKILL:12 |
| 7 | L907, capability row entered; four tables; 7 rows | Quote at 908 (D13). No capability table row names citation-drift (E5, exit 1). Tables at 617, 2134, 2206, 2373 (E1). Rows: 8, not 7 (E3). Inline text at 919-920 (D16). Gap note at 1268-1269 (D14, D15). | FAILS on counts and cites; the no-row claim holds |
| 8 | L615-624, Capabilities section [inference item 8] | Section holds 5 rows, 619-623; row 623 is the round-27 C2 row (E3). Card holds 8 rows, not 7. No pointer to the appended tables (text at 615-625). The note is at 2138-2139 (D18, D19). "6→7" at 2365 is a round-17 measurement (D20). Appended tables at 2132, 2204, 2371 (E2). | FAILS: stale counts and cites; "undercounts by 3" is a reading of the layout, presented as a correction |
| 9 | L631-632, rounds 6-8 [inference item 9] | Sentence at 632-633 (D21, D22). The luna-round-10 claim holds: header 617 with two rows, luna-round-6 and -8 (E6). Rows at 2136, 2208, 2375 sit in three appended tables, not "the same table". "Spans luna-round-6 through round-17" is false: row 623 is round 27 (E3). | FAILS: mis-attribution and false span |
| 10 | L14, AXES.md:33-39 | Quote right (D23). Fleet AXES.md: working tree and HEAD c58b7e7 both hash 04ea5c9e (G1; fleet HEAD check). Lines 33-39 are the round-admission rules; line 79 is the axes spec (G2). e867f78 table at 33-39, axes row at 37 (G3). Last change 84bade0, 2026-10-16 (G6). | FAILS on one identifier: "fleet revision c265db9b" is a lane commit, absent from the fleet repo (G4 exit 128, G5). Rule cite is 16-17, not 15-16 (X5). |
| 11 | L3061, planned depth order; probe times | Quote at 3062 (D24); line 3061 is blank. Round-26 probe 11:59:16Z, exit 0 (H1). c27f445 lacks tools/round-26 (H4 exit 128; H5). Disclosure at 3067, not 3066 (D25). Claim-freezes row 14 correct (H8). Round-27 probe 14:45:23Z, before freeze 14:51:23Z (H2, H3). The probe is not a runs.tsv row (H6, count 0), so the counter never saw it (H7 shows the refusal text exists). "Current planned field :3081": line 3081 is blank; round-26 field is 3082, round-27 field 3121 (D26-D28). | FAILS: cites; "excluded by the counter"; "current" pointer. The order departure holds. |

## Inference items 1, 8, 9 (question 3)
- Item 1 overstates. A dated round-25 prospective sentence is presented as the card's current reading.
- Item 8 overstates. "Undercounts by 3" treats the layout (summary table plus appended tables) as a defect, with no inference label. Its own "4 rows" is stale.
- Item 9 overstates. It calls rows in three separate tables "the same table", and the "through round-17" span is false at the tip.
- The section header says items 1, 8 and 9 are "partly inference" but does not say which sentences are. The wave 1 reference calls them "inference only". I disagree for 8 and 9: their present-tense counts and row placement are observed errors.

## Appended note at c4ec7a2e (SCORECARD 3123-3129; N1, N9)
- Checked true: the line basis is a4f674b3, whose SCORECARD hash equals cd32264f's (X7); two bullets' "at main" means a4f674b3; the table holds 5 rows and the card 8 (E3); the map is 110/110 (N4, K1).
- Not corrected: bullet 1's "current card reads"; bullet 8's "undercounts" framing; bullet 9's "same table" and round-17 span (the note's "5 rows" implies the span is wrong, but does not say so); bullet 10's c265db9b label; bullet 11's counter mechanism and its 3081 pointer.
- Conflict: line 3125 says "the current planned field is the round-27 one" (3121). Line 3128 says its planned line "supersedes the planned field above". Bullet 11's pointer stays ambiguous.

## Other notes
- The C2 row (97358f75) went into the summary table, not into a new appended "Capability addition" table, which is how earlier rounds added rows. The card's note at 2138-2139 says the earlier summary table is unchanged. That convention is my inference, not a stated rule. The hygiene section discusses this exact table and did not flag the placement.
- The wave 1 reference gives the owned-axes rows as 22-24. They are 23-25 (C1), so bullet 1's cite is right. It also reads line 56 as recording the planned surface reconciliation as done; I read 56 as covering only per-client pins, so bullet 6's narrower reading holds.

## Residual risk and gaps
- Not checked: the rest of the c4ec7a2e note (the C2 selftest exit, seat counts); the C1 and C2 measurements; PROVINCE and SKILL text beyond the cited lines; the "discharged" judgement in bullet 4 beyond the two scope notes.
- Recipe A ran at three revisions only. Its counts depend on the corpus README map at each revision.
- Block A1 in replay.log shows c4ec7a2e, because the commit landed during that run. The diff, recipe and quote checks use explicit revisions or the 4084d897 scratch copy; the lane-file checks (F1-F4) give the same answers at both tips (N6, N7).
- Bullets keep stale text by design ("old lines stay as written"). A reader who skips the appended note still reads 109/109 and 4-row counts.

## Scratch artifacts (dir /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewHygieneLanded/; sha256)
- replay.log d54629f7ccf200d2cb67c018a526bfbe703f743ba2218532ac3e6c75e0d4b31a
- replay-moved.log f24675c2a325830c66e4016917358dbb272b89fc77d14546c86820b43db01d8e
- replay-new-tip.log c4c974bac7cb800c78f21f058fee74256ff230123c6d1a96ccfa4c774a37ce37
- replay-extra.log 460dc30fbc9b4e81699011ab253707cb99454b26e5f9b97393a951a377fb4378
- replay-scorecard-cd32-main.diff 3616bfd1081f01b9a876c826a547b0d64a872305899ffa82c03d370e6c756999
- moved-scorecard-4084-main.diff fca56879ee02a694881e18e514def59d10b28e25873ef994a27fffaec859c587
- moved-province-skill-readme.diff 8dc63a0b1a94b7ad4fd384219484e51f0d7d98878e89f958ce733c50908f3764
- worktree-scorecard-vs-head.diff e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- province-skill-cd32-to-main.diff 4db8e0668c74cac79417d1cbb17f37649bf6aeedd59a65bfcc189a18623c8f6b
- recipeA.py 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01 (SCORECARD 94-122 body; same hash as the wave 1 copy)
- recipeA.at-a4f674b3.out 4f29fd60e7ef0b166cf9857bbe2d5d114187f4f15030e13f928266a423fc0c5e
- recipeA.at-4084d897.out 7e223c15faff29ba2de51cfbf9247e3817b2e31da8adb475981e785b0920c217
- recipeA.at-97358f75.out e93e30406a89215741eb7676ad8795768e435d13d89881de37e4a4d878f55203
- SCORECARD.main-4084d897.md 2e1f9995709645b881394df6cb9190d510081e7254dd2cf113c3e77f1d7575ee
- SCORECARD.base-cd32264f.md fbd7691cdc6d58473d6e354b50f7bb0ee320ca36bb0bde66616de9c028ea4e9d (same hash as a4f674b3)
- SCORECARD.661ce3e3.md 3d82d3c8c39e9be1b11323d0ec57f09616707101cb9d25b57930e98d8f649b31
- AXES.fleet-e867f78.md 4492a9084262a2b530633ceb0a600ba54434476d669149871335c85f0bbf7655
- PROVINCE.6645585.md fa915ec7bd42ec516d0639c72d0fa443014ae5c4bf5c10ff90a661241c6ae312
- PROVINCE.cd32264f.md 73df22ffba7735cef880e3c3797f25c4a967dc617cf4132fd3e810cd17b79408
