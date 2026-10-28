# R45W2RestoredArm — adversarial falsification of the `restored` classifier (routed R44-CL10)

Seat: `R45W2RestoredArm` (wave 2, round 45). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`;
amendment A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`. Lane HEAD at the end of this seat's run:
`0ee50aaff516571aa607769bbbdf19a3db90dfa5` (all three are ancestors; `merge-base --is-ancestor` yes).

Seat task: attack the `restored` classifier in `tools/round-45/frozen-path-preflight.py`
(`evaluate()`, the `blob_changed` / `restored` loop) against the frozen row it landed for
(R44-CL10: "a later restore does not un-block").

## Instrument identity (what was attacked)

| item | value |
|---|---|
| lane interpreter | `tools/round-45/frozen-path-preflight.py` sha256 `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| attacked copy | `$S/preflight.py`, sha256 identical, `cmp` exit 0 |
| claims file | `plans/round-45-claims.md` sha256 `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` |
| frozen-path drift since freeze | `git log --oneline f762b72..HEAD -- tools/round-45 plans/round-45-claims.md` → no lines |
| lane worktree under frozen paths | `git status --porcelain -- tools/round-45 plans/round-45-claims.md` → no lines |

All runs used `python3 -I -B` on the scratch copy, so no bytecode or state was written into the lane.
Every fixture was `mktemp -d -p "$S"` + `git init -q -b main`, with
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the first commit
(printed `toplevel_ok` in every receipt). `TMPDIR=$S` throughout; nothing written under `/tmp`.

Detector under test, for every run:

```
python3 -I -B <copy> --root <D> --freeze <F> --rev <R> \
  --pathspec frozen/ --freeze-path frozen --require-pathspec --json-out <json>
```

Discipline: each fixture's **baseline** run (`--rev` = the freeze commit) is recorded first and
must be exit 0 `clean`; a baseline failure would make that fixture inconclusive. All seven
baselines printed exit 0 with empty lists (stdout sha256 varies only with the embedded shas).

## Verdicts

| # | attack | expected by the landed record | observed | verdict |
|---|---|---|---|---|
| A1 | commit freeze bytes → tamper one file + commit → write back the exact bytes + commit | exit 1, `restored` contains the path, `blob_changed` empty | **exactly that** | **holds** |
| A2 (a) | same, but the "restore" writes FREEZE bytes **plus one trailing newline** | claim row 2 says "restored to its FREEZE bytes"; a byte difference is not that | exit 1, `restored []`, `blob_changed ["frozen","frozen/a.txt"]` | **holds** (blob arm, not the restored arm) |
| A3 (b) | tamper **only** in a commit before the freeze; REV only touches an unrelated file | clean (the freeze is the reference) | exit **0**, `verdict clean`, all lists empty | **holds** |
| A4 (c) | file **added after** the freeze, **deleted before** REV | a touch → exit 1 | exit 1, carried by `touched[]` (two records: `A`, then `D`); `blob_changed []`, `restored []` | **holds** |
| A5 (d) | **mode-only** tamper after the freeze (`100644`→`100755`, content never edited) | row 2: `restored` = "touched and later restored to its FREEZE bytes" | exit 1, but the path is in **`restored[]`** while the entry at REV **still differs** from FREEZE (mode `100755`); blob oid identical on both sides | **falsified** (receipt semantics) |
| A6 | tamper+restore committed on a side branch, folded with `git merge --squash`, REV on main | "History, not tip equality, is the evidence: a path that was edited post-freeze and then restored to its exact bytes is still a violation" | exit **0**, `verdict clean`, `touched []`, `restored []`, `blob_changed []` | **falsified** (stated guarantee; no table row violated) |
| A7 | mutation probe: delete the `restored` branch in a copy; also replace it with a tip-equality classifier | the selftest is the red-case evidence for this arm | mu1: selftest **byte-identical** to pristine (11/0, same stdout hash) and M1 still exit 1; mu2: selftest 11/**4**, clean control exit 1 | **holds with the recorded limit** (R45-CL15 confirmed, new evidence) |

## Receipts

Each `.receipt.txt` carries the exact command, exit code, stdout sha256 and UTC. JSON receipts and
raw stdout are stored beside them under `receipts/`.

### A1 — the routed R44-CL10 shape: exact byte restore is caught (holds)

```
FREEZE 327723d7c2d8e84603c89df742d9ba1cc582566a
tamper 9b5e4f76aca41c3eefb7b4b1493266b2ee383f2f   frozen/a.txt "alpha\n" -> "tampered\n"
REV    f2dfb9cd263f2e89557a2f07ed72af9e56bfdc8e   frozen/a.txt -> bytes from `git show FREEZE:frozen/a.txt`
exit=1  stdout sha256 514987387cc39a49b8fd7792ad3e9921b17347514f0846cc778f71f801142118
{"restored": ["frozen/a.txt"], "blob_changed": [], "touched": [
   {"commit": "f2dfb9cd…", "path": "frozen/a.txt", "status": "M"},
   {"commit": "9b5e4f76…", "path": "frozen/a.txt", "status": "M"}],
 "verdict": "frozen_path_changed"}
