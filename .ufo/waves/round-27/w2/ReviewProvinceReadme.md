# ReviewProvinceReadme: round 27, wave 2 (falsify)

Seat: KaidokuR27.ReviewProvinceReadme. Leaf review; read-only on the lane.
Lane tip under review: 4084d8975b684a8837b1c858eea0008ce9ab49e0 (HEAD). Base: cd32264f7ee356a9c0f48bd8e3fcdac222db22a0. Claims frozen at a4f674b343d8564e21f7eb8984630a95089c82d6.
Git state: HEAD is detached (`git symbolic-ref -q HEAD` exits 1); the brief said branch main. The working copies of corpus/README.md and PROVINCE.md equal HEAD (sha256 cbb74c3d1f13... and 74a40e736... ; exit 0 at 15:37:12Z).
Scope: the 26 lines added to corpus/README.md (coverage-map row line 76; Knowledge index row line 168; Known-gaps sub-bullets lines 209-211) and to PROVINCE.md (round-27 section, lines 305-324).

## Verdicts

| # | What was attacked | Verdict |
|---|---|---|
| 1 | Coverage-map row uses the entry stem that recipe A expects | holds |
| 2 | Numbers in README and PROVINCE match the entry and receipts | holds (one minor gap, 2d) |
| 3 | Round-27 text discloses the frozen C1 counter result (15 of 16, exit 1) | fails |
| 4 | Nothing claims a Frontier item moved to Core | holds (one note) |
| 5 | The tinyxxd layout "same-path repeat" is an independent run | could-not-evaluate |

## Check 1: coverage-map stem (holds)

- Command: recipe A, copied verbatim from SCORECARD.md lines 93-123 (scratch recipe_a.py), run from the lane with the revision as argument.
- Output at 4084d897: `{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 110, "mapped": 110, "missing": [], "rule_blocks": 17, ...}`. Exit 0, batch ending 15:38:48Z. Matches SCORECARD.md:3099 (110/110, depth 17/17).
- Probe in the same run: `"coverage_section_stems_with_r27": ["2026-10-22-r27-renamed-copy-evidence-id-identity"]`, `"r27_stem_in_files": true`.
- At cd32264f (exit 0, same batch): knowledge_files 109, mapped 109, missing [], dangling []. The count moved by one, the new entry.
- The row stem equals the file stem of corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md. Recipe A's pattern `2026-10-\d{2}-[a-z0-9-]+` captures the whole stem. No dangling stem.
- Limit: recipe A reads only the coverage-map section, so the Knowledge index row was checked by hand (check 2).

## Check 2: numbers against entry and receipts (holds, one minor gap)

a. Command: `cut -f3 corpus/evidence/round-27/c1/table.tsv | sort | uniq -c`, plus an awk count of base equal to repeat. Output: 10 content-keyed, 6 rename-sensitive, 16 rows; base equals repeat in 16 of 16 rows. Exit 0 at 15:40:35Z. README lines 76 and 209 and PROVINCE line 314 say the same.
b. Command: count of envelope files and runs.tsv columns 13-14. Output: 48 envelope files; 48 runs, all pkg_version 6.5.0 and pkg_json_sha256 a500302319...050a6c. Exit 0 at 15:41:35Z. Matches "three runs each, eight verbs, two carriers".
c. Command: `sha256sum /usr/bin/jq /usr/bin/tinyxxd` and the two renamed copies. Output: e815667571...7806 and 7b1e5d0c970...ae65; each equals its renamed copy under /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/. Exit 0 at 15:40:35Z. "Byte-identical copy" holds.
d. Command: `/usr/bin/jq -e 'tostring | contains("12.1.4")'` over the 48 envelopes (output saved as ghidra-version-check.txt, sha256 67de169e...fe16). Output: 42 envelopes contain 12.1.4; the 6 that do not are exactly the six inspect-binary-layout envelopes. Exit 0 at 15:45:21Z. Holds for the seven Ghidra-backed verbs. Minor gap: the inspect-binary-layout envelopes record no Ghidra build, so "one Ghidra build (12.1.4)" is not evidenced for that verb in README lines 76 and 209 or PROVINCE line 312.
e. Command: `/usr/bin/jq -r '.data.normalized_result.document'` on jq and tinyxxd analyze envelopes. Output: target-e815667571d0.bin and .dat (jq); target-7b1e5d0c970a.bin and .dat (tinyxxd). Exit 0 at 15:39:57Z. The observation holds. The causal word "because" rests on code reading in the entry (lines 42-50), which line 209 does not label as inference. Minor.
f. Command: `cut -f1-3` on corpus/evidence/round-26/c1/table.tsv. Output: analyze and inspect content-keyed; inspect-binary-layout path-sensitive (jq). Exit 0 at 15:40:35Z. Matches the "against round 26" wording. Holds.
g. Command: grep of corpus/SOURCES.md and the entry header. Output: S079 at line 85, S082 at line 88; entry verified-at 2026-10-22. Exit 0 at 15:38:22Z. "48 committed envelopes" matches check b. Holds.
h. Command: `cut -f5` over all 48 rows of corpus/evidence/round-27/c2/r27-c1-attribution.tsv; the same on keyless-default.tsv and keyless-parse.tsv. Output: 42 `6.5.0`, 6 `both`, no `6.7.0`, no `none`; keyless-default 37 `both`; keyless-parse 37 accept (6.5.0) and 37 reject (6.7.0). Exit 0 at 15:39:57Z. Re-run of the committed tool at HEAD on the 48 envelopes (node v24.21.0): exit 0, stderr 0 bytes, stdout byte-identical to the committed TSV, at 15:41:16Z. The tool has no file-write calls (grep, no matches). Holds.
i. Command: sha256sum of the two counters, and `git diff --stat a4f674b3 4084d897 -- tools/round-27`. Output: e0a07995...743bb7 and d8de667f...209bd3, both equal to claims.json; since the freeze only assemble-c1.py (+66) and xpin-attribute.mjs (+267) were added. Exit 0 at 15:38:22Z. The counters were not edited. Holds.

