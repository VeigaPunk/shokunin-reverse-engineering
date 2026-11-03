# Legacy prefile authority and round64 delta

Measured baseline c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 and terminal record
178c7742d6599513c3407ddae791b9dc4291dd55. Reviewed191-line legacy script before
copied-script execution under90s/256MiB; digest and actual outputs retained in
legacy-review-pin.txt and legacy-{base,final}-review.json. Both exits1.

## Still mandatory, not retired

- corpus/QUALITY.md:57, row47: round is filed only when prefile-check exits0
  immediately before report commit; tree clean and **both freeze gates** pass
  --disclosures. Nonzero/skipped/missing output is a failure of this criterion.
- QUALITY:56, row46: disclosed ledger must agree with its gate at filing.
- SKILL.md:1185–1190 still prescribes round24 --disclosures
  corpus/claim-freezes.tsv and appending the round's ledger row.
- SKILL:1386 registers prefile0 only when both freeze gates exit0.
- tools/round-29/prefile-check.sh:5–9 and executable branches explicitly
  require legacy round24 and active round29/v2 legs. Neither is conditional
  on whether the baseline was already red (v2 only conditional on presence).
- Active fleet PROTOCOL.md:412–417: red gate is a routed conformance defect,
  status-neutral unless round rules prescribe failed; this is not a waiver
  of QUALITY47's stricter no-clean-filing criterion.

Scoped search of current QUALITY/SKILL,53–63 lessons and LOG found no retirement
or supersession of this duty. V2's existence alone never superseded both-gates
language. Row100 governs append-only v2 corrections, not legacy retirement.

## Measured delta and bounded repair

At baseline:31 audited,15 clean,20 exact disclosures, missing53–63,stray35.
At data d9a04cd5:32 audited,16 clean,20 exact, missing53–64,stray35.
Thus missing64 was genuinely new avoidable bookkeeping harm, not inherited.
At terminal178c7742:32 audited,16 clean,21 exact, missing53–63,stray35.
Only audited64 CLEAN/empty findings was appended to each ledger. Independent
rerun confirms the new omission is repaired and the residual finding sets
match baseline; no historical row was rewritten. This restores baseline
conformance debt, not prefile cleanliness.

Appending missing53–63 from their actual audited verdicts could reduce missing
rows if separately authorized, but cannot eliminate stray35. Legacy parser
rejects duplicate row keys and any orphan; appending a correction/exemption row
creates another stray and is not a repair. Removing/reinterpreting the old35
row or replacing the gate/rule would alter historical authority and is outside
this frozen domain capability task. Do not do so merely to turn the exit green.

Recommendation: preserve demonstrated reader semantics separately; retain
explicit QUALITY47 conformance/final-filing limitation and route legacy ledger
reconciliation as future authorized work. No baseline-red waiver, no claim of
clean prefile, no silent gate substitution, and no full-round promotion here.
Parent decides truthful closure disposition under the operative contract.
