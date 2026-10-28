# CritC2Scope — round 47, seat critique of R47-C2's scope

**Seat**: leaf critic, read-only. **Lane**: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Base**: `13a9e9e1`. **First freeze**: `5017e1f7`. **Declared freeze / measured rev (card)**:
`07d2894e` (A5). **Lane tip while writing**: `f7d6e58d` (moved 6× during this seat; every number
below is rev-pinned).

**Verdict — predicate too weak, here is what closes it.** Clause 5 (`sections` = the last two
`## Round N` headings) is a *scope choice*, not a check: the claimant picks the window, the
window moves whenever a heading is added, and `SCORECARD.md`'s heading parser counts duplicate,
in-fence and non-round headings. A false atom is therefore retired by **adding a heading**, not by
correcting it. Demonstrated in a committed fixture repo: red at `dbe5c8ea` (exit 1), green at
`fccbb3c9` (exit 0) after appending a verbatim duplicate of the round-47 section, with the false
revision still printed at line 3601 of the same card.

---

## 1. How much of `SCORECARD.md` the claimed scope covers

Measured with the counter's own `sections()` / `collect()` / `collect_axes()` over
`git show <rev>:SCORECARD.md` (`fixtures/verify.py <REV> <BASE>`, receipts `receipts/verify-tip.json`,
`receipts/verify-head.json`, `receipts/probe2-a631bba0.json`).

| | tip `31b092d1` | base `13a9e9e1` |
|---|---|---|
| card lines | 3724 | 3661 |
| in-scope lines (2 sections + `## Owned axes` body) | 121 | 155 |
| **line share** | **3.25 %** | **4.23 %** |
| section-borne atoms derived in scope | 42 (incl. 2 axes) | 48 (incl. 2 axes) |
| section-borne collectible atoms (all `## Round N` + round-like) | 606 | 588 |
| **atom share of section-borne** | **6.93 %** (42/606) | **8.16 %** (48/588) |
| front-matter atoms read | 2 of 57 | 2 of 57 |
| level-2 sections | 77 | 75 |
| `^## Round \d+` headings | 34 (46, 47 in scope) | 33 (45, 46 in scope) |
| round-like sections the pattern never matches | 33 | 33 |

**What the rest contains** (`receipts/probe2-a631bba0.json`, buckets by heading):

| bucket | sections | lines | atoms | read? |
|---|---|---|---|---|
| `## Round N` matching | 34 | 1517 | 500 | 40 (8 %) |
| `## luna-round-N`, `## arc2/arc3-loop1-roundN`, `## Post-review correction` | 33 | 1919 | 104 | **0** |
| front matter (`Current assessment`, `## Owned axes`, `Reconciled current state`, `Open gaps`, `Measurement recipes`, `Verdicts`, `Interactive round-1 recovery`, `Capabilities`, `Saturation`) | 9 | 266 | 57 | 2 |
| `## Record corrections — round 47` | 1 | 17 | 0 | 2 lines |

Load-bearing atoms that are **never derived**: `## Owned axes` holds 33 collectible atoms
(5 `.ufo/waves/…` paths, 28 backticked revisions — e.g. the `e1c83313`/`4d62ee5a` history inside the
coverage and depth rows) of which only the *leading fraction* of two rows is read; `## Capabilities`
holds 21 path/rev atoms, 0 read; the `calibration` row is not matched by `AXIS_ROW` at all
(`coverage|depth` only). The three atoms the round-46 spot-check found false (R46-V1 seat counts,
R46-V2 window, R46-V3 before-cell revision) live in exactly this unread mass.

Reading the claim literally — "the last two `## Round N` sections plus the current `## Owned axes`
leading fractions" — the measurement matches the claim. The claim is *true and narrow*: **96.75 % of
the card's lines, 93.1 % of its section-borne atoms and 55 of its 57 front-matter atoms are outside
the re-derivation.**

## 2. Is `sections == 2` a boundary the round can move to dodge an atom? Yes.

`sections()` = `re.finditer(r"(?m)^## Round (\d+)", card)[-2:]`. No uniqueness check, no fence
awareness, no relation to the round being scored. Four moves, all measured:

| # | move | fixture | red-before | after |
|---|---|---|---|---|
| D1 | **push forward**: one `## Round N` heading with an empty body | append `## Round 47 — landing\n\nno atoms yet` | `2e4ae434`, 50 atoms, 2 exempted | `2e4ae434`: exit **0**, 26 atoms, 1 exempted — round-45's seat atom **and its exemption** vanish |
| D2 | **duplicate the newest heading** | copy the round-47 section verbatim | see §4 fixture | exit **0**, `sections [round-47, round-47]` |
| D3 | **in-fence heading**: a heading inside a code block is a section boundary | append ` ```markdown\n## Round 47 — example\n``` ` | `2e4ae434`, exit 1 | exit **0**, `sections [round-46, round-47]` where "round-47" is a fenced example, 26 atoms |
| D4 | **self-exclusion by heading string**: the round writes its record under `## r47` | same three false atoms under `## r47` vs `## Round 47` | `## Round 47`: exit **1**, 3 mismatches | `## r47`: exit **0**, receipt **byte-identical** to the honest card (`2c231d10b614327e`) |

