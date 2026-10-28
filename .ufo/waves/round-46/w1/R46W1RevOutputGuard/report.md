# R46W1RevOutputGuard — attack on `gate.out_path` (the R45-CL22 fix)

Seat: `R46W1RevOutputGuard` (wave 1, round 46). Read-only on the lane tree; every test ran in a
throwaway clone under `/fast/scratch/hyaku/kaidoku-r46/R46W1RevOutputGuard/`.

## Anchor

| item | value |
|---|---|
| lane HEAD at measurement | `deee6595ae3dda094aa5a577fac0f6903e873e16` |
| `tools/round-46/gate.py` blob | `9ab7e2a3…`, sha256 `847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223` |
| same blob at | `781e19ae`, `49e6cac4`, `21b55a8f`, `deee6595` (byte-identical, `git diff 781e19ae..HEAD -- tools/round-46/gate.py` is empty) |
| `tools/round-46/attest.py` blob | `936910fe…` from `781e19ae` to `deee6595` (identical) |
| `tools/round-46/registry.py` blob | `c95128c9…` at `781e19ae`, `26f9e9c6…` at `49e6cac4`..`HEAD` (the change is the v1-profile checks only; `main()`/`out_path` usage unchanged) |
| measured verdict pair used for the harness | `--freeze 65678df0… --rev 781e19ae…` → attest exit 0, `failing []` (proves the runs are real evaluations, not early aborts) |
| anchor hashes of the graded surface | `SKILL.md 2a428bca…`, `plans/round-46-claims.md a09564e0…`, `corpus/SOURCES.md 13d14bb5…`, `LOG.md 71bc44ef…`, `SCORECARD.md 14061e38…`, `tools/round-46/attest.py e6c44d2d…`, `gate.py 847aa33b…`, `registry.py 5e16e4af…`, `census.py 960c516d…` |

Method: `git clone --no-hardlinks` of the lane into `$S/lane{,2,3,4}` (four clones: `.git/` writes
poison a clone, so each destructive class got a fresh one). Every case ran
`python3 -I -B <clone>/tools/round-46/{attest,registry}.py --root <clone> --freeze … --rev … --no-battery --json-out <target>`
with CWD = clone root unless stated. A 12-path watch list (`SKILL.md`, `LOG.md`, `SCORECARD.md`,
`SHONEN.md`, `PROVINCE.md`, `plans/round-46-claims.md`, `corpus/SOURCES.md`, the four
`tools/round-46/*.py`, `.git/config`, `.git/hooks/pre-commit`) was sha256-snapshotted immediately
before and immediately after every single run. All receipts are flattened into `receipts/`, the
series letter carrying the clone they came from (A/B/C = clone 1, D = clone 2, E = clone 3, R =
clone 4); the drivers that produced them are in `drivers/`.

## Bottom line

The R45-CL22 hole is **genuinely closed for the six attack shapes the seat names**, and the write
is strictly post-verdict. Two real holes remain, one by construction (hardlink), one by scope
(`.git/**`), plus a documented exit-code promise the code does not keep.

## Table 1 — the seat's targets and their behaviour

`expect` = what the claim "output: `out_path()` refuses any target inside the graded or frozen set
and any path outside the lane root | 2" requires. `Δ` = any watched byte changed (before/after sha256).

