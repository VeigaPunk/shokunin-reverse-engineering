Seat: ExecPrintedRun (executor). Claim: R85-C2 (depth). Target file: tools/round-82/printed-command.py (bytes at 91eeb72f). You own the eight rows below. Another executor (ExecPrintedCmd) edits the same file for other rows. Your new selftest cases must be top-level functions named `r85b_<case>` placed at the END of the file (before any `if __name__` block), and registered by ONE `guarded("<declared name>", …)` line each inside a block you add at the end of `selftest()` marked with the comment `# R85-B cases`. Your candidate is the complete file.

# Rows you own (table: .ufo/waves/round-85/mutants.json; read it, never edit it)
Each mutant applies `find`→`replace` to the pristine target (the anchor occurs exactly once). The declared case must FAIL under the mutant and PASS on pristine. The case must invoke the production function under test (not a re-typed copy of its expression), build its fixture under `$TMPDIR`/--work, and assert the exact outcome (refusal token, verdict, or returned value).
- pc-pin-normprefix → `dot-slash-script-refused`: a command `python3 -I -B ./tools/round-82/conjunction-gate.py …` must be refused with SCRIPT_NOT_PINNED by the production pin check (pristine refuses; the mutant admits).
- pc-run-rc1-strict → `rc1-without-expectation-executable`: a block whose script exits 1 with no expected counter is accepted as executable by production (the mutant turns it into EXECUTION_FAILED). Use the production `run_block` path.
- pc-run-counter-type → `string-counter-refused`: a counter value that is a string (not an integer) must produce the COUNTER_NOT_INTEGER defect on pristine; the mutant accepts it.
- pc-run-counter-mismatch-raw → `int-counter-equals-string-expectation`: an integer counter 13 against the expectation string "13" is accepted by production (string comparison of str(value)); the mutant compares raw values and refuses. Assert pristine accepts.
- pc-run-defects-static-dropped → `static-defect-ledger-copied`: a command with a static defect must have that defect present in the aggregated `defects` ledger returned by production (the mutant empties it; the early return still fires). Assert the ledger, not only `static_defects`.
- pc-token-metachar-drop-pipe → `pipe-metachar-refused`: a command containing `|` must be a static defect on pristine (the mutant drops `|` from METACHARS).
- pc-token-ellipsis-drop-ascii → `ascii-ellipsis-refused`: a placeholder written with ASCII `...` must be refused on pristine (the mutant drops the ASCII form).
- pc-token-allowlist-widened → `unbound-plan-variable-refused`: a command using `$PLAN` (not in the production allowlist) must produce VARIABLE_UNBOUND on pristine; the mutant admits PLAN.

# Measure
Build a sandbox clone (see the shared rules), write your candidate into the clone at tools/round-82/printed-command.py, commit it there (sandbox only), then run the frozen counter from the sandbox:
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-84/mutation-closure.py --root "$D" --rev <sandbox commit> --mutants /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/mutants.json --work "$S/c2" --json-out <wave dir>/after-printed-run.json
Report the status of YOUR eight rows and the pristine selftest rc and case names. Also confirm the pre-existing cases of printed-command.py still pass pristine.

# Deliverables (wave dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/w1/ExecPrintedRun/)
- `candidate/tools/round-82/printed-command.py` (full file); `candidate.diff` (unified diff vs 91eeb72f bytes);
- `selftest-pristine.txt`, `selftest-candidate.txt`; `per-row.md` (table: id, declared case, status, failing case names under the mutant, pristine outcome);
- any change you made to pre-existing cases (should be none), with reasons;
- `DONE` marker last.
