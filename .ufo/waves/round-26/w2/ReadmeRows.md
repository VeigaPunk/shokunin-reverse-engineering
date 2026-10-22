# R26 wave 2, ReadmeRows (seat KaidokuR26.ReadmeRows)

Scope: corpus/README.md round-26 coverage-map row (line 75), knowledge row (line 166) and Known-gaps sub-bullet (line 206), checked against the entry and the table; SCORECARD recipe A at the tip.
Tip checked: fe3eb4edf410244eff46151a148c8f754be1ce80 (committed bytes, read with git show into scratch). Lane base a0639d8e61e486e2a716ff94cddd89a73200a02c. Access date 2026-10-22. All times UTC.

## Verdicts

- Coverage-map row (README:75): HOLDS WITH TWO CORRECTIONS (F1, F2).
- Knowledge row (README:166): HOLDS. No defect found.
- Known-gaps sub-bullet (README:206): HOLDS WITH THREE CORRECTIONS (F1, F2, F3).
- Command A at the tip: HOLDS. mapped 109 of 109; missing [], dangling [], exit 0.

No row claim meets a counterexample. Every correction is wording or scope.

## Command A at the tip

Recipe: SCORECARD.md lines 93-123 (the python block), extracted verbatim by script into scratch recipeA.py (sha256 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01). Run as `python3 -I -B recipeA.py <REV>` with the lane root as the working directory.

