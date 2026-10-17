## CLAIM
Re-audit luna-round-3 (MANIFEST round 7; work `638fb211` + records `0772d54`); independently characterize the W3-flagged SCORECARD rewrite in `0772d54`.

## METHOD
Read-only Git objects. difflib opcodes for `0772d54^→0772d54` and every records commit; byte prefix tests; command A reproduced via `.ufo/waves/luna-round-5/receipts/census-pre.sh`'s algorithm (untracked file); literal `f(content, path, params)` census; MANIFEST round-7 row read.

## FINDINGS
`0772d54` changes SCORECARD in exactly three blocks (322→370 lines):
1. replace line 24 (1:1), living depth row — old `9/9 existing queue-drain rule blocks … measured revisions in evidence/round-1-2026-10-15/result.json … r1 measurement; no depth change` → new `… at 638fb211 … baseline a79945c4, measured 638fb211 … + luna-round-3`.
2. replace old 61-66 → new 61-67 (6→7), open-gaps bullet — `- **Authority contradiction:** … These two summaries remain unresolved, not silently fixed.` deleted for `closed by luna-round-3 …`.
3. insert new 324-370 (47 lines) — pure tail append `## luna-round-3`.

Bytes 20916→23810, prefix-identical **False**; LOG 47099→49294, **True**. Blocks 1-2 undisclosed: report grep `depth row|open gap|Authority contradiction` = 0 hits; LOG and MANIFEST cover only work-commit edits.

Arc context: r1 `a4bd355` did the same (living coverage row line 23; Coverage-map bullet 53-55) and *disclosed* it — `the coverage row's README range pointer was updated 11-58 → 11-60 as this row's own evidence-field hygiene` (`SCORECARD.md:267-269`). Records commits r2/r3/r4/r7 rewrite living rows (prefix False); r5/r6/r8/r9 and `c343939` are pure appends (True).

Substance reproduces: command A equality `638fb211` = `638fb211^` — `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9}`. Formula hits SKILL 1→0, README 1→0, QUALITY 1 (row 14 kept, row 15 supersedes it). 64/64 unique seat files; MANIFEST row 7 verdicts exact enums; both commits lane-identity ancestors.

## THREATS
The rewritten depth row froze: still `measured 638fb211` while command A runs 79-file 10.0 at HEAD. Command A's definition lives only in an untracked wave file; C4's census command was never persisted. Whether living-row edits breach the append-only criterion (`P0.md:5,8`) or are sanctioned-if-disclosed practice (r1; Last-change-round column) is an operator call.

## VERDICT
FINDING: `0772d54` edited two living SCORECARD regions in place (depth row; authority-contradiction gap) with zero disclosure, and lane A's r2/3/4/7 rewrite list misses round 1 (`a4bd355`) — the first instance, which did disclose.
