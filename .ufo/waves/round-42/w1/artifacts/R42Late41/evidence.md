# R42Late41 audit evidence — commands and observed outputs (read-only session, 2026-10-26 ~19:0x -03)

All git/ls commands run against the lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No VCS mutation, no lane write outside this artifacts dir and the report `.ufo/waves/round-42/w1/R42Late41.md`.

## 1. Lane state at audit time

`git status --porcelain=v1 --untracked-files=all` → 13 lines, all under `.ufo/waves/round-42/`:

```
?? .ufo/waves/round-42/w1-validate.out
?? .ufo/waves/round-42/w1.ready.dispatched
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/collisions
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/collisions-zero
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/reg-ids
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/reg-ids-zero
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/registry.md
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/staged-ids
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/staged-ids-zero
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/guard/staged.md
?? .ufo/waves/round-42/w1/artifacts/R42AssimIds/assimilation/quarantine-slice
?? .ufo/waves/round-42/w1/artifacts/R42ScoutCalib/SCORECARD.base.md
?? .ufo/waves/round-42/w1/artifacts/R42ScoutCalib/SHONEN.base.md
?? .ufo/waves/round-42/w1/artifacts/R42ScoutCalib/cands.tsv
?? .ufo/waves/round-42/w1/artifacts/R42ScoutCalib/extract.txt
?? .ufo/waves/round-42/w1/swarm-registry.json
```

No `M`/`D` lines, nothing under `.ufo/waves/round-41/`, no `green.err`/`red.err`. `.gitignore` is only `__pycache__/` + `*.pyc`, so untracked ≠ ignored.

## 2. Commits since the round-41 tip `74064474`

`git log --format='%h|%an|%ai|%s' 740644747865c1c331bfacaf4daf46ea218762c3..HEAD`:

```
fdabdfa4|kaidoku-shokunin|2026-10-26 18:50:50 -0300|round-42: draft claims (not frozen), start census, wave-1 spec/generator/dispatch
ae5dc3f3|kaidoku-shokunin|2026-10-26 18:36:04 -0300|round-41: wave-2 settled — remaining reports, results ledger, lesson wave-2 section
c4a38ea2|protocol-shokunin|2026-10-26 18:31:27 -0300|round-41 verifier spot-check (integrator, hyaku): non-author admit/reject
```

`git show -s --format=%ci ae5dc3f3` → `2026-10-26 18:44:28 -0300` (committer date; author date 18:36:04).
`git show --name-only ae5dc3f3` non-w2 paths: `.ufo/waves/round-41/r41-w2-results.json`, `.ufo/waves/round-41/w2.ready.dispatched`, `corpus/lessons/round-41.md`.
`git show --name-only fdabdfa4 | grep round-41` → empty (round-42 launch touched no round-41 path).

## 3. Directory mtimes around the stray cleanup

`ls -la --time-style=full-iso` (excerpt):

```
lane root .            drwxr-xr-x 1 ... 352  2026-10-26 18:44:18.003442569 -0300 .
.ufo/waves/round-41/w2 .            drwxr-xr-x 1 ... 1116 2026-10-26 18:43:24.071462808 -0300 .
corpus/evidence/round-41/c1/V4 .    drwxr-xr-x 1 ... 144  2026-10-26 18:44:18.003442569 -0300 .
```

`ls green.err red.err` in lane root and in `corpus/evidence/round-41/c1/V4/` → all four: `No such file or directory`. The identical nanosecond mtime on lane root and V4 = one cleanup instant at 18:44:18, 10 s before ae5dc3f3's committer timestamp 18:44:28.

## 4. Per-file commit attribution

`git log --format='%h|%ai|%s' -- <path>` (first entry each):

```
R41W2C1Rescore.md      ae5dc3f3|2026-10-26 18:36:04|round-41: wave-2 settled …
R41W2C2CounterMut.md   ae5dc3f3|2026-10-26 18:36:04|…
R41W2Reservation.md    ae5dc3f3|2026-10-26 18:36:04|…
R41W2C2Table.md        ae5dc3f3|2026-10-26 18:36:04|…
R41W2C1Docs.md         ae5dc3f3|2026-10-26 18:36:04|…
R41W2C1Mutants.md      ae5dc3f3|2026-10-26 18:36:04|…
R41W2ReproV4.md        ae5dc3f3 (added-line delta) — first entry; prior state 74064474|…wave-2 reports landed so far
```

`git diff 74064474..HEAD -- .ufo/waves/round-41/w2/artifacts/R41W2Reservation/tx-exec-calls.json` → empty (tracked at 74064474, unchanged since; the closure's `D` worktree deletion was restored, never committed). `git log` for that file: last commit `74064474`.

## 5. Post-commit write check (M41-4 recurrence)

`find .ufo/waves/round-41/w2 -type f -newermt '2026-10-26 18:44:28'` → **no output**: no file under w2 is newer than ae5dc3f3's commit instant. The three reports with late mtimes (C2Table 18:38:22, C1Docs 18:40:44, C1Mutants 18:43:24) all predate 18:44:28.

## 6. Dispatch ↔ report coverage

`jq -r '.taskCall.tasks[].name' .ufo/waves/round-41/w2-dispatch.json | sort` = 33 names; `git ls-files .ufo/waves/round-41/w2/ '*.md'` = the same 33 `R41W2*.md` files (1:1). Ledger `.ufo/waves/round-41/r41-w2-results.json`: `.seats` = 33, `.results | length` = 33.

## 7. R41W2ReproV4.md closure-era delta (the tracked `M` at closure)

```diff
-`c1-run.sh` cannot write `run.json` for V4 (EPIPE of `MAX_ARG_STRLEN`), leaving the
+`c1-run.sh` cannot write `run.json` for V4 (E2BIG: a 146,561-byte `--argjson summary`
+over `MAX_ARG_STRLEN` = 131,072), leaving the
 flagship carrier's only evidence as `after.json` plus a raw shell error line.
```

## 8. unblob.log in the lane root (checked, NOT a round-41 stray)

`git ls-files --error-unmatch unblob.log` → tracked; last touched by `7a1ac7fe` 2026-10-26 04:13:36 -0300 "round-38 (attempt 2): … misroot unblob.log". Worktree matches HEAD (clean status). It is committed round-38 evidence, not a leftover.
