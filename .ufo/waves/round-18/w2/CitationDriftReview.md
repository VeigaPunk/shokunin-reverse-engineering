PARTIAL — all three assigned checks hold: `--selftest` passes 15/15, explicit-rev results match the baseline in 28 of 28 old-vs-new pairs, and both new finding IDs exit 2 with and without `--strict`. Two parts of the change do not fully hold. The R2 guard catches only the exact string `HEAD`, so other spellings of HEAD get through. The self-test does not catch a change to explicit-rev handling or to `branch_missing` (2 mutants survive). There are also 4 low-severity edge defects.

# CitationDriftReview — round 18 wave 2 (falsify), author-side advisory seat

Target: `git diff 9011581d84527ba34c675f9cf912e54d2e72d470 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/gates/citation-drift/`. Only the probe changed (+140/−22). `pointer-table.json` (7994eec7…) and `expected.json` (05c251fb…) are byte-identical at both revisions.
Anchors are `git show REV:path` with REV=b2aad08…; B=9011581…. The lane HEAD (detached) and `refs/heads/main` were both b2aad08… before and after my runs. The worktree probe sha256 is `d3e24de4…`, the same as the REV blob, so running the lane path runs the REV bytes. The baseline probe (`e2665074…`) came from `git show B:…`.

Shorthand used in the commands below: `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `P=$L/.ufo/gates/citation-drift/citation-drift-probe.py`, `A="--table $L/.ufo/gates/citation-drift/pointer-table.json --expected $L/.ufo/gates/citation-drift/expected.json"`, `BASE=` the baseline probe extracted to a mkdtemp directory (with `expected.json` beside it), `T=` a mkdtemp scratch directory.

## Assigned checks (observed)

| # | Command | Exit | Key output |
|---|---|---|---|
| 1 | `TMPDIR=$T python3 -I -B $P --selftest` | 0 | `CITATION_DRIFT_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`. The 13 old cases are unchanged; `detached_head_default` exits 0 and `detached_head_rev_head` exits 2 with `head_not_branch_tip`. |
| 1b | `TMPDIR=$T python3 -I -B $BASE --selftest` (reference) | 0 | `CLEAN cases=13 passed=13` |
| 2 | SKILL.md:448 argv (`python3 -I` + `-B`) `--root $L --rev b2aad08… $A --strict` | 0 | `REV_REQUESTED`/`REV_RESOLVED: b2aad08…`, `BRANCH: main`, `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` |
| 3 | same argv with `--rev 9011581…` | 0 | `REV_RESOLVED: 9011581…`, `clean findings=0 exit=0` |
| 4 | same two argvs run with `$BASE` | 0, 0 | `CITATION_DRIFT_REVISION: <rev>`, `clean findings=0 exit=0` |
| 5 | Old-vs-new comparison: 14 `--rev` forms, each with and without `--strict` (28 pairs). Forms: R, B, `b2aad08`, `refs/heads/main`, `main`, R~5, R~20, `af51e911…`, `c265db9b…`, `deadbeef…`, `R^{tree}`, `@`, `HEAD~0`, `HEAD`. | 0 | `MATRIX: pairs=28 mismatches=0`. Exit code, every `CITATION_DRIFT:` row and the verdict line are identical. This includes `af51e911` (23 findings; strict 1, probe mode 0), `c265db9b` (43 findings; strict 1, probe mode 0), and `deadbeef`/`^{tree}` (both exit 2 `revision_unresolvable`). |
| 6 | `python3 -I -B $P --root $L --branch no-such-branch $A --strict` | **2** | `branch_missing entry=no-such-branch …`. The same command without `--strict` also exits **2**. |
| 7 | `… --rev HEAD --branch no-such-branch $A --strict` | **2** | `head_not_branch_tip … HEAD b2aad08… != refs/heads/no-such-branch (missing)` |
| 8 | Clone A (detached off-branch HEAD `ff8049e2…` with the same tree as main): `--rev HEAD`, with and without `--strict` | **2**, **2** | `head_not_branch_tip … HEAD ff8049e2… != refs/heads/main b2aad08…`. With `--rev` omitted, it grades `b2aad08…` and exits 0. |
| 9 | Clone B (jj 0.45.1 colocated; `jj commit -m off-branch-w2` makes git HEAD `d299a164…`, not on main): `--rev HEAD --strict` | **2** | `head_not_branch_tip`. With `--rev` omitted, `REV_RESOLVED: b2aad08…` and exit 0. |

Conclusions from the observations above:
- Explicit-rev behaviour is unchanged at REV (`citation-drift-probe.py:339-342`; checks 2–5).
- Both new IDs are in the could-not-evaluate set at `:93-94` and exit 2 in both modes (checks 6–9).
- At the tip, a literal `HEAD` is accepted with no false refusal (check 5, `rev=HEAD`).

## Findings (by severity)

**F1 Medium — the R2 guard catches only the exact string `HEAD`; other spellings grade an unlanded HEAD and exit clean.** (observed)
- In `resolve_rev`, only `rev == "HEAD"` is checked (`:329`). Every other spelling goes through unchecked (`:339-342`).
- In clone A, `--rev @`, `--rev HEAD~0`, `--rev 'HEAD^{commit}'` and `--rev 'HEAD@{0}'` all print `REV_RESOLVED: ff8049e2…` and `clean findings=0 exit=0` in strict mode (exit 0 without `--strict` too). Literal `HEAD` in the same clone exits 2.
- In clone B (real jj), `--rev @` prints `REV_RESOLVED: d299a164…` (`git show --stat @` shows only `W2-OFFBRANCH.txt`) and `clean exit=0`.
- The probe's own docstring (`:42-47`) says attesting such a tree "would certify a revision that never landed". The jj audit's R2 fix asked for a check "when `rev` came from HEAD" (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:164-166,244`).
- The code does match the literal wording of `contract.md:75` and the probe docstring `:47-48` ("any other form behaves exactly as before"). So this is a gap in the scope of the fix, not a deviation from the implementation spec.
- No lane caller passes these spellings: the registered argv uses a SHA. [INFERENCE] Under jj, `@` is the idiomatic way to name the working copy, so a manual run with it is plausible.
- Reproduce in a mkdtemp clone:
  ```
  git clone -q --shared --no-checkout $L $T/c
  git -C $T/c remote remove origin
  git -C $T/c update-ref refs/heads/main b2aad08…
  c=$(git -C $T/c -c user.name=x -c user.email=x@x commit-tree -p main -m off 'main^{tree}')
  git -C $T/c update-ref --no-deref HEAD $c
  python3 -I -B $P --root $T/c --rev @ $A --strict
  ```
  The last command exits 0 with `REV_RESOLVED=$c`.
