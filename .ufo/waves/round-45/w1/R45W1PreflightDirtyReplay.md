# R45W1PreflightDirtyReplay — the M44-2 worktree shape scored against the frozen preflight

Seat: leaf executor, round 45 wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, lane HEAD at run
`faa875bc0eb839d15b83c4afa6078819e5a7b381`. Read-only on the lane tree; every measurement below
ran in private fixtures under `/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightDirtyReplay`
(removed after the receipts were copied here). No lane file was written except this report
directory, no mutating git command ran in the lane repo, no tool was installed.

Canonical copy of this report: `.ufo/waves/round-45/w1/R45W1PreflightDirtyReplay.md`
(same content, written because the assignment names both paths).

## Bottom line

The dirty arm is **load-bearing and correct on the M44-2 shape**: eight modified frozen fixtures
uncommitted → exit 1 with exactly the eight `git status --porcelain -z` entries; the same tree
without `--check-dirty` → exit 0. A nine-path sweep commit → exit 1 with **9 `touched` when the
log scope reaches the outside path** (`--pathspec .` or no pathspec), and 8 `touched` under the
assigned `--pathspec frozen/`, which is correct pathspec scoping rather than a miss.

Three classes of **false green** exist in the frozen instrument and were reproduced
(`F-5`, `F-6`, `F-7`; F-5 needs both the pathspec and the freeze-path to miss). None changes a
current R45 verdict — the live lane is clean and the frozen
names are plain ASCII — but two of them let a *correctly spelled* invocation return `clean`
without examining a frozen path: a frozen **file** named only by `--freeze-path` is invisible to
the dirty arm, and `--require-pathspec` is satisfied by a pathspec **narrower** than the frozen
dir. §7 gives the invocation that closes both, with a clean receipt on the live lane.

## 1. Instrument under test

Executed bytes = the freeze blob, copied out of the lane repo with `git show`:

```
git -C <lane> show f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/frozen-path-preflight.py
```

| property | value |
|---|---|
| sha256 | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` |
| bytes | 11987 |
| executed from | `/fast/scratch/hyaku/kaidoku-r45/R45W1PreflightDirtyReplay/frozen-path-preflight.py` (scratch copy) |
| `--selftest` | exit 0, `PREFLIGHT_SELFTEST: cases=11 failures=0` |
| selftest stdout sha256 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` |

That sha256 **equals** the sha256 of the committed receipt
`.ufo/waves/round-45/controls/preflight-selftest.txt` at the freeze (791 bytes by
`git cat-file -s`; sha256 by `git show … | sha256sum`), i.e. the frozen instrument reproduces its
committed selftest receipt byte for byte. Peer `R45W1PreflightReplay` re-measured the same 791 B and
`9f03df65…` independently (their `probe-p23`).

Freeze identity of the graded paths (worktree bytes vs `git show <freeze>:<path>`), all identical:

| path | sha256 | bytes |
|---|---|---|
| `plans/round-45-claims.md` | `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e` | 9461 |
| `tools/round-45/frozen-path-preflight.py` | `633ebc05…523b` | 11987 |
| `tools/round-45/c1-counter.py` | `2cfc5a48…a509` | 14319 |
| `tools/round-45/c2-counter.py` | `50212d0f…b025` | 9560 |
| `tools/round-45/registry-scope.json` | `6e2dda71…dff9` | 750 |

Machine-readable: `provenance.json`.

## 2. Fixtures

**(a) assigned shape** — `/fast/scratch/…/fixture-m44-2`, `git init` + local identity, toplevel
asserted equal to the fixture root before the first commit:
`frozen/control-fixtures/c0.json … c7.json` plus `outside.txt` committed as
`11bd14ef9075c7a8baa31cbcd6626209b3ab63e3`; the sweep commit is
`7b227d0f0d17fc132614726713ba2f3970520d5f`.

**(b) exact M44-2 shape** — `/fast/scratch/…/fixture-real-m44-2`, the **eight real paths** taken
from `git diff-tree -r --name-only c86ea508^ c86ea508 -- tools/round-44/control-fixtures/`, mirrored
under `frozen/` with the **real pre-sweep bytes** (`c86ea508^`) at the freeze and the **real
c86ea508 bytes** as the uncommitted tamper:

