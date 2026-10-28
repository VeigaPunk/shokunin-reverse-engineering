# R44C2Rubric — the frozen R44-C2 calibration rubric (wave 1)

Seat `R44C2Rubric` (executor). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `c29360e3ba5381a5ab69e372d0d9577970f85018`.

**Deliverables**

| artefact | path |
|---|---|
| the frozen rubric | `.ufo/waves/round-44/w1/artifacts/R44C2Rubric/tools/round-44/c2-rubric.json` (the L1 installs it as `tools/round-44/c2-rubric.json`) |
| this report | `.ufo/waves/round-44/w1/R44C2Rubric.md` |
| receipts | `.ufo/waves/round-44/w1/artifacts/R44C2Rubric/receipts/` |

**Rubric digest**: `rubric_sha256` below (the dev copy and the shipped file are byte-identical).
The counter used for these receipts: `.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py`,
sha256 `085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277`. Every entry carries
`check_script_sha256` = the sha256 of its inline script text (the argv element after `-c`), which is
the counter's per-entry script pin: the script text cannot drift between the freeze and REV.

**Rubric**: 80 entries, 6 of them `expected: "superseded"`, 0 unevaluable at the base
census, **3 mismatches at the base** (all three in the `## Owned axes` table).
`inventory_sha256` over the sorted entry ids: `2037e565ef6fbc721c9f36a3cdfcc3a1584fe1d95df4aea7f759cc48a4e1c89e`.

