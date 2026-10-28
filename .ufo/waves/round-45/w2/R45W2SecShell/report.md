# R45W2SecShell — command injection and write scope in the three round-45 instruments

Seat: `R45W2SecShell` (sentinel, wave 2). Read-only on the lane and the fleet repo: every
mutation below happened under `S=/fast/scratch/hyaku/kaidoku-r45/R45W2SecShell`, on copies.

Measured against freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` and amendment A1
`1f4b27f82353d6544dc0c8048b3cfdadd8525d12` (the measured revision).

```sh
git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
git -C "$S/clone" checkout -q 1f4b27f82353d6544dc0c8048b3cfdadd8525d12
git -C "$S/clone" rev-parse --show-toplevel   # -> $S/clone (asserted before any commit)
```

The three tool files in the clone are byte-identical to the lane's working tree
(`cmp` for each of `c1-counter.py`, `c2-counter.py`, `frozen-path-preflight.py`);
`git -C <lane> diff --stat f762b72 1f4b27f -- tools/round-45 plans/round-45-claims.md` is
empty, and each frozen file's worktree sha256 equals its `HEAD` blob. Nothing was written
to the lane, `plans/`, `tools/`, `corpus/`, `LOG.md` or `SCORECARD.md`; no git mutation was
run in the lane; no install was needed or made (python3 3.14.8, git 2.56.0 present).

## Verdicts

| # | attack | surface | verdict |
|---|---|---|---|
| A1 | `shell=True`, `os.system`, string argv | all three | **holds** — no shell anywhere; four `subprocess.run` sites, all list argv |
| A2 | argv built from file content or a claim string | preflight `ls-tree` paths, c1 citations, c2 scope | **holds** — no token can start with `-`, no shell metachar reaches a shell |
| A3 | repo-config hook execution inside the dirty arm's `git status` | preflight `evaluate` | **not run** — fixture could not induce execution; git itself did not run the hook |
| B1 | `--json-out ../../SKILL.md` overwrites the graded surface | all three | **falsified** — 3/3 write, 3/3 exit 0 |
| B2 | `--json-out` onto a frozen path (claims / `registry-scope.json`) | c2, preflight | **falsified** — written, incl. at exit 2 |
| B3 | `--json-out` through a symlink | c1 | **falsified** — symlink followed |
| B4 | unwritable `--json-out` | c1, preflight | **falsified** — exit 1 with empty stdout, no receipt (contract says 2) |
| C1 | `HYAKU_SCRATCH=<lane>` redirects the selftest into the tree | preflight, c1, c2 | **falsified** — 662 paths and 11 nested `.git` repos planted, exit 0 |
| C2 | `TMPDIR=<lane>` alone | preflight | **falsified** — identical effect |
| C3 | relative `HYAKU_SCRATCH` | c1 | **falsified** — resolved against CWD |
| C4 | `GIT_DIR=<repo>/.git` redirects the fixture commits | all three | **falsified, HIGH** — commits land in the named repo, exit 0 |
| C5 | `GIT_INDEX_FILE=<repo>/.git/index` | all three; the *scoring* run of c1 | **falsified, HIGH** — index rewritten, `met_target: True` |
| C6 | "never a bare /tmp root" (preflight docstring `:26`) | preflight | **not run** — would write `/tmp`; code path and host env stated below |
| C7 | registry `write scope` cell for the round-45 rows | `SKILL.md:1655-1657` | **falsified** — both halves of the cell are wrong |

Counts are unaffected: in a clean env at A1, `c1` exits 0 with `met_target true`,
`rule_blocks`/`block22_rows` 10, `block22_refs` 7, selftest 11/0; `c2` exits 0 with
`unregistered []`, `thin []` (`receipts/base.receipt.txt`). This seat attacks the
instruments' *write-scope and execution* claims, not the two predicate values.

---

## Falsified 1 — `--json-out` is an unvalidated write (B1–B4)

Code: `frozen-path-preflight.py:158-161` (`emit`), `c1-counter.py:358-360`,
`c2-counter.py:260-262`. All three do `open(path, "w")` on the raw argument: no root
check, no `O_NOFOLLOW`, no temp-and-rename, no `realpath`. The write happens **after**
`evaluate()`, so it fires on exit 2 as well; in preflight and c1 it happens **before** the
receipt is printed, so a write failure suppresses stdout entirely.

Exact input and observation (cwd `= clone/tools/round-45`):

| case | command tail | exit | graded surface |
|---|---|---|---|
| B1 | `c1-counter.py … --json-out ../../SKILL.md` | 0 | `SKILL.md` `19c20927…` → `da9d99b4…` |
| B2 | `c2-counter.py … --json-out ../../SKILL.md` | 0 | `19c20927…` → `0daf63d3…` |
| B3 | `frozen-path-preflight.py … --json-out ../../SKILL.md` | 0 | `19c20927…` → `58aee105…` |

After B1 the file is 529 bytes of receipt JSON; `grep -c 'Queue-drain craft' SKILL.md` = 0
(saved as `receipts/B1b-clobbered-SKILL.md`). The resolvent is plain relative traversal —
`clone/tools/round-45/../../SKILL.md` — not an exotic path.

Frozen paths are equally reachable:

- **B4** `c2-counter.py … --json-out plans/round-45-claims.md` (cwd = clone root): exit 0,
  `plans/round-45-claims.md` `56bacf31…` → `0daf63d3…`, `git status` shows ` M`.
- **B8** `frozen-path-preflight.py --freeze-path tools/round-45 --require-pathspec
  --json-out tools/round-45/registry-scope.json`: exit **2** (`pathspec_required`), stdout
  is the correct could-not-evaluate receipt, **and** the frozen scope file is rewritten
  `6e2dda71…` → `eeb9d88b…`. A non-evaluable run still destroys a frozen path.
- **B9** `ln -sf clone2/SKILL.md $S/linkout.json` then `--json-out $S/linkout.json`: exit 0,
  target sha changed — the `open(..., "w")` follows the link.
- **B6/B7** `--json-out <directory>` and `--json-out /proc/nonexistent/x.json`:
  `IsADirectoryError` / `FileNotFoundError` uncaught → **exit 1**, 0 bytes stdout, no
  receipt. Exit 1 is the registered "not met" code, so a pure write failure reads as a
  claim failure. (Same class the round-35 registry rows already record as "an uncaught
  exception exits 1, so a crash reads as failed".)

Exploit path: any caller that forwards a path — a seat writing its own receipt, a wave
script templating "put the json wherever", a `--json-out` taken from a sibling artifact —
truncates the graded surface or a frozen file with no error and no receipt. The counters
themselves read `git show rev:path`, so a worktree overwrite does not immediately change a
score; the next lane-wide `git add -A` commits it, which is either a freeze violation
manufactured by the gate or, for `SKILL.md`, deletion of the graded surface.

Impact: graded-surface loss; frozen-path corruption makes both counters exit 2
`frozen_path_changed` permanently; the exit-1-on-OSError path silently converts
"could not write" into "claim not met".

Smallest remediation:
1. `realpath` the argument, refuse unless it lies under an explicit `--out-root`
   (default CWD) and is not a tracked/frozen path at `--rev`;
2. open with `os.open(..., os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW)` and `os.replace` from a
   temp file in the same directory (kills the symlink follow and the partial write);
3. print the receipt **before** writing, so a failed write cannot swallow it;
4. `except OSError as exc → return 2` with `{"reason": f"json_out: {exc}"}`.

## Falsified 2 — `HYAKU_SCRATCH`/`TMPDIR` redirect the fixtures into any tree (C1–C3)

Code: `frozen-path-preflight.py:50-58` (`scratch_root`), `c1-counter.py:45-48`,
`c2-counter.py:174-176` — `os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR") or
tempfile.gettempdir()`, joined without any validation of absolute-ness or of whether the
base is inside a git worktree. `preflight:168-171` (`_commit`) then runs `git add -A` and
`git commit` in each fixture with no `rev-parse --show-toplevel` assertion.

```sh
(cd "$S" && env HYAKU_SCRATCH="$C" python3 -I -B "$C/tools/round-45/frozen-path-preflight.py" --selftest)
# exit 0, "PREFLIGHT_SELFTEST: cases=11 failures=0"
```

Observed in the scratch clone `$C`: `git -C $C status --porcelain` → `?? kaidoku-r45/`;
`find $C/kaidoku-r45 | wc -l` → **662**; `find $C/kaidoku-r45 -name .git | wc -l` → **11**.
Eleven untracked git repositories with committed fixtures were planted inside the tree the
gate is meant to protect — the M44-2 shape (`corpus/lessons/round-44.md:18,63`) produced by
the M44-2 fix itself, at exit 0.

- **C2** `env -u HYAKU_SCRATCH TMPDIR="$C" … --selftest`: same 662/11, exit 0. `TMPDIR`
  alone is sufficient; the variable is not a fallback in practice, it is a selector.
- **C1 (c1/c2)** both create and leave `<base>/kaidoku-r45/` (1 path, empty) — invisible to
  `git status` but still a filesystem write into the named tree.
- **C3** `env HYAKU_SCRATCH=rel … --selftest` with cwd `= $C`: creates `$C/rel/kaidoku-r45/`.
  A relative value is not rejected, so the target is the caller's CWD — for every seat in
  this wave the host guard puts that CWD at the fleet root, i.e. one level above the lane.

Impact: untracked nested repos planted where a lane-wide `git add -A` (the exact M44-2
sweep) would commit them; and the dirty arm cannot see them when invoked with this round's
`--pathspec tools/round-45/`, because the plant lands at the repo root.

Smallest remediation: require `os.path.isabs`; reject a base for which
`git -C base rev-parse --show-toplevel` succeeds (it is inside a worktree); `mkdtemp` the
fixture dir and `rmtree` it in `finally` (preflight removes nothing today); in `_commit`,
assert `git -C d rev-parse --show-toplevel == realpath(d)` before `add`/`commit` and turn a
mismatch into a **failed case**, not a pass.

## Falsified 3 — `GIT_DIR` makes the fixture commits land in the named repo (C4) — HIGH

`git -C <dir>` does not override `$GIT_DIR`; the fixture `git init`/`add -A`/`commit` in
`preflight:168-171`, `c1-counter.py:186-203` and `c2-counter.py:149-166` therefore operate
on whatever repository the environment names.

```sh
(cd "$S" && env HYAKU_SCRATCH="$S/c5scratch" GIT_DIR="$C/.git" \
   python3 -I -B "$C/tools/round-45/frozen-path-preflight.py" --selftest)
