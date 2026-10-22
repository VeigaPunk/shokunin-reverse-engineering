# Harm sweep, round 27, wave 2 (seat HarmSweep)

Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0. Freeze a4f674b343d8564e21f7eb8984630a95089c82d6. Tip main = HEAD = 4084d8975b684a8837b1c858eea0008ce9ab49e0 (rev-parse, exit 0, 15:36:21Z). Commits in base..main: a4f674b3, 9dca26df, c6d619a3, 97358f75, 4084d897.

Scope: committed blobs and history only; working tree not read. Lane writes: this report only. No REA calls, no subagents. Tools: none installed or updated (git and Python 3 standard library only). Reproducible run: `python3 -I -B harm_sweep.py` in the scratch directory, run 2026-10-22T15:44:44Z, exit 0.

## Verdicts

| Attack item | Verdict |
|---|---|
| Every deletion, net base to main | holds: none |
| Every deletion, commit by commit | holds: one line removed and rewritten in-round (F3) |
| Owned-axes rows in SCORECARD | holds: unchanged, byte-identical |
| Append-only: SKILL, QUALITY, README, SOURCES, PROVINCE | holds: nothing removed or altered |
| No knowledge entry lost bytes | holds: 110 of 110 base blobs identical |
| Verdict honesty in README and PROVINCE | fails (F1) |

## Findings by severity

F1 MEDIUM, fails: README and PROVINCE state 16 verdicts with no 15-of-16 caveat. corpus/README.md:76 labels R27-C1 "held narrowly". corpus/README.md:209 and PROVINCE.md:314 say "10 of 16 content-keyed, 6 rename-sensitive, 0 unstable". The arithmetic matches table.tsv, but the sixth rename-sensitive row is the one the frozen counter refuses. Receipt `.ufo/waves/round-27/after/c1-at-97358f75.txt` line 13: "INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run". Line 18: "rows_complete=15/16 entry_ok=1". Line 19: "exit=1". Over the 15 complete rows the split is 10 content-keyed and 5 rename-sensitive. Script CHECK5 at main: README "10 of 16" x2, "15 of 16" x0, "INCOMPLETE" x0; PROVINCE "10 of 16" x1, "15 of 16" x0. The miss is disclosed in SCORECARD.md:3090, LOG.md:2972, knowledge entry lines 88-92 and lesson M27-2. The entry's result table (lines 25-34) gives the refused row a plain verdict with no mark. For the L1 to decide: restate README:76, README:209 and PROVINCE:314 as 15 of 16 complete, name the refused row, and do not call R27-C1 held.

F2 LOW, holds for the counted claim, ledger gap: tools/round-27/assemble-c1.py was added in 9dca26df, after the freeze. Its docstring (lines 2-6) says it writes table.tsv and that the pinned counter checks its verdicts again. claims.json pins only the two counters, and the round-24 freeze gate takes instrument paths from the frozen claim text only, so it cannot see this script. Ledger row CF15 (corpus/claim-freezes.tsv line 15) does not list it.

F3 INFO, holds: 97358f75 removed one line of corpus/README.md (the first "Round 27 update" bullet, added by c6d619a3) and wrote three lines in its place. After case folding the first new line equals the removed one (CHECK1 "equal after case fold: True"). The only change is "against" to "Against". No base content lost.

F4 INFO, holds: CF15 flags reconcile to paths. Gate logic at `.ufo/waves/round-24/tools/freeze-gate.py` lines 100-113, with `git log freeze..main` per path (CHECK5). tools/round-27/xpin-attribute.mjs is absent at the freeze and touched only by 97358f75, giving INSTRUMENT_ABSENT and INSTRUMENT_REVISED. tools/round-26/recompute-ids.py is named in the claim rules and unpinned, giving INSTRUMENT_UNPINNED. Its sha256 is 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b (`git cat-file blob main:tools/round-26/recompute-ids.py | sha256sum`, exit 0, 15:45:27Z), matching the CF15 text. The row names the paths but not the flag words. I did not run the gate.

## Checks (command; excerpt; exit; UTC; verdict)

C1 Net deletions. `git diff --no-renames --numstat cd32264f main`, also --name-status, --summary and -U0 removed-line count. Excerpt: "114 files; insertions 6790; rows with deleted count not 0: []"; "{'A': 106, 'M': 8}"; "create-mode lines: 106 delete-mode or mode-change lines: []"; "removed lines, base to main: 0". Exit 0. UTC 15:36:28Z (first run), 15:44:44Z (script). Verdict: holds. Full list of deletions: none. Modified files, additions only: LOG.md, PROVINCE.md, SCORECARD.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md, corpus/claim-freezes.tsv. No file deleted, renamed or mode-changed.

C2 Deletions per commit. `git rev-list --reverse --parents cd32264f..main`, then `git diff --no-renames -U0 <parent> <commit>` for each. Excerpt: removed lines 0 for a4f674b3, 9dca26df, c6d619a3, 4084d897; 1 for 97358f75 (corpus/README.md). Exit 0. UTC 15:44:44Z. Verdict: holds (F3).

