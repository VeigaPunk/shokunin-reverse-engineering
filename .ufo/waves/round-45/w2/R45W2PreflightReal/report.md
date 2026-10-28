# R45W2PreflightReal — the sweep-contamination fix attacked on real history

Seat: `R45W2PreflightReal` (leaf). Lane `kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`.
Instrument under attack: `tools/round-45/frozen-path-preflight.py` (v2, five arms) and
`SKILL.md` `## Queue-drain craft` rule block 22 / `plans/round-45-claims.md` §"Frozen paths".

Method: lane tree read-only. Every run is a read-only `git` invocation (`log`, `diff-tree`,
`ls-tree`, `rev-parse`, `cat-file`, `status --porcelain`) made by the gate under test; every
mutation lives in a private fixture under
`/fast/scratch/hyaku/kaidoku-r45/R45W2PreflightReal/fx` and was deleted before yield. No
install, no stage/commit/push, nothing written outside this seat's report dir.

Frozen bytes: the interpreter I executed is the frozen blob, not a later copy —
`git rev-parse f762b727:tools/round-45/frozen-path-preflight.py` = blob `b4239827…`,
`sha256sum` of the extracted file and of the worktree file both
`633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`. Environment: Python
3.14.8, git 2.56.0.

## Verdicts

| # | attack | verdict | one-line evidence |
|---|---|---|---|
| A1 | r44 sweep on real history, with `--pathspec` + `--require-pathspec` | **holds** | exit 1, `touched` = **8**, all `M`, all in `c86ea508`, zero non-fixture records (`a1`, sha `264e92af…`) |
| A2a | r45 frozen range `f762b727..f59565b7`, assigned command | **holds (narrow)** | exit 0 `clean`, `touched/dirty/blob_changed/restored` all `[]` (`a2`, sha `7f3617b9…`) |
| A2b | does A2a's `clean` certify the declared two-path freeze? | **falsified** | A2a names only `tools/round-45`; the freeze file is the *other* declared path; same shape returns `clean` after a post-freeze edit of an undeclared frozen file (`f1`), and the certifying two-pathspec run `b1` is the only one that names both |
| A3 | r44 range, **no** `--pathspec`, **no** `--require-pathspec`: does the whole-tree scan still catch the eight? | **falsified as a "catch"** | exit 1, `touched` = **542** records / 536 distinct (8 of them the fixtures), `blob_changed` = `["tools/round-44/control-fixtures"]` only; the control `a4` gets the *same exit 1* on a frozen path nothing touched → the red is not attributable to the eight |
| C1 | base interpreter is "an untested single-arm gate" | **holds** | `149133d4:tools/round-45/frozen-path-preflight.py` = 4008 B, 0 hits each for `check-dirty`, `require-pathspec`, `restored`, `selftest` |
| C2 | "432-path bulk commit" and "eight under the frozen dir" | **holds** | `git show --name-status c86ea508` = 432 paths (400 A / 32 M); the 8 fixture entries are all `M` |
| C3 | `--selftest` = 11 cases, 7 named red cases, 0 failures | **holds** | exit 0, `PREFLIGHT_SELFTEST: cases=11 failures=0`; case names are exactly `green-clean, red-touched, red-restored, red-dirty, green-dirty-without-arm, red-dirfreeze-no-pathspec, green-dirfreeze-pathspec, red-unknown-freeze, red-nonancestor, red-bulk-sweep, green-empty-range` (`a8`, sha `9f03df65…`) |
| C4 | the pathspec guard fails closed (no decoy pathspec passes) | **holds** | sibling-prefix pathspec → exit 2 `pathspec_required`; `:(exclude)` magic in the pathspec → exit 2 `ls-tree at freeze failed` (`c1a`, `c2a`) |
| C5 | block 22's stated `--dirty-pathspec` false-clean | **holds (reproduced)** | fixture: dirty frozen file + `--dirty-pathspec other/` → exit 0 `clean`; same call without the flag → exit 1 `dirty [" M frozen/a.txt"]` (`f3`) |
| C6 | the fix is placed in the fleet sweep/pre-push path (R44-CL1(c)) | **not in place — stated, not fixed** | `grep -r frozen-path-preflight /home/vgpnk/Projects/shokunin/scripts` → 0 matches; block 22 itself says placement "is not a lane edit … stays an operator/integrator request" |

Nothing is "not run": every listed row was executed. What I did **not** attack (out of seat):
the C2 registry rows and both counters' predicates.

## A1 — the r44 sweep, with the fix

Command (see `receipts.json`):

```sh
python3 -I -B tools/round-45/frozen-path-preflight.py --root <LANE> \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 \
  --pathspec tools/round-44/control-fixtures/ \
  --freeze-path tools/round-44/control-fixtures --require-pathspec
```

