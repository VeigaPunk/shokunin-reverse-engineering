# ExecGate — R80-C3 gate seat (candidate selftest cases + decision-table draft)

Role: executor. Base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`; declaration commit
`84d68e90` (lane HEAD when this seat ran; `tools/round-78/attack-gate.py` unchanged by it —
gate blob `a1f9b81c`). No lane production file was edited; every write is under
`.ufo/waves/round-80/w1/ExecGate/` plus this report.

## Deliverables

| path | what |
|---|---|
| `.ufo/waves/round-80/w1/ExecGate/attack-gate.py` | candidate gate: lane blob + exactly eight isolating `validate_receipt` cases (one hunk, +59/−0, sha256 `df6fb85670549ff1a03f925a3bed456cc3b64a311ae8681754c8efcc567149d6`) |
| `.ufo/waves/round-80/w1/ExecGate/guard-table-draft.md` | strict nine-row SKILL block between the frozen markers (no header/separator rows) |
| `.ufo/waves/round-80/w1/ExecGate/mutants.py` | per-clause mutation probe (AST-located `defects.append` spans) |
| `.ufo/waves/round-80/w1/ExecGate/mutants.json` | nine-mutant receipt + pristine tally + candidate digest |
| `.ufo/waves/round-80/w1/ExecGate/mutants/G0N-*.txt` | each mutant's full `--selftest` output |
| `.ufo/waves/round-80/w1/ExecGate/selftest-pristine.json` | pristine `--selftest` receipt (37 case names, exit, digest) |

Pristine tally of the candidate:

```
SELFTEST cases=37 failures=0        (exit 0; base 29 + 8 new)
sha256(df6fb856…)  candidate = lane blob + one insertion hunk
```

## The eight new cases (source order; G05 pre-existed)

Each forged receipt is built from the module's own `ATTACKS` table (no 10-item literal), is
healthy except for the one perturbation, and asserts the **whole** defect list, so a sibling
clause's message cannot keep it green:

| case | forged receipt | expected defects |
|---|---|---|
| `red-validate-duplicate-fixture-id` | first fixture cloned, counts +1 | `["duplicate fixture id"]` |
| `red-validate-fixture-id-set` | last `ATTACKS` entry dropped, counts −1 | `["fixture ids ['<dropped id>'] differ from the declared set"]` |
| `red-validate-fixture-dir` | first fixture's `fixture` dir moved | `["<id>: fixture dir mismatch"]` |
| `red-validate-base-accepted-bool` | first `base.accepted = "true"` (truthy, non-bool) | `["<id>: base.accepted is not a bool"]` |
| `red-validate-refused-other-rule` | first reason names `some_other_rule` | `["<id>: refused by some_other_rule, not its declared rule"]` |
| `red-validate-base-accepted-count` | `base_accepted = len(ATTACKS) - 1` | `["base_accepted does not re-derive from the fixture list"]` |
| `red-validate-refused-count` | `refused = len(ATTACKS) - 1` | `["refused does not re-derive from the fixture list"]` |
| `red-validate-instrument-digest` | `instrument.sha256 = "0"*64` | `["instrument sha256 is not this file's digest"]` |

`healthy()` computes `base_accepted`/`refused`/digest from the fixture list and
`pathlib.Path(__file__)`, so a mutant copy stays self-consistent and a different `ATTACKS`
set needs no edit.

## Nine-mutant table (`defects.append` → `pass`, one statement each)

Clauses located with `ast` inside `validate_receipt()`: exactly nine, distinct positions, each
spliced by source span and asserted unique (`text.count(stmt) == 1`). Every run printed
`SELFTEST cases=37`; only the declared case failed.

| clause | stmt line | declared case | failing on mutant | isolating |
|---|---|---|---|---|
| G01-duplicate-fixture-id | 782 | `red-validate-duplicate-fixture-id` | same | yes |
| G02-fixture-id-set | 785–786 | `red-validate-fixture-id-set` | same | yes |
| G03-fixture-dir | 790 | `red-validate-fixture-dir` | same | yes |
| G04-base-accepted-bool | 792 | `red-validate-base-accepted-bool` | same | yes |
| G05-refused-no-reason | 794 | `red-validate-refused-no-reason` (pre-existing) | same | yes |
| G06-refused-other-rule | 797–798 | `red-validate-refused-other-rule` | same | yes |
| G07-base-accepted-count | 801 | `red-validate-base-accepted-count` | same | yes |
| G08-refused-count | 804 | `red-validate-refused-count` | same | yes |
| G09-instrument-digest | 807 | `red-validate-instrument-digest` | same | yes |

`bound 9`, `survivors []`, `pristine.cases 37`, `pristine.failures 0`.
Pre-existing case G05 is also isolating, so the frozen bijection now has one case per clause
(8 new + 1 existing = 9) and one row per clause.

## Draft block (`guard-table-draft.md`)

```
<!-- round-80 receipt-guard table: begin -->
| G01-duplicate-fixture-id | the receipt's `fixtures` list names the same fixture id more than once | `duplicate fixture id` | `red-validate-duplicate-fixture-id` |
| G02-fixture-id-set | the receipt's fixture id set differs from the declared `ATTACKS` id set | `fixture ids` | `red-validate-fixture-id-set` |
| G03-fixture-dir | a fixture's `fixture` dir differs from the declared dir for that id | `: fixture dir mismatch` | `red-validate-fixture-dir` |
| G04-base-accepted-bool | a fixture's `base.accepted` is not a bool | `: base.accepted is not a bool` | `red-validate-base-accepted-bool` |
| G05-refused-no-reason | a fixture is marked refused and carries no `reasons` | `: refused without a reason` | `red-validate-refused-no-reason` |
| G06-refused-other-rule | a refusal reason names a rule other than the fixture's declared `rule` | `: refused by ` | `red-validate-refused-other-rule` |
| G07-base-accepted-count | `base_accepted` does not equal the count of fixtures whose `base.accepted` is true | `base_accepted does not re-derive` | `red-validate-base-accepted-count` |
| G08-refused-count | `refused` does not equal the count of fixtures marked refused | `refused does not re-derive` | `red-validate-refused-count` |
| G09-instrument-digest | the receipt's `instrument.sha256` is not the digest of the gate file | `instrument sha256 is not` | `red-validate-instrument-digest` |
<!-- round-80 receipt-guard table: end -->
```

Re-derived check (own scratch script, not a shipped instrument): block splits to exactly
**9 rows × 4 cells**; every row's ordinal matches its source-order clause (`G01`…`G09`); every
backticked prefix is a literal prefix of the clause's message literal; every backticked case
name occurs as `case("<name>"` in the candidate source.

## Findings for the L1 / battery seat

1. **Header-row hazard in the pre-existing draft.** `.ufo/waves/round-80/l1/guard-table-draft.md`
   (another seat's, read-only for me) puts a header row `| clause | exact trigger | … |` and a
   `|---|` separator **inside** the markers. The frozen contract says each row is exactly
   `| G<NN>-<slug> | … |` and the target is `rows 9`; a parser that counts every pipe line
   inside the block reads 11 rows (two malformed). My draft is header-free so it parses as 9.
   If that file is the one that lands, either drop its header/separator or make the battery skip
   non-`G<NN>` rows explicitly.
2. **Slug text is unconstrained, the ordinal is the key.** The two drafts word G03/G04/G05 slugs
   differently (`fixture-dir` vs `fixture-dir-mismatch`, …). Binding uses `G<NN>` + prefix + case
   name, so either wording binds; only one draft may land or the block has 18 rows.
3. **Prefix derivation must join the constant fragments.** The clauses G03–G06 open with a
   formatted value, so the message literal that a prefix can bind to is
   `"".join(constant parts)`: `": fixture dir mismatch"`, `": base.accepted is not a bool"`,
   `": refused without a reason"`, `": refused by , not its declared rule"`. Comparing instead
   against the interpolated runtime message (`"<id>: fixture dir mismatch"`) cannot bind the
   frozen prefix `: fixture dir mismatch`; the battery must use the join-of-literals reading.
4. `--validate` on a healthy receipt still exits 0 with `{"defects": [], "fixtures": 10}`; the
   eight cases do not disturb the CLI path.
5. Untested here by design: `--battery` (needs committed attack fixtures and the lane tree); this
   seat's acceptance is `--selftest` only, and main/L1 owns the post-integration gate.

## Commands run (read-only over the lane; all mutants in scratch)

```
diff -u tools/round-78/attack-gate.py .ufo/waves/round-80/w1/ExecGate/attack-gate.py   # 1 hunk, +59/−0
TMPDIR=/fast/scratch/hyaku/kaidoku-r80/ExecGate python3 -I -B mutants.py attack-gate.py <scratch> <evidence>
python3 -I -B attack-gate.py --selftest                       # SELFTEST cases=37 failures=0, exit 0
python3 -I -B attack-gate.py --validate <healthy-receipt>     # exit 0, defects []
```

Scratch: one dir `/fast/scratch/hyaku/kaidoku-r80/ExecGate/` created, passed as both cwd and
`TMPDIR` to every subprocess, receipts copied into the evidence dir, then removed; no tool
hardcoded `/tmp`. No tool installed or upgraded (nothing was needed). No git/jj write, no
message to `agent://all`, no write outside this seat's evidence dir and this report.

## Risks

- The battery (`tools/round-80/guard-battery.py`) is another seat's deliverable and did not exist
  when this ran; binding is verified against its stated rules re-implemented locally, so a
  divergent battery reading (finding 1/3) is an integration risk, not a candidate defect.
- Landing moves the gate's `instrument.sha256` (the file's own digest changes); every receipt that
  pins the round-78 gate digest must be regenerated by the L1, which is R80-C2's surface.
- The candidate digest `df6fb856…` is the pin to compare after landing; any other byte change to
  the gate in the same landing invalidates it.