- Tip fe3eb4ed, exit 0, 2026-10-22T13:01:10Z: {"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 109, "mapped": 109, "missing": [], "revision": "fe3eb4edf410244eff46151a148c8f754be1ce80", "rule_blocks": 17}
- ebe2cb4a, exit 0, same time: knowledge_files 109, mapped 109.
- a0639d8e (base), exit 0, same time: knowledge_files 108, mapped 108.
- Falsifier in a sandbox clone (commit 19f2de44, README:75 deleted), exit 0, 13:04:05Z: mapped 108, knowledge_files 109, missing ["2026-10-22-r26-native-reader-evidence-id-identity"], coverage_score 9.91. The 109 count rests on the coverage-map row alone. The knowledge table (line 166) and the Known-gaps bullet (line 206) sit outside the Coverage map section and count for nothing.
- The SCORECARD owned-axes coverage row (109/109, measured ebe2cb4a) matches command A at that revision.

## What holds (observation unless marked)

- Verb set: the table lists the eight frozen verbs (analyze, inspect, decompile, xrefs, read-bytes, function, instructions, inspect-binary-layout). Seven are content-keyed and one is path-sensitive. Matches README:75 and :206. Programmatic check, about 13:02Z, exit 0.
- Entry abbreviations (entry lines 29-36) match the table ids by prefix and suffix for all eight verbs.
- R26-C1 instrument (committed copy, sha256 11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa), run on the sandbox clone root: tip gives rows_complete 8 of 8, entry_ok 1, exit 0; base gives rows_complete 0, entry_ok 0, exit 1. Matches claims.json.
- recompute-ids.py on the 24 tip envelopes: "recomputed ids: 24 match of 24 total", exit 0, 13:03Z.
- 24 envelopes are committed under corpus/evidence/round-26/c1/envelopes (git ls-tree at tip).
- Sources S079 and S080 (SOURCES.md lines 85-86) and the lesson Gate rows (corpus/lessons/round-26.md lines 27-31) show opened 2026-10-22.
- analyze and inspect share one operation: installed cli.js (sha256 168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204) lines 10347 and 10355 both call runDirectAnalysis(args.path, "binary_overview", ...). The table gives both one id.
- inspect-binary-layout path mechanism: installed BinaryLayoutService.js (sha256 b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4, the digest S079 records) line 33 requires an absolute path, line 61 sets parameters to input.data, line 67 writes an artifact-path location. The alternate-copy envelope (jq, 13:04Z) carries the run path in subject.local_path, parameters.path, normalized_result.artifact.path and the location; function envelopes carry none of these.

## Findings

F1 (minor, scope omitted). README:75 and :206.
- The entry Limits paragraph (entry line 108) says "one address for the five address-taking verbs, default parameters otherwise." Neither row says so. A grep of the tip README for "0x103fa0|default param|one address|address-taking" returned no matches, 13:05Z.
- The content-keyed verdicts for decompile, xrefs, read-bytes, function and instructions were measured only at 0x103fa0 (entry line 20). A reader could take them as general.
- Correction: add "at 0x103fa0 for the five address-taking verbs; default parameters" to both rows.

F2 (minor, wording ahead of the measurement). README:75 ("ids are pin-specific (6.5.0 versus 6.7.0 differ)") and README:206 ("Id values differ between 6.5.0 and 6.7.0 for the same bytes").
- Live REA CLI runs on /usr/bin/jq, 13:02Z, each exit 0; --version printed 6.5.0 and 6.7.0. Producing argv: `TMPDIR=<scratch>/tmp npx -y rea-agents@<pin> <argv>` with argv `function /usr/bin/jq 0x103fa0`, `inspect-binary-layout /usr/bin/jq` and `analyze /usr/bin/jq`, each with `--format json --full-output`; the 6.5.0 control is `function`.
  - function 0x103fa0, 6.5.0 control: ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5. Equals the table base id.
  - function, 6.7.0 (13:02:12Z): ev_177586c695241d1e2552be2ca7def13c291756b00ae13c226875c6c615915be8. Equals the value quoted in the entry's Pin dependence section.
  - inspect-binary-layout, 6.7.0 (13:02:13Z): ev_d1256a9649ddcb43a9251b202eb4dafb049ab50c11f92f907915899fa3d4cb2a. Equals the entry quote. The 6.5.0 id is ev_294a449c.
  - analyze, 6.7.0 (13:02:20Z): ev_9bb49adfaa0ab12ed6bd73818732c8c9f08e661f0c56f6bacb55c6028f36b8aa. The 6.5.0 id is ev_14f9d92f. Differs (new datum).
- No verb kept its id across pins. That is measured for three of the eight verbs, one run each.
- Source gives the mechanism for all eight (inference for five): 6.7.0 evidence.js line 178 always emits relationship_coverage; 6.5.0 evidence.js lines 175-177 omit it when null. sha256 6.5.0 f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff, 6.7.0 a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb. The entry's own text (line 95) calls the eight-verb relation inference.
- Correction: "measured at 6.7.0 for function, inspect-binary-layout and analyze (one run each); the other five by source inference."

F3 (nit, citation precision). README:206, "measured at 6.4.0 in corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md:83-85".
- The 6.4.0 pin is stated at r5-01 line 7 and in the verify lines 26 and 28 (`grep -n 6\.4\.0` on the committed r5-01, exit 0, 13:03Z). It is not inside lines 83-85.
- That 6.4.0 run used a patched embedded RISC-V ELF carve with two different file names (r5-01 line 85), not /usr/bin/jq. The sentence should cite line 7 for the pin and name the carrier.

Out of scope, noted only. r5-01 line 85 points to corpus/README.md:133 for the r4 path-sensitivity note. Line 133 is now a Knowledge-table row (the r8-02 queue entry), not that note. Pre-existing; the qualify-don't-rewrite rule applies; no action proposed.

## Residual risk and verification gaps

- Live replay: I re-ran only function (6.5.0 control) and three 6.7.0 calls. The seven content-keyed verdicts at 6.5.0 were not replayed by me. The committed envelopes recompute 24 of 24 and the instrument passes; replay of the 24 runs belongs to the replay seats.
- Address, parameter and file-name sensitivity: untested for other addresses, other parameters and other file names.
- Lesson Gate and SOURCES quotes: I confirmed dates and ids only, not the located quotes (other seats).
- Entry heading at line 83 says "the verdicts transfer across pins" as a finding; the body (lines 93-95) calls it inference. Not a README row; noted for the entry review seat.
- The lane tree holds other seats' uncommitted wave-1 edits (git status at 13:06Z: M w1/CounterC1.md, EntryCorrection.md, MutR25Coverage.md; new w1/CustodyNote.md, ScorecardRows.md). I read committed bytes only; none of my evidence came from those files.
- Lane touch: read-only git only (show, ls-tree, log, diff, rev-parse, git clone of the lane into scratch, and git status twice: short form at the start, porcelain form at 13:06Z). git status may refresh the index stat cache without changing content. No lane file was written by me apart from this report.

## Tooling and artifacts

- Installed or upgraded: nothing. npx ran rea-agents@6.5.0 and @6.7.0 from the cache roots named in the contract (ad9a3fdbcad992c6 and a1722018f28f9df2); no install step appeared in the output.
- Scratch root: /fast/scratch/hyaku/kaidoku-r26/seats/w2/ReadmeRows/ (manifest.sha256 lists the run artifacts below; the committed copies are hashed in committed.sha256).
  - recipeA.py 236dde1d; commandA-fe3eb4ed.json c915212f; commandA-ebe2cb4a.json 291bd537; commandA-a0639d8e.json 56f064fc; commandA-mutant-no-r26-row.json 068e6c33.
  - c1-tip.json 4a57e912; c1-base.json fcb49c34; recompute-tip.txt 3e45dbb0.
  - rea650-function.json 47e0af7a; rea670-function.json e2516662; rea670-inspect-binary-layout.json 2a9202df; rea670-analyze.json 081b3085.
  - committed/ holds git show copies at fe3eb4ed (sha256 list in committed.sha256); installed-sources.sha256 holds the installed-package digests.
- Sandbox clone: clone/ (HEAD 19f2de44 = mutant on top of fe3eb4ed). Not the lane.
- Sources, plain file reads, access 2026-10-22, sha256: corpus/README.md ff5fc422; corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md b03fcdc4; evidence table.tsv 89eca152; SOURCES.md 94590093; lessons/round-26.md 28f55b8f; SCORECARD.md 10ae7acf; SKILL.md 9c2494cd; r5-01 000c4e28; installed rea-agents 6.5.0 evidence.js f992d93e and BinaryLayoutService.js b7c249a7 and cli.js 168cd322; 6.7.0 evidence.js a3fb9f02.
- Located quotes (each at most 25 words): "one address for the five address-taking verbs, default parameters otherwise" (entry line 108); "is inference from the shared projection rule, not a measurement" (entry line 95); "Id values differ between 6.5.0 and 6.7.0 for the same bytes" (README:206).

## Hand-off

- The corrections change no count. After they are applied, rerun command A at the new tip and expect mapped 109 of 109 again.
