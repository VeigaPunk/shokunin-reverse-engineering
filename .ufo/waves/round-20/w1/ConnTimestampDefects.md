# ConnTimestampDefects — fleet future-dated evidence timestamps

Seat: ConnTimestampDefects. Read-only. No tool installed. Clock at write: `2026-10-20T17:50:47-03:00` (`date -Iseconds`, exit 0). Axes: calibration, coverage, depth.

`W20/tools/evidence-timestamps.py` is absent (`test -e` exit 0, printed `ABSENT`). Grammar claims below are readings of the frozen D2 pattern, not a tool run.

## Commands

From `/home/vgpnk/Projects/shokunin`:

```
grep -ril 'future-dated\|future dated' */corpus/lessons
```

Exit 2. Cause observed: the glob also names fleet-root files and directories with no `corpus/lessons` (`Not a directory` / `No such file`). Hits before the errors:

- `audio-shokunin/corpus/lessons/round-101.md`
- `game-dev-3d-shokunin/corpus/lessons/round-108.md`
- `kaidoku-shokunin/corpus/lessons/round-19-verifier-spotcheck.md`
- `kake-shokunin/corpus/lessons/round-6-aggregator-audit.md`
- `kake-shokunin/corpus/lessons/round-7.md`
- `kama-shokunin/corpus/lessons/round-16-verifier-spotcheck.md`
- `mori-shokunin/corpus/lessons/round-16-verifier-spotcheck.md`
- `tabi-shokunin/corpus/lessons/round-17-verifier-spotcheck.md`

```
grep -ril 'future-dated\|future dated' .ufo/reports
```

Exit 0. Six files: `AGGREGATE.md`, `round-10/protocol.md`, `round-108/game-dev-3d.md`, `round-19/kaidoku.md`, `round-8/protocol.md`, `round-9/protocol.md`.

```
find -L . -mindepth 3 -maxdepth 4 -type d -path '*/corpus/lessons' -print0 | xargs -0 grep -ril -E 'future-dated|future dated'
```

Exit 0. Twenty-one lesson directories. Same eight files as the first command. No ninth lesson hit.

Read-only git (exit 0 unless noted):

- `git -C kaidoku-shokunin log -1 --format='%cI' 4f6c73f` → `2026-10-20T16:09:17-03:00`
- `git -C kaidoku-shokunin blame -L 36,36 --porcelain 14f0260ad319ecc26994381b2415d5a999003375 -- .ufo/waves/round-19/claims.json` → introducing commit `4f6c73f`, committer-time `1792523357` = `2026-10-20T16:09:17-03:00` (`date -d @1792523357`, exit 0). Line text is the `16:20:00-03:00` amendment.
- `git blame -L 44,45` at the same rev → `b26a6c4`; `git log -1 --format='%cI' b26a6c4` → `2026-10-20T16:46:03-03:00`
- `git -C kake-shokunin log -1 --format='%cI' 9544914` → `2026-09-28T16:49:59-03:00` (19:49:59Z)
- `git -C kake-shokunin log -1 --format='%cI' 83d08e4` → `2026-09-28T16:39:21-03:00` (19:39:21Z)
- audio `SCORECARD.md:738` blame `1ba81039` → `2026-10-14T12:17:40-03:00`; `:748` blame `49747ba1` → `2026-10-14T12:51:23-03:00`
- audio `ports/frontier/fb-pipewire.md:3` blame `c079abaf` → `2026-10-14T11:16:08-03:00`
- game-dev-3d `SCORECARD.md:109` blame `31cf56a6` → `2026-10-14T12:12:42-03:00`; `:119` blame `f8a088c5` → `2026-10-14T13:01:29-03:00`
- `PROTOCOL.md:359` blame `6bd4f388` → `2026-09-28T20:15:40-03:00`

`/tmp` mtimes cited by kake (`19:46Z`, `19:35Z`) were not re-measured. Those files are absent in the later kake headers.