```

The restored bytes were proven equal to FREEZE before the run, not assumed:
`git hash-object frozen/a.txt` = `git rev-parse FREEZE:frozen/a.txt` = `4a58007052a65fbc2fc3f910f2855f45a4058e74`.
The claim's three-part expectation (`exit 1`, path in `restored`, `blob_changed` empty) is met
exactly. **R44-CL10 is closed for the content-edit case.**

### A2 (a) — restore with a trailing-newline difference (holds; blob arm carries it)

```
FREEZE 327723d7…   REV f36cd353f0bb68871e15afad93e52edbab641696
freeze blob 4a580070…   tip blob dede4985aac14104ba113ac3f13fdfa7c2bbc843  (FREEZE bytes + "\n")
exit=1  stdout sha256 b62cabe7db09d107548e74a58ac6095fa925f762e397e6521374996e35893c1a
{"blob_changed": ["frozen", "frozen/a.txt"], "restored": [], "touched": [M, M], "verdict": "frozen_path_changed"}
```

Not `restored`: the classifier is blob-oid equality, and a one-byte difference is a difference.
The verdict is still red, so the gate is safe — the operator's intent does not launder it.

Calibration note (not a falsification): `blob_changed` mixes a **directory** path (`frozen`, its
tree oid) with the file path, so one edited file yields two records. The table row documents this
("a directory entry is its tree oid, not a file"), but a consumer that counts `len(blob_changed)`
over-counts and a consumer that filters on the file path gets the right answer only if it also
reads the parent. Worth one clause in the receipt column.

### A3 (b) — tamper only before the freeze (holds; clean)

```
C1 initial "alpha\n"  → C2 tamper "tampered-before-freeze\n"  → C3 FREEZE (base = tampered bytes)
REV feae0c73c8b1d8e7f16fc2bb73d90ccbfc257bb9 touches only other.txt
exit=0  stdout sha256 c56e4e9eb9dbcf63cbabcbd2b92acb9aa1bfe05245b2216896404f02e0554da1
{"blob_changed": [], "dirty": [], "restored": [], "touched": [], "verdict": "clean"}
```

Correct by definition: a `FREEZE..REV` scan cannot audit the freeze. Calibration for the record —
this gate is not a freeze-content auditor; the frozen bytes are only as good as the commit that
was frozen. That division of labour should be said once in block 22, because the block's first
sentence ("A freeze is ... an instrument") reads as if it were.

### A4 (c) — added after the freeze, deleted before REV (holds; `touched` is the only carrier)

```
FREEZE 327723d7…   A e142aa74053b185c61720c8fdcdbaa463c6c575d frozen/new.txt
                   D + REV 8d5f53fef7d9345754e9d161f262f8949c55d758 frozen/new.txt
exit=1  stdout sha256 2b4a167850769b3a5fddb40fc92c12f71d45dd67d356d4784b75e3417145012f
{"blob_changed": [], "restored": [], "touched": [
   {"commit": "8d5f53fe…", "path": "frozen/new.txt", "status": "D"},
   {"commit": "e142aa74…", "path": "frozen/new.txt", "status": "A"}],
 "verdict": "frozen_path_changed"}
```

`touched` carries it, twice, and nothing else can: the path exists at neither endpoint, so it is
not in `frozen` (built from `ls-tree` at FREEZE) and both blob arms skip it. The directory entry
`frozen` is *not* in `blob_changed` because the net tree oid is unchanged. Verdict is right; the
row "any commit in FREEZE..REV touches a frozen path → `touched[]`" is the exact rule that fires.
Note for the L1: `touched[]` therefore is not a subset of "paths present at REV", which matters if
anyone joins these lists.

### A5 (d) — **FALSIFIED**: a path that was never restored is reported as `restored`

Exact input (fixture `fx-d-*`, baseline exit 0):

```
FREEZE ec4c2ec27061e8008c3c097a64e986bb19147540   frozen/a.txt mode 100644, blob 4a580070…
chmod +x frozen/a.txt                              content NOT touched
REV    9846d2428770ec4e10e75db2aa4c32a9835594a4   mode 100755, blob 4a580070… (identical)
exit=1  stdout sha256 61764341d01b2384fffca8b2c08bf90de54e07c6b9fa493460c677a6e4fa1e81
{"blob_changed": ["frozen"], "restored": ["frozen/a.txt"],
 "touched": [{"commit": "9846d242…", "path": "frozen/a.txt", "status": "M"}],
 "verdict": "frozen_path_changed"}
