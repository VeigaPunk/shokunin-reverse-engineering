# C2CorrGrammar — correction-grammar agreement, end to end (round 47, wave 1)

Seat: `C2CorrGrammar`. Lane root `kaidoku-shokunin`. Frozen rule read at
`plans/round-47-claims.md@5017e1f7299c3a812e87e7950148f54313dd279e` (R47-C2 §"Landed
surface"/"Predicate"). Lane tree read-only throughout: every card was written in a **clone**
of the lane at the freeze, committed there, and scored by the frozen counter.

## 0. Method and the two counter states

Fixture: `git clone` of the lane into scratch, branch at `5017e1f7`; each case rewrites
`SCORECARD.md`, commits, and is scored twice with the same command:

```sh
python3 -I -B <counter> --root <fixture-clone> --rev <case-commit> --json-out <receipt>
```

| state | bytes | sha256 | status |
|---|---|---|---|
| `frz` | `git show 5017e1f7:tools/round-47/record.py` | `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` | the frozen rule |
| `a1` | lane `tools/round-47/record.py` | `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` | the amended counter; **uncommitted while this seat measured**, committed later in the series A1–A6 (§5) |

Both were captured byte-identical for every one of the 15 cases (`counter_sha256` per run in
`C2CorrGrammar/ledger.jsonl`). `a1` differs from `frz` in four places (§5). Case commits, exit
codes, stdout sha256 and UTC times are in the ledger; receipts are under
`C2CorrGrammar/receipts/`. The measurement ran while the lane was landing (`HEAD` moved
`3186f69b → 09a9f912`); the fixture clone is cut at `5017e1f7` and is unaffected by that.

Conclusions are about the *mechanism*, measured on a realistic card (the freeze
`SCORECARD.md` with only the named sentences changed), not about the live 45/46 atoms.

## 1. The refused text — the round-45/46 appendix wording

Text A, pasted verbatim under the required heading:

```markdown
## Record corrections — round 47

- corrects seats round-45: Wave 1: 40 seats; wave 2: 36 seats (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)
- corrects window round-46: `git log 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above
- corrects axes coverage: 138/138
```

Case `c02-foreign-wording`, rev `861ae30e`. Exit 1 under **both** states. Verbatim refusals
(`corrections` = 2, i.e. the third line is not even counted):

```
a seats correction must state '<n> waves, <total> seats total'
   line: - corrects seats round-45: Wave 1: 40 seats; wave 2: 36 seats (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)
a window correction must state 'empty in A..B -- paths'
   line: - corrects window round-46: `git log 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above
```

`failing` = `mismatches 2 != 0` (the two `axes` atoms), `corrections that do not re-derive:
2`, `battery forgeries_green 2 != 0`.

Three things to read off this receipt:

1. **The refusal is real.** Wording copied from the round sections does not buy a green.
2. **The atoms still disappear from `mismatches`.** The `seats` and `window` atoms are in
   `exempted` even though both corrections are invalid: exemption is applied before the
   correction is re-derived (`record.py:326-345` builds `exempt` from parsed lines only).
   So `mismatches == []` is not evidence that an atom re-derived — see §4.1.
3. **`axes` is not part of the grammar at all.** `CORR = re.compile(r"^- corrects
   (seats|window|path|rev) (\S+):\s*(.+)$")` (`record.py:50`) has no `axes` alternative, so
   `- corrects axes coverage: 138/138` is invisible: it is neither parsed, nor counted, nor
   complained about. `corrects()` nevertheless carries an `axes` branch
   (`record.py:280-289`, duplicated and unreachable at `record.py:292-298` where it references
   an undefined `atom`), so the claims file's clause 3 sentence "an `axes` correction must state
   `<resolved>/<total>`" (`plans/round-47-claims.md:147`, frozen numbering; +21 lines in the
   working tree after A1/A2) describes a line the parser cannot reach. Case `c05` proves it:
   adding both axes lines to an otherwise identical card leaves `corrections` at 2 and leaves
   both axes mismatches in place.

Also note what the battery did here: `wrong_total` and `non_empty` find no anchor in this
wording, return the card unchanged, and a **no-op mutation is scored as a surviving forgery**
(`forgeries_green 2`). Consequence for the landing: a corrections section that does not contain
one `N waves, M seats total` line *and* one `empty in A..B -- paths` line fails clause 6 no
matter how correct it is (same effect in `c10`/`c11`: `forgeries_green 1`).

