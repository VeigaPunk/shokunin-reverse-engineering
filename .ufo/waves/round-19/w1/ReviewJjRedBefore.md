# Review — round-18 `jj-red-before.py` env and path handling

**Axes:** calibration (separate source facts from inference), freshness (check the actual target delta), depth (enumerate subprocess call sites and effective environments).

## Scope and verification

- **[O]** `.ufo/waves/round-18/tools/jj-red-before.py` has no diff from baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` to `refs/heads/main`, nor from `refs/heads/main` to the working tree. Its blob is `0d9b65f67dd9dea49095db1f8e52381745fa68af`, identical to the blob reviewed at `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; these are carried findings, not newly introduced changes.
- **[O]** `xd://lsp` is unavailable (`No such tool: xd://lsp`; the mounted-tool list contains no LSP device). I used literal search only to locate subprocess sites, then read the source at those anchors; the search output is not semantic proof.
- **[O]** No tool installation, Python execution, selftest, or subprocess behavior test was run in this review. Runtime exit codes below are only stated where an earlier report explicitly recorded them.

Commands run for this review (exit codes shown):

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- .ufo/waves/round-18/tools/jj-red-before.py; printf 'git-diff-exit=%s\n' "$?"
# git-diff-exit=0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet refs/heads/main -- .ufo/waves/round-18/tools/jj-red-before.py; printf 'worktree-diff-exit=%s\n' "$?"
# worktree-diff-exit=0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main:.ufo/waves/round-18/tools/jj-red-before.py b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/jj-red-before.py; printf 'rev-parse-exit=%s\n' "$?"
# 0d9b65f67dd9dea49095db1f8e52381745fa68af (both revisions); rev-parse-exit=0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree refs/heads/main -- .ufo/waves/round-18/tools/jj-red-before.py; printf 'ls-tree-exit=%s\n' "$?"
# 100755 blob 0d9b65f67dd9dea49095db1f8e52381745fa68af; ls-tree-exit=0

