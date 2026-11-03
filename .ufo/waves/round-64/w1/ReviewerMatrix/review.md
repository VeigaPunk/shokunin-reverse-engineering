# R64-C1 instrument review (ReviewerMatrix, w1, round 64)

Read-only review of `tools/round-64/jsc-route-matrix.py` (329 lines) against the frozen predicate and the frozen plan. The matrix was not run. Commands run: `--selftest` (22 cases, 0 failures, exit 0) and `--skip-run --out <scratch>` (0/18, exit 1), both with `TMPDIR` in my scratch, which I removed. Read-only `check_pins` call on the real files (no d8 execution): returned `None`.

## Checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | instrument sha256 = 29efef4f… | PASS | `sha256sum` = `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`, 329 lines |
| 2 | PREDICATE = claims.json = plan | PASS | instrument L49-51 (concatenated); `claims.json` L12 and `plans/round-64-claims.md` L23. Byte-equal under Python `==`, both `in` checks True |
| 3 | PREDICTED = plan table | PASS | instrument L69-76; plan "Frozen predicted labels" table (6 rows parsed with escaped `\|` handled) equal to PREDICTED, `==` True |
| 4 | classifiers vs docstring | PASS, one doc mismatch (F5) | L94-102, L105-111, L114-115, L89-91 |
| 5 | verdict counts 18, missing = not-run | PASS | L124-140: `total = len(PREDICTED)*REPS` = 18; `labels.get(..., "not-run")`; `--skip-run` gives `runs_total` 18, `runs_matching` 0 |
| 6 | check_pins before any run | PASS for the pins it has; gap in coverage (F1) | L179-182 precede the first `d8` call at L195; real files pass `check_pins` (`None`) |
| 7 | writes only under --work/--out | FAIL (F2) | `view8.py` run with `cwd=view8_dir` (L204-207) imports `Parser.sfi_file_parser` (view8.py L3) and writes `__pycache__` into the frozen toolchain tree |
| 8 | emit cannot print verified on incomplete run | PASS | L223-232: `verified` is `matches == total`; labels not seen count as not-run; `verified: false` with exit 1 |
| 9 | exit 0 without 18 matching runs | PASS for the counting command; `--selftest` returns 0 without a matrix run (F3) | L316-317 |

## Findings

| id | line | class | blocking? | evidence |
|---|---|---|---|---|
| F1 | L56-66 (PINS), L142-166 (check_pins), L101 n/a | predicate-coverage | **blocking** | Predicate requires "every input and binary sha256 equal to its pin". PINS covers probe, typora, d8 binaries D1-D3, D1 snapshot and icudtl, and `view8.py` only. Not pinned or checked: `snapshot_blob.bin` for D2 and D3 (L159 checks D1 only). Observed on disk: D2 `601efdc6…`, D3 `80590f45…`, both differ from D1 pin `b5c418dc…`; D2/D3 `icudtl.dat` = `c5da2fc3…` (same as D1). Also unpinned: `node`, the venv `python`/parse 1.22.4, and the rest of the View8 tree (only `view8.py` is pinned, L163-165). Whether d8 loads the neighbour's snapshot from its own directory is **[INFERENCE]**, not observed. |
| F2 | L204-207, L211-212 (cwd=view8_dir) | side-effect / rule 7 | **blocking** | `view8.py` imports `Parser.sfi_file_parser` (view8.py L3) from the frozen jsc2js tree. Evidence: `View8/Parser/__pycache__/*.cpython-314.pyc` and `cpython-315.pyc`, plus `View8/Simplify/__pycache__/*`, all mtime 2026-11-03 19:36 (`git status --ignored` shows them as `!!`). `PYTHONDONTWRITEBYTECODE` is unset in this shell. Violates the "never writes outside --work and --out" check and the "never write into the toolchain" rule. The instrument does not set the variable, and it cannot be edited here. The run must set `PYTHONDONTWRITEBYTECODE=1` in its environment (no instrument edit needed). |
| F3 | L316-317 | exit-semantics | non-blocking | `--selftest` returns 0 (`SELFTEST CLEAN`) without running any matrix cell. Not in the counting command, and the selftest's `verified` is not printed. A wrapper that treats exit 0 as verified would be wrong. |
| F4 | L173-174 (timeout only for d8), L204-207 (view8 timeout 600), L211-212 (node timeout 120), L179-182 | exit-class | non-blocking | Missing `node` or `python`, and `subprocess.TimeoutExpired` for view8 or node, raise uncaught exceptions. Python exits 1 with a traceback and no receipt is written. The docstring (L30-32) says exit 2 for "missing tool". No false pass: incomplete runs still never print `verified: true`. Only the could-not-evaluate class is misreported. A view8 timeout has no label; it is a crash, not a cell label. |
| F5 | L100-101 vs docstring L25 | doc mismatch | non-blocking | `dump-empty` is returned for any stdout that lacks `[SharedFunctionInfo]` (L100-101), not only for empty output. Docstring says "empty". No predicted cell depends on this path, so the verdict is unaffected. |
| F6 | L179 | TOCTOU | non-blocking | Pins are checked once before the 18 runs and never again. A binary swapped mid-run would not be detected. Low risk here, but the predicate's "every ... equal to its pin" is only checked at start. |
| F7 | L171 | quoting | non-blocking | `loadjsc('{artifact}')` interpolates the path into JS with single quotes and no escaping. Current inputs are fixed paths with no quote characters. |

## Verdict

Verified: checks 1-6 pass with F1 noted; checks 8 and 9 pass for the counting command; check 7 fails (F2).

`instrument-defective: F1, F2`

Notes for L1 (no edit made): F1 means "every binary pinned" is not literally true for the frozen instrument; the receipt must either list the unpinned binaries as out of scope or the claim is overstated. F2 can be neutralised at run time with `PYTHONDONTWRITEBYTECODE=1`, which the executor should set and record. Neither needs an edit to the frozen instrument; both are reported, not made.
