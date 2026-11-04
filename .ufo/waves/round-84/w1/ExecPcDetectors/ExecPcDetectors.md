# ExecPcDetectors — round-84 w1 — printed-command detector cases

Seat: executor, lane `kaidoku-shokunin`, wave `r84-w1`, L1 `KaidokuR84`.
Scope: extend the selftest of `tools/round-82/printed-command.py` so the seven
declining sourced/pin/static mutants die at their declared cases, without
editing the frozen file. Claim served: R84-C2 (depth).

## Deliverables (all under `.ufo/waves/round-84/w1/ExecPcDetectors/`)

| file | what |
|---|---|
| `printed-command.py` | candidate — full replacement copy of the frozen tool (frozen sha256 `88b1dff23855…`, candidate sha256 `91a01190bed4…`) |
| `printed-command-candidate.patch` | unified patch frozen→candidate, exactly 2 hunks (159 lines) |
| `mutants-seven.json` | derived 7-row sub-table: the seven recorded round-82 survivor rows of the frozen table, verbatim; frozen table untouched (its sha256 `dbb6d4c93df6…` is recorded inside) |
| `pristine-selftest.json` | pristine candidate selftest receipt |
| `closure-seven.json` | mutation-closure receipt, 7-row derived table vs candidate |
| `closure-full.json` | mutation-closure receipt, full frozen 13-row table vs candidate + frozen `conjunction-gate.py` + frozen `source-bind.py` in a scratch repo |

Report trailer copy: this file is written at
`.ufo/waves/round-84/w1/ExecPcDetectors.md` per the seat item, with a
byte-identical copy at `.ufo/waves/round-84/w1/ExecPcDetectors/ExecPcDetectors.md`.

## The seven declared cases (exact names, as the frozen table binds them)

| declared case | mutant id | production path driven | asserted exactly |
|---|---|---|---|
| `runtime-pin-mismatch-refused` | `pin-call` | `run_block` (the execution path where `pin_matches` is called) on a fixture git repo whose claims container pins `member.py` to a decoy digest; **not** a direct `pin_matches` call | refusal `REFUSED: SCRIPT_PIN_MISMATCH`, `executed` false |
| `static-defect-no-execution` | `static-refusal` | `run_block` with a command carrying `VARIABLE_UNBOUND: $HOLD` and a correctly pinned script; non-execution proven by a canary (`canary.txt` the committed script creates on execution) absent after the call | static defect `VARIABLE_UNBOUND`, `executed` false, canary absent |
| `sourced-row-rejected-status` | `source-mined` | production `sourced_arm` on a fixture repo with the row `queued` (date right) | defects == `["SOURCED_ROW_UNMET"]` |
| `sourced-row-wrong-date` | `source-date` | production `sourced_arm`, row `mined` with date `2025-12-31` | defects == `["SOURCED_ROW_UNMET"]` |
| `sourced-row-at-base` | `source-base` | production `sourced_arm`, row present at the fixture's base revision (`base_rev` = commit 1) | defects == `["SOURCED_ROW_AT_BASE"]` |
| `sourced-plan-missing` | `source-plan` | production `sourced_arm`, plan carries no `S[0-9]+` token | defects == `["SOURCED_ROW_NOT_IN_PLAN"]` |
| `sourced-entry-uncited` | `source-entry` | production `sourced_arm`, entry's `source:` line cites `S260` only | defects == `["SOURCED_ENTRY_UNCITED"]` |

The five sourced fixtures pass their own values (`sid="S777"`,
`base_rev=<commit-1 hash>`), so the parameterization is genuinely exercised
with non-production values; every case is `guarded` so a fixture failure fails
only its own case and the selftest always completes with a parseable summary.

## Parameterization diff (the only production change)

```diff
-def sourced_arm(root: str, rev: str) -> dict:
+def sourced_arm(root: str, rev: str, sid: str = SOURCED_ROW,
+                base_rev: str = BASE) -> dict:
+    # The row id and base revision are parameters with the production values
+    # as keyword defaults; they are bound to local names of the frozen
+    # spelling so the body below stays byte-identical for the round-84
+    # mutant anchors, while a fixture repo can pass its own values.
+    SOURCED_ROW, BASE = sid, base_rev
     row = sources_row(read_text(root, rev, SOURCES), SOURCED_ROW)
```