D2/D4 receipts are indistinguishable from honest ones: at `2e4ae434`,
`evaluate_text(card)` and `evaluate_text(card + corrupted round-45 rev + "## Round 46 — duplicate heading")`
both yield receipt sha `88f83d292a007ca2`; and `evaluate_text(card)` equals
`evaluate_text(card + false `## r47` section)` at `2c231d10b614327e`. The receipt carries no card
digest and no section offset, so an auditor cannot tell a laundered pass from a clean one.

**The grammar is 2-of-67.** 67 headings in the card name a round (34 matching + 33 round-like luna/
arc sections); the counter reads the last two *matching* ones — 2 of 67. Existing duplicates
(`## Round 25 attempt 3`, `## Round 34, run-6 re-dispatch`) already show the parser accepts two
headings for one round; `heads[-2:]` then silently picks whichever pair sits nearest the EOF.

**What blocks the dodge today, and why it is an accident.** `atoms_by_class[c] == 0` (the class
coverage clause) is the only guard: `receipts/verify-tip.json` cases `A2`, `A3`, `A6` go red with
`no atoms of class(es) ['seats']`, not because the counter saw the corruption. It holds only because
the landed round-47 section is a **one-wave round that writes no seats atom** — `SEATS_PAIR`
requires both waves and `SEATS_SUM` requires `a + b = c`; the natural sentence `Wave 1: 75 seats`
yields **0 atoms** (`fixtures/` seat-shape probe, `receipts/verify-head3.json`). Add the true
sentence `Waves: 75 + 0 = 75 seats` to the round's own section and the guard is gone.

## 3. Committed fixture that falsifies the predicate at the current tip

Fixture repo `$S/fx/lane` (`git clone --no-hardlinks`, `git -C rev-parse --show-toplevel` verified,
throwaway identity only there). Two commits on top of `f7d6e58d`:

```
commit A dbe5c8eadc2b33bf8e19fc8297eeb23a51914155
  SCORECARD.md: round-47 section gains the true sentence `Waves: 75 + 0 = 75 seats.`
                round-46 section's first backticked rev becomes `deadbee85f9d8617fe242fc116819b8055dfc4c7`
commit B fccbb3c92bec30f7513522080b01273365ff638a
  + a verbatim duplicate of the round-47 section appended (49 lines, no edits)
```

| run | command | exit | receipt |
|---|---|---|---|
| base `f7d6e58d` | `python3 -I -B tools/round-47/record.py --root "$D" --rev f7d6e58d` | 0 | `receipts/fx-base.out`, sha `ba75e586…` — `sections [46,47]`, `atoms 44`, `exempted 1` |
| **A `dbe5c8ea`** | `… --rev dbe5c8ea` | **1** | `receipts/fx-A.out`, sha `0a5e9168…` — `mismatches ['`deadbee85f…`']` |
| **B `fccbb3c9`** | `… --rev fccbb3c9` | **0** | `receipts/fx-B.out`, sha `02a96b60…` — `sections ['round-47','round-47']`, `atoms 40`, `mismatches []`, `exempted 0`, `met_target true` |

At B, `git show fccbb3c9:SCORECARD.md` still prints
`3601: Base `deadbee85f9d8617fe242fc116819b8055dfc4c7`. Frozen claims …` and carries two
`## Round 47` headings (3680, 3728). Nothing was corrected; the window moved.

## 4. Landed defect: the round's own C2 cells contradict the receipt they cite

The scope slide is not hypothetical — it already fired on this round, and the record kept the
pre-slide numbers:

| measurement | sections | atoms | exempted |
|---|---|---|---|
| `1e2c3102` (A4, *before* the record section) | `[45,46]` | **50** | **2** |
| `07d2894e` (A5, the declared freeze) | `[46,47]` | **41** | **1** |
| `31b092d1` (tip at measurement) | `[46,47]` | 44 | 1 |
| `09a9f912` (tip at write time) | `[46,47]` | 44 | 1 |

`receipts/rev-1e2c3102.out` sha `c609b3e1…`, `receipts/rev-07d2894e.out` sha `d366b080…`,
`receipts/rev-31b092d1.out` sha `d24410d1…`; the same figures are in the lane's own
`.ufo/waves/round-47/l1/scores/c2-at-A5.json` (`atoms 41`, `exempted 1`).