# exit 0 ; PREFLIGHT_SELFTEST: cases=11 failures=0
```

Observed on the scratch clone (receipt `C5.receipt.txt`):

- `HEAD` `1f4b27f8` → `45f6aa90`; new log `45f6aa90 freeze`, `dc6d0ad7 sweep`,
  `0c28eec0 freeze`, `a59321fd later` — 463 commits now reachable;
- the branch **tip tree** is `frozen/a.txt`, `frozen/b.txt`, `other.txt`: the repository's
  entire content is now untracked and the previous history is no longer on the branch;
- `git config --local user.email` = `preflight@selftest` — the repo's config is overwritten;
- `plans/round-45-claims.md` in that repo now differs from `HEAD`.

c1 and c2 reproduce it (`E-c1-counter.py.receipt.txt`, `E-c2-counter.py.receipt.txt`), each
with a green selftest:

| tool | exit | selftest line | HEAD | local `user.email` | tip tree |
|---|---|---|---|---|---|
| preflight | 0 | `cases=11 failures=0` | `1f4b27f8`→`45f6aa90` | `preflight@selftest` | `frozen/a.txt frozen/b.txt other.txt` |
| c1 | 0 | `cases=9 failures=0` | `1f4b27f8`→`95b7fba0` | `c1@selftest` | `SKILL.md … plans/round-45-claims.md tools/round-45/frozen-path-preflight.py` |
| c2 | 0 | `cases=7 failures=0` | `1f4b27f8`→`b939f8f7` | `c2@selftest` | `SKILL.md plans/round-45-claims.md tools/round-45/registry-scope.json` |

Exploit path: any wrapper that exports `GIT_DIR` (or a caller whose shell already has it)
and then runs a tool's `--selftest` — including the L1's scoring run, because
`c1-counter.py:104-105` builds the child environment as `dict(os.environ, …)` and pops
**only** `GIT_DIR` (so a `GIT_DIR` in the parent is removed from the child but the parent's
own fixtures still run under it). The class is also reachable by a hostile `--rev`: the
counter executes the interpreter bytes it finds at `--rev` and would report clause 6 green.

Impact: the gate destroys the repository it is asked to protect and prints `failures=0`.
In the lane this is strictly worse than M44-2: a foreign sweep that also moves the branch
tip and rewrites the local config, leaving `plans/round-45-claims.md` differing from `HEAD`
so the next `git add -A` commits a fixture tree over the claim.

Smallest remediation: at process start **and** in the child env, drop the whole prefix —
`for k in [k for k in os.environ if k.startswith("GIT_")]: os.environ.pop(k)` — and add the
`rev-parse --show-toplevel == realpath(d)` assertion per case (cheap, and it converts this
class into a red case instead of a silent pass).

## Falsified 4 — `GIT_INDEX_FILE` rewrites the index; the *scoring* run still reports `met_target` (C5) — HIGH

```sh
(cd "$C" && env HYAKU_SCRATCH="$S/score-scratch" GIT_INDEX_FILE="$C/.git/index" \
   python3 -I -B tools/round-45/c1-counter.py --root "$C" \
     --freeze f762b72… --rev 1f4b27f… --json-out "$S/score-c1.json")
