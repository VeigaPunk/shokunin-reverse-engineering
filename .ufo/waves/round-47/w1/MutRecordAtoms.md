# MutRecordAtoms — R47-C2 atom-digit mutation probe

Seat `MutRecordAtoms` (mutation tester), wave `round-47/w1`.
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`;
declared freeze for the probe **A4 `1e2c3102952dc636650095643c1963c833859019`**; measured/mutated tip
**`07d2894eabe88c326e9036262f20ad02662c860d`** (lane HEAD when the probe ran, 2026-10-28T17:59:42Z–18:00:07Z).
Nothing frozen was modified: every mutation is a commit inside a scratch clone.
No tool installs (nothing needed; `git` + `python3` only).

## Bottom line

- Baseline at `07d2894e` is green: `record.py` exit **0**, `atoms 41`, `verified 40`, `corrections 2`,
  `corrections_bad []`, `exempted 1`, `battery.forgeries_green 0`, `met_target true`
  (`receipts/M0-baseline.json`).
- The four assigned digit mutations — seat count, window hash, path segment, commit hash — are
  **all caught** (exit 1, one named mismatch each; M1–M4).
- **Three further one-digit mutations are silent (exit 0)**: an exempted placeholder window's base
  (F1), a path token swapped to a different *existing* file (F2/F2b), and an `axes` correction line
  (F3). A silent digit is a finding.
- Two non-digit degeneracies are also silent: a window atom and a *correction's own* window can be
  made `X..X`, which is empty by construction (F4/F5) — the same vacuity class A2 was created to
  remove, surviving in the repair path.
- One character of shape damage silently deletes an atom from the count (`1e2c310295` → `1e2c31029z`:
  `atoms 41 → 40`, exit 0; F6). Nothing re-derives the atom population.
- Separate, higher-severity: `record.py` carries **no freeze guard at all** (`CLAIMS`/`SELF` are
  defined and never read, no `--freeze`), and commit `07d2894e` **A5 rewrites `tools/round-47/record.py`
  after the declared freeze A4**. `exact.py` sees it and exits 2 `frozen_path_changed`; `record.py`
  scores itself green (F7).

## Method

`record.py` grades **committed bytes**: `evaluate()` reads the card with
`gate.show(root, tip, "SCORECARD.md")` → `git show <rev>:SCORECARD.md`. A working-tree edit is
therefore invisible to it. The probe commits each mutation in a scratch clone:

```sh
S=/fast/scratch/hyaku/kaidoku-r47/MutRecordAtoms; export TMPDIR="$S" HYAKU_SCRATCH="$S"
git clone --shared --quiet /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/fix"
git -C "$S/fix" rev-parse --show-toplevel      # asserted == $S/fix before every commit
# per probe: git -C "$S/fix" reset --hard 07d2894e…; patch one atom; git -c user.name=mut
#   -c user.email=mut@invalid commit -am "probe …"; then:
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py \
  --root "$S/fix" --rev <mutant> --json-out "$S/fix/.receipts/<probe>.json"
# after: git -C "$S/fix" reset --hard 07d2894e…
```

`--json-out` must live inside `--root` (the counter rejects an out-of-root path with exit 2), hence
`.receipts/` inside the clone. Every probe receipt (`receipts/M*.json`, `receipts/log.json`) carries
the exact command, commit, exit code, UTC time and stdout sha256.

## Mutation table

Assigned four first, then the probes that hunt for silences. "Digit" = a single decimal/hex character
changed in place, nothing else in the document touched.

| # | mutation (atom → mutant) | exit | detected by |
|---|---|---|---|
| M0 | baseline, no mutation @ `07d2894e` | 0 | `met_target true`, `atoms 41` |
| **M1** | seats `Waves: 40 + 40 = 80 seats` → `… = 81 seats` | **1** | `mismatches 1` class `seats` key `46`, `derived [40,40,80]` |
| **M2** | round-47 window `e856beb5..1e2c310295` → `…1e2c310296` | **1** | `mismatches 1` class `window` key `47` (`git log failed`) |
| **M3** | path `…/round-47/l1/scores/c1-at-A4.json` → `c1-at-A9.json` | **1** | `mismatches 1` class `path`, `exists false` |
| **M4** | rev cell in the R47-C2 row `` `1e2c310295` `` → `` `1e2c310296` `` | **1** | `mismatches 1` class `rev` key `1e2c310296`, `resolves false` |
| M5 | exempted window base `0425224..<tip>` → `0425225..<tip>` | **0** | **SILENT** — atom exempted wholesale (F1) |
| M6 | path `…/round-47/l1/scores/c1-at-A4.json` → `c1-at-A2.json` (exists) | **0** | **SILENT** — existence-only (F2) |
| M7 | `- corrects axes coverage: 138/138` → `139/138` | **0** | **SILENT** — `CORR` never matches `axes` (F3) |
| M8 | control: axes row `138/138 knowledge files mapped` → `139/138` | **1** | `mismatches 1` class `axes` key `coverage` |
| M9 | rev cell `` `1e2c310295` `` → `` `1e2c31029z` `` (one char) | **0** | **SILENT** — atom vanishes, `atoms 41 → 40` (F6) |
| M10 | round-47 window → `332f4884..332f4884` | **0** | **SILENT** — degenerate window (F4) |
| M12 | seats correction `2 waves, 76 seats total` → `77` | **1** | `corrections_bad 1`, `claimed [2,77] vs [2,76]` |
| M13 | window correction `332f4884..58eb04b6` → `…58eb04b5` | **1** | `corrections_bad 1` (`git log failed`) |
| M14 | window correction → `58eb04b6..58eb04b6` | **0** | **SILENT** — correction "re-derives" against an empty-by-definition window (F5) |
| M15 | claim evidence path `…/round-47/l1/scores/c2-at-A4.json` → `c2-at-A2.json` | **0** | **SILENT** — the claim's own after-receipt is swappable (F2b) |

Killed 7 (M1, M2, M3, M4, M8, M12, M13); survived 8 (M5, M6, M7, M9, M10, M14, M15). Every mutant
commit is a one-line diff from `07d2894e`, verified with
`git show <mutant>:SCORECARD.md | grep -c -F '<mutated text>'` → 1.

## Findings

### F1 — a placeholder window atom's *base* is unvalidated, and the exemption is unconditional (silent digit)

Mutant `44fc9061` changes one digit: `0425224..<tip>` → `0425225..<tip>` (record.py `SCORECARD.md`,
Round 46 "Freeze-integrity disclosure"). `0425225` **is not a commit**
(`git -C fix rev-parse --verify 0425225^{commit}` → exit 1, no output). `record.py` exit **0**;
the atom appears in `exempted`, not in `mismatches`.

Mechanism: `derive()` classifies the atom `unverifiable` (`WINDOW.search` fails on `<tip>`), then
`exempt()` (record.py:330–335) returns `True` for **any** window atom whose `pair is None` as soon as
one parsed window correction exists — it never looks at the revisions the atom does name. The
correction's own pair (`332f4884..58eb04b6`) has no relation to `0425224`. Clause 4's second arm
("an atom that names no concrete window") is therefore an unconditional blanket over the whole
sentence, including its resolvable half.

Reproduction: clone, replace `0425224..<tip>` with `0425225..<tip>`, commit, run the counting command →
exit 0. Fixture mutant commit in this seat's clone: `44fc9061`; receipt
`receipts/M5-window-placeholder-base-digit.json`.

### F2 — `path` atoms bind existence, not identity (silent digit)

M6: `.ufo/waves/round-47/l1/scores/c1-at-A4.json` → `c1-at-A2.json` (one digit; **both files exist**)
→ exit 0. `derive()` (record.py:221) is `exists = files(atom["path"]) is not None` — no binding to the
sentence, the claim, or the receipt's contents. A mutated path survives whenever the target name is
taken.

F2b (sharper): M15 changes `.ufo/waves/round-47/l1/scores/c2-at-A4.json` → `c2-at-A2.json` **in the
R47-C2 row's `after` cell** — the claim's own evidence pointer. Exit 0; the card now cites the A2
receipt as proof of the A4 measurement and the counter still reports `met_target true`.
Mutants `56260134`, `4cc46a43`.

### F3 — `axes` corrections are inert text; a false one is accepted (silent digit)

The corrections section carries four `- corrects` lines, but `CORR` (record.py:50) accepts only
`(seats|window|path|rev)`. Proof:

```
python3 -c "import record; print(record.CORR.match('- corrects axes coverage: 138/138'))"  → None
python3 -c "import record; print(bool(record.CORR.match('- corrects seats round-45: …')))"  → True
```

Consequences, all measured:

- M7 mutates `- corrects axes coverage: 138/138` → `139/138` (a **false** statement about the record's
  own axes): exit 0, `corrections 2` (the two axes lines are not even counted), `corrections_bad []`.
  Claims-file clause 3's sentence "an `axes` correction must state `<resolved>/<total>`" is never
  evaluated; the battery's three forgeries contain no `axes` case.
- The `axes` branches inside `corrects()` (record.py:280 and the duplicated copy at 292) are dead code:
  no `entry` with `class == "axes"` can exist. `exempt()` would likewise never see one, so an axes
  mismatch has **no repair path at all** — M8 (control) shows the mismatch is red and the correction
  line beside it cannot exempt it.

This matters for the round's own record: the two `axes` correction lines are the *only* place the
round documents how the 133→138 and 20→24 heads were repaired, and the counter neither re-derives
nor counts them. A false or deleted axes correction is invisible; the heads are only protected
because the `## Owned axes` table itself was rewritten to the derived values.

### F4 — the `window` clause is satisfiable by `X..X` (silent, non-digit)

M10: round-47 window `e856beb5..1e2c310295` → `332f4884..332f4884` (the round's own measured freeze as
both ends). Exit 0. `git log --name-status --format= 332f4884..332f4884 -- …` prints 0 lines, so
"is empty" is true — vacuously. The clause tests emptiness only; a window naming the same revision
twice, or a range over a pathspec that cannot change, is green forever. This is exactly the class
A2 identified (a "forgery" that is a no-op); A2 fixed the *battery fixture*, not the predicate.

### F5 — a correction's own re-derivation has the same degenerate hole (silent, non-digit)

M14: `- corrects window round-46: empty in 332f4884..58eb04b6 -- …` → `58eb04b6..58eb04b6`. Exit 0,
`corrections_bad []`. `corrects()` calls the same `window_empty()`, so the exemption that covers
F1's atom can itself be justified by a window that asserts nothing. The counter's `exempted`
atom and its justification are then both vacuous, and the card still reports `met_target true`.

### F6 — atoms that stop matching are silently deleted, not failed (one-character)

M9: `` `1e2c310295` `` → `` `1e2c31029z` `` inside the R47-C2 `measured at` cell. `REV_TOKEN`
(record.py:48) no longer matches, so the atom does not exist: `atoms 41 → 40`, `verified 40 → 39`,
exit **0**. Nothing counts atoms: `atoms_by_class` (record.py:375–377) only asserts each of the five
classes has ≥ 1 atom, so dropping one of 28 `rev` atoms (or one of 8 `path` atoms) is free, while
dropping the *only* `seats` atom is caught. The card's own sentence "over 50 atoms" is not re-derived
either (see F8), so atom-population drift has no detector. A one-length-short token
(e.g. truncating a hash to 6 hex) has the same effect.

### F7 — `record.py` has no freeze guard, and the frozen counter was rewritten after the declared freeze

- `record.py:32–33` defines `SELF` and `CLAIMS`; neither is read anywhere in the file. There is no
  `--freeze` option, no self-sha256 pin, and no frozen-path check.
- `07d2894e` ("A5 - the ghost-atom forgery lands inside the corrections section") modifies
  `tools/round-47/record.py` **after** the declared freeze A4 `1e2c310295`, and the card's Round-47
  section discloses a five-commit series ending at A4 — A5 is a sixth, undisclosed edit.
- The sibling instrument sees it; `record.py` does not:

```
python3 -I -B tools/round-47/exact.py --root <clone> --freeze 1e2c3102952dc636650095643c1963c833859019 \
  --rev 07d2894eabe88c326e9036262f20ad02662c860d --json-out <clone>/.receipts/exact-at-head.json
# → exit 2, reason "frozen_path_changed",
#   frozen_path_changed ["tools/round-47/", "tools/round-47/record.py"], restored ["tools/round-47/record.py"]
```
(`receipts/exact-at-head.json`.)

So the claims file's sentence "Nothing in this file or in `tools/round-47/` changes after the freeze: a
change makes **both** counters exit 2 `frozen_path_changed`" is true for `exact.py` and false for
`record.py`. C2 can be re-tuned after its own freeze and still score `met_target true`; only C1's
instrument (a different claim) notices, which breaks the "either lands and scores without the other"
separability the claims file asserts.

### F8 — the record's numbers about the counter are not re-derived, and drift at the tip

The R47-C2 row says "`record.py` over 50 atoms" and "`exempted 2 <= 3`". Both reproduce **at A4**,
whose last two round sections are Round 45 + Round 46:

```
--rev 1e2c310295… → exit 0, atoms 50, verified 48, exempted 2, atoms_by_class {path 12, rev 33, seats 2, window 1}
```

(identical to `.ufo/waves/round-47/l1/scores/c2-at-A4.json`, so the after-cell is honest). At the
card's own tip `07d2894e` the sections are Round 46 + Round 47 and the same command measures
**`atoms 41`, `exempted 1`**. Landing one new `## Round N` section halves the population and
retires an exemption; the counter never notices, because no clause re-derives the numbers the record
states about the counter. This is coverage/calibration noise the L1 should state as a limitation of
the claim ("50 atoms at the measured revision, 41 at any later tip") rather than repeat unqualified.

## What L1 may want to land (non-binding; frozen bytes untouched by this seat)

1. Count atoms instead of only classes: re-derive the atom population for the two sections and fail on
   a shrink (F6), or bind the card's "N atoms" sentence to the measurement.
2. Make `CORR` accept `axes` (and drop the duplicate branch at record.py:292), so the two axes
   corrections are counted, re-derived, and can exempt (F3). Otherwise delete the axes correction
   lines and the claims-file sentence, and state that axes repairs are made in the table only.
3. Reject a degenerate window in both predicates: `A..B` with `A == B`, or `A` not an ancestor of `B`,
   is `unverifiable` (F4/F5).
4. Make the placeholder exemption state what it accepts: an atom with `pair is None` is exempt only if
   the correction's window covers the atom's own base, or the atom's base resolves (F1).
5. Bind `path` atoms to the sentence that cites them, or at least forbid an atom whose *basename*
   exists at a different digit (F2/F2b) — cheapest honest form: require the cited receipt's own
   `rev` field to equal the row's `measured at` cell.
6. Add the freeze guard `exact.py` already has, or remove "both counters" from the claims sentence and
   cite `exact.py` as the lane-wide freeze gate (F7).
7. If the record keeps "over 50 atoms", annotate it with `at <REV>` so the drift in F8 is a stated
   limit instead of an unqualified number.

## Limits of this probe (what I did not test)

- Only `SCORECARD.md` atoms were mutated; `tools/round-47/record.py`'s own clauses were not
  falsified beyond the `--freeze` observation (that is `MutRecordClauses`'s probe).
- No domain fixture, no network, no second runtime was invoked; no claim verdict is offered.
- The lane advanced during the probe (`caafeffa` → `07d2894e` → later). All numbers are pinned to
  `07d2894e`; A4 numbers are pinned to `1e2c310295`.
- `M9`/`M10`/`M14` are non-digit mutations and are labelled as such; M15 is a digit mutation.
- Exit code 2 (could-not-evaluate) did not arise for `record.py` on any probe; every probe evaluated.

## Restoration evidence

- Fixture `$S/fix` started at `07d2894eabe88c326e9036262f20ad02662c860d`; `git rev-parse --show-toplevel`
  asserted `== /fast/scratch/hyaku/kaidoku-r47/MutRecordAtoms/fix` before every commit (all commits used
  `-c user.name=mut -c user.email=mut@invalid`, fixture-local only).
- Baseline `SCORECARD.md` sha256 `1212d2736b563e2d566731428185e30e7892c00023c6752d535411816b22d826`
  (`git show 07d2894e:SCORECARD.md | sha256sum` = same). Each mutant commit's card sha256 is recorded in
  `receipts/log.json` (`card_sha256_mutated`).
- After the last probe: `git reset --hard 07d2894e…`; on-disk `SCORECARD.md` sha256 equals the baseline
  hash (asserted in the driver; the run printed `restored True base 07d2894e…`), `git status --porcelain`
  shows only `?? .receipts/`.
- The lane tree was opened read-only: no write, no git mutation, no install. The scratch clone under
  `/fast/scratch/hyaku/kaidoku-r47/MutRecordAtoms` was removed after these receipts were copied here.

## Receipts

`receipts/M0-baseline.json`, `receipts/M{1,2,3,4,5,6,7,8,9,10,12,13,14,15}-*.json`,
`receipts/base.json` (same as M0), `receipts/at-A4.json` (50-atom A4 re-measurement),
`receipts/exact-at-head.json` (C1 counter, exit 2 `frozen_path_changed`), `receipts/log.json`
(every probe with command, commit, exit, UTC, stdout sha256).
