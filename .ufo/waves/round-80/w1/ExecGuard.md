# ExecGuard — R80-C3 counter (`guard-battery.py`)

Seat: ExecGuard (w1, leaf). Evidence dir: `.ufo/waves/round-80/w1/ExecGuard/`.
Deliverable (candidate counter; `tools/round-80/guard-battery.py` is already
landed by the L1 with a different implementation — see §4 and §6):
`.ufo/waves/round-80/w1/ExecGuard/guard-battery.py`, 1083 lines,
sha256 `d97fcc6063f8587d76522e178b1b89ec550754c9c7614640f70b4eccec059c50`.

No lane production file was written and no git write was performed in the lane;
read-only `git log/show/rev-parse/status` only. No tools were installed
(PACMAN paused; nothing needed `uv`/`npx`/a release binary).

## 1. What the instrument does

`--battery` (also triggered by `--rev` alone, because the frozen predicate
passes no `--battery`):

1. **Clause enumeration** — parses `git show <rev>:tools/round-78/attack-gate.py`,
   walks `validate_receipt()`'s AST for every `Expr` whose call is
   `defects.append(...)`, sorts by `(lineno, col_offset)` (source order, not
   `ast.walk` order), and emits `G01`..`G09` with 1-based line, the message
   literal (the f-string's literal parts concatenated, holes elided), the
   stable leading literal, and the source segment. An empty clause set raises
   `Unevaluable` → exit 2 (empty-set gaming refused).
2. **Table parse** — the block between
   `<!-- round-80 receipt-guard table: begin -->` and
   `<!-- round-80 receipt-guard table: end -->` of `git show <rev>:SKILL.md`;
   rows are split on unescaped `|`, and each data row must have exactly four
   cells: `G<NN>-<slug>`, trigger prose, one backticked message prefix, one
   backticked case name. A separator row is skipped; a header/legend line with
   no backticked cell and no `G<NN>` first cell is recorded as ignored (so the
   gate seat's header + separator parse cleanly); a 3-cell row, a
   backtick-less message/case cell, or a `G`-prefixed id that is not
   `G<NN>-<slug>` is a named malformed-row defect. An absent block is
   `block_present: false, rows: 0` — the base state, not an error.
3. **Binding** — a clause is bound only when it is named by exactly one row,
   that row's prefix is a prefix of the clause's (hole-elided) message, the
   row's case name occurs as `case("<name>"` (or `case('<name>'`) in the gate's
   `selftest()` source, and no other row names the same clause id or the same
   case name. Orphan row, duplicate clause id, a prefix that prefixes no
   clause, a prefix that prefixes two clauses, a row whose prefix binds another
   clause, and a case named twice are each a named defect and bind nothing.
4. **Mutation** — for every clause (bound or not) the exact statement segment
   is located by line span, asserted to occur exactly once in the blob, and
   replaced by `pass` at the same indent. The copy is compiled in-process,
   then run as `python3 -I -B <copy> --selftest` under a four-key child
   environment (`HOME`, `LANG`, `PATH`, `TMPDIR`). `killed` requires the clause
   to be bound AND the declared case PRESENT in that output AND failing there;
   a non-compiling copy, a copy with no `SELFTEST` summary, an absent case, or
   a passing case is inconclusive/survived, never a kill. An unbound clause is
   always a survivor.
5. **Receipt** — `guards, rows, bound, killed, survivors, survivor_ids,
   pristine{cases,failures,case_names,failed_cases,ok}, target_pin{expected,
   actual,matched}, instrument{path,sha256}, rev, checked_at, clauses[],
   rows_detail[], table{block_present,ignored_lines}, guard_defects[], exit,
   ok`. `pristine.cases` is re-derived from the copy's own
   `SELFTEST cases=<n> failures=<m>` line and cross-checked against its case
   lines — no hardcoded number. `--rev` is resolved with
   `git rev-parse <rev>^{commit}` so the receipt carries a 40-hex commit and
   `--validate` can re-derive from the same blobs.
6. **`--validate`** re-enumerates the clauses and re-parses the SKILL block at
   `receipt.rev`, re-binds them, re-derives `guards/rows/bound/killed/
   survivors`, re-runs the gate's own `--selftest` for `pristine`, and checks
   `exit`/`ok`/`target_pin`/`pristine.ok` two-directionally.
7. **Exit** — 0 iff `guards>0 ∧ rows==guards ∧ bound==guards ∧ survivors==0 ∧
   pristine.failures==0`; 1 otherwise; 2 unevaluable. `ok` additionally
   requires `target_pin.matched` and no guard defects (the claim-level verdict).

## 2. Selftest

`python3 -I -B guard-battery.py --selftest` → `SELFTEST cases=33 failures=0`,
exit 0. Cases include every required one: unbound clause, orphan row,
malformed row, duplicate clause id, absent declared case, case passing on the
mutant, non-compiling mutant, empty clause set refused, summary-less copy
inconclusive, ambiguous prefix refused, plus header tolerance, typo'd row id,
escaped `|`, source ordering, hole-elided message, non-isolating case, and
three forged-receipt validator cases.

## 3. Base arm — the frozen do-nothing control

Runs at base `16dfa009` and, as a cross-check, at the declaration commit
`84d68e90` (same gate and SKILL blob):

```
python3 -I -B .ufo/waves/round-80/w1/ExecGuard/guard-battery.py --rev 16dfa009 \
  --expect-sha256 4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf \
  --json-out .ufo/waves/round-80/w1/ExecGuard/guard-battery-base.json
```

Both receipts: `guards 9`, `rows 0`, `bound 0`, `killed 0`, `survivors 9`
(`G01`..`G09`), `pristine.cases 29`, `pristine.failures 0`,
`target_pin.matched true`, `exit 1`, `guard_defects []`.
`--validate` on both is defect-free (exit 0).

**My reading equals the frozen expectation; there is no difference to report.**

Enumerated clauses, source order (line · frozen prefix · hole-elided message):

| id | line | prefix | message |
|---|---|---|---|
| G01 | 782 | `duplicate fixture id` | `duplicate fixture id` |
| G02 | 785 | `fixture ids ` | `fixture ids  differ from the declared set` |
| G03 | 790 | `: fixture dir mismatch` | `: fixture dir mismatch` |
| G04 | 792 | `: base.accepted is not a bool` | `: base.accepted is not a bool` |
| G05 | 794 | `: refused without a reason` | `: refused without a reason` |
| G06 | 797 | `: refused by ` | `: refused by , not its declared rule` |
| G07 | 801 | `base_accepted does not re-derive …` | `base_accepted does not re-derive from the fixture list` |
| G08 | 804 | `refused does not re-derive …` | `refused does not re-derive from the fixture list` |
| G09 | 807 | `instrument sha256 is not …` | `instrument sha256 is not this file's digest` |

All nine frozen prefixes are prefixes of the corresponding messages, in the
frozen source order. Note G05's clause is already isolated at base by the
pre-existing `red-validate-refused-no-reason` case (its deletion fails that
case), but with no row it is still a survivor — the binding, not the
detection, is what C3 buys.

## 4. Target arm — the landed gate and table

The gate seat's commit `b8260107` ("the gate's nine clauses get one isolating
case and a decision-table row each (37 cases)") landed the gate and the block;
the gate blob is unchanged at the current lane tip `b00419fb`. Measured at
`--rev HEAD`, resolved to `b00419fb8c3d083761034605fec2eed1897f60ad`
(gate blob sha256 `df6fb85670549ff1…`, 49314 bytes):

- `guards 9`, `rows 9`, `bound 9`, `killed 9`, `survivors 0`,
  `pristine.cases 37`, `pristine.failures 0`, `target_pin.matched true`,
  `exit 0`, `ok true`, `guard_defects []`; `--validate` defect-free.
- Per clause exactly one case fails on the mutant and it is the declared one:
  G01 `red-validate-duplicate-fixture-id`, G02 `red-validate-fixture-id-set`,
  G03 `red-validate-fixture-dir`, G04 `red-validate-base-accepted-bool`,
  G05 `red-validate-refused-no-reason`, G06 `red-validate-refused-other-rule`,
  G07 `red-validate-base-accepted-count`, G08 `red-validate-refused-count`,
  G09 `red-validate-instrument-digest`.
- `guard-battery-landing.json` is an **independent measurement of the landed
  pair** at `rev b00419fb…` with *this* candidate instrument. It is not a
  replacement landing receipt: `tools/round-80/guard-battery.py` is already
  landed (sha256 `b9b3b10c41a3…`, 544 lines) and its own
  `.ufo/waves/round-80/l1/scores/c3-at-landing.json` reports the same
  `guards 9 / rows 9 / bound 9 / survivors 0`. The two implementations agree on
  every count, which is the useful part of this arm.
- `pristine.cases 37 = 29 + 8`, not 29 + 9: the gate reuses the pre-existing
  case name `red-validate-refused-no-reason` for G05 (one occurrence in its
  selftest) instead of adding a ninth name, so the claim's 37 is arithmetically
  correct. The bijection is unaffected: nine rows, nine distinct case names,
  one case per clause.
- Before the gate landed, the same instrument was run on the gate seat's
  working copy in a scratch repo: byte-identical gate (`df6fb856…`), same
  numbers. That pre-landing receipt (`guard-battery-gate-candidate.json`,
  fixture rev `6f7d98b3…`) is retained as the prediction the landing confirmed.
- My own nine-new-name simulation (`guard-battery-sim-target.json`) reaches
  `pristine.cases 38` with the same full target shape; it exists only to show
  the counter is not tuned to one edit.

## 5. Negative control — the counter can fail

Same gate with two deliberately broken table rows (G03 prefix changed to
`no such prefix here`, G07 case changed to `red-nonexistent-case`):
`rows 9`, `bound 7`, `survivors 2` (`G03`, `G07`), `exit 1`, with the two
defects named:

```
row G03-fixture-dir-mismatch: prefix 'no such prefix here' prefixes no clause
row G07-base-accepted-rederive: declared case 'red-nonexistent-case' is absent from the gate's selftest source
```

The receipt is still internally consistent, so `--validate` passes (exit 0)
while the battery exits 1 — consistency is not the target.

## 6. Operator notes for the L1

- Both files must be **committed** before measuring: the instrument reads only
  `git show <rev>:…`, never the working tree. An uncommitted SKILL block
  measures as `rows 0`.
- Pass `--expect-sha256 <sha256 of the landed gate's bytes>`; it is optional and
  does not change `exit` (per the frozen exit rule), but `ok` and
  `target_pin.matched` require it. Use
  `git show <rev>:tools/round-78/attack-gate.py | sha256sum` — **not**
  `git rev-parse <rev>:<path>`, which returns the SHA-1 object id, not the
  content digest.
- `--work` is optional; when absent the battery creates its scratch under
  `$TMPDIR` and removes it. It never uses a bare `/tmp` path of its own.
- The battery validates `instrument.sha256` against its own bytes, so **any
  edit to the file invalidates every existing receipt** — land it verbatim
  (sha256 `d97fcc60…`) or regenerate all receipts.
- **Do not land this file at `tools/round-80/guard-battery.py`**: that path
  already carries the landed instrument (sha256 `b9b3b10c41a3…`), and
  overwriting it would invalidate `l1/scores/c3-at-landing.json` and break
  R80-C2's provenance check. If a second counter is wanted, land it at a
  distinct path (e.g. `tools/round-80/guard-battery-crosscheck.py`) in the same
  commit as its receipt; otherwise keep these receipts as evidence-dir
  cross-checks. `guard-battery-landing.json` must **not** be copied under
  `l1/scores/` as-is: its `instrument.sha256` is this candidate's digest, not
  the committed digest of `tools/round-80/guard-battery.py`.
- A row prefix is scored against the hole-elided message. A prefix written
  with the interpolation text (`{fixture.get('id')}`) will not bind.
- If the receipt is placed under `.ufo/waves/round-80/l1/scores/`, R80-C2's
  sweep will require its `instrument.sha256` to equal the committed blob of
  `tools/round-80/guard-battery.py` — land the file in the same commit as the
  receipt.

## 7. Files

| path | role |
|---|---|
| `guard-battery.py` | the candidate counter (land as `tools/round-80/guard-battery.py`) |
| `guard-battery-landing.json` | independent full-target measurement of the landed pair at `b00419fb` (cross-check, not a landing receipt) |
| `guard-battery-base.json` | base arm at `16dfa009` (lane-committed rev; re-validatable) |
| `guard-battery-declaration.json` | cross-check at `84d68e90` (same shape) |
| `guard-battery-gate-candidate.json` | target-arm prediction on the gate seat's candidate pair |
| `guard-battery-sim-target.json` | self-contained target simulation (38-case variant) |
| `guard-battery-negative.json` | negative control, two broken rows |
| `sim-target-SKILL-block.md` | the nine-row block as parsed and scored |
| `sim-target-selftest-cases.py.txt` | the nine isolating cases used by the simulation |

Scratch `/fast/scratch/hyaku/kaidoku-r80/ExecGuard/` (fixture repos, mutant
copies, work dirs) was removed after the receipts were copied here.

## 8. Risks / limits

- The clause enumeration is bound to `validate_receipt()`'s **statement shape**
  (`defects.append(...)`); a clause rewritten as `defects += [...]` or a local
  helper would drop out of the count (guards would fall, which the exit rule
  catches, but the row would become an orphan).
- The message literal is the concatenated literal parts, so a message whose
  leading text lives inside a hole (e.g. `f"{prefix} rest"`) has no stable
  leading literal and its row prefix must match the concatenated text.
- `--validate` re-runs the gate's own `--selftest`, so it needs the revision's
  blobs in `--root`. `guard-battery-landing.json` and the base/declaration
  receipts are lane-committed and re-validatable there; the fixture-rev
  receipts (sim/gate-candidate/negative) are only re-validatable while their
  scratch repo exists and are shipped as controls, not as landing receipts.
- The gate seat's re-use of the pre-existing case name for G05 means that row
  declares a case that is not new; it is still present-and-failing on the
  mutant, so it scores, but it does not add a ninth case (hence 37, not 38).
