# ExecRunbook — round 49 wave 1 (pre-freeze): the L1 after-freeze runbook

**Verdict: DELIVERED, WITH ONE BLOCKING FINDING FOR THE L1 BEFORE THE FREEZE.**
`w1/ExecRunbook/after-freeze.sh` is an executable, phase-driven runbook (`pre`, `score-before`, `data`, `land-evidence`, `post`; `--dry-run`, `--rev`, `--yes`). I ran it end-to-end on a scratch clone (`REHEARSAL=1`) and with `--dry-run` on the real lane. It did **not** run against the real lane, and I never invoked `c1-run.sh --data-run`.

1. **Blocking: a fleet-root misroot already exists.** `/home/vgpnk/Projects/shokunin/tools/round-49/control-fixtures/{c1,c4,c5}/**` holds 23 untracked files (≈1.1 MB), written 17:55:03–17:55:24 (-03). `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | grep -c tools/round-49` prints 23. The lane draft `tools/round-49/` has **no** `control-fixtures/`, so those 23 files are the only copy of the CTL-C1 fixtures. Cause: `c1-controls.py:88` sets `FIXTURES = 'tools/round-49/control-fixtures'` (relative), and `--fixtures-root` defaults to it (`:1271`), so a run with cwd = fleet root writes into the fleet. A before/after status diff baselines this away. The runbook's `misroot_absolute` check catches it (it fails `pre` now). The L1 must rebuild the fixtures inside the lane (`--fixtures-root <LANE>/tools/round-49/control-fixtures`, or cwd = lane) and remove the fleet copy. The plan requires every control fixture to exist in the FREEZE commit, and the runbook's `pre` fails if they do not.
2. **The runbook's mechanics are verified.** Rehearsal results (clone, dev freeze `f2e3be06…`):
   - `score-before`: C1 exit 1 with `carriers_matched 0` and all six documentation bindings false; C2 exit 1 with `mismatches 9`.
   - `data`: the runner guard refuses the committed evidence root without `--data-run` (exit 2); the data run exits 0 for 4 carriers; `provenance.json` records the `/kaidoku-r49/` scratch `output_directory`.
   - `post`: C1 reaches `carriers_matched 4`, `failing []`, `frozen_path_changed []`, with only the six doc bindings false (the docs are not landed in the clone); C2 on the `c2-after.py` GREEN fixture gives `mismatches 0`, `battery.failing []`, 11 mutations ok, do-nothing red ×9, exit 0.
   - The rehearsal covers every step except a C1 all-green. That arm is CTL-C1-POS (`run-ctl.sh`), not run by me.
3. **Stale comment in `c1-run.py:337-343`** restates the round-44 two-ways sentence: `evidence (default)` plus a quoted plan sentence ("names a corpus/evidence/round-49/c1/ path") that the plan does not contain. The plan says the `/kaidoku-r49/` scratch segment, and the CLI default (`:799`) is `scratch`. The comment and the `build_plan(outdir_mode='evidence')` default (`:330`) contradict the plan in frozen bytes. Wave 2 would cite it.

## Findings

