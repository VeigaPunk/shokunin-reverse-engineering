# ScoutState — lane working state

Seat: ScoutState. Read-only on the lane. Nothing was deleted. No tool was installed. The two counters (`exact.py`, `record.py`) were **not run**.

The worktree moved while it was being measured. Counts below are tied to a named snapshot. Do not add them together.

## Cited porcelain snapshot

UTC `2026-10-28T17:51:51Z`. `jj_post` stdout sha256 `7e41905b68a2bc5a745d70538a06789812dc244870473fa4e6c5a8481b52d67c`, exit 0:

```
state branch=main local=62e33f7dd75c8e3285967b26419842c106f6c965 remote=e856beb552080c03ede6000b96f1b58bde44c421 ahead=1 behind=0 head=detached tracked=5 untracked=98
```

`git status --porcelain` (`por_post`) 103 lines, stdout sha256 `75dc4a50d084814d8c993f0c1faaec3002b4299dc0cb51fbe732a27567de38f3`, exit 0. `git status --porcelain=v1 -uall` (`por_post_all`) 192 lines, stdout sha256 `90c1086d47c6faf95c5f3e8657bb952f74c797c5729765780b43c4c730e1ff1d`, exit 0. Index empty at `2026-10-28T17:52:13Z` (`cached_post`, exit 0, 0 bytes). HEAD was still `62e33f7d` at `2026-10-28T17:52:13Z` (`head_a2`).

`jj-lane.sh` counts default porcelain, not `-uall`: `tracked=5` and `untracked=98` are the five ` M` lines and 98 `??` lines. `-uall` expands untracked directories, so it is larger (192).

`git symbolic-ref -q HEAD` at `2026-10-28T17:49:52Z` exited 1 with empty stdout (detached). Every later `jj-lane.sh state` line says `head=detached`.

## Prefix counts (cited snapshot)

Default porcelain, first path component and round prefix:

| prefix | lines | of which |
|---|---:|---|
| `.ufo` | 103 | the entire dirty set |
| `.ufo/waves/round-45` | 8 | 2 ` M`, 6 `??` |
| `.ufo/waves/round-46` | 74 | 3 ` M`, 71 `??` (directories collapsed) |
| `.ufo/waves/round-47` | 21 | 0 ` M`, 21 `??` (directories collapsed) |
| `SCORECARD.md` / `SKILL.md` / `corpus/` / `tools/` | 0 | clean at this instant |

`-uall` file inventory (directories expanded):

| bucket | files |
|---|---:|
| round 45 | 8 |
| round 46 | 158 |
| round 47 | 26 |
| anything else | 0 |

The 21 default round-47 rows are `l1/`, `w1.ready`, `w1.ready.partial`, and 18 seat directories (`por_post.out` lines 83–103). Expansion to 26 files is `l1/scores/` (2), `C1Ids/` (2), `C2Atoms/` (2), `ScribeAxesRow/` (2), `ScribeLesson/` (2): five extra files, 21+5=26.

## What belongs to this round vs an earlier one

Inherited means present and uncommitted at the cited snapshot. This seat had not written a lane path yet.

**This round, untracked (26 files).** Wave receipts and two L1 score files. Not in HEAD. Full list in the inventory below.

**This round, but already committed by the cited snapshot** (not dirty): `SKILL.md` block 24, `SCORECARD.md` record-corrections section and axis heads, `corpus/SOURCES.md` S143. They were dirty against `3186f69b` at `2026-10-28T17:49:52Z`–`17:50:35Z` and were committed by `e856beb5` (`land_names`: only those three paths). `diff --numstat` at the cited snapshot does not name them.

**Earlier rounds, still dirty (166 `-uall` paths = 8 + 158).** Five of them are tracked modifications; `numstat_tracked` (exit 0, stdout sha256 `43e233d7673951788b3fcaeddf23cfca1cd39f509c3cf52d23719fd5f51151fd`):

| path | insertions | deletions |
|---|---:|---:|
| `.ufo/waves/round-45/w2/R45W2Immutable/G-final-tip.txt` | 10 | 0 |
| `.ufo/waves/round-45/w2/R45W2Immutable/report.md` | 63 | 19 |
| `.ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/manifest.txt` | 16 | 3 |
| `.ufo/waves/round-46/w1/R46W1MutC1Checks/report.md` | 50 | 13 |
| `.ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/runs.jsonl` | 4 | 0 |

The other 161 earlier-round paths are untracked. Round-46 default porcelain collapses some of them into directory rows (74 lines vs 158 files). No staged changes.

## `__pycache__`

Ignored. `check_pyc` at `2026-10-28T17:51:51Z`, exit 0, stdout sha256 `3f4f5d9b31edaeee782c5a22fe523dfe8a3202e2e4c55a2202df40968fbae105`:

```
.gitignore:1:__pycache__/	tools/round-47/__pycache__
.gitignore:1:__pycache__/	tools/round-47/__pycache__/exact.cpython-314.pyc
.gitignore:1:__pycache__/	tools/round-47/__pycache__/record.cpython-314.pyc
```

