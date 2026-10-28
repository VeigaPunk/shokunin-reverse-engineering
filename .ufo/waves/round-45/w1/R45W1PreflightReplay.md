# R45W1PreflightReplay — replay of the round-44 sweep defect against real lane history

Seat: `R45W1PreflightReplay` (leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Instrument under test: `tools/round-45/frozen-path-preflight.py`, sha256
`633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` (the frozen copy in
scratch hash-equals the lane original; both hashed in the same call).

All receipts are under `.ufo/waves/round-45/w1/R45W1PreflightReplay/`; the index with
argv/exit/UTC/stdout-sha256 is `receipts-index.json`. Nothing in `plans/`, `tools/`,
`corpus/`, `SKILL.md`, `LOG.md`, `SCORECARD.md` was written; no mutating git command ran
(the fixture repos under `$S` used `git -C "$D"` only, each with a verified
`rev-parse --show-toplevel` == `$D`, `probe-fixture-toplevel.json`). No tool was installed.

## 1. Revisions (both re-derived, both resolvable, freeze is an ancestor)

| role | given | `git rev-parse --verify <r>^{commit}` | derivation |
|---|---|---|---|
| round-44 freeze | `c48f8a4bfd449300c975668e59aae5b5538b6a84` | resolves to itself | `git log --format=%H -1 -- plans/round-44-claims.md` → `c48f8a4b…` ✔ matches the claims-file rule |
| round-44 rev | `c86ea508` | `c86ea508188c50e2645b1f9bba65df4177cda6b1` ("round-44: land the post-freeze control fixtures and unsettled wave evidence") | — |
| round-45 freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | resolves to itself | `git log --format=%H -1 -- plans/round-45-claims.md` → `f762b72…` ✔ |

`git merge-base --is-ancestor c48f8a4b c86ea508` → exit 0. **Neither revision is unknown and
the freeze is an ancestor of the rev**, so no substitution was needed. (`tools/round-44/
control-fixtures` is a `tree` at `c48f8a4b`, i.e. a genuine directory freeze: `git cat-file -t
c48f8a4b:tools/round-44/control-fixtures` → `tree`.)

**The instrument executed is the frozen blob** (`receipt-e-freeze-blob-identity.json`): every
frozen path's worktree bytes hash-object to exactly its blob id at `f762b72`, so the replay
below ran the freeze bytes, not a post-freeze edit, and `git status` cleanliness (receipt D) is
backed by content hashes rather than mtime.

| frozen path | bytes | sha256 | hash-object == blob at freeze |
|---|---|---|---|
| `plans/round-45-claims.md` | 9461 | `56bacf3143e904ae…` | yes |
| `tools/round-45/c1-counter.py` | 14319 | `2cfc5a4853585879…` | yes |
| `tools/round-45/c2-counter.py` | 9560 | `50212d0f456107ed…` | yes |
| `tools/round-45/frozen-path-preflight.py` | 11987 | `633ebc058f0ea5a7…` | yes |
| `tools/round-45/registry-scope.json` | 750 | `6e2dda713a474dd6…` | yes |

(11987 B for the preflight agrees with the peer's `git cat-file -s`; its selftest stdout agrees
to the byte — §5.)

## 2. The replay (canonical command, exit code, count, verdict)

```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-45/frozen-path-preflight.py --root . \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 \
  --pathspec tools/round-44/control-fixtures/ \
  --freeze-path tools/round-44/control-fixtures --require-pathspec \
  --json-out .ufo/waves/round-45/w1/R45W1PreflightReplay/receipt-a-replay-pathspec.json
```

**exit `1`** — verdict `frozen_path_changed`. `touched` = **8**, and the subset under
`tools/round-44/control-fixtures/` is **all eight** (expectation met), every one of them from
the sweep commit `c86ea508`:

| # | status | path |
|---|---|---|
| 1 | M | `tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json` |
| 2 | M | `tools/round-44/control-fixtures/c3/manifest.json` |
| 3 | M | `tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1be/after.json` |
| 4 | M | `tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json` |
| 5 | M | `tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2be/after.json` |
| 6 | M | `tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v2le/after.json` |
| 7 | M | `tools/round-44/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` |
| 8 | M | `tools/round-44/control-fixtures/pos/manifest.json` |

`blob_changed` has 9 entries (the eight files **plus** the `control-fixtures` tree entry, whose
tree hash necessarily differs); `restored` `[]`, `dirty` `[]` (dirty arm not requested).
UTC `2026-10-28T15:41:56Z`; stdout sha256 `264e92af1911798a69663fca07b61591c808b41d42a43a6c3df2b011dc7bf535`.
Re-run reproduces the byte-identical stdout (same sha as the first capture at 15:38:58Z).

Context that makes the count meaningful: the range `c48f8a4b..c86ea508` is **7 commits, 536
distinct paths**, and the sweep commit on its own is **exactly 432 paths**
(`git diff-tree --no-commit-id --name-only -r c86ea508 | wc -l` → 432 — this is the "432 paths"
figure in `plans/round-45-claims.md`; it is the single commit, not the range). The pathspec
narrows the gate's own count from 536/542 to the 8.

## 3. Same gate WITHOUT `--pathspec` (must not silently pass)

Two variants, because "without `--pathspec`" leaves the `--require-pathspec` arm as a choice:

| receipt | args | exit | reported |
|---|---|---|---|
| `receipt-b1-nopathspec-required.json` | no `--pathspec`, `--require-pathspec` kept, `--freeze-path tools/round-44/control-fixtures` | **2** | `{"verdict":"could_not_evaluate","reason":"pathspec_required","uncovered_frozen_dirs":["tools/round-44/control-fixtures"]}` |
| `receipt-b2-nopathspec-norequire.json` | no `--pathspec`, **no** `--require-pathspec`, same `--freeze-path` | **1** | `frozen_path_changed`, `touched` = **542** (whole-tree scan over the 7 commits), of which **8** under `control-fixtures/` |

So the gate does **not** silently pass. B1 fails closed at exit 2 before scanning; B2 is red
but with the wrong scope — 542 `touched` entries for a defect of 8, i.e. exactly the round-44
counting failure shape in which "a whole-tree scan hid the frozen eight"
(`plans/round-45-claims.md` §Frozen paths; `corpus/lessons/round-44.md:18,63`). B2's 542 > 536
distinct paths because `touched` is a **per-commit-entry list, not a distinct-path set** (a path
touched in two commits is counted twice) — a receipt consumer must not compare it to
`git diff --name-only | wc -l`.

## 4. This round's own frozen paths at its own freeze — `clean`, exit 0

```sh
python3 -I -B tools/round-45/frozen-path-preflight.py --root . \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
  --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md --require-pathspec
```

**exit `0`**, verdict `clean`, `touched []`, `blob_changed []`, `restored []`, `dirty []`
(`receipt-c-freeze-eq-rev.json`, stdout sha
`862ae746a7eb9b0c30c6112a032438f880df81142d54bf45da907fe2d0d2a43d`).

Extra live receipt (`receipt-d-live-head-dirty.json`): the same frozen set at `--rev HEAD`
= `faa875bc0eb839d15b83c4afa6078819e5a7b381` with `--check-dirty` → **exit 0, `clean`,
`dirty []`**. Independent confirmation: `git log f762b72..HEAD -- plans/round-45-claims.md` and
`-- tools/round-45/` are both empty (5 post-freeze commits, none touching a frozen path). The
landing is clean as of this seat's run; my own writes land only under
`.ufo/waves/round-45/w1/R45W1PreflightReplay*/`, outside every frozen pathspec.

## 5. Attack on the instrument — three false-green classes survive the frozen selftest

`--selftest` on the frozen copy: **exit 0, `PREFLIGHT_SELFTEST: cases=11 failures=0`**
(`probe-p7-selftest.json`), and that stdout is **byte-identical** to the committed
`.ufo/waves/round-45/controls/preflight-selftest.txt` — both 791 bytes, sha256
`9f03df6538de49b7…` (`probe-p23-selftest-vs-committed.json`), so the C1 clause-6 artifact does
reproduce from the frozen bytes. The eleven cases nevertheless leave the following unpinned. Each
finding is a fixture repo under `$S` (verified toplevel) plus a control on the *same* history,
so the difference is the argument set, not the fixture. A standalone reproducer for D1/D2 is
`repro-probes.sh` in this directory (four fixtures, four controls, plus the reversed-pair
exit 2); its last run reproduced every label — 0 for each false green, 1 for each control,
2 for the reversed pair.

### D1 (high) — a frozen **file** not named in `--pathspec` is invisible to 3 of 4 arms

`--require-pathspec` only demands coverage for a frozen path that is a **tree** at freeze
(`tools/round-45/frozen-path-preflight.py:86-89`, via `tree_at` at `:68-70`). A frozen *file*
has no such requirement, and `pathspecs` scopes the commit arm (`:93-95`, `git log … -- <pathspec>`
at `:95`), the dirty arm (`:135`, `dirty_pathspecs or pathspecs`) and, indirectly, the restored
arm (only fires for paths in `touched`, `:126-131`).

| probe | history | args | exit | receipt |
|---|---|---|---|---|
| `probe-p1-filefreeze-dirpathspec.json` | frozen `f.md` written post-freeze, then restored to freeze bytes; frozen dir `d/` | `--pathspec d/ --freeze-path f.md --freeze-path d --require-pathspec` | **0 `clean`** | `touched 0`, `restored []`, `blob_changed []` |
| `probe-p2-control-file-in-pathspec.json` | same repo, same revs | `--pathspec d/ --pathspec f.md …` | 1 `frozen_path_changed` | `restored ["f.md"]` |
| `probe-p3-control-no-pathspec.json` | same | no pathspec, both `--freeze-path`s | 1 | `restored ["f.md"]` |
| `probe-p13-dirty-file-out-of-scope.json` | frozen `f.md` dirty in the worktree, `--check-dirty` | `--pathspec d/ --freeze-path f.md --freeze-path d` | **0 `clean`** | `dirty []` |
| `probe-p14-dirty-file-control.json` | same dirty tree | no pathspec, `--check-dirty` | 1 | `dirty` 1 entry |

This is the round-44 M44-2 shape (a frozen write no arm of the pre-landing gate saw) re-armed
for file freezes. On the **real** round-44 range the same shape stays red —
`probe-p9-real44-filefreeze-excluded.json`, `--pathspec tools/round-44/control-fixtures/` with
the extra `--freeze-path plans/round-44-claims.md`, exits 1 with the 8 — because the frozen
*directory* is itself in scope and the claims file never changed in `c48f8a4b..c86ea508`
(`git log --format=%h c48f8a4b..c86ea508 -- plans/round-44-claims.md` is empty; blob equal,
`db6e06649931…` both sides). The gap turns into a false green only when the touched frozen
path is a **file** outside the scope, as P1/P13 show. **Live instance:** §Frozen paths of
`plans/round-45-claims.md` freezes two
paths — the directory `tools/round-45/` **and the file `plans/round-45-claims.md`** — while the
invocation documented there ("scoring passes `--pathspec tools/round-45/` and `--freeze-path
tools/round-45`") names only the directory. The landed control receipt
`.ufo/waves/round-45/controls/preflight-at-freeze.json` shows `"freeze_paths": ["tools/round-45"]`
and `"pathspec": ["tools/round-45/"]`: **the claims file was not in the gate's frozen set at
all** in the evidence this round already filed. Reproduced as `probe-p16b-documented-head.json`
(exit 0, `freeze_paths ["tools/round-45"]`).

Severity is bounded, not nil: the two counters do cover the file — `tools/round-45/c1-counter.py:32`
and `c2-counter.py:30` hold `FROZEN = [CLAIMS, "tools/round-45"]` and their `frozen_path_changed`
runs `git log --name-only … -- *FROZEN` with no pathspec scope, so a post-freeze write still
scores exit 2. **The gap is at land time, which is the only time the data can still be saved** —
precisely M44-2's lesson (`corpus/lessons/round-44.md:63`). I did not run the counters (their
seats own that); the two constants above are read, not executed.

### D2 (high) — `covers()` accepts a pathspec **narrower** than the frozen directory

`covers(pathspecs, frozen_path)` (`tools/round-45/frozen-path-preflight.py:62-65`) is true when
a pathspec *equals or lies under* the frozen path, so `--pathspec d/a.txt` satisfies
`--require-pathspec` for the freeze-path `d` while the scan covers one file of the directory.
The eight frozen fixtures can therefore be out of scope again with the arm reporting nothing.

| probe | history | args | exit | receipt |
|---|---|---|---|---|
| `probe-p17-narrow-pathspec-restore.json` | frozen dir `d/`; `d/b.txt` (not named in the pathspec) written post-freeze then restored | `--pathspec d/a.txt --freeze-path d --require-pathspec` | **0 `clean`** | `touched 0`, `restored []`, `blob_changed []` |
| `probe-p17-control-dir-pathspec.json` | same repo/revs | `--pathspec d/ …` | 1 | `restored ["d/b.txt"]` |
| `probe-p18-narrow-pathspec-dirty.json` | `d/b.txt` dirty, `--check-dirty` | `--pathspec d/a.txt …` | **0 `clean`** | `dirty []` |
| `probe-p18-control-dir-pathspec-dirty.json` | same dirty tree | `--pathspec d/ …` | 1 | `dirty [" M d/b.txt"]` |

Note the docstring/arm mismatch: the arm's stated purpose is "never by the default whole-tree
scan", but soundness needs the opposite containment direction (the pathspec must **contain**
the frozen path) — the narrow pathspec is the round-44 defect by another route.

### D3 (medium) — the parsers cite S141's `-z` but do not pass it

The docstring cites S141 ("`--name-status` with `-z` terminates fields with NUL", docstring
`:32`, S141 row), yet the log call at `:93-94` uses `--name-status` **without** `-z`, and the
blob arm feeds `ls-tree --name-only` output (`:116`) straight into `git rev-parse "<rev>:<path>"`
(`:123-124`). A path needing C-quoting (non-ASCII bytes, control chars) is emitted quoted, so:

- `probe-p8-nonascii.json` (frozen `frozen dir/naïve.txt` modified): exit 1 via the **commit**
  arm only — `touched` = `[{"path":"\"frozen dir/na\\303\\257ve.txt\"", status:"M"}]`, while
  `blob_changed` = `["frozen dir"]`, i.e. the file itself was silently skipped by the blob arm
  (both `rev-parse <rev>:<quoted…>` fail ⇒ "never existed on either side" ⇒ `continue`).
- `probe-p11-nonascii-restore.json` (same path, touched then restored): exit 1, but
  `restored []` and `blob_changed []` — the **restored classifier never fires** for such a path;
  red came only from `touched` being non-empty. The C1 predicate's "restored" arm is therefore
  proven only for ASCII paths.

No false green results from D3 alone *inside* a covered directory; it composes with D1/D2 into
one, and the reported path strings are not usable as repo paths.

### D4 (medium) — a non-matching pathspec plus a freeze-path absent at freeze is a silent clean

Independently reported by seat `R45W1PreflightDirtyReplay` and reproduced here on this seat's
own fixture (frozen `d/keep.txt`; then 8 files committed into `d/` in one commit):

| probe | args | exit | receipt |
|---|---|---|---|
| `probe-p19-nonmatching-pathspec-real-dir.json` | `--pathspec nosuch/ --freeze-path d --require-pathspec`, `d` a tree at freeze | **2** `pathspec_required` | fails closed |
| `probe-p20-nonmatching-pathspec-and-freezepath.json` | `--pathspec nosuch/ --freeze-path nosuch --require-pathspec` | **0 `clean`** | `touched 0`, `blob_changed 0` — the 8 committed changes are invisible |
| `probe-p21-nonmatching-pathspec-and-freezepath-norequire.json` | same, no `--require-pathspec` | **0 `clean`** | same |
| `probe-p22-control-correct-pathspec.json` | `--pathspec d/ --freeze-path d` | 1 | `touched` 8 |

The fail-open needs **both** arguments to miss: `--require-pathspec` catches a bogus pathspec
whenever the freeze-path really is a tree at freeze (`tree_at`, `:68-70`), but a freeze-path
that does not exist at freeze is never required to be covered, and the log scope then matches
nothing. So the arm that exists to force an explicit scan cannot notice that the scan is
empty — the same "gate reports clean because it looked at nothing" shape as D1/D2, reachable by
a typo in both arguments.

### D5 (low) — `dirty` is a porcelain-field list, not a violation count

`dirty` is every non-empty NUL field of `git status --porcelain -z` (`:135-139`), and porcelain
v1 with `-z` emits a rename's old path as its own field:

| probe | history | exit | `dirty` |
|---|---|---|---|
| `probe-p24-rename-dirty.json` | one staged `git mv d/old.txt d/new.txt` inside the frozen dir, `--check-dirty` | 1 (correct) | `["R  d/new.txt", "d/old.txt"]` — **2 entries for 1 rename** |
| `probe-p24b-rename-porcelain-raw.json` | raw `git status --porcelain -z -- d/` | — | `R  d/new.txt\0d/old.txt\0` |

The verdict is right; the count is not, and the second entry is a bare path with no status
prefix. Same class as the `touched` counting note in §3; measured independently by seat
`R45W1PreflightDirtyReplay` as F-3.

### D6 (info) — scope direction and exit-code hygiene that hold

- `probe-p10-broad-pathspec.json`: `--pathspec tools/round-44/` is refused, exit 2
  `pathspec_required` — a broader-but-sufficient pathspec fails closed, so no false green; a
  caller simply cannot pass a superset.
- `probe-p15-nonancestor-real.json`: `--freeze f762b72 --rev c86ea508` (reversed pair on real
  history) → exit **2** `freeze is not an ancestor of rev`. Correct `could-not-evaluate`, never a
  pass — this is the guard that would have caught a swapped-argument replay.
- `probe-p5-spaced-path.json`: a filename with a space parses correctly (`touched` carries the
  raw path); `core.quotepath` default does not quote spaces, only high bytes.

## 6. Verdict

| question | answer | receipt |
|---|---|---|
| does the frozen gate reproduce the round-44 defect against real history? | yes — exit 1, `touched` 8, all eight under `control-fixtures/` | `receipt-a-replay-pathspec.json` |
| does it pass silently without `--pathspec`? | no — exit 2 `pathspec_required`; and the naive form is exit 1 with 542 entries for 8 defects | `receipt-b1…`, `receipt-b2…` |
| is this round's freeze clean at its own freeze commit? | yes — exit 0 `clean`, both frozen paths named | `receipt-c-freeze-eq-rev.json` |
| is the landing clean now (HEAD `faa875bc`, worktree)? | yes — exit 0 `clean`, `dirty []` | `receipt-d-live-head-dirty.json` |
| is the instrument sufficient as the pre-landing gate for *this* round's frozen set? | **no**, as invoked: the frozen **file** is unprotected (D1), the dir arm can be satisfied by a narrower scan (D2), and an all-missing argument pair scans nothing and reports clean (D4) | probes P1/P13/P16b/P17/P18/P20/P21 |
| does `--selftest` cover those two? | no — 11 cases, 0 failures, no case for any of D1/D2/D4 | `probe-p7-selftest.json` |
| does the committed `controls/preflight-selftest.txt` reproduce from the frozen bytes? | yes — byte-identical, 791 B, sha256 `9f03df6538de49b7…` | `probe-p23-selftest-vs-committed.json` |
| is the instrument this seat ran the frozen bytes? | yes — all five frozen paths hash-object to their `f762b72` blob ids (preflight 11987 B) | `receipt-e-freeze-blob-identity.json` |

Cross-seat agreement: seats `R45W1PreflightReplay` (D1, D2, D4) and `R45W1PreflightDirtyReplay`
(F-6, F-7, non-matching pathspec; report at `.ufo/waves/round-45/w1/R45W1PreflightDirtyReplay/`)
reached the same three classes on **independently constructed fixtures**, each with a
dir-pathspec control on the same history; their F-3 (rename double-count) matches D5 and their
F-4 matches D3, and their selftest sha `9f03df65…` matches p23's byte-identity. Their live-lane
run with the full invocation agrees with receipt D: exit 0, frozen bytes identical across
`f762b727..faa875bc`.

## 7. What the L1 can land from this (nothing applied — I am read-only on the lane tree)

1. C1's receipt for the preflight gate should cite the **both-paths** invocation (receipts C/D),
   not the dir-only form already filed as `controls/preflight-at-freeze.json`; the latter does
   not exercise `plans/round-45-claims.md` at all.
2. D1/D2/D4 are instrument defects in a *frozen* file: they cannot be fixed at `f762b72` without
   making the counters exit 2 `frozen_path_changed`. They belong in `corpus/lessons/round-45.md`
   and in the round-46 claim, not in a post-freeze edit — the counters are the enforcing arm in
   the meantime, and they are sound on both paths.
3. The C1 predicate's clause 6 ("`cases >= 11`, `failures == 0`") is satisfiable while D1/D2/D4
   are open; a count-based selftest clause is a weak proxy for "the arms cover the freeze shape".
4. Neither `touched` nor `dirty` is a path set: `touched` is per-commit-entry (542 vs 536
   distinct in the real range) and `dirty` is per porcelain `-z` field (one rename = 2 entries,
   D5). A receipt that reports "N paths" from either count is wrong about what changed.
5. Invocation-level mitigation usable *now*, without touching the frozen instrument: pass every
   frozen path (both `tools/round-45/` **and** `plans/round-45-claims.md`) as `--pathspec` **and**
   `--freeze-path`, add a `--dirty-pathspec` per frozen path (seat `R45W1PreflightDirtyReplay`
   measured the dirty false green turning to exit 1 under `--dirty-pathspec`), and treat any
   receipt whose `touched` is empty while the range is non-empty as unreviewed rather than clean.
   The durable fix for the next round: make the required containment direction "pathspec ⊇ frozen
   path", pass `-z` to `git log`/`ls-tree` (S141), and refuse an empty scan.

## 8. Not run (stated, not claimed)

- The two counters (`c1-counter.py`, `c2-counter.py`) — other seats own them; only their `FROZEN`
  constant and the `frozen_path_changed` shape were read.
- The round-44 *scoring* re-run — out of this seat's scope.
- No tool installed or upgraded.

Scratch `$S=/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightReplay` (fixtures + the tool copy) was
removed after every receipt above was copied into this directory; nothing under `/tmp` was used.
