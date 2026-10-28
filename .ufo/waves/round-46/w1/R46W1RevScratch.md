# R46W1RevScratch — attack on the R45-CL20 scratch policy (`gate.scratch`)

Seat: `R46W1RevScratch` (wave 1, round 46). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane: no lane byte was
written, no git/jj mutation ran (fixture repos under `$S` only), no package was installed.
Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RevScratch` was removed after its receipts
were copied here.

Instrument measured (bytes, not names):

| file | sha256 | note |
|---|---|---|
| `tools/round-46/gate.py` | `847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223` | HEAD during all runs; copy at `gate.py.measured` |
| `tools/round-46/attest.py` | `e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346` | `attest.py.measured` |
| `tools/round-46/registry.py` | `5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73` | `registry.py.measured` |

`gate.scratch()` is **byte-identical** at the assignment freeze `31820472784284727546808acc31b3ea1e73919b`
and at HEAD: `git diff 3182047..HEAD -- tools/round-46/gate.py` shows one hunk, in
`main_guard` (gate.py:217-220) only. So every result below applies to the frozen bytes and to
the working tree equally.

The lane was live while I measured: HEAD moved `781e19ae…` → `1e32827b…` → `deee6595…` →
`47b5e265…`, and another seat left an uncommitted `gate.py` edit in the worktree at
14:09Z (sha `c3ba6b93…`). Every receipt below pins its own revisions; §7 treats the pending
edit separately and does not judge it as landed.

---

## 1. Verdict

1. **The policy holds on every case this seat named** — 19 of 21 env cases match the frozen
   row exactly (`SKILL.md` block 23, R45-CL20: *"output: `scratch()` refuses a temporary
   partition and returns could-not-evaluate instead of degrading"*, exit `2`).
2. **Two counter-examples, one defect class**: tmpfs scratch roots outside the two hard-coded
   names (`/dev/shm`, `/run/user/1000`) are **accepted** and written to. Exit 0 for both
   counters; the base directory is created on the ramdisk and survives the run. The row's own
   wording ("refuses a temporary partition") is false for a class of temporary partitions,
   and the failure mode is the one R45-CL20 exists to prevent: evidence that is not citable.
   No verdict changes: the battery passes identically on a ramdisk (same receipt sha as on
   `/fast`), so this is an evidence-durability defect, not a false green.
3. **Both counters still reach 1 and 0 (never 2) with a normal scratch root** — see §5. Exit 2
   arises only from a refused root or from `frozen_path_changed`, never from a usable root.
4. **Nothing attributable to either driver was created under `/tmp`** (or `/var/tmp`) in any
   of the 21 cases: host `find -newermt` sweep plus a pristine-tmpfs mount-namespace arm;
   `/dev/shm` is the exception, from the two accepted-ramdisk cases (§2, §4).
5. Three defects sit outside the scratch axis but inside this seat's frame, each with a
   fixture receipt: the claimed **dirty scope has no caller** in the frozen bytes (F4); **no
   red case exercises `gate.scratch`** (F5); and the interpreter **pin does not bind the
   executing file** (F8). Two calibration numbers in the frozen claims do not reproduce
   (F6/F7).

Severity is my calibration, not the round's: F4 high (claim vs code), F1/F5/F8 medium,
F2/F6/F7 low-medium, F3 low.

---

## 2. Method

A refused scratch root is only reached **after** the structural clauses pass
(`evaluate()`: `if with_battery and structural == 0` — attest.py:451, registry.py:399). A run
at the do-nothing freeze therefore never consults `gate.scratch` at all. I measured each env
case at **pairs where the artefact is structurally green**, so the scratch call is on the
executed path:

- C1 pair `freeze = rev = 6e018068aaf9beb3c66ed270aeee08b300531976` (battery: 9 forgeries).
- C2 pair `freeze = rev = 781e19ae674225b6be0b5de56ee8574679bac0b6` (battery: 7 forgeries).

Both pairs are self-pinned (`freeze == rev`), so `frozen_path_changed == []` and the scratch
semantics are isolated from the freeze defect in §6. 21 env cases × 2 counters = 42 runs, plus
unit-level probes, the do-nothing controls, the L1 landing pair, selftests, and five fixture
experiments.

`/tmp` observation, per case: `find <root> -xdev -mindepth 1 -maxdepth 3 -newermt @<start>
-printf '%p\t%T@\n'` over `/tmp`, `/var/tmp`, `/dev/shm`, with base-directory and
`git status` snapshots. Host `/tmp` is shared with ~100 sibling seats, so I attribute only by
strict name prefix (`kaidoku-`, `fx-`, `self-`, `regsrc`) and cross-check with a **pristine
mount namespace** (`unshare -rm --propagation private`, `tmpfs` over `/tmp`, `/var/tmp`,
`/dev/shm`, all three empty at start: `tmp=0 vartmp=0 shm=0`), where any new entry is
attributable to the run. The host sweep was demonstrably live: 1 423 new entries appeared
under `/tmp` across the 21 windows (909 distinct paths, all sibling lanes: `tameshi-*`,
`ecc-*`, `census-*`, `claude-*`), 21/21 windows non-empty — so "zero ours" is a real reading,
not an empty window.

Harnesses are archived beside this report (`matrix.py`, `receipts.py`) so every number is
reproducible.

---

## 3. Case table (21 cases, both counters at the green pairs)

Expected column = the frozen text (R45-CL20 row and `gate.py` docstring); for `/dev/shm` and
`/run/user/1000` the expectation follows the row's own wording ("a temporary partition") and
the code comment at gate.py:33-35 ("anything here is reaped … nothing there is citable").

| case | HYAKU_SCRATCH | TMPDIR | expected | observed C1/C2 | match | driver-created under a temp root | base after |
|---|---|---|---|---|---|---|---|
| `unset_both` | unset | unset | 2 | 2 / 2 | yes | none (`/tmp/r46relcwd` is my harness fixture) | empty |
| `hk_tmp` | `/tmp` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_tmp_trailing` | `/tmp/` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_double_slash` | `//tmp` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_dotdot` | `/fast/scratch/../../tmp` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_symlink_tmp` | `S/linktmp` → `/tmp/…` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_empty` | `""` | unset | 2 | 2 / 2 | yes | none | empty |
| `tmpdir_tmp` | unset | `/tmp/r46revtmp` | 2 | 2 / 2 | yes | none | empty |
| `hk_vartmp` | `/var/tmp` | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_tmp_fast_tmpdir` | `/tmp` | `S/tmproot` | 2 | 2 / 2 | yes | none | empty |
| `tmpdir_fast` | unset | `S/tmproot2` | 0 | 0 / 0 | yes | none | empty |
| `hk_fast` | `S/root` | unset | 0 | 0 / 0 | yes | none | empty |
| `hk_deep_new` | `S/a/b/c` | unset | 0 | 0 / 0 | yes | none | `S/a/b/c` persists (F3) |
| `hk_relative_fastcwd` | `relroot` | unset | 0 | 0 / 0 | yes | none | `S/relcwd/relroot` persists (F2) |
| `hk_relative_repo` | `relroot` | unset | 0 | 0 / 0 | yes | none | `fixture-repo/relroot` created (F2) |
| `hk_shm` | `/dev/shm/r46scratch` | unset | **2** | **0 / 0** | **NO** | `/dev/shm/r46scratch` | ramdisk base persists (F1) |
| `hk_runtime` | `/run/user/1000/r46scratch` | unset | **2** | **0 / 0** | **NO** | `/run/user/1000/r46scratch` | runtime base persists (F1) |
| `hk_readonly` | `S/ro` (mode 0555) | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_unreadable` | `S/noread` (mode 0000) | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_file` | `S/afile` (regular file) | unset | 2 | 2 / 2 | yes | none | empty |
| `hk_file_nested` | `S/afile/sub` | unset | 2 | 2 / 2 | yes | none | empty |

Reason strings observed (identical for both counters, from the receipts):

```
no HYAKU_SCRATCH/TMPDIR root set
scratch root is a temporary partition: /tmp
scratch root is a temporary partition: /var/tmp
scratch root is a temporary partition: /tmp/r46revtmp
scratch root is a temporary partition: /tmp/r46-symlink-target
scratch root unusable: [Errno 13] Permission denied: '…/ro/kaidoku-r46-battery-…'
scratch root unusable: [Errno 13] Permission denied: '…/noread/kaidoku-r46-battery-…'
scratch root unusable: [Errno 17] File exists: '…/afile'
scratch root unusable: [Errno 20] Not a directory: '…/afile/sub'
```

Green-path receipts are deterministic: the eight accepted cases produced exactly **one**
stdout byte-string each — C1 `1809c018bce9831a…`, C2 `5ca8195dfb5d3b0f…` — through the
shared `/tmp` host under full sibling load. That is the "one canonical runtime" reading for
this axis: no reroute, no nondeterminism.

---

## 4. Findings

### F1 — MEDIUM — a tmpfs root outside the two hard-coded names is accepted (counter-example to the row)

`TEMP_PARTITIONS = ("/tmp", "/var/tmp")` (gate.py:29) is a two-element deny-list, not a
predicate over partitions. `/dev/shm` and `/run/user/<uid>` are tmpfs — wiped at reboot or
logout, exactly what the comment at gate.py:33-35 says must never hold evidence.

```
HYAKU_SCRATCH=/dev/shm/r46scratch python3 -I -B tools/round-46/attest.py \
  --root <lane> --freeze 6e018068 --rev 6e018068      → exit 0, met_target true
