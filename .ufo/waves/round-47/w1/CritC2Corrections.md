# CritC2Corrections — R47-C2 correction mechanism, attacked

Seat: `CritC2Corrections`, wave 1, round 47. Lane tree read-only; every mutation below is in a
throwaway fixture repo or a scratch clone. Declared freeze measured: `1e2c3102952dc636650095643c1963c833859019`
(A4); lane tip at measurement time `a631bba01633d2b5353306a569be4ce2e683d364`.

**Verdict: predicate too weak.** The sanctioned repair route does not repair: a correction line
never has to be *about* the atom it exempts. The cheapest false-but-passing card is one true
correction that restates an already-true atom plus one tautological window correction; it scores
**exit 0** with a false seat cell and an unverifiable empty-window sentence left standing in the
card. The landed card at the declared freeze is the live instance (its correction names
`332f4884..58eb04b6`, a window chosen so that it cannot contain the change that falsifies the
sentence), and reducing that correction to the pure tautology `332f4884..332f4884` still scores
exit 0. Neither `corrections >= 2` nor `exempted <= 3` stops it.

## 0. Scope of what I ran

| what | how |
|---|---|
| frozen counter | `python3 -I -B tools/round-47/record.py --root <root> --rev <rev>` (never `--json-out`, to stay inside the lane) |
| fixture repo | `git init` in `$S/fx`, toplevel asserted equal to `$S/fx` before the first commit |
| live card variants | `git clone --no-hardlinks` of the lane into `$S/realclone`, commits made **only** in the clone |
| scratch | `S=/fast/scratch/hyaku/kaidoku-r47/CritC2Corrections`, `TMPDIR=HYAKU_SCRATCH=$S` |

Nothing under `/tmp` is cited. No installs.

