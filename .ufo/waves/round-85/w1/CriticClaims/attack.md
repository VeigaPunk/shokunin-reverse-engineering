# CriticClaims attack — round 85 (lane kaidoku-shokunin, declaration 91eeb72f, BASE c7e2e8e1)

Scope: the frozen plan and its controls. Candidates were not waited on. The lane tree was not written; all control builds ran in a sandbox clone under scratch (`clone.kqv0`, detached at 91eeb72f). Sandbox commits (not pushed, not in the lane): ctlA `fe3a64cc`, ctlB `57ebd936`, ctlC `e906955b`. Receipts and the control generator are in this directory.

Commands used (all read-only against the lane; writes only to scratch and this dir):
- `git -C <lane> show 91eeb72f:plans/round-85-claims.md`, `… show 91eeb72f:.ufo/waves/round-85/mutants.json`, `… show c7e2e8e1:.ufo/waves/round-85/pre/c2/base-mutation-closure.json`
- `python3 -I -B tools/round-84/mutation-closure.py --root <clone> --rev 91eeb72f… --mutants .ufo/waves/round-85/mutants.json --work <scratch> --json-out <receipt>` (base rerun; ctlA/B/C at their sandbox commits)
- `python3 -I -B tools/round-84/mutation-closure.py … --mutants .ufo/waves/round-84/mutants.json` (frozen-13 arm, on ctlC)
- `python3 -I -B tools/round-84/freeze-precheck.py --root <clone> --rev 91eeb72f… --container … --expect … --control instruments-only --json-out …` (r84 gate, F1/F2/R84)

## R85-C1 (calibration)

V1.1 Predicate / kill rule / label identity — FALSIFIED.
- The predicate has three operative clauses: "(a) a blob at $REV, (b) pinned … at its blob digest, (c) not negated" (plan, R85-C1 Predicate).
- The labels named in the target are only `PB_NO_PREDICATE_PATH` and `PB_PREDICATE_NEGATED`. The kill rule's "a counter path in the predicate that is not a blob or not pinned at its digest" has no label, and no fixture produces a blob or pin finding. The three clauses do not map one-to-one to labels.
- The negation list is "frozen in the counter's source". `git show 91eeb72f:tools/round-85/predicate-bind.py` → `fatal: path … does not exist`. The operative token list is not frozen at declaration.
- "`none` as a predicate qualifier" is ambiguous. R84-C1 reads "with mismatches none"; R84-C2 reads "survivors none, inconclusive none, pristine_failed none" (`cheap-rule/cheap-rule.out.txt`, second block). A list that includes `none` flags the positive control R84-C2 and R84-C1.

V1.2 Do-nothing control reaches the target — HOLDS.
- Rerun of the frozen r84 gate at 91eeb72f: F1 CLEAN, F2 CLEAN, R84 CLEAN, `refused_expected 0`, `met false`, mismatches `[F1:CLEAN, F2:CLEAN]`. Receipt `r84-gate-rerun.json`; matches `pre/c1/base-freeze-precheck.json`.
- F1 is what it appears to be. `check_container` runs `SCRIPT_RE` over `"\n".join(strings(claim))`, i.e. every string in the claim object, including `kill_rule`. The path `tools/round-84/freeze-precheck.py` in `kill_rule` therefore satisfies `CLAIM_NO_COUNTER_PATH`. The pinned digest `4aae3f26…` equals the blob digest, so no pin finding either. F1 is refused only by a predicate-level check.

V1.3 Cheapest rule that meets the target — FALSIFIED (target does not test clauses (a) and (b)).
- Two grep tests over each container's `predicate` string (`cheap-rule/cheap-rule.sh`): path-in-predicate, and negation token (`not|no|never|without|neither|nor|cannot`, `none` excluded) → F1 `PB_NO_PREDICATE_PATH`, F2 `PB_PREDICATE_NEGATED`, R84 `CLEAN`. That is exactly the target: `refused_expected 2`, `accepted_expected 1`, exact findings. The `instruments-only` control accepts F1 and F2 as the target requires.
- Neither forgery exercises (a) or (b): both carry a pin equal to the blob digest. A rule with no blob check and no pin check meets the target. The target does not require the counter to implement the predicate it declares.
- Effect on value: as frozen, the claim measures a naming-and-negation regex. The predicate and kill rule state more than the fixtures can detect. Including `none` in the token list fails the target (V1.1).
- Candidate `ExecPredBind` implements (a), (b), and sentence-scoped negation with `none` excluded. That is candidate code, not the frozen target, so this verdict does not change.

V1.4 "for every container" — FALSIFIED (universal without an enumerating command).
- The plan's counter invocation takes `--container <json>` explicitly. Nothing enumerates the containers.
- At 91eeb72f there are 68 `claims*.json` files under `.ufo/waves/round-*` (`git ls-tree -r --name-only 91eeb72f | grep -E '(^|/)claims[^/]*\.json$'`). "Every container" is therefore scoped to whatever is listed on the command line.

## R85-C2 (depth)

V2.1 Target is measured by a field the counter does not pass — FALSIFIED (wording).
- Target: "killed ≥ 16 of 21".
- The counter's `ok` and exit code require `len(killed) == total` and no survivors (`score()`: `ok = not survivors and not inconclusive and … and len(killed) == total`). A run at 16 will report `ok false` and exit 1. The target therefore reads the `killed` field only, and the plan does not say so.

V2.2 Do-nothing control — HOLDS.
- Base rerun at 91eeb72f: `killed 3 / 21`, `ok false`, `pristine_failed []`, instrument sha `e5cfd2ed…`. Matches `pre/c2/base-mutation-closure.json` (killed 3; survivors 18; the one `declared_case_present: true` survivor is `pc-cells-status-ne-queued`).

V2.3 Cheapest cheat that reaches the target — FALSIFIED (the target can be met with no semantic check).
- Control A (literal reading of the cheapest cheat: one always-passing `guarded`-style case per declared name, no assertion). Receipt `ctlA-mutation-closure.json`: `killed 3 / 21`. Always-passing cases cannot kill; this control does not reach the target.
- Control B (tripwire). Each target gets one selftest-appended block, registered via `atexit` under `--selftest`. It emits the target's declared case names, and marks them failed when the file minus the appended block no longer hashes to the pristine digest. It asserts nothing about behaviour. Receipt `ctlB-mutation-closure.json`: `killed 21 / 21`, `ok true`, `pristine_failed []`, all three targets green. Sandbox commit `57ebd936`; diff `controls/ctlB.diff`; generator `controls/mkctl.py` (mode `B`).
- Consequence: the counter binds a declared case *name* to "fails under the mutant", and any byte change satisfies that. The declared limit ("a fabricated case that asserts the declared failure would also score") understates the leak. The target "killed ≥16" is reachable by a tripwire. The target is wrong as a measure of depth.
- Build note: the first tripwire build was appended after the `if __name__ == "__main__"` guard and never registered (3/21), and it used `__file__` inside `atexit` (NameError at shutdown). Both were corrected before the numbers above. The reported numbers are from the fixed commits.

