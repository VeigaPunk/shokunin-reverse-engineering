# Round 48 claims — freeze

Lane `kaidoku`, round 48, attempt 1. Base `61b87d742032e65fca9c38267d7d6ed7e555edad`
(`jj-lane.sh state` at claim time: `branch=main local=61b87d74 remote=61b87d74`).

**Freeze** = the commit that first contains this file, `tools/round-48/` (a directory
pathspec) and `tools/round-48/census2.json`. Receipts under `.ufo/waves/round-48/controls/`
are not frozen: a do-nothing control can only be scored against a freeze that already
exists. `git log --format=%H -1 -- plans/round-48-claims.md` re-derives the freeze; the
report cites it as `plans/round-48-claims.md@<freeze>`. Nothing in this file or in
`tools/round-48/` changes after the freeze: a change makes both counters exit 2
`frozen_path_changed`.

Owned axes are all tied at 10 (`SCORECARD.md` `## Owned axes`), none retired; the last
capability entered in round 43, so the stagnation nudge does not waive the lowest-axis
obligation. Two claims on two distinct tied-lowest axes. Coverage gets no claim: this round
adds no domain surface (no knowledge entry, no PROVINCE move, no coverage-map row).

| claim | axis | surface |
|---|---|---|
| R48-C1 | depth | `SKILL.md` `## Queue-drain craft` rule block 25 — the **verdict-meaning** matrix over the two HIGH round-47 routed defects — its interpreter `tools/round-48/meanings.py`, and the instrument-registry section re-bound to `tools/round-48/census2.json` by meaning, not by digit |
| R48-C2 | calibration | the lane's **record instrument**: `tools/round-48/record2.py` re-derives `SCORECARD.md` from committed bytes (the round-47 atom oracle executed from `--rev`), with a completeness floor, quoted-receipt binding, `axes`-correction parsing and the Owned-axes score-cell binding |

**Why this round exists.** The round-47 non-author spot-check routed two HIGH defects and
three MEDIUM/LOW instrument defects (`corpus/lessons/round-47.md` `## Routed defects`):

- `R46-CL7` (HIGH) the registry counter binds the digits 0/1/2, not their meanings: a row
  reading `0=banana; 1=nope; 2=whatever` scores met;
- `R47-CL10` (HIGH) both round-47 predicates are satisfiable by an artefact that does no
  work — the C1 side because four rows naming the wrong arm still pass, the C2 side because
  the record counter measures consistency, never completeness;
- `R47-CL1` both counters grade committed bytes but execute their own code from the
  worktree, so a replaced helper is an unexamined instrument;
- `R47-CL2` the `axes` class binds the leading fraction, not the 0–10 score cell beside it;
- `R47-CL13` a number the record quotes from its own receipt is never bound to that receipt;
- `R47-CL14` an `axes` correction line is silently inert (the grammar parses only
  `seats`, `window`, `path`, `rev`).

## R48-C1 — predicate (frozen)

`tools/round-48/meanings.py --root <LANE> --freeze <F> --rev <REV>` exits 0 **iff every
clause below is true**, and 1 otherwise, naming each false clause in `failing`:

1. the marker `<!-- verdict-meaning-table v1 -->` occurs exactly once and marks exactly one
   craft rule block; that block is the last craft block and its title starts `25. `;
2. the block's table header is exactly `trigger | v1 hole | v2 arm | exit`, it has exactly
   two data rows of exactly four cells, and every exit cell is in `{0,1,2}`;
3. each row names exactly one routed id, the multiset over the rows is exactly
   `{R46-CL7, R47-CL10}` once each, and **the row's arm cell equals the arm expected for its
   routed id** (`EXPECTED_ARM = {R46-CL7: meaning, R47-CL10: floor}`) — the R47-CL10
   permutation hole;
4. every arm cell is exactly one of `meaning`, `floor`;
5. `mutations_sha256` in the block equals sha256 over each mutation's **name and its own
   source body**, in list order, and all four mutation names appear in the block (R47-CL4);
6. `interpreter_sha256` equals sha256 of `tools/round-48/meanings.py` at `--rev`;
7. the block carries ≥5 resolving path citations inside
   `corpus/lessons/ | corpus/knowledge/ | plans/ | tools/round-48/`, each with a line
   selector, including `corpus/lessons/round-47.md` and at least one `corpus/knowledge/`
   entry (QUALITY row 77(a));
8. **registry meaning binding (R46-CL7).** The marker-bound registry section's rows are
   exactly the `tools/round-48/census2.json` path set (no duplicate, no missing, no extra);
   the committed `census2.json` equals a fresh derivation of its own rule at `--rev`; and
   every row's verdict map splits into three `N=meaning` segments whose meanings carry the
   class their digit claims — exit 0 a success class, exit 1 a not-met class, exit 2 an
   unevaluable class — the three segments distinct, and no placeholder text;
