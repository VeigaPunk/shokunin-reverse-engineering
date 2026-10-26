# R38SentinelBounds — wave-1 seam integrity (bounds / VCS / secrets / scratch / misroot)

Seat: `R38SentinelBounds` (sentinel, leaf — no dispatch, no background jobs, no `agent://all`).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Advisory only: nothing below was repaired.
Observation window: 2026-10-26 03:20:30 → 03:26:00 -03. The wave was **live** throughout (30
artifact dirs, 25 reports, seats still writing); every number here is a timestamped snapshot, not a
final state.

My own writes: this file plus
`.ufo/waves/round-38/w1/artifacts/R38SentinelBounds/` (12 evidence files). Nothing else.

---

## 0. Headline

The seam is intact in two important ways and broken in three:

| # | surface | verdict |
|---|---|---|
| 1 | frozen `tools/round-38/c1-counter.py` | **BROKEN — mutated in the worktree, uncommitted, 7 post-freeze byte-states, none self-verifying** (CRITICAL; **see §11 — the L1 has since posted a freeze-v2 amendment, also uncommitted; the latest counter runs 18 cases but fails its own green case**) |
| 2 | C1 premise ("no external extractor dependency") | **contradicted by the wave's own probes; withdrawn by the L1's v2 note (§11a)** (HIGH) |
| 3 | lane root | **contaminated: untracked `unblob.log` written by a seat** (MEDIUM; removed by 03:26:53) |
| 4 | seat reports/artifacts containment | clean: no escapes, no symlinks, no corpus writes, no secrets |
| 5 | VCS | clean for leaves: every mutating `jj` op is the orchestrator (`plazir27`); `w1/` untracked at HEAD |
| 6 | freeze v2 (`plans/round-38-claims.md`) | **in flight, not landed**: no commit, no before receipts, v1 controls, counter unrunnable (§11b) |

---

## 1. CRITICAL — the frozen counter was rewritten in the worktree during the wave

`plans/round-38-claims.md:60-61` (frozen at `e059ca93`): "the counter, predicate, carriers and
oracle are **never changed after this commit**." `plans/round-38-claims.md:26-27` states the
predicate as "the committed REA extract-firmware after-receipt (run with stock unblob 26.6.4; **no
external extractor dependency**)".

### Evidence — five states, one of them frozen

```
$ git -C <lane> status --porcelain            # 03:20:30 … 03:25:40, every sample
 M tools/round-38/c1-counter.py
?? .ufo/waves/round-38/assimilation/
?? .ufo/waves/round-38/w1.ready[.dispatched]
?? .ufo/waves/round-38/w1/
?? unblob.log                                   # appeared 03:24:32, see §3
$ git -C <lane> rev-parse HEAD                       # cb4326b2aa4c2024af0651fe6115b82d0c4de3df
$ git -C <lane> rev-parse e059ca93:tools/round-38/c1-counter.py
8e33ac6843c07d60835118312cb844def4385935
$ git -C <lane> diff e059ca93 HEAD --stat -- tools/round-38/c1-counter.py
(empty — frozen bytes == HEAD bytes)
$ git show e059ca93:tools/round-38/c1-counter.py | sha256sum
a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8
```

| observed (mtime) | sha256 | state | my measurement |
|---|---|---|---|
| frozen / HEAD | `a7a62b09…` | frozen predicate, after-arm only | `--selftest` → `{"selftest":"c1-counter","cases":15,"green_ok":1,"red_ok":14,"failures":[]}`, **exit 0** |
| 03:22:17 | `f27f982b…` | docstring rewrites the frozen P38-C1 sentence; `measure()` gains a `before` leg; the old `try:` loses its `except` | **`SyntaxError: expected 'except' or 'finally' block` at line 173, exit 1**, no cases run |
| 03:23:27 | `12f09870…` | syntax repaired; per-carrier `ok` now also requires `before_present`, `before_subject_ok`, `before_operation_ok`, `before_missing_extractor_gap`, `before_oracle_hits == 0` | **`AttributeError: 'NoneType' object has no attribute 'get'`** (`:186` via `gaps()` `:135`), exit 1 |
| 03:24:19 | `21105978…` | fixture builder gains a `be_before` envelope | same **`AttributeError`**, exit 1 |
| 03:24:52 | `733be016…` | further fixture work | **`UnboundLocalError: cannot access local variable 'be_before'`**, exit 1 |

