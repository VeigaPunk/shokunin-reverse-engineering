# SafetyReads — credential/config reads and target execution (r16 w1, sentinel)

Axes: depth, calibration. This is a static review of the proposed scripts. The scripts were still being edited during the wave, so the findings apply to this snapshot (sha256 taken 05:16 -03):

- `selection.py` `97a9a8b3…bc24`
- `selfcheck.py` `474cfa17…1693`
- `controls.py` `3e31a3bf…cdc0`
- `measure.py` `a1aa289b…94d`
- `selection-fixtures.json` `ff2483d8…aaa`

`negative-fixtures.json` was read for its case ids only. Later edits need a re-read. Paths below are relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/`.

## Verdict on the assigned surface

None of the four scripts reads credentials or executes a target. Every finding below is Low and needs either adversarial input or a non-default environment. No pass, score or capability is claimed.

## Non-defects (evidence)

**selection.py reads only the data files.**
- It imports `argparse, hashlib, json, re, sys, pathlib` (:34-39). There is no subprocess, no environment read and no network.
- File names come from parsed integers: the base name is `"go%d.%d.%d.json"` (~:182), and diff entries must fullmatch `_DIFF_NAME_RE` in `root/patchverdiffs` (:207-216). `goos`/`goarch` only build arch keys (:96-110) and never reach a path.
- Diff files are hashed, never parsed.
- The base file is parsed, but only top-level keys equal to search-order names are printed (`base_matching_buckets`). A hostile or symlinked root can therefore expose only the relative path, size, sha256 and a JSON-decoder position message, not the file's contents.

**selfcheck.py stays inside the fixture data.**
- It imports stdlib only (:68-76).
- It runs `selection.py` by path through `importlib` (:96-102), without changing `sys.path`.
- `--selection` (:346) can execute any Python file, but only one the operator names. That is the designed behaviour, not a boundary crossing.
- The current `selection.py` defines functions only at top level.

**controls.py and measure.py only call `git`.**
- Their only subprocess is `["git","-C",ROOT,…]` in list form, with no shell (controls:42-46, measure:43-46).
- The subcommands used are `rev-parse --verify`, `ls-tree` and `show <rev>:<path>`.
- `git show` prints plain blob contents (git-show(1) man source line 48). textconv runs by default only for diff/log output (lines 2218-2221).
- stdout is a pipe, so `GIT_PAGER` (set in this session's env) never runs. [INFERENCE: these commands do not refresh the index, so no fsmonitor or hooks run; not observed.]

**Target execution: none.** No Ghidra, Java, `GoApiSnapshot`, JsonPatch or Go binary is invoked anywhere.

## Findings

### R1 — Low: `selection.py` exits outside the 0/2 contract, and the outcome depends on the environment
- **Exploit path:** a request component longer than 4300 digits makes `int()` at :83 raise a plain `ValueError`, not `RequestError`. A deeply nested base JSON raises `RecursionError`, which escapes `except (OSError, ValueError)` at :148. The CLI catches only `RequestError, UnreadableError` (:281), so the result is a traceback and exit 1.
- **Config dependence:** without `-I`, `PYTHONINTMAXSTRDIGITS=0` removes the digit limit. The same request then becomes `RequestError` and exit 2. [INFERENCE from the documented env var; not run.]
- **Evidence:** a stdlib-only probe (`python3 -I -c`; it did not import or run any proposed script) showed `default_max_str_digits` = 4300. `int("1"*5000)` raised `ValueError`, and `json.loads(b"["*200000)` raised `RecursionError` (not a `ValueError`).
- **Impact:** an unreadable or invalid input gets an exit code the contract does not define. selfcheck masks this, because `run_case` catches every `Exception` (selfcheck:314).
- **Smallest remediation:**
  - Reject any component longer than 10 digits before calling `int()`, or convert its `ValueError` into `RequestError`.
  - Add `RecursionError` to the except clause at :148.

### R2 — Low (calibration/provenance): `controls.py` builds its "producing_command" instead of recording it
- **Evidence:** `producing_command` (:283-286) hard-codes `python3` and renders only `-I`, from `sys.flags.isolated`. It drops every other interpreter flag (`-E/-s/-P/-X/-S`) and the real executable, and it does not quote the revision names.
- **Exploit path:** run it as `/usr/bin/python3.14 -E -s controls.py A B`. The record claims `python3 <abs> A B`, which is a different argv. This is exactly the fidelity gap that round-15 routes 1 and 3 are about (`corpus/lessons/round-15-verifier-spotcheck.md:185,187`).
- **Remediation:** record `sys.executable` and `sys.orig_argv` (available on the host's Python 3.14), and render them with `shlex.join`. Keep `argv_note`.

### R3 — Low (latent): the documented commands run without interpreter isolation
- **Evidence:** the usage lines omit `-I`: measure:4, controls:4, selfcheck:10,16. Run that way, Python honours `PYTHON*` env vars, enables user site-packages (`site.ENABLE_USER_SITE` is True; `~/.local/lib/python3.14/site-packages` currently has no `.pth`/customize file) and puts the script's directory first on `sys.path`.
- **Current state:** no sibling file in `round-16/` shadows a stdlib module the scripts import.
- **Limit:** `-I` is not fully isolating either. The system `distutils-precedence.pth` still runs and reads `SETUPTOOLS_USE_DISTUTILS`. Do not write "`-I` = no host config read".
- **Remediation:** document the `-I` absolute-path form, as EntryDraft does for `selection.py`.

### R4 — Low (latent, calibration): git environment and replace refs can change which objects are read
- **Evidence:** `subprocess` passes the whole environment to `git`.
  - `GIT_DIR`, `GIT_OBJECT_DIRECTORY` and `GIT_ALTERNATE_OBJECT_DIRECTORIES` override `-C ROOT`. [INFERENCE from git docs.]
  - `refs/replace/*` is honoured by default.
  - Observed now: 0 replace refs, and no `GIT_DIR`/object-dir variable in this session.
- **Impact:** the docstrings promise "immutable Git objects". Under a hook-like or harness environment, the census could read a different object store.
- **Remediation:** drop `GIT_*` repository-selection variables and set `GIT_NO_REPLACE_OBJECTS=1` in the subprocess env, or state this as a limit.

### Adjacent (outside this lane; for SafetyPaths/L1) — Low, latent
- **Evidence:** selfcheck:309 uses `TemporaryDirectory(prefix=f"selcheck-{cid}-")`. CPython `tempfile.py:378` joins the prefix without sanitizing it.
- **Exploit path:** an id containing `/` either crashes or, if `/tmp/selcheck-…` exists, creates the case root outside the temp area. The crash comes from an uncaught `OSError` and gives exit 1, so it reads as a mismatch rather than a harness error. Note that `/tmp` is world-writable.
- **Current state:** none of the current ids (9 selection, 17 negative) contains `/`.
- **Remediation:** use a fixed prefix, or validate `id` against `[A-Za-z0-9_.-]+`.

## Limits
- This is a static review of a moving snapshot.
- I did not run selection, selfcheck, controls, measure, fixtures or git-mutating commands. The only execution was the stdlib probe above, plus read-only `ls`/`git for-each-ref`/`env` key-name listings.
- Single host: Python 3.14.7, Ghidra 12.1.4. The installed golang dir has no symlinks.
- Tool installs/updates: none (pacman paused per operator ruling).
