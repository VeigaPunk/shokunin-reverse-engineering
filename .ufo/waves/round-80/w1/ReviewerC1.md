# ReviewerC1 — R80-C1 independent re-derivation

Seat: ReviewerC1 (reviewer, leaf). Round 80, wave w1. Scored at 2026-11-04.
Scope: R80-C1 only (calibration: strict pointer binding + duplicate-cell rule). No lane
production file was edited. Writes are under `.ufo/waves/round-80/w1/ReviewerC1/` plus this
report. Scratch lived at `/fast/scratch/hyaku/kaidoku-r80/ReviewerC1/` and was removed after the
receipts were copied.

## Verdict

**The frozen R80-C1 predicate passes on the landed canonical instrument** (exact command and
numbers in §3): `cases 4`, `green_cases 2`, `candidate_false_greens 0`, `control_false_greens 4`,
`candidate_green_refusals 0`, `control_green_refusals 0`, `ok true`, `--validate` defects `[]`; the
base arm reports `candidate_false_greens 4`; the live arm exits 0 with `checks_total 5`,
`matched 5`, `mismatches 0`, `unparsed 0`, `duplicates []`, `--validate` defects `[]`.

**But the counter under-enforces the frozen duplicate rule, and the landed binder has a latent
duplicate-cell defect.** Two executable counterexamples (§6) each violate one half of the rule and
still score `ok true`; the landed canonical itself binds only 1 of 2 duplicate cells per record
(§7). So the claim is true of the landed bytes, not established by the battery alone. Details in
the findings.

## 1. Frozen inputs (verified, not assumed)

| Item | Value |
|---|---|
| Base | `16dfa009bf143080dfcdfc5f9ec34bd359536d90` |
| Fixture declaration commit | `84d68e90f8a1ea3a3a7f94a208695c21023c0472` (`plans/round-80-claims.md` and the fixture share it) |
| Fixture file | `.ufo/waves/round-80/l1/fixtures/strictness.json` |
| Fixture sha256 | `40f99456aff65f5b8b1ee7098820b2086499ae0c62b372d575f5f09d34510feb` |
| Committed blob = worktree | true (`git show 84d68e90:…/strictness.json` hashes to the same digest) |
| Shape | 4 red (2 `bind`, 2 `record`), 2 green (`bind`); ids unique; `base` field = declared base |
| HEAD while scoring | `b00419fb…` (the L1 advanced `253fc817` → `b8260107` → `b00419fb` for C2/C3; the fixture commit and digest did not change) |

`declaration_is_head` is now false by design: the lane moved after the declaration, but the
declaration commit is still in history and the fixture bytes are unchanged.

## 2. Method (independent)

Own scorer: `.ufo/waves/round-80/w1/ReviewerC1/reviewer-strictness.py`. No executor driver,
battery or fixture runner is imported into it. It loads each module by path with
`importlib.util.spec_from_file_location` and:

- `bind` cases: calls `bind(pointer, tokens, lines)` with the frozen lines.
- `record` cases: creates a throw-away git repo under scratch (`PROVINCE.md` =
  `record_template` + `append_cell`, committed), asserts the repo toplevel equals the fixture dir,
  then calls `battery(repo, "HEAD", None)`.
- Implements ReviewerC1's own both-sides-delimited reference rule, the degenerate models, a
  template-only record baseline, weak-rule probes, and the live arm by subprocess.

I also ran the landed canonical counter exactly as the claim states and validated its receipt.

## 3. Implementations scored (bytes)

| Arm | Path | sha256 |
|---|---|---|
| Control (round 79) | `tools/round-79/pointer-bind.py` | `40905d396245313bedb7d0ae25b63f322b39e8e877371630e84d7616f12cb877` |
| **Landed canonical (C1 target)** | `tools/round-80/pointer-bind.py` | `2e4a7852c791862b2e0626b07803f6250f189d95c4234d14dcfb35800b1f5c01` |
| Counter instrument | `tools/round-80/strictness-battery.py` | `2b26d75a1277fbc57bb17336719727ce1595759138aa2ff0083585a360d11342` |
| ExecBinder candidate (supplementary) | `.ufo/waves/round-80/w1/ExecBinder/pointer-bind.py` | `b01e7b494acd88caed037a473824ab0b0cb524b520659114c4d46234a1ff8f8a` |

