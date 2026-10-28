# ScoutState

Lane working state, read-only. Full command table and the `-uall` path inventory: `.ufo/waves/round-47/w1/ScoutState/report.md`. Receipts: `.ufo/waves/round-47/w1/ScoutState/receipts/`. Nothing deleted. No install. `exact.py` and `record.py` were not executed.

## Cited snapshot (2026-10-28T17:51:51Z)

`jj-lane.sh state` exit 0, stdout sha256 `7e41905b68a2bc5a745d70538a06789812dc244870473fa4e6c5a8481b52d67c`:

```
state branch=main local=62e33f7dd75c8e3285967b26419842c106f6c965 remote=e856beb552080c03ede6000b96f1b58bde44c421 ahead=1 behind=0 head=detached tracked=5 untracked=98
```

HEAD is detached (`symbolic-ref -q HEAD` exit 1, empty stdout, 17:49:52Z). The helper's `tracked`/`untracked` are default `git status --porcelain`, not `-uall`.

| porcelain | lines | sha256 | round-45 | round-46 | round-47 | other |
|---|---:|---|---:|---:|---:|---:|
| `git status --porcelain` | 103 | `75dc4a50d084814d8c993f0c1faaec3002b4299dc0cb51fbe732a27567de38f3` | 8 (2 ` M` + 6 `??`) | 74 (3 ` M` + 71 `??`) | 21 `??` | 0 |
| `-uall` | 192 | `90c1086d47c6faf95c5f3e8657bb952f74c797c5729765780b43c4c730e1ff1d` | 8 | 158 | 26 | 0 |

All 103 default lines are under `.ufo`. Index empty (`diff --cached --name-only`, 17:52:13Z, exit 0, empty). `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`, and `tools/round-47/` were clean at this instant.

## `__pycache__` is ignored

`git check-ignore -v` exit 0 (17:51:51Z, stdout sha256 `3f4f5d9b31edaeee782c5a22fe523dfe8a3202e2e4c55a2202df40968fbae105`): rule `.gitignore:1:__pycache__/`. On disk and ignored, not in porcelain: `tools/round-47/__pycache__/exact.cpython-314.pyc`, `tools/round-47/__pycache__/record.cpython-314.pyc`.

## Inherited uncommitted paths

**This round (26 `-uall` files, all `??`).** `.ufo/waves/round-47/l1/scores/c1-at-L1.json`, `c2-at-L1.json`, `w1.ready`, `w1.ready.partial`, and seat receipts under `w1/` (`C1Battery`, `C1Digest`, `C1Ids` ×2, `C1Order`, `C1Refs`, `C1Struct`, `C1Tokens`, `C2Atoms` ×2, `C2Corrections`, `C2Mismatch`, `C2Vacuity`, `RevC2Axes`, `RevC2Before`, `RevC2Dispatch`, `ScoutAxes`, `ScribeAxesRow` ×2, `ScribeCorrections`, `ScribeLesson` ×2).

**Earlier rounds (still dirty).** Round 45: 2 tracked + 6 untracked. Round 46: 3 tracked + 155 untracked. Tracked numstat (exit 0, sha256 `43e233d7673951788b3fcaeddf23cfca1cd39f509c3cf52d23719fd5f51151fd`): `R45W2Immutable/G-final-tip.txt` 10/0, `R45W2Immutable/report.md` 63/19, `R46W1MutC1Checks/receipts/manifest.txt` 16/3, `R46W1MutC1Checks/report.md` 50/13, `R46W1SimplInstruments/receipts/runs.jsonl` 4/0. Names: `receipts/classified-post.txt`.

`SKILL.md`, `SCORECARD.md`, and `corpus/SOURCES.md` were uncommitted landing drafts against `3186f69b` at 17:49:52Z and were committed by `e856beb5` (`diff-tree` names only those three; frozen stat empty). They are not inherited dirt at the cited snapshot.

## The prompt freeze is an ancestor, not the frozen tip

`5017e1f7299c3a812e87e7950148f54313dd279e` is an ancestor of every HEAD observed (`merge-base --is-ancestor` exit 0). `git log --format=%H -1 -- plans/round-47-claims.md` printed `5017e1f` at 17:50:22Z and `62e33f7dd75c8e3285967b26419842c106f6c965` at 17:51:51Z and again at 17:53:37Z. `exact.py` blob is unchanged from the prompt freeze (`diff --quiet 5017e1f HEAD -- tools/round-47/exact.py` exit 0 at 17:52:13Z; absent from later name-status). `plans/round-47-claims.md` and `tools/round-47/record.py` are not.

| commit | subject | frozen paths |
|---|---|---|
| `9018c53b` | A1 drop the unreachable window-pair clause | `M` claims.md, `M` record.py, plus `A` `controls/ctl-c2-2-freeze-amendment.json` |
| `e856beb5` | land block 24, corrections, axis heads, S143 | none (`9018c53b..e856beb5` frozen stat empty) |
| `62e33f7d` | A2 window forgery; arm cells carry only the token | `M` claims.md, `M` record.py (also `M` `SKILL.md`, not frozen) |
| `2e4ae434` | A3 seats/window correction for an older round | not diffed alone |
| `1e2c3102` | A4 historical-correction selftest fixture | net `62e33f7d..1e2c3102` is `M` record.py only (+14/−3) |

At 17:50:35Z, before A1, the worktree `record.py` blob was already `79fb27a8` while HEAD and `5017e1f` were `1f8e7928` (` M tools/round-47/record.py`). That dirt was committed as A1, not left behind.

A2's paragraph says the battery change is not a clause and that every clause is byte-identical to A1. The `e856beb5..62e33f7d` diff of `record.py` is not empty: `run_battery` forges `empty in <root>..<rev>` instead of `empty in <captured>..<rev>`.

## Both counters do not exit 2 on a frozen-path change

Source only (counters not run). `exact.py` `evaluate` calls `gate.freeze_state` and returns 2 when it does. `gate.py` `freeze_state` returns 2 `frozen_worktree_dirty` or 2 `frozen_path_changed`. `record.py` `evaluate` never calls `freeze_state` and the file has no `frozen_path_changed` string. The claims sentence that a post-freeze change makes both counters exit 2 `frozen_path_changed` is false for `record.py`.

Inference, not a run: `exact.py --freeze 5017e1f --rev 62e33f7d` (and `--rev 1e2c3102`) would be exit 2 `frozen_path_changed`, because those commits change `record.py` / claims bytes and the worktree matched HEAD at 17:52:14Z.

## After the inventory

17:53:37Z, HEAD `1e2c3102`, local=remote, ahead=0, `tracked=5 untracked=110`. Default porcelain 115 versus 103: twelve new `??` round-47 directories (`C1FreezeWindow`, `CritC1Sizing`, `RevC1Before`, `ScoutCraftTail`, `ScoutDispatch`, `ScoutRounds`, `ScoutState`, `ScoutTools`, `ScribeBlock24`, `ScribeQuality`, `ScribeReport`, `ScribeShonen`). No earlier-round path disappeared. `-uall` was not re-expanded. This report's own files landed inside `ScoutState/` after that porcelain line.