```
frozen/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json
frozen/control-fixtures/c3/manifest.json
frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v1be/after.json
frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json
frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v2be/after.json
frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v2le/after.json
frozen/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md
frozen/control-fixtures/pos/manifest.json
```

freeze `3fa2894d06b350d3ae3bffb6ceaed7a92c4658e4`, sweep `8eeecad53019a703d56c5c712eeb4d93f03fa26a`.

## 3. Assigned arms — exact commands, exits, receipts

Base argv for every arm: `python3 -I -B <scratch>/frozen-path-preflight.py --root $D --freeze $F --rev $R`
plus the delta shown. Receipts are the tool's own `--json-out` files, listed by filename in this
directory; `receipts.json` carries every step with argv, exit, UTC and stdout sha256.

| arm | delta | expected | got | stdout sha256 | receipt |
|---|---|---|---|---|---|
| (a) | `--check-dirty --pathspec frozen/` | 1, 8 `dirty` | **1, 8** | `2f21a2d54dd72563edb1813f442d039b19fe61fd042e0ce386ae71694c3207c5` | `a-check-dirty-pathspec-frozen.json` |
| (a0) negative pre-run | *(no flags)* | — | 0 | — | in `receipts.json` (`probe-no-flags-invocation`) |
| (b) | `--pathspec frozen/` | 0 | **0** | `fa5b558de3b91407bff5669bd799e0b77bc40e2fa4cf4a7f646486e7204f5118` | `b-no-check-dirty-pathspec-frozen.json` |
| (c) frozen scope | `--pathspec frozen/` | 1 | **1, 8 `touched`** | `91281f9abe840aa31914f83de15479f94a930b7636b1d475160d5faaee1075b0` | `c1-sweep-pathspec-frozen.json` |
| (c) whole tree | `--pathspec .` | 1, 9 | **1, 9** | `e2c8b4a774a784adfb99c9e576cdf91b879052476172e4d06700e4c5f2bda702` | `c2-sweep-pathspec-dot.json` |
| (c) default scope | *(no `--pathspec`)* | 1, 9 | **1, 9** | `925bde97ff41c9d530aa6d911fae91cab061a655e6e26f4faf4cedce489ad02b` | `c3-sweep-no-pathspec.json` |
| (c) require, uncovered | `--freeze-path frozen --require-pathspec` | 2 | **2** `pathspec_required` | `0493c9104be340cf880ec4f9f45b5dc0b04e3aee80cae22eba2012808637307b` | `c4-sweep-require-pathspec.json` |
| (c) require, covered | `+ --pathspec frozen/` | 1, 8 | **1, 8** | `af165b3ccb4d…` | `c5-sweep-require-pathspec-covered.json` |
| (c) dot + require | `--pathspec . --freeze-path frozen --require-pathspec` | 2 (lexical) | **2** (same bytes as c4) | `0493c910…` | `c6-sweep-dot-require-pathspec.json` |
| (c) dot+frozen + require | `--pathspec . --pathspec frozen/ …` | 1, 9 | **1, 9** | `10701820b2fa037786966e538dbd862cf023a6478b9b27b1be2b08206ddae919` | `c7-sweep-dot-plus-frozen-require.json` |

### (a) eight modified fixtures, uncommitted — exit 1, 8 dirty

`probe-no-flags-invocation` is the honest negative: the **same dirty tree**, called with neither
`--check-dirty` nor `--pathspec`, returns exit 0. Both flags are load-bearing.

`git -C $D status --porcelain -z -- frozen/` bytes (280, sha256 `3881bf3dd0137b07…`, file
`status-dirty-frozen.porcelain.z`), entries separated by NUL:

```
 M frozen/control-fixtures/c0.json
 M frozen/control-fixtures/c1.json
 M frozen/control-fixtures/c2.json
 M frozen/control-fixtures/c3.json
 M frozen/control-fixtures/c4.json
 M frozen/control-fixtures/c5.json
 M frozen/control-fixtures/c6.json
 M frozen/control-fixtures/c7.json
```

