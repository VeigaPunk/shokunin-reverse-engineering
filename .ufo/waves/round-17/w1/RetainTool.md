# RetainTool-3 — retain.py report (round 17, wave 1)

## Files written
- `.ufo/waves/round-17/tools/retain.py` (new, executable; sole assigned file)

## Implementation vs contract (`contract.md:22-29`)
- CLI `retain.py --out RECEIPT.json [--pin PATH]... [--cwd DIR] [--timeout S] -- ARGV...`;
  args split manually on the first `--` (`retain.py:166-190`), never argparse REMAINDER.
- Imports sibling pins.py via `importlib.util.spec_from_file_location` resolved from
  `Path(__file__).parent / "pins.py"` (`retain.py:29`, `56-63`). **Observation:** pins.py
  was absent when drafting began (10:36Z) but landed at 10:39Z before finish; retain.py was
  coded against the contract signatures and verified against the delivered file
  (`pins.py:62` `snapshot(paths)->dict`, `pins.py:75` `compare(pre,post)->dict` returning
  `equal`/`changed`/`missing`). No stub was written.
- Flow (`retain.py:80-157`): pins.snapshot pre → `subprocess.Popen(argv, shell=False)`
  with stdout/stderr opened directly to `RECEIPT.json.stdout`/`.stderr` next to the
  receipt (inference: "RECEIPT.stdout" read as literal `RECEIPT + ".stdout"` suffix) →
  `wait(timeout)`, kill on TimeoutExpired → pins.snapshot post → pins.compare → atomic
  receipt write (`.tmp` + `os.replace`, `retain.py:66-72`).
- Receipt carries exactly the contract fields (`retain.py:132-147`): argv, cwd, started/
  ended_at_utc, exit, stdout/stderr path+sha256, `python: sys.version`,
  `orig_argv: sys.orig_argv` (getattr fallback), pins_pre, pins_post, pins_compare.
  Extra keys only on failure paths: `timed_out`, `spawn_error`.
- Exit codes (`retain.py:150-157`): 0 child ran + pins equal (any child exit recorded,
  never propagated); 1 pins differ; 2 spawn failure/timeout/bad input/missing pins.py.
- Stdout emits a JSON summary `{receipt_path, child_exit, timed_out, spawn_error,
  pins_equal, exit}` on every non-selftest path, errors included (contract.md:5).
- `--help`/docstring states the pins limitation ("same bytes at two instants, never
  unchanged throughout"), matching pins.py's own caveat.

## Selftest (run once, after pins.py landed)
- Command: `python3 -I .../tools/retain.py --selftest` → stdout ended `SELFTEST: CLEAN
  cases=3`, exit 0.
- Cases (all children are `sys.executable -c ...`, i.e. `python3 -c` only, `retain.py:201`):
  1. clean: child exits 3, pinned file untouched → tool 0, `pins_compare.equal=true`,
     `RECEIPT.stdout` captured `b"ok\n"`.
  2. red: `python3 -c` child mutates the pinned file → tool 1, `changed` names the path.
  3. timeout: `time.sleep(30)` with `--timeout 1` → tool 2, `timed_out=true`,
     `exit=-9` (SIGKILL recorded).
- Fixtures built under `tempfile.mkdtemp()` and removed (`retain.py:198`, `253-254`).

## Other verified behavior
- Missing pins.py path (observed before pins.py landed): JSON error on stdout, exit 2,
  no capture/receipt files created.
- Missing `--` separator: JSON error, exit 2. `py_compile` clean; stray `__pycache__`
  from the compile check removed.

## Limits / notes for L1
- Child killed on timeout reports `exit: -9` (signal), not null — recorded truthfully.
- `cwd` defaults to the retaining process's cwd when `--cwd` omitted (recorded resolved).
- Receipt files land in whatever dir `--out` names; `retain.py` creates that dir if absent.
- No carrier binaries were executed; selftest children are `python3 -c` only per contract.
- No installs performed; stdlib only. No tools installed or upgraded.