realpath -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin /home/vgpnk/Projects/shokunin; printf 'realpath-exit=%s\n' "$?"
# Both paths resolve to themselves; realpath-exit=0
```

## Findings

### MEDIUM — pointer-table and marker paths can write outside the sandbox

**[O: source]** `pick_cited_line` takes `e["file"]` from the cloned pointer table and accepts it if `Path(sb, e["file"]).is_file()` (`.ufo/waves/round-18/tools/jj-red-before.py:203-217`). `commit_off_branch` then uses `Path(sb, cited_file)` and writes the selected line (`:294-307`). An absolute path makes `Path(sb, ...)` ignore `sb`; `..` can walk out; `is_file()` also follows symlinks. The fixed marker write at `:307` follows a symlink at the marker name too. `_refuse_inside` is only applied to the temporary directory (`:105-110`, `:237-239`), not to either write destination.

**[O-prior]** The identical blob was exercised in `corpus/lessons/round-18/w2/JjSandboxSafety.md:22-32`: its E2 records an absolute-path and a `../` pointer-table entry rewriting a victim file outside the clone, while the `lane-tip-unchanged` oracle still held; E7a records that a pointer to `LANE/SCORECARD.md` resolves to the real lane file. I did not rerun these destructive reproductions. **[O-current]** A query of the current `.ufo/gates/citation-drift/pointer-table.json` entries for absolute or `..` paths returned `[]`; that only means the reviewed table does not presently exercise the defect.

### MEDIUM — `--selftest` fixture setup bypasses the environment scrub

**[O: source]** `_child_env` removes `GIT_*`, `JJ_*`, and `TMPDIR` (`:113-125`), but the three fixture Git commands at `:889-894` call `subprocess.run` without `env` (or `cwd`), so they inherit the full caller environment and working directory. The filtered env is constructed only afterward at `:898`; that later env removes only `GIT_*` and is used for the fixture `sha_of` at `:899`.

**[O-prior]** `JjSandboxSafety.md:34-43,82-84` records the concrete effect against the identical blob: `env GIT_INDEX_FILE=$W/victim-idx/.git/index python3 -I -B $W/jjrb.py --selftest` returned exit **0** (`SELFTEST: CLEAN`) while changing the victim index; `env GIT_DIR=$W/victim-dir/.git python3 -I -B $W/jjrb.py --selftest` returned exit **1** and moved the victim HEAD. These were prior reviewer runs, not rerun here. This can corrupt a caller-selected repo during what the fixture claims is an isolated selftest.

### LOW — in-process `revpin` checks do not receive the scrubbed child env

**[O: source]** The harness invokes `revpin.resolve_source(sb)` in-process through `run_expr` (`jj-red-before.py:432-451,671-690`), not through `run(..., env=...)`. The imported module's `_git` calls `subprocess.run` without an `env` argument (`.ufo/waves/round-18/tools/revpin.py:71-76`). Thus `GIT_*` and other caller variables reach these Git reads even though the other harness children use `_child_env`.

**[O-prior]** `JjSandboxSafety.md:51-55,88-89` records `GIT_DIR` causing `resolve_source(sb)` to report a different repository's source/head, and an evaluate run to fail its revpin expectations. These are wrong-measurement/fail-closed risks, not writes by `revpin`.

## Complete subprocess inventory and effective env

The wrapper is `subprocess.run(list(argv), cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)` at `jj-red-before.py:128-141`. It retains `p.returncode` at `:134` and records `exit=None` on exceptions at `:137-140`. Its default `env=None` would inherit the process environment; the production `run(...)` call sites pass an env explicitly. The following are static command forms; **they were not executed here, so no runtime exit code is claimed**.

Let **E** = `_child_env(tmp)`: inherited environment except `GIT_*`, `JJ_*`, and `TMPDIR`; `HOME`, `PATH`, and other XDG variables remain. Let **J** = E plus `HOME=tmp/jj-home` and `XDG_CONFIG_HOME=tmp/jj-xdg`, created by `_child_env(tmp, for_jj=True)` (`:113-125`).

| Call site(s) | Command(s) | Effective env and cwd |
|---|---|---|
| `sha_of`, `:157-163` | `git -C ROOT rev-parse --verify --quiet REV^{commit}` | Env supplied by each caller. E for sandbox/evaluate checks (`:254-255,269-284,318,351-352,700`); the fixture hash at `:899` instead gets the `:898` mapping with only `GIT_*` removed (JJ/TMPDIR remain). Cwd supplied by each caller. |
| `git_show`, `:165-169`, called at `:487-494` | `git -C ROOT show REV_PATH` | E; cwd `tmp`. |
| Sandbox setup, `:244-272` | `git clone --no-local LANE SB`; `git -C SB remote remove origin`; `git -C SB remote`; `git -C SB update-ref refs/remotes/origin/BRANCH TIP`; conditional `git -C SB update-ref refs/heads/BRANCH TIP`; `git -C SB checkout --quiet BRANCH` | E; cwd `tmp`. |
| JJ setup/commit, `:275-278,310-314` | `jj --config user.name=... --config user.email=... git init --colocate`; `jj --config user.name=... --config user.email=... -R SB commit -m off` | J; cwd `sb`. These are the only `jj` subprocess calls in the harness. |
| D0/D1 HEAD reads, `:377-378,659-660` | `git -C SB rev-parse HEAD` | E; cwd `tmp`. |
| Citation-drift child calls, `:389-392,503-505,525-528,552-554,576-579` | `sys.executable -I -B CD_FIXED --root SB --rev HEAD --table TABLE --expected EXPECTED`; baseline `CD_BASE` with `--root SB --table TABLE --expected EXPECTED`; baseline control adds `--rev refs/heads/BRANCH`; fixed probe without `--rev`; fixed probe with `--rev HEAD` | E; cwd `tmp`. Each call is captured by `run`. |
| Custody-pair child calls, `:409-414,600-602,626-629` | `sys.executable -I -B CP_FIXED capture --repo SB --out RCP ...`; baseline `CP_BASE capture --out RCP --label ... --paths ...`; fixed `CP_FIXED capture --repo SB --out RCP --label ... --paths ...` | E; cwd `tmp` for D0/fixed calls, cwd `sb` for baseline capture. |
| Embedded baseline citation fixture, `:736-742` | `git -C ROOT rev-parse --verify --quiet REV^{commit}`; `git -C ROOT show REV:SCORECARD.md` | No `env`/`cwd` passed by fixture code; inherits its parent citation-probe process, which the harness launched with E and cwd `tmp`. |
| Embedded fixed citation fixture, `:758-763` | `git -C ROOT rev-parse --verify --quiet REV^{commit}` (called for `refs/heads/main` and `HEAD`) | No `env`/`cwd`; inherits the harness-launched E/cwd `tmp`. |
| Embedded baseline custody fixture, `:786-788` | `git rev-parse HEAD` | No `env`/`cwd`; inherits the harness-launched E and cwd `sb`. |
| Embedded fixed custody fixture, `:809-815` | `git -C REPO rev-parse --verify --quiet REV^{commit}` (HEAD and branch tip); `git -C REPO status --porcelain --untracked-files=no` | No `env`/`cwd`; inherits the harness-launched E and its cwd (`tmp`). |
| Embedded revpin fixture, `:850-860` | `git -C ROOT rev-parse --verify --quiet REV^{commit}` (source, HEAD, remote) | No `env`/`cwd`; this fixture is imported in-process by `run_expr` during selftest, so it inherits the full harness process environment. |
| Selftest fixture builder, `:889-897` | `git init --quiet -b main LANE`; `git -C LANE -c user.name=fx -c user.email=fx@x add -A`; same `-c` options with `commit --quiet -m B` | Direct `subprocess.run`, no `env` or `cwd`: full caller env/current cwd. This is the F2 bypass. |
| Real imported revpin, target calls `:439,679`; `.ufo/waves/round-18/tools/revpin.py:71-90` | `git -C ROOT rev-parse --verify --quiet REV`; conditionally `git -C ROOT merge-base --is-ancestor OLDER NEWER` | Direct `subprocess.run`, no `env` or `cwd`; full caller environment/current cwd. This is the F3 bypass. |

## Additional path risks / residuals

- **[O] Relative override paths are not normalized.** `--root` accepts the caller string as-is (`:1009`) but `git clone` runs with `cwd=tmp` (`:244-245`); a relative `--root .` therefore refers to the temporary directory, not the invoking directory. Relative `--cd-probe`/`--custody-pair` paths are also run from `tmp` (`:389-414,552-629`), while relative `--revpin` is imported relative to the process cwd (`:434-438,674-678`). Defaults are absolute. **[I]** Callers may reasonably expect relative CLI paths to be based on their invocation directory; if so, these options resolve inconsistently.
- **[O]** `emit` creates parent directories and writes `--out` exactly as supplied (`:996-1002`) without `_refuse_inside`; callers must keep this output outside the protected lane/fleet roots if the no-write contract applies to receipts too.
- **[O-prior]** The script is executable (`100755`) and imports `revpin` with `exec_module` (`:434-438,674-678`), whose default path is under the lane (`:1020-1022`). `JjSandboxSafety.md:45-49,86` records the resulting `.pyc` write when invoked without `-B`. The prescribed `python3 -I -B` invocation avoids this; direct shebang execution does not.
- **[O-current]** The protected path constants resolve to their literal values on this host (`realpath` output above), so `_refuse_inside`'s comparison against uncanonicalized constants is not itself an active alias mismatch here.
