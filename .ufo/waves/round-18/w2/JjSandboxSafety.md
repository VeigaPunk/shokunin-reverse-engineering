PARTIAL

# JjSandboxSafety — security review of `W18/tools/jj-red-before.py` at REV

- **Target:** `.ufo/waves/round-18/tools/jj-red-before.py` at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. `ls-tree`: mode `100755`, blob `0d9b65f6…`. sha256 `cc2d7fb4…a892`, the same as the lane working-tree file. Line anchors below are `git show REV:<path>` line numbers. A bare `:N` means this file.
- **Seat:** author-side advisory (wave 2, falsify). Tools: jj 0.45.1, git 2.56.0, Python 3.14.8. No installs. No REA, Ghidra or carrier runs. I ran no jj and no git write in the lane.
- **Labels:** **[O]** = observed by a command below. **[I]** = inference.

## Verdict by axis

| Axis | Verdict | Evidence |
|---|---|---|
| Origin removal | **HOLDS** | `:244-273`. Only reads run between clone and `remote remove` (`:254-255`). The empty-`git remote` assertion is at `:260-263`. E3 [O]: `remote -v` empty; local config is only `core.*`; no `objects/info/alternates`; `.jj/repo/store/git_target` = `../../../.git`; refs = `heads/main` + fake `remotes/origin/main`; `jj-xdg` holds no repo-config entry. [I] jj wrote no `trunk()` alias because no remote is configured; the other seats' recent `~/.config/jj/repos` entries that carry one belong to repos with an origin. |
| Env scrub | **PARTIAL** | `_child_env` (`:113-125`) is passed to every `run()` on the evaluate path (`:158,166,244-278,313-318,351-352,377,389,409,503,525,552,576,600,626,659,700`). It is **not** applied to the selftest fixture builder (`:889-897`), whose scrubbed dict is built only *after* those git calls (`:898`). It is also not applied to the in-process `revpin` import (`:433-438`, `:673-678` → `revpin.py:71-76`, `subprocess.run` with no `env`). So the docstring claim "stripped from every child" (`:9`) is false → F2, F4. |
| HOME/XDG isolation | **HOLDS** (jj) | `:118-125`, used at `:241`/`:277-278` and `:312-314`. E3 [O] used canary `XDG_DATA_HOME`/`XDG_STATE_HOME`/`XDG_CACHE_HOME`: canaries 0 entries, `jj-home` 0, `jj-xdg` 0. `grep -rl` for both sandbox paths in the real `~/.config/jj/repos/` → exit 1 (no residue). Git children keep the operator HOME by design. The observed `~/.config/git/config` has no `hooksPath`, `fsmonitor` or `include`. Its `filter.lfs.*` is inert: 0 `.gitattributes` at REV. |
| rmtree target guard | **HOLDS** | Only `mkdtemp` return values reach `rmtree`: `:229→:233`, `:363→:722`, `:904→:984`, and none is reassigned. `_refuse_inside` (`:105-110`) uses `realpath`; E7b [O] shows a symlink into the lane is refused. Caveats, no reachable exploit: the guard runs after creation (`:238`, `:905`), and there is no prefix assert at rmtree time (w1 `SentinelSandbox.md:137` F9 was not adopted). No `/tmp/jj-red-before-*` dir was left after E1/E2/E5/E6 [O]. |
| `-R` on jj calls | **HOLDS** | There are exactly two jj argv. `:277-278` is `git init --colocate` with `cwd=sb` (`-R` can't be used with init, per w1 F4). `:313-314` is `-R sb commit` with `cwd=sb`. The executed child tools (`citation-drift-probe.py`, `custody-pair.py` at REV and B, `revpin.py`) contain `jj` only in comments [O, grep]. |
| Any path that writes LANE or the fleet repo? | **YES — 3 conditional paths** | F1 is driven by data, F2 by env, F3 by how the tool is invoked. None fires under the documented invocation (`SKILL.md:589`, `verify.py:36,190-191`: `python3 -I -B`) with the REV table (0/60 escaping entries) and an env with no absolute `GIT_DIR`/`GIT_INDEX_FILE`. E1 [O] reproduced the wave-1 shape: exit 0, 14/14 held, with the clone's refs, HEAD and index hashes identical before and after. |

## Findings

### F1 — MEDIUM (latent): the off-branch rewrite writes any path a pointer-table entry names
- **Exploit path:**
  - `pick_cited_line` (`:211-216`) takes `e["file"]` verbatim from `sb/.ufo/gates/citation-drift/pointer-table.json`. That file is lane-committed data, edited by many seats.
  - `commit_off_branch` then does `Path(sb, cited_file)` and `write_text` (`:295-301`). An absolute `file` makes `Path` discard `sb`. A `../` file walks out of it. The same applies to the marker at `:307` if the lane commits a symlink.
  - `_refuse_inside` exists but is never applied to this target.
- **Evidence:**
  - E2 [O]: one prepended `exact` entry, `file=$W/victim-abs/SCORECARD.md` or `file=../../jjsbx-JQvPXL/victim-rel/SCORECARD.md`. Each run exited 1, and each victim's line 1 became `OFF-BRANCH REWRITE by jj-red-before (was a pointer-table-cited line)`. The victim sha256 went from `9c61c973…` to `996dd40f…`. `lane-tip-unchanged` **held** in both receipts.
  - E7a [O]: with an entry naming `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md`, `pick_cited_line` returns that path and `Path(sb, file)` is the real lane file (`is_file: True`). `_refuse_inside(target)` would refuse it, but it isn't called.
- **Impact:** one line of an arbitrary user-writable file is rewritten, including LANE or fleet files. jj would snapshot the change into the lane's working-copy commit [I]. The receipt's only no-write oracle can't see it.
- **Not live at REV:** 60 entries, 20 qualifying, first = `SCORECARD.md:59`, 0 absolute or `..` [O]. The probe's legitimate out-of-repo form is `@slug` (`citation-drift-probe.py:30`), which `is_file()` skips.
- **Remediation:** in `:211-216`, accept an entry only if `os.path.realpath(os.path.join(sb, f))` starts with `os.path.realpath(sb) + os.sep` and is not a symlink. Assert the same containment immediately before `:301` and `:307`.

### F2 — MEDIUM (conditional): `--selftest` writes the repo named by an inherited absolute `GIT_DIR`/`GIT_INDEX_FILE`
- **Exploit path:**
  - `build_fixture_lane` runs `git init`, `add -A` and `commit` with the full `os.environ` (`:889-897`).
  - `verify.py:123` forwards `os.environ` (`env={**os.environ, …}`) into `jj-red-before.py --selftest` (`verify.py:159`).
- **Evidence** (victims are mkdtemp clones of LANE, origin removed, HEAD detached at REV like the lane):
  - E4a [O], `GIT_INDEX_FILE=<victim>/.git/index`: the run printed `SELFTEST: CLEAN cases=5` (exit 0), while the victim's index went from 16135 entries to 6, its sha256 changed (`364b75df…`→`926041d1…`), and HEAD was unchanged. The damage is silent and the selftest is green.
  - E4b [O], `GIT_DIR=<victim>/.git`: the selftest FAILED (exit 1), and the victim's HEAD moved `b2aad08`→`11f9ccc` (fx "B", parent b2aad08)→`fdfe460`. `diff --shortstat b2aad08 HEAD`: `16135 files changed, 41 insertions(+), 1674280 deletions(-)`.
  - E4c [O], control: relative `GIT_DIR=.git GIT_INDEX_FILE=.git/index` with cwd at the victim root → CLEAN, victim unchanged. So only absolute values trigger it.
- **Impact:** pointed at LANE or the fleet repo, this corrupts that repo's index or adds commits on its detached HEAD. `refs/heads/main` is untouched. Recovery needs `jj op restore` or reflog [I]. I observed no fleet caller exporting absolute values; my env has only `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT`.
- **Remediation:** delete `GIT_*`/`JJ_*`/`TMPDIR` from `os.environ` at the top of `main()` (`:1005`). That also fixes F4. The narrowest F2-only fix is to move `:898` above `:889` and pass `env=env` at `:894`.

### F3 — LOW: running the tool without `-B` writes `revpin.cpython-314.pyc` into LANE
- **Exploit path:** the file is executable (`100755`, shebang `#!/usr/bin/env python3`, `:1`, so no `-B`). `exec_module` (`:437`, `:677`) caches bytecode next to `--revpin`, which defaults to LANE's tools dir (`:1020-1021`).
- **Evidence:** E5 [O], `$W/jjrb.py … --revpin <clone>/…/revpin.py` → exit 0, `all_held: True`, `lane-tip-unchanged` held. It created `<clone>/.ufo/waves/round-18/tools/__pycache__/revpin.cpython-314.pyc` (20368 B). `git status --porcelain` showed 0 lines; `--ignored` showed `!! .ufo/waves/round-18/tools/__pycache__/` (`.gitignore:1`).
- **Context [O]:** LANE already holds `…/tools/__pycache__/routed-defects.cpython-314.pyc` (13:46:17, after the REV commit at 13:38:07). It wasn't made by this tool, but it shows this class of write is live in the lane (w1 F3).
- **Remediation:** set `sys.dont_write_bytecode = True` before `:437`/`:677`.

### F4 — LOW: the in-process `revpin` measures the `GIT_DIR` repo instead of `sb` (read-only, fails closed)
- **Evidence:**
  - E6 [O], `GIT_DIR=<v3>/.git` against a lane clone: exit 1. Both revpin steps raised `RevPinError: branch_not_pushed` and are not held. In `sb` the expected outcomes were D0 clean and D1 `head_not_branch_tip`.
  - E7c [O]: `resolve_source(<lane-e6>)` under the same env returned `source = head = dfe9d0eb…` (v3's main), not `b2aad08`.
- **Remediation:** same as F2's `main()` scrub.

### O1 — INFO: `lane-tip-unchanged` cannot support "Never writes LANE" (`contract.md:98`)
- `:700-704` compares only `refs/heads/<branch>`. It held in E2 and E5 while files were written [O].
- The w1 postconditions (`SentinelSandbox.md:145-149`: LANE `.git/HEAD` bytes, op_heads listing, no new `__pycache__` under `LANE/.ufo`) are absent. Fix F1 and F3 at the source first; widening the oracle is optional.

## Commands (exit codes; `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `REV=b2aad08…`, `W=/tmp/jjsbx-JQvPXL`, now removed)
```
git -C $LANE rev-parse --verify $REV^{commit}                                   # 0
git -C $LANE show $REV:.ufo/waves/round-18/tools/jj-red-before.py               # 0 (1046 lines)
git -C $LANE show $REV:{contract.md,tools/revpin.py,verify.py} (round-18), B/REV probes  # 0 each
jj --version; git --version; python3 --version                                  # 0
git config --global --list --show-origin                                        # 0
git config --system --list --show-origin                                        # 128 (no /etc/gitconfig)
git -C $LANE ls-tree -r $REV | awk '$1=="120000"'                               # 0 (2 symlinks -> /var/tmp/ex25-r4/...)
git -C $LANE ls-tree -r --name-only $REV | grep -c '(^|/)\.gitattributes$'      # 1 (count 0)
git -C $LANE show $REV:.ufo/gates/citation-drift/pointer-table.json | python3 -I -B -c '<qualifying/abs/.. scan>'  # 0
W=$(mktemp -d /tmp/jjsbx-XXXXXX); git clone --no-local $LANE $W/lane            # 0
git -C $W/lane remote remove origin; git -C $W/lane remote                      # 0; 0 (empty)
# E1  faithful run (all tool paths -> $W/lane)
python3 -I -B $W/jjrb.py --root $W/lane --cd-probe … --custody-pair … --revpin … --out $W/e1-receipt.json   # 0, 14/14 held
# E3  python3 -I -B e3_sandbox_state.py $W  (REV _build_sandbox_in + commit_off_branch, XDG canaries)  # 0
grep -rl -e jjsbx-JQvPXL -e jj-red-before-imdx_b9f ~/.config/jj/repos/          # 1 (no match)
# E2  clones lane-{abs,rel}: origin removed, entry prepended, git commit -qam   # 0 each
python3 -I -B $W/jjrb.py --root $W/lane-abs … --out $W/e2-abs-receipt.json      # 1 (victim line 1 rewritten)
python3 -I -B $W/jjrb.py --root $W/lane-rel … --out $W/e2-rel-receipt.json      # 1 (victim line 1 rewritten)
# E4  victims: git clone --no-local $LANE; remote remove origin; checkout --detach  # 0 each
env GIT_INDEX_FILE=$W/victim-idx/.git/index python3 -I -B $W/jjrb.py --selftest # 0 (CLEAN; index 16135 -> 6)
env GIT_DIR=$W/victim-dir/.git python3 -I -B $W/jjrb.py --selftest              # 1 (HEAD b2aad08 -> fdfe460)
git -C $W/victim-dir diff --shortstat $REV HEAD                                 # 0
(cd $W/victim-relenv && env GIT_DIR=.git GIT_INDEX_FILE=.git/index python3 -I -B $W/jjrb.py --selftest)  # 0, unchanged
# E5  chmod +x $W/jjrb.py; $W/jjrb.py --root $W/lane … --revpin $W/lane/…/revpin.py --out $W/e5-receipt.json  # 0 (pyc written)
# E6  git init -q -b main $W/victim-e6 && commit --allow-empty                   # 0
env GIT_DIR=$W/victim-e6/.git python3 -I -B $W/jjrb.py --root $W/lane-e6 … --out $W/e6-receipt.json  # 1
python3 -I -B e7_chain.py $W ; env GIT_DIR=$W/victim-e6/.git python3 -I -B e7_chain.py $W  # 0; 0
git -C $LANE for-each-ref | diff <start snapshot> -                             # 0 (lane refs unchanged; HEAD = main = b2aad08)
rm -rf /tmp/jjsbx-JQvPXL; rm -f <REV extracts + refs snapshot in /tmp>          # 0; 0
```

To reproduce F1 in one shot, after `W`/clone setup:
```
python3 -I -B -c 'import json,sys;p=sys.argv[1]+"/.ufo/gates/citation-drift/pointer-table.json";t=json.load(open(p));t["entries"].insert(0,{"id":"x","kind":"exact","file":sys.argv[2],"line":1,"must_match":"v"});open(p,"w").write(json.dumps(t))' <clone> <victim>
```
Then `git commit -qam x` in the clone, run E1's command with `--root <clone>`, and check `head -1 <victim>`.

## Residual inference (not reproduced; not findings)
- On timeout, `run()` (`:128-133`) kills only the direct child. A grandchild could outlive the `finally` rmtree (`:722`) [I]. This gives no path to LANE.
- On a jj-colocated LANE, F2's moved HEAD would be imported by the next jj command [I]. I didn't exercise this, since jj is never run in the lane.

## Hygiene
- I wrote only this report in the lane.
- Scratch outside a mkdtemp (REV extracts and the lane-refs snapshot, written straight to `/tmp`) has been removed. So has the mkdtemp workspace `W` (exit 0).
