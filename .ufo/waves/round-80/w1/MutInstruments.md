# MutInstruments — round 80 seat report

**Seat.** MutInstruments (mutation tester), round 80 wave 1.
**Milestone.** r80-w1: strict pointer binding, receipt provenance and guard-table binding frozen with base arms, attacked from four directions.
**Base.** `16dfa009bf143080dfcdfc5f9ec34bd359536d90`.
**Frozen at test time.** claims guard `84d68e90f8a1ea3a3a7f94a208695c21023c0472`
(`plans/round-80-claims.md`, three predicates, kill rules and controls);
strictness fixture set `40f99456aff65f5b8b1ee7098820b2086499ae0c62b372d575f5f09d34510feb`
(`.ufo/waves/round-80/l1/fixtures/strictness.json`, 4 red / 2 green).

**Question asked.** Does any conjunct of the round-80 instruments' own logic
survive a one-edit mutation with every `--selftest` case still green?

**Answer.** Yes — 15 survivors across 4 scored targets (47 mutants, 31 killed,
1 inconclusive, 14 survivors proved by a scratch case and 1 proved an
equivalent mutant). The five that matter most for the round-80 predicates:
`target_pin.matched` re-derivation (guard), `guards` re-derivation (guard),
`verdict_exit`'s rows/survivor conjuncts (guard), `delimited: false` evidence
(binder) and `checks_total` re-derivation (binder).

No lane production file was written, no git write was executed, no tool was
installed.

## Targets (tested bytes, not the moving candidate)

| target | path (lane-relative) | sha256 | pristine selftest |
|---|---|---|---|
| round-79 control binder (4th target) | `tools/round-79/pointer-bind.py` | `40905d39…12cb877` | 21 cases, 0 failures |
| C1 candidate binder | `.ufo/waves/round-80/w1/ExecBinder/pointer-bind.py` | `b01e7b49…a1ff8f8a` | 61 cases, 0 failures |
| C2 candidate provenance | `.ufo/waves/round-80/w1/ExecProv/receipt-provenance.py` | `b07ee0c0…4242c4001` | 20 cases, 0 failures |
| C3 candidate guard battery | `.ufo/waves/round-80/w1/ExecGuard/guard-battery.py` | `d97fcc60…ec59c50` | 33 cases, 0 failures |

All four files re-hashed after the runs and unchanged (`receipt.json`
`targets[].unchanged_since_run: true`). Each candidate was observed at 2–4
earlier revisions while its seat was still writing; those revisions were not
scored (see *Superseded attempts*).

## Method

1. Copy the target into `/fast/scratch/hyaku/kaidoku-r80/MutInstruments/`,
   record `sha256`, run `--selftest` pristine under `TMPDIR` inside that root.
2. Cut one-hunk mutants (anchor asserted to occur exactly once in the pristine
   bytes; replacement is one statement or one expression edit; `compile()`-checked
   before running). Every scored mutant diffs as exactly **1 hunk** (`diffs/hunks.txt`).
3. Run each mutant's `--selftest` under a **four-key child env**
   (`PATH`, `HOME`, `TMPDIR`, `LANG`; nothing inherited), cwd = the scratch copy's dir.
4. `killed` = a `SELFTEST cases=N failures=M` summary is present and `M >= 1`;
   `killed_by` = the failing case names; `sole_detector` = exactly one case fails.
   A copy that does not compile, prints no summary, or whose anchor is absent is
   `inconclusive` — never `killed`.
5. Every survivor gets a case in scratch (`survivor-probes-*.py`) that returns
   **True on pristine, False on the mutant**. If it returns True on both, the
   mutant is reported as *equivalent* (no assertion can pin it), not as a kill.

## Results

### round-79 control binder — 9 mutants, 6 killed, 3 survived

