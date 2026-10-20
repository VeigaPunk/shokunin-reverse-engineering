HOLDS

# Verify17Review: round-17 `verify.py` preflight (REV `b2aad08`, baseline `9011581`)

**Scope.** This reviews `git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-17/verify.py` (exit 0; +57/−2).

**Verdict.** The verdict covers the assigned property:
- the preflight runs before any write;
- an off-branch HEAD exits 2 before `verification.json` is written.

The property holds on the shipped REV bytes (blob `810f138`, sha256 `3205f05e…`). It was shown in a plain git clone and in a jj-colocated clone, with only the LANE line changed.

The diff also adds two ineffective items: the "run it in a clone" advice (F1) and the `:81` lint annotation (F2). Neither weakens the property.

**Seat.** Author-side advisory recommendation, not an admission. The lane was read-only.

## Anchors at REV (`git show b2aad08:.ufo/waves/round-17/verify.py`)

- `:30` `LANE` is absolute, and `:31-33` derive `W`, `T` and `OUT` from it. `:59-60` `git()` runs `git -C LANE`.
- `:63-67` `_git_or_none` catches only `CalledProcessError`.
- `:70-101` `resolve_source`:
  - `:80` source = `refs/heads/main^{commit}`
  - `:81` the comment `# head-rev-lint: compare-only`
  - `:82` the HEAD read
  - `:83` `refs/remotes/origin/main`
  - `:85` `status --porcelain --untracked-files=no`
  - `:89-99` the named findings
- `:108-111` run the preflight and `return 2` on any finding.
- The first write is `:115` `os.makedirs(OUT)`. Later writes are at `:128`, `:173`, `:197` and `:234-235`. The real pass runs `run-carriers.sh` at `:213-214`.
- `:112` resolves `base` with no branch check.
- `:225` writes `head_equals_source`.
- `:10-17` is the round-18 header. `:15-17` says "Rerunning this script overwrites that retained round-17 evidence … run it only in a throwaway clone."

## Proof (observation unless labelled)

**Setup.**
- Scratch was `mktemp -d /tmp/r18v17.XXXXXX` → `/tmp/r18v17.pO3tbs`.
- Each clone: `git clone <lane>`, then `git remote remove origin`, then `:30` replaced with the clone path and committed on `main`.
- `refs/remotes/origin/main` was recreated with `git update-ref` where a scenario needs it.

**Safety rule.** Each state was first run under a no-exec harness (appendix), which fakes every non-git, non-find subprocess. The real script ran only after the harness showed a refusal, so no carrier, REA or Ghidra command could start.

1. **Static order.** `resolve_source()` (`:108`) does no file I/O except four `git` subprocesses. Every write is at `:115` or later.

2. **Test A: plain clone, off-branch HEAD.**
   - State: `git checkout --detach` plus an empty commit. HEAD=`af2d668`, main=origin/main=`580670e`, 0 tracked-dirty lines.
   - Command:
     ```
     strace -f -e trace=openat,creat,mkdir,unlink,unlinkat,rename,renameat,renameat2 -o strace-A.txt \
       python3 -I -B .ufo/waves/round-17/verify.py 9011581d84527ba34c675f9cf912e54d2e72d470   # exit 2
     ```
   - stdout: `"findings": ["head_not_branch_tip"], "refused": true`.
   - `verification.json` sha256 was `af312ef6…` before and after. The `.git/index` sha256 was unchanged. `git status --porcelain` showed 0 lines, and there were 0 `__pycache__` directories.
   - The only write-mode syscall was git's optional `.git/index.lock` (`O_RDWR|O_CREAT|O_EXCL`, then `unlink`, no rename).
   - A rerun with `-e trace=execve` (exit 2) shows exactly four successful children:
     - `git rev-parse --verify refs/heads/main^{commit}`
     - `git rev-parse --verify HEAD^{commit}`
     - `git rev-parse --verify refs/remotes/origin/main^{commit}`
     - `git status --porcelain --untracked-files=no`

