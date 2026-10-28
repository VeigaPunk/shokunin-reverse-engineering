# CritGold — seat report (round 47, wave 1)

Task: construct the gold-plated forgery that reaches `met_target: true` for **both** frozen claim
instruments without any of the round's real work, score it, and say whether the predicate holds.

**Verdict: `predicate too weak` — both. Here is what closes each.** Full findings, per-claim clause
numbers and smallest safe corrections: `../CritGold.md`. Receipts: `receipts/`. Reproduce:
`sh rebuild.sh`.

## The fixture (cheapest artefact, 12 inserted lines / 157 deleted)

`rebuild.sh` clones the lane at `1e2c3102` into scratch (`mktemp -d -p $S`, toplevel asserted
before the first commit), then makes **one** commit:

1. block-24 table rows → four rows that name the *wrong* arm for every routed defect, `n/a` in
   every `v2 hole` cell, `0` in every `exit` cell:
   `R46-CL2|n/a|order|0`, `R46-CL3|n/a|digest|0`, `R46-CL4|n/a|symbol|0`, `R46-CL6|n/a|once|0`.
2. `SCORECARD.md` last two round sections → five tautologies (seats read off the dispatch files,
   `git log X..X` "is empty", one existing path token, one backticked tip), plus a corrections
   section of five lines of which none exempts a red atom and one (`round-3`) names a round that
   does not exist.
3. Header, marker, title, citations, `mutations_sha256` and `interpreter_sha256` left untouched —
   the pins were never a constraint.

## The score

| command | exit | result |
|---|---|---|
| `python3 -I -B tools/round-47/exact.py --root $D --freeze 1e2c3102 --rev <fixture>` | **0** | `met_target true`, `failing []`, `battery 4/4/0/1/0` |
| `python3 -I -B tools/round-47/record.py --root $D --rev <fixture>` | **0** | `met_target true`, `failing []`, `atoms 10`, `verified 9`, `exempted 1`, `corrections 4`, `corrections_bad []` |

The genuine artefacts at `1e2c3102` score the same two zeros (`receipts/genuine-c1.json`,
`genuine-c2.json`): the counters cannot tell the forgery from the landing.

Second fixture (separate proof, `receipts/noop-c1.json`): all four mutation bodies in `exact.py`
emptied, `interpreter_sha256` restated in the same commit → still `forgeries_total 4 / v2_green 4 /
v3_green 0`, exit 0. The battery of an emptied counter reports the genuine numbers.

## The three holes that matter most

- **C1 clause 5 / clause 9** — the arm column binds vocabulary membership, not correspondence, and
  the `exit` column binds nothing; a mutation that is a no-op is booked as `v2_green`. Close with a
  fixed `{routed id → arm}` map, `exit == "1"` on all four rows, `battery.noop == 0`, and a digest
  over `inspect.getsource` rather than the mutation names.
- **C2 clause 1** — content is unbound: deleting both round sections is scored `mismatches []`.
  Close with atom monotonicity against each round's landing commit (`git show <landing>:SCORECARD.md`).
- **C2 clause 3/4** — `X..X` is an always-empty window, a correction need not name a red atom, and
  a pair-less `<tip>` atom is exempted by any window at all. Close by rejecting `base == tip`, by
  requiring every correction to be load-bearing, and by forbidding placeholder laundering.

Also found (each with a receipt): `freeze == rev` makes the frozen-set arm vacuous (the lane's own
`c1-at-A4.json` is `freeze == rev`); `axes` corrections are unreachable because `CORR` omits the
class while `corrects()` implements it; a forgery that no-ops makes the C2 battery go *red* for a
missing line; and only the first `A..B` on a line is ever checked.

No lane file was written; no install performed; fixture clones lived in
`/fast/scratch/hyaku/kaidoku-r47/CritGold*` and were removed after the receipts were copied here.