`ls-files -o -i --exclude-standard -- tools/round-47` lists exactly those two `.pyc` files (stdout sha256 `30b4a92dd897fc60707daf03d277147724da43853ebbd5f4cb1378d621945242`). They are absent from porcelain. An earlier probe of a non-existent `exact.cpython-313.pyc` also matched the same rule: `check-ignore` matches the path pattern, not a file that has to exist. `ls-files -v` at `17:50:35Z` printed `H` for the three frozen paths (cached, not assume-unchanged).

## HEAD motion (do not treat the prompt freeze as the tip)

| when (UTC) | local main | what changed |
|---|---|---|
| 17:49:52Z `jj_state` | `3186f69b49798f2cc05727bbfd1604505fcee03b` (local=remote, ahead=0) | worktree dirty: the five earlier-round edits, plus uncommitted `SKILL.md` / `SCORECARD.md` / `corpus/SOURCES.md`, plus uncommitted `tools/round-47/record.py` |
| 17:50:22Z | still `3186f69b` (freeze log still `5017e1f`) | `diff --quiet 5017e1f HEAD -- plans/round-47-claims.md tools/round-47` exit 0. `diff --quiet HEAD --` those paths exit 1 (worktree record.py dirty). `merge-base --is-ancestor 13a9e9e1 5017e1f` exit 0. `merge-base --is-ancestor 5017e1f HEAD` exit 0 |
| 17:50:35Z `jj_state2` | still `3186f69b`, tracked=9 untracked=93 | porcelain shows ` M tools/round-47/record.py`. Worktree blob `79fb27a8`, HEAD/freeze blob `1f8e7928`. exact.py and claims.md worktree blobs still equal freeze (`fb21a166`, `81aeb65e`) |
| 17:50:58Z `jj_final` | `9018c53b16503c8d06d398b75503406508119946` local=remote | A1 committed. tracked=8 untracked=95 (product files still dirty) |
| 17:51:17Z | `e856beb552080c03ede6000b96f1b58bde44c421` | landing commit, parent `9018c53b`. Worktree frozen paths match HEAD (exit 0) |
| 17:51:51Z cited snapshot | `62e33f7d` local, remote `e856beb5`, ahead=1 | A2. See below |
| 17:53:05-03:00 commit, observed 17:53:37Z | `1e2c3102952dc636650095643c1963c833859019` local=remote, ahead=0, tracked=5 untracked=110 | A3 then A4. Porcelain +12 round-47 directory rows, zero removals. See below |

Commit subjects (`log_post`, then `log_span`):

- `9018c53b` `2026-10-28T14:50:37-03:00` round-47: freeze amendment A1 - drop the unreachable window-pair clause
- `e856beb5` `2026-10-28T14:51:02-03:00` round-47: land craft block 24, the record corrections, the current axis heads and S143
- `62e33f7d` `2026-10-28T14:51:50-03:00` round-47: A2 - make the window forgery a real forgery; block 24 arm cells carry only the token
- `2e4ae434` `2026-10-28T14:52:38-03:00` round-47: A3 - a seats/window correction for a round older than the window stays valid evidence
- `1e2c3102` `2026-10-28T14:53:05-03:00` round-47: A4 - the historical-correction selftest fixture gets its round-3 dispatch

Per-commit paths that were actually diffed:

- `3186f69b..9018c53b` (`split_a1`): `A .ufo/waves/round-47/controls/ctl-c2-2-freeze-amendment.json`, `M plans/round-47-claims.md`, `M tools/round-47/record.py`. `diff --quiet 5017e1f 9018c53b --` frozen paths exit 1.
- `9018c53b..e856beb5` (`land_names`, frozen stat empty): `M SCORECARD.md`, `M SKILL.md`, `M corpus/SOURCES.md`. The landing commit does not touch a frozen path.
- `e856beb5..62e33f7d` (`a2_names`): `M SKILL.md`, `M plans/round-47-claims.md`, `M tools/round-47/record.py`. Frozen stat: claims +9, record.py +5/−3.
- `62e33f7d..1e2c3102` net (`names_late`): `M tools/round-47/record.py` only, +14/−3. A3's own path list was **not** diffed separately. The net tree versus A2 contains no other path. `git log -1 -- plans/round-47-claims.md` at `17:53:37Z` still prints `62e33f7d` (`rederive_late`).

`tools/round-47/exact.py` blob is unchanged from `5017e1f` through `62e33f7d` (`exact_same` exit 0) and is absent from the `62e33f7d..1e2c3102` name-status.

`git log --format=%H -1 -- plans/round-47-claims.md`, the claims file's own freeze re-derivation:

- `17:50:22Z` → `5017e1f7299c3a812e87e7950148f54313dd279e` (41-byte stdout, sha256 `1679a923d4a6048a81d536b6e7876107a8f1332476597a7cbb1a4fd2f560cf43`)
- `17:51:51Z` and `17:53:37Z` → `62e33f7dd75c8e3285967b26419842c106f6c965`

