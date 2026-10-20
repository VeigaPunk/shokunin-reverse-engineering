# ConnFleetJjPractice — how sibling lanes pin revisions under jj (read-only)

Round 18, connector seat. Scope: sibling `*-shokunin` repos + the fleet-level hyaku tooling, read-only.
No REA, no carrier execution, no `jj`, no git write. Time of measurements: 2026-10-20T15:2xZ.
Labels: **[OBS]** = command output read here; **[INFER]** = my reading, not executed.

## 0. Bottom line

**[OBS] No sibling lane has yet migrated a *live* HEAD-keyed revision pin to a branch ref.** The
working patterns exist in exactly two places: the fleet helper `scripts/hyaku/jj-lane.sh`
(+ its *uninstalled* `.new` variant) and `souji-shokunin`'s pushed-receipt resolver. Every other
lane still ships `rev-parse HEAD` in live tooling, including the two lanes whose own jj audits named
the exact fix. Kaidoku's C2 would therefore be the first lane-level implementation, and the reusable
material is fleet-level, not peer-lane.

## 1. Evidence

### 1.1 No live code uses a branch ref

Command (per repo, tracked files, reports/corpus/.ufo excluded):

```
$ git grep -l 'refs/heads' -- ':(exclude)reports/**' ':(exclude)corpus/**' \
    ':(exclude).ufo/**' '*.py' '*.sh' '*.mjs'
```
[OBS] Non-empty results only:
- `souji-shokunin` — `tools/*.sh` (fixture plumbing at `symbolic-ref HEAD refs/heads/...`,
  `branch=${branch#refs/heads/}` at `tools/souji-verify.sh:346,805`) plus `tests/fixtures/*`
- `kotodama-shokunin/tools/harness/receipt_guard.py` — `.git/refs/heads/control` **fixture writes**
  (`:175,197,331,334,341`), not pin resolution.

The table's two remaining non-souji hits are also non-pins: kaidoku's is a `.ufo` fixture
(`.ufo/waves/arc3-loop1-round1/claims/c2/CR-4/evidence/run-all.sh:63` `git update-ref refs/heads/sim-census`),
tabi's is `scripts/selftest-measurement-binding.mjs:377` `update-ref refs/heads/-x` (the
`--end-of-options` red fixture).

File-count census (files with ≥1 match; `headP` = `rev-parse … HEAD`, `refsH` = any `refs/heads/`,
`anc` = `merge-base --is-ancestor`, `lsr` = `ls-remote`). Exact loop, run at 15:2xZ, rc=0
(`wc -l` always succeeds; per-repo `git grep` returned 0 or 1):

```sh
for d in */; do d=${d%/}; [ -d "$d/.git" ] || continue
  h=$(git -C "$d" grep -l -E 'rev-parse [^|]*HEAD' -- '*.py' '*.sh' '*.mjs' | wc -l)
  r=$(git -C "$d" grep -l -E 'refs/heads/'           -- '*.py' '*.sh' '*.mjs' | wc -l)
  a=$(git -C "$d" grep -l 'merge-base --is-ancestor' -- '*.py' '*.sh' '*.mjs' | wc -l)
  l=$(git -C "$d" grep -l 'ls-remote'                -- '*.py' '*.sh' '*.mjs' | wc -l)
  printf '%-24s %5s %5s %5s %5s\n' "$d" "$h" "$r" "$a" "$l"
done
```

| repo | headP | refsH | anc | lsr |
|---|---|---|---|---|
| audio | 21 | 0 | 0 | 0 |
| mori | 32 | 0 | 0 | 0 |
| mado | 6 | 0 | 0 | 0 |
| kaidoku | 33 | 1 | 1 | 0 |
| souji | 41 | 124 | 76 | 1 |
| game-dev-3d | 2 | 0 | 0 | 2 |
| game-dev-2d | 2 | 0 | 0 | 0 |
| tabi | 2 | 1 | 0 | 0 |
| kotodama | 2 | 1 | 0 | 0 |
| kotoba | 2 | 0 | 0 | 0 |
| kama | 1 | 0 | 0 | 0 |
| kengaku | 1 | 0 | 0 | 0 |
| lore | 1 | 0 | 0 | 0 |
| tameshi | 2 | 0 | 0 | 0 |

