# DraftLessonMistakes — round 20 `## Mistakes` rows (R19-D1, R19-D2)

Written 2026-10-20T17:49:30-03:00 (`date -Iseconds`). Baseline B = `14f0260ad319ecc26994381b2415d5a999003375`.
Lane is read-only for this seat. Only this report was written. Installs: none.

## Scope

Two rows, mined from the round-19 spot-check routed defects `D1` and `D2`
(`corpus/lessons/round-19-verifier-spotcheck.md:180-183`). Classes come from the CORPUS vocabulary
(`CORPUS.md:171-178`; list at `.ufo/waves/kaika-w1/mistakes.md:447-449`).

## Method and commands (observed; run from the lane with `git --no-optional-locks`)

| # | command | exit | observed |
|---|---|---|---|
| 1 | `git blame --porcelain -L 36,36 4f6c73f… -- .ufo/waves/round-19/claims.json` | 0 | header `4f6c73f…`; `committer-time 1792523357`; `author-time 1792522664` |
| 2 | `date -d @1792523357 -Iseconds` / `date -d @1792522664 -Iseconds` | 0 | `2026-10-20T16:09:17-03:00` / `2026-10-20T15:57:44-03:00` |
| 3 | `git log -1 --format='%H %cI' 4f6c73f…` | 0 | `4f6c73f81ae8…  2026-10-20T16:09:17-03:00` |
| 4 | `git blame --porcelain -L 36,36` and `-L 45,45` at `14f0260…` | 0 | line 36 → `4f6c73f…`; line 45 → `b26a6c42…` (`committer-time 1792525563`) |
| 5 | `git show 14f0260…:.ufo/waves/round-19/claims.json \| sed -n '36p;45p'` | 0 | line 36 is the 16:20:00-03:00 amendment; line 45 is the `correction` text |
| 6 | `git status --porcelain` (lane) | 0 | `?? .ufo/waves/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/repo-fixture/` and `…/repo-sub-fixture/` (plus untracked round-20 wave files, not in scope) |
| 7 | `find .ufo/waves/round-19/verify/scratch-custody -maxdepth 3 -name .git` | 0 | `…/repo-fixture/.git`, `…/repo-sub-fixture/.git` |
| 8 | `python3 -I -B .ufo/gates/custody-pair/custody-pair.py selftest --scratch <mkdtemp under /dev/shm>` | 0 | `CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0`; scratch kept `custody-pair-selftest-at2mvoh6/` with `repo-fixture/.git` and `repo-sub-fixture/.git`; I then removed my `/dev/shm` scratch |
| 9 | `git ls-tree -r --name-only 14f0260… -- .ufo/waves/round-20/tools .ufo/gates \| grep -E 'timestamps\|carrier\|custody'` | 0 | only `.ufo/gates/custody-pair/README.md` and `custody-pair.py`; no evidence-timestamp or carrier-guard tool at B |
| 10 | `_grep` for `rmtree` in `custody-pair.py` | — | no match; `mkdtemp` at `custody-pair.py:898` is the only root creation |

## Draft

## Mistakes

