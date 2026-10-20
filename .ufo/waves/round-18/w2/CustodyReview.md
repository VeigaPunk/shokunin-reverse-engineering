PARTIAL

**KaidokuR18.CustodyReview, round 18, wave 2 (falsify).** This review covers the `custody-pair.py` R3 change at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` against baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.

**What holds:**
- selftest passes 30/30.
- A capture run from `cwd=/` pins the lane root, and all six `repo-*` headers agree with independent git reads.
- `verify` ignores the header lines. Swapping headers between receipts gives MATCH 5/5 in both directions, and the baseline tool reads the new receipt the same way.
- A real jj 0.45.1 sandbox run with the REV bytes moves from red to green.

**What does not hold:**
- The new `git status` takes `<repo>/.git/index.lock` on every capture. The default repo is the live lane, and selftest does this 25 times per run. jj fails immediately when that lock is held (F1).
- The REV tool crashes on import when it is copied to a shallow path (F2).
- selftest kills only 3 of 7 mutations of the R18 code (F3).

## Identity and safety
- [OBS] `git diff 9011581… b2aad08… -- .ufo/gates/custody-pair/` exited 0: one file changed, +129/−8.
- [OBS] The working tree is byte-identical to the REV blob: sha256 `171d9089…e448`, blob `1193c91d`, the same blob as at `eb6c2668`. During the review, HEAD = `refs/heads/main` = `b2aad08`.
- No `lsp` device exists in this session. I searched for callers with `git grep` at REV. That is a literal search, not semantic proof.
- Every lane-touching run used `GIT_OPTIONAL_LOCKS=0`, because of F1. The lane `.git/index` was the same before and after (ino 43430732, mtime_ns 1792514292032618406).
- I ran jj only in a `/dev/shm` mkdtemp sandbox: a fresh repo with no remote, with HOME and XDG redirected into the sandbox. I installed no tools.

## Commands (exit codes)
1. `cd LANE && GIT_OPTIONAL_LOCKS=0 python3 -I -B .ufo/gates/custody-pair/custody-pair.py selftest` exited **0** with `CUSTODY_PAIR_SELFTEST: CLEAN cases=30 passed=30 failed=0 exit=0`. Both `repo-header-off-branch-tip-no` and `repo-arg-and-lane-root-default` passed. The scratch directory `/dev/shm/custody-pair-selftest-g1u0ay6v` has since been deleted.
2. `cd / && GIT_OPTIONAL_LOCKS=0 python3 -I -B LANE/.ufo/gates/custody-pair/custody-pair.py capture --out /tmp/kr18w2-c.txt` exited **0** with `CUSTODY_PAIR_CAPTURE: OK paths=5/5`; the receipt sha256 is `4c8d8443…`. Its header:
   `# cwd: /`, `# repo-HEAD: b2aad08…`, `# repo-root: /home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `# repo-branch: main`, `# repo-branch-tip: b2aad08…`, `# repo-HEAD-is-branch-tip: yes`, `# repo-dirty: no`.
   Independent reads, each exit 0, all agree with that header: `git -C LANE rev-parse HEAD` returned `b2aad08…`, `rev-parse --verify refs/heads/main^{commit}` returned `b2aad08…`, `--no-optional-locks status --porcelain --untracked-files=no` printed nothing, and `rev-parse --show-toplevel` returned LANE.