- Negative control: `--branch` cannot be used to point the tip at HEAD. `refs/heads/{../HEAD,..,@,HEAD}^{commit}` does not resolve in clone A (observed).

**F2 Medium — the self-test does not protect the explicit-rev guarantee or `branch_missing`.** (observed; mutants were run in `$T` only)
- Mutant M7 changes `:341-342` so that any explicit rev that resolves is graded at the branch tip instead. Its `--selftest` gives `CLEAN cases=15 passed=15 exit=0`.
  - On the lane, `M7 --root $L --rev c265db9bd3c0883fbaf4487f839559c85a736826 $A --strict` prints `clean findings=0 exit=0`. The real probe gives `failed findings=43 exit=1` (check 5).
  - Cause: all 13 old cases call `run_check(root, "HEAD", …)` (`:560-566`), which goes through the literal-HEAD path. The only explicit-rev case is the unresolvable `deadbeef`.
  - The guarantee in `contract.md:77` ("explicit 40-hex `--rev` behaves exactly as before") is therefore checked only by out-of-band runs like check 5.
- Mutant M5 removes `"branch_missing"` from the could-not-evaluate set at `:94`. Its self-test also gives `CLEAN 15/15`.
  - On the lane with `--branch no-such-branch`, probe mode prints `reported findings=1 exit=0`: a silent pass. Strict mode exits 1, not 2.
