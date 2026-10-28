# CritBattery — round 47 wave 1: falsifying the two frozen batteries

Seat `CritBattery`, leaf member (no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane tree: every fixture
lives in `S=/fast/scratch/hyaku/kaidoku-r47/CritBattery`, every lane write is under
`.ufo/waves/round-47/w1/CritBattery/`. No commits, no staging, no mutating git. No tool
installed (nothing needed; `pacman` untouched per the host pause).

## Revisions this report is pinned to

| name | commit | note |
|---|---|---|
| base | `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5` | the claims' base |
| first freeze | `5017e1f7` | the commit the frozen claims file defines as the freeze |
| landing | `e856beb5` | the commit that first carries craft block 24 |
| A4 | `1e2c3102` | the card as it stood when this seat started |
| A6 (declared freeze) | `f54b3b6d` | the last commit that touches `tools/round-47/` |
| A7 (declared measured rev) | `a0753786` | `c1-at-A7.json`, `c2-at-A7.json` |
| HEAD at attack time | `31b092d1` | the record with the A6/A7 paragraph |

The lane advanced twice under me (A5 `07d2894e`, A6 `f54b3b6d`, A7 `31b092d1`). Every number
below names the revision it was measured at; the A4 numbers are kept because that is the
revision the round itself recorded as the landing measurement.

Receipts: `.ufo/waves/round-47/w1/CritBattery/receipts/manifest.jsonl` — one line per command
with `argv`, `cwd`, `exit`, `utc`, `stdout_sha256`; the raw stdout of each is the sibling
`<name>.stdout`. Drivers are in scratch (`drv_c1.py`, `drv_c2b.py`, `drv_c2c.py`,
`drv_denominator.py`, `run_receipts.py`) and the tampered interpreters are preserved as
`receipts/tampered-exact.py` (C1 denominator fixture) and `S/tpy/tools/round-47/record.py`
(C2, sha256 `2d2d964f7a004f415c8e5a149d15f01cd45effd35c62bc1a785b1db57d34e944`).

## The seven forgeries, one verdict each

Verdict key: **one defect** = the artefact differs from the genuine one in the single respect the
class names and is red for that reason alone; **different artefact** = the mutation changes
something else too, so the green→red cannot be attributed to the clause it claims to measure.

### C1 (`tools/round-47/exact.py` `MUTATIONS`)

| # | forgery | what it actually mutates | v2 / v3 (measured) | verdict |
|---|---|---|---|---|
| 1 | `substring-arm` | **all four** v3-arm cells → `order-ish` | 0 / 1, `arm cells not exact vocabulary tokens: ['order-ish' x4]` | **one defect**, applied four times; over-broad |
| 2 | `duplicate-routed-id` | inserts a **fifth row** | 0 / 1, `rows 5 != 4` **and** cardinality | **different artefact**: clause 3 fires first |
| 3 | `stale-mutations-digest` | the block's digest → sha256 of 3 names | 0 / 1, `mutations_sha256 does not match …` | **one defect**; honest |
| 4 | `flag-order-drift` | `tools/round-46/gate.py` in the fixture; `SKILL.md` byte-identical | 0 / 1, `gate.py flag order: 0 correct, 1 reversed` | **different artefact**: the claimed surface is untouched |

Evidence: `receipts/c1-declared-pair.stdout` (the four fixture verdicts as landed) and
`receipts/c1-variants.stdout` (my variants, `exit 0`, sha `f1ef583085a3ec61…`).

**1. `substring-arm` — keep, but one cell is enough.** The class is honest: only clause 5 fires.
It is not minimal, and because it rewrites rows 2–4 as well it also erases the row↔arm mapping
(row 3 no longer carries `once`). My one-cell form (`receipts/c1-variants.stdout`):

```
{"name": "order-ish-one-arm", "v2_exit": 0, "v3_exit": 1,
 "v3_failing": ["arm cells not exact vocabulary tokens: ['order-ish', 'once', 'digest', 'order']"]}
```

Same discrimination, one defect, battery counts unchanged (`v2_green 4 / v3_green 0`).

**The class's stated example is false.** The frozen claims' C1 kill rule says *"A block with
`blobberish` in a v3-arm cell fails clause 5 while the v2 profile passes it."* It does not —
`blobberish` contains none of round 47's tokens, so the ported v2 profile rejects it too:

```
{"name": "blobberish-one-arm", "v2_exit": 1,
 "v2_failing": ["arm cells outside the vocabulary"],
 "v3_exit": 1,
 "v3_failing": ["arm cells not exact vocabulary tokens: ['blobberish', 'once', 'digest', 'order']"]}
```

The claims borrowed round 46's vocabulary (`blob` was an arm token then); block 24's row 1 says
the same thing ("`blobberish` satisfies `blob` in the arm-vocabulary test"), which is a true
statement about round 46 and a false illustration of this round's `v2` profile. **Smallest safe
correction:** restate the kill rule with `order-ish` (the token `MUTATIONS` actually uses) and
say in row 1 that the exemplar is round 46's vocabulary, not the ported one.

**2. `duplicate-routed-id` — different artefact; here is the mutation that keeps it honest.**
A fifth row necessarily trips clause 3 (`rows 5 != 4`), so the battery would stay red even if
clause 4 were deleted. Keep four rows and let one row name two ids:

```
{"name": "dup-id-4rows-double-cell", "v2_exit": 0, "v3_exit": 1,
 "v3_failing": ["rows naming != 1 routed id: [0]",
                "routed cardinality {'R46-CL2': 1, 'R46-CL3': 2, 'R46-CL4': 1, 'R46-CL6': 1} != each of [...] exactly once"]}
```

Scored against the frozen counter: **v2 0 / v3 1**, i.e. it fills exactly the two battery slots
(`v2_green`, `v3_green`) that the current mutation fills, with the red attributable to clause 4
alone. A 4-row variant that *drops* an id cannot be used: it makes v2 red (`missing CL6`) and
would break `v2_green == 4`.

**3. `stale-mutations-digest` — honest, but it tests the pin, not the denominator.** Only clause 6
fires. The class's *other* half — R46-CL4's real defect, deleting a mutation — is not in the
battery, and it is not bound when the freeze is the commit that carries the tool. I built that
counterexample (`receipts/c1-denominator-coforgery.stdout`, sha `720de26db1845b5e…`): a
lane-shaped two-commit fixture whose second commit replaces `("flag-order-drift", …)` with a
second `("substring-arm", …)` — four entries, so `forgeries_total` stays 4 — and re-pins the
block's `mutations_sha256` and `interpreter_sha256` to the tampered bytes.

```
"freeze=c1 rev=c2": {"exit": 2, "reason": "frozen_path_changed"}
"freeze=c2 rev=c2": {"exit": 0, "failing": [],
                     "battery": {"forgeries_total": 4, "v2_green": 4, "v3_green": 0,
                                 "genuine_green": 1, "crash": 0,
                                 "mutations_sha256": "01a121851db108aa…"},
                     "fixtures": ["substring-arm", "duplicate-routed-id",
                                  "stale-mutations-digest", "substring-arm"]}
```

The counter reports **exit 0 with the order class deleted from its own denominator**, and the
fixture list it prints contains `substring-arm` twice and no `flag-order-drift`. Clause 6's
`unnamed` check runs one way only (names in `MUTATIONS` missing from the block), so a block that
names all four classes cannot notice that the list no longer contains one of them. **Smallest
safe correction:** make clause 6 a two-way set equality between the names the block states and
the names in `MUTATIONS`, and add a fifth forgery `mutation-list-substituted` that must be red
under a fixed denominator. The freeze arm catches the same tampering only while the freeze
predates the tool bytes (`freeze=c1 rev=c2` → exit 2) — see finding F1.

**4. `flag-order-drift` — different artefact, and no block-side content binds the order.**
`SKILL.md` is byte-identical to the genuine artefact; the mutation is in round-46 `gate.py`. The
claims declare this ("or, for `flag-order-drift`, the `gate.py` copy in the fixture repo"), so it
is inside the declared contract, but it means the battery's fourth forgery says nothing about
block 24. To show the gap, I made the block assert the *reversed* pair as the correct invocation
and left `gate.py` alone:

```
{"name": "block-asserts-reversed-order", "v2_exit": 0, "v3_exit": 0, "v3_failing": null}
```

**exit 0** on a block whose order row teaches the wrong flag order. **Smallest safe correction:**
carry the required literal in the block (e.g. a `literal:` line in the order row) and add a clause
"the block contains `"-m", "--diff-merges=first-parent"` exactly once"; then the forgery is a
block edit and the class is about the claimed surface. A naive text clause over the whole block
will not do: row 4 already quotes the reversed pair as the defect.

### C2 (`tools/round-47/record.py` `run_battery`)

| # | forgery | what it mutates | exit / failing | verdict |
|---|---|---|---|---|
| 5 | `correction-wrong-seat-total` | the seats correction's total, +1 | 1, `corrections that do not re-derive: 1` | **one defect**; honest |
| 6 | `correction-window-not-empty` | the correction's window → `root..rev` | 1, `corrections that do not re-derive: 1` | **one defect**, but fragile targeting |
| 7 | `correction-ghost-atom` | appends `- corrects path does/not/exist…` inside the corrections section (A5) | 1, `corrections that do not re-derive: 2` | **one defect**, counted twice |

Evidence: `receipts/c2-at-head.stdout`, `receipts/c2-declared-rev.stdout`
(`correction_forgeries 3 / forgeries_green 0` at both).

**5. honest.** It proves a false correction is caught. It does not test the inverse — a *true*
correction that exempts a false atom — which is the shape that actually passes (F5).

**6. honest in intent, fragile in targeting.** `non_empty` rewrites the *first* `empty in A..B`
in the whole card. At the current revisions that is the correction line, but it is not anchored
there: I scored a card whose round-46 atom sentence uses the phrase "is empty in 0425224..58eb04b6"
and the forgery then mutated the **claim**, going red for a different reason
(`receipts/c2-attacks-31b092d1.stdout`, case `battery-window-target-fragility`: failing
`mismatches 1 != 0`, `mismatches [window/46]`, `corrections_bad 0`). **Smallest safe correction:**
anchor the replacement on the `- corrects window` line, not on a phrase search.

**7. honest after A5.** Before A5 it appended the ghost line at the end of the card, outside the
corrections section, where `CORR_HEAD`'s body never reaches it — a no-op (A5's own commit message
says so). It is now inside and red; it is counted twice (nonexistent path **and** unknown
class/key), which is one defect class with two symptoms, not two defects.

