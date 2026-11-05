# ExecSelftests (round 91, lane kaidoku, executor seat)

Item: run every selftest and compile check of the round-91 and round-90 instruments once and report exit codes.

## Result

All 8 commands exited 0 in the lane (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD `fe1913d90`). The same 8 commands also exited 0 in a scratch clone checked out at the declaration commit `deb2765a55fef0e4e81500a027dfe59951b69e87`. No selftest failed, so there are no failing cases to report.

Lane HEAD `fe1913d90` descends from `deb2765a5` (`git merge-base --is-ancestor` rc=0). `git diff --stat deb2765a5 HEAD -- tools SKILL.md` is empty, so the instruments are byte-identical to the declaration commit. The clone run is therefore a reproduction at the declaration commit, not a different code path.

## Commands and results

Run from the lane root (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`), `TMPDIR=/fast/scratch/hyaku/kaidoku-r91/ExecSelftests/tmp`:

| # | Command | rc | Last output line |
|---|---|---|---|
| 1 | `python3 -I -B -X pycache_prefix=$S/pycache -m py_compile tools/round-91/upx-stop-boundary-repair.py tools/round-91/stop-boundary-battery.py tools/round-91/depth-blocks-v3.py tools/round-91/record-cells.py` | 0 | (no output) |
| 2 | `python3 -I -B tools/round-91/record-cells.py --selftest` | 0 | `selftest cases=4 failures=0` |
| 3 | `python3 -I -B tools/round-91/depth-blocks-v3.py --selftest` | 0 | `SELFTEST cases=6 failures=0` |
| 4 | `python3 -I -B tools/round-91/depth-blocks-v3.py --prose-proof --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 0 | `{"control_killed": true, "prose": {"rows": 0, "v2_accepts": true, "v3_accepts": false, "v3_table": false, "v3_table_problems": ["table:rows:0<3", "table:cells:0<4"]}, "table": {"rows": 3, "v2_accepts": true, "v3_accepts": true, "v3_table": true, "v3_table_problems": []}}` |
| 5 | `python3 -I -B tools/round-91/upx-stop-boundary-repair.py --selftest` | 0 | `SELFTEST cases=4 failures=0` |
| 6 | `python3 -I -B tools/round-90/upx-break-repair.py --selftest` | 0 | `SELFTEST cases=17 failures=0` |
| 7 | `python3 -I -B tools/round-89/depth-blocks-v2.py --selftest` | 0 | `SELFTEST cases=10 failures=0` |
| 8 | `python3 -I -B tools/round-90/upx-later-block-battery.py --selftest --work $S/work` | 0 | `SELFTEST cases=8 failures=0` |

Deviations from the literal command list, both deliberate:
- Command 1 adds `-X pycache_prefix=$S/pycache` instead of relying on `PYTHONPYCACHEPREFIX`. `-I` ignores `PYTHON*` environment variables, so the environment variable would not have redirected bytecode. The `-X` option is a command-line option and is honoured under `-I`. Confirmed: the `.pyc` files landed under the scratch pycache prefix, and `tools/round-91/__pycache__` does not exist in the lane.
- Command 8 adds `--work $S/work`, per the seat rule. The other commands take no `--work` flag (checked against each script's argparse), so they got `TMPDIR` only.

The same eight commands in the declaration-commit clone (`$S/clone`, checked out at `deb2765a5`) gave identical rc values and identical last lines. Command 4 gave an identical JSON line there too.

## Git status before and after (lane)

Before and after are identical (`diff` empty):

```
?? .ufo/waves/round-91/r91-w1.ready.dispatched
?? .ufo/waves/round-91/w1/
```

The two untracked entries were present before my run. `w1/` is my own seat directory, which I created with `mkdir -p`. No tracked file changed, and no file was modified in `tools/` (`find tools -newer` after the run returned nothing). Ignored `__pycache__` directories under `tools/` were not modified by this run.

## What these selftests do and do not establish

These are the instruments' own self-checks plus the depth prose-proof control. They establish that the scripts run, that their internal cases pass at the declaration commit, and that the prose-proof control kills the v3 accept rule on prose while the table form is accepted. They do not establish the frozen counter labels (for example `refused 8 of 8; unsafe 0; intact 4 of 4`, `P1 6 of 6; P2 4 of 4; P3 4 of 4`, or `blocks 31, resolved 31, required-shaped 1/1`). Those belong to the C1 and C2 items.

## Environment and installs

- `upx` at `/usr/bin/upx`, version 5.2.0 (`upx --version`). Not installed or changed by this seat.
- Python from the bytecode tag `cpython-314`.
- No installs, upgrades, or pacman calls by this seat.

## Files written

Seat directory `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ExecSelftests/`:
- `git-status-before.txt`
- `git-status-after.txt`
- `logs/lane/*.log` (one per command) and `logs/lane/summary.tsv`
- `logs/declaration-clone/*.log` and `logs/declaration-clone/summary.tsv`

Report (path given in the seat spec): `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-91/w1/ExecSelftests.md` (this file).

Scratch `/fast/scratch/hyaku/kaidoku-r91/ExecSelftests` (clone, tmp, work, pycache, run.sh) is removed before yield.

## Checks the main agent should run

Nothing further is needed from this seat for the selftests. The main agent should run the frozen counters (`stop-boundary-battery.py`, `upx-later-block-battery.py --repair-cmd tools/round-91/upx-stop-boundary-repair.py`, `depth-blocks-v3.py --expect-blocks 31 --expect "blocks 31, resolved 31, required-shaped 1/1"`) in their own seats.
