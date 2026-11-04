# ScribeKnowledge — round 80, wave r80-w1

Seat: `ScribeKnowledge` (scribe — drafts prose and registry cells; the L1 lands them).
Base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`; declaration guard
`84d68e90f8a1ea3a3a7f94a208695c21023c0472` (`git log -1 --format=%H -- plans/round-80-claims.md`);
lane head at draft `84d68e90…`, with the base an ancestor. The working tree was clean of tracked
modifications when this seat started and stayed so (the only pre-existing untracked entry was
`.ufo/waves/round-80/r80-w1.ready.dispatched`).

## Behavior

Drafted the round-80 knowledge entry `corpus/knowledge/2026-11-04-r80-four-bindings.md` and its
registry cells, entirely under `.ufo/waves/round-80/w1/ScribeKnowledge/`. Nothing in `tools/`,
`corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `plans/` or another seat's directory
was written or edited.

The entry, titled **"Four bindings: an exact token, a unique cell, a committed blob, an isolating
case"**, has four decision-table sections in the lane's register:

1. **Exact-token binding** — the delimiter class `[A-Za-z0-9._-]`, the two refusal signatures
   (`rea-agents@6.7.05` and `rea-agents@6.7.00` against the declared `rea-agents@6.7.0`) and the two
   green controls (the same pin in quotes; `GHIDRA_INSTALL_DIR=` inside a two-line `.bashrc` range),
   with the anti-degenerate argument: the green control carries the *same* token the reds refuse.
2. **Duplicate-cell rule** — the round-79 dict comprehension collapses before the checks are built, so
   `checks_total` stays 5 and `duplicates` is absent; what is lost is the count of declarations, not
   the token. RFC 8259 section 4 (S049) supplies the reason a reader cannot be blamed: last-wins is a
   documented behaviour, and the RFC's verb is SHOULD, so the lane's refusal is its own stricter policy.
3. **Receipt provenance** — a declared `instrument.sha256` must equal a committed blob of the path it
   names; committed revs are enumerated, working-tree bytes and symbolic revs are not committed. The
   worked failure is round 79's `c2-at-landing.json` whose `a0044c4c…` matches neither committed blob
   of `tools/round-79/pointer-bind.py`. The all-zero `prov-forged-instrument.json` is the control, and
   its well-formed `instrument.rev` shows rev presence is not the discriminator.
4. **Guard-table binding** — the block delimiters, the four-cell row shape, the nine clause prefixes in
   source order with base-blob line numbers, an absent declared case counting as a survivor, and the
   two base numbers that answer different questions (deletion probe: 8 survivors, 1 killed; frozen
   battery: 9 survivors by declaration).

Every quantitative sentence names its command and a receipt path under `.ufo/waves/round-80/`; every
value the round has not measured is written literally as `pending the landing receipt`.

## Gates

| acceptance item | state |
|---|---|
| draft entry, full markdown | `draft-entry.md` — front-matter trio (`source:` / `verified-at:` / `recheck:`), four rule sections, shared-conclusion section, six limits, evidence block |
| coverage-map row | `coverage-row.md` — one row in the existing `\| section \| entries \| state \|` shape plus a coverage-consequence note |
| `used_by` values for the two rows | `sources-used-by.md` — S297 append; S049 append with tier/scope unchanged; S143 append; S298 explicitly withheld |
| receipt JSON with `title`, `cites`, `commands` | `receipt.json` — plus base arms with receipt paths, the pending list, risks and the bounds record |
| report | this file |

## Touched surfaces

Written (all under the seat dir except the report itself):

- `.ufo/waves/round-80/w1/ScribeKnowledge/draft-entry.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/coverage-row.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/sources-used-by.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/receipt.json`
- `.ufo/waves/round-80/w1/ScribeKnowledge.md`

Read for grounding (no writes): `plans/round-80-claims.md`, the frozen fixture set, the sources seat's
`receipt.json` and snapshots, `ExecGate`'s table draft / candidate gate / pristine selftest,
`ReviewerC3`'s deletion receipt, `ReviewerC1`'s control receipt, `ScribeLesson`'s C1 base-arm
grounding, `.ufo/waves/round-80/l1/scores/c2-at-base.json`, `tools/round-78/attack-gate.py`,
`tools/round-79/pointer-bind.py`, `PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`,
`SCORECARD.md`.

