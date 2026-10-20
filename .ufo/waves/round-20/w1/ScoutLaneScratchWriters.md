# ScoutLaneScratchWriters — writes inside the lane tree during selftests/verification

Timestamp (clock at write time): 2026-10-20T17:52:28-03:00
Baseline observed: `14f0260ad319ecc26994381b2415d5a999003375` (read-only; no git/`jj` writes in the lane).
Scope swept: `.ufo/gates/**` (3 tools), `.ufo/waves/round-16/**` (4 scripts), `round-17/tools/*.py` (13) +
`round-17/{verify,measure,controls,run-carriers}`, `round-18/tools/*.py` (5) + `round-18/{verify,measure,controls,*gen-*}`,
`round-19/tools/*.py` (4) + `round-19/{verify,measure,controls-r19,postfix-mutations,run-carriers,*gen-*}`.
No tool was installed or updated for this task. No `verify.py`, no `run-carriers.sh` and no carrier/REA/Go command was
executed (read-only seat; those would write the lane).

## 1. Observation — the D1 residue exists now, in two forms

```
$ git status --porcelain -- .ufo/waves/round-19/verify/scratch-custody      # exit 0
?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-fixture/
?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-sub-fixture/
$ find .ufo/waves/round-19/verify/scratch-custody -name .git -maxdepth 5   # exit 0
.../custody-pair-selftest-k_zd4w5n/repo-fixture/.git
.../custody-pair-selftest-k_zd4w5n/repo-sub-fixture/.git
```
The two nested `.git` trees cannot be added by git; every sibling file of the same mkdtemp root **was**
committed, so residue survives as tracked scratch:

```
$ git ls-files .ufo/waves/round-18/verify/scratch-custody | wc -l           # exit 0 -> 83
$ git ls-files .ufo/waves/round-19/verify/scratch-custody | wc -l           # exit 0 -> 85
$ git ls-files -s .ufo/waves/round-1[89]/verify/scratch-custody | awk '{print $1}' | sort | uniq -c
     82 100644 / 1 120000      (round-18: total 83)
     84 100644 / 1 120000      (round-19: total 85)
$ git log --oneline -1 -- .ufo/waves/round-18/verify/scratch-custody       # exit 0 -> 454dee6
$ git log --oneline -1 -- .ufo/waves/round-19/verify/scratch-custody       # exit 0 -> 2a6229f
```
Both are the wave's own "post-integration verification" commits. The committed 120000 entries are
`custody-pair-selftest-*/symlink-loop` — an absolute self-referential symlink (created at
`.ufo/gates/custody-pair/custody-pair.py:1334-1336`) pointing back into the lane's verify/scratch-custody.
`.gitignore` holds only `__pycache__/` and `*.pyc` (`.gitignore:1-2`); `git check-ignore` on the residue
returns 1 (not ignored). The pre-round record agrees:
`.ufo/waves/round-20/evidence/d1-residue-before.txt` lists the same two `??` lines.

## 2. Reproduction with a scratch root outside the lane (my own fixtures)

```
$ base=$(mktemp -d /dev/shm/kr20-cust-XXXXXX)
$ python3 -I -B .ufo/gates/custody-pair/custody-pair.py selftest --scratch "$base";   # exit 0
  CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0
  leftover_dirs=1, nested_git=2, files=136
```
Observation: `custody-pair.py` **never removes** its mkdtemp root. `cmd_selftest` prints the scratch path and
returns at `.ufo/gates/custody-pair/custody-pair.py:1456-1459` with no `rmtree`/`remove` anywhere in the file.
Two fixture repos are created inside that root: `repo-fixture` (:1372) and `repo-sub-fixture` (:1426), each
with a `.git`. With `--scratch` pointing inside the lane (what the two verify scripts do, §3) this is exactly
the observed D1 residue — untracked nested repos plus, after `git add -A`, committed scratch.

