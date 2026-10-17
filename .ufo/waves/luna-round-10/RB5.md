## CLAIM
Review X4's round-10 closeout draft (R8 outline + F1/F2 text) against every seat it cites and the live records; decide whether it is complete enough to serve as the arc's final report.

## METHOD
Static, read-only: read cited seats (R8, F1/F2, C1/C3/C4, Y1-Y3, N2, A1, W2-W4/W7/W9, S4/S5, D1-D4, K1, R6) plus later arrivals D5/D6; re-ran Command A (`SCORECARD.md:92-123`) at `6e83a20`, `40162fc`, `c343939`; byte-prefix plus `git diff --numstat` on LOG/SCORECARD at the r2/r3/r4/r7 records commits; resolve/ancestry/identity check of all 19 refs; read `MANIFEST.json:2747-2866`, `SHONEN.md`, the nine report Verdicts blocks; sibling files read read-only. No network, no live probes, no sibling writes.

## FINDINGS
1. Measurements reproduce. My runs: Command A 79/79, 9/9, 10.0/10.0 at `6e83a20`, `40162fc`, and true HEAD `c343939` (one commit above the brief's premise; +28 LOG/SCORECARD lines, zero deletions). 19/19 refs resolve, are ancestors, exact lane identity. Direct count: 36 axis verdicts = 9 improved/27 unchanged/0 harmed/0 unprovable (r1-r3: 3 each; r4-r6: 4; r7-r9: 5). Six prose MANIFEST values in five rows (`:2791`, `:2805`, `:2819`, `:2846-2847`, `:2860`). Census 896/895, r6=127, r9's 121 files non-roster, SHONEN four `[~]` — all hold.
2. Not carried: R8.md:10's required disclosure of non-append-only SCORECARD rewrites in rounds 2/3/4/7. Reproduced: prefix(SCORECARD)=False at `a9580eb`/`0772d54`/`cfc84c2`/`6e2ee8f` (deletions 8/7/1/1); prefix(LOG)=True throughout. The draft leaves "append-only" as an unexplained verdict word.
3. Not carried: K1.md:2's two sibling-facing items. Verified sibling-side: tameshi `corpus/knowledge/verification-patterns-fleet.md:35,73,102` (stale formula; kaidoku `SCORECARD.md:353-357` shows it superseded); tsukuroi `PROVINCE.md:42,70-71` + `adjacency-handoffs-fleet-r1.md:54` + workspace `.ufo/l0-questions.md:42` (ADJ-06 arbitration). X4's debt list and SHONEN section omit both.
4. Minor: "Landed changes" cites `R6.md:8-15` (inherited from R8) — that seat reviews the round-6 report and states no round-10 scope; the scope text is at `P0.md:8`, `P1.md:10`, `W10.md:13`.

## THREATS
Static checks only; no REA execution. I reviewed X4's draft, not a later integrated report; integration lands on `c343939`, which the draft predates. D5/D6 postdate D1-D4.

## VERDICT
FINDING: all measurements reproduce, but the draft omits the rounds 2/3/4/7 SCORECARD-rewrite disclosure R8.md:10 requires and drops K1's two sibling-facing outbound items; incomplete until added.
