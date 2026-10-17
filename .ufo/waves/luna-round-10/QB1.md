## CLAIM
Gate the final luna-round-10 report text clause by clause. That text does not exist yet (`.ufo/reports/luna-round-10/` absent; `PB0.md:22`), so this pre-gates the prospective clause set (R8:8-14 outline; round-9 format; brief findings 1-6) against primary evidence at live HEAD and names what integration must correct before landing it.

## METHOD
Read-only, HEAD `c343939` (brief says `6e83a20`; `c343939` additive +16/+12). Ran: per-records-commit `git diff --numstat`; command A (`SCORECARD.md:92-123`) replayed at `40162fc` and `c343939`; Python parse of the 13 kaidoku rows in fleet `MANIFEST.json` with `sed` spot-checks; heading and verdict scans of the nine reports; sibling `sed` reads only. Sole write: this file.

## FINDINGS
- Reproduced — clauses hold: command A both revisions `{"mapped":79,"knowledge_files":79,"missing":[],"dangling":[],"citation_resolved_rules":9,"rule_blocks":9,"coverage_score":10.0,"depth_score":10.0}`; LOG 0 deletions in all nine records commits; SCORECARD deletions only `a4bd355:4, a9580eb:8, 0772d54:7, cfc84c2:1, 6e2ee8f:1`; PROVINCE sha256 `fe7f3f61…` at `40162fc`+HEAD; 36 axis verdicts = 9 improved/27 unchanged/0 harmed/0 unprovable under the multi-axis-line-per-axis convention (r1-3:3, r4-6:4, r7-9:5; my count command); round 6 = 127 distinct (`luna-round-6/kaidoku.md:47-52`, `BC6.md:15-25`); five short-counts (`r2:57-59; r4:60-62; r5:60-62; r6:47-49; r7:3-4`); SHONEN 4×`[~]` (`SHONEN.md:5,7,9,11`); K1 outbound confirmed sibling-side (tameshi `corpus/knowledge/verification-patterns-fleet.md:35,73,102`; tsukuroi `PROVINCE.md:42,70-71`); D4/D6 race texts (`D4.md:2`; `D6.md:5` exit 2).
- Required corrections: (a) the rewrite disclosure must say five records commits including `a4bd355` (round 1), not 2/3/4/7 — 8 sites/21 deleted lines arc-wide; (b) MANIFEST clause: six enum-led prose rows = historical `:1509` plus luna `:2791,:2805,:2819,:2846,:2860` — 7 fields (`:2846/:2847` one row) — plus three non-enum `verified (…)` rows `:1522,:1535,:1548` (10 values/9 rows); luna-only is five rows/six fields, so "six rows" holds only with `:1509`; (c) pin HEAD `c343939` and record it as a landed change; (d) state the 36-verdict counting convention.
- Owed/unpregatable: the report text itself; round-10 saturation line + window N (`c343939` scaffold; `AXES.md:57-83` — due this round); round-10 LOG/SCORECARD append and fleet MANIFEST row; any admission verdict (records-only round claims no improvement); r5's 126-vs-128 (DB2:12) stays carried, not closed.

## THREATS
Point-in-time: lane B still landing; integration must re-run guards on final bytes. Command A is index arithmetic, not semantic truth. The goal text "appended, never rewritten" is not locatable in-repo (`WB3.md:20`); living-row sanction is operator adjudication. The 36 count depends on the stated convention.

## VERDICT
FINDING: prospective clauses largely evidenced, but the landed text must add r1 to the rewrite class, split MANIFEST counts precisely, pin `c343939`, state the verdict convention, and leave saturation/append/admission open; a literal clause-by-clause gate is owed at integration.
