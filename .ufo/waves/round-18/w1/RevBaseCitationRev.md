# RevBaseCitationRev — falsification of jj risk R2 at baseline `9011581d`

Scope: `JjAuditKaidoku.md` risk **R2** (`.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:244`), the
`citation-drift-probe.py` default `--rev HEAD`. Read-only in LANE; writes only this report. jj and git
writes ran only in `/tmp/revbase-r2-j9clqygg` (mkdtemp sandbox), per `contract.md:20`. No REA, Ghidra,
`analyzeHeadless`, or carrier execution.

Verdict in one line: **the citations are exact; effect (a) is a real mechanism, reproducible in a jj
sandbox and capable of both false green and false red, but it is not active at `9011581d` (HEAD == main ==
origin/main) and is only transient in the lane's own write path; effect (b) is misattributed to jj — it
reproduces identically under plain git and is revision-scoped-by-design.** The contract's prescribed fix
(`contract.md:73-77`) is the right minimal change; it has two implementation traps (D1, D2) and one
acceptance metric that is probably unsatisfiable (D3).

## 1. Citation check — exact at `9011581d`

Observation: every anchor R2 and its table row name still holds, byte-for-byte, at the current baseline.
`cmp` of the working file against the committed blob at `9011581d` → **exit 0**, so no sibling edit was
in flight when measured.

| audit anchor | cited content | observed at `9011581d` |
|---|---|---|
| `JjAuditKaidoku.md:164` | `citation-drift-probe.py:102` = `["git","-C",root,"show",f"{rev}:{path}"]` | exact (`citation-drift-probe.py:102-103`) |
| `JjAuditKaidoku.md:165` | `:265` = `["git","-C",root,"rev-parse","--git-dir"]` | exact (`:265-266`) |
| `JjAuditKaidoku.md:166` | `:273-275` = `["git",...,"rev-parse","--verify","--quiet","%s^{commit}"%rev]` | exact (`:273-275`) |
| `JjAuditKaidoku.md:244` | default `--rev HEAD` at `L477`, used by `L102`/`L274` | exact: `ap.add_argument("--rev", default="HEAD")` at `:477`; `run_check(args.root, args.rev, ...)` at `:489`; `Tree` gets `rev` at `:314`; `git_show(root, self.rev, ...)` at `:131`; `rev_ok(root, rev)` at `:285` |

No citation drift. Note the audit's own baseline was `da64646…`, not `9011581d`; the cited lines did not
move between the two.

## 2. Lane state at measurement (observation)

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin
state branch=main local=9011581d84527ba34c675f9cf912e54d2e72d470 remote=9011581d84527ba34c675f9cf912e54d2e72d470 ahead=0 behind=0 head=detached tracked=0 untracked=1
(exit 0)

$ git -C LANE rev-parse HEAD main origin/main
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
(exit 0)

$ git -C LANE symbolic-ref -q HEAD        -> (no output) exit 1
$ git -C LANE merge-base --is-ancestor HEAD refs/heads/main -> exit 0
$ git -C LANE status --porcelain
?? .ufo/waves/round-18/
(exit 0)
```

A later sample (siblings writing) gave `tracked=1 untracked=1` with
` M .ufo/waves/round-17/tools/compare.py` added; HEAD/main/origin stayed `9011581d…`. `.jj` exists;
`trunk()` resolves to `main@origin` (`jj config list --repo`).

Probe behaviour at this state (observation):

```
$ python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 9011581d…
CITATION_DRIFT_REVISION: 9011581d84527ba34c675f9cf912e54d2e72d470
CITATION_DRIFT_VERDICT: reported findings=0 exit=0            (exit 0)

$ python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py --root .
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_VERDICT: reported findings=0 exit=0            (exit 0)
```

So at the current state the default path and the explicit-tip path are the same tree. R2 is latent here,
not active.

## 3. R2(a) — mechanism is real (sandbox observation)

Sandbox `/tmp/revbase-r2-j9clqygg/repo`: `git init -b main`, one commit `ba6dd215…`, then
`jj git init --colocate` (jj 0.45.1, `snapshot.auto-track="none()"`), one edited file, one
`jj file track`ed new file, `jj commit -m off` **without** moving `main`.

```
$ git rev-parse --verify --quiet HEAD^{commit}            -> ea31114f2b33… exit 0
$ git rev-parse --verify --quiet refs/heads/main^{commit} -> ba6dd215b9c2… exit 0
$ git symbolic-ref -q HEAD                                -> (no output) exit 1
$ git merge-base --is-ancestor HEAD refs/heads/main       -> exit 1
$ git status --porcelain                                  -> (empty) exit 0
```

Baseline probe against this repo (table clean at `main`, dead at the off-branch commit):

```
default (no --rev):  CITATION_DRIFT_REVISION: HEAD
                     CITATION_DRIFT: citation_dead entry=e-old TARGET.md:3 lacks 'pinned claim lives here'
                     CITATION_DRIFT_VERDICT: failed findings=1 exit=1     (--strict, exit 1)   <- false RED
