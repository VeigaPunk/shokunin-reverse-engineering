# C2 observation-envelope and log-path review

**Axes:** C1 calibration (tied-lowest) and C2 depth. This is a read-only C2 review of the round-20 comparator/extractor and the retained exact-artifact records; no production files were edited and no checks were run.

## Finding — missing strict observation-envelope validation

**Baseline defect:** `.ufo/waves/round-20/tools/compare-first-failure.py:72-78` unwraps an extractor result only when it is a dictionary containing both `first_failure` and `last_line`. Otherwise it passes the entire JSON value to `validate_failure`. Since `validate_failure(None)` returns successfully (`:12-15`), a bare JSON `null` is accepted as an observation; with a predicted null, `same_failure` reports a match (`:28-34`) and the comparator returns exit 0 (`:81-99`). This treats an unbounded absence as bounded observed silence, contrary to frozen C2 case `naked_null` (expected exit 2). A bare valid failure object can likewise be compared without an observation envelope (`:75-78`), contrary to `naked_failure`.

The envelope’s required keys are checked only for presence, not value validity. For example, `{"first_failure":null,"last_line":false}` or a negative/string `last_line` is unwrapped to null and can match a null prediction; `last_line` is never type- or range-checked. Those are frozen C2 cases `boolean_last_line`, `negative_last_line`, and `string_last_line` (each expected exit 2). For nested failures, `validate_failure` uses `value.get("index")` without requiring the member (`:20-23`); a missing index can pass validation. `same_failure` later indexes it directly (`:34`), while `evaluate_paths` catches only `OSError` and `ValueError` (`:88-94`), so a non-null comparison can escape as an uncaught `KeyError` rather than the contract’s exit 2. The frozen `missing_index` case requires distinguishing absent from explicit null. Required `kind` and typed `phase` are checked (`:18-25`); `va` is type-checked when present but is not required by this frozen case set.

These are manifestations of one missing envelope/shape-validation defect, not separate target counts. The frozen contract is `.ufo/waves/round-21/fixture-contract.json` (`naked_null`, `naked_failure`, `missing_last_line`, `negative_last_line`, `boolean_last_line`, `string_last_line`, `missing_index`; expected exit 2 for each). Other declared shape checks should remain intact: null index is valid when the member exists, and equality intentionally ignores phase/VA while matching non-null observations by kind/index.

### Proposed independently specified fixture pair (not executed)

Use a temporary existing empty log, prediction `{"first_failure":{"h1":null}}`, and a deterministic stub extractor. Positive stdout is a valid envelope with `first_failure:null`, `last_line:0`, and the log’s absolute path; expected comparator exit 0 (bounded silence). Negative stdout is bare JSON `null` for the same requested log; expected exit 2 with an unevaluable/missing-envelope finding, not a clean match. This pair preserves the positive while exposing the false-accept path above. The expected decisions are from the frozen contract; the current-baseline result is source-derived and was not run.

## Log-path semantics

The ordinary paired flow is coherent: `compare-first-failure.py:53-61` checks the supplied log path and passes that same argument to the extractor; `first-failure-extract.py:137-140` opens it, and `:189-196` reports `os.path.abspath(log_path)`. The subprocess inherits the caller’s working directory, so a relative path is resolved consistently by both processes. No ordinary-flow path mismatch is demonstrated here.

The comparator does not consume or compare the returned `log_path` field (`compare-first-failure.py:72-78`) and does not itself bind the result to a log digest. That is a provenance limitation if the comparator is expected to validate arbitrary extractor output, but `log_path` identity is not one of the frozen C2 cases; do not count it as an additional frozen-contract defect. R20’s retained `runs/t1246-go/comparison-log-binding.json:2-5` separately records the absolute log path, SHA-256 and `verified:true`; the retained `evidence/compare-rerun/summary.txt:1-19` reports all nineteen artifact comparisons as exit 0 with matching observations and log hashes. These retained results do not demonstrate the malformed-envelope defect occurred in those nineteen runs.

## Review limits and parent checks

No LSP device/server was exposed: the initial `xd://lsp` lookup returned “No such tool” and enumerated mounted devices without LSP. Accordingly, no LSP status, references, definition, or diagnostics were available; no grep-based semantic claims were used. Review was limited to the cited source ranges, frozen fixture contract, round-20 lesson, and retained comparator/path-binding records. No tests, builds, linters, or smoke checks were run.

Parent should run the frozen C2 battery against the completed lane/revision (`python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C2`) and the planned changed-path smoke/final suite once after integration; specifically ensure the required malformed-envelope and missing-index cases return exit 2 while the three bounded valid positive/mismatch cases retain their declared exits.

Report: .ufo/waves/round-21/w1/C2EnvelopeFields.md
