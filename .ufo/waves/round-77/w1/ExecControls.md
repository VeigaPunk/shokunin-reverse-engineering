# ExecControls-8 — round-77 do-nothing controls scored against the frozen targets

Seat ExecControls-8, wave r77-w1, measured revision (base) `188562d43e3cc58b217ad7aa763fb296c5b8a0b7`.
Lane instruments verified byte-identical to the freeze pins before any run (sha256 vs `.ufo/waves/round-77/claims.json`): `verdict-bind.py` 45280392… ✓, `prefile-receipt.py` 174eedb5… ✓, `gen-controls.py` 001fccd6… ✓, `prefile-check.sh` 9a403dc1… ✓, `record-audit.py` 805a8ba5… ✓. Worktree HEAD is the freeze `6767a879`, 12 in-flight dirty paths of other seats; every command used the freeze-pinned tools. All scratch lived under `/fast/scratch/hyaku/kaidoku-r77/ExecControls-8/` (deleted on exit); evidence first copied under `.ufo/waves/round-77/w1/ExecControls-8/`.

## Receipt

```json
{
 "schema": "kaidoku-r77-execcontrols-w1-v1",
 "seat": "ExecControls-8",
 "rev_measured": "188562d43e3cc58b217ad7aa763fb296c5b8a0b7",
 "c1_controls": [
  {"control": "no-binding", "exit": 1, "mismatch_count": 4, "bound_clauses": 21,
   "meets_target": false, "actual_mutation_applied": false},
  {"control": "all-false", "exit": 1, "mismatch_count": 4, "bound_clauses": 21,
   "meets_target": false, "actual_mutation_applied": false}
 ],
 "pointer_only": {"argv": "python3 -I -B tools/round-76/record-audit.py --root . --rev 188562d4 --json-out pointer-only-at-base.json",
  "exit": 0, "mismatch_count": 0, "mismatches": [], "D24_capability_rows": true,
  "atoms": 9, "validate_defects": 0, "ok": true,
  "false_annotation": "standing — the receipt named by the annotation records exit 1, mismatch_count 1, D24_capability_rows false"},
 "c2_gate_alone": {"argv": "bash <shared-clone at 188562d4>/tools/round-29/prefile-check.sh <clone>",
  "prefile_line": "prefile: PASS", "exit": 0,
  "files_written_by_run": 0, "tree_dirty_after_run": 0,
  "battery_at_base": {"arms_ok": 4, "arms_total": 6, "exit": 1, "ok": false, "validate_defects": 0},
  "record_receipt_arm": {"met": false,
   "observed": ".ufo/waves/round-77/l1/scores/prefile-at-filing.json absent at 188562d43e3cc58b217ad7aa763fb296c5b8a0b7"},
  "gate_exits_arm": {"met": false,
   "observed": "round-76: 5 gate receipts without exit (gate-at-freeze, gate-at-record, gate-at-tip, gate-disclosures, gate-selftest-at-tip)"}
 },
 "forged_arms_defects": ["arms_ok disagrees with the arm rows", "ok disagrees with arms_ok/arms_total"],
 "targets_reachable_by_control": false
}
```

## C1 — controls regenerated and scored (target: exit 0, `mismatch_count 0`, `bound_clauses >= 18`)

`python3 -I -B tools/round-77/gen-controls.py --root . --base 188562d43e3cc58b217ad7aa763fb296c5b8a0b7 --out-dir <scratch>/controls --json-out controls-at-base.json` → exit 0, `{"controls_do_not_meet_target": true, "no_binding": 1, "all_false": 1}`. Generator receipt `ExecControls-8/controls-at-base.json` records per control `meets_target` false.

| control | exit | mismatch_count | bound_clauses | meets_target |
|---|---|---|---|---|
| no-binding | 1 | 4 | 21 | false |
| all-false | 1 | 4 | 21 | false |

**Defect found (reported, not fixed — lane files are L1-owned): both control patches are dead code.** `verdict-bind.py` ends with `if __name__ == "__main__": sys.exit(main())` at lines 629–630; `gen-controls.py` appends the override after it (AST: `FunctionDef parse_clause line 634` after `If __main__ line 629`), so `sys.exit(main())` unwinds before the override binds. Proof (`ExecControls-8/ast-deadcode.txt`): the full receipt of the no-binding control at base is **byte-identical to the real instrument's base receipt** (diff over `jq -S 'del(.instrument)'` → identical; evidence copy `ExecControls-8/real-at-base.json` vs `ctrl-no-binding.json`), and all-false is identical too — each reports the real base 4 mismatches (D24 + mismatch_count twice: the `capability-row binding` row and PROVINCE.md line 585). Had `parse_clause→None` applied, `bound_clauses` would be 0 (not 21); had `bind→False` applied, `mismatch_count` would be 21 (not 4). The generator's "every mutation actually applied" check only greps for the marker text after the words "control mutation" — it cannot see a dead patch, the exact silently-missed-patch failure its docstring claims to guard. The controls-as-run are the unmutated instrument, so they trivially fail the target, but they also cannot certify that the target requires the claimed work; and if the mutations HAD applied, the designed outcomes (bind nothing → 0 binds < 18 floor; fail everything → mismatch 21 ≠ 0) also fail the target — so the no-control-reaches-target conclusion holds under every reading.

