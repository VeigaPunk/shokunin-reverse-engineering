# SC1 — Arc 2 loop 1 rounds 1–4 Git census

**Verdict: PASS — the arc contains 13 commits; `1692acb` is the sole non-lane identity.** The endpoint footprint from `4b806e1` through `0e8c96b` is 287 paths (`+96,300/-34`), distinct from gross per-commit numstat churn (`+96,678/-412`).

## Commit identities and per-commit numstat totals

All entries below are from the requested range `4b806e1..HEAD`, oldest first. The file and line totals are sums of each commit's `git log --numstat` rows (and agree with `git log --shortstat`).

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
| **Gross total** | **13 commits; 12 lane / 1 non-lane** | **302 commit-file entries** | **96,678** | **412** |

## Endpoint file-change footprint

`git diff 4b806e1..HEAD` contains 287 unique paths: 277 added and 10 modified. By path group:

- `.ufo/waves/arc2-loop1-round1/`: 73 paths (64 seat reports, 9 receipts)
- `.ufo/waves/arc2-loop1-round2/`: 69 (60 seat reports, 9 receipts)
- `.ufo/waves/arc2-loop1-round3/`: 64 (60 seat reports, 4 receipts)
- `.ufo/waves/arc2-loop1-round4/`: 63 (60 seat reports, 3 receipts)
- `.ufo/reports/`: 4 round reports
- `.ufo/gates/`: 4 files (census gate + citation-drift probe, expected data, pointer table)
- repository-root docs: 5 — `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`
- `corpus/`: 5 — `README.md`, 3 knowledge notes, 1 lesson

The one non-lane commit's four additions were `.ufo/waves/arc2-loop1-round4/E23.md`, `.ufo/waves/arc2-loop1-round4/E4.md`, `.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt`, and root `e16-table.json`. `265e1aa` deletes the latter, so `e16-table.json` is historical churn, not part of the endpoint footprint. The defect and removal are independently recorded at `LOG.md:1147-1153`, `SCORECARD.md:927-933`, and `.ufo/reports/arc2-loop1-round4/kaidoku.md:5-8`.

## Evidence: commands and observed excerpts

1. Identity enumeration (exact requested format):

```sh
git log --reverse --format='%h %an <%ae>' 4b806e1..HEAD
```

Observed output (all 13 rows are listed in the table above):

```text
58116aa kaidoku-shokunin <kaidoku@shokunin.local>
...
1692acb v <v@x>
...
0e8c96b kaidoku-shokunin <kaidoku@shokunin.local>
```

2. Per-commit numstat source:

```sh
git log --reverse --format='COMMIT %h %an <%ae> %s' --numstat 4b806e1..HEAD
```

Observed excerpt:

```text
COMMIT 1692acb v <v@x> rule 11
210 0 .ufo/waves/arc2-loop1-round4/E23.md
315 0 .ufo/waves/arc2-loop1-round4/E4.md
6 0 .ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt
362 0 e16-table.json
COMMIT 265e1aa kaidoku-shokunin <kaidoku@shokunin.local> ...
0 362 e16-table.json
```

The full numstat stream has no binary entries. Sum of all rows by commit: 302 commit-file entries, 96,678 additions, 412 deletions; per-commit totals are tabulated above.

3. Endpoint totals and path status:

```sh
git diff --shortstat 4b806e1..HEAD
git diff --name-status 4b806e1..HEAD
```

Observed shortstat:

```text
287 files changed, 96300 insertions(+), 34 deletions(-)
```

Observed name-status output starts with the four `.ufo/gates/` additions and ends with `M` for `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/README.md`, the three `corpus/knowledge/` notes, and `corpus/lessons/2026-10-15-round-1.md`; counting the full output gives `A:277 M:10`. The full path list groups to the footprint counts above.

4. Direct anomaly inspection:

```sh
git show --format='commit %h%nAuthor: %an <%ae>%nSubject: %s' --stat 1692acb
git show --format='commit %h%nAuthor: %an <%ae>%nSubject: %s' --name-status 265e1aa -- e16-table.json
```

Observed excerpt: `1692acb` author `v <v@x>`, subject `rule 11`, `4 files changed, 893 insertions(+)`; the second command reports `D e16-table.json` at `265e1aa`. The contemporaneous record says the scratch chain's `/tmp` quota failure skipped its `cd`, causing `git add -A && git commit` at repo root, with no custody path (`LOG.md:1147-1153`).

## Conclusions

- **Observation:** The Git range yields 13 commits; 12 use `kaidoku-shokunin <kaidoku@shokunin.local>` and one is `1692acb`, `v <v@x>`. Direct per-commit stats sum to 302 entries and `+96,678/-412`; the endpoint diff is 287 unique paths and `+96,300/-34`.
- **Inference:** `1692acb` is the non-lane defect commit: author identity differs from all lane commits, and the repo's round-4 records call it non-lane and document the accidental root commit (pointers above).
- **Unknown / boundary:** This committed-range census does not classify untracked worktree contents. The exact command `git status --short --untracked-files=normal` returned `?? .ufo/waves/arc2-loop1-round5/`; it is excluded from the base-to-HEAD diff.

## Verbatim landing text for parent

```text
Arc census (`4b806e1..0e8c96b`): 13 commits total—12 by `kaidoku-shokunin <kaidoku@shokunin.local>` and one non-lane commit, `1692acb` by `v <v@x>`. Per-commit numstat totals are 302 commit-file entries, +96,678/-412. The endpoint footprint is 287 paths (277 added, 10 modified), +96,300/-34; `1692acb`'s root `e16-table.json` was removed in `265e1aa`.
```