| # | `--json-out` target | expect | exit | Δ graded/frozen | target written |
|---|---|---|---|---|---|
| A1 | `SKILL.md` (rel, CWD=lane) | refuse 2 | **2** | none | no |
| A2 | `../../SKILL.md` | refuse 2 | **2** | none | no |
| A3 | `plans/round-46-claims.md` | refuse 2 | **2** | none | no |
| A4 | `corpus/SOURCES.md` | refuse 2 | **2** | none | no |
| A5 | `tools/round-46/gate.py` | refuse 2 | **2** | none | no |
| A6 | `<clone>/SKILL.md` (absolute, inside lane) | refuse 2 | **2** | none | no |
| A6b | `<clone>/.ufo/waves/round-46/w1/…/abs-ok.json` (absolute, inside, non-graded) | allow | **0** | none | yes, receipt JSON |
| A7 | `<clone>/../outside.json` (outside lane root) | refuse 2 | **2** | none | no |
| A8 | `.ufo/waves/…/link-skill.json` → symlink to `SKILL.md` | refuse 2 | **2** | none | no |
| A8b | symlink → `plans/round-46-claims.md` | refuse 2 | **2** | none | no |
| A8c | `.ufo/waves/…/link-tools/round-46/gate.py` → dir symlink into `tools/` | refuse 2 | **2** | none | no |
| A9 | `.ufo/waves/round-46/w1/…/ok.json` (normal receipt path) | allow | **0** | none | yes |
| A10 | `plans/../SKILL.md` | refuse 2 | **2** | none | no |
| A11 | `.ufo/waves/plans/round-46-claims.md` (graded basename under `.ufo`) | allow | **0** | none | yes (shadow file) |
| E1 | `plans/new-file.md` (graded path that does not exist) | refuse 2 | **2** | none | no |
| E2 | `tools` (graded directory itself) | refuse 2 | **2** | none | no |
| E4 | `.ufo/waves/link-tools/round-46/evil.py` → new file inside `tools/` via dir symlink | refuse 2 | **2** | none | no |
| E5 | `../../../../../SKILL.md` from a seat dir (climb out, re-enter at `SKILL.md`) | refuse 2 | **2** | none | no |
| E6 | `.ufo/waves/link-plans/new.md` → new file inside `plans/` via dir symlink | refuse 2 | **2** | none | no |
| C7/E-D5 | `--root <clone>/.ufo`, absolute `<clone>/SKILL.md` | refuse 2 | **2** | none | no |
| C8/E-D6 | `--root <clone>/.ufo`, rel `SKILL.md` | refuse 2 | **2** | none | no |
| C6/D7 | `tools/round-46/gate.py` via **registry.py** | refuse 2 | **2** | none | no |

Every refusal printed exactly one line, `{"reason": "--json-out inside a graded or frozen surface: <rel>"}`
or `{"reason": "--json-out outside the lane root: <arg>"}`, exit 2, and left all twelve watched
files bit-identical. Allowed targets were written with the receipt JSON and the verdict's exit code.

## Table 2 — write ordering (the "written before the verdict" hole)

| question | evidence | answer |
|---|---|---|
| Is `out_path` called before evaluation? | `attest.py:484` / `registry.py:432`, before `gate.main_guard(lambda: evaluate(...))` | **yes — refusal short-circuits evaluation** |
| Is `emit` called after the verdict? | `attest.py:491` / `registry.py:439`, after `main_guard` returns `(code, receipt)` | **yes — strictly post-verdict** |
| Can a refused target still be written when the verdict is exit 0? | B4: `--json-out <clone>/SKILL.md`, verdict would be 0 → exit 2, stdout = refusal only, `SKILL.md` sha unchanged | **no** |
| Does an exit-2 verdict still write an *allowed* receipt? | B5: `--freeze 3182047…` (frozen_path_changed) + `.ufo/…/frozen-touch.json` → exit 2, receipt written, no watched path changed | **yes, and correctly** |
| Does `--selftest` reach `out_path`? | B3: `--selftest --json-out SKILL.md` → exit 0, no write | **no** (returns first; harmless, but selftest cannot test the guard) |

So `emit` truncation happens only after the verdict exists, and never on a refused path. The
"written before the verdict" half of the R45-CL22 row is closed.

## Findings

### F1 (high, exit semantics — both counters). An allowed `--json-out` that cannot be opened exits **1**, i.e. "not met"

`gate.emit` is called **outside** `gate.main_guard` (`attest.py:491`, `registry.py:439`), so an
`OSError` from `open(path, "w")` (`gate.py:209`) escapes `main()`, prints a traceback to stderr,
leaves stdout **empty**, and Python exits **1**.

| command (excerpt) | exit | stdout | stderr |
|---|---|---|---|
| `attest.py … --json-out .ufo/waves` (existing directory) | **1** | empty | `IsADirectoryError: [Errno 21] Is a directory: …/.ufo/waves` |
| `attest.py … --json-out .ufo/nope/x.json` (absent parent) | **1** | empty | `FileNotFoundError: [Errno 2] …` |
| `registry.py … --json-out .ufo/waves` | **1** | empty | `IsADirectoryError: [Errno 21] …` |
| `attest.py … --json-out .ufo/waves` at current HEAD pair (`--freeze 04252247 --rev 49e6cac4`) | **1** | empty | same class |