3. **jj-colocated clone, shipped bytes (cloneJ2).**
   - Setup: `JJ_CONFIG=<scratch>/jjconfig.toml` (user name/email only), then `jj git init --colocate` (exit 0), then `printf … >> LOG.md; jj commit -m "off-branch content"`.
   - State: HEAD=`7b97d17`, detached, `bookmarks=[]`. main=origin/main=`aa9a747`.
   - `strace -f -e trace=…,execve python3 -I -B .ufo/waves/round-17/verify.py 9011581…` → **exit 2**, finding `head_not_branch_tip`.
   - There were **zero** write-mode syscalls. `verification.json` and `.git/index` were unchanged. The children were the same four git probes.

4. **Refusal matrix.** "Real exit" is `$?` of the real script run directly after the harness refused.

   | clone | state | real exit | findings | `verification.json` unchanged |
   |---|---|---|---|---|
   | C1 | HEAD=main=`af66ac2`, origin/main=`b2aad08` (unpushed) | 2 | `branch_not_pushed` | yes |
   | C2 | `refs/remotes/origin/main` absent | 2 | `branch_not_pushed` | yes |
   | C3 | ` M LOG.md` | 2 | `worktree_dirty` | yes |
   | C4 | `M  LOG.md` (staged only) | 2 | `worktree_dirty` | yes |
   | C5 | `git branch -m main trunk` | 2 | `branch_missing`, `head_not_branch_tip`, `branch_not_pushed` | yes |
   | cloneJ J1 | `jj commit` of an empty, unbookmarked commit | harness `main_return` 2 | `head_not_branch_tip` | yes |
   | cloneJ J2 | `jj new main` plus a dirty working copy | harness `main_return` 2 | `worktree_dirty` | yes |

   My first cloneJ pass also printed `real_exit=0` for the real script. That capture was wrong: `PIPESTATUS` was read after an intervening `echo`. I disregard those lines; item 3 redoes the off-branch case with `$?`.

5. **No false refusal (harness only).** Three passing states were tested:
   - C6: detached at the synced tip, which is the lane's normal state.
   - S: attached, synced.
   - J3: the jj normal state (empty `@` on main, HEAD detached at the tip).

   Each printed `main_return 1` (the harness fakes exit codes) and 79 faked commands. Each record had `source_revision` = tip, `source_branch:"main"` and `head_equals_source:true`. The harness process exits 0 by design; observed 0 in C6, S and C7.

6. **Red-before (cloneR).**
   - State: off-branch empty commit `84afde2`; main=origin/main=`b2aad08`.
   - REV copy under the harness: `main_return 2`, 0 faked calls. The real run `python3 -I -B ../verify.rev.cloneR.py 9011581…` exits **2**.
   - Baseline bytes (`git show 9011581:…`, LANE swapped) under the same harness write `verification.json` with `source_revision:"84afde242101659e3af1568cb45f56589baf04ef"`, the unbookmarked commit.
   - So the test state tells the two versions apart.

7. **Header claim at `:14-15` holds.**
   - `git rev-parse d0ab299:<p>` and `9011581:<p>` are the same blob, `b6852f9`.
   - Its sha256 `2896f53a…1903` equals the retained `verification.json` `pins_pre` and `pins_post` entry for verify.py.
   - REV is blob `810f138` (sha256 `3205f05e…`).

8. **Baseline lint.** `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root <lane> --rev 9011581…` → exit 0, `live_count` 3, including `.ufo/waves/round-17/verify.py:59`.

## Findings

### F1 — Medium (operability): the advice at `:15-17` causes the harm it warns about

**Problem.** `:15-17` says "run it only in a throwaway clone". But `LANE` is absolute (`:30`) and every path derives from it (`:31-33`). An unedited copy in a clone therefore probes and writes the **live lane**. The preflight cannot stop this: it checks LANE's refs, and those are in sync.

**Repro with a stand-in lane (observed).**
- cloneB has `:30` naming cloneB, committed and synced.
- `git clone cloneB cloneBx; git -C cloneBx remote remove origin`
- `cd cloneBx && python3 -I -B ../harness.py .ufo/waves/round-17/verify.py 9011581…`
- Output: `LANE=/tmp/…/cloneB`, `main_return` 1, 79 faked commands.
- cloneB's `verification.json` changed from `af312ef6…` to `385f11ca…`, leaving 80 dirty paths. cloneBx was unchanged (0 dirty).

