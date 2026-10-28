# RevC2Exempt — attack on the R47-C2 exemption path

Seat: `RevC2Exempt` (leaf, no dispatch). Lane read-only throughout; every write is under
`/fast/scratch/hyaku/kaidoku-r47/RevC2Exempt` (removed after the receipts were copied into
`receipts/`) and this report directory. No installation was made (nothing needed).

Instrument generations attacked, because the lane moved while I reviewed:

| label | rev | `record.py` sha256 | note |
|---|---|---|---|
| ticket freeze | `5017e1f7` | `af666ce2…` | carries the window-pair clause A1 later deleted |
| A2 | `62e33f7d` | `fb6d5735…` | first instrument whose bytes score the landing |
| A5 (current) | `a631bba0` (bytes frozen at `07d2894e`) | `abf35257…` | adds the "historical correction" allowance and the in-section ghost forgery |

Landing card measured at `07d2894e`; base at `13a9e9e1`. Every number below is from a command
whose stdout is in `receipts/` with its sha256 and UTC time in `receipts/manifest.txt`.

## The answer to the question asked

**Yes.** With `EXEMPT_MAX = 3` a round can exempt exactly the atoms it falsified and never
correct them: three true statements (two `seats`, one `window`) turn three false atoms green
while the card keeps every one of the false sentences. The fourth false atom is caught:

| fixture | exit | failing | mismatches |
|---|---|---|---|
| `receipts/fixture-F1a-SCORECARD.md` (3 exemptions, 3 false atoms) | **0** | `[]` | `[]`, `exempted [seats 45, seats 46, window 46]` |
| `receipts/fixture-F1b-SCORECARD.md` (+ a fourth false atom) | **1** | `['mismatches 1 != 0']` | `[path .ufo/waves/round-46/w9/ghost.json]` |

Receipts `r03-a5-at-fx-three` (exit 0) and `r04-a5-at-fx-fourth` (exit 1), instrument A5.

Command (the fixture is a `git clone --shared` of the lane at `62e33f7d`, then the two cards in
`receipts/` committed in file order):

```sh
git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/fx
git -C $S/fx config user.email revc2@r47 && git -C $S/fx config user.name revc2
cp receipts/fixture-F1a-SCORECARD.md $S/fx/SCORECARD.md && git -C $S/fx commit -qam F1a
cp receipts/fixture-F1b-SCORECARD.md $S/fx/SCORECARD.md && git -C $S/fx commit -qam F1b
python3 -I -B $S/inst-a631bba0/round-47/record.py --root $S/fx --rev <commit>
```

The F1b card's fourth false atom is inserted into the round-46 body as
`Receipt \`.ufo/waves/round-46/w9/ghost.json\`.`; the three exemptions are
`- corrects seats round-45: 2 waves, 76 seats total`,
`- corrects seats round-46: 2 waves, 80 seats total`,
`- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md`
(all three re-derive, `corrections_bad []`), and the falsified round-46 seat atom reads
`Waves: 41 + 40 = 81 seats`.

So the cap is real but the *mechanism* is not a repair: see F1.

## Findings

### F1 (HIGH) — exemption is a substitute for correction, and nothing ties it to the atom

`exempted` counts atoms whose `derive()` failed and for which some correction line matches
class+key. The atom's own text is never re-read, so a *true* statement about the repository
retires a *false* statement in the card without editing it. This is not a corner case: it is
how the landing passes.

Evidence, landing card, instrument A5:

```
$ python3 -I -B <inst-a631bba0>/round-47/record.py --root <lane> --rev 07d2894e
exit 0; atoms 41 {axes 2, path 8, rev 28, seats 1, window 2}; verified 40;
exempted [window 46]; corrections 2; corrections_bad []; battery 3/0
```
(`receipts/r01-a5-at-landing.out`, exit 0)

The card at that same revision still says:

- `SCORECARD.md:3527` `Wave 1: 40 seats; wave 2: 32 seats (counts from …` — the dispatch files
  (`git show 07d2894e:.ufo/waves/round-45/w2-dispatch.json` → `{"spawn": 36, "resume": 0,
  "total": 36}`, same at `a631bba0`) report `counts.spawn 36`;
- `SCORECARD.md:3635` `0425224..<tip> -- tools/round-46 plans/round-46-claims.md\` is empty …` —
  a window no command can resolve.

At `e856beb5` (the first landing) both of those were **exempted**, and the counter exited 0:
`exempted [seats 45, window 46]` (`receipts/r08-panels-a2.out`, panel `P0-landed-card`).
So the two record defects the round was created to repair (R46-V1, R46-V2) are still in the
record and the counter says met.