raw repr: `b' M frozen/control-fixtures/c0.json\x00 … \x00 M frozen/control-fixtures/c7.json\x00'`

The arm saw exactly those eight entries; its receipt is `dirty` = the same eight strings, with
`touched: []`, `blob_changed: []`, `restored: []`, `verdict: "frozen_path_changed"`, and
`freeze == rev == 11bd14ef…`. Nothing else was inspected — the whole verdict rides on the dirty arm.

### (b) same tree, no `--check-dirty` — exit 0

`{"blob_changed": [], "dirty": [], …, "verdict": "clean"}`. This is the M44-2 failure mode reduced
to one flag: the commit-only gate is blind to the worktree.

### (c) nine-path sweep commit — exit 1

`git log --name-status --format=%x00%H 11bd14ef..7b227d0f` (`sweep-log-name-status.txt`) lists
nine `M` entries: the eight fixtures plus `outside.txt`.

- `--pathspec frozen/` → 1, **8** touched: the outside path is outside the log scope. Correct, and
  it is why the "9" in the assignment needs the next two rows to be true.
- `--pathspec .` → 1, **9** touched, `outside.txt` included (`c2-…json`).
- no `--pathspec` → 1, **9** touched (`c3-…json`).
- `--freeze-path frozen --require-pathspec` with no pathspec → **2** `pathspec_required`
  (`uncovered_frozen_dirs: ["frozen"]`) — a 2, never counted as a pass.
- `--pathspec .` **plus** `--require-pathspec` → still **2**, because `covers()` is lexical and `.`
  does not cover the name `frozen`. Full-sweep + coverage needs **both** specs: row (c7) → 1, 9.

## 4. Exact M44-2 replay (real paths, real diffs)

| arm | result | receipt |
|---|---|---|
| `status --porcelain -z -- frozen/` | 8 entries, one per real fixture (548 bytes, sha256 `88113dfe…`) | `real-shape-status-dirty.porcelain.z` |
| (a) `--check-dirty --pathspec frozen/` | **1**, 8 `dirty` (stdout sha256 `d1616374ee32b159c365bc6c7cbb4ac8cb4f7a30b18a1f82dc07e7738e564b9d`) | `real-a-check-dirty.json` |
| (b) `--pathspec frozen/` | **0** (`ebd00b2055a275ef…`) | `real-b-no-dirty-arm.json` |
| (c) `--pathspec frozen/` | **1**, 8 touched | `real-c1-sweep-pathspec-frozen.json` |
| (c) `--pathspec .` | **1**, 9 touched | `real-c2-sweep-pathspec-dot.json` |
| (c) no pathspec | **1**, 9 touched | `real-c3-sweep-no-pathspec.json` |

The eight dirty entries are the eight real fixture paths, verbatim:

```
 M frozen/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json
 M frozen/control-fixtures/c3/manifest.json
 M frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v1be/after.json
 M frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json
 M frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v2be/after.json
 M frozen/control-fixtures/pos/corpus/evidence/round-44/c1/v2le/after.json
 M frozen/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md
 M frozen/control-fixtures/pos/manifest.json
```

## 5. Probes (beyond the assigned arms)

