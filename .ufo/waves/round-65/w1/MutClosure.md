# MutClosure — R65-C1 instrument mutation test (round 65, w1)

## Target and method

Instrument under test, frozen and never edited:
`tools/round-65/jsc-closure-matrix.py`, sha256
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`, 24706 bytes.
All six mutants are byte copies under scratch with exactly one conceptual change each,
asserted to differ from the pristine bytes and `compile()`-checked. Every arm was run on
identical fixtures twice — pristine bytes, then mutant bytes — so a red arm is caused by the
mutation. Full per-mutant log, diffs, commands, exits and hashes:
`.ufo/waves/round-65/w1/MutClosure/mutants.md`; raw payloads:
`.ufo/waves/round-65/w1/MutClosure/evidence/`.

Fixtures (scratch `S=/fast/scratch/hyaku/kaidoku-r65/MutClosure`, deleted at the end of the seat):
`ti` = byte copy of the 27 pinned `CLOSURE` files + that venv's `bin/`, cache-free and
manifest-clean (`ok=true, entries=30`, exit 0); `ti-m4/ti-m5/ti-m6/ti-m6p` = further copies,
each verified cache-free (0) and manifest-clean before use; `farm-full` = 27 symlinks to the
real toolchain files at their pinned paths (pristine `--manifest` exit 0); `farm-missing-D2snap`
and `farm-cache` differ from `farm-full` by exactly one omitted pin / one added
`Parser/__pycache__`. Matrix arms read the round-64 probe
(`a86f6ea0…fd1d710`), the pinned node binary and their copy's `venv/bin/python`; `--work`
always under scratch, except in the two M6 arms where it is placed inside the toolchain copy by
design.

Baseline: pristine bytes, `ti`, `--work` outside the root → `runs_matching 18/18`,
`verified true`, `closure.ok true` (`entries=30`), `census.equal true`, exit 0, wall 511 s.
Observed label classes were exactly the three frozen ones
(`dump-ok|view8-ok|node-fail`, `dump-exit-139|view8-skipped|node-skipped`,
`dump-exit-134|view8-skipped|node-skipped`). Every mutant verdict below is scored against this
green run on the same fixture family.

## Result — 6 mutants, 6 killed, 0 survived

| id | mutation (one change unless noted) | caught by selftest | caught by CLI arm | verdict |
|---|---|---|---|---|
| M1 | delete `"d8-14.8.178.1/snapshot_blob.bin"` from `CLOSURE` | no (CLEAN 34/34) | `--manifest` on `farm-missing-D2snap`: 2 → **0** (`missing=[]`, `entries=29`) | killed |
| M2 | `cache_entries()` → `return []` | yes (2 failures) | `--manifest` on `farm-cache`: 2 → **0** | killed |
| M3 | `compare_censuses()` → `{"equal": True, …}` | yes (3 failures) | `--compare` on differing censuses: 1 → **0** | killed |
| M4 | drop `-B` from view8 argv **and** empty `SUBPROCESS_ENV` | no (CLEAN 34/34) | matrix: 0 → **1**, labels 18/18, `census.added` = 8 `*.cpython-315.pyc` | killed |
| M5 | `classify_dump()` → `return "dump-ok"` | yes (5 failures) | matrix: 0 → **1**, `runs_matching 6/18`, 12 mismatches (`probe D3`, `typora D1/D2/D3`) | killed |
| M6 | `emit()`: `verified = labels_ok and closure_ok` (census clause dropped) | no (CLEAN 34/34) | matrix with `--work` inside root: pristine control **1** (18/18, `census.equal false`, 42 added) → mutant **0** with the same unequal census | killed |

What each kill establishes about the frozen instrument's own controls, on this host:

- **M1** — the manifest really is per-entry (27 + probe + node + interpreter): the pristine
  instrument refuses a tree missing the D2 `snapshot_blob.bin` and names it; the mutant accepts
  the same tree with `ok=true`. The mutated entry is live: the file's real hash equals the pin
  (`601efdc6…e24d`).
- **M2** — the cache clause is not decorative: with `cache_entries()` short-circuited, the
  instrument reports a tree carrying `jsc2js-src/View8/Parser/__pycache__` as `ok=true` and its
  payload becomes byte-identical to the clean-tree pass (`sha256 5b682ec1…`, equal to the
  `farm-full` control) — a reader cannot tell the two apart from the JSON.
- **M3** — `--compare` and the census comparison detect added/changed/removed paths; forcing
  `equal=true` erases all three classes.
- **M4** — the round-64 F2 repair is load-bearing and is caught *by the census clause*, not by
  the cache check: the run starts cache-free (`closure.cache_present=[]`), the unsuppressed
  view8 imports write 8 `.pyc` under `View8/{Parser,Simplify,Translate}/__pycache__` and
  `venv/…/parse/__pycache__`, and `census.equal=false` drives exit 1 while labels still match
  18/18. No selftest case notices the missing `-B`/env.
- **M5** — the label fixtures are meaningful in both directions: the classifier is exercised on
  rc 0/1/-6/-11/`"timeout"` and its forced-`dump-ok` version turns `probe D3` (rc 139) and
  `typora` (rc 134) cells into `dump-ok|view8-empty|node-skipped`, breaking 12 of 18 labels and
  the end-to-end verdict.
- **M6** — clause (iii) is reachable and independent: with labels matching and the census
  unequal (cells written inside the root), pristine exit is 1 and the mutant exit is 0 with
  `verified=true` alongside `census.equal=false`. The mutant's own payload is self-contradictory;
  nothing but the exit code distinguishes it.

## Coverage findings (frozen bytes; reported, not repaired)

1. **The selftest cannot pin the closure count.** `closure-nonempty` is `len(CLOSURE) >= 20`
   and `closure-missing-count` is `len(CLOSURE) + 3` — both relative to the dict under test.
   Dropping an entry passes 34/34 (M1) and yields `ok=true, entries=29`. The predicate says
   "count and sha256"; the count is only self-consistent, so a receipt consumer must compare
   `closure.entries` against the frozen 30, not trust the field.
2. **No selftest case exercises subprocess spawning or its environment.** M4 (missing `-B`/env)
   and M6 (`emit` never called with an unequal delta) both leave the selftest CLEAN. Only
   end-to-end arms catch them; the selftest's reach stops at pure functions.
3. **Clause ordering leaves one unguarded slot.** `closure_findings` (line 287, cache check at
   244) and `before = census(root)` (305) both run *before* `python_probe` (300). Bytecode
   written by the probe would therefore be absent from `cache_present` and present in both
   census maps → invisible to clauses (i) and (iii). The frozen probe argv carries `-B` (262)
   and inherits `SUBPROCESS_ENV`, so nothing is written today; this is an ordering limit of the
   instrument, not an observed failure, and it was not exercised further (out of seat scope).
4. **`census()` skips symlinks while the manifest hashes through them** (`is_file()`/
   `sha256_file()` follow links; `census` does `if p.is_symlink(): continue`). A symlink-farm
   toolchain satisfies the manifest while contributing nothing censused. The real root is
   regular files, so this is not a hole in the operative run; it is why the M1/M2 fixtures are
   manifest-only arms.

## Independent observations for the C1 reviewers

- Pristine bytes on an isolated byte copy of the 27 pins reproduce all 18 frozen labels with
  `closure.entries=30` and an equal census, exit 0 (`evidence/base2.json`, 511 s). This is a
  scratch rehearsal, not the operative run.
- The frozen toolchain root was cache-free at the 20:27, 20:42 and 20:46 checks
  (`__pycache__`/`*.pyc` count 0), the D2 snapshot hash still equals its pin, and the frozen
  instrument hash is unchanged (this seat only read both).
- **Transient contamination seen, source not this seat:** at 20:27:4x `find` reported
  `jsc2js-src/View8/{Parser,Simplify,Translate}/__pycache__` and
  `venv/…/site-packages/parse/__pycache__` (directories, zero `*.pyc`), gone by 20:28. All of
  this seat's writes were under `$S`; the directories were not created by these commands. A
  real run launched inside such a window exits 2 by design, but a sibling fixture inside the
  frozen root can also perturb a concurrent run's before/after census — worth a look by the L1
  when reconciling the operative receipt.
- No write reached the real tree or the real interpreter: 0 files newer than 20:20 under
  `/home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu`, 0 cache entries under
  the frozen root afterwards.

## Limits

Manifest arms use symlink farms (regular-file copies only for the matrix arms); matrix arms run
against byte copies of the pinned files plus a copied venv whose `sys.prefix` is the copy
(verified), never the frozen root. One change per mutant, one run per arm — no repetition, so
flake cannot be excluded statistically; none was observed (all arms were internally consistent
across 18 reps × 6 cells). No survivor, so no defect is asserted against the frozen instrument.
Scratch `/fast/scratch/hyaku/kaidoku-r65/MutClosure` was deleted at the end of the seat; the
evidence payloads and the diff log are preserved under
`.ufo/waves/round-65/w1/MutClosure/` (`mutants.md`, `evidence/`).

Report: .ufo/waves/round-65/w1/MutClosure.md
