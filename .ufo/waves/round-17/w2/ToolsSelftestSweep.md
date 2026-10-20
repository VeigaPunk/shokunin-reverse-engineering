# ToolsSelftestSweep — round-17 selftest sweep + bytecode/vacuity audit

Scope: every `tools/*.py` plus `measure.py`, `controls.py` in
`.ufo/waves/round-17/`, invoked exactly as
`python3 -I -B <tool> --selftest`. Machine-readable record: `w2/selftests.json`.

## Results (observation)

All 13 selftests at the assigned tree state (HEAD `da64646` during the
sweep, 2026-10-20 11:09:08–11:09:10 -0300) exited 0 in a single pass
(~2.7 s wall for all 13):

| tool | exit | summary line |
| --- | --- | --- |
| buildinfo-probe.py | 0 | `SELFTEST: CLEAN cases=11` |
| carrier-census.py | 0 | `SELFTEST: CLEAN cases=10` |
| carrier-run.py | 0 | `SELFTEST: CLEAN cases=2` |
| compare.py | 0 | `SELFTEST: CLEAN cases=10` |
| controls.py | 0 | `SELFTEST: CLEAN cases=11` |
| invocation-audit.py | 0 | `SELFTEST: CLEAN cases=6` |
| log-extract.py | 0 | `SELFTEST: CLEAN cases=8` |
| measure.py | 0 | `SELFTEST: CLEAN cases=22` |
| pins.py | 0 | `red case observed: compare exit 1 names /tmp/.../a.txt` + `CLEAN cases=7` |
| predict.py | 0 | `SELFTEST: CLEAN cases=17` |
| receipt-validate.py | 0 | `SELFTEST: CLEAN cases=5` |
| retain.py | 0 | 3 JSON receipts (clean/pins-differ/timeout) + `CLEAN cases=3` |
| temporal-sweep.py | 0 | `SELFTEST: CLEAN cases=6` |

`find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo -name __pycache__`
is **empty after the sweep** (verified twice, latest ~11:26). My runs wrote
no bytecode anywhere (observation; `-B` end-to-end).

## Findings

### F1 — residual `__pycache__` hole survived the HEAD hardening (defect, observation)

`spec_from_file_location` + `exec_module` caches bytecode even under
`python3 -I`; only `-B`/`sys.dont_write_bytecode` suppresses it. Reproduced
in `/tmp` (selection.py copy → `__pycache__/selection.cpython-314.pyc`;
pins.py copy → `__pycache__/pins.cpython-314.pyc`). Note the pyc records
the *source* mtime (header field = 1792485220 → 05:33), not the write time.

At the committed HEAD `95e34db` the fix landed partially:
`tools/predict.py:67` and `tools/carrier-run.py:30` now set
`sys.dont_write_bytecode = True`, but the two other file-path importers of
the sibling `pins.py` do not:

- `tools/receipt-validate.py:89-91` (`_load_pins` via `load_pins`, called
  on every invocation including `--selftest`, `main():588`)
- `tools/retain.py:55-57`

`pins.py` cannot fix itself — the flag is read when the loader writes
cache, before module code runs — so `python3 -I receipt-validate.py …` or
`python3 -I retain.py …` (both documented invocations) still writes
`.ufo/waves/round-17/tools/__pycache__/pins.cpython-314.pyc`, inside the
lane tree and outside the paths the CLIs are given (contract.md:7).
Invisible to blob-based controls; gitignored (`!!` in `git status
--ignored`).

During this sweep `.ufo/waves/round-16/__pycache__/selection.cpython-314.pyc`
reappeared at mtime 11:08:56 — i.e., the F6 artifact noted by
`w1/CriticNoHarm.md` (mtime 10:32:31) was deleted and **recreated** before
my first selftest ran; a concurrent seat invoking `predict.py` without
`-B` is the only in-lane writer of that path. This independently confirms
the defect class still fires. (My sweep did not write it: `.st-*.out`
mtimes all ≥11:09:08.)

### F2 — vacuity audit: no vacuous selftest; two weak-red notes (observation)

Every selftest asserts on at least one red path; none is vacuous:

- `pins.py` C2/C6 assert `equal is False` and the changed list **names** the
  mutated path (`tools/pins.py:226-230`); C4 pins a never-existent file and
  asserts `equal is False` via `errors` (line 205-210) — a genuinely nasty
  negative.
