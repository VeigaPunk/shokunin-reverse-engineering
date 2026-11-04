# MutationR87 notes (round 87, R87-C1, mutation-tester)

Axes: coverage (which defects the selftest and counter detect), depth (why the survivors survive), calibration (whether a pass means what the claim says).

## Method
- `mutate.py` (this dir) read the production repair and counter, asserted their pins
  (repair f4ebd152…c49723, counter 0f2d2bd8…5384b0), and wrote 22 repair mutants and 14 counter
  mutants into scratch `/fast/scratch/hyaku/kaidoku-r87/MutationR87/m/`. Every mutant is one
  string substitution whose anchor occurs exactly once in the source. Production files were only read.
- Repair mutants: ran each mutant's `--selftest`, then the pristine counter with `--repair-cmd <mutant> --no-rea`.
- Counter mutants: ran each mutant's `--selftest`, then the mutant counter three times: with the
  committed repair (`--no-rea`), with `identity` (REA on), and with `naive-global` (`--no-rea`).
- Baselines used the pristine counter. The committed repair scored 8/8 on the non-REA arms with all
  controls ok. identity scored 0/8 with met=false and N1 false, matching the committed
  pre/c1-control-identity-at-base.json. naive-global passed the non-REA arms on 4/8, matching the
  committed 4/8. Both selftests passed. Since every baseline held, every verdict counts as a result.
  No verdict is inconclusive.
- `tabulate.py` turned raw-results.json into mutation.json and mutation.md. Per-run counter receipts
  are in receipts/. They contain scratch paths, which are not evidence.
- Restoration: the production sha256 values match before and after the run, and so do the pristine
  scratch copies (mutation.json `restoration`). The scratch dir was deleted before the DONE marker
  was written.
- Tools installed: none.

## Results
- Repair: 10 killed, 12 survived. Counter: 8 killed, 6 survived. No counter mutant turned the
  do-nothing control green.
- See mutation.md for the table and ../MutationR87.md for the findings.
