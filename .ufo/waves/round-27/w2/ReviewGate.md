# ReviewGate: round-27 Gate against SOURCES contract v1

Seat KaidokuR27.ReviewGate, leaf reviewer, read-only on the lane. Scratch: /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewGate/ (hashes in section 6). Nothing was staged, committed or edited by this seat.
Pin: lane tip 4084d8975b684a8837b1c858eea0008ce9ab49e0 on main (`git rev-parse HEAD`, 2026-10-22T15:37:00Z, exit 0). Base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0.
Moved: at 15:48:37Z HEAD was c4ec7a2e04889ed3a07fa1bd03550fbf467e0c19 (one commit on the pin), and at 15:48:54Z the working tree had uncommitted edits to SOURCES.md, the round-27 knowledge entry and the round-27 lesson. Section 3 covers that state.
Rules: /home/vgpnk/Projects/shokunin/CORPUS.md, "SOURCES.md — contract v1" (lines 64-156); corpus/QUALITY.md row 36 (line 46).
Tooling: no installs or upgrades were needed; used curl 8.23.0, Python 3.14.8, jq 1.8.2, bsdtar, gzip, sha256sum, all already present. No REA call, no MCP device, no subagent.

## 1. Verdicts (item: pin 4084d897 / moved tree 15:50Z)

A. Each new row has a Gate line with URL or path, access date, sha256 and a quote of 25 words or fewer: FAILS on fidelity. Presence holds (14 of 14 new-row lines, plus 2 S079 re-open lines). Counterexamples: row 11 hash does not reproduce from its URL; rows 11-14 quotes are not source bytes (K1, K5). Moved: unchanged; S083's three new lines hold (M3).
B. Search-log sentence counts (rule 5): FAILS. Gate sentence 6/6/3/1 does not add up, and no note has a stop rationale (K11). Moved: FAILS again; the S083 entry repeats the pattern (M5).
C. Row changes old to new logged: pin HOLDS for the S081 and S082 additions, FAILS for S079 used-by, which omitted the round-27 entry and lesson (K10). Moved: HOLDS; S079 changed only used-by, S083 added, both logged in the lesson (M3, uncommitted).
D. Round-26 S037 reversal recorded as QUALITY row 36 asks: FAILS in part. Pointers hold (K12). Fails: SCORECARD silent, LOG gives no line, not-needed search absent from the lesson Gate (K7, K13). Moved: same failures (M5).
E. Census, CORPUS.md commands: HOLDS at the pin (82 rows, 0 malformed, 0 duplicate ids, 0 enum or tier violations, 0 missing used-by paths; K9) and on the moved tree (83 rows, 81 mined; M4).
Overall against contract v1: NOT CONFORMANT at the pin. On the moved tree F1 and F3 are fixed in the working tree; F2, F4, F5, F6 (disclosed only), F7-F10 remain.

## 2. Checks at the pin (command; excerpt; exit; UTC; verdict)