- `retain.py` red case mutates the pin via a real `python3 -c` child and
  asserts exit 1 + `changed` names the path (lines 227-236); timeout case
  asserts `timed_out is True` + exit 2 (240-246).
- `receipt-validate.py` (swept version, da64646) asserts tampered-file → 1,
  forged `pins_compare` → 1, unreadable → 2 (lines 590-655 at HEAD).
- `controls.py` asserts the red commit is *detected and named*:
  `files[...]["unchanged"] is False`, `violations["1"] ==
  "row_text_changed"` (lines 476-488).
- `compare.py`, `predict.py`, `log-extract.py`, `temporal-sweep.py`,
  `buildinfo-probe.py`, `carrier-census.py`, `invocation-audit.py`,
  `measure.py`, `carrier-run.py` each assert mismatch/negative cases
  (e.g. `predict.py` invalid strings → exit 2; `log-extract.py`
  missing file → exit 2 via subprocess; `buildinfo-probe.py` truncated
  magic → `found=False`; `measure.py` Case A asserts the zero-counts).

Weak-red notes (not vacuous; candidates if a deeper hardening pass lands):

1. `receipt-validate.py` red cases assert the *exit code* only, not which
   finding fired — a validator that exits 1 for the wrong reason still
   prints CLEAN (`tools/receipt-validate.py:563-565`; the `detail` field is
   recorded but never checked). The HEAD version's new cases
   (`carrier_foreign_log_red`, `carrier_mid_run_drift_red`, lines
   622-650) share this property.
2. `carrier-run.py` selftest never exercises the CLI layer — `run()` is
   called in-process with injected runners (line 560+); `main()`'s argv
   contract (`--carrier/--label/--out-dir` required, exit 2 otherwise) is
   unexercised, unlike `pins.py`/`compare.py`/`predict.py`/`log-extract.py`
   which spawn `[sys.executable, "-I", script, …]`.

### F3 — `assert`-based selftests silently vacuous under `python3 -O` (inference)

`temporal-sweep.py` (all 6 cases, e.g. lines 253-345) and parts of
`buildinfo-probe.py` use bare `assert` inside `selftest()`. Under the
contracted `python3 -I` these fire correctly; under `python3 -O` they are
compiled out and the selftest would print `SELFTEST: CLEAN cases=N` having
asserted nothing. `contract.md:4` pins `python3 -I <abs path>` so the sweep
is unaffected; flagging only because every other tool uses explicit
`check()`/`failures[]` plumbing (`carrier-census.py:251-258`,
`pins.py:166-169`, `retain.py:201-210`, `compare.py:324+`, …) and
`temporal-sweep.py` deviates from that convention without need.

## Provenance

- Sweep ran against working tree `da64646adcb19c1ede7537b799b8c7d283fe43da`.
  During the wave the lane committed `95e34db62f2693c455d7ee4dfef24b8f3ebc007d`
  ("w2-hardened tools"); `receipt-validate.py` mtime 11:24:40. Re-run at
  HEAD: `SELFTEST: CLEAN cases=7` exit 0 — recorded in
  `w2/selftests.json.post_sweep_rerun`.
- `carrier-run.py` selftest spawns real `sys.executable` children for its
  fake analyzer (line 530-574); all fixtures under `tempfile.mkdtemp`
  prefixes (`*-selftest-*`) and cleaned up — observed: no leftover temp
  dirs, no writes outside /tmp.
- No tool executes a carrier; `invocation-audit.py`/`temporal-sweep.py`/
  `measure.py`/`controls.py` selftests create throwaway git repos only.
- `pins.py` selftest children use `-I` without `-B` (`tools/pins.py:181-182`),
  but only execute `pins.py` itself, which imports nothing local — no
  pycache written even without `-B` in children. `predict.py` children
  (lines 289-290) *do* import `round-16/selection.py` by path; with `-B`
  on the parent this stayed clean, without it this is the F1 write path.
- Installs: none. Python 3.14.x stdlib only.

## Bounded conclusion

13/13 selftests green; `find` post-condition currently satisfied; no
selftest is vacuous. One real residual defect (F1: two file-path importers
still leak `__pycache__` into the lane under documented `python3 -I`
invocation) and two hardening notes (F2 weak-red assertions, F3
`assert`-style selftests).