| probe | setting | result | receipt |
|---|---|---|---|
| dirty scope = whole tree | `--check-dirty` (no pathspec) | 1, 8 dirty | `probe-check-dirty-whole-tree.json` |
| outside dirt invisible | frozen 8 dirty + `outside.txt` dirty, `--pathspec frozen/` | 1, 8 (outside absent) | `probe-frozen-dirty-plus-outside.json` |
| `--dirty-pathspec` override | `--dirty-pathspec outside.txt` | 1, `[' M outside.txt']` | `probe-dirty-pathspec-outside.json` |
| granular specs | `--pathspec frozen/weird/with space.json` / `frozen` / `frozen/weird/` | 1, 1 dirty each | `probe-granular-g{1,2,3}.json` |
| staged dirt | `M  frozen/…` in index | 1, 1 dirty | `probe-staged-dirty.json` |
| untracked under frozen | `?? frozen/…/new-untracked.json` | 1, 1 dirty | `probe-untracked-dirty.json` |
| deleted under frozen | ` D frozen/…/c7.json` | 1, 1 dirty | `probe-deleted-dirty.json` |
| rename under frozen | `R  c0-renamed.json\0c0.json\0` | 1, **2** dirty entries for **one** rename | `probe-rename-dirty.json`, `probe-rename-status.porcelain.z` |
| tab in a frozen path, tamper+restore | commit tamper, commit restore | 1, `touched` carries `"frozen/weird/a\\tb.json"` (quoted), `restored: []` | `probe-tab-restored.json`, `oddpaths-log-name-status.bin` |
| **pathspec matches nothing** | 8 fixtures committed at `control-fixtures/`, gate scoped `frozen/` | **0, clean, 0 touched** | `probe-nonmatching-pathspec-*.{json,porcelain.z}` |
| boundary: real freeze tree, bad pathspec | `--pathspec nosuch/ --freeze-path frozen --require-pathspec` | **2** `pathspec_required` (fails closed) | `probe-f5b-pathspec-nosuch-real-freeze-tree.json` |
| boundary: **both** arguments miss | `--pathspec nosuch/ --freeze-path nosuch --require-pathspec` | **0, clean**, 8 commits in the frozen dir invisible | `probe-f5b-both-arguments-miss.json` (and `…-norequire.json`) |
| boundary control | `--pathspec frozen/ --freeze-path frozen --require-pathspec` | 1, 8 touched | `probe-f5b-control-correct-pathspec.json` |
| **frozen file outside pathspec, dirty** | `--pathspec frozen/ --freeze-path plans/claims.md --check-dirty` | **0, dirty []** | `probe-p1-dirty-frozen-file-out-of-scope.json` |
| control (same file inside pathspec) | `--pathspec plans/claims.md` | 1, `[' M plans/claims.md']` | `probe-p1c-control-file-in-scope.json` |
| remediation | `+ --dirty-pathspec plans/claims.md` | 1, 1 dirty | `probe-p1d-dirty-pathspec-remediation.json` |
| **narrow pathspec satisfies require** | `--pathspec frozen/control-fixtures/c0.json --freeze-path frozen --require-pathspec --check-dirty`, c1 dirty | **0, dirty []** (requirement "covered") | `probe-p2-narrow-pathspec-dirty.json` |
| control (dir pathspec) | `--pathspec frozen/` | 1, c1 dirty | `probe-p2c-control-dir-pathspec.json` |
| **narrow pathspec hides a restore** | same narrow spec, c1 touched-then-restored | **0, touched [], restored []** | `probe-p3-narrow-pathspec-restored.json` |
| control (dir pathspec) | `--pathspec frozen/` | 1, touched 2, `restored ['…c1.json']` | `probe-p3c-control-dir-restored.json` |

R45-shaped scope matrix (fixture = one frozen dir + one frozen file, `probe-scope-v*.json`):

| variant | dirty `plans/claims.md` | committed change to `plans/claims.md` |
|---|---|---|
| `--pathspec frozen/` only | **0 clean** (file invisible) | **0 clean** (v4: file never enumerated) |
| `+ --freeze-path plans/claims.md` | **0 clean** (v2: dirty scope is the pathspec) | **1**, `blob_changed ['plans/claims.md']` (v5) |
| `+ --dirty-pathspec plans/claims.md` | **1**, 1 dirty (v3) | — |

## 6. Findings

**F-1 (confirmed, no defect).** On both shapes the assigned arms behave exactly as claimed: dirty
arm 1/8 with the exact porcelain entries, arm absent 0, sweep 1 with 9 `touched` under a whole-tree
scope. Exit codes stay in `{0,1,2}`; the two `2` receipts (`c4`, `c6`) print no `met_target` and
were not counted as passes.

**F-2 (claims wording, low).** "A sweep commit … 9 `touched`" is only true when the *log* scope
contains the outside path. Under the claim's own `--pathspec tools/round-45/` the same commit gives
8 touched — that is scoping, not a miss, but the report row should name the scope, and note that
`--pathspec .` cannot satisfy `--require-pathspec` (lexical `covers()`), so full-sweep + coverage
needs `--pathspec . --pathspec tools/round-45/`.