C3 Append-only. `git cat-file blob <rev>:<file>` for base and main, then byte-prefix and line-order tests (script CHECK2). All base lines kept in order in every file. Byte prefix holds for SKILL.md (108012 to 110015 bytes; one insertion at end of file, 26 lines), PROVINCE.md (33782 to 35552; end, 21 lines), LOG.md (end, 11 lines) and claim-freezes.tsv (end, 1 line). Byte prefix does not hold for corpus/QUALITY.md (27505 to 32439; rows 38-40 after row 37), corpus/README.md (55458 to 58669; table rows after lines 75 and 166, sub-bullets after 206), corpus/SOURCES.md (87123 to 92518; S081 and S082 after S080, bullets after 150) or SCORECARD.md (34 added lines: one capability row after 622, a 33-line round-27 section at end). Exit 0. UTC 15:44:44Z. Verdict: holds. No base line altered. SKILL.md and PROVINCE.md are pure end-of-file appends; the other three named files take interior rows.

C4 Knowledge bytes. `git ls-tree -r <rev> -- corpus/knowledge` for base and main, blob ids compared. Excerpt: "base 110 blobs (109 .md and .gitkeep); main 111 (110 .md and .gitkeep); identical 110; changed []; missing []; new: corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md". Every .md slug appears in README (interactive substring check, before 15:42Z; only .gitkeep lacks one). Exit 0. UTC 15:44:44Z. Verdict: holds. SCORECARD:3099 "110/110 knowledge files mapped" matches the count.

C5 Owned-axes rows. Compare SCORECARD base and main, lines 1-622 and rows 21-25. Excerpt: "lines 1-622 identical in main: True"; rows 23-25 identical: coverage "9.72 to 10.0", depth "10 to 10", calibration "0 to 10". Exit 0. UTC 15:44:44Z. Verdict: holds, unchanged. None improved, none claimed. The round-27 section line "Owned axes rows above are unchanged this round" matches.

C6 Freeze integrity. Blob compare at a4f674b3 and main for claims.json and both counters, plus `git diff --name-status` since freeze. Excerpt: "identical freeze vs main: True" for all three (sha256 ff45e9ce, e0a07995, d8de667f); since freeze: "A tools/round-27/assemble-c1.py; A tools/round-27/xpin-attribute.mjs". Sha256 values equal the pins in claims.json (interactive check, before 15:42Z). Exit 0. UTC 15:44:44Z. Verdict: holds.

C7 Verdict honesty. Text counts, table and receipt reads (script CHECK5). Excerpt: see F1. Exit 0 for the reads; the receipt itself records exit=1. UTC 15:44:44Z. Verdict: fails (F1).

C8 Table shape of inserted rows. Pipe and tab counts against each header (script CHECK6). Excerpt: SCORECARD:623 5 to 5; QUALITY:48-50 5 to 5; README:76 4 to 4; README:168 5 to 5; SOURCES:87-88 12 to 12; claim-freezes row 15 has 3 tabs, same as header. Exit 0. UTC 15:44:44Z. Verdict: holds.

## Residual risk and gaps
- Counters not re-run. F1 rests on the committed receipt, table and text.
- Working tree not read; uncommitted edits would not appear here.
- Freeze gate not run; F4 comes from its code and git log.
- The meaning of the "held narrowly" label was not checked against a written rubric; F1 rests on the frozen target (16 of 16), not on the label.
- Owned-axis rows elsewhere (PROVINCE scores, other capability tables) were not compared.

## Artifacts (sha256; scratch /fast/scratch/hyaku/kaidoku-r27/seats/w2/HarmSweep/)
- harm_sweep.py f42553cc9c77b51bfe31d5c92ef9e69546f0b409d9dcd96613494d9b7caa8b2f
- harm-sweep-output.txt e45f1bb264a188928db5ab4a8d20a339f1949d908968a4f803b963306f4e1521
- numstat.txt 803791305eb5b7a116d4121c00352975e7158b5a7028056ddcf583358ba1c51f
- name-status.txt 94f75a9cfd4b82706514306e1f4f087762e30609275fb5bcb0b2bddef5d90e4a
- diff-U0.patch 96968362463626efd6e61e8b83df17524144fc171d622a7936354189dbbd4204
- diff-full.patch f046d6a22795ddb10176ea848c5e641aecd54a0c8f0eda363a99e1205b748a0d
- knowledge-base-manifest.txt c89cd9f5627a0d6ebb90a33ce852e0b522bac1178048a7c201ee1330135f6b4f
- readme-c6d6-to-97358-U0.patch c9da7efa4af7c3d982c73792c9aa23925c08923175fd715f2a28b077097d6219
- readme-97358-to-4084-U0.patch e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
