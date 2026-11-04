# MutClosure - R66-C1 counter mutation probe (scoped findings)

Target: `tools/round-66/closure-boundary.py` sha256 `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b`
(frozen, never edited). Five mutants in isolated scratch mirrors, each scored by both `--selftest` and `--verify`.
Full table, diffs and verbatim detector lines: `.ufo/waves/round-66/w1/MutClosure/mutants.md`.

Pristine baseline: `--selftest` exit 0 `SELFTEST CLEAN cases=30 failures=0`; `--verify` exit 0 `passed 5 of 5`.

| # | mutant | `--selftest` | `--verify` | verdict |
|---|---|---|---|---|
| M1 | post-probe `cache_entries` scan moved before the probe | exit 1, failures=3 | exit 1, 4/5 | killed (a2; selftest red-ok / red-cache-names-pyc / red-finding-names-cache) |
| M2 | `count_ok` dropped from `ok` | exit 1, failures=1 | exit 1, 4/5 | killed (a4; selftest trunc-ok) |
| M3 | skip-run synthetic `closure.ok=true`, `closure_claimed=true` | exit 1, failures=2 | exit 1, 4/5 | killed (a5; selftest skiprun-closure-none / skiprun-not-claimed) |
| M4 | `fixture_probe` always guarded | exit 1, failures=3 | exit 1, 4/5 | killed (a2; selftest red-ok / red-cache-names-pyc / red-finding-names-cache) |
| M5 | `arm()` returns `passed: True` unconditionally | exit 0, CLEAN 30/0 | exit 0, 5/5 | **SURVIVED** |

Survivor finding: `tools/round-66/closure-boundary.py:219-220` (`def arm(...)` / `"passed": bool(passed)`) is bound by
neither detector. `selftest()` (lines 331-437) never calls `arm(`; every call is in `run_verify` (243, 255, 265, 275, 283),
and on a green host all five arm conditions are true, so `--verify` (consuming `a["passed"]` at line 288) cannot tell the
mutant from the pristine counter. Controlled red with the same entry point - `--verify --python /nonexistent/r66-python` -
pristine exits 1 with `passed 2 of 5`, M5 exits 0 with `passed 5 of 5` while every arm detail is `ok:false`. That is a
coverage gap in the counter's own two detectors, not a change to the R66-C1 predicate.

Incidental: a4 passes with a missing `--probe` (`findings: ["missing 1: probe", "count 29 != 30"]`), so it does not
isolate the count clause; a3 caught the same condition. No verdict depends on it.

Integrity: frozen counter sha256 unchanged after all runs (`3c5cfb03...`, 20908 bytes); frozen r65 instrument
`79a4dca4...` unchanged. No git/jj command run; scratch `/fast/scratch/hyaku/kaidoku-r66/MutClosure` deleted.
