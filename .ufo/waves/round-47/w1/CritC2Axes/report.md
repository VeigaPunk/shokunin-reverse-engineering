# CritC2Axes — seat report (R47-C2 `axes` atom)

Full findings and the landed-clause critique: `../CritC2Axes.md`.
Receipts and their sha256: `MANIFEST.md`, `receipts/`.

**Fixture.** No repo fixture was required: each attack imports the frozen counter
(`tools/round-47/record.py`, sha256 `c704c3d4…`), takes
`gate.show(root, <rev>, "SCORECARD.md")` (or `corpus/README.md`), applies exactly one string
substitution, and calls `record.evaluate_text(card, files, ROOT, tip, battery=None)`
(`files = gate.show` at the same rev, with a single per-path override for the dangling-token
case). Closure cases use `receipts/record.patchedC.py`, a scratch copy carrying the four
edits described in `../CritC2Axes.md` § "Smallest safe correction"; the originals were never
written.

**Command.**

```sh
cd /fast/scratch/hyaku/kaidoku-r47/CritC2Axes
export TMPDIR=$PWD HYAKU_SCRATCH=$PWD
python3 -I -B drive.py  <REV>     # E1..E9   -> drive.out
python3 -I -B drive2.py <REV>     # E10..E14 -> drive2.out
python3 -I -B drive3.py <REV>     # patchAB (naive axes-in-CORR) -> drive3.out
python3 -I -B drive4.py <REV>     # patchB  (score + column anchoring) -> drive4.out
python3 -I -B drive5.py <REV>     # patchC  (+ per-axis presence + dangling) -> drive5.out
python3 -I -B drive6.py 1e2c3102  # subject swap / score reversal -> drive6.out
python3 -I -B toolsC/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 1e2c3102                  # patched CLI, incl. battery -> cC-1e2c3102.json
python3 -I -B /home/vgpnk/…/tools/round-47/record.py --root … --rev <REV>   # canonical
```

**Exit codes.** Frozen counter at `2e4ae434` and at `1e2c3102`: **0** (`atoms 50`,
`corrections 2`, `exempted 2`, battery `3/0 green`); frozen `--selftest`: 0
(`cases=10 failures=0`). Score forgeries `3.14 → 4.20`, `0.00 → 1.00`, `42.0 → 99.9`,
`9.72 → 8.40`, `10.0 → 9.72`, fraction-moved-into-score-column, subject-swapped, ghost map
token, `Coverage` relabel: all **0**. Fraction forged `137/138`: **1** (the only thing bound).
Patched C: real card **0** (receipt byte-identical to the frozen one), all six score forgeries
**1**, relabel **1**, ghost token **1**; patched C `--selftest` is **1** until its own `_card`
fixture gains a baseline line and a depth row.

**Verdict: predicate too weak, here is what closes it.** The `axes` atom is the first `n/m`
in the row tail (`record.py:39-40`, `:173-183`); the score cell the axis is scored on is
never read, so `138/138` coexists with `9.72 → 8.40` or `42.0 → 99.9`. Today's `9.72 → 10.0`
is true (70/72 at the card's baseline `6645585…`, 138/138 and 24/24 at `--rev`, by the card's
own `round(10*n/d,2)`), so the claim is latently overstated: it verifies the proxy, not the
score. Close it by binding the score cell to the derived pair at the card's baseline revision
and at `--rev`, taking the fraction from the observable column, requiring an atom for each of
`coverage`/`depth`, and requiring `dangling == 0` — measured green on the real card, red on
every forgery. Secondary: `CORR` (`record.py:50`) cannot parse `axes`, so the two landed
`- corrects axes …` lines are inert (receipt says `corrections 2` of four) and claims clause 3's
`axes` sentence is dead; adding `axes` to `CORR` *alone* opens an exemption hole via
`exempt()` (`:330-337`) — verified: score forgeries then pass.