- Mutants M1 (omitted rev means HEAD), M2 (no HEAD guard), M3 (guard never fires), M4 (`head_not_branch_tip` not could-not-evaluate) and M6 (explicit rev ignored) were each killed by exactly one failing case. The detached pair does discriminate for what it covers.

**F3 Low — `--rev HEAD` is wrongly refused when a path named `HEAD` exists in `--root`.** (observed)
- `head_commit` runs `git rev-list --max-count=1 HEAD` with no `--` (`:304`).
- Reproduce:
  ```
  git init -q -b main $T/f && echo alpha > $T/f/A.md && git -C $T/f add A.md && git -C $T/f -c user.name=x -c user.email=x@x commit -qm a
  touch $T/f/HEAD
  ```
  Then run the probe with a one-entry table whose digest is pinned in its expected file.
- Result: `--rev HEAD --strict` exits **2** with `head_not_branch_tip … HEAD (unresolvable) != refs/heads/main 9d2e6d21…`, although HEAD == main (`rev-parse` confirms).
- `$BASE` on the same input exits 0. Raw `git -C $T/f rev-list --max-count=1 HEAD` exits 128 ("ambiguous argument 'HEAD': both revision and filename"); adding `--` makes it exit 0.
- `:301-302` say `rev-list` was chosen to keep HEAD out of a `rev-parse` argv for the lint. `revpin.py:98-119` uses `rev-parse --verify` and does not have this problem.
- The failure is fail-closed (exit 2), so it does not break safety. It does contradict "otherwise … head_not_branch_tip" in `:44-46`, because HEAD here does equal the tip.

**F4 Low — the self-test's command-line children drop `-I`, so the result depends on the caller's environment.** (observed)
- `:548` runs `[sys.executable, os.path.abspath(__file__), …]` with no `-I` and no scrubbed environment.
- Reproduce: `mkdir $T/s && echo 'raise SystemExit(7)' > $T/s/argparse.py`, then `PYTHONPATH=$T/s python3 -I -B $P --selftest` exits 1 with `FAILED cases=15 passed=13 failed=2`; both detached cases report exit 7.
- The same environment with `$BASE --selftest` exits 0 (`CLEAN 13/13`). Controls: `python3 -I` ignores the shadow module; `python3` without `-I` exits 7.
- The registered argv is `python3 -I` (SKILL.md:448). The lane's own child-process convention is `-I -B` plus a scrubbed environment: `jj-red-before.py:113-125` (`_child_env`) and its probe children at `:389`, `:552` and `:576`.
- [INFERENCE] A user-site `.pth` file or a PYTHONPATH shadow module could equally make these cases pass falsely.

**F5 Low — the run-provenance header lines are wrong outside the graded path.** (observed)
- When git is missing or the table is malformed, `main` replaces `findings` with a fresh `Findings()` (`:609-611`), and `report` falls back to defaults (`:397-401`).
  - `env -i PATH=/nonexistent /usr/bin/python3 -I -B $P --root $L --rev b2aad08… --branch release $A --strict` prints `REV_REQUESTED: (default)`, `REV_RESOLVED: (unresolved)`, `BRANCH: main`, with `internal_error … FileNotFoundError`, exit 2.
  - `$BASE` with the same input prints `CITATION_DRIFT_REVISION: b2aad08…`, so the requested rev is lost: a regression.
  - A pinned table containing the regex `"("` gives the same pattern (`PatternError`, exit 2).
- `REV_RESOLVED` is also not a resolved commit on other non-graded paths:
  - `HEAD` on refusal (check 7, clone A/B; already visible in `.ufo/waves/round-18/evidence/jj-red-before.json:526`).
  - `None` for `branch_missing` (check 6).
  - The raw input for `deadbeef…` and `R^{tree}` (check 5). This comes from `:341` (`… or rev`) and `:348`.
- PROTOCOL.md:393: "A verdict names the revision it was measured against."