Reproduce (read-only, scratch only; snapshots preserved in
`artifacts/R38SentinelBounds/c1-counter.*`):

```
$ python3 -c "import ast;ast.parse(open('tools/round-38/c1-counter.py').read())"     # per snapshot
snapshot-0322  SYNTAX_ERROR 173 expected 'except' or 'finally' block
snapshot-0323  PARSE_OK 403 lines
snapshot-0324  PARSE_OK 413 lines
final-snapshot PARSE_OK 417 lines
$ TMPDIR=$S python3 -I -B tools/round-38/c1-counter.py --selftest \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
…line 173: SyntaxError: expected 'except' or 'finally' block          # exit 1   (03:22 state)
$ TMPDIR=$S python3 -I -B <copied frozen blob>/c1-counter.py --selftest --pkg65 <pkg65>
{"selftest": "c1-counter", "cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}   # exit 0
```

Control: the frozen blob was re-run from a scratch tree (`$S/tree/tools/round-38/` + `round-27/`,
fixture dir intact) — 15 cases, `failures: []`, exit 0. So the break is the worktree edit, not a
pre-existing defect.

### What the mutation does to the predicate (not cosmetic)

`git diff -- tools/round-38/c1-counter.py` (snapshot at 03:22, `artifacts/R38SentinelBounds/c1-counter.diff-vs-HEAD`):

* docstring: `(run with stock unblob 26.6.4; no external extractor dependency)` →
  `(run with sasquatch-v4be available, as unblob 26.6.4's SquashFSExtractor requires)`;
* **plus a whole new conjunct**: "the paired committed before-receipt (run with sasquatch-v4be
  unavailable) publishes none of them and names sasquatch-v4be as a missing extractor dependency";
* `measure()` now reads `c1/K{1..4}/before.json` **and** `after.json` and gates `matched` on both.

That is a post-freeze expansion of a scored predicate, uncommitted, in a file the freeze doc says is
never changed. No claim amendment exists: the claims doc still carries the old sentence at
`plans/round-38-claims.md:26-27`, and no `before.json` receipt exists anywhere in the lane
(`corpus/evidence/round-38/c1/` holds **no files** — `git ls-files corpus/evidence/round-38 | wc -l`
→ 0 — and no artifact dir holds a `before.json`). Under the mutant, all four carriers would be
`before_present: false` → `carriers_matched == 0`.

### Impact

* Any seat or integrator invoking the **worktree** counter in any post-freeze state gets a crash —
  no verdict at all (03:22 `SyntaxError`; 03:23-03:24 `AttributeError`; 03:24:52 `UnboundLocalError`).
* If the mutant is ever committed, the scored predicate for R38-C1 changes retroactively and the
  freeze id stops describing the instrument.
* Recomputation of the measured revision with the worktree instrument is impossible; only the frozen
  blob scores.

### Smallest remediation (L1)

1. Restore the frozen bytes: `git -C <lane> checkout e059ca93 -- tools/round-38/c1-counter.py`
   (target sha256 `a7a62b09…`); confirm `--selftest` → 15 cases, exit 0.
2. Do **not** delete the proposal: keep the `before`-arm diff as a next-round predicate draft (it is
   a correct reaction to §2, but a predicate change is a claim change, not an instrument change).
3. If the corrected premise is wanted **this** round, it needs an explicit re-freeze (new freeze id,
   amended `plans/round-38-claims.md`, controls re-scored) — never a silent worktree edit.
