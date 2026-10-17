## CLAIM
P1's seat envelope conforms to the required section contract, but its FINDINGS instantiates none of the four round-report slots the P1 seat has carried since r1 — Work performed, Landed changes, Before → after measurements, Findings & named debt — so the round's acceptance invariant (Command A 79/79 + 9/9) has no scaffold slot.

## METHOD
Read-only. `nl -ba .ufo/waves/luna-round-9/P1.md` (24 lines, 312 words); heading census `for r in 1 2 3 4 5 6 7 8; do grep -n '^#' .ufo/reports/luna-round-$r/kaidoku.md; done`; read P1s r1–r5, r7; `grep -n '79\|command A\|9/9\|invariant' .ufo/waves/luna-round-9/P1.md` → no match (exit 1). No probes, network, or edits other than this file.

## FINDINGS
1. Envelope conforms: `## CLAIM` :1, `## METHOD` :4, `## FINDINGS` :7, `## THREATS` :20, `## VERDICT` :23; VERDICT is one line (:24); SHONEN nests under FINDINGS (:17-18; precedent r3 P1:12, r4 P1:34, r5 P1:23, r7 P1:21).
2. Four-section precedent: r1 P1:8,19,30,34; r2 P1:10,12,14; r3 P1:8 "Use this four-section round-report skeleton:"; r4 P1:8-12; r5 P1:8-11; r7 P1:8-21. Round-9 P1 has no such slots — FINDINGS is an item-keyed table (:8-13) plus debt ledger (:15); no "Work performed"/"Landed changes"/"Before → after" text exists in the file.
3. Material gap: every r1–r8 final report opens with those four headings (e.g. `.ufo/reports/luna-round-8/kaidoku.md:6,20,30,40`); the round invariant 79/79 + 9/9 (baseline `E2.md:5,8`; recipe `SCORECARD.md:93-123`) appears nowhere in P1 (grep exit 1). Integration must re-derive the scaffold from precedent.
4. Minor: P1's four table rows match the round's four queue items 1:1 and preserve no-deletion (:12) and PROVINCE-untouched (:13).

## THREATS
The round-9 brief is not on disk, so "the four-section contract" is reconstructed from in-repo precedent (P1 slots plus all eight report heading sets); if the brief re-scoped P1 to dispositions only, the deviation is authorized — unverifiable here. Content dispositions, command A, and P1's citations were not re-audited (shape scope only). Read as "the four queue items", P1 passes; no repo text supports that reading.

## VERDICT
FINDING: envelope and item coverage hold, but P1 drops the four-section scaffold every prior P1 carried; restore the slots — especially Before → after for 79/79 + 9/9 — at integration.