3. `sha256sum -c custody-r17.v2.txt.sha256` (cwd `round-17/custody`) exited **0** (`OK`). The r17 header has `repo-HEAD: d0ab299…` and no `repo-*` lines.
4. `verify custody-r17.v2.txt /tmp/kr18w2-c.txt` exited **10** (CONTENT-DRIFT). Two of five paths drifted: `~/.config/devin/mcp_config.json` and `~/.omp/agent/mcp.json`. The other three were MATCH on 11/11 fields. The reversed order also exited **10**, and so did `--require-paths 5`.
5. These checks separate the header from the stanzas. All three show that verify MATCHes on stanzas and ignores metadata headers (**HOLDS**). The exit 10 in step 4 is real stanza drift.
   - `verify R17 [r18 header + r17 stanzas]` exited **0** (MATCH 5/5, 11/11).
   - `verify r18 [r17 header + r18 stanzas]` exited **0** (MATCH 5/5).
   - The baseline blob tool, `verify R17 r18`, exited **10** with identical rows.
   - **Custody observation, not a tool defect.** [OBS] Both drifted files were rewritten at 2026-10-20T16:35:56Z, after the r17 capture at 14:47:36Z. Both got new inodes (43426867 and 43426873). The omp file's size went from 453 to 429 bytes; the devin file stayed at 406. I did not open the contents. L1 should confirm with the operator that this change was expected.
6. jj sandbox replay with the REV bytes. Every step exited 0 except where noted. Captures used `capture --out … --paths $SB/f.txt --repo $SB/repo` from `cwd=/`.
   - After `git init -b main`, commit c1 `c7aae451`, then `jj git init --colocate`: `yes`, dirty `no`.
   - After a tracked edit: dirty `yes`.
   - After `jj commit -m off`, with `@-` = `346a0964` and the `main` bookmark not moved: `repo-HEAD 346a0964`, `repo-branch-tip c7aae451`, **`no`**.
   - After `jj bookmark set main -r @-`: tip `346a0964`, **`yes`**.
   - `verify cap-C cap-E` exited **0** (MATCH), as designed: the flag never reaches verify.

## Findings (by severity)

**F1 MEDIUM (operability and contract; new in R18; low frequency) — every capture takes the repo's index lock, and selftest does it 25 times against the live lane.**
- Code:
  - `_git_at` (`custody-pair.py:350-361`) is documented as "Read-only" at `:351`, but runs `git -C <repo> …` with optional locks enabled (`:353-356`).
  - `repo_context` runs `status --porcelain --untracked-files=no` (`:383`).
  - The repo defaults to `LANE_ROOT` (`:744`).
  - The selftest helper `capture_to` builds a `Namespace` without `repo` (`:872-876`), so every selftest capture pins the live lane. The section banner says "fixtures only" (`:842`).
- Evidence:
  - [OBS] Fresh-stat sandbox repo: `strace -f -qq -e trace=openat,rename,renameat,renameat2,unlink,unlinkat -o … python3 -I -B TOOL capture --out - --paths $SB/f.txt --repo $SB/repo2` exited **0**. It shows `openat(".../.git/index.lock", O_RDWR|O_CREAT|O_EXCL|O_CLOEXEC) = 3` and then `unlink(...index.lock) = 0`. With `GIT_OPTIONAL_LOCKS=0` there are 0 such syscalls.
  - [OBS] Stale-stat sandbox repo (after `os.utime` on a tracked file): one capture exited 0 and **rewrote** `.git/index` (inode 4551 → 4567). With `GIT_OPTIONAL_LOCKS=0` it was unchanged. With the default env again: 4567 → 4572.
  - [OBS] `GIT_OPTIONAL_LOCKS=0 GIT_TRACE2_EVENT=$SB/trace2.json python3 -I -B TOOL selftest --scratch $SB/scr-trace` exited **0** (CLEAN 30/30). It ran **100** git commands against the lane path: 25 × {`rev-parse --git-dir`, `rev-parse HEAD`, `rev-parse --verify refs/heads/main^{commit}`, `status --porcelain --untracked-files=no`}.
  - [OBS] In the jj sandbox, with `.git/index.lock` present, `jj commit -m locktest` exited **1**: `Error: Failed to reset Git HEAD state … could not be obtained immediately after 1 attempt(s)`. `jj log` also exited **1**. After `rm` of the lock, `jj st` (exit 0) showed `@-` still at `off`, so no commit was made.
  - [OBS] In the lane, `git --no-optional-locks status --porcelain --untracked-files=no` takes 5.8–7.7 ms over 16,135 tracked entries. That is roughly the lock window per capture.