| mutant | edit | verdict | killed by |
|---|---|---|---|
| m1-invert-duplicate-id | invert the duplicate-check-id comparison | killed | green-forged-consistent |
| m2-invert-checks-total | invert the checks_total re-derive | killed | green-forged-consistent |
| m3-drop-start-bound | drop `start >= 1` | **survived** | — |
| m4-drop-token-scan | drop the per-token occurrence scan | killed | red-range-token-outside, red-stale-line |
| m5-drop-digest-guard | drop matched-without-digest | killed | red-forged-no-digest |
| m6-drop-control-guard | drop ok-under-a-control | killed | red-forged-control-ok |
| m7-instrument-digest-constant | compare the instrument digest to a constant | killed | green-forged-consistent |
| m8-drop-range-order | drop `start <= end` | **survived** | — |
| m9-drop-unparsed-overlap | drop matched-and-unparsed | **survived** | — |

Both inversion mutants (m1, m2) are killed only by the **green** forged case —
i.e. the selftest pins the false-positive direction and not the true direction.

### C1 candidate binder — 13 mutants, 9 killed, 3 survived, 1 inconclusive

| mutant | edit | verdict | killed by |
|---|---|---|---|
| b1-substring-reintroduced | accept an undelimited occurrence (round-79 rule) | killed | red-substring-live-token, red-substring-argv-token, red-substring-package-pin, red-prefixed-token, red-followed-token, red-mixed-occurrence |
| b2-drop-closing-delimiter | keep the opening delimiter foot, drop the closing one | killed | same five substring cases |
| b3-last-wins-collapse | collapse duplicate cells to the last one | killed | red-duplicate-omp-cell, red-duplicate-omp-counted, red-duplicate-devin-cell |
| b4-drop-duplicate-report | stop reporting a duplicated cell id | killed | red-duplicate-omp-cell, red-duplicate-devin-cell |
| b5-drop-ok-duplicates | drop ok-true-with-duplicate-cells | killed | red-forged-duplicates-under-ok |
| b6-drop-delimited-evidence | accept evidence that never says `delimited` | **survived** | — |
| b7-bounded-ignores-duplicates | verdict ignores duplicate cells | killed | red-bounded-five-with-duplicate |
| b8-rev-acceptance-widened | accept a symbolic rev in a receipt | killed | red-forged-rev-symbolic, red-forged-rev-nonhex |
| b9-drop-start-bound | drop `start >= 1` | **survived** | — |
| b10-occurrences-zero-accepted | accept `occurrences: 0` with `delimited: true` | killed | red-forged-zero-occurrences |
| b11-drop-evidence-token-match | stop matching evidence tokens to declared tokens | killed | red-forged-wrong-evidence-token |
| b13-drop-checks-total | drop the `checks_total` re-derive | **survived** | — |
| b12-drop-duplicate-check-id | drop the duplicate-check-id guard | inconclusive | anchor absent: the guard was removed from the candidate mid-wave; `duplicates does not re-derive` now covers the behaviour |

The round-80 binder closes two of the round-79 survivors by name
(`red-forged-no-range` covers m8, `red-forged-matched-unparsed` covers m9) and
keeps the third (b9 = m3).

### C2 candidate provenance — 10 mutants, 7 killed, 3 survived

| mutant | edit | verdict | killed by |
|---|---|---|---|
| p1-accept-working-tree | count working-tree bytes as a committed blob | killed | red-working-tree-only, green-expected-control |
| p2-attacks-not-excluded | drop the `/attacks/` filter | **survived (equivalent)** | — |
| p3-symbolic-rev-accepted | treat a symbolic ref as a committed revision | **survived** | — |
| p4-bad-digest-not-skipped | score a malformed digest instead of skipping it | killed | red-no-instrument-skipped, green-expected-control, green-validate-consistent |
| p5-all-flags-expected | every flagged receipt is the control | killed | green-expected-control, red-validate-unexpected-mismatch |
| p6-drop-unexpected-guard | drop the `unexpected` re-derive | killed | red-validate-unexpected-mismatch |
| p7-drop-self-digest | drop the instrument self-digest guard | killed | red-validate-self-digest |
| p8-drop-matched-rev-guard | committed row with no matched revision | killed | red-validate-committed-without-rev |
| p9-drop-receipts-guard | drop the `receipts` re-derive | killed | red-validate-receipts |
| p10-drop-checked-at | drop the `checked_at` guard | **survived** | — |

