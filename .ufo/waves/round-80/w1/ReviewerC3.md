# ReviewerC3 — R80-C3 independent re-derivation

Seat: `ReviewerC3` (reviewer, r80-w1). Lane `kaidoku-shokunin`, measured base
`16dfa009bf143080dfcdfc5f9ec34bd359536d90`, declaration commit
`84d68e90f8a1ea3a3a7f94a208695c21023c0472` (HEAD at my check; `tools/round-78/attack-gate.py`
and `SKILL.md` are byte-identical between the two). Python 3.14.8, every child run
`python3 -I -B … --selftest` under `{PATH, HOME, TMPDIR, LANG}` only.

I did not reuse ExecGate's parser or mutants. Enumeration is `ast.parse` over the blob at the
rev; mutation is a textual replacement of the one statement; scoring binds table rows to
clauses by the frozen prefixes.

## 1. The nine clauses at `16dfa009` (my enumeration)

Blob `5925decc…` (git), sha256 `4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf`.
The file carries 17 `defects.append` statements; nine are inside `validate_receipt()`
(lines 782, 785, 790, 792, 794, 797, 801, 804, 807), the other eight are in
`check_receipt_like()` and out of scope.

| n | line | message literal (template) | enclosing condition |
|---|---|---|---|
| 1 | 782 | `duplicate fixture id` | `len(ids) != len(set(ids))` |
| 2 | 785–786 | `fixture ids {sorted(set(ids) ^ declared)} differ from the declared set` | `set(ids) != declared` |
| 3 | 790 | `{id}: fixture dir mismatch` | `fixture["fixture"] != next(a["fixture"] …)` |
| 4 | 792 | `{id}: base.accepted is not a bool` | `not isinstance((fixture.get("base") or {}).get("accepted"), bool)` |
| 5 | 794 | `{id}: refused without a reason` | `fixture.get("refused") and not fixture.get("reasons")` |
| 6 | 797–798 | `{id}: refused by {reason["rule"]}, not its declared rule` | `reason.get("rule") != fixture.get("rule")` (inside `for reason in fixtures[i].reasons`) |
| 7 | 801 | `base_accepted does not re-derive from the fixture list` | `receipt["base_accepted"] != Σ fixtures with base.accepted` |
| 8 | 804 | `refused does not re-derive from the fixture list` | `receipt["refused"] != Σ fixtures refused` |
| 9 | 807 | `instrument sha256 is not this file's digest` | `inst["sha256"] != sha256(__file__)` |

Source order equals the frozen prefix order exactly. Full record with conditions:
`.ufo/waves/round-80/w1/ReviewerC3/clauses.json`.

## 2. Base deletion tally — confirmed, with one reading to fix

Nine mutants of the base blob (one statement → `pass` each), pristine `SELFTEST cases=29
failures=0`:

- **killed 1**: `: refused without a reason` (by `red-validate-refused-no-reason`);
- **survivors 8**: every other clause;
- unevaluable 0 (every mutant compiles and prints a summary).

That is the base shape I was asked to confirm. It does **not** contradict the claim's base arm
(`survivors 9`): the claim's `survivors` counts unbound clause→row pairs in the battery, mine
counts surviving mutants. All nine clauses are unbound at base because no table block exists;
eight of them also have no selftest case at all.

## 3. Candidate scoring

ExecGate's `attack-gate.py` (sha256 `df6fb85670549ff1a03f925a3bed456cc3b64a311ae8681754c8efcc567149d6`,
base + 60 lines = 8 new cases) and its `guard-table-draft.md`.

| arm | guards | rows | bound | survivors | pristine | strict-isolating | issues |
|---|---|---|---|---|---|---|---|
| draft block | 9 | 9 | **9** | **0** | **37 / 0** | 9 | none |
| my independent block | 9 | 9 | 9 | 0 | 37 / 0 | 9 | none |
| no block | 9 | 0 | **0** | **9** | 37 / 0 | 9 | — |

Per case (all nine, identical in both block arms): exists, passes pristine, dies on its own
mutant, and **passes on the other eight mutants** — the mutant × case matrix is exactly
diagonal, which is stronger than the frozen predicate demands. The draft block parses as nine
four-cell rows, `G01…G09-<slug>`, prefixes exactly the frozen nine, case names exactly the
37-case selftest population, no duplicate row id, no non-conforming row, no orphan clause.
`guards` re-derive to the same nine source lines `[782, 785, 790, 792, 794, 797, 801, 804, 807]`.

The candidate's own receipt agrees (`ok true`, `bound 9`, `survivors []`, pristine 37/0) but
that is not evidence for it; the table above is my run.

Not verifiable in this seat: `target_pin.matched` and the battery's `--validate`, because
`tools/round-80/guard-battery.py` does not exist yet. This report verifies the inputs those
fields must consume.

## 4. Binding attacks

### A. A row prefix that matches two clauses — conditional
G05's prefix rewritten to `` `: refused` `` (prefixes clauses 5 and 6), every case still real.

- total match + bijection: `bound 8`, issues `G05 matches [5,6]` and `clause 6 has two rows` → caught;
- first-match matcher: `bound 9`, `survivors 0`, no issue → **missed**.

The frozen text pins "exactly one row" per clause but never says what a prefix matching several
clauses means, so an implementation that resolves to the first match is faithful to the letter
and wrong in effect. Variant, same family: a substring *case-name* matcher would accept
`red-validate-base-accepted` against both `…-bool` and `…-count`; names must be compared exactly.

### B. A case that asserts a source literal — **missed**
Eight injected cases assert a clause's message text is present in `pathlib.Path(__file__)`
(needle split so the case body cannot satisfy it), clause 5 keeps the existing behaviour case,
the block names the injected cases. Result: `guards 9, rows 9, bound 9, survivors 0,
pristine 37/0`, and the same eight cases are cross-mutant exclusive. Every frozen count is met
by eight assertions that never call `validate_receipt`.