The ExecBinder candidate churned three times during this seat (`5708e470…` → `d46806d9…` →
`b01e7b49…`). The canonical was stable at `2e4a7852…` for the scored runs. **The landed canonical
is not the ExecBinder candidate**; the L1 landed its own instrument. The claim's predicate is on
the landed path, so that is the scored C1 arm; the ExecBinder candidate is scored as the seat's
deliverable.

## 4. Canonical predicate (the claim's own command)

`strictness-battery.py --root . --impl tools/round-80/pointer-bind.py --control-impl
tools/round-79/pointer-bind.py --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json`
→ exit 0:

```
cases 4  green_cases 2  candidate_false_greens 0  control_false_greens 4
candidate_green_refusals 0  control_green_refusals 0  ok true  validate defects []
```

Red rows: rb01/rb02 refused; rb03 `{"checks_total":6,"duplicates":["omp-pin"],"matched":5}`;
rb04 `{"checks_total":6,"duplicates":["devin-pin"],"matched":5}`. Green rows both bound.

Base arm (`--impl tools/round-79/pointer-bind.py`, my run): exit 1,
`candidate_false_greens 4`, `control_false_greens 4`, `ok false`, `--validate` defects `[]`,
candidate reds all four. This reproduces the L1's `c1-at-base.json`.

Live arm (`pointer-bind.py --root . --rev 16dfa009… --json-out …`): exit 0,
`checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`, `duplicates []`, `ok true`,
`--validate` defects `[]`. Receipt: `record.rev` = the 40-hex base, `record.sha256` =
`99d29a00…` (equals the committed `PROVINCE.md` blob at both base and HEAD), `instrument.sha256`
= the scored file digest.

My independent scorer reproduces the same direction: control `false_greens 4`,
`green_refusals 0`; canonical `false_greens 0`, `green_refusals 0`, `duplicate_detections 2/2`.

## 5. Per-case result

| id | kind | control | canonical | ExecBinder |
|---|---|---|---|---|
| rb01-substring-longer-line | bind red | **false-green** (`matched=True`, reason `""`) | refused: `token 'rea-agents@6.7.0' occurs on line 1 only inside a longer token ('"rea-agents@6.7.05')` | refused: names `rea-agents@6.7.05` |
| rb02-substring-longer-token | bind red | **false-green** (`matched=True`, reason `""`) | refused: longer token `'"rea-agents@6.7.00'` | refused: names `rea-agents@6.7.00` |
| rb03-duplicate-omp-cell | record red | **false-green**: `checks_total=5` (6 expected), `duplicates=[]`, `matched=5`, `ok=True` | refused: `checks_total=6`, `duplicates=['omp-pin']`, `ok=False`, ids `omp-pin`, `omp-pin#2` | refused: `checks_total=6`, `duplicates=['omp-pin']`, `ok=False`, ids `omp-pin` ×2 |
| rb04-duplicate-devin-cell | record red | **false-green**: `checks_total=5` (6 expected), `duplicates=[]`, `matched=5`, `ok=True` | refused: `checks_total=6`, `duplicates=['devin-pin']`, `ok=False`, ids `devin-pin`, `devin-pin#2` | refused: `checks_total=6`, `duplicates=['devin-pin']`, `ok=False`, ids `devin-pin` ×2 |
| gr01-exact-pin-line | bind green | bound | bound | bound |
| gr02-exact-range-second-line | bind green | bound | bound | bound |

