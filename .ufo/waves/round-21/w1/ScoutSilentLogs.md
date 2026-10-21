# Silent-log shape — bounded observation only

## Axes and scope

- **C1 calibration:** out of this slice; no C1 evidence was evaluated.
- **C2 depth:** one retained R20 silent-log example and the R21 frozen observation-envelope contract, read-only.
- No source/registry rows were changed; no tests, REA/provider/carrier execution, or external URLs were used. This is advisory research, not a fresh run or a global-success judgment.

## Findings

**Observed retained shape (one example).** The retained extraction record `.ufo/waves/round-20/evidence/extract/t1246-asm.json:1-8` has `first_failure: null`, `first_failure_line: null`, `cause_line: null`, `last_line: 227`, and `other_errors: []`; its log is the relative path `runs/t1246-asm/logs/rea-ghidra-15p1Vy/ghidra.log` (record line 6). The retained comparator summary has `t1246-asm exit=0 logsha_ok=y [null,null]` at `.ufo/waves/round-20/evidence/compare-rerun/summary.txt:2`. This is one retained null/null first-failure comparison with a matching log-hash indicator—not an assertion that the analyzer, process, or overall task succeeded.

**The source explicitly bounds absence.** In `.ufo/waves/round-20/tools/first-failure-extract.py:2-11`, the extractor says: **“not that analysis succeeded beyond it.”** (6 words; lines 7-8). `parse_log` computes `last_line`, searches for the recognized Go-analysis failure records, and returns the nullable first-failure plus line bound and separately collected `other_errors` (`:134-195`). `main` prints that envelope for the requested log (`:296-312`). Thus this null means no qualifying Go-analysis failure was found through the reported final line; it does not certify global success.

**Historical comparator gap relevant to C2.** `.ufo/waves/round-20/tools/compare-first-failure.py:28-34` treats two nulls as equal. `run_extractor` unwraps an envelope only if both `first_failure` and `last_line` exist, but otherwise sends the decoded JSON value directly to `validate_failure` (`:50-78`); `validate_failure(None)` returns successfully (`:12-25`). Therefore, by static inspection, the old comparator does not itself require a bound for a naked null (nor a failure object); it can compare an unbounded null as silence. `evaluate_paths` maps comparator match/mismatch/unevaluable to exits 0/1/2 (`:81-99`), so the retained `exit=0` is a comparison result, not a process-success signal.

**Frozen R21 C2 contract.** `.ufo/waves/round-21/fixture-contract.json:19-39` makes the intended distinction testable: `bounded_silent_positive` requires prediction null plus an envelope with `first_failure: null` and integer `last_line` (exit 0); `naked_null`, `naked_failure`, missing `first_failure`, missing/negative/bool/string `last_line`, and failed extraction are unevaluable (exit 2). The contract also retains separate typed mismatch controls. Its `:41-43` states C2 remains separate from the C1 successor and the 19 R20 pairs remain retrospective regression, not new predictions. `claims.json:9` names the same C2 objective and requires preservation of those nineteen exact-artifact matches.

## Evidence limits / confidence

- **High confidence** in the reported record fields, summary row, frozen case expectations, and the static R20 source behavior; these are exact retained files/lines.
- This slice covers only `t1246-asm`; it does not independently validate the log digest, rerun extraction/comparison, establish the other 18 results, or infer overall analyzer success.
- The lsp device was unavailable (`read xd://lsp` returned “No such tool”); definition/caller lookup used literal grep plus focused source reads, not semantic LSP proof. No outside source was consulted, so there are no external URLs or access dates.

## Parent checks (not run here)

Run the frozen C2 battery on the settled lane/revision: `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C2`. Confirm its existing 20 frozen C2 cases remain intact, then run the parent-owned changed-path smoke and final suite once. No verification was performed for this report.