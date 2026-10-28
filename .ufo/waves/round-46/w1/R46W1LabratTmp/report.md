# R46W1LabratTmp — labrat report (single experiment, run in-seat)

Parent: `R46W1ProbeTmp`. Full evidence and cross-cutting findings: `../R46W1ProbeTmp.md` and
`../R46W1ProbeTmp/evidence/`. This file is the experiment log only.

## Hypothesis

`tools/round-46/attest.py` (the round-46 C1 battery) writes nothing outside the scratch root it is given.

## Verdict

**Not falsified** for the canonical invocation (`python3 -I -B`, explicit `HYAKU_SCRATCH`): 2523 write-class file
syscalls, 2208 resolved inside the given root, 314 `/dev/null` device opens, **0** unresolved, and exactly **1**
write outside the root — the `--json-out` receipt this seat explicitly asked for, inside its own report directory.
Every one of the 641 paths the run created under the scratch root was gone after exit.

Two scoped exceptions, both reported as findings in the parent report (F4, F5-class): CPython writes
`<tools>/__pycache__/*.pyc` when `-B` is omitted (demonstrated on a copy; the lane already carries three such
files at 13:53/13:54/14:00, gitignored), and the `--json-out` channel is a legitimate write outside the scratch
root by design.

## Commands (exact) and outcomes

Environment for all: `S=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeTmp`, `HYAKU_SCRATCH=S`, `TMPDIR=S`,
cwd `/home/vgpnk/Projects/shokunin`, lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`--freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390`.

```
# baseline (as prescribed)
find /tmp /var/tmp -maxdepth 2 -newermt '-5 minutes' | sort      # 235 entries BEFORE any run — siblings' files

# the three assigned runs, each wrapped in:
strace -f -qq -y -e trace=%file -o $S/traces/<run>.trace -- \
  python3 -I -B <lane>/tools/round-46/attest.py --root <lane> [--selftest | --no-battery | (full)]

python3 -I -B <lane>/tools/round-46/attest.py --root <lane> --selftest
  -> exit 2, empty stdout: argparse requires --freeze/--rev even for --selftest   (documented form does not run)
python3 -I -B <lane>/tools/round-46/attest.py --root <lane> --freeze REV --rev REV --selftest
  -> exit 0, "ATTEST_SELFTEST: cases=16 failures=0"
python3 -I -B ... --no-battery
  -> exit 0, sha256(stdout)=8c55d92fc9cd0a40…, failing []
python3 -I -B ... (full battery)
  -> exit 0, sha256(stdout)=4fca83c63d4b3ca6…, forgeries_total 9 / v1_green 9 / v2_green 0 / genuine_green 1 / v2_crash 0

# post
find /tmp /var/tmp -maxdepth 2 -newermt '-5 minutes' | sort      # 307 entries; 255 new vs baseline,
                                                                 # all from other lanes (tameshi-*, ed.*, rc.strace, …)
find /tmp /var/tmp -maxdepth 3 \( -name 'kaidoku-r46-battery-*' -o -name 'fx-*' \)   # empty
ls $S | grep -c 'kaidoku-r46-battery'                            # 0
```

## Write-set attribution (r9 trace, attest battery)

| resolution | count |
|---|---|
| inside `$HYAKU_SCRATCH` | 2208 |
| `/dev/null` (device, no bytes) | 314 |
| outside, non-device | **1** — `<lane>/.ufo/waves/round-46/w1/R46W1ProbeTmp/c1-r9-receipt.json` (requested `--json-out`) |
| unresolved | **0** |

Relative-path writes (git's `.git/objects/...` under each fixture) were resolved through the `AT_FDCWD<…>` and
dirfd (`3</dir>`) decorations; the first, naive pass without dirfd resolution produced false positives and was
discarded rather than reported.

## Leftover paths with mtime

None from this experiment. Scratch root removed at exit; the injected-exception control (`run_battery` patched to
raise, on a copy) also exited 2 with no scratch directory left. The only surviving files with these mtimes are
pre-existing and not ours: `tools/round-46/__pycache__/{gate,attest,registry}.cpython-314.pyc`
(13:53:37, 13:54:50, 14:00:26, gitignored, written by earlier seats without `-B`).
