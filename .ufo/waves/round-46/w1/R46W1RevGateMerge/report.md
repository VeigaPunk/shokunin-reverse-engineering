# R46W1RevGateMerge — evidence dossier (merge arm of the round-46 freeze core)

Scoped findings for the L1: `.ufo/waves/round-46/w1/R46W1RevGateMerge.md`.
This file is the reproduction record: method, scripts, the full shape table, and the
receipt inventory.

## Method

1. Read `plans/round-46-claims.md` and `tools/round-46/gate.py` at the freeze commit
   `31820472784284727546808acc31b3ea1e73919b` (not the worktree, which has moved).
2. Extracted the freeze-commit bytes of `gate.py` with
   `git -C <LANE> show <FREEZE>:tools/round-46/gate.py` into `gate_frozen.py`
   (`sha256:64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e`),
   plus the claims file (`sha256:a09564e0…`) and the other frozen files, and imported the
   module directly, so the tests measure the frozen instrument rather than a copy of prose.
3. Built each fixture under `$HYAKU_SCRATCH/fx/<name>` with
   `git init -q -b main`, a local identity, `commit.gpgsign=false`, a verified
   `rev-parse --show-toplevel == <fixture>`, and every later call as `git -C <fixture>`.
   The freeze commit is the fixture's initial commit (claims file + `tools/round-46/*` +
   `notes.txt`), exactly mirroring the lane's frozen set (`plans/round-46-claims.md` and the
   directory `tools/round-46/`).
4. Called `gate.freeze_state(root, freeze, tip)` on each and recorded
   `{exit, touched, blob_changed, restored, frozen_path_changed}`, plus a per-commit
   `git log -m --diff-merges=first-parent --name-status --format='%h %s'` breakdown so the
   detecting commit is named.
5. Cross-checked at counter level with the frozen `attest.py` / `registry.py` binaries, and
   at lane level with `lane_probe.py` (four candidate freeze bases × HEAD, read-only).

Every recorded step carries `{cmd, cwd, exit, stdout_sha256, utc}`. Exit codes are semantic:
0 clean/met, 1 violation, 2 could-not-evaluate.

## Files in this directory

| file | sha256 | role |
|---|---|---|
| `drive_gate_merge.py` | `b8f32c04…` | main battery: a1, a2, a3, b, c, c2, d, d2, e, f, g, h, i, j, k |
| `extras.py` | `b5f59723…` | adjacent probes: m (amend), n (dirty), o (squash resolution restore) |
| `lane_probe.py` | `a599d3fa…` | four freeze bases at HEAD, both frozen counters, the landed CL19 row |
| `gate_frozen.py` | `64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` | byte copy of the frozen `gate.py` under test |
| `receipts.json` | `b0925c7a…` | 355 receipts from `drive_gate_merge.py` |
| `lane_receipts.json` | `486bd86a…` | lane-level receipts at HEAD `deee6595` |
| `extras_receipts.json` | `f2deb73b…` | receipts for m, n, o |

Run pattern (scratch removed afterwards):

```sh
export TMPDIR=<SCRATCH> HYAKU_SCRATCH=<SCRATCH>
python3 -I -B drive_gate_merge.py && python3 -I -B extras.py && python3 -I -B lane_probe.py
```

## Shape table (frozen gate bytes)

`restored` shown where non-empty; "WRONG" marks the F2 mislabel.

| # | shape | expected | exit | touched | blob_changed | restored |
|---|---|---|---|---|---|---|
| a1 | conflict on the frozen file, both sides edited it, resolution restores freeze bytes | 2 | 2 | `tools/round-46/gate.py` | `[]` | `[gate.py]` |
| a2 | one-sided frozen edit, clean auto-merge, merge resolution reverts it | 2 | 2 | `[gate.py]` | `[]` | `[gate.py]` |
| a3 | conflict on `notes.txt`, one-sided frozen edit, resolution restores it | 2 | 2 | `[gate.py]` | `[]` | `[gate.py]` |
| b | same conflict, resolution keeps the tampered bytes | 2 | 2 | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` WRONG |
| c | squash folds a branch tamper+restore away | 0 | 0 | `[]` | `[]` | `[]` |
| o | squash, resolution restores the bytes | 0 | 0 | `[]` | `[]` | `[]` |
| c2 | control: squash folds an unrestored tamper | 2 | 2 | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` WRONG |
| d | fast-forward, nothing frozen touched | 0 | 0 | `[]` | `[]` | `[]` (0 merge commits) |
| d2 | control: fast-forward carrying a tamper | 2 | 2 | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` WRONG |
| e | merge's own resolution adds the frozen edit (R45-CL6) | 2 | 2 | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` WRONG |
| f | tamper, then a later commit restores, no merge | 2 | 2 | `[gate.py]` | `[]` | `[gate.py]` |
| g | merge resolved on the side branch; main fast-forwards to it | 2 | 2 | `[gate.py]` | `[]` | `[gate.py]` |
| h | merge whose second parent predates the freeze | 0 | 0 | `[]` | `[]` | `[]` |
| i | `git merge -s ours` discards the tamper | 2 | 2 | `[gate.py]` | `[]` | `[gate.py]` |
| j | rename inside the frozen dir | 2 | 2 | `[tools/round-46/census.json]` | `[tools/round-46/]` | `[census.json]` WRONG |
| k | rename into the frozen dir from outside | 2 | 2 | `[tools/round-46/thing.py]` | `[tools/round-46/]` | `[thing.py]` WRONG |
| m | tamper commit rewritten by `commit --amend --allow-empty` | not claimed | 0 | `[]` | `[]` | `[]` |
| n | uncommitted frozen tamper | row says 1 | 0 | `[]` | `[]` | `[]` |

