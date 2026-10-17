# GB1 — G-draft review 2: lane-A drafts vs converged texts

## CLAIM
Element-diff of lane-A drafts (A2, B2, C2, D2–D4, P2) against converged texts (Z1, Z2, Z4) and landing list Z5: no item-1 loss; six draft elements dropped elsewhere. Calls: four drops stand; two restores — C2's operator preconditions, item-4's `:12`/`:217-219` loci.

## METHOD
Read drafts at source (A2:8-10, B2:8-13, C2:8,10, D2:8-12, D3:8-10, D4:8, P2:10-17); convergence (Z1:8-10, Z2:8-10, Z4:8-10, Z5:8-11); drop-predicting reviews (A3:8-10, B3:9-10, H4:8-11, E1:11, R5:11, Q4:8, CB4:8-12). Item-by-item presence diff; no source-truth re-derivation. Guards at HEAD `a280e07133f52f719b0805fc73c0b997e77b5062`: command A (SCORECARD.md:92-123) → 79/79 mapped, 9/9 rules, coverage/depth 10.0/10.0; `git diff --quiet HEAD --` exit 0; PROVINCE blob `8a1cec88…ad47` = HEAD. Read-only; no probes, network, or `/tmp`.

## FINDINGS
1. **Item 1, no drop.** A2's pointer and corrected four-site account both survive in Z1:10 (`:97-108`→`:99-104` refinement only). H4:8/CB4:8 wanted that account trimmed to a pointer; Z1:10/Z5:8 retain it — retained-content call, not a drop.
2. **Item 2, drop stands.** B2:10,12-13's heading and two imperatives are absent from Z2:10's bounded round-history note; ratify (B3:9-10, H4:9, X4). B3:10's "ADJUDICATED not PASS / repair-retest" bound is also absent; it stands only because SCORECARD.md:453-460 keeps both checks as instrument debt — reinstate if landing is read as matcher repair.
3. **Item 3, restore.** Absent from Z5:10 are C2:10's operator preconditions (exact-path attribution-first, retain-ambiguous, manual deletion after close-state review). RESTORE one bounded sentence; DROP C2:8's two-snapshot audit and committed-manifest practice (H4:10).
4. **Item 4, restore.** Z4:10's scope sentence names `:217,236-237`; D4:8 (`:217-219`), E1:11 (`:12`), R5:11, Q4:8 agree; lane-B CB4:11 and VB4 corroborate. RESTORE scope to `:12,:217-219,:236-237`. D3:9's r3 extension: DROP this round (Z5:11) but queue it — F3:10 mentions it with no slot/owner.
5. **P2, no call.** Drafted LOG/SCORECARD elements reappear across Z2/Z5; placeholder hazard is CB4:12's, not a drop.

## THREATS
- No artifact is literally named "G-draft"; the diff is A2/B2/C2/D2–D4/P2 vs Z1–Z5.
- Z4:10's text ("qualifies, does not rewrite") and Z5:11's instruction ("disavowing… label historical") differ in force — reconcile before landing.
- H4:8/CB4:8 cite `Y1.md:8-10` for item-1 duplication, but Y1:8-10 is a PROVINCE check; the trim call rests on Z1 only.
- Untracked wave files still arriving (Z6:8's F3/Z5-absence claim already stale); presence/absence only, no source truth rechecked.

## VERDICT
FINDING: restore C2's operator preconditions and item-4's `:12`/`:217-219` loci; ratify the other four drops; queue item-4's r3 bleed.