## 2. The accepted text — minimal correct line per class

Text B, the card that exits 0 under **both** counter states (case `c06-row-edit-honest-window`,
rev `b0dcdd91`, `failing []`, `corrections 2`, `exempted 1`, `battery 3 / 0`):

Row edit in `## Owned axes` (no correction line can do this, §1 point 3):

```markdown
| coverage | 9.72 → 10.0 | 138/138 ...
| depth | 10 → 10 | 23/23 ...
```

(The numbers are the observables at the freeze revision, which is where the matrix ran; at the
landing the depth head is `24/24` because block 24 exists — the landed record already reads
`138/138` / `24/24`, `SCORECARD.md:23-24`.)

Rewrite of the round-46 window sentence to a concrete, genuinely empty window (this is the
part a correction cannot supply at the freeze, §3.2):

```markdown
`git log --name-status 5017e1f7..3186f69b -- tools/round-47/` is empty at every measurement above.
```

Corrections section:

```markdown
## Record corrections — round 47

- corrects seats round-45: 2 waves, 76 seats total
- corrects window round-46: empty in 5017e1f7..3186f69b -- tools/round-47/
```

Per-class minimal line, and where it is accepted:

| class | minimal accepted line | what the counter derives | case |
|---|---|---|---|
| `seats` | `- corrects seats round-45: 2 waves, 76 seats total` | `len(spawns)=2`, `sum=76` from `w1-dispatch.json` 40 + `w2-dispatch.json` 36 at rev | `c06` green both |
| `window` | `- corrects window round-46: empty in 5017e1f7..3186f69b -- tools/round-47/` | `git log --name-status --format= 5017e1f7..3186f69b -- tools/round-47/` prints nothing | `c06` green both |
| `axes` | **no line exists** | — | `c05` red both; only the row edit clears the atom (`c06`) |
| `path` | **no line can repair a false path atom** | the correction's predicate is identical to the atom's (`files(key) is not None`) | `c10` red both |
| `rev` | `- corrects rev <sha>: <any text>` | only `rev-parse --verify key^{commit}`; the statement is never read | `c11` |

Two hard constraints on the paste, both mechanical:

* The heading must be exactly `## Record corrections — round 47` (em dash). Case
  `c15-heading-hyphen` uses `## Record corrections - round 47`: `corrections 0 < 2` and every
  line is silently dropped, while the atoms stay red.
* `corrections >= 2`. A correct single-line repair fails (`c04` shape).

`c06`'s window pair `5017e1f7..3186f69b` is a placeholder for the landing's own revs: it must
be a pair some window atom in the card also names (freeze rule, `record.py:361-366`), i.e. the
sentence and the correction must be the same window.

## 3. What each class actually binds

### 3.1 `seats` — the "must state" is a substring search anywhere in the line

`CORR_SEATS = r"(\d+) waves?,\s*(\d+) seats total"` (`record.py:51`). Prose is free around it:
case `c03`'s line `- corrects seats round-45: wave 2 was not dispatched as written; the true
arithmetic is 2 waves, 76 seats total` is accepted (`corrections_bad []` under `a1`). This is
the same containment test R46-CL2 routed for the arm vocabulary, reintroduced one layer up.
It also means the counter never reads the *claim's* wording: one `seats` line keyed on the
round exempts **every** seats atom in that round (`exempt()` matches `(class, round)` only).

### 3.2 `window` — the freeze rule cannot repair a placeholder atom; the amendment can

At the freeze bytes, a `window` correction is only accepted when its `A..B` pair already
appears on some window atom (`record.py:361-366`). The one window atom in the last two
sections names `<tip>`, i.e. it has no pair. Case `c04` (minimal correct lines, rows untouched)
at `frz`: `corrections_bad: ['window pair names no atom in scope']`, exit 1; the same bytes at
`a1`: no `corrections_bad`. So:

* freeze `af666ce2`: `- corrects window ...` **cannot** repair the round-46 placeholder, and
  the claims file's "Repairs append a `## Record corrections — round 47` section"
  (`plans/round-47-claims.md:135`) is false for the one atom the round must repair. This is
  the amendment's stated red-before (`A1` paragraph) and my receipt reproduces it.
* amended `abf35257`: the correction is accepted, but see §4 — acceptance is by *some* empty
  window, not by the claim's window.

