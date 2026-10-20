HOLDS (clean for kaidoku; one cross-lane content match, listed)

# MisrootSweepW1 — round-19 wave 1: fleet-root untracked sweep

Seat KaidokuR19.MisrootSweepW1 · sweep at 2026-10-20T15:48:20-03:00 · Read-only.
Installs: none (git/grep/sha256sum/stat are preinstalled; no pacman, `uv`, or `npx` run).
No REA/Ghidra, no carrier execution, no subagents, no `jj`, no git writes. Sole write: this report.
Fleet HEAD `bb44c290cb4af797541e61267560bb87abd431e6` ("round-18: tsukuroi dispatch evidence
(hyaku inline attempt 1)", 15:38:14). Lane `refs/heads/main` = `85589ac757f9ca3cb25efcd702d0963e25c9c4df`,
one commit above baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (`merge-base --is-ancestor` EXIT=0).

## Target commands (pasted, with exit codes)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain              # EXIT=0, 11 lines
 M .ufo/watchdog.log
?? .ufo/reports/round-19/mado.md
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline

$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall       # EXIT=0, same 11 lines
# no collapsed untracked directories; empty directories are invisible to porcelain either way

$ cd /home/vgpnk/Projects/shokunin && grep -il kaidoku .ufo/reports/round-19/mado.md .ufo/state/*.report-baseline
# no output, EXIT=1  (zero content matches)

$ cd /home/vgpnk/Projects/shokunin && grep -il round-19 .ufo/reports/round-19/mado.md .ufo/state/*.report-baseline
.ufo/reports/round-19/mado.md                                          # EXIT=0

$ grep -c round-19 .ufo/reports/round-19/mado.md                       # 12, EXIT=0
$ grep -n round-19 .ufo/reports/round-19/mado.md                       # EXIT=0
20: .ufo/waves/round-19/anchor-durability.py ...       48: round-19 frozen baseline re-pinned
67: wave-1 integration ... round-19 checkers            68: tripwire merge ... round-19 frozen re-pin
83: C2 freshness ... round-19/fresh-pins.py             84: C3 operability ... round-19/tw-recall.py
87: .ufo/waves/round-19/receipt-claims.json             121: round-19.md § Gate
142: SKILL.md ... round-19 errata                       143: LOG round-19 entry
145: PROVINCE.md round-19 line                          157: at the fleet root `.ufo/waves/round-19/` ...

$ while IFS= read -r f; do echo "--- $f"; head -5 "$f"; echo "head_exit:$?"; done < <(git status --porcelain | grep '^??' | cut -c4-)
# EXIT=0 overall; head_exit:0 per file
--- .ufo/reports/round-19/mado.md
# mado — round 19 (hyaku phase 2, attempt 1)

Lane `mado-shokunin`, branch `master`. Baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` →
lane tip **`⟨TIP⟩`** (landed and pushed by `scripts/hyaku/jj-lane.sh`; `state …
local=remote=⟨TIP⟩ ahead=0 behind=0`). The lane VCS is jj-colocated, and every lane commit
--- .ufo/state/kaidoku.report-baseline
19 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/kake.report-baseline
21 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/kama.report-baseline
17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/mado.report-baseline
19 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/mori.report-baseline
17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/souji.report-baseline
17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/tabi.report-baseline
18 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/tameshi.report-baseline
17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
--- .ufo/state/tsukuroi.report-baseline
18 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

## Requested list

- Untracked files whose **content** names `kaidoku`: **none** (0/10; `grep -il` EXIT=1).
- Untracked files whose **content** names `round-19`: **one** — `.ufo/reports/round-19/mado.md`
  (12 matching lines, anchors above). Nothing was moved or deleted.
- Full untracked list with `head -5` each: the 10-file block above. The nine `.report-baseline`
  files are one line each (`<round> <sha256>`), so `head -5` renders the whole file.

## Findings (observation O / inference I)

- **F1 (O):** 11 porcelain lines = 1 tracked modification (`.ufo/watchdog.log`, ` M`) + 10 untracked
  files; 10 = 1 report + 9 driver baselines. No untracked directory entry exists (`-uall` identical).
- **F2 (O):** The only content match is another lane's live report, at the driver-canonical path
  `$FLEET/.ufo/reports/round-<N>/<lane>.md` (`scripts/shokunin-watchdog.sh:121`): 12,652 bytes,
  mtime 15:34:57, head unfinalized (`⟨TIP⟩` placeholders, mado.md:1-5). Its four siblings in that
  directory (`kagi.md`, `kake.md`, `kotoba.md`, `kotodama.md`) are tracked (`git ls-files` → 4);
  `mado.md` is the only uncommitted one and `kaidoku.md` is absent. It is not a kaidoku stray.
- **F3 (O):** All nine baselines are `<round> <sha256>` with digest
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` = `sha256("")`
  (`sha256sum /dev/null` EXIT=0), i.e. the named report did not exist at capture. Rounds:
  kaidoku 19, mado 19, kake 21, tabi 18, tsukuroi 18, kama/mori/souji/tameshi 17.
- **F4 (O, producer/rooting):** `.ufo/state/<lane>.report-baseline` at the fleet root is by design.
  `scripts/shokunin-watchdog.sh:31-32` documents the format; `report_digest` :108-118 hashes a missing
  report as the empty stream; `record_report_baseline` :120-138 writes `"$n $digest"` atomically
  (path :121-122, tmp+mv :127-136). The hyaku driver calls it at `scripts/hyaku/inline.sh:100`,
  immediately before the `launch … pgid=$$ driver=hyaku-inline` line at :103 (dispatch evidence is
  committed separately at :102). So neither path is misrooted; both are fleet-level driver state.
- **F5 (O, freshness cross-check):** each baseline's mtime lands 1-3 s before its launch line in
  `.ufo/watchdog.log`: kake 05:51:50→:468 05:51:51; kama 11:52:24→:484; tameshi 12:07:32→:485;
  souji 12:43:23→:493; mado 13:54:20→:495; mori 15:26:13→:499; kaidoku 15:28:56→:500 15:28:58;
  tabi 15:36:23→:501; tsukuroi 15:38:14→:502. The out-of-repo hyaku claim agrees:
  `~/.local/state/shokunin-hyaku/claims/kaidoku/{round,attempt,dispatched}` = `19`, `1`,
  `2026-10-20T15:28:56-03:00` (EXIT=0).
- **F6 (O):** The fleet root has **no** `.ufo/waves/round-19/` (`find` → `No such file or directory`).
  `.ufo/waves/round-17/w1/` and `.ufo/waves/round-21/w1/` exist as empty directories only (porcelain
  cannot show them). This matches mado.md:156-158 ("seat QualityDraft wrote two files at the fleet
  root `.ufo/waves/round-19/`; copied byte-exact into the lane … the fleet copies deleted (lesson M8);
  final fleet sweep clean") — the sweep result it cites is a no-file result.
- **F7 (O + I, sweep boundary):** fleet `.gitignore:1` is `*-shokunin/`
  (`git check-ignore -v kaidoku-shokunin` → `.gitignore:1:*-shokunin/	kaidoku-shokunin`, EXIT=0), so
  every lane tree is invisible to fleet `status`; and porcelain never lists empty directories.
  [I] Therefore "fleet sweep clean" is bounded to non-ignored, non-empty file paths at the fleet
  root and says nothing about any lane's working tree. Within the lane (read-only,
  `GIT_OPTIONAL_LOCKS=0 git --no-optional-locks … status --porcelain`, EXIT=0) the only untracked
  path is `?? .ufo/waves/round-19/w1/` — the intended w1 report/patch home. No lane-side kaidoku
  stray was observed at the fleet root by any route.
- **F8 (O + I, stale state, not a defect):** `.ufo/state/kaidoku.round` = `1`, `.mission` = `2685004`,
  both mtime 2026-10-15T01:50:57, matching `.ufo/watchdog.log:384`
  `launch kaidoku round=1 pid=2685004` (the pre-hyaku driver). `inline.sh` does not read these files;
  it takes round/attempt from `$HOME/.local/state/shokunin-hyaku/claims` (`inline.sh:19`, `:32`) = 19/1.
  [I] They are frozen watchdog-era state, not evidence of a relaunch and not a date for round 19.
- **F9 (O, adjacent, outside the untracked list):** the only version-controlled text that names
  kaidoku is the tracked-modified `.ufo/watchdog.log` (diff `28 insertions(+)`, 5 added lines matching
  `kaidoku|round-19`, `grep -c` EXIT=0): `:496 complete kaidoku round=18` and `:500 launch kaidoku
  round=19`. Driver bookkeeping, no seat content; log mtime 15:38:16.

## Unresolved / not swept

- Ignored paths were not enumerated (all `*-shokunin/` lane trees; out of target, and enumerating
  them would not change the file-level answer).
- The three lane files under `w1/` were not content-scanned (they are lane-internal, not part of the
  fleet-root target). `mado.md` was read only to locate the requested matches.
- No write beyond this report; no git/jj write; no process started.

Report: .ufo/waves/round-19/w1/MisrootSweepW1.md