```

Receipt `E-score.receipt.txt`: exit **0**, `met_target: True`, `failing: []`, and

- `$C/.git/index` `a322d0bb…` → `eaede2e2…`;
- afterwards `git -C $C status --porcelain` prints
  `fatal: unable to read e45c9c2666d44e0327c1f9c239a74c508336053e` — the index now points at
  objects that exist only in the fixture.

`E-index.receipt.txt` (`c1 --selftest`) and `E-pre-idx.receipt.txt` (`preflight --selftest`,
i.e. the exact bytes the counter's child executes) show the same index mutation; the c1
case additionally stages the whole tree as deleted (`D  .gitignore`, `D  .ufo/…`).

Exploit path: `c1-counter.py:104-107` hands the child `dict(os.environ, TMPDIR=work,
HYAKU_SCRATCH=work)` and pops only `GIT_DIR`, so `GIT_INDEX_FILE`, `GIT_WORK_TREE`,
`GIT_OBJECT_DIRECTORY` and `GIT_COMMON_DIR` all reach the interpreter that writes fixtures.

Impact: this is a soundness problem for the R45-C1 pass, not just hygiene. A green
`met_target: True` coexists with a repository whose index is unusable; the next
`git add && git commit` (any author) stages the deletion of every tracked file. The claim's
clause 6 ("`--selftest` exit 0, cases ≥ 11, failures 0") is satisfied by exactly this run.

Smallest remediation: the `GIT_*` scrub above; plus one assertion in `run_preflight`: record
`git rev-parse --verify` of the index blob (or `sha256` of `.git/index`) before and after
the child and fail the clause if it moved.

## Held — no injection (A1, A2)

- **A1** `grep -n 'shell=True\|os.system\|os.popen\|subprocess\.\(call\|Popen\|check_output\)\|eval(\|exec(' *.py`
  → no match. The only subprocess sites are `frozen-path-preflight.py:47`,
  `c1-counter.py:37`, `c1-counter.py:106`, `c2-counter.py:35`; all pass argv lists, and the
  child is `[sys.executable, "-I", "-B", path, "--selftest"]`. No string-typed command
  exists to inject into.
- **A2** every element that comes from file content always carries a resolved-hash prefix:
  `git rev-parse f"{base}:{path}"` (path from `ls-tree --name-only`), `git cat-file -e
  f"{rev}:{name}"` (name from a `SKILL.md` citation), `git show f"{rev}:{path}"`. Such an
  argument can never be parsed as an option, and no shell exists to expand it.
  Empirical (receipt `A2-names.receipt.txt`): a fixture committing
  `frozen/$(touch PWNED1).txt`, `frozen/; touch PWNED2 ;.txt`, `frozen/-n.txt`,
  `frozen/--upload-pack=sh -c id.txt` and ``frozen/`id`.txt`` yields exit 1 with all five
  in `touched[]` by exact path, and **no** `PWNED*` file anywhere.
  The citation regex is the only content-derived name source and admits no `/`, space,
  backtick or `$` after its fixed prefixes (inline probe over the tool's own `REF`
  pattern; the twelve probe strings and their matches are quoted here):
  `plans/../../SKILL.md:1`, `corpus/lessons/../../../etc/passwd.md:1`,
  `plans/--output=/tmp/x.md:1` and ``plans/`id`.md:1`` all match nothing;
  `plans/-c.md:1` matches but the argv is `<rev>:plans/-c.md`.
  Claim/scope strings never reach argv at all: `CLAIMS` (`c1:33`) and `SCOPE` (`c2:30`) are
  constants, and c2's scope entries are used only as dictionary keys (`c2:92-100`).

## Not run

- **Repo-config hook execution (A3).** Fixture `$S/fx-fsmon` with `core.fsmonitor=true` and
  an executable `.git/hooks/fsmonitor-watchman` writing a marker; `preflight --check-dirty`
  exited 1 with the marker **absent**, and the control `git -C $S/fx-fsmon status` did not
  execute the hook either on git 2.56. The fixture therefore cannot distinguish tool
  behaviour from git behaviour: unresolved, no execution observed. (`A-fsmon*.txt`).
- **`/tmp` fallback (C6).** With `HYAKU_SCRATCH` and `TMPDIR` both unset — the host's actual
  state, verified with `printenv` — `scratch_root()`/`scratch_dir()` fall through to
  `tempfile.gettempdir()` and the fixture path becomes `/tmp/kaidoku-r45/…`. I did not
  execute it: my contract forbids writing under `/tmp`. The docstring sentence
  "never a bare /tmp root" (`preflight:26`) is therefore a statement about the caller's
  environment, not about the tool.

## Record the L1 must reconcile

1. `SKILL.md:1655` (registry row, `tools/round-45/frozen-path-preflight.py`) writes
   `write scope`: "`--json-out` only; selftest fixtures under `$HYAKU_SCRATCH` or
   `$TMPDIR`". Both halves are falsified: `--json-out` is unbounded (B1/B4/B8/B9), and the
   fixtures also write wherever `GIT_DIR`/`GIT_INDEX_FILE` row (C4/C5) — including the
   graded repository's `.git`. The c1 row's "scratch under `$HYAKU_SCRATCH` or `$TMPDIR`"
   (`SKILL.md:1657`) has the same defect.
2. `frozen-path-preflight.py:22-27` "The gate is read-only." and `c1-counter.py:18-19`
   "Reads Git objects only" are false for `--selftest`, and for c1 also for the plain
   scoring command (E-score).
3. R45-C1 clause 6 is not a read-only witness: a `--selftest` that reports `cases=11
   failures=0` can leave the graded repo's index pointing at foreign blobs. Either add a
   write-scope arm (a case that plants `GIT_DIR`/`GIT_INDEX_FILE`/`HYAKU_SCRATCH` and
   asserts the named repo is byte-unchanged) or state the limit in block 22 beside the
   existing arm-isolation limit.

Proposed routings:

- **R45-CL18 (HIGH)** — `GIT_DIR`/`GIT_INDEX_FILE`/`GIT_WORK_TREE` unsanitised: `--selftest`
  commits into and rewrites the named repo, exit 0, in all three tools (C4/C5).
- **R45-CL19 (MEDIUM)** — `--json-out` unvalidated: relative traversal over the graded
  surface, frozen-path overwrite (also at exit 2), symlink follow, and `OSError` → exit 1
  with no receipt (B1–B9).
- **R45-CL20 (MEDIUM)** — `HYAKU_SCRATCH`/`TMPDIR` accept a relative value and a base inside
  a git worktree: 662 planted paths and 11 nested `.git` repos, exit 0; preflight removes
  none of its case dirs (C1–C3).
- **R45-CL21 (LOW)** — "never a bare /tmp root" (`preflight:26`) holds only when the caller
  sets a variable (C6).

Cheapest fix order: scrub `GIT_*` (one line per tool, plus the child env) → toplevel
assertion inside `_commit`/`make_repo` (three lines) → `--json-out` realpath + `O_NOFOLLOW` +
print-then-write + `OSError → 2` (about five lines) → scratch-base validation and cleanup.

## Receipts

All under `.ufo/waves/round-45/w2/R45W2SecShell/receipts/`; each `.txt` carries the exact
command, exit code, stdout sha256 and UTC. `$S` was removed after copying.

| file | what it shows |
|---|---|
| `base.receipt.txt` | clean-env A1 baseline: c1/c2 `met_target true`, selftest 11/0, repo clean |
| `B1..B3.receipt.txt` | `--json-out ../../SKILL.md` for c1/c2/preflight: exit 0, SKILL.md sha changed |
| `B1b-clobbered-SKILL.md` | the 529-byte receipt JSON that replaced the graded surface |
| `B4.receipt.txt` | c2 rewrites the frozen `plans/round-45-claims.md`, exit 0 |
| `B5.receipt.txt` | c1 exit 2 `unknown rev` still overwrites SKILL.md |
| `B6/B7.receipt.txt` | unwritable `--json-out` → exit 1, 0-byte stdout, traceback |
| `B8.receipt.txt` | preflight exit 2 `pathspec_required` still rewrites a frozen file |
| `B9.receipt.txt` | `--json-out` follows a symlink to SKILL.md |
| `C-frozen-path-preflight.py.receipt.txt` | 662 planted paths, 11 nested `.git`, exit 0 |
| `C-tmpdir.receipt.txt` | same with `TMPDIR` only |
| `C-c1-counter.py.receipt.txt`, `C-c2-counter.py.receipt.txt` | parent `kaidoku-r45/` left behind |
| `C4.receipt.txt` | relative `HYAKU_SCRATCH` resolved against CWD |
| `C5.receipt.txt` | `GIT_DIR`: HEAD moved, tip tree is the fixture, config rewritten, exit 0 |
| `E-c1-counter.py.receipt.txt`, `E-c2-counter.py.receipt.txt` | same for c1 and c2 |
| `E-index.receipt.txt`, `E-pre-idx.receipt.txt` | `GIT_INDEX_FILE` rewrites the index |
| `E-score.receipt.txt` | the scoring command: `met_target true` with the repo index corrupted |
| `A2-names.receipt.txt` | five metachar filenames reported literally, no `PWNED*` |
| `A-fsmon.receipt.txt`, `A-fsmon-control.txt` | hook not executed by the tool nor by git |
