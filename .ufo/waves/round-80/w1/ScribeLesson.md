author: ScribeLesson seat (r80-w1), scribe
round: 80 — kaidoku
date: 2026-11-04
base: `16dfa009bf143080dfcdfc5f9ec34bd359536d90`
declaration: `84d68e90f8a1ea3a3a7f94a208695c21023c0472`
measured rev (after arms): `b00419fb8c3d083761034605fec2eed1897f60ad`
verdict: draft delivered; C1 and C2 fully green, C3 green except the target-pin conjunct its own printed command cannot reach

# ScribeLesson — the round-80 lesson draft and the grounding behind it

## What this seat did

Read `corpus/lessons/round-79.md` and `corpus/lessons/round-79-verifier-spotcheck.md` first, then
grounded every prose claim in bytes: the round-79 landing receipt's instrument digest, the round-79
binder's substring test and last-wins cell map, the round-78 gate's sole `validate_receipt` case and
its nine clause lines, and one prose pointer that moved between two committed blobs. Wrote the
candidate lesson, a machine receipt and four grounding arms. Ran all four landed round-80
instruments at base, at the declaration and at the landed tip; HEAD moved three times during the
seat (`253fc817`, `b8260107`, `b00419fb`), every movement a landing of this round's work. No lane
production file was edited, no git write was made, and no `SOURCES.md` row was appended by this seat.

## Measured (commands, observed, verdict)

| arm | command shape | observed | verdict |
|---|---|---|---|
| R80-C1 candidate | `strictness-battery.py --impl tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --fixtures …/strictness.json` | exit 0, `cases 4`, `green_cases 2`, `candidate_false_greens 0`, `control_false_greens 4`, both refusal counts 0, `--validate {"defects": []}` | all frozen C1 targets met |
| R80-C1 control-as-candidate (base shape) | same, `--impl tools/round-79/pointer-bind.py` | exit 1, `candidate_false_greens 4`, naming `rb01`–`rb04` | the fixtures are the before state |
| R80-C1 live arm | `pointer-bind.py --rev b00419fb…` | exit 0, `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`, `duplicates []`, `--validate {"checks": 5, "defects": [], "matched": 5}` | frozen live target met |
| R80-C2 base | `receipt-provenance.py --rev 16dfa009… --from-round 60 --to-round 79` | exit 1, `receipts 34`, `flagged 2`, `expected_control_flags 1`, `unexpected 1`, naming only `c2-at-landing.json`; `--validate` defect-free | base arm reproduces exactly |
| R80-C2 declaration | same at `84d68e90…` | exit 1, 34 / 2 / 1 / 1 — identical | after arm absent at that rev |
| R80-C2 after | same at `b00419fb…` | exit 0, 34 / **1** / 1 / **0**, `unexpected_receipts []`, `--validate` defect-free | target met |
| R80-C3 base | `guard-battery.py --rev 16dfa009…` | exit 1, `guards 9`, `rows 0`, `bound 0`, `survivors 9`, `pristine 29/0`, `target_pin.matched false`; `--validate` defect-free | base arm reproduces exactly |
| R80-C3 after | same at `b00419fb…` | exit 0, `guards 9`, `rows 9`, `bound 9`, `survivors 0`, `pristine 37/0`, **`target_pin.matched false` (`expected ""`)**, `--validate` defect-free | every counter but the pin |
| R80-C3 after + pin | same, plus `--expect-sha256 df6fb856…` | exit 0, `target_pin.matched true`, `actual == expected == df6fb856…`, `--validate` defect-free | pin met only with the flag |
| independent deletion arm | `ast` on a scratch copy of `attack-gate.py`, remove each clause's `If` | clause 5 → `failures 1`; the other eight → `failures 0`; byte copy and ast round-trip both `29/0` | one clause exercised, none declared |
| independent provenance sweep | 141 `l1/scores/*.json` receipts, rounds 60–79, `/attacks/` excluded | 34 declare an `instrument` block, 107 do not; `flagged 2` = forged control + round-79 landing receipt; revs 31 hex / 3 absent / 0 symbolic | counter 34 is mechanical |

Instrument digests of the bytes that produced the numbers: `receipt-provenance.py` `b59068d6…`,
`guard-battery.py` `b9b3b10c…`, `strictness-battery.py` `2b26d75a…`, `pointer-bind.py` `2e4a7852…`,
control `tools/round-79/pointer-bind.py` `40905d39…`, gate `tools/round-78/attack-gate.py`
`df6fb856…` at `b00419fb` (`4e4baf00…` at base). Selftests as run: 14/0, 19/0, 8/0, 33/0.

## Deliverables and acceptance checks

- `.ufo/waves/round-80/w1/ScribeLesson/round-80.md` — candidate `corpus/lessons/round-80.md`:
  three tables (`## Mistakes` 4 rows × 4 cells, `## Gate` 2 admits + 2 rejects, `## Sources`), every
  mistake row carries class, `path:line@blob` evidence, captured-by, and a fix shown able to fail and
  (for three of four) able to pass; each capture mechanism restated as a command.
- `.ufo/waves/round-80/w1/ScribeLesson/receipt.json` — `mistakes`, `gate_admits`, `gate_rejects`,
  `commands`, plus `sources`, `instruments`, `findings`, `limits`; JSON parses.
- `.ufo/waves/round-80/w1/ScribeLesson/grounding/` — base, declaration and after arms for all three
  claims (`c1-*`, `c2-*`, `c3-*`, `after-arms.txt`), `c3-clause-deletion.txt`, `m1-provenance.txt`,
  `m4-line-drift.txt`, `gate-quotes.txt`.
- `.ufo/waves/round-80/w1/ScribeLesson/sources/` — `man7-grep.html`, `toml-v1.0.0.html`,
  `uax29-tr29.html`, byte counts and digests in the Gate/Sources tables.

## Findings

1. **F1 — high for a verbatim re-derivation — the C3 prose predicate and the machine record disagree
   on `--expect-sha256`.** `plans/round-80-claims.md` requires `target_pin.matched true` but prints
   the command without the flag; `guard-battery.py:320-322` sets `expected` only from the flag, so
   the prose's literal command exits 0 with `expected ""` and `matched false`, and `--validate` does
   not flag the empty expectation. The machine record `.ufo/waves/round-80/claims.json:34,37`
   (sha256 `0f33ea87…`, committed) carries the flag, so the predicate of record is satisfiable and my
   run with `--expect-sha256 df6fb856…` reaches `matched true`. Round-79's M-class ("a printed
   counting command that was never run as printed") recurs in prose form; the wave's critic
   (`w1/CriticClaims.md:205-211`, `:422` G1) already routes it as a blocker with the same correction.
   Route: land the prose with the flag (or a disclosed supersession); never report `matched false` as
   green.
2. **F2 — medium — the C2 sentence and its counter disagree on the population.** The predicate says
   "every `l1/scores/*.json` receipt (excluding `/attacks/`)"; the instrument's population is the 34
   that declare an `instrument` block, and 107 of 141 JSON files never enter it. The frozen base
   `receipts 34` fixes the intended reading, so the counter is right and the sentence should be
   narrowed to "every receipt that declares an `instrument` block" (or the instrument should flag a
   missing block). Reported, not edited: claims are frozen.
3. **F3 — medium — R80-C3's base arm is 9 only because the rule says "declared case".** My deletion
   arm shows eight clauses have no failing case at all, and clause 5 has one
   (`red-validate-refused-no-reason`, `attack-gate.py:921`) that no table row declares; the
   instrument's survivor reason is "no declared case bound to this clause". A re-implementation that
   scored "any case fails" would report `survivors 8` and could reach `survivors 0` without a table
   row. Keep the word **declared** in the claim, the battery and the SKILL block.
4. **F4 — info — the registry append diverges from the sources seat's draft.** The seat drafted
   `re` as `S297` and withheld the RFC row as a reuse (`w1/ScribeSources/rows-draft.md`); the L1
   landed `S297` = RFC 8259 and `S298` = `re` in the working tree (204 rows, sha `b4d67a32…`,
   uncommitted at this read; 202 committed). Both quotes and digests verify against the landed
   snapshots; the seat receipt's `next_ids` now misdescribes the registry. The post-append census is
   the L1's.
5. **F5 — info — HEAD moved three times during the seat** (`253fc817` instruments, `b8260107` gate +
   SKILL block, `b00419fb` round-79 receipt re-take). Every arm in this report names its commit and
   its instrument digest, so a later movement does not silently re-label an observation.
6. **F6 — info — the round-79 receipt has a prose-only working-tree edit after `b00419fb`.** The
   uncommitted change rewrites `supersession.reason` (the disclosure text); instrument digest, rev,
   checks and counts are unchanged, so the C2 after arm is unaffected.
7. **F7 — low — `--validate` on a missing receipt raises a traceback.** `receipt-provenance.py
   --validate <absent>` and `guard-battery.py --validate <absent>` both exit 1 through
   `FileNotFoundError` rather than a clean message; observed once while a failed run had written no
   receipt. Cosmetic, but it makes an operator error look like an instrument crash.

## Out of scope / not done

No production edit (`tools/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `plans/`,
`corpus/`), no `SOURCES.md` append, no L1 landing, no commit/push/checkout, no fleet-root write, no
post-append census. No tool installs; pacman untouched. One scratch dir
`/fast/scratch/hyaku/kaidoku-r80/ScribeLesson/` was created, passed as `TMPDIR`, and deleted before
yield; no tool was found to hardcode `/tmp`.

## Risks

- Landing the prose predicate with its printed command as-is leaves `target_pin.matched false` under
  a green exit; the kill rule ("a target pin that is not re-derived from the same revision") can be
  read to void the claim. The machine `claims.json` already carries the flag.
- Landing the lesson's `path:line` cells without their blob digests reintroduces the M4 defect.
- If the L1 reorders the registry rows again, the Gate's `S297`/`S298` cells must be corrected; the
  quotes and digests are independent of the id.
- The registry append is uncommitted at this read; the lesson's Sources cell records both states.

## Artifact paths

- `.ufo/waves/round-80/w1/ScribeLesson.md` (this report)
- `.ufo/waves/round-80/w1/ScribeLesson/round-80.md` (candidate lesson)
- `.ufo/waves/round-80/w1/ScribeLesson/receipt.json`
- `.ufo/waves/round-80/w1/ScribeLesson/grounding/` (20 files) and `…/sources/` (3 snapshots)
