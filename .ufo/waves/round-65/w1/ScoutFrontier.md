# ScoutFrontier — r65 w1, round-65 claim scout (read-only data walk)

Seat bounds honoured: no scratch dir created (nothing large was copied or built), no
matrix run, no receipt written, no writes outside
`.ufo/waves/round-65/w1/ScoutFrontier/`. Everything below was measured with `sha256sum` /
`find` / `stat` / `read` at base `c99e907cb5576c13a7b22755d776b356fdfc1752` (worktree; no
git mutation, read-only `git status`/`git ls-files`/`git check-ignore` only).

## 1. (a) R65-C1 manifest re-derived independently — 0 mismatches of 30

Method: the `CLOSURE` literal and the three singleton pins were lifted from the frozen
instrument with `ast.parse` + `ast.literal_eval` of the **source text** (never `import`,
so no bytecode was written anywhere), then each path was opened and hashed with
`hashlib.sha256`. `closure_findings()`/`--manifest` was not invoked: this is a second
implementation of the same check, not a re-run of the first.

- `ENTRIES 30 CLOSURE_DICT 27` — 9 d8 files + 12 View8 files + 5 venv-identity files +
  `inputs/atom.compiled.dist.jsc` = 27, plus probe + node + interpreter = 30 (the count
  the plan states and the count `closure_findings()` reports as `len(CLOSURE) + 3`).
- `MISMATCHES 0 []`; missing 0.
- Table, both hash columns and the verdict, at
  `w1/ScoutFrontier/manifest-recheck.md`. That table was itself re-parsed afterwards and
  every row re-hashed by path: 30/30 rows aligned, 0 deviations (self-check included in
  the same command run).
- Instrument bytes at measurement time:
  `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6  tools/round-65/jsc-closure-matrix.py`
  — equal to the frozen sha in `claims.json.instruments` and in the seat brief.

So the closure half of clause (i) holds on the worktree as measured. Clauses (ii) labels
and (iii) census are not mine and were not measured.

## 2. (b) Cache state and interpreter chain

```
$ find /home/vgpnk/.local/share/kaidoku-jsc \( -name '__pycache__' -o -name '*.pyc' \) -print | wc -l
0
```

Exit 0, no output: the toolchain root is cache-free; all four directories listed in
`.ufo/waves/round-65/prep/precache-dirs.txt` are absent.

**Observed fact outside that scope (for the reviewers, not a predicate failure):** a
bytecode cache exists in the lane repo next to the frozen tools —

```
tools/round-65/__pycache__/jsc-closure-matrix.cpython-314.pyc   38922  2026-11-03 20:24:49.798052283 -0300
tools/round-65/__pycache__/coverage-recipe.cpython-314.pyc      16671  2026-11-03 20:24:49.800012043 -0300
```

- It is gitignored (`.gitignore:1:__pycache__/`, `git check-ignore -v` rc 0) and untracked
  (`git status --porcelain -- tools/round-65` empty; `git ls-files tools/round-65` lists
  only the two `.py` files), so it cannot enter the declaration.
- The `.pyc` headers were read with `struct`: both record flags 0, source mtime and size
  **equal** to the current source stat
  (`jsc-closure-matrix`: 1793747991 / 24706; `coverage-recipe`: 1793747760 / 10777).
  Conclusion: both modules were compiled from exactly the frozen bytes, and neither source
  has changed since.
- The write happened at 20:24:49.798/.800, the same instant as
  `.ufo/waves/round-65/claims.json` (mtime 20:24:49.800316883). Both frozen modules being
  cached means a process **imported** them (running a script as `__main__` caches nothing)
  without `-B`/`PYTHONDONTWRITEBYTECODE`, under CPython 3.14 (tag `cpython-314`; the host
  `python3` is 3.14.8 at `/usr/bin/python3` — not the 3.15 venv used by the matrix).
- Scope: the instrument's cache test is root-scoped (`cache_entries(root)`,
  `tools/round-65/jsc-closure-matrix.py:244`) and both censuses are root-scoped
  (`before = census(root)` line 305, `after = census(root)` line 339). Neither sees
  `tools/round-65/`. The predicate's "no Python bytecode cache present" is therefore
  satisfied *on the root the instrument defines*; the round-64 F2 repair ("subprocesses
  stage with bytecode writes disabled" — `SUBPROCESS_ENV` line 129, view8 spawn line 324
  `-B`) covers the matrix's own children, not the seat process that froze the container.

**Interpreter chain** (`ls -la`, `readlink`, `readlink -f`, `sha256sum`):

```
kaidoku-jsc/venv/bin/python -> python                     (relative, same dir)
kaidoku-jsc/venv/bin/python3 -> python
kaidoku-jsc/venv/bin/python3.15 -> python
python -> /home/vgpnk/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin/python3.15
        -> /home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu   (uv major-minor alias dir)
resolved binary: /home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15
sha256 aac3ade3f7d90fbf63e3ea0c46120a0cfbd159e1e503dde04721979507a1548b  == INTERPRETER_PIN
```