The prompt freeze remains an ancestor (`ancestor_freeze` exit 0, `anc` exit 0). It is not the tip of the frozen paths.

`diff --stat 5017e1f HEAD` for the frozen paths at `17:52:13Z` (HEAD `62e33f7d`): claims.md +21, record.py +8/−8. Worktree matched that HEAD (`wt_frozen` exit 0). At `17:53:37Z` HEAD had moved again and record.py had moved again; that second stat is `frozen_late`, not a replacement for the first.

## What the freeze sentence claims vs what the counters contain

Observed in source, counters not executed:

- `tools/round-47/exact.py` `evaluate` calls `gate.freeze_state` and returns 2 immediately when that returns 2 (`exact.py` around the `freeze_state` call). `tools/round-46/gate.py` `freeze_state` returns 2 `frozen_worktree_dirty` when `git status -z` shows an uncommitted frozen path, else 2 `frozen_path_changed` when blob or history differs between `--freeze` and `--rev`.
- `tools/round-47/record.py` imports `gate` but `evaluate` uses only `resolve`, `show`, `out_path`, `main_guard`, `emit`. Grep of `record.py` for `freeze_state`, `frozen_path`, and `--freeze` found no matches. A frozen-path edit does not, in this source, make `record.py` exit 2 `frozen_path_changed`.

Inference, not a counter run: `exact.py --freeze 5017e1f --rev 62e33f7d` (and likewise `--rev 1e2c3102`) would take the `frozen_path_changed` branch, because the committed blobs differ and, at `17:52:14Z`, the worktree was clean. `record.py` would not take that branch. The claims sentence that a post-freeze change makes **both** counters exit 2 `frozen_path_changed` is false for `record.py` as read at HEAD `1e2c3102`.

A2's added paragraph says the battery-window change is not a clause and that every clause is byte-identical to A1. The diff `e856beb5..62e33f7d` of `record.py` is not empty: `run_battery` forges `empty in <root-commit>..<rev>` instead of `empty in <captured-hex>..<rev>`. That is a frozen-path byte change. Whether it is "a clause" is the paragraph's wording; the bytes are not the A1 bytes.

## Not run

- `python3 -I -B tools/round-47/exact.py` (any arguments)
- `python3 -I -B tools/round-47/record.py` (any arguments)
- no fixture repo, no commit, no install

## Inventory at the cited snapshot (`-uall`)

Source file `receipts/classified-post.txt`, captured from `por_post_all`. This list does **not** include paths that appeared after `17:51:51Z`.

## other (0)

## r47 (26)
?? .ufo/waves/round-47/l1/scores/c1-at-L1.json
?? .ufo/waves/round-47/l1/scores/c2-at-L1.json
?? .ufo/waves/round-47/w1.ready
?? .ufo/waves/round-47/w1.ready.partial
?? .ufo/waves/round-47/w1/C1Battery/base-v3.json
?? .ufo/waves/round-47/w1/C1Digest/receipt.json
?? .ufo/waves/round-47/w1/C1Ids/receipt-head.json
?? .ufo/waves/round-47/w1/C1Ids/receipt.json
?? .ufo/waves/round-47/w1/C1Order/receipt-freeze.json
?? .ufo/waves/round-47/w1/C1Refs/receipt.json
?? .ufo/waves/round-47/w1/C1Struct/receipt.json
?? .ufo/waves/round-47/w1/C1Tokens/receipt.json
?? .ufo/waves/round-47/w1/C2Atoms/receipt-at-landing.json
?? .ufo/waves/round-47/w1/C2Atoms/receipt.json
?? .ufo/waves/round-47/w1/C2Corrections/receipt.json
?? .ufo/waves/round-47/w1/C2Mismatch/receipt.json
?? .ufo/waves/round-47/w1/C2Vacuity/receipt.json
?? .ufo/waves/round-47/w1/RevC2Axes/r47-freeze-record.json
?? .ufo/waves/round-47/w1/RevC2Before/record-base.json
?? .ufo/waves/round-47/w1/RevC2Dispatch/base-c2.json
?? .ufo/waves/round-47/w1/ScoutAxes/record-at-freeze.json
?? .ufo/waves/round-47/w1/ScribeAxesRow/receipts/record-3186f69b-head.json
?? .ufo/waves/round-47/w1/ScribeAxesRow/receipts/record-e856beb5.json
?? .ufo/waves/round-47/w1/ScribeCorrections/c2-at-3186f69b.json
?? .ufo/waves/round-47/w1/ScribeLesson/receipts/head-exact.json
?? .ufo/waves/round-47/w1/ScribeLesson/receipts/head-record.json

## r45 (8)
 M .ufo/waves/round-45/w2/R45W2Immutable/G-final-tip.txt
 M .ufo/waves/round-45/w2/R45W2Immutable/report.md
?? .ufo/waves/round-45/l1/preflight-c86ea508.json
?? .ufo/waves/round-45/l1/preflight-round45-frozen.json
?? .ufo/waves/round-45/w1.ready.dispatched
?? .ufo/waves/round-45/w2.ready.dispatched
?? .ufo/waves/round-45/w2/R45W2Immutable.md
?? .ufo/waves/round-45/w2/R45W2Immutable/I-supplementary.txt

