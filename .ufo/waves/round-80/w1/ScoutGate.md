# ScoutGate — round 80 / w1 recon: the nine `validate_receipt()` clauses

Read-only reconnaissance. **No lane production file was written**; evidence is under
`.ufo/waves/round-80/w1/ScoutGate/`. Scratch: `/fast/scratch/hyaku/kaidoku-r80/ScoutGate/`
(created, used with `TMPDIR`, removed at exit).

Measured state: base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`, worktree `84d68e90f8a1ea3a3a7f94a208695c21023c0472`;
lane tree has no diff in the gate. `tools/round-78/attack-gate.py` sha256
`4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf` (974 lines), identical at base
(blob `5925deccb971bafb2957daac5f388a84d28b4be6`, `git cat-file -p 16dfa009:… | sha256sum`).

Method: three independent instruments, all in `ScoutGate/probe.py` (`probe-out.json` is its raw output):
(a) AST enumeration of the clauses and their enclosing `if`; (b) one single-statement `pass` mutant per
clause in scratch, each run as `python3 -I -B <copy> --selftest`; (c) an instrumented copy that appends
the clause index before each `defects.append`, plus nine crafted receipts checked against the pristine
module.

## 1. The nine clauses — count 9, source order (observed)

`defects: list[str] = []` is line 779; the function spans 778–808. Two statements are two-line f-strings.

| id | lines | condition that fires it | message literal | frozen prefix |
|---|---|---|---|---|
| G01-duplicate-fixture-id | 782 | `len(ids) != len(set(ids))` | `duplicate fixture id` | `duplicate fixture id` |
| G02-fixture-id-set | 785–786 | `set(ids) != declared` | `fixture ids {…} differ from the declared set` | `fixture ids` |
| G03-fixture-dir-mismatch | 790 | `fixture.get("fixture") != next(a["fixture"] …)` | `{id}: fixture dir mismatch` | `: fixture dir mismatch` |
| G04-base-accepted-not-bool | 792 | `not isinstance((fixture.get("base") or {}).get("accepted"), bool)` | `{id}: base.accepted is not a bool` | `: base.accepted is not a bool` |
| G05-refused-without-reason | 794 | `fixture.get("refused") and not fixture.get("reasons")` | `{id}: refused without a reason` | `: refused without a reason` |
| G06-refused-other-rule | 797–798 | `reason.get("rule") != fixture.get("rule")` (inside `for reason in fixture.get("reasons")`) | `{id}: refused by {rule}, not its declared rule` | `: refused by ` |
| G07-base-accepted-count | 801 | `receipt.get("base_accepted") != sum(1 for f in fixtures if (f.get("base") or {}).get("accepted"))` | `base_accepted does not re-derive from the fixture list` | `base_accepted does not re-derive` |
| G08-refused-count | 804 | `receipt.get("refused") != sum(1 for f in fixtures if f.get("refused"))` | `refused does not re-derive from the fixture list` | `refused does not re-derive` |
| G09-instrument-digest | 807 | `inst.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes())` | `instrument sha256 is not this file's digest` | `instrument sha256 is not` |

All nine frozen prefixes occur verbatim in their literal (`declared_prefix_in_literal: true` for 9/9).
`ATTACKS` has **10** rows (a1–a6, b1–b4); `receipt["fixtures"]` is expected to carry all ten.

## 2. Which selftest cases reach a clause (observed)

- Exactly **one** case syntactically calls `validate_receipt`: `red-validate-refused-no-reason`
  (line 921, `validate_receipt(no_reason)["defects"]`). No other `case(...)` expression calls it, and
  `battery()` (the only other caller, line 767) is not exercised by `--selftest`.
- The instrumented pristine run records **only clause 5 firing**. So:

| clause | reaching cases | reached incidentally | pinned |
|---|---|---|---|
| G05 | `red-validate-refused-no-reason` | no | **yes** |
| G01,G02,G03,G04,G06,G07,G08,G09 | none | — | **no** |

- Derived from the one case's receipt (not instrumented): conditions 1–4, 7–9 are evaluated **false**;
  clause 6's loop body is never entered (`reasons` is empty everywhere). The eight clauses are not
  "reached incidentally" — they are unexercised.

## 3. Independent deletion tally (observed)