## Findings

1. **The RFC row is a refused reuse, and the entry says so.** S049 (round 21) already holds RFC 8259
   section 4, page 6, with a scope cell naming duplicate-name interoperability and a teaches cell
   naming unpredictable receiver behaviour; S289 already holds the same `.txt` bytes
   (`61a5378f4255c720…`). The sources seat's receipt independently recorded `disposition: withhold` for
   S298. The entry therefore cites S049 and gives S298 no `used-by`.
2. **The `\b` row is the only genuinely new source, and it is S297.** No registry row covers word
   boundaries (`grep -in 'word boundary' corpus/SOURCES.md` returns 0 hits); S143 covers `re.fullmatch`,
   a different anchor. The entry uses S143 for the equality-over-containment principle and explicitly
   refuses to claim `fullmatch` can bind a token inside a longer line — that distinction is why the
   `\b` row is needed at all.
3. **C3's two base numbers are compatible and the entry says how.** The deletion probe at the pristine
   29-case gate kills exactly one clause (`: refused without a reason`) and leaves 8 survivors; the
   frozen battery reports 9 survivors because no row declares a case. The gate therefore had one
   behavioural detector and no record of it. This also explains the target `pristine.cases 37`: eight
   new cases plus the pre-existing `red-validate-refused-no-reason`, not nine new ones.
4. **The C2 denominator is conditional.** 34 of the 141 `l1/scores/*.json` files in rounds 60–79
   declare an `instrument` block, which is exactly the frozen `receipts 34`; a receipt with no
   instrument block is outside the sweep. The entry states this and marks the 141 as a seat-local count
   with its command, not as a lane receipt.
5. **The delimiter trap is worth recording.** The pin token itself contains `@`, which is outside
   `[A-Za-z0-9._-]`; the rule tests only the neighbours of an occurrence. The refusal diagnostic widens
   the class with `@` solely to name the longer token whole. A naive reading of the class would refuse
   every real pin.
6. **The round-79 digest is unrecoverable by any committed revision.** Over the committed revisions of
   `tools/round-79/pointer-bind.py` the blob digest takes only two values (`40905d39…`, `91d23dad…`);
   the receipt's `a0044c4c…` is neither, so widening the comparison from "the declared rev" to "any
   committed revision" does not rescue it.

## Out of scope / not done

- Did not run any round-80 battery, binder or sweep: those are the executor and reviewer seats'
  measurements, and the landing receipts are theirs. Values not yet landed stay `pending the landing
  receipt`.
- Did not edit lane production, did not assign or reserve source ids, did not choose the landing
  receipt filenames beyond the established `l1/scores/` convention where it already exists.
- Did not fetch any source; cited the snapshots the sources seat already retained.

## Bounds deviation (self-reported)

One deviation: while diffing the base gate's selftest case names against the candidate, this seat wrote
a transient file `/tmp/b.py` and removed it in the same command. That is a scratch-path violation of
this seat's bounds (scratch belongs under `/fast/scratch/hyaku/kaidoku-r80/ScribeKnowledge/`). Nothing
depends on it and no receipt cites it; it is recorded here rather than silently dropped. All other
work used the mandated scratch dir, which was removed before yield.

## Open items for the L1

- Land the entry and the coverage row; append the three `used-by` values and leave S049's scope cell
  untouched.
- If the L1 decides to land an RFC 8259 section-4 row despite the refused-reuse verdict, this entry
  must be re-cited to that row and S049's `used-by` dropped — otherwise the registry claims two rows
  for one sentence.
- Land the guard table block from `.ufo/waves/round-80/w1/ExecGate/guard-table-draft.md` verbatim; the
  entry's nine prefixes and case names are the draft's, and the battery's `rows 9` is only meaningful
  once the block is in `SKILL.md`.

## Artifacts

- `.ufo/waves/round-80/w1/ScribeKnowledge/draft-entry.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/coverage-row.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/sources-used-by.md`
- `.ufo/waves/round-80/w1/ScribeKnowledge/receipt.json`
- `.ufo/waves/round-80/w1/ScribeKnowledge.md`
