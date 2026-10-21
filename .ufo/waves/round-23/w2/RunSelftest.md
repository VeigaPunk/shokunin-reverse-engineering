# RunSelftest — candidate counter `--selftest` at 2838351450ff1ee4baa620c962a1153450d53311

Seat: `KaidokuR23.RunSelftest` (designated Run seat). Scope: one execution of
`count-c1.py --selftest` against a private clone at the candidate, plus read-only
source checks of that same item. No other tests, builds, or linters were run.

## Findings

Labels: **observed** = seen in this run's bytes or output; **inferred** = derived from
source reading, not executed; **unknown** = not established.

### F1 — observed: the 21/21 assertion held on the single run

- argv: `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --selftest --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/RunSelftest/repo`
- cwd: private clone `runtime/RunSelftest/repo`, HEAD `2838351450ff1ee4baa620c962a1153450d53311`, `git status --porcelain` 0 lines before and after
- exit `0` (`selftest-exit.txt`); stderr 0 bytes; stdout 1 line, 36,424 bytes
- top-level: `finding: selftest_clean`, `passed: 21`, `total: 21`
- Started 2026-10-21T15:09:07Z, ended 15:10:07Z (about 60.6 s); Python 3.14.8, git 2.56.0

Every case matched its `expected-v2.json` tuple (exit, count, finding) exactly; each inner stderr was 0 bytes:

| case | exit | count | finding |
|---|---|---|---|
| positive | 1 | 2 | c1_incomplete |
| all_six | 0 | 6 | c1_complete |
| same_verb | 1 | 1 | c1_incomplete |
| mention_only | 1 | 1 | c1_incomplete |
| missing_source | 1 | 1 | c1_incomplete |
| old_source | 2 | null | unevaluable |
| wrong_usedby | 1 | 1 | c1_incomplete |
| refused_parent | 1 | 1 | c1_incomplete |
| nested_refusal | 1 | 1 | c1_incomplete |
| wrong_command | 1 | 1 | c1_incomplete |
| wrong_operation | 1 | 1 | c1_incomplete |
| duplicate_member | 1 | 1 | c1_incomplete |
| helper_tamper | 2 | null | unevaluable |
| invalid_utf8 | 2 | null | unevaluable |
| meta_false | 1 | 1 | c1_incomplete |
| meta_array | 1 | 1 | c1_incomplete |
| sibling_refusal | 1 | 1 | c1_incomplete |
| absolute_citation | 1 | 1 | c1_incomplete |
| historical_root_injection | 2 | null | unevaluable |
| inherited_lost | 2 | null | unevaluable |
| catalog_changed | 2 | null | unevaluable |

Per-case argv, stdout, stderr, and exit are all retained in `selftest-stdout.json`.

### F2 — observed: 3 of 4 identity digests are pinned; the counter under test is not

- Pre-run sha256 in the clone, all matching the candidate's own pins:
  - `counter-fixtures.py` `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`, pinned by `expected-v2.json` line 4 and checked in `count-c1.py` `selftest()` (:136–146)
  - `frozen/fixture.json` `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`, pinned by `expected-v2.json` line 5, same check
  - `frozen/expected-v2.json` `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`, pinned by `count-c1.py:25` `SELFTEST_MANIFEST_SHA256` and checked at `count-c1.py:139`