Against that, `SCORECARD.md@31b092d1`:

- line 3701 (`## Round 47`, R47-C2 row): `atoms 50`, `exempted 2 <= 3`, receipt
  `c2-at-A5.json`, measured at `1e2c310295`. The cited receipt says `41 / 1`. The prose above the
  table says "**The declared freeze is A5 `07d2894e`** … and the measured revision of both claims".
- line 25 (`## Owned axes`, calibration row): "re-derives 50 atoms … `exempted 1 <= 3` …
  (`c2-at-A7.json`)". `c2-at-A7.json` says `atoms 42`. The row mixes the pre-slide atom count with
  the post-slide exemption count.

So the C2 "after" evidence is not reproducible at the revision the round declares as measured, and
one of its two required corrections (`corrects seats round-45`) now exempts **nothing** — at
`a631bba0`+ the `exempted` list is `[window:46]` only; the seats line survives on the A3
"historical" carve-out (`key < oldest in-scope round`) and on nothing else. `corrections 2` is met by
a correction whose atom is no longer in the window.

## 5. The correction mechanism reaches 4 of the 5 classes, and deletion is a free repair

- `CORR = r"^- corrects (seats|window|path|rev) (\S+): …"` — **`axes` is not admitted**. The card
  carries 4 `- corrects` lines, the counter parses **2** (`receipts/verify-tip.json`
  `corrects_lines 4 / corrects_parsed 2`). Claims clause 3's sentence "an `axes` correction must
  state `<resolved>/<total>`" is therefore unreachable — vacuously satisfied. `corrects()` also
  contains two `if cls == "axes":` branches; the second is dead.
- Deleting the two axes correction lines changes nothing: exit 0, same receipt
  (`verify-tip.json` case `C0`).
- An axes atom cannot be exempted even with the intended syntax: coverage head regressed to
  `137/138` stays red with `- corrects axes coverage: 137/138` appended
  (`verify-tip.json` cases `B0`/`B1`).
- **Deletion as repair**: removing a corrupted token from the card makes the counter green with no
  correction line — `a631bba0` corrupt path atom deleted → exit 0 (`receipts/verify-head2.json`
  case `D2`, `atoms 41`); corrupt rev replaced by prose → exit 0
  (`receipts/verify-head3.json` case `F4`). Clause 1 (`mismatches == []`) cannot distinguish
  "made true" from "removed".
- A `window` placeholder exemption ignores the correction's key: one `- corrects window round-46`
  line exempts **every** placeholder window in scope (two here: `receipts/e16-placeholder-exemption.json`,
  `atoms 51`, `exempted 3` — one line short of `EXEMPT_MAX`).

Corollary of the slide: at the tip, appending `## Round 46 — duplicate heading` turns the *valid*
`corrects window round-46` into `corrections that do not re-derive: 1` (`verify-tip.json` case
`A2`) — the verdict on a correction line is a property of the window position, not of the line.

## 6. Smallest safe correction (for the round-48 claims; frozen bytes untouched)

Ordered by value per line:

1. **Pin the window at freeze.** `--sections <A>,<B>` (or `sections_sha256` over the two section
   texts declared in `plans/round-4N-claims.md`), and require the pair to be
   *(round being scored, previous round)*. Re-choosing the window at scoring time then becomes a
   frozen-path change → exit 2. Closes D1–D4 and §3 in one clause.
2. **Make the receipt self-identifying**: `card_sha256`, per-section `sha256` + line offset.
   Today two different cards produce byte-identical receipts (§2); without this, no auditor can
   tell "no record section written" from "record section written where the counter does not look".
3. **Strip fenced blocks before heading scan**, and require the two in-scope round numbers to be
   distinct and strictly ascending (cheap, closes D2/D3 even without 1; the card already carries
   duplicate round numbers).
4. **Atom preservation**: each in-scope section's atom multiset at `--rev` must be a superset of its
   multiset at the previous measured revision unless a correction line declares the removal.
   Closes deletion-as-repair (§5).
5. **Admit `axes` in `CORR`** and delete the dead second `axes` branch in `corrects()`. Otherwise
   the two repairs this round actually made (coverage `138/138`, depth `24/24`) are unrecorded and
   clause 3's axes sentence stays vacuous.
6. Bind the placeholder-window exemption to the correction's key (no cross-round exemption).

Also worth fixing in the record itself (not the counter): re-state §4's two cells at the declared
freeze (`atoms 41 / exempted 1` at `07d2894e`, or move "measured at" to `1e2c3102` and say so), and
note that a one-wave round's seat count is expressible only as `Waves: N + 0 = N seats`.

