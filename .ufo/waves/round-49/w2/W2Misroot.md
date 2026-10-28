# W2Misroot — seat write hygiene

**Verdict: violation (exit 1).** One pre-freeze kaidoku round-49 misroot is still on the fleet root: 23 untracked files under `tools/round-49/control-fixtures/{c1,c4,c5}/`, 1164980 bytes, mtimes 2026-10-28T17:55:03–17:55:24 -0300. Wave 1 `ExecRunbook` F1 named this same set and asked the L1 to remove it; it is still there after landing `29883d4ec35a31a8393c4ffb220888c44c0bb022`. Wave-2 seats have not added a new path outside `.ufo/waves/round-49/`. The base→landing diff has 0 unexpected paths.

Nothing was moved or deleted. Scratch `/fast/scratch/hyaku/kaidoku-r49/W2Misroot` was removed after these receipts were copied to `.ufo/waves/round-49/w2/W2Misroot/receipts/`.

## Findings

| id | decision | path | evidence |
|---|---|---|---|
| F1 | **misroot, kaidoku round-49, still present** | `/home/vgpnk/Projects/shokunin/tools/round-49/control-fixtures/{c1,c4,c5}/**` (23 files) | Porcelain collapses the dir to `?? tools/`. `-uall -- tools` lists exactly the 23 paths below. Same count, same trio, same mtime window as `w1/ExecRunbook.md` F1. Cause recorded there: `c1-controls.py` `FIXTURES = 'tools/round-49/control-fixtures'` is cwd-relative, so a run whose cwd is the fleet root writes here. c4 manifest sha256 `1b105b78a6873660b48eeec5ba0a39f2c30984742590513ac15bea0d509c5228` equals the manifest `w1/C1TmpScratch.md` F5 produced with `--build-only` (that probe's own cwd was scratch; the fleet tree is a separate cwd=fleet write of c1+c4+c5 in one 21-second burst). |
| F1a | c1 bytes **equal** the landed lane copies | five `c1` files | Worktree and `29883d4e:tools/round-49/control-fixtures/c1/…` match. Manifest sha256 `ab5150e6e6d35f17723cd28a17599af7ef0dbc9d4fc4a14b18aecb755d45fbcf`. |
| F1b | c4 bytes **differ** from the landed fixtures | five `c4` files | Fleet manifest is the pre-amendment plant (`title`: "pre-freeze committed envelopes relabelled onto round-49"; sources `corpus/evidence/round-42/c2/heldout/H41,H43,H44,H45`). Landed `tools/round-49/control-fixtures/c4/manifest.json` sha256 `f52f51b65cd2fdb18b175e26d87fa5a7826a52b5f3c88b41f77c12e7e5ee385d` (1299 bytes). Fleet manifest is 2750 bytes. The four `after.json` files differ the same way (fleet lengths 10441/14529/10440/10441 vs landed 15837/15838/18008/18009). |
| F1c | c5 is **absent** from REV | 12 bins + `c5/manifest.json` | `git ls-tree -r 29883d4e -- tools/round-49` has no `c5/` and no `superbyte-mutation`. Manifest sha256 `af12880e4d1802992aaaeabb81eceb3d944f2e6be4688a1d0cc97be869bd80df`. `v1le/bad-magic.bin` sha256 `706f65284d1e6b75ded40fe9e3e0f6d7a3fc22a2bee1ed94dbc7d810d82e43ed` equals the round-44 control bin `tools/round-44/control-fixtures/c5/.../v1le/bad-magic.bin`. This is the retired CTL-C1-5 superbyte plant. |
| F2 | **no unexpected landing path** | `e4f2cfa5…`..`29883d4e` | 2231 paths. 0 outside the allowed set below. |
| F3 | **wave-2 lane writes stay in the wave dir** | `kaidoku-shokunin` worktree | `status --porcelain -uall`: 887 paths, 0 outside `.ufo/waves/round-49/`. Collapsed status: 11 lines, all under that prefix (L1 dispatch/scores + `w2/`). No tracked modification. |
| F4 | not a kaidoku round-49 seat | `.ufo/waves/round-56/w3/T56W3Led13.md` | Untracked, mtime 2026-10-28T17:56:16 -0300 (inside 6 h). Head: seat `T56W3Led13`, tameshi round-56. `grep -a -c -E 'kaidoku\|round-49'` printed `0`. |
| F5 | excluded, other lane | `lane3/` | Untracked. `origin` is `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. HEAD `297e17927ba9342a87ba27a48cc5270a001de7cb` author `kengaku-shokunin`, subject round-50. Round-49 names inside it are kengaku's round 49. |
| F6 | excluded by the inclusion rule | `o.bin`, `oldrep1.out`, `oldrep2.out` | Staged adds (`A `). Names do not mention kaidoku or round-49. `grep -a -E 'kaidoku\|round-49'` matched nothing. mtimes 2026-10-27T16:58:36 and 2026-10-28T09:10:14 / 09:11:48 -0300, outside 6 h. `o.bin` head is a Cloudflare "Just a moment..." HTML page. `oldrep1.out` / `oldrep2.out` heads are health-check PASS lines. |
| F7 | excluded | `.scratch/**` | 41 of 47 porcelain lines. The one unstaged mod is `M .scratch/goal-20261028-hyaku-run11.md`. |

Per-file sha256 of the 23 misroot files: `receipts/fleet-tools-r49-sha256.txt` (file sha256 `470817c2d25a3e2d591645dd049512e510b0a29d8d90fb15f6fa7c5e82cbb470`).

## Commands

| utc | exit | stdout sha256 | command |
|---|---|---|---|
| 2026-10-28T22:42:02Z | 0 | `63190faf88d0a89fb27a2d0989175e835fcc4584c4b6474b11ba6a1c45f6d0a0` (47 lines, 2540 bytes) | `git -C /home/vgpnk/Projects/shokunin status --porcelain` |
| 2026-10-28T22:47:05Z | 0 | `d4acfccdfacec90787d13819b88b327656752f3e62baa8e98cbb529a5dc1091f` (23 lines) | `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall -- tools` |
| 2026-10-28T22:42:02Z | 0 | `edaed556a92b07575fef260660394392f6c80b6c72e8e669812344c1e75ed2f8` (2231 lines) | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-only e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9 29883d4ec35a31a8393c4ffb220888c44c0bb022` |
| 2026-10-28T22:42:08Z | 0 | `accaf2118d35d32e61463ace4288f5d75615675c15b3dd169ee4ba49c5f4973e` (11 lines) | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain` |
| 2026-10-28T22:45:42Z | 0 | `accaf2118d35d32e61463ace4288f5d75615675c15b3dd169ee4ba49c5f4973e` (same 11 lines) | same command, repeated |
| 2026-10-28T22:47:05Z | 0 | `76f62b62b979ebc363e86f24a51b173c650bc0b70fff7a2440dd2a9b78bc4282` (887 lines) | `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -uall` |

`GIT_NO_REPLACE_OBJECTS=1` on every git command. Lane HEAD at check: `29883d4ec35a31a8393c4ffb220888c44c0bb022`. Freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` is an ancestor (merge-base `--is-ancestor` exit 0).

## Landing diff (F2)

Allowed and present, nothing else:

- `.ufo/waves/round-49/**` — 2135 paths
- `corpus/evidence/round-49/**`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, `corpus/lessons/round-49.md` — 59 paths under `corpus/`
- `tools/round-49/**` — 33 paths
- `plans/round-49-claims.md`, `LOG.md`, `PROVINCE.md`, `SCORECARD.md` — one each

Prefix sum 2135+59+33+1+1+1+1 = 2231. No `.ufo/` path outside `waves/round-49/`. No `SHONEN.md`, `SKILL.md`, or other round's tools/plans/lessons.

Commits on that range, oldest first: `14936cb9` wave-1 evidence, `decc5697` FREEZE, `76d7ad6f` controls scored, `4aabb0b4` C1 data run, `3847f393` landing, then three landing revisions `188ddee`, `b58f9b1`, `29883d4e` (S147/S148 form and S145 restore).

## Lane worktree outside the wave dir (F3)

`status` shows no staged or unstaged edit. Files under the lane with mtime inside 6 h and outside `.ufo/waves/round-49/` fall in three classes:

- Landing paths (`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, `corpus/lessons/round-49.md`, `corpus/evidence/round-49/**`, `plans/round-49-claims.md`, `tools/round-49/**`). `git diff --quiet HEAD` exit 0 on `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/QUALITY.md`.
- Older lessons and tools (`corpus/lessons/round-4{6,7,8}*`, `plans/round-4{6,7,8}-claims.md`, `tools/round-4{6,7,8}/*`, `SKILL.md`). `git diff --quiet HEAD` exit 0 on each sampled path. Content matches HEAD; the mtime change is not a content write.
- Ignored residue: `tools/round-{46,49}/__pycache__/` (`.gitignore` rule `__pycache__/`), `.ruff_cache/` (its own gitignore), `.jj/repo/index/op_links` (`.jj/.gitignore`). Not seat reports.

`find -mmin -360` also hit 2926/1004/601 paths under the lane's `.ufo/waves/round-{47,46,48}/`. Those rounds are not this seat's write root; they are not in `git status`, so they are not untracked or content-modified.

## Porcelain rows that are not F1

Inclusion rule applied to the 47-line porcelain: keep a path when the name or the content mentions `kaidoku` or `round-49`, or the mtime is inside 6 h (cutoff used: 2026-10-28T16:42Z, capture at 22:42Z), and drop `.scratch/`, `.ufo/state/`, and another lane's directory.

- `?? tools/` → F1 (name `round-49`, mtime inside the window).
- `?? .ufo/waves/round-56/` → F4.
- `?? lane3/` → F5, dropped as another lane.
- `A o.bin`, `A oldrep1.out`, `A oldrep2.out` → F6, dropped.
- 41 `.scratch` lines → F7, dropped.

`/home/vgpnk/Projects/shokunin/D=` is an empty directory (child `D=/fast/scratch` only), mtime 2026-10-28T12:07:44 -0300, outside the 6 h window, absent from porcelain. Not counted.

Fleet `git log --all --since='6 hours ago'` includes `5265c931f8f406cdc51eec85f573f88f4a4c434d` (2026-10-28 17:40:42 -0300, author `kaidoku-shokunin <kaidoku@shokunin.local>`, subject `round-49: kaidoku dispatch evidence (hyaku inline attempt 1)`), which adds only `.ufo/prompts/kaidoku-round-49.md` and is an ancestor of fleet HEAD. That is the dispatcher prompt, and the path is not dirty. Three other objects with the same author at 17:40:42–17:40:44 (`616a2007b69dc6ddcedcc707560e93a928586381`, `51a8d5c7d74167ea835ca06f88d1982bfc87c340`, `faa1b20453b27249f21caed5db2f405929dce4c9`) are not ancestors of HEAD (`merge-base --is-ancestor` exit 1) and add `o.bin` together with `.scratch/**`. Those files are F6/F7, not round-49 seat text.

During this check fleet HEAD moved from `6789eb0f437fabefd9010ee4fbaef22c62ac1095` (`git log -1` at porcelain time) to `c7fb588a9ab95d8200edb31b1fec86ceb3c93171` (2026-10-28 19:44:14 -0300, `tameshi-shokunin`, `round-56: tameshi dispatch evidence`). This seat did not commit. The 23-file tools listing was taken after that move and is unchanged.

## Not run

Counters `c1-counter.py` and `c2-mismatch.py` were not run. This seat is write hygiene only.