K1. `python3 -I -B quote_gate_check.py` over all 16 Gate lines; excerpt `rows_with_a_flag=5 of 16` (rows 5, 11, 12, 13, 14); quote words 1-10; cited lines 178, 183, 8, 4, 14, 78 and pacman key lines hold; exit 0; 15:43:01Z; holds for presence, fails fidelity on flagged rows.
K2. `sha256sum` of installed files: 6.7.0 evidence.js a3fb9f02..., canonicalDigest.js f46d6bd4..., package.json 3f6c47fb...; 6.5.0 GhidraTargetSnapshot.js a27e4107...; exit 0; 15:40:54Z; equal to Gate lines 1-4, 15, 16; holds.
K3. `curl -fsSL` of rea-agents-6.7.0.tgz: sha256 20958a66..., sha1 11f23ba3..., computed sha512 equals registry dist.integrity; `diff -rq` of unpacked dist and installed dist empty; exit 0; 15:40:54Z; holds; row 5 records the tarball hash, not the member's (F7).
K4. `sha256sum` pacman records: desc a2d70e53..., sync member a8a2df3f..., /usr/bin/tinyxxd 7b1e5d0c...; mtree line `./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c...`; `date -u -d @1790704346` gives 2026-09-29T17:52:26Z; exit 0; 15:40:54Z; holds for rows 6-10.
K5. Arch page: four live curl fetches (15:40-15:41Z) gave four hashes (0d6136e0..., c9afb765..., a541ddfc..., 890c746e...); the retained seat copy seats/SrcS082/arch-tinyxxd.html gives the Gate hash 4e5fff12... (exit 0, 15:44:53Z); the page's script nonce differs per fetch (arch_check.py, exit 0, 15:46:24Z); the three page quotes span tags and are not contiguous; JSON hash 30e4c410... reproduces live, and raw JSON has a space after the colon. Verdict: rows 11-13 fail reproducibility from the URL; row 14 fails quote fidelity.
K6. S081 teaches against code (read, 15:41Z): 6.7.0 dist/domain/evidence.js:178 projects relationship_coverage unconditionally; 6.5.0 :175-177 projects it only when not null. Holds; the 6.5.0 half is not quoted in this Gate.
K7. `grep -rn "relationship_coverage" <6.7.0 dist> | wc -l` gives 74; distinct files 25; 6.5.0 tree 73; exit 0; 15:40:54Z and 15:46:16Z; reproduces the recorded search, which sits only in the SOURCES search log (F5).
K8. `git diff cd32264f 4084d897 -- corpus/SOURCES.md`: numstat `6 0`; S081 and S082 added, two search-log entries, S079, S037, S080 unchanged; exit 0; 15:46:16Z; holds.
K9. Census checks 1-7 on the pin file: 82 / 0 / A=76 B=5 C=1 / mined=80 rejected=2 / no output / no output / no output; exit 0 each; 15:39:11Z and 15:46:16Z; holds.
K10. S079 used-by at the pin lists the round-26 entry and round-26 lesson only; round-27 entry line 1 and lesson lines 22, 40-41 cite S079; `grep -c GhidraTargetSnapshot corpus/SOURCES.md` gives 0 (exit 1); fails (F1, F3). S037 used-by unchanged; its citation in the Gate is prose only (see Info).
K11. Search-log arithmetic: Gate sentence "identified 6, screened 6, included 3 as rows or row re-opens, excluded 1" then "Rejected: none." (lesson line 50); S081 entry (SOURCES line 154) identified 3, screened 3, included 1, excluded 1; S082 entry (line 156) identified 3 families, screened 3, included 1 row, excluded 0; `grep -n -i stop` on the lesson: no output; of the SOURCES lines 117-152, 16 carry "Stop:" (round 26 at 152), lines 154 and 156 carry none; exit 0; 15:48:37Z; fails.
K12. round-26.md:37 reads "is already row S037's family; no new row for it. Rejected: none."; round-26-verifier-spotcheck.md:165 reads "disagree (minor)"; :197 is "routed defect 1"; S081 anchor cites all three; exit 0; 15:46:16Z; holds.
K13. `grep -n "round-26-verifier-spotcheck" SCORECARD.md LOG.md`: one hit, LOG.md:2975 (path and "routed defects 1 and 4", no line); SCORECARD round-27 region lines 3090-3200 has no spot-check pointer (awk, exit 0); fails (F2).
K14. round-26.md Gate lines 19-37: no consumer-code search command; exit 0; 15:48:37Z; fails for round 26 (F9).

## 3. Moved tree (HEAD c4ec7a2e plus working tree, 15:48-15:51Z)

M1. `git diff --stat 4084d897 HEAD`: 7 files, 65 insertions (lesson +9 appended corrections, knowledge entry +30, SCORECARD +8, SKILL +10, PROVINCE +2, README +2, one r17 pointer +4); LOG.md unchanged; 15:49:03Z.
M2. `git status --porcelain` (15:48:54Z): modified SOURCES.md, knowledge entry and lesson; working-tree diff saved as worktree-vs-head.diff.
M3. moved_state_check.py (exit 0, 15:50:30Z): S079 changed cells against the pin are used-by only; S083 row has 11 cells, status mined, opened 2026-10-22, recheck on-release; S083 anchor hashes match installed files (64c07dae... binary-BVOr2mgE.js; db16aed4... ReaGhidraBridge.java; a27e4107... GhidraTargetSnapshot.js); three S083 Gate lines have sha in row and quote on the cited line (binary :5318 and :293; bridge :1975); anchor lines :5261, :293, :5318 and bridge :1972-1976 read by awk (exit 0, 15:50:48Z). Verdict: F1 and F3 fixed, uncommitted.
M4. Census on the working tree (exit 0 each, 15:50:22Z): 83 rows, 0 malformed, A=77 B=5 C=1, mined=81 rejected=2, no duplicates, no enum violations, no missing used-by paths; holds.
M5. Re-run of K11, K13, K14 on the moved state: lesson Gate still has no consumer-search command, stop text or spot-check result line; S083 entry (SOURCES line 158) has no stop clause; SCORECARD at c4ec7a2e has no round-26 spot-check pointer (15:50:22Z); F2, F4, F5, F9, F10 open.
M6. Lesson header line 21 still reads "Each quote is contiguous"; the appended correction admits rows 11-14 are not; F6 disclosed, not repaired.
M7. Re-checked 15:53:54Z: SCORECARD.md has a 9-line uncommitted edit (hygiene and wave-2 notes, scorecard-worktree-vs-head.diff, sha256 41c3477d482d12eb8e9d2dadcb3b65fe2bf214479b8f67f42107e6ae649bb628); it adds no round-26 spot-check pointer, so F2 stays open.

## 4. Findings by severity (pin status; moved-tree status in brackets)

High
- F1. The S079 re-open had no registry row: the round-27 entry's extension mechanism cites dist/ghidra/GhidraTargetSnapshot.js as "S079 family" (K10), and no row names that file; anchors cannot change in place. [Moved: fixed by row S083 (M3); needs a commit.]
- F2. QUALITY row 36 fails its outside-disagreement clause: the round-27 SCORECARD section is silent on the round-26 spot-check (K13), and the LOG entry gives path and defect numbers but no line. Fix: add round-26-verifier-spotcheck.md:165 and :197 to the SCORECARD round-27 section and the LOG entry. [Moved: open.]