| # | Finding | Command / location | Result |
|---|---|---|---|
| F1 | Fleet-root misroot, 23 files (blocking, see above) | `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall \| grep -c 'tools/round-49'` | `23`; `find /home/vgpnk/Projects/shokunin/tools/round-49 -type f` lists c1 (5), c4 (5), c5 (13) files, mtimes 17:55:03–17:55:24 |
| F2 | `c1-controls.py` default fixture root is cwd-relative | `c1-controls.py:88`, `:1271` | Same defect class as M38-7 and M39. Wave 2 could repeat it if run from the wrong cwd |
| F3 | Stale / contradictory comment, wrong default in frozen runner | `c1-run.py:330`, `:337-343` vs plan P49-C1 and `:799` | See finding 3 above |
| F4 | `disk-guard.sh status` is expensive, so the runbook uses `df` instead | `time disk-guard.sh status` | 67 s wall, 7m12s user, 3m59s sys. Replaced by `df -B1G --output=avail` (≥ 20 GiB gate) |
| F5 | The runner and the counter pass the **ambient** environment through to REA (they override only PATH, TMPDIR, `REA_UNBLOB_COMMAND`) | `c1-run.py:545` (`env = dict(os.environ)`), `c1-counter.py:1878` | This seat's env carries `REA_BINWALK_COMMAND`, `REA_PWNTOOLS_PYTHON`, `REA_WAKARU_COMMAND`, `REA_ADB_PATH`, `REA_APKTOOL_COMMAND`, `REA_JADX_MCP_JAR`, `npm_config_yes=true`. The runbook records them in `pre` (`l1/env-pre.txt`) and `post` diffs them (`env-post.txt`); a change fails the run. Secret-shaped names are filtered out |
| F6 | Overrides that would silently redirect the runner: `C1_RUN_PY` (`c1-run.sh:42`), `C1_UNBLOB_LOG_TEE=0`, `C1_REAL_UNBLOB`, `C1_LOG_COPY`, `KAIDOKU_C1_DATA_RUN`, `PYTHONPATH` | `pre` | Gated. Negative test: `C1_RUN_PY=/x after-freeze.sh pre` prints `FAIL env C1_RUN_PY is set (/x)` |
| F7 | `--scratch` appends `/kaidoku-r49`, so `--scratch /fast/scratch/hyaku/kaidoku-r49/l1` gives `…/l1/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/rea-out` | `c1-run.py` `scratch_root`; rehearsal `provenance.json` | Contains `/kaidoku-r49/`, passes the counter's `run_provenance_ok`. The run dir carries the PID and is deleted after the run |
| F8 | `/fast/scratch/hyaku/kaidoku-r49/l1` already holds the L1's draft-phase clone, `ctl-out`, `ctl-work`, `devarm`, `self`, `popper.html`, `sysexits.html` | `ls /fast/scratch/hyaku/kaidoku-r49/l1` | No collision: the data run writes `l1/kaidoku-r49/…`. Keep the pre-freeze snapshots out of any committed path |
| F9 | Writes outside lane evidence root, wave dir and scratch | strace -f of the rehearsal `data` phase, `w1/ExecRunbook/data-run-outside-writes.txt` | Only `npx`: `~/.npm/_cacache/{tmp,index-v5}`, `~/.npm/_npx/ad9a3fdbcad992c6/concurrency.lock`, `~/.npm/_logs/<ts>-debug-0.log`. Every `npx -y rea-agents@6.5.0` also opens a TCP/443 connection to the npm registry (`strace -e connect`, `npx-version-connect.strace`; cache hit, version `6.5.0`). The data run and the counter's 4 reruns each do this. Nothing under `/tmp`, the fleet root or the lane root |
| F10 | `jj-lane.sh state` is pure git; it needs `refs/remotes/origin/main` and reports `head=detached` | `jj-lane.sh state <LANE>` → `state branch=main local=e4f2cfa5… remote=e4f2cfa5… ahead=0 behind=0 head=detached tracked=0 untracked=1` (exit 0) | The runbook gates on `behind=0` and `tracked=0`, and on `local` (main tip) `== git rev-parse HEAD` |
| F11 | `jj-lane.sh commit` refuses `.ufo` exactly and `.ufo/state*` only, so `.ufo/waves/round-49/…` pathspecs are committable | `jj-lane.sh:513`, `repo_path_allowed` | `land-evidence` commits only `corpus/evidence/round-49/c1`, `--as kaidoku`. **Not run** (it mutates the lane); rehearsed with `git commit` in the clone only |
| F12 | SOURCES `opened` for S138/S139 is already `2026-10-28`, so the C1 `sourced` binding needs only a `used-by` edit, which `registry-immutable.sh` permits (columns 9, 11, 12) | `awk -F'\|' '/^\| S13[89] /' corpus/SOURCES.md` | No conflict between the C1 `opened == 2026-10-28` binding and CORPUS rule 2 |
| F13 | C1 before-score takes ≈1 s and needs no REA run; the C1 after-score reruns REA ×4 (≈10 s total in rehearsal) | `score-before`, `score-after` receipts | Scoring `--rev FREEZE` can be done before data. The runbook does it in `score-before` |
| F14 | Evidence gitignore: all 51 files of the evidence tree are trackable | `git check-ignore -v corpus/evidence/round-49/c1/v1le/{stdout.log,unblob.log,run.json}` → exit 1; clone `git ls-files … \| wc -l` = 51 = files on disk | `*.log` is not ignored, so `jj-lane` directory tracking will not drop receipts |

## Commands (resolved argv; `<FREEZE>`, `<REV>` placeholders; paths are the real lane)

Run as `FREEZE=<hash> w1/ExecRunbook/after-freeze.sh before-landing`, then land the docs by hand, then `… after-landing`. The script prints each argv before running it. Full dry-run transcript: `w1/ExecRunbook/dry-run-real-lane.txt`.