**Pointer-only control (round 76's `record-audit.py --rev 188562d4`)**: exit 0, `mismatch_count 0`, mismatches `[]`, `D24_capability_rows` true over 9 atoms, `validate.defects []` (`ExecControls-8/pointer-only-at-base.json`). This is the pointer-only weakness the round-76 §6.5 routed defect named: the audit is green while the annotation it covers is false — PROVINCE.md line 585 (the `capability-row binding` bullet at base) names `.ufo/waves/round-76/l1/scores/c1-at-landing.json` as `(D24 true, mismatch_count 0)`, and that receipt at base records `rev 821d9eb6…, exit 1, mismatch_count 1, D24_capability_rows false` (read from the base fixture). A pointer-only control cannot reach the frozen C1 target because it never re-derives any verdict.

**One line (C1):** No — no do-nothing control reaches the frozen target: the derived controls score exit 1 with `mismatch_count 4` / `bound_clauses 21` / `meets_target` false, but they are byte-appended dead patches that merely re-run the real instrument at base; the pointer-only audit is green by construction (mismatch_count 0, D24 true) precisely because it never reads the verdict written beside a resolving path.

## C2 — gate alone at base and the forgery (target: exit 0, `arms_ok 6 of 6`, `ok true`)

Clean shared clone at base (fixture `mktemp -d` under scratch; toplevel asserted == fixture; HEAD asserted == `188562d4`): `bash <clone>/tools/round-29/prefile-check.sh <clone>` → `prefile: tree clean` / `prefile: ledger1 retired (erratum r68-1) …` / `prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at 188562d… exit=0` / **`prefile: PASS`, exit 0** (full capture `ExecControls-8/prefile-at-base.txt`). After the run the fixture tree stayed clean (`git status --porcelain | wc -l` = 0) and `.ufo/waves/round-77/` does not exist at base — **the gate run retained no receipt of its own**.

Battery at base (`--root . --rev 188562d4 --work <scratch>/battery --battery --json-out c2-at-base-mine.json`): exit 1, `arms_ok 4 of 6`, `ok false`, `validate.defects []`. The `record-receipt` arm: `met false`, observed `.ufo/waves/round-77/l1/scores/prefile-at-filing.json absent at 188562d4`. The `gate-exits` arm: `met false`, observed five round-76 gate receipts without exit (gate-at-freeze, gate-at-record, gate-at-tip, gate-disclosures, gate-selftest-at-tip) — note the frozen prose says "three round-76 gate receipts without exit"; the measured arm names five. The operative predicate number `arms_ok 4` matches the freeze; only the prose count is loose (see Findings F2).

Forgery: copied `.ufo/waves/round-77/pre/c2-at-base.json` to scratch, set `arms_ok 4 → 6` while `record-receipt.met` stayed `false` (and `gate-exits.met false`), then `python3 -I -B tools/round-77/prefile-receipt.py --validate-battery <forged>` → exit 1, defects pasted:

```
"arms_ok disagrees with the arm rows"
"ok disagrees with arms_ok/arms_total"
```

(`ExecControls-8/forged-battery.json`, validate capture `forged-battery.validate.json`.) An arms_ok inflation cannot survive the battery's own internal validator, which re-counts the arm rows.

**One line (C2):** No — running the prefile gate alone at base yields `prefile: PASS` at exit 0 but retains no receipt, so the battery stays at `arms_ok 4 of 6` with the `record-receipt` arm unmet; faking `arms_ok 6` while an arm row says `met false` is refused by `--validate-battery` with the two defects above.

## Findings

- **F1 (C1, material):** round-77's two derived controls are dead-code no-ops — the mutation text is appended after the `__main__` guard and never binds, so each control is the unmutated instrument (byte-identical base receipts). `gen-controls.py`'s apply-check greps text only and reports the controls as correctly derived (`controls_do_not_meet_target: true` came out true for the wrong reason). Route for repair: place the override before the guard (or exec the derived file after rebinding), and assert behavioral divergence (e.g., diff a probe run) instead of marker presence. Until repaired, C1's control arm carries no independent evidence that the target needs the claimed work — the analytical designed-outcomes (0 binds < 18; 21 mismatches ≠ 0) still back that conclusion, and the controls-as-run still fail the target.
- **F2 (C2, minor):** frozen `before` prose says "three round-76 gate receipts without exit"; the measured `gate-exits` arm names five. The predicate's `arms_ok 4` matches; the prose count should say five or name the set.
- **F3 (context, verified not hypothetical):** the pointer-only audit reproduces the round-76 §6.5 defect class end to end — green (mismatch_count 0, D24 true) at the base while the receipt named in the evidence cell records `exit 1, mismatch_count 1, D24 false`.

## Evidence files (under `.ufo/waves/round-77/w1/ExecControls-8/`)

`controls-at-base.json` (generator receipt incl. per-control `meets_target`), `ctrl-no-binding.json`, `ctrl-all-false.json`, `real-at-base.json` (identity diff anchor), `pointer-only-at-base.json`, `c2-at-base-mine.json` (battery at base), `prefile-at-base.txt`, `forged-battery.json` + `forged-battery.validate.json`, `verdict-bind-no-binding.py` / `verdict-bind-all-false.py` (derived dead-patch copies), `ast-deadcode.txt`. Scratch `/fast/scratch/hyaku/kaidoku-r77/ExecControls-8/` deleted after the copies. No lane file, fleet file, or `.ufo/state` was written; only this report and the seat evidence dir. No tools installed; no git writes anywhere (fixture clone only, deleted with scratch).
