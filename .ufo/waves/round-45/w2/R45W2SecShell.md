# R45W2SecShell — command injection and write scope (trailer)

Full report with commands, diffs and per-finding remediation:
`.ufo/waves/round-45/w2/R45W2SecShell/report.md`; receipts in
`.ufo/waves/round-45/w2/R45W2SecShell/receipts/` (exact command, exit code, stdout sha256,
UTC for each).

Surface: `tools/round-45/{frozen-path-preflight.py,c1-counter.py,c2-counter.py}` at
freeze `f762b72` / A1 `1f4b27f`. Every mutation ran on a `git clone --no-hardlinks` copy
under `/fast/scratch/hyaku/kaidoku-r45/R45W2SecShell` (toplevel asserted; scratch removed
after copying receipts). No lane write, no git mutation in the lane, no install. Frozen
paths verified byte-identical to `HEAD` before and after.

## Verdicts

| # | attack | verdict |
|---|---|---|
| A1 | `shell=True` / string argv | **holds** — four `subprocess.run` sites, all list argv, no shell |
| A2 | argv from file content or claim strings | **holds** — hash-prefixed args; citation regex admits no `/`, space, backtick, `$`; five metachar filenames reported literally, no `PWNED*` |
| A3 | hook execution from repo config in the dirty arm | **not run** — fixture and direct git 2.56 both failed to run the hook; unresolved, no execution observed |
| B1 | `--json-out ../../SKILL.md` | **falsified, 3/3** — c1/c2/preflight all overwrite the graded surface and exit 0 |
| B2 | `--json-out` onto a frozen path | **falsified** — `plans/round-45-claims.md` at exit 0; `tools/round-45/registry-scope.json` at exit 2 |
| B3 | `--json-out` through a symlink | **falsified** — followed |
| B4 | unwritable `--json-out` | **falsified** — exit 1, empty stdout, no receipt (should be 2) |
| C1 | `HYAKU_SCRATCH=<repo>` | **falsified** — 662 planted paths, 11 nested `.git` repos, exit 0 |
| C2 | `TMPDIR=<repo>` alone | **falsified** — identical |
| C3 | relative `HYAKU_SCRATCH` | **falsified** — resolved against CWD (the fleet root, for a seat) |
| C4 | `GIT_DIR=<repo>/.git` | **falsified, HIGH** — fixture commits land in the named repo, HEAD moved, tip tree replaced, local config overwritten, exit 0 with `failures=0` (3/3 tools) |
| C5 | `GIT_INDEX_FILE=<repo>/.git/index` | **falsified, HIGH** — the *scoring* run of c1 reports `met_target: True` while rewriting the graded repo's index; `git status` afterwards is `fatal: unable to read …` |
| C6 | "never a bare /tmp root" (`preflight:26`) | **not run** — would write `/tmp`; both env vars are unset on this host, so `gettempdir()` → `/tmp` by code |
| C7 | registry `write scope` cells (`SKILL.md:1655-1657`) | **falsified** — `--json-out` is unbounded and the fixtures also write wherever the `GIT_*` vars point, including `.git` |

Counts unaffected: clean env at A1, c1 → `met_target true`, rows 10, refs 7, selftest 11/0;
c2 → `unregistered []`, `thin []`, both exit 0.

## Record consequences for the L1

1. The preflight dogfoods the M44-2 failure: with `HYAKU_SCRATCH` (or `TMPDIR`) pointing at
   a working tree it plants eleven nested git repos there; with `GIT_DIR` it commits into
   that tree and moves its branch tip — always at exit 0.
2. R45-C1 clause 6 is not a read-only witness: `--selftest` green coexists with a corrupted
   graded index, and `--json-out` can truncate `SKILL.md` or a frozen file with no error.
   Fix by scrubbing the `GIT_*` prefix, asserting `rev-parse --show-toplevel == d` per
   fixture, and validating `--json-out` (realpath + `O_NOFOLLOW` + print-then-write +
   `OSError → 2`).
3. Proposed routings: **R45-CL18** (HIGH, `GIT_*` unsanitised), **R45-CL19** (MEDIUM,
   `--json-out` unvalidated incl. exit-2 write and `OSError → 1`), **R45-CL20** (MEDIUM,
   scratch base unvalidated + no cleanup), **R45-CL21** (LOW, the `/tmp` claim).
