# SC4 — Arc commit census at `54bc9dd`

**Verdict: PASS — `4b806e1..54bc9dd` is 16 first-parent commits; `1692acb` remains the sole non-lane identity.** Gross per-commit numstat is 369 commit-file rows, `+103,410/-412`. Endpoint footprint vs `4b806e1` is 352 paths, `+103,032/-34` (342 added, 10 modified). Round-5 delta vs the prior census endpoint `0e8c96b` is 3 lane commits, 67 paths, `+6,732/0`.

## Commit identities and per-commit numstat totals

Range `4b806e1..HEAD` (`HEAD` = `54bc9dd90b0aea67c345c1c6aa180e160164d151`), oldest first. File and line totals are sums of each commit's `git log --numstat` rows and agree with `git show --shortstat`. Zero binary (`-`) rows. Zero merges (`git rev-list --count --merges 4b806e1..54bc9dd` = 0).

| Commit | Author identity | Numstat files | Added | Deleted |
|---|---|---:|---:|---:|
| `58116aa` | kaidoku-shokunin <kaidoku@shokunin.local> | 13 | 4,189 | 2 |
| `df31bfb` | kaidoku-shokunin <kaidoku@shokunin.local> | 64 | 12,466 | 0 |
| `165057e` | kaidoku-shokunin <kaidoku@shokunin.local> | 3 | 330 | 0 |
| `b3cd790` | kaidoku-shokunin <kaidoku@shokunin.local> | 13 | 3,498 | 40 |
| `b21c0da` | kaidoku-shokunin <kaidoku@shokunin.local> | 60 | 18,945 | 0 |
| `679af5d` | kaidoku-shokunin <kaidoku@shokunin.local> | 3 | 248 | 1 |
| `fd30b9c` | kaidoku-shokunin <kaidoku@shokunin.local> | 8 | 92 | 2 |
| `dbba2dd` | kaidoku-shokunin <kaidoku@shokunin.local> | 60 | 26,521 | 0 |
| `158a966` | kaidoku-shokunin <kaidoku@shokunin.local> | 3 | 257 | 0 |
| **`1692acb`** | **v <v@x> (non-lane)** | **4** | **893** | **0** |
| `265e1aa` | kaidoku-shokunin <kaidoku@shokunin.local> | 10 | 1,114 | 367 |
| `fc8e53c` | kaidoku-shokunin <kaidoku@shokunin.local> | 58 | 27,887 | 0 |
| `0e8c96b` | kaidoku-shokunin <kaidoku@shokunin.local> | 3 | 238 | 0 |
| `9ce9ff9` | kaidoku-shokunin <kaidoku@shokunin.local> | 4 | 73 | 0 |
| `3f4a685` | kaidoku-shokunin <kaidoku@shokunin.local> | 60 | 6,405 | 0 |
| `54bc9dd` | kaidoku-shokunin <kaidoku@shokunin.local> | 3 | 254 | 0 |
| **Gross total** | **16 commits; 15 lane / 1 non-lane** | **369 commit-file entries** | **103,410** | **412** |

Prior census (`.ufo/waves/arc2-loop1-round5/SC1.md:3`, endpoint `0e8c96b`) was 13 commits, 302 entries, `+96,678/-412`, endpoint 287 paths `+96,300/-34`. Delta of the gross totals equals the three new commits (`+6,732/0`, 67 commit-file entries). The first 13 rows match that table exactly.

## Endpoint file-change footprint

`git diff --shortstat 4b806e1..54bc9dd`: `352 files changed, 103032 insertions(+), 34 deletions(-)`. Name-status: `A` 342, `M` 10. By path group:

- `.ufo/waves/arc2-loop1-round1/`: 73 (64 seat reports, 9 receipts)
- `.ufo/waves/arc2-loop1-round2/`: 69 (60 seat, 9 receipts)
- `.ufo/waves/arc2-loop1-round3/`: 64 (60 seat, 4 receipts)
- `.ufo/waves/arc2-loop1-round4/`: 63 (60 seat, 3 receipts)
- `.ufo/waves/arc2-loop1-round5/`: 63 (60 seat, 3 receipts) — new vs prior census
- `.ufo/reports/`: 5 round reports (rounds 1–5)
- `.ufo/gates/`: 4 (`c1-census-v10.py`, citation-drift probe, expected.json, pointer-table.json)
- repository-root docs: 5 — `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md` (all `M`)
- `corpus/`: 6 — `README.md` (`M`), 3 knowledge notes (`M`), `corpus/lessons/2026-10-15-round-1.md` (`M`), `corpus/lessons/2026-10-18-wave-dispatch-counting.md` (`A`)

Round-5-only endpoint (`0e8c96b..54bc9dd`): `67 files changed, 6732 insertions(+)`; name-status `A` 65, `M` 2 (`LOG.md`, `SCORECARD.md`). Per-commit files: `9ce9ff9` adds the lesson plus `receipts/{config-pre-pair,config-post-pair,MANIFEST}.txt`; `3f4a685` adds the 60 seat reports; `54bc9dd` adds `.ufo/reports/arc2-loop1-round5/kaidoku.md` and modifies `LOG.md` and `SCORECARD.md`. Seat-prefix counts in round 5: C4 CR8 E24 P4 R8 S2 SC2 V6 Z2.