[OBS] Concrete unfixed sites, still at each repo's current commit:

```
$ git -C kake-shokunin grep -n -e "rev-parse', 'HEAD" -e "origin/main..HEAD" -- scripts/freshness-sweep.mjs
scripts/freshness-sweep.mjs:701:      gate.head = g(['rev-parse', 'HEAD']);
scripts/freshness-sweep.mjs:702:      gate.unpushed = Number(g(['rev-list', '--count', 'origin/main..HEAD']));
scripts/freshness-sweep.mjs:854:    pq2.head = g(['rev-parse', 'HEAD']);
scripts/freshness-sweep.mjs:855:    pq2.unpushed = Number(g(['rev-list', '--count', 'origin/main..HEAD']));
rc=0
```

- kake already reads the **true** remote tip (`scripts/freshness-sweep.mjs:700` `ls-remote origin main`)
  and then compares it to `rev-parse HEAD` and counts `origin/main..HEAD`. This is the "half-fixed"
  anti-pattern: remote truth acquired, local referent still wrong.
- `tabi-shokunin/scripts/check-round-contract.mjs:231-233` — `rev-parse HEAD` + `merge-base --is-ancestor baseline HEAD`.
- `game-dev-3d-shokunin/corpus/knowledge/unreal-mcp/gate/run_gate.sh:98` (`LANE_HEAD=$(… rev-parse HEAD)`),
  `:210`, `:229`, `:231` (`git ls-files`) — its own audit prescribed the fix at `JjAuditGameDev3d.md:52-59`.
- `kotodama-shokunin/tools/harness/receipt_guard.py:69` — `rev-parse --verify --quiet HEAD^{commit}`.
- `tameshi-shokunin/tools/pin-disposition.py:318` — same. Its round-17 rewrite
  (`.ufo/waves/round-17/staged/tools/pin-disposition.py:43-51`) *documents* the branch ladder
  ("`refs/remotes/origin/HEAD`, then `refs/heads/master`, then `refs/heads/main`") but still calls
  `HEAD^{commit}` at `:328`; the whole `round-17/` directory is untracked (`?? .ufo/waves/round-17/`).
  [INFER] tameshi wrote the contract text one round before the code.

### 1.2 Where the working pattern does live

**Fleet helper, current** — `scripts/hyaku/jj-lane.sh`:

```
$ git -C kaidoku-shokunin rev-parse -q --verify 'refs/heads/main^{commit}'
9011581d84527ba34c675f9cf912e54d2e72d470          rc=0
$ git -C kaidoku-shokunin rev-parse -q --verify 'refs/remotes/origin/main^{commit}'
9011581d84527ba34c675f9cf912e54d2e72d470          rc=0
```

- `jj-lane.sh:53-65` `detect_branch`: attached `symbolic-ref` → `refs/remotes/origin/HEAD` →
  `refs/heads/master` → `refs/heads/main` → first local branch. Never `@{u}`, never `--abbrev-ref`.
- `jj-lane.sh:71-75` state line: both sides read from **full refs**, and `ahead`/`behind` are
  `rev-list --count refs/remotes/origin/$b..refs/heads/$b` — branch-vs-branch, HEAD never enters.
- `jj-lane.sh:155` sets `revset-aliases."trunk()" = "<branch>@origin"`.

**Fleet helper, `.new` variant** (written today 12:01, *not installed*; `inline.sh` still names
`jj-lane.sh`, mtime 11:08):

- `:160-163` validates **both** refs as `^[0-9a-f]{40}$` and exits 1 otherwise — an absent or
  non-hash ref cannot become a comparison operand.
- `:225-249` `report_landed`: `git ls-remote origin refs/heads/$b` is the authoritative remote tip,
  must equal the local tip, and this run's commit must be its ancestor; prints exactly one citable
  `landed <hash>` (and `rewritten <old> -> <new>` when push recovery rebased it).