No control or candidate call raised. All `bind` results report `unparsed=False`. The template-only
record baseline is `checks_total=5, matched=5, ok=True`; both duplicate reds return the **same**
verdict as the baseline under the control, so the appended duplicate is completely invisible
(collapse plus an empty duplicate signal), exactly as the fixture's `why` states.

## 6. Counter under-enforcement — two executable counterexamples (F1)

`tools/round-80/strictness-battery.py:88-95` scores a record red as refused if **either**
`cell_id in duplicates` **or** `checks_total > 5 and ok is not True`. Each half alone suffices, so
the battery does not enforce the frozen rule's two halves together. I built two fixture modules in
scratch and ran the canonical battery on each:

| Fake module | Record receipt it returns | Canonical battery result |
|---|---|---|
| `fake-loose-record.py` | `checks_total 6`, `duplicates []`, `ok false` | **`ok true`, exit 0, `--validate` defects `[]`** — refuses without ever carrying the duplicate id |
| `fake-collapsed-record.py` | `checks_total 5`, `duplicates ['omp-pin','devin-pin']`, `ok false` | **`ok true`, exit 0, `--validate` defects `[]`** — flags the id but still last-wins-collapses the cell map |

Both violate the claim's rule ("every declared cell is counted … the receipt carries the duplicate
id in `duplicates`") and both pass the frozen counter. My stricter scorer catches them:
`loose-record` scores `false_greens 2`; `collapsed-record` scores `duplicate_detections 0/2`
(checks_total 5 ≠ 6) even though it reports the id. The landed canonical satisfies both halves, so
the claim is true of the landed bytes; the instrument does not establish it.

## 7. Landed canonical duplicate-cell defect (F2)

`tools/round-80/pointer-bind.py:195-236` keeps the duplicate cell but renames the second id
`<id>#2` (to keep the validator's unique-id guard quiet). `declared_ok` (`:88-91`) resolves
`DECLARED.get(check_id)`, which is `None` for `omp-pin#2`/`devin-pin#2`, so the second cell is
forced `matched=False` with the false reason *"the pointer does not name the declared live object"*
— although that cell points at the correct file and line. Measured on both record reds:

- canonical: `checks_total 6`, `matched 5`, `mismatches 1`; the unbound cell is `omp-pin#2`
  (resp. `devin-pin#2`) with that reason.
- ExecBinder candidate: `checks_total 6`, `matched 6`, `mismatches 0`; both duplicate cells bind.

This does not falsify the frozen predicate (the record is refused via the duplicate signal), but it
violates the ExecBinder contract's "each duplicate cell is still bound independently (no last-wins
collapse)" and puts a false statement in the receipt. The frozen battery cannot see it because
refusal is the expected red outcome and `duplicate_refused` is a disjunction (§6). It is a concrete
defect in the landed instrument and a fixture blind spot.

## 8. Degenerate checks (fixture set strength)

| Model | Result |
|---|---|
| bind-all (every bind matches; every record accepted, duplicates ignored) | **REJECTED** — fails rb01–rb04 |
| refuse-all (every bind refused; every record flagged duplicate) | **REJECTED** — fails gr01, gr02 |
| ReviewerC1 strict reference (both-sides delimited + duplicate count) | passes all six |
| weak right-digit-only rule (left neighbour ignored) | **passes all four bind cases** — gap F3 |
| weak left-only rule (right neighbour ignored) | caught by rb01, rb02 |

## 9. Findings (by severity)

**F1 (medium, counter under-enforcement).** `strictness-battery.py:88-95` accepts either half of
the duplicate rule alone; two fake candidates pass `ok true` while violating one half each (§6).
The frozen predicate therefore does not establish the rule it states. Fix direction: require
`cell_id in duplicates` **and** `checks_total == 6` **and** `ok is False`, and add a
`--validate` re-derivation for that conjunction.

