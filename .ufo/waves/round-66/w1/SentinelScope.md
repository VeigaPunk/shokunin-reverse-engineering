# SentinelScope — r66-w1 report

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · tip `7b63dd5d5199ed30bc3f213573d8594434a18eb6`
(`main`, detached HEAD) · audited commits `b5b02e1f`, `78fa9666`, `7b63dd5d` · read-only, no lane edit,
no tool installed (pacman untouched), scratch deleted.

Full detail, commands and evidence tables: `.ufo/waves/round-66/w1/SentinelScope/audit.md`.

## Verdicts

| # | Surface | Verdict |
|---|---|---|
| 1 | Write scope of the round's three commits | **clean** |
| 2 | Secret material in new/changed bytes | **clean** |
| 3 | Toolchain integrity + file count | **clean** (entries 30, cache empty, 105 files, delta 0) |
| 4 | Frozen-path integrity (4 paths) | **clean** (freeze = tip = disk, sha256 = claims pin) |
| 5 | Registry rows for `tools/round-66` | **clean** (2 rows, 7 cells, no escaped pipe, 0/1/2) |

## Evidence pointers

1. **Scope** — `git diff-tree --no-commit-id --name-status -r <c>` per commit: 14 distinct paths, 12 A /
   2 M, insertions only (+8 / +1531 / +230, 0 deletions). All lane-relative; 0 absolute, 0 `..`, 0
   fleet-root. The fleet repo does not contain these commits (`git cat-file -t b5b02e1f` → fatal,
   exit 128), so no fleet-root path can appear. `LOG.md`/`SKILL.md` are the lane's copies (lane
   toplevel `…/kaidoku-shokunin`).
2. **Secrets** — 0 hits for private-key headers/`op://`/cookie jars, 0 for bearer-token/password
   assignments, 0 for `ghp_`/`sk-`/`xox*`/`AKIA`/`AIza`/`OPENSSH`/`age1` shapes, 0 base64 runs ≥100.
   All 10 distinct 32+ hex values resolve: 3 git commit ids (40-hex base/carry-in/instruments), 6
   sha256 pins of named files (re-verified with `sha256sum` — closure-boundary, coverage-selfcheck,
   both control scripts, `tools/round-65/jsc-closure-matrix.py`), `recipe_a_block_sha256` (named by
   its key), and `sha256("abc")` (selftest oracle; recomputed `printf 'abc' | sha256sum` → identical).
3. **Toolchain** — `TMPDIR=$S python3 -I -B tools/round-65/jsc-closure-matrix.py --manifest
   --toolchain-root /home/vgpnk/.local/share/kaidoku-jsc --probe …/round-64/inputs/probe-electron.jsc`
   → exit 0, `{"cache_present": [], "entries": 30, "findings": [], "missing": [], "ok": true,
   "pin_mismatch": []}`. `find … -type f -not -path '*/.git/*' | wc -l` → **105**, delta 0 vs the r65
   freeze; composition 9 (3 d8 builds × 3) + 1 inputs + 72 jsc2js-src (12 View8 + 60) + 23 venv = 105.
   0 `__pycache__`/`*.pyc`; 0 files modified in the last 20 min (newest is `jsc2js-src/.git/index`,
   19:43, pre-session) — the read-only run left the tree untouched.
4. **Frozen paths** — `closure-boundary.py` `3d36f91a`, `coverage-selfcheck.py` `3751998c`,
   `c1-do-nothing.py` `2dd5f178`, `c2-do-nothing.py` `f95aabe6`: blob at `7b63dd5d` = blob at `main` =
   worktree `hash-object`, and each sha256 equals its `claims.json` instrument pin. Ordering atoms hold
   (`merge-base --is-ancestor` exit 0 for both `b5b02e1f` and `78fa9666` into the freeze).
5. **Registry** — `SKILL.md:1856` and `:1857` at the tip, 8 pipes / `NF=9` = 7 cells each, matching the
   7-column header at `:1782`; 0 escaped `\|`; both verdict cells name 0/1/2 with explicit
   could-not-evaluate conditions.

## Observations (no verdict impact)

- **O1** A blank line at `SKILL.md:1822` breaks the instrument registry into a second, headerless run
  before the round-47 rows. Verified identical at base `311079d8:1822` → pre-existing, outside this
  round's write scope. Rendering-only; flagged for any future cell-count sweep.
- **O2** `closure-boundary.py:455` hardcodes an fnm node path for the selftest default (`--node` is
  overridable). Portability nit: without that exact version the selftest arm degrades instead of
  passing silently. `:80`'s `DEFAULT_TOOLCHAIN` is the seat-specified root and is expected.
- **O3** Write-scope claim confirmed statically: all write call sites in both counters target
  `--work`/`--out`/`TMPDIR` (closure-boundary `:175,176,213,327`; coverage-selfcheck `:199,285,365,397`),
  `rmtree` stays inside those scratch roots, subprocess is argv-only (no `shell=True`), and the only
  git subcommands invoked are read-only (`show`, `ls-tree`).
