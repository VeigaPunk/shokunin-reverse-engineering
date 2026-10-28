# R49 wave 1 — scratch-discipline audit and `--help` no-write check (seat C1TmpScratch)

Draft tree audited (read-only): `.ufo/waves/round-49/draft/tools/round-49/` plus the draft helpers `mkclone.sh`, `run-ctl.sh`, `c2-after.py`. Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Probes ran only in `/fast/scratch/hyaku/kaidoku-r49/C1TmpScratch/` (removed before yield); receipts copied to `w1/C1TmpScratch/`.

## Verdict

**Not clean.** Every draft tool's `--help` makes zero write syscalls (verified by strace). The scratch-discipline audit found **one guard that can reach the fleet repo (F1), one helper that commits into whatever repo it is pointed at (F2), and five routed defects (F3–F7)**: two code paths write under `/tmp` when `TMPDIR` is unset, one control driver writes its fixtures into the cwd (the lane's frozen `tools/round-49/` when run from the lane), and the REA capture child does not pin `TMPDIR`. Nothing was patched and no data or control run was executed. The L1 should fold F1–F5 before the single freeze.

## `--help` no-write check (strace, `-e trace=openat,mkdir,mkdirat,rename,renameat2,unlink,unlinkat,rmdir,symlink,symlinkat,link,linkat,truncate,creat`, run with `env -u TMPDIR -u HYAKU_SCRATCH`)

| tool | command | exit | stdout sha256 (first 16) | write-like syscalls |
|---|---|---|---|---|
| c1-counter.py | `python3 -I -B c1-counter.py --help` | 0 | ddf84ff1fc293078 | 0 |
| c1-controls.py | `python3 -I -B c1-controls.py --help` | 0 | f6389acd3489b1da | 0 |
| c1-oracle.py | `python3 -I -B c1-oracle.py --help` | 0 | c6ab72422c0c9a4d | 0 |
| c1-run.py | `python3 -I -B c1-run.py --help` | 0 | 055a9f95e70eaaa0 | 0 |
| c1-run.sh | `bash c1-run.sh --help` | 0 | 055a9f95e70eaaa0 | 3, all bash's own `/dev/null` redirect; none into the tree |
| c2-mismatch.py | `python3 -I -B c2-mismatch.py --help` | 0 | e31c7c1d868696946 | 0 |
| mkclone.sh | `mkclone.sh --help` | 2 (`dest must be under …`) | — | 0 |
| c2-after.py | `python3 -I -B c2-after.py --help` | 1 (traceback at `assert` line 11, before any write) | — | 0 |
| run-ctl.sh | `run-ctl.sh --help` | 1 (`$2: unbound variable`, before any write) | — | 0 |

Note on my own invocation: my first attempt ran `python3 -I -B c1-run.sh --help` (a shell script run as Python) and exited 1. That was my error, not a tool defect; the wrapper is run with `bash`, as above.

Argparse runs before any `makedirs`/`mkdtemp` in `c1-controls.py` (`parse_args` at line 1289, scratch base created at 1291–1297), so `--help` writes nothing there.

## Scratch-discipline audit (per tool)

| tool | `TMPDIR`/`HYAKU_SCRATCH`/`--work` handling | verdict |
|---|---|---|
| c1-counter.py | `scratch_root()` (452–463) = `--work` > `$HYAKU_SCRATCH` > `/fast/scratch/hyaku`; deliberately avoids `gettempdir()` (R44-SCR-TMP comment). REA rerun pins `env['TMPDIR']=d` (1880). Selftest uses `scratch_root()` (2783, 2792). | clean (writes); hardcoded literals see F6 |
| c1-run.py | `--scratch`/`$HYAKU_SCRATCH` + `/kaidoku-r49`; REA child pins `TMPDIR=run_dir` (547); evidence writes only under `--evidence-root` (1034). | clean |
| c1-controls.py | scratch base via `--work`/`HYAKU_SCRATCH` (1291–1295, `mkdtemp(dir=base)`); **REA dev-arm capture does not pin `TMPDIR` (489–506)**; **`--fixtures-root` default is cwd-relative (1271, 98, 1420)**. | defects F4, F5 |
| c1-oracle.py | `--work` optional; without it `tempfile.mkdtemp(prefix=…)` with no `dir` (1236–1237) → `$TMPDIR` else `/tmp`; `HYAKU_SCRATCH` ignored. | defect F3 |
| c2-mismatch.py | no temp use; battery overlays are in-memory over `git show`/`diff`; only write is `--json-out` (634). Git subcommands are read-only (`show`, `cat-file`, `merge-base`, `ls-tree`, `rev-parse`, `log`, `diff`). | clean (confirmed by strace on a dev clone, see below) |
| mkclone.sh | scratch guard is a `case` glob (line 7); `rm -rf "$D"` (8) | defect F1 (traversal) |
| c2-after.py | no scratch or lane guard; `git add -A` + `git commit` in `D` (50) | defect F2 |
| run-ctl.sh | exports `HYAKU_SCRATCH` but not `TMPDIR` (6); `rm -rf "$W/ctl-work" "$W/ctl-out"` unguarded (8) | F4 (no TMPDIR pin reaches REA), F7 |

