# ScoutSources — `corpus/SOURCES.md` at freeze `5017e1f`

Mapped at commit `5017e1f7299c3a812e87e7950148f54313dd279e`, blob `bc817412d6c3952deeb316914db24b5e89794cf6`, file sha256 `13d14bb593d3f0c5cbc2f23ccc0c55a5d30dba7f29ed1e88e81a4438407b970b` (246 lines, 162754 bytes, trailing newline). Extract `git hash-object` matches that blob (`receipts/fz-identity.out`). No install. Exact argv is `receipts/<id>.cmd`. Stdout bytes are `receipts/<id>.out`.

Axes: coverage (every requested count, plus both census runners), depth (freeze blob vs later HEAD, exact used-by token), calibration (exit 0 is not cleanliness; a wrong `--file` base is not a registry failure).

## Freeze map

| measurement | value |
|---|---|
| row count | 142 |
| highest id | `S142` (numeric 142) |
| id gaps | none. Ids are `S001`..`S142` in file order. Next unused id on **this blob** is `S143` |
| tier | `A=134 B=7 C=1` (trailing space in the awk stdout). Sum 142. `queued` is not a tier |
| status | `mined=137 rejected=5` (trailing space). Sum 142. Awk omits zero buckets; maintained census adds `status.queued=0` |
| malformed (`NF!=13`) | `0` |
| duplicate ids | none (empty stdout) |
| enum / tier-inflation | none (empty stdout) |
| mined used-by missing on disk, checked from the lane root | none (empty stdout). 234 mined refs, 67 unique paths, `missing_commit=0` at the freeze and `missing_worktree=0` at 2026-10-28T17:52:41Z |
| rows outside `## Registry` | 0. Heading line 3, all 142 data rows are lines 7–148, next heading `## Paths` is line 153 |

`used-by` naming `corpus/lessons/round-46.md`: **one row**, exact comma/semicolon token. `grep -n 'round-46.md'` on the freeze extract prints only line 148 (`receipts/fz-round46-mentions.out`, exit 0, stdout sha256 `fddebc848ddeddf0c223aa7df4c6a18012bf343ad6f71661a0770ccbde4ebfd7`, 2026-10-28T17:55:22Z).

| line | id | tier | status | used-by cell |
|---|---|---|---|---|
| 148 | S142 | A | mined | `corpus/lessons/round-46.md` |

S142 is the git-log manual row (`https://git-scm.com/docs/git-log`). It is the last registry row.

## Where the next row is appended

On the freeze blob, append the next registry row **immediately after line 148**. Lines 149–152 are empty. Line 153 is `## Paths`. A row inserted after those blanks is outside the markdown table. A row at or after line 153 is outside `## Registry` (`E12` in `scripts/sources-census.sh`). Do not append into `## Paths` (line 153), `## Search log` (line 178), or `## Leads (unopened)` (line 236).

## Census exit

`CORPUS.md` "### Census" is seven commands, not one exit. Frozen manual commands, lane cwd, input = the freeze extract:

| check | exit | stdout | stdout sha256 | utc |
|---|---|---|---|---|
| rows `grep -cE` | 0 | `142\n` | `1dadd7223f8953c76459851cca53c62990c1a7b87a5795d31bbfa4059160e9f8` | 2026-10-28T17:50:44Z |
| malformed | 0 | `0\n` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | 2026-10-28T17:50:44Z |
| tier | 0 | `A=134 B=7 C=1 \n` | `bd9958c6ed64dc98b6c3b7b37170f637cdb2395889c2748acd095ef4e08bbd8d` | 2026-10-28T17:50:44Z |
| status | 0 | `mined=137 rejected=5 \n` | `7bcfcbebdef8b50437f0e6e70966c6038a183aa3d48687698b205d5c09965d44` | 2026-10-28T17:50:44Z |
| duplicate ids | 0 | empty | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| enum | 0 | empty | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |
| mined used-by exists | 0 | empty | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:50:44Z |

That is the freeze census. Every command exited 0 and the three "must print nothing" commands printed nothing.

