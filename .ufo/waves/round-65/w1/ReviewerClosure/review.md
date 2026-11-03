# R65-C1 closure review (ReviewerClosure, w1, round 65)

Read-only review of `tools/round-65/jsc-closure-matrix.py` (514 lines, sha256
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` — re-hashed, matches
the frozen claim) against the frozen predicate and round 64's blocking findings F1/F2
(`.ufo/waves/round-64/w1/ReviewerMatrix/review.md`). The matrix was not run. No LSP
server was available for this file (no lsp device in this session); all checks are
text + programmatic (importlib constant load, read-only globs/greps over the toolchain
tree). Commands run: `sha256sum` (instrument, probe), `wc -l`, read-only globs for the
View8/d8/venv trees and `__pycache__`/`*.pyc`/`*.pth`, a `^(import|from)` derivation
over the View8 tree, and a byte-compare of the predicate in the three artifacts.
Nothing was written outside this report directory; no scratch was created.

## Q&A (one row per question)

| Q | Question | Pointer | Verdict |
|---|---|---|---|
| Q1 | Does CLOSURE pin every file the run reads and every executable it spawns? | CLOSURE L81-108 (27 entries), pins L110-114, check L229-254; spawns: d8 L273-279, view8 L323-326, node L330-331, probe L257-271 | **closed** (residuals named below) |
| Q2 | Does the census cover every write the run could make? | `CENSUS_EXCLUDE = ("jsc2js-src/.git/",)` L77, applied L215-216; symlink skip L212; census before/after L305, L339-340 | **closed** (exclusion is a formal blind spot only) |
| Q3 | Does the cache-free clause fire on a contaminated tree? | `cache_entries` L193-203 (both `__pycache__` dirs and `*.pyc`), folded into `ok` L244/L250-251/L254; operative gate L287-290 (exit 2 before `work_root.mkdir` L304 and census L305); `--manifest` L494-500; selftest covers both classes | **closed** |
| Q4 | Is the predicate sentence byte-identical in plan, claims.json, instrument? | plan L29-33 (quote block, unwrapped), claims.json L15, instrument PREDICATE L68-73 | **closed** — proven `==` True programmatically (importlib constant vs JSON field vs quote-unwrapped plan text) |
| Q5 | Is the do-nothing arm reachable, exit 1, and is the `--skip-run` closure bypass a hole? | dispatch L501-505 (before the required-args check L506-509), `emit` L344-353 (`verified ... and not skip_run` L347) | **closed** (advisory on synthetic receipt fields) |
| Q6 | Does any label class admit a value the predicate counts as matching while the run failed? | classify_dump L145-153, classify_view8 L156-162, classify_check L165-166, compose L169-172, verdict L175-190 | **closed** (semantic limit noted) |

### Q1 detail — derived import closure vs the map

`^(import|from)` over `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src/View8`:

- `view8.py:1-3` — argparse, sys, `Parser.sfi_file_parser`
- `Parser/sfi_file_parser.py:1-5` — `Parser.shared_function_info`, `parse` (venv), re, traceback, typing
- `Parser/shared_function_info.py:1-2` — `Translate.translate`, `Simplify.simplify`
- `Simplify/simplify.py:1-2` — re, `Simplify.function_context_stack`
- `Simplify/global_scope_replace.py:1-2` — re, collections
- `Translate/translate.py:1-3` — `Translate.translate_table`, `Translate.jump_blocks`, re
- `Translate/jump_blocks.py:1` — bisect; `Translate/translate_table.py:1` — ast
- No `__init__.py` exists anywhere in the tree (namespace packages); the View8 dir
  contains exactly 12 files (glob) and all 12 are pinned (L91-102).

The executed route (`view8.py --disassembled`, L323-326) imports 9 in-tree files —
all pinned. `Parser/parse_v8cache.py` (which references `Bin/VersionDetector.exe`,
parse_v8cache.py:9) is imported by nobody on this route, so `VersionDetector.exe` is
never executed; the README documents `--disassembled` as skipping the detector.
Every read file and every spawned executable is pinned: 9 d8-triple files (each build
dir contains exactly `d8`, `snapshot_blob.bin`, `icudtl.dat` — glob-verified; nothing
else for d8 to read), the two artifacts (probe L110, typora L108), the 9-file View8
import closure, `venv/pyvenv.cfg` + `parse/__init__.py` (import read), the resolved
interpreter (INTERPRETER_PIN, resolved at L286/L284, checked L238-243) and node
(NODE_PIN, resolved L285).

Read-but-unpinned (residual, outside any manifest scope): the interpreter's stdlib and
site bootstrap (argparse/sys/subprocess/os/re/traceback/typing/collections/bisect/ast,
site.py) live under the uv CPython, outside the root and outside the census. No `*.pth`
exists under the venv (glob) and site-packages holds only `parse/` +
`parse-1.22.4.dist-info/`, so the exposure is the CPython's own stdlib only.

Pinned-but-never-read (6 of 30, over-pinning, harmless): `README.md`,
`Bin/VersionDetector.exe`, `Parser/parse_v8cache.py`, `parse/__init__.pyi`,
`parse-1.22.4.dist-info/METADATA`, `parse-1.22.4.dist-info/RECORD`. The docstring
"every file the matrix run reads" (L11) over-claims in both directions (includes
unread files; excludes stdlib).

### Q2 detail — the exclusion

The census hashes every regular file under the toolchain root except
`jsc2js-src/.git/` (L77, L215-216), justified in the docstring (git index refresh by a
read-only git call). The run spawns only d8, the venv python and node; none writes git
metadata, and the instrument never invokes git — so no realistic write of the run can
hide behind the exclusion. Formal blind spots: a write under `jsc2js-src/.git/` would
be invisible; symlinks are skipped (L212), so a symlink retarget (e.g. the unpinned
`venv/bin/python` link) or a symlinked directory's contents are census-blind; scope is
the toolchain root only (repo-side `--work`/`--out` writes are outside by design);
mtime-only rewrites are invisible and stated as a limit (docstring L31-32).

### Q5 detail — reachability and the bypass

`--skip-run` is dispatched at L501, before the required-args check (L506-509), so it is
reachable with no other arguments. `emit` computes
`verified = summary.verified and closure.ok and delta.equal and not skip_run` (L347):
with 0/18 matching, verified is False; closure.ok is the fabricated True (L502-503), so
the exit is 1, exactly as the plan's do-nothing control expects (0/18, exit 1).
The bypass IS real — `--skip-run` never touches the tree and fabricates
`closure.ok=True` and `census.equal=True` — but it is not a hole for the claim: the
`and not skip_run` term makes verified/exit 0 unreachable on this path. The cost is
provenance only: the do-nothing receipt carries synthetic closure and census blocks.

## Findings

| id | line | class | severity | evidence |
|---|---|---|---|---|
| A1 | L496 | footgun | advisory | `--manifest` without `--probe` pins PROBE_PIN against `inputs/atom.compiled.dist.jsc` (the Typora artifact) → guaranteed `pin mismatch: probe` and exit 2 for the wrong reason. Every manifest call (incl. controls 2 and 3) must pass `--probe` and record it; A2's manifest-at-freeze (30 entries, ok true) implies it did. |
| A2 | L501-505 | provenance | advisory | `--skip-run` fabricates a green closure and an equal census into the receipt. Not a claim hole (L347 forces verified False); L1 must not cite those blocks as closure evidence. Plan A2 claims only "exit 1, runs_matching 0, skip_run true" — consistent. |
| A3 | L323-326, L330-331 | exit-class (carried r64 F4) | advisory | Uncaught `subprocess.TimeoutExpired`/`OSError` for the view8 (timeout 600) and node (timeout 120) spawns; a missing node binary is not pre-checked (L300-303 covers only the interpreter). Crash = traceback, exit 1, no receipt, where the docstring promises exit 2 could-not-evaluate. No false pass is possible. |
| A4 | L287 vs L339-340 | TOCTOU (carried r64 F6, narrowed) | advisory | Pins are checked once (L287). The after-census now catches any mid-run change to the 27 root entries (all of CLOSURE is under root) — r64-F6's core is repaired — but probe (repo), node (fnm) and interpreter (uv) live outside the root: a mid-run swap of those three stays undetected. |
| A5 | L212 | census limit | advisory | Census skips symlinks: `venv/bin/python` (a symlink) is never censused and the link itself is unpinned — only its resolved target is pinned once. A retarget during the run is invisible to both closure and census. Same for symlinked dirs (rglob does not descend). |
| A6 | docstring L11 vs tree | closure scope | advisory | Stdlib/site bootstrap read by every Python subprocess is pinned nowhere (outside root and census; no `.pth`, site-packages = parse only — verified). The closure is complete only within the toolchain root. |
| A7 | docstring L44-46 vs L275-276, L330-331 | doc overstatement | advisory | "Every subprocess runs with PYTHONDONTWRITEBYTECODE=1 ... and -B in its argv" is true only for the Python spawns (L260-264, L307, L323-326); d8 gets no env override, node no -B. Neither can write Python bytecode — repair substantively complete, wording only. |
| A8 | claims.json A3 vs L103-107 | doc drift | advisory | A3 says "4 venv identity files" inside a "27 toolchain-root entries" total: 9+12+4+1=26; the frozen map has 5 (pyvenv.cfg, L107) and 27 is correct. The plan enumerates all 5 and its 30-entry total is right. Container text only; the map is authoritative. |
| A9 | L91-107 | over-pinning | advisory | 6 of 30 entries are never read by the run (README.md, VersionDetector.exe, parse_v8cache.py, `__init__.pyi`, METADATA, RECORD). Harmless — over-pinning cannot weaken the check — recorded because Q1 asks. |

## Round-64 repair status

- **F1 (unpinned binaries/inputs) — repaired.** D2/D3 `snapshot_blob.bin` + `icudtl.dat`
  now pinned (L85-90), the whole 12-file View8 tree pinned (L91-102), the 5 venv
  identity files pinned (L103-107), node + resolved interpreter pinned (L111-114) and
  checked at L238-243.
- **F2 (`__pycache__` written into the frozen tree) — repaired.** Cache-free
  precondition fires before any run (L287-290), every Python spawn carries `-B` and
  `PYTHONDONTWRITEBYTECODE=1` (L129, L262, L307, L324), and the before/after census
  (L305, L339-340) gates `verified` (L347). The tree is cache-free right now
  (tree-wide globs for `__pycache__` and `*.pyc` returned nothing).

## VERDICT

VERDICT: Q1-Q6 all closed; nine advisory findings (A1-A9), none blocking; r64 F1/F2
repairs present and effective; `--skip-run` bypass is not a claim hole. Instrument is
fit for the operative run provided every `--manifest` invocation passes `--probe` (A1).