The discriminator the predicate lacks: per clause, replace the **enclosing `if` test with
`False`** and leave the message literal in the file. Behavioural cases go red; source-text cases
stay green. Measured: ExecGate candidate 9/9 behavioural; attack-B instrument 1/9 behavioural
(8 stay green). This single extra mutant separates the two classes and is cheap.

### C. A case that fails on everything — **missed**
One case (count of `defects.append` lines == 17) passes pristine and fails on all nine mutants;
seven pads bring the population to 37; the **same case is declared in all nine rows**. Result:
`bound 9, survivors 0, pristine 37/0`, `distinct_declared_cases 1`, strict-isolating 0.
A case that also fails on pristine *is* caught (`pristine.failures 0`); the pristine-green variant
is not. The frozen rule requires "exactly one declared selftest case" per clause but never says
the nine are distinct nor that a case must pass on its siblings' mutants.

### D. A clause merged into one `defects.append` — caught
Clauses 4 and 5 merged behind one `or` with one message: compiles, `guards 8`, pristine 29/1.
Caught twice — `guards 9` fails at 8, and the frozen kill rule explicitly forbids
`survivors 0` below nine guards. A refactor that kept nine statements but merged two conditions
also loses one frozen prefix, so `bound 9` fails. This holds only if the receipt prints the
source-derived guard list; a hardcoded 9 would hide it.

## 5. Findings, by severity

1. **F1 (contract, open).** The frozen prefixes for clauses 3–6 are not prefixes of the message
   literal: those literals begin with the fixture-id placeholder, the prefixes begin at `: `.
   `template.startswith(prefix)` binds zero of them, and matching the *rendered* message (which
   starts with the id) binds zero as well. The only consistent reading is *the literal text after
   the leading `{…}` placeholder*. The draft block uses exactly the frozen strings, so the intent
   is clear, but the rule is unwritten; the gate seat and the battery seat must implement the
   same canonicalization or `rows`/`bound` diverge with both sides faithful.
2. **F2 (high, open).** Attack B lands on every frozen count. Add the condition-disabled mutant
   to the battery and require the declared case to fail there as well.
3. **F3 (high, open).** Attack C lands: one case in nine rows. Require nine distinct declared
   case names and, per clause, the case to pass on the other eight mutants.
4. **F4 (medium, conditional).** Attack A is caught only under total matching plus the bijection;
   make "prefix matches more than one clause" an explicit receipt defect and compare case names
   exactly.
5. **F5 (low, closed).** Attack D is caught by `guards 9` and the empty-set kill rule, given a
   source-derived guard list.
6. **F6 (medium, open).** `tools/round-80/guard-battery.py` absent at my check; `target_pin` and
   `--validate` are unverified here.
7. **F7 (low, note).** ExecGate's `selftest-pristine.json` names `tools/round-78/attack-gate.py`
   with the candidate digest `df6fb856…`. It is provenance-true only after the candidate lands at
   that path; it must not be filed into `l1/scores/` before then (R80-C2's class).

## 6. Residual risk and verification gaps

- My clause→prefix canonicalization is a reading, not a quotation (F1). If the landed battery
  reads the frozen prefixes differently, its `rows`/`bound` will differ from this receipt with no
  defect on either side; the L1 should pin the reading in the battery's docstring.
- F2/F3 are strengthenings beyond the frozen predicate. They do not block the frozen target, but
  without them the target is reachable by eight vacuous assertions or by one case.
- `target_pin.matched`, the battery's `--validate`, and the landed `SKILL.md` block position are
  unverified: the battery does not exist yet and the block is still a seat draft, not a lane file.

## 7. Artefacts and reproduction

All under `.ufo/waves/round-80/w1/ReviewerC3/`: `receipt.json` (machine receipt),
`clauses.json`, `deletion-driver.py` + `deletion-receipt.json` +
`deletion-receipt-candidate.json`, `binding-lab.py` +
`score-execgate-{draft-block,with-block,noblock}.json` + `attack-receipt.json` +
`discriminate-{execgate,atk-b,atk-c}.json`, `candidate-block-reviewer.md`,
`declare-execgate.json`. Scratch `/fast/scratch/hyaku/kaidoku-r80/ReviewerC3/` was created for
this seat and removed before the report was filed; receipts were copied first.

```sh
TMPDIR=<scratch> python3 -I -B .ufo/waves/round-80/w1/ReviewerC3/deletion-driver.py \
  --root <lane> --rev 16dfa009 --work <scratch>/del --json-out <ev>/deletion-receipt.json
TMPDIR=<scratch> python3 -I -B .ufo/waves/round-80/w1/ReviewerC3/binding-lab.py score \
  --gate .ufo/waves/round-80/w1/ExecGate/attack-gate.py \
  --block .ufo/waves/round-80/w1/ExecGate/guard-table-draft.md --work <scratch>/s
TMPDIR=<scratch> python3 -I -B .ufo/waves/round-80/w1/ReviewerC3/binding-lab.py attacks \
  --gate <base-blob> --candidate-gate .ufo/waves/round-80/w1/ExecGate/attack-gate.py --work <scratch>/a
TMPDIR=<scratch> python3 -I -B .ufo/waves/round-80/w1/ReviewerC3/binding-lab.py discriminate \
  --gate .ufo/waves/round-80/w1/ExecGate/attack-gate.py \
  --block .ufo/waves/round-80/w1/ExecGate/guard-table-draft.md --work <scratch>/d
```

No lane production file was written. No `git` mutation was run. No `/tmp` use; ExecGate's tools
take `--work` and its only `/tmp` mention is a docstring saying not to default there.