Content blindness is total: a card whose round-45 atom says `wave 2: 90 seats` is exempted by
the same `2 waves, 76 seats total` line (`receipts/r09-panels-a2b.out`, `Q4`, exit 0), and two
mutually contradictory seat atoms in one round are both exempted by one statement
(`receipts/r10-panels-a5.out`, `R3`, exit 0). Because the key is the round number, one line
covers every seat atom in that round: a round-45 pair claim plus a contradictory round-45 sum
claim, both false, are retired by the single `- corrects seats round-45` line (`exempted` counts
both atoms; write a third false seat atom in that round and the cap trips at `exempted 4 > 3`,
`r08` panels `P4` exit 0 and `P4b` exit 1).

**What the claim must say.** Predicate clause "Each `- corrects <class> <key>: <statement>` line
exempts the atoms it names and is itself re-derived" must become a binding, e.g.: *a correction
exempts an atom only if the correction `(class, key)` equals the atom's `(class, key)`, the
statement re-derives, **and** the statements's own figures differ from the atom's figures
(the atom's claim is contradicted, not merely retired); at most one atom per `(class, key)`
may be exempted, so `len(exempted) <= len({(c.class, c.key) for c in corrections})`.* Without the
contradiction clause the exemption is a licence to leave a false sentence in the record.

### F2 (HIGH) — a correction may name a round the card never contains (A3 allowance)

`evaluate_text` accepts any `seats`/`window` correction whose key is a decimal number smaller
than the oldest round in the fold, without checking that the card contains that round:

```sh
# card = landed card + "- corrects window round-3: empty in 13a9e9e1..13a9e9e1 -- corpus/"
exit 0; corrections 3; corrections_bad []
```
(`receipts/r10-panels-a5.out`, `R1`)

Worse, that phantom line is enough to satisfy `CORR_MIN` and to grant the exemption:
`- corrects seats round-45: 2 waves, 76 seats total` plus
`- corrects window round-3: empty in 13a9e9e1..13a9e9e1 -- corpus/` gives
`corrections 2, corrections_bad [], exempted [window 46]`, exit **0** through the full CLI
(`R1b`). Round 3 exists nowhere in `SCORECARD.md`; the exemption it grants is of the round-46
window atom, and `git log 13a9e9e1..13a9e9e1 -- corpus/` is empty for the trivial reason that
the window has no commits.

This is a direct code-vs-claim divergence: the claim says *"A correction that exempts an atom the
card does not contain is itself a defect"*, and the `A3` allowance ("a correction for a round
older than the window stays valid evidence") makes exactly that case legal.

**What the claim must say.** Either drop the allowance, or bind it: *a historical correction is
accepted only when `## Round <key>` occurs in the card at `--rev` and a `seats` correction for
that round still re-derives from its dispatch files; a `window` correction for a round with no
atom in the card is always a defect.*

### F3 (HIGH) — the fold advances, so a round's record defects leave scope unexamined

`sections()` takes the **last two** `## Round N` headings. Because the round must write its own
section, one round's false atoms are examined only until the next round's section lands. At the
landing rev the fold is `round-46, round-47`: the round-45 seat atom is not in the atom set at
all, and `- corrects seats round-45` exempts nothing (it passes only because A3 calls it
historical — `r01` receipt shows `exempted [window 46]`, one atom, not two).

The round's own C2 row is measured on the pre-fold card and reports the other scope:

- `SCORECARD.md:3698` — "over **50 atoms** … `exempted 2 <= 3` … measured at `1e2c310295`";
- `.ufo/waves/round-47/l1/scores/c2-at-A5.json` (the receipt the row cites) — `rev 07d2894e`,
  **`atoms 41`**, `exempted 1`.

Both are true *of different atom sets*, which is the R46-V3 defect class (a cell naming the wrong
revision) landing inside the round that claims to have repaired it. And the "before/after" pair is
not the same measurement: `4 mismatches → 0` compares the base fold (rounds 45+46) against a fold
(rounds 46+47) in which one of the four has been removed by the fold, not corrected.

Proved with the A2 instrument: landed card + a `## Round 47` heading, corrections kept →
`corrections_bad ['exempts an atom that does not exist']` (`r08`, `P2`); corrections reduced to
the ones that name in-fold atoms → the round-45 false sentence is simply never read.

**What the claim must say.** *The before and the after are measured over the same atom set: the
counter folds the last two rounds at both revisions, or it folds the two rounds the claim names;
a round's own section does not retire an atom the claim's before-cell names, and the after-cell is
measured at the revision the row names (`rev` in the receipt must equal the row's cell).*

### F4 (HIGH) — C2 has no freeze guard; the frozen bytes changed five times after the freeze

`record.py` has no `--freeze`, no `frozen_path_changed`, no dirty arm
(`receipts/r11-record-help.out`: `usage: record.py [-h] --root ROOT --rev REV [--no-battery]
[--selftest] [--json-out JSON_OUT]`). The claims file says "Nothing in this file or in
`tools/round-47/` changes after the freeze: a change makes both counters exit 2
`frozen_path_changed`." That sentence is true of `exact.py` and false of `record.py`:

```
$ python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f --rev a631bba0
exit 2 reason frozen_path_changed
  ["plans/round-47-claims.md", "tools/round-47/", "tools/round-47/record.py"]   # r06
$ python3 -I -B <inst-5017e1f>/round-47/record.py --root <lane> --rev a631bba0
exit 1                                                       # r05; no freeze field at all
```

The instrument that ran the landing is not the instrument that was frozen: `tools/round-47/record.py`
changed in A1 (`9018c53b`), A2 (`62e33f7d`), A3 (`2e4ae434`), A4 (`1e2c3102`), A5 (`07d2894e`).
Under the ticket's freeze `5017e1f`, C1 cannot score at all (exit 2, `r06`); only at the
self-declared A5 freeze does it score (`r07`: exit 0, `rows 4`, `refs 8`, battery
`4 / 4 / 0 / 1 / 0`, both pins equal to the bytes at rev).

**What the claim must say.** *C2's counting command takes `--freeze` and calls
`gate.freeze_state(root, freeze, rev, "plans/round-47-claims.md")` first; a changed frozen path is
exit 2 with `met_target` absent, for both counters.* Until then the sentence must be deleted, and
the ticket's freeze (`5017e1f`) cannot be the grading freeze for either claim.

### F5 (MID) — the `axes` correction form the claim specifies cannot be parsed

`CORR = ^- corrects (seats|window|path|rev) (\S+): …` excludes `axes`, so an `axes` line is not a
correction at all, and `corrects()`'s `axes` branch is dead code (it also appears twice — the
second block is leftover from `derive`). Consequence on the landed card: the two lines
`SCORECARD.md:3675` and `:3677` (`- corrects axes coverage: 138/138`, `- corrects axes depth:
24/24`) are inert — `corrections` is 2, not 4 — and if an axes atom were false no correction could
exempt it:

```
card + "- corrects axes coverage: 138/138"      -> corrections 1 (axes line unparsed)
card with coverage head 133/133 + that line     -> mismatches [window 46, axes coverage], exit 1
```
(`receipts/r13-axes-correction.out`)

This is the same unreachable-clause class as A1: the claim promises "an `axes` correction must
state `<resolved>/<total>`" for a class the parser rejects.

**What the claim must say.** Either add `axes` to `CORR` and to `corrects()`'s key existence
check, or delete the axes sentence and say axes atoms are repaired in place in the `## Owned axes`
row and never exempted.

### F6 (MID) — a window correction need not share a pathspec with the atom it exempts

`exempt()` returns `True` for any placeholder window atom (`atom["pair"] is None`) whenever *any*
window correction exists in the class. The atom's own pathspec (`tools/round-46
plans/round-46-claims.md`) is never compared with the correction's:

```
card + "- corrects window round-46: empty in 332f4884..58eb04b6 -- corpus/lessons/"
exit 0; exempted [window 46]                                  # r10, R2
```

and a vacuous pathspec re-derives "empty" too: `-- corpus/no-such-tree/` and
`-- .ufo/waves/round-46.` (trailing dot) both give `corrections_bad []`, exit 0 at clause level
(`r09`, `Q1`, `Q2`; control: the same window over a real path is non-empty, `Q3` exit 1). The CLI
does go red on the vacuous pathspec, but only accidentally: the battery's `correction-window-not-empty`
forgery rewrites the window to `root..rev` over the *same* pathspec, which is empty when that
pathspec matches nothing, so the forgery stops being a forgery (`forgeries_green 1`,
`r08`/`P3`, `P7`). The diagnosis it prints names the battery, not the vacuous pathspec.

**What the claim must say.** *A window exemption requires the correction's pathspec set to equal
the atom's pathspec set and its `A..B` to be the concrete replacement for a placeholder; a
pathspec that selects no file at either end of the window is a defect, not an empty window.*

### F7 (MID) — the battery is coupled to the landing's shape, not to the correction's content

The three forgeries mutate the landing's own corrections. `wrong_total` is a no-op when the
corrections section has no `seats` line, and `non_empty` is a no-op when it has no `window` line;
`forged()` credits a no-op as `forgeries_green += 1`. So a *correct* record repaired in place with
only `path`/`rev` corrections fails clause 6:

```
card repaired in place; corrections = ["- corrects path .ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json: landed",
                                       "- corrects rev 781e19ae: measured"]
clauses 1-5 exit 0; full CLI exit 1  "battery forgeries_green 2 != 0"    # r09, Q5/Q6
```

and, symmetrically, two corrections that exempt nothing pass every clause (`r08`, `P5`: repaired
record + the two original lines → exit 0, `exempted []`), while the same clean record *without* a
corrections section fails `corrections 0 < 2` (`P5b`). `CORR_MIN 2` is therefore a floor on the
number of statements, not on repairs; the round's own record already lists "`CORR_MIN 2` is a floor
on corrections, not on their importance" as routed, so this is a second, sharper instance.

**What the claim must say.** *The battery's forgeries are built against a fixed minimal card
shipped with the counter, not against the landing's corrections section; a forgery whose mutation
is a no-op is a harness error (exit 2), never a green.* Then `CORR_MIN` should bind repairs:
`corrections` counts only lines that exempt a failing atom or contradict an atom in place.

### F8 (LOW) — battery green while nothing was scored (pre-A5 state, for the record)

At the base rev, `run_battery` reports `correction_forgeries 3`, `forgeries_green 0` with all three
fixtures carrying `error: "no corrections section"` (`receipts/r02-a5-at-base.out`). Clause 6 is
satisfied in a state where no forgery was scored. A5 fixed only the ghost forgery's placement; the
no-section path still credits `3 / 0`.

## What the L1 can keep

- C1, at the A5 freeze, is genuinely discriminating: the receipt `r07` shows the four forgeries
  `v2_exit 0 / v3_exit 1` each, `genuine_exit 0`, `crash 0`, and both pins equal to the bytes at
  `a631bba0` (`interpreter_sha256 dcef54f1…`, `mutations_sha256 19a2166e…`). I found no way to
  satisfy block 24's clause 5/6/7 without the exact tokens, the digest over the counter's own
  name list, or the flag order.
- C2's `seats`, `path`, `rev` derivations are sound and do catch fabricated atoms: an invented
  path, an unresolvable rev, and a wrong dispatch total are all red and cannot be exempted
  (a correction for them must itself re-derive from the same bytes — `r04`, `r13`).
- The cap is enforced: four exemptible atoms → `exempted 4 > 3`, exit 1 (`r10`, `R4`).

## Reproducibility note (also a claim defect)

The claims file's C1 counting command is not runnable as written: `exact.py` needs
`HYAKU_SCRATCH` or a non-`/tmp` `TMPDIR` and otherwise exits 2:

```
$ env -u TMPDIR -u HYAKU_SCRATCH python3 -I -B tools/round-47/exact.py --root <lane> \
    --freeze 07d2894e --rev a631bba0
exit 2  {"reason": "no HYAKU_SCRATCH/TMPDIR root set"}        # receipts/r12-exact-no-scratch.out
```

The claim must state the environment the counting command requires (the round-46 core refuses
`/tmp` by design, R45-CL20).

## Doc drift in the frozen claims file

`plans/round-47-claims.md` at the declared freeze still reads "the freeze is a series of two"
(A1 paragraph) and carries only the A1 and A2 paragraphs, while `SCORECARD.md:3682` says "a
disclosed series of six" and names A3/A4/A5 as the declared freeze. A frozen file that is one
amendment behind its own record is the same class of defect it reports.

## Verification gaps / not run

- I did not attack R47-C1's clause 1–4 text (rows, header, cardinality) beyond running the counter
  at `a631bba0` and reading its `failing`/battery receipt; the C1 seat work is not mine.
- I did not build a fixture for a *forged* `rev`/`path` exemption: `corrects()` re-derives both
  against the same bytes, so the only route is the ghost case (`corrections_bad`), which A5's
  battery already covers.
- All refs cited are fixed revisions readable with `git show`; the lane kept moving during the
  review (HEAD was `9018c53b` at my first command and `a631bba0` at my last), so re-measure
  before quoting any number at a moving tip.
