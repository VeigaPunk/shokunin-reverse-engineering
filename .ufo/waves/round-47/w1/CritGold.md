# CritGold — round 47: the gold-plated forgery over both frozen claims

Seat: critic, wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, lane HEAD at
review time `1e2c3102952dc636650095643c1963c833859019`, declared freeze for the current bytes
`1e2c3102` (`git log --format=%H -1 -- plans/round-47-claims.md` → `62e33f7d`, but `record.py`
changed at A2–A4, so the freeze that makes C1 evaluate is the tip; see F-C1-5).
Frozen bytes read only; all mutation happened in fixture clones under
`/fast/scratch/hyaku/kaidoku-r47/CritGold/` (removed after the receipts were copied here).
Installs: none. No lane file, receipt, or `.ufo/state` path was written by this seat.

**Verdict: both predicates are too weak — the gold-plated forgery passes both, exit 0, at one
revision.** The forgery is two edits and requires none of the round's work: permute the four arm
tokens (and blank the four `v2 hole` cells, and set every `exit` to `0`), and *delete* the two
round records down to five tautologies, adding corrections that exempt nothing. This is the
round-47 honest-stop: a green `c1-at-*`/`c2-at-*` pair does not establish that block 24 states the
exactness matrix or that the record was re-derived, only that whatever text survived is
self-consistent.

| claim | genuine @ `1e2c3102` | forged @ `d495835c` | discriminated? |
|---|---|---|---|
| R47-C1 `exact.py --profile v3` | exit 0, `met_target true` (`receipts/genuine-c1.json`) | exit 0, `met_target true` (`receipts/final-c1.json`) | **no** |
| R47-C2 `record.py` | exit 0, `met_target true` (`receipts/genuine-c2.json`) | exit 0, `met_target true` (`receipts/final-c2.json`) | **no** |

## The artefact

Fixture: a `git clone --no-hardlinks` of the lane at `1e2c3102` in scratch (toplevel asserted
`== $D` before the first commit), five commits on top:

| commit | edit |
|---|---|
| `9fc5b49f` | block-24 table rows replaced (below); round-45/46 bodies → 2 sentences each; 2 corrections |
| `1c178823` | corrections → 3 lines, none of which exempt anything (**exit 0 for both counters**) |
| `27ad6cb` | + `- corrects window round-3: …` and `- corrects axes depth: 24/24` |
| `6b93eeb` | a `0425224..<tip>` placeholder window appended *inline* (silently swallowed, F-C2-8) |
| `d495835` | the same placeholder on its own line — exempted by `empty in X..X` (**exit 0**) |

`git diff --stat 1e2c3102 d495835` → `SCORECARD.md | 163 +---…`, `SKILL.md | 8 +--`,
**14 insertions, 157 deletions**: the forgery is 12 lines of new text and 157 lines removed.

The block-24 table the counter accepts (semantically the inverse of the landed one — every row
names the *wrong* arm, no row states a hole, every exit claims `0` = met):

```
| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 | n/a | `order` | 0 |
| R46-CL3 | n/a | `digest` | 0 |
| R46-CL4 | n/a | `symbol` | 0 |
| R46-CL6 | n/a | `once` | 0 |
```

The five surviving record atoms, one per class, all tautologies:

```
## Round 45 — gutted
Waves: 40 + 36 = 76 seats. `git log 1e2c3102..1e2c3102 -- corpus/knowledge/` is empty. See `.ufo/waves/round-45/w1-dispatch.json`.
## Round 46 — gutted
Waves: 40 + 40 = 80 seats. `git log 1e2c3102..1e2c3102 -- corpus/knowledge/` is empty. See `.ufo/waves/round-46/w1-dispatch.json`. Base `1e2c3102`.
```

and the corrections section, none of whose four lines exempts anything except one placeholder:

```
- corrects seats round-45: 2 waves, 76 seats total
- corrects path .ufo/waves/round-45/w1-dispatch.json: present at the measured revision
- corrects window round-46: empty in 1e2c3102..1e2c3102 -- corpus/knowledge/
- corrects window round-3: empty in 1e2c3102..1e2c3102 -- corpus/knowledge/
```
(`- corrects axes depth: 24/24` is additionally in the card and is *invisible* — F-C2-6.)