## Findings — R47-C1

**F1. The freeze that binds C1 is chosen after the tool's last edit, and the frozen file's own
freeze makes the counting command exit 2.**
The frozen claims define the freeze as the commit that first carries the file and `tools/round-47/`,
re-derived by `git log --format=%H -1 -- plans/round-47-claims.md`. At the declared measured
revision `a0753786` that command returns **`62e33f7d`** (A2), and the first-carrying commit is
`5017e1f7`. The SCORECARD declares **A6 `f54b3b6d`**, which is neither — it is the last commit
that touches `tools/round-47/`. Measured:

```
$ python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f7 --rev a0753786 --no-battery
exit 2  reason frozen_path_changed
        ['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/exact.py', 'tools/round-47/record.py']
$ python3 -I -B tools/round-47/exact.py --root . --freeze 62e33f7d --rev a0753786 --no-battery
exit 2  reason frozen_path_changed
$ python3 -I -B tools/round-47/exact.py --root . --freeze f54b3b6d --rev a0753786
exit 0  failing []  battery 4 / 4 / 0 / 1 / 0  frozen_path_changed []
```

Receipts `c1-claims-freeze-at-declared-rev` (sha `79fd40f3c489639f…`), `c1-claims-freeze-rev-line`
(sha `a11dd329b676e99c…`), `c1-declared-pair` (sha `68ea3e3f764d88bd…`). This is the A1
"unreachable by construction" class again, one level up: the claim's target is reachable only by
re-declaring the freeze as the commit whose bytes define the denominator — so the freeze arm can
never constrain the counter's content, only later edits to it. **Smallest safe correction:** freeze
at the claims' own definitional commit and land no later edit to `tools/round-47/` or the claims
file; if a tool defect is found after the freeze, land it as a *disclosed* second freeze (A1 style)
*and* state the counting command with that freeze, so the `<FREEZE>` token in the claims file and
the freeze in the record are the same object.

