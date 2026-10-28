# R45W2PathspecArm — falsifying `--require-pathspec`

Seat: leaf mutation/attack seat, round 45 wave 2. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`;
landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`; amendment A1 (measured)
`1f4b27f82353d6544dc0c8048b3cfdadd8525d12`; lane tip during this run
`0ee50aaff516571aa607769bbbdf19a3db90dfa5` (moved from `a63d109f` between my first and last
measurements — a concurrent L1 commit; both frozen blobs are identical at every revision named
here, so the move does not affect any receipt).

Read-only on the lane: the only lane paths written are this report and its receipt directory.
Nothing was staged/committed/pushed; no tool was installed; every fixture lived under
`/fast/scratch/hyaku/kaidoku-r45/R45W2PathspecArm` with `TMPDIR` pinned there, and the scratch tree
was removed after the receipts were copied (list in §9).

## 1. Instrument under test

Executed bytes are the freeze blob, extracted with `git show` (never the worktree by path):

```sh
git -C <lane> show f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/frozen-path-preflight.py
```

| property | value |
|---|---|
| sha256 | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| bytes | 11987 |
| blob id at freeze, landing, A1, tip | `b42398273da0449c01f6f26cc630853d58ea55ec` (all four) |
| selftest | `PREFLIGHT_SELFTEST: cases=11 failures=0`, exit 0 |
| environment | python 3.14.8, git 2.56.0, linux 7.2.11-arch1-1 |

The two lines that decide every attack below:

```
:62  def covers(pathspecs, frozen_path):
:63      """True when some pathspec equals or lies under the frozen path."""
:64      fp = frozen_path.rstrip("/")
:65      return any(p.rstrip("/") == fp or p.rstrip("/").startswith(fp + "/") for p in pathspecs)

:86      if require_pathspec:
:87          missing = [fp for fp in freeze_paths
:88                     if tree_at(root, base, fp) and not covers(pathspecs, fp)]
:89          if missing:
:90              return 2, {"reason": "pathspec_required", "uncovered_frozen_dirs": missing}
```

`covers()` accepts `p == fp` **or `p` a descendant of `fp`**. The claim text is the other relation.
`SKILL.md:590` row 5 reads "a frozen path is a directory at FREEZE and **no pathspec covers it** …
a whole-tree scan is refused", and `plans/round-45-claims.md:136-137` says `--require-pathspec`
"refuses a directory freeze without the pathspec (the round-44 defect: a whole-tree scan hid the
frozen eight)". A pathspec covers a directory when it **is** that directory or an ancestor of it.
The implementation accepts only the directory itself or something **inside** it. Coverage and
containment are inverted, and both directions of the inversion are observable (§3, P-1/P-2).

## 2. Fixtures

Every attack runs in its own fresh repo (`git init -q`, `user.email`/`user.name` set, one `freeze`
commit), under `$TMPDIR` = scratch; `git -C "$D" rev-parse --show-toplevel` was asserted equal to
`realpath "$D"` before the first commit in every fixture (`TOLEVEL_FAIL=0` in `attacks.out`).

```
tools/x/a.txt                 "alpha\n"
tools/x/sub/s.txt             "sub\n"
tools/x/nested/deep/d.txt     "deep\n"      (attacks.out fixture only)
tools/xy/k.txt                "sib\n"       (attacks2.out fixture only)
plans/c.md                    "plan\n"
other.txt                     "other\n"     (attacks.out fixture only)
```

The driver is one function, so every receipt names its exact arguments:

```sh
python3 -I -B "$PF" --root "$D" --freeze "$F" --rev "$R" [attack flags]
# $PF = the extracted freeze blob; $F/$R = fixture commit ids or the lane's freeze/tip
```

## 3. Attack results

`expect` is what the frozen claim text says should happen, `obs` is exit / decisive stdout fields.
All stdout sha256 values are of the shipped `attacks*.out` lines (full stdout is in those files).

### 3.1 The five assigned attacks