## Check 3: C1 counter result not disclosed (fails)

Counterexample. Sandbox clone at 4084d897; command `python3 -I -B tools/round-27/c1-rename-identity.py --root <clone> --rev 4084d897`; exit 1; 15:38:48Z. Output excerpt:
  `INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run`
  `rows_complete=15/16 entry_ok=1`
The frozen target is 16 of 16 rows, entry_ok 1, exit 0 (claims.json, claim R27-C1).

The lane records the miss in SCORECARD.md:3090 ("honest stop, 15 of 16") and :3096 ("target missed"); LOG.md:2977 ("missed by one row"); QUALITY.md:50; corpus/lessons/round-27.md:68 (M27-2: "R27-C1 measures 15 of 16"); and the entry's Limits section (lines 88-92).

The README and PROVINCE round-27 text does not:
- README line 76 (coverage state, "held narrowly"): "10 of 16 content-keyed, 6 rename-sensitive, 0 unstable".
- README line 209 (Known gaps): the same counts.
- PROVINCE lines 311-314 (Core addition): "now rests on two carriers and a renamed copy ... 10 of 16 content-keyed, 6 rename-sensitive, 0 unstable".

None of these says the counter is incomplete, that it counts 15 of 16, or that the sixteenth verdict is derived by hand. The Known-gaps section (README 203-211) has no bullet for it, although lesson M27-2 says the row "stays incomplete". README line 76's "held narrowly" contradicts SCORECARD's "honest stop" for the same claim.

Not a timing gap: the README map rows went in commit c6d619a3, after data commit 9dca26df, where the entry says the counter already gave 15 of 16.
Not a numeric error: the sixteenth row's ids check out. `/usr/bin/jq -r '.. | strings | select(startswith("ev_"))'` on the tinyxxd inspect-binary-layout base envelope gives ev_aeeab0db1f5c0d08...7ca6; the repeat is byte-identical; the renamed envelope gives ev_02e910c6b112a964...1891. Rename-sensitive follows from the rule (exit 0, 15:40:35Z). The defect is disclosure: a Core addition and a coverage state rest on a row the frozen instrument refuses, and the text does not say so.
Suggested fix for the lane lead (not applied): name the counter status (15 of 16, exit 1, the INCOMPLETE row) in README line 76, add a Known-gaps bullet, and qualify PROVINCE lines 311-314 to "15 of 16 counter-verified; the sixteenth derived by hand from the ids".

## Check 4: Frontier not moved to Core (holds, one note)

