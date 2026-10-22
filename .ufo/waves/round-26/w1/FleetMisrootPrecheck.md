# Fleet-root misroot precheck (round 26, wave 1)

Item: baseline for the round-26 misroot sweep. Scope: fleet root
`/home/vgpnk/Projects/shokunin` only. Lane repo untouched except this file.

Baseline instant: **2026-10-22T12:12:58Z**. Fleet HEAD `a20e701ece1c9c8ea6d8d87db1b800947501f88f`
(committed 2026-10-22T09:08:07-03:00 = 12:08:07Z), `.git/index` mtime 12:08:07Z.
Round 26 launch line (fleet `.ufo/watchdog.log`): `2026-10-22T08:54:45-03:00 launch kaidoku round=26 pgid=1976991 driver=hyaku-inline attempt=1`
= 11:54:45Z. Everything below is compared against that launch time.

## Command and stability

- Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only), exit 0, run at
  **2026-10-22T12:11:59Z** and again with `-uall` at **2026-10-22T12:12:58Z**.
- Both runs byte identical: `git status --porcelain -uall | sha256sum` =
  `5667f088f37c717a3fc33d371c4c09125bd51fe713147858e72416ec162e474d` (observation).
- 19 porcelain records; 18 files plus one untracked file expanded from a collapsed untracked dir.
- mtimes read with `date -u -r <path>` / `stat`; all times below are UTC.

## A. Modified or staged paths (15)

| status | path | mtime (UTC) | size |
|---|---|---|---|
| A | .scratch/goal-20261022-hyaku-12h.md | 2026-10-22T07:54:00Z | 17367 |
| M | .ufo/state/chousa.report-baseline | 2026-10-21T23:38:09Z | 68 |
| M | .ufo/state/kagi.report-baseline | 2026-10-21T17:32:03Z | 68 |
| M | **.ufo/state/kaidoku.report-baseline** | **2026-10-22T11:54:44Z** | 68 |
| M | .ufo/state/kake.report-baseline | 2026-10-22T11:45:33Z | 68 |
| M | .ufo/state/kama.report-baseline | 2026-10-22T09:19:50Z | 68 |
| M | .ufo/state/kengaku.report-baseline | 2026-10-21T17:32:03Z | 68 |
| A | .ufo/state/kotoba.report-baseline | 2026-10-22T09:30:26Z | 68 |
| A | .ufo/state/kotodama.report-baseline | 2026-10-22T10:32:12Z | 68 |
| M | .ufo/state/kumitate.report-baseline | 2026-10-22T09:43:13Z | 68 |
| M | .ufo/state/mado.report-baseline | 2026-10-22T10:43:09Z | 68 |
| M | .ufo/state/mori.report-baseline | 2026-10-22T09:42:02Z | 68 |
| A | .ufo/state/revenger.report-baseline | 2026-10-21T17:54:50Z | 68 |
| M | .ufo/state/tameshi.report-baseline | 2026-10-22T12:07:31Z | 68 |
| M | .ufo/state/tsukuroi.report-baseline | 2026-10-22T09:59:28Z | 68 |
| M | **.ufo/watchdog.log** | **2026-10-22T12:07:33Z** | 56091 |
| A | scripts/hyaku/__pycache__/append-closure.cpython-314.pyc | 2026-10-22T08:01:42Z | 10738 |
| A | **write** | **2026-10-21T22:52:50Z** | 25 |

(That table is 18 rows; the 19th record is the untracked file in section B.)

## B. Untracked path (1, from `-uall`)

- `.ufo/waves/round-49/falsify/RowGameDev2d.md` — mtime 2026-10-22T11:38:25Z, 13630 B,
  sha256 `37aaa836a5d650b658484cf99d3722acff55cd569a7410a36c588d60aaedce99`.
  The bare command shows only `?? .ufo/waves/round-49/` (collapsed dir).

## C. Paths that already name kaidoku or round 26

- `.ufo/state/kaidoku.report-baseline` — name names kaidoku; content `26 e3b0c442...b855`,
  i.e. the round 26 marker with the empty-string sha256. mtime **11:54:44Z**, one second before
  the round-26 launch line at 11:54:45Z (observation). This is the fleet root's normal per-round
  marker write, not a misroot; record it so later diffing does not mistake it for drift.
- `.ufo/watchdog.log` — path names no lane, but its bytes contain the line
  `2026-10-22T08:54:45-03:00 launch kaidoku round=26 pgid=1976991 driver=hyaku-inline attempt=1`;
  mtime 12:07:33Z, the tameshi r27 launch line (observation).
