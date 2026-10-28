# Round 46 — the measure becomes a discriminator: the freeze-integrity matrix and a census-bound instrument registry

Lane `kaidoku`, round 46, attempt 1. Base `5382acc85f9d8617fe242fc116819b8055dfc4c7`;
freeze `31820472784284727546808acc31b3ea1e73919b` (`plans/round-46-claims.md` and
`tools/round-46/`); instruments `tools/round-46/{gate,attest,registry,census}.py`.

Round 45 landed two genuine artefacts and reported `met (instrument non-discriminating)`:
a 44-line forged C1 artefact and a six-fenced-row C2 artefact each scored
`met_target: true` (`corpus/lessons/round-45.md` R45-CL13, R45-CL14). Round 46 replaces the
measure with one that scores **its own forgeries** red: nine mutations of rule block 23 for
C1, seven mutations of the registry section for C2, each built from the landed bytes, with
the round-45 clause set ported alongside so the same battery is scored both ways.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M46-1 | `control-named-a-measurement-that-cannot-exist-at-the-freeze` — the frozen claims plan names `controls/ctl-c1-1-v1-profile.json` as the v1-profile control "at the freeze", but the battery builds its forgeries by mutating the LANDED block 23, so that receipt cannot exist before the landing. The plan describes a measurement whose subject does not yet exist. | `plans/round-46-claims.md` (the R46-C1 "Before" bullet) against `tools/round-46/attest.py` `run_battery` (which returns `cannot build a battery: marker blocks 0` at the freeze) | the satisfiability preflight asked "can the instrument compute this value", but never "at which revision does this value exist" | the v1-profile gap is produced post-landing as `.ufo/waves/round-46/l1/scores/c1-v1-gap.json`, the freeze keeps only the two do-nothing controls plus the two v1-fidelity receipts, and the report states the corrections; the frozen wording is not edited (the file is a frozen path) |
| M46-3 | `freeze-moved-four-times` — the freeze commit `3182047` did not contain the bytes that could be scored: the guard returned an int where the caller unpacked a tuple, `run_battery` referenced a renamed regex and could only fail, and the v1 registry profile applied the v2 strict checks to historical rows. Three further commits (`50862e4a`, `65678df0`, `04252247`) were needed before a counter produced a verdict, so the freeze is a series and the claims plan's "the commit that first contains this file and tools/round-46/" is false for the declared freeze. | `plans/round-46-claims.md` (freeze definition) against the four commits; each defect has its own receipt: the do-nothing control exiting 2 `battery: cannot build a battery`, `NameError: name 'REF' is not defined`, and `thin verdict-map cells: 6` in `l1/scores/` | `none` in the instrument — the selftest ran with `with_battery=False`, so `run_battery` was never executed by any case, and no gate compared the freeze commit with the bytes it was supposed to freeze | the selftest now carries a `green-with-battery` case (16 cases), and the criterion is `QUALITY.md` row 77: an instrument is frozen only when the path its claim scores has been EXECUTED once, not merely imported |
| M46-4 | `proxy-harm-recurrence` — block 23 landed citing lessons and plans only, so command A read `citation_resolved_rules 22/23`, `depth_score 9.57`: a depth claim that lowers the depth proxy. This is the round-45 A1 defect exactly, one round later. | `l1/scores/c1-at-A2.json` (22/23) against `c1-at-A3.json` (23/23) after A3 `7bf33e31` cites `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66` | the round-45 LOG recorded the repair as an amendment but no `QUALITY.md` row carried it, so nothing stood between the lane and the repeat | `QUALITY.md` row 77 now requires a new craft block to cite a knowledge entry; the landing is re-measured with command A before the claim is called met |
| M46-2 | `plan-froze-a-number-the-code-does-not-fix` — the plan names `forgeries_total == 9` and `== 7` as clause values, but the counts come from `MUTATIONS` in code, so deleting one mutation from the list would silently change the denominator the claim is judged on. | `plans/round-46-claims.md` R46-C1 clause 7 and R46-C2 clause 6 against `tools/round-46/attest.py` `MUTATIONS` and `registry.py` `MUTATIONS` | `none` in the instrument: the equality is checked, but nothing pins the mutation list itself to a digest | routed as R46-CL4: both counters should print `mutations_sha256` (a digest of the mutation names and their order) and the closure should compare it with the value the claims file names |

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S142 | https://git-scm.com/docs/git-log | 2026-10-28T16:49Z, HTTP 200, 375,834 bytes, page sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`; anchor `--diff-merges=<format>`, value `first-parent` | "Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits." (19 words) |