- Command: `git diff -U0 cd32264f 4084d897 -- PROVINCE.md corpus/README.md`. Output: 26 insertions, 0 deletions; every hunk is an addition. Exit 0 at 15:37:07Z.
- PROVINCE Frontier section (lines 73-94) is untouched. Its five bullets (PE subtypes; recorded crashes above 32 MiB; alternate providers; macOS-only surfaces; EVM bytecode extended) are exactly the five named at lines 307-309, which say none is retired.
- Scan of the 26 added lines (text read between 15:37:12Z and 15:38:22Z; the read tool does not stamp time): "Frontier" appears only in "Neither retires a Frontier bullet" and "the Frontier list ... is unchanged". No line says an item moved, was promoted or was retired. README additions do not mention Frontier.
- Command: targeted grep of LOG.md for move-to-Core wording (single-line pattern). Output: matches at lines 17-21 and 36-40 ("Promoted to Core" in earlier entries), 143-147 and 1067-1070 (Frontier-versus-Core drift notes), 2954-2958 (round 25); none in the round-27 entry (lines 2972-2980). Exit 0 at 15:40:35Z.
- Note, not a violation: MINT.md line 36 still lists "cross-version diffing" as a claimed Frontier item. PROVINCE's "Cross-version residuals" bullet (lines 157-160) concerns application-version comparison and is untouched; the round-27 Core addition is REA pin attribution. The MINT wording is unreconciled; that predates round 27.

## Check 5: tinyxxd layout "same-path repeat" (could-not-evaluate)

- Command: cmp of the base and repeat envelopes. Output: byte-identical (sha256 f601872b...3130 for both). Exit 0 at 15:39:36Z. Both meta blocks read duration 132ms; the meta block holds only command and duration.
- Command: `/usr/bin/jq -r '.meta.duration'` over the base and repeat envelopes of all 8 verbs on both carriers. Output: the other 15 pairs differ (for example jq inspect-binary-layout 143ms and 144ms; tinyxxd inspect 5944ms and 6674ms). Exit 0 at 15:39:57Z.
- The receipts cannot tell a replayed stored envelope from two computations that matched to the millisecond. LOG.md:2977 and lesson M27-2 call the runs "genuine"; README lines 76 and 209 say "three runs each" and do not mention this pair. This is residual risk for the same-path control; no number is wrong.

## Residual risk and gaps

- The C1 counter was run at HEAD only; the 9dca26df result comes from the entry and lesson.
- SCORECARD and LOG were checked by targeted search only, not read in full.
- The S079 source lines cited by the entry were not opened; they are outside these two files.
- No REA call was run.

## Artifacts (sha256), scratch directory /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewProvinceReadme/

- recipe_a.py eb9bb75d73d3e3239c75efbbefc2d902dae0cda3a25d48bb431c9c941b3b6de4
- recipeA_base.out 54a3117f5c9c84f20b4c0426ad8b445871153ebb9a5fa083e01da3598ff5c473
- recipeA_head.out 7a06c5e3767eae45807272b1d8c8dc93f4831e9d14e6b6abb218eef839ce9a9f
- recipeA_data.out eefbc84c0a8425918e8888fa9897aaf1abc03ba8a263fea083a7d4ac7a815491
- c1-counter-head.out a02047192099a8546be7162dbff293fd108e8357be225be30f67fa0e463ccfb8
- xpin-r27-c1.out 751bbce4481dc79c4b168f3c0cbb513e12930d18adce0f287716db2496fd4599
- ghidra-version-check.txt 67de169ec6e10e098105f01654a9c5a8645ae686debae7cc600089c53dc2fe16
- review-commands.txt c6e9d74d26c9fe6ccaf727e8ba229af2f7a3db8e96c51d9bafc1481e2ac609b6
- six empty .err files: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- clone/: sandbox clone at 4084d897, used only for the counter run.

Installs or updates: none. Host tools used: python3, node v24.21.0, git (read-only), /usr/bin/jq (read-only on lane files).

## Addendum: lane working tree changed during review (uncommitted)
At 15:45:52Z `git status` showed uncommitted edits (README line 212; PROVINCE lines 325-326). HEAD was still 4084d897 at 15:46:02Z; the verdicts above are for the committed tip.
- The uncommitted lines disclose the 15-of-16 miss, matching check 3's counter output; check 3 would hold once committed. Not verified by me: .ufo/waves/round-27/w2/RederiveC1Own.md, FalsifyExtensionOnly.md, and the entry's uncommitted corrections section.
- The sixteenth row checks out from the envelopes (check 3). PROVINCE's "genuine" repeats the check 5 issue; "extensions that do not change the route" is unclear wording. Check 4 holds: no Frontier mention in the new lines.