**Claim scope = the three target ids** (the L1 narrowed the plan's C2 scope to exactly these):

```
C2-a1-owned-coverage-count
C2-a2-owned-depth-count
C2-a4-owned-depth-craft-range
```

Every other census candidate is listed BY ID in the rubric (`scope.excluded_entry_ids`, 77
ids) and carries `"scope": "excluded-census-candidate"`: it is part of the frozen census (a
non-regression gate, green at the base) and is **not** a claim target.

**Control vectors (exact per-id)** - the rubric carries them in `control_vectors`:

| control | exit | mismatches (exact ids) | per-id |
|---|---|---|---|
| CTL-C2-0 do-nothing (base census) | 1 | the 3 target ids | target = mismatch, every excluded id = match |
| CTL-C2-POS positive (bound correction block appended) | 0 | none | all 80 ids = match, `met_target true`, `frozen_path_changed []` |
| CTL-C2-1 seed (positive + LOG.md round-43 heading renamed) | 1 | `C2-d17-sharpen-log-round43-entry` only | the 3 target ids = match, the seed id = mismatch |
| CTL-C2-1b in-place SCORECARD.md statement edit | 2 | - | `frozen_path_changed ["SCORECARD.md"]` (a freeze violation, never a scoreable mismatch) |

## 1. What the rubric measures

The rubric enumerates the checkable self-assessment statements of the claim's frozen scope -
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md` - in the six categories the draft claims file names
(`plans/round-44-claims.md`, R44-C2 "Rubric (to be enumerated and frozen)"):

| id prefix | category | entries |
|---|---|---|
| `C2-a` | (b) the `## Owned axes` CURRENT observable vs the freeze tree | 4 |
| `C2-b` | (b)/(c) pinned clauses re-derived at their own revision | 9 |
| `C2-c` | (a) every `## Capabilities` row's Evidence pointer | 18 |
| `C2-d` | (c)/(e) SHONEN countable claims and the round-43 receipts | 17 |
| `C2-e` | (e) the `## Round <N>` claim-table verdicts vs the cited receipts | 14 |
| `C2-f` | (f) the pinned command-A numbers of the round owned-score lines | 7 |
| `C2-g` | (d) the `planned (round <N+1>)` rows vs the next round's declaration | 8 |
| `C2-h` | (f) the README coverage map and the README entry tables | 3 |

Every entry carries `id`, `file`, `line_at_base`, `line_sha256` (the sha256 of that base line),
`asserted`, `expected`, `note`, `check`/`command` (the argv the counter runs), `observed_key`,
`compare`, `timeout`, `check_script_sha256`, plus `pin` (the revision the statement is scored at, or
`null`) and `category`.

## 2. The check contract every entry obeys

* The command runs with cwd = the exported tree of REV; `{rev}`, `{freeze}`, `{repo}` are
  substituted by the counter. The only path source a check may use is `HYAKU_REPO` (the scratch
  clone that holds the git objects): git objects only, no network, no REA, no execution of committed
  code, no writes.
* Each check prints one JSON object: `{"observed": ..., "derived": ..., "detail": ...}`.
* `derived` is the value re-derived INDEPENDENTLY (command A, a heading range, a committed receipt, a
  marker, a git diff). `observed` is the value the STATEMENT carries at REV - the frozen base line,
  overridden by an appended `<!-- c2-correction: <id> -->` block - but only when it EQUALS
  `derived`; otherwise `observed` is `UNSUPPORTED:<statement value>`.
  **A note is a declaration, never evidence** (R44C2Sentinel B3, hard rule): a note carrying a wrong
  value leaves the entry a mismatch.
* A pinned statement (its own text carries `at <rev>`) is scored at that revision, never at REV
  (R44C2Sentinel B1). The pin is taken from the cited base line.

## 3. The base census (CTL-C2-0) - 3 mismatches, all repairable

`python3 -I -B .ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py --root <LANE> --rev c29360e3ba5381a5ab69e372d0d9577970f85018 --rubric <this rubric> --pre-freeze --work <SCRATCH> --json-out <OUT>`

```
exit_code 1; entries_evaluated 80; mismatches 3; unevaluable 0;
frozen_path_changed []; met_target false
```

The three mismatches are the `## Owned axes` current observables, which the round-41 landing last
refreshed:

| entry | statement says | the freeze tree says |
|---|---|---|
| `C2-a1-owned-coverage-count` | `133/133` knowledge files mapped (round-41 landing, pin `e1c83313`) | `137/137` |
| `C2-a2-owned-depth-count` | `20/20` rule blocks with resolvable citations (round-41 landing, pin `e1c83313`) | `21/21` |
| `C2-a4-owned-depth-craft-range` | craft section `SKILL.md:81-449` (round-41 pin `e1c83313`) | `SKILL.md:81-543` |

The row's own Evidence cell names the counting command (`tools/round-38/c2-counter.py`, whose O1/O2
checks compare the row's count with command A at the scored revision) and its Last-change cell records
the rounds at which the count is refreshed, so the row is the lane's CURRENT observable (rule R2). The
**pinned clauses stay pinned**: `C2-b1`, `C2-b2`, `C2-b3`, `C2-b9` re-derive 133/133, 20/20, 81-343 and
81-449 at their own revisions and all match - the round-44 repair is an appended dated statement, not a
rewrite of the pinned cell (rule R6).

**Repair (frozen in the rubric as `expected_edits`)**: append to `SCORECARD.md`, and nothing else:

```
- **Round-44 calibration correction (2026-10-28):** the `## Owned axes` current observables are re-derived from the round-44 freeze tree: command A reports 137/137 knowledge files mapped (`missing []`, `dangling []`), 21/21 rule blocks with resolvable file/range citations, and the `## Queue-drain craft` section spans `SKILL.md:81-543`. The round-41 pins quoted above (`e1c83313`, `52b0eb29`) remain true at their own revisions.
<!-- c2-correction: C2-a1-owned-coverage-count -->
c2-correction-value: 137/137
<!-- c2-correction: C2-a2-owned-depth-count -->
c2-correction-value: 21/21
<!-- c2-correction: C2-a4-owned-depth-craft-range -->
c2-correction-value: 81-543
```

**Proof that the repair works** (dev arm, scratch clones, the real counter):

```
counter exit 0; mismatches 0; met_target True; frozen_path_changed []
```

**Proof in claim mode** (the rubric + the counter committed in the freeze commit, then a C1-style
coverage-map row inserted into `corpus/README.md` after the freeze, plus the bound correction block):

```
counter exit 0; entries_evaluated 80; mismatches 0; unevaluable 0; frozen_path_changed []; met_target True; claim_score True
```

`frozen_path_changed []` and `claim_score true`: because the rubric does not byte-freeze
`corpus/README.md`, C1's landing no longer trips C2's freeze walk.

**Proof that a wrong repair does not work**: a note carrying a wrong value leaves the entry a
mismatch (the check reports `UNSUPPORTED:<note value>`), because the derived value is the only thing
that can make `observed == asserted`.

## 4. The seeded-mismatch control (CTL-C2-1)

`seeded_mismatch` in the rubric names the control, the entry, the file and the expected observation:

* **primary** - `C2-d17-sharpen-log-round43-entry`: rename the LOG.md round-43 entry heading in a
  scratch clone. `LOG.md` is not a frozen path of this claim, so the entry is scored and must report
  the mismatch; the counter exits 1.
  `counter exit 1; mismatches 1; reported ids ['C2-d17-sharpen-log-round43-entry']`
* **secondary** - `C2-c01-cap-pointer`: replace a `## Capabilities` evidence path with a
  non-existent one. `SCORECARD.md` is frozen with an append-only bound edit, so an in-place
  statement edit is a FREEZE VIOLATION: the counter exits 2 `frozen_path_changed`, never a scoreable
  mismatch. The control must be written to that measured behaviour.
  `counter exit 2; frozen_path_changed ['SCORECARD.md']; unevaluable ['frozen_path_changed']`

## 5. Fitness: the per-entry mutation witness (R44C2Sentinel R2)

Every entry is shown able to FAIL on its own statement. The witness harness mutates the value
source in a scratch clone of the base tree, commits, and runs that entry's own command against the
mutated tree (rev = freeze = the mutated commit): the entry must then report a mismatch.

| | count |
|---|---|
| entries with a measured witness | 80 |
| entries that FAIL as required when their source is mutated | 80 |
| entries whose witness is not demonstrated | 0 |

`none`

Every entry carries its own `mutation_witness` (the mutation applied, the observed value, the
verdict). The three claim targets fail under their witnesses as well:
C2-a1 (the statement's `133/133` mutated -> `UNSUPPORTED:...`), C2-a2, C2-a4.

## 6. The README entry-table check (hardened, R44C2Sentinel R6/R9)

`C2-h2` (the README `## Knowledge` table) and `C2-h3` (the `## Lessons` table) resolve every entry
they name against the committed file set. Two hardening points, both measured:

| attack | before | now |
|---|---|---|
| a row whose first cell repeats the free-text phrase `not a corpus note` (a phantom entry) | skipped, the entry stayed green | `UNSUPPORTED:dangling:2099-01-01-bogus-phantom` - the exemption is STRUCTURAL (an entry that names a `lessons/...` document is a lesson, not a knowledge file); no free-text phrase is honoured |
| a C1 row written as `knowledge/<stem>` instead of the bare `<stem>` | reported dangling | accepted (the leading `knowledge/` is normalised to the bare stem) |

## 7. Dropped statements (10 ids, with reasons)

| `D1` | corpus/README.md `## Frontier` bullets vs PROVINCE.md `## Frontier` bullets | the two lists are prose with no mechanical correspondence rule; a keyword-overlap check would be a green generator (R44C2Sentinel H6). No re-derivable value. |
| `D2` | SHONEN.md box 1/box 3 selftest counts (`selftests 35/35 and 27/27`, `tools/round-40/sqfs-triage-v2.py --selftest` 45 cases) | the second source is the tools' own selftest output, which requires EXECUTING committed code; the counter's checks must stay read-only (git objects only). |
| `D3` | SHONEN.md box 3 `refuses mismatches with exit 3/no manifest` | the refusal exit code is not recorded in any committed receipt; re-deriving it would require running tools/round-43/heldout-gen-v4r43.py (execution, not read-only). |
| `D4` | SHONEN.md box 1 `v4 table region hash remains 92540586...` | the digest is stated truncated with an ellipsis; the full value is not in the lane, so it cannot be re-derived. |
| `D5` | corpus/README.md per-row `state` cells (e.g. `3/7 supported native surfaces`) | the second source of those counts is an external measurement, not a committed artefact; no re-derivable value. |
| `D6` | SHONEN.md box 2/box 3 wave-2 seat reports (`R40W2C2IndepEval.md`, `R41W2Repro*.md`, `R39W2C2Rescore.md`) | the prose inside the seat reports is not a countable claim with a second source; the reports are evidence of a run, not a re-derivable value (their EXISTENCE is checked by the capability-pointer entries). |
| `D7` | SCORECARD.md round-43 heading wording (`overstrict`) vs the round-43 closure correction | the contradiction is already corrected inside the same file (SCORECARD.md:3503 and the text erratum at :3509); it is a text erratum, not a re-derivable value check, and it sits outside the frozen categories (a)-(f). Reported as lesson material. |
| `D8` | SCORECARD.md round-43 section line `wave 2: 32 seats dispatched and pending final settlement` | a stale wave-status sentence (round 43's wave 2 has settled by the base commit); it is not one of the enumerated categories (a)-(f) and names no counting command. Reported as lesson material, not as counter ground. |
| `D9` | SCORECARD.md `## Round <N>` `before` column of the claim tables | the before-cells cite receipts that live in the producing round's scratch paths (e.g. `controls/ctl-c1-0-do-nothing.json` without a repository prefix); the repository does not hold them, so they cannot be re-derived at any revision. |
| `D10` | SHONEN.md box 3 `the smallest table that also scores 20/20 is 8 rows / 7 cells` | the second source is a wave-2 shortcut report, not a committed counting command; the value is a property of that report, not of the lane's committed state. |

## 8. Cross-claim conflicts the L1 must settle (not rubric defects)

1. **`corpus/README.md` is frozen by C2 and appended by C1.** The counter freezes
   `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `SKILL.md` by default; C1's landing adds a
   coverage-map row to `corpus/README.md`, so the C2 freeze walk will report
   `frozen_path_changed` (exit 2) on a correct C1 landing. The rubric needs NO change: its README
   entries read the map at the freeze tree (`C2-h1`, `C2-h2`, `C2-h3`), so the file need not be
   frozen at all. But `C2_DEFAULT_FROZEN` in the counter is applied unconditionally, so dropping
   `corpus/README.md` from the rubric's `frozen_paths` does NOT remove it - the counter author must
   make the rubric's declaration authoritative (or the L1 must rule that C1's README insertion is
   bound). This is the one open item that needs a decision outside the rubric
   (R44ConnRouted A1/A6, R44C2Sentinel B5/B6).
2. **The round-44 landing section cannot be appended to `SCORECARD.md`** under the current counter
   contract: the bound edit allows exactly the correction block and nothing else. The L1 must land
   the round record elsewhere or re-freeze with it bound.
3. **`SCORECARD.md:3508`'s pinned command-A line and the round owned-score lines** are scored at
   their pins, so C1's later landing does not move them.

## 9. How the L1 must run the counter

The claim score must be run WITHOUT `--rubric`, so the rubric is read from the freeze commit
(`rubric_source: "freeze"`, `claim_score: true`); with `--rubric <file>` the counter marks the run
`rubric_source: "file"` and `claim_score: false` (a census/dev arm, never a claim score). The
receipts in this report are dev-arm runs (`rubric_source: "file"`), which is why they carry
`claim_score: false`.

```
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>     --work <SCRATCH> --json-out <OUT>            # the claim score (rubric read from the freeze)
python3 -I -B tools/round-44/c2-counter.py --root <LANE> --rev <BASE> --pre-freeze     --work <SCRATCH> --json-out <OUT>            # CTL-C2-0: the base census
```

**Landing requirement (the L1's open item).** The rubric, the counter and every other round-44
tool must be committed IN the freeze commit: `frozen_dirs` is `tools/round-44`, so a file added under
it after the freeze is `added_under_frozen_dir` -> exit 2, and recovering needs a new freeze. Install
this rubric as `tools/round-44/c2-rubric.json` in the SAME commit as the counter, the carriers and
`c1-run.sh`.

## 10. Evidence and receipts

| receipt | what it shows |
|---|---|
| `receipts/base-census-summary.json` | the base census: command, exit code, stdout sha256, wall time, entries evaluated, the three mismatch ids |
| `receipts/census-base.json` | the counter's full base-census receipt |
| `receipts/control-repair.json` | the counter run after the bound correction block was appended (exit 0, mismatches 0) |
| `receipts/control-seeded-mismatch.json` | the seeded-mismatch control (LOG.md round-43 entry) |
| `receipts/control-seeded-in-place-edit.json` | the in-place SCORECARD.md edit control (exit 2, frozen_path_changed) |
| `receipts/control-claim-mode-c1-readme-row.json` | claim mode (rubric+counter in the freeze commit, a C1-style README row after the freeze, the bound SCORECARD block): exit 0, mismatches 0, met_target true, claim_score true, frozen_path_changed [] |
| `receipts/mutation-witness.json` | the per-entry mutation witness (the fitness gate: every entry shown able to fail) |
| `receipts/census-shipped-artifact.json` | the base census run against the SHIPPED rubric file itself (exit 1, 3 mismatches, 0 unevaluable) |

Scratch (mine): `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Rubric/`.