The non-lane commit's four additions and the later deletion of root `e16-table.json` are unchanged from the prior census. Defect record: `LOG.md:1147`, `SCORECARD.md:927`, `.ufo/reports/arc2-loop1-round4/kaidoku.md:7`.

## Evidence: commands and observed excerpts

Working directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only git. No repo file edited except this report.

1. HEAD and identity enumeration:

```sh
git rev-parse HEAD
git log --reverse --format='%h %an <%ae>' 4b806e1..HEAD
git rev-list --count --merges 4b806e1..54bc9dd
```

Observed:

```text
54bc9dd90b0aea67c345c1c6aa180e160164d151
58116aa kaidoku-shokunin <kaidoku@shokunin.local>
...
1692acb v <v@x>
...
0e8c96b kaidoku-shokunin <kaidoku@shokunin.local>
9ce9ff9 kaidoku-shokunin <kaidoku@shokunin.local>
3f4a685 kaidoku-shokunin <kaidoku@shokunin.local>
54bc9dd kaidoku-shokunin <kaidoku@shokunin.local>
0
```

Full hashes: `4b806e14db22ea44cc57729f5fa3f7b46b616178` (range base, parent of `58116aa`), `0e8c96b48a8823e8c6964081cfc04e21f6adcf56`, `9ce9ff9b0952c8a6b9c5533f9cfa9e957eb985c0`, `3f4a685e66f98bd59bea3a155b9e654989fecca0`, `54bc9dd90b0aea67c345c1c6aa180e160164d151`. `54bc9dd` subject: `arc2-loop1-round5: records — SCORECARD verification section …`; author date `2026-10-18 17:38:12 -0300`.

2. Per-commit numstat, cross-checked two ways:

```sh
git log --reverse --format='COMMIT %h %an <%ae>' --numstat 4b806e1..54bc9dd
git log --numstat --format='COMMIT %h' 4b806e1..54bc9dd | awk 'BEGIN{c=0} /^COMMIT/{c++; next} NF==3 && $1!="-" {a+=$1; d+=$2; f++} END{print "rows",f,"add",a,"del",d,"commits_seen",c}'
git show --shortstat --format='' --no-renames <each>
```

Observed awk line: `rows 369 add 103410 del 412 commits_seen 16`. New-commit shortstat excerpts: `9ce9ff9` `4 files changed, 73 insertions(+)`; `3f4a685` `60 files changed, 6405 insertions(+)`; `54bc9dd` `3 files changed, 254 insertions(+)`. `1692acb` shortstat still `4 files changed, 893 insertions(+)`.

3. Endpoint totals:

```sh
git diff --shortstat 4b806e1..54bc9dd
git diff --name-status 4b806e1..54bc9dd
git diff --shortstat 0e8c96b..54bc9dd
```

Observed: `352 files changed, 103032 insertions(+), 34 deletions(-)`; name-status letters `342 A` / `10 M`; round-5 delta `67 files changed, 6732 insertions(+)`. The ten `M` paths and the one new corpus lesson are listed above.

4. Untracked boundary:

```sh
git status --porcelain
```

Observed: `?? .ufo/gates/__pycache__/` and `?? .ufo/waves/arc2-loop1-round6/`. Neither is in the committed range.

## Conclusions

- **Observation:** `4b806e1..54bc9dd` yields 16 linear commits. Fifteen are `kaidoku-shokunin <kaidoku@shokunin.local>`; one is `1692acb`, `v <v@x>`. Gross numstat `+103,410/-412` over 369 rows. Endpoint vs `4b806e1` is 352 paths, `+103,032/-34`. Round-5 delta vs `0e8c96b` is `9ce9ff9` + `3f4a685` + `54bc9dd`, `+6,732/0`, 67 paths.
- **Inference:** Updating the round-5 census (`.ufo/waves/arc2-loop1-round5/SC1.md:3`, endpoint `0e8c96b`, 13 commits / `+96,678/-412` / 287 paths `+96,300/-34`) by the three new commits accounts for every total difference. `1692acb` is still the only non-lane identity; the defect text is unchanged at `LOG.md:1147`.
- **Unknown:** This census does not classify untracked worktree contents (`?? .ufo/waves/arc2-loop1-round6/` and `?? .ufo/gates/__pycache__/`). It does not re-verify custody hashes. It does not claim the round-6 PE service state.

## Verbatim landing text for parent

```text
Arc census (`4b806e1..54bc9dd`, HEAD `54bc9dd90b0aea67c345c1c6aa180e160164d151`): 16 first-parent commits — 15 by `kaidoku-shokunin <kaidoku@shokunin.local>` and one non-lane commit, `1692acb` by `v <v@x>`. Gross per-commit numstat: 369 commit-file rows, +103,410/−412 (0 binary). Endpoint vs `4b806e1`: 352 paths (342 added, 10 modified), +103,032/−34. Round-5 delta vs prior census endpoint `0e8c96b`: `9ce9ff9` (4 files, +73), `3f4a685` (60 files, +6,405), `54bc9dd` (3 files, +254); endpoint 67 paths, +6,732/0. Untracked and excluded: `.ufo/waves/arc2-loop1-round6/`, `.ufo/gates/__pycache__/`.
```