**Instrument identity.** Every receipt below was produced by
`tools/round-47/record.py@abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`
(the worktree bytes, which are the lane HEAD and the scratch clone's HEAD). While wave 1 ran, the tree
moved past the freeze named in the prompt: A4 `1e2c310295` → A5 `a631bba0` → A6 `f54b3b6d` → A7
`31b092d1` → `f7d6e58d`. A5 touched only the ghost-atom forgery (`record.py`, +7/−1) and not the
exemption logic, so these findings hold on the newest bytes; the receipts that name a card revision
(`--rev 1e2c310295`, `--rev 2e4ae434`) are card revisions, not instrument revisions.

## 1. The mechanism as measured, not as described

1. `derive()` runs before exemption (`record.py:341-353`). A true atom goes to `verified`; only a
   failing atom is ever offered to `exempt()`. **Therefore every entry in `exempted` is, by
   construction, a false or unverifiable statement the card keeps.** `mismatches == []` plus
   `exempted <= 3` is the assertion "at most three lies, each footnoted", not "the record is true".
2. `exempt()` (`record.py:330-338`):
   - window class: `if atom.get("pair") is None: return True` — **any** window atom whose line does
     not carry two concrete hex revs is exempted by **any** window correction that re-derives, with
     no relation to the atom's own rev, window or pathspec;
   - every other class: `str(atom["key"]) == str(entry["key"])` — a seats atom's key is the round
     number, so **one** seats correction exempts every seats atom of that round, whatever the atom
     claims.
3. `corrects()` (`record.py:258-303`) validates only the correction's own statement against
   committed state. It never sees the atom.
4. `corrections()` (`record.py:242-255`) parses **every** matching line, duplicates included.
   Thresholds are `CORR_MIN = 2`, `EXEMPT_MAX = 3` (`record.py:36-37`), applied at
   `record.py:382-387`.
5. Grammar `CORR` (`record.py:50`) is `seats|window|path|rev` — **no `axes`** — although `corrects()`
   carries an axes branch and claims-file clause 3 (`plans/round-47-claims.md:168`) states a rule
   for axes corrections.

## 2. The cheapest false-but-passing card

Fixture repo `$S/fx`, base `03ff8de444947739eee57d66137a7c2675c5847f`, three commits; the only
dispatch files are round 7 (`counts.spawn 2`) and round 9 (`counts.spawn 1`, `1`). Card at
`deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e`:

```
## Round 9

Base `03ff8de4`. Waves: 1 + 1 = 2 seats. Wave 1: 7 seats; wave 2: 9 seats. Wave 1 evidence is in
`.ufo/waves/round-9/w1-dispatch.json`.
`git log 0425224..<tip> -- tools/x/keep.md` is empty at every measurement above.

## Record corrections — round 47

- corrects seats round-9: 2 waves, 2 seats total
- corrects window round-9: empty in 03ff8de4..03ff8de4 -- tools/x/keep.md
```

`Wave 1: 7 seats; wave 2: 9 seats` is false (dispatched 1 and 1) and the empty-window sentence names
a rev that exists in no repo. The first correction is the *repair of nothing*: it restates the
already-true sum atom `Waves: 1 + 1 = 2 seats`. It nevertheless exempts the false pair atom, because
the atoms share the key `9`. The second correction is a degenerate self-window that is empty for any
repo.

```sh
python3 -I -B tools/round-47/record.py --root $S/fx --rev deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e
# exit 0
# failing [], mismatches [], corrections 2, corrections_bad [],
# exempted [('seats','9','Wave 1: 7 seats; wave 2: 9 seats'),
#           ('window','9','`git log 0425224..<tip> -- tools/x/keep.md` is empty …')]
# battery correction_forgeries 3, forgeries_green 0, atoms 7
```

Full matrix, same fixture, each row a commit and a separate counter run:

| card | rev | exit | corrections | exempted | failing |
|---|---|---|---|---|---|
| A cheapest-false (above) | `deda0d5` | **0** | 2 | 2 | `[]` |
| B padded (adds `- corrects seats round-7: 1 waves, 2 seats total`, repairs nothing, exempts nothing) | `811601b` | **0** | 3 | 2 | `[]` |
| C uncorrected (same card, no corrections section) | `10cb1ec` | 1 | 0 | 0 | `mismatches 2 != 0`, `corrections 0 < 2` |
| D axes-arm (coverage row false `0/1`, plus `- corrects axes coverage: 1/1`) | `ee6ccb4` | 1 | 2 | 2 | `mismatches 1 != 0` (the axes line is not parsed) |
| E duplicate-padding (the identical seats line twice + window tautology) | `861c3e7` | **0** | 3 | 2 | `[]` |
| F four-false (false sum + false pair + two placeholder windows) | `791c0a9` | 1 | 2 | 4 | `exempted 4 > 3` |
| H grammar-evasion (§5) | `5d0aefa` | **0** | 3 | 0 | `[]` |

C is the red-before: the false sentences alone are red; appending A's two lines flips the whole card
green without editing a single false character.

## 3. Live proof on the real card (no fixture)

The round-46 section at the declared freeze contains (`SCORECARD.md` round-46, "Freeze-integrity
disclosure"):

> `git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every
> measurement above.

Round 47 exempts that atom with `- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md`.

Measured facts (read-only `git log`):

```sh
git log --name-status --format= 0425224..1e2c310295 -- tools/round-46 plans/round-46-claims.md
# M  tools/round-46/attest.py
# M  tools/round-46/gate.py            → the sentence's own window is NOT empty
git log --name-status --format= 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md
# M  tools/round-46/attest.py
# M  tools/round-46/gate.py            → not empty at the round-46 tip either
git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md
# (nothing)                            → the correction's window is empty because it STARTS at the
#                                        very commit (332f4884) that made those two edits
```

So the correction is true and vacuous, and the false sentence it exempts stays in the record
unrefuted. The counter says the record is calibrated.

Variants applied in the scratch clone (`$S/realclone`, each its own commit):

| variant | correction text | exit | failing |
|---|---|---|---|
| T0 lane tip as landed | `empty in 332f4884..58eb04b6 -- …` | **0** | `[]`, `exempted [('window','46')]` |
| T1 tautology | `empty in 332f4884..332f4884 -- …` | **0** | `[]`, battery 3/0 |
| T2 honest | `empty in 0425224..58eb04b6 -- …` (the window the sentence names) | **1** | `corrections that do not re-derive: 1`, detail `{'empty': False, 'window': '0425224..58eb04b6'}` |
| T3 removed | (line deleted) | **1** | `mismatches 1`, `corrections 1 < 2`, `forgeries_green 1` |

T1 = T0: the landed evidence line is not load-bearing. T2 is the sharpest result — **the only
correction that would state the truth about the sentence is rejected**, so the instrument pays for a
correction that changes the subject.

## 4. Do the two floors stop it?

**`corrections >= 2` — no.** It is a count of parsed lines with three independent ways to pad:

- duplicates count: E scores `corrections 3` with one line appearing twice (`record.py:242-255`
  appends every match);
- corrections for a round older than the window count and need only a dispatch file: B adds
  `- corrects seats round-7: 1 waves, 2 seats total`, which re-derives true and exempts nothing
  (`record.py:366-376` historical branch);
- the exempting correction itself can be the restatement of an already-true atom (A). The floor
  therefore forces a second *true* line, never a second *repair*.

**`exempted <= 3` — no, and it is mis-scaled.** It is an upper bound on falsehoods, not a lower
bound on repairs; with `derive()` first, three false atoms are licensed. It bites only at four (F,
`exempted 4 > 3`). And it counts *atoms*, so one correction can consume the whole budget by
fan-out: at the declared freeze one seats correction exempts the round's atom, and a round with a
sum cell and a pair cell spends 2 of the 3 on one root cause (A, F).

Neither floor requires the exempted sentence to be edited, struck or quoted by the correction.
The claims-file sentence "Each `- corrects …` line exempts the atoms it names" is not implemented:
for `window` the line does not even have to name a rev the atom names; for `seats` it names a
*round*, not an atom.

## 5. Adjacent defects found while attacking

1. **The `axes` arm is unreachable.** `CORR` (`record.py:50`) cannot match `axes`, so a
   `- corrects axes …` line is silently ignored — no exemption, no `corrections_bad`, no diagnostic
   (D: `corrections 2` for a section with 3 lines, coverage mismatch stays red). The landed card
   shows the cost exactly: it carries **4** `- corrects` lines and the counter reports
   `corrections 2` (both at A4 and at the lane tip); the two axes lines are decorative prose while
   the record text claims "corrections 2 both re-derived". `corrects()`'s axes branch
   (`record.py:280-289`) is dead, and the second block at `record.py:292-299` is dead code that
   references an undefined `atom` — it would `NameError` if the grammar ever produced `axes`.
2. **The battery's window forgery is pathspec-dependent.** `non_empty` (`record.py:431-446`) forges
   `root..rev` over the correction's own pathspec. If that path did not change since the root
   commit, the forgery is inert and a *correct* card is scored red: my first fixture run failed only
   on `battery forgeries_green 1 != 0` for an otherwise green card. Conversely a card with no
   window correction leaves the forgery a no-op that counts green (H before I added a window line).
   The 3/0 requirement measures the card's shape, not the mechanism.
3. **`--selftest` is unreachable as documented.** `--root` and `--rev` are `required=True`
   (`record.py:459-461`), so `record.py --selftest` exits 2 with an argparse usage error before the
   selftest runs; I had to pass `--root /nonexistent --rev deadbeef`. With those dummies it reports
   `RECORD_SELFTEST: cases=10 failures=0`.
4. **The atom grammar is the truth surface, and it is three regexes.** Seats are read only as
   `Waves: A + B = C seats` or `Wave 1: A seats; wave 2: B seats` (`record.py:45-46`). Card H (the
   cheapest card plus one window correction so the battery has a target) writes
   `Wave 1 — 7 seats; wave 2 — 9 seats` (em dashes, false: 1 and 1) and scores **exit 0,
   `mismatches []`, `exempted []`** with the false sentence on display; before that line was added
   the same card scored exit 1 only on `battery forgeries_green 1`, i.e. for the forgery's own
   no-op. Same for windows: only lines containing `is empty` are atoms (`record.py:156`). This is a
   scope statement, not a bug in the correction code — but it means the correction mechanism is the
   only guard for the shapes it reads, which is why (2)–(4) matter.

## 6. Smallest safe correction, ranked (not applied — the bytes are frozen)

**S1 — bind a window correction to the atom it exempts** (`record.py:330-337`). This alone closes the
live T1/T0 hole. In `exempt()`, for the window class:

```python
cm = CORR_WINDOW.search(entry["statement"])
if not cm:
    return False
a, b = cm.group(1), cm.group(2)
if a == b:                                   # degenerate window is a tautology, never evidence
    return False
atom_a = re.search(r"([0-9a-f]{7,40})\.\.", atom["line"])
atom_b = re.search(r"\.\.([0-9a-f]{7,40})", atom["line"])
if atom_a and a != atom_a.group(1):          # must keep the window the sentence named
    return False
if atom_b and b != atom_b.group(1):
    return False
if not git(root, "ls-tree", "-r", "--name-only", rev, "--", *cm.group(3).split()).stdout.strip():
    return False                             # pathspec must resolve to a tracked path
return True
```

and the same `a == b` + pathspec test in `corrects()` (`record.py:271-279`) so a tautology cannot
re-derive. Effect on the live card: the only correction that passes is
`0425224..<measured tip>`, which is non-empty — the record must then *edit* the false sentence.
That is the honest stop, and it is what T2 proves the instrument currently forbids.

**S2 — bind a seats correction to the atom's shape** (`record.py:338`). A `pair` atom is exempted
only by a correction that states the pair figures and re-derives them
(`wave 1: <a> seats; wave 2: <b> seats`, compared against the same `counts.spawn` list); a `sum`
atom only by the `N waves, T seats total` form. This kills the "restate the true sum, exempt the
false pair" pattern (A). The landed round-45 line must then be split into the pair form
(`wave 1: 40 seats; wave 2: 36 seats`) — one line of card text, no new machinery.

**S3 — dedupe before counting** (`record.py:242-255` / `382`): key on
`(class, key, statement)`; two identical lines are one correction.

**S4 — budget root causes, not atoms** (`record.py:386`): count corrections that exempt ≥ 1 atom
against a cap (2 is enough for the before-state's four mismatches: three classes), and require
`len({(c["class"], c["key"]) for c in corr if c exempts something}) == len(exempted_root_causes)`.
S1+S2 remove the fan-out that made the atom cap the only bound.

**S5 — make `axes` reachable or delete the claim.** Add `axes` to `CORR` and to the key set
(`coverage|depth`), or delete `record.py:280-289` and `292-299` and drop the clause-3 sentence; the
current state is a claimed repair route that silently does nothing, and the landed card relies on
the *table edit* while its axes lines read as corrections.

**S6 — forge over a path that changed** (`record.py:431-446`): pick the path from
`git log --name-status --format= root..rev` rather than from the card's statement, and treat
"mutation was a no-op" as `forgeries_green += 1` only after the mutation is proven applicable.

**S7** — `record.py:459-461`: `required=False` for `--root`/`--rev`, rejected inside `main` only
when `--selftest` is absent.

If only one change is affordable: **S1**. It is 12 lines, it closes the live instance at the declared
freeze, and it needs no card edit beyond the one sentence the record should not be making.

### Measured effect of S1 + S2 (patch in this directory)

`record-s1s2-patch.py` is the A5 instrument with exactly S1, S2 and the symmetric grammar for
`corrects()` (it accepts `wave 1: <a> seats; wave 2: <b> seats` and re-derives it against the same
`counts.spawn` list). It was run from scratch only; the frozen bytes are untouched.

| card | frozen instrument | patched instrument |
|---|---|---|
| live card at `1e2c310295` (A4) | exit 0, `exempted [seats 45, window 46]` | **exit 1**, `mismatches 2` — the record must edit both sentences, which is the point |
| fixture A, cheapest-false | exit 0 | **exit 1**, `mismatches 2` + `corrections_bad` (degenerate window) |
| fixture honest repair (`fixture-run11.json`, `ebc4b8b35c2ffa1da24ffbfcedc3b115d7f94316`) | **exit 1** — `corrections that do not re-derive: 1`, `a seats correction must state '<n> waves, <total> seats total'` | **exit 0**, `mismatches []`, `exempted [seats 9]`, battery 3/0 |

The third row is the calibration that matters: the card that actually names the false atom's figures
(`- corrects seats round-9: wave 1: 1 seats; wave 2: 1 seats`, derived equal to the dispatch) is
**rejected by the frozen predicate** and accepted by the patched one. The frozen predicate pays only
for corrections that avoid the atom's content.


## 7. Receipts

Commands are exactly as run; `$REC = /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py`
at `sha256 abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7` (A5 instrument).

| receipt | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| `fixture-run3.json` | `python3 drive.py` (cards A–D, one counter run each) | 0 (driver) | `124b15f053111813c722ac23ed5b5c533e399fbe201ba8a5237fd6793c0c2549` | 2026-10-28T17:57:38Z |
| `fixture-run4.json` | `python3 drive2.py` (E, G) | 0 | `c974b21b03bbef4397ab52ec29e376b90e0c091ca696bf7cf023affb12cd50ab` | 2026-10-28T17:58:43Z |
| `fixture-run5.json` | `python3 drive2.py` (F, four false atoms) | 0 | `ac9844cc807e306c92ed99c8e3db5a3c8731091614abd4df908e010d9df01dc2` | 2026-10-28T17:58:52Z |
| `fixture-run6.json` | `python3 drive3.py` (H without a window correction) | 0 | `280a650a5b3a0e77de07cc2ddde088cba3624da6558c6faa3f1e7060d2ced0b1` | 2026-10-28T17:59:22Z |
| `fixture-run7.json` | `python3 drive3.py` (H with a window correction) | 0 | `6d5c7379b86f2f8b9426f3379b44cfa528a6587585bdf7852b958002de121ce5` | 2026-10-28T17:59:33Z |
| `realvariants.json` | `python3 realvariants.py` (T0–T3 in the scratch clone) | 0 | `80bbd172e4624c899ec40a4a67965551caa8e1659c187edca2b744d4ab663bce` | 2026-10-28T17:58:24Z |
| `rec-1e2c310295….json` | `$REC --root <lane> --rev 1e2c3102952dc636650095643c1963c833859019` | **0** | `c609b3e1c8ac00d03f8b80c9313d96b25466e53116b40121422f43e94224209d` | 2026-10-28T17:56:46Z |
| `rec-2e4ae434….json` | `$REC --root <lane> --rev 2e4ae43463aabdae707f8c8a4daa41441ad67a71` | **0** | `553be365645d8fe69adfac6a1888c67dacd72f12e608ebe71784ea9467d88fc0` | 2026-10-28T17:56:48Z |
| `head-nobattery.json` | `$REC --root <lane> --rev HEAD --no-battery` | **0** | `eb0cfbcce43993ba3edb7c2d1834df17235ac77c678f8dfbc28da3e82b2ac668` | 2026-10-28T17:56:24Z |
| `selftest.out` | `$REC --root /nonexistent --rev deadbeef --selftest` | **0** | `a389791d57f1c0b488feb5a5276a9e64f552dcc76e0fb2c6906a1ff80a72eeeb` | 2026-10-28T17:53:53Z |
| `patch-liveA4.json` | `python3 record-s1s2-patch.py --root <lane> --rev 1e2c3102952dc636650095643c1963c833859019` | **1** | `eb894efe28d865dbac9e64b9ab9ceba7b0283353492d7d440a8ccd0ef09bb864` | 2026-10-28T18:01:46Z |
| `patch-fixtureA.json` | `python3 record-s1s2-patch.py --root $S/fx --rev deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e` | **1** | `e2e55276d8fd0d9b0c601819af9ce5e60df4034972fa0f221d7a6063a6fc4d7d` | 2026-10-28T18:01:46Z |
| `fixture-run10.json` | `python3 drive4.py` (honest repair, placeholder window) | 0 (driver) | `cdf54d4038371926edd75402655a9422a9081162c0f08f7e4dcbd61abdd16b1e` | 2026-10-28T18:02:16Z |
| `fixture-run11.json` | `python3 drive4.py` (honest repair, concrete window; both instruments) | 0 (driver) | `431801c511ba909c6e2f592cb13eb9012bdcbd88a7f4de3267a49a350361f93f` | 2026-10-28T18:02:25Z |

Drivers are copied alongside: `drive.py` (A–D), `drive2.py` (E–G), `drive3.py` (H), `drive4.py`
(honest repair), `realvariants.py` (T0–T3), and `record-s1s2-patch.py` (the S1+S2 instrument, scratch
only). Each driver rebuilds its fixture from scratch, so the receipts are reproducible except for
commit hashes (the driver prints the base and each rev it measured).

## 8. What I did not run

- R47-C1 / `tools/round-47/exact.py` — other seats own that instrument; I did not score it.
- No `--json-out` run against the lane: `gate.out_path` refuses a target outside the lane root and
  every path inside it is either frozen or graded, so the lane receipts above are stdout captures
  from my scratch.
- No mutation of the lane, no commit, no stage, no stash; the clone and the fixture are the only
  git histories I wrote.

**One-line verdict: predicate too weak — R47-C2's correction route exempts atoms without being
about them (a restatement of an already-true atom and a degenerate `A..A` window both score exit 0,
live at the declared freeze), and it rejects the one card that does name the atom's own figures
(fixture `ebc4b8b3`: frozen exit 1, patched exit 0); `corrections >= 2` counts duplicate and vacuous
lines and `exempted <= 3` only caps falsehoods, so binding a window correction to its atom's named
rev and a seats correction to its atom's shape (S1, S2) is what closes it.**
