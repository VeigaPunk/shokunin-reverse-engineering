# SentinelSandbox — jj-red-before sandbox and lane jj state (round 18, w1)

Scope: security/safety review of `W18/tools/jj-red-before.py` as planned in `.ufo/waves/round-18/contract.md:88-98`, plus the VCS rule `contract.md:17-21`, plus the lane's current jj/git state. The tool doesn't exist yet (`glob W18/tools/*` → "Path not found"), so this reviews the plan. Every rehearsal ran in `mkdtemp` dirs under `/tmp`, some of them throwaway clones of LANE. I never ran `jj` or a git write in LANE. The only lane file I wrote is this report.

Labels: **[OBS]** means I ran it and saw the result here. **[INF]** means inference from code or docs, not executed.

## Verdict
As planned, the sandbox can't write LANE through TMPDIR or hardlinks on this host today **[OBS]**. It has one high-severity unguarded path to LANE's `refs/heads/main`: a push from `sb` **[OBS in analog]**. It also has two quiet LANE-write paths, `git diff` index refresh and child-process `__pycache__` **[OBS in analog]**, plus three calibration traps that would make "red-before" pass or fail for the wrong reason **[INF]**.

## Environment facts
| Command | Exit | Result |
|---|---|---|
| `echo "TMPDIR=[$TMPDIR]"` | 0 | `TMPDIR=[]` (unset). `env \| grep -E '^(GIT_\|JJ_\|TMP\|TEMP\|PYTHON…)'` shows no `GIT_DIR`/`GIT_WORK_TREE`/`JJ_*`/`TMP`/`TEMP` **[OBS]** |
| `findmnt /tmp` | 0 | `/tmp /dev/nvme0n1p1 xfs rw,nosuid,nodev,…` **[OBS]** |
| `findmnt -T LANE` | 0 | `/home /dev/mapper/root[/@home] btrfs` **[OBS]**. So `/tmp` and LANE are on different devices: `stat -c %d` gives 66305 vs 57 **[OBS]** |
| `ls -la / /tmp \| grep -E ' \.(jj\|git)$'` | 1 | No `.jj`/`.git` in `/` or `/tmp`, so walking up from a `/tmp/tmpXXXX` dir finds nothing **[OBS]** |
| `jj --version` | 0 | `jj 0.45.1-7c41cdeb…`. `git version 2.56.0`. `Python 3.14.8` **[OBS]** |

## Lane jj state (read-only)
- `.git/HEAD` holds the raw SHA `9011581d…`, so HEAD is detached. `git rev-parse HEAD refs/heads/main` returns `9011581d…` for both (exit 0) **[OBS]**. This matches `contract.md:17-18` and `contract.md:4`.
- **Op log**, read from a copy (`cp -a LANE/.git LANE/.jj $D`, then `jj --ignore-working-copy -R $D op log`, exit 0) **[OBS]**:
  - 11 ops total.
  - Init ops at 11:51:47 used `--config 'snapshot.auto-track="none()"' git init --colocate .`.
  - The last op is at 12:06:56: `jj git push --remote origin --bookmark main`.
  - The ops before it were `file track`, `diff --summary` (snapshot), `metaedit`, `commit`, and `bookmark set main -r 9011581…`.
  - No op is later than 12:06:56. `contract.md` mtime is 12:19:51, so no jj ran in LANE after the contract was written **[OBS]**.
- The working copy `@ = cb7ec426` is empty, with parent `main` at `9011581`. Workspace: `default: .` **[OBS]**.
- The per-repo jj config `~/.config/jj/repos/82edd62c643a3add383a/config.toml` contains `snapshot.auto-track = "none()"`, user `kaidoku-shokunin`, and `trunk() = main@origin` **[OBS]**. A stray jj command in LANE would therefore not auto-track new files. It *would* still snapshot edits to tracked files such as `LOG.md` into `@` and add an op **[INF]**.
- LANE `remote.origin.url` is GitHub (`.git/config`). LANE `.gitignore:1-2` ignores `__pycache__/` and `*.pyc` **[OBS]**.
- The fleet repo `/home/vgpnk/Projects/shokunin` is a plain git repo (no `.jj`). It ignores LANE via `.gitignore:1 *-shokunin/` (`check-ignore` exit 0) **[OBS]**.

## Findings