## Commands and exits

```
$ python3 -I -B tools/round-47/exact.py --root $D --freeze 1e2c3102952dc636650095643c1963c833859019 \
      --rev d495835cb6ef8096a83b1e511c090ddb638b1355 --json-out receipts/final-c1.json
exit 0 · stdout sha256 b4b6b318332c0bdca1262d8c283b3040ef4288629b3e057e4824a8ee06173427 · 17:58:18Z
  met_target true, failing [], battery forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0

$ python3 -I -B tools/round-47/record.py --root $D --rev d495835cb6ef8096a83b1e511c090ddb638b1355 \
      --json-out receipts/final-c2.json
exit 0 · stdout sha256 d5c0a3e96551cfbf0f22cf0b221cc10f3f26ff8c9d1bcd2d3887addd7a019b56 · 17:58:20Z
  met_target true, failing [], atoms 10, verified 9, exempted 1, corrections 4, corrections_bad []
```

`receipts/` holds the JSON for every run named here, plus the genuine pair at `1e2c3102`
(`genuine-c1.json` exit 0, `genuine-c2.json` exit 0). `rebuild.sh` in this directory recreates the
whole fixture from the lane and re-scores it; an independent run from a fresh clone reproduced
`C1 exit=0` / `C2 exit=0` with fixture rev `7790c879` (`receipts/rebuild-c1.json`,
`receipts/rebuild-c2.json`, stdout shas `5a21c6ab…` and `f64c91d9…`).

A second fixture (`fx-noop`, lane clone + block pin untouched, all four mutation bodies emptied and
`interpreter_sha256` re-stated, commit `b972bf3`, `receipts/noop-c1.json`):

```
$ python3 -I -B tools/round-47/exact.py --root $D --freeze b972bf3… --rev b972bf3… 
exit 0 · forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0
  fixtures: [('substring-arm','mutation was a no-op'), ('duplicate-routed-id','mutation was a no-op'),
             ('stale-mutations-digest','mutation was a no-op'), ('flag-order-drift','mutation was a no-op')]
```

The battery of an emptied counter reports exactly the numbers of the genuine one.

## Findings — R47-C1 (depth), `tools/round-47/exact.py`

**F-C1-1 predicate too weak — the arm column binds membership, not correspondence; the exit column
binds nothing.** Clause 5 is `a in VOCAB`, and no clause relates a row's `R46-CLn` to its arm, or
its `exit` to the defect's detection class. My four rows name the wrong arm for every defect and
claim `exit 0` ("met") for four defects that were routed violations; exit 0, `failing []`.
*Smallest safe correction:* replace membership with a fixed map — `EXPECT = {"R46-CL2":"symbol",
"R46-CL3":"once","R46-CL4":"digest","R46-CL6":"order"}` — require `exit == "1"` on all four rows
(each routed defect is detected, not tolerated), and require each `v2 hole` cell to state a
mechanism (`len(cell.split()) >= 6`, no placeholder token) so a table of `n/a` cannot stand in for
a matrix.

**F-C1-2 defect in a frozen clause — a no-op mutation is booked as a hole measured.**
`run_battery`: `if text == block and not overrides: … out["v2_green"] += 1; continue`. Emptying
the four mutation bodies keeps `forgeries_total 4 / v2_green 4` and exits 0 (receipt above).
Clause 9's "the four forgeries mutate the landed block … one defect class at a time" is therefore
unfalsifiable by the instrument that is supposed to test it.
*Smallest safe correction:* a no-op is an instrument error — set `out["noop"] += 1`, add
`battery.noop == 0` to the clause-9 tuple, and require each red fixture's `v3_failing` to contain
the class-specific message it was built to trip (otherwise a mutation that trips a *neighbouring*
clause counts as discriminating).