Medium
- F3. S079 used-by omitted the round-27 entry and lesson, which cite it (K10). [Moved: fixed in working tree (M3); needs a commit.]
- F4. Search-log counts do not reconcile and no note has a stop rationale (K11, M5). "Included" counts rows while "identified" and "screened" count candidates. Fix: one unit, and a stop clause in the Gate sentence and in the S081, S082 and S083 entries. [Moved: open.]
- F5. The not-needed exclusion ("already row S037's dataset family") has its consumer search only in SOURCES (K7); QUALITY row 36 requires it in the lesson Gate, and "Rejected: none." (line 50) sits beside that exclusion. Fix: copy the command and counts (74 hits, 25 files; 73 at 6.5.0) into the Gate and reword. [Moved: open.]
- F6. Arch rows 11-14 (K5): the hash ties to a retained copy, not to the URL; quotes span tags (11-13) or drop a space (14); the header claim "contiguous" stands. Fix: name the retained artifact path, quote contiguous text (the title "Arch Linux - tinyxxd 1.3.17-1 (x86_64)" is one), write the JSON spacing exactly, correct the header. The registry row S082 repeats the composite Build Date string and cannot change in place. [Moved: disclosed in an appended correction, not repaired.]

Low
- F7. Rows 2 and 5 store \` escapes inside code spans, so the cell is not source text until unescaped (K1); [INFERENCE: such spans probably render broken, not rendered here]. Row 5 records the tarball hash, not the member file's (a3fb9f02..., equal to the installed file). [Moved: open.]
- F8. S082 teaches says the version agrees with the Arch record; no Gate quote covers the version. [Moved: open.]
- F9. The round-26 not-needed rejection recorded no consumer search (K14); row 36 says that fails the row, and round 27 neither discloses nor repairs it. [Moved: open.]

Info
- F10. The Gate has no spot-check result line, which the CORPUS "## Gate" rule lists. [Moved: open.]
- Not counted: S037 used-by does not list the round-27 lesson, which names S037 in prose; round 26 did the same.
- The S083 anchor cites :5261 with no Gate quote; the line is the snapshot path (M3).

## 5. Residual risk and gaps

- All 16 pin Gate lines and the 3 S083 lines were re-opened; nothing was sampled.
- Not checked: the lane's correction claims about realpath, symlinks and Hopper (read from code by the lane), other c4ec7a2e edits beyond the pointers, and the R27-C1 and R27-C2 numbers (other seats).
- The working tree can still change; re-run moved_state_check.py and quote_gate_check.py after the commit.
- The Arch page is served per request; only the retained copy reproduces its hash.

## 6. Artifacts (scratch dir; full list with sha256 in SHA256SUMS-final.txt)

- reopen/quote_gate_check.py 4b95e2ae9ddc2ca7721dc7e7fa976c55211d68dc2b882641e0c86d27dd45d2d1
- reopen/quote_gate_check.out 0c2900be8e90a0964652ee7ce47f563bbbeabd55e509feb305e707e5be32184f
- reopen/moved_state_check.py 44de8f371557ea8f66faaa7b8b1c1ba5b1e585fa0ef062892bd888c170a0e114
- reopen/moved-state-check.out 1fae27b3c69bd0098f09a427a018d4a2a41eb167dbe4939f0a281928149baa70
- reopen/arch_check.py 1b118cd24a5f8049ccfbeccfbba7df106c24840fd6c7a0ceb740526e62436b85
- reopen/arch-check.out 0198ef3effdf60850454473bbe41065ab962643f78d4e72f1c30c5390cfee2d0
- census-tip.out bd067274a8bf4754ee89ddbc921c9de7d71f62242b176d55695cf3e24e2ad7ad
- moved-state-census-and-checks.out 54a1de9b0e38119987af488e967394fdbcfa245e10932680e0cdb8ee292c5e36
- gate-search-pointers.out 616fe3bac83a31a4d9ef0bdf9e0bebab620dbbb489cb8a366ba7c097d7714eb0
- pointers.out 7c055ebce648358638cff23297ea334c074fc1acc541838ff41da1e40d468bba
- sources-diff.out d76f0848d94ecbdfaee53622a00f5f472972de8740b97f5784f4ced5d882af69
- commit-delta-lesson-entry.diff 115305751e202f8475d4fe21b265c60042e23fa0a083a67d75ab17d23582b0e0
- worktree-vs-head.diff 0cb07c1c69a7154ba2392d6e42dfda079ee606fc006f848e000d9c72e155e84c
- SOURCES-base-cd32264f.md ef4385a138f2f1430bbb2fbe0c50b5a69cc74dec604fbb30c23031e9ee33c602
- s083-anchor-lines.out 4dc9f985ec6c084681b6f6ad7b6ab5185409b005c9e00c32539588096792a084
- reopen/rea-agents-6.7.0.tgz 20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90
- reopen/arch-json.json 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb
- retained, read only, outside scratch: seats/SrcS082/arch-tinyxxd.html 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89
