# ScoutMisrootFleet — fleet-root untracked sweep (read-only)

Question: does any untracked file at the fleet root (`/home/vgpnk/Projects/shokunin`,
a repo distinct from this lane) have content naming `kaidoku` or `round-18`?

**Answer (observation): zero. 11 untracked files exist; `grep -lE 'kaidoku|round-18'`
matches none of them (grep exit 1). One untracked *filename* names kaidoku —
`.ufo/state/kaidoku.report-baseline` — and it is driver state whose content is
`18 <sha256-of-empty-stream>`, i.e. it names round `18`, not the string `round-18`.**
Nothing was deleted or modified.

## Commands and exit codes (verbatim)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/watchdog.log
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline
?? scripts/hyaku/jj-lane-selftest.sh.new
?? scripts/hyaku/jj-lane.sh.new
EXIT=0
```

```
$ files=$(git ls-files --others --exclude-standard) && grep -lE 'kaidoku|round-18' $files
grep-exit=1
files-tested=11
```

```
$ for p in kaidoku 'round-18' round18 'round 18' R18 hyaku wave; do
    git ls-files --others --exclude-standard -z | xargs -0 grep -licF "$p" ...
  done
kaidoku
round-18
round18
round 18
R18
hyaku      scripts/hyaku/jj-lane-selftest.sh.new scripts/hyaku/jj-lane.sh.new
wave       scripts/hyaku/jj-lane-selftest.sh.new
EXIT=0
```

```
$ git ls-files --others --exclude-standard | grep -E 'kaidoku|round-18'
.ufo/state/kaidoku.report-baseline
EXIT=0                     # filename match only
```

```
$ git status --porcelain -uall | cut -c4- | while read f; do grep -qE 'kaidoku|round-18' -- "$f" && echo "MATCH $f"; done
MATCH .ufo/watchdog.log
EXIT=0                     # the only status path with matching CONTENT is the tracked M file
```

```
$ git status --porcelain --ignored=matching -uall | cut -c1-2 | sort | uniq -c
     37 !!
     11 ??
      1  M
EXIT=0
```

## Observations

1. **Untracked set is drive-state plus orchestrator WIP, not lane artifacts.**
   The nine `.ufo/state/*.report-baseline` files are all 68 bytes, form
   `<round> <sha256>`; the sha is `e3b0c442…` (SHA-256 of the empty stream) in
   every one. Contract: `scripts/shokunin-watchdog.sh:31-32` ("holds `round SHA256`
   … captured immediately before launch") and `:121-138`
   (`record_report_baseline`, missing report hashed as the empty stream);
   `:47` pins `UFO="$SHOKUNIN_ROOT/.ufo"` (fleet root, not a lane).
   `/home/vgpnk/Projects/shokunin/.ufo/state/kaidoku.report-baseline:1` is
   exactly `18 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

2. **Kaidoku round-18 was launched from that baseline.** mtime of the baseline is
   `2026-10-20 12:07:52`; `.ufo/watchdog.log:486` records
   `2026-10-20T12:07:53-03:00 launch kaidoku round=18 pgid=4070059 driver=hyaku-inline`.
   The inline driver writes the baseline then logs the launch
   (`scripts/hyaku/inline.sh:97-103`). **Inference:** this is the driver's own
   round-18 state file, one second pre-launch — not a misrooted seat file.

3. **The actual report destination is the fleet root, and it is still absent.**
   `scripts/hyaku/inline.sh:109` sets `rep=".ufo/reports/round-$n/$lane.md"`;
   `scripts/hyaku/lane-addendum.md:105` and `:146-147` require the report at
   `{{FLEET_ROOT}}/.ufo/reports/round-<N>/<LANE>.md`, committed last.
   `.ufo/reports/round-18/` contains only `kasegi.md`, `kengaku.md`,
   `kotodama.md` — no `kaidoku.md`. `.ufo/reports/round-17/kaidoku.md` exists
   (14301 B, commit `7807afe`), so the convention is real. **Inference:** no
   kaidoku round-18 content has landed yet (lane still running); this is pending,
   not misrooted.

4. **The two `.new` scripts are fleet-orchestrator work, and they name neither
   kaidoku nor round-18.** `scripts/hyaku/jj-lane.sh.new:46` hardcodes
   `FLEET_ROOT_REAL=/home/vgpnk/Projects/shokunin`; `:4` says "shokunin lane repos";
   `scripts/hyaku/jj-lane-selftest.sh.new:7,18` default to `kake-shokunin`
   (`SRC=/home/vgpnk/Projects/shokunin/kake-shokunin`). Both differ from their
   tracked counterparts (`diff -q` exit 1 for each). This matches the prior
   classification in `.ufo/reports/round-17/mado.md:149-152` ("orchestrator files
   (`scripts/hyaku/jj-lane*.sh.new`); no … seat file at the fleet root").

5. **`kaidoku-shokunin/` is a nested repo and is ignored at the fleet root.**
   `git -C kaidoku-shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`;
   `git status --ignored` lists `!! kaidoku-shokunin/`. Round-18 wave artifacts
   live there by design and never appear in the fleet repo's untracked set.

## Adjacent finding (out of the assigned match, ignored not untracked)

An ignored, malformed directory tree named from a shell error exists at the fleet
root: `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory`
(the last component is an empty file; parent chain is directories). Dated
`Oct 18 14:01`, i.e. before the round-18 launch; it contains no `kaidoku` or
`round-18` name (`grep` does not reach it because `git status --ignored` reports it
as `!! "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/"`, and the nested
`souji-shokunin/` matches the ignore rule). **Inference:** a prior failed
redirection/mkdir, unrelated to this lane; worth a separate cleanup decision,
not attributable to round 18.

## Limits / remaining unknowns

- Content search covered the 11 non-ignored untracked files and the tracked
  modified path; the 37 ignored entries were not content-searched wholesale.
- `.ufo/reports/round-18/kaidoku.md` may appear while this scout's sibling seats
  run; at observation time it was absent.
- No tool installs or upgrades were performed; no VCS writes were made.