**F-C1-3 defect — `mutations_sha256` pins names, not behaviour.** `MUT_DIGEST` is sha256 over
`"\n".join(name for name, _ in MUTATIONS)`. Deleting all four function bodies leaves the digest
and the pin valid (same receipt). Clause 6's purpose ("deleting a mutation changes the denominator")
is met only for the *count*, while the denominator's content is now empty.
*Smallest safe correction:* digest `name + "\n" + inspect.getsource(fn)` per entry (source is
stable for a frozen file), or pin a second `mutations_body_sha256` over the four function bodies.

**F-C1-4 defect — `interpreter_sha256` is self-consistency, not provenance.** The pin is the digest
of the file the forger edits, restated in the same commit; no clause compares either pin to
`--freeze`. The A1–A4 series is the same pattern at lane scale: each amendment edited a frozen
path and re-declared the freeze, which is why `frozen_path_changed` is empty in every green
receipt.
*Smallest safe correction:* require `interpreter_sha256 == sha256(exact.py at --freeze)`, and
derive the freeze rather than accept it: `git log --diff-filter=A -1 --format=%H -- tools/round-47/exact.py`.

**F-C1-5 defect — `freeze == rev` makes the frozen-set arm vacuous.** `c1-at-A4.json` (the lane's
own green C1 receipt) carries `freeze 1e2c3102 == rev 1e2c3102`; `freeze_state` then compares a
commit with itself and reports `frozen_path_changed []` by construction. My C1 forgery is also
scored at `--freeze 1e2c3102` (a *different* commit, honest for the frozen paths, which I did not
touch).
*Smallest safe correction:* exit 2 `degenerate_freeze` when `freeze == rev`, or require the freeze
to be the add-commit of the frozen paths from the previous bullet.

## Findings — R47-C2 (calibration), `tools/round-47/record.py`

**F-C2-1 predicate too weak — content is unbound; deletion is cheaper than correction.**
`collect()` can only see atoms that are present. Round-45+46 lost 157 lines (both full sections,
~14 kB of record) and the counter reports `mismatches []`: the two atoms the real landing had to
*research and correct* were simply removed. Nothing compares the sections to what they held at
their own landing, so "the record was repaired" and "the record was emptied" are the same receipt.
*Smallest safe correction:* atom monotonicity — for each of the last two rounds, every atom found
in `SCORECARD.md` at that round's landing commit (`git show <landing>:SCORECARD.md`) must still
appear, or be named by a `corrects` line; add `atoms_lost == 0` to clause 1.

**F-C2-2 predicate too weak — `X..X` is an unfalsifiable window.** `window_empty(X, X, paths)`
is `git log X..X` → empty for every X and every pathspec, in both the atom form and the correction
form. All four window atoms/corrections in my fixture are `X..X`.
*Smallest safe correction:* `base == tip` → `unverifiable` (and `base` must be a strict ancestor
of `tip`), in `derive()` and in `corrects()`.

**F-C2-3 predicate too weak — a correction that corrects nothing satisfies clause 3.**
`exempt()` is consulted only for red atoms and `corrects()` never asks whether the atom it names
was red. Three of my four correction lines point at atoms that already verify, and
`corrections 3 / corrections_bad []` passes.
*Smallest safe correction:* score the card twice, with and without exemptions, and require every
correction to be load-bearing (`corrections_idle == 0`), or at least `len(corr) == len(exempted) +
historical`.

**F-C2-4 predicate too weak — a placeholder atom is exempted by an irrelevant window.**
`exempt()` returns `True` for any pair-less atom without reading the correction's window, so the
round-46 `0425224..<tip>` sentence — which `derive()` itself calls `unverifiable`, counting as a
mismatch per the claims file — is excused by `empty in 1e2c3102..1e2c3102 -- corpus/knowledge/`,
which shares neither revision nor pathspec with it. Exit 0, `exempted 1`.
*Smallest safe correction:* drop the pair-less escape and require an atom's own window to be
concrete (`unverifiable == 0` outright); if an exemption must survive, require the correction's
pair to be concrete *and* its trailing pathspec to equal the atom's.