**Live lane (read-only, `GIT_OPTIONAL_LOCKS=0`).**
- HEAD=main=origin/main=`b2aad08`, with 0 tracked-dirty lines.
- HEAD's `:30` names the lane.
- `verification.json` and 176 `verify/` files are tracked.
- [INFERENCE, not run] An unedited clone copy would pass the preflight today. It would overwrite those tracked files and run the full pass in the lane, including `:213-214` → `run-carriers.sh calib-shfmt`. Likelihood is low because the r17 pass is a past one-shot; the impact would be high.

**Prior art.** `.ufo/waves/round-18/w1/CriticNoHarmPlan.md:91-95` (D4) proposed this exact sentence as the mitigation. It was adopted without checking it against `:30`.

**Fix.** Derive `LANE` from `__file__` (`Path(__file__).resolve().parents[3]`). Alternatively, refuse unless `realpath(__file__) == realpath(LANE + "/.ufo/waves/round-17/verify.py")`. At minimum, the advice should say "with `LANE` (`:30`) edited to the clone path".

### F2 — Low–Medium (calibration of the C2 lint for this file): the `:81` annotation does nothing and the HEAD read is invisible to the lint

**What the lint reports.**
- At REV the lint emits no verify.py site: `head-rev-lint.py --root <clone> --rev b2aad08… --strict` → exit 0.
- The annotated paths are only `citation-drift-probe.py`, `custody-pair.py` and `jj-red-before.py`.
- So `.ufo/waves/round-18/claims.json:38` ("after 0 live with compare-only/red-before sites listed as annotated") does not list verify.py's compare-only read at `:82`.

**Cause.**
- The lint's first pass (`head-rev-lint.py:452-468`) treats a function as a git wrapper only when its own body contains a literal `["git", …]`.
- `_git_or_none` calls `git(*args)` (`:65`), so calls to it are never tokenized (`:421`).
- The annotation rule reads only the site line (`head-rev-lint.py:525`, docstring `:37`). A comment on `:81` would not count even if the call were visible.

**Mutants (cloneM).** Each change was committed, then linted with `--strict`.

| mutant | change | live | verify.py site | exit |
|---|---|---|---|---|
| M1 `130a4ad` | `:80` → `source = _git_or_none("rev-parse","--verify","HEAD^{commit}")`, i.e. the routed R1 regression | 0 | none | 0 |
| M2 `90c9a3b` | `:82` calls `git(...)`; comment left on `:81` | 1 | `:82` live | 1 |
| M3 `af51505` | M2 plus a trailing annotation on `:82` | 0 | `:82` annotated | 0 |
| M4 `42f4677` | fix: `:65` builds `["git","-C",LANE,*args]`; annotation trails the HEAD line | 0 | `:81` annotated | 0 |
| M5 `e2b7b99` | M4 plus M1's regression | 1 | `:80` live, `:81` annotated | 1 |

**Impact.**
- For this file, "3 → 0" comes from the lint no longer seeing the call, not from the annotation.
- The lint cannot catch the routed regression when it goes through the new helper (M1).
- Runtime is unaffected: `source` is the branch tip at REV (items 2–6).
- [INFERENCE, not run] M1 would still refuse most off-branch states via `branch_not_pushed` (`:94-95`).

**Fix.** M4: two lines, checked by M4 and M5 above.

### F3 — Low (routed recommendation partly implemented): `base` gets no branch check

**Problem.**
- The audit's R1 recommendation asks to "Apply the same to `base`" (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:260`; row `:186`).
- `:112` accepts any commit-ish.
- The contract (`.ufo/waves/round-18/contract.md:83-86`) does not require the check.

**Repro (cloneK, synced).**
- `D=$(git commit-tree -m dangling 'HEAD^{tree}')`
- `git merge-base --is-ancestor $D refs/heads/main` → exit 1.
- `git for-each-ref --contains $D` → empty.
- `python3 -I -B ../harness.py .ufo/waves/round-17/verify.py $D` → preflight passes, 79 commands run, and the record has `baseline_revision:"354f863f86f4126b07446594f97a73ac26bc682b"`.

### F4 — Low: one error path breaks the docstring contract

**Problem.** `:76-78` says each git probe failure maps to a named finding. `_git_or_none` catches only `CalledProcessError` (`:66`).

**Repro (cloneA).** `env PATH=/var/empty /usr/bin/python3 -I -B .ufo/waves/round-17/verify.py 9011581…` → exit **1**, `FileNotFoundError: … 'git'` raised along `:108`→`:80`→`:65`→`:60`. The failure still happens before any write: `verification.json` was unchanged.