- `:371-373` refuses to colocate when HEAD is detached on a non-tip commit
  (`git rev-parse -q HEAD != refs/heads/$branch`).
- `:494-507` commit path resolves the commit target from `refs/heads/$branch`, not HEAD.
- `:273-277` records the pre-fetch remote tip from `refs/remotes/origin/$b`, fetches, re-reads, and
  refuses a remote that moved sideways or backwards.

**Fleet doctrine, this phase:** `scripts/hyaku/inline.sh:33-34` ("never read `@{u}`/HEAD for lane
state"), `scripts/hyaku/lane-addendum.md:136-139` ("read the lane tip with `git rev-parse <branch>`"),
`scripts/hyaku/closure-prompt.md:23-24` ("test ancestry against the branch ref, never `@{u}`") and
`:54` (confirm with `git ls-remote origin refs/heads/<branch>`).

**souji's pushed-receipt resolver** — `souji-shokunin/tools/souji-verify.sh:139-159`:

1. `symbolic-ref --quiet --short refs/remotes/origin/HEAD` → `refs/remotes/origin/<b>`;
2. else if exactly one `refs/remotes/origin/*` exists, use it;
3. else return 1 with the comment *"Local refs (refs/heads/master) can NEVER establish a pushed
   receipt."*

Callers then require `merge-base --is-ancestor "$intro" "$ref"` (`:238`) **and** presence of the
path at that ref (`rev-parse --verify "$ref:$rel"`, `:854,892,943`) — ancestry alone is not treated
as byte evidence. This is the strongest match to C2's `require_pushed`.

### 1.3 Live colocation snapshot (why the window is real)

`symbolic-ref -q HEAD` / `rev-parse -q --verify HEAD` / branch tip, per lane:

| lane | `.jj` | HEAD | branch tip |
|---|---|---|---|
| kaidoku | yes | DETACHED (`rc=1`) | 9011581d… = HEAD |
| kama | yes | DETACHED (`rc=1`) | cff9e62f… = HEAD |
| tameshi | yes | DETACHED (`rc=1`) | 98bea7da… = HEAD |
| mado | yes | DETACHED | d9a5a18e… = HEAD |
| tabi | yes | attached `refs/heads/master` | 1205d261… = HEAD |
| other 16 | no | attached | HEAD = tip |

[OBS] mado's HEAD was `0ab1ccc` at 15:2x and `d9a5a18` in the next probe minutes later — a lane
commit landed mid-measurement. [INFER] Any resolver that reads HEAD and the branch in two separate
`git rev-parse` calls on a *live* lane can observe a commit between them and report a false
`head_not_branch_tip`.

### 1.4 `rev-parse` failure semantics (probed, read-only)

```
$ git rev-parse --verify HEAD refs/heads/main
stderr: fatal: Needed a single revision                     rc=128
$ git rev-parse HEAD refs/heads/main refs/remotes/origin/main
9011581d… \n 9011581d… \n 9011581d…                          rc=0
$ git rev-parse refs/heads/__nope__
refs/heads/__nope__            (stdout echoes the unresolved name)   stderr: unknown revision   rc=128
$ git rev-parse --verify refs/heads/__nope__
stderr: fatal: Needed a single revision                    rc=128
$ git rev-parse HEAD refs/heads/__nope__
9011581d… \n refs/heads/__nope__        (partial stdout, then the literal)   rc=128
```

[OBS] `--verify` cannot take two revisions. A multi-ref `rev-parse` resolves all three in one process
but on failure leaves a **positional prefix** on stdout with the unresolved ref's *name* in a hash slot.
[INFER] This is exactly why `jj-lane.sh.new:162-163` insists on a 40-hex shape check; a resolver that
splits stdout by line and trusts it would record the literal string `refs/heads/main` as a commit.

### 1.5 Pitfalls with sibling evidence

- **Cloning a colocated worktree lands detached.** `JjAuditGameDev3d.md:149-155`: `git clone
  work clone-from-coloc` → "Note: switching to '14d6074…'", `symbolic-ref -q HEAD` rc=1, while
  `main=35919d1`. The bare-remote control (`:157-163`) is attached and clean. C2's `jj-red-before.py`
  builds its sandbox with `git clone --no-local LANE sb`; kaidoku is detached *right now* (1.3), so
  **[INFER]** `sb` will start detached and `jj git init --colocate` may then behave like the
  `refs/jj/root` case below rather than a `main` branch.
- **A missing branch ref reads as "pushed".** `JjAuditClosurePrompt.md:78-89`: `state branch=jj/root
  local=- remote=- ahead=0` while `refs/heads/master ABSENT`; `detect_branch` returned `jj/root`
  because HEAD was attached to `refs/jj/root`. `ahead` defaults to 0 when either ref is absent.
  [INFER] C2's `remote: null` parenthetical is the same trap one level up: `remote is None` must
  produce `branch_not_pushed`, never `pushed: true`.
- **`git status` mutates the index it reports on.** `JjAuditGameDev3d.md:139-146` (E4): after a jj
  mutation the first `git status` changes `.git/index` bytes; `--no-optional-locks` leaves them
  unchanged. The fleet's own gates were told to add it (`JjAuditSouji.md:392`).
- **`git ls-files` is index-addressed.** `game-dev-3d …/run_gate.sh:231` and the audit row
  `JjAuditGameDev3d.md:58`; the jj-safe form is `ls-tree -r --name-only <rev>`.
- **`rev-parse --show-toplevel` / `--git-dir` are not HEAD reads** and are safe (`mori-census.sh:2129`
  `rev-parse --git-dir`, `:2197` `rev-parse --verify -q HEAD`; the first is fine, the second is a
  HEAD-existence probe). mori also scrubs the environment:
  `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C "$repo" …` — [INFER]
  the same scrub belongs in any `revpin` that takes a `--root` from the caller.
- **`--end-of-options`** is already the sibling idiom for a caller-supplied revision:
  `tabi-shokunin/scripts/check-measurement-binding.mjs:232` (`rev-parse --verify --end-of-options
  ${text}^{commit}`), with the red fixture `refs/heads/-x` at `:377`.

### 1.6 In-flight kaidoku bytes (context, not a sibling claim)

`.ufo/waves/round-17/verify.py` is ` M` in the working tree (`git status --porcelain`); baseline
`9011581` still has `source = git("rev-parse","HEAD")` at `:59`. The working tree now has
`resolve_source()` at `:66-87`: `rev-parse --verify refs/heads/{branch}^{commit}`, `remote=None` on
`CalledProcessError`, findings `head_not_branch_tip` / `branch_not_pushed` / `worktree_dirty`.
Two observations:
- HEAD is read with `git log -n 1 --format=%H` ("so no `rev-parse HEAD` revision site is reintroduced",
  `:67-68`). [OBS] `head-rev-lint.py`'s four site kinds do not cover `git log`/`show`/`cat-file` with
  no revision operand, all of which default to HEAD. [INFER] a lint-reported `live_count: 0` is a
  statement about *syntax*, not about "no HEAD-keyed reads".
- `git status --porcelain --untracked-files=no` is called without `--no-optional-locks`, so the
  "read-only" pass rewrites `.git/index` in a colocated lane (1.5).

## 2. Affected axes

- **operability (C2, primary):** removes the torn read on a live lane and makes finding attribution
  unambiguous.
- **calibration (C1/C2, secondary):** the lint's coverage claim becomes honest only if the exclusion
  of `git log`/`show` is stated or the kind is added.
- **depth (C3):** neutral. No carrier bytes, predictions, or Ghidra surface involved.

## 3. Proposed move (one)

**In `revpin.resolve_source`, read HEAD, `refs/heads/<branch>` and `refs/remotes/origin/<branch>` in a
single `git rev-parse` argv, validate every output line as `^[0-9a-f]{40}$`, and use `--verify`
per ref only to attribute a failure.**

Shape:

```python
def _refs(lane, branch):
    specs = ["HEAD", f"refs/heads/{branch}", f"refs/remotes/origin/{branch}"]
    p = run(lane, ["rev-parse", *specs])                 # no --verify: it takes one rev
    if p.rc == 0:
        lines = p.out.splitlines()
        if len(lines) == 3 and all(HEX40.fullmatch(x) for x in lines):
            return dict(zip(("head", "branch", "remote"), lines))
    # attribution only: one --verify per ref, in fixed order
    head   = _verify(lane, "HEAD")                       # absent -> head_not_branch_tip (head != source)
    src    = _verify(lane, f"refs/heads/{branch}^{{commit}}")            # absent -> branch_missing
    remote = _verify(lane, f"refs/remotes/origin/{branch}^{{commit}}")   # None if absent
    ...
```

Why this and not the obvious form: it is the only compatible synthesis of the two sibling patterns —
the `.new` helper's 40-hex gate (`jj-lane.sh.new:162-163`, which exists *because* `rev-parse` echoes
unresolved names, probed in 1.4) and the multi-ref single-invocation form (`JjDocPush.md:345`). It
costs ~10 lines over three `--verify` calls and removes a measured race (1.3) rather than a
hypothetical one.

