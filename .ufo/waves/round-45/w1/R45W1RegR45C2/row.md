# R45-C2 — registry row for `tools/round-45/c2-counter.py`

Seat `R45W1RegR45C2`, round 45 wave 1. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (`git log --format=%H -1 -- plans/round-45-claims.md`
re-derives it). Frozen bytes read from the freeze, never from the worktree.

## Row (exact, 7 cells)

```markdown
| `tools/round-45/c2-counter.py` | gate — R45-C2 calibration: every scope instrument has a registry row with a real exit map | `0` met; `1` not met (`unregistered`, `thin` or `scope_size`); `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-45/c2-counter.py --selftest` — 7 cases, green at the freeze | `tools/round-45/registry-scope.json` and the `SKILL.md` registry rows | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |
```

sha256 of the row plus its newline: `4332538d808fb29aaf052d37d9ab5b5993e3c01430ee27e87b91fe2f471c56fd`
(483 bytes including its newline, 482 without).

This is the row landed in `SKILL.md:1641` under `### Round-44/45 instrument registry` (post-freeze
commit `e715263c`); the file at `HEAD` is byte-identical to it. Landing it again is a no-op —
the draft is retained so the L1 can diff against drift.

## Cell-by-cell grounding

| # | column | content | how it was verified |
|---|---|---|---|
| 0 | tool | `` `tools/round-45/c2-counter.py` `` | First cell is exactly that backticked path. `c2-counter.py`'s own `ROW_TOOL` (`:31`) matches it; an independent checker using `re.fullmatch` on the first cell returned the same six paths at `HEAD`, lines 1636–1641, all 7 columns. |
| 1 | gate or probe | R45-C2 calibration gate | Frozen docstring `:2-18` states the three clauses (`unregistered`, `thin`, `scope_size`) and that exit 1 is "not met". Not a probe: it returns a verdict. |
| 2 | verdict map | `0` met; `1` not met (`unregistered`, `thin` or `scope_size`); `2` could-not-evaluate, including `frozen_path_changed` | Read from `evaluate` `:70-132`: `reasons` (`:110-113`) is exactly those three strings, `return (0 if not reasons else 1)` (`:132`). Exit 2 paths: unknown freeze/rev, freeze not ancestor, `git log` failure, scope file absent/unreadable, `SKILL.md` absent, usage. All three digits are present, so `exits_ok(cell)` is true — confirmed by the counter scoring itself green at `HEAD`. |
| 3 | self-test command | `python3 -I -B tools/round-45/c2-counter.py --selftest` — 7 cases | Ran the frozen bytes: exit 0, `C2_SELFTEST: cases=7 failures=0`; cases are `green`, `red-unregistered`, `red-wrong-path-rows`, `red-thin-exit-cell`, `red-unknown-rev`, `red-frozen-touched`, `red-scope-size`. |
| 4 | pinned-value path | `tools/round-45/registry-scope.json` and the `SKILL.md` registry rows | The scope is enumerated from that file only (`json.loads(scope_body)["paths"]`, `:88`); `scope_size` is `len(scope)`, never a literal. The registry side is `SKILL.md` at `--rev` (`:91`). The claims file is a **pathspec only** (frozen-path arm), never parsed for scope. |
| 5 | write scope | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | `--json-out` writes the receipt; `--selftest` builds fixtures under `$HYAKU_SCRATCH`/`$TMPDIR` + `kaidoku-r45/`. No other write. |
| 6 | owner | kaidoku | Lane owns the instrument. |

## Inputs named by the row

- `tools/round-45/registry-scope.json` — blob `4855e97e`, sha256
  `6e2dda713a474dd6479a0af1430af9f38013d058a7cf9d2cc3fe293b9bd8dff9`. Six entries, six unique,
  all six present at both the freeze and `HEAD`, byte-identical at both revisions. Scope order:
  `tools/round-44/{c1-counter.py,c1-run.sh,c2-counter.py}`, `tools/round-45/{frozen-path-preflight.py,c1-counter.py,c2-counter.py}`.
- `SKILL.md` registry rows at `--rev` — `SKILL.md` is **not** frozen (claims `## Frozen paths`), so
  the row side is evaluated at the graded tip. At the freeze there are **0** such rows
  (`registry_rows 39`, all six scope paths unregistered); at `HEAD` there are **45**, and the
  set difference `HEAD − freeze` is exactly the six scope paths — the land added the six rows and
  nothing else the counter counts.
- `plans/round-45-claims.md` — appears in the row only through exit 2: it is one of the two
  frozen pathspecs (`FROZEN`, `:30`).

## Instrument identity

| property | value |
|---|---|
| freeze blob (git) | `7d83de6258cb624b1ebb0e18c326cf9fb5fd1aee` |
| sha256 of frozen bytes | `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` (9560 bytes) |
| sha256 at `HEAD` | same — unchanged through `HEAD` |
| commits touching `tools/round-45/` or the claims file in `FREEZE..HEAD` | none (`git log --name-only --format= …` → empty) |

## Scope note for the L1

The row registers one instrument; it does not claim the instrument is sound. The measured
weaknesses (any table row counts as a registry row, no 7-column enforcement, first-row-wins
duplicates, a cell that merely quotes the path) are in `receipt.md` § Attacks. None of them
changes the target value at `HEAD`; all of them are arguments for a v2 counter, not for
restating this row.