V2.4 Table pin — FALSIFIED (the kill rule's pin is not enforced).
- Kill rule: "a table edited after the declaration (its sha256 is pinned in the container's `fixtures`)". No round-85 container exists at 91eeb72f (`ls-tree .ufo/waves/round-85` lists `mutants.json` and `pre/` only), and the frozen command passes no `--claims`.
- Base receipt: `table_identity {"claims": null, "expected": null, "matches": null}`; `table_ok` is True when `matches` is None. A changed or dropped row would still score ok.
- Contrast: `ctlC-frozen13.json` has `table_identity.matches true`, claims `.ufo/waves/round-84/claims.json`. The round-84 table is pinned; the round-85 table is not.

V2.5 Removal of existing cases is not measured — FALSIFIED against the kill rule as written.
- Kill rule: "a removed or weakened existing case in the three targets".
- Control C (`ctlC-mutation-closure.json`, sandbox commit `e906955b`, `controls/ctlC.diff`): ctlB plus every existing selftest body in the three targets disabled (each `selftest` returns before running a case), tripwire re-pinned to the edited body. Result: `killed 21 / 21`, `ok true`, all three pristine green. Every existing case is gone and the frozen command reports success.
- The only removal detector is the frozen-13 arm: the same rev scores `killed 2 / 13`, `ok false` (`ctlC-frozen13.json`). It catches removal only for the 13 r84 declared names. Removal of any case that neither table names is invisible: the counter has no base-inventory comparison.

V2.6 "all three targets" pristine green — HOLDS.
- The counter's pristine loop is over the table's distinct targets, which are exactly `printed-command.py`, `source-bind.py`, `conjunction-gate.py` (21 rows: 15 / 4 / 2). Green on the lane and on all three controls.

## Harm check (item 4)

V4.1 Frozen-13 names the planned edits must keep present and failing (`.ufo/waves/round-84/mutants.json`, same three targets; base 13/13, `ok true`):
floor-refused, failures-refused, binder-refused, bare-name-refused, runtime-pin-mismatch-refused, static-defect-no-execution, sourced-row-rejected-status, sourced-row-wrong-date, sourced-row-at-base, sourced-plan-missing, sourced-entry-uncited, late-single-header, duplicate-target-second.
- A rename or removal of any of these breaks frozen-13. That is the only regression detector for removed cases (V2.5).
- Overlap: `pc-cells-status-ne-queued` (r85) declares `sourced-row-rejected-status`, which is also r84's `source-mined`. It survives at base because its case does not fail under the mutant. A strengthened case is an improvement; a renamed case breaks frozen-13.
- Candidate `ExecSourceBind/candidate.diff` (informational): one `for` header replaced by a concatenation with two new `r85c_*` case functions; no case removed. Those cases are semantic fixtures, not tripwires.

## Step 5 (optional, one check, no sleep loop)
- DONE present: `ExecPredBind`, `ExecSourceBind`. `ExecPrintedCmd` has no DONE at check time.
- V1.1 and V1.3 unchanged: `ExecPredBind`'s rule meets clauses (a)–(c), but the frozen target is still reachable by the grep in V1.3. Its negation list and `none` exclusion are defined in its own docstring, after the declaration. That is a candidate-side definition, not a frozen one.
- V2.3 unchanged: the tripwire control does not depend on any candidate. `ExecSourceBind`'s after-receipt (rev `f341d0e0`) reports `killed 6 / 21` with `printed-command` not yet landed, so it is not a basis for any verdict here.

## Verdict summary
| # | Item | Verdict |
|---|---|---|
| V1.1 | C1 predicate/kill-rule/label identity | FALSIFIED |
| V1.2 | C1 do-nothing (r84 gate) | HOLDS (0/2) |
| V1.3 | C1 cheapest grep meets target | FALSIFIED (target does not test (a),(b)) |
| V1.4 | C1 "every container" | FALSIFIED (no enumerator) |
| V2.1 | C2 "≥16" vs counter `ok` | FALSIFIED (wording) |
| V2.2 | C2 do-nothing (base) | HOLDS (3/21) |
| V2.3 | C2 cheapest cheat (tripwire) | FALSIFIED (21/21, ok true) |
| V2.4 | C2 table pin enforced | FALSIFIED (no container; matches None) |
| V2.5 | C2 removed-case clause | FALSIFIED (ctlC 21/21 with all existing cases removed) |
| V2.6 | C2 "all three" pristine green | HOLDS |
| V4.1 | Harm: frozen-13 names | HOLDS as a regression arm (13 names listed) |

Installs: none. No pacman, no packages installed or upgraded.
