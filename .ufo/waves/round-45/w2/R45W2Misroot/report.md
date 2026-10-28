# R45W2Misroot — fleet-root misroot sweep

Axes: coverage (every porcelain `??` path), depth (bytes, first line, sha256, mtime), calibration (seat misroot vs canonical report vs other-lane scratch). Nothing under `.scratch/`, `.ufo/state/`, or another lane was deleted or moved. No tool install.

## Command

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

Exit 0. UTC `2026-10-28T16:02:47Z`. stdout sha256 `70110fe71edf10b42488d6d271f57a48db5fcaf3a2f7e7fbb859eee23f9fa930` (194 bytes). Receipt: `.ufo/waves/round-45/w2/R45W2Misroot/status.stdout`. Same seven `??` lines and one ` M` at `2026-10-28T16:01:10Z`.

```
 M .ufo/l0-questions.md
?? .scratch/closure-mado-r50.json
?? .scratch/closure-r54/
?? .scratch/source-routing-queue.md
?? .ufo/reports/round-45/kaidoku.md
?? o.bin
?? oldrep1.out
?? oldrep2.out
```

## Untracked paths whose content names `kaidoku` or `round-45`

Case-insensitive byte scan (`kaidoku`, `round-45`, `round 45`).

| path | verdict | first line | size | sha256 | mtime UTC |
|---|---|---|---|---|---|
| `.ufo/reports/round-45/kaidoku.md` | content match | `# kaidoku — round 45` | 20881 | `eec126742219126f867b51a4f73c39e50c9d00ecc68a0b2edfed0ad794920a76` | `2026-10-28T16:01:33Z` |

That is the only porcelain-listed file with a hit. It is the uncommitted fleet round report (canonical path: sibling `round-45/*.md` files are tracked; `git ls-files` does not list `kaidoku.md`). It is not a seat wave file. An earlier read in this seat saw 20603 bytes / `c96ddd356766ecd160ff66da4bcbd081b9e299471477914c87e698a9d1bdcffd` before the misroot paragraph landed; the hash above is the bytes judged.

No other porcelain-listed file contains the strings:

| path | first line | sha256 |
|---|---|---|
| `.scratch/closure-mado-r50.json` | `{"round": 50, "date": "2026-10-27", "type": "closure", "lane": "mado", ...` | `dd7024d4de2e79ac58fdb3ec0561e8ec076a73b04717906ba2dbb9c8fa702149` |
| `.scratch/source-routing-queue.md` | `# Source-routing queue — operator directives 2026-10-27 (hyaku run 10)` | `8441ee954d5f4af1a0624588f72ea2d65dc5899d1426c7e14a68c9a5c55d7428` |
| `o.bin` | `<!DOCTYPE html>...<title>Just a moment...</title>...` | `5d670538e975a622f5380465e444002f71c30e5a392570b4fc6abce6d8d23757` |
| `oldrep1.out` | `PASS healthy: all planes pass (exit 0, HEALTHY)` | `f8c8acfba89b45f4a5c015d1da0f0d33b610f620b0734026bd56dae6a12eb51c` |
| `oldrep2.out` | `PASS healthy: all planes pass (exit 0, HEALTHY)` | same sha256 as `oldrep1.out` |

`git status --porcelain -uall` lists the files inside `.scratch/closure-r54/` except three nested git dirs. Those enumerated files have no hit. The nested dirs (`.scratch/closure-r54/lane/`, `work-c2/clone/`, `work-c2-base/clone/`) are not expanded by status. A read-only walk found the substrings inside them; each `LOG.md` first line is `# tameshi-shokunin — Iteration Log`. They are tameshi closure clones, not kaidoku seat drops. Left in place.

## Attacks

### 1. Report sweep count — falsified

Attacks `.ufo/reports/round-45/kaidoku.md:237-240` (bytes `eec12674…`): the cited command "shows three untracked fleet-root files" (`o.bin`, `oldrep1.out`, `oldrep2.out`).

Observed: seven `??` lines, not three. Omitted: `.scratch/closure-mado-r50.json`, `.scratch/closure-r54/`, `.scratch/source-routing-queue.md`, and `.ufo/reports/round-45/kaidoku.md` itself.

Fix: quote the full porcelain and classify every line. Do not delete the scratch or the three pre-existing root files.