### F1 — HIGH: `sb`'s origin is LANE, and LANE accepts pushes to `main`
- **Exploit path:** `git clone --no-local LANE sb` (`contract.md:89`) leaves `origin = LANE` in `sb`. LANE's HEAD is detached, so `receive.denyCurrentBranch` doesn't protect `main`. Any `git push` or `jj git push` from `sb`, whether a bug, a "helpful" retry, or a selftest copy-paste, moves LANE's `refs/heads/main`.
- **Evidence:**
  - `git -C sb remote -v` → `origin /home/vgpnk/Projects/shokunin/kaidoku-shokunin (fetch)/(push)`, exit 0 **[OBS]**.
  - Analog run: after `jj commit -m off` in `sb`, HEAD was detached (`e245559e` vs main `9011581d`). I made `sb2 = clone of sb`, committed there, and ran `git -C sb2 push -q origin HEAD:refs/heads/main` → exit 0. `sb` main moved `9011581d… → ba5c188e…` **[OBS]**.
  - Control: the same push while `sb` HEAD was still attached to `main` was rejected ("refusing to update checked out branch", exit 1) **[OBS]**.
- **Impact:** the branch-tip pin that every round-18 tool relies on (`contract.md:18`) silently moves. The next `jj` in LANE would import the moved ref **[INF]**.
- **Fix:** right after the clone, run `git -C sb remote remove origin`. Assert `git -C sb remote` prints nothing before `jj git init`. Never put `push` or `fetch` in an argv. As a cheaper alternative: `git -C sb remote set-url --push origin /nonexistent`.

### F2 — MEDIUM: the contract's "read-only" `git diff` rewrites LANE's `.git/index`, and peers are already doing this in LANE
- **Evidence:** each test below was done in a clone of LANE under `/tmp`, after `touch README.md`, comparing `.git/index` mtime before and after **[OBS]**:

  | Command | Index |
  |---|---|
  | `git diff --quiet` | REWRITTEN |
  | `env GIT_OPTIONAL_LOCKS=0 git diff --quiet` | REWRITTEN |
  | `git --no-optional-locks diff --quiet` | REWRITTEN |
  | `git diff --quiet refs/heads/main` | REWRITTEN |
  | `git status --porcelain` | REWRITTEN |
  | `env GIT_OPTIONAL_LOCKS=0 git status --porcelain` | unchanged |
  | `git diff --quiet main~1 main` (tree-to-tree) | unchanged |
  | `git log` / `git show -s` / `git ls-tree` | unchanged |

  Every rc was 0 except the tree-to-tree `diff`, which returned 1 because the trees differ.
- **Live lane:**
  - Polling `LANE/.git` every 10 ms for 20 s caught a transient `index.lock` at 12:28:36 **[OBS]**.
  - A `/proc` sample caught `git -C LANE status --porcelain` at 12:29:10 and `git status --porcelain` with cwd LANE at 12:29:15. Both are peer processes **[OBS]**.
  - `.git/index` mtime was still 12:06:58 when checked at about 12:26 **[OBS]**.
  - Disclosure: I also ran `git -C LANE status --porcelain` once, around 12:25 (exit 0, output `?? .ufo/waves/round-18/`). That was before I knew it takes the lock.
- **Impact:**
  - LANE's `.git` gets written while the contract calls these commands read-only (`contract.md:19-20`).
  - Concurrent `index.lock` holders can make the L1's later commit or `jj` import fail with "index.lock exists" **[INF]**.
  - Before/after fingerprints of LANE `.git` are useless as a no-write oracle while peers run. My first rehearsal fingerprint changed even though nothing in it writes LANE; the second matched before and after (`2faad7e0fa907c6d` both). Three back-to-back `git clone --no-local LANE` runs left `LANE/.git` mtime unchanged in 2 of 3, and the mtime also moved during a window where I ran only `sleep` **[OBS]**.
- **Fix:**
  - Amend the allowed list to `diff <rev> <rev>` only.
  - Ban `status` and worktree `diff` in LANE, or require `GIT_OPTIONAL_LOCKS=0` for `status`. That env var does **not** cover `diff`.
  - jj-red-before should touch LANE only through `git clone --no-local` and rev-addressed `show`.

### F3 — MEDIUM: child Python processes write `__pycache__` into LANE, invisibly
- **Evidence:**
  - A parent `python3 -I -B` spawned `[sys.executable, "-I", "-c", "…import revpin_fake"]` (child had no `-B`) → `__pycache__/revpin_fake.cpython-314.pyc` was created **[OBS]**.
  - Same spawn with `-I -B` in the child → no `__pycache__` **[OBS]**.
  - `PYTHONDONTWRITEBYTECODE=1 python3 -I` → `dont_write_bytecode 0`, because `-I` ignores `PYTHON*` env vars **[OBS]**.