| # | class | evidence | captured-by | fix (red-before must be shown) |
|---|---|---|---|---|
| 1 | scope | R19-D1 nested-repo residue. The round-19 driver passed a lane path as selftest scratch: `verify.py:537-539` (`os.makedirs(OUT + "/scratch-custody")`, then `["selftest", "--scratch", OUT + "/scratch-custody"]`), recorded in `verification.json:323-325`. The selftest creates its root with `tempfile.mkdtemp` (`custody-pair.py:898`) and creates git repos `repo-fixture` and `repo-sub-fixture` under it (`custody-pair.py:1372-1373`, `:1426-1428`); `custody-pair.py` has no `rmtree`, so nothing removes the root. Observed in the lane: `git status --porcelain` lists both fixture dirs as `??`, each holding `.git` (`round-19-verifier-spotcheck.md:29,33-35`; command rows 6-7). Observed off-tree: `custody-pair.py selftest --scratch <dir>` exited 0 (`CLEAN cases=31`) and left `custody-pair-selftest-*/repo-fixture/.git` and `repo-sub-fixture/.git` (command row 8). | none. No QUALITY row or gate reports untracked residue; the pathspec-limited commit rule (`PROTOCOL.md:476-479`) keeps residue out of commits but does not detect it. It was caught by hand (`round-19-verifier-spotcheck.md:29`). | Red-before, in a clone at `14f0260` and never in the lane: (a) `custody-pair.py selftest --scratch <DIR inside clone>` exits 0 and `test -z "$(git status --porcelain)"` exits 1, listing both `??` fixture dirs; (b) `selftest --scratch <outside dir>` exits 0 and leaves a `custody-pair-selftest-*` dir. Fix, `custody-pair.py` only: refuse in-worktree scratch with exit 2 and stderr `scratch_inside_worktree` (`.ufo/waves/round-20/contract.md:38-40`); remove the root in `try/finally`; add cases `scratch_in_worktree_refused` and `cleanup_after_run`. Green: the same commands exit 2 with that stderr and an empty status, and the outside run leaves no `custody-pair-selftest-*`. The existing round-19 residue is removed by the L1, not by this row. |
| 2 | number-drift | R19-D2 future-dated timestamp. `.ufo/waves/round-19/claims.json:36` states `"at": "2026-10-20T16:20:00-03:00 …"`. Blame at `14f0260` attributes that line to `4f6c73f` (command rows 1, 4). Commit `4f6c73f` has committer date `2026-10-20T16:09:17-03:00` (command row 3), so the stated instant is 10 min 43 s after the commit that ships it. The amendment is withdrawn at `claims.json:45` as "future-dated relative to the commit carrying it" (command row 5). Lesson records: `round-19-verifier-spotcheck.md:100-103` and `:182-183`. Blame's `author-time` for the line is 15:57:44 -03; the comparison is against the committer time (`contract.md:44-45`). | `PROTOCOL.md:358-360` ("A timestamp on evidence must be at or before the commit that ships it"), prose only. At `14f0260` no checker exists (command row 9). The same pattern is recorded for number drift: "The rule exists; the gate does not" (`.ufo/waves/kaika-w1/mistakes.md:140-142`). | Red-before: at `14f0260`, `python3 -I -B evidence-timestamps.py --root <clone> --rev 14f0260… --path .ufo/waves/round-19 --strict` must exit 1 with `future_dated .ufo/waves/round-19/claims.json:36`. The tool is absent at B (command row 9), so the red state is first shown on a mkdtemp fixture repo: a line with an instant later than its commit exits 1 with `future_dated`, and the corrected line exits 0. The green claim must be scoped: `--path .ufo/waves/round-20 --rev <delivered tip>` exits 0. The round-19 path stays exit 1 by construction, because the line persists in history. Report it as a registered residual that points to `claims.json:45`; do not turn it green by editing `claims.json`. |

## Findings

- **Observation.** Both rows reproduce at B. D1: `git status` shows the two fixture dirs (command row 6); the selftest leaves its root after exit 0 (row 8). D2: line 36 is 16:20:00-03:00 and its introducing commit is 16:09:17-03:00 (rows 1-3).
- **Observation.** `custody-pair.py` has no removal path for its selftest root (row 10, `custody-pair.py:898`).
- **Inference.** The class choices follow CORPUS.md:171-178. `scope` for D1 matches the write-outside-declared-scope pattern in round-19 row 5 (`round-19.md:90`) and `mistakes.md:144` (C03). `number-drift` for D2 matches C02 (`mistakes.md:125-142`): a stated number that differs from the observed record. The alternative `landing` (C09, `mistakes.md:244`) was rejected because D2 has no marker, placeholder, or overwrite.
- **Calibration risk.** The contract's D2 check, run on the round-19 path, will stay red after the fix (see row 2). A green claim for D2 must therefore be scoped to the round-20 path, with the round-19 finding disclosed, or the check will be seen as an overclaim.
- **Calibration risk.** D1's red-before must include the cleanup clause, not only the refusal. The refusal alone (command 1a) does not show that residue leaves after a run outside the worktree (command 1b).
- **Not verified.** The fixer's red-before runs and the `evidence-timestamps.py` and `custody-pair.py` selftests were not executed. Those are the L1's checks.

## Out of scope

- No lane file was edited. No clone was made. The patch and the red-before runs belong to the fixing seats.
- The `scratch_inside_worktree` refusal and the `evidence-timestamps.py` tool are proposals in `contract.md`; they are not observed at B.