- No other status path names kaidoku or round 26. `find . -iname '*round*26*'` at the fleet root
  finds only tracked fleet surfaces: `.ufo/reports/round-26/` (8 tracked files: chousa, kagi,
  kake, kengaku x3, kotodama, tameshi), `.ufo/prompts/{closure/,}*round-26.md`, and the lane
  directories themselves (e.g. `kaidoku-shokunin/.ufo/waves/round-26`). Fleet root has **no**
  `.ufo/waves/round-26` (absent, observation).

## D. Misroot fingerprints present but invisible to `git status`

These are ignored or empty, so the required command cannot see them. All predate the round-26
launch; listed so the sweep does not re-attribute them to this round.

| path (literal name) | mtime (UTC) | note |
|---|---|---|
| `write` (regular file, staged A) | 2026-10-21T22:52:50Z | content is exactly `agent://U100N079H334f935b` (25 B), sha256 `95443b228053f4522714b3ba9cdb56cbce2e2c43b43b073b56e2c70978e0bac0`; a tool-URL written as a filesystem path |
| `bash: /home/vgpnk/Projects/shokunin/souji-shokunin` (directory; name contains colon, space, trailing part) | 2026-10-18T17:01:47Z | contains `tests/tools`; ignored via `.gitignore:1:*-shokunin/` (check-ignore -v proof) |
| `tameshi-shokukin/` (typo of lane name) | 2026-10-21T05:50:33Z | contains `tameshi-shokunin/.ufo`; not ignored, but empty of files so git never reports it |
| `mori-shokukin/` (typo of lane name) | 2026-10-21T12:53:32Z | contains `.ufo` only; not ignored, no files |
| `reports/` | 2026-10-18T16:05:53Z | empty directory at fleet root; fleet convention is `.ufo/reports/` |
| `local/fleet-analysis/` | (empty) | empty directory |

`kaidoku-shokunin/` itself is ignored (`!! kaidoku-shokunin/`, matched by `.gitignore:1`),
so no lane file can ever appear in this status output; the sweep must look for lane-shaped
content under non-ignored fleet paths (`.ufo/waves/round-*`, `tools/`, `corpus/`, root files).

Also flagged, in-round but expected: `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc`
is staged (`A`) although `__pycache__` is not in `.gitignore` (check-ignore: NOT-IGNORED);
mtime 08:01:42Z, i.e. 3h53m before launch, so pre-round, but it is a build artifact that a
future commit would carry.

## E. Verdict

- Observation: the round-26 window opened with the fleet root carrying one lane-shaped misroot
  candidate, `.ufo/waves/round-49/falsify/RowGameDev2d.md` (kotoba round 49, arrived 11:38:25Z,
  16 minutes before the round-26 launch). Its filename names kotoba, not kaidoku or round 26.
  It has **no** twin in `kotoba-shokunin` (`find kotoba-shokunin -name RowGameDev2d.md` returns
  nothing), while `kotoba-shokunin/.ufo/waves/round-49/build/` does exist (observation).
  Inference: it is a kotoba seat report written to the fleet root instead of the kotoba lane.
  Unknown: which tool path produced it; no writer record was consulted.
- Inference: the same class of failure already left four older root-level fingerprints
  (`write`, `bash: ...`, `tameshi-shokukin/`, `mori-shokukin/`), none of them from this round.
- Unknown: whether `.ufo/state/*.report-baseline` churn and `.ufo/watchdog.log` writes are the
  expected fleet bookkeeping (they look periodic and match watchdog lines) or drift; not judged.

## F. Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/FleetMisrootPrecheck/)

| file | sha256 |
|---|---|
| porcelain.txt (raw `git status --porcelain -uall`, 2026-10-22T12:12:58Z) | `5667f088f37c717a3fc33d371c4c09125bd51fe713147858e72416ec162e474d` |
| status-baseline.tsv (status, mtime, size, path; one row per record) | `aaf840b29cf2335f3520fa6963a1734e849ee2807a732cb77938f08fa63b95d7` |
| status-run-utc.txt (run timestamp, content `2026-10-22T12:12:39Z`) | `3b6cd2ee212e03cfaf754fd011b43d85bbcddb36e1a23b0dae2742a6eb9bb85f` |

All three hashes are verbatim `sha256sum` output from this session (exit 0). No tools installed
or upgraded; no files mutated outside this lane report path and the scratch directory.
