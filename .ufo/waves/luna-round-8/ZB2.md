# ZB2 — final disposition list (cutoff 2026-10-16 21:25 -0300)

## CLAIM
Every defect/open item from lane A (52 reports) and lane B (CB1/3/4/6/8, DB1, FB2, HB1/2, KB1, QB2, RB2/4/8, SB1/2/3, TB1, VB1–8, ZB1/3), each disposed fixed-by / adjudicated-as / carried-debt.

## METHOD
Read all reports/receipts; independently reran: MANIFEST check (legs 1–9 OK, leg-10 FAILED); head-59 leg-10 → `c89eea7a…`; leg-3 block 21–22 → `5c6820…`; leg-2-tools → 170 lines, `397531ac…`. No probes.

## FINDINGS
1. leg-3 mismatch — fixed-by repair (18-byte `"listChanged"` drop; now `1be7e4f9…` = claim = /tmp raw; ZB3/RB2/VB2/DB1); mark RE1.md:9 stale, don't edit.
2. leg-10 post-MANIFEST append (VB5/HB1/RB2, independent) — adjudicated-as supersession (head-59 `c89eea7a…`).
3. MANIFEST/CA6 leg-10 hash citations stale — carried-debt: refresh MANIFEST (omits replays/census; CB1).
4. Ten stale verdicts (VB6/ZB1: PS1–3, RE2, RV6, RV8, RV1, CA7, XG1, RE6) — adjudicated-as superseded; PR1 rows stale (DB1).
5. XG1/CA3 forgeability — resolved: VB7 uniform `-32602`; CB3 request = echo = prediction 6/6; legs 4–8 raw absent — carried-debt.
6. CA10 gate — satisfied: CB8 seven criteria PASS (analyze → `-32602`).
7. CA6 zero drift — closed-by TB1/SB2 (78/78; 4/4 sentinels vs round 6); no pre-battery capture — carried-debt.
8. mtime-ordering unsound (RB2/RB4/ZB3) — caveat; hashes unaffected.
9. CA8/PS4 prediction provenance — carried-debt.
10. CA1 offline spoofing — carried-debt.
11. CA4 cache outside /tmp — adjudicated-as no drift.
12. RE1 asserted timeouts — upheld (RB2); minor.
13. RE3 protocol varied — adjudicated-as class-invariant (VB7).
14. XG2 rg-carrier asymmetry — adjudicated-as no impact (VB8).
15. CA9 six-of-37 scope — carried-debt into entry wording.
16. RE5/RE6/K1/KB1 cross-round — closed clean (RB4); no sibling `170` cross-cite.
17. VB1 leg-1 stderr nit — adjudicated-as environmental.
18. leg-9 no 6.4.0 pin — informational.
19. SH1 safety-language bleed — carried-debt, pre-existing.
20. SE1/SB1/SB3 residue/processes — benign (SB3).
21. census-pre.txt stale (`leg-3/4` pre-repair epoch; RB2/RB4/CB3/SB2) — carried-debt: regenerate or annotate; pre-repair bytes unrecoverable.
22. CA5 knowledge entry (78→79) — open: use RB8/QB2 hyphenated slug (79/79 simulated; verify `/tmp/rb8-knowledge-manifest.txt`); CA5's dotted example truncates (mapped 78); keep leg-3 defect out.
23. EX1–10, K1, CA2, CE2, SE2/3, RV2–5/7, RE4, X1, CB1/3, SB2 — no defect, no action.

## THREATS
Lane B may land more seats; cutoff-bounded. Hashes verify consistency, not execution.

## VERDICT
FINDING: all visible items dispositioned; parent-owned remain — MANIFEST leg-10 refresh, census update, knowledge-entry 78→79 decision.