- **Exploit path:** step 2 runs "the fixed probe from LANE's working tree" (`contract.md:93`). If that probe imports `revpin` from `W18/tools` (`LANE/.ufo/waves/round-18/tools`), a child launched without `-B` writes `LANE/.ufo/waves/round-18/tools/__pycache__/`. LANE `.gitignore:1-2` and jj's `auto-track none()` both hide it, so "Never writes LANE" (`contract.md:98`) fails with no visible trace **[INF]**.
- **Fix:** every child argv is `[sys.executable, "-I", "-B", …]`. At the end, assert that no new `__pycache__` exists under `LANE/.ufo/waves/round-18` or `LANE/.ufo/gates`.

### F4 — MEDIUM (latent): jj walks up from a mkdtemp dir and would snapshot whatever repo it finds
- **Evidence:**
  - With `TMPDIR` set inside a scratch jj repo `fake_lane`, `python3 -I` `tempfile.mkdtemp()` returned `…/fake_lane/tmp/tmpc05vem9b`. `-I` doesn't shield `TMPDIR` **[OBS]**.
  - `jj root` from there printed `…/fake_lane`, exit 0 **[OBS]**.
  - A read-only-looking `jj log` from there, with `auto-track all()` and one file in the tmp dir, raised `fake_lane`'s op count from 2 to 3 **[OBS]**.
  - Control: `jj root` in a plain `/tmp` mkdtemp → "There is no jj repo", exit 1 **[OBS]**.
- **Today's exposure:**
  - TMPDIR is unset and `/tmp` holds no `.jj`, so this doesn't fire on this host now **[OBS]**.
  - It fires if an executor environment sets `TMPDIR`/`TEMP`/`TMP` under LANE, or if any jj subprocess runs with cwd = LANE **[INF]**.
  - An executor's default cwd may be the fleet repo `/home/vgpnk/Projects/shokunin`. That is a git repo, so a mis-targeted `jj git init --colocate .` there would create `.jj` in the fleet repo **[INF, not executed]**.
- **Operability trap:** `jj -R "$D/sb" git init --colocate .` fails ("There is no jj repo", exit 1), because `-R` doesn't work with `init` **[OBS]**. `cd "$D" && jj git init --colocate sb` works (exit 0) **[OBS]**. A fallback that retries init without `cwd=` would run in the executor's cwd **[INF]**.
- **Fix:**
  - Build the sandbox with `D = tempfile.mkdtemp(dir="/tmp", prefix="jj-red-before-")`, not TMPDIR. Assert `os.path.realpath(D)` is not under `realpath(LANE)` or `realpath("/home/vgpnk/Projects/shokunin")`.
  - Run every subprocess with `cwd=D` or `cwd=sb`, never inherited.
  - Initialize with `jj git init --colocate sb` and `cwd=D`.
  - After init, assert `jj root` (cwd=sb) equals `realpath(sb)`. Every later jj call uses `-R sb`.
  - For git in the sandbox, set `GIT_CEILING_DIRECTORIES=D`.
  - Remove `GIT_*`, `JJ_*`, `TMPDIR`, `TEMP`, `TMP` from the child environment.
  - Exit 2 on any setup failure; never retry.

### F5 — LOW: "Removes the sandbox" leaves jj residue outside D, and user config leaks in
- **Evidence:**
  - jj 0.45 writes a per-repo entry `~/.config/jj/repos/<id>/` on every init. There are 644 entries; 636 point to paths that no longer exist (`strings metadata.binpb`) **[OBS]**.
  - With `XDG_CONFIG_HOME=$D/xdg` set for the jj calls, the new entry landed in `$D/xdg/jj/repos` (count 1). The global count stayed 644, and no global entry referenced `$D` **[OBS]**.
  - The user's global jj config sets `ui.default-command = "log"` and `git.auto-local-bookmark = true` (`~/.config/jj/config.toml`) **[OBS]**. So a bare `["jj"]` argv bug runs `log`, which snapshots.
  - Disclosure: my own copy-based op-log read created residue entry `~/.config/jj/repos/78ce0e73351d28bdfdf3`, which pointed at `/tmp/tmp.2qH9D5eANC/.jj/repo`. I removed it (`rm` exit 0).
- **Fix:** run jj subprocesses with `XDG_CONFIG_HOME=D/xdg` and identity via `--config` (as `contract.md:90` already requires), and remove `D` with it. Use the same isolation for any L1 op-log audit done on a copy of LANE.

### F6 — LOW, calibration: the baseline probe can go "red" or "green" for the wrong reason
- **Evidence:**
  - `citation-drift-probe.py:60-62` resolves `pointer-table.json`/`expected.json` next to `__file__`.
  - `:476-477` defaults `--root` to `dirname(HERE)` (LANE-ward) and `--rev` to `"HEAD"` **[OBS by reading]**.