Findings stay exactly the contract's three; `remote is None` **must** raise `branch_not_pushed`
(1.5, `JjAuditClosurePrompt.md:78-89`), and a non-40-hex line is `branch_missing`, never a silent
`source`.

## 4. Risks

1. **`refs/remotes/origin/<branch>` is fetch-scoped.** [OBS] `JjDocRecovery.md:629` warns that
   `heads(<branch>@origin)` must not be cited without a preceding fetch; [OBS] `JjDocPush.md:350-351`
   shows jj exports the ref immediately after a push. [INFER] `pushed: true` is therefore "as of the
   last fetch/export", not "as of the remote". Keep `ls-remote` out of the default path (no-network
   contract) and say so in the output (`remote_scope: "fetch"` or a `limits` row).
2. **`jj-red-before.py` sandbox shape.** If `sb` is cloned from a detached LANE (kaidoku is detached
   now), attach it before colocating — `git clone --branch main`, or `git -C sb checkout -B main
   refs/heads/main` — and assert `symbolic-ref -q HEAD` = `refs/heads/main` before
   `jj git init --colocate`. Otherwise step (4)'s expected `head_not_branch_tip` may never be
   reachable and step (1) measures the wrong baseline (1.5, E5/E6).
3. **Concurrent lane commits.** `require_head=True` on a lane under active commit can refuse
   legitimately (mado moved mid-probe). Expected for the post-integration pass (lane quiescent);
   document it so a future caller does not read the refusal as a defect.