This is exactly the defect class the round exists to remove (`R45-CL13f`, and the round-45
`c2-counter.py` registry row states it in words: "the exit of an uncaught OSError when `--json-out`
points into a missing directory, so an IO failure is not distinguishable from a scored not-met").
It also contradicts both the module docstring of `main_guard` ("a crash is a could-not-evaluate, not
a verdict") and **the landed registry row for `tools/round-46/attest.py`**, which promises
`2=could-not-evaluate: … or an unhandled exception`. A one-character typo in a receipt directory
therefore records a met measurement as a violation.

Suggested shape (not applied): wrap the `emit` call in `main_guard`, or have `emit` catch `OSError`,
print the receipt JSON to stdout anyway, and return 2.

### F2 (high, scope). `.git/**` is writable and one allowed write makes every later verdict unmeasurable

`GRADED` (`gate.py:35-36`) names `SKILL.md LOG.md SCORECARD.md PROVINCE.md SHONEN.md plans tools
corpus evidence`. `.git` is not in it, and the claim's wording ("graded or frozen set") does not
cover the repository, so the guard lets the counter byte-replace the repository:

| case | target | exit | effect (measured) |
|---|---|---|---|
| D13 | `.git/config` | **0** | `config` replaced by receipt JSON; immediately after, `git -C clone rev-parse HEAD` → rc **128**, `fatal: bad config line 1` |
| D14 | (follow-up) | **128** | every subsequent counter run returns exit 2 `unknown freeze revision` |
| D11 | `.git/hooks/pre-commit` | **0** | hook file created with receipt content (arbitrary code runs on the next commit in that clone) |
| E8 | `.git/refs/heads/main` | **0** | receipt JSON written as a loose ref over the packed one; `git rev-parse HEAD` → rc 128 `unknown revision` — silent branch corruption |
| D12 | `.ufo/state/probe2.json` | **0** | allowed; the fleet contract forbids seats from touching `.ufo/state/`, the guard does not |

The severity is the asymmetry: the *writer* exits 0 while the *revision's measurability* is
destroyed. A single seat that mis-types its receipt path cannot do this accidentally (it would
have to name `.git`), so this is deliberate-only; but the guard's stated job is to stop a
co-operating seat from crossing a boundary it was told about, and `.git` is the one boundary that
kills the measurement rather than a graded document.

Suggested shape (not applied): refuse any head in `(".git", ".ufo/state")` and `.ufo/watchdog.log`,
or invert the rule to an allowlist (`.ufo/waves/**` only) for `--json-out`.

### F3 (medium, realpath limitation). A hard link defeats the guard; the graded/frozen file is truncated with exit 0

`os.path.realpath` resolves symlinks but cannot resolve hard links, so a target inside the allowed
`.ufo/` area whose inode *is* `SKILL.md` passes every check and `open(..., "w")` truncates the
graded inode:

| case | preparation | exit | before → after |
|---|---|---|---|
| C1 / D10 | `ln clone/SKILL.md .ufo/waves/round-46/w1/…/hardlink.json`, then `--json-out` that path | **0** | `SKILL.md 2a428bcaf88e…` → `9494851b4d0d…` (the receipt JSON) |
| R2 | `ln clone/plans/round-46-claims.md …/claimslink.json`, then `--json-out` that path | **0** | claims `a09564e0a2e2…` → `9494851b4d0d…` |

Both graded *and frozen* files are destroyable. Worse, the counter does not notice: it reads
`rev:path` from git objects, so R3 (a re-run after the claims file was destroyed on disk) still
exits **0** with `frozen_derived` intact. The damage is silent until someone commits the working
tree, at which point the freeze measures a file that is now a receipt.

Suggested shape (not applied): `os.lstat` the resolved target and refuse `st_nlink != 1`; and/or
write through a same-directory temp file + `os.replace`, which also fixes the non-atomic
truncation of F4.

### F4 (calibration, semantics). The guard is CWD-relative, not `--root`-relative, and the refusal message hides that

`out_path` computes `os.path.realpath(path)` (CWD-relative) and only then compares with
`realpath(root)`. The same argument text is therefore refused from one directory and accepted from
another:

| case | CWD | argument | exit | written |
|---|---|---|---|---|
| A3 | clone root | `plans/round-46-claims.md` | **2** refused | no |
| D4 | `.ufo/waves/round-46/w1/R46W1RevOutputGuard` | `plans/round-46-claims.md` | **0** | **yes**, at `…/R46W1RevOutputGuard/plans/round-46-claims.md` |

No graded byte changes either way, so this is not a safety hole — it is an evidence-integrity and
diagnosability one: a receipt can land at a path that *reads* like `plans/round-46-claims.md` while
being a shadow file under `.ufo/`, and the refusal message echoes the argument, not the resolved
path (`C8`: `"--json-out outside the lane root: SKILL.md"` for a path that actually resolved to
`<clone>/SKILL.md` while `--root` was `<clone>/.ufo`). Suggested shape (not applied): resolve
`os.path.join(root, path)` when `path` is relative (or refuse relative paths outright), and print
the resolved path in the reason.

### F5 (design coupling). The write guard does not use the frozen set it derives

`out_path` consults the hard-coded `GRADED` tuple; `freeze_state` derives `frozen_derived` from the
claims file (`gate.py:152`). At the current claims both frozen entries (`plans/round-46-claims.md`,
`tools/round-46/`) happen to sit under `GRADED` heads, so there is **no live hole** — but the two
sets are independent, and any future freeze outside `GRADED` (a pinned receipt under `.ufo/`, a
`res/` artefact) would be writable while frozen. Suggested shape (not applied): pass
`frozen_set(root, rev)` into `out_path` and refuse the union.

### F6 (positive — state it, the round needs the closure recorded)

For the eight attack shapes the seat names plus the seven extra shapes above, the refusal is
correct, exit 2, and byte-preserving: relative graded paths, `../` escapes, absolute inside-lane,
absolute outside-lane, **file symlink**, **directory symlink (existing and new filenames)**,
dot-dot normalization, a graded directory, a non-existent graded path, a narrowed `--root`, and the
`registry.py` side of the shared guard. The write is strictly post-verdict and never on a refused
path (Table 2). The R45-CL22 "written before the verdict" defect is closed; the residual holes are
F1 (exit code), F2 (`.git` scope), F3 (hardlink), F4 (CWD), F5 (coupling).

## Freeze boundary observation (context, not my seat's verdict)

The prompt names freeze `31820472784284727546808acc31b3ea1e73919b`, which is the commit that first
adds `plans/round-46-claims.md` **and** `tools/round-46/` (`git log --format=%H -1 -- plans/round-46-claims.md`
→ `3182047…`; `git ls-tree 3182047… tools/round-46/` lists all four tools). But `50862e4a` and
`65678df0` both touch `tools/round-46/` afterwards, so measuring with `--freeze 3182047…` at any
later rev returns exit 2 `frozen_path_changed` with
`["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]`
(reproduced on the clone; `attest.py` blob at the freeze is `25883520…`, at `781e19ae` `936910fe…`).
The lane's own receipts already score at `--freeze 65678df0…` (`c2-at-781e19ae.json`) and later, and
`50862e4a`'s message declares itself "the authoritative freeze". Both behaviours are consistent with
the claims text ("nothing in `tools/round-46/` changes after the freeze: a change makes both
counters exit 2"); what is not consistent is that the *prompt* and the *claims derivation* still
name `3182047…` while the *scores* use a later commit. That is the L1's call to reconcile, and it is
why my harness measured at `65678df0…/781e19ae` (verified exit 0) and re-checked the two decisive
cases at the newest available pair.

## Not run / residual risk

- **TOCTOU**: `out_path` resolves, then `emit` opens later with no `O_NOFOLLOW`/`O_EXCL` and no
  temp-and-rename. A symlink swapped between the two calls, and a crash mid-write, are both
  unexercised; the code read predicts them. Recorded as residual, not measured.
- **Permission-denied (`EACCES`) and `ENOSPC`**: same code path as D2 (`FileNotFoundError`), not
  separately measured, so F1's instance list is one case longer than what I ran.
- **Case-insensitive / bind-mount filesystems**: not applicable on this host's ext4/btrfs layout; not
  tested.
- I did **not** attempt to write into the real lane, and the real lane's `SKILL.md`
  (`2a428bcaf88e…`) and `tools/round-46/gate.py` (`847aa33b…`) were re-verified against
  `git cat-file -p HEAD:<path>` after all runs: unchanged. Each clone's damage (hardlink, `.git/config`,
  `.git/refs/heads/main`) was confined to the clone; `SKILL.md` was restored in `lane`/`lane2` from a
  pre-attack copy and re-hashed, and the scratch root is removed before this report is filed.

## Install log

None. Only `python3` (system) and `git` (system) were used; no package, `uv tool`, or `~/.local/bin`
entry was added or modified.

## Receipts

`receipts/`: A1–A11, B1–B5, C1–C8, D1–D14, E1–E8, R1–R3 (48 JSON receipts; R1–R2 also carry the
raw `.out/.err/.before/.after` captures). Each receipt carries the exact argv, exit code, stdout
sha256 (or empty stdout), the 12-path before/after map, target resolution, and a UTC timestamp.
`drivers/drive.py`, `drive2.py`, `drive3.py` reproduce the A/B/C, D and E series against a fresh
`git clone --no-hardlinks` of the lane; the R series was run inline and its commands are quoted in
F1/F3 and the receipts' `argv`.
