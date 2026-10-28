# R45W2ReviewPreflight — adversarial review of the freeze-integrity gate

Seat: `R45W2ReviewPreflight` (reviewer, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Attacks: `tools/round-45/frozen-path-preflight.py` (the interpreter behind `SKILL.md` rule block 22,
marker `<!-- freeze-integrity-table v1 -->`) and the exits/lists block 22 promises.

## 0. Target bytes, method, and what is not mine to restate

* Verified before any run: `sha256(tools/round-45/frozen-path-preflight.py)` = `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`
  — identical in the worktree, at the freeze `f762b727`, and at the review revision
  `f59565b782c18b0eb691bec12f52d2f80d9f5032` (`git show <rev>:tools/round-45/frozen-path-preflight.py | sha256sum`).
  `git log --name-status f762b727..HEAD -- tools/round-45/ plans/round-45-claims.md` prints **nothing**,
  so the frozen set is untouched post-freeze and my fixtures are the only mutation surface.
* Read-only on the lane: every fixture is a private `git init` repo under
  `/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight/fx/`, built by `driver.py` with
  `git -C "$D" rev-parse --show-toplevel == "$D"` asserted before the first commit; every gate call is
  `python3 -I -B preflight.py` on a byte-identical copy in scratch. No lane write, no gate `--json-out`
  inside the lane.
* Every gate receipt and every scripted raw receipt in `receipts/` records: exact argv, exit,
  `stdout_sha256`, UTC. Generator scripts in `receipts/generator/`. `$S` removed after copying.
  One inline probe (`b10-quoted-revparse.json`) captured argv/exit/stdout but no wall clock; it says so
  in its own `utc_note` rather than carrying an invented timestamp.
* Selftest at the frozen bytes reproduces the control: `PREFLIGHT_SELFTEST: cases=11 failures=0`
  (same 11 case names as `.ufo/waves/round-45/controls/preflight-selftest.txt`).
* Live-lane run (`b7-lane-live.json`, pinned to `rev=0ee50aaff516571aa607769bbbdf19a3db90dfa5`;
  HEAD advanced while I worked): exit **0**, `verdict clean`, stdout sha `979f3825…` with the
  two-pathspec invocation (`--pathspec tools/round-45/ --pathspec plans/round-45-claims.md`,
  `--check-dirty --require-pathspec`). So the shipped invocation is clean on the shipped tree.

Verdict vocabulary: `holds` (artefact survives, command shown), `falsified` (artefact wrong: input,
differing value, fix), `not run` (why).

## 1. Verdict summary

| # | Attack (what it attacks) | Verdict | Receipt (case → exit, stdout sha256 prefix) |
|---|---|---|---|
| A1 | `R`/`C` record: is the second path (source) counted? | **holds** | `a1-rename-within` 1 `8e7a5ce06d82`; `a1b-rename-into` 1 `c116965e21bb`; `b2-copy` 1 `29338ea2bcd7`; `c1-rename-out` 1 `0b206e4915cf` |
| A2 | untracked dir collapses to one entry — does it hide the count? | **holds** for the verdict, **receipt collapses** (F6) | `a2-untracked-dir` 1 `950f21f618ca`; `a2b-untracked-files` 1 `8a44477b126f` |
| A3 | deleted-then-recreated path | **holds** | `a3-deleted-recreated` 1 `67fa27292dcf` (`restored`) |
| A4 | submodules and symlinks | **holds** | `a4b-submodule-bump` 1 `30c4886f98e9`; `a4a-symlink-retarget` 1 `d926bc4c55a0`; `a4a2-symlink-to-file` 1 `dca5bfb059c3` |
| A5 | `not a_ok and not b_ok → continue`: can a path escape both lists? | **holds** for the exit code; **falsified as a classifier** (F3) | `b1-added-then-deleted` 1 `f8d41c93bf67`; `a7-nonascii` 1 `e6281573cef9` |
| A6 | `git log -m --diff-merges=first-parent` on a merge | **holds** (`-m` itself is inert: F7) | `a5-pristine-merge-ours` 1 `21403026d056`; `a5b-merge-conflict` 1 `fcf407f1b7ce`; `b9-plainlog-a5` **0** `06ed9f25f3a0` |
| B1 | `covers()` direction: parent pathspec | **falsified** (F2) | `a6-covers-parent` **2** `dc5a4a97388b` |
| B2 | `covers()` direction: descendant file pathspec | **falsified** (F1) — false clean | `a6b-covers-file` **0** `267b6a1b2c67`; control `b8-a6b-control-full-pathspec` 1 `0b01b69e1d9a` |
| B3 | non-ASCII / quoted path in the blob arm | **falsified** (F3) as a receipt | `a7-nonascii` 1 `e6281573cef9`; `b10-quoted-revparse` (git) 128 |
| B4 | `--check-dirty` vs index flags (`--assume-unchanged`, `--skip-worktree`) | **falsified** as a worktree claim (F4) | `a9-assume-unchanged` **0** `439e10113b89`; `b5-skip-worktree` **0** `f496a458f51c` |
| B5 | `--check-dirty` vs ignored untracked content | **holds** as specified; limit recorded (F5) | `a8-ignored-untracked` **0** `55bebfabd729`; lane instance `b11-lane-ls-files-others` |
| B6 | guard with `--freeze-path` omitted | **holds**; table row 5 is conditional on a flag it never names (F8) | `b3-no-freeze-path` **0** `d4bd5e6fb151` |
| B7 | glob pathspec through `covers()` | **holds** (accepted, `frozen/*` really covers) | `b4-glob-pathspec` 0 `7b1a219cd631` |

`restored[] ∩ blob_changed[] == ∅` in all 27 gate receipts that produced a receipt (checked mechanically,
table in §6) — row 2's disjointness claim is untroubled.

## 2. The six named attacks, with the measured values

### A1 — `R`/`C` two-path records: is the source counted? **holds**

`R100` carries two path cells. The parser loops `for path in parts[1:]` (line 108), so both are counted.
Measured on `a1-rename-within` (`git mv frozen/a.txt frozen/c.txt`):

```
R100\tfrozen/a.txt\tfrozen/c.txt        (a1-raw-log.json)
touched = [ {…, path: frozen/a.txt, status: R100}, {…, path: frozen/c.txt, status: R100} ]   exit 1
blob_changed = [frozen, frozen/a.txt]
```

`C` is unreachable with the gate's argv: `git log --name-status` with no `-C`/`--find-copies` reports a
copy as `A` (`b2-raw-log.json`), and only `-C --find-copies-harder` yields `C100` (`b2-raw-log-with-C.json`).
So the "second cell of a `C`" cannot occur; the `C` branch in the status set is dead but harmless.
Rename **into** the frozen dir is reported as `A <dest>` under the path-limited log (the source is not
listed at all, `a1b-raw-log-pathlimited.json`) — the destination is still counted, exit 1. Rename **out**
is `D <source>`, exit 1 (`c1-rename-out`). No rename/copy shape reads clean.

### A2 — untracked directory collapse: does it hide the count? **no false clean; receipt collapses**

Eight untracked files under a new directory inside the frozen pathspec:

```
git status --porcelain -z -- frozen/   →   '?? frozen/pack/\x00'          (a2-raw-status-z.json)
gate receipt: dirty = ["?? frozen/pack/"]                                   exit 1
```

Eight untracked files placed directly in a tracked directory → eight entries
(`a2b-untracked-files`: `dirty` length 8). And with `--dirty-pathspec frozen/sub/`, the collapse still
names a directory (`?? frozen/sub/pack/`, `a2c`). So the arm's boolean is right; its `dirty[]` is
path-shaped, not file-shaped: the receipt cannot say how many frozen files are dirty and names a directory
that does not exist at the freeze. Fix: `git status --porcelain -z --untracked-files=all`.

### A3 — deleted-then-recreated. **holds**

Delete `frozen/a.txt`, commit; recreate it with the exact freeze bytes, commit:

```
touched = 2 (D, A), blob_changed = [], restored = ["frozen/a.txt"], exit 1   (a3-deleted-recreated)
```

Deleted only: `blob_changed = [frozen, frozen/a.txt]`, exit 1 (`a3b-deleted-only`). Bonus shape — a
symlink replaced by a regular file carrying the same bytes (`T frozen/link`, identical blob oid): it lands
in `restored`, exit 1 (`a4a2-symlink-to-file`). "History, not tip equality" survives all three.

### A4 — submodules and symlinks. **holds**

* Gitlink bump (`frozen/sub` from `s1` to `s2`): `blob_changed = [frozen, frozen/sub]`, `touched = [M]`, exit 1.
* Symlink retarget `a.txt → b.txt`: `blob_changed = [frozen, frozen/link]`, exit 1.
  `rev-parse base:<link>` returns the link blob's oid, so the blob arm sees it.
* The only mode/type blindness found is the symlink→file case above, which `touched` still catches.

### A5 — `not a_ok and not b_ok → continue`: can a path escape both lists? **yes from both lists, never from the exit code**

* Path **added after the freeze and deleted before REV** (`b1-added-then-deleted`): it is not in the
  freeze's `ls-tree`, so `frozen` never contains it; `rev-parse` fails at both revisions, so the new
  `continue` (lines 126-127) fires. Result: `blob_changed = []`, `restored = []` — **it escapes both
  lists** exactly as suspected. It does not escape the verdict, because the commit arm records both
  commits (`touched = [D,A]`, exit 1). The two findings are one defect: the path is invisible to every
  non-commit arm, so the commit arm is load-bearing for it (see F1, where narrowing the log turns it into
  a false clean).
* The same `continue` is **falsified as a classifier** by a path that exists on both sides but whose name
  git quotes (§F3): `a_ok` and `b_ok` are both false for a reason the comment cannot see.

### A6 — `git log -m --diff-merges=first-parent` on a merge. **holds**

* Merge `-s ours` that keeps the first parent's side (tip bytes identical to the freeze, so `blob_changed`
  empty): the side commit is listed and the path is classified `restored`:
  `touched = [{commit: 77c95ebb…, path: frozen/a.txt, status: M}]`, `restored = ["frozen/a.txt"]`, exit 1
  (`a5-pristine-merge-ours`, sha `21403026…`).
