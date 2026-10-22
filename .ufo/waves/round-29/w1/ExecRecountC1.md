# R29-C1 tip recount — ExecRecountC1

## Scope and execution

Ran the counter and selftest from the lane clone at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/clone`. The count used the requested measured revision `18be864a528873b2b70d8c94e31f880290249e90`; afterward the clone was detached at that revision before emitting the tally. No lane implementation/evidence files were edited. No tools were installed.

## Counter

**[OBSERVATION]** At `2026-10-22T20:21:24Z`, ran:

```text
python3 -I -B tools/round-29/c1-fresh-naming.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/clone --rev 18be864a528873b2b70d8c94e31f880290249e90
```

Full stdout:

```text
primary rule openchain_sole_unfiltered_args_consistent: named 122, right 122, wrong 0, no_name 30
runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1
```

Exit code: `0`.

## Selftest

**[OBSERVATION]** At `2026-10-22T20:21:34Z`, ran:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I -B tools/round-29/c1-fresh-naming.py --selftest
```

Exact summary stdout: `selftest cases=22 failures=0`; all emitted case lines were `ok`. Exit code: `0`.

## Detached-tip tally recompute

**[OBSERVATION]** At `2026-10-22T20:21:51Z`, ran in the clone:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout -q --detach 18be864a528873b2b70d8c94e31f880290249e90
```

Output: `EXIT=0`; command exit code: `0`. At `2026-10-22T20:22:04Z`, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD` output exactly `18be864a528873b2b70d8c94e31f880290249e90`.

At `2026-10-22T20:21:57Z`, ran:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I -B tools/round-29/c1-fresh-naming.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/clone --emit-tally
```

Stdout was redirected to `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/emitted-tally.json`; exit code: `0`.

**[OBSERVATION]** At `2026-10-22T20:22:04Z`, from the clone, ran:

```text
diff -u corpus/evidence/round-29/c1/tally.json /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/emitted-tally.json
```

Stdout: empty (no differences). `DIFF_EXIT=0`; exit code: `0`.

## Verdict

**[INFERENCE] Holds.** At the requested measured tip, the counter reported `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` and exited `0`; the selftest reported zero failures and exited `0`; the detached-tip recomputation exactly matched the committed C1 tally.

## Scratch artifacts and SHA-256

Hashes were produced by `sha256sum` at `2026-10-22T20:22:47Z` (exit code `0`):

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/counter.stdout.txt` — `11f451e77f91930c715943948220ac408686714821b6b41952f305c0fbc4e9b4`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/selftest.stdout.txt` — `db513ee5f8e16016a8b6e4b82d67a436a4bf51a6a89667348f30e6ae19929dfe`
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecRecountC1/emitted-tally.json` — `dc1eddf0a03f36c9e7eaa70fa8f63264aa05fa14e65428b5c6bee125cfa9b1da`
