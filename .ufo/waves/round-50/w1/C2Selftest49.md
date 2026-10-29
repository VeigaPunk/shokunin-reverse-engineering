# C2Selftest49 — hermetic self-test for the frozen `tools/round-49/c2-mismatch.py`

**Verdict: BUILT AND PASSING. `selftest-r49-c2.py` runs 40 cases (green ×2; every atom A1..A9 red on its own defect; counter-bytes mismatch and 5 other refusals; 3 CLI cases; 2 known-blind) against a hand-written expected file, exit 0, wall 75 s under host load ~54, writing nothing outside `$TMPDIR` (proven under a read-only bind mount).** It also kills 21 of 22 counter mutants (the 22nd is an equivalent mutant). `tools/round-49/c2-mismatch.py` was not edited (sha256 `9b80b3b0…595d`, working tree clean for `tools/round-49`). I did not touch the lane; nothing was committed.

Deliverables (seat dir `.ufo/waves/round-50/w1/C2Selftest49/`):
- `tools/round-50/selftest-r49-c2.py` (sha256 `7d0523ab6b80c0b570f36e682eb0f446ffdd455d48e84d50399876b79a3e7fbc`)
- `tools/round-50/selftest-r49-c2.expected.json` (sha256 `0a9ddec8dc917f835a609352218854f41b6038a17418962b3047dfc5b033c36f`)
- `receipts/selftest-run-bwrap.json` (sha256 `5954a2c94fa7c7d61f626b5f5007dc752bcf7d1d62c4a488c34390e4874377ef`, equal to the run's stdout sha256), `receipts/mutant-summary.{json,txt}` (json sha256 `f4c21c0827112f4758ed4a0be35b488570e0ebe3c10ffdfc64b527c200639eb0`), `receipts/mutants/*.py` (22 edited copies of the frozen counter plus `drive.py`; no vendor bytes).

## Design (what the L1 should know before freezing it)

- **Fixture**: one `git clone --shared --no-checkout <lane>` into `WORK/clone`; toplevel asserted equal to the clone path before the first commit; `user.name/email`, `commit.gpgsign=false`, `core.hooksPath=/dev/null` set in the clone only; all git calls `-C clone`; child env drops `GIT_*`, sets `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, `HOME=WORK/home`, `TMPDIR=WORK`. Each case: `checkout --detach BASE`, `clean`, ONE regex/byte edit of committed bytes (every edit asserts it matched and changed something; an empty commit is a fixture error, exit 2), commit, run the counter `python3 -I -B` at that REV with `--freeze decc5697…`.
- **Why the real history and not a synthetic repo**: the counter hard-codes `LANE_BASE e4f2cfa5…`, `R48_BASE`, `R48_TIP`, `decc5697` ancestry, five round-48 blobs and the round-48 `w1/` tree; a synthetic repo cannot carry those hashes. The green fixture is therefore the real lane commit `7c678ae6…` (REV == BASE, no commit). The lane object store is read through alternates; nothing is written to it.
- **Expected values are independent**: `selftest-r49-c2.expected.json` is hand-written (exit, red atom set, `reason` prefix, optional `why_contains` fragment of the red atom's message, battery facts). The runner never derives an expectation from a counter run, pins the counter sha256 (mismatch → exit 2), pins BASE/FREEZE, `cases_total`, and fails if the case list and expected keys differ or if some atom has no single-defect red case.
- **`why_contains`** pins a fragment of the clause that must fire. Atom-level checks alone let removable clauses survive (see F4/F5); the fragments fixed that.
- **Exit codes of the self-test**: 0 all cases match; 1 a case differs (or list/expected disagree); 2 could not evaluate (clone/commit missing, counter sha ≠ pin, work dir inside lane, fixture edit matched nothing).
- **`--mutant-counter PATH`**: grafts the mutant's bytes into synthetic FREEZE'/BASE' commits (plumbing in the clone only) so it passes its own `counter_not_frozen` guard, then applies the same expectations. Exit 1 = the self-test caught the mutant.
- `--list`, `--only ID,..`, `--keep`, `--work`, `--json-out` (refused inside the lane) exist; `--work` default is a fresh dir under `$TMPDIR`, removed at the end.

## Findings table

Env for runs: cwd = scratch, `TMPDIR=/fast/scratch/hyaku/kaidoku-r50/C2Selftest49/bw`, `HYAKU_SCRATCH=/fast/scratch/hyaku`.

| # | what | command | exit | evidence |
|---|---|---|---|---|
| F0 | Frozen counter at the real revs is green | `python3 -I -B tools/round-49/c2-mismatch.py --root <clone@7c678ae6> --rev HEAD --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d` | 0 | `atoms_total 9`, `mismatches 0`, `counter_sha256 = counter_sha256_at_freeze = 9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d`, 0.24 s |
| F1 | **Self-test, final, read-only sandbox** | `bwrap --ro-bind / / --dev /dev --proc /proc --bind $S $S --setenv TMPDIR $S/bw python3 -I -B selftest-r49-c2.py --json-out $S/final-bwrap.json` (2026-10-29T00:06:22Z–00:07:37Z) | **0** | `cases 40`, `passed 40`, `failed []`, `wall_sec 74.66` (load average 54; an earlier 34-case run on a lighter host took 23 s; green+battery alone is 13–18 s); stdout sha256 `5954a2c94fa7c7d61f626b5f5007dc752bcf7d1d62c4a488c34390e4874377ef` |
| F2 | **Writes nothing outside `$TMPDIR`** | same command; controls inside the same sandbox: `touch /home/vgpnk/probe-write` and `touch <lane>/probe` | F1 0; controls 1, 1 | both controls: `Read-only file system`; the self-test ran to completion with `/` and the lane read-only and only `$S` writable; `ls $S/bw` empty afterwards (work dir removed) |
| F3 | Per-case outcomes, all 40 match the expected file | `receipts/selftest-run-bwrap.json` `per_case` | — | green ×2 (`green`, `green-battery`: 16 mutations all ok, do-nothing red ×9); single-defect ×25 each red on exactly one atom (A1 ×3, A2 ×2, A3 ×5, A4 ×1, A5 ×2, A6 ×3, A7 ×3, A8 ×3, A9 ×3); `a9-battery` red A9 plus battery `genuine REV is not green`; `battery-incomplete` exit 1 with `mismatches 0` and `mutation set incomplete`; `freeze-is-rev` exit 1, all nine red; refusals exit 2: `x-counter-bytes` `counter_not_frozen`, `x-frozen-{edit,add,plan}` `frozen_path_changed`, `x-freeze-not-ancestor`, `x-bad-rev` `unresolvable rev or freeze`; CLI: `cli-noargs` 2, `cli-selftest-flag` 2 (`unrecognized arguments: --selftest`), `cli-jsonout-missing-dir` 1 (uncaught `FileNotFoundError`); known-blind ×2 exit 0 |
| F4 | **Self-test discriminates** | `selftest-r49-c2.py --mutant-counter <mutant>.py` for 22 counter mutants (`receipts/mutant-summary.txt`) | 1 for 21, 0 for 1 | 21 killed, each by the case designed for it (e.g. `a2-dead-commit-off`→`a2-dead-resolves`, `a3-keys-off`→`a3-extra-key`, `a3-appendonly-off`→`a3-log-rewritten`, `a7-ex64-off`→`a7-repinned`, `battery-failing-ignored`→`battery-incomplete`, `exit-always-0`→25 cases). Survivor `a2-real-ancestor-off`: an **equivalent mutant** — the real hash `663f30ee…822` is an ancestor of `decc5697` (`merge-base --is-ancestor` exit 0), so for any REV descending from FREEZE the `elif not r.ancestor(real, rev)` branch is unreachable |
| F5 | The first draft (34 atom-level cases) let 6 mutants live (`a1-stale-clause-off`, `a2-real-ancestor-off`, `a3-keys-off`, `a3-appendonly-off`, `a7-ex64-off`, `battery-failing-ignored`) and missed `a2-dead-commit-off` | first mutant pass (34 cases; passed 34/34 on its first run) | — | closed by cases `a1-stale-only`, `a3-extra-key`, `a3-log-rewritten`, `a7-repinned`, `battery-incomplete`, `a2-dead-resolves` and the `why_contains` fragments; the final 40-case pass is the 21/22 in F4 |
| F6 | An un-grafted mutant is meaningless | run a mutated counter against the real freeze | 1 (29 of 34 cases failed) | the counter's `counter_not_frozen` guard (exit 2) swamps any semantic edit; that is why `--mutant-counter` grafts the blob into synthetic FREEZE'/BASE' commits |

## Counter behaviour observed (for the L1 / `C2AtomSpec` / the R50 atoms)

1. **KNOWN-BLIND (exit 0 where the record is forged)**: the only `- A9 …` line inside an HTML comment (`<!--`/`-->` on their own lines) or inside a ``` fence is still counted. Cases `blind-a9-comment`, `blind-a9-fence`. The in-counter battery cannot see this, and the plan's R50-C2 rule "atoms inside an HTML comment or fenced block do not count" is this defect. The mutant `a9-comment-aware (fix)` turns the comment case red and the self-test flags it as a changed behaviour (exit 1 on `blind-a9-comment`): the blind cases are tripwires, not endorsements.
2. `--json-out` into a missing directory is an uncaught `FileNotFoundError` → Python exit **1**: an I/O failure is indistinguishable from "scored not met".
3. `--root` not a git repo → exit 2, `reason unresolvable rev or freeze`.
4. **No `--selftest`**: argparse `unrecognized arguments: --selftest`, exit 2. `--help` exits 0.
5. A battery can exit 1 on a **green record** (`mismatches 0`) when a mutation does not apply (`mutation set incomplete`): case `battery-incomplete` (drop the backticks round the S147 section anchor).
6. Unreachable/redundant clauses under the freeze: the A2 ancestor branch (F4). The A3 `keys` clause is reachable only by an **extra** key; a dropped key trips the per-key line check first.
7. Not covered (stated, not run): a merge-shape fixture (round-49 W2 F4: a benign merge makes `touched()` non-empty → fail-closed exit 2), `refs/replace`, `diff.renames=copies`, quoted/non-ASCII paths.

## Registry-row fields for `tools/round-49/c2-mismatch.py` (as observed; SKILL.md carries **0** `tools/round-49` rows today)

Seven-cell shape of the round-46 section (`tool | gate or probe - purpose | verdict map | self-test command | pinned-value path | write scope | owner`):

- **entry command**: `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev <REV> --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d [--battery] [--json-out <PATH>]`
- **verdict map**: `0=met, mismatches 0 over the nine atoms (and, with --battery, a clean battery); 1=not met, at least one atom red or a battery failure (the receipt is still printed), and also an uncaught OSError such as --json-out into a missing directory (a traceback, not a scored verdict); 2=could-not-evaluate: unresolvable rev or freeze, freeze not an ancestor of rev, frozen_path_changed, counter_not_frozen (own bytes differ from FREEZE's blob) or an argparse usage error`
- **self-test spelling**: the counter has none (`--selftest` → exit 2). The self-test is `python3 -I -B tools/round-50/selftest-r49-c2.py` (40 cases, exit 0; `--mutant-counter` for the discrimination check). Do not register `--selftest` on `c2-mismatch.py`.
- **purpose**: `gate — R49-C2 calibration: nine round-48 self-assessment atoms A1..A9 (declared freeze, dead hash, LOG pointers, wave accounting, receipt digests, S147/S148 rows, search log, SCORECARD A9 line) re-derived from git objects at --rev and the round-49 lane base, with a freeze-integrity walk, a counter-bytes pin and a 16-mutation plus do-nothing battery under --battery`
- **pinned-value path**: the counter's own blob at FREEZE (`counter_sha256 9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d`); in-source constants `R48_BASE 61b87d74…`, `R48_TIP 8847042a…`, `LANE_BASE e4f2cfa5…`; for the self-test, `tools/round-50/selftest-r49-c2.expected.json`.
- **write scope**: `--json-out` only; it reads git objects (`show`, `cat-file`, `ls-tree`, `log`, `diff`, `merge-base`, `rev-parse`) and never writes the lane or scratch.
- **owner**: kaidoku. Meaning words the round-48 rule accepts (`tools/round-48/meanings.py:59-62`): `0=` carries `met`, `1=` carries `not met`, `2=` carries `could-not-evaluate`; `0=not met` is rejected as opposite polarity.

## Limits and not-run

- The fixture needs the lane `.git` object store with `7c678ae6` and `decc5697` (`--lane`); a fleet clone lacking them → exit 2.
- Wall times are load-dependent (host load average 49–62 during the runs); 75 s is not a benchmark.
- The self-test does not run the counter against the lane's working tree and does not exercise `--root` = lane.
- No `--data-run`, no REA, no network. Scratch `/fast/scratch/hyaku/kaidoku-r50/C2Selftest49` is removed after this report. Tools installed: none.
