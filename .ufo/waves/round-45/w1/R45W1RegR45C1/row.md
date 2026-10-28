# R45-C1 — registry row for `tools/round-45/c1-counter.py`

Seat `R45W1RegR45C1`, round 45 wave 1, leaf. Freeze
`f762b7273e3f6ca3c710bb37d5de92a4a4417aec` — re-derived independently twice,
`git log --format=%H -1 -- plans/round-45-claims.md` and
`git log --format=%H -1 -- tools/round-45/`, both printed that commit (stdout sha256
`97150e76f53a53146147fe3d2c3d6318d1e08cd3e8d23cadde679512bf85b67f`, exit 0).

Every claim below was measured by executing the **frozen** bytes
(`sha256 2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`, 14319 bytes,
366 lines, blob `4ce400b2`, mode 100755), never a worktree edit. Receipts, with exit
codes and stdout sha256: `receipt.md` in this directory.

## The row (exact, 7 cells)

This is the row **already landed at `SKILL.md:1640`** under
`### Round-44/45 instrument registry` (post-freeze commit `abfeda50`, present unchanged at
`HEAD`). It was verified cell by cell against measured behaviour; no cell was found wrong,
so landing it again is a no-op.

```markdown
| `tools/round-45/c1-counter.py` | gate — R45-C1 depth: rule block 22 in `## Queue-drain craft`, its citations, and the interpreter's own selftest | `0` met; `1` not met (each false clause named in `failing`); `2` could-not-evaluate, including `frozen_path_changed` | `python3 -I -B tools/round-45/c1-counter.py --selftest` — 9 cases, green at the freeze | `SKILL.md` craft section, `tools/round-45/frozen-path-preflight.py`, `plans/round-45-claims.md` | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | kaidoku |
```

sha256 of the line plus its newline: `2c30eb70ea075dcf8c4c6aa02c032c7ab3314030b339a5221d45a6c354657731`
(529 bytes with newline; `b5cf3726b0e8322c2ca78d57055a3a633e554ffcb4f6ef263075b911a6fbe965` without).

## Delta row — optional, only if the L1 wants the exit-2 set named

The landed cell 3 says "including `frozen_path_changed`"; measurement shows the arm misses
merge commits (see "What this row does not claim"), so the landed wording overstates it.
The house style already discloses such limits in the row (cf. the round-38 row: "an unknown
or unresolvable revision is **not** detected"). This variant names all five exit-2 triggers
and the merge qualification, in the same 7 cells. **Replace `SKILL.md:1640`, do not append a
second row** — the c2 counter keeps the first matching row per path, so a duplicate is noise.

```markdown
| `tools/round-45/c1-counter.py` | gate — R45-C1 depth: `SKILL.md` `## Queue-drain craft` rule block 22 (marker `<!-- freeze-integrity-table v1 -->`): 22 blocks, header cells trigger/arm/exit/receipt, at least 8 data rows with every exit cell in `{0,1,2}`, at least 4 `path:line` citations resolving at `--rev`, `S140` and the interpreter both cited, and the interpreter's `--selftest` run from the `--rev` bytes (cases at least 11, failures 0) | `0` met (`met_target true`, `failing []`); `1` not met, each false clause named in `failing`; `2` could-not-evaluate: `frozen_path_changed` (a non-merge commit in FREEZE..REV touching `plans/round-45-claims.md` or `tools/round-45/`), unknown `--freeze` or `--rev`, freeze not an ancestor of rev, `SKILL.md` absent at rev, usage | `python3 -I -B tools/round-45/c1-counter.py --selftest` — 9 cases measured at the freeze (`C1_SELFTEST: cases=9 failures=0`); the embedded interpreter selftest is 11 cases | `plans/round-45-claims.md` (R45-C1), `tools/round-45/frozen-path-preflight.py` (run from `--rev` bytes), `SKILL.md` `## Queue-drain craft` block 22 | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` (`kaidoku-r45/c1-*`, removed on exit) | kaidoku |
```

sha256 of the line plus its newline: `dc4cf9fdd1b5aa256964f63504f52bda7293121e7805b8a33e0144817a65a08a`
(1213 bytes with newline). Both variants are 7 cells.

## Cell-by-cell grounding

| # | column | content | measurement that backs it |
|---|---|---|---|
| 0 | tool | `` `tools/round-45/c1-counter.py` `` | First cell is exactly that backticked path; the counter's own `PREFLIGHT`/`CLAIMS` constants and its file identity are as tabled here. c2-counter's scope file lists this path, and its first-cell equality rule is satisfied by this row. |
| 1 | gate or probe | R45-C1 depth gate over `SKILL.md` craft block 22 plus the interpreter selftest | `evaluate()` computes `rule_blocks`, `block22_present`, `block22_rows`, header cells, exit cells, `block22_refs`, `block22_unresolved_citations`, `S140`/interpreter citations, and runs `frozen-path-preflight.py --selftest` from `--rev` bytes. A verdict, not a probe. |
| 2 | verdict map | `0` met; `1` not met; `2` could-not-evaluate including `frozen_path_changed` | Measured: exit 0 at `1f4b27f8` and at `HEAD` (`met_target true`, `failing []`); exit 1 at the freeze and at the base with five named clauses in `failing`; exit 2 on a frozen-path touch (direct, restored, bulk, claims-file-only), unknown `--rev`, non-ancestor freeze, and no-argument usage. A `2` receipt carries `verdict: could_not_evaluate` and **no** `met_target` key. |
| 3 | self-test command | `python3 -I -B tools/round-45/c1-counter.py --selftest` — **9 cases**, green at the freeze | Frozen bytes: exit 0, final line `C1_SELFTEST: cases=9 failures=0`, stdout sha256 `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d`. Cases: `green`, `red-relabelled-21-block`, `red-thin-table`, `red-bad-citation`, `red-no-s140`, `red-interpreter-fails`, `red-bad-exit-cell`, `red-frozen-touched-is-exit-2`, `red-unknown-rev`. The embedded interpreter adds its own **11 cases** (`PREFLIGHT_SELFTEST: cases=11 failures=0`, stdout sha256 `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c`), reported as `preflight_selftest {cases: 11, failures: 0}` in every green receipt. |
| 4 | pinned-value path | `plans/round-45-claims.md`, `tools/round-45/frozen-path-preflight.py`, `SKILL.md` `## Queue-drain craft` block 22 | The claims file is one of the two frozen pathspecs and the document the counter's predicate encodes (blob `f93df4c3`, 9461 bytes, 175 lines). The interpreter is read with `git show <rev>:<path>` and executed from a private scratch copy. The craft section is parsed from `SKILL.md` at `--rev` by the literal split token `"## Queue-drain craft "`. |
| 5 | write scope | `--json-out`; scratch under `$HYAKU_SCRATCH` or `$TMPDIR` | The only file writes are `--json-out` and `mkdtemp(dir=$HYAKU_SCRATCH or $TMPDIR/kaidoku-r45, prefix="c1-")`, removed with `shutil.rmtree` before exit; measured: no `c1-*` directory survives a run. Everything else is `git show`/`git log`/`git rev-parse` reads (plus `git cat-file -e`/`git ls-tree` style existence probes inside `unresolved_refs`). |
| 6 | owner | kaidoku | Lane owns the instrument. |

