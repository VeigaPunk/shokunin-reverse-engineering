## CLAIM
Item-2 inventory independently verified: the two adjudicated census instrument limits exist as distinct classes and every canonical pointer resolves; the SCORECARD documentation home is adjudicated (X4) but the note is not yet landed at HEAD a280e07.

## METHOD
Read-only at a280e07. Pointers checked: `SCORECARD.md:407-410,442,458-460`; `.ufo/reports/luna-round-4/kaidoku.md:28-46`; `.ufo/waves/luna-round-4/C04.md:34-46`; `.ufo/waves/luna-round-4/receipts/census-pre.txt:29,71`; `.ufo/reports/luna-round-5/kaidoku.md:50-55,63-67`; `.ufo/waves/luna-round-5/X1.md:12,14,16,32-34`; `.ufo/waves/luna-round-5/CB4.md:11`; `LOG.md:744-745,768-770,776-779`; X4, B1–B4, P1, R7. Reproduced CB4's comma one-liner in-memory; re-executed the F18 predicate on git objects at `0772d548`/`6a71cd5`; hex↔decimal via python. No writes beyond this receipt, no probes, no network, `/tmp` untouched.

## FINDINGS
- Comma-token (round-5 SIZES): `X1.md:12` normalizes only the haystack; `X1.md:32` passes raw `29,367,752`/`84,258,816` needles, so no input can pass. Repro: `'29,367,752' in n('x = 29,367,752')` → `False`; `'29367752'` → `True`. Correct content exists (r4u-01 tail at `7125dd4` carries the comma form and the plain recheck). Canonical: `CB4.md:11`; r5 report `:50-55`; `LOG.md:776-779`; `SCORECARD.md:442,458-459`.
- Opener-detector breadth: round-4 F18 row `C04.md:34`; DEBT receipt `:29,:71`; adjudication report `:43-44`. My F18 re-execution at `6a71cd5`: `len(xs)=1`, stale=False, repl=False — the unsatisfiable conjunct is the replacement pair (`v42`,`kimi`), i.e. refuted encoding (`SCORECARD.md:409`'s own "or refuted-encoding" limb). Round-5 manifestation: `X1.md:33-34` rejects normalized `runtime obs extended`; `LOG.md:768-769` records the rename; r5 report `:63-67` names both classes. Two wave-specific predicates, one adjudicated class (`B1.md:8-9`).
- Home/status: `X4.md:2,:17` recommends `SCORECARD.md` and rejects `corpus/QUALITY.md`. No "Known instrument limits" text exists in `SCORECARD.md` at HEAD (grep); `B2.md:10` is a draft only. `P1.md:11` and `R7.md:2` call the home open; both predate X4 (21:46/21:48 vs 21:48:57).

## THREATS
The r4 report's parenthetical "z=1 line-count is structurally unsatisfiable" does not reproduce — count=1; I verified the replacement-token branch instead and did not re-adjudicate it. No census re-run beyond the F18 predicate; command A is not this item; landing remains the parent's integration step.

## VERDICT
CLEAN — both adjudicated instances and their canonical pointers verified; SCORECARD note remains pending integration.
