# Mutant-kill binding: a kill is an observed outcome change, not a matching name

source: S304 — https://doi.org/10.1016/bs.adcom.2018.03.015 (Papadakis, Kintis, Zhang, Jia, Le Traon, Harman, "Mutation Testing Advances: An Analysis and Survey", Advances in Computers vol. 112 (2019), pp. 275–378). Full text read 2026-11-04 from the ORBilu author postprint archived 2019-04-29 at https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf (HTTP 200).
verified-at: 2026-11-04 (round 85, lane commit to be filled at landing)
recheck: 180d

Wave-relative paths below are under `.ufo/waves/round-85/w1/ScribeSource/`.

## Claim

A mutant counts as killed only when a named detector's outcome changes under the mutant and does not change on pristine. The survey defines the kill the same way: "When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'" (Section 2 "Background", author postprint PDF p. 6; 24 words). Killing is an observed difference between the mutant's run and the original's run — the outcome of the test run — and not the presence of a test whose name happens to match.

## What the frozen counter measures

The frozen round-84 instrument `tools/round-84/mutation-closure.py` binds that definition to a declared case name. For each row of the frozen 21-row table `.ufo/waves/round-85/mutants.json` (sha256 `ef031dbe3525ff8454b1b120ed18f88a8918c981c7a4726ab626430e72e1ec41`) it applies that row's declared single-behaviour edit to a scratch copy of the target tool's bytes at the measured revision, runs the tool's own `--selftest`, and scores the mutant `killed` only when **the row's declared case appears in the mutant run's failing-case list and the same case is present in the pristine run's inventory, with pristine green**. The instrument names the rule at the scoring site (QUALITY 138: "a mutant is killed by a detector present in the target's own output"; the operative comment reads "an absent declared case is a survivor, never a pass", and the code scores it `survived`, reason `declared-case-absent-from-selftest`). Receipt fields: `killed`, `survivors`, `inconclusive`, `pristine_failed`, `table_identity`, and `results[]` (each with `status`, `declared_case`, `declared_case_present`, `failures`).

Counting command (the frozen one, run verbatim):

```
python3 -I -B tools/round-84/mutation-closure.py --root . --rev <rev> \
  --mutants .ufo/waves/round-85/mutants.json --work <scratch> --json-out <receipt>
```

Measured at the round-85 declaration revision `91eeb72f` with that command:

- 21 rows, killed 3, survivors 18, inconclusive 0, pristine_failed [] (`receipts/base-mutation-closure-at-declaration.json`; counts equal the committed BASE receipt `.ufo/waves/round-85/pre/c2/base-mutation-closure.json`). The three killed ids are `sb-window-13th`, `sb-two-fields-first`, `cg-floor-le`.
- Pristine green for all three targets at the same revision: `tools/round-82/conjunction-gate.py` (21 cases, exit 0), `tools/round-82/printed-command.py` (22 cases, exit 0), `tools/round-83/source-bind.py` (exit 0, plain `selftest <case>: FAIL` shape).
- Regression arm, same counter and revision, frozen r84 table `.ufo/waves/round-84/mutants.json` (13 rows): killed 13, survivors 0, inconclusive 0, pristine_failed [], `ok true`, exit 0 (`receipts/base-frozen13-regression-at-declaration.json`).

## Limit

A kill binds a case **name**. The counter proves that the named case changed outcome under the mutant and was present and green on pristine; it does not certify that the case's assertion is semantically the right assertion for that defect. A fabricated case that asserts the declared failure would also score. Semantic certification of each case's assertion is not claimed here (routed r84 R6, carried forward).

## Falsification

One observation would refute this entry: a mutant row whose declared case is absent from the pristine inventory, or whose declared case does not appear in the mutant run's failing-case list, being scored `killed` by `tools/round-84/mutation-closure.py`. Equivalently, a receipt in which `results[].status == "killed"` while `declared_case_present` is false, or in which the declared case is missing from `results[].failures`. The instrument's own selftest asserts the opposite for the `declared-case-absent` fixture row (`survived`, reason `declared-case-absent-from-selftest`).

## Receipts

- `receipts/base-mutation-closure-at-declaration.json`, `receipts/base-frozen13-regression-at-declaration.json`
- `source-snapshot.txt` (sha256 `3452916192a447db89545cf9cdb4c0c7bfbd7f162b67482fb7582691e6bd7bee`) and `source-snapshot.sha256`
- `.ufo/waves/round-85/pre/c2/base-mutation-closure.json`, `.ufo/waves/round-85/pre/c2/base-frozen13-regression.json` (BASE receipts, committed at `c7e2e8e`)
- `plans/round-85-claims.md` — the frozen C2 predicate, counting command and kill rule this entry restates.