## 7. Receipts (all read-only; scratch removed after copy)

`receipts/` (in this directory) holds every stdout/stderr artefact cited above; `fixtures/` holds
the drivers. Nothing was written outside `.ufo/waves/round-47/w1/CritC2Scope/` and
`/fast/scratch/hyaku/kaidoku-r47/CritC2Scope` (now removed).

| receipt | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| `base-13a9e9e1.out` | `python3 -I -B tools/round-47/record.py --root . --rev 13a9e9e1` | 1 | `53d81a3d…` | 2026-10-28T17:56Z |
| `landing-e856beb5.out` | `… --rev e856beb5` | 0 | `facc68dc…` | 2026-10-28T17:57:38Z |
| `rev-1e2c3102.out` | `… --rev 1e2c3102` | 0 | `c609b3e1…` | 2026-10-28T17:59Z |
| `rev-07d2894e.out` | `… --rev 07d2894e` | 0 | `d366b080…` | 2026-10-28T17:59Z |
| `rev-31b092d1.out` | `… --rev 31b092d1` | 0 | `d24410d1…` | 2026-10-28T17:59:42Z |
| `fx-base.out` | `… --root $S/fx/lane --rev f7d6e58d` | 0 | `ba75e586…` | 2026-10-28T18:00:54Z |
| `fx-A.out` | `… --rev dbe5c8ea` | **1** | `0a5e9168…` | 2026-10-28T18:01:07Z |
| `fx-B.out` | `… --rev fccbb3c9` | **0** | `02a96b60…` | 2026-10-28T18:01:13Z |
| `verify-tip.json` | `python3 -I -B fixtures/verify.py 31b092d1 13a9e9e1` | 0 | `3ac46873…` | 2026-10-28T18:00:10Z |
| `verify-head.json` | `… verify.py a631bba0 13a9e9e1` | 0 | `7b4bf5e5…` | 2026-10-28T17:58:24Z |
| `verify-head2.json` | duplicate/deletion fixtures at `a631bba0` | 0 | `e260c938…` | 2026-10-28T17:59Z |
| `verify-head3.json` | seat-shape + deletion fixtures | 0 | `423be626…` | 2026-10-28T17:59Z |
| `verify-head4.json` | decisive G2 transform via `evaluate_text` | 0 | `3c61d715…` | 2026-10-28T17:59Z |
| `dodge-2e4ae434.json`, `dodge2-2e4ae434.json`, `fence-2e4ae434.json`, `laundry-base.json` | D1–D4 fixtures at `2e4ae434` / `13a9e9e1` | 0 | `69ae313b…`, `0dd8b955…`, `ef3e376d…`, `dff489d0…` | 2026-10-28T17:54–17:56Z |
| `probe-2e4ae434.json`, `probe2-*.json`, `probe4-2e4ae434.json` | coverage/atom inventories | 0 | `3d7734d7…`, `77b3caa5…`, `64e9cd8c…`, `65710383…` | 2026-10-28T17:55–17:59Z |
| `e16-placeholder-exemption.json` | one extra placeholder-window sentence, `2e4ae434` | 0 | `ce0e447a…` | 2026-10-28T18:02:36Z |

Note on `--json-out`: `gate.out_path` (`tools/round-46/gate.py:205`) refuses any path outside the
lane root, so a seat that may not write into the lane cannot emit a receipt *file*; stdout capture
is the only route (first attempt, exit 2, `{"reason": "--json-out outside the lane root: …"}`).
The D1–D4 and §2 fixtures drive `record.evaluate_text(card, files, root, rev)` — the exact function
`evaluate()` calls with the same `git show <rev>:<path>` accessor — because a mutated card cannot be
committed to the read-only lane; the §3 fixture is a real two-commit repo where the counter was run
as the CLI.

## 8. Not run / limits

- Not run: the C1/craft-block counter (`tools/round-47/exact.py`) — outside this seat.
- Not run: `--selftest`; not run: any mutation of the lane tree; no commits outside the scratch
  clone; no installs (nothing needed).
- Unverified by me: whether the L1 intends `1e2c310295` or `07d2894e` as the C2 measured rev — the
  card states both; §4 gives both measurements so either choice can be made honest.
- The lane tip moved from `2e4ae434` to `f7d6e58d` while this seat ran; §1's table is pinned to
  `31b092d1` (the last tip I measured both buckets at). Atom counts drift with each landed card
  edit without any scope change (`42` at `a631bba0` → `44` at `31b092d1`, same two-section window),
  which is itself an argument for §6.2: the receipt should carry the card digest it was computed
  over, so a drifting count can be attributed to a card edit rather than guessed at.
