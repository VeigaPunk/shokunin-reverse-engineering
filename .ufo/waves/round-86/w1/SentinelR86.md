# SentinelR86: R86 containment review (read-only)

Full findings table, commands and observed output: `.ufo/waves/round-86/w1/SentinelR86/containment.md`. Receipts: `.ufo/waves/round-86/w1/SentinelR86/receipts/`.
Counters: `tools/round-86/record-agreement.py` (R86-C1), `tools/round-86/gate-registry.py` (R86-C2). No production edit, no commit, no install.

## Findings (severity, id)

- **High, C-1.** gate-registry G2/G3 run `tools/round-85/predicate-bind.py` from the worktree under `--rev`. This breaks the S255 rule the counter's own docstring states. Committed-green plus red worktree gives 3/5; committed-red plus green worktree gives 5/5. The receipt is stamped with the committed `HEAD`.
- **High, C-2.** gate-registry G3 accepts any row-declared argv. `python3 -c ...` in the self-test cell turns G3 green (5/5) with no run of the named gate. G3 does not check that the command path equals TOOL.
- **Medium, C-3.** G3 executes outside `--root` (`python3 ../escape/esc.py`, and an absolute path). Marker written outside the fixture root.
- **Medium, C-6.** `git` children inherit the full 274-variable environment. `GIT_DIR` redirects evidence reads, and the receipt still reports the lane as `root`.
- **Medium, C-13.** `--json-out` has no refusal. It overwrites frozen evidence (proved on a mirror of `pre/`: `c1-at-base.json` clobbered). The real `pre/` probe failed only by accident (`FileExistsError`), and I did not write into the real `pre/`.
- **Low, C-7.** `--rev=--output=PATH` makes git write a file. Operator-supplied, so low.

## Holds

- No shell: metacharacters and `$(...)` reach Python as literal argv (C-4).
- Tool children get a four-key env: `HOME, LANG, PATH, TMPDIR` (C-5).
- No `/tmp` hardcoding. TMPDIR set gives 0 `/tmp` opens; unset falls back to the system temp dir (C-11).
- Pinned-cell traversal (`../../etc/passwd`, `/etc/passwd`) does not escape. record-agreement's SCORECARD path grammar refuses traversal (C-9, C-10).
- `--rev` reads committed bytes for record-agreement (C-8).
- Production runs leave the lane tree unchanged: digest and `git status --porcelain --ignored` identical before and after (C-14).
- BASE calibration reproduced: record-agreement 0/3, gate-registry 0/5 (C-15).

## For L1

- The C2 green state (5/5) is reachable only in `--worktree` mode. The registry row is an uncommitted edit to `SKILL.md`; at HEAD the gate is 0/5 (C-16). Commit the row after C-1 is fixed, then re-score at a committed revision.
- Observed outside scope (C-17): an untracked `.ufo/waves/round-86/pre/sources-census-before.txt` appeared during the review, so `pre/` is not write-protected.

## Recommended fixes (not applied)

Export the executed blob from `--rev`; require G3 path equals TOOL with no `-c`/`-m`; fix the git env and validate `--rev`; refuse `--json-out` over an existing or frozen path. Details in containment.md.

## Scratch

Scratch under `/fast/scratch/hyaku/kaidoku-r86/SentinelR86/` removed after receipts were copied.
