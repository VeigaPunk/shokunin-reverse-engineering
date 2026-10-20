# CompareEofFields — round-18 w1 report (compare.py extra_expectations)

## Files changed

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/compare.py` (in place, additive only)

## Behavior added (contract.md bullet `compare.py`, contract.md:126-127)

Three new `extra_expectations` keys evaluated mechanically in `compare()`:

- `analyzer_errors_empty: bool` — match iff `len(observation.get("analyzer_errors") or []) == 0`
  equals the predicted bool (`isinstance(pred, bool)` guard included); an absent observed list counts
  as empty, mirroring the `analyzer_errors_contain` pattern at compare.py:192-196.
- `eof_reads: [[a, b]...]` — match iff `observation.get("eof_reads")` equals the predicted list
  exactly (order-sensitive). Raw fetch, no `or []` normalization: a stale observation lacking the
  field mismatches even a predicted `[]` (INFERENCE: this strictness follows `invalid_version_strings`
  precedent at compare.py:182-186 and makes r17-era extracts visibly red instead of silently green;
  selftest encodes it).
- `invalid_index_reads: [int...]` — L1 follow-up: exact list equality against raw
  `observation.get("invalid_index_reads")`; absent field mismatches, same as `eof_reads`.

New code at compare.py:197-216, immediately after the `analyzer_errors_contain` block. Eight selftest
cases appended at compare.py:405-448, including red cases: `analyzer_errors_empty: true` vs non-empty
observed errors (exit 1), `eof_reads` order swap `[[1,2],[3,4]]` vs `[[3,4],[1,2]]` (exit 1),
predicted `eof_reads: []` vs observation without the field (exit 1), and predicted
`invalid_index_reads: [3,7]` vs observation without the field (exit 1). Green cases cover `true`+empty,
`false`+non-empty, exact `[[17645861, 111938854]]` equality (the aether EOF pair, contract.md:107), and
`invalid_index_reads: [3,7]` on both sides (exit 0).

## Commands run and exits (observation)

1. `ls` runs dirs / `grep` run-carriers.sh, carrier-run.py — orientation, all exit 0.
2. `python3 -I -B tools/compare.py --selftest` → last line `SELFTEST: CLEAN cases=23`, `EXIT=0`
   (was cases=15 before the change; +8 new cases, all pass).
3. Re-ran compare on every retained r17 pair (stdout to mktemp dir, retained files untouched):

   `for label in <8 labels>: python3 -I -B tools/compare.py --prediction predictions/$label.prediction.json --observation runs/$label/observation.json > $tmp/$label.compare.json`

   Result per label — `old_exit` = retained `runs/<label>/compare.exit`, `new_exit` = this run:

   ```
   calib-esbuild-0.25.12 old_exit=0 new_exit=0 stdout_same_as_retained=yes
   calib-shfmt          old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-aether           old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-containerd-shim  old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-esbuild-0.21.5   old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-esbuild-0.27.7   old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-notesmd-cli      old_exit=0 new_exit=0 stdout_same_as_retained=yes
   pro-op               old_exit=0 new_exit=0 stdout_same_as_retained=yes
   ```

   All 8 exits unchanged (0 → 0); every fresh stdout is byte-identical to the retained
   `compare.json` (`diff -q` per label). Confirms the new code paths are dormant when the
   prediction carries no new keys — only `pro-esbuild-0.27.7.prediction.json:14-19` has
   `extra_expectations`, and only the four r17 keys (`language_compiler`,
   `invalid_version_strings`, `bootstrap_attempts_at_least`, `analyzer_errors_contain`).

## Risks / notes for the L1

- The strict `obs.get("eof_reads")` equality means W18 compare goes red (exit 1, not 2) if a
  prediction sets `eof_reads` and the observation JSON predates the log-extract.py `eof_reads`
  field — W18 run-carriers must pair with the updated log-extract sibling (contract.md:123-125).
  `invalid_index_reads` behaves identically (raw fetch, absent → mismatch).
- `analyzer_errors_empty` tolerates an absent observed `analyzer_errors` key (treated as empty);
  `analyzer_errors` is not in `OBS_REQUIRED` (compare.py:58-62), unchanged.
- No git/jj writes; only compare.py and this report were written.
- No installs needed (Python 3 stdlib only).

Report: .ufo/waves/round-18/w1/CompareEofFields.md