Detector attribution (from the per-commit breakdowns):

- `a2`: `git diff HEAD^1 HEAD` is **empty**; only the side commit (`side: edit frozen gate.py`)
  names the path. The restore is invisible in the merge itself, as predicted.
- `e`: the merge commit is the only commit naming the path; the round-45 argv
  (`git log --name-only`, no `--diff-merges`) emits **nothing** (`sha256:e3b0c442…`, the
  empty-string digest). This is the R45-CL6 closure, measured.
- `c`: the squashed commit's own diff is `M notes.txt` only; `git diff --quiet FREEZE TIP --
  plans/round-46-claims.md tools/round-46/` exits 0 (identical trees). The branch ref was
  still present, so reachability is not the reason the tamper is invisible.
- `h`: `v2_exact` and `without_dash_m` both produce **zero** bytes; `--diff-merges=separate`
  produces six frozen paths. That is the F3 false positive, one flag away.
- `j`: the rename's status is `R100 old new`; `touched` records only the old path.
- `k`: with the pathspec confined to `tools/round-46/`, git reports `A tools/round-46/thing.py`
  (not an `R`), so nothing outside the frozen scope leaks into `touched`.

## Counter-level receipts

Frozen `attest.py` / `registry.py` (extracted from the freeze commit) over the fixtures:

```
$ python3 -I -B frozen-tools/attest.py --root fx/a1-conflict-frozen --freeze <a1-F> --rev <a1-tip>
{ "counter": "round-46-c1", "reason": "frozen_path_changed",
  "frozen_path_changed": ["tools/round-46/gate.py"], "blob_changed": [],
  "restored": ["tools/round-46/gate.py"], "touched": ["tools/round-46/gate.py"], … }
EXIT=2                                   # no met_target

$ python3 -I -B frozen-tools/attest.py --root fx/c-squash-fold --freeze <c-F> --rev <c-tip>
{ "counter": "round-46-c1", "reason": "SKILL.md absent at rev" }
EXIT=2                                   # freeze gate was CLEAN; the counter moved on
```

The same shape holds for `registry.py` on `fx/c-squash-fold`.

(`frozen-tools/` is assembled with `git -C <LANE> show <FREEZE>:tools/round-46/<file>` for
`gate.py`, `attest.py`, `registry.py`, `census.py` and `census.json`, then `chmod +x` the
`.py` files; it lives in scratch only.)

Lane at HEAD `deee6595ae3dda094aa5a577fac0f6903e873e16` (measured 2026-10-28T17:04:46Z; HEAD moved
four times during the seat: `781e19ae` → `49e6cac` → `21b55a8f` → `deee6595`):

| base | exit | frozen_path_changed |
|---|---|---|
| `3182047…` | 2 | `tools/round-46/`, `attest.py`, `gate.py`, `registry.py` |
| `50862e4a` | 2 | `attest.py`, `registry.py` |
| `65678df0` | 2 | `registry.py` |
| `04252247` | 0 | `[]` |

```
attest.py    exit 2  reason frozen_path_changed  met_target absent  stdout sha 3a471c33…
registry.py  exit 2  reason frozen_path_changed  met_target absent  stdout sha dec44f87…
```

`restored` at that HEAD names `attest.py`, `gate.py`, `registry.py` — the same paths as
`frozen_path_changed` (F2 on the real lane).

Landed row under test, `SKILL.md:624` at `deee6595` (was `:617` at `781e19ae`):

Wrapped here for width; the file has it as one line:

```
| R45-CL19 a tamper-then-restore folded away by `git merge --squash` | the surviving history names nothing | blob: the blob arm still compares the two revisions; the limit is stated in the table, not claimed away | 2 |
```

Corroborating literal in the instrument's selftest fixture, `tools/round-46/attest.py:516`:
`("R45-CL19", "squashed side branch is invisible", "blob", "2")`.

## Corrections made during the seat (honest capture)

- The first `c` fixture had `main` and `side` both editing `notes.txt`, so `git merge --squash`
  exited 1 with `Recorded preimage for 'notes.txt'`. Fixed by giving `main` an unrelated
  `other.txt` change; the receipts record both the failing and the successful invocations.
- The first `m` probe ran `git commit --amend --no-edit`, which **exited 1**: "You asked to
  amend the most recent commit, but doing so would make it empty." The recorded result at that
  point was the *tamper kept* case (exit 2), not an amend. Re-ran with `--allow-empty`, which
  is the real amend shape (exit 0). Both runs are in `extras_receipts.json` under distinct
  command lines; only the `--allow-empty` run is cited in the findings.
- The initial blob check used the result key (`b-conflict-keep-edit`) as a directory name; the
  fixture directory is `b-conflict-keep`. Corrected before the values were used.

## Boundaries

Read-only on the lane: no writes outside `.ufo/waves/round-46/w1/R46W1RevGateMerge{,md}`; no
git/jj mutation in the lane; fixtures and all git writes confined to
`/fast/scratch/hyaku/kaidoku-r46/R46W1RevGateMerge` (removed after the receipts were copied).
No tool installs. No subagent dispatch.