The same seven commands run **verbatim** on `corpus/SOURCES.md` from the lane root do **not** measure the freeze. At 2026-10-28T17:50:44Z that file was already one row ahead (worktree sha256 `c5b4014de20cb275bfb8489b37e48e72d147724073cd5dc2c5ce1247ab261a7f`, git blob `a7201ac9d0dbf6cec62f7acb60e0578234f12ea9`). Rows printed `143` (exit 0). The missing-path command printed `missing: corpus/lessons/round-47.md` and still exited 0, because `|| echo` makes a hit succeed. **Exit 0 is not a clean census.** Re-run of that missing-path command at 2026-10-28T17:53:17Z produced the same stdout sha256 `57aba0780e66bafd09a7d800cf494445b2a945dc881bc8f3fe992753bd571f30`.

Maintained parser (`CORPUS.md` "outside frozen v1"), not a substitute for the block above:

| run | exit | what it actually says | stdout sha256 | utc |
|---|---|---|---|---|
| `validate --root … kaidoku` (live lane) | **1** | 15× `W04` plus `E11 S143 missing used-by corpus/lessons/round-47.md`. Same stdout at 17:50:44Z and 17:53:17Z | `8c588ddeb4acac30b6310aadd9715a2fd5d4f61ce39d2b91692b4907abfcf3c5` | 2026-10-28T17:53:17Z |
| `census --root … kaidoku` | 0 | rows 143, `tier.A=135`, `status.mined=138`, `status.queued=0`, `FLEET.missing=0` (missing **registry file**, not used-by) | `784b6b4fbbaaa0e15bf76d53603173e0bc461eb396f75fc56362795cd6e9f5c4` | 2026-10-28T17:50:45Z |
| `validate --file` on a `view/corpus/SOURCES.md` byte-identical to the freeze blob, other lane paths symlinked | **0** | 15× `W04`, no `E` line, final `ok`. Includes `W04 S142 duplicate url git-scm.com/docs/git-log across scopes`. Warnings do not fail this script | `d8b6f9f508efa1695ac414441e628e071138be910224c374e566c778f8ee1455` | 2026-10-28T17:51:49Z |
| `census --file` on that view | 0 | rows 142, tier A/B/C 134/7/1, mined 137, rejected 5, queued 0, `FLEET.missing=0` | `a29f7abcc61ddbcf045e9f27d54cceb5cf522a7d3897795a54570a69e32352ed` | 2026-10-28T17:51:49Z |
| `validate --file` on the extract sitting **directly** in scratch | 1 | **not a verdict.** `--file` sets the path base to `dirname(file)/..` (`sources-census.sh` around the `dir_abs` assignment), which was `/fast/scratch/hyaku/kaidoku-r47`, so every used-by path was `E11`. Discard | `149491f4c7f135f039e0510c0370280482d3e30ef979405b93d4c6ddf8523c8e` | 2026-10-28T17:50:45Z |

## HEAD is not the freeze

`5017e1f` is an ancestor of HEAD (`merge-base --is-ancestor` rc 0 at 2026-10-28T17:52:56Z). HEAD moved during this seat (`3186f69b…` at 17:49:58Z, `2e4ae434…` at 17:52:41Z, `1e2c3102952dc636650095643c1963c833859019` at 17:53:17Z). At that last pin, `HEAD:corpus/SOURCES.md` and the worktree file are both blob `a7201ac9…`, one insertion past the freeze (`1 0 corpus/SOURCES.md`). Last commit that touches the file: `e856beb552080c03ede6000b96f1b58bde44c421` (2026-10-28T14:51:02-03:00), subject `round-47: land craft block 24, the record corrections, the current axis heads and S143`.

That commit's row, still on the 17:53:17Z HEAD blob, is line 149: `S143`, tier A, status mined, used-by `corpus/lessons/round-47.md`. That path is absent from the worktree, from the freeze tree, and from `HEAD` at 17:53:17Z. The live `validate` exit 1 is that `E11`. The freeze blob has no `S143` and its manual census does not see this row.

Consequence for an append on the **freeze** bytes: the next id is `S143` after line 148. That id is already the last row on current HEAD. A second `S143` collides. On the HEAD blob the next unused id is `S144`, and the append line is 149, not 148. This seat did not edit `SOURCES.md`.

`corpus/lessons/round-46.md` is named by S142 and was present at the freeze (`missing_commit=0`). `corpus/lessons/round-47.md` was not checked as a freeze used-by path because the freeze registry does not cite it.

## Not run

`sources-census.sh overdue`, `shared`, and `selftest` were not run. No claim about them.

## Receipts

`.ufo/waves/round-47/w1/ScoutSources/receipts/`. Full measurement table: `.ufo/waves/round-47/w1/ScoutSources/report.md`.
