## CLAIM
GB5 spill-completeness 2: every named-debt item in the rounds 1–8 reports has a status in F3's ledger (`.ufo/waves/luna-round-9/F3.md`)? Mostly yes; six gaps listed.

## METHOD
Read all eight `.ufo/reports/luna-round-{1..8}/kaidoku.md` debt/defect blocks and F3.md; cross-checked claimed closures against `SCORECARD.md` and `LOG.md`. Command A replayed per `SCORECARD.md:92-123` at HEAD `a280e07`: `knowledge_files 79, mapped 79, missing [], dangling [], citation_resolved_rules 9/9, 10.0/10.0` — invariant holds. Only untracked GB5.md written; no tracked file touched.

## FINDINGS
Covered (spot-checked): r1 drift block (r4 drain), r5's seven dispositions, r4-16, C05, F05, instrument debt, r6 litter, B2 hash, AC2/RV5, scout reports, r8 pre-pair/MANIFEST, four short-counts.

Gaps — named in rounds 1–8, no status line in F3:
1. Four untracked `.ufo/interactive-sessions/` files (r1:68-69; `LOG.md:646-647`; r4:66-68) — still untracked in the worktree now (`git status`).
2. Pre-existing unattributable `/tmp/probe*.log` (r3:65-68; r4:66-68) — absent from F3's `/tmp` thread (`F3.md:11`).
3. r14-01/r14-02 own content debt — stale 6.4.0 pins, dead citations, `/tmp` scratch pointers (r1:18-20) — never resurfaces in r2–r8.
4. r8 leg-3 display-hash defect plus `/tmp` pre-repair copy kept "for audit" (r8:42-44) — F3 cites r8:37-38,44-51, skipping it.
5. r6 L9 class-level-evidence/BC5 correction and L10 route deviation (r6:58-63) — F3 names only AC2/RV5 though citing :53-66.
6. r1 C7 SCORECARD `:157` pointer (r1:69-70) — closed via r4 record hygiene (`SCORECARD.md:70-72`), unnamed in F3 (minor).

Uncarried class (adjudicated in-round, no status): seat defects G1, R2/C4, V11a/R09, E4V/S1, Q1–Q6, BB1 (r2:63-64; r3:65-68; r4:65-68; r7:44-52); SHONEN box-4 open question (r5:71-73).

## THREATS
Absence from F3 is not proof of openness: items 1–5 could legitimately be ruled operator hygiene (as r6 litter was, `F3.md:11`), but no such written disposition exists anywhere I checked. Block citations cover round-6 text F3 never names (item 5). I did not inspect `/tmp` (no-probe discipline), so items 2 and 4 liveness is unverified. F3 is a bounded reading ledger, same method as mine.

## VERDICT
FINDING: ledger carries the headline debt; six named items, plus the seat-defect class, have no F3 status.
