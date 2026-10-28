# R45W1RegR45C2 — receipt

Seat `R45W1RegR45C2`, round 45 wave 1. Every run below executed the **frozen** bytes
extracted from `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, with `TMPDIR`/`HYAKU_SCRATCH`
pointed at `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR45C2`. Nothing under `/tmp` is cited.
All timestamps UTC, `2026-10-28`.

## Identity

| item | value |
|---|---|
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (`git log --format=%H -1 -- plans/round-45-claims.md` → same) |
| base | `149133d47aa7e90796f96047afe6d251a3e65b2c` |
| instrument blob at freeze | `7d83de6258cb624b1ebb0e18c326cf9fb5fd1aee` (mode 100755) |
| instrument sha256 | `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025`, 9560 bytes, 268 lines |
| instrument sha256 at `HEAD` | identical — unchanged |
| scope blob at freeze | `4855e97e497e329737f00076bdf686bf71b0827d` |
| scope sha256 | `6e2dda713a474dd6479a0af1430af9f38013d058a7cf9d2cc3fe293b9bd8dff9`, byte-identical at freeze and `HEAD` |
| claims sha256 | `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e`, byte-identical at freeze, `HEAD` and the worktree |
| commits in `FREEZE..HEAD` touching `plans/round-45-claims.md` or `tools/round-45/` | **none** (`git log --name-only --format= f762b727..HEAD -- plans/round-45-claims.md tools/round-45` printed nothing) |
| `HEAD` measured | `faa875bc0eb839d15b83c4afa6078819e5a7b381` |

## Lane-level runs

| id | command | exit | stdout sha256 | len | UTC |
|---|---|---|---|---|---|
| `lane-selftest` | `python3 -I -B <S>/frozen/c2-counter.py --selftest` | **0** | `aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d` | 501 | 15:43:14Z |
| `lane-do-nothing-freeze` | `python3 -I -B <S>/frozen/c2-counter.py --root <LANE> --freeze $FREEZE --rev $FREEZE --json-out <S>/ctl2.json` | **1** | `d6e202aac80ee78d9a6fbd1113ea5b62fb51b27503faccb38dec8afdb9216dd0` | 905 | 15:43:14Z |
| `lane-score-HEAD` | same with `--rev HEAD` | **0** | `398b6dc6e7f0a76656bf26b1e806e602c7f1346a585658434e4a6ab51aaa6c9d` | 689 | 15:43:14Z |
| `lane-base-unevaluable` | same with `--freeze $BASE --rev $BASE` | **2** | `ab4227f82c5ece64…` | — | 15:43:14Z |
| `lane-reversed-range` | same with `--freeze $FREEZE --rev $BASE` | **2** | `c1b9db741fabb5e7…` | — | 15:43:14Z |

### What the lane runs say

- **Selftest: 7 cases, 0 failures.** `C2_SELFTEST: cases=7 failures=0`; the cases are
  `green` (0), `red-unregistered` (1), `red-wrong-path-rows` (1), `red-thin-exit-cell` (1),
  `red-unknown-rev` (2), `red-frozen-touched` (2), `red-scope-size` (1). The stdout is
  **byte-identical** (sha256 `aea7e363…`) to the committed control
  `.ufo/waves/round-45/controls/c2-selftest.txt` (501 bytes) — an independent re-execution,
  not a copy.
- **Do-nothing control at the freeze: exit 1**, `registered []`,
  `unregistered` = the six scope paths, `thin []`, `registry_rows 39`, `met_target false`.
  My `--json-out` file is **byte-identical** to the committed
  `.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json` (953 bytes, sha256 `f61c6b99…`):
  `diff` printed no difference. The claims' "measurable before" is reproduced exactly.
- **Graded tip: exit 0**, `registered` = all six, `thin []`, `scope_size 6`,
  `registry_rows 45`, `failing []`, `frozen_path_changed []`.
- **Base arm: exit 2** `{"reason": "scope file absent at rev", "verdict": "could_not_evaluate"}`
  — matches `.ufo/waves/round-45/controls/ctl-c2-0-base-unevaluable.json` (102 bytes).
  The base is not a measurable before, as the claims state.
- **Reversed range: exit 2** `freeze is not an ancestor of rev`.

## Row-set delta (why 45 and not 44 or 46)

Table rows whose first cell carries a backticked `tools/*.py|.sh`:

| revision | rows | note |
|---|---|---|
| freeze `f762b727` | 39 | zero registry rows for the scope |
| `HEAD` `faa875bc` | 45 | `+6` |
| set difference `HEAD − freeze` | 6 | exactly the six scope paths; no other tool row was added |

That is the causal trace for the calibration claim: the land added the six rows the counter
needs and nothing else it counts. The six first matches are `SKILL.md:1636-1641`, each with
7 cells; the registry table header at `:1634-1635` has 7 cells.

## Independent reimplementation (not the counter)

A separate checker (own parser; `re.fullmatch` on the first cell, so cell equality, not
substring search) reproduced the verdict at both revisions:

- `HEAD`: `scope_size 6`, `missing []`, `thin []`, all six `ncols == 7`.
- freeze: `scope_size 6`, `missing` = 6 (i.e. zero registered).

It also confirmed the landed row at `:1641` is the only table row naming
`tools/round-45/c2-counter.py` (the other text occurrence is prose at `:1627`), and that
`tools/round-45/frozen-path-preflight.py` has exactly one table row (`:1639`); `:1640`
merely cites it in the c1 row's pinned-value cell.

## Attack matrix (isolated fixtures)

Each fixture is a fresh `mktemp -d -p $S` repo, `git -C "$D" init -q`, toplevel verified
equal to `$D` before the first commit, throwaway identity set inside that fixture only.

| id | attack | expect | got | stdout sha256 |
|---|---|---|---|---|
| `fx-green` | six correct rows | 0 | **0** | `f683a40bdca716cc…` |
| `A1-any-table-row` | six rows in a generic 3-column `## Decision log` table, `0/1/2` in column 3, **no registry section at all** | 0 | **0** | `ee3174430dfad9cc…` |
| `A2-four-cell-row` | 7-column header, 4-cell body rows (no pinned/write-scope/owner) | 0 | **0** | `c37eea06b0072d96…` |
| `A3a-thin-row-first` | thin duplicate row **before** a good one | 1 | **1** (`thin: ['tools/round-45/x.py']`) | `9e985e51e0e50ce9…` |
| `A3b-thin-row-masked` | thin duplicate row **after** a good one | 0 | **0** (`thin []`) | `b9b6beb749624a9b…` |
| `A4-ghost-tool-path` | rows name files that do not exist at `--rev` | 0 | **0** | `9fd821ccbad7be5c…` |
| `A5-lexical-012` | exit cell `pinned at revisions `0`, `1`, `2`; verdict not stated` | 0 | **0** | `0405bd90ba2aa078…` |
| `A9-cell-not-exact` | first cell `` `path` (frozen instrument) `` | 0 | **0** | `c17a208f6afdd894…` |
| `A10-path-in-col2` | path quoted in column 2, other text in column 1 | 1 | **1** (`unregistered: ['z.py']`) | `68da336a9cc849a6…` |
| `A11-digit-adjacency` | cell `exit `0` ok, `1` fail, 1024-byte cap` | 1 | **1** (thin) | `c2a187f19ab2d87e…` |
| `A6-frozen-scope-touched` | post-freeze commit edits `tools/round-45/registry-scope.json` | 2 | **2** (`frozen_path_changed: [tools/round-45/registry-scope.json]`) | `0b283d791222802a…` |

All 16 recorded runs matched their expectation; no mismatch.

### Reading of the attacks

- **A1 is the sharpest finding.** The counter never locates a registry heading or validates
  the table header. Any markdown table row in `SKILL.md` whose first cell quotes the path and
  whose third cell names `0`, `1`, `2` is a "registry row". Claims R45-C2 says "some
  `SKILL.md` registry row's first cell is **exactly** that path"; the implementation is
  weaker than the word *registry*.
- **A2** means the 7-column landing standard is a drafting rule, not a counted clause: a row
  with no pinned-value, write-scope or owner cell still scores green.
- **A3a/A3b** are two-directional: `by_tool.setdefault(path)` keeps the first matching row,
  so a redundant thin row after a good one is silent (masked), while a thin row before a good
  one fails the run even though a correct row exists. Neither case is in the selftest or the
  kill rule.
- **A4** confirms the disclosed limit (`SKILL.md` "Limit: `c2-counter.py` checks that a row
  names the path, not that the tool exists at `--rev`", routed R45-CL2). It is real, and it
  is the one gap a v2 could close cheaply with `git cat-file -e <rev>:<path>`.
- **A5/A9** are lexical: `exits_ok` accepts `0/1/2` anywhere in the cell, and cell equality is
  substring equality. **A11** shows digit adjacency is handled correctly (`1024` does not
  supply the `2`), so the lexical risk is prose-shaped, not numeric.
- **A10** is correct behaviour: a path quoted outside the first cell does not register.
- **A6** shows the frozen-path arm covers the *scope file itself*, not just the counter — a
  scope widened after the freeze is refused, which is the property the round needs.

## Separability (C1 vs C2)

`grep -c` over the frozen bytes: `Queue-drain` 0, `block22` 0, `rule_blocks` 0, `S140` 0,
`preflight` 0. `CLAIMS` (`:28`) is used only inside `FROZEN` (`:30`) as a git pathspec, plus
the selftest fixture (`:155`); the claims file's *content* is never parsed. C2 cannot be moved
by block 22, and C1 cannot be moved by a registry row.

## Scratch hygiene, limits, and what was not run

- `--selftest` creates `$TMPDIR/kaidoku-r45/` and removes its per-run workroot; the empty
  `kaidoku-r45` parent remains. Harmless, but it is a write the row does not spell out.
- The path regex admits only `.py`/`.sh` (`:31`); a scope entry in another language could
  never be registered. No current impact — all six frozen entries are `.py`/`.sh`.
- `scope_size` is `len(scope)`, so six entries with a duplicate and a missing path could
  reach 6 distinct tools while reporting 6. The frozen scope has 6 unique paths, all present.
- **Not run:** the counter was not exercised against a corrupted git object store, a
  read-only `--json-out` path, or a shallow clone missing the freeze. Those are unevaluable-path
  claims I did not measure and do not assert.
- No installs, no network, no package transactions. No `git add/commit/push` outside the
  throwaway fixtures; the lane tree was read-only for this seat.