## Findings

| id | sev | where | what | evidence (exact) | not run because |
|---|---|---|---|---|---|
| F1 | high (guard) | `mkclone.sh:7–8` | The scratch guard is a glob on the raw string and `rm -rf "$D"` follows. `..` passes it. | `case "/fast/scratch/hyaku/kaidoku-r49/../../../../home/vgpnk/Projects/shokunin" in /fast/scratch/hyaku/kaidoku-r49/*) echo MATCH;; esac` → `MATCH`; `realpath -m /fast/scratch/hyaku/kaidoku-r49/../../../../home/vgpnk/Projects/shokunin` → `/home/vgpnk/Projects/shokunin` (the fleet root). | running it would delete the fleet repo |
| F2 | high if misused | `c2-after.py:10–11, 50` | No scratch/lane guard. Its only check is `git rev-parse --show-toplevel == D`, which holds for the lane path too. It then runs `git add -A` and `git commit -q -m 'dev after'` (no `-c` identity) and overwrites `corpus/lessons/round-49.md`, `corpus/SOURCES.md`, `SCORECARD.md` in `D`. | `python3 -I -B c2-after.py <lane>` would pass the assert and commit the lane. Same class as the run-6 incident. | would commit the lane |
| F5 | medium (pre-freeze lane write) | `c1-controls.py:1271–1273` (default `tools/round-49/control-fixtures`, relative, not `abspath`), `:98, :105, :1420` (`write_fixtures` on build without `--from-fixtures`), docstring `:67` ("writes only --out, --work and --json-out") | `--build-only` writes control fixtures to the **cwd**, not `--root`, `--work` or `--out`. Run from the lane root it writes into the lane's frozen `tools/round-49/control-fixtures`, untracked, where the freeze could commit stale bytes. `run-ctl.sh:9` is safe only because it `cd`s into the clone. | Probe: `cd $S/cwd-probe2 && python3 -I -B $CLONE/tools/round-49/c1-controls.py --root $CLONE --controls c4 --build-only --work $S/cwd-probe2/work --out $S/cwd-probe2/out --json-out …` (exit 0). Files created under the cwd: `tools/round-49/control-fixtures/c4/manifest.json` and four `corpus/evidence/round-49/c1/*/after.json`. `$CLONE/tools/round-49/control-fixtures` does not exist. Listing: `w1/C1TmpScratch/probes/c1-controls-build-only-c4.cwd-files.txt`; manifest sha256 `1b105b78a6873660b48eeec5ba0a39f2c30984742590513ac15bea0d509c5228`. | the probe itself was run in scratch; the lane was not |
| F3 | medium (routed) | `c1-oracle.py:1232–1237`, `:1400–1407` | Without `--work` the scratch is `tempfile.mkdtemp(prefix="r49-c1-oracle-")` with no `dir`. It lands in `$TMPDIR` or `/tmp`, ignoring `HYAKU_SCRATCH`. This contradicts `c1-counter.py:452–456`, which says why it never calls `gettempdir()`. | `env -u TMPDIR python3 -I -c 'import tempfile; print(tempfile._candidate_tempdir_list())'` → `['/tmp', '/var/tmp', '/usr/tmp', …]`; with `TMPDIR=$S` the first entry is `$S`. Not run: running the oracle without `--work` writes under `/tmp`, which is the defect. | writing under `/tmp` is the defect |
| F4 | medium (routed) | `c1-controls.py:489–506` (`capture_real`), `run-ctl.sh:6` | The REA child gets `dict(os.environ)` with only `PATH` pinned; `TMPDIR` is not set. REA creates its per-run root with `PrivateRuntimeRoot.create({prefix:"rea-firmware-"})` (`dist/cli-runtime/cli.js:15035`) → `mkdtemp(join(options.parent ?? tmpdir(), prefix))` (`dist/cli-runtime/PrivateRuntimeRoot-DAy0PiBM.js:241`). `os.tmpdir()` honours `TMPDIR` and falls back to `/tmp`. `c1-counter.py:1880` and `c1-run.py:547` do pin it; `c1-controls` does not. | `env -u TMPDIR node -e 'console.log(require("os").tmpdir())'` → `/tmp`; `env TMPDIR=/x/y node …` → `/x/y`. The positive arm (`control_pos`, CTL-C1-POS) and every `run-ctl.sh` run go through this capture. Not run (it would invoke REA and create `/tmp/rea-firmware-*`). | a live REA capture |
| F6 | low (literals; no write) | `c1-counter.py:2657` (`rehost`), `:2846`, `:3053`, `:3131`, `:3135`; `c1-controls.py:694`, `:955` | Hardcoded `/fast/scratch/hyaku/kaidoku-r49/...` strings ignore `HYAKU_SCRATCH` and `--work`. Consequence: the CTL-C1-POS arm rewrites every captured receipt's `output_directory` to a path REA never wrote to (`c1-controls.py:955–958`). The positive arm therefore does not exercise where REA actually wrote, and the selftest/`rehost` projection assumes the default root. | source reads only; no write | — |
| F7 | low | `run-ctl.sh:5–8` | `D` and `W` are unguarded; `rm -rf "$W/ctl-work" "$W/ctl-out"` runs for any `W` (a relative `W` resolves against cwd). The usage line says "under /fast/scratch" but nothing enforces it. `--help` as `$1` fails with `$2: unbound variable` (exit 1, no write). | `run-ctl.sh --help` → exit 1, strace 0 writes | the rm path is the hazard; not exercised |