| # | fixture / flags | expect (claim text) | obs | exit | verdict |
|---|---|---|---|---|---|
| a | dir `tools/x`; `--freeze-path tools/x --require-pathspec` | 2 `pathspec_required` | `{"reason":"pathspec_required","uncovered_frozen_dirs":["tools/x"],"verdict":"could_not_evaluate"}` | **2** | **holds** |
| b | same; `+ --pathspec tools/x/` | 0/1 as evaluated | `verdict clean`, `touched []`, `blob_changed []` (clean tree); with `tools/x/a.txt` touched → exit **1**, `blob_changed ["tools/x","tools/x/a.txt"]`, one `touched` entry | **0** / **1** | **holds** |
| c | same; `+ --pathspec tools/x` (no trailing slash) | covered? | `verdict clean`, `pathspec ["tools/x"]`; the equals branch of `covers()` accepts it, and git treats `tools/x` as the directory recursively (a touch of `tools/x/a.txt` under this spec is red, F/G pattern) | **0** | **holds** |
| d | same; `+ --pathspec tools/` (parent) | covered → 0/1 | **2** `pathspec_required`, `uncovered_frozen_dirs ["tools/x"]` — byte-identical to attack (a) | **2** | **falsified** (safe direction) |
| d2 | same; `+ --pathspec .` (repo root) | covered → 0/1 | **2**, same bytes as (a) | **2** | **falsified** (safe direction) |
| e | **file** freeze `plans/c.md`; `--freeze-path plans/c.md --require-pathspec`, no pathspec | rule fires only for a directory → no fire | `verdict clean`; and the file is still verified: a committed change → **1** `blob_changed ["plans/c.md"]`, a touch-then-restore → **1** `restored ["plans/c.md"]` | **0** | **holds as written** — see 3.2 (e′) |

The `d`/`d2` receipts are not "wrong exit for a broken tree": the tree is clean and the instrument
returns 2 because a pathspec that **covers** the frozen dir is refused. That is `covers()` reading
containment as coverage. It fails closed (a 2 is never a pass), so it is a usability/claim-text
defect, not a false green.

### 3.2 What the five attacks do not cover — and where the false green is

| # | fixture / flags | expect | obs | exit | verdict |
|---|---|---|---|---|---|
| e′ | dir `tools/x` **+ file** `plans/c.md` frozen; `--pathspec tools/x/ --require-pathspec`; `plans/c.md` tampered, then restored in a second commit | 1 `restored ["plans/c.md"]` ("a later restore does not un-block", `plans/round-45-claims.md:143-145`) | `{"blob_changed":[],"touched":[],"restored":[],"verdict":"clean"}` | **0** | **falsified** |
| e″ | same tree, `+ --pathspec plans/c.md` | 1 | `restored ["plans/c.md"]`, two `touched` entries | **1** | control (holds) |
| H | dir only; `--pathspec tools/x/sub/`; `tools/x/a.txt` tampered then restored | 1 | `verdict clean`, `touched []`, `restored []` | **0** | **falsified** |
| U | dir only, second fixture; `--pathspec tools/x/sub/`; same tamper/restore | 1 | `verdict clean` | **0** | **falsified** |
| U2 | same repo, `--pathspec tools/x/` | 1 | `restored ["tools/x/a.txt"]` | **1** | control (holds) |
| G | `--pathspec tools/x/sub/`; `tools/x/a.txt` **left** changed | 1 | exit 1 but `touched []`; only `blob_changed ["tools/x"]` (the tree oid) fires | **1** | holds; receipt shape wrong (P-4) |
| S4 | dir freeze, `--pathspec tools/x/a.txt` (one file inside the dir) | covered | `verdict clean`, `pathspec ["tools/x/a.txt"]` | **0** | **falsified**: a one-file scan satisfies the directory requirement |
| W1 | **live lane**, `--freeze-path tools/round-45 --require-pathspec --pathspec tools/round-45/c1-counter.py` | covered | `verdict clean` | **0** | **falsified** on real names (see P-1) |
| W2 | live lane, both frozen paths, pathspec still only `tools/round-45/c1-counter.py` | covered | `verdict clean`, `freeze_paths ["tools/round-45","plans/round-45-claims.md"]`, `pathspec ["tools/round-45/c1-counter.py"]` | **0** | **falsified** |

### 3.3 The "whole-tree scan" question, tested in both directions

| # | flags | obs | exit | reading |
|---|---|---|---|---|
| S3 | `--pathspec .` alone | `pathspec_required ["tools/x"]` | **2** | refused — the only case where row 5's "a whole-tree scan is refused" is true |
| S2 | `--pathspec . --pathspec tools/x/` | `pathspec [".","tools/x/"]`, `verdict clean` | **0** | **accepted whole-tree scan** — row 5's clause is false as written; this scoping is strictly wider than the freeze, so nothing is hidden by it |
| S | same as S2 in a repo carrying a restored file | `restored ["plans/c.md"]` (the `.` pathspec pulled `plans/c.md` into the frozen set via `ls-tree`) | **1** | the whole-tree spec also broadens the blob set; no hiding |