- [INF] A capture or selftest that overlaps a jj operation in the lane can fail that operation. One case is the helper sequence `jj commit` → `bookmark set`: if the second step fails, HEAD is left off-branch, which is the very state R3 flags. I did not observe such a collision in the lane.
- This also contradicts the "READ-ONLY over every path it inspects" claim (`:13`) and the w1 report's "all read-only" (`w1/CustodyPairBranchTip.md:17-20`).
- Fix: use `["git", "--no-optional-locks", "-C", str(repo), *argv]` at `:354`, and pass a fixture `repo=` in `capture_to`.

**F2 LOW (operability; new in R18) — the tool crashes on import when it lives fewer than four directories deep.**
- `LANE_ROOT = TOOL_PATH.parents[3]` is evaluated at import (`:214`).
- [OBS] `git -C LANE show REV:.ufo/gates/custody-pair/custody-pair.py > /tmp/kr18-custody-rev.py`, then `cd / && python3 -I -B /tmp/kr18-custody-rev.py paths`, exited **1**: a traceback at line 214, `IndexError: 3`. `verify R17 /tmp/kr18w2-c.txt` with the same copy also exited **1**.
- Exit 1 is outside the declared exit map (`:152-178`).
- The baseline blob at the same depth works: `verify` exited 10 and `paths` exited 0.
- [INF] This breaks the fleet's usual REV-extraction pattern: `jj-red-before` writes copies to `/tmp/jj-red-before-*/…py`, which has only three ancestors.

**F3 LOW (depth) — selftest kills only 3 of 7 single-line mutations of the R18 code.**
- Method: copy the tool to `/dev/shm/<mkdtemp>/mut/<M>/a/b/c/custody-pair.py`, apply one replacement, then run `python3 -I -B <copy> selftest --scratch <dir>`. The unmutated control exited **0** (30/30).
- Survived (exit **0**, 30/30):
  - M1: `ctx["dirty"]="no"` always (`:390`).
  - M2: `--untracked-files=no` dropped (`:383`).
  - M3: `LANE_ROOT = TOOL_PATH.parents[2]`.
  - M4: `LANE_ROOT = Path("/")`.
- Killed (exit **3**): M5, the `head ==` comparison dropped (`:388`); M6, tip read from `HEAD` (`:382`); M7, root taken from cwd (`:372`).
- Causes:
  - Case 27 compares the default against the same constant (`want = str(LANE_ROOT)`, `:1384`), so the check cannot catch a wrong `LANE_ROOT`.
  - No case covers `repo-dirty: yes` or the exclusion of untracked files. The fixture repo has only empty commits (`:1348-1351`).
- The live capture in step 2 shows the actual value is correct. This is a gap in regression protection only.

**F4 LOW (calibration; raised in wave 1, still unfixed) — `repo-root` records the argument, not the repository top level.**
- `"root": str(repo)` (`:372`).
- [OBS] `capture --out - --paths $SB/f.txt --repo $SB/repo/sub/dir` exited **0** with `repo-root: …/repo/sub/dir`. HEAD and tip come from the enclosing repo; `rev-parse --show-toplevel` returns `…/repo`.
- Already raised at `w1/RevBaseCustodyHead.md:231-233` and `:308-309`.

**F5 LOW (calibration of the C2 count) — the HEAD read at `:381` is annotated "compare-only", but its value is recorded in the receipt.**
- `:381` carries `# head-rev-lint: compare-only`, yet `:407` writes that value verbatim as `# repo-HEAD:`.
- The lint trusts annotations (`head-rev-lint.py:142-143`).
- [OBS] `python3 -I -B LANE/.ufo/waves/round-18/tools/head-rev-lint.py --root LANE --rev <rev>` exited **0** for both revisions:
  - 9011581: live 3, including custody `:327`.
  - REV: live 0, annotated 6, including custody `:381`, `:1350`, `:1353`.