`red-working-tree-only` fires on p1 — the R80-C2 kill rule "a digest compared
only against the working tree" is properly pinned.

### C3 candidate guard battery — 15 mutants, 9 killed, 6 survived

| mutant | edit | verdict | killed by |
|---|---|---|---|
| g1-drop-duplicate-clause-id | drop duplicate-clause-id | killed | red-duplicate-clause-id |
| g2-drop-ambiguous-prefix | drop ambiguous-prefix | killed | red-ambiguous-prefix |
| g3-drop-prefix-binds-other | drop prefix-binds-another-clause | **survived** | — |
| g4-drop-case-absent-from-source | drop case-absent-from-source | killed | red-case-absent-from-source |
| g5-drop-duplicate-case | drop one-case-per-row | killed | red-case-declared-twice |
| g6-mutate-nonunique-accepted | accept a non-unique clause statement | killed | red-mutate-nonunique |
| g7-killed-without-failing-case | killed though the declared case passes | killed | red-case-passes-on-mutant |
| g8-drop-case-present | stop reporting the absent-case *reason* | **survived** | — |
| g9-verdict-drop-rows | exit verdict ignores a row-count mismatch | **survived** | — |
| g10-verdict-drop-survivors | exit verdict ignores survivors | **survived** | — |
| g11-drop-pristine-cases | drop `pristine.cases` re-derive | killed | red-validate-pristine-cases |
| g12-drop-target-pin | drop `target_pin.matched` re-derive | **survived** | — |
| g13-drop-guards-rederive | drop `guards` re-derive | **survived** | — |
| g14-drop-killed-case-guard | killed without its case failing | killed | red-validate-killed-without-case |
| g15-empty-set-allowed | empty clause set passes the verdict | killed | red-empty-set-verdict |

## Survivors — the assertion each one escapes

Every row was proved by a scratch case that passes on the pristine module and
fails on the mutant (`survivor-probes-*.txt`).

| survivor | missing assertion (case to add) | proof |
|---|---|---|
| guard `target_pin.matched` (g12) | a receipt whose `target_pin.matched` disagrees with `expected == actual` is a defect. Validator has the guard; **no case exercises it**, and the receipt's `ok` can be set so nothing else fires. | pristine: defect present; mutant: clean |
| guard `guards` (g13) | a receipt whose `guards` disagrees with its clause list is a defect. | pristine: defect present; mutant: clean |
| guard `verdict_exit` rows (g9) | `verdict_exit(2, 1, 2, 0, 0) == 1`. | pristine: 1; mutant: 0 |
| guard `verdict_exit` survivors (g10) | `verdict_exit(1, 1, 1, 1, 0) == 1` — one surviving clause must not exit 0. | pristine: 1; mutant: 0 |
| guard prefix-binds-other (g3) | a row whose prefix matches exactly one clause that is *not* its declared clause is a defect. | pristine: "binds G02, not G01"; mutant: row reason `bound` |
| guard absent-case reason (g8) | `judge_mutant(...)` reports `"declared case absent from the mutant output"`, not `"declared case passes on the mutant"`. | pristine: absent reason; mutant: passing reason |
| binder `delimited` flag (b6) | a matched check whose `delimiter_evidence` says `delimited: false` is a defect. | pristine: `matched without delimiter evidence`; mutant: clean |
| binder `checks_total` (b13) | a receipt whose `checks_total` disagrees with its check list is a defect. | pristine: defect present; mutant: clean |
| binder `start >= 1` (b9) / round-79 (m3) | `bind("f.json:0", …)` reports the not-1-based range reason. | pristine: range reason; mutant: token reason |
| prov symbolic rev (p3) | a hex-looking symbolic ref (branch `deadbeef`) is refused; the instrument's own case only uses `HEAD`/`main`/`@HEAD@`, which the hex gate refuses first. | pristine: raises; mutant: returns a commit |
| prov `checked_at` (p10) | a receipt with `checked_at` deleted is a defect. | pristine: defect present; mutant: clean |
| round-79 range order (m8) | a matched check whose `line_start > line_end` is a defect. | pristine: defect present; mutant: clean |
| round-79 matched+unparsed (m9) | a check that is both matched and unparsed is a defect. | pristine: defect present; mutant: clean |
| prov `/attacks/` (p2) | **equivalent mutant** — `discover()` gates on `os.path.isfile` and only lists direct children, so a `/attacks/`-containing path can never be produced; both modules exclude the subdirectory. The case `red-attacks-excluded` is green for the wrong reason. | pristine: true; mutant: true |