## Not defects (observed)

- `head_equals_source` (`:225`) is always `true` in any written record, because `:109-111` refuses otherwise.
- Untracked files are not refused (`:85` uses `--untracked-files=no`, as `contract.md:84-85` specifies). They are recorded and pinned: in C7, `zz_untracked_probe.py` appears in `worktree_dirty_at_start` and in `pins_pre`.
- The preflight's `git status` can take git's optional `.git/index.lock` (seen in Test A). Setting `GIT_OPTIONAL_LOCKS=0` at `:85` would make it lock-free.

## Residual risk and verification gaps

- **No `lsp` device.** `read xd://lsp` returned "No such tool", so caller checks fell back to text grep. Nothing imports the round-17 `resolve_source` or `_git_or_none`. Round-18 `verify.py:92` uses `revpin.resolve_source` instead.
- **Divergence (outside this target).** At REV, `revpin.py` has 0 matches for `status|dirty|porcelain`. So the round-18 pass does not refuse a dirty tree, while round-17's does. For Verify18Review.
- **First run of the shipped bytes.** jj-red-before exercises `revpin.resolve_source` (`jj-red-before.py:55,438`), not these bytes. Items 2, 3 and 6 are the first runs of the shipped round-17 preflight, as asked in `.ufo/waves/round-18/w1/CriticC2.md:24` (A7) and `:158`.
- **Harness limits.** Passing states, F1, F3 and the baseline red-before ran under the harness. Their `main_return 1` and `unexpected_exits` come from faked exits; the record fields `source_*`, `baseline_revision` and `head_equals_source` are real.
- **Not tested: refs moving mid-pass.** Refs could move after `:108` during a pass. `source` is captured once and the git-object tools use it, but tools that run on the worktree do not.

## Lane safety and tooling

- **Lane after:** HEAD=main=origin/main=`b2aad08`, 0 tracked-dirty lines, 0 untracked under round-17. The lane's `verification.json` and `verify.py` blobs equal the REV blobs (`3815e2c`, `810f138`).
- **Lane access:**
  - Only read-only git ran in the lane.
  - My first lane probe used plain `git status --porcelain --untracked-files=no`; later probes set `GIT_OPTIONAL_LOCKS=0`.
  - `head-rev-lint.py` ran from the lane path against the lane and clones, using read-only git.
  - jj ran only in cloneJ and cloneJ2, both with origin removed.
- **Never run:** REA, Ghidra, any carrier, the round-17 pass in the lane.
- **Installs or updates:** none. Preinstalled tools used: git 2.56.0, jj 0.45.1, strace 7.2, Python 3.14.8.
- **Cleanup:** the scratch directory `/tmp/r18v17.pO3tbs` was removed after this report was written.

## Appendix: `harness.py` (verbatim; run from the mkdtemp directory)

```python
"""Throwaway review harness (outside any repo): run a verify.py main() with every
non-git/find subprocess.run call faked (never executed). git/find pass through.
usage: python3 -I -B harness.py VERIFY_PY BASELINE_REV
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

path, base = sys.argv[1], sys.argv[2]
real_run = subprocess.run
faked = []


def fake_run(argv, *a, **k):
    head = argv[0] if isinstance(argv, (list, tuple)) else str(argv).split()[0]
    if os.path.basename(head) in ("git", "find"):
        return real_run(argv, *a, **k)
    faked.append(list(argv) if isinstance(argv, (list, tuple)) else argv)
    return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")


subprocess.run = fake_run
spec = importlib.util.spec_from_file_location("verify_under_review", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
vj = mod.W + "/verification.json"


def digest(p):
    if not os.path.exists(p):
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


pre = digest(vj)
sys.argv = [path, base]
rc = mod.main()
post = digest(vj)
summary = {"main_return": rc, "LANE": mod.LANE, "verification_json": vj,
           "verification_sha_pre": pre, "verification_sha_post": post,
           "verification_changed": pre != post, "faked_subprocess_calls": len(faked)}
if post and pre != post:
    rec = json.load(open(vj))
    summary.update({k: rec.get(k) for k in ("source_revision", "baseline_revision",
                                             "source_branch", "head_equals_source")})
print("HARNESS " + json.dumps(summary, sort_keys=True))
```
