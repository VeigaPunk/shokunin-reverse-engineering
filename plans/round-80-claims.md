# Round 80 — declared claims (frozen; no amendments after the freeze commit)

Base `16dfa009bf143080dfcdfc5f9ec34bd359536d90` (the round-79 lane tip after the round-79
non-author spot-check; lane tree clean and pushed at the start; `jj-lane.sh state` reports
`ahead=0 behind=0 tracked=0 untracked=0`).

Three claims on three distinct axes, causally separable: C1 changes the pointer binder's
**match rule** and reads only the two implementations' behaviour on a frozen fixture set; C2
changes the **receipt population's provenance status** and reads only committed git blobs; C3
changes the attack gate's **selftest and the SKILL decision table** and reads only that
instrument's own selftest output. No counter reads another's receipt, and no two claims write
the same file. All three are capability acquisitions in the AXES sense: the instrument runs, its
output verifies, and its row enters the SCORECARD capabilities table in the same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies. The stagnation nudge's waiver is not met (capability rows entered
in rounds 74–79, inside the 10-round window), so no waiver is claimed. **`lowest-axis:
calibration`** — R80-C1 works the tied-lowest axis; C3's axis is `depth` and C2's is `freshness`,
which this round enters as an owned axis with its first measured baseline (round-79 non-author
spot-check item 4: `freshness` was claimed without an owned-axis row).

**Population — the round-79 closure's routed survivors and defects.** The round-79
mutation-tester (`MutInstruments`) proved five `--selftest` survivors in the round-79 instruments
and the round-79 non-author spot-check routed six defects. Disposition:

- spot-check item 1 (a landing receipt naming an unrecoverable instrument revision) and the
  `MutInstruments` class behind it → **R80-C2**, generalised from a one-off repair to a sweep over
  every landing-class receipt of rounds 60–79.
- spot-check item 4 (`freshness` claimed without an owned axis) → the `freshness` axis row, and
  **R80-C2** as its first measured move.
- `MutInstruments` finding 2 ("`validate_receipt` guards are broadly unpinned") and finding 1
  (the `gm-f` survivor) → **R80-C3**, measured over all nine clauses of
  `tools/round-78/attack-gate.py`'s `validate_receipt()`.
- round-79 ReviewerC2's two named limits (a duplicate client cell collapses last-wins; a
  substring pin `rea-agents@6.7.05` binds against `@6.7.0`) → **R80-C1**.
- spot-check items 2 (registry tally 19 vs 21), 3 (S296 says 17 words, the quote is 15), 5 (no
  rejection in the round-79 Gate) and 6 (capability-row name) are record/prose repairs carried
  **unclaimed**, closed in this round's registry update, lesson and record.

## R80-C1 — calibration: the record's pointer cells bind as exact tokens, and a duplicate cell is a defect

**Type.** Capability acquisition. Round 79 landed a binder that matched a declared token with a
bare substring test and built its cell map with a dict comprehension, so a longer live token
(`rea-agents@6.7.05`) satisfied a shorter declared pin (`rea-agents@6.7.0`) and a record naming
the same client twice silently kept the last cell. Both limits were named by the round-79 wave
(ReviewerC2) and neither was measured.

