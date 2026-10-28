# SentFixtures — round-47 fixture hygiene (R47-C1 / R47-C2)

Seat: `SentFixtures`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Pinned measurement revision for all fixtures: `07d2894eabe88c326e9036262f20ad02662c860d`
(the A5 frozen-path commit; `c1-at-A5.json` / `c2-at-A5.json` are green there).
Scratch root `S=/fast/scratch/hyaku/kaidoku-r47/SentFixtures` (removed after receipt copy).
Receipts: `.ufo/waves/round-47/w1/SentFixtures/receipts/`, manifest
`MANIFEST.sha256` (utc `2026-10-28T18:15:13Z`). Recipes: `fixtures.py`, `counters.py`,
`probes.py` beside this file; the fixture directories themselves were removed after the
receipt copy, and the recipes recreate them from the pinned rev. No tool was installed
(git 2.56.0, python 3.14.8 preinstalled).

All work is read-only on the lane. Every fixture was a full-history clone of the lane at the
pinned rev with its own local identity (`sent-fixtures@round47.invalid`). For fixtures
F2–F5 every mutating git call carried `-C <fixture>` and re-asserted
`git rev-parse --show-toplevel` equal to the fixture dir (29/29 audited in
`fixtures-structural.json` `_meta`). Deviation, disclosed: F1 and F1b were built in a bash
block with `cd $D` and a cwd-based `git rev-parse --show-toplevel` assertion before the first
mutation, then cwd-based `git` calls rather than `-C` — the cwd was always the fixture (never
the lane) and the assertion held, but the literal `-C` rule was not followed for those two
builds. The lane was never the target of a mutating call (trace2 and the audit agree).

## Baseline (fixture reproduces the lane receipt)

Both counters, pointed at the clone with `--freeze 07d2894e --rev 07d2894e`, reproduce the
A5 result byte-for-byte at the receipt level:

| run | argv | rc | stdout sha256 |
|---|---|---|---|
| C1 baseline | `python3 -I -B tools/round-47/exact.py --root $S/F1 --freeze 07d2894e --rev 07d2894e` (battery on) | 0 | `fb40aaf4a67d73efb92dac2c11039411…` |
| C2 baseline | `python3 -I -B tools/round-47/record.py --root $S/F1 --rev 07d2894e` (battery on) | 0 | `d366b080e0112a5750edc6d169f76064…` |

`receipts/baseline-c1.json`, `baseline-c2.json`; full shas in `MANIFEST.sha256`.

## The five required fixtures

| # | fixture | construction (all at `$S/<name>`) | C1 (`exact.py`) | C2 (`record.py`) | receipt |
|---|---|---|---|---|---|
| 1 | merge with conflict resolution | `side` and `main` both edit `tools/round-47/exact.py`; merge conflicts; resolution restores the freeze blob so the endpoint **blob** arm is empty (F1b below isolates a merge that is the only frozen touch) | **2** `frozen_path_changed`, `restored:["tools/round-47/exact.py"]` | not run (tree differs only in frozen tool bytes) | `f1-c1.json`, `f1-history-arms.txt`, `f1-flag-permutations.txt` |
| 2 | rename | `git mv tools/round-47/exact.py tools/round-47/exact-core.py` + `git mv corpus/lessons/round-45.md tools/round-47/round-45-lesson.md` | **2** `frozen_path_changed` (dir blob arm) | not run | `f2-rename-tokens.txt`, `fixtures-structural.json` |
| 3 | symlink | `SKILL.md` becomes a symlink to `skill-real.md`; `probe/dangling.md` is a dangling symlink; second branch makes the frozen claims path a symlink | **2** `no '## Queue-drain craft ' section`; claims-link **2** `claims file has no '## Frozen paths (exact)' section` | **1** `mismatches 1 != 0` (axes depth `unobservable`) | `counter-runs.json`, `fixtures-structural.json` |
| 4 | submodule | `evidence/sub` is a local submodule (gitlink); variant `F4c` replaces the frozen dir `tools/round-47/` with a gitlink | outside frozen paths **0** (green, battery on); frozen-dir gitlink **2** `frozen_path_changed` | **0** (green) | `counter-runs.json` |
| 5 | bare repo | `git clone --bare` at the pinned rev | **2** `git status failed` | **0** (green) | `counter-runs.json`, `probes.json` |