## Mechanisms

### 1. Kaidoku — keep the instant, withdraw it, judge the introducing line

Observation. `.ufo/waves/round-19/claims.json:36` still asserts `2026-10-20T16:20:00-03:00`. That line was introduced by `4f6c73f` at `16:09:17-03`, so the token is 10m43s after its shipping commit. `:44-45` (commit `b26a6c4` at `16:46:03-03`) supersedes `amendments[0].at` only and says to use Git chronology, not the withdrawn timestamp. Blame at baseline `14f0260` still attributes line 36 to `4f6c73f`; the withdrawal did not rewrite it.

`corpus/lessons/round-19-verifier-spotcheck.md:100-103` calls this a §Evidence-standard conformance defect (D2) and status-neutral for C3 because `predictions/decision-rule.json` did not change after outcomes. `:182-183` leaves the fix open: timestamps must be at or before the shipping commit. `.ufo/reports/round-19/kaidoku.md:123` records the same withdrawal. Round-20 contract `:33-34` forbids writing a future or estimated instant; `:41-45` defines the checker as per-line `git blame` against a zoned timestamp. `gen-wave1.py:94-100` requires red-before on `claims.json:36` at baseline, no quotation exemption, and `--allow FILE:LINE` as the only skip. `claims.json` round-20 `:6` puts no timestamp in the declaration file.

### 2. Kake — detect against the shipping commit; prescribed repair never landed

Observation. `corpus/lessons/round-6-aggregator-audit.md:84-92` and `:131-132`: `~21:15Z` in `kimi-subpath-audit.md` and `lessons/round-8.md:4`, shipped in `9544914` at 19:49:59Z (re-measured `16:49:59-03`); `~20:20Z` in `sitemap-orphan-audit.md:3,62` and `lessons/round-7.md:4`, shipped in `83d08e4` at 19:39:21Z (re-measured `16:39:21-03`). The audit bounds the runs by `/tmp` mtimes and requires appended real-UTC entries, never a silent edit.

Those labels are still the text. `corpus/knowledge/kimi-subpath-audit.md:1-2,7` and `sitemap-orphan-audit.md:2,6,66` repeat `~21:15Z` / `~20:20Z` inside later `source:` / `verified-at:` headers (`historical-not-live-reverified`). `corpus/lessons/round-7.md:82` says the gate does not correct the label. `.ufo/waves/round-21/w1/GateTruth.md:111` and `PriorGates.md:133,143` still call both findings open. Fleet ledger: `.ufo/reports/AGGREGATE.md:691` (D-24 OPEN, second instance → D-67), `:725` (D-67 OPEN, same append-real-UTC form), `:754`. `.ufo/reports/round-10/protocol.md:208` D-24 OPEN at `dd4eabf`. `.ufo/reports/round-8/protocol.md:75` and `round-9/protocol.md:33,131` list the class; `:70-71` states the conformance sentence. No later AGGREGATE row closes D-24 or D-67 (pattern search of that file returned only those three lines).

### 3. Audio and game-dev-3d — date-only headers left in place; forward rule only

Observation. Audio `corpus/lessons/round-101.md:16` (M10 → Q13): `SCORECARD.md:738,748` date rounds 73/74 `2026-11-01`; `ports/frontier/fb-pipewire.md:3-4` uses that date as the measurement date. The wave path on `:4` is `shokunin-train-20261101-w10`. Re-measured introducing commits are all `2026-10-14` (`1ba81039` 12:17:40-03, `49747ba1` 12:51:23-03, `c079abaf` 11:16:08-03). `corpus/QUALITY.md:21` Q13: observation date, not a planned wave date. No SCORECARD note retracts the headers; they still read `2026-11-01`.