### 3.3 `path` — inert and unfixable

Case `c10`: a card citing `.ufo/waves/round-46/gone-dispatch.json` plus
`- corrects path .ufo/waves/round-46/gone-dispatch.json: retired, not re-derived`. The
correction is false (`corrections_bad: [{'exists': False, ...}]`) **and the atom still moves to
`exempted`** — `mismatches` no longer contains it. The only thing that reddens the run is the
`corrections_bad` clause. With the atom's own predicate equal to the correction's, no path
correction can ever be simultaneously true and needed; the class is decoration.

### 3.4 `rev` — the statement is never read

Case `c11`: the card cites an off-branch commit `42767cc5` (side branch, not an ancestor of the
graded branch) in the round-46 section. Atom red (`ancestor False`). Line
`- corrects rev 42767cc5: off-branch side measurement, kept for provenance` → atom lands in
`exempted`, `corrections_bad []`. `corrects()` for `rev` (`record.py:300-302`) calls only
`rev-parse --verify`; the statement is not parsed at all, so a citation that is provably not an
ancestor is waived by a sentence that asserts nothing.

## 4. Forgeries that score green under **both** states

### 4.1 A false window claim waived by a correction naming a pathspec that does not exist

Case `c09`, rev `4941651a`, exit **0** under `frz` and `a1`, `battery 3 / 0`,
`exempted = [seats 45, window 46]`, `mismatches []`.

Card (round-46 sentence replaced):

```markdown
0425224..1e32827b -- .ufo/waves/round-46/` is empty at every measurement above.
A second window, `5017e1f7..5017e1f7 -- SCORECARD.md`, is empty.
```

Corrections:

```markdown
- corrects seats round-45: 2 waves, 76 seats total
- corrects window round-46: empty in 5017e1f7..5017e1f7 -- SCORECARD.md
- corrects window round-46: empty in 0425224..1e32827b -- no/such/path.md
```

The claim is **false** and the counter says so nowhere:

```
$ git -C <fixture> log --name-status --format= 0425224..1e32827b -- .ufo/waves/round-46/
A  .ufo/waves/round-46/l1/scores/c1-at-F4.json
A  .ufo/waves/round-46/l1/scores/c2-at-781e19ae.json
A  .ufo/waves/round-46/l1/scores/c2-at-F4.json          (3 changed lines → not empty)
$ git -C <fixture> cat-file -e 4941651a:no/such/path.md  ; echo $?   → 128
$ git -C <fixture> log --format= 0425224..1e32827b -- no/such/path.md | wc -l   → 0 (empty)
```

Mechanism: `exempt()` for a window atom compares only the `A..B` pair (`record.py:330-337`),
never the pathspec; `corrects()` re-derives the emptiness of *the pathspec the correction names*
(`record.py:271-279`). A pathspec that matches no path makes `git log` print nothing, so the
correction is "reproduced as empty" and the atom is exempted. The same construction with a
missing path is what the claims file calls a killed forgery ("An exemption whose correction is
false keeps the atom red", `plans/round-47-claims.md:138-139`): it does not keep it red, it
moves it to `exempted`. Case `c12` repeats it with the two window lines swapped: also green.

### 4.2 The same forgery is not caught by the battery, and its order matters

`run_battery`'s `non_empty` mutates the **first** `empty in A..B` occurrence. In `c09` that is
the harmless `X..X` line, so the offending correction is never mutated and every forgery stays
red; in `c12` the vacuous line is first, the mutation removes the exemption, and the forged
card is red for a different reason. Either way `forgeries_green 0` and the landed card is green:
the battery's three forgeries do not cover "exemption by an unrelated/empty pathspec".

### 4.3 A false window claim on the same physical line is not an atom

Case `c13`, rev `2a4d88cf`, green both states, `verified 50`, `mismatches []`. The section
carries one line: `` 5017e1f7..5017e1f7 -- SCORECARD.md` is empty at every measurement above,
and `0425224..1e32827b -- .ufo/waves/round-46/` is empty too. `` — the second, false claim is
never checked, because `collect()` emits **one** window atom per line and `WINDOW.search` takes
the first pair (`record.py:49`, `record.py:155-162`). A landing can assert a false window
sentence anywhere on a line that already carries a true one.

### 4.4 A vacuous `X..X` window is a full-strength correction