--rev refs/heads/main: CITATION_DRIFT_VERDICT: clean findings=0 exit=0   (--strict, exit 0)
```

With a table that reds at `main` and is clean off-branch:

```
default (no --rev):  CITATION_DRIFT_VERDICT: clean findings=0 exit=0     (--strict, exit 0)   <- false GREEN
--rev refs/heads/main: CITATION_DRIFT_VERDICT: failed findings=2 exit=1  (--strict, exit 1)
                     citation_dead e-new-text; citation_file_absent NEWFILE.md
```

That is R2(a) exactly: the probe passes or fails against a tree that is not the branch tip. The mechanism
is not in doubt.

### Realizability inside LANE (observation + inference)

`jj-lane.sh` `commit` is `metaedit --update-author` → `jj commit -m … -- paths` (`scripts/hyaku/jj-lane.sh:230`)
→ `hash=$(jj_ids '@-')` (`:231`) → `bookmark set "$branch" -r "$hash"` (`:233-234`) → `do_push`. So the only
HEAD-off-`main` window in the lane's sanctioned write path is between `:230` and `:233`, and the lane lock
(`take_lock`, `:84-89`, taken at `:187`) is honored only by other `jj-lane.sh` invocations — a probe run
does not take it. Direct `jj` in LANE is forbidden (`contract.md:20`). Conclusion: **R2(a) is real as a
mechanism but transient in the lane's operating model**; the audit's "any default/manual run evaluates
`@-`" overstates the steady state (HEAD == `@-` == `main` after the helper returns, as measured here and
in the audit's F1). It remains worth fixing because manual `--rev HEAD` runs are common in this lane's
history (e.g. `.ufo/waves/round-17/w1/DraftReadmeRow.md:21`) and the window is real.

Inference: the contract's rule ("literal `--rev HEAD` accepted only when HEAD **equals** the branch tip",
`contract.md:75-76`) is strictly better than the audit's "refuse when HEAD is not an ancestor"
(`JjAuditKaidoku.md:166`): an older detached HEAD is an ancestor of an advanced `main`, and an ancestry
test would accept it while reading a stale tree. Keep the equality rule.

## 4. R2(b) — not a jj risk (observation)

Plain git, no jj anywhere: one commit, then an untracked `NEWFILE.md`, table cites it at line 1.

```
$ probe --root <plain repo> --rev HEAD
CITATION_DRIFT: citation_file_absent entry=NEWFILE.md absent at HEAD
CITATION_DRIFT_VERDICT: reported findings=2 exit=0
```

Identical to the jj sandbox because the probe reads Git objects (`git show <rev>:<path>`), never the
worktree. Under the lane's "landed = committed" semantics this is a **true red**, not a false one; it only
misleads a pre-commit manual run. The audit's own remedy is documentation, and `contract.md:73-77` omits
it. Low severity, but the C2 claim's prose ("two concrete effects under jj") should not carry (b) as a jj
effect.

Also observation: `.ufo/waves/round-18/` is untracked and `git ls-tree -r 9011581 -- .ufo/waves/round-18`
returns 0 paths; `pointer-table.json` has 0 round-18 entries. So no current pointer entry can trigger (b)
today.

## 5. Minimal change — the contract's fix, prototyped in the sandbox

`contract.md:73-77` is the minimal change and preserves explicit-rev behaviour: `--rev` loses its default;
omitted → `refs/heads/<branch>^{commit}` (`--branch`, default `main`); literal `HEAD` accepted only when it
equals that tip, else exit 2 `head_not_branch_tip`; output records `rev_requested`, `rev_resolved`,
`branch`; explicit revisions pass through untouched. The essential resolution is ~12 inline lines plus a
`report()` signature change — no new abstractions needed.

Prototype (`/tmp/revbase-r2-j9clqygg/patched-probe.py`, 545 vs 499 lines, sandbox only) verified:

| case | observed |
|---|---|
| off-branch, no `--rev` | `REVISION: ba6dd215…` (tip), `reported findings=0 exit=0` |
| off-branch, `--rev HEAD` | `head_not_branch_tip`, `could-not-evaluate … exit=2` (with and without `--strict`) |
| off-branch, `--rev refs/heads/main` | `reported findings=0 exit=0` |
| off-branch, explicit 40-hex | findings/verdict identical to baseline |
| LANE, no `--rev` | `REVISION: 9011581d…`, findings=0 |
| LANE, `--rev HEAD` (HEAD == tip) | `REVISION: 9011581d…`, findings=0 (accepted) |
| LANE, `--rev 9011581d… --strict` | `clean findings=0 exit=0` (registered argv unchanged) |
| patched `--selftest --expected LANE/…/expected.json` | `CLEAN cases=13 passed=13 failed=0 exit=0` |
| baseline `--selftest` | `CLEAN cases=13 passed=13 failed=0 exit=0` |

## 6. Findings for the C2 owner

**D1 (medium, observation) — exit 2 requires adding the two ids to the CNE set.** `Findings.verdict()`
maps exit 2 only for the fixed tuple at `citation-drift-probe.py:80-84`. A prototype with correct
resolution but without touching that tuple returned `reported … exit=0` for `head_not_branch_tip` (and
would return 1 under `--strict`), not the contract's exit 2. Add `branch_missing` and
`head_not_branch_tip` to `:80-84`.

**D2 (medium, observation) — the two new selftest cases need a harness extension.** `selftest()` calls
`run_check(root, rev, …)` directly with `rev = "HEAD"` (`:451-453`); `expected.json` carries 13 flat
`(case, exit_code, finding)` rows; `build_fixture()` (`:347-368`) only mutates fixture content. Nothing in
that path reaches `main()` or a resolution helper, so "add the two new cases" (`contract.md:77`) requires a
CLI-level case (subprocess of the probe) or a direct resolver unit case. Two traps: (i) fixtures are
`git init -q` and this host's `init.defaultBranch` is `master`, so any `main()` fixture must use
`git init -b main` or pass `--branch master`; (ii) a copied probe's `--selftest` default `--expected`
resolves next to the copy (`HERE`, `:60-62`), so the copy must be given `--expected` — observed as
`selftest_table_unreadable` before I passed it. Also note the contract's "existing selftest cases keep
their exits" is satisfied trivially, because those cases bypass `main()` entirely.

**D3 (medium, inference) — the C2 metric `live_count 3 -> 0` is probably unattainable as specified.**
`head-rev-lint.py`'s `rev-parse-HEAD` kind is defined syntactically as "a git argv with `rev-parse` and
literal `HEAD` as a revision" (`contract.md:63-65`), while every prescribed fix must still read HEAD to
*validate* it: the probe's resolver, `verify.py`'s "exit 2 unless HEAD equals the branch tip"
(`contract.md:83-84`), and `custody-pair`'s `repo-HEAD-is-branch-tip` (`:79-80`). A literal-argv scanner
will count those comparison reads. The distinction the contract intends is semantic ("validates", not
"uses", cf. the already-landed `revpin.py` docstring), so the lint needs a narrowing rule or allowlist, or
`claims.json:20` must state the metric differently (e.g. `default-HEAD` sites 1 → 0, or HEAD-as-evaluated-
revision). Label INFERENCE: `head-rev-lint.py` does not exist yet; only `revpin.py` had landed at
measurement time. This does not change the probe fix itself.

**D4 (low, observation) — keep `root_ok` before branch resolution.** With the root guard stripped, a
non-repo `--root` produced `branch_missing … exit=2` instead of the baseline's `root_unreadable … exit=2`
(both observed; guarded prototype and baseline both emit `root_unreadable`). Exit is unchanged but the
documented finding id changes (`SKILL.md:448` registers could-not-evaluate classes), so resolve only after
`root_ok`, or pass the requested rev through untouched when the root is not a repo.

**D5 (low, calibration) — R2(b) needs the audit's documentation remedy, not code.** See §4. If C2 wants
the (b) text to be true, add one line to the probe's output or `SKILL.md` row noting that revision-scoped
checks cannot see untracked/uncommitted paths by construction under `snapshot.auto-track="none()"`.

## 7. Residual risk and verification gaps

- The probe's default pins **local** `refs/heads/main`, not pushedness. A helper run that commits and fails
  to push (exit 3) leaves local `main` ahead; a default probe run would then attest an unpushed tip.
  Pushedness is `verify.py`/`revpin.resolve_source(require_pushed=True)`'s remit (`contract.md:52-56`,
  `:83-85`), not R2's, but the probe should not be described as pinning "the landed tree".
- I did not run `head-rev-lint.py` or `jj-red-before.py` (neither existed at measurement); D3 is therefore
  inference from contract text. I did run the C2 tool that exists: `revpin.py --root LANE` →
  `{branch: main, source: 9011581…, head: 9011581…, head_equals_source: true, remote: 9011581…,
  pushed: true}`, exit 0.
- Lane state was sampled twice while siblings wrote (`tracked 0 → 1`); probe bytes were confirmed equal to
  the `9011581d` blob by `cmp` (exit 0), so §1-§5 are anchored to that blob.
- No tool installs were needed or made.
