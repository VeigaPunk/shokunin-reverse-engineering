# RevpinModule — round-18 wave-1

Seat: `KaidokuR18.RevpinModule` (leaf, author-side advisory).
Scope: implement `.ufo/waves/round-18/tools/revpin.py` (module + CLI) per
`.ufo/waves/round-18/contract.md:51-59` ("C2 — jj-safe revision pins",
"### W18/tools/revpin.py"), honoring the jj-lane VCS rule at
`contract.md:17-21`. Selftest once, one read-only run against the lane,
explain against `scripts/hyaku/jj-lane.sh state`.

## Result: PASS — module, CLI, selftest, live lane run all green

File written: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/revpin.py`
(only file written besides this report).

### Contract conformance (observation)

- `resolve_source(lane, branch="main", require_pushed=True, require_head=True)`
  at `revpin.py:93` returns `{branch, source, head, head_equals_source,
  remote, pushed}`; resolves exactly the three contract revisions —
  `refs/heads/<branch>^{commit}` (`revpin.py:98`), `HEAD^{commit}`
  (`revpin.py:110`), `refs/remotes/origin/<branch>^{commit}`
  (`revpin.py:111`) — via `git rev-parse --verify` in `_resolve` at
  `revpin.py:79-84`; absent remote → `remote: null` (`revpin.py:115`).
- `RevPinError` at `revpin.py:60` carries `.finding` + `.result`;
  findings `branch_missing`, `head_not_branch_tip`, `branch_not_pushed`
  raised at `revpin.py:100`, `:119`, `:121`. Check order head-then-pushed
  matches the contract's selftest ordering (the detached-HEAD case must
  not be masked by a pushed check).
- CLI `revpin.py --root DIR [--branch main] [--no-require-pushed]
  [--no-require-head]` at `revpin.py:286`; JSON `sort_keys=True,
  indent=2`; exit 0 ok, 2 on finding (the emitted dict gains a
  `"finding"` key).
- Read-only git only (`rev-parse`, `merge-base`; `update-ref`/`checkout`
  appear inside mkdtemp fixtures only); never runs `jj`, never writes the
  lane.
- `pushed` is implemented as `merge-base --is-ancestor source remote`
  (`revpin.py:87-90`, used at `revpin.py:116`), not hash equality: a tip
  that is behind but fully pushed counts as pushed; ahead/diverged does
  not. [INFERENCE] — the contract says only "absent remote →
  `remote: null`" and names the finding `branch_not_pushed`;
  ancestor-containment is the reading that keeps a stale-but-pushed lane
  green, matching `jj-lane.sh`'s separate ahead/behind model
  (`scripts/hyaku/jj-lane.sh:73-75`).

### Selftest (required)

Command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/revpin.py --selftest`
Exit: `0`. Exact last line:

```
SELFTEST: CLEAN cases=11
```

11 cases over mkdtemp fixtures (real `git init` + push to a local bare
remote — no clone needed, so no `protocol.file.allow` concerns): clean
API+CLI; **red** `branch_not_pushed` (tip ahead of origin, exit 2 API and
CLI, waived green via `--no-require-pushed`); **red**
`head_not_branch_tip` (detached HEAD + off-branch commit — the jj
working-copy shape — exit 2 API and CLI, waived green via
`--no-require-head`); **red** `branch_missing` (non-repo dir and
unborn-HEAD repo); non-default `side` branch resolves. Fixtures removed
(`tempfile.mkdtemp` + `shutil.rmtree`).

### Live lane run (required)

Command: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/revpin.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Exit: `0`. Output:

```json
{
  "branch": "main",
  "head": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "head_equals_source": true,
  "pushed": true,
  "remote": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "source": "9011581d84527ba34c675f9cf912e54d2e72d470"
}
```

### Explanation vs `jj-lane.sh state`

`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state
/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (exit 0) printed:

```
state branch=main local=9011581d84527ba34c675f9cf912e54d2e72d470 remote=9011581d84527ba34c675f9cf912e54d2e72d470 ahead=0 behind=0 head=detached tracked=0 untracked=1
```

The two views agree on every shared fact — `local`/`remote`/`source`/
`head` are all the baseline `9011581d` (`claims.json:4`), ahead=behind=0,
exit 0 — with one deliberate difference: `jj-lane.sh:77` reports
`head=detached` because it tests `git symbolic-ref -q HEAD` (the
attached-vs-detached *symbolic* form), while revpin's
`head_equals_source: true` compares *commit identities*. That asymmetry
is exactly the C2 defect (`contract.md:17-18`: "Git HEAD is detached
after a helper commit; the branch tip is `refs/heads/main`"): in a
colocated lane HEAD is detached by design, so a lane tool may pin the tip
but must validate `HEAD^{commit} == refs/heads/main^{commit}` rather than
requiring an attached HEAD — which would fail on every healthy jj
working copy. `untracked=1` in the state line is this newly written
`tools/revpin.py` before lane commit; revpin intentionally ignores
working-tree dirt (custody-pair owns the `repo-dirty` metadata,
`contract.md:78-82`).

### Other commands run

| command | exit |
|---|---|
| `ls` of round-18/ and round-17/tools dirs | 0 (`round-18/tools/` absent — created by the write) |
| `bash .../jj-lane.sh state .../kaidoku-shokunin` | 0 |
| `git rev-parse --verify refs/heads/main^{commit}` + `HEAD^{commit}` + `refs/remotes/origin/main^{commit}` + `git rev-parse --symbolic-full-name HEAD` + `git status --porcelain --untracked-files=no` (read-only, in lane) | 0; all three resolve to `9011581d…`; symbolic-full-name prints `HEAD` (detached); status empty |
| `ls` + `head -20` of `w1/*.md` (peer report-format check) | 0 |
| `grep -n` for `def`/`raise` anchors inside `revpin.py` (read-only) | 0 |

### Retained evidence

- Module: `.ufo/waves/round-18/tools/revpin.py` (`RevPinError` :60,
  `_resolve` :79, `_is_ancestor` :87, `resolve_source` :93, `_selftest`
  :130, `main` :286).
- Contract anchors: `contract.md:51-59` (spec), `:8-15` (tool rules),
  `:17-21` (VCS rule).
- Comparator anchors: `scripts/hyaku/jj-lane.sh:68-82` (`print_state`),
  `:77` (detached-HEAD test), `:50-51` (colocated-HEAD rationale comment).

### Risks / blockers

- [INFERENCE] `pushed` = ancestor-containment, not hash equality (see
  above); if the L1 intended strict equality it is a one-line change at
  `revpin.py:116`. A tip strictly *behind* origin is treated as pushed —
  consistent with the lane's never-amend-pushed rule but worth a glance.
- `head` may be `null` on an unborn HEAD; `head_equals_source` is then
  false → `head_not_branch_tip` under `require_head` (the unborn-repo
  selftest hits `branch_missing` first because `source` is also absent).
- No blockers. No tools installed; stdlib + git only.

Report: `.ufo/waves/round-18/w1/RevpinModule.md`
