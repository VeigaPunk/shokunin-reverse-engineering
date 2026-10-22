# R29 W1 — `prefile-check.sh` mutation probe

## Scope and detector

**Observation.** Tested `tools/round-29/prefile-check.sh` in `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/clone`, against three isolated target clones: clean, tracked-dirty, and untracked-only-dirty. The tested command pattern was:

```sh
sh /fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/clone/tools/round-29/prefile-check.sh <absolute-target-clone>
```

The shell wrapper recorded UTC and `detector_exit=$?` (the script's exit code); the wrapper itself returned 0. Expected detector: clean clone prints exactly `prefile: clean` and exits 0; either dirty clone prints the porcelain path and `prefile: NOT CLEAN (1 paths)` and exits 1. `matrix-output.txt` contains the run commands and captured output excerpts.

**Observation.** Initial clone command was the required local clone command with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. Its HEAD was `18be864a528873b2b70d8c94e31f880290249e90`; committed script bytes hashed `34edba0460cf9c5d3eb51e15367b3f54718da81bdd6b993d8cacc03379dd5672`.

At 2026-10-22T20:24:16Z, read-only `git diff -- tools/round-29/prefile-check.sh` showed that the lane working-tree copy had a two-line read-only adjustment absent from that HEAD: it documents `GIT_OPTIONAL_LOCKS=0` and invokes `git status` with that variable set. The lane working-tree hash was `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84`. Attribution for that worktree delta is unknown; this seat did not modify the lane. I applied that current source version to the sandbox runner, confirmed the same `205079...` hash, and ran the final full matrix below against it. Target clones remained at the cloned HEAD; their test dirt was created only in scratch.

## Behavioral observations

**Observation — current pristine bytes** (`205079...`, 2026-10-22T20:24:52Z):

| Target | Exact stdout | Detector exit |
|---|---|---:|
| Clean | `prefile: clean` | 0 |
| Tracked dirty | ` M .ufo/waves/round-28/a2w/ExecR27SelftestFix.md`<br>`prefile: NOT CLEAN (1 paths)` | 1 |
| Untracked only | `?? .prefile-mutant-marker`<br>`prefile: NOT CLEAN (1 paths)` | 1 |

**Observation — mutation results and restoration:**

| Mutant | Before → mutant → restored SHA-256 | Exact distinguishing output; UTC | Detector verdict |
|---|---|---|---|
| M1: `-n` → `-z` | `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` → `239430633351afc754e01d696d25d1f000623eaa02eaec04ce36f51b07e2cc16` → `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` | Clean stdout bytes: `\nprefile: NOT CLEAN (1 paths)\n`, exit 1; tracked and untracked dirty each printed `prefile: clean`, exit 0. 2026-10-22T20:24:59Z (untracked rerun 20:25:04Z). Restored matrix passed at 20:25:12Z. | **Killed**: clean and both dirty expectations invert. |
| M2: add `--untracked-files=no` | `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` → `353f941ccb4fff0653dca7c9c18273d70efd38d9411726d3d291787a92543cdd` → `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` | Clean printed `prefile: clean`, exit 0; tracked dirty printed its path and `prefile: NOT CLEAN (1 paths)`, exit 1; untracked-only printed `prefile: clean`, exit 0. 2026-10-22T20:25:23Z. Restored matrix passed at 20:25:31Z. | **Killed by the untracked-only case**; tracked-only case passes. |
| M3: dirty-branch `exit 1` → `exit 0` | `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` → `56b4a5a0bd07379110fa9f05fd6964c9be2705a47605f60b8c5b95ab0f6e410a` → `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84` | Clean printed `prefile: clean`, exit 0; each dirty case printed its path and `prefile: NOT CLEAN (1 paths)`, but exited 0. 2026-10-22T20:25:40Z. Restored matrix passed at 20:25:50Z. | **Killed**: dirty exit is wrong. |

No baseline failure: pristine and each restored state met the expected clean/tracked-dirty/untracked-dirty behavior. The final sandbox script hash is byte-identical to the lane working-tree source hash `205079...`.

## Red receipt coverage verdict

The opened red receipt records a clean run (`prefile: clean`, `exit=0`, lines 1–3) and a tracked modification with `prefile: NOT CLEAN (1 paths)`, `exit=1` (lines 5–8).

| Mutant | Would `.ufo/waves/round-29/after/prefile-check-red-r28.txt` catch it? | Basis |
|---|---|---|
| M1 `-z` | **Yes** | On the receipt's clean input it emits a NOT CLEAN result and exits 1; on its tracked-dirty input it says clean and exits 0. Both contradict the recorded receipt. |
| M2 `--untracked-files=no` | **No** | The receipt tests a tracked modified path, which the mutant still detects; its clean example also stays clean. The mutant survived the receipt's cases, but the separate untracked-only probe killed it. |
| M3 dirty `exit 0` | **Yes** | The dirty text remains, but the receipt's required `exit=1` becomes exit 0. |

**Inference.** The receipt distinguishes M1 and M3 but does not cover omission of untracked paths. **Observation.** The untracked-only probe is the specific counterexample for M2: `prefile: clean`, exit 0 despite `?? .prefile-mutant-marker`.

## Evidence and artifacts

Commands were local; no network lookup, REA invocation, tool installation, or lane write was performed. All timestamps are UTC on 2026-10-22.

Local source records (read from the filesystem; no remote URL):

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-29/prefile-check.sh` — accessed 2026-10-22; current worktree SHA-256 `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84`; quote, line 3: “Exit 0 when `git status --porcelain` is empty”.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-29/after/prefile-check-red-r28.txt` — accessed 2026-10-22; SHA-256 `7f0e802672162671854a25fee7c23f03c578ae08cef05094da91d72bb76ea6bd`; quote, line 2: “prefile: clean”.

Scratch artifacts and hashes:

- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/matrix-output.txt` — `a01a52d1bffebe731f2bbd37eefd36c2d5ec28475766fe9efdf47df8321df5ed`.
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/clone/tools/round-29/prefile-check.sh` after restoration — `20507911c5f51e6e610499838f600b8a8515e05eb6afdeeb93755f887e868d84`.
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/tracked-dirty/.ufo/waves/round-28/a2w/ExecR27SelftestFix.md` test fixture — `18a1af9a6dd7ff23845d3346bf334748c393626bcace800228e0562995f42795`.
- `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutPrefile/untracked-dirty/.prefile-mutant-marker` test fixture — `78d2a1135e65102f06fd41944ec3b33a0131374624082463076e23b94785578b`.

The scratch runner was restored to the current lane source bytes after each mutant. No mutation remains in the runner. The target fixtures are isolated in scratch and were not applied to any lane file.

Report: .ufo/waves/round-29/w1/MutPrefile.md