# CritC2Axes — R47-C2 `axes` atoms, attacked

Seat `CritC2Axes`, round 47 wave 1. Read-only on the lane tree; every mutation below is a
copy under `S=/fast/scratch/hyaku/kaidoku-r47/CritC2Axes` (`tools/` copy) or an in-process
call to `record.evaluate_text(card, files, …)` with a forged card/`files` — no fixture repo
was needed and no tracked byte was touched.

**Verdict: predicate too weak, here is what closes it.** The `axes` atom is the *first*
`n/m` in the row tail (`tools/round-47/record.py:39-40`, `:173-183`). It never reads the
score cell — the `0–10` number the axis is actually scored on. The counter therefore reads
`138/138` while the score column can say anything: `3.14 → 4.20`, `0.00 → 1.00`,
`42.0 → 99.9` (outside the card's own 0–10 scale), `9.72 → 8.40` (regression where the pair
derives 10.0) and `10.0 → 9.72` (reversed) are all **exit 0**. The landed `9.72 → 10.0` is
*true* (I re-derived it), so the overstatement is latent, not active — the clause cannot
distinguish true from false.

## The assigned question, answered with the counter

Can the counter read `138/138` while the score column still says `9.72 → 10.0`? It cannot do
otherwise: the score cell is outside the atom set. Receipts, frozen counter, rev
`2e4ae43463aabdae707f8c8a4daa41441ad67a71` (`record.py` sha256
`c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7`, unchanged at
`1e2c3102`):

| # | forged card | exit | receipt |
|---|---|---|---|
| E1 | card as committed | **0** | `receipts/drive.out` `05fea863…` |
| E2 | `coverage 9.72 → 10.0` → `3.14 → 4.20` | **0** | do. |
| E3 | `depth 10 → 10` → `0.00 → 1.00` | **0** | do. |
| E4 | `coverage …` → `42.0 → 99.9` (out of scale) | **0** | do. |
| E5 | headline `138/138` → `137/138` (control) | **1** | do. `mismatches 1 != 0` |
| E6 | `\| coverage \| 138/138 \| 0/138 knowledge files mapped …` | **0** | do. |
| E7 | + `- corrects axes coverage: 7/9`, `depth: 1/24`, `calibration: 0/0` | **0** | do. |
| E8 | the two landed `- corrects axes …` lines deleted | **0** | do. |
| E9 | `corpus/README.md` gains a coverage-map token naming no knowledge file | **0** | do. |
| E14 | `coverage 9.72 → 8.40` | **0** | `receipts/drive2.out` `a3492df6…` |
| E15 | `138/138 bytes of the moon accounted for …` | **0** | `receipts/drive6.out` `b5b06866…` |
| E16 | `coverage 10.0 → 9.72` (score reversed) | **0** | do. |
| E12 | `\| coverage \|` → `\| Coverage \|` | **0**, `axes_atoms 1` | `receipts/drive2.out` |

Baseline of the same counter, same byte: exit 0, `atoms 50`, `verified 48`, `corrections 2`,
`exempted 2`, `battery.correction_forgeries 3 / forgeries_green 0`, stdout sha256
`553be365645d8fe69adfac6a1888c67dacd72f12e608ebe71784ea9467d88fc0`
(`receipts/c2-head.json`); identical fields at `1e2c3102`, sha256
`c609b3e1c8ac00d03f8b80c9313d96b25466e53116b40121422f43e94224209d`
(`receipts/frozen-1e2c3102.json`). Frozen `--selftest`: `cases=10 failures=0` (exit 0).

Command (both runs, `S` exported as both `TMPDIR` and `HYAKU_SCRATCH`):

```sh
python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <REV>            # stdout is the receipt; --json-out is refused outside the lane root
```

Forgery commands (`receipts/drive*.py`, run as `python3 -I -B driveN.py <REV>`): each imports
the frozen `record.py`, takes `gate.show(root, tip, "SCORECARD.md")`, applies one string
substitution and calls `record.evaluate_text(card, files, ROOT, tip, battery=None)`. `files` is
`gate.show` at the same rev, with a per-path override for E9.

## What is actually true today (so nobody "fixes" a correct number)

`record.coverage_pair` / `record.depth_pair` at the revisions the card names
(`receipts/base.out`, `27355baf…`), scored by the card's own formula
(`SCORECARD.md:30`, `round(10 * numerator / denominator, 2)`):

| rev | coverage | score | depth | score |
|---|---|---|---|---|
| `6645585873c4e66372b15687c47000abf8d91978` (card's baseline, `SCORECARD.md:27`) | 70/72 | **9.72** | 9/9 | **10.0** |
| `e1c83313f33a3d97edbd8fef402db2d06172fcdc` (round 41) | 133/133 | 10.0 | 20/20 | 10.0 |
| `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` (round 40) | 130/130 | 10.0 | 19/19 | 10.0 |
| `2e4ae434…` / `1e2c3102` (round 47 landing) | 138/138 | 10.0 | 24/24 | 10.0 |

So `9.72 → 10.0`, `10 → 10`, `138/138`, `24/24` are all correct. The defect is that the
clause does not require them to be: an `axes` atom that ignores column 2 is an atom about a
*proxy*, not about the score the axis is judged on — the R46-CL7 class ("the clause binds the
digits, not their meanings") one layer down.

## Second defect: `axes` corrections are unreachable, and their naive repair is unsafe

The landed `## Record corrections — round 47` section carries four `- corrects` lines
(`SCORECARD.md:3669-3678`: seats round-45, window round-46, **axes coverage 138/138**,
**axes depth 24/24**). `CORR` (`record.py:50`) parses `seats|window|path|rev` only, so the
receipt says `corrections 2` and the two axes lines are inert (E7, E8: adding false axes
corrections or deleting the true ones changes nothing). Consequences:

- claims clause 3 ("an `axes` correction must state `<resolved>/<total>`") is **dead text**:
  no `axes` line can ever reach `corrects()`. The entire axes handling in `corrects()` is
  dead code — and `record.py:292-299` is a second, unreachable `if cls == "axes"` branch
  that references an undefined `atom` (latent `NameError` if it ever executed).
- the card's corrections section claims four counter-validated repairs; the counter validates
  two. `corrections >= 2` is met by exactly the seats+window pair.

Adding `axes` to `CORR` alone is **not** the fix: `exempt()` (`record.py:330-337`) matches
non-window classes on class+key only, so the landed `- corrects axes coverage: 138/138` line
then excuses *any* coverage-atom failure. Measured with that patch
(`receipts/record.patchedAB.py`, `receipts/patch-1e2c3102.json`, exit 0, `corrections 4`) the
score forgeries survive: P2 `3.14 → 4.20`, P3 `0.00 → 1.00`, P4 `42.0 → 99.9`,
P5 `9.72 → 8.40`, P6 `9.70 → 10.0` all exit **0** (`receipts/drive3.out`, `2de23ba7…`).

## Smallest safe correction (verified, not proposed)

`receipts/record.patchedC.py` = frozen `record.py` plus four edits, none of which change any
other atom class:

1. `record.py:40` — add `SCORE = re.compile(r"(\d+(?:\.\d+)?)\s*→\s*(\d+(?:\.\d+)?)")` and
   `BASELINE = re.compile(r"(?m)^Baseline source revision: \`([0-9a-f]{7,40})\`")`.
2. `record.py:173-183` — split `m.group(2)` into cells and take the fraction from **cell 2**
   (the observable column) instead of `FRAC.search(<whole row tail>)`; capture cell 1's
   `baseline → current` pair.
3. `record.py:223-231` (`derive`, `cls == "axes"`) — after the pair check, require
   `(baseline_score, current_score) == (round(10*b/t,2) at BASELINE, round(10*r/t,2) at --rev)`;
   a row without a score cell, or a card without a baseline revision, is a mismatch
   (`unverifiable`, the same rule the `window` class already applies).
4. `record.py:378` — require an atom for **each** of `coverage`, `depth` (`no axes atom for
   ['coverage']`), and for the coverage axis require `len(mapped - stems) == 0`, because the
   row's own observable cell asserts `dangling []`.

Measured (`receipts/drive4.out` `99b48dc9…`, `receipts/drive5.out` `e76c22ab…`):

| case | frozen | patched C |
|---|---|---|
| real card, `2e4ae434` and `1e2c3102` (CLI, incl. battery) | **0** `c609b3e1…` | **0** `c609b3e1…` (byte-identical receipt) |
| B2/B5/B6/P2/P5 score forged (baseline, current, both directions) | 0 | **1** |
| B3/P3 depth score forged | 0 | **1** |
| B4/P4 score outside 0–10 | 0 | **1** |
| B7 fraction moved into the score column (`0/138` observable) | 0 | **1** |
| B8 `137/138` (control) | 1 | **1** |
| C2 row relabelled `Coverage` | 0 | **1** `no axes atom for ['coverage']` |
| C4 ghost coverage-map token | 0 | **1** `dangling_tokens 1` |

**Caveat the L1 must respect:** this is a change to frozen bytes, so it needs a disclosed
amendment (A5) *and* the counter's own selftest fixture update — `_card` (`record.py:494-514`)
has one coverage row, no `Baseline source revision` line and no depth axis, so the patched
counter's `--selftest` reports `cases=10 failures=3` (every fixture reddens on
`no axes atom for ['depth']` / `unverifiable`). That selftest failure is the patch being
under-fixtured, not the patch being wrong; verified separately that the real card stays green.
Also, if `axes` is added to `CORR`, `exempt()` must exclude `axes` (or bind the correction's
pair to the atom) — otherwise patchAB's hole reopens.

**Cheaper alternative, if the L1 will not amend:** keep the frozen counter and narrow the
claim. R47-C2 then verifies "the leading `<resolved>/<total>` of the two axis rows plus four
atom classes of the last two round sections", and the frozen clause 3 sentence about `axes`
corrections must be deleted (it is unreachable). The claim must not be described as
re-deriving the self-assessment "atom by atom" while the 0–10 score column is outside it.

## Impacted axes

- **calibration (R47-C2)** — the claimed class. Overstates: it binds a proxy and the row's
  subject text, not the score (E2–E4, E14–E16) and not the row's identity (E12).
- **depth (R47-C1)** — untouched by this attack; no reading of `SKILL.md` is involved. The
  `flag-order`/`digest` clauses are other seats' surface and I did not exercise them.
- **coverage** — no claim this round; note only that E9/E15 show the *observable* cell's prose
  (`missing []`, `dangling []`, `command A mapped 138`) is unbound, and gap 4 closes the one
  part of it that is mechanically checkable.

## Residual gaps I did not close

- The observable cell's free text stays unbound (E15: replacing the subject keeps the atom
  met). Binding it means either dropping the prose or atomising each sentence part; the
  fraction + dangling check covers the mechanically meaningful part.
