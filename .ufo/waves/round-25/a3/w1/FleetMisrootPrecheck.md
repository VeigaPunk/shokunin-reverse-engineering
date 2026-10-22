# FleetMisrootPrecheck — fleet-root files belonging to kaidoku round 25

Scope: `/home/vgpnk/Projects/shokunin` (fleet root), read-only. Lane and fleet repos untouched; no
jj, no git writes, no installs. Times UTC unless a `stat` line carries `-03:00`.
Labels: **observation** = command output; **inference** = my reading; **unknown** = not resolvable
from current state.

## Commands

| # | Command | Exit | UTC |
|---|---|---|---|
| 1 | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 0 | 2026-10-22T10:42:54Z |
| 2 | same, saved (18 lines) | 0 | 2026-10-22T10:45:24Z |
| 3 | `git status --porcelain -uall` count `^??`; `git ls-files --others --exclude-standard` | 0 | 2026-10-22T10:45:24Z |
| 5 | `git ls-files -s <candidates>`; `git diff --numstat` | 0 | 2026-10-22T10:45:12Z |
| 6 | `find .ufo/waves/round-25 -mindepth 1`; `stat`; `ls -la` | 0 | 2026-10-22T10:45:24Z |
| 7 | `strings -n 4 <pyc>`; `grep -n` excerpts; `grep -rl kaidoku` over fleet non-lane paths | 0 | 10:42–10:45Z |
| 8 | re-check `git status --porcelain` | 0 | 2026-10-22T10:48:29Z |

## Observation: the status set

Command 2 output, 18 lines, complete (command 1 had the same lines minus line 11 `mado`, which a
fleet process touched between the two runs; not a kaidoku path):

```
 A .scratch/goal-20261022-hyaku-12h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 A .ufo/state/kotoba.report-baseline
 A .ufo/state/kotodama.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 A .ufo/state/revenger.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
```

No `??` line: command 3 gave `0`, command 4 gave nothing (0 paths). **Observation:** the fleet root
has zero ordinary untracked files. The six ` A` entries are intent-to-add: command 5 shows each with
mode `100644` and blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (empty blob), while `git diff
--numstat` reports worktree content (`247 0` goal; `1 0` each new baseline; `1 0` `write`; `- -`
pyc). They are untracked in substance. This matches the fleet ledger's own note at
`.ufo/waves/hyaku/PHASE3.md:192` ("intent-to-add (` A`) entries for untracked files").

## Candidates (acceptance)

1. `.scratch/goal-20261022-hyaku-12h.md` — intent-to-add, 17,367 B, 247 lines, mtime
   `2026-10-22 04:54:00 -03`. Excerpts (`sed -n '86,87p;104p'`):
   - `2026-10-21/22 author; fresh attempt"`. This applies to kaidoku r25, kotoba r48, mori r24,`
   - `tameshi r25, tsukuroi r24, kake r28 and kotodama r51; all are at attempt 1, so the result is`
   - `| C6 | kaidoku (r25) | Healthy corpus (107 entries). Measured r25 work exists to re-verify and reuse. |`
   Verdict: **not misrooted.** It is the session-wide goal for eleven lanes, and
   `scripts/hyaku/lane-addendum.md:4` cites this exact path as the authoritative scope file.

2. `.ufo/waves/round-25/` — untracked empty directory (git cannot list empty directories).
   `find .ufo/waves/round-25 -mindepth 1` → one entry, `build/`; `find ... -type f` → 0 files;
   `build/` size 0, mtime `2026-10-21 04:32:22 -03`; parent mtime `2026-10-22 06:46:52 -03`
   (09:46:52Z).
   Verdict: **candidate marker, no content to cite.** The child predates kaidoku r25's launch
   (`2026-10-21T20:38:06-03`, `.ufo/watchdog.log:642`), so it is not a kaidoku-r25 artifact. The
   parent then changed during a3, which launched `09:19:48Z` (PHASE3 line 203); the added or
   removed entry is gone, so its content is **unknown**. Lane-relative outputs are absent:
   `.ufo/waves/round-25/a3` and `.ufo/reports/round-25/kaidoku.md` both do not exist.

3. `write` — intent-to-add, 25 B, mtime `2026-10-21 19:52:50 -03`; exact bytes
   `agent://U100N079H334f935b` (no newline).
   Verdict: **stray, not kaidoku round 25.** The id is at
   `.ufo/waves/hyaku/s3-unjoined100/dispatch.json:884` as `"kind": "spawn", "role": "scout"`, and
   that dispatch's payload at line 1532 carries `"lane": "kotodama"`. **Inference:** a seat of the
   non-kaidoku unjoined100 wave passed a message id as a file path named `write`.