Guard check (contract D1's `scratch_inside_worktree`): a scratch path inside a **temporary** Git worktree is
accepted, not refused:
```
$ mkdir -p $base/repo/sub && git init -q $base/repo
$ python3 -I -B .../custody-pair.py selftest --scratch "$base/repo/sub";               # exit 0
  stderr: grep -c scratch_inside_worktree -> 0 ; leftover=1 ; SELFTEST CLEAN cases=31
```
Observation: the baseline has no worktree-containment guard at all (`grep -n 'scratch_inside_worktree|inside_worktree'`
finds nothing in the file). Default scratch is already outside the lane (`/dev/shm`, `/var/tmp`, `/tmp` excluded —
`:752-759`), so the hazard is only exercised by a caller that passes a lane path.

## 3. Write sites by class (path:line)

### A. Scratch under the lane, created by the verification scripts themselves (auto residue)
- `.ufo/waves/round-18/verify.py:166` `os.makedirs(OUT + "/scratch-custody")`; `:169` passes
  `--scratch {OUT}/scratch-custody` to custody-pair, where `OUT = W + "/verify"` (`:33`, `:104`). Every
  verification run drops a full custody fixture root inside `round-18/verify/`.
- `.ufo/waves/round-19/verify.py:537-539` — identical pattern (`OUT` at `:71`, makedirs at `:455`).
- There is no pre-run cleanup of `scratch-custody` in either script (`grep rmtree` finds only the scripts'
  own selftest temps at `round-19/verify.py:337,368`).
- **Can leave untracked or nested-repo residue: yes.** That is the observed round-19 D1 state (§1), and the
  non-nested part additionally gets committed by the wave's `git add -A`, i.e. the residue becomes lane history.

### B. Fixed output dirs inside the lane (by-design evidence; untracked on new labels)
- `round-17/verify.py:34,116,128-129` — writes `<label>.stdout/.stderr`, pins snapshots and prediction
  copies under `round-17/verify/`; `:198` `os.makedirs(W + "/custody")`; `:214-215` runs run-carriers with
  `env={"RUNS_DIR": "verify/replicate"}` resolved against LANE (`cwd=LANE`, `:132`).
- `round-18/verify.py:104,118-145` same writer; `:269` `os.makedirs(W + "/custody")`.
- `round-19/verify.py:200-262` (`Verifier.run` writes `OUT/<label>.stdout|.stderr`), `:455` `makedirs(OUT)`,
  `:579-580` `OUT/scratch-predictions`, `:624-626` rewrites prediction bytes there.
- These directories are intentional artifacts (mostly tracked), but not ignored: a renamed label or a
  re-run with a new tool list creates fresh untracked files in the lane working tree.

### C. `RUNS_DIR` — default lane write; containment guard only from round-18 onward
- `round-17/run-carriers.sh:19-23` — `out="${RUNS_DIR:-runs}/$label"`, relative resolved against `$W`, then
  `rm -rf "$out"; mkdir -p "$out"` with **no** realpath containment check. Any `RUNS_DIR` (absolute) is
  accepted, so a mistargeted value writes — or `rm -rf`s — outside `runs/`.
- `round-18/run-carriers.sh:208-216` and `round-19/run-carriers.sh:286-293` add the guard
  (`"$W/runs/"*|/tmp/*`), refusing `run-carriers: refusing out dir outside W19/runs or /tmp`.
- Default without `RUNS_DIR` is `<wave>/runs/<label>` — a lane write by design (evidence), not scratch.

### D. `TMPDIR`
- `round-17/tools/carrier-run.py:283` sets the child env `TMPDIR=private_root`, created by
  `:301` `mkdtemp(prefix="kr17-rea-", dir="/tmp")` — always `/tmp`, never the lane; removed with the run
  (cleanup at the `rmtree` sites in the same file). No other tool exports or accepts `TMPDIR` as an output
  root; `round-18/tools/jj-red-before.py:125,143` strips `TMPDIR`/`GIT_*`/`JJ_*` from child envs and
  `:116`/`:310` refuses a sandbox root under the lane.

### E. Default `mkdtemp()` (system temp) + cleanup — verified clean
Sites (all `tempfile.mkdtemp()` with no `dir=`, cleaned in `finally`/loop):
`gates/citation-drift/citation-drift-probe.py:503` (removed `:695`; case dirs `:612` TemporaryDirectory),
`round-17/tools/{carrier-census:194,compare:451,invocation-audit:370,predict:284,retain:197,log-extract:313,
receipt-validate:806,pins:170,carrier-run:547}`, `round-17/measure.py:238,255`, `round-17/controls.py:449`
(removed via `os.remove/os.rmdir :494-496`), `round-18/tools/{revpin:166,head-rev-lint:803,routed-defects:1055,
swiss-misread:1748,jj-red-before:1043}`, `round-18/measure.py:121`, `round-18/controls.py:620`,
`round-19/tools/{rea-catalog:280,province-pins:430,routed-r18:402,wave-outcomes:417}`, `round-19/measure.py:154`,
`round-16/selfcheck.py:339` (TemporaryDirectory). `round-17/tools/buildinfo-probe.py:502` has no rmtree but
removes files/dirs individually at `:599-602`; `round-17/tools/temporal-sweep.py:235` removes with
`rm -rf` at `:393`. No lane path is used at any of these sites.

Empirical check with a private `TMPDIR` (fixtures only under my mkdtemp):
```
$ TMPDIR=$base python3 -I -B <tool> --selftest
buildinfo-probe rc=0 left=0 | temporal-sweep rc=0 left=0 | citation-drift rc=0 left=0
wave-outcomes rc=0 left=0  | controls17 rc=0 left=0     | controls18 rc=0 left=0
```
(Observation: no temp residue for these six; inference: the listed `finally` cleanup covers the normal and
the tested failure paths, not SIGKILL.)

### F. `mkstemp(dir=<caller out dir>)` atomic writes
- `round-19/tools/rea-catalog.py:258` (`--out` parent) and `round-19/tools/wave-outcomes.py:362`
  (`--out` parent) write `.rea-catalog-*` / `.wave-outcomes-*.tmp` **beside the requested output**, then
  `os.replace` and unlink in `finally` (`rea-catalog:264-268`, `wave-outcomes:363-370`). If `--out` is in
  the lane the temp file exists in the lane for the write window; normal exit leaves nothing.

### G. Generation (not selftest) writes the lane by design
- `round-20/gen-wave1.py:670` writes `wave1-spec.json` next to itself; `round-18/19 gen-*.py` similarly emit
  wave JSON. These are authoring steps, not selftests; no scratch root involved.

## 4. Calibration notes against contract D1

- The contract's D1 shape is "exit 2 `scratch_inside_worktree` when DIR is inside any Git worktree; otherwise
  runs and **leaves no `custody-pair-selftest-*` dir under DIR on exit**". Observation: at baseline both
  halves are missing — no worktree walk exists, and no removal path exists (custody-pair.py returns at
  `:1459` after printing the root). A fix that only adds the guard would still leave the round-18/19 pattern
  intact if any caller passes a path outside a worktree but inside the lane tree's non-Git parts (e.g. a
  detached copy), and would not clean the already-committed scratch.