- So custody's contribution to the 1 → 0 drop rests on a comment that the code contradicts. The accurate statement is "HEAD is still recorded (`contract.md:79`), and is now flagged (`:411`)".

**F6 INFO (doc drift)**
- At REV, `README.md:230` and `:247` still say 28 cases and `cases=28`, and do not mention `--repo`. The executor flagged this at `w1/CustodyPairBranchTip.md:92-94`.
- The custody row at `SKILL.md:449` has no `--repo` and no new header fields.
- Reproduce: `git show REV:.ufo/gates/custody-pair/README.md | sed -n '230p;247p'`.

**F7 INFO (pre-existing class, now with a second vector) — a newline in an argument escapes the `#` header.**
- [OBS] `capture --repo $'…/nonexistent\nPATH: /etc/hostname' …` exited 0, and the receipt gained a `PATH: /etc/hostname` stanza.
- [OBS] `verify clean.txt inj-repo.txt` exited **12** (METADATA-DRIFT, EXTRA-PATH).
- `--label` with a newline does the same on REV and on the baseline tool (both exit **12**).
- This breaks "all `#` header lines are metadata" (`:116-117`) only when the operator supplies such a value. It is the same self-harm class as `:55-57`.

## Residual risk and verification gaps
- **The flag lives only in the header.** An off-branch or non-repo capture still exits 0 and prints `CUSTODY_PAIR_CAPTURE: OK` (`:801-803`). For example, a non-repo `--repo` gives all `(none)` and `no`, with exit 0. The only code at REV that reads `repo-HEAD-is-branch-tip` is `jj-red-before.py` (git grep).
- **`repo-dirty` depends on when jj last ran.** [OBS] In the sandbox, under default jj auto-track, a new file reads `repo-dirty: no` until any jj command runs. After `jj diff --summary`, which wrote the intent-to-add entry ` A new.txt`, it reads `yes`.
  - [OBS] The lane's jj config `~/.config/jj/repos/82edd62c643a3add383a/config.toml` (config-id taken from `LANE/.jj/repo/config-id`) sets `snapshot.auto-track = "none()"`. [INF] The lane is therefore unaffected.
  - This corrects `w1/RevBaseCustodyHead.md:326-333`: the setting is verifiable, from that per-repo config.
- **Non-atomic reads.** HEAD, tip and status are read separately (`:381-383`), as noted at `w1/RevBaseCustodyHead.md:254-259`. I did not re-measure this.
- **Evidence binding.** The `d0-fixed-custody-capture` and `fixed-custody-capture` steps in `evidence/jj-red-before.json` (steps 2 and 11) ran the working-tree tool without recording its sha256. The JSON has no `171d9089`, and the receipts were deleted. My step 6 replay reproduces the same outcomes with the REV bytes.
- **Not checked:** the stale `/tmp` EDQUOT warning string (pre-existing), and `GIT_DIR` env overriding `-C` (pre-existing). The verify18 harness end to end was not run.

## Cleanup
- `rm -rf /tmp/kr18w2-c.txt{,.sha256} /tmp/kr18w2-hdrswap-{a,b}.txt /tmp/kr18-custody-{rev,base}.py /dev/shm/custody-pair-selftest-g1u0ay6v /dev/shm/kr18w2-custody-q9ycy0uq` exited **0**. A follow-up `ls` showed my paths are gone (exit 2).
- `/tmp/kr18w2-jjrb*` belongs to another seat and was not touched.
- The sandbox jj wrote its config-id directory only inside the sandbox HOME. The newest real `~/.config/jj/repos` entries point to `/tmp/fbr-jj-…` and `/var/tmp/souji-r17-…`, which are not mine.
- I made no lane writes other than this report.