So: **no acceptance lets a whole-tree scan pass *as* a directory-freeze scan in a way that hides a
frozen path** — the hazard is the mirror image. A **narrower-than-the-freeze** pathspec is accepted
as coverage (S4, W1/W2 on real names), and then the log scope at `:92-94` and the blob set at
`:112-119` are both derived from that narrow pathspec, so everything outside it is invisible:
G shows the commit arm already blind (`touched []`), and H/U/e′ show the restore arm going to
`clean`. That is the flag the wave asked for, in the direction the rule actually fails.

### 3.4 Fail-closed controls (all hold)

| # | flags | obs | exit |
|---|---|---|---|
| O | two dir freezes, `--pathspec tools/x/` only | `uncovered_frozen_dirs ["tools/xy"]` | **2** |
| P | `--pathspec tools/xy` for frozen `tools/x` (shared character prefix) | `pathspec_required` | **2** (the `fp + "/"` test is segment-safe) |
| Q | `--freeze-path tools/x/` (trailing slash), no pathspec | `uncovered_frozen_dirs ["tools/x/"]` | **2** |
| Q2 | same, `+ --pathspec tools/x/` | clean | **0** |
| N | `--pathspec tools/x/`, unrelated `other.txt` touched | clean | **0** |
| M | `--freeze-path tools/nosuch` (absent at FREEZE), `--require-pathspec` | **clean**, no arm records the absence | **0** (P-3) |
| K2/T3 | both frozen paths, no pathspec | `pathspec_required ["tools/x"]` | **2** |

## 4. Findings

**P-1 (HIGH — false green, reachable with a correct spell).** `covers()` (`:62-65`) accepts a
pathspec **inside** the frozen directory, and that pathspec then narrows the commit arm (`:92-94`)
and the blob set (`:112-119`). A pathspec inside the freeze is therefore not coverage, it is a
scope reduction.

- Input: freeze `tools/x`; commit 1 writes `tools/x/a.txt`; commit 2 restores the freeze bytes;
  `--pathspec tools/x/sub/ --freeze-path tools/x --require-pathspec`.
- Observed: exit **0**, `{"touched":[],"restored":[],"blob_changed":[],"verdict":"clean"}`
  (`U`, `H`).