- The two verify scripts should stop passing a lane path: `tempfile.mkdtemp()` outside the lane (or
  `--scratch` pointed at `/dev/shm`) removes the writer side entirely; the custody-pair cleanup is still
  required for contract conformance and for direct callers.
- The 85/83 committed scratch entries were introduced by the wave verification commits `2a6229f`/`454dee6`
  (observed). Whether the round-20 fix deletes that tracked residue is an integration-owner decision; it is
  not covered by my read-only scope.

## 5. Remaining unknowns / limits

- I did not execute `round-17/18/19/20 verify.py` (they write the lane working tree) or any
  `run-carriers.sh` real run (carrier execution is prohibited); their write sites above are static reads.
  [INFERENCE] their observed behaviour matches the committed residue from the two prior verification commits.
- `.ufo/waves/round-20` has no `verify.py` or `tools/` at the baseline, so no W20 selftest writer could be
  audited; contract D5 will add `W20/verify/final-census.json` — a lane write by design.
- Static-only, lower confidence, out of the named scope: `round-17/w2/log-extract-attack.py:131` and
  `round-17/w2/stopgroup-attack.py:261` each `mkdtemp(dir="/tmp")` with zero cleanup tokens in the file
  [INFERENCE: /tmp residue per run, never the lane]. The two `gen-wave1/gen-wave2` "0 cleanup" hits are
  docstring mentions, not mkdtemp calls.
- Did not inspect contents under the residue `.git` dirs (not needed to establish the class).