```

The classifier is `a.stdout != b.stdout`, i.e. **blob-oid** equality. A mode-only change leaves the
blob oid equal, so the file path falls into `restored[]` even though its **tree entry at REV still
differs from FREEZE** (`100755` vs `100644`). Nothing was restored; `restored` names the one list
that is supposed to mean "put back".

Differing value, stated exactly:

* claimed (block 22, row 2): `restored` = a frozen path "touched and later **restored to its FREEZE
  bytes**", receipt `restored[]`, disjoint from `blob_changed[]`;
* observed: `restored = ["frozen/a.txt"]` for a path whose FREEZE entry was `100644 blob 4a580070…`
  and whose REV entry is `100755 blob 4a580070…` — restored is false.

A second shape makes the same defect visible through the disjointness claim (`fx-e-*`, baseline
exit 0): tamper the content **and** chmod to 755, then restore only the content —

```
FREEZE ec4c2ec2…  REV 98999cb2f10ae562f8f999750ee010cdedf99f75   mode 100644 -> 100755
exit=1  stdout sha256 679260a6ce616897563a5bd239410a13a424bd97f593d3cf54f2507d9648252d
{"blob_changed": ["frozen"], "restored": ["frozen/a.txt"], …}
```

`restored[]` and `blob_changed[]` are disjoint **as path strings**, as claimed — and the very tree
entry they both describe is reported as "restored" at file level and "changed" at parent level.
The disjointness is mutual exclusion by construction (`if … elif`), so it carries no information
about whether the entry is intact. The claim is true and the receipt is still misleading.

**Fix (smallest correct change).** Classify on entry equality, not blob equality. Replace the blob
`rev-parse` pair with a mode+oid comparison, e.g.

```python
def entry(root, rev, path):
    p = git(root, "ls-tree", rev, "--", path)
    return p.stdout.strip() or None          # "100644 blob <oid>\tpath"
...
a, b = entry(root, base, path), entry(root, tip, path)
if a != b:  blob_changed.append(path)        # covers content AND mode
elif any(t["path"] == path for t in touched):
    restored.append(path)
```

or, minimally, keep the blob pair and add `git diff --quiet base tip -- <path>` (returncode 1 →
`blob_changed`) before admitting the path to `restored`. Then either add a twelfth selftest case
(`red-chmod-only`, expect 1 with `restored == []`) or state in row 2 that "restored" means
**blob**-equal, not entry-equal — the first is the real fix, the second is the honest label.

Exit code is unaffected in both shapes (still 1), so this is a receipt-integrity finding, not a
false-clean here. It becomes a false-clean the moment a consumer treats `restored[]` as "safe to
ignore" — which is precisely what the list name invites.

### A6 — **FALSIFIED**: rewritten history degenerates the arm to tip equality

Exact input (fixture `fx-squash-*`, baseline exit 0):

```
FREEZE 327723d7…  main
  git checkout -b side
  side: frozen/a.txt "alpha\n" -> "tampered\n"      (commit side_tamper)
  side: frozen/a.txt -> exact FREEZE bytes          (commit side_restore)
  git checkout main
  git merge --squash side      # net diff on frozen/ is empty
  commit "squash_merge_of_side" + one unrelated other.txt edit = REV 8a6134828363506b9db2ff187cbbf4ee5816bd35
