## CLAIM
Ledger review (DB6): DB4 (`.ufo/waves/luna-round-10/DB4.md`, final merged ledger, mtime 22:49:15 — postdates D6 22:32:20, D4 22:33:09, so it saw all inputs) vs every round report's named-debt section. DB4's numerics replicate exactly; its merge drops 13 carried no-closure items present in its inputs.

## METHOD
Read D1–D6, DB1–DB5, and all nine report debt sections (r1:55-70, r2:55-68, r3:55-68, r4:48-68, r5:11-39,58-67, r6:45-67, r7:42-56, r8:37-51, r9:13-24,46-56). Reproduced read-only: `git show --numstat` on the nine records commits — SCORECARD deletions r1 `a4bd355` 4, r2 `a9580eb` 8, r3 `0772d54` 7, r4 `cfc84c2` 1, r7 `6e2ee8f` 1, LOG 0/9; `ls .ufo/waves/luna-round-{4..9}/*.md | wc -l` → `64/126/127/127/100/121`; MANIFEST JSON scan. Omission probe: `grep -c -E 'no-peeking|S2 |interactive-sessions|r14|G9|misnamed|C4 |V11a|RV5|L10|L9 |cold-cache|L7-01' DB4.md` → `0`. No probes, network, or non-seat writes.

## FINDINGS
- DB4's claims replicate: rewrite census 5/9 rounds (LOG clean); r6 127/128 (BC6); rosters exact; MANIFEST = briefed six rows, 7 enum+prose values {1,8,9,10,12×2,13} + 3 non-enum rows {2,3,4}; B2 `dc740c46…`; `PROTOCOL.md:447` (fleet root) LOG-only; SCORECARD.md:68-72 row self-labels content debt. Read-only sibling checks: Tameshi `verification-patterns-fleet.md:35,:102` unresolved U4; tsukuroi ADJ-06 `PROVINCE.md:42,70-71` confirmed. On disk: `R2-reviewer-readme.md` (r3) still misnamed; r4 `V11a.md` absent (0 matches).
- 13 report-named no-closure items absent from DB4 (each present in D1–D3/DB1–DB2/DB5): R4 no-peeking (r1:66-67); S2 pointer-style (r1:67-68); four untracked `.ufo/interactive-sessions` files (r1:68-69; still `??` in git status); r14-01/02 content caveats (r1:18-20); G9 E-draft dates (r2:65-66); misnamed R2 report (r3:65); C4 unpersisted census (r3:66-68); `/tmp/probe*.log` (r3:68; N3's regex misses bare names); V11a misnaming (r4:65); RV5 manifest L1-only (r6:53-54); L9 class-level (r6:60-63); L10 route deviation (r6:58-60); L7-01 cold-cache (r9:20-24).

## THREATS
Keyword-level probe; DB4 was also read in full and none found, but differently-worded coverage could hide an item. In-wave-closed items were deliberately not counted. Rosters are point-in-time; DB4 predates this review. All 13 drops are record/hygiene-class, not corpus-content debt.

## VERDICT
FINDING: DB4 replicates the arc numerics and carries all major classes, but its merge drops 13 carried minor items — re-union D1–D6/DB1–DB5 (or append them) before treating DB4 as the closeout ledger.