Single `pass` substitution at the exact AST span; every mutant differs from base by exactly that one
statement (the two two-line f-strings collapse to a single `pass` line; the rest are 1:1); every mutant prints
`SELFTEST cases=29` — the cases are present, they simply do not change verdict.

| clause | exit | failures | failing cases | killed |
|---|---|---|---|---|
| G01–G04, G06–G09 | 0 | 0 | — | no (survivor ×8) |
| G05 `: refused without a reason` | **1** | **1** | `red-validate-refused-no-reason` | **yes** |

`got: []`, `want: ["receipt-unauth: refused without a reason"]`. Result: **9 clauses, 8 survivors,
1 killed** — exactly the ticket's expected base shape, **no deviation**. Reproduce:
`ScoutGate/probe.py` (mutants are generated in scratch from the gate, never committed).

## 4. Pristine arm (observed)

`python3 -I -B tools/round-78/attack-gate.py --selftest` → **`SELFTEST cases=29 failures=0`, exit 0**,
no stderr. Gate sha256 `4e4baf00…d2bf` (worktree == base blob).

Cross-check against the frozen target: `pristine.cases 37 − 29 = 8` = the number of surviving clauses,
and the L1 guard-table draft names exactly 8 new cases plus the existing G05 case. The arithmetic is
consistent; none of the eight new case names exists at base (grep count 0 each).

## 5. Findings that constrain how the battery/cases must be written

1. **Four "prefixes" are not prefixes of the emitted message** (G03–G06). Emitted examples:
   `receipt-unauth: fixture dir mismatch`, `receipt-unauth: base.accepted is not a bool`,
   `receipt-unauth: refused without a reason`,
   `receipt-unauth: refused by not_the_declared_rule, not its declared rule`.
   `defect.startswith(prefix)` binds **5/9**; substring (segment) matching binds **9/9**. G06's prefix
   ends in a significant space (`": refused by "`), so `strip()`-normalised comparison loses it.
   The table's third column should be treated as the clause's *literal segment*, matched against the
   f-string's literal part (or `in` the emitted defect), never as `startswith` on the message.
2. **Draft block contains 11 pipe-rows inside the markers**: header (`| clause | exact trigger |
   message fragment | declared case |`), separator (`|---…|`), then 9 data rows. A parser that treats
   every pipe-row as a data row reports `rows 11` and two orphan rows → the frozen kill rule. The
   parser must skip rows whose first cell is not `G\d\d-`.
3. **All nine clauses are independently fireable with exactly one defect each** (`fireability`, 9/9,
   `defect_count 1`). The constructions are in `probe-out.json`; they are ready-made isolating
   receipts: all ten declared fixtures, then one delta — duplicate `ATTACKS[0]` entry with
   `base_accepted 11`; drop `ATTACKS[0]`; wrong `fixture` dir; `base.accepted="yes"`; `refused` +
   `reasons []` + `refused 1`; `refused` + `reasons [{"rule": "not_the_declared_rule"}]`; `base_accepted
   9`; `refused 1`; `instrument.sha256 = "0"*64`.
4. **Case assertions must be exact.** Any new case that asserts "defects non-empty" instead of the
   exact one-element list stays green when its clause is deleted (a co-firing or later clause keeps the
   list non-empty) and would score as a survivor.
5. **`survivors 9` at base is not the raw tally.** With no rows the battery has no declared case per
   clause, so all nine count as survivors even though G05 is already killed by an existing case. The
   claim's base arm (9) and this tally (8) are consistent; do not "fix" one to match the other.

## 6. Provenance discrepancy in R80-C3's Type sentence (observed; flag for L1)

R80-C3 says "the round-79 mutation-tester proved three of the round-78 attack gate's
`validate_receipt()` refusal clauses survive deletion … (`gm-f`, `gm-g`, `gm-h`)". The artifacts:

- `.ufo/waves/round-79/w1/MutInstruments/receipt.json` pins its instruments to
  `tools/round-79/gate-mutation.py` (`682f1e78…`) and `tools/round-79/pointer-bind.py` (`91d23dad…`).
  The three survivors are mutants of **`tools/round-79/gate-mutation.py`** (diff header
  `--- tools/round-79/gate-mutation.py@ed68cd0a6cc7`), and their `declared_case` is `null`. They are a
  *different* `validate_receipt()` (mutation-battery receipt schema: `: no declared case`,
  `: killed without its declared case failing`, `pristine.ok with nonzero failures`,
  `: killed without an applied edit`). The string `tools/round-78` does not occur in that receipt.
