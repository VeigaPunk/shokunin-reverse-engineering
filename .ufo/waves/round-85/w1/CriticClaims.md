# CriticClaims (round 85, seat CriticClaims) — scoped findings

Full verdicts, commands, and receipts: `.ufo/waves/round-85/w1/CriticClaims/attack.md` (receipts and control generator in the same directory).

## Key numbers
- C2 do-nothing (base rerun at 91eeb72f): killed 3/21, ok false. Matches the BASE receipt.
- C2 always-pass control (literal "guarded" cases): killed 3/21. Cannot reach the target.
- C2 tripwire control (fingerprint per target, no behavioural assertion): killed 21/21, ok true, pristine green on all three targets. The target "≥16 of 21" is reachable without semantics. FALSIFIED as a depth measure.
- C2 removed-cases control (existing selftest bodies disabled, tripwire kept): killed 21/21, ok true. The frozen counter does not measure removal of existing cases. Frozen-13 arm on the same rev: 2/13, ok false.
- C2 table pin: no round-85 container at 91eeb72f; table_identity matches None. The kill rule's pin is not enforced.
- C1 do-nothing (r84 gate at 91eeb72f): F1 CLEAN, F2 CLEAN, R84 CLEAN; refused 0/2. HOLDS.
- C1 cheapest rule: a path-in-predicate grep plus a negation grep (`none` excluded) gives F1 PB_NO_PREDICATE_PATH, F2 PB_PREDICATE_NEGATED, R84 CLEAN. That meets the target without checking blob or pin. FALSIFIED as a measure of the declared predicate.
- C1 label/predicate identity: the predicate has clauses (a) blob, (b) pin, (c) negation; the target names labels only for (c). The negation list is not in the declaration (`tools/round-85/predicate-bind.py` absent at 91eeb72f). `none` is used as a count value in the positive controls. FALSIFIED.

## Receipts (this directory)
- `base-mutation-closure.rerun.json`, `ctlA-mutation-closure.json`, `ctlB-mutation-closure.json`, `ctlC-mutation-closure.json`, `ctlC-frozen13.json`, `r84-gate-rerun.json`
- `controls/` (mkctl.py, ctlA/ctlB/ctlC diffs against 91eeb72f, sandbox commit SHAs `fe3a64cc`, `57ebd936`, `e906955b`)
- `cheap-rule/` (F1/F2/R84 blobs, cheap-rule.sh, cheap-rule.out.txt)

## Harm check
- Frozen-13 (`.ufo/waves/round-84/mutants.json`) declared names must remain present and failing. They are the only regression detector for removed cases. Named list in attack.md V4.1.
- Informational: `ExecSourceBind` candidate diff removes no case. `ExecPredBind` and `ExecSourceBind` DONE markers present at check time; `ExecPrintedCmd` not yet. No candidate changes any verdict above.

## Blockers and installs
- Blockers: none. The round-85 container and the C1 counter source are absent at the declaration rev, so C1's counter and container-wide scope could only be tested by the candidate and the control scans above.
- Installs: none.
