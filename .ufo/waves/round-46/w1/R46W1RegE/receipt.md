# R46W1RegE receipt — three registry rows, round-46 C2 census (tag `reg-e`)

Rows delivered: `rows.md`, sha256 `8355f2a8f873c98ab369b065149a321f29971daade6fd7398801ffdee63b95f0`.

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, freeze
`31820472784284727546808acc31b3ea1e73919b`, measured at that same commit (nothing
after it is read). Machine-readable companion: `evidence/receipt.tsv`
(sha256 `6bbbd43b3ccbe8d8c0ff882b4d0d37661b2024c067f7e2492381f68a5b1c1a31`, 14 lines: the driver's 13 plus one rerun line), one
line per command: name, exit code, sha256 of captured combined stdout+stderr,
t0, t1 (UTC), command. Captured output for every command is in `evidence/out.*.txt`.

## Commands actually run

| # | command (cwd = lane) | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| 1 | `git -C LANE cat-file -e 31820472784284727546808acc31b3ea1e73919b:tools/round-41/c2-counter.py` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty stdin) | 2026-10-28T16:56:44Z |
| 2 | same for `tools/round-42/fetch-carrier.py` | 0 | e3b0c442…b855 | 2026-10-28T16:56:44Z |
| 3 | same for `tools/round-44/c2-counter.py` | 0 | e3b0c442…b855 | 2026-10-28T16:56:44Z |
| 4 | `python3 -I -B tools/round-41/c2-counter.py --selftest` | 0 | f3db407a7763381d5a7b16c7c2ef5361b90a036f94c5855cc9cb301e00bb29a6 | 16:56:44Z→16:58:12Z |
| 5 | `python3 -I -B tools/round-42/fetch-carrier.py --selftest` | 0 | e92198797789c841aae65cf64772fac1eb0897af36d9a4f4e332072228c33c99 | 2026-10-28T16:58:12Z |
| 6 | `python3 -I -B tools/round-44/c2-counter.py --selftest` | 0 | a5e942a1efa3172ba522a2174c68f62f80b01c009f9495027d4bbfde7558fbc3 | 2026-10-28T16:58:12Z→16:58:15Z |
| 7 | `python3 -I -B tools/round-42/fetch-carrier.py --spec …/probe/spec.json --cache …/probe/cache --work …/probe` (image_sha256 pinned to 64 zeros) | 1 | 98003af115b3a7f9cf80572945241b2ef485a6e41017b7119a69b9981763e2bd | 2026-10-28T16:58:15Z |
| 8 | `python3 -I -B tools/round-42/fetch-carrier.py --cache …/probe/cache` (no `--spec`, no `--root/--rev`) | 2 | b0666e0f38ef093b1e5706fedc22e7d063df9ade5424cdea6077e4abc778e624 | 2026-10-28T16:58:15Z |
| 9 | `python3 -I -B tools/round-41/c2-counter.py --root /nonexistent` (no `--rev`/`--freeze`) | 2 | 5b4ad767fd08477938e5708c21e02d2473caddfa73ebb98a45eba737e92994b8 | 2026-10-28T16:58:15Z |
| 10 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev HEAD` (no `--freeze`, no `--pre-freeze`) | 2 | d1e2dab0a5cdd982a1bcc3077226f468ccb470d0496c0186c6437d7450892729 | 2026-10-28T16:58:15Z |
| 11 | `python3 -I -B tools/round-44/c2-counter.py --schema` | 0 | b12cb81b354e0f53d6306b0203721a2820bc2d2600c9e86143e632f7d7e3cee7 | 2026-10-28T16:58:15Z |
| 12 | `python3 -I -B check_rows.py` (frozen `registry.py` `score()`, rows.md as input; `evidence/check_rows.py`) | 0 | 631c915c80116b4880f2b8280cf48ce7c4448683ff43b4a372858394d8d7d71f | 16:58:15Z and 16:59:15Z (rerun after tightening two verdict cells; identical stdout) |
| 13 | `git -C LANE show <freeze>:tools/round-46/census.json` + membership probe | 0 | e62b3e34994c4fe3e4ecf95a8bfc2e0ab59796d36beb65a9bc770c0ddca70ee4 | 2026-10-28T16:58:15Z |

Selftest results (stdout, verbatim first/last line):

- #4 `{"selftest": "c2-counter r41 (v3)", "cases": 70, "green": 20, "red": 50, "pass": 70, "fail": 0, "failures": []}` / `SELFTEST cases=70 pass=70 fail=0`
- #5 `SELFTEST cases=36 pass=36 fail=0`
- #6 `{"selftest": "P44-C2", "ok": true, "arms": [24 arms]}`

Commands #4–#6 were each run twice (once interactively, once inside the receipt
driver) and produced the same stdout sha256 both times.

## Where each verdict map comes from (source at the freeze, read not guessed)

**`tools/round-41/c2-counter.py`** — module docstring `Exit` block (lines 54–60) and
`main()` (1605–1652): `return selftest()` (0/1), `return 2` on missing `--root/--rev/--freeze`
(usage), `Unevaluable` → receipt with `exit_code: 2` and `return 2`, otherwise
`return res['exit_code']` where `res['exit_code'] = 0 if met else 1` (line 1598). Belief
"receipt still written" on exit 1: `main()` prints and writes `--json-out` before
returning `res['exit_code']`. The exit-2 reason set is enumerated in the docstring
(`frozen_path_changed`, `freeze_not_ancestor_of_rev`, `unknown_revision`,
`no_manifest_at_rev`, `generator_absent_at_freeze`, … `met_target_inconsistent`).

**`tools/round-42/fetch-carrier.py`** — docstring `Exit:` line (72–73) and `main()`
(897–934): `return selftest()` (0/1); `return 2` for `not a.cache or not (a.spec or
(a.root and a.rev))`; `ChainError` from `load_spec`/`workdir`/`_check_path` → `return 2`;
`recs, rc = run(...)` and `return rc`. `run()` (531–549) ends
`ok = managed > 0 and all(r['ok'] …); return recs, (0 if ok else 1)` — so exit 0
requires **at least one** managed carrier, which is why the row says so explicitly.
`--repo-spec` defaults to `REPO_SPEC = '.ufo/waves/round-42/c1/carriers.json'` (line 90).

**`tools/round-44/c2-counter.py`** — docstring `Exit codes:` line and `score()`'s
`code = EXIT_MET if (not mismatches and not unevaluable and (not
frozen_path_changed or pre_freeze) and entries_evaluated > 0) else (EXIT_FAIL if
mismatches and not unevaluable else EXIT_CANT)` (1302–1307), with `EXIT_MET = 0`,
`EXIT_FAIL = 1`, `EXIT_CANT = 2` (123–125). `--schema` prints `__doc__` and returns
`EXIT_MET` (#11). The pin is `tools/round-44/c2-rubric.json` plus the counter's own
sha256 at the freeze; `claim_gate.usable_as_claim_score` is true only when
`counter_sha256_at_freeze` and `rubric_sha256_at_freeze` are both set.

## Exit codes outside {0, 1, 2}: none

AST scan of each frozen file, skipping string literals (so the embedded fixture
stubs do not count): the only literal exits in the three tools' own code are
`return 0`, `return 2`, `EXIT_MET/FAIL/CANT = 0/1/2`, and `sys.exit(main())`.
The `sys.exit(3)` / `sys.exit(9)` / `sys.exit(1)` occurrences inside
`round-41/c2-counter.py` sit in the `STUB_EVAL` / `STUB_INTERP` fixture templates
(strings the counter writes as *test subjects*), not in the counter's control flow.
Argparse contributes `--help` → 0 and a bad option → 2, both inside the set.

## Rows scored by the frozen checker itself (not by my own regexes)

`evidence/check_rows.py` copies `tools/round-46/registry.py` and `gate.py` **from the
freeze** into scratch, imports `registry`, and calls `registry.score()` with an
in-memory `files()` (no repo, no lane write). Results (`evidence/out.check_rows.txt`):

| case | input | exit | `unregistered` | `thin` | verdict |
|---|---|---|---|---|---|
| A | my three rows, census = those three paths | 0 | [] | [] | `met_target: true`, `header_ok: true` |
| B2 | the six **landed** round-45 rows alone | 1 | [] | all six | every landed row is thin |
| B3 | the six landed rows under their **landed** header | 1 | — | six | also `header != house schema` (cell 2 is `gate or probe`, house is `gate or probe - purpose`) |
| C | my row 1 reworded as the landed rows word it (`` `0` met; `1` not met; `2` could-not-evaluate ``) | 1 | [] | that one path | backticked digits without `=` bind nothing |
| D | my row 1 with cell 0 = `see \`path\` (wrapper)` | 1 | that one path | [] | substring is not registration |

Case B2 is the finding the L1 needs: the six existing rows in
`### Round-44/45 instrument registry` are all thin under clause 4 and their header is
not the house header, so landing round-46 C2 means **rewording all six** rows as well
as adding the census rows.

Row-shape checks my script also asserts on `rows.md`: 3 rows, 7 cells each, cell 0
exactly one backticked path (`tools/round-41/c2-counter.py`,
`tools/round-42/fetch-carrier.py`, `tools/round-44/c2-counter.py`), exactly two
backticks per line (none outside cell 0), no literal `|` inside a cell,
`shape_violations: []`.

## Census membership at the freeze

`tools/round-46/census.json`@freeze has `scope_size 38`, `named_but_absent 0`, and all
three assigned paths are members (`evidence/out.census.members.txt`).

## Scope discipline

No write outside `.ufo/waves/round-46/w1/R46W1RegE/` and
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegE` (removed at exit). No git/jj mutation;
only `show`, `cat-file -e`. No installs (nothing needed beyond python3 and git already
on the host).