## Findings

**F1 (C3, high). `target_pin.matched` is scored but unpinned.** R80-C3's
predicate reads `target_pin.matched true`; `validate_receipt` re-derives it, but
no selftest case exercises that line. A receipt can carry `matched: true` while
`expected` and `actual` disagree (or `false` while they agree) and validate clean
once `ok` is made consistent. Add `red-validate-target-pin` asserting the exact
defect string, beside `red-validate-bound`.

**F2 (C3, high). `guards` re-derivation is unpinned.** `receipt["guards"]` is
the count the C3 predicate reads (`guards 9`); a receipt claiming 9 guards while
listing fewer clauses only trips the `guards does not re-derive` line, which no
case reaches. Add `red-validate-guards`.

**F3 (C3, high). `verdict_exit`'s row and survivor conjuncts are unpinned.** The
battery's exit code is what the L1 runs; deleting two of its three comparisons
keeps all 33 cases green. A battery that exits 0 with a surviving clause, or
with `rows != guards`, would still pass its own selftest. Add
`red-verdict-rows` and `red-verdict-survivors`.

**F4 (C3, medium). `bind_rows`' "prefix binds another clause" guard has no
case.** A row whose prefix matches exactly one clause that is not its declared
clause is accepted as `bound` by the mutant. This is the one-row-wrong-clause
case the table contract exists to prevent. Add `red-prefix-binds-other`.

**F5 (C3, low). `judge_mutant`'s absent-case reason is not asserted.**
`red-case-absent-in-mutant` checks only `(status, case_present)`, so the reason
text — what distinguishes "case absent" from "case passes" — can be wrong while
the case stays green. Assert the reason.

**F6 (C1, high). The receipt's own `delimited` flag is unpinned.** The round-80
match rule is "delimited token on both sides"; `delimiter_evidence_ok` rejects
`delimited: false`, but no case feeds it. A binder could keep the substring
behaviour internally, emit `delimited: false`, and the receipt would validate.
Add `red-forged-undelimited-evidence` asserting
`"c0: matched without delimiter evidence"` exactly.

**F7 (C1, high). `checks_total` re-derivation is unpinned.** The C1 predicate
reads `checks_total 5`; a receipt whose `checks_total` disagrees with its check
list passes the whole 61-case selftest (the `ok` clause checks `len(checks)`,
not the field). Add `red-forged-checks-total`.

**F8 (C1, medium). The `start >= 1` foot of the range guard is unpinned — in
both the round-79 instrument and its successor.** Line 0 is still refused, but
for the token reason with `line_start: 0` in the receipt. The successor fixes
the round-79 `start <= end` and matched+unparsed survivors but not this one.
Add `red-forged-zero-line` (and a `bind("f.json:0", …)` case).

**F9 (C2, high). The symbolic-rev guard is unreachable from its own case.**
`red-symbolic-rev` uses `HEAD`, `main`, `@HEAD@`; `RE_ABBREV` refuses all three
before the symbolic-ref check runs. Only a hex-looking ref name reaches the
guard — a branch named `deadbeef` is refused by the pristine instrument and
accepted by the mutant. The claim's kill rule ("a `rev` that is a symbolic name
accepted") is therefore pinned only accidentally. Add a hex-named ref fixture.

