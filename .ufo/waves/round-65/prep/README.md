# round-65 prep — toolchain cache cleanup (pre-freeze)

Observed 2026-11-03 20:12 -03, before the round-65 instruments were frozen.

Command: `cd /home/vgpnk/.local/share/kaidoku-jsc && find . -name '__pycache__' -type d -print | sort`
Output (retained verbatim in `precache-dirs.txt`):

```
./jsc2js-src/View8/Parser/__pycache__
./jsc2js-src/View8/Simplify/__pycache__
./jsc2js-src/View8/Translate/__pycache__
./venv/lib/python3.15/site-packages/parse/__pycache__
```

Command: `find . -name '*.pyc' | wc -l` -> `15`. The 15 filenames were printed by
`find . -name '*.pyc'` in the same pass but not written to a file; only the count and the
four directories above are retained. This is stated as a limit, not a reconstruction.

Removal: `find . -name '__pycache__' -type d -prune -exec rm -rf {} +`; re-check
`find . -name '*.pyc' | wc -l` -> `0`.

Why: the round-64 non-author review F2 found the View8 runs wrote `__pycache__` into the
retained toolchain. Round 65's closure requires a cache-free start (the instrument's
`cache_entries()` clause refuses a contaminated tree) and disables bytecode writes for
every subprocess (`-B` + `PYTHONDONTWRITEBYTECODE=1`).

The cache-free state is re-asserted at every manifest check; the census proves the run
writes nothing (before/after maps equal, `jsc2js-src/.git/` excluded as non-input git
metadata).