S142 is cited by the round's R46-C1 landing: `tools/round-46/gate.py`'s history arm passes
`--diff-merges=first-parent` so a merge's own resolution edit is visible, which is the arm
`R45-CL6` found missing. The row enters as `mined`, tier A, recheck `on-release`,
`used-by corpus/lessons/round-46.md`.

S140 and S141 (round-45 rows) stay `mined` and unchanged; block 22 still cites S140 and the
round-46 counters cite S141's `-z` statement only indirectly (the history arm uses
`--name-status -z`).

### Admission and rejection

- **Admit** S142 as a registry row (`docs`, tier A): opened this round and cited by R46-C1's
  instrument.
- **Assimilation: none.** No `merge/kaidoku/` theme and no `considerthese/` proposal applies
  to an instrument-discrimination round (`considerthese/` is absent in this lane); the
  round-44 quarantine refusals stand and nothing is adopted.
- **Census before → after:** `corpus/SOURCES.md` rows 141 → 142
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`). Round-start census and
  round-end census outputs are recorded in the fleet report.

## Routed defects (for round 47)

- **R46-CL1.** The counters' freeze arm reads `git log -m --diff-merges=first-parent`, which
  sees a merge's first-parent diff. It still cannot see a tamper+restore folded away by
  `git merge --squash` (R45-CL19): no surviving history names it. The blob arm is the only
  defence and after a restore it is clean. Stated in the table; not closed.
- **R46-CL2.** `attest.py`'s arm-vocabulary check is a substring test over a lowercased cell,
  so `blobberish` satisfies `blob`. The plan says "names a token", the code allows a
  substring; the wording and the code should agree in round 47.
- **R46-CL3.** The routed-id check requires every id to appear in *some* row, not exactly
  once, and `R45-CL13`/`R45-CL14` cover six defects each while the table carries one row per
  group. A row may claim a group it does not really address.
- **R46-CL4.** The mutation list is not pinned: `forgeries_total` is checked but the list
  itself has no digest, so a deletion changes the denominator without failing a clause.
- **R46-CL6.** `gate.history_touched` passes `-m --diff-merges=first-parent`, and the arm is
  **order-sensitive**: `git log --diff-merges=first-parent -m` prints a merge twice (one entry
  per parent) because the later flag wins, which restores the very blindness `R45-CL6` was
  about. The order is correct today and nothing in the code enforces it; one argument reorder
  silently undoes the arm. Wave-1 seat `R46W1ScribeSource` measured this on a deterministic
  merge fixture. Round 47: assert the flag order in a selftest case.
- **R46-CL7 (HIGH; wave-1 `R46W1RegL`).** The C2 clause that was supposed to close
  R45-CL14 (d) binds the DIGITS 0/1/2, not their meanings: a row whose `purpose`, `self-test`,
  `pinned-value` and `write-scope` cells are empty and whose verdict map reads
  `0=banana; 1=nope; 2=whatever` scores `met_target: true`, exit 0, with the seven-forgery battery
  still green — reproduced by the L1 on a fixture repo at `47b5e265`. Sixteen forgery classes are
  caught; a contentless row is not one of them. Round 47: require the verdict cell to match the
  tool's own exit constants, or make the purpose cell a value the counter derives.
- **R46-CL8 (LOW; wave-1 `R46W1RegL`).** The claims file records
  `registry.py --selftest prints cases=11`; the runnable form needs `--root/--freeze/--rev` (a bare
  `--selftest` exits 2 from argparse) and prints `cases=12`. The count in the plan is stale by one
  and the invocation in the plan is not runnable as written.
- **R46-CL5.** The registry row's `purpose` cell is not validated at all: a row can satisfy
  the census path with a false description. Only presence, exact cell 0 and the verdict map
  are checked.
