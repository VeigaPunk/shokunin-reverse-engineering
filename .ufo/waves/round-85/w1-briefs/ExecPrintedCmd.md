Seat: ExecPrintedCmd (executor). Claim: R85-C2 (depth). Target file: tools/round-82/printed-command.py (bytes at 91eeb72f). You own the seven rows below. Another executor (ExecPrintedRun) edits the same file for other rows. Your new selftest cases must be top-level functions named `r85a_<case>` placed at the END of the file (before any `if __name__` block), and registered by ONE `guarded("<declared name>", …)` line each inside a block you add at the end of `selftest()` marked with the comment `# R85-A cases`. Your candidate is the complete file.

# Rows you own (table: .ufo/waves/round-85/mutants.json; read it, never edit it)
Each mutant applies `find`→`replace` to the pristine target (the anchor occurs exactly once). The declared case must FAIL under the mutant and PASS on pristine. The case must invoke the production function under test (not a re-typed copy of its expression), build its fixture under `$TMPDIR`/--work, and assert the exact outcome.
- pc-row-last → `duplicate-row-first-binds`: a ledger with two rows for one id; the FIRST row must bind (assert the returned row is the first).
- pc-row-prefix → `id-prefix-not-bound`: a ledger with a row `S2999` listed BEFORE a row `S299`; a query for `S299` must return the `S299` row.
- pc-cells-len-ge → `row-width-thirteen-exact`: a 14-cell row for the id must be refused by the production row check.
- pc-cells-index-shift → `fully-mined-row-green`: a fully valid 13-cell mined row must produce the accepted/green outcome; under the mutant the status is read from the wrong column and it goes red.
- pc-entry-any-line → `entry-second-source-line-ignored`: an entry whose FIRST `source:` line does not cite the id and whose SECOND `source:` line does must NOT be attributed (production uses the first line only).
- pc-cells-status-ne-queued → `sourced-row-rejected-status`: this case name already exists (`guarded("sourced-row-rejected-status", …)`) and currently PASSES under the mutant. Make it assert that a row whose status is `rejected` keeps the sourced arm RED through the production `sourced_arm`, and confirm it fails under the mutant. If the existing fixture is the wrong shape, change the fixture and state the change; do not weaken its assertion.
- pc-cells-date-ge → `sourced-row-later-date`: a mined 13-cell row whose date cell is LATER than 2026-11-04 (use 2026-11-05) must be refused by production; the mutant's `>=` accepts it.

# Measure
Build a sandbox clone (see the shared rules), write your candidate into the clone at tools/round-82/printed-command.py, commit it there (sandbox only), then run the frozen counter from the sandbox:
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-84/mutation-closure.py --root "$D" --rev <sandbox commit> --mutants /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/mutants.json --work "$S/c2" --json-out <wave dir>/after-printed-cmd.json
Report the status of YOUR seven rows and the pristine selftest rc and case names. Also confirm the pre-existing cases still pass pristine.

# Deliverables (wave dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/w1/ExecPrintedCmd/)
- `candidate/tools/round-82/printed-command.py` (full file); `candidate.diff` (unified diff vs 91eeb72f bytes);
- `selftest-pristine.txt`, `selftest-candidate.txt`; `per-row.md` (table: id, declared case, status, failing case names under the mutant, pristine outcome);
- any change you made to pre-existing cases, with reasons;
- `DONE` marker last.