exit=0  stdout sha256 4a6baadd2eabfb529af9d7d45e212f7cf914622a02d02557bfa52d289becbfa2
{"blob_changed": [], "dirty": [], "restored": [], "touched": [], "verdict": "clean"}
git log --name-status FREEZE..REV -- frozen/   -> no output
git log --oneline FREEZE..REV                  -> 8a61348 squash_merge_of_side
```

A frozen file was edited after the freeze and put back, and the gate returns **clean, exit 0**.
The mechanism is exact: `touched` is derived from `git log FREEZE..REV`, and the two commits that
performed the edit and the restore are **not reachable** from REV after a squash, so there is no
touch to find; the blob arms then see tip equality. This is the R44-CL10 failure mode restored in
full, reachable with three ordinary git commands.

Scope of the finding, stated honestly: **no table row is violated.** Row 1/row 2 are scoped to
"any commit in FREEZE..REV", and after a squash there is no such commit. What is false is the
prose guarantee the row is justified by — block 22: "History, not tip equality, is the evidence: a
path that was edited post-freeze and then restored to its exact bytes is still a violation". Under
a squash fold that sentence is simply untrue; the gate is at tip equality for that subtree.

**Fix (prose + procedure, no code can see it).** Amend block 22 to name the precondition:
"…*provided the touch commits are reachable from REV*. History rewriting that drops them (squash,
rebase, a discarded branch) makes this arm tip-equality again; the only cover there is the
`--check-dirty` arm at write time, so the gate must be run per commit on the branch that is being
written, not once at REV." If the lane wants code rather than prose, the only detector is to run
the gate against each written commit's own tip (which the L1 commit sequence can do), not to
widen `git log` (there is no wider range that contains an unreachable commit).

I did **not** exercise rebase (`git rebase --onto` dropping the tamper commit); it is the same
class, but this receipt is squash only, and I am not claiming rebase without a run.

### A7 — mutation probe on the scratch copy (restored arm not isolable)

| mutant | bytes | selftest | M1 fixture | clean control |
|---|---|---|---|---|
| pristine | `633ebc05…` | exit 0, 11/0, stdout `9f03df65…` | exit 1, `restored ["frozen/a.txt"]` | exit 0 |
| mu1: `elif any(...)` → `elif False:` | `93ce71c1…` | exit 0, 11/0, stdout **`9f03df65…` (byte-identical)** | exit 1 (touched absorbs), `restored []` | exit 0 |
| mu2: same branch → `else:` (tip equality) | `f4e1bef5…` | exit 1, 11/**4** (`green-clean`, `green-dirty-without-arm`, `green-dirfreeze-pathspec`, `green-empty-range`), stdout `dd2a3741…` | exit 1, `restored ["frozen","frozen/a.txt","frozen/b.txt"]` | exit 1, three `restored` entries |

* mu1 **survives** everything: identically to the recorded R45-CL15 claim, deleting the `restored`
  classification changes no exit code and — new evidence — produces a **byte-identical selftest
  transcript**. The arm has zero unique detection in the whole 11-case battery. This seat added no
  kill; the finding stands as recorded.
* mu2 is killed, but only by the four *green* cases (a false positive on clean input). No case
  distinguishes the correct restored predicate from any other predicate on the red side, because
  `touched` supplies the exit.

Restoration: the pristine scratch copy was never edited (mutants are separate files:
`preflight-mu1.py`, `preflight-mu2.py`), the lane interpreter's sha256 is unchanged before and
after (`633ebc05…`), and `git status --porcelain -- tools/round-45 plans/round-45-claims.md` is
empty at HEAD `0ee50aaf`. No restore step was needed because no shared byte was mutated.

## What this seat says to the L1

1. **R44-CL10 is fixed for content edits** (A1: exact restore → `restored`, exit 1) and for the
   byte-difference variant (A2: `blob_changed`, exit 1). Restoring does not un-block.
2. **Row 2's receipt is wrong for non-content touches** (A5). `restored` means blob-equal, so a
   mode-only change is reported as restored while the entry still differs. Fix: entry equality
   (`ls-tree`) or `git diff --quiet`; add `red-chmod-only`.
3. **The prose overstates history-vs-tip-equality** (A6). A squash fold of a tamper+restore branch
   is `clean, exit 0`. No row is violated; the sentence needs its precondition and the procedure
   needs per-commit gating.
4. **The arm remains non-isolable** (A7), now with a byte-identical-transcript receipt rather than
   only a case count. Round 46's "add per-arm isolation cases" (R45-CL15) is still the right call,
   and the isolation case must assert **receipt values**, not exits: a case that only checks exit 1
   cannot kill mu1.
5. A2/A3 carry two calibration clauses the block does not yet state: `blob_changed` contains the
   parent tree path alongside the file, and the gate cannot audit the freeze it is given.

## Not run (honest gaps in this seat)

* rebase/rebase-onto as a second rewritten-history shape (same class as A6, not exercised);
* `filter-branch`/`git replace` history rewriting (out of the bounded gate's threat model);
* untracked `??` entries and the `--dirty-pathspec` replacement false-clean (wave-1 `x2`/`x3`
  already hold those receipts; not re-run here).

## Receipt index (`receipts/`)

`m1-baseline`, `m1-restored`, `a-baseline`, `a-trailing-nl`, `b-baseline`, `b-pre-freeze-tamper`,
`c-baseline`, `c-add-then-delete`, `d-baseline`, `d-chmod-only`, `e-baseline`,
`e-restore-content-only`, `s-baseline`, `s-squash`, `mut-pristine-on-m1`, `mut-mu1-on-m1`,
`mut-mu2-on-m1`, `mut-pristine-clean`, `mut-mu1-clean`, `mut-mu2-clean` — each with
`.receipt.txt` (command, UTC, exit, stdout sha256), `.stdout` and `.json`; plus
`selftest-preflight{,-mu1,-mu2}.{stdout,receipt.txt}`, `mutants.sha256`,
`lane-frozen-state.receipt.txt`, and the drivers `run-attacks.sh`, `run-probes.sh`
(copied verbatim from `$S`).