- **Not pinned:** `count-c1.py` itself, sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`. It is the counter under test and is executed as `Path(__file__).resolve()` (`count-c1.py:146`). All 21 inner runs used that same path (verified from each case's argv).
- Consequence (observed by reading): the selftest stdout does not record the counter's digest, so the 21/21 result binds to the executed bytes only through the commit and this report.

### F3 — inferred (source only, not executed): exit-code convention gap

- `count-c1.py:9` documents `2=could-not-evaluate`.
- `counter-fixtures.py:24–27` `command()` raises `RuntimeError` on any nonzero git exit during fixture setup.
- `count-c1.py:167` catches only `(OSError, ValueError, UnicodeError, RecursionError, KeyError)`. `RuntimeError` is not in that tuple, and nothing between `selftest()` (:136–146) and `main()` (:149–173) catches it.
- So a fixture-setup failure should escape as an uncaught exception. CPython then exits `1` with a traceback and empty stdout.
- Exit `1` is also the code for `selftest_failed` (`counter-fixtures.py:115–116`). A setup failure would be classed as "failed" instead of "could-not-evaluate". Only empty stdout distinguishes it.
- Not executed. No further run was authorized to confirm.

### F4 — observed (source): the oracle compares only exit, count, and finding

- `counter-fixtures.py:111–112`: `observed = {exit, count, finding}`; `passed = all(observed.get(k) == v for k, v in expected.items())`.
- Inner stdout, stderr, and argv are stored (:113–114) but never compared. The `error` payload of `unevaluable` results is never compared either.
- Inferred consequence: every `exit=2` case (old_source, helper_tamper, invalid_utf8, historical_root_injection, inherited_lost, catalog_changed) produces the identical triple `(2, null, unevaluable)` from any of the five exception types caught at `count-c1.py:167`. These cases do not prove which check fired. For example, `old_source` is meant to trigger `historical_sources_changed` in `measure()`, but any other caught `ValueError` or `KeyError` would also pass it.

### F5 — observed (source): `count: null` also matches an absent key

- `counter-fixtures.py:111` uses `out.get('t1_exercised_count')`, which returns `None` for both a JSON `null` and a missing key.
- The unevaluable payload (`count-c1.py:167–168`) has no count key, so `null` and absent cannot be told apart.

### F6 — observed: `mention_only` passed without any evidence file

- `counter-fixtures.py:43–44` selects no verbs. `:46` creates the `evidence/c1` directory unconditionally before any write. `:100` names that directory in `git add`.
- The commit succeeded and the case passed. The directory's existence comes from `:46`, not from pathspec matching. Git 2.56.0 accepted it in this run; other git versions were not checked.

### F7 — observed: contract caveat on the lane

- I ran `git status -sb | head -3` in the lane root during candidate checks. This was intended as read-only.
- Git may refresh the `.git/index` stat cache as a side effect. I did not compare index bytes before and after, so index immutability is unverified.
- I made no tracked-content, ref, or staging change. I did not modify the lane's pre-existing untracked entries (`wave2-dispatch.json` and the rest of `w2/`); the only file I added under `w2/` is this report.

### Attack log

| # | attack | result |
|---|---|---|
| A1 | pre-run identity pins vs code/manifest | 3/3 pinned digests match; counter unpinned (F2) |
| A2 | clone cleanliness and HEAD before run | 0 status lines; HEAD = candidate |
| A3 | single execution exit and stderr | exit 0; stderr 0 bytes |
| A4 | exact per-case (exit, count, finding) | 21/21 equal to expected |
| A5 | inner counter identity | all 21 inner argv use the clone's `count-c1.py`; inner stderr 0 bytes |
| A6 | exception path and oracle strength | source only: F3, F4, F5 |
| A7 | post-run residue | nested fixture clones reaped; only an empty `runtime/` dir remained; clone removed (`test ! -e` true) |

Nested fixture clones were created under the private clone's ignored `runtime/fixture-*` directory (`counter-fixtures.py:20–22`). They were reaped by `TemporaryDirectory`.

## Produced files and hashes

All in `.ufo/waves/round-23/runtime/RunSelftest/` (lane-ignored runtime dir; `.ufo/waves/round-23/.gitignore` line 1 `/runtime/`):

| file | sha256 | note |
|---|---|---|
| `selftest-stdout.json` | `811a728b9d6633ddd7af2023b2709d17d009911f122cce8efd3a37a07d0b72bd` | 1 line, 36,424 bytes |
| `selftest-stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 bytes |
| `selftest-exit.txt` | `19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061` | `exit=0` |
| `run-meta.txt` | `d0c7cf87205b5341b2d69e9d5e9a7204ad17816166cf70790fe965ae47962eab` | START/ARGV/CWD/END, python and git versions |

The private clone `runtime/RunSelftest/repo/` was removed per contract. This report
(`w2/RunSelftest.md`) is the only file written under `w2/`.

## Installs

None. Pacman was paused and no tool was needed or installed.

## Open risks

- **Observed:** the 21/21 assertion held once. It is not established as deterministic. Only one execution was authorized, so flakiness is unknown.
- **Inferred, not executed (F3):** a setup `RuntimeError` probably exits `1` with empty stdout. That collides with `selftest_failed` and violates the documented `2=could-not-evaluate`.
- **Observed by reading (F4, F5):** the oracle checks only three keys, so right-triple/wrong-reason passes are possible, and `null` and absent count are indistinguishable.
- **Observed by reading (F2):** the counter's own digest is not pinned by the manifest or recorded in selftest output.
- **Unknown (F6):** the empty-directory `git add` behavior was observed on git 2.56.0 only.
- **Unknown (F7):** whether the lane `git status` call rewrote `.git/index` stat data.