- `parse` fragility: `WINDOW`/pathspec parsing and the `rev` class were outside my seat.
- `record.py:292-299` dead branch (latent `NameError`) — cosmetic, but it should go.

## Scratch hygiene and tooling

`S=/fast/scratch/hyaku/kaidoku-r47/CritC2Axes` removed after its receipts were copied to
`.ufo/waves/round-47/w1/CritC2Axes/receipts/`. Nothing written outside this report dir and
`$S`; no git/jj mutation, no `/tmp`, no `~/.local/bin`. No package installed (no pacman, uv,
npx or release binary was needed; `python3` + `git` sufficed).

Receipt window: 2026-10-28T17:53Z–17:58Z (file mtimes are the later copy, 17:58Z).

## Sources

- `plans/round-47-claims.md` (R47-C2 clauses 1–6, frozen at
  `5017e1f7299c3a812e87e7950148f54313dd279e`)
- `tools/round-47/record.py:39-40,50,104-127,173-183,188-231,258-304,330-337,378-386,494-514`
  (sha256 `c704c3d4…`)
- `SCORECARD.md:27-30` (baseline revision + the scoring formula the card itself states),
  `SCORECARD.md` `## Owned axes` rows `coverage`/`depth`, `SCORECARD.md:3663-3678`
- `corpus/lessons/round-46.md` `## Routed defects` R46-CL2 (substring arm), R46-CL7 (contentless
  row scores met) — the two defect classes this finding reproduces one layer down
- receipts: `.ufo/waves/round-47/w1/CritC2Axes/receipts/` (command, exit, stdout sha256 per file)

**One-line verdict: predicate too weak — the `axes` atom binds the fraction and ignores the
score cell, so `138/138` coexists with any `baseline → current` pair; binding
`round(10*num/den,2)` at the card's own baseline revision and at `--rev`, taking the fraction
from the observable column, requiring both axes present and `dangling == 0`, closes it and
keeps the landing green.**
