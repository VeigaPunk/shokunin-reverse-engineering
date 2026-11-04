source: S297 (Python `re` `\b` definition, snapshot line 747) for the delimiter rule; S049 (RFC 8259 section 4, held since round 21 — duplicate-name interoperability) for the duplicate-cell rule; S143 (Python `re` `re.fullmatch`, held since round 47) for equality-over-containment
verified-at: 2026-11-04
recheck: 180d

# Four bindings: an exact token, a unique cell, a committed blob, an isolating case

Round 79 left two rules about what evidence *names* (a pointer names its own line; a mutant names its
own detector). Round 80 is the same question asked four more times, and in each case the earlier
instrument tested **existence** where the property is **resolution**: a token occurred somewhere in
the line, a client key was present in the parsed map, a digest was present and well-formed, a clause
was present in the source. Each of the four rules below replaces that test with a resolution against
something the store can be asked to produce — a delimited occurrence, a cell count, a committed blob,
a case that fails when the clause is removed.

The three round-80 instruments are `tools/round-80/strictness-battery.py`, `tools/round-80/pointer-bind.py`,
`tools/round-80/receipt-provenance.py` and `tools/round-80/guard-battery.py`. Each is a capability
acquisition in the AXES sense: it runs, its output verifies, and its row enters the SCORECARD
capabilities table in the same round. The frozen fixture set is
`.ufo/waves/round-80/l1/fixtures/strictness.json` (schema `kaidoku-r80-strictness-fixtures-v1`,
base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`).

## 1. A pointer binds a token only when the token is delimited on both sides

**The rule.** A pointer binds only when every declared token occurs in the pointed lines as a
*delimited token*: each occurrence is delimited on both sides by start or end of line, or by a
character outside `[A-Za-z0-9._-]`. A pointer with an occurrence and no delimited occurrence is a
mismatch, and the refusal names the longer token the pin was hiding inside.

**What the substring rule did.** Round 79's `bind()` used `token in line`. The frozen set holds two
red fixtures of that defect and two green controls that a correct rule must still bind:

| case | pointed line | declared token | round-79 substring rule | round-80 delimited rule |
|---|---|---|---|---|
| rb01 | `  "rea-agents@6.7.05",` | `rea-agents@6.7.0` | binds (false green) | refuses — the character after the token is `5`, inside the class |
| rb02 | `args = [ "-y", "rea-agents@6.7.00", "mcp" ]` | `rea-agents@6.7.0` | binds (false green) | refuses — the character after the token is `0`, inside the class |
| gr01 | `  "rea-agents@6.7.0",` | `rea-agents@6.7.0` | binds | binds — `"` on both sides |
| gr02 | `#!/bin/bash` / `export GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` | `GHIDRA_INSTALL_DIR=` | binds | binds — space before, `/` after, inside a two-line range |

The two refusals are one defect with different endings (`:05` and `:00`), so a rule that
special-cased either string would fail the other. **The green controls are the anti-degenerate
arm.** gr01 carries the *same declared token* as rb01 and rb02 in an exact-looking line, so an
implementation that refuses `rea-agents@6.7.0` outright passes all four reds and fails this control;
gr02 is also the only fixture that exercises a range, whose token sits on the second line.

**At base.** [observation] The round-79 binder scores the four red fixtures as four false greens
(both binds `matched=True`; both duplicate records `checks_total=5`, `duplicates=ABSENT`), recorded at
`.ufo/waves/round-80/w1/ScribeLesson/grounding/c1-base-arm.txt`; the frozen battery reproduces the
count as `candidate_false_greens 4` and the control as `control_false_greens 4`
(`plans/round-80-claims.md`; the target-arm counts are `pending the landing receipt`).

**Why `\b`, and why not `re.fullmatch`.** S143 already grounds the principle — a token clause needs
equality, not containment, "so a superstring like `order-ish` fails a `order` token test that
`re.search` would pass". But a pointed line is a whole JSON or shell line, which the token never
equals; `fullmatch` cannot express "the token occurs *inside* this line". S297 supplies that scoping:
a `\b` match sits at the beginning or end of a word, formally "the boundary between a `\w` and a `\W`
character (or vice versa), or between `\w` and the beginning or end of the string". The lane keeps
the *shape* of that boundary and pins its own alphabet — ASCII `[A-Za-z0-9._-]`, narrower than `\w`
and adding `.` and `-` — so the source grounds the delimiter idea, not the exact class.

**The trap this class sets.** The token itself contains `@`, which is *outside* the class. The rule
tests the characters immediately before and after an occurrence, never the token's own characters; a
reading that required every token character to be a class character would refuse every real pin. The
refusal diagnostic widens the class to `[A-Za-z0-9._-@]` only to report the longer token whole
(`rea-agents@6.7.05`, not `6.7.05`).

## 2. A record may declare a client cell once, and every declaration is counted

**The rule.** A record that declares the same client cell twice is a duplicate defect. Every declared
cell is counted, so `checks_total` includes both; the receipt carries the check id in `duplicates`;
`ok` is false while `duplicates` is non-empty. No suppression, no last-wins collapse.

**What a collapsing parser loses.** Round 79's `parse_record()` built its map with
`pins = {name: (pin, pointer) for name, pin, pointer in RE_PIN.findall(text)}` — one entry per client
name, so the second declaration overwrote the first *before* any check was built. On both duplicate
fixtures the round-79 receipt reports `checks_total 5` with `duplicates=ABSENT`
(`.ufo/waves/round-80/w1/ScribeLesson/grounding/c1-base-arm.txt`; the two rows read
`ids=['devin-pin','omp-pin','kimi-pin','ghidra-version','bashrc-exports']`). The fixture appends a
cell with the *same* pin, so no token is lost — what disappears is the **count**: the record declared
OMP twice and the receipt said five checks. A reader that trusts the receipt has no way to see the
second declaration at all.

**Why the parser cannot be blamed.** RFC 8259 section 4 (S049): "The names within an object SHOULD be
unique", and where they are not, "the behavior of software that receives such an object is
unpredictable. Many implementations report the last name/value pair only." A last-wins dict is one of
the documented behaviours of a conforming reader, so no parse can be relied on to notice a duplicate;
the record layer must count declarations before it collapses them. The RFC's verb is SHOULD, not MUST:
it does not forbid the document, and the lane's refusal is its own policy — stricter than the grammar
(S049's teaches cell already records that distinction).

## 3. A receipt's instrument digest must name a committed blob

**The rule.** A receipt that declares `instrument.path` and `instrument.sha256` is provenance-bound
only when that digest equals a **committed blob** of that path: the blob at the receipt's declared
`rev` or `record.rev`, the blob at the lane branch tip, or a blob of that path at any committed
revision of the branch. A digest matching no committed blob is a defect. Working-tree bytes are not
committed, and a symbolic rev (`@HEAD@`, `main`) is not a committed revision.

**The worked failure.** [observation] `.ufo/waves/round-79/l1/scores/c2-at-landing.json` declares
`instrument.path "tools/round-79/pointer-bind.py"` with digest `a0044c4c5006ac0f…`; the committed
blobs of that path take only two values, `40905d396245313b…` and `91d23dade98d831f…`
(`for rev in $(git log --all --format=%H -- tools/round-79/pointer-bind.py); do git cat-file blob
"$rev:tools/round-79/pointer-bind.py" | sha256sum; done`). The recorded digest names nothing the
repository ever held, so the receipt cannot say which implementation produced its numbers.

**The declared control.** `prov-forged-instrument.json` (round 69) carries an all-zero digest
(`0000…`) and must stay flagged, so `flagged 0` is not the target and cannot be reached by refusing
everything. Its `instrument.rev` is present and well-formed: rev presence is not the discriminator,
digest-versus-blob is.

**At base.** [observation] `python3 -I -B tools/round-80/receipt-provenance.py --root . --rev
16dfa009bf143080dfcdfc5f9ec34bd359536d90 --from-round 60 --to-round 79` reports `receipts 34`,
`flagged 2`, `expected_control_flags 1`, `unexpected 1` with the unexpected flag naming
`.ufo/waves/round-79/l1/scores/c2-at-landing.json` and the expected control naming
`prov-forged-instrument.json` (`.ufo/waves/round-80/l1/scores/c2-at-base.json`). The target arm
(`flagged 1`, `unexpected 0`) is `pending the landing receipt`.

**The denominator is conditional.** [observation] Of the 141 `l1/scores/*.json` files in rounds
60–79 (excluding `/attacks/`), 34 declare an `instrument` block with both `path` and `sha256`
(`find .ufo/waves -type f -path '*/round-*/l1/scores/*.json'` filtered to rounds 60–79 and piped
through `json.load`; a seat-local count, not a lane receipt). So the rule quantifies over receipts
that declare an instrument, not over every JSON file in the directory: a receipt with no `instrument`
block cannot name an uncommitted digest.

## 4. A guard clause binds one table row and one isolating case

**The rule.** Each of the nine `defects.append` clauses of `tools/round-78/attack-gate.py`'s
`validate_receipt()` has exactly one row in the round-80 block of `SKILL.md` and exactly one declared
selftest case that is present in the gate's `--selftest` output and **fails** when the clause is
deleted from a copy at the measured revision. The binding is a bijection: no clause without a row, no
orphan row, no duplicate clause id, no two rows on one clause.

**The block contract.** The block is delimited by
`<!-- round-80 receipt-guard table: begin -->` and `<!-- round-80 receipt-guard table: end -->`, and
each row is exactly
`| G<NN>-<slug> | <exact trigger, prose> | <message prefix in backticks> | <case name in backticks> |`.
The nine prefixes, in source order, with the base-blob line of each clause:

| row | line | clause prefix | the receipt state that triggers it |
|---|---|---|---|
| G01 | 782 | `duplicate fixture id` | the `fixtures` list names the same id twice |
| G02 | 785 | `fixture ids` | the id set differs from the declared `ATTACKS` set |
| G03 | 790 | `: fixture dir mismatch` | a fixture's dir is not the declared dir |
| G04 | 792 | `: base.accepted is not a bool` | `base.accepted` is `"true"`, not `true` |
| G05 | 794 | `: refused without a reason` | `refused` is true and `reasons` is empty |
| G06 | 797 | `: refused by ` | a reason names a rule other than the fixture's |
| G07 | 801 | `base_accepted does not re-derive` | the count disagrees with the fixture list |
| G08 | 804 | `refused does not re-derive` | the count disagrees with the fixture list |
| G09 | 807 | `instrument sha256 is not` | the digest is not the gate file's own |

**An absent declared case is a survivor.** A case that is not in the mutant's `SELFTEST` output is
never a pass (round 79's rule), and a case that already fails on the pristine instrument is not
isolating. That is why the base arm reports `survivors 9` with `rows 0`: no row exists to declare any
case, so every clause is a survivor *by declaration*.

**Two base numbers, two different questions.** [observation] Deleting each clause from the pristine
29-case gate and running the gate's own selftest gives `mutants 9`, `killed 1` and `survivors 8`
(`.ufo/waves/round-80/w1/ReviewerC3/deletion-receipt.json`); the single killed clause is
`: refused without a reason`, caught by the one case that already existed,
`red-validate-refused-no-reason`. The frozen battery's `survivors 9` is not a contradiction: it counts
*declared* detectors, and at base nothing declares one. The gate therefore had exactly one behavioural
detector among nine clauses and no record that said so.

**After the eight new isolating cases.** [observation] The gate's selftest reports
`SELFTEST cases=37 failures=0` (`.ufo/waves/round-80/w1/ExecGate/selftest-pristine.json`; base blob
`git show 16dfa009…:tools/round-78/attack-gate.py | grep -c 'case("'` gives 29). Eight new cases plus
the pre-existing `red-validate-refused-no-reason` make nine declared cases for nine clauses, which is
why the target is `pristine.cases 37` and not 38. Whether each declared case isolates its clause is
proved by deletion, not by its name (`pending the landing receipt` for the battery's `bound 9`,
`survivors 0`, `target_pin.matched true`).

## What the four rules share

A name must resolve to a thing the store can produce. The token resolves to an occurrence with
boundaries; the cell resolves to one declaration before any collapse; the digest resolves to bytes a
commit holds; the clause resolves to a case that fails without it. In each case the cheap test —
substring, key membership, digest shape, clause text — is satisfiable by something that is not the
thing named, and the instrument that only asks the cheap question cannot fail. The round's own
instruments are the evidence: the base arms are green on the cheap test and red on the resolution, and
the transition is what enters the capabilities table.

## Limits

- **One delimiter alphabet.** The class is ASCII `[A-Za-z0-9._-]`; Python's `\b` is Unicode-aware by
  default, so the source grounds the boundary shape only. Non-ASCII neighbours, and tokens followed by
  `.` or `_` (both inside the class), are not fixture-covered: the frozen reds exercise digit
  suffixes only.
- **Six bind fixtures.** Four red and two green cannot cover every delimiter or every pointer shape;
  gr02 is the only range case, and no fixture places two declared tokens on one line.
- **Two duplicate clients.** OMP and Devin are both covered, so the rule is not a single-client
  special case; but the fixture appends the *same* pin, so two divergent declarations for one client
  are untested.
- **Provenance proves membership, not execution.** "Any committed revision of the branch" means a
  receipt whose instrument was legitimately amended later still binds to the older blob. The rule
  establishes that the digest was once committed, not that the run used those bytes; it cannot
  separate "edited after the receipt" from "forged before it" beyond blob membership.
- **One function's clauses.** The bijection covers the nine `validate_receipt()` clauses; the seven
  `defects.append` clauses elsewhere in the gate (lines 582–607) are untouched by R80-C3 and remain
  without declared isolating cases.
- **The table block was not yet in `SKILL.md` when this entry was drafted.** The row text exists as
  `.ufo/waves/round-80/w1/ExecGate/guard-table-draft.md`; the landed row count and the battery's
  binding are `pending the landing receipt`.

## Evidence

- Fixtures: `.ufo/waves/round-80/l1/fixtures/strictness.json` (`red_cases` 4, `green_cases` 2).
- C1 base behaviour: `.ufo/waves/round-80/w1/ScribeLesson/grounding/c1-base-arm.txt` (rb01/rb02
  `matched=True`; rb03/rb04 `checks_total=5`, `duplicates=ABSENT`).
- C1 predicate: `python3 -I -B tools/round-80/strictness-battery.py --root . --impl
  tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --fixtures
  .ufo/waves/round-80/l1/fixtures/strictness.json --json-out <receipt>`; live arm
  `python3 -I -B tools/round-80/pointer-bind.py --root . --rev <measured> --json-out <live>` — target
  counts `pending the landing receipt`.
- C2 base arm: `.ufo/waves/round-80/l1/scores/c2-at-base.json` (`receipts 34`, `flagged 2`,
  `expected_control_flags 1`, `unexpected 1`, `validate.defects []`).
- C3 deletion probe: `.ufo/waves/round-80/w1/ReviewerC3/deletion-receipt.json` (`mutants 9`,
  `killed 1`, `survivors 8`); pristine selftest:
  `.ufo/waves/round-80/w1/ExecGate/selftest-pristine.json` (`cases 37`, `failures 0`).
- C3 predicate: `python3 -I -B tools/round-80/guard-battery.py --root . --rev <measured> --json-out
  <receipt>` — `rows 9`, `bound 9`, `survivors 0`, `target_pin.matched true` are
  `pending the landing receipt`.