## r46 (158)
 M .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/manifest.txt
 M .ufo/waves/round-46/w1/R46W1MutC1Checks/report.md
 M .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/runs.jsonl
?? .ufo/waves/round-46/r46-w1-results.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attack10.py
?? .ufo/waves/round-46/w1/R46W1CritC1/attack7.py
?? .ufo/waves/round-46/w1/R46W1CritC1/attack9.py
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks10.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks2.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks3.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks4.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks5.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks6.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks7.json
?? .ufo/waves/round-46/w1/R46W1CritC1/attacks9.json
?? .ufo/waves/round-46/w1/R46W1CritC1/census-regen.json
?? .ufo/waves/round-46/w1/R46W1CritC1/cheapest-green-block.md
?? .ufo/waves/round-46/w1/R46W1CritC1/freeze-matrix.json
?? .ufo/waves/round-46/w1/R46W1CritC1/g-final-04252247.out
?? .ufo/waves/round-46/w1/R46W1CritC1/g-final-31820472.out
?? .ufo/waves/round-46/w1/R46W1CritC1/matrix-round-46.json
?? .ufo/waves/round-46/w1/R46W1CritC1/matrix.py
?? .ufo/waves/round-46/w1/R46W1CritC1/measured-rev.txt
?? .ufo/waves/round-46/w1/R46W1CritC1/receipts-C1.json
?? .ufo/waves/round-46/w1/R46W1CritC1/receipts.py
?? .ufo/waves/round-46/w1/R46W1CritC1/report.md
?? .ufo/waves/round-46/w1/R46W1CritDenominator.md
?? .ufo/waves/round-46/w1/R46W1CritDenominator/report.md
?? .ufo/waves/round-46/w1/R46W1LabratBatteryCost/report.md
?? .ufo/waves/round-46/w1/R46W1MutC1Checks.md
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/harness/analyse.py
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/harness/capture.py
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/harness/driver.py
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/harness/driver_c.py
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/harness/probe.py
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/artefact-arm-prefix.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/curreal-cur-m10-drop-refs-min.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/curreal-cur-m4-rows-floor-8.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/curreal-cur-m7-vocab-whole-row.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/curreal-cur-m9-drop-allowlist.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/curreal-cur.json
?? .ufo/waves/round-46/w1/R46W1MutC1Checks/receipts/summary-cur.json
?? .ufo/waves/round-46/w1/R46W1MutGate.md
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/cov.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/cov2.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/matrix.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p12b.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p12c.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p1_m1_merge.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p1c.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p1p2_final.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p2_m2_blob.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p2c.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p2d.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p2e.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p2f.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p3_shrink.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p3b.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p46_m4_m6.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p4b.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p5b.py
?? .ufo/waves/round-46/w1/R46W1MutGate/probe/p5c.py
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/coverage/cov2-base-attest.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/coverage/cov2-base-registry.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/coverage/cov2-headbase-attest.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/coverage/cov2-headbase-registry.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/freeze-admissibility.txt
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/h2h-base-attest.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/headprobe-h1.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/headprobe-h2.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/headprobe-headbase.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/mt2-04252247-1e32827b.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/mt2-50862e4a-781e19ae.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/mt2-50862e4a-87578656.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/mt2-65678df0-17a72375.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/mutation-matrix.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p1c-merge-direction2.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p2e2-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p2e2-m2.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p2f-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p2f-m2.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p3b-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p3b-m3.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p46-h6.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p46-headbase.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p5b-h5.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/p5b-headbase.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/probe-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/probe-m1.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/probe-m1b.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/probe-m2.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-base-attest-nobat.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-base-attest.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-base-registry-nobat.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-base-registry.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-m2-attest.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/real-m2-registry.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/selfref-attest-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/selfref-attest-fullbattery.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/selfref-attest-headbase.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/selfref-registry-base.json
?? .ufo/waves/round-46/w1/R46W1MutGate/receipts/selfref-registry-headbase.json
?? .ufo/waves/round-46/w1/R46W1MutGate/report.md
?? .ufo/waves/round-46/w1/R46W1ProbeCost.md
?? .ufo/waves/round-46/w1/R46W1ProbeCost/attest-F5-full.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/attest-freeze3182-revF4.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/attest-literal-freeze.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/attest-r45-fidelity-no-battery.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/attest-r45-fidelity-with-battery.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/c1-F5.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/c1-F5b.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/c2-F5.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/c2-F5b.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/c1-F5.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/c2-F5.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/env.txt
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/frozen-attest-3182047.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/frozen-registry-3182047.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/drive.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/drive2.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/drive3.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/fixtime.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/measure.sh
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/memo.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/harness/rss.py
?? .ufo/waves/round-46/w1/R46W1ProbeCost/receipts/receipts.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/registry-F5-full.json
?? .ufo/waves/round-46/w1/R46W1ProbeCost/registry-literal-freeze.json
?? .ufo/waves/round-46/w1/R46W1SentTools.md
?? .ufo/waves/round-46/w1/R46W1SentTools/ab.json
?? .ufo/waves/round-46/w1/R46W1SentTools/current.json
?? .ufo/waves/round-46/w1/R46W1SentTools/freezeathead.json
?? .ufo/waves/round-46/w1/R46W1SentTools/frozen-c2.json
?? .ufo/waves/round-46/w1/R46W1SentTools/frozen-probes.json
?? .ufo/waves/round-46/w1/R46W1SentTools/receipts-table.md
?? .ufo/waves/round-46/w1/R46W1SentTools/receipts.json
?? .ufo/waves/round-46/w1/R46W1SentTools/report.md
?? .ufo/waves/round-46/w1/R46W1SentTools/shrink-cli.json
?? .ufo/waves/round-46/w1/R46W1SentTools/verify.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments.md
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/attest-v2.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/R10-registry-v2-count.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/R13-attest-selftest-F5.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/R14-registry-selftest-F5.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/R15-provenance.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/R9-attest-v2-count.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/demo2_out.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/demo3_out.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/demo_m12.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/demo_out.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/muts.out
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/muts2.out
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/muts3.out
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/muts4.out
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/receipts/probe-output-sha256.txt
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/registry-v2.json
?? .ufo/waves/round-46/w1/R46W1SimplInstruments/report.md



