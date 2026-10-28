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
| M46-2 | `plan-froze-a-number-the-code-does-not-fix` — the plan names `forgeries_total == 9` and `== 7` as clause values, but the counts come from `MUTATIONS` in code, so deleting one mutation from the list would silently change the denominator the claim is judged on. | `plans/round-46-claims.md` R46-C1 clause 7 and R46-C2 clause 6 against `tools/round-46/attest.py` `MUTATIONS` and `registry.py` `MUTATIONS` | `none` in the instrument: the equality is checked, but nothing pins the mutation list itself to a digest | routed as R46-CL4: both counters should print `mutations_sha256` (a digest of the mutation names and their order) and the closure should compare it with the value the claims file names |

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S142 | https://git-scm.com/docs/git-log | 2026-10-28T16:49Z, HTTP 200, 375,834 bytes, page sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`; anchor `--diff-merges=<format>`, value `first-parent` | "Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits." (21 words) |

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
- **R46-CL5.** The registry row's `purpose` cell is not validated at all: a row can satisfy
  the census path with a false description. Only presence, exact cell 0 and the verdict map
  are checked.