**F-3 (receipt fidelity, low for R45).** The dirty arm splits `porcelain -z` on NUL without
consuming the paired source path of a rename: a **single** rename yields **two** `dirty` entries,
the second a bare path with no status (`probe-rename-dirty.json`:
`['R  frozen/control-fixtures/c0-renamed.json', 'frozen/control-fixtures/c0.json']`). The verdict
is right (1); any evidence that counts or classifies `dirty` entries is not.

**F-4 (citation vs code, medium for C1's depth claim).** The docstring cites S141 for `-z` field
termination, but the commit arm does **not** pass `-z`
(`tools/round-45/frozen-path-preflight.py:93-94`) and parses `splitlines()` + `split("\t")`
(`:99`, `:103`). Git therefore C-quotes unusual names: a tamper-then-restore of a tab-named frozen
file records `touched[].path == "\"frozen/weird/a\\tb.json\""` and leaves `restored: []`
(exit 1 via `touched`); `ls-tree --name-only` (`:116-119`) quotes the same way, so such a path is
skipped by the blob arm (`rev-parse` fails on both sides, `:126`). R45's frozen names are plain
ASCII, so no R45 verdict is affected — but the claim's "the commit arm parses that" is not what the
code does.

A related receipt note: a directory passed as `--freeze-path` is itself inserted into the frozen set
(`:114-115`), so when any child changes the blob arm also reports the **directory path**, comparing
tree hashes (`probe-f5b-control-correct-pathspec`: `blob_changed` = `["frozen", "frozen/c0.json" …]`).
The verdict is unaffected; the array mixes trees and blobs.

**F-5 (false green, high for any gate use; boundary pinned).** A pathspec that matches nothing can
return **exit 0 clean**: nothing validates that a pathspec matched ≥1 path. My own first replay hit
it (fixtures mirrored at `control-fixtures/`, gate scoped `frozen/`, eight changed files committed
→ `verdict: "clean"`, `touched: []`, `probe-nonmatching-pathspec-*`). The boundary matters:
`--require-pathspec` fails **closed** when a real tree is named by `--freeze-path` —
`--pathspec nosuch/ --freeze-path frozen --require-pathspec` → **2** `pathspec_required`
(`probe-f5b-pathspec-nosuch-real-freeze-tree`). The silent clean needs **both** arguments to miss,
because `tree_at()` is false for a freeze-path absent at FREEZE, so no coverage is demanded and
`git log -- nosuch/` scopes to nothing: `--pathspec nosuch/ --freeze-path nosuch`
→ **0 clean, touched 0, blob_changed []** with eight commits into `frozen/`
(`probe-f5b-both-arguments-miss`, and the `--require-pathspec`-less variant
`…-norequire`); the correct-pathspec control is 1 with 8 touched
(`probe-f5b-control-correct-pathspec`). So a typo'd pathspec alone is caught by
`--require-pathspec` **only if** `--freeze-path` still names the real frozen tree — which is exactly
the invocation the R45 claims describe, and why F-6/F-7 (real names, wrong coverage) are the
reachable ones. Peer `R45W1PreflightReplay` pinned the same boundary independently
(`probe-p19..p22`); cross-seat agreement.

**F-6 (false green, high; peer-corroborated).** A frozen **file** named only by `--freeze-path` is
invisible to the dirty arm, whose scope is `dirty_pathspecs or pathspecs` (`:135-137`). With the
claim-shaped invocation (`--pathspec frozen/ --freeze-path plans/claims.md --check-dirty`) a dirty
`plans/claims.md` gives **exit 0, dirty []**; with no `--freeze-path` a **committed** change gives 0
as well (`probe-scope-v1/v2/v4`). This maps directly onto R45: `plans/round-45-claims.md` is frozen
but is not under `tools/round-45/`. Fix on the invocation side: pass the file as both
`--freeze-path` and `--dirty-pathspec` (`probe-scope-v3`, `probe-p1d`: exit 1).

**F-7 (false green, high; peer-corroborated).** `--require-pathspec` is satisfied by a pathspec
**narrower** than the frozen dir, because `covers()` is a string-prefix test (`:60-64`): with
`--pathspec frozen/control-fixtures/c0.json --freeze-path frozen`, a dirty c1 gives **exit 0 clean**
(`probe-p2`), and a c1 tamper-then-restore gives **exit 0 clean** (`probe-p3`); the controls with
`--pathspec frozen/` return 1 with the expected `dirty`/`restored` (`probe-p2c`, `probe-p3c`). The
narrow spec also shrinks the blob arm's frozen set (`:115-119` enumerates from the pathspecs).

**F-8 (positive).** Dirty detection is not worktree-only: index dirt (`M `), untracked (`??`) and
deletion (` D`) all trip the arm; the pathspec scopes it correctly (outside dirt invisible);
`--dirty-pathspec` overrides; subdirectory and single-file pathspecs behave as expected.

**F-9 (positive, live).** At HEAD `faa875bc` the lane is clean for the frozen set: preflight exit 0
with the claim's scope (`live-lane-preflight-head.json`), exit 0 with `--check-dirty`
(`live-lane-preflight-head-dirty.json`), `git status --porcelain -z -- tools/round-45/ plans/round-45-claims.md`
empty, and `git log --name-only <freeze>..HEAD -- <frozen paths>` empty. Worktree bytes of all five
frozen files equal the freeze blobs (§1).

**F-10 (grounding).** The real M44-2 numbers hold: `c86ea508` carries **432** paths, **8** of them
under `tools/round-44/control-fixtures/`, and exactly **one** commit in `c48f8a4b..c86ea508` touches
that directory — `git diff-tree -r --name-only --no-commit-id c86ea508 | wc -l`,
`… -- tools/round-44/control-fixtures/ | wc -l`, `git log --oneline c48f8a4b..c86ea508 -- … | wc -l`.

## 7. Recommended invocation for the landing (and wave 2)

The claims' prose names `--pathspec tools/round-45/` and `--freeze-path tools/round-45`; that leaves
`plans/round-45-claims.md` unexamined (F-6) and is satisfied by any narrow spec (F-7). The
invocation that checks the whole frozen set, verified clean on the live lane
(`live-recommended-invocation.json`, exit 0):

```sh
python3 -I -B tools/round-45/frozen-path-preflight.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev <REV> \
  --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
  --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md \
  --require-pathspec --check-dirty \
  --dirty-pathspec tools/round-45/ --dirty-pathspec plans/round-45-claims.md
```

If the L1 wants the 9-path sweep receipt, add `--pathspec .`.

## 8. What was not run / limits

- The two counters (`c1-counter.py`, `c2-counter.py`) were not executed; out of this seat's scope.
- Did not exercise merge commits beyond the `--diff-merges=first-parent`/`-m` path the arm already
  uses, nor submodule/gitlink entries, nor non-ASCII (UTF-8) quoted names beyond the tab/newline probe.
- No lane mutation, no `git` write anywhere outside the private fixtures; no install.
- The peer `R45W1PreflightReplay` found the same two false-green classes (F-6, F-7) independently
  (their `probe-p13/p17/p18*`) and pinned F-5's boundary with the same result (their
  `probe-p19..p22`: real freeze tree + bad pathspec → 2; both arguments missing → 0 clean; control
  1/8), matching my `probe-f5b-*`. Their live-lane receipt (`receipt-d`: HEAD `faa875bc`, exit 0,
  `dirty []`) matches mine, so the landing verdict on the frozen set is two-seat.
- Verification of the R45 predicates themselves is the main agent's step; this report supplies
  instrument evidence only.

## 9. Artifacts

- `receipts.json` — every step: argv, exit, UTC, stdout sha256, stdout, stderr (64 steps).
- `provenance.json` — freeze, instrument sha256, frozen-file sha256s, fixture commit ids.
- `receipt-manifest.json` — sha256 + size of every file in this directory.
- `*.json` — the instrument's own `--json-out` receipts, named per arm/probe.
- `*.porcelain.z` — raw `git status --porcelain -z` bytes the arm consumed.
- `sweep-log-name-status.txt`, `oddpaths-log-name-status.bin` — raw commit-arm input.

Scratch was removed after these receipts were copied; nothing citable lived under `/tmp`.
Installs: none.
