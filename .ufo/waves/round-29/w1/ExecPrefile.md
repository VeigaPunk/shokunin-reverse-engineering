# ExecPrefile — round 29, wave 1

## Scope and verdict

**Observation:** Tested `tools/round-29/prefile-check.sh` in the required sandbox clone at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone`, cloned at `18be864a528873b2b70d8c94e31f880290249e90`. Its initial `git status --porcelain` was empty. No lane files other than this exclusive report were written.

**Verdict on QUALITY row 47: HOLDS for the requested cases.** Each separate modified-tracked, untracked, and staged-change case printed its path and exited 1; the clean case exited 0. **Inference:** The implementation's nonempty-output branch supports the row's criterion for these tested path classes; this was not an exhaustive test of every possible porcelain status record or a timing/race test at filing.

## Run evidence

Commands below invoke the cloned script directly. Times are UTC; quoted output is the exact script output (the recorded exit is the script's exit, not the wrapper shell's).

### Clean clone

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone`
- **UTC:** `2026-10-22T20:21:22Z`
- **Observation — output:**
  ```text
  prefile: clean
  ```
- **Exit:** `0`

### One modified tracked file

**Setup:** Inserted a comment at line 16 of the clone's tracked `tools/round-29/prefile-check.sh`; this was the only changed path. The fixture was removed after this run.

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone`
- **UTC:** `2026-10-22T20:21:37Z`
- **Observation — output:**
  ```text
   M tools/round-29/prefile-check.sh
  prefile: NOT CLEAN (1 paths)
  ```
- **Exit:** `1`

### One untracked file

**Setup:** Created `ExecPrefile-untracked-fixture` in the clone root; removed it after this run.

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone`
- **UTC:** `2026-10-22T20:22:08Z`
- **Observation — output:**
  ```text
  ?? ExecPrefile-untracked-fixture
  prefile: NOT CLEAN (1 paths)
  ```
- **Exit:** `1`

### One staged change

**Setup:** Added a comment at line 16 of the clone's tracked `tools/round-29/prefile-check.sh`, then staged only that file. The staging command was `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone add -- tools/round-29/prefile-check.sh`; it produced no output and exited `0`.

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone`
- **UTC:** `2026-10-22T20:22:23Z`
- **Observation — output:**
  ```text
  M  tools/round-29/prefile-check.sh
  prefile: NOT CLEAN (1 paths)
  ```
- **Exit:** `1`

### No argument

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh`
- **UTC:** `2026-10-22T20:21:22Z`
- **Observation — output:**
  ```text
  usage: prefile-check.sh <lane-root>
  ```
- **Exit:** `2`

### Non-repository directory

- **Command:** `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/nonrepo`
- **UTC:** `2026-10-22T20:21:22Z`
- **Observation — output:**
  ```text
  fatal: not a git repository (or any parent up to mount point /)
  Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
  ```
- **Exit:** `2`

## Source and artifact records

Local primary sources read (access date `2026-10-22`):

- `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/prefile-check.sh` — SHA-256 `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84`; line 4 quote: “exit 1 and print the paths otherwise; exit 2 on usage.”
- `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md` — SHA-256 `da2ddf0930f20e76ba6a498f502b3b3469d1e4f1d7da2520c87dfd86d98e9605`; line 57 quote: “Fails when the lane's `git status --porcelain` is non-empty at filing.”

The retained staged test fixture in the sandbox clone is `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPrefile/clone/tools/round-29/prefile-check.sh`, SHA-256 `c8d64192f45d83c3bade1995fd1d94f0888c35af6bada5bf192083978c55f550` (hashed at `2026-10-22T20:22:55Z`). No separate scripts, drafts, or raw-output files were created; exact run output is retained above. No tools were installed or updated.