4. Add a pre-integration gate: `git status --porcelain tools/` must be empty at the measured revision.

Peer corroboration (independent, same object): `R38ExecAfterK1.md:219-224` (D5) and
`artifacts/R38ExecSelftests/lane-drift-observation.json`.

---

## 2. HIGH — the frozen C1 premise is false by the wave's own evidence

`plans/round-38-claims.md:61-64` (frozen): "**Not claimed**: … or that sasquatch-v4be is required
(stock unblob handles standard BE v4; measured probes at the base show the `squashfs_v4_be` handler
publishing all oracle files without any external extractor — the round-37
"missing-extractor-dependency" before-arm does not reproduce on these carriers …)".

The wave measured the opposite (`artifacts/R38ExecAfterK4/dep-probe/*.json`, parsed by me):

```
env-nosasq-gap.json     handlers ['squashfs_v4_be']  gaps [('missing-extractor-dependency',['sasquatch-v4be'])]
env-leonly-gap.json     handlers ['squashfs_v4_be']  gaps [('missing-extractor-dependency',['sasquatch-v4be'])]
env-v4beonly-ok.json    handlers ['squashfs_v4_be']  gaps []
```

The frozen harness still repeats the false premise in its header
(`tools/round-38/c1-run.sh:5-6`, unchanged by `cb4326b2` and by the worktree):
"with stock unblob (no external extractor dependency needed for standard BE v4)".

Impact: C1 is still **scorable** (the frozen counter only requires the after-receipt to have no
gaps, which holds when sasquatch-v4be is on PATH), but it would be **met under a stated premise that
the round's own evidence refutes** — a calibration defect in the claim text, and the direct cause of
§1 (somebody tried to repair the text inside the counter instead of reporting it).

Response I would advise the L1 to own: an honest premise correction in the claim/knowledge entry
("BE v4 needs sasquatch-v4be; measured, both arms"), and the freezing of the harness header — not a
counter edit. Peers already flagged it: `R38CrossToolK1.md:208`, `R38CrossToolK4.md:145`.

---

## 3. MEDIUM — lane-root contamination by a seat's tool run

```
$ git -C <lane> status --porcelain          # from 03:24:32
?? unblob.log                               # 3,617 B, mtime 03:24:32.055
```

Attributed from the file's own content:

```
2026-10-26 06:24.31 [debug] Logging configured  extract_root=. pid=2284863
… Activated FS access restrictions; rules=[Read("/"), ReadWrite("/dev/shm"),
  ReadWrite("/fast/scratch/hyaku/kaidoku-r38/R38ExecBeforeArmRecheck/run/unblob-stock"), …,
  ReadWrite("unblob.log")]  status=FullyEnforced
… Running extract command command='sasquatch-v4be -be -no-exit-code -f -d
  /fast/scratch/hyaku/kaidoku-r38/R38ExecBeforeArmRecheck/run/unblob-stock/carrier.bin_extract
  <lane>/corpus/evidence/round-37/c1/K3/carrier.bin'
```

Seat `R38ExecBeforeArmRecheck` ran `unblob` with its CWD at the **lane root**; unblob logs to
`./unblob.log` and the landlock rule `ReadWrite("unblob.log")` (relative) let it write there. Content
is benign (K3 carrier paths, handler names), no secrets, but it is a write outside the seat's
report/artifact area — and it is untracked in a tree the L1 commits wholesale (`jj file track` +
`commit` on whole subtrees is the observed pattern, §5), so it would ride into an integration commit.

Remediation: `rm <lane>/unblob.log` before integrating; seat should run with
`cd "$S" && unblob …`; optionally add `unblob.log` to `.gitignore` and a clean-tree assertion to the
integration gate. (I did not delete it — not mine.)

---

## 4. MEDIUM — one peer artifact carries a false green on drifted bytes