Game-dev-3d `corpus/lessons/round-108.md:25` (M17 → Q16): `SCORECARD.md:109,119` date r81/r82 `2026-11-01`. Introducing commits `31cf56a6` `2026-10-14T12:12:42-03:00` and `f8a088c5` `2026-10-14T13:01:29-03:00`. `SCORECARD.md:389` keeps the dates and says to read them as recording errors. `corpus/lessons/round-108.md:82` says M17 stays open as a historical defect; this round's own records are the ones that pass. `corpus/QUALITY.md:27` Q16 compares each ISO date with the declared round date before landing. `.ufo/reports/round-108/game-dev-3d.md:19` names future-dated blocks as one mined class, not as a rewritten header.

### 4. Kama, mori, tabi — checks that passed, not repairs

Observation. These files match the search because they deny the defect.

- kama `corpus/lessons/round-16-verifier-spotcheck.md:86`: `recorded_utc` 14:13:02Z is between predecessor `726f737` (14:10:32Z) and shipping `ccc4bb3` (14:15:00Z).
- mori `corpus/lessons/round-16-verifier-spotcheck.md:50-53`: each receipt `started_at` precedes the commit that first adds that receipt.
- tabi `corpus/lessons/round-17-verifier-spotcheck.md:71`: `generatedAt` 13:49:59-03 precedes `6c97851` (14:06:25-03) and M (14:44:26-03).

### 5. Protocol sentence (outside the assigned grep)

Observation, follow-on from the round-9 report's citation, not a `grep -ril` hit. `PROTOCOL.md:358-360`: a timestamp on evidence must be at or before the commit that ships it. `PROTOCOL-APPENDIX.md:28` names kake's `~21:15Z` (~46 min ahead) as the instance. The sentence names no checker.

## Move

Instantiate D2 selftest `future_line_flagged` / `later_commit_line_uses_own_time` as the kaidoku two-commit shape, not as one commit and not as kama's bracket.

At rev `b26a6c4` (and at baseline `14f0260`), line 36's token `16:20:00-03` is after the introducing committer time `16:09:17-03` and before the withdrawal commit `16:46:03-03`. A comparison against the file's latest commit, or kama's "between predecessor and shipping commit" (`round-16-verifier-spotcheck.md:86`) with the upper bound set to `b26a6c4`, classifies that line as not future-dated. Per-line blame does not. The withdrawal sentence is not an exemption; `gen-wave1.py:97-98` allows only `--allow`, and red-before must still emit `future_dated` for `.ufo/waves/round-19/claims.json:36`.

Do not repair by appending an mtime-derived "real UTC" (kake `:91-92`). That writes an estimated instant, which contract `:33-34` forbids, and kake's own later headers copied the bad token instead. Do not rewrite line 36: the red-before specimen is the baseline blob.

Out of the frozen grammar at contract `:42-44` (inference: the tool was not run): `~21:15Z` / `~20:20Z`, and date-only `2026-11-01`. Selftest cases for those strings should expect no finding, so a green D2 run is not reported as closing D-24, D-67, audio M10, or game-dev-3d M17. Widening the grammar to catch them would change the interface the counter relies on (contract `:36`).

## Risks

- A single-commit fixture hides the false-clean. The withdrawal commit is the case that makes it.
- `--allow` on `claims.json:36` would zero the red-before the writer is required to paste.
- Treating PROTOCOL.md:359 as already satisfied by D2 over-claims coverage: the sentence was motivated by kake's tilde clock, which the frozen pattern does not match.

## Verification for the fixing seat

At `14f0260`, blame line 36 → `4f6c73f` `16:09:17-03`, line 45 → `b26a6c4` `16:46:03-03`. `evidence-timestamps.py --rev 14f0260 --path .ufo/waves/round-19` must report `future_dated` on `claims.json:36` and must not do so merely because a whole-file committer time is after `16:20`. A fixture line `~21:15Z` and a fixture line `2026-11-01` must not be findings. No `--allow` entry for line 36 on that red-before.