`venv/pyvenv.cfg` (sha256 matches the frozen pin `87a6b46e...`):
`home = /home/vgpnk/.local/share/uv/python/cpython-3.15-linux-x86_64-gnu/bin`,
`implementation = CPython`, `uv = 0.13.0`, `version_info = 3.15`,
`include-system-site-packages = false`.

**Two stated bounds on that pin** (both fail-closed for the common case):
- identity is **byte**-identity, not path identity: `run_matrix` resolves the interpreter
  and then tests `is_file()` + sha256 (`closure_findings`), so a byte-identical copy at a
  different path would pass; a uv re-point of the alias to another patch level resolves to
  a different path whose bytes differ, so it exits 2 — the fail-closed direction is the
  one that matters.
- `pyvenv.cfg.home` names the **unpinned** major-minor alias, not the pinned `3.15.0`
  directory; the pin is carried by the resolved binary, so the alias is only a resolution
  step, never a trust anchor.

## 3. Predicate parity (checked because the claim depends on it)

| location | verdict | how |
|---|---|---|
| `tools/round-65/jsc-closure-matrix.py` `PREDICATE` | reference string | `ast.literal_eval` of the source literal |
| `.ufo/waves/round-65/claims.json` → `claims["R65-C1"]["predicate"]` | byte-identical | `==` |
| `plans/round-65-claims.md` | identical after removing blockquote markers and line wrapping | whitespace-normalised `in` test |

So the plan renders the sentence as a wrapped blockquote but does not alter a character;
the container carries it verbatim. The plan states "Closure (30 pinned entries)" — which
matches the 30 measured here.

## 4. Ordering limit observed in the frozen instrument (report-only; bytes not touched)

`python_probe` (line 300, the venv interpreter importing `parse` from the View8 cwd) runs
**after** the closure/cache check (line 244) and **before** `before = census(root)`
(line 305). Any bytecode that probe wrote would therefore enter the before-map and be
invisible to the delta, and could not fail the cache check of the same run. It is invoked
with `-B` and `PYTHONDONTWRITEBYTECODE=1` (lines 260/262) and writes nothing on this tree,
so this is a bound on what the census can witness, not an observed contamination. Same
shape for `census()`'s symlink skip: a symlink *added* to the root during a run is not a
census row (an existing file replaced by a symlink does surface, as `removed`).

## 5. (c) Section-scoped record sweep — planning note (next round's plan, not an R65 claim)

Source: r63 `planned` ("a section-scoped sweep over the record sections with their own
bindings would close the corpus's last unchecked edge class; a new instrument and its own
freeze per the r60 rule"), carried as open by r64's `Planned`.

Enumerates: every `## Round <N>` section of `SCORECARD.md` and every round block of
`LOG.md` at one named revision — the sections themselves, not the
`.ufo/waves/round-N/l1/(scores|records)/` receipt paths the r60/r62/r63 sweeps already
enumerate. Per section it yields the line bounds and the commit span the section's own rev
names cover.

Bindings each section must supply:
- identity: round number, date, title, first/last line;
- rev map: base, declaration, freeze, landing, record, tip, each as 40-hex, either printed
  in the section or supplied by an explicit per-section table the sweep records as
  caller-supplied (SCORECARD prints abbreviated hashes — which is exactly why the r61 gate
  cannot be reused unchanged: its own Limits paragraph says abbreviated form does not
  resolve);
- receipt pointers: path plus `rev=` and `check=` trailer values;
- edge atoms: the r61 grammar's `SKILL|LOG|SCORECARD|PROVINCE delta a->b exactly "x y"`
  claims and the LOG close-entry equivalents;
- the `planned` field, as that round's declared open items, compared against the next
  section's executed set.

Cheapest control that shows it unmoved: two in-memory fixtures, no new data. A = a
section's committed bytes verbatim with its rev map supplied; expected exactly the one
known r60 T7 finding and its exit class, zero others. B = the same bytes with one character
changed inside that claim's measured pair (`1 0` to `1 1`); expected the same single key and
the same exit class, every other key identical. A third zero-claim fixture must exit 2
(unevaluable), never clean — the QUALITY #66 boundary. Keys and exits compare against an
expected table committed before the first run; the sweep is unmoved iff A and B differ in
exactly that one key and every exit matches the table.

(324 words, no implementation.)

## 6. Not done here (boundaries)

No matrix run, no label or census measurement, no `--selftest`, no toolchain copy, no
`git`/`jj` mutation, no writes outside `w1/ScoutFrontier/`. The scratch dir
`/fast/scratch/hyaku/kaidoku-r65/ScoutFrontier` was never created because nothing needed
staging.