**F-C2-5 predicate too weak — the historical escape accepts a round that does not exist.**
`- corrects window round-3: empty in X..X -- corpus/knowledge/` passes: the `historical` branch
only tests `int(key) < oldest`, and the window branch never consults dispatch files (the seats
branch does).
*Smallest safe correction:* require `.ufo/waves/round-<key>/w1-dispatch.json` at rev, and the
atom present in the card at that round's landing.

**F-C2-6 defect — `axes` corrections are unreachable; the claim's clause 3 sentence about them is
unimplemented.** `CORR = ^- corrects (seats|window|path|rev) …` excludes `axes`, so the
`if cls == "axes"` branch in `corrects()` is dead. Adding `- corrects axes depth: 24/24` left
`corrections` at 3 → 4 for two added lines, i.e. the axes line was ignored, not validated.
Consequence: a wrong `## Owned axes` fraction has **no** exemption route (fatal, fine) while the
claims file promises one (misleading), and a mistyped class silently disappears instead of
erroring.
*Smallest safe correction:* add `axes` to `CORR` (the branch already exists), and make an
unrecognised `- corrects` line an error rather than a no-match.

**F-C2-7 defect — a no-op forgery is booked green, so the battery punishes an absence.** With no
`seats` correction in the card, `wrong_total()` returns the card unchanged and
`run_battery` does `forgeries_green += 1` → `failing: battery forgeries_green 1 != 0`. Observed in
my first forgery attempt (`receipts/gold-c2.json` lineage) and in the lane's own A2 red-before
(`c2-at-L1.json`). The counter goes red for the *shape of the text*, not for a false claim — and
the cheapest way to fix that red is to add a correction line, which is how F-C2-3 gets exploited.
*Smallest safe correction:* a no-op forgery is exit 2 / `forgeries_noop`, never a verdict.

**F-C2-8 defect — only the first `A..B` on a line is checked.** `WINDOW.search` per line, one atom
per line: in commit `6b93eeb` a `0425224..<tip>` window sat next to a true `X..X` window on the
same line and produced no atom at all (atoms 9, not 10). An unverifiable claim hides one line
away from a verified one.
*Smallest safe correction:* one atom per `WINDOW.finditer` match, with the tail taken from that
match.

**F-C2-9 note — `rev` atoms bind resolution and ancestry, not the claim.** Any backticked 7–40 hex
that resolves and is an ancestor passes, so "measured at `X`", "base `X`", "landing `X`" are all
the same atom; a card may cite `X` for a measurement made at `Y`. Low severity for this round
(the genuine card's revs are real) but the class is named in the claims file as if it were bound.

## What the L1 can land without re-opening the freeze

Nothing above requires new round-47 work; each correction is a 1–5 line change in a file already
frozen. The order that costs least:

1. F-C1-2 / F-C2-7 first (a no-op must be an error, not a verdict) — they are the two holes that
   make every other battery number unfalsifiable.
2. F-C1-1 (fixed arm map + bound exit column) and F-C2-1 (atom monotonicity) — the two findings
   that make the claims mean what their titles say.
3. F-C2-2 / F-C2-4 / F-C2-5 (window must be strict and path-matched; no placeholder laundering).
4. F-C1-3 / F-C1-4 / F-C1-5 and F-C2-6 / F-C2-8 — hygiene: pin what is measured, derive the
   freeze, wire the dead branch, parse every match.

If none of these land, the honest description of the round is: *block 24 has the right shape and
`record.py` is self-consistent*, not *the exactness matrix is stated* and *the record was
re-derived*. The forgery above is 12 inserted lines and passes both.

## Provenance

- Lane read-only: `git log/show/status/rev-parse` only; no mutating git command outside the
  fixture clones (each `git -C "$D" rev-parse --show-toplevel` asserted `== $D` before the first
  commit; identity `fx@round47` set inside the fixture only).
- Fixture roots `/fast/scratch/hyaku/kaidoku-r47/CritGold/{fx-gold,fx-noop}` were removed after
  `receipts/` was copied here; `rebuild.sh` regenerates them.
- Receipts here are the counters' own stdout, byte-identical to `--json-out`; the sha256 in the
  table above is of that stdout.