**F2. The landing block fails the frozen counter; the block was repaired after the landing.**
`exact.py` as frozen (`5017e1f7`, sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`
— the exact value block 24 pins) scoring the block at `e856beb5`:

```
exit 1  failing ['arm cells not exact vocabulary tokens: ["symbol: the arm cell must equal one token …",
                                                         "once: every row names exactly one routed id …",
                                                         "digest: `mutations_sha256` is sha256 …",
                                                         "order: the gate's argv literal is required …"]']
```

Receipt `c1-freeze-blob-vs-landing` (sha `f8c7899fae9e0717…`). The landed arm cells were prose
sentences; clause 5 was only satisfied by A2 `62e33f7d` ("block 24 arm cells carry only the
token"), which is **after** the landing. So `c1-at-A4/A6/A7` measure a post-landing repair, not
the landing, and the round's own before/after pair is measured on two different artefacts.

**F3. Clause 7 is not a clause about block 24** — see forgery 4: a block that asserts the reversed
pair scores exit 0. Also note clause 9's `v2_green 4` is green by construction of the v2 profile
(it has no order clause and no digest clause), so it is evidence about the loose profile only.

**F4. Clause 8 exempts the block's own interpreter from the line-selector rule** (`check_refs`
skips `SELF`), while the claims' clause 8 says *every* reference carries a line selector. Minor,
but the frozen text and the frozen code disagree; the code is the kinder one.

**F5. Neither counter's `--selftest` is runnable as documented (R46-CL8, still open).**
`python3 -I -B tools/round-47/exact.py --selftest` → **exit 2**, argparse usage error
(`the following arguments are required: --root, --freeze, --rev`), because `parse_args()` runs
before the `args.selftest` branch. Same for `record.py`. With dummy required args the case sets do
run and pass: `EXACT_SELFTEST: cases=16 failures=0`, `RECORD_SELFTEST: cases=10 failures=0`. No
receipt in the round records a selftest run.

## Findings — R47-C2

**F6. The counter is green on its own record, whose after-cell contradicts the receipt it cites.**
At HEAD `31b092d1` the R47-C2 row states `atoms 50 … exempted 2 <= 3`, citing `c2-at-A7.json`;
that receipt reports `atoms 42`, one exempted atom, and 2 parsed corrections while the card
contains four `- corrects` lines:

```
{"row_atoms": true, "receipt_atoms": 42, "row_exempted": true, "receipt_exempted": 1,
 "receipt_corrections": 2, "card_corrects_lines": 4}
```

(`receipts/c2-receipt-vs-row.stdout`, sha `f7d9891bafad0b12…`; the same 42 vs 50 at `a0753786`.)
`atoms 50` is the A4 number, carried over after the graded window moved. The counter cannot see
this because the claim table's numbers are not an atom class — `atoms`, `exempted`,
`corrections`, `rule_blocks`, `refs` are all machine-checkable and none is re-derived. **This is
the R46-V3 defect class (a cell measured at the wrong revision) inside the record that claims to
close it.** Smallest safe correction: add a `receipt` atom class that re-reads the cited
`.ufo/waves/round-47/l1/scores/*.json` and compares `rev`, `atoms`, `refs`, `exempted`,
`corrections` and the battery counts to the numbers the row states.

**F7. `axes` corrections are unparseable — two of the four landed correction lines are dead text.**
`CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")` has no `axes`
alternative, while the docstring, `corrects()` and the claims' clause 3 all require an `axes`
correction. Consequence, measured at `31b092d1`:

```
{"name": "false-axes-correction-coverage", "exit": 0, "failing": [], "corrections": 2}
{"name": "false-axes-correction-depth",    "exit": 0, "failing": [], "corrections": 2}
```

A correction line reading `- corrects axes coverage: 999/999` leaves the counter **green**. The
`axes` branches in `corrects()` are unreachable (and one of them references an undefined `atom` —
a copy-paste from `derive`), so `corrections 2` in the record means "2 of the 4 `- corrects`
lines the card contains", not "both re-derived". **Smallest safe correction:** add `axes` to
`CORR`, delete the dead branch, and require `parsed == corrects_lines` as a clause.

**F8. Exemption is class/key-only, so a true statement that cannot express the defect launders it.**
`exempt()` matches on `(class, key)` and never compares the atom's claim with the correction's.
At A4, with the round-45 seats atom inside the window:

```
{"name": "launder-seats-pair-55-17", "exit": 0, "failing": [],
 "exempted": ["seats/45", "window/46"]}                       # Wave 1: 40; wave 2: 32 -> 55; 17
{"name": "launder-seats-sum-60-20-new-correction", "exit": 0, "failing": [],
 "exempted": ["seats/45", "seats/46", "window/46"]}            # Waves: 40 + 40 = 80 -> 60 + 20 = 80
```

(`receipts/c2-launder-A4.stdout`, sha `4e369aee3f378353…`.) A 60/20 split of the true 80 is
exempted by a correction that states `2 waves, 80 seats total` — the correction's grammar
(`<n> waves, <total> seats total`) cannot express a split, so the split is never re-derived and
`exempted 3 <= 3` is exactly full. Worse, the *honest* repair is rejected while the laundering is
accepted:

```
{"name": "correction-states-the-split", "exit": 1,
 "corrections_bad": 1}     # "- corrects seats round-45: wave 1: 55 seats; wave 2: 17 seats"
```

**Smallest safe correction:** an exemption must state the atom's own claim — for a `seats` pair,
`wave 1: <A> seats; wave 2: <B> seats`; for a sum, `<A> + <B> = <C> seats` — and `exempt()` must
require `CORR_SEATS`-style equality with the atom's `claim`, not just its class and key.

**F9. A placeholder window atom is exempted by any empty window of that round; its base and
pathspec are never checked.** `exempt()` returns `True` for a `pair is None` atom whatever the
correction says, so the concrete base and pathspec in the claim are ungraded:

```
{"name": "launder-window-base-pathspec", "exit": 0, "failing": [], "exempted": ["window/46"]}
# "0425224..<tip> -- tools/round-46 plans/round-46-claims.md" -> "13a9e9e1..<tip> -- SKILL.md"
```

The R46-V2 defect ("the record's own empty window") is closed only in the sense that *a* concrete
empty window now exists; the sentence's own window is still unverified. **Smallest safe
correction:** a `window` exemption must quote the atom's base and pathspec and the counter must
reproduce *that* window as empty (or require the atom's sentence to be rewritten, which is what
the corrections section already promises).

**F10. `rev` atoms are resolution-only, so the revision an after-cell was measured at is
unbound.** Every backticked 7–40 hex token is checked with `rev-parse --verify` plus
ancestor-of-`rev`; nothing ties the token to the sentence around it. Measured at `a0753786`:

```
{"name": "after-cell-measured-at-swapped", "exit": 0, "failing": []}
# the C1 row's measured-at cell `1e2c310295` replaced by `13a9e9e1` (the base, where C1 is red)
```

That is exactly R46-V3's class (the before-cell's revision), still open. **Smallest safe
correction:** a `receipt` atom class as in F6 binds the revision a row names to the receipt's
`rev`; a bare `rev` atom cannot.

**F11. `record.py` is unpinned and has no freeze arm — C2 is self-certifying.**
No sha256 of `tools/round-47/record.py`
(`abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7`) appears in `SKILL.md`,
`SCORECARD.md` or `plans/round-47-claims.md` (`git grep` at `a0753786`: nothing), and the CLI has
no `--freeze` (`--freeze` → argparse error). A three-line edit to a copy (drop the `mismatches`
check, drop the `corrections` floor, empty the battery key list) scores the **base card** — the
round's own before-state, 4 mismatches and 0 corrections — green:

```
$ python3 -I -B tpy/tools/round-47/record.py --root <LANE> --rev 13a9e9e1
exit 0  failing []  mismatches [(seats,45),(window,46),(axes,coverage),(axes,depth)]  corrections 0
        battery 3 / 0
```

Receipt `c2-tampered-interpreter` (sha `11b780c18e1458a5…`), tampered bytes sha
`2d2d964f7a004f41…`. Contrast C1, which pins its interpreter in the block: C2's instrument is
bound only by the freeze declaration, and F1 shows the freeze is chosen after the last edit.
**Smallest safe correction:** state `interpreter_sha256` for `record.py` in the round-47 section
(as block 24 does for `exact.py`) and re-derive it as an atom; add the `--freeze` arm.

**F12. The graded window scrolls, so one before-mismatch left scope instead of being repaired.**
`sections()` takes the last two `## Round N` headings. At the base the last two are 45 and 46
(50 atoms, mismatches `seats/45`, `window/46`, `axes/coverage`, `axes/depth`); from the landing
onward they are 46 and 47 (42 atoms at `a0753786`, 44 at `31b092d1`), and the round-45 sentence
**still reads `Wave 1: 40 seats; wave 2: 32 seats`** at HEAD. The after-cell's "4 → 0 mismatches"
therefore compares different populations, and one of the four before-mismatches is not repaired
but ungraded. The `seats round-45` correction is kept alive only by the "historical" clause (A3).
This is a scope choice the claims declare ("the last two `## Round N` sections"), so it is a
tradeoff, not a bug — but the claim's before/after phrasing ("the current self-assessment is
re-derived") is then true of a moving target, and the record must say which atoms left scope.

## Predicate verdicts

**R47-C1 — predicate too weak; here is what closes it.**
The text clauses are tight (equality over the arm cell, exactly-once ids, both pins, the flag
literal). What is weak is the *binding*: the denominator (`MUTATIONS`) and the artefact can be
co-forged in the commit named as the freeze (F1, forgery 3), the round's landing fails clause 5
(F2), clause 7 does not read the block (F3), and clause 4 is not isolated by its own forgery
(forgery 2). Closing set, in order of value: (a) freeze at the claims' definitional commit and
make `tools/round-47/` immutable from it; (b) two-way set equality between the block's stated
mutation names and `MUTATIONS`; (c) the 4-row duplicate-id fixture; (d) the required order literal
inside the block plus a clause over it; (e) restate the kill rule with `order-ish`.

**R47-C2 — predicate too weak; here is what closes it.**
Five classes work as implemented and the base control is honest (4 mismatches at `13a9e9e1`,
exit 1). But `mismatches == []` is not a claim about the record's truth: exemptions are
class/key-only (F8), placeholder windows are exempted by any empty window (F9), `axes` corrections
are unparsed (F7), revisions are resolution-only (F10), the record's own claim-table numbers are
not atoms and two of them are false (F6), the interpreter is unpinned (F11), and the window
scrolls (F12). Closing set: (a) value-bound exemptions (a correction must state the atom's own
claim, in a grammar that can express it); (b) `axes` in `CORR` and `parsed == corrects_lines`;
(c) a `receipt` atom class binding the numbers and the `rev` a row cites to the receipt it cites;
(d) `interpreter_sha256` for `record.py` plus a `--freeze` arm; (e) state in the record which
atoms left the window.

## Not run / limits

- I did not mutate the frozen originals; every mutation is a copy in scratch
  (`receipts/tampered-exact.py`, `S/tpy/.../record.py`, `S/t5017/...`).
- I did not run the two counters' `--selftest` as documented — they are unrunnable that way
  (F5); the case sets pass with dummy required args (16/0, 10/0).
- I did not attack `tools/round-46/gate.py`'s `history_touched` beyond the flag-order literal;
  the merge/`--diff-merges` semantics are round-46's surface and R46-CL1 stays open as recorded.
- The lane advanced under me (A5–A7). Numbers are pinned to the revisions named above; the A4
  laundering receipts are kept because that card is the one the round recorded as measured.