HYAKU_SCRATCH=/run/user/1000/r46scratch … registry.py --freeze 781e19ae --rev 781e19ae
                                                      → exit 0, met_target true
```

Observed on disk afterwards (still present at 14:04Z / 14:06Z UTC): `/dev/shm/r46scratch`,
`/run/user/1000/r46scratch`. The mkdtemp child is cleaned by the `finally`; the **base** is
created and left (F3). In the pristine namespace arm (`/dev/shm` empty at start) the same run
created `/dev/shm/r46scratch` again — attribution is direct, not inferred.

Calibration: **no verdict changes.** The battery receipt on `/dev/shm` is byte-identical to
the receipt on `/fast` (`1809c018…` / `5ca8195d…`), so this cannot make a forgery green. It is
the arm's *purpose* that fails: run on a ramdisk and the forgeries' receipts die with the
reboot.

Recommendation (for a v3, not an edit to the frozen bytes): classify by filesystem type
(`statvfs`/`/proc/self/mountinfo` → refuse `tmpfs`) or add `/dev/shm`, `/run/**`,
`$XDG_RUNTIME_DIR` to the deny set. One conditional; no clause change.

### F2 — LOW/MEDIUM — a relative root is accepted and resolved against the CWD; it can write inside the measured repo

`os.path.realpath(base)` resolves a relative `HYAKU_SCRATCH` against the process CWD
(gate.py:195). Nothing requires an absolute path, and `scratch()` never sees `root`, so it
cannot refuse a base inside the repository being measured — contradicting gate.py's own
docstring ("Reads Git objects only; **never writes inside the repo it measures**").

- `HYAKU_SCRATCH=relroot`, `cwd=S/relcwd` → exit 0, `S/relcwd/relroot/` created.
- `HYAKU_SCRATCH=relroot`, `cwd=fixture-repo` (a real one-commit git repo, toplevel asserted
  `= $S/fixture-repo`) → exit 0, `fixture-repo/relroot/` created.
- Killed run (`timeout -s KILL 0.8`), base at the fixture repo root:
  `scratch/kaidoku-r46-battery-8mxave81/fx-dn6r7nsq/` survived and
  `git -C fixture-repo status --porcelain` printed `?? scratch/` — an interrupted run leaves
  fixture git repos inside the measured tree.

Consequence today is bounded only because **no arm reads the working tree** (F4). If the lane
is ever run with a relative root from the lane root, the write lands in the lane. Fix
candidates: require `os.path.isabs`, and reject a base under `root` (one `commonpath` test with
the same helper `out_path()` already uses).

### F3 — LOW — the base directory is created and never removed

`os.makedirs(base, exist_ok=True)` (gate.py:199) creates the whole chain; only the mkdtemp
child is `rmtree`d. Evidence: `S/a/b/c` still present after `hk_deep_new`; `S/relcwd/relroot`
after the relative case; `/dev/shm/r46scratch` after F1. A typo'd root leaves a tree behind.
Hygiene only; no verdict effect.

### F4 — HIGH (cross-cutting: claim vs code) — the "dirty scope" has no caller in the frozen bytes

`gate.frozen_set`/`blob_changed`/`history_touched` are wired into `freeze_state`, but
`gate.dirty()` (gate.py:132) is **never called** — `grep -n "dirty(" tools/round-46/*.py` returns
its definition only. Two frozen texts assert otherwise:

- `plans/round-46-claims.md` `## Frozen paths (exact)`: *"both counters derive this list from
  this section and use it for the history arm, the blob arm **and the dirty scope**"*.
- `SKILL.md` block 23, R45-CL15 row: *"dirty: the dirty scope is the union of the pathspecs,
  and each arm has a **red case that names it**"* — no such red case exists (§F5).

Fixture receipt (`fixture-dirty-frozen-path.json`): a measured root whose
`tools/round-46/attest.py` carries an **uncommitted** comment line —

```
git -C $S/fx-green status --porcelain     →  M tools/round-46/attest.py
python3 -I -B <lane>/tools/round-46/attest.py --root $S/fx-green \
  --freeze 7e4a968f… --rev 7e4a968f…      → exit 0, met_target true,
                                             frozen_path_changed [], touched 0
```

`met_target: true` with a modified frozen interpreter in the measured tree. The counters read
committed bytes only, so the frozen set's history arm and blob arm cannot see it. This is the
R45-CL24 class (the record drifted from the instrument), inside round 46's own freeze.

### F5 — MEDIUM — nothing in the instrument's own batteries exercises `gate.scratch`

Counts measured from the freeze's own bytes (`--root … --freeze … --rev … --selftest`):

- `attest.py --selftest`: **16** cases at the working tree, 15 at `3182047`/`50862e4a`; the
  two exit-2 cases are `red-malformed-heading-is-exit-2`, `red-frozen-touched-is-exit-2`.
- `registry.py --selftest`: **12** cases at every revision measured; **zero** exit-2 cases.
- forgery batteries: 9 (C1) + 7 (C2) classes; none is a scratch-root forgery.

So block 23's R45-CL20 row (`arm output`, `exit 2`) is *stated*, and the code path exists, but
no case in either instrument ever drives it red. A row whose arm no battery can falsify is the
exact shape round 46 exists to remove — for row 23 itself the claim says "each row is a defect
the round-45 closure routed", and this one row's defect is not covered by the round's own
battery. Proposal (v3, one case): in `selftest`, run `evaluate()` for a green fixture in a
subprocess with `HYAKU_SCRATCH=/tmp` and expect `2`; cheaper still, assert
`gate.scratch("x")` returns `(None, "…temporary partition…")` for `/tmp`, `/var/tmp` and
(once F1 is fixed) `/dev/shm`. No predicate change required.

### F6 — MEDIUM (calibration) — the frozen claims' selftest numbers do not reproduce

`plans/round-46-claims.md` `## Satisfiability preflight` says
"`attest.py --selftest` prints `cases=15 failures=0`" and "`registry.py --selftest` prints
`cases=11 failures=0`". Measured, each freeze scored by **its own bytes**:

| interpreter at | attest.py | registry.py |
|---|---|---|
| `31820472784284727546808acc31b3ea1e73919b` (assignment freeze) | cases=15 failures=0 | **cases=12** failures=0 |
| `50862e4a041499dd2ce0da68d10301b765bb9997` ("complete freeze") | cases=15 failures=0 | **cases=12** failures=0 |
| `65678df0f1666e83cdeea7233bfb31ffe73ec709` (freeze the L1 C2 receipt uses) | **cases=16** failures=0 | **cases=12** failures=0 |
| working tree (HEAD) | **cases=16** failures=0 | **cases=12** failures=0 |

`registry.py`'s frozen number (`11`) is wrong at **every** declared freeze, including the one
the round claims; `attest.py`'s `15` holds only for the first two. A preflight number that no
declared freeze reproduces is the record-drift defect the round is closing, one level up.

### F7 — LOW/MEDIUM (calibration) — the preflight command as written cannot run

`--root`, `--freeze` and `--rev` are `argparse`-required, so the literal commands in the
claims —

```
python3 -I -B tools/round-46/attest.py --selftest
```

— exit **2 with empty stdout** (`sha256 e3b0c442…`, the empty-string hash) and print usage on
stderr (`attest.py: error: the following arguments are required: --root, --freeze, --rev`).
A reader reproducing the preflight literally sees exit 2 and no reason: the
"exit 2, no output" shape R45-CL13(f) forbade for a malformed heading, reintroduced by the
CLI. Two cheap remedies for v3: make `--selftest` not require the other three (or require only
`--root`), and emit a JSON `{"reason": …}` on the usage path, since exit 2 otherwise means
"could-not-evaluate".

### F8 — MEDIUM (attribution limit, with a live instance) — the pin binds the cited interpreter, not the executing one

C1's clause 6 checks the `sha256:` in block 23 against `rev:tools/round-46/attest.py`. It does
not — and cannot — bind the file being executed, and the receipt records only the two values
it compared. Demonstration (`rogue-driver-receipt.json`): a copy of `attest.py` with one
appended comment (sha `a53fb830…`) run against the green fixture:

```
exit 0, met_target true, pin == pin_expected == e6c44d2d57dbbc65…25b8fe532346,
failing []
```

i.e. a green receipt naming the frozen interpreter while different bytes produced it. C2 has
no pin clause at all (only the table *column* "pinned-value path"), and neither receipt
carries the driver's own sha256. Live instance from this seat's own window: at 17:03Z HEAD was
`781e19ae` and `git status` showed `M tools/round-46/registry.py` (worktree `5e16e4af…`) while
`781e19ae:tools/round-46/registry.py` is `db5adc02…`; C2 scored **exit 0, met_target true** at
that rev. The same is true of the pending `gate.py` edit in §7 — the executed instrument is not
the judged one.

**One hash for three states.** Three runs that differ in exactly the ways that should matter —
(i) a measured root with an **uncommitted edit to a frozen tool** (§F4), (ii) an executing
interpreter with **different bytes**, (iii) the pending `gate.py` with the dirty arm wired and
a **repo-root scratch directory** present (§7) — emit **byte-identical** green receipts:
`sha256 cb473c4964df9d72…`, 27 keys, `pin == pin_expected == e6c44d2d…`, `failing []`
(`fixture-dirty-frozen-path.json`, `rogue-driver-receipt.json`,
`pending-green-receipt-rootscratch.json`). Only the failing path differs (13 keys, `reason:
frozen_worktree_dirty`). The green receipt is invariant under every state F4/F4b/F8 name, which
is why the recommendation below is about recording identity, not about another clause.

Recommendation (no clause change): add `"driver_sha256": sha256(open(__file__,"rb").read())`
to both receipts. One line; turns "a green receipt" into "a green receipt produced by these
bytes", and gives the F4 dirty arm something to compare against.

---

## 5. The seat's two direct questions

**(a) Each named env case — {env, expected, observed, anything created under /tmp}:**

| # | env | expected | observed (C1 / C2) | anything under `/tmp` |
|---|---|---|---|---|
| 1 | `HYAKU_SCRATCH` unset, `TMPDIR` unset | 2 `no HYAKU_SCRATCH/TMPDIR root set` | 2 / 2, same reason | no (strict-prefix 0; namespace arm: only my own cwd fixture `/tmp/r46relcwd`) |
| 2 | `HYAKU_SCRATCH=/tmp` | 2 `temporary partition` | 2 / 2 | no |
| 3 | `TMPDIR=/tmp/x` (HK unset) | 2 `temporary partition: /tmp/x` | 2 / 2 | no |
| 4 | `HYAKU_SCRATCH=/var/tmp` | 2 `temporary partition: /var/tmp` | 2 / 2 | no (and `/var/tmp` 0 entries in all 21 windows) |
| 5 | `HYAKU_SCRATCH=S/root` (real fast path) | 0 | 0 / 0, batteries 9 and 7 green | no |
| 6 | `HYAKU_SCRATCH=relroot` (relative) | unspecified by the row | **0 / 0** — resolved against CWD, dir created under CWD (F2) | no |
| 7 | read-only `HYAKU_SCRATCH` (`chmod 0555`) | 2 | 2 / 2 `scratch root unusable: [Errno 13]` | no |

Extra cases (2 more counter-examples, 12 more envelopes) are in §3–§4.

**(b) Do both counters still reach exit 1/0 (not 2) with a normal scratch root?** Yes.

| pair | C1 (`attest.py`) | C2 (`registry.py`) | stdout sha256 (first 16) |
|---|---|---|---|
| `freeze=rev=3182047` (do-nothing) | **1** | **1** | `dda3086b126619bb` / `8841358751b18788` |
| `freeze=rev=6e018068` (green, C1) | **0** | — | `1809c018bce9831a` |
| `freeze=rev=781e19ae` (green, C2) | — | **0** | `5ca8195dfb5d3b0f` |
| `freeze=04252247 rev=1e32827b` (L1 landing pair) | **0** | **0** | `9336deb37f5c1889` / `75946e3215e5b955` |
| `freeze=3182047 rev=1e32827b`, normal root | 2 `frozen_path_changed` | 2 `frozen_path_changed` | `4800c402fb3f3a64` / `66408e857fb1b5f5` |
| no root set (C1 at `6e018068`, C2 at `781e19ae`, both self-pinned) | 2 `no HYAKU_SCRATCH/TMPDIR root set` | 2, same reason | `ef924935c3857505` / `71b082e079d94143` |

The only exit 2 in the presence of a usable root is the freeze arm — never the scratch arm.
Note the last-but-one row: under **the freeze my brief names** (`3182047`), round 46's own
landing revision exits 2. With the L1's re-declared freeze (`04252247`) it exits 0. See §6.

---

## 6. Cross-cutting facts the L1 must reconcile (not this seat's finding to fix)

1. **Three freezes are in play.** `git log --format=%H -1 -- plans/round-46-claims.md` →
   `3182047…` (the freeze named in the assignment and the one the claims' own sentence
   "`git log …` re-derives it" yields). Commit `50862e4a…` says *"complete the freeze — …
   declared as the authoritative freeze because the first freeze commit did not carry the
   final bytes"*. The L1's own C2 receipt `l1/scores/c2-at-781e19ae.json` carries
   `"freeze": "65678df0f1666e83cdeea7233bfb31ffe73ec709"`. Measured consequence:
   `freeze=3182047, rev=1e32827b` → both counters exit 2 `frozen_path_changed`
   (`tools/round-46/{attest,gate,registry}.py` listed as `restored`), while
   `freeze=04252247, rev=1e32827b` → both exit 0. A round whose claim is "nothing in
   `tools/round-46/` changes after the freeze" has changed it three times, and its own
   `restored` arm is what flags the earlier declarations.
2. **`dirty()` is dead code in the frozen bytes** (F4) — the claimed dirty scope does not
   exist, and a working-tree modification of a frozen tool scores green.
3. **No red case for the scratch arm** (F5), and the preflight's case counts do not reproduce
   (F6), and the preflight command does not run as written (F7).
4. **The pin does not bind the executing interpreter** (F8); C2 has no pin.

---

## 7. Pending worktree edit observed at 14:09Z (uncommitted; not judged as landed)

While writing this report I read (never wrote) an uncommitted `tools/round-46/gate.py`
(`sha256 c3ba6b93…`, `git diff` hunk in `freeze_state`) that another seat is preparing. I
exercised it only to check whether my findings survive it:

- frozen-set derived at **both** ends and unioned → a rev that rewrites its own
  `## Frozen paths` cannot shrink the scope. Good.
- `dirty()` wired, `reason: frozen_worktree_dirty`, exit 2. Verified in the fixture:
  `M tools/round-46/attest.py` → **exit 2**, `dirty: ["tools/round-46/attest.py"]`,
  `frozen_from` equal at both ends. So F4 is closed **if this edit lands**.
- Two residual gaps in that edit, both cheap:
  1. **The green receipt drops `dirty`.** `evaluate()`'s `receipt.update({...})` copies
     `freeze`, `frozen_derived`, `frozen_path_changed`, `touched`, `restored` — not `dirty`
     (nor `frozen_from`). Observed: green receipt keys contain no `dirty`; only the failing
     path (which returns the `fs` dict whole) shows it. A reviewer of a green receipt still
     cannot see that the frozen tools were clean.
  2. **`dirty()` is pathspec-scoped**, so a scratch write at the repo root is invisible:
     with `?? scratch/` present at the measured root, the run still exits 0 and `dirty` is
     not reported (`pending-green-receipt-rootscratch.json`). F2's damage therefore survives
     the fix; only a write *under* `tools/round-46/` or `plans/round-46-claims.md` trips it.
     Conversely, a residue under a frozen path (a killed run whose `HYAKU_SCRATCH` was
     `tools/round-46/…`) permanently forces exit 2 — strict but worth stating.

---

## 8. Limits — what I did not run

- **Bind-mount / hardlink aliasing** of a temporary partition under a non-temporary path was
  not tested (needs host mount privileges; out of seat scope). F1 is measured for the two
  tmpfs instances on this host only; the class is larger than what I proved.
- **`strace`-level attribution** was not used; host-arm attribution is prefix-based, and the
  pristine-namespace arm (all three roots empty at start) carries the airtight claim.
- I did not re-run the counters under `--json-out` (that is R45-CL22's arm, not this seat's).
- The lane moved under me (`781e19ae` → `47b5e265`); every receipt names the exact revisions,
  and the instrument bytes I measured are archived here (`*.measured`).
- No package installed; nothing under `/tmp`, `/dev/shm`, `/run/user` or `$S` was left behind
  (removed after the receipts were copied).

---

## 9. Evidence in this directory

| file | what it is |
|---|---|
| `receipts.json` | the 10 headline runs + 8 selftest runs: command, exit, stdout sha256, UTC |
| `results-matrix-host.json` | 21 env cases × 2 counters, per-case `/tmp`,`/var/tmp`,`/dev/shm` sweeps, base before/after, fixture `git status` |
| `results-matrix-namespace.json` | the same cases under a pristine tmpfs mount namespace |
| `selftest-attest-at-6e018068.out`, `selftest-registry-at-6e018068.out` | full selftest output (16 / 12 cases) |
| `fixture-dirty-frozen-path.json` | F4 receipt: uncommitted frozen-path edit → exit 0, met true |
| `rogue-driver-receipt.json` | F8 receipt: non-pinned executing bytes → exit 0, pin matches |
| `pending-dirty-arm-scope.json`, `pending-green-receipt-rootscratch.json` | §7 observations of the pending edit |
| `matrix.py`, `receipts.py` | the harnesses, so every number is reproducible |
| `gate.py.measured`, `attest.py.measured`, `registry.py.measured` | the exact instrument bytes scored above |

Report: .ufo/waves/round-46/w1/R46W1RevScratch.md
