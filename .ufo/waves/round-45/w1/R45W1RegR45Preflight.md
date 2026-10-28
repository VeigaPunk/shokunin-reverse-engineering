# R45 wave-1 registration — `tools/round-45/frozen-path-preflight.py`

Seat: `R45W1RegR45Preflight` (read-only on the lane tree; writes confined to
`.ufo/waves/round-45/w1/R45W1RegR45Preflight/`). Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, rev `faa875bc0eb839d15b83c4afa6078819e5a7b381`.
Row drafted and parsed: `row.md`. Per-command receipts: `receipt.md`.

Frozen bytes were verified identical at the freeze and in the worktree (sha256
`633ebc05…30523b`, git blob `b4239827…5ec`, 11987 bytes) and
`git diff --stat f762b727..HEAD -- tools/round-45/ plans/round-45-claims.md` is empty,
so every measurement below is of the frozen instrument.

## Answer to the assigned question

- **Exact 7-column row** — `row.md`. Header `SKILL.md:1634`
  (`tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value
  path | write scope | owner`); the row is 8 pipes = 7 cells; first cell is exactly
  `` `tools/round-45/frozen-path-preflight.py` ``. Parsed with the frozen
  `c2-counter.py` parser: `tool == "tools/round-45/frozen-path-preflight.py"`,
  `exits_ok true`; `c2-counter --rev HEAD` reports it `registered`, `thin []`,
  `unregistered []`, exit 0.
- **Exit cell** names `0` clean, `1` violation (a frozen path changed, a restored
  touch, or a dirty worktree), `2` could-not-evaluate (incl. `pathspec_required`,
  unknown/non-ancestor revision). All three were measured, not inferred: 0 in
  `gate-real`, 1 in A2/A4b/A5/A6 and selftest touched/restored/dirty/bulk-sweep,
  2 in A3 and selftest unknown-freeze/non-ancestor.
- **Arms** — the instrument enumerates **five**: `commit`, `blob`, `restored`,
  `dirty`, `pathspec`. The base instrument (`149133d4`) already had `commit` and
  `blob`, so the measured delta at the freeze is **three** new arms plus
  `--selftest`. `plans/round-45-claims.md` says "The interpreter gains the four
  arms" — one more than measured. Flagged for L1, not repaired.
- **Selftest case count measured: 11**, `failures=0`, exit 0, from the frozen
  extraction (`PREFLIGHT_SELFTEST: cases=11 failures=0`; 12 stdout lines). The
  drafted row's "11 cases, green at the freeze" is accurate.

## Findings (all measured against the frozen bytes; nothing was fixed)

1. **Three of the five arms are not independently proven red.** Killing one arm
   at a time and rerunning `--selftest`: `dirty` → 1/11 fails (`red-dirty`);
   `pathspec` → 1/11 fails (`red-dirfreeze-no-pathspec`, both by disabling
   `--require-pathspec` and by forcing `covers()` true); but `commit`, `blob` and
   `restored` each still give `cases=11 failures=0`. Their red fixtures are
   double-covered. This falsifies the docstring's "each has a red selftest case";
   the row's cell 4 is silent on it and should say so.
2. **`restored` can never change a verdict.** Every path in `restored` is also in
   `touched` and `ok` requires `touched` empty; measured subset relation in a
   tamper-then-restore fixture (`restored ["frozen/a.txt"]` ⊂ `touched
   ["frozen/a.txt","frozen/a.txt"]`). The arm is a receipt label, not a
   classifier — relevant because R44-CL10 is the restore-defect routing.
3. **A1, false clean.** `covers()` accepts a pathspec strictly *inside* a frozen
   directory, so `--require-pathspec` passes while the commit arm's `git log`
   scope is narrower than the freeze. A sibling added and deleted inside
   `FREEZE..REV` then reads exit 0 `clean`; the same history with `--pathspec
   frozen/` reads exit 1. Existing-path edits are still caught by the literal
   directory entry behaving as a tree hash (A5 → `blob_changed ["frozen"]`).
   Not reachable from the claims' own counting commands, which pass
   `--pathspec tools/round-45/` exactly.
4. **A4, false clean.** `dirty_pathspecs or pathspecs` replaces the dirty arm's
   scope; `--dirty-pathspec elsewhere.txt` hides a dirty `frozen/a.txt` (exit 0)
   where the default scope catches it (exit 1).
5. **A3 over-strict.** A strictly broader pathspec (`.`) is refused with exit 2
   `pathspec_required` although it covers the frozen directory. Safe direction,
   still a wrong refusal.
6. **A6 false positive.** A file-only `--freeze-path` with no `--pathspec` leaves
   `--require-pathspec` nothing to guard (files are not trees) and the commit arm
   falls back to the whole tree, so an unrelated commit reads exit 1. Scoring is
   not exposed (both pathspecs are always passed).
7. **Write-scope cell incomplete.** `$HYAKU_SCRATCH` → `$TMPDIR` →
   `tempfile.gettempdir()`; measured `/tmp` when both are unset, and the selftest
   never removes its fixtures (99 dirs / 15 MiB after 9 invocations). The row cell
   names only the first two.
8. **Row already present at HEAD** (`SKILL.md:1639`, added post-freeze by
   `faa875bc`, `SKILL.md` is not frozen). Its cell 2 (five arms, no delta) and
   cell 6 are the two factual gaps; cell 3 and cell 4 check out as written.

## Evidence index

| item | where |
|---|---|
| proposed 7-column row, column-by-column verification, row delta | `w1/R45W1RegR45Preflight/row.md` |
| R1–R13 receipts (command, exit, sha256, UTC mtime) | `w1/R45W1RegR45Preflight/receipt.md` |
| selftest 11/0 (frozen extraction) | receipt R2, sha256 `9f03df65…` |
| real-lane gate clean freeze..HEAD | receipt R3, sha256 `4b5a685d…` |
| A1–A6 attacks | receipt R4, sha256 `04def84e…` |
| arm mutants M0–M6 | receipts R5/R6, sha256 `0fd44620…`, `f8049aa7…` |
| `restored ⊆ touched` | receipt R7, sha256 `e70dc979…` |
| c2 at HEAD 0 / c2 at freeze 1 | receipts R8/R9 |
| c1 at HEAD 0 (cross-check) | receipt R10 |

## Risks

- The depth claim's "four arms" and the row's five-arm list must be reconciled in
  one sentence, or the registry and the claims file disagree on the same
  instrument while both are cited as evidence.
- If a future seat passes a narrower `--pathspec` under a directory freeze, this
  gate can certify a history that touched a frozen path (A1). The sound shape is
  a pathspec equal to the frozen directory or broader; `covers()` currently
  rewards the opposite.
- The restore classifier does not classify anything beyond `touched`; do not cite
  it as the R44 restore defect's fix without that caveat.

## Blockers

None. No install or upgrade was needed or performed. Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45Preflight` was removed after the
receipts above were written; no tracked file outside this wave directory was
touched and no mutating git/jj command was run.