4. **Lint coverage.** If `head-rev-lint.py` keeps the four kinds, its `live_count: 0` must be stated
   as "no `HEAD`-as-argument sites", and the `git log`/`show`/`cat-file` default-rev class recorded
   as a known exclusion (1.6). Adding a fifth kind would also flag the new `verify.py` line, which
   the round does not want to fail.

## 5. Verification (for the main agent; not run here)

1. `python3 -I -B .ufo/waves/round-18/tools/revpin.py --root <LANE>` → exit 0, `head == source ==
   remote`, three equal 40-hex values. Cross-check the same three values with
   `git -C <LANE> rev-parse HEAD refs/heads/main refs/remotes/origin/main` (observed rc=0 today).
2. Selftest red cases: absent `refs/remotes/origin/main` → `branch_not_pushed` (not `pushed: true`);
   absent `refs/heads/main` → `branch_missing`; off-branch detached HEAD → `head_not_branch_tip`;
   a ref whose `rev-parse` output is not 40-hex → `branch_missing`.
3. `jj-red-before.py` → `all_held`, with the `sb`-attach assertion from risk 2 in place.
4. `head-rev-lint.py --root <LANE> --rev <REV> --strict` → `live_count: 0`, and the output states the
   default-rev exclusion (risk 4).

Tool installs: none. No package manager, `uv`, `npx`, or `~/.local/bin` changes were made.