exit **1**, stdout sha256 `264e92af1911798a69663fca07b61591c808b41d42a43a6c3df2b011dc7bf535`,
UTC 2026-10-28T16:00:21Z. Receipt: `verdict: frozen_path_changed`, `touched: 8`,
`dirty: []`, `restored: []`, `blob_changed: 9` (the directory tree oid + its eight files).
There is **no** non-fixture record in `touched` — the pathspec did what it claims.

The eight (all `M`, all `commit c86ea508…`):

```
tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json
tools/round-44/control-fixtures/c3/manifest.json
tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1be/after.json
tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json
tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2be/after.json
tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2le/after.json
tools/round-44/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md
tools/round-44/control-fixtures/pos/manifest.json
```

Calibration of the record: the eight are 5 × `after.json` + 2 × `manifest.json` + 1 ×
knowledge `.md`, so "eight frozen control **fixtures**" (`plans/round-45-claims.md` §Frozen
paths) is a loose noun for "eight files under the fixtures directory"; the **count** is exact.
`c48f8a4b` is the right freeze label: its subject is `round-44: freeze C1/C2 claims, carriers,
counters, and controls`, and it is the last commit to have touched `plans/round-44-claims.md`
before `c86ea508`.

Independent reproduction: my `a1` receipt is **identical on all ten semantic fields**
(`gate, freeze, rev, pathspec, freeze_paths, touched, blob_changed, restored, dirty, verdict`)
to the lane's own `.ufo/waves/round-45/l1/preflight-c86ea508.json`. The L1's r44 number is
reproducible, not asserted.

## A2 — the r45 frozen range, and the scope of the `clean`

Assigned command → exit **0**, `verdict: clean`, every arm empty, stdout sha256
`7f3617b90723bfe0dde44f05527692147e33cfe79a6a109052c37e193d6b5f61`, UTC 16:00:21Z.
The same command without `--require-pathspec` (`a7`) prints **byte-identical** stdout (same
sha256): on a clean, covered range the guard is invisible, as it should be. `--rev 1f4b27f8`
(A1, the measured revision) and `--rev HEAD` (= `0ee50aaf` at run time, after the wave-1
landing) are also `clean` (`a5` sha `5a506572…`, `a6` sha `34b275d6…`). So the frozen bytes
survived every post-freeze amendment: `git log f762b727..HEAD -- plans/round-45-claims.md
tools/round-45/` is empty and both blobs are unchanged (`plans` blob `f93df4c3…`,
`tools/round-45` tree `8cb6fa80…` at freeze and at HEAD).

**The defect the assignment's command hides.** That freeze has *two* frozen paths
(`plans/round-45-claims.md` and the directory `tools/round-45/`), and block 22 states the
required invocation explicitly: `--pathspec tools/round-45/ --pathspec
plans/round-45-claims.md` with the matching two `--freeze-path` values, because "one pathspec
certifies four of the five frozen files" (routed R45-CL10). The assigned A2 command passes
**one** pathspec and **one** freeze-path, so `plans/round-45-claims.md` is in neither the
commit arm's scope nor the blob arm's frozen set. It prints `clean` whether or not that file
was touched. Reproduced in fixture `f1`:

| call | exit | `touched` | `blob_changed` | verdict |
|---|---|---|---|---|
| under-declared (`--pathspec frozen/ --freeze-path frozen`) after a commit editing the frozen file `plan/claims.md` | **0** | `[]` | `[]` | `clean` |
| fully declared (adds `plans/claims.md` to both lists) | **1** | `plan/claims.md` | `plan/claims.md` | `frozen_path_changed` |

Fixture `f2` is the same asymmetry for the history arm: touch-then-restore of the undeclared
frozen file → under-declared exit **0** `clean`, fully declared exit **1**
`restored: ["plan/claims.md"]`.

The prescribed two-pathspec form, run on real history (`b1`, sha `565f7251…`), is exit **0**
`clean` with `freeze_paths: ["tools/round-45", "plans/round-45-claims.md"]` — so the landing's
freeze **did** hold; but `b1` is the certificate, not `a2`. Note the lane's own receipts
(`.ufo/waves/round-45/l1/preflight-c86ea508.json` and `preflight-round45-frozen.json`) both use
the one-pathspec form, i.e. the record's rule (block 22 / R45-CL10) and the record's receipts
disagree. This is the reconcilable item for the L1: keep the `clean`, cite `b1`, and label the
one-pathspec runs as covering `tools/round-45/` only.

## A3 — the whole-tree scan: red, but not a catch

Command: same r44 range, `--freeze-path tools/round-44/control-fixtures`, **no** `--pathspec`,
**no** `--require-pathspec`. Exit **1**, stdout sha256
`2d7a672f825fea13f50160a8640491ecb87618c3dfc433fc73674287907b79ed`, UTC 16:00:21Z.

- `touched`: **542 records / 536 distinct paths** — the eight are inside it (all `M`, commit
  `c86ea508`), but so is every other path of the seven-commit range. Path counts per commit:
  51, 3, 5, 1, 47, 3, **432**; sum 542 (the 432 is `c86ea508` alone, the sweep).