Also checked and NOT defects: `c1-counter` `show`/`ls-tree`/`log`/`rev-parse`/`merge-base`/`cat-file` (all read-only); `c1-counter`'s `npx` writes `~/.npm/_npx` (host npm cache, not `/tmp`, disclosed as inherent to `npx -y`); `c2-mismatch` writes only `--json-out`.

## Dev-clone check of C2 (read-only, scratch clone at the dev freeze)

`python3 -I -B $CLONE/tools/round-49/c2-mismatch.py --root $CLONE --rev $H --freeze $H --battery --json-out $S/c2-battery.json` on the mkclone dev freeze (no `c2-after.py` landing): exit 1, `atoms_total 9`, `mismatches 9`, `battery.failing` = `['genuine REV is not green', 'mutation set incomplete: 0 of 11']`. Expected for a pre-landing tree. strace shows no write-like syscall except the `--json-out` file. Stdout sha256 `ff6a6b80683eafa9fc25ad277ca9cebf142161ad6ffafcc21534e16f49e3cea9`. Copies: `w1/C1TmpScratch/c2-battery-devclone.{json,stdout}`.

## Fixes proposed to the drafts (not applied)

1. **F1** `mkclone.sh`: `D=$(realpath -m "$1")`; require `case "$D" in /fast/scratch/hyaku/kaidoku-r49/?*)` on the resolved path; refuse if `$D` equals the lane or fleet root.
2. **F2** `c2-after.py`: refuse unless `realpath(D)` is under `/fast/scratch/hyaku/kaidoku-r49/` and `!= L`.
3. **F5** `c1-controls.py`: `ap.add_argument('--fixtures-root', default=None)`, then after `root` is resolved, `fixtures_root = os.path.abspath(a.fixtures_root or os.path.join(root, FIXTURES))`; fix the docstring at line 67 to list the writes.
4. **F3** `c1-oracle.py:1237`: `work = tempfile.mkdtemp(prefix="r49-c1-oracle-", dir=scratch_root())`, with `scratch_root()` as in `c1-counter.py`.
5. **F4** `c1-controls.py:489`: `env['TMPDIR'] = work` (the same pin as `c1-counter.py:1880`).
6. **F6/F7**: derive the literal scratch strings from the same root, or state them as provenance literals; guard `run-ctl.sh`'s `rm -rf` by requiring `W` under the scratch segment.

## Verification gaps / not run

- Not run: any `--data-run`; `c1-run.sh` in any non-help mode; `c1-oracle.py` without `--work` (writes `/tmp`); `c1-controls.py --selftest`; a live REA capture (F4); `mkclone.sh` with a traversal path (F1); `c2-after.py` against the lane (F2); `run-ctl.sh` (not run; `CTL` controls not scored).
- Scratch hygiene for my probes: all probe writes landed under `/fast/scratch/hyaku/kaidoku-r49/C1TmpScratch/`; a `find /tmp` for the oracle/REA/counter patterns after my probes found nothing from my runs. Disk guard before the heavy-ish passes: `/tmp` 21% used, `/fast/scratch/hyaku` 36% used (518G free).
- No install or upgrade performed (no tool added; `strace` was already present at `/usr/bin/strace`).

## Artifacts (`w1/C1TmpScratch/`)

- `tool-sha256.txt`: sha256 of every draft tool and helper audited (e.g. `c1-controls.py` 209f0f4a…a4, `c1-counter.py` d6d70cb7…79, `c1-oracle.py` 80f8212d…fb, `c1-run.py` f9161ff3…fb, `c2-mismatch.py` 90fa4722…a4, `mkclone.sh` d7d2cd71…95, `run-ctl.sh` f74939ec…73, `c2-after.py` cb7f35d6…d8).
- `strace/*.log` + `*.stdout`: the `--help` write audit, one log per tool; `mkclone.out`, `c2after.out`, `runctl.out` for the helpers.
- `probes/c1-controls-build-only-c4.{stdout,cwd-files.txt}`: F5 probe output and the list of files it created under the cwd.
- `c2-battery-devclone.{json,stdout}`: the read-only dev-clone C2 battery.
