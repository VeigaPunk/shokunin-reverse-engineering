# ReopenS079Snapshot: S079 re-open lines, round 27 wave 2

Seat: KaidokuR27.ReopenS079Snapshot. Leaf, read-only on the lane; no subagents, installs or lane edits.
Lane tip read: 4084d8975b684a8837b1c858eea0008ce9ab49e0 (main); claims freeze a4f674b343d8564e21f7eb8984630a95089c82d6. Checks ran 2026-10-22 15:35:59Z to 15:46:09Z (UTC). Scratch: /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReopenS079Snapshot/.

## Verdicts

- A1 Re-hash of 6.5.0 dist/ghidra/GhidraTargetSnapshot.js: holds.
- A2 Quote at :14 verbatim: holds. A3 Quote at :78 verbatim, at most 25 words: holds (6 words each).
- A4 Entry pointers :13-14 and :76-78 cover both quoted lines: holds.
- A4b Entry sentence "program name ... reports it as document" (entry lines 47-48) has no pointer: could-not-evaluate.
- A5 Re-open of a file the row did not list should have been a row change (cells), not a Gate note: fails (section 2).
- A6 S079 used-by names every citing entry or lesson (side check): fails. A7 Registry search log records the re-open (side check): fails (observation).

## 1. Checks (command, excerpt, exit code, UTC, verdict)

C1 Hash. `sha256sum …/rea-agents/dist/ghidra/GhidraTargetSnapshot.js` gives `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b`, 4063 bytes; exit 0; 15:35:59Z. Python re-check (exit 0, 15:40:13Z) matches. Lesson rows 40-41 and entry line 1 carry this digest. Holds.

C2 Quotes at :14 and :78. `python3 -I -B check_s079.py`, exit 0, 15:40:13Z: `PASS line 40 quote equals pkg line 14 minus indent :: 'const snapshotPath = join(runtimeRoot, `target-${expectedSha256.slice(0, 12)}${suffix}`);'` and `PASS line 41 quote equals pkg line 78 minus indent :: 'return /^\\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : ".bin";'`. Each equals the whole line after the four-space indent. Holds (A2, A3).

C3 Word count, same run: `PASS line 40 quote word count <= 25 :: 6 words`; `PASS line 41 … :: 6 words`. Holds (A3).

C4 Pointers, same run: `entry pointers (13, 14) (76, 78)`; `PASS quote line 14 lies inside entry pointer 13-14`; `PASS quote line 78 lies inside entry pointer 76-78`; `FAILED CHECKS 0`. Line 13 is the suffix assignment, line 76 opens `safeExtension`, line 77 is `extname(path)`. Holds (A4).

C5 Unpointed sentence. Read tool, entry lines 47-50, window 15:36:40Z to 15:41:57Z (no exit code printed). Line 48 says the Ghidra program name is the snapshot name and `binary_overview` reports it as `document`. The next pointer, `dist/domain/evidence.js:156-182`, covers subject fields. The only caller I found, `dist/ghidra/GhidraClient.js:418` (Python scan, 15:43:14Z; the grep tool shows the same line), stores `snapshot.path`. I did not find the import that makes the snapshot name the program name, or the code that fills `document`. Could-not-evaluate (A4b).

C6 Tarball identity. Python, 15:43:14Z; curl exit 0 for both registry URLs: `integrity sha512 equals registry dist.integrity: True`; `shasum sha1 equals registry dist.shasum: True`; tarball member `package/dist/ghidra/GhidraTargetSnapshot.js` has sha256 a27e4107…, 4063 bytes, `byte-identical: True`. Holds: the file sits inside the S080 identity chain.

C7 Lane identity. `git rev-parse HEAD` gives 4084d897…; `sha256sum` of the working copies equals `git show HEAD:<path> | sha256sum` for the lesson (da8392a0…), entry (34074737…) and SOURCES.md (12b2f182…). Exit 0, 15:36:40Z. No drift.

C8 Contract. CORPUS.md lines 107-118 (sha256 88556402…). Rule 2, line 116: "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`." Field `used-by` (lines 107-108) names "the knowledge entries or lessons citing the row". "re-opens" appears once, Rule 1 line 115: "Non-author verification re-opens a sample." The kaika copy (sha256 6c674a22…) matches lines 40-51 on reading. Read tool; hashes at 15:41:57Z.

C9 Census. CORPUS.md lines 133-147, run from the lane root (script sha256 d8f708b8…): 82 rows; 0 malformed; `A=76 B=5 C=1`; `mined=80 rejected=2`; duplicate ids, enum violations and missing used-by paths none; every step `[exit 0]`; 15:43:14Z. Holds, but the census only tests that listed paths exist, so it cannot see C10.