4. `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` — intent-to-add, 10,738 B, mtime
   `2026-10-22 05:01:42 -03`. `strings -n 4` yields `append one closure entry to MANIFEST.json
   rounds[].` and `lanes must be {lane: lane_round}`; no `kaidoku` and no round-25 token.
   Verdict: **stray bytecode, not kaidoku round 25.**

5. `.ufo/state/kaidoku.report-baseline` — tracked, ` M`, one line `25 e3b0c442...`; `25` is a report
   byte count and only the path names kaidoku. Verdict: **legitimate fleet state**, written at
   06:19:46 -03, the same second as the a3 prompt.
## Tracked fleet-root files that name kaidoku round 25 (not misroots)
- `.ufo/prompts/kaidoku-round-25.md`, tracked, 26,237 B, mtime `2026-10-22 06:19:46 -03`; line 1:
  `You are the kaidoku L1, round 25. Working dir: /home/vgpnk/Projects/shokunin/kaidoku-shokunin.`
- `.ufo/waves/hyaku/PHASE3.md`, tracked; line 78 `Stale claim: kaidoku r25`; line 165
  `Dispatch kaidoku r25 attempt 2 (C6)`; line 203 `Dispatch kaidoku r25 attempt 3`.
- `.ufo/waves/hyaku/kaidoku25-prerequisite/`, 19 tracked files (`freeze-landing.json`,
  `measurement-authority.json`, ...), naming kaidoku lane paths and `/fast/scratch/hyaku/kaidoku-r25-*`.
- No fleet-root `corpus/`, `tools/`, `claims.json`, `carriers.tsv`, `c1-calibration.py` or
  `resolve-selectors.py` exists; a name search outside `kaidoku-shokunin` returned only other lanes'
  unrelated round-25 files and the ledgers above.
## Verdict

Attack: "earlier kaidoku round-25 seats left fleet-root files that belong to the lane."
- Files with readable content: **holds that none exist.** Zero ordinary untracked files; the only
  untracked content naming kaidoku r25 is the fleet-wide goal file, sited correctly.
- The transient in `.ufo/waves/round-25/`: **could-not-evaluate** — the directory is empty and the
  added or removed entry left no bytes; origin is not attributable from timestamps.
- Unknowns: who touched `.ufo/waves/round-25` at 09:46:52Z, and whether any fleet-root file was
  created and deleted before 10:42:54Z. Neither can name content now.

Nothing was moved, deleted, staged or modified at the fleet root or in the lane.
## Artifacts (sha256), `/fast/scratch/hyaku/kaidoku-r25-a3/seats/FleetMisrootPrecheck/`

```
3ee62a15426661a518f2bfd17ae4955291226cc65dfaead4a48ce70443578c84  status.txt
01d05cfa383b83912b04c95bf3494f6052fc720982c319f5d816749036ed0da0  status-final.txt
dce0b51f2af611326f5fbd990d22ba0773fbf3001dd59c6a26896e188aa978bf  untracked.txt
d659bf6654be60d1a5f0a28fd34cc84107c65675aeeff62eb9b7624d1b8c63b3  intent-to-add.txt
7ca1a8fdc2f21e6de412da527adc6514943d4fc96cb7e3f622eb1fc7571e2a1c  excerpts-and-times.txt
```

Tool installs/updates: none.
