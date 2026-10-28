# ExecMeasure — round-48 counter measurement harness

Seat task: before/after invocations for both counters with captured exit code,
`met_target`, `failing`, `meaning_rows_failed`, `floor`, `quotes_bad`, `battery` —
one JSON per invocation plus a re-runnable `measure.sh`.

## Declared-freeze resolution (important)

The prompt's declared freeze `dc73587a…` (A1) is **stale**. Two more amendments
landed during the wave — A3 `f3a7afc4` (census object-vs-list compare) and
A4 `0f06251b` (exit-0 classifier accepted a negated meaning; row parser skipped
an indented row). The claims file is the rule: each amendment's text re-declares
"the freeze is the commit that carries this paragraph", and
`git log --format=%H -1 -- plans/round-48-claims.md` = **`0f06251bf6a3a6964c715f67243d4df12e854258`**.
All "after" measurements below are at that revision. Tip is now `663f30ee…`
("inherited receipt > 1 MiB" + "inherited seat evidence") — no landing yet
(`verdict-meaning-table` absent from `SKILL.md`, no `## Round 48` in `SCORECARD.md`
at 0f06251b or tip), so the declared freeze IS the current "after".

A `--freeze dc73587…` invocation at rev 0f06251b correctly exits 2
`frozen_path_changed` — receipt-proven that any seat using the prompt's literal
gets a could-not-evaluate, and that the freeze-integrity arm itself works
(see `c1-stalefreeze-tip`, `c2-stalefreeze-tip`, `*-stalefreeze-a2`).

## Harness (re-runnable by L1)

`measure.sh` in this directory. Usage:

    ./measure.sh                # grades the declared freeze (current "after")
    ./measure.sh <LANDING_REV>  # after L1 lands: pass the landing revision
    ./measure.sh <REV> <FREEZE> # explicit

Per invocation it writes `receipts/raw/<name>.counter.json` (the counter's own
receipt via `--json-out`), `receipts/raw/<name>.stdout`, and a wrapped
`receipts/<name>.json` carrying argv, exit code, UTC time, stdout sha256, and the
graded fields. `manifest.json` aggregates all 16.

Notes learned the hard way: `--json-out` refuses paths outside the lane root
(exit 2 `"--json-out outside the lane root"`) — receipts must live under
`.ufo/waves/`, not scratch. `PYTHONDONTWRITEBYTECODE=1` keeps the runs
byte-clean in the worktree; `git status` on the graded surfaces stayed clean
after all runs (`touched 0`, `restored []`, `frozen_path_changed []` in the
receipts).

## Result matrix (rev = declared freeze 0f06251b unless noted)

| invocation | exit | reason / met | key fields |
|---|---|---|---|
| c1-before-base (freeze=DECL, rev=61b87d74) | 2 | `freeze is not an ancestor of rev` | pre-freeze rev is could-not-evaluate, by design |
| c1-before-base-freezebase (freeze=rev=base) | 2 | `claims file absent at rev` | both "before" shapes are 2 — never count toward target |
| c1-after-0f06251b | 1 | met=false | `failing: marker_occurrences 0 != 1, marker_block_count 0 != 1`; battery skipped (structural clause fails first) |
| c1-after-0f06251b-v2 | 1 | met=false | `marker_block_count 0` |
| c1-stalefreeze-tip (freeze=A1) | 2 | `frozen_path_changed` | A3+A4 touched frozen bytes → stale literal is caught |
| c1-stalefreeze-a2 (freeze=A2) | 2 | `frozen_path_changed` | same for A3/A4 relative to A2 |
| c1-control-a1-self (freeze=rev=A1) | 1 | met=false | matches committed `ctl-c1-0-do-nothing.json` |
| c1-selftest | 0 | — | A4's two new cases (`red-opposite-polarity`, `red-hidden-row`) included |
| c2-before-base (+freezebase) | 2 | same as C1 | — |
| c2-after-0f06251b | 1 | met=false | `failing` 3: round-47 has no seat atom nor seats correction; `## Record corrections — round 48` absent; `exempted 2` quoted in round-47 not backed by its cited receipts (`c1-at-A7`/`c2-at-A7` say 1). `floor` shows round-46 complete (seat/path/rev/claims ok) vs round-47 missing seats |
| **c2-after-0f06251b-v2** | **0** | **met=TRUE on the un-landed card** | the R47-CL10 hole, receipt-proven: v2 = oracle-only, so an un-landed card scores green |
| c2-stalefreeze-tip / -a2 | 2 | `frozen_path_changed` | — |
| c2-control-a1-self | 1 | met=false | matches committed `ctl-c2-0-do-nothing.json` |
| c2-selftest | 0 | — | — |

`battery` is `{"skipped": ...}` on every v3 invocation — by design it only runs
when all structural clauses pass, which requires a landing. `meaning_rows_failed`
is likewise unreached pre-landing (registry clause runs after the block check).
**L1: re-run `./measure.sh <landing_rev>` post-landing and check
`battery.forgeries_total 4/5, v2_green 4/5, v3_green 0, genuine_green 1, crash 0`
plus `meaning_rows_failed == 0`.**

## Verification vs falsification observations

- The counters genuinely grade committed bytes (`git show`) and keep the
  worktree clean — no observed mutation to graded surfaces across 16 runs.
- Freeze-integrity arm works both directions: wrong freeze → 2, claims absent →
  2, non-ancestor → 2.
- The "before" revision cannot produce a verdict at all (exit 2 in both
  shapes) — do-nothing controls live at the freeze revision instead
  (`control-a1-self` receipts match the committed `ctl-*-0-do-nothing.json`).
- Known instrument caveat (R47-CL1, out of scope): the counters execute their
  own code from the worktree while grading committed bytes — `interpreter_sha256`
  binds the rev's bytes into the block but nothing verifies the running
  interpreter is those bytes. A tampered worktree `meanings.py` would run
  unexamined; receipts show the frozen-path dirty check does at least exit 2
  if the frozen files themselves are dirty in the worktree.

## Install/tool record

None — no installs (python3, git, jq, sha256sum already present). Scratch:
`/fast/scratch/hyaku/kaidoku-r48/ExecMeasure` (removed after receipts copied).