The narrower claim that those three files do not contain `kaidoku` or `round-45` **holds** (table above). `o.bin` mtime `2026-10-27T19:58:36Z` is 16:58 at UTC−3, matching the report's unlabeled `2026-10-27 16:58`. `oldrep1.out` `2026-10-28T12:10:14Z` and `oldrep2.out` `2026-10-28T12:11:48Z` match unlabeled 09:10/09:11 at UTC−3. `oldrep1.out:167` is `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)` — tsukuroi, not this lane. The report's "12:20 launch" clock was **not run** here.

### 2. "None names kaidoku" over the whole porcelain set — falsified

If "none names `kaidoku` or `round-45`" is read as the whole `??` set, it is false. `.ufo/reports/round-45/kaidoku.md` is in that set and its first line is `# kaidoku — round 45`. Grammatically the report attaches "none names" to the three files it listed; that attachment **holds**, and the count it rests on does not.

### 3. Seat wave artefact at the fleet root — holds

Historical misroot shape is a seat file under fleet `.ufo/waves/round-N/` or a loose seat report (lessons round 21, 26, 34, 39).

```
git -C /home/vgpnk/Projects/shokunin status --porcelain -uall -- .ufo/waves
```

Exit 0, empty stdout. `git ls-files .ufo/waves/round-45` prints nothing.

Lane `git status --porcelain -uall` at `2026-10-28T16:01:40Z` (stdout sha256 `db1ec87b6722ab9ea8dd88d7a8de04f131e903e09bedeaa9ca276d7666868308`) listed only paths under `kaidoku-shokunin/.ufo/waves/round-45/` (`l1/` preflight json, `w1.ready.dispatched`, `w2.ready.dispatched`, `w2/R45W2PreflightReal/`, `w2/R45W2MutC1Landing/`). Those are in-lane. The lane tree was live; this is not a frozen census.

`kaidoku.md` at the fleet reports path is an uncommitted closure draft, not a seat misroot. Nothing was moved.

### 4. "No fleet-root file edited" — falsified

Attacks the same report, line 112: `` `SHONEN.md` untouched; no fleet-root file, template or script edited. ``

`git -C /home/vgpnk/Projects/shokunin diff -- .ufo/l0-questions.md` exit 0, stdout sha256 `855a1e8f8de9c0a1b6bc68e0e41bcd47464920f6500dbb85b0e21433c44b23c3`. Two added lines, absent at HEAD (`git grep -e 'kaidoku | round-45' HEAD -- .ufo/l0-questions.md` exit 1):

```
kaidoku | round-45 | streak-brake cleared by orchestrator after 3x rejected-honest-stop (r42-r44); ...
kaidoku | round-45 | The freeze-integrity preflight (tools/round-45/frozen-path-preflight.py) can only run where a lane can put it; ...
```

Worktree sha256 of the file `bdbf1853547571350649305dc4c9c2ca511c69dbae787e1c7f66f1e1ef43f19b`, mtime `2026-10-28T15:53:54Z`. The report's own lines 263-264 say the question was appended to `.ufo/l0-questions.md`.

Fix: line 112 must name that uncommitted two-line append (and this untracked report) instead of claiming no fleet-root edit. `SHONEN.md` was not checked by this seat.

### 5. Admission sentence still says A2 — falsified

Attacks the same report, line 248: "The two frozen predicates are met at A2".

Line 15 of that file says the measured revision is `f59565b782c18b0eb691bec12f52d2f80d9f5032` (A3). Committed record agrees: `LOG.md` "A3 is the round's measured revision" and `SCORECARD.md` "The measured revision for the round is A3" at that hash. Both commits resolve (`git rev-parse --verify`). Fix: line 248 should say A3, matching the header and the ledger. Not a misroot.

## Not run

- Content of ignored `.ufo/state/kaidoku.mission`, `.ufo/state/kaidoku.out`, `.ufo/state/kaidoku.report-baseline`, `.ufo/state/kaidoku.round`. Names only, from `git status --porcelain --ignored -uall`. Seat forbids touching `.ufo/state/`. They are absent from the assigned porcelain (no `--ignored`). `kaidoku-shokunin/` is ignored because it is the nested lane repo.
- The report's "12:20 launch" instant.
- Whether `SHONEN.md` is untouched.

## Installs

None.