Case `c08`, rev `c2f53226`, green both states: the sentence is rewritten to
`5017e1f7..5017e1f7 -- SCORECARD.md` and the correction restates it. `A..A` is empty for every
path, so this satisfies "a window the counter itself reproduces as empty" while asserting
nothing. It is the shortest green window repair at the freeze bytes.

## 5. Amendment series: what changed, what the claims file says about it

`tools/round-47/record.py` changed **three times while this seat was measuring**, then the
changes were committed:

| time | sha256 | state |
|---|---|---|
| first read | `787f909a76d43f9b9c5597d13ef57b17ad5b241d1a300b668ee968194a986d43` | working tree; `git diff 5017e1f` = pair-check deletion only |
| second | `c704c3d407325264f8e2d990a8873524b0c5bbbf52d5dcc10ee8df411c9d6fa7` | working tree; adds `root_repo` and the root-anchored `non_empty`; tree-identical to `1e2c3102` (A4) |
| measured | `abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` | working tree at measurement; tree-identical to `09a9f912` (A5) |
| freeze | `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` | `git show 5017e1f:tools/round-47/record.py` |

The four semantic deltas between `frz` and `a1`, and their declaration status:

| delta | clause or fixture | declared where |
|---|---|---|
| window correction's `A..B` pair need not appear in the card | **clause** (exemption/admissibility) | claims file, A1 paragraph (`9018c53b`) |
| `non_empty` forgery uses `root..tip` | battery fixture | claims file, A2 paragraph (`62e33f7d`) |
| a `seats`/`window` correction for a round older than the last two needs no atom | **clause 3 relaxed** | commit subject only (`2e4ae434`, A3); **not** in the claims file |
| `ghost_atom` inserts inside the section | battery fixture | commit subject (`07d2894e`, A5) |

The claims file was last touched by A2 and still says both "A2 … nothing else" and, in clause
3, "A correction that exempts an atom the card does not contain is itself a defect"
(`plans/round-47-claims.md:148`). A3 contradicts that sentence and no amendment paragraph
records it; the round-47 record section discloses the seven-commit series (`SCORECARD.md`
`## Round 47`, "The freeze is a disclosed series of seven commits"), so the *series* is
disclosed but the *clause text* the counter enforces is not the clause text the claims file
states. Measured: case `c14-historical-correction`,
`- corrects window round-44: empty in 5017e1f7..5017e1f7 -- SCORECARD.md` → `frz` exit 1 with
`['exempts an atom that does not exist', 'window pair names no atom in scope']`, `a1` exit
**0**, `exempted` unchanged (the line exempts nothing).

Second, independent of the amendments: `record.py` never derives a frozen set.
`grep -n "frozen_set\|frozen_path_changed" tools/round-47/record.py` → no match
(`exact.py:408` has it; `record.py` imports `gate` but never calls `gate.frozen_set`, and
`SELF`/`CLAIMS` at `record.py:32-33` are unused). The claims file's
`plans/round-47-claims.md:11` — "a change makes **both** counters exit 2
`frozen_path_changed`" — is false for R47-C2: a mutated C2 interpreter returns a *verdict*.
Every `a1` receipt in this report is a verdict produced by a counter that is not the frozen
counter, and nothing in the counter would have said so.

## 6. What the L1 should paste (and what it must not)

1. **`## Owned axes`**: change the two leading fractions to the observed values — `138/138`
   and, once block 24 exists, `24/24` (derived at rev: coverage map ∩ `corpus/knowledge/*.md`;
   craft-block citation count, 23 at the freeze, 24 after the landing).
   No correction line can do this; `- corrects axes …` is silently ignored (`c05`).
2. **Round-46 window sentence**: rewrite to a concrete pair the counter reproduces as empty —
   `c06`'s shape is green at both states. Do not leave the `<tip>` placeholder and expect a
   correction to repair it at the freeze (`c04`).
3. **Corrections section**, heading exactly `## Record corrections — round 47`, at least two
   lines, one containing `N waves, M seats total`, one containing `empty in A..B -- paths`
   (otherwise clause 6 counts a no-op mutation as a surviving forgery, §1). `c06` is the
   minimal green pair.
4. **Do not** use `- corrects path …` (inert, `c10`), do not use `- corrects rev …` to waive a
   citation (`c11`), and do not let a window correction name a pathspec the claim does not
   name — it is accepted and it exempts (`c09`/`c12`). Keep one window claim per physical line
   (`c13`).