Exit codes are semantic: 0 met, 1 not met, 2 could-not-evaluate. No fixture produced a silent
green on a tampered frozen surface.

### 1. Merge with conflict resolution — the arm works, but the "order" story is false

Range `07d2894e..40fe6ae6` has `blob_changed: []` for the frozen path (resolution restored the
freeze blob), so the blob arm sees nothing; the history arm sees the path and the counter
exits 2 with `restored` naming it. That is the R46-CL6 guarantee working.

Flag permutations on the cleaner evil-merge fixture `F1b` (the merge commit is the **only**
commit in the range that touches the frozen path; the branch commits touch unrelated files):

```
canonical  -m --diff-merges=first-parent   entries=1  touched=True
reversed   --diff-merges=first-parent -m   entries=2  touched=True
fp-only    --diff-merges=first-parent      entries=1  touched=True  (sha == canonical)
separate   --diff-merges=separate          entries=2  touched=True
m-only     -m                              entries=2  touched=True
none       (no merge-diff flag)            entries=0  touched=False   <-- the only blind arm
```

So a reorder does **not** blind the arm (it is a superset: `-m` last means
`--diff-merges=separate`), while dropping the merge-diff option does. And
`--diff-merges=first-parent` alone is byte-identical to the canonical pair. See finding **F-1**.

### 2. Rename — verdict safe, receipt wrong

Raw `--name-status -z` under the frozen pathspec is
`R100 tools/round-47/exact.py tools/round-47/exact-core.py` and
`A tools/round-47/round-45-lesson.md` (a cross-boundary rename is emitted as an add of the
new side). `gate.history_touched` returns
`["tools/round-47/exact.py", "tools/round-47/round-45-lesson.md"]`: the new frozen path
`tools/round-47/exact-core.py` is absent from `touched`, and `restored` names both the
renamed-away file and the added file as "restored". The verdict is still 2 because the frozen
**directory** entry's tree oid changed. No bypass found for renames; see **F-3**.

### 3. Symlink — a dangling link satisfies a `path` atom

`git show <rev>:SKILL.md` returns the link target text (`skill-real.md`), so C1 exits 2
(could-not-evaluate) and C2 turns the depth axis `unobservable` (exit 1) — a symlinked craft
file cannot fake the fraction. The frozen claims file as a symlink is also refused (2).
But a dangling symlink at `probe/dangling.md` makes `record.derive` return
`ok=True, detail={"exists": True}` even though the target is absent on disk
(`git show <rev>:probe/dangling.md` → `../../nowhere.md`, rc 0). See **F-4**.

### 4. Submodule — transparent outside frozen paths, refused inside

`git show <rev>:evidence/sub` returns rc 128 and empty stdout, so `gate.show` → `None`: a
gitlink does **not** satisfy a `path` atom (unlike a symlink). A submodule addition outside
the frozen paths leaves both counters green. `git status --porcelain` with the submodule
worktree at a different commit prints ` M evidence/sub`; `gate.dirty(root, [])` returns it,
`gate.dirty(root, ["plans/round-47-claims.md","tools/round-47/"])` returns `[]` — submodule
dirt is invisible unless it sits under a frozen path. A gitlink at `tools/round-47/` gives
`blob_changed:["tools/round-47/"]` and exit 2.
Hygiene note: `git submodule add` wrote the absolute scratch URL
(`url = /fast/scratch/hyaku/kaidoku-r47/SentFixtures/subchild`) into the fixture's
`.gitmodules` — inside scratch only, but it shows why a submodule in the lane would embed a
host path.

### 5. Bare repo — C2 works, C1 cannot