`sid` and `base_rev` default to the production constants (behavior of the
existing `battery` callsite `sourced_arm(root, rev)` is unchanged), and the
local rebind keeps the three frozen anchor lines
(`base_absent = sources_row(base_text, SOURCED_ROW) is None`,
`plan_names = SOURCED_ROW in re.findall(…)`,
`entry_ok = entry_cites(entry_text, SOURCED_ROW)`) byte-identical, so all
seven anchor strings of the frozen mutant table still occur exactly once in
the candidate — proven by the closure runs (every mutant scored, none
`anchor-not-exactly-once`). The second hunk is the selftest extension only.

## Measured results

Pristine candidate selftest: `SELFTEST cases=22 failures=0`, exit 0
(15 pre-existing cases unchanged + 7 new). Receipt: `pristine-selftest.json`.

Closure, derived 7-row table against the candidate at scratch-repo `HEAD`
(`python3 -I -B tools/round-84/mutation-closure.py --root <scratch-repo> --rev
HEAD --mutants mutants-seven.json`):
`killed 7, mutants 7, survivors [], inconclusive [], pristine_failed [], ok
true`, exit 0. Per-mutant `failures` equals exactly its declared case
(`closure-seven.json`), `restored_equal` true ×7.

Closure, full frozen 13-row table against the same scratch repo (candidate
`printed-command.py` + frozen `conjunction-gate.py` + frozen `source-bind.py`):
`killed 11, survivors [sb-header-position, sb-duplicate-last], inconclusive
[], pristine_failed []` — all three targets pristine green (21 / 22 cases /
plain-line shape), conjunction's four BASE kills reproduce (`floor`,
`failure`, `binder`, `membership`), and the two survivors are the round-83
source-bind declared cases `late-single-header` / `duplicate-target-second`,
which are sibling seat ExecSbDetectors' scope, not this seat's. Receipt:
`closure-full.json`.

Frozen integrity after my work: all eight frozen files
(`printed-command.py`, `conjunction-gate.py`, `source-bind.py`,
`mutation-closure.py`, `freeze-precheck.py`, `nested-sqfs.py`,
`mutants.json`, `claims.json`) hash-equal to their `git HEAD` blobs
(verified read-only); no production, fleet or sibling-lane writes; no git/jj
mutations outside scratch fixtures (each fixture asserts
`git rev-parse --show-toplevel` equals its own realpath before committing).

## Scratch hygiene

Scratch was `/fast/scratch/hyaku/kaidoku-r84/ExecPcDetectors/` only
(realpath == abspath, no symlink components); `/tmp` never used; all receipts
copied into the wave dir; scratch removed before this yield. The candidate
selftest's fixture repos live under `TMPDIR` and clean themselves up.

## Tooling record (operator authorization 2026-10-19)

No installs or upgrades. Used preexisting host tools only: python 3.14.8,
git 2.56.0, GNU diff. `RULES.md` consulted; pacman pause respected (nothing
installed via any channel).

## Risks / notes for L1

1. The full-table C2 counting command at the measured revision needs both
   detector seats landed: my candidate closes the seven printed-command
   survivors; `sb-header-position` / `sb-duplicate-last` stay survivors until
   ExecSbDetectors' source-bind cases land.
2. `mutants-seven.json` is a disclosed derived subset for seat-scoped
   demonstration; the official C2 run must use the frozen
   `.ufo/waves/round-84/mutants.json` (used for `closure-full.json`).
3. The parameterization relies on a local rebind of the module-constant names
   inside `sourced_arm` — intentional and documented in-code; it is the
   minimal-diff way to satisfy both the parameterization requirement and the
   frozen anchors. Flagging for reviewer eyes.
4. In the full-table run the `membership` mutant also fails
   `unpinned-path-refused` besides its declared `bare-name-refused` —
   pre-existing BASE behavior (both BASE cases hit the disabled pins check),
   harmless: scoring binds each kill to the declared case only.

Blockers: none.