- `blob_changed`: `["tools/round-44/control-fixtures"]` — **one** entry, the directory's tree
  oid. No file under it is named by the frozen arm.
- `restored: []`, `dirty: []`.

So the eight are *present* in the receipt and the exit is red, but the gate contributes no
field that says "these eight are the frozen ones". The control `a4` settles whether the red is
evidence: the same range and the same whole-tree scan with `--freeze-path
plans/round-44-claims.md` — a file that is **byte-identical across the range** (`git diff
c48f8a4b c86ea508 -- plans/round-44-claims.md` empty) — also exits **1**
(`frozen_path_changed`, `touched` 542, `blob_changed []`, sha `c52fb273…`). A verdict that does
not change when the frozen path is untouched carries no information about the frozen path; it
is red because the *range* is non-empty.

Therefore the proposition "without the pathspec the whole-tree scan still catches the eight" is
**falsified**: the scan reports them only as 8 of 542 records, and the red is the same red it
would print for a freeze that nothing violated. The r44 defect shape is not "hidden" by the
scan, it is **drowned** by it — which is exactly why R44-CL1(b) asks for the pathspec, and why
the `--require-pathspec` guard is the load-bearing part of the fix rather than the scan.
Corollary for the record: block 22 row 5 ("a whole-tree scan is refused", exit 2) is true only
when the caller passes `--require-pathspec`; a caller who omits that flag gets row-6-shaped
red at 542 records, not a refusal. That is an opt-in guard, and `a3` is the receipt.

## What else the artefacts got right (calibration, measured)

- **Arm coverage vs arm isolation.** The selftest is genuinely 11/0 with the seven red cases
  the claims name (`a8`), and block 22 already states the isolation limit (deleting the
  `restored` or `blob` arm still reads 11/0 because `touched` absorbs the kill). My `f2`
  under-declared run is a second, independent instance of that class: `restored` is empty
  because the *scope* is empty, not because the history is clean.
- **`--dirty-pathspec` false-clean** (`f3`): confirmed exactly as block 22 states — it
  *replaces* the dirty scope; narrowed to `other/` the gate reads `clean` on a dirty frozen
  file. This round's invocation never passes the flag, so the record's own limit stands.
- **Guard fails closed**: a sibling-prefix pathspec (`…/control-fixtures-extra/`) → exit 2
  `pathspec_required`; a compound pathspec using `:(exclude)` → exit 2
  (`ls-tree at freeze failed for :(exclude)…`). The string comparison in `covers()` does not
  let a magic pathspec through as a pass — it refuses to evaluate.
- **Base-vs-landed diff**: the base interpreter (`149133d4`, 4008 B) has zero occurrences of
  `check-dirty`, `require-pathspec`, `restored`, `selftest`; the landed one has all five arms
  and the selftest. The C1 "gains the four arms and an `--selftest`" clause is literal.

## Risks that stay open

1. **Prevention is not installed.** The M44-2 vector was a *non-author fleet sweep*, and no
   fleet script calls the gate (`grep -r frozen-path-preflight` under
   `/home/vgpnk/Projects/shokunin/scripts` → 0 matches). The gate can only be run by whoever
   remembers; the record says this, and it is still the largest residual risk.
2. **Under-declared invocations are silent.** Nothing in the gate requires the caller to
   enumerate every frozen path; a file freeze path omitted from *both* `--pathspec` and
   `--freeze-path` is invisible (`f1`, `f2`), and the one-pathspec form used by the lane's own
   receipts is that shape for `plans/round-45-claims.md`. A `--freeze-manifest <file>`-style
   row, or a compare of the passed freeze set against the claims file's §"Frozen paths", would
   close it.
3. **The `restored` arm is scope-bound.** It can only fire for paths inside the commit arm's
   pathspec; block 22 row 2 states the trigger unconditionally. Row 2 is accurate for a
   correct invocation, but the table would be truer if the row said "touched *within the
   declared pathspec*".
4. `touched` counts records, not paths (542 vs 536 here) because the commit arm uses `-m
   --diff-merges=first-parent`; a reader comparing counts to `git show`'s 432 sees a
   110-record surplus. Not a defect, but the receipt gives no field that reconciles the two.

## Receipts

`receipts.json` (12 runs: command, exit, stdout sha256, UTC, parsed receipt), `exits.tsv`,
`<run>.stdout` / `<run>.stderr` for every run, and the exact drivers `drive.sh`, `drive2.sh`,
`drive3.sh`, `drive4.sh`, `fixtures.py`, `mkreceipts.py`, plus `frozen-preflight.py` — the
byte-frozen copy that `a8` executed. Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2PreflightReal`
removed after these were copied. No installs; lane tree untouched (`git status --porcelain`
shows only this seat's untracked report dir).
