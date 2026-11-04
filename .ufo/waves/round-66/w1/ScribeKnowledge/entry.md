# Closure-counter boundaries and the coverage self-assessment — round 66

source: S??? — the round-66 SOURCES row for CPython 3 `sys.dont_write_bytecode`
(`https://docs.python.org/3/library/sys.html`; scope: the environment variable sets the flag that
`-B` sets) was not on disk when this body was written: `.ufo/waves/round-66/w1/ScoutSources/` does
not exist and an `ls` of it plus a `find -name row.md` under `.ufo/waves/round-66` found nothing.
The registry's last row is S266, so the next free id is S267, but
the id and the located quote are the scout's to supply; this entry asserts no quote. Everything
else is sourced from the two frozen instruments `tools/round-66/closure-boundary.py`
(sha256 `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b`) and
`tools/round-66/coverage-selfcheck.py`
(sha256 `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`), both re-hashed this
round; the first loads `tools/round-65/jsc-closure-matrix.py` by path under sha256
`79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6` and refuses to run on any
drift.
verified-at: round 66, base `311079d869f068bc083a8d180977e49634120fdf`, operative freeze
`7b63dd5d5199ed30bc3f213573d8594434a18eb6`; measured at the base (receipts
`.ufo/waves/round-66/l1/pre/dryrun-c1-verify.json` and
`.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json`) and at the freeze
(`.ufo/waves/round-66/w1/ExecClosure/verify.json`,
`.ufo/waves/round-66/w1/ExecCoverage/selfcheck-at-freeze.json`)
recheck: `python3 -I -B tools/round-66/closure-boundary.py --selftest` (30 cases, 0 failures) and
`python3 -I -B tools/round-66/closure-boundary.py --verify --repo . --out RECEIPT` (exit 0, 5/5);
`python3 -I -B tools/round-66/coverage-selfcheck.py --selftest` (26 cases, 0 failures) and
`python3 -I -B tools/round-66/coverage-selfcheck.py --selfcheck --rev REV --out RECEIPT` (exit 0
only where the `## Owned axes` coverage row is re-derived at REV). Selftest counts are as committed
at `l1/pre/selftest-c1.txt` and `l1/pre/selftest-c2.txt`; this body re-ran neither.

## What the two counters decide

`closure-boundary.py` is the new freeze that repairs the r65 closure counter's three routed
defects: it loads the frozen r65 module under its sha256 pin and re-hosts `CLOSURE`,
`cache_entries` and the census in one ordered check — pre-probe pin check, the probe, the
post-probe cache scan, the count assertion — and it removes `--skip-run`'s synthetic closure.
`coverage-selfcheck.py` is the new freeze that repairs the coverage ground: recipe A transcribed
with its hidden-filename list, the committed SCORECARD block re-run at the same revision for
equivalence, and two self-assessment atoms re-derived from the `## Owned axes` coverage row.
`closure-boundary.py` does not edit the r65 instrument — a drift in its pinned bytes is exit 2 —
and `coverage-selfcheck.py` reads its inputs only as git objects at `--rev` (its one write is the
extracted recipe-A block under `--work`).

R66-C1 clause → emitted field (`--verify`):

- a1 → `arms[0].detail.ok`, `.cache_present`, `.findings`; the arm condition is
  `ok is True and cache_present == [] and count_ok is True` on a fixture whose two-file manifest
  plus three external pins is five entries.
- a2 → `arms[1].detail.ok`, `.cache_present`, `.probe`; the condition is
  `ok is False and bool(named_pyc) and probe.ok is True`, with `named_pyc` filtering
  `cache_present` for entries ending `.pyc`.
- a3 → the real-toolchain closure object's `entries`, `count_ok`, `ok`, `findings`; the condition
  is `ok is True and count_ok is True and entries == 30`.
- a4 → the truncated-manifest closure object's `entries`, `count_ok`, `ok`, `dropped_entry`,
  `findings`; the condition is `ok is False and count_ok is False and entries == 29 and
  "count 29 != 30" in findings`.
- a5 → `skip_run_receipt`'s `closure: null`, `closure_claimed: false`, `verified: false`,
  `exit: 1`.
- top level → `passed` of `arms_total` (5), `ok`, `exit` (0 verified / 1 not verified /
  2 could-not-evaluate); `v1_pin` is the loaded r65 digest.

R66-C2 clause → emitted field (`--selfcheck`):

- `recipe_a_equivalent` → `recipe_a_equivalence()` returns `recipe_a_equivalent`,
  `recipe_a_diffs`, `recipe_a_block_sha256`, `recipe_a_block_keys` and `recipe_a`; `--selfcheck`
  re-emits all but `recipe_a_block_keys`. `diffs` is computed over the nine `RECIPE_A_KEYS` after
  the committed SCORECARD heredoc is extracted at `--rev` and run as its own subprocess at the same
  revision.