9. **battery.** On the artefact at `--rev` the counter must score `forgeries_total 4`,
   `v2_green 4` (the ported round-46/47 semantics accept every forgery), `v3_green 0`,
   `genuine_green 1`, `crash 0`.

The four forgeries are the counter's own `MUTATIONS`: `gold-meaning` (every verdict cell
replaced by `0=banana; 1=nope; 2=whatever`), `swapped-meaning` (exit 0 and exit 2 texts
swapped), `duplicate-meaning` (exit 1 text replaced by the exit 0 text), `permuted-arm`
(the two block rows' arm cells swapped).

**Kill rule.** If any forgery scores green under `--profile v3`, the claim is not met,
whatever the genuine artefact does.

## R48-C2 — predicate (frozen)

`tools/round-48/record2.py --root <LANE> --freeze <F> --rev <REV>` exits 0 **iff**:

1. the **oracle** — `tools/round-47/record.py` executed from the bytes at `--rev`, never
   from the worktree — accepts the card (`mismatches []`, `met_target true`), i.e. every
   atom the round-47 counter re-derives still re-derives;
2. **completeness floor (R47-CL10 C2 side).** For each of the last two `## Round N`
   sections: ≥1 seat atom **or** a re-derived `seats` correction for that round; ≥1 `path`
   atom; ≥1 `rev` atom; ≥1 claim id `R\d\d-C\d`. Claim ids are unique across the two
   sections. The `## Owned axes` head yields ≥2 `axes` atoms;
3. **corrections.** `## Record corrections — round 48` exists and every line re-derives —
   `seats`, `window`, `path`, `rev` through the round-47 oracle's own `corrects()`,
   `axes` against the card's Owned-axes rows (R47-CL14), and `quote` against the receipt
   the corrected section cites;
4. **quoted numbers (R47-CL13).** Every `atoms|exempted|corrections|mismatches N` quoted
   inside a round section is backed either by a receipt that section cites (the receipt's
   own cell for that key equals N) or by a re-derived `quote` correction for that round;
5. **Owned-axes score cell (R47-CL2).** For the `coverage` and `depth` rows the second
   number of the score cell equals `round(10 * n / d, 2)` for the first `n/d` fraction in
   that row;
6. **battery.** `forgeries_total 5`, `v2_green 5` (the round-47 semantics accept every
   forgery), `v3_green 0`, `genuine_green 1`, `crash 0`.

The five forgeries are `gold-tautology` (both round sections replaced by tautologies that
keep only the seat and window atoms), `seats-moved` (the seat total moved into the older
section only), `quote-off-by-one` (a quoted receipt number incremented), `axes-score-cell-off`
(the current score cell decremented), `axes-correction-forged` (an `axes` correction stating
`999/999`).

**Kill rule.** If any forgery scores green under `--profile v3`, the claim is not met.

## Causal separability

R48-C1's counter reads `SKILL.md`, `tools/round-48/census2.json` and `tools/round-48/`;
it never reads `SCORECARD.md`. R48-C2's counter reads `SCORECARD.md`, the round-47 oracle's
committed bytes, the `.ufo/waves/round-*/` dispatch files and receipts; it never reads the
craft section. Either lands and scores without the other. They share `tools/round-46/gate.py`,
frozen infrastructure from round 46, not a claimed surface.

## Frozen paths (exact)

- `plans/round-48-claims.md`
- `tools/round-48/`

## Landing requirement (frozen, so the counters can be green)

- `SKILL.md` gains craft rule block 25 (marker `<!-- verdict-meaning-table v1 -->`, two
  rows, the pins of clauses 5–6, the citations of clause 7).
- The instrument-registry section gains a row for each `tools/round-48/` path in the census
  and repairs every verdict map that does not carry its meaning class.
- `SCORECARD.md` gains `## Round 48 — …`, `## Record corrections — round 48` (a re-derived
  `seats` correction for round 47, a re-derived `quote` correction for round 47's
  `exempted` cell) and the Owned-axes head updates for this round.

## Freeze amendment A1 (disclosed; declared before any claim data)

The first freeze `7fe11332781356ec3d5b0b314698de27dd25b50d` carried a vacuous clause:
`record2.axis_scores()` read the *evidence* cell where it meant the *score* cell, so
clause 5 scored nothing — `axis_score_cells {}` with `axis_score_bad []` on the freeze
card, which is a green clause over zero rows (the same "measures consistency, never
completeness" class this claim exists to close). Red-before:
`.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json` (`axis_score_cells {}`).
A1 changes that parser to `cell[0]` and nothing else; every clause, threshold, kill rule
and mutation is byte-identical to the first freeze. **The declared freeze is the commit
that carries this paragraph**, i.e. the first commit whose `record2.py` scores the two
Owned-axes score cells. No seat had scored a claim and no landing had been measured when
A1 was made.

## Freeze amendment A2 (disclosed; declared before any claim data)

A1's counter still carried a false-red: the exit-0 classifier required a success token
**and** the absence of any not-met token, so the legitimate row
`tools/round-47/exact.py` (`0=met with failing empty; …`) was scored as naming no
success meaning — the word `failing` in the prose tripped the guard. Requiring an edit
there would force dishonest prose, which is the opposite of the claim. Red-before: the
row list above (16 rows at the A1 bytes; that row is among them only because of the
guard). A2 drops the guard and nothing else: a swap is still caught because the exit-0
segment then carries the exit-2 text and no success token. **The declared freeze is the
commit that carries this paragraph.** No seat had scored a claim and no landing had been
measured when A2 was made.

## Freeze amendment A3 (disclosed; declared before any claim data)

The census clause compared the freshly derived census **object** with the committed
`paths` **list**, so `census_rederived_equal` could never be true: a clause that fails by
construction on a correct artefact. It is unreachable while block 25 is absent (the
counter returns before the registry clauses), so no do-nothing control could show it; the
red-before is the pre-landing simulation at the A2 bytes
(`.ufo/waves/round-48/controls/ctl-c1-a3-simulation.json`, `failing` names
`committed census2.json does not equal a fresh derivation` on a registry whose path set
already equals the census). A3 compares `derived["paths"]` and nothing else. **The
declared freeze is the commit that carries this paragraph.** No seat had scored a claim
and no landing had been measured when A3 was made.

## Freeze amendment A4 (disclosed; two fixes of one class, declared before any claim data)

Two wave-1 attacks on the frozen bytes found checks that accept what they should reject,
both measured by the seats that found them:

- **C1Gold**: the exit-0 classifier matched `\bmet\b`, which also matches inside
  `not met`, so the map `0=not met; 1=violation; 2=usage` scored as success / not-met /
  unevaluable — a direct opposite-polarity false green. A4 requires the exit-0 segment to
  carry no `not met` / `no verdict` phrase.
- **CritAxis / CritSeparability**: `registry_rows()` recognised only rows whose stripped
  form starts `| \``, so a row written `|  \`path\`` was skipped by the path-set and
  meaning checks — the 0–3 leading-space class the census clause already rules out for
  ids. A4 parses any row whose pipe is followed by optional whitespace and fails closed
  on a row that does not have seven cells.

Two selftest cases are added (`red-opposite-polarity`, `red-hidden-row`); the predicate's
four forgeries, every clause, threshold and kill rule are unchanged. Red-before:
`w1/C1Gold.md` (the classifier counterexample, with the exact map) and `w1/CritAxis.md`
(the skipped-row counterexample). **The declared freeze is the commit that carries this
paragraph.**

## Freeze amendment A5 (disclosed; the instruments' own inputs, declared before any claim data)

The landing pre-flight on a scratch clone (not a claim measurement) found two ways an
instrument's *inputs* made a correct artefact red:

- **R48-C1 battery**: `_fixture_files` copied the claims file, the census and the block's
  citations but not the `plans/round-41..48-claims.md` files the census rule reads, so the
  battery's genuine score re-derived a shorter census and reported `genuine_green 0` on a
  landing that satisfies every clause. A5 adds the census's own input files to the fixture.
- **R48-C2 corrections**: the heading was matched with a substring split, and the round-48
  section quotes the heading in its claim table, so `corrections_section()` returned `[]`
  on a card that carries two correction lines. A5 anchors the heading to a whole line.

Red-before: the pre-flight receipts (`.ufo/waves/round-48/l1/scores/` preflight runs,
`battery genuine_green 0` and `no ## Record corrections — round 48 line re-derived` on a
card that carries both). **The declared freeze is the commit that carries this paragraph.**
No seat had scored a claim and no landing had been measured when A5 was made.

## Controls (not frozen; committed as wave evidence)

- `ctl-c1-0-do-nothing.json` — the counter at the freeze revision: block absent, registry
  meaning rows failing > 0.
- `ctl-c2-0-do-nothing.json` — the counter at the freeze revision: floor and quote clauses
  red; `--profile v2` green, which is the hole being closed.
- `ctl-c1-1-v2-profile.json`, `ctl-c2-1-v2-profile.json` — the ported profiles on the same
  revision, showing the forgeries green.
