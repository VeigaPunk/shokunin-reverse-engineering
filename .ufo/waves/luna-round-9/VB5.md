# VB5 — cross-verifier, items 1–4 (lane A × lane B)

## CLAIM
Cross-verify lane A (A1–A4, B1–B4, C1–C4, D1–D4) against lane B (VB1–VB4); list divergences; re-check load-bearing citations and round invariants.

## METHOD
Read-only at HEAD `a280e07`: all 20 seat reports; spot-checked every load-bearing citation (r4-16, r12-01, PROVINCE `:100-116`, SCORECARD, round-4/5 reports, X1/C04/CB4, SKILL `:38-40`, QUALITY `:7-25`, l7-01/l8-01 `:5`, verify-recovery.py `:120-123`, lessons `:145-155`, X4, P1, R7); counted `verify:` bullets (468); ran command A. No probes/network; no tracked writes.

## FINDINGS
1. Item 1: A1's "errata explicitly supersede" the r4-16 account is overbroad — r12-01 `:112-114` supersedes only its own loci (`:13,:38,:40,:42,:67`); A3/A4's narrow form holds; VB1 confirms staleness (material supersession). VB1 pins the append to EOF (last section r14-01 `:875`); A2's draft left location unstated; A3's "no line shift" holds only at EOF.
2. Item 2 cause: B1 cites round-4's "z=1 structurally unsatisfiable"; VB2's re-execution found count=1, not reproducing that branch — the unsatisfiable conjunct is the replacement pair (`v42`/`Kimi`) = refuted-encoding limb (SCORECARD `:409`). B2's draft wording "structurally impossible" inherits the wrong cause; B3's evidence-first guard is supported.
3. Item 2 home: B1/B4 defer placement to X4 as open; X4 `:2,:17` already recommends SCORECARD and rejects `corpus/QUALITY.md`. B2's SCORECARD target matches X4; P1 `:11`/R7 `:2` predate X4.
4. Item 3 scope: C1's no-live-dependency result covers instructions/gates/rechecks; VB3 quantifies its excluded set — 468 historical `verify:` bullets use round-era `/tmp`, superseded by tracked receipts (LOG `:798`; SCORECARD `:497`); L7-01's `/tmp` npm cache is the sole soft, untested candidate.
5. Peer availability: A3, C2 `:5`, C3, D3 report peer-artifact absence ("No matches", "only A1.md and R4.md") that contradicts the live tree — those files existed; absence-dependent conclusions are snapshot artifacts; C4 already reconciled C1/C2.
6. Item 4 scope: D2 (`:217,:236-237`) ⊂ D4 (`:217-219`) ⊂ VB4 (`:12,:219`, plus r3 `:60,:136` and stale SCORECARD `:79`/lessons `:149-153` pointers). VB4 endorses scoping (D2/D4) while confirming D3's r3 gap; D3's no-retained-"benign" remedy remains an open policy call.

## THREATS
Textual/static only; no `/tmp` inspection, census rerun, or live probe (round constraint). VB2's F18 nuance rests on its own git-object re-run (`0772d548`/`6a71cd5`), not mine. Seat-level absence claims are unreliable (finding 5).

## VERDICT
FINDING: six divergences (items 1 supersession scope/append location; 2 F18 cause + home status; 3 excluded-recipe count; 4 benign scope/r3 coverage; peer-availability artifacts); command A 79/79 + 9/9; PROVINCE untouched.