- Expected by the claim: exit 1, `restored ["tools/x/a.txt"]` — the frozen claims file states "a
  later restore does not un-block (the counter's arm reads commit history, not tip equality)"
  (`plans/round-45-claims.md:143-145`), and block 22 row 2 names exactly this trigger.
- Real-name reach: on the live lane a single instrument file is enough —
  `--pathspec tools/round-45/c1-counter.py` returns exit **0** with both frozen paths named
  (`W1`, `W2`), i.e. the requirement certifies 1 of the 5 frozen files. `SKILL.md:570-571` already
  says "one pathspec certifies four of the five frozen files (R45-CL10)"; the fifth can be the
  *only* file named.
- Fix: invert the predicate to coverage-or-equality and scope the arms from the frozen set, not
  from the caller's pathspecs (§6).

**P-2 (MEDIUM — claim text falsified in two clauses, safe direction).** `SKILL.md:590` row 5 and
`plans/round-45-claims.md:136-137`:

1. "no pathspec **covers** it" is implemented as "no pathspec is equal to or inside it". A parent
   pathspec (`tools/`, `.`) covers the frozen dir and is refused with exit 2 (`D`, `D2`), byte-
   identical to the no-pathspec receipt (`e36c9e48…`).
2. "a whole-tree scan is refused" is false unqualified: `--pathspec .` alone is refused (`S3`), but
   the whole-tree scan is accepted whenever a covered pathspec is also present (`S2`, exit 0), and
   a whole-tree scan is also accepted for a file-only freeze with no pathspec at all (`R`, exit 0).
   The refusal is of a *bare* `.` token, not of the scan.

**P-3 (HIGH — false green when the table's own invocation is followed).** Block 22 row 5 scopes the
pathspec rule to "a directory at FREEZE", and the R45 freeze has one directory **and one file**.
Following the table exactly — `--pathspec tools/round-45/ --freeze-path tools/round-45
--freeze-path plans/round-45-claims.md` — leaves the frozen **file** outside the log scope. A
tamper-then-restore of that file then yields exit **0 clean** (`T`), while the same repo with the
file's pathspec added yields exit **1**, `restored ["plans/c.md"]` (`T2`). The dirty arm has the
same shape (peer `R45W1PreflightDirtyReplay` F-6, and `SKILL.md:571-572` routes it as R45-CL10);
the **history/restore** arm is the part the record does not name. The command that closes it is the
one A2 already prescribes (`SKILL.md:569`) — so the record's *invocation* is right while its *rule*
(row 5) is incomplete. Score impact: none for C1, because the scored counter does not take a
pathspec (§5).

**P-4 (LOW — receipt fidelity).** When the commit arm is blinded by scope, the failure is reported
through the blob arm only, and `touched` is empty while the verdict is red (`G`:
`blob_changed ["tools/x"]`, `touched []`). Row 1's receipt cell is `touched[]`; a consumer that
reads the receipt shape as the table describes it sees no commit record for a real touch. A3
already states the arms are not isolated; this is the same limit seen from the receipt side, and it
matters for P-1 because the tree-oid entry is what prevents `G` (a left-changed file) from being a
full blind spot — only the *restore* case escapes both arms.

**P-5 (LOW — evidence).** A `pathspec_required` receipt does not echo the pathspecs that were
supplied, so attack (a) (no pathspec) and attack (d) (a covering pathspec, refused) print
**byte-identical** stdout (`e36c9e48…`). A receipt consumer cannot tell "no pathspec" from "a
pathspec that covers the freeze was refused". Also `M`: a `--freeze-path` absent at FREEZE yields
`verdict clean` with no arm recording that the named path was never inspected (peer F-5 pins the
same boundary: both arguments must miss for the clean).

**P-6 (MEDIUM — the stated rationale is inverted, and the item it justifies does not close the
defect it cites).** `plans/round-45-claims.md:137` attributes round 44 to "a whole-tree scan hid the
frozen eight". Measured on the M44-2 shape in a fixture: a whole-tree **dirty** scan reports all
eight (`X1`, exit 1, 8 `dirty`), the frozen-scope dirty scan reports the same eight (`X2`, exit 1),
and the same tree **without** the dirty arm reports `clean` (`X3`, exit 0). A whole-tree *log* scan
over-reports rather than hides — the W1 replay measured 542 `touched` for a defect of 8
(`w1/R45W1PreflightReplay/report.md:91-94`), and `corpus/lessons/round-44.md` R44-CL1 states the
cause as "no gate saw the frozen-path write … the round had no commit-time gate", not as a scope
problem. The defect closed by the pathspec requirement is the *counting* one (8 vs 542), not
detection; and the requirement as implemented reduces detection (P-1). The rationale should say
what the arm actually does, or the arm should be re-specified to add coverage instead of removing
it.

## 5. Blast radius on the landed verdict

- **R45-C1's score is not affected.** `tools/round-45/c1-counter.py:52-56` implements the freeze arm
  itself over a hard-coded `FROZEN = [CLAIMS, "tools/round-45"]` and accepts no pathspec argument;
  it cannot be narrowed by a caller. The measured receipt
  `.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json` reports `frozen_path_changed []`,
  `met_target true`, exit 0. P-1/P-3 are defects of the **standalone gate** and of the **rule text**
  (block 22 row 5, claims `:136-137`), not of the scored predicate.
- The record already names half of this: `SKILL.md:565-572` requires an invocation to name every
  frozen path and routes "one pathspec certifies four of the five frozen files" as R45-CL10, and
  SCORECARD cites the *both-path* receipt (`preflight-round45-frozen-both.json`, exit 0 at
  `faa875bc`). What is missing is that a **narrower** pathspec certifies the requirement at all
  (P-1), and that the frozen file's **restore** is invisible under the table's own directory-only
  invocation (P-3).
- Receipt hazard, no claim damage: `.ufo/waves/round-45/l1/preflight-round45-frozen.json` (the
  round-named one) has `freeze_paths ["tools/round-45"]` and `pathspec ["tools/round-45/"]` — the
  frozen claims file is absent from it, and a clean verdict there is scoped to 1 of 2 frozen paths.
  It is not cited by SCORECARD (which cites the `…-both.json` receipt), and the W1 report saw it as
  an untracked file. Keep it out of the evidence chain, or rename it; as filed it invites the
  reading that the round's freeze was verified whole.

## 6. Fix specification (patch-level, for the L1 to route)

1. `covers()` (`:62-65`) — invert to coverage-or-equality:

```python
def covers(pathspecs, frozen_path):
    """True when some pathspec is the frozen path or an ancestor of it."""
    fp = frozen_path.rstrip("/")
    return any(fp == p.rstrip("/") or fp.startswith(p.rstrip("/") + "/") for p in pathspecs)
```

2. Arms must not be narrowed by the caller's pathspecs (`:92`, `:112-119`). Scope them by the union
   of the frozen paths and the pathspecs, and enumerate the blob set from `freeze_paths` first:

```python
scope_paths = sorted(set(pathspecs) | set(freeze_paths))
scope = ["--"] + scope_paths if scope_paths else []
...
for fp in freeze_paths:      # plus each extra pathspec, for the sweep-count use case
    listing = git(root, "ls-tree", "-r", "--name-only", base, "--", fp)
```

   Either change alone closes H/U/e′; both together keep the sweep-counting property the pathspec
   was introduced for.
3. Receipt: echo the supplied `pathspec` on the `2` path (P-5), and report
   `absent_frozen_paths[]` when `tree_at()` is false instead of returning clean with no record
   (`M`).
4. Selftest: add `red-narrow-pathspec-restore` (P-1), `red-file-freeze-restore-outside-pathspec`
   (P-3), and `green-parent-pathspec-accepted` (P-2). Today's 11 cases cannot see any of the three:
   `dir_with_pathspec` passes the exact directory only, and no case passes a pathspec that is
   narrower or broader than the freeze.

## 7. What holds

- (a) fails closed with the right reason and the right `uncovered_frozen_dirs`.
- (b) evaluates on a clean tree and goes red on a real touch (both arms).
- (c) the no-trailing-slash spelling is accepted and is genuinely recursive in git.
- (e) a file-only freeze does not trip the rule, and the file is still caught by the whole-tree scan
  for both a change and a restore (`E2`, `R2`).
- Fail-closed on: a second uncovered directory (O), a sibling with a shared character prefix (P), a
  trailing-slash freeze path (Q), a rename-free unrelated touch (N).
- The frozen bytes are intact: the interpreter blob and `plans/round-45-claims.md` are
  `b4239827…`/`f93df4c3…` at freeze, landing, A1 and tip; no receipt in this report was affected by
  the concurrent tip move.

## 8. Not run / limits

- The counters and the registry scope were not executed (out of seat scope); `c1-counter.py:52-56`
  was read to establish §5 only.
- No rename, delete, submodule or non-ASCII path was exercised against the pathspec check; no merge
  commit was put in `FREEZE..REV` for this arm.
- Git pathspec magic was not tested: `:(top)tools/x`, `:/`, and `:!` forms are all refused by the
  lexical test (a P-2 false-2 class), but I did not measure them.
- The wave-1 reports' F-6 (dirty arm for a frozen file) and F-7 (narrow pathspec accepted) are
  independent prior findings; H/U replicate F-7 and e′/T extends F-6 from the worktree to the
  restore arm. I have not re-litigated their other findings.

## 9. Artifacts and restoration

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-45/w2/R45W2PathspecArm/`:

- `attacks.out` — the five assigned attacks plus controls (A–N), 16:00:23Z.
- `attacks2.out` — fail-closed controls, file-freeze history, live-lane pair (O–V2), 16:01:38Z.
- `attacks3.out` — whole-tree clause and real-name narrow pathspec (S2–W3), 16:02:02Z.
- `attacks4.out` — M44-2 shape with and without the dirty arm (X1–X3), 16:03:08Z.
- `attacks{,2,3,4}.sh` — the drivers; every receipt row is `name | expect | exit | stdout sha256 |
  UTC | full stdout`.
- `report.md` (this file); the same content is at `.ufo/waves/round-45/w2/R45W2PathspecArm.md`.

Restoration evidence: the instrument copy was never edited — its sha256 equals the freeze blob at
every revision measured (`633ebc05…`, 11987 bytes); no lane file outside this report directory was
written (git status showed only untracked `.ufo/waves/round-45/*` before and after this run); the
scratch tree (`preflight.py`, four drivers, four outputs, all `repo.*` fixtures) was removed after
the copy, so nothing citable lived under `/tmp`. Installs: none (pacman paused host-wide, nothing
needed).