`git -C F5.git status --porcelain` → rc 128 `fatal: this operation must be run in a work tree`;
C1's `freeze_state` therefore exits 2. C2 reads only objects (`show`, `ls-tree`, `log`,
`rev-parse`, `merge-base`) and exits 0 on the bare repo, including with
`--json-out $S/F5.git/out.json` (allowed: containment is relative to `--root`).

## Extra history-shape fixture: shallow clone

`git clone --depth 1 file://<lane>` at the live tip: C1 green (`--freeze <tip> --rev <tip>`,
rc 0); C2 red, 32 mismatches (28 `rev` atoms unresolvable, one `window` correction whose
`A..B` objects are absent). Receipts `f6-shallow-c1.json`, `f6-shallow-c2.json`. C2 needs a
full-history clone; C1 needs only the tree (or a non-bare worktree when the freeze precedes
the rev). See **F-6**.

## Does the fixture's identity land anywhere outside scratch?

**No counter-emitted byte contains an absolute fixture path.** Checked all 11 counter stdout
receipts (`baseline-*`, `f1*`, `f3*`, `f6*`, `lane-*`): none contains `$S` or any `/home/`
path — they carry relative paths, oids and fractions only. Absolute paths appear only in this
seat's own wrapper receipts (`counter-runs.json` argv, `probes.json`, trace2), which the
contract requires me to copy here.

- Fixture commit oids are absent from the lane object DB:
  `git -C <lane> cat-file -e <F1|F1b|F2|F4 rev>^{commit}` → rc 128 for all four.
- `git -C <lane> grep -F $S HEAD` → rc 1 (no match); the same literal is absent from
  `SKILL.md`, `SCORECARD.md`, `plans/`, `tools/` (grep, no matches).
- `~/.config/git/config` sha256 unchanged across the session
  (`724b68916d3a7d1e1d4b353403d95672f64ad7344c062959da7f59788b1db8dd` before and after);
  `~/.gitconfig` still absent; `git -C <lane> worktree list` unchanged; no
  `kaidoku-r47-battery-*` dirs left under `$S`; no `kaidoku-r47-*` dir under `/tmp`.
- `--root` is followed through symlinks to its realpath, and `--json-out` containment is
  relative to `--root`: a symlinked root still resolves to the real fixture, an output
  outside the root is refused (2 `--json-out outside the lane root`), an output inside a
  graded head is refused (2 `inside a graded or frozen surface`), and an output inside the
  fixture root is written. So pointing `--root` at a fixture makes that fixture "the lane"
  for containment purposes — no escape from the given root, but also no protection for the
  real lane if a seat passes the wrong root.
- Observed but not caused by this seat: the lane worktree showed `M SCORECARD.md` at
  `18:04:46Z` and was clean again at `18:15:13Z`; lane HEAD advanced
  `a631bba0 → 04469ee8 → 09a9f912 → b1a058f3` during the session (L1 exports). Timestamps are
  in `pre-cross.json` / `probes.json` / `post-cross.json`.

## No `git commit` runs with a throwaway identity in the lane tree — confirmed

Static (frozen bytes, cited by line):

- `tools/round-47/exact.py:301-319` — `_repo` does `mkdtemp(dir=scratch_root)`,
  `git -C d init`, **local** `git -C d config user.email/user.name`,
  `rev-parse --show-toplevel` compared to `d` (`RuntimeError` on mismatch), then
  `git -C d add` / `git -C d commit`.
- `tools/round-47/record.py:526-547` — the selftest's repo is the only place record.py
  commits; same local-config + `-C d` pattern. `record.py:400-437` (battery) creates no repo
  and runs no commit; its only git call is `rev-list --max-parents=0`.
- `tools/round-46/gate.py` never commits; `dirty` is `status --porcelain` (line 132-137).

Dynamic:

- `GIT_TRACE2_EVENT` on a full C1 run (battery on): exactly 4 `git init` and 4 `git commit`,
  every `-C` target under `$S/kaidoku-r47-battery-*/fx-*`, zero outside scratch
  (`trace2-c1-baseline.json`, parsed summary in `probes.json`). C2 run: 0 commits.
- This seat's driver audit: 29 mutating calls, 29 under scratch (`fixtures-structural.json`
  `_meta`).