* Two-sided conflict resolved to a third value (`a5b-merge-conflict`): three records, three **different**
  commits (side, main, merge), so `-m` does not double-report the merge against both parents — the last
  diff-selection flag wins and it is `first-parent`.
* The arm's protection is real but thin: removing `-m` alone produces a **byte-identical** stdout
  (`b6-nom-a5`, same sha `21403026d056…`), while removing `--diff-merges=first-parent` as well makes the
  same fixture exit **0 clean** (`b9-plainlog-a5`, sha `06ed9f25…`). This corroborates the block's claim
  that the plain scan misses a merge's own resolution edit (R45-CL6) on the gate too — and shows the gate
  escapes it only through the long flag.

## 3. Additional attacks (not in the L1's list) that found something

### B1/B2 — `covers()` is direction-blind; the guard admits the scan it exists to refuse. **falsified**

`covers()` (lines 62-65) is `any(p.rstrip("/") == fp or p.rstrip("/").startswith(fp + "/") …)` — "the
pathspec is at or under the frozen path". Consequences, both measured:

* **Descendant accepted (soundness).** `--pathspec frozen/a.txt --freeze-path frozen --require-pathspec`
  passes the guard although the scan sees one file of the frozen directory. With `frozen/b.txt` tampered
  and restored inside `FREEZE..REV`, the gate prints `verdict clean`, exit **0**, `touched []`,
  `blob_changed []` (`a6b-covers-file`, sha `267b6a1b…`; reproduced twice with the same sha). Control —
  identical history, `--pathspec frozen/` — exits **1** with `touched 2`, `restored [frozen/b.txt]`
  (`b8-a6b-control-full-pathspec`, sha `0b01b69e…`). Row 1 of block 22 ("any commit in FREEZE..REV touches
  a frozen path → 1") is false for this input; row 5 is what let it through.
* **Ancestor rejected (over-strict).** `--pathspec frozen/ --freeze-path frozen/sub` exits **2**
  `{"reason": "pathspec_required", "uncovered_frozen_dirs": ["frozen/sub"]}`
  (`a6-covers-parent`, sha `dc5a4a97…`) although `git log -- frozen/` demonstrably covers `frozen/sub`.
  Row 5's trigger ("no pathspec covers it") is false here: a covering pathspec is present.
* The same predicate accepts a glob (`frozen/*` → exit 0, `b4-glob-pathspec`), which happens to cover but
  is another unverified acceptance.

Fix: compare pathspecs to the frozen path **exactly**, after stripping magic, and treat any pathspec that
is a strict ancestor or a strict descendant of a frozen directory as 2 `pathspec_not_exact`, naming both;
make the log scope `frozen ∪ pathspecs` so a wrongly-narrow pathspec can never shrink the commit arm.
This is adjacent to R45-CL15's `x4b` ("a log scope narrower than the frozen path, where the blob arm is
the only defence") but the root cause here is the guard that was supposed to forbid that scope.

### B3 — the blob arm silently drops every path git quotes. **falsified (receipt), row 3**

`frozen/ä.txt` changed at REV:

```
git ls-tree -r --name-only <freeze> -- frozen/  →  frozen/a.txt\n"frozen/\303\244.txt"\n   (a7-raw-ls-tree)
git rev-parse '<freeze>:"frozen/\303\244.txt"'  →  exit 128
    fatal: path '"frozen/\303\244.txt"' does not exist in '4d92eba7…'            (b10-quoted-revparse)
gate receipt: blob_changed = ["frozen"] only; touched = [M "frozen/\303\244.txt"]; exit 1   (a7-nonascii)
```

The changed file is in neither `blob_changed[]` nor `restored[]`; only its parent directory tree oid
appears. The mechanism is the unguarded `continue`: the `ls-tree` name is C-quoted, `rev-parse` rejects
it, and "unresolvable name" is indistinguishable from "absent on both sides". Row 3's receipt column
(`blob_changed[]`) is therefore false for any frozen path with a non-ASCII byte, a quote or a backslash.
The exit code still comes out 1 via `touched` — but that is precisely why the arm cannot be credited.

Fix: `git ls-tree -r -z --name-only` (`b10-ls-tree-z` returns `frozen/a.txt\x00frozen/ä.txt\x00`) and
`git log -z` (R45-CL11's fix, now shown to matter for the blob arm too); and make the both-missing branch
a hard 2 `unreadable_frozen_path` when the path came from `ls-tree`, reserving `continue` for paths that
were never listed.

### B4 — `--check-dirty` is git-status-dirty, not worktree-bytes-dirty. **falsified as a worktree claim**

```
git update-index --assume-unchanged frozen/a.txt ; echo modified > frozen/a.txt
git status --porcelain -z -- frozen/   →  ''                       (a9-raw-status-z)
gate: dirty = [], verdict clean, exit 0                            (a9-assume-unchanged)

git update-index --skip-worktree frozen/a.txt    →  same          (b5; ls-files -v prints 'S frozen/a.txt')
```

Block 22 calls `--check-dirty` "the arm that matters most … catches the precursor before any sweep
exists"; with either index flag the precursor is present and the arm reads clean. This is git's own
contract (both flags mean "pretend this file is unmodified"), so the gate is not lying about `git status`
— it is the table's trigger text ("the worktree is dirty under the frozen pathspec") that over-reads.
Fix: after the status call, `git ls-files -v -- <scope>` and exit 2 when any frozen path carries the `h`
(assume-unchanged) or `S` (skip-worktree) tag.

### B5 — ignored untracked content under the frozen path is invisible. **holds as specified; limit, with a live instance**

```
.gitignore: `__pycache__/`; write frozen/__pycache__/x.cpython-313.pyc
git status --porcelain -z -- frozen/   →  ''        gate: clean, exit 0        (a8-ignored-untracked)
```

The lane instantiates it: `git ls-files --others -- tools/round-45/` prints
`tools/round-45/__pycache__/{c1,c2}-counter.cpython-314.pyc` (`b11-lane-ls-files-others`), while
`git status --porcelain -z -- tools/round-45/` is empty and my live gate run reports `dirty: []`.
Honest calibration: this is **not** the M44-2 loss shape — `git add -A` cannot add ignored files, so a
sweep cannot pick them up; only `git add -f` could. Recorded as a limit of the worktree arm, not as a
false pass of the freeze claim. Optional fix: `--ignored=matching` plus a separate `ignored[]` list.

### B6 — the guard needs `--freeze-path`, which the table never names. **holds; claim precision**

With a directory freeze and **no** `--freeze-path` (lines 87-90 have nothing to check), the gate exits 0
and prints a clean receipt (`b3-no-freeze-path`). Row 5's trigger reads unconditionally ("a frozen path is
a directory at FREEZE and no pathspec covers it → 2"); in the code it is conditional on the caller having
declared the path. The claims file does declare it, so scoring is unaffected; block 22 should say the
guard is caller-declared, or derive directory-ness from the pathspec's own `ls-tree`.

## 4. Findings by severity (what to fix, in order)

1. **MEDIUM-HIGH — F1 `covers()` accepts a descendant pathspec** (lines 62-65). False clean: a tamper +
   restore of a sibling is reported `verdict clean`, exit 0, under an invocation the guard admits
   (`a6b-covers-file` vs control `b8-…`). Fix in §B1/B2. Table rows 1 and 5 both need the correction.
2. **MEDIUM — F2 the guard rejects a covering ancestor pathspec** (`a6-covers-parent`, exit 2). A caller
   following block 22 with `--pathspec tools/ --freeze-path tools/round-45` gets could-not-evaluate, which
   is never a pass — a silent scoring hole if a counter maps 2 to "no claim".
3. **MEDIUM — F3 quoted-path drop in the blob arm** (`a7-nonascii`, `b10-quoted-revparse`). Row 3's
   `blob_changed[]` is incomplete and the `continue` cannot tell absence from unreadability; `-z` on both
   `ls-tree` and `log` plus a 2 on unreadable frozen paths is the fix. Distinct from R45-CL11's commit-arm
   note: this is the `ls-tree`/`rev-parse` path.
4. **LOW-MEDIUM — F4 index flags defeat `--check-dirty`** (`a9`, `b5`). Exit 0 while the frozen file's
   worktree bytes differ from the freeze. Fix with `ls-files -v` → 2.
5. **LOW — F5 ignored untracked content** (`a8`, lane's `tools/round-45/__pycache__`). Limit, not a sweep
   vector; state it in block 22 or list it separately.
6. **LOW — F6 `dirty[]` collapses an untracked directory** (`a2` = 1 entry for 8 files).
   `--untracked-files=all` restores the count.
7. **INFO — F7 `-m` is inert; `--diff-merges=first-parent` is load-bearing** (`a5-pristine` and
   `b6-nom-a5` share sha `21403026d056…`; `b9-plainlog-a5` exits 0). The block's sentence attributes the
   merge-visibility to "the `-m --diff-merges=first-parent` form"; the measured truth is that only the
   long flag matters. Either drop `-m` or say which half is load-bearing — otherwise the next tidy-up
   that removes the "redundant" long flag re-opens R45-CL6 blindness inside the gate.
8. **INFO — F8 row 5 is conditional on `--freeze-path`** (`b3-no-freeze-path`).

## 5. Residual risk and what I did not run

* **Not run — the two counters.** `c1-counter.py` / `c2-counter.py` carry the freeze arm themselves
  (R45-CL6 already routes their plain-form blindness); out of this seat's target.
* **Not run — octopus merges (>2 parents).** [INFERENCE] `--diff-merges=first-parent` diffs an octopus
  only against parent 1; the other parents' own commits are still traversed, so the A5 result should
  generalise, but I have no receipt for it and do not claim one.
* **Not run — `core.quotePath=false`.** The quoted-name drop would change shape (raw bytes in the parse);
  the non-ASCII case is measured only under the default config.
* **Not run — Windows/`protectNTFS` path spellings, unicode-normalisation collisions.** No fixture.
* **Not run — `--dirty-pathspec` false clean.** Already reproduced and routed (R45-CL15; SKILL.md:574,
  lesson `round-45.md:177-182`); re-running it would add nothing. My `a2c` run used the flag only to show
  the collapse, and it still exits 1.
* **Live lane moved under me**: HEAD was `a63d109f` when I started and `0ee50aaf` when the live gate ran;
  the lane-live receipt pins `0ee50aaf`. Everything byte-sensitive in this report is pinned to the freeze.
* **Scope of the F1 false clean**: it needs a pathspec narrower than the frozen directory. The round's own
  invocation (`--pathspec tools/round-45/`) is not affected — measured clean in `b7-lane-live`. The defect
  is in the guard that exists to make that unreachable, so the severity is about the instrument's stated
  guarantee, not about this round's score.

## 6. Arm coverage of my fixtures (which arm produced the verdict)

| case | exit | touched | blob_changed | restored | dirty | comment |
|---|---|---|---|---|---|---|
| a1-rename-within | 1 | 2 (R100×2) | 2 | 0 | 0 | both cells counted |
| a1b-rename-into | 1 | 1 (A) | 1 | 0 | 0 | dest counted, source not listed |
| c1-rename-out | 1 | 1 (D) | 2 | 0 | 0 | |
| b2-copy | 1 | 1 (A) | 1 | 0 | 0 | no `C` without `-C` |
| a2-untracked-dir | 1 | 0 | 0 | 0 | **1** | 8 files → 1 entry |
| a2b-untracked-files | 1 | 0 | 0 | 0 | 8 | file-shaped |
| a3-deleted-recreated | 1 | 2 | 0 | 1 | 0 | restored, disjoint |
| a3b-deleted-only | 1 | 1 (D) | 2 | 0 | 0 | |
| a4a-symlink-retarget | 1 | 1 | 2 | 0 | 0 | |
| a4a2-symlink-to-file | 1 | 1 (T) | 1 | 1 | 0 | type change, same bytes |
| a4b-submodule-bump | 1 | 1 | 2 | 0 | 0 | gitlink oid |
| a5-pristine-merge-ours | 1 | 1 | 0 | 1 | 0 | side commit found |
| a5b-merge-conflict | 1 | 3 | 2 | 0 | 0 | 3 commits, no dup |
| b6-nom-a5 (mutation) | 1 | 1 | 0 | 1 | 0 | byte-identical to a5 |
| b9-plainlog-a5 (mutation) | **0** | 0 | 0 | 0 | 0 | false clean without the flag |
| a6b-covers-file | **0** | 0 | 0 | 0 | 0 | **false clean (narrow pathspec)** |
| b8-a6b-control-full-pathspec | 1 | 2 | 0 | 1 | 0 | same history, dir pathspec |
| a10-child-pathspec | 1 | 0 | 1 | 0 | 0 | sibling caught only by tree oid |
| a7-nonascii | 1 | 1 | 1 (dir only) | 0 | 0 | file dropped from blobs |
| b1-added-then-deleted | 1 | 2 (D,A) | 0 | 0 | 0 | escapes both lists |
| a8-ignored-untracked | **0** | 0 | 0 | 0 | 0 | ignored ⇒ invisible |
| a9-assume-unchanged | **0** | 0 | 0 | 0 | 0 | index flag ⇒ invisible |
| b5-skip-worktree | **0** | 0 | 0 | 0 | 0 | index flag ⇒ invisible |
| a6-covers-parent | **2** | – | – | – | – | false could-not-evaluate |
| b3-no-freeze-path | 0 | 0 | 0 | 0 | 0 | guard needs the flag |
| b4-glob-pathspec | 0 | 0 | 0 | 0 | 0 | glob accepted |

## 7. Reproduce

`receipts/generator/` holds `driver.py` + `cases1..6.py`. Each `receipts/<case>.json` carries its argv, so
any case can be rebuilt:

```sh
S=/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight
mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH="$S"
cp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py "$S/preflight.py"
python3 "$S/cases1.py"; python3 "$S/cases2.py"; python3 "$S/cases3.py"; python3 "$S/cases5.py"; python3 "$S/cases6.py"
python3 -I -B "$S/preflight.py" --root "$S/fx/a6b-covers-file" --freeze <freeze> --rev <rev> \
  --pathspec frozen/a.txt --freeze-path frozen --require-pathspec   # → 0, clean
```
(`cases4.py` is superseded by `cases5.py`, which fixes the receipt it had renamed; the `a6b` narrow
receipt reproduced byte-identically across both runs, sha `267b6a1b…`.)

## 8. Receipt index

`receipts/` — gate receipts: `a1-rename-within`, `a1b-rename-into`, `a2-untracked-dir`,
`a2b-untracked-files`, `a2c-untracked-dir-narrow`, `a3-deleted-recreated`, `a3b-deleted-only`,
`a4a-symlink-retarget`, `a4a2-symlink-to-file`, `a4b-submodule-bump`, `a5-pristine-merge-ours`,
`a5b-merge-conflict`, `a6-covers-parent`, `a6b-covers-file`, `a7-nonascii`, `a8-ignored-untracked`,
`a9-assume-unchanged`, `a10-child-pathspec`, `b1-added-then-deleted`, `b2-copy`, `b3-no-freeze-path`,
`b4-glob-pathspec`, `b5-skip-worktree`, `b6-nom-a5`, `b8-a6b-control-full-pathspec`, `b9-plainlog-a5`,
`b7-lane-live`.
Raw git receipts: every `*-raw-*.json`, plus `b10-quoted-revparse`, `b10-ls-tree-z`,
`b11-lane-ls-files-others`.

The two mutation probes were built in scratch and are **not** in `receipts/` (scratch was removed after
capture): copy the frozen file, then apply exactly one one-token replacement — `b6`: `"log", "-m",
"--diff-merges=first-parent"` → `"log", "--diff-merges=first-parent"` (mutation sha
`1fbe3c90b48ed5c24bb5e56aaf631d92fbb42cfb2c83f3c940ec40fcf1acac85`); `b9`: `"log", "-m",
"--diff-merges=first-parent"` → `"log"` (mutation sha
`76c9f576d545c464bc4181a9fc7b7d3f6fc197534ec9f2935e49af704797a3a1`). The resulting exit codes are in
`b6-nom-a5.json` (1) and `b9-plainlog-a5.json` (0).
