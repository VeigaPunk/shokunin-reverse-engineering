# R64-C1 instrument mutation probe — MutCounter (w1, seat 12)

Frozen target: `tools/round-64/jsc-route-matrix.py`
sha256 `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` (329 lines).
Read-only throughout: source hash identical before and after the probe (29efef4f…ba20deb).

Method: each mutant is a byte-copy of the frozen source under
`/fast/scratch/hyaku/kaidoku-r64/MutCounter/` with exactly one textual change applied via
`str.replace(old, new, 1)` guarded by `assert text.count(old) == 1`. Detector for every copy
(pristine included): `python3 <copy> --selftest` with `TMPDIR` inside the scratch dir
(in-memory fixtures only — no d8, no view8, no node, no network, no writes outside scratch).
Do-nothing control: `python3 <copy> --skip-run`, expected exit 1.

## Baseline (pristine copy of the frozen bytes)

| run | exit | summary |
|---|---|---|
| `pristine.py --selftest` | 0 | `SELFTEST CLEAN cases=22 failures=0` |
| `pristine.py --skip-run` | 1 | `runs_total=18 runs_matching=0 verified=false exit=1` |

Baseline is green, so every mutant verdict below is interpretable.

## Results

| mutant | change | selftest exit | survived? | do-nothing exit |
|---|---|---|---|---|
| M1 | `classify_dump`: add `if code == 134: return "dump-ok"` before the exit check | 1 | no (KILLED) | 1 |
| M2 | `norm_rc`: `return rc` (signal deaths left negative) | 1 | no (KILLED) | 1 |
| M3 | `verdict`: `ok = matches >= total - 1` | 1 | no (KILLED) | 1 |
| M4 | `PREDICTED[("typora","D1")]` → `"dump-ok\|view8-ok\|node-pass"` | 1 | no (KILLED) | 1 |
| M5 | `SFI_RE = re.compile(rb"SharedFunctionInfo")` (brackets dropped) | 0 | **YES (SURVIVED)** | 1 |
| M6 | `classify_check` always `return "node-pass"` | 1 | no (KILLED) | 1 |

Every mutant still exits 1 under `--skip-run`: the do-nothing arm is not collapsed by any of
the six changes, so `--skip-run` cannot stand in for the selftest. All six mutants report
`runs_matching=0`, `verified=false`, `exit=1` on that arm (M4 is the only one whose
`predicted` payload changes, and it is still not verified).

## Kill evidence (verbatim FAIL lines)

- **M1** — killed by the signal-death fixture only:
  `FAIL dump-sigabrt got='dump-ok' want='dump-exit-134'`
  (`dump-sigsegv`, `dump-exit-1`, `dump-timeout` still pass: the mutation is keyed to 134.)
- **M2** — killed by both signal fixtures:
  `FAIL dump-sigabrt got='dump-exit--6' want='dump-exit-134'`
  `FAIL dump-sigsegv got='dump-exit--11' want='dump-exit-139'`
- **M3** — killed by the one-mismatch verdict fixture:
  `FAIL verdict-one-mismatch-exit got=0 want=1`
  (`verdict-all-match` and both do-nothing verdict cases still pass, so the off-by-one is
  caught solely because a 17/18 matrix is exercised.)
- **M4** — killed by the fake-green fixture:
  `FAIL verdict-fake-green-count got=3 want=0`
  The three reps of `typora|D1` now match the fake-green label, so the case that forbids a
  uniformly green table is what catches a mis-predicted cell. `verdict-one-mismatch-*` do not
  catch it (they only flip `typora|D2`).
- **M6** — killed by the failing-check fixture:
  `FAIL check-fail got='node-pass' want='node-fail'`

Each kill is a single-case kill: the instrument's self-test has exactly one load-bearing case
per behaviour probed here (134 mapping → `dump-sigabrt`; negative-rc mapping → `dump-sigabrt`
+ `dump-sigsegv`; verdict strictness → `verdict-one-mismatch-exit`; prediction fidelity →
`verdict-fake-green-count`; node failure → `check-fail`). That is adequate (each mutant dies)
but gives no margin: removing any one of those five cases would silently admit its mutant.

## Survivor M5 — coverage gap

`SFI_RE = re.compile(rb"\[SharedFunctionInfo\]")` → `rb"SharedFunctionInfo"`.

`python3 M5.py --selftest` exits **0** with `SELFTEST CLEAN cases=22 failures=0`, and its
stdout is **byte-identical** to pristine (`diff` reports no difference). The mutant is not
equivalent, though — it changes classification on inputs the self-test never constructs:

| fixture | pristine | M5 |
|---|---|---|
| `b"0x1: [SharedFunctionInfo] in OldSpace\n"` (real dump shape) | `dump-ok` | `dump-ok` |
| `b"0x1: SharedFunctionInfo in OldSpace\n"` (no brackets) | `dump-empty` | `dump-ok` |
| shipped `dump_ok` fixture | `dump-ok` | `dump-ok` |
| `b""` | `dump-empty` | `dump-empty` |

Cause: the self-test's only positive dump fixture is
`b"Start SharedFunctionInfo\n0x1: [SharedFunctionInfo] in OldSpace\n"` — its first line already
contains the unbracketed token, so a regex that has dropped the brackets still matches. The
fixture conflates V8 banner text with the SFI record marker, and `dump-empty` has no fixture
whose only content is the unbracketed token.

Scope of the gap: within the frozen 18-run matrix, `dump-empty` is predicted nowhere (the six
predicted cells are `dump-ok`/`dump-exit-134`/`dump-exit-139`), so M5 changes no predicted
label and cannot by itself flip R64-C1's verdict. It is a self-test sensitivity gap, not an
observed misclassification — the frozen prediction table is untouched by M5 and was not
re-predicted.

## Non-findings / deliberately not probed

- No mutant was aimed at `check_pins` coverage for the `D1-snapshot`, `D1-icudtl` or
  `view8.py` pins (the self-test exercises only `probe`/`typora` pin paths) — out of the six
  assigned changes, recorded here only as adjacent coverage to consider, not asserted.
- No real matrix run, no d8/view8/node invocation, no network, no edit to the frozen
  instrument, claims file or pins.

## Restoration / cleanup evidence

- `sha256sum tools/round-64/jsc-route-matrix.py` after the probe:
  `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` — unchanged.
- All mutant copies, the pristine copy and `TMPDIR` live only under
  `/fast/scratch/hyaku/kaidoku-r64/MutCounter/`; the directory is removed before yielding.
- Mutant sha256: M1 `7665b906…9d17`, M2 `2d8c735c…c09`, M3 `8c189982…df1`,
  M4 `081ef02a…ad03`, M5 `b4dfc41a…817c`, M6 `c225cde0…c503`; pristine copy equals the
  frozen `29efef4f…ba20deb`.