- `recipe_a_hidden` → `recipe_hidden(files, section)` = the sorted set of knowledge stems minus
  the date tokens `2026-10-\d{2}-[a-z0-9-]+`; emitted as `recipe_a_hidden` and
  `recipe_a_hidden_count`, and `bool(hidden)` is one of the four `ok` conjuncts.
- `mismatches` → the two atoms `A1-head-score` and `A2-cited-fraction` under `atoms`, with
  `mismatches = sum(1 for a in atoms if not a["ok"])`; `ok` also requires `stem.mapped > 0`.
- the base arm → the same counter at `--rev 311079d869f068bc083a8d180977e49634120fdf`, where
  `A2-cited-fraction` is false.
- exit → 0 verified / 1 not verified / 2 could-not-evaluate (unparseable coverage row, missing
  `## Coverage map` section, absent recipe-A block, unknown revision, failed git call).

## The five C1 boundary arms

| arm | what it decides | emitted field | before-arm → freeze |
|---|---|---|---|
| a1 guarded fixture green | the fixture probe with `-B` and `PYTHONDONTWRITEBYTECODE=1` leaves the closure green with an empty post-probe cache | `arms[0].detail.ok`, `.cache_present` | true → true |
| a2 unguarded fixture red | the same probe with neither guard turns the closure red and names a `.pyc` path while the probe itself still succeeds | `arms[1].detail.ok`, `.cache_present`, `.probe.ok` | false → true |
| a3 real manifest count green | the frozen 27-key map plus three external pins verifies at exactly 30 entries with `count_ok` | `closure.entries`, `.count_ok`, `.ok` | false (r65 has no `count_ok` line) → true |
| a4 truncated manifest red | the same manifest one entry short reports `entries 29` and the finding `count 29 != 30` | `closure.entries`, `.count_ok`, `.dropped_entry`, `.findings` | false (r65 `--manifest` exits 0 at 29) → true |
| a5 skip-run no closure | `--skip-run` emits no closure object that claims ok | `closure`, `closure_claimed` | false (r65 hardcodes `closure.ok true`) → true |

Before-arm source: `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` (1 of 5, a1 only).
Freeze source: `.ufo/waves/round-66/w1/ExecClosure/verify.json` (5 of 5, exit 0).

## The three C2 conditions

| condition | what it decides | emitted field | before-arm → freeze |
|---|---|---|---|
| recipe-a equivalence | the committed SCORECARD recipe-A block at `--rev` reproduces the counter's own recipe A on all nine keys | `recipe_a_equivalent`, `recipe_a_diffs`, `recipe_a_block_sha256` | false (the r65 date mode shares only `mapped`) → true (`diffs {}`) |
| recipe-a hidden list | the date-token numerator's unmapped stems are emitted as names, not as a count | `recipe_a_hidden`, `recipe_a_hidden_count` | false (r65 emits `population_dropped: 3`, no names) → true (3 names) |
| self-assessment atoms | the `## Owned axes` coverage row's head score and cited fraction equal the stem recipe's at the same revision | `atoms` (A1-head-score, A2-cited-fraction), `mismatches` | false (r65 emits no atoms) → false at the base **and** at the freeze: `mismatches 1`, A2 claimed `142/142` vs observed `145/145` |

Before-arm source: `.ufo/waves/round-66/l1/controls/c2-do-nothing.json` (0 of 3).

## Measured numbers

### Base — `311079d869f068bc083a8d180977e49634120fdf`

R66-C1, receipt `.ufo/waves/round-66/l1/pre/dryrun-c1-verify.json` (exit 0, `scratch`
`/fast/scratch/hyaku/kaidoku-r66/l1/verify`): `passed` 5 of `arms_total` 5; `count` 30;
`v1_pin` `79a4dca4…c6`. a2 `cache_present` = `__pycache__`,
`__pycache__/fixture_mod.cpython-315.pyc`; a3 `entries` 30, `count_ok` true, `findings` []; a4
`entries` 29, `dropped_entry` `d8-14.7.173/d8`, `findings` `["count 29 != 30"]`; a5 `closure`
null, `closure_claimed` false. Before-arm, receipt
`.ufo/waves/round-66/l1/controls/c1-do-nothing.json`: 1 of 5 (`a1` only); a4's r65 reproduction
ran its own `--manifest` at `entries 29, ok true, exit 0`, and a5's r65 `--skip-run` emitted
`closure.ok true`.

R66-C2, receipts `.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json` and
`.ufo/waves/round-66/w1/ExecCoverage/selfcheck-at-base.json` (both exit 1): `recipe_a_equivalent`
true, `recipe_a_diffs` {}, `recipe_a_block_sha256`
`1d697af103985da0d056f6d0113059891a7658c1a3c4fbf568720166cf44a0db`. Recipe A: `knowledge_files`
145, `mapped` 142, `missing` the three non-October names
(`2026-11-03-r65-jsc-closure-matrix`, `jsc-mapper-cli-contract`,
`jsc-mapper-release-inventory`), `dangling` [], `citation_resolved_rules` 27, `rule_blocks` 27,
`coverage_score` 9.79, `depth_score` 10.0. `recipe_a_hidden` 3 (the same three names). Stem
recipe: `mapped` 145 of 145, `mismatches` 0, `stem_score` 10.0. Atoms: A1-head-score true
(`10.0` vs `10.0`), A2-cited-fraction false (claimed `[142, 142]` vs observed `[145, 145]`);
`mismatches` 1, `ok` false. Before-arm, receipt
`.ufo/waves/round-66/l1/controls/c2-do-nothing.json`: 0 of 3 (the r65 date mode shares only
`mapped`, emits `population_dropped` as an integer, and carries no atoms).