C10 used-by. Python, exit 0, 15:43:14Z. `S079 used-by:` the round-26 entry and round-26 lesson only. `cites S079:` round-27 entry (lines 1, 47); round-27 lesson (lines 22, 40, 41, 49, 56, 60); round-26-verifier-spotcheck (lines 95, 163, 165, 173). Same round, S082 lists the round-27 entry and lesson (SOURCES.md line 88). Lesson line 60: "S079 cells unchanged; its re-open is logged here". Fails (A6).

C11 Coverage. Python, 15:43:14Z: `S079 source or anchor cell names GhidraTargetSnapshot: False`. Python, 15:40:13Z: `S083 absent from registry`; `S083 mentions under corpus/ and tools/: 0`. Corpus lines naming the file: round-26 entry 77; round-27 entry 1, 47; round-27 lesson 40, 41, 47.

C12 Search log. Read tool, SOURCES.md lines 150-158, window 15:36:40Z to 15:41:57Z: round-27 notes only at line 153 (S081) and line 155 (S082). Lesson lines 47-49 say "included 3 as rows or row re-opens", while the registry gained two rows. Fails (observation).

C13 Markdown (observation). Lesson line 40 has unescaped backticks inside a single-backtick code span. [inference from the CommonMark code-span rule; not rendered] The stored bytes are verbatim. Minor.

C14 Sibling copy (observation). The 6.7.0 file (sha256 f9677c4d…, 5492 bytes) has the same suffix rule at lines 15-16 and 93-95 (grep; no timestamp printed; run after 15:43:14Z). S081 does not list it. Not part of the 6.5.0 claim.

## 2. A5: row change or Gate note?

Verdict: fails. A cell edit to S079 was not the contract route, and a Gate note alone does not comply.

(a) Rule 2 allows in-place change only to status, recheck and used-by. The file cannot enter S079's source or anchor cell in place (C11).
(b) A source that a knowledge entry relies on, and that no row's anchor covers, needs its own row [inference from Rule 1 and the anchor field]. Rule 1 says "A row is a claim", and the Gate records URL, date and quote for each new row. The next unused id is S083. Lesson rows 40-41 hold the Gate fields, but they are labelled S079 and feed no registry row.
(c) The cell change the contract does require here is used-by (C10): add the round-27 entry and lesson, logged old→new. Lesson line 60, "S079 cells unchanged", is the omission.
(d) Counter-reading [inference]: the Gate could carry new quotes for S079's teaches. That does not repair the registry: the anchor still lacks the file, and Rule 1 names the Gate for new rows only.
(e) Precedent: a re-opened source became a new row ("S054 is a superseding row", SOURCES.md line 131); S062 supersedes S058 (registry line 68). S081 is a new row for the 6.7.0 file, though the lane counts it in S037's family (lesson lines 52-56 apply QUALITY row 36). The round-26 spot-check (line 165) rejected that family argument.
(f) Predates round 27 [observation]: the round-26 entry already cites `dist/ghidra/GhidraTargetSnapshot.js:14` under S079 (entry lines 76-78), with `dist/process/PrivateRuntimeRoot.js:38` and `dist/application/binary/AnalysisSnapshotCache.js`. None of the three is in S079's file list (SOURCES.md line 85).

## 3. Recommendation for the L1 (not applied)

- Add S083 for the file at 6.5.0: anchor `:13-14` and `:76-78`, sha256 a27e…, kind code, tier A, status mined, opened 2026-10-22, recheck on-release, used-by the round-27 entry and lesson. Relabel lesson rows 40-41 to S083 and log the row in the lesson.
- Change S079 used-by in place to add the round-27 entry and lesson (logged old→new); decide whether the round-26 spot-check counts as citing.
- If no row is added, remove the snapshot-naming sentence (entry lines 44-48), and make the same choice for round-26 entry line 77.

## 4. Residual risk and verification gaps

- Unknown: the step that names the Ghidra program after the snapshot, and the code that fills `binary_overview.document` (C5). Envelope values behind `document` were not checked (outside this item).
- Rules 1 and 2 compared by reading, not byte for byte; no markdown renderer run.
- Only S079 was checked for unlisted-file citations; other rows may carry the same gap. No REA calls, by item design.

## 5. Artifacts (sha256; all under /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReopenS079Snapshot/)

- check_s079.py a4e660d4cdc9135234297d68babf8aa8f06cf82d03eeff33b9b9741044af2504
- check_s079.out 116cd0cdecea6521fb14a3762b32938a41f12a2e19c80dbacabd45e804b12806
- census_sources.sh d8f708b8a64fd4e9da1640d46231a2ca361a9952012f85cea115bbac5a6fb2db
- s079_used_by_census.out fd9d1bf4c229563350adaa1a2231db6a04e35d4104386ab4a492539150d1f306
- tarball_identity.out 74d642f60c3b77f7c04731f4cd48bf443519c9d1ceca135a2ebe065a96603afb
- tmp/rea-agents-6.5.0.tgz 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699
- tmp/rea-agents-6.5.0.version.json 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde

Tooling: no installs or upgrades. Used bash, git (read-only), curl, Python 3 standard library, and the read and grep tools.