`artifacts/R38ExecSelftests/lane-drift-observation.json` records, for the 03:22 drift:

```
{"at":"03:22:04","sha256":"f27f982bb4c8…","equals_frozen":false,
 "selftest":"15 cases / green 1 / red 14 / failures [] / exit 0 (drift invisible to the selftest at this stage)"}
```

Those bytes cannot produce that verdict: `ast.parse` fails (`SyntaxError` line 173) and running the
live file gave exit 1 with no cases (both measured twice, and the identical sha is preserved as
`artifacts/R38SentinelBounds/c1-counter.py.snapshot-0322`). The same artifact's **next** entry does
record the correct `AttributeError` for 03:23, so this is a mislabelled verdict (frozen-copy result
attached to drifted bytes), not a fabricated observation of the later state.

Remediation: correct that row to "NO VERDICT: SyntaxError line 173, exit 1" before the L1 quotes it.
A drifting instrument means every "selftest still green" claim in the wave must name the sha it ran.

---

## 5. INFO — VCS seam is clean for leaves; one mid-wave L1 commit

All 25 mutating `jj` operations in the window are by the orchestrator identity `plazir27`; none by a
wave-1 seat. Sequence (op-store descriptions, read-only):

```
03:06:31  commit … → bookmark main → e059ca93  (freeze)   + push
03:09:14  commit … → bookmark main → efd5c47a  (controls)  + push
03:15:59  commit … → bookmark main → 9c9d496b  (w1 spec/dispatch) + push
03:19:01  commit … → bookmark main → cb4326b2  (c1-run.sh fix)   + push
```

`cb4326b2` ("harness fix (REA refuses existing extraction root; oracle mode unchanged)") is
`tools/round-38/c1-run.sh`, 3 insertions / 2 deletions — `mkdir -p "$OUT"` → `rm -rf "$OUT"` plus a
header note. It landed **at 03:19:01, after receipts at 03:16-03:18 and while seats ran**, so wave-1
receipts span two harness generations; the harness sha is pinned in no receipt I inspected
(`artifacts/*/after.json` carry `subject.digest.sha256` and `engine.executable_sha256`, not the
harness blob). `git ls-files .ufo/waves/round-38` shows only the frozen L1 paths; the whole `w1/`
subtree is untracked at HEAD, i.e. **no seat output has entered VCS**.

Also benign-but-unclean: `tools/round-38/__pycache__/` (03:04, 03:09, 03:23) — bytecode from runs
that did not pass `-B`; git-ignored, stale entry invalidated by mtime+size, so no stale-pyc risk.

---

## 6. Seam checks that came back clean