**F10 (C2, medium, equivalent mutant). The `/attacks/` filter is dead code.**
`discover()` lists only direct children and requires `os.path.isfile`, so a path
containing `/attacks/` cannot be produced; `red-attacks-excluded` is green
because the subdirectory is skipped, not because the filter ran. Either delete
the filter or make the population reach it (nested listing), and rename the case
to what it proves.

**F11 (C2, low). `checked_at` is unpinned.** A receipt with no `checked_at`
validates clean. Add `red-validate-no-checked-at`.

**F12 (all, process). Two candidates were rewritten while being tested.** The
binder grew 49 → 61 cases and the provenance instrument 19 → 20 between my first
read and the scored revision; two mutants had to be re-cut (`b11`, `p4`). The
guard battery was observed at four revisions, one of which (`b25eace`, 48,935
bytes, 10:49:26) **raised `Unevaluable` in its own `--selftest`**
(`validate_receipt() has no defects.append clause` in a synthetic nested fixture)
and was superseded ~74 s later. Score a candidate only by the sha256 in the
receipt, and re-run the selftest when the file moves.

## Inconclusive / superseded

- `b12-drop-duplicate-check-id` — anchor absent: the candidate removed its
  dedicated duplicate-check-id guard between revisions; the behaviour is covered
  by `duplicates does not re-derive`.
- Superseded first-pass attempts (anchor miss after candidate churn, re-cut
  against the stable bytes): `b11-evidence-extra-accepted` (the evidence-length
  check was removed) and `p4-bad-digest-not-skipped` (guard renamed
  `RE_HEX64` → `RE_HEX64_ANY`).
- Nothing is reported `killed` on a crash or a missing summary; no mutant failed
  to compile.

## Limits

- Mutants are statement/expression edits, not semantic rewrites; a conjunct
  reached only through I/O (e.g. `git show` failure branches) was not mutated
  except where named (p1, p4, p5).
- The guard battery's *battery* path (`--rev`, clause deletion, mutant
  compilation) was not executed end-to-end — the seat scores selftest
  sensitivity, not the live counter; `g6`, `g7`, `g14` mutate the deletion and
  verdict machinery that path uses.
- Equivalent mutants are reported as such, not as kills: `p2`.
- Fixture repos created by the provenance probes live under my scratch root,
  assert `rev-parse --show-toplevel == fixture`, and were removed with it.

## Evidence index (`.ufo/waves/round-80/w1/MutInstruments/`)

| file | contents |
|---|---|
| `receipt.json` | acceptance receipt: `targets`, `mutants` (47), `survivors` (15), `inconclusive` (1) |
| `mutation-harness.py` | one-hunk mutant runner (anchor-uniqueness, compile check, four-key env, kill rule) |
| `spec-round79.json`, `spec-binder-prov.json`, `spec-binder-extra.json`, `spec-guard.json` | mutation specs (anchors, replacements, edits) |
| `receipt-round79.json`, `receipt-binder-prov.json`, `receipt-binder-extra.json`, `receipt-guard.json` | per-run receipts |
| `survivor-probes.py`, `survivor-probes-binder.py`, `survivor-probes-prov.py`, `survivor-probes-guard.py` | the missing assertions, as executable cases |
| `survivor-probes-round79.txt`, `survivor-probes-binder.txt`, `survivor-probes-prov.txt`, `survivor-probes-guard.txt` | pristine-True / mutant-False transcripts |
| `selftest-pristine-round79.txt`, `selftest-pristine-binder.txt`, `selftest-pristine-prov.txt`, `selftest-pristine-guard.txt` | pristine `SELFTEST` summaries |
| `diffs/hunks.txt`, `diffs/*.diff` | per-mutant diff and hunk count (46 scored mutants: 1 hunk each) |
| `consolidate.py` | receipt merge (targets re-hashed at consolidation) |

**Environment.** Python 3.14.8, git 2.56.0; no installs; child env keys
`PATH/HOME/TMPDIR/LANG`; scratch root `/fast/scratch/hyaku/kaidoku-r80/MutInstruments/`
(removed after the receipts were copied here).
