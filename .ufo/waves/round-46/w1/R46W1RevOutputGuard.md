# R46W1RevOutputGuard — scoped findings: `gate.out_path` / `--json-out`

Anchor: lane HEAD `deee6595ae3dda094aa5a577fac0f6903e873e16`; `tools/round-46/gate.py` blob
`9ab7e2a3…` sha256 `847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223`, byte-identical
from `781e19ae` to `HEAD` (`git diff 781e19ae..HEAD -- tools/round-46/gate.py` empty); `attest.py`
`936910fe…` identical over the same range. Harness verdict verified real: `--freeze 65678df0… --rev
781e19ae…` → attest exit 0, `failing []`. All runs in throwaway clones under
`/fast/scratch/hyaku/kaidoku-r46/R46W1RevOutputGuard/`; 12-path sha256 before/after every run.
Full report + 56 receipts: `.ufo/waves/round-46/w1/R46W1RevOutputGuard/report.md` and
`.ufo/waves/round-46/w1/R46W1RevOutputGuard/receipts/`.

## Verdict on the claimed arm (block 23 row `R45-CL22 | output | 2`)

| target | expect | exit | any graded/frozen byte changed |
|---|---|---|---|
| `SKILL.md` | refuse 2 | 2 | no |
| `../../SKILL.md` | refuse 2 | 2 | no |
| `plans/round-46-claims.md` | refuse 2 | 2 | no |
| `corpus/SOURCES.md` | refuse 2 | 2 | no |
| `tools/round-46/gate.py` | refuse 2 | 2 | no |
| absolute `<lane>/SKILL.md` | refuse 2 | 2 | no |
| absolute outside the lane root | refuse 2 | 2 | no |
| symlink in lane → `SKILL.md` (also → claims; also a dir symlink into `tools/` with an existing and a new filename) | refuse 2 | 2 | no |
| normal `.ufo/waves/…` path | allow | 0, receipt written | n/a |

Also refused, exit 2, byte-clean: `plans/../SKILL.md`, a graded directory, a non-existent graded
path, a climb out of a seat dir back onto `SKILL.md`, and `--root` narrowed to `.ufo` (absolute and
relative). Also refused on the `registry.py` side. **The six named shapes are closed.**

## Ordering (write before verdict?)

`out_path` is called at `attest.py:484` / `registry.py:432`, **before** `evaluate`; `emit` at
`attest.py:491` / `registry.py:439`, **after** the verdict. Confirmed by behaviour: a graded target
returns exit 2 with only the refusal on stdout even when the verdict would be 0; an allowed target
still receives the receipt when the verdict is exit 2 `frozen_path_changed`. A frozen path can
never be written, because it never reaches `emit`. (`--selftest` returns before `out_path`; it
neither examines nor writes any target — so it cannot be used to test the guard.)

## Findings

**F1 — high, both counters. `emit` is outside `main_guard`, so an unopenable allowed target exits 1.**
`--json-out .ufo/waves` (existing dir) → exit **1**, empty stdout,
`IsADirectoryError` at `gate.py:209`; `--json-out .ufo/nope/x.json` → exit **1**, `FileNotFoundError`.
Reproduced at the newest pair (`--freeze 04252247 --rev 49e6cac4`) and on `registry.py`. Exit 1 is
"not met", so a typo in a receipt directory records a met measurement as a violation — and the
landed registry row for `attest.py` promises `2=… or an unhandled exception`. Fix shape: wrap `emit`
in `main_guard` (or catch `OSError`, print the receipt, return 2).

**F2 — high, scope. `.git/**` is writable.** `GRADED` omits `.git`. Measured, all exit **0**:
`.git/config` replaced by receipt JSON → `git rev-parse HEAD` rc **128** `bad config line 1`, every
later counter run exit 2 `unknown freeze revision`; `.git/refs/heads/main` replaced → `rev-parse
HEAD` rc 128 `unknown revision`; `.git/hooks/pre-commit` writable (code runs on the next commit).
`.ufo/state/` also allowed though the fleet contract forbids it. Fix shape: refuse `.git`,
`.ufo/state`, `.ufo/watchdog.log`, or allowlist `.ufo/waves/**`.

**F3 — medium, realpath limit. Hard link defeats the guard.** `ln SKILL.md .ufo/waves/…/x.json` then
`--json-out` it → exit **0**, `SKILL.md` `2a428bca…` → `9494851b…`; same for the frozen
`plans/round-46-claims.md` (`a09564e0…` → `9494851b…`). The counter does not notice — it reads
`rev:path`, so a re-run after destroying the file still exits **0**. Fix shape: refuse
`st_nlink != 1`, and/or temp-file + `os.replace`.

**F4 — calibration. The guard is CWD-relative, not `--root`-relative.** `plans/round-46-claims.md`
from the lane root → refused (exit 2); the same argv from a seat dir → **accepted, exit 0**, written
to `…/R46W1RevOutputGuard/plans/round-46-claims.md`. No graded byte changes, but a receipt can land
at a path that reads lane-like, and `--root <lane>/.ufo --json-out SKILL.md` refuses with
`"outside the lane root: SKILL.md"` (the argument, not the resolved path). Fix shape: resolve
relative targets against `--root`; print the resolved path.

**F5 — design coupling.** `out_path` uses the hard-coded `GRADED` and not the `frozen_set` the same
module derives. No live hole at the current claims (both frozen entries sit under `GRADED` heads),
but a future freeze outside those heads would be writable while frozen. Fix shape: refuse
`GRADED ∪ frozen_set(root, rev)`.

## Freeze observation (for the L1, not a verdict)

`--freeze 3182047…` (the prompt's, and the commit that first adds both frozen paths) at any later rev
returns exit 2 `frozen_path_changed` for `tools/round-46/{attest.py,gate.py,registry.py}`, because
`50862e4a` and `65678df0` touch `tools/round-46/` afterwards; the lane's receipts already score at
`65678df0…` and later. The prompt, the claims derivation and the scored freeze therefore name
different commits. Reconciling is the L1's call.

## Residual / not run

TOCTOU between `out_path`'s `realpath` and `emit`'s `open` (no `O_NOFOLLOW`/`O_EXCL`, no atomic
rename); `EACCES`/`ENOSPC` instances of F1 (same code path as the measured `FileNotFoundError`, not
separately run); case-insensitive filesystems (n/a here). The real lane was never written: its
`SKILL.md` `2a428bca…` and `gate.py` `847aa33b…` were re-verified against `git cat-file -p HEAD:<path>`
after all runs. No installs; `python3` and `git` only. Scratch root removed before filing.