**Surface.** `PROVINCE.md`'s five pointer cells and the match rule
`tools/round-79/pointer-bind.py` applies to them (`bind()`'s `token in line` test and
`parse_record()`'s `{name: (pin, pointer)}` collapse) — not the cells' values (round 79's
surface, whose 5/5 reading is unchanged and must not regress).

**Rule.** A pointer binds only when every declared token occurs in the pointed lines as a
**delimited token**: each occurrence is delimited on both sides (start/end of line, or a
character outside `[A-Za-z0-9._-]`). A record that declares the same client cell twice is a
**duplicate** defect: every declared cell is counted (`checks_total` includes both) and the
receipt carries the duplicate id in `duplicates`, matching no suppression and no last-wins
collapse.

**Predicate (one sentence, frozen).** R80-C1 is verified iff
`python3 -I -B tools/round-80/strictness-battery.py --root . --impl tools/round-80/pointer-bind.py
--control-impl tools/round-79/pointer-bind.py --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json
--json-out <receipt>` exits 0 with `cases 4`, `green_cases 2`, `candidate_false_greens 0`,
`control_false_greens 4`, `candidate_green_refusals 0`, `control_green_refusals 0` and a
defect-free `--validate`, and
`python3 -I -B tools/round-80/pointer-bind.py --root . --rev <measured> --json-out <live>` exits 0
with `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0` and `duplicates []`; at base
`16dfa009` the same battery with `--impl tools/round-79/pointer-bind.py` reports
`candidate_false_greens 4`.

**Kill rule (frozen).** Any of: a red fixture counted refused while the candidate still reports
the pointer matched or the duplicate collapsed; a green control refused by the candidate; a
`control_false_greens` below 4 (the control arm must reproduce the old weakness, else the
fixtures are not the before state); a case or green-control count other than 4/2; a live arm with
one mismatch, one unparsed cell or one duplicate; a receipt whose `--validate` is not defect-free;
a candidate that refuses every input (caught by the two green controls, whose refusal count must
be 0).

**Controls (scored before data).** The round-79 implementation is the do-nothing control and must
score `control_false_greens 4` on the frozen fixtures — a control that already refuses them would
prove the fixtures are not red. Two green controls (an exact pin line and an exact range line)
must bind under both implementations, so an implementation that refuses everything fails the
predicate. The fixture set is committed at the declaration:
`.ufo/waves/round-80/l1/fixtures/strictness.json`.

## R80-C2 — freshness: every landing-class receipt's instrument digest names a committed blob

**Type.** Capability acquisition. Round 79's non-author spot-check found that
`.ufo/waves/round-79/l1/scores/c2-at-landing.json` records an instrument digest
(`a0044c4c50…`) that matches no committed blob of `tools/round-79/pointer-bind.py`, so its
provenance is unrecoverable; that was one receipt found by reading, not a class checked by an
instrument.

**Surface.** The `l1/scores/*.json` receipts of rounds 60–79 under this lane's `.ufo/waves/`,
excluding any path containing `/attacks/` (those are declared forged fixtures in their own
directories), and the committed blobs of the instrument path each receipt declares.

**Rule.** A receipt is provenance-bound only when its `instrument.sha256` equals a committed
blob of its `instrument.path` — the blob at the receipt's declared `rev`/`record.rev`, the blob
at the lane branch tip, or a blob of that path at any committed revision of the branch. A digest
that matches no committed blob is a defect. One receipt is a **declared negative control**
(`prov-forged-instrument.json`, round 69's forged-instrument fixture) and must stay flagged.

**Predicate (one sentence, frozen).** R80-C2 is verified iff
`python3 -I -B tools/round-80/receipt-provenance.py --root . --rev <measured> --from-round 60
--to-round 79 --json-out <receipt>` exits 0 with `receipts 34`, `flagged 1`,
`expected_control_flags 1`, `unexpected 0` and a defect-free `--validate`, while at base
`16dfa009` the same command exits 1 with `flagged 2`, `expected_control_flags 1`, `unexpected 1`
and the unexpected flag names `.ufo/waves/round-79/l1/scores/c2-at-landing.json`.

**Kill rule (frozen).** Any of: a receipt counted provable whose digest matches no committed blob
of its declared path; a flagged receipt dropped from the population (deleted, or its
`instrument` block removed) instead of repaired; the declared control flag absent; a `receipts`
count other than 34 without a disclosed population change committed with the receipt; a digest
compared only against the working tree; a `--validate` defect; a receipt whose `rev` is a
symbolic name (`@HEAD@`, `main`) accepted as a committed revision.

**Controls (scored before data).** `prov-forged-instrument.json` is the natural negative control:
a correct sweep must flag it, so "flagged 0" is not the target and cannot be reached by refusing
everything. The base arm is the do-nothing control: repairing nothing leaves `unexpected 1`.

## R80-C3 — depth: the receipt-validation clauses become a decision table with one isolating case each

**Type.** Capability acquisition. The round-79 mutation-tester proved three of the round-78
attack gate's `validate_receipt()` refusal clauses survive deletion with every selftest case
green (`gm-f`, `gm-g`, `gm-h`), and its finding 2 names the class: each clause is a sentence of a
frozen kill rule with no isolating case. Round 79's plan carries the item as (a) and (b).

**Surface.** The nine `defects.append(...)` clauses inside
`tools/round-78/attack-gate.py`'s `validate_receipt()` (duplicate fixture id, fixture ids differ
from the declared set, fixture dir mismatch, `base.accepted` not a bool, refused without a
reason, refused by another rule, `base_accepted` not re-derived, `refused` not re-derived,
instrument sha256 not this file's digest) and the SKILL decision table that names them.

**Rule.** Each clause has exactly one row in the round-80 decision-table block of `SKILL.md`
(clause id, exact trigger, the clause's message prefix) and exactly one declared selftest case
that is present in the gate's `--selftest` output and FAILS when the clause is deleted from a
copy of the instrument at the measured revision. The binding is a bijection: no clause without a
row, no orphan row, no duplicate clause id, no two rows on one clause.

**Predicate (one sentence, frozen).** R80-C3 is verified iff
`python3 -I -B tools/round-80/guard-battery.py --root . --rev <measured> --json-out <receipt>`
exits 0 with `guards 9`, `rows 9`, `bound 9`, `survivors 0`, `pristine.cases 37`,
`pristine.failures 0`, `target_pin.matched true` and a defect-free `--validate`, while at base
`16dfa009` the same command exits 1 with `guards 9`, `rows 0`, `bound 0`, `survivors 9`.

**Kill rule (frozen).** Any of: a clause counted bound whose declared case is absent from the
mutant's output or passes there; a declared case that also fails on the pristine instrument (a
case that is not isolating); a duplicate clause id, an orphan row or a row naming no clause; a
mutant copy that does not compile or prints no `SELFTEST` summary counted as killed; `survivors 0`
reached with fewer than 9 guards (empty-set gaming); a `pristine.cases` value that does not
re-derive from the instrument's own `--selftest`; a target pin that is not re-derived from the
same revision.

**Controls (scored before data).** The base arm is the do-nothing control: with no table block
and no isolating case, the battery reports `rows 0`, `bound 0`, `survivors 9` (an absent declared
case is a survivor, never a pass — round 79's rule). The declared case names are frozen in the
SKILL block, so a case named but not written cannot score green.

## Frontier step (inside the 1–3 claim cap, not a fourth claim)

- `corpus/SOURCES.md` is curated by a scribe from sources opened this round; each new row's Gate
  entry carries this round's access date and a ≤25-word located quote. At least one rejection is
  recorded with reason and flip (round-79 spot-check item 5).
- At least one claim rests on a row opened this round: R80-C1's exact-token rule and
  duplicate-cell rule cite the two new rows (a word-boundary matching authority and a
  duplicate-name authority).
- One mistake is mined into `corpus/lessons/round-80.md` `## Mistakes`: the round-79 landing
  receipt's unrecoverable instrument digest (class · evidence · captured-by · fix), where the fix
  is the R80-C2 sweep, shown able to fail on the base population.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  reports exit 0 with 202 rows at round start.

## Wave shape

ONE v1 wave (`r80-w1`) of 15 seats under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 8–16): 4 executors, 2 scouts, 3 scribes, 2 reviewers, 1 critic, 1 mutation-tester,
1 sentinel, 1 connector. Attack roles 4/15 = 26.7 % (reviewer ×2, critic, mutation-tester);
one connector. The L1 holds the canonical planner seat (the validator rejects a planner role).
Residual: none planned; any residual goes to one ordinary call of ≤4 seats and is counted.