- Lane local identity is `kaidoku@shokunin.local` and was not used by any fixture commit;
  fixture authors are `round47 fixture <fx@round47>` / `SentFixtures fixture
  <sent-fixtures@round47.invalid>`. Lane HEAD/reflog moved only by L1's exports.

Environment coupling (informational): the counters read the caller's global git config and
environment. With `GIT_AUTHOR_NAME/EMAIL` and `GIT_COMMITTER_*` set, `_repo`'s commits carry
those values even though `.git/config` says `fx@round47` (probe `identity_poisoned`); without
them the local identity wins (`identity_control`). Global `init.defaultBranch`, `rerere.*`,
`filter.lfs.*` and credential helpers are read; none of it leaves scratch. See **F-7**.

## Findings (severity, exploit path, evidence, impact, remediation)

### F-1 — MEDIUM (claim rationale falsified): the "order" row's hole is not reproducible; the literal rejects a correct gate

- Exploit path: none for an attacker; the defect is in the claim's exactness rationale.
  `git log --diff-merges=first-parent -m` = `separate`, a **superset** of the canonical
  first-parent diff, so reordering sees at least as much. Only removing the merge-diff option
  (`git log --name-status` with neither `-m` nor `--diff-merges=*`) hides the merge
  (`entries=0`). And `--diff-merges=first-parent` alone is byte-identical to
  `-m --diff-merges=first-parent`.
- Evidence: `f1b-flag-permutations.txt` (evil merge, merge commit is the only frozen touch in
  range), `f1-flag-permutations.txt` (conflict merge). Canonical and fp-only share sha
  `41dc986754824db5…`; reversed/separate/m-only share `1a8f980fbee9fda2…`; none shares
  `e3b0c442…` (empty).
- Impact: block-24 row R46-CL6 and `exact.py` clause 7 bind the literal
  `"-m", "--diff-merges=first-parent"`. A gate.py carrying only
  `--diff-merges=first-parent` (correct, shorter) scores red; the row's stated hole
  ("one argument reorder blinds the merge arm") is false. The clause is a style pin, not a
  behavioral one.
- Smallest remediation: reword the row to "dropping the merge-diff option blinds the arm" and
  either accept `--diff-merges=first-parent` with an optional `-m`, or keep the literal and
  label it a textual style invariant. Do not edit the frozen bytes in this round; L1 decides.

### F-2 — MEDIUM (freeze declaration stale after amendments): the claims' declared freeze cannot measure any post-A2 revision