## Pinned inputs, with identity at the freeze

| input | identity at `f762b727` | how the counter uses it |
|---|---|---|
| `plans/round-45-claims.md` | blob `f93df4c3bd4069a0cd576d9649f1157609b6a5d5`, sha256 `56bacf3143e904ae1c9683c61f0d3f30900257c6fd90d38965d735c7c50b915e`, 9461 bytes, 175 lines | frozen pathspec only (`FROZEN`) — the file's prose is never parsed; a commit touching it in `FREEZE..REV` is exit 2 |
| `tools/round-45/frozen-path-preflight.py` | blob `b4239827`, sha256 `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`, 11987 bytes | read from `--rev`, written to scratch, run `--selftest`; `cases >= 11`, `failures == 0`, exit 0 — and its path string must appear in block 22 |
| `SKILL.md` `## Queue-drain craft` | not frozen (graded surface), read at `--rev` | split on the literal `"## Queue-drain craft "`, then each `^- \*\*` is a rule block; block 22 is the one carrying `<!-- freeze-integrity-table v1 -->` |
| citation targets inside block 22 | `corpus/lessons/round-44.md:18-19,63-69,88-92`, `corpus/lessons/round-44-verifier-spotcheck.md:89-92`, `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, `corpus/lessons/round-45.md:12-17`, `plans/round-45-claims.md:132-147` | 7 refs, all resolving at `1f4b27f8` and at `HEAD`; `block22_unresolved_citations == []` |

## What this row does not claim

The row describes the instrument; it does not certify the predicate text. Two measured
instrument limits must be read with it (details and commands in `receipt.md`):

1. **The frozen-path arm fails open on merge commits.** `frozen_path_changed()` is
   `git log --name-only --format=`, without `-m`/`--diff-merges`. On a merge commit whose
   *resolution* edits a frozen path, that log prints the commit header and **no paths**, so
   the counter does not exit 2 — it proceeds and can print `met_target: true`. Measured on
   a fixture: counter exit **0**, `frozen_path_changed []`, `met_target true`, while the
   frozen interpreter's blob differed (`4ce400b2…` → `d98d51e3…`) and
   `frozen-path-preflight.py` on the same range exited **1** with
   `touched: [{path: tools/round-45/c1-counter.py, status: M}]`.
   The round's real history has **0** merge commits (`git rev-list --merges f762b727..HEAD`
   empty) and both gates score it clean, so no measured score is affected.
2. **Crash is not `2`.** If the craft heading loses its trailing space
   (`## Queue-drain craft(`), `craft_blocks` raises `IndexError`; the process exits **1**
   with empty stdout — the code for "not met". A predicate that cannot be evaluated is
   reported as failed, not as could-not-evaluate.