## 6.1 Audit of the section that has already landed

`SCORECARD.md:3663-3678` (`## Record corrections — round 47`) carries **four** visible
`- corrects` lines. The counter parses **two** and, at the current tip, one of those exempts
nothing:

| line | parsed | operative |
|---|---|---|
| `:3669` `- corrects seats round-45: 2 waves, 76 seats total — …` | yes | not at `09a9f912`: round 45 has left the last-two window, and A3 keeps the line admissible without an atom |
| `:3672` `- corrects window round-46: empty in 332f4884..58eb04b6 -- …` | yes | yes (exempts the `<tip>` atom, via A1's deleted pair clause) |
| `:3675` `- corrects axes coverage: 138/138 — …` | **no** — `CORR` has no `axes` alternative | no (the atom is cleared by the row edit) |
| `:3677` `- corrects axes depth: 24/24 — …` | **no** | no |

Live receipts (read-only runs on the lane, `--json-out` inside this seat's directory):

```
$ python3 -I -B tools/round-47/record.py --root <lane> --rev 09a9f912 --json-out …/landed-09a9f912.json
  exit 0; atoms 44; corrections 2; corrections_bad []; mismatches [];
  exempted = [(window, 46)]; battery 3 / 0
$ python3 -I -B tools/round-47/record.py --root <lane> --rev 1e2c310295 --json-out …/landed-at-1e2c310295.json
  exit 0; atoms 50; corrections 2; exempted = [(seats, 45), (window, 46)]; battery 3 / 0
```

So the R47-C2 "after" cell reproduces exactly at the revision it names (`atoms 50`,
`corrections 2`, `exempted 2`) and drifts at the tip (`atoms 44`, `exempted 1`) without
changing the verdict. Two consequences for the L1:

* `corrections 2` is not "two lines in the section": four lines are visible and two are inert.
  If the axes lines are meant to be evidence, either drop them (they document nothing the row
  edit does not) or fix `CORR` to admit `axes` — the latter is a clause change to a frozen
  counter and needs an amendment paragraph, not a silent edit.
* The landed window excuse is *true* (`git log --name-status --format= 332f4884..58eb04b6 --
  tools/round-46 plans/round-46-claims.md` prints 0 lines) but it is admissible only because
  A1 deleted the pair clause: the `<tip>` sentence was never rewritten, so no atom names
  `332f4884..58eb04b6`. §4.1 shows the same machinery also admits a *false* window, which is
  the residual risk the battery does not cover.

## 7. Not run / limits

* §1–§4 receipts are on a fixture clone at `5017e1f7` plus case commits (the landing did not
  exist when the matrix ran). §6.1 receipts are live, read-only runs on the lane at
  `09a9f912` and `1e2c310295`. The fixture is reproducible with `C2CorrGrammar/drive.py`
  (clone the lane at `5017e1f7` first).
* R47-C1/`exact.py` was not scored by this seat (separate lane work); only its
  `frozen_path_changed` presence at `exact.py:408` is cited, as contrast in §5.
* No tool installs (nothing was needed); no writes outside
  `.ufo/waves/round-47/w1/C2CorrGrammar*`; lane `git` reads only (`show`, `log`, `diff`,
  `rev-parse`, `status`), all fixture mutations inside the verified clone
  (`git -C <clone> rev-parse --show-toplevel` asserted before the first commit).

## Receipts

* `C2CorrGrammar/ledger.jsonl` — per case: rev, counter sha256, exact command, exit, stdout
  sha256, UTC, `failing`, mismatches, corrections, `corrections_bad`, exempted, battery.
* `C2CorrGrammar/receipts/<case>.<frz|a1>.json` — the full counter receipts (30).
* `C2CorrGrammar/drive.py` — the case generator.
* `C2CorrGrammar/snap/record-a1-abf35257.py`, `C2CorrGrammar/snap/claims-abf35257.md` — the
  exact `a1` bytes these receipts were produced against (= `tools/round-47/record.py` in the
  tree at `09a9f912`, sha256-identical).
* `C2CorrGrammar/receipts/landed-09a9f912.json` (+ `.stdout`) and
  `C2CorrGrammar/receipts/landed-at-1e2c310295.json` — the live §6.1 audit.