- Commands (read-only, at the lane), `exact.py --root <lane> --rev 07d2894e --no-battery`
  (the last row uses `--rev b1a058f3`, the live HEAD):

  | `--freeze` | rc | reason |
  |---|---|---|
  | `5017e1f7` (prompt's freeze) | 2 | `frozen_path_changed` (`plans/round-47-claims.md`, `tools/round-47/`, `record.py`) |
  | `9018c53b` (A1; "declared freeze" per the claims paragraph) | 2 | same |
  | `62e33f7d` (A2) | 2 | `tools/round-47/record.py` |
  | `1e2c3102` (A4) | 2 | `tools/round-47/record.py` |
  | `07d2894e` (A5) | 0 | clean |
  | `f54b3b6d` (A6) vs live HEAD `b1a058f3` | 0 | clean |

  Receipts `freeze-series.txt`, `freeze-*.json`, `lane-c1-head.json`,
  `lane-c1-head-lastfreeze.json`. L1's `c1-at-FINAL.json` already uses
  `freeze=f54b3b6d`, `rev=6f9fd7f8`, i.e. the last frozen-path touch.
- Impact: anyone following the claims text (freeze `5017e1f`/A1) gets exit 2
  `frozen_path_changed`, not a score; A3–A6 each re-invalidated the previous freeze, and the
  claims file declares only A1 (A2 is described without a hash). The counter is correct; the
  declaration is not re-derived by any clause.
- Smallest remediation: in the (re-frozen) claims file state
  `freeze := git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/` at the
  measured rev, and cite that commit as `plans/round-47-claims.md@<freeze>`; or re-declare a
  hash after every amendment. A clause that re-derives the declared freeze from the last
  frozen-path commit would make the citation self-checking.

### F-3 — LOW (receipt fidelity): rename new-side path dropped; `restored` mislabels renames

- Evidence: `f2-rename-tokens.txt`, `fixtures-structural.json` `F2-rename`
  (`history_touched` = `["tools/round-47/exact.py","tools/round-47/round-45-lesson.md"]`,
  `new_side_paths_missed_by_gate` = `["tools/round-47/exact-core.py","corpus/lessons/round-45.md"]`,
  `restored` names the renamed-away file).
- Impact: verdict stays 2 via the directory blob arm, so no bypass; the receipt misdescribes
  what happened (a rename reads as tamper-then-restore) and omits the new frozen name.
- Smallest remediation: in `history_touched`, consume both sides of `R`/`C` entries
  (`i += 3`, add both paths); or document `touched` as old-side-only and `restored` as
  "touched but blob-clean".

### F-4 — LOW (forgery surface, C2 `path` class): a dangling symlink satisfies path existence

- Evidence: fixture `F3`, `git show <rev>:probe/dangling.md` → `../../nowhere.md` (rc 0);
  `record.derive` path atom → `ok=True`, `{"exists": true}`; `os.path.exists` on the target
  is false. A `- corrects path <link>: …` line would re-derive the same way.
- Impact: the record can "verify" a path that is unreadable; dispatch files are still caught
  (`json.loads` on the link text fails), but report/evidence paths are not.
- Smallest remediation: require mode `100644`/`100755` for a `path` atom (reject `120000`), or
  state that tree existence includes symlinks.

### F-5 — LOW (operational): untracked file under a frozen path turns the measurement into exit 2

- Evidence: `touch tools/round-47/scratch-notes.tmp` → C1 exit 2
  `frozen_worktree_dirty ["tools/round-47/scratch-notes.tmp"]`; removing it restores 0
  (`f1-dirty-untracked.json`, `f1-clean-rerun.json`). `__pycache__/` is gitignored
  (`.gitignore:1`), so `python3 -B` is safe.
- Impact: a seat that leaves scratch inside `tools/round-47/` silently converts a would-be
  score into could-not-evaluate.
- Smallest remediation: keep scratch out of frozen paths; retain `-B` in the counting
  command.

### F-6 — INFORMATIONAL (history/worktree shape): C1 needs a worktree, C2 needs history

- Bare repo: C1 2 (`git status failed`), C2 0. Shallow clone: C1 0 (freeze==rev), C2 1
  (32 mismatches). Evidence `counter-runs.json`, `f6-shallow-*.json`.
- Impact: a verification environment must be a non-bare, full-history clone for C2; C1 only
  needs the tree plus a worktree for `git status`. A snapshot clone (`git archive` + commit)
  makes C2 red with 29–32 `rev` mismatches, not because the record is wrong.
- Smallest remediation: state the required repository shape next to each counting command.

### F-7 — INFORMATIONAL (identity/environment coupling)

- `GIT_AUTHOR_*`/`GIT_COMMITTER_*` in the caller's environment override the fixture's local
  identity, so fixture commit objects can embed the operator's real identity — inside scratch
  only. Global `init.defaultBranch`, `rerere.enabled`, `filter.lfs.*` and credential helpers
  are read by fixture git calls; the lane has no `.gitattributes`, so no filter driver runs on
  lane content. Evidence `probes.json` `identity_control` / `identity_poisoned`.
- Smallest remediation (optional): run counters with `GIT_CONFIG_GLOBAL=/dev/null` and a
  scrubbed author environment if strict isolation is wanted.

## Not run (honest gaps)

Windows/macOS behaviour; partial/blobless clones; fixtures with `.gitattributes` filter
directives; hook injection via `core.hooksPath`; `git fsck`; concurrent counter runs sharing
one scratch root; any `jj` operation; network remotes. No claim score was produced or changed
by this seat.