**F6 Info — the finding-ID taxonomy differs from revpin and from the registry text.**
- `--rev HEAD` with a missing branch yields `head_not_branch_tip … (missing)` (check 7; `:329-336`).
- `revpin.resolve_source` raises `branch_missing` first (`revpin.py:98-100`). The contract calls the probe logic "revpin-equivalent" (`contract.md:74`).
- SKILL.md:448 cell 2 ("… else exit 2 `head_not_branch_tip` (`branch_missing` when the branch is absent)") reads as applying to the `--rev HEAD` clause. Exit code 2 is the same either way.

**F7 Info — the new self-test expectations live in the script, not in the pinned table.**
- `:502-503` hard-code the two new cases, against the probe's own note at `:459-461` ("NOT defined here … independent of the recomputation") and PROTOCOL.md:385-387.
- `expected.json` still lists 13 cases and its digest `05c251fb…` is unchanged (it is pinned at `.ufo/waves/round-16/verification.json:417`). So 2 of the 15 expectations are outside every pinned file.
- SKILL.md:448 cell 3 discloses this ("the original case table committed in `expected.json`"). Cell 4 still says "`expected.json` pins the self-test case table".

**F8 Info — some anchors in the wave-1 report point at the wrong lines** (`.ufo/waves/round-18/w1/CitationDriftBranchTip.md`).

| Report says | Correct at REV |
|---|---|
| argparse `:575-580` (lines 575-580 are the self-test tally) | `:590-597` |
| `revision_unresolvable` `:353-356` | `:357-360` |
| `:340` | `:341` |
| `:431` | `:432` |
| `:394-400` | `:395-401` |
| new cases `:497-502` | `:502-503` |

## Residual risk and verification gaps

- [INFERENCE] An explicit symbolic rev (`main`, `@`) is resolved once for `REV_RESOLVED` (`:341`), but each file is read with the symbolic string (`git_show` `:111-120`, called from `Tree.lines` `:136-147`). A ref that moves mid-run could therefore make the header name a different commit from the one some entries were read at. I did not reproduce this; it would need concurrent ref movement. The behaviour itself is pre-existing: the baseline also read by the symbolic name.
- The wave-1 receipt `evidence/jj-red-before.json` does not record the sha256 of the fixed probe it ran (lane tip 9011581 at that time; no `d3e24de4…` in the receipt). My re-runs on the REV bytes reproduce its probe-side expectations (checks 7–9; check 5 `rev=HEAD` at the tip).
- Cross-check (not a finding): `head-rev-lint.py` (extracted from REV) at REV reports live 0. The probe sites are `:304 other-HEAD annotated` and `:452 fixture`. At B it reports `:477 default-HEAD live`.
- No live consumer parses `CITATION_DRIFT_REVISION`. `jj-red-before.py:185-200` accepts both header forms, and `round-17/verify.py:192-196` checks only the exit code. The other matches are historical wave docs.
- Not exercised: `--root` pointing at a subdirectory, bare repositories, and the selftest under hosts with a global `core.hooksPath` or GPG commit signing.

## Custody and tools

- Lane access was read-only git: show, rev-parse, rev-list, grep, ls-tree, diff, log and merge-base, plus clone reads from the lane as source. Some early calls did not set `GIT_OPTIONAL_LOCKS=0`: the first diff/show/rev-parse calls, one `git status --porcelain -- .ufo/gates/citation-drift/`, and the direct probe runs. Of these, only `git status` may refresh the index stat cache, and that changes no content. Later lane git calls set `GIT_OPTIONAL_LOCKS=0`.
- Writes went only to mkdtemp `/tmp/cdr-w2-MDxqa1`: clone A (`--shared --no-checkout`), clone B (`--no-local`), fixtures, mutants and the comparison harness. `origin` was removed immediately after each clone (verified `remotes=[]`). jj ran only inside clone B, with HOME and XDG_CONFIG_HOME pointed at the sandbox.
- After all runs, lane HEAD and `main` are still b2aad08…, and the probe directory has no new files.
- Scratch was removed after this report was written.
- Installs and updates: none. Tools already present: git 2.56.0, Python 3.14.8, jj 0.45.1 (`~/.local/bin/jj`).