| Step | Argv | Expected exit | Writes |
|---|---|---|---|
| pre (a) | `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 0 | none |
| pre (b) | `git merge-base --is-ancestor <FREEZE> HEAD` (and `refs/heads/main`), `diff <(git ls-tree -r <FREEZE> -- <frozen set>) <(git ls-tree -r <main> -- <frozen set>)`, `git diff --name-only <FREEZE> -- <frozen set>`, `git log -m --diff-merges=first-parent --name-status --pretty=format: <FREEZE>..<main> -- <frozen set>`. Frozen set = `tools/round-49`, `plans/round-49-claims.md`, `tools/round-42/{fixtures,prior-pins,rea-pkg}.json`, `tools/round-42/c1-counter.py`, `tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`, `corpus/evidence/round-44/oracle` | each empty / equal | none |
| census before | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`; `… census --root … kaidoku`; `git show e4f2cfa5…:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 0, 0, 146 | `$WAVE/l1/census/` |
| misroot before | `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` plus `misroot_absolute`; lane `status --porcelain -uall -- . ':!.ufo'`; marker `touch /fast/scratch/hyaku/kaidoku-r49/l1/misroot.marker` | fails now (F1) | `$WAVE/l1/misroot/`, scratch marker |
| score-before C1 | `cd <LANE> && python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev <FREEZE> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r49/l1/counter-c1-before --json-out <LANE>/.ufo/waves/round-49/l1/scores/c1-before.json` | 1 (`carriers_matched 0`) | json-out + work dir |
| score-before C2 | `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev <FREEZE> --freeze <FREEZE> --json-out <LANE>/.ufo/waves/round-49/l1/scores/c2-before.json` | 1 (`mismatches 9`) | json-out |
| data (plan) | `cd /fast/scratch/hyaku/kaidoku-r49/l1 && <LANE>/tools/round-49/c1-run.sh --dry-run --lane-root <LANE> --scratch /fast/scratch/hyaku/kaidoku-r49/l1 --freeze <FREEZE>` | 0 | none |
| data | `cd /fast/scratch/hyaku/kaidoku-r49/l1 && env TMPDIR=/fast/scratch/hyaku/kaidoku-r49/l1/tmp <LANE>/tools/round-49/c1-run.sh --lane-root <LANE> --scratch /fast/scratch/hyaku/kaidoku-r49/l1 --freeze <FREEZE> --data-run --timeout 900` | 0 | `<LANE>/corpus/evidence/round-49/c1/` + scratch (+ F9) |
| land-evidence | `jj-lane.sh commit <LANE> --as kaidoku -m '…' -- corpus/evidence/round-49/c1` (needs `--yes`) | 0, prints `landed <hash>` | lane history (**not run**) |
| score-after C1 | `python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 <PKG> --work …/l1/counter-c1-after --json-out …/l1/scores/c1-after.json`, then `… --verify-receipt …/c1-after.json` | 0, 0 | json-out + work dir |
| score-after C2 | `python3 -I -B tools/round-49/c2-mismatch.py --root <LANE> --rev <REV> --freeze <FREEZE> --battery --json-out …/l1/scores/c2-after.json` (plus a no-battery run) | 0 | json-out |
| census after | validate and census as above, `git show <REV>:corpus/SOURCES.md`, `bash tools/round-38/registry-immutable.sh <LANE> e4f2cfa5… <REV>` | 0, 0, rows, 0 | `$WAVE/l1/census/` |
| misroot after | status diff vs before; name and content probes (fleet, lane root, `/tmp`); tracked strays `unblob.log` and `glibc-tag-object.json` unmodified; `misroot_absolute` | 0 findings | `$WAVE/l1/misroot/` |

`<LANE>` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `$WAVE` = `<LANE>/.ufo/waves/round-49`.

**Write scope.** `guard_write` aborts with exit 2 on any script-owned write outside `<LANE>/corpus/evidence/round-49/c1`, `<LANE>/.ufo/waves/round-49/l1/**` or `/fast/scratch/hyaku/kaidoku-r49/l1/**`.
- Unit test: `/etc/x`, `/s/../home/x`, `/sx` (a sibling prefix) and `/s/a/../../tmp/y` are refused; `/l1/../s/ok` is allowed.
- `land-evidence` also writes lane history (outside those paths) and needs `--yes`.
- The F9 `~/.npm` writes are outside the guard and unavoidable.

## Rehearsal receipts (scratch clone; the real lane was not touched)

Each row below is a step in `rehearsal/after-freeze/<step>.json` or `rehearsal/census/` (stdout sha256 prefix; `exit` is the step's own exit code; times UTC 2026-10-28). Full values are in the per-step JSON.

| Step | Exit (expected) | stdout sha256 (prefix) |
|---|---|---|
| c1-before | 1 (1) | `b4c6de6b41708d07` |
| c2-before | 1 (1) | `18c229129b3a7f1e` |
| c1-run-guard (no `--data-run`) | 2 (2) | `e3b0c44298fc1c14` (empty) |
| c1-run-data (4 REA runs) | 0 (0) | `ab0cc21dd892fdd6` |
| c1-after | 1 (0): `carriers_matched 4`, `failing []`, 6 doc bindings false | `b795cab58bb32859` |
| c1-after-verify-receipt | 0 (0) | `3b3b67a592280259` |
| c2-after on the RED clone | 1 (0): `9`, as expected (no landing) | `41a095d64aba1e80` |
| c2-after on the GREEN `c2-after.py` clone (DEV_AFTER `a0526c6c…`, earlier run, `reh-4`) | 0: `atoms_total 9`, `mismatches 0`, `battery.failing []`, 11 mutations ok, do-nothing red A1..A9 | `f8cfe253dbf4236f…` |
| census-before-validate / -after-validate | 0 / 0 | `065a45eb8e760d65` (equal to `l1/sources-census-start.txt` minus its `exit=` line; 15 W04 warnings, final `kaidoku ok`) |
| census-before-counts / -after-counts | 0 / 0 | `7eb55d1014d465e6`; rows 146 → 146 in the clone |
| census-after-immutable (`registry-immutable.sh <LANE> BASE REV`) | 0 (0) | `e3b0c44298fc1c14` |
| misroot after (rehearsal, delta-only part) | 0 findings | status 69 lines before and after |

Counter receipt sha256 prefixes (`rehearsal/scores/`): `c1-after.json` `f30a6e6617854fef`, `c1-before.json` `ed94b336ae6809df`, `c2-after.json` `41a095d64aba1e80`, `c2-after-nobattery.json` `1516e6891afbfcba`, `c2-before.json` `18c229129b3a7f1e`. Draft file sha256 at attack time: `c1-counter.py d6d70cb7…`, `c1-run.py f9161ff3…`, `c1-run.sh 5ebb453f…`, `c2-mismatch.py 90fa4722…`, `carriers.json 829e3392…`, `c1-controls.py 209f0f4a…`, `plans/round-49-claims.md 984e1026…`.

**Negative gate tests (all fired):**
- A one-line change to a frozen file in the clone worktree gave `FAIL worktree differs from FREEZE in the frozen set`.
- An untracked `tools/round-49/__pycache__/x.pyc` gave `FAIL untracked file(s) under tools/round-49 or plans/`.
- `C1_RUN_PY=/x` gave the F6 failure.
- A synthetic fleet-status delta (3 lines dropped from the `before` snapshot) gave the name-hit and content-hit failures in `misroot_diff`.
- `control-fixtures` absent at FREEZE failed `pre` in the clone, as it will in the lane if the fixtures are not committed.

## Not run / limits

- **Not run:** any command against the real lane beyond `jj-lane.sh state`, `--dry-run`, and read-only git. Specifically not run: `jj-lane.sh commit`/`push`, `c1-run.sh --data-run`, the real C1/C2 scores.
- **Not run:** the C1 all-green arm (`post` with docs landed) and `controls/summary.json`. The `pre` check on `kill_rule_fires false` exists but has no file to read yet.
- The rehearsal ran in a clone, so the `jj` path (`state`, `commit`) differs from the lane; `jj-lane.sh state` was checked live on the lane only.
- `misroot_diff`'s content grep is bounded to new untracked fleet files ≤ 1 MiB. Sibling lanes also write the fleet, so a hit is a judgment call, not an automatic fault. `misroot_absolute` has the same property, but today its only hits are the 23 files of F1.
- The strace for F9 was taken on the pre-final script version. The final edits changed only gates (frozen-gate refactor, env checks, absolute misroot), not what the `data` step executes.
- `final dry-run on the real lane` currently exits 1: F1 (`tools/round-49` at the fleet root) plus the gates that cannot pass before a freeze exists (FREEZE unset).

Files: `w1/ExecRunbook/after-freeze.sh` (sha256 `195575a9e781dee8…`), `dry-run-real-lane.txt`, `dry-run-clone-transcript.txt`, `rehearsal-transcript.txt`, `data-run-outside-writes.txt`, `npx-version-connect.strace`, `rehearsal/**` (per-step receipts, scores, census, misroot; evidence run/provenance JSON under `rehearsal/evidence-run-json/`). Tooling installed: none.