## After the cited snapshot (17:53:37Z)

`jj_late` exit 0, stdout sha256 recorded in `receipts/jj_late.meta`:

```
state branch=main local=1e2c3102952dc636650095643c1963c833859019 remote=1e2c3102952dc636650095643c1963c833859019 ahead=0 behind=0 head=detached tracked=5 untracked=110
```

Default porcelain 115 lines versus 103. Added only these 12 `??` directory rows (none removed):

- `.ufo/waves/round-47/w1/C1FreezeWindow/`
- `.ufo/waves/round-47/w1/CritC1Sizing/`
- `.ufo/waves/round-47/w1/RevC1Before/`
- `.ufo/waves/round-47/w1/ScoutCraftTail/`
- `.ufo/waves/round-47/w1/ScoutDispatch/`
- `.ufo/waves/round-47/w1/ScoutRounds/`
- `.ufo/waves/round-47/w1/ScoutState/` (this seat's receipt copy; the report files written after this line are also here)
- `.ufo/waves/round-47/w1/ScoutTools/`
- `.ufo/waves/round-47/w1/ScribeBlock24/`
- `.ufo/waves/round-47/w1/ScribeQuality/`
- `.ufo/waves/round-47/w1/ScribeReport/`
- `.ufo/waves/round-47/w1/ScribeShonen/`

The five earlier-round tracked modifications were still the dirty tracked set (`tracked=5`). Round-45 and round-46 paths were not removed. This seat did not re-expand `-uall` after 17:51:51Z.

## Every measurement

Receipts: `.ufo/waves/round-47/w1/ScoutState/receipts/`. Empty stdout sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is sha256 of zero bytes. `symbolic` exit 1 is the detached-HEAD result, not a failed command. `diff --quiet` exit 1 means the trees differ.

| name | UTC start | UTC end | exit | stdout sha256 | bytes | command |
|---|---|---|---:|---|---:|---|
| check_ignore | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `ce1aae04af9dbc3c52d4dd958c68fcafec7dec08191c98eb6942a28623b6ae6d` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin check-ignore -v -- tools/round-47/__pycache__ tools/round-47/__pycache__/ tools/round-47/__pycache__/exact.cpython-313.pyc` |
| jj_state | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `c7dc4a604bca350768200336a8d4e88b01bdcd6bff21b01021d9a142b813947d` |  | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| ls_r47 | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `30b4a92dd897fc60707daf03d277147724da43853ebbd5f4cb1378d621945242` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files -o -i --exclude-standard -- tools/round-47` |
| ls_tracked | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `83b4f30b3da5292e5b09e1de4a7c5d2e25815f36d2818bc057b7f1b55283a1fd` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files -- tools/round-47` |
| rev_parse | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `8baac26a7a1be7cb93cc68476e62c43f81dd5d79334795a72104fd0dc7248d48` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD refs/heads/main refs/remotes/origin/main` |
| status | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 0 | `124f763e0a1d4e9017758baa8a63035d590c8077060c691188568748d362ddb5` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain=v1 -uall --untracked-files=all` |
| symbolic | 2026-10-28T17:49:52Z | 2026-10-28T17:49:52Z | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |  | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin symbolic-ref -q HEAD` |
| ancestor_base | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 5017e1f7299c3a812e87e7950148f54313dd279e` |
| ancestor_freeze | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 5017e1f7299c3a812e87e7950148f54313dd279e HEAD` |
| check_ignore_real | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `229ed3135a5042b9eb5ef304476b5f8a7384071960b2549bda73f4d1380b7ec4` | 151 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin check-ignore -v -- tools/round-47/__pycache__/exact.cpython-314.pyc tools/round-47/__pycache__/record.cpython-314.pyc` |
| diff_cached_names | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --cached --name-only` |
| diff_names | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `20f60a202277f75d3162279d23f3ab7ddad4a89dee4edeb2eda2008ed30e103c` | 344 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-only` |
| diff_stat | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `359f40012e95a84fb3551357de2620ff98e4ff05f92a0260226684543302ac6f` | 161 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat -- SKILL.md SCORECARD.md corpus/SOURCES.md` |
| freeze_log | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `1679a923d4a6048a81d536b6e7876107a8f1332476597a7cbb1a4fd2f560cf43` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H -1 -- plans/round-47-claims.md` |
| frozen_vs_freeze | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 5017e1f7299c3a812e87e7950148f54313dd279e HEAD -- plans/round-47-claims.md tools/round-47` |
| frozen_vs_head | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet HEAD -- plans/round-47-claims.md tools/round-47` |
| porcelain_default | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `6bbe9bedf33b4c2789d198c8ef07a1a42c829339bfc2da3572ee2e0658aeeb45` | 5589 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| pyc_ls | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 0 | `6dd0260683786f1c7d7cf6f1716b59225d7891f3df6ef0a41d3037ce8cf59e9e` | 28 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files -o -i --exclude-standard --directory -- tools/round-47/__pycache__` |
| wt_vs_freeze | 2026-10-28T17:50:22Z | 2026-10-28T17:50:22Z | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 5017e1f7299c3a812e87e7950148f54313dd279e -- plans/round-47-claims.md tools/round-47` |
| diff_product | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `6db27492f9671c5d988139cd1f334ba6bf5ace49fdc4ecd6b7256cf07ebda698` | 21265 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff -- SKILL.md SCORECARD.md corpus/SOURCES.md` |
| diff_record | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `12c345c16282a0d2f377adda19b5716c563ce7f92985d1b42e388b24bcd695e6` | 1182 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff -- tools/round-47/record.py` |
| diff_record_stat | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `1ce9e43c991c1195b86aafe65716cbcb9a19220ebb72c8245475cbeebb3b6044` | 88 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat -- tools/round-47/record.py tools/round-47/exact.py plans/round-47-claims.md` |
| hash_head | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `3794d82c28138065c0299865aa0b17911727564c5dede8e33f072aec9e245b17` | 246 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD:tools/round-47/record.py HEAD:tools/round-47/exact.py HEAD:plans/round-47-claims.md 5017e1f7299c3a812e87e7950148f54313dd279e:tools/round-47/record.py 5017e1f7299c3a812e87e7950148f54313dd279e:tools/round-47/exact.py 5017e1f7299c3a812e87e7950148f54313dd279e:plans/round-47-claims.md` |
| hash_wt | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `bec7bfd5f49cbcfca55070fec43d5ef1c221389295a3ccdeea9991b377f620c3` | 123 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin hash-object -- tools/round-47/record.py tools/round-47/exact.py plans/round-47-claims.md` |
| jj_state2 | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `d1d523849c43f4f30c1d2fcb3c907654cb4d4b64a6d438bdcaff5038413a446e` | 167 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| lsfiles_v | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `297bdd3e2dcf9dfddab80ff2cde650406f502ad2e081b1f01dfbf9ab0a432a80` | 80 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files -v -- tools/round-47 plans/round-47-claims.md` |
| porcelain2 | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `6bbe9bedf33b4c2789d198c8ef07a1a42c829339bfc2da3572ee2e0658aeeb45` | 5589 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| porcelain_r47tools | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `3a538e3f051bcf656b879af029b09c23847a2a6dea0ff12730ae762338d0de27` | 28 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain --untracked-files=all -- tools/round-47 plans/round-47-claims.md` |
| stat_files | 2026-10-28T17:50:35Z | 2026-10-28T17:50:35Z | 0 | `d14d1ac75ff2e4913c7637890766a156e343c6d4159e26e81bb27f3baeeb3d99` | 797 | `stat -c %n mtime=%y size=%s /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-47-claims.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/__pycache__ /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/__pycache__/exact.cpython-314.pyc /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/__pycache__/record.cpython-314.pyc` |
| jj_final | 2026-10-28T17:50:58Z | 2026-10-28T17:50:58Z | 0 | `1866e806704f0a2582b84df199d0a2e9835525f327ea33c81e0cd991766721a7` | 167 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| por_all | 2026-10-28T17:50:58Z | 2026-10-28T17:50:59Z | 0 | `6b42f34b5a49cead98febe3261f273525b32f29f2467fa4f3633c917500c81f1` | 11436 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain=v1 -uall --untracked-files=all` |
| por_final | 2026-10-28T17:50:58Z | 2026-10-28T17:50:58Z | 0 | `6af9d1cdadf8853f242f230049eb27c78b221f42e9828c4c6d55a78b9a4da5c4` | 5641 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| hash_final | 2026-10-28T17:50:59Z | 2026-10-28T17:50:59Z | 0 | `2e435335dae4fa474474f8c934fdc7990e635e806acc7c5996afa4d9612568e3` | 123 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin hash-object -- tools/round-47/record.py tools/round-47/exact.py plans/round-47-claims.md` |
| anc | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 5017e1f7299c3a812e87e7950148f54313dd279e HEAD` |
| blobs | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `bd7288c809f09dbec84c52ee23442fafba18143a92f81be32c8324f4cc67a2f7` | 246 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse 5017e1f7299c3a812e87e7950148f54313dd279e:tools/round-47/record.py HEAD:tools/round-47/record.py 5017e1f7299c3a812e87e7950148f54313dd279e:tools/round-47/exact.py HEAD:tools/round-47/exact.py 5017e1f7299c3a812e87e7950148f54313dd279e:plans/round-47-claims.md HEAD:plans/round-47-claims.md` |
| frozen_diff | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `13c37b5a1d275dd200dbc237c18c38e0d77542df7cb662b4f87c50cb900c580e` | 3065 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff 5017e1f7299c3a812e87e7950148f54313dd279e HEAD -- plans/round-47-claims.md tools/round-47` |
| frozen_stat | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `346f2b84c56d6fe5184f35a1c77126008680d42ad6fa300fe213bd00c8e32acc` | 135 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 5017e1f7299c3a812e87e7950148f54313dd279e HEAD -- plans/round-47-claims.md tools/round-47` |
| head_now | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `02f0effe441fe4da7e4a10cd7708e66d4351cdd02b73493b8aff25a42d50654c` | 123 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD refs/heads/main refs/remotes/origin/main` |
| log1 | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `b692df0b075ad195dff9455626155bf903675d5394fcd21128fd53b9fd853c4c` | 367 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log -1 --format=hash=%H%nparents=%P%nsubject=%s%nauthor=%an <%ae>%ncommitter=%cn <%ce>%nauthor_date=%aI%ncommit_date=%cI` |
| log_freeze | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `84026be9b4489b3d60c0e57e8fb0ecf93c816813cc0ec699262bd11dd11d4a9c` | 291 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H %cI %s -5 -- plans/round-47-claims.md tools/round-47` |
| names_new | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `ff22296f1166288dee30de63da538834fd27c6a8709ae8471f010c07a8b3a199` | 162 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r 3186f69b49798f2cc05727bbfd1604505fcee03b HEAD` |
| wt_vs_head | 2026-10-28T17:51:17Z | 2026-10-28T17:51:17Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet HEAD -- plans/round-47-claims.md tools/round-47` |
| check_pyc | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `3f4f5d9b31edaeee782c5a22fe523dfe8a3202e2e4c55a2202df40968fbae105` | 204 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin check-ignore -v -- tools/round-47/__pycache__ tools/round-47/__pycache__/exact.cpython-314.pyc tools/round-47/__pycache__/record.cpython-314.pyc` |
| head_post | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `b9eaff9d411b5b6cb7ec14270b30e4891c83d8f24c53ef6535cc1ac5256b9b56` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` |
| jj_post | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `7e41905b68a2bc5a745d70538a06789812dc244870473fa4e6c5a8481b52d67c` | 167 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| log_post | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `32af23607bf46f7382deb11d44a3e4754fc0a34f9df12ef7a38fd94b1a7484dc` | 455 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log -3 --format=%H %cI %s` |
| ls_pyc | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `30b4a92dd897fc60707daf03d277147724da43853ebbd5f4cb1378d621945242` | 99 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-files -o -i --exclude-standard -- tools/round-47` |
| numstat_tracked | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `43e233d7673951788b3fcaeddf23cfca1cd39f509c3cf52d23719fd5f51151fd` | 305 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --numstat` |
| por_post | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `75dc4a50d084814d8c993f0c1faaec3002b4299dc0cb51fbe732a27567de38f3` | 5693 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| por_post_all | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `90c1086d47c6faf95c5f3e8657bb952f74c797c5729765780b43c4c730e1ff1d` | 11726 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain=v1 -uall --untracked-files=all` |
| quiet_a1_head | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 9018c53b16503c8d06d398b75503406508119946 HEAD -- plans/round-47-claims.md tools/round-47` |
| quiet_freeze_a1 | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 5017e1f7299c3a812e87e7950148f54313dd279e 9018c53b16503c8d06d398b75503406508119946 -- plans/round-47-claims.md tools/round-47` |
| rederive | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `b9eaff9d411b5b6cb7ec14270b30e4891c83d8f24c53ef6535cc1ac5256b9b56` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H -1 -- plans/round-47-claims.md` |
| split_a1 | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `3ca39e1e92f344c2708a1e1ca07a78f6f0c4a1343fa8aeb7c853b60b2ca8b91e` | 116 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r 3186f69b49798f2cc05727bbfd1604505fcee03b 9018c53b16503c8d06d398b75503406508119946` |
| split_land | 2026-10-28T17:51:51Z | 2026-10-28T17:51:51Z | 0 | `4244d71f32777ed11c848034a6d6c6e8f7bae82d8315d21944e03fcae954abda` | 100 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r 9018c53b16503c8d06d398b75503406508119946 HEAD` |
| a2_frozen_diff | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `bd45d564572e532349832cacdd3391c786f00ef8fbe9d15e9e8ea1327b12d50c` | 2653 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff e856beb552080c03ede6000b96f1b58bde44c421 HEAD -- plans/round-47-claims.md tools/round-47` |
| a2_frozen_stat | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `51d390959c2bdeda7b745b1468b4d1a87010d17fbc993f5e4768885c1b349e73` | 130 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat e856beb552080c03ede6000b96f1b58bde44c421 HEAD -- plans/round-47-claims.md tools/round-47` |
| a2_names | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `a0325db7a655448dc6ec357d376d35d9e5b8f2d0eaa6fcca96847034cc34bc42` | 65 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r e856beb552080c03ede6000b96f1b58bde44c421 HEAD` |
| cached_post | 2026-10-28T17:52:13Z | 2026-10-28T17:52:14Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --cached --name-only` |
| exact_same | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 5017e1f7299c3a812e87e7950148f54313dd279e HEAD -- tools/round-47/exact.py` |
| freeze_to_head_stat | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `18b107e5eb5eed4aec41e7807734ab33b32b9481bdc0054ac01a3ded1fedb90d` | 152 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 5017e1f7299c3a812e87e7950148f54313dd279e HEAD -- plans/round-47-claims.md tools/round-47` |
| head_a2 | 2026-10-28T17:52:13Z | 2026-10-28T17:52:13Z | 0 | `b9eaff9d411b5b6cb7ec14270b30e4891c83d8f24c53ef6535cc1ac5256b9b56` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` |
| wt_frozen | 2026-10-28T17:52:14Z | 2026-10-28T17:52:14Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet HEAD -- plans/round-47-claims.md tools/round-47` |
| land_frozen | 2026-10-28T17:53:24Z | 2026-10-28T17:53:24Z | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 9018c53b16503c8d06d398b75503406508119946 e856beb552080c03ede6000b96f1b58bde44c421 -- plans/round-47-claims.md tools/round-47` |
| land_names | 2026-10-28T17:53:24Z | 2026-10-28T17:53:24Z | 0 | `09daec5e0c64aeb6fa8a7612828c3665512cafe242bd9d5629d937e93b60123a` | 46 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r 9018c53b16503c8d06d398b75503406508119946 e856beb552080c03ede6000b96f1b58bde44c421` |
| head_last | 2026-10-28T17:53:25Z | 2026-10-28T17:53:25Z | 0 | `1759e693c8f1090a7130cbba2885b2b67393f4279a679a4f21e069c021c4db14` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` |
| frozen_late | 2026-10-28T17:53:37Z | 2026-10-28T17:53:37Z | 0 | `1e33f01ca5492f233e0f400e5531c20b33a2c4acd0d1060aff43715c11322014` | 99 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat 62e33f7dd75c8e3285967b26419842c106f6c965 HEAD -- plans/round-47-claims.md tools/round-47` |
| jj_late | 2026-10-28T17:53:37Z | 2026-10-28T17:53:37Z | 0 | `b5721d5cd0b13800c678afcdac5ce79f308052ee11892e50710ea92f28af4313` | 168 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| log_late | 2026-10-28T17:53:37Z | 2026-10-28T17:53:37Z | 0 | `f57cbf7305bf7f9f4e52ee8d2b98455385609bbf89c339f97eb03beba24b6c32` | 192 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log -1 --format=%H%n%P%n%cI%n%s HEAD` |
| names_late | 2026-10-28T17:53:37Z | 2026-10-28T17:53:37Z | 0 | `a3f5e288d54c67ca4601d53473d49e77047d73bc655652153e6ac14c458521bc` | 27 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --name-status -r 62e33f7dd75c8e3285967b26419842c106f6c965 HEAD` |
| por_late | 2026-10-28T17:53:37Z | 2026-10-28T17:53:37Z | 0 | `8f8557cb029e0625c184dc6af0e14910c1f45ef14f8fc8a1693ea1c76274641d` | 6174 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| head_write | 2026-10-28T17:53:48Z | 2026-10-28T17:53:48Z | 0 | `1759e693c8f1090a7130cbba2885b2b67393f4279a679a4f21e069c021c4db14` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD` |
| log_span | 2026-10-28T17:53:48Z | 2026-10-28T17:53:48Z | 0 | `f78be6c7cbad424dcee067ad50f1d77f8ad1b30991e4f81229a6f7991d453252` | 314 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H %cI %s 62e33f7dd75c8e3285967b26419842c106f6c965..HEAD` |
| rederive_late | 2026-10-28T17:53:48Z | 2026-10-28T17:53:48Z | 0 | `b9eaff9d411b5b6cb7ec14270b30e4891c83d8f24c53ef6535cc1ac5256b9b56` | 41 | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H -1 -- plans/round-47-claims.md` |
