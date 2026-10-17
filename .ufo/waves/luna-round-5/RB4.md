## CLAIM
Canonical round-5 census picked (X1's skeleton + two CB4-confirmed amendments); T3's invariant checklist covers the four round invariants with three named gaps; X1's SIZES matcher blocks any correct integration unamended.

## METHOD
Read-only. Ran the receipted census verbatim: `REV=HEAD bash .ufo/waves/luna-round-5/receipts/census-pre.sh` → `7/7 DEBT; TOKENSET PASS 72 72; MAP-ROWS PASS; COMMAND_A_UNCHANGED PASS`, exit 1 (matches X1.md:54 and XB1's receipt). Simulated X1's matcher functions (X1.md:12-13, also receipts/census-pre.sh:5-6) on DB2's actual drafted r4u-01 block (DB2.md:21-30). Lane-B siblings cross-read after my own pass: CB4, CB5, RB2, ZB1/ZB2/ZB5/ZB6/ZB7, Y1/Y6, DB2/DB6/DB7.

## FINDINGS
1. **X1 census defect (hard).** On DB2's recommended block: prefix-ok; per-needle `0x1c01dc8` True, `29,367,752` False, `0x505b000` True, `84,258,816` False → SIZES False; C4-style raw-lowercase check True; normalized-needle variant True. Cause: comma-bearing needles against a punctuation-stripping normalizer — unsatisfiable for any correct repair, so a correct integration would still read SIZES DEBT. CB4:11 found it independently (same diagnosis, one-line repro).
2. **Canonical pick: X1 + two amendments.** (a) `h=lambda s,*x:all(n(t) in n(s) for t in x)` — the fix for the defect; (b) edit-set containment per CB4:12/T3:4 — `git diff --name-only BASE WORK` must equal exactly the seven targets (X1 alone lets a stray tracked edit pass). Residual wording-locks (R12-01 `exactly`, R5-02 `283`, README/PIN phrases) are satisfiable by the landed drafts (ZB6:9 dual-gate body; DB6; ZB1; Y1:13; Y6:9) — except R12-01: ZB7:9 shows most item-7 seats recommend no append, and DB7:13 warns "7 values" is not re-derivable; the parent must settle append-vs-no-append before integration. C4's r9-02 literals appear in no draft (ZB5:11), so retaining C4 as a second gate requires re-worked texts.
3. **T3 completeness.** Covers command A (§1), token set (§2), append-only (§3), containment and records (§4-5), `git diff --check`. Gaps: (i) no seat-phase `git status --porcelain`/`git diff HEAD` guard (SB1 ran it; §4's committed-diff check misses uncommitted strays); (ii) §4's "human evidence ledger" is stale — the wave adopted a lexical census; require running it at WORK and freezing output/exit; (iii) README scoping stays human — add MAP-ROWS byte-identity (X1.md:43).

## THREATS
Function-level simulation, not a committed work tree; drafts are pre-integration and may change; CB4's design is a review artifact sharing X1's lexical limits; CB4 landed late in my pass, so my read of it is single-pass.

## VERDICT
FINDING: adopt X1's census with needle-normalization plus edit-set containment (else SIZES false-DEBTs every correct repair); add the three T3 items; CB4's SIZES finding confirmed; settle item-7 append before integration.