- The only recorded mutant of the round-78 gate's clauses is
  `.ufo/waves/round-78/w1/MutGate/mutation-receipt.json` `m08-validate-no-refusal-guard`
  ("validate_receipt skips the refused-without-reason guard"), a survivor at rev
  `c9d986eb…`/sha `961d5a23…` — i.e. **one** clause, since killed at base by
  `red-validate-refused-no-reason`.

So the claim's number three is a different instrument's survivor count; at base the round-78 gate has
**eight** unpinned clauses. The frozen predicate (`guards 9 … survivors 0`, `pristine.cases 37`) is
unaffected and measurable; only the provenance sentence is not re-derivable from the cited receipt.
Claims are frozen — this is recorded, not amended.

## 7. What the surface misses (unknowns)

- `tools/round-80/guard-battery.py` does not exist at base (`tools/round-80/` absent from the tracked
  tree), so the claim's base arm cannot be reproduced by running the battery at `16dfa009`; §8
  re-derives its numbers with the untracked copy's pure functions, but the CLI arm itself remains
  unreproducible at base until the battery lands.
- The frozen row contract does not say whether header/separator pipe-rows count. The in-flight battery
  skips both (§8); an implementation that instead treats every pipe-row as a data row would report
  `rows 11` and two orphan rows. Reading the contract as "data rows only" is the only reading that
  reaches `rows 9` with the L1 draft as written.
- `SKILL.md` at base carries **0** occurrences of the two markers, so `rows 0` is consistent.

## 8. Cross-check against the in-flight battery (observed; untracked, not a deliverable)

`tools/round-80/guard-battery.py` appeared in the lane during this seat (untracked, another seat's
in-flight file; sha256 `b9b3b10c41a329f18ff5b39a4f546875101285ee97d2385de6c36ac84c508272` at observation
time). Imported read-only and called on the gate and on `.ufo/waves/round-80/l1/guard-table-draft.md`:

- `enumerate_clauses` → `guards 9`. It walks only `validate_receipt` and keeps `defects.append`
  expressions, matching §1.
- `parse_table(draft)` → `rows 9`, `table_defects []`: the header and separator are skipped
  (`clause_id.lower() in ("clause", "clause id")`; `set(line) <= set("|-: ")`), so F8 is already handled.
- `bind` → `bound 1` at base: only G05 binds (`red-validate-refused-no-reason`); the eight remaining
  rows fail with "case … is absent from the gate's selftest", naming exactly the eight cases to write.
  Binding is by `row["fragment"] in clause["message"]` (segment, not `startswith`), so F6 is handled.
- No table block → `rows 0`, `bound 0`, nine unbound: the claim's base arm, re-derived with the
  battery's own functions rather than by reading its prose.
- `CASE_DEF = case\(\s*"([^"]+)"`: a new case must be declared as `case("…", …)` with double quotes or
  the binder reports it absent. `child_env` passes `TMPDIR = --work`; its `HOME` fallback to `/tmp`
  only applies when `HOME` is unset and is not a write target — not a `/tmp`-hardcoding defect.

This does not change the measurements in §§1–4 (they read the tracked gate at base); it says the
in-flight implementation already matches the two conventions this recon derived.

## Evidence index

| path | content |
|---|---|
| `.ufo/waves/round-80/w1/ScoutGate/receipt.json` | acceptance receipt: `clauses` (line, literal, condition, reaching_cases, pinned), `deletion_tally`, `pristine`, `gate`, `fireability`, findings |
| `.ufo/waves/round-80/w1/ScoutGate/probe.py` | the recon driver (AST enumeration, mutant generator, trace, probes) |
| `.ufo/waves/round-80/w1/ScoutGate/probe-out.json` | raw driver output |

Tooling: nothing installed (no pacman transaction, no `~/.local/bin` write). No environment, token or
config value was captured; the only external reads are lane git objects (`cat-file`, `log`, `diff`).
