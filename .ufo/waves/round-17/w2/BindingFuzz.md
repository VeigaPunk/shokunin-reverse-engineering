# BindingFuzz — falsify bind_session + LogPoller (carrier-run.py)

Target: `W/tools/carrier-run.py` @ da64646a (tool sha256
`609503461722761c901ab15871afe07b490422b34aff5b50eb4d171a138f157c`).
Ran: `python3 -B -I W/w2/binding-attack.py` → exit 1, 17 cases, **13 defects**.
No REA/Ghidra invoked; injected fake runner only; all fixtures under /tmp.

`bind_session` (carrier-run.py:124-139) binds a session dir to a carrier by
two **unanchored substring tests on the CURRENT bytes** of the retained
`ghidra.log`: line 136 `Using log file: <dir>/ghidra.log`, lines 137-138
`IMPORTING: file://<dir>/target-<sha[:12]>.bin`. `run()` then trusts this:
`bound_sessions` (355-359) and the `len(bound) != 1 + len(searches)` → exit 2
gate (380-381).

## False bindings (OBSERVED)

- **F1 — 12-hex sha prefix collision (b04).** Carrier sha differing in all
  chars 13-64 binds: `target_ok` only tests `sha[:12]` (carrier-run.py:137-138).
  Two different carriers are indistinguishable → receipt can name the wrong
  carrier as bound and the exit-2 count still passes.
- **F2 — suffix/line-context false binds (b05, b06, b07).** Needles are bare
  substrings, not line-anchored:
  - `target-<sha12>.bin.bak` matches `target_ok` (b05);
  - both needles appearing **only inside a stack trace / error text**
    (assigned case) bind `logfile_ok`+`target_ok` (b06);
  - only the rotated name `ghidra.log.1` matches `logfile_ok` (b07).
- **F3 — stale-digest bind via retained-file mutation (b08).** After the
  poller records `files["ghidra.log"]["sha256"]`, replacing the retained file
  with a **symlink** to a foreign log makes `bind_session` (line 133 plain
  `open`) bind bytes whose sha256 was never recorded — recorded digest and
  bound bytes differ. Scan() refuses symlink *sources* (line 210) but nothing
  rechecks the retained path at bind time.
- **F4 — replayed foreign log binds (b09a, b09b).** A verbatim `ghidra.log`
  retained by a *different* round-17 run (fixture discovered from
  `runs/*/logs/*/ghidra.log`) binds when queried with its own embedded
  session dir + carrier sha, even though that session dir was deleted at run
  end and never tracked by this caller; same log with the dir string
  rewritten to the queried dir also binds. Binding = "log claims it", with
  no run-id/pid check (w1 SentinelPollRace F2 shows `ownership.json` exists
  for exactly this purpose).

## LogPoller defects (OBSERVED)

- **F5 — symlinked session dir silently dropped (p01).**
  `list_session_dirs` excludes dir symlinks (carrier-run.py:73); the dir is
  never tracked and the receipt has no record that a dir existed and was
  skipped — distinguishable from "no session" only by absence.
- **F6 — stale retention of vanished dirs (p03, p04).** A tracked dir
  deleted mid-run (assigned case) or swapped to a symlink stays in
  `self.tracked`/`retained()` forever (nothing reconciles `tracked` against
  the filesystem, carrier-run.py:196-241) → ghost entries in
  `retained_logs`/`unbound_sessions`; under the private-root path this
  inflates `len(bound)` arithmetic and forces spurious exit 2 (INFERENCE:
  gate reachable only when `runner is None`, which needs a real REA spawn —
  not exercised per contract).
- **F7 — crash: uncaught FileExistsError in scan (p05a, p05b).**
  `os.makedirs(logs_dir, exist_ok=True)` (carrier-run.py:216) sits **outside**
  the two `except OSError: continue` guards; a regular file at
  `out/logs/<basename>` raises through `_run_polled`'s poll loop
  (carrier-run.py:415) and out of `run()` → **interpreter traceback, no
  receipt.json**, violating contract exit semantics. Observed end-to-end:
  `FileExistsError: [Errno 17] ... out2/logs/rea-ghidra-CRASH2`, receipt not
  written. Trigger is plausible residue from a prior run/crash reusing
  `--out-dir`.
- **F8 — basename collision shares one output file (p06).** `logs_dir` is
  keyed by `os.path.basename(d)` only (carrier-run.py:215): two session dirs
  with the same basename under different parents (nested `session_glob`)
  share `out/logs/<name>/ghidra.log`; last sorted writer wins, then
  `bind_session(p1)` reads p2's bytes while p1's recorded digest attests the
  overwritten copy → false bind on unattested bytes. (Current flat glob is
  safe; defect if glob ever spans parents.)

## Correct refusals (calibration)

- b02 log naming a different session dir → `logfile_ok` false; b03 correct
  dir + wrong 12-hex prefix → `target_ok` false. Genuine wrong-carrier /
  wrong-dir logs DO refuse — the falsification is in substring, truncation,
  and provenance gaps, not the happy path.
- p02 file-level symlink skip works (only `script.log` retained; session
  lands unbound silently — minor observability gap, not counted as defect).
- Dir deleted mid-scan does not crash scan (p03) — graceful, but see F6.

## Exit / artifacts

Script: `W/w2/binding-attack.py` (exit 0 attack failed / 1 findings).
Full JSON: `/tmp/bindfuzz-out.json` (ephemeral; verdicts reproduced above).
Installs: none.
