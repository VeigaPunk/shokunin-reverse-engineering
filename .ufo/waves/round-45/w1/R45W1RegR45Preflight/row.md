# Row — `tools/round-45/frozen-path-preflight.py`

Seat `R45W1RegR45Preflight`. Target instrument, frozen at
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
(`git ls-tree` blob `b42398273da0449c01f6f26cc630853d58ea55ec`, 11987 bytes,
mode 100755). Frozen bytes == worktree bytes: sha256
`633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` for both the
`git show <freeze>:…` extraction and the tracked file; `git status --porcelain --
tools/round-45/ plans/round-45-claims.md` printed nothing and `git diff --stat
<freeze>..HEAD -- tools/round-45/ plans/round-45-claims.md` printed nothing.

## Proposed landing row (exact 7 columns, single line)

```markdown
| `tools/round-45/frozen-path-preflight.py` | gate — freeze integrity at commit time (M45-1 fix): five arms `commit`, `blob`, `restored`, `dirty`, `pathspec` — the freeze adds `restored`, `dirty` and `pathspec` to the base's `commit` and `blob` | `0` clean; `1` a frozen path changed, a restored touch, or a dirty worktree; `2` could-not-evaluate, including `pathspec_required` and an unknown or non-ancestor revision | `python3 -I -B tools/round-45/frozen-path-preflight.py --selftest` — 11 cases, 11 green / 0 failures at the freeze; independent kills measured for `dirty` and `pathspec` only — killing `commit`, `blob` or `restored` alone still reads 11/0 | the caller's `--freeze`, `--pathspec` and `--freeze-path`; `plans/round-45-claims.md:132-147` names this round's frozen paths | `--json-out` only; selftest fixtures under `$HYAKU_SCRATCH`, else `$TMPDIR`, else `tempfile.gettempdir()` (host `/tmp`), and no fixture cleanup | kaidoku |
```

Column count: 7 (8 pipes). Table header at `SKILL.md:1634`
`| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |`.

## Column-by-column verification (measured, never read-only-inferred)

| # | column | value in the row | measurement |
|---|---|---|---|
| 1 | tool | `` `tools/round-45/frozen-path-preflight.py` `` | exact backticked path; `tools/round-45/c2-counter.py --rev HEAD` returns it in `registered` with `unregistered: []` (exit 0) |
| 2 | gate or probe | five arms, three new at the freeze | docstring `Arms:` block names `commit`, `blob`, `restored`, `dirty`, `pathspec`; the base instrument at `149133d4:tools/round-45/frozen-path-preflight.py` (107 lines, no `--selftest`) already parses `--name-status` into `touched` and already has the ls-tree/blob backstop, so the measured delta is 3 arms, not 4 |
| 3 | verdict map | `0` clean; `1` violation; `2` could-not-evaluate | measured: `0` on the clean range (`gate-real.stdout`), `1` on touched / restored / dirty / bulk-sweep / narrow-pathspec-blob (`attack.out`), `2` on `pathspec_required` (`attack.out` A3) and on unknown-freeze / non-ancestor (selftest `red-unknown-freeze`, `red-nonancestor`). `c2-counter.exits_ok` (word-boundary `\b0\b\|\b1\b\|\b2\b` on cell 3) accepts it: `thin: []` |
| 4 | self-test command | `--selftest` — 11 cases, 11/0 at the freeze | frozen extraction exits 0 and prints `PREFLIGHT_SELFTEST: cases=11 failures=0`; 11 case lines + 1 summary = 12 stdout lines. Independent-kill result from behavioural mutants M1–M6 (`mutants.out`, `mutants2.out`) |
| 5 | pinned-value path | caller's `--freeze`/`--pathspec`/`--freeze-path`; `plans/round-45-claims.md:132-147` | 132 is `## Frozen paths (exact)`, 134–136 carry the two frozen paths and the `--pathspec tools/round-45/` + `--freeze-path tools/round-45` requirement; the file has ≥147 lines, so the range resolves |
| 6 | write scope | `--json-out` only, selftest scratch, no cleanup | code path `scratch_root()`: `$HYAKU_SCRATCH` → `$TMPDIR` → `tempfile.gettempdir()`; measured `gettempdir()` with both unset is `/tmp`. 9 selftest invocations left 99 fixture dirs / 15 MiB under `$S/kaidoku-r45/preflight-selftest` (no `rmtree`) |
| 7 | owner | `kaidoku` | lane |

## Row delta against `SKILL.md:1639` as currently drafted at HEAD

The row is already present in the working tree (added after the freeze, `SKILL.md`
is not frozen). Three cells need correction before it is cited as verified:

1. **Cell 2** — it lists the five arms without saying which are new, while
   `plans/round-45-claims.md` says "The interpreter gains the four arms". Exact
   facts: base has `commit` + `blob`; freeze has five; delta is `restored`,
   `dirty`, `pathspec` (3) plus `--selftest`. Either the claims sentence or this
   cell states one arm too many. Not repaired here — L1 reconciles.
2. **Cell 4** — "11 cases, green at the freeze" is true but silent on
   independence: only `dirty` (M3 → `red-dirty`) and `pathspec` (M5/M6 →
   `red-dirfreeze-no-pathspec`) fail the selftest when killed. Killing `commit`
   (M4), `blob` (M1) or `restored` (M2) individually still yields `cases=11
   failures=0`, because `red-touched`/`red-restored`/`red-bulk-sweep` are each
   satisfied by a second arm as well. The instrument docstring's "each has a red
   selftest case" is therefore false for three of five arms.
3. **Cell 6** — "$HYAKU_SCRATCH or $TMPDIR" is incomplete: with neither set the
   selftest writes under `tempfile.gettempdir()`, i.e. `/tmp` on this host, and it
   never removes the fixtures.

## Behavioural limits to disclose beside the row (measured, not fixed)

- **A1 (false clean).** `covers()` accepts a pathspec strictly *inside* a frozen
  directory, so `--require-pathspec` passes while the commit arm is scoped
  narrower than the freeze. A sibling added and deleted inside `FREEZE..REV`
  then reads `exit 0 / clean` (fixture `a1`, `attack.out`). With the wide
  `frozen/` pathspec the same history reads exit 1 (fixture `a2`), so the defect
  is the certification of a narrow pathspec, not the parser.
- **A3 (over-strict).** A broader pathspec (`.`) covering the frozen dir is
  refused with exit 2 `pathspec_required` — safe direction, but it rejects a
  strictly-covering pathspec.
- **A4 (false clean).** `--dirty-pathspec` replaces the dirty arm's scope
  entirely (`dirty_pathspecs or pathspecs`); pointing it elsewhere hides a dirty
  frozen file (exit 0), while the default scope catches it (exit 1, `dirty:
  [" M frozen/a.txt"]`).
- **A6 (false positive).** With a file-only freeze path and no `--pathspec`,
  `--require-pathspec` has nothing to guard (a file is not a tree), the commit
  arm falls back to the whole tree, and an unrelated commit reads exit 1. The
  claim's own counting command passes both pathspecs, so scoring is not exposed.
- **`restored` cannot change a verdict.** Every path in `restored` is also in
  `touched` (same commit history, same pathspec), and `ok` requires `touched` to
  be empty, so the arm is a receipt label only; measured subset relation
  `restored ⊆ touched` true in `restored_shape.out`. Its red case is carried by
  the commit arm.