**6a. Write containment.** Full lane status at 03:20:30 and 03:25:40 is identical except `unblob.log`:
`M tools/round-38/c1-counter.py` + the four untracked wave paths. `git status --porcelain tools/ .ufo/
plans/ corpus/` shows **no** change under `corpus/`, `plans/`, `PROVINCE.md`, `corpus/SOURCES.md`,
`corpus/README.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`. `corpus/evidence/round-38/c1/` exists but
holds **zero files** (L1 created the dir at 03:03; no seat landed receipts). Lane writes outside the
wave dir since 03:02: only `.jj/repo/{op_store,store}/…` internals (the orchestrator's commits above)
and `unblob.log`.

**6b. Artifact path escapes.** At 03:20:30: 113 files / 29 dirs; at 03:26:00: 267 files / 30 dirs.
`find artifacts -type l` → **empty** (no symlinks at all). `find artifacts -path '*..*'` → empty.
Every path's `realpath -m` resolves under the artifacts root. `find artifacts ! -type f ! -type d` →
empty (no FIFO/device/socket). Extraction trees present (`R38ExecProvincePatch/extract-K*`,
`R38ExecAfterK4/extracted`) contain only regular files with plain names — nothing that a later
`cp -r` could turn into an escape.

**6c. Executable payloads in artifacts** (4, `0755`): `R38ExecMirrorGate/{merge-mirror,normalize-append,selftest-normalize}.py`,
`R38ScribeScorecardDraft/draft-clauses.py`. Inspected because the L1 may run them:
`merge-mirror.py` copies `--lane` read-only and **refuses** `--mirror` equal to or inside the lane
(`:64-67`), but it then does `shutil.rmtree(mirror)` on whatever `--mirror` names — safe only if the
caller passes a scratch path; worth an explicit `HYAKU_SCRATCH` prefix assertion if it is ever
promoted out of the artifacts dir. No absolute write targets to `corpus/` in any of them.

**6d. Secrets / credentials.** `grep -rInE` over `w1/` (all file types, not just md) plus
`round-38/controls/` and `round-38/c1/` for `sk-…`, `ghp_/gho_`, `op://`, `AKIA…`,
`-----BEGIN … PRIVATE KEY`, `eyJ….`, `xox[baprs]-`, `npm_…`, and for
`(password|passwd|secret|token|credential|\.netrc|id_rsa|ssh-|https?://[^ ]*@)` → **0 matches**
(only false-positive hits were prose like "no token"). No credentials in extraction logs either.

**6e. pacman / host mutation.** `grep -rn '\bpacman\b' w1/` → 3 hits, **all negative assertions**
(`R38CrossToolK4.md:24`, `R38CrossToolK2.md:30`, `R38ExecAfterK3.md:225`). No `-Sy/-Syu/-S/-U/-R`, no
service restarts, no installs by this seat (python3 stdlib, `git` read-only, `node` via the frozen
selftest, `ast`/`sha256sum`/`stat` only).

**6f. shokuknow read-only.** `find /home/vgpnk/Projects/shokuknow -newermt '2026-10-26 02:00' -type f`
→ empty. No campaign tool run there.

---

## 7. Scratch hygiene

`/fast/scratch/hyaku/kaidoku-r38`: **30 dirs, 498 M** at 03:25 (823 M at 03:20 — live seats are
cleaning as they finish). Named-seat dirs with a finished report **and a removed scratch** (verified
absent): `R38CrossToolK2`, `R38CrossToolK4`, `R38ScoutFreetzAvm`, `R38ScoutUnblobHandler`,
`R38ExecRecountBase`; `R38ScoutSasquatchReadme` / `R38ScoutUnblobFixtures` never created one.

Leftovers, by owner class:

* live seats (report not yet written or seat still running): `R38ConnSiblingOverlap`,
  `R38CriticClaimsC1`, `R38CriticClaimsC2`, `R38CriticSourcedClaim`, `R38CrossToolK1`,
  `R38CrossToolK3`, `R38ExecAfterK1..K4`, `R38ExecAfterK3-after`, `R38ExecBeforeArmRecheck`,
  `R38ExecEnvelopeRules`, `R38ExecIdCollision`, `R38ExecMirrorGate`, `R38ExecProvincePatch`,
  `R38ExecQuarantine`, `R38ExecSelftests`, `R38ScoutUnblobFixtures`, `R38ScribeSOURCES`;
* **orphan / non-seat (L1-owned, no seat to clean them)**: `c2dbg.yhy5xg3i` (03:05),
  `controls-c1-1`, `controls-c1-2`, `controls-c2-1..3` (all 03:08-03:09, 0 B),
  `l1-harness`, `l1-harness2`, `l1-k3-envset`, `l1-k3-envunset`, `l1-k3-rerun`, `l1-test`,
  `l1-test-k3`, `xpin-dbg`, `xpin-dbg2`, and the loose file `mint.wrapped.json` (10,486 B, 03:24 —
  still being rewritten, so the counter selftest is running somewhere).

Two of the large ones dominate the footprint: `R38ExecAfterK4` 400 M, `R38ExecMirrorGate` 243 M.
`/tmp` was at 89 % per `.ufo/state/disk-guard.log` at 02:31 — nothing in this wave is under `/tmp`.

My own `S=/fast/scratch/hyaku/kaidoku-r38/R38SentinelBounds` (716 K) is removed before yield; the
evidence it produced was copied into `artifacts/R38SentinelBounds/`.

---

## 8. Misroot pre-scan (fleet root, read-only; nothing deleted or moved)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | awk '{print $1}' | sort | uniq -c
      1 ??
    157 A
     19 M
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | grep '^??'
?? .ufo/state/disk-guard.log          # 1,095,447 B, 12,074 lines, appended continuously
```

* **Untracked fleet-root files: 1.** `.ufo/state/disk-guard.log` — a disk-guard log, not a lane
  artifact. Content check: `grep -icE 'kaidoku|round-38'` → 2 matching lines, both **older bases**
  (`/fast/scratch/hyaku/kaidoku-r36` "absent", `/fast/scratch/hyaku/kaidoku-r37` "keep-live"). It
  names **no round-38 path**.
* **Staged-added (157) and modified (19) entries**: `grep -c 'round-38'` over every one of those
  paths → **no matches** (checked all 157 `A` entry names in the first 120 by content). They are the
  pre-existing tower/.ufo bookkeeping from rounds 18-100 plus other lanes — not round-38 content.
* Fleet-root files touched since wave start and outside the lane: `.ufo/reports/round-38/kengaku.md`,
  `.ufo/prompts/closure/kengaku-round-38.md`, `.ufo/state/{inline-dispatcher.log,disk-guard.log,
  kasegi.report-baseline,watchdog.log}` and work inside the sibling lanes
  `kasegi/kengaku/tsukuroi/tabi/souji-shokunin`. Those name `kengaku`/`kasegi` rounds, **not**
  kaidoku — sibling-lane work, not a kaidoku misroot. No kaidoku file exists at the fleet root.

Verdict: **no misroot**; the misroot pre-scan is clean for round 38.

---

## 9. Counts at 03:26:00 -03 (final snapshot)

| metric | value |
|---|---|
| registry members (`swarm-registry.json`) | 40 |
| reports in `w1/` | 25 |
| artifact dirs | 30 (267 files) |
| reports with no artifact dir | 4 (`R38ConnSeparability`, `R38ScoutFreetzAvm`, `R38ScoutSasquatchReadme`, `R38ScoutUnblobFixtures`) |
| artifact dirs with no report | 9 (`R38CriticClaimsC1/2`, `R38CriticSourcedClaim`, `R38ReviewerCodeAudit`, `R38ReviewerEntryQuality`, `R38ReviewerPredicateIdentity`, `R38ScribeEntry`, `R38ScribeLessonSkeleton`, `R38SentinelBounds`) |
| reports whose trailer path ≠ filename | 0 (report paths are declared by dispatch — `w1-dispatch.json` `Report: write your scoped findings to .ufo/waves/round-38/w1/<Seat>.md` — and not repeated inside the file; every landed `.md` matches a registry member name) |
| stray files directly in `w1/` | 1 (`swarm-registry.json`, expected) |
| lane files modified outside the wave dir | 1 (`tools/round-38/c1-counter.py`), plus untracked `unblob.log` |
| files written into `corpus/` by seats | **0** |
| secrets found | **0** |
| pacman invocations | **0** |
| symlinks / escaping paths in artifacts | **0 / 0** |

---

## 10. Bottom line for the L1

1. **Revert `tools/round-38/c1-counter.py` to `a7a62b09…` before scoring anything**; the worktree
   instrument has been unrunnable since 03:22:17 and the frozen blob is the only one that produces a
   verdict (15/15, exit 0, re-verified in this seat). Snapshot set + diffs are in
   `artifacts/R38SentinelBounds/`.
2. Treat the `before`-arm rewrite as a **predicate proposal**, not an instrument fix: it needs an
   amended claim/premise (§2) and a re-freeze, or it stays out of round 38.
3. Resolve the premise contradiction one way or the other **before** landing the C1 knowledge entry —
   the round's own probes say `sasquatch-v4be` is required, the frozen predicate and harness header
   say it is not.
4. `rm <lane>/unblob.log` and correct the `f27f982b` selftest row in
   `artifacts/R38ExecSelftests/lane-drift-observation.json`.
5. Everything else on my surface is clean: no seat wrote into `corpus/`, no VCS mutation by a leaf
   seat, no secrets, no escaping artifact paths, no misroot at the fleet root.

`[INFERENCE]` — stated as inference, not measured: the author of the counter edits is **not** a
leaf seat (all five executor/cross-tool reports that touch the counter explicitly disclaim changing
it — `R38CrossToolK1.md:9`, `R38ExecAfterK1.md:15`, `R38ExecAfterK2.md:141`, `R38ExecAfterK3.md:6`,
`R38ExecAfterK4.md:4` — and the only other identity mutating this repo in-window is the orchestrator
`plazir27`); I have no process-attribution evidence tying a specific agent to the writes.

---

## 11. ADDENDUM (03:26:29 → 03:27:40) — the amendment arrived, and it is not a freeze yet

While I was writing §1-§10 the L1 acted on exactly the two defects above. This section records the
new state, because it changes what §1 means and what the L1 must still do.

### 11a. `plans/round-38-claims.md` is now a **freeze-v2 amendment** — uncommitted

```
$ git -C <lane> status --porcelain
 M plans/round-38-claims.md          # NEW at 03:26 (was clean for the whole window before)
 M tools/round-38/c1-counter.py
?? .ufo/waves/round-38/{assimilation/,w1.ready,w1.ready.dispatched,w1/}
$ git -C <lane> diff --stat -- plans/round-38-claims.md
 plans/round-38-claims.md | 83 +++++++++++++++++++++++++++--------------------
 1 file changed, 48 insertions(+), 35 deletions(-)
$ git -C <lane> log --oneline -1
cb4326b2 round-38: harness fix (REA refuses existing extraction root; oracle mode unchanged)
```

What v2 changes (diff preserved at `artifacts/R38SentinelBounds/claims-diff-vs-HEAD.txt`, full doc at
`round-38-claims.md.snapshot-0326`):

* header → "frozen claims (**freeze v2**)" with an explicit **pre-scoring amendment** note: v1's
  "no external extractor dependency" framing is withdrawn, and v2 states the measured truth —
  unblob 26.6.4's `SquashFSExtractor` **requires `sasquatch-v4be` on PATH** for BE v4 — plus the
  root cause of the v1 miss: "the L1's v1 probes never actually stripped `~/.local/bin` —
  `grep -v sasquatch` filters PATH component names, not the binaries inside them."
* P38-C1 restated with a **paired before-receipt** ("run with `sasquatch-v4be` unavailable …
  names `sasquatch-v4be` as a missing extractor dependency"), before receipts declared **frozen with
  the claim** at `corpus/evidence/round-38/c1/K*/before.json`, after receipts the claim data.
* Selftest target raised from 15 to **18 cases**; kill rule re-scoped to "the v2 freeze / the v2
  controls"; "No claim was scored under v1".
* C2 gains a disclosure paragraph (several red cases fail via `guards_ok`, three cases use paths the
  LANE allowlist rejects) — text only; `c2-counter.py` is byte-identical to the freeze
  (`7f137b66…`, re-verified at 03:25).

This **confirms §2** (v1's premise was false and its probes were methodologically wrong) and it is the
right instrument for §1 — a claim change belongs in the claims doc, not in the counter.

### 11b. …but as of my last sample none of the four pieces of a v2 freeze exist

| required for "the v2 freeze" | state at 03:27 |
|---|---|
| a **commit** holding v2 claims + v2 counter | **absent** — HEAD is still `cb4326b2`; both files are worktree `M` |
| frozen `before.json` receipts ("frozen with the claim") | **absent** — `find corpus/evidence/round-38 -type f` → nothing |
| v2 controls scored at the v2 freeze | **absent** — `.ufo/waves/round-38/controls/ctl-c1-{0,1,2}*.json` carry `--rev/--freeze e059ca9391642d5b71b6662cabcbdce0d9308719` (v1), committed at `efd5c47a` |
| a counter that implements v2 (18-case selftest green) | **closest yet, still short** — 8th state (03:28:2x) runs 18 cases and returns `green_ok: 0`, `failures: ["green: want 0 got 1"]`, exit 1 |

Counter drift continued past §1's table:

| 6th observed state (mtime 03:26:29) | sha256 `1b4dc73003bc0f295884207d94ca5ae4888d77542f6f7f69c951c12268df9a14` |
|---|---|
| parse | `PARSE_OK`, 417 lines |
| `--selftest` (scratch tree, `TMPDIR=$S`) | **`UnboundLocalError: cannot access local variable 'n' where it is not associated with a value`, exit 1** |

| 7th observed state (mtime 03:27:4x) | sha256 `dd08322b93c54b7dee99af5fd73e30bec2e1f987eca6d662ed16dde2c643dd75` |
|---|---|
| parse | `PARSE_OK`, 427 lines |
| `--selftest` | **`AttributeError: 'NoneType' object has no attribute 'get'`, exit 1** |

| 8th observed state (mtime 03:28:2x, last sample 03:28:31) | sha256 `122fb982309db9570c8127b0f618b05087e05fe013151587d259b77f9e469b95` |
|---|---|
| parse | `PARSE_OK` |
| `--selftest` | **runs, reports `{"cases": 18, "green_ok": 0, "red_ok": 17, "failures": ["green: want 0 got 1"]}`, exit 1** |

Eight distinct byte-states of a frozen instrument in 6m14s: **six post-freeze states produced no
verdict at all, and the eighth now matches v2's 18-case spec but fails its own green case**
(`green: want 0 got 1`) — so it is still not an admissible instrument. The only runnable *and*
self-verifying bytes remain the frozen blob `a7a62b09…` (15/15, exit 0). `unblob.log` (§3) was removed
by 03:26:53 (`ls unblob.log` → No such file). Snapshots of every state are in
`artifacts/R38SentinelBounds/` (`c1-counter.py.snapshot-0322/0323/0324/0326/0327/0328`,
`c1-counter.py.final-snapshot`, `c1-counter.HEAD-e059ca93.py`).

### 11c. What this costs, and the one thing that closes it

A receipt produced now cannot name a freeze: the counting command needs `--freeze <FREEZE>` and no
revision contains the v2 claim, the v2 counter or the before receipts. Any report that already says
"frozen under v2" (none did at 03:26) would be unpinnable, and the "no claim scored under v1" claim
is only checkable against a commit. The freeze is therefore **in flight, not landed** — the honest
state for the scorecard is still "no freeze v2".

Closing move for the L1, in this order: (1) finish the counter so `--selftest` gives **18 cases,
`failures: []`, exit 0** against the v2 case list; (2) land the four before receipts and re-score the
three C1 controls at the new freeze; (3) one commit containing v2 claims + counter + before receipts
+ controls, and record that commit id as the freeze; (4) only then have seats produce after receipts
and run the counting command with `--freeze <that id>`; (5) require `git status --porcelain tools/
plans/` empty at the measured revision so no seat can score a worktree instrument again.

Severity of §1 as of this addendum: still **CRITICAL until step (3) lands** — the worktree counter is
unrunnable and the predicate text in it outranks nothing until committed — but the *honesty* defect is
being handled openly in v2 rather than silently, which is the direction the round should keep.