**F2 (medium, landed duplicate-cell binding).** `pointer-bind.py:88-91` + `:195-236`: the suffixed
duplicate id is absent from `DECLARED`, so the second duplicate cell is force-failed with a false
reason (canonical `matched 5/6`; ExecBinder `6/6`). It violates "each duplicate cell is bound
independently" and is invisible to the frozen battery. Fix direction: resolve `DECLARED` on the
base client id for suffixed duplicate cells (or carry the declared-object identity per cell).

**F3 (medium, fixture sensitivity).** Both bind reds continue the token with a **digit** (`05`,
`00`); no red exercises a left-side boundary or a non-digit continuation. A right-digit-only rule
(the left neighbour never checked) passes all four bind cases. The delivered canonical and the
ExecBinder candidate both implement both sides (`TOKEN_CHARS` is exactly `[A-Za-z0-9._-]`; both
`before` and `after` are checked), so the capability is real, but the frozen fixture cannot prove
it. A future red with a letter/punctuation continuation or a left-side prefix (`xrea-agents@6.7.0`)
would close the gap.

**F4 (low, record attribution).** Both record reds append a byte-identical cell. The observable
false-green is the 5-vs-6 count plus the absent duplicate signal; the fixture cannot distinguish
"keeps the last cell" from "keeps the first" (the control's dict comprehension is last-wins by
code, but the fixture proves only the count/signal).

**F5 (low, guard location).** The four red fixtures do not catch a record-only refuse-everything
implementation (the reds *want* refusal). The guards are the two green bind controls and the live
arm's `duplicates []` with `checks_total 5`; both were verified green for both arms.

**F6 (residual).** Any candidate can special-case the six frozen inputs. The live arm on the five
real pointer cells is the only generalisation guard; it passed for both arms.

**F7 (verification gap).** The lane moved while this seat ran (`253fc817` → `b8260107` →
`b00419fb`) and the ExecBinder candidate churned three times. All C1 numbers here are for the
canonical bytes `2e4a7852…` (stable across the scored runs). If the L1 re-lands the canonical, the
canonical battery must be re-run; this receipt is exact for the named bytes only.

## 10. Byte discipline / bounds

- Candidate and control receipts retain `line_sha256` digests only; no pointed-line bytes. Every
  pointed-slice digest in both fixture repos re-derived from the live files, and the record digest
  equalled the committed `PROVINCE.md` blob.
- Fixture git repos were created under the scratch root; `git rev-parse --show-toplevel` equalled
  each fixture dir before the first commit. No git write touched the lane, a sibling lane, the
  fleet root, `/tmp`, or a lane production file.
- Writes: this report plus `.ufo/waves/round-80/w1/ReviewerC1/` only. Scratch removed.

## 11. Evidence files

`.ufo/waves/round-80/w1/ReviewerC1/`: `reviewer-strictness.py`,
`receipt.json` (canonical), `receipt-execbinder.json`, `receipt-control-only.json`,
`battery-receipt.json` (canonical), `battery-base-arm.json`,
`battery-loose-record.json`, `battery-collapsed-record.json`,
`receipt-fake-loose-record.json`, `receipt-fake-collapsed-record.json`,
`live-canonical.json`.

## 12. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r80/ReviewerC1 && mkdir -p "$S/work"
TMPDIR="$S" python3 -I -B tools/round-80/strictness-battery.py --root . \
  --impl tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py \
  --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json \
  --work "$S/work" --json-out .ufo/waves/round-80/w1/ReviewerC1/battery-receipt.json
python3 -I -B tools/round-80/pointer-bind.py --root . --rev 16dfa009bf143080dfcdfc5f9ec34bd359536d90
TMPDIR="$S" python3 -I -B .ufo/waves/round-80/w1/ReviewerC1/reviewer-strictness.py \
  --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json \
  --control-impl tools/round-79/pointer-bind.py \
  --candidate-impl tools/round-80/pointer-bind.py \
  --work "$S/work2" --json-out .ufo/waves/round-80/w1/ReviewerC1/receipt.json \
  --lane-root . --base 16dfa009bf143080dfcdfc5f9ec34bd359536d90
rm -rf -- "$S"
```