### Freeze — `7b63dd5d5199ed30bc3f213573d8594434a18eb6`

R66-C1: `.ufo/waves/round-66/w1/ExecClosure/verify.json` (exit 0) — 5 of 5, the same five arm
details as the base receipt. `.ufo/waves/round-66/w1/ExecClosure/manifest.json` (exit 0) —
`closure`: `entries` 30, `expected_count` 30, `count_ok` true, `cache_before` [], `cache_present`
[], `missing` [], `pin_mismatch` [], `probe` `{ok: true, message: ok}`, `findings` [], `ok` true.
`.ufo/waves/round-66/w1/ExecClosure/skiprun.json` (exit 1) — `closure` null,
`closure_claimed` false, `verified` false, `runs_total` 0, `receipts` [].

R66-C2: `.ufo/waves/round-66/w1/ExecCoverage/selfcheck-at-freeze.json` (exit 1) — every field
equal to the base receipt except `rev` and `recipe_a.revision` = `7b63dd5d…`:
`recipe_a_equivalent` true, `recipe_a_hidden` 3, stem 145/145 with `mismatches` 0, atoms A1 true
and A2 false, `mismatches` 1, `ok` false. The
`## Owned axes` coverage row still cites `142/142` against `145/145` at the freeze, so the C2
predicate's measured-revision clause is **not** green at the freeze; its after-arm is the
landing's repair of that row, and no after-arm receipt existed when this body was written.

## Limits

- The ordering proof is fixture-only. a2 discriminates the two orders with a two-file fixture
  (`fixture_mod.py`, `blob.bin`) imported by a real subprocess, because the unguarded import writes
  `__pycache__/fixture_mod.cpython-315.pyc`. a3 runs the real probe on the real toolchain root, but
  with `-B` and `PYTHONDONTWRITEBYTECODE=1`, so its empty `cache_present` is consistent with either
  ordering and cannot discriminate. The 18-cell matrix is not re-run: the fix is demonstrated on
  the fixture and then applied, not re-demonstrated on the full run.
- The cache observation is bounded to two instants. `closure_state` calls `cache_entries` before
  and after `probe_fn()` and compares nothing else; a cache written and removed between the scans,
  or an mtime-preserving byte-identical rewrite of an existing path, is not detected and is not
  claimed detected (the r65 entry's QUALITY #19 limit survives).
- `count_ok` is a cardinality test. `entries = len(manifest) + 3` and `count_ok = entries == 30`
  prove the count, not the identity of the 30 paths; identity is only as strong as the
  sha256-pinned `mod.CLOSURE` dict the counter loads. a4 shows the cardinality red, not a key-set
  comparison.
- The stem recipe's bare-token rule is permissive in one direction and blind in the other.
  `map_tokens` counts every backticked claim-shaped token (`[a-z0-9][a-z0-9-]+`) toward `mapped`,
  so a bare undated token matches a file even where the map never writes `knowledge/`; but
  `dangling` only considers tokens marked `claimed` (`knowledge/`-prefixed or date-dated by
  `DATED_STEM_RE`), so an undated, unprefixed token that names no file is invisible and
  `mismatches 0` does not prove the map is free of dead bare references. Non-file tokens that
  happen to equal a stem would also count as mappings.
- `--equiv` is not cheap. `recipe_a_equivalence` extracts the SCORECARD heredoc and runs it in a
  fresh subprocess of the counter's own interpreter (`sys.executable -I -B`) with `cwd` at the lane
  root and a 900 s timeout;
  the block itself calls `git show` for `SKILL.md` and, through recipe A's line counter, once per
  cited knowledge file, so every `--selfcheck` pays a full recipe-A reproduction (27 rule blocks)
  on top of the parent's own `git` reads. It also compares only the nine `RECIPE_A_KEYS`: a tenth
  key the block might emit is ignored.
- a3 and a4 need the read-only toolchain root. When it is absent, `run_verify` returns 2 before
  `emit`, so no receipt is written and the two fixture arms' results are not preserved; and
  `--manifest` signals a red closure with exit 2 (`0 if st.ok else 2`), unlike `--verify`'s 1.
- The counters decide their own predicates; they do not decide the claims. R66-C1 is 5/5 at the
  freeze by its emitted fields. R66-C2 is not green at the freeze, and this entry records that
  number rather than a landing result.