- **Path:**
  - The baseline is written to a temp file (`contract.md:92`), so its `HERE` is the temp dir. The table is missing, the probe reports `pointer_table_unreadable`, and that non-zero exit could be scored as the expected "red" **[INF]**.
  - If any step omits `--root sb`, it evaluates LANE, where HEAD equals `main`, and reports green **[INF]**.
- **Fix:**
  - Pass `--root sb`, plus `--table` and `--expected` extracted from `B`, into D.
  - Each expectation should check the resolved rev or finding kind, not just the exit code.
  - Record `git -C <root> rev-parse --show-toplevel` and `rev-parse HEAD` per step in the receipt.

### F7 — LOW: custody-pair `capture` hashes secret-adjacent files and takes repo identity from cwd
- **Evidence:**
  - `custody-pair.py:191-197`: the default paths include `~/.omp/agent/mcp.json`, `~/.config/devin/mcp_config.json`, and `~/.kimi-code/config.toml`.
  - `:324-349`: `repo-HEAD` comes from `git rev-parse HEAD` in `Path.cwd()`.
  - `:1316`: `--out` is required. The sidecar `<out>.sha256` is written next to it (`:736`) **[OBS by reading]**.
- **Path:**
  - "capture against sb" (`contract.md:95`) only targets `sb` if `cwd=sb`. With cwd = LANE it reports LANE's HEAD, which equals main, a false green **[INF]**.
  - With the default `--paths`, it opens credential-adjacent files, which the host-safety rule forbids **[INF]**.
  - A relative `--out` with cwd = LANE writes the receipt and sidecar into LANE **[INF]**.
- **Fix:** run with `cwd=sb`, `--paths <a file inside sb>`, and an absolute `--out D/receipt.txt`.

### F8 — none observed: hardlinks
- `--no-local` uses the transport and copies objects. The highest link count among `sb/.git/objects` files was 1 **[OBS]**.
- Cross-device clones can't hardlink anyway (`/tmp` is xfs, LANE is btrfs) **[OBS devices; INF on link(2) EXDEV]**.
- Git objects are never rewritten in place, so a same-device hardlinked clone still couldn't change LANE content **[INF]**.

### F9 — LOW: the sandbox removal itself
`shutil.rmtree(D)` running on a mis-computed `D` (empty string, `LANE`, `..`) would be catastrophic **[INF]**. **Fix:** use `tempfile.TemporaryDirectory(dir="/tmp", prefix="jj-red-before-")`. Before rmtree, assert `realpath(D)` starts with `/tmp/jj-red-before-` and contains no LANE prefix.

## Recommended guard block for jj-red-before.py (smallest set)
1. Create the sandbox with `D = mkdtemp(dir="/tmp", prefix="jj-red-before-")`. Assert its realpath is not under LANE or the fleet repo.
2. Build the child env as `os.environ` minus `GIT_*`, `JJ_*`, `TMPDIR`/`TEMP`/`TMP`, plus `XDG_CONFIG_HOME=D/xdg`, `GIT_CEILING_DIRECTORIES=D`, and `GIT_OPTIONAL_LOCKS=0`. Give every subprocess an explicit `cwd`.
3. Clone with `git clone --no-local LANE D/sb`, then `git -C sb remote remove origin`, then assert there are no remotes (F1).
4. Initialize with `jj git init --colocate sb` (cwd=D). Assert `jj root` equals `sb`. Every later jj call uses `-R sb`. Use no `push`/`fetch` argv (F1, F4).
5. Every Python child runs as `[sys.executable, "-I", "-B", …]` (F3). Pass `--root`/`--table`/`--expected` explicitly. custody-pair runs with `cwd=sb`, explicit `--paths`, and an absolute `--out` in D (F6, F7).
6. Postcondition (exit 2 if violated):
   - `git -C LANE rev-parse refs/heads/main` still equals its value at start.
   - `.git/HEAD` bytes are unchanged.
   - `LANE/.jj/repo/op_heads/heads` listing is unchanged.
   - No new `__pycache__` under `LANE/.ufo`.

   Don't use a full `.git` fingerprint (F2).
7. Remove the sandbox with a prefix-checked rmtree of D (F9).

## Out of scope / not done
- I didn't review `resume_continuity_v1`; no artifact for it was named in this assignment.
- I didn't execute any carrier, REA, or Ghidra.
- Tools installed: none.
- Files I wrote outside LANE are all removed:
  - `/tmp/sentinel-r18-rehearsal.sh`, `/tmp/sentinel-fp-{before,after}.txt`
  - `/tmp/sentinel-r18-*`, `/tmp/sentinel-clone-*`, `/tmp/sentinel-lock-*`, and the `/tmp/tmp.2qH9D5eANC` copy
  - the jj residue entry from F5
