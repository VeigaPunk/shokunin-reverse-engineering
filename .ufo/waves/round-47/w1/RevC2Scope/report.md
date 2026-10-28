# RevC2Scope — section scoping of the two frozen round-47 claim instruments

Seat: `RevC2Scope` (reviewer, leaf). Round 47, wave 1, no landing performed.
Assignment: *which `## Round N` headings does the counter select (last two in file order),
and can an amendment appended AFTER the last section hide a false atom?*

Short answer: **the counter selects the last two `## Round N` headings by file position and
nothing else, so yes — an appended section that carries no atoms hides a false atom in an
earlier round with zero corrections, and the landing round does this to round 45 automatically.**
It is a real hole for this claim's own landing, and it is worse than a silent drop: the landing
*orphans* the correction written for the dropped round, so the honest repair cannot survive its
own landing. Evidence below, with fixtures, commands, exit codes and stdout digests.

---

## 0. Bytes evaluated (pinned)

| object | identity |
|---|---|
| assigned freeze | `5017e1f7299c3a812e87e7950148f54313dd279e` |
| `tools/round-47/record.py` @ freeze | blob `1f8e7928…`, sha256 `af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d` |
| `tools/round-47/exact.py` @ freeze | blob `fb21a166…`, sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| `tools/round-46/gate.py` @ freeze | sha256 `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` |
| `plans/round-47-claims.md` @ freeze | blob `81aeb65e…` |

All counters below were executed from a byte-frozen copy of those files materialised with
`git cat-file -p 5017e1f:<path>` under
`/fast/scratch/hyaku/kaidoku-r47/RevC2Scope/frozen/tools/`, never from the lane worktree.
`record.py@freeze` and `exact.py@freeze` are re-attached to this report dir for independent
re-hashing.

Two scratch fixture families (each an independent git repo, `git -C "$D"` on every call,
`rev-parse --show-toplevel` asserted equal to `$D` before the first commit):

- `S=/fast/scratch/hyaku/kaidoku-r47/RevC2Scope`
- synthetic cards: `$S/fix/repo6` (driver `drive.py`, seed `c1=bed34b7d41af`, `c2=e07372b7ddd6`)
- the lane's own bytes replayed: `$S/fix/lane` (full `git clone --no-hardlinks`, pinned to
  `62e33f7dd75c8e3285967b26419842c106f6c965`, driver `replay.py`)

The counter under test is always:

```
python3 -I -B frozen/tools/round-47/record.py --root <FIXTURE> --rev <REV> --json-out <FIXTURE>/receipts/<name>.json
```

Scratch `$S` was removed after these receipts were copied here (see `receipts/`).

---

## 1. BLOCKER-1 — the frozen pair is no longer measurable together

`exact.py` refuses at every revision at or after `9018c53b`:

```
$ git -C <lane> log --format='%h %s' 5017e1f..62e33f7 -- tools/round-47
62e33f7d round-47: A2 - make the window forgery a real forgery; block 24 arm cells carry only the token
9018c53b round-47: freeze amendment A1 - drop the unreachable window-pair clause
$ git -C <lane> log --format='%h %s' 5017e1f..62e33f7 -- plans/round-47-claims.md
62e33f7d … / 9018c53b …
```

| command | exit | receipt | receipt sha256 |
|---|---|---|---|
| `exact.py --root <clone> --freeze 5017e1f… --rev 62e33f7…` | **2** | `receipts/c1-62e33f7.json` | `d6ad1d9e…` |
| `exact.py --root <clone> --freeze 9018c53b --rev 62e33f7…` | **2** | `receipts/c1-A1freeze-62e33f7.json` | `114128a9…` |
| `exact.py --root <clone> --freeze 62e33f7 --rev 62e33f7` | 0 | `receipts/c1-freeze-eq-rev.json` | `7d406926…` |

`frozen_path_changed` names `plans/round-47-claims.md`, `tools/round-47/`,
`tools/round-47/record.py` in the first, and `tools/round-47/` + `record.py` in the second.
The only configuration that scores is `--freeze == --rev`, i.e. a zero-length history window —
the very arm that proves the frozen surface did not change. So R47-C1 is currently satisfiable
only vacuously, and its `--freeze <FREEZE> --rev <REV>` counting command exits 2 for every
`REV > FREEZE`.

**What the claim would have to say.** One immutable freeze commit per frozen surface, stated as
a sha that is *also* the last commit touching `plans/round-47-claims.md` and `tools/round-47/`,
plus a sentence that any later edit to either is a `frozen_path_changed` and therefore a stopped
round, not an amendment. "The declared freeze is the commit that carries this paragraph" is not
machine-checkable: the paragraph is carried by two commits (`9018c53b` and `62e33f7d`) whose
frozen sets differ, and the counter derives its frozen set from whichever one it is handed.

## 2. BLOCKER-2 — R47-C2 has no freeze clause at all

`record.py@freeze` defines `SELF = "tools/round-47/record.py"` and
`CLAIMS = "plans/round-47-claims.md"` (lines 32–33) and **never reads either**:
`grep -n "freeze\|frozen_path_changed\|SELF\|CLAIMS" record.py@freeze` returns exactly three
lines — 32, 33, and line 579, which matches only because `RECORD_SELFTEST` contains `SELF`.
There is no `frozen_path_changed` arm, no digest of its own bytes, and no `--freeze` argument. Consequence, measured:

| counter bytes | `--rev 62e33f7` | receipt |
|---|---|---|
| frozen (`af666ce2…`) | **exit 1**, `corrections_bad: ["window pair names no atom in scope"]` | `receipts/R0-pinned-card-as-is.json` (`708d3b29…`) |
| as committed at `62e33f7` (`fb6d5735…`) | **exit 0**, `failing []`, `mismatches []` | `receipts/am-62e33f7.json` (`7ba2c7b8…`) |

The claims file asserts "a change makes **both** counters exit 2 `frozen_path_changed`". That is
false for C2: only C1's `exact.py` observes the change, and the C2 verdict is produced by bytes
that no C2 clause pins. R47-C2's "frozen instrument" is frozen only by R47-C1's cross-check,
which contradicts the file's own "causal separability … Either lands and scores without the other".

**What the claim would have to say.** Either C2 takes `--freeze`, derives its own blob at that
commit, and fails with `frozen_path_changed`, or the separability sentence is deleted and C2 is
declared dependent on C1. As written, C2 can be made green by editing C2.

## 3. HIGH — the seat's question: an appended section hides a false atom, and orphans its correction

Card shape mirrors the real one: round 45 carries `Wave 1: 40 seats; wave 2: 32 seats` against
dispatched `40 / 36`; round 46 is true; the corrections block carries three lines that re-derive
and exempt nothing (`exempted: []`).

| variant | card | exit | receipt |
|---|---|---|---|
| V1 | rounds 45+46 | **1** `mismatches 1 != 0` | `receipts/V1-false-atom-in-scope.json` (`43f579a9…`) |
| V2b | same card + `## Round 47` with **no atoms**, corrections last | **0**, `sections ["round-46","round-47"]`, `atoms 6`, `mismatches []`, `corrections 3` | `receipts/V2b-empty-appended-section-corr-last.json` (`6cedfcab…`) |
| V3 | V2b + the round-45 seats correction kept | **1** `corrections that do not re-derive: 1`, detail `exempts an atom that does not exist` | `receipts/V3-correction-out-of-scope.json` (`67db0ef2…`) |

V2b is the hole: the false sentence is still in `SCORECARD.md`, **no correction names it**, and
the counter exits 0 — `mismatches` is empty because round 45 is no longer read, not because the
atom was repaired. V3 is the trap: the moment round 45 leaves scope, the correction written for
it becomes a *defect*, so the lander is forced to delete the repair and leave the false sentence.

Replayed on the lane's own card at `62e33f7d` (real bytes, clone):

| replay | exit | receipt |
|---|---|---|
| R0 as-is | **1** (`window pair names no atom in scope`) | `receipts/R0-pinned-card-as-is.json` |
| R1 append empty `## Round 47` after the corrections block | **1** — corrections 2, both bad: `exempts an atom that does not exist` **and** `window pair names no atom in scope`; `atoms 26` | `receipts/R1-append-empty-round47-after-corrections.json` (`32a52eaa…`) |
| R2 same, round section above corrections, round-45 correction withdrawn | **1** (`window pair names no atom in scope`) | `receipts/R2-round47-above-corrections-withdrawn.json` (`1b2bf4f0…`) |
| R3 R2 + the round-46 sentence rewritten to the concrete window `332f4884..58eb04b6` | **0**, `failing []`, `mismatches []`, `sections ["round-46","round-47"]`, `corrections 2` | `receipts/R3-concrete-window-planted.json` (`819554254f…`, identical stdout to the amended-bytes run) |

R3's card still contains, verbatim and in scope of nothing:

```
$ git -C <clone> show 635d21ed:SCORECARD.md | grep -n 'wave 2: 32 seats'
3527:measured revision `1f4b27f8`. Wave 1: 40 seats; wave 2: 32 seats (counts from
```

So the claim's own Before-cell defect (`R46-V1`, the round-45 seat atom) survives untouched in
a green card, four lines below the round that is now "the current self-assessment". The claim's
prose ("the lane's current self-assessment", "the record was corrected") is satisfied by a card
that still prints a number the counter proved false two commits earlier.

**What the claim would have to say.** Pin the audited set explicitly — e.g. "the sections the
landing corrects **plus** the last two `## Round N` headings", or "every section named by a
`- corrects` line **plus** the last two" — and require `sections` in the receipt to equal a
declared list with no round number twice. Add a clause that a correction whose round has left
scope keeps the round in scope (self-extending), so a repair cannot be orphaned by an append.

## 4. HIGH — clause 5 is a tautology

Clause 5: "`sections` is exactly the last two `## Round N` headings of `SCORECARD.md` at `--rev`."
`record.py@freeze` computes `secs = sections(card)` and writes
`"sections": [f"round-{rnd}" for rnd, _ in secs]` into the receipt; nothing compares that value
to anything else, and no clause reads the list back. The clause cannot fail, cannot detect a
duplicate, a re-ordered set, or a truncated body. It is the one clause that could have carried
the scope pin, and it carries nothing.

**What the claim would have to say.** A pinned expected set (round numbers **and** a digest of
each section's text, or at minimum a count of atoms per class per section) compared as equality;
`len(set(rounds)) == len(rounds)`; and a failure mode "section truncated at a `## ` heading".

## 5. HIGH — an embedded `## ` heading truncates a round section silently

`sections()` ends a section at the first `\n## ` after its heading, so any subheading inside a
round section cuts every atom after it, and the receipt's `sections` list is unchanged.

| variant | card | exit | receipt |
|---|---|---|---|
| V4 | round 45 with `## Learning trends` above the false seats sentence | **0**, `sections ["round-45","round-46"]`, `atoms 10` | `receipts/V4-embedded-heading-truncation.json` (`f264ae07…`) |
| V1 (honest, same card without the subheading) | — | 1, `atoms 11` | `receipts/V1-false-atom-in-scope.json` |

The only tell is `atoms 10` vs `11`; no clause compares atom counts, and the section list is
byte-identical to the honest card. A round section that grows a `## Evidence` or
`## Freeze-integrity disclosure` heading (the round-45/46 sections use bold for this reason)
silently loses its tail.

**What the claim would have to say.** "A `## Round N` section ends only at the next
`^## Round ` heading" (or at `## Record corrections`), and a per-section atom count pinned in the
receipt.

## 6. HIGH — window exemptions are unbound and `A..A` is accepted

Two independent looseness arms in one class:

1. `exempt()` for `window` returns `True` for **any** correction of class `window` whenever the
   atom's pair is `None` (`if atom.get("pair") is None: return True`) — the correction's
   round key is not compared. `receipts/V8-misdirected-window-exemption.json` (`90c612fa…`,
   exit **0**): the correction names `empty in <c1>..<c1> -- tools/x/` (round 45's window) and
   the atom it actually exempts is round 46's `<tip>` placeholder.
2. `window_empty()` runs `git log A..B`; `A == B` is empty for every pathspec, so the letter of
   clause 3 ("a window the counter itself reproduces as empty") is met by a window that proves
   nothing. V2b's corrections include `empty in <c1>..<c1> -- SCORECARD.md` and re-derive green
   (`corrections_bad: []`).

`receipts/V7-placeholder-window-correction.json` (`95f09bf0…`, exit 1) shows the complementary
defect: with only the placeholder atom in scope, `known_pairs` is empty and the frozen clause
rejects *every* window correction (`window pair names no atom in scope`) even though the
correction is the repair the claim prescribes. This is the clause A1 removed — so the frozen
counter both rejects the honest repair (V7) and accepts a misdirected or degenerate one (V8).

**What the claim would have to say.** The correction must name the exempted atom's own round key;
`A != B`; and the window must be `base..tip` of the round the atom belongs to, with the base
derived from that round's section rather than typed by the author.

## 7. HIGH — the `axes` class has no correction grammar

`CORR = ^- corrects (seats|window|path|rev) (\S+): (.+)$` — `axes` is not in the alternation.
`CLASSES` includes `axes`, `corrects()` has a full `axes` branch, and `CORR_AXES` is defined; all
three are unreachable. Measured on the lane's own card: it carries **four** `- corrects` lines,
`corrections` reports **2** (`receipts/R0-pinned-card-as-is.json`), and the two `axes` lines are
invisible to every clause.

| variant | card | exit | receipt |
|---|---|---|---|
| V9 | coverage row `1/1` against derived `1/2`, plus `- corrects axes coverage: 1/2` | **1**, `mismatches ["coverage 1/1 …"]`, `corrections 3` (the axes line not counted) | `receipts/V9-axes-correction-ignored.json` (`f1400189…`) |

So an `axes` mismatch can only be repaired by editing the `## Owned axes` row — the exact
"append a correction" protocol the claim describes cannot touch it, and the claim's own repair
table names `axes` twice ("an `axes` correction must state `<resolved>/<total>`").

**What the claim would have to say.** `CORR` must include `axes`; the receipt must print
`corrections_by_class`; and clause 3's sentence about an `axes` correction must be deleted if the
grammar is not widened.

## 8. MEDIUM — duplicate heading, two appended rounds, no-op corrections, battery layout

| # | variant | result | receipt |
|---|---|---|---|
| M1 | V5: `## Round 45` appended a second time carrying a true pair | **0**, `sections ["round-46","round-45"]`, `atoms 8` — no uniqueness check | `receipts/V5-duplicate-heading.json` (`694b713b…`) |
| M2 | V6: `## Round 47` + `## Round 48` appended, both true | **0**, `sections ["round-47","round-48"]`, `atoms 10` — the whole audited range is unread | `receipts/V6-two-appended-rounds.json` (`6d92be9c…`) |
| M3 | V2b/V4/V5/V6 all report `exempted []` with `corrections 3` | `corrections >= 2` is met by corrections that exempt nothing (`exempt()` is never consulted because the atoms are already green) | same receipts |
| M4 | V2 vs V2b / R3 vs R4 | moving the corrections block relative to the last `## ` section flips `forgeries_green` 0↔1 with `corrections_bad: []` unchanged in V2b and `forgeries_green: 1` in V2 | `receipts/V2-empty-appended-section.json` (`720e9634…`) vs V2b |

M4 has a concrete landing consequence: `run_battery`'s `ghost_atom` forgery appends its line to
EOF, so it is a no-op — counted **green** — whenever any `## ` section follows the corrections
block. The natural append order (`## Round 47` last) therefore makes a clean card exit 1 on the
battery alone (V2), and the lander must instead insert the round section *above* the corrections
block (V2b, exit 0). Nothing in the claim states that ordering requirement.

The same mechanics make the corrections block effectively append-hostile: a second
`## Record corrections — round 47` block appended later is never read (`corrections()` splits on
the first occurrence and stops at the next `\n## `), demonstrated by
`receipts/R4-second-corrections-block.json` (`dcd16389…`): three `- corrects` lines on the card,
`corrections 2`, and the injected false line `- corrects seats round-46: 2 waves, 999 seats total`
is invisible.

## 9. MEDIUM — an exemption is granted before the correction is validated

In V7 and R1 the placeholder window atom appears under `exempted` while the same correction that
exempted it appears under `corrections_bad`. `exempt()` is consulted in the atom loop; validity
is computed afterwards for the whole correction. The receipt therefore reports `mismatches: []`
for an atom that was never re-derived, and a reader reconciling "0 mismatches" against
`corrections_bad` sees two contradictory statements about the same atom.

**What the claim would have to say.** Exemption counts only for a correction that passed
`corrects()`; an invalid correction's exemptions must fall back to `mismatches`.

## 10. LOW — C1's craft-section boundary (checked, mostly sound)

`craft_section()` truncates at the next `\n## `, so `block_is_last` is judged inside that span.
The clause does bite inside the section: inserting `- **25. a later craft block** …` before the
terminating heading yields exit **1**, `rule_blocks 25`, `block_is_last false`
(`receipts/c1-p1.json`, rev `b8af478b`). A block placed behind an embedded `## ` heading is
invisible (`receipts/c1-probes.json`, rev `a9bb5d79`, exit 0, `rule_blocks 24`) — acceptable if
"craft block" means "block of the `## Queue-drain craft ` section", which the claim's clause 1
should state rather than leave to the parser.

---

## 11. Calibration that passes (run, not inferred)

| check | command | exit | receipt |
|---|---|---|---|
| the claim's own Before-cell | `record.py --root <clone> --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5` | 1 | `receipts/base-13a9e9e-do-nothing.json` (`53d81a3d…`): `mismatches 4` = round-45 seats `(40,32)` vs `(40,36)`, the `<tip>` window `unverifiable`, coverage `133/133` vs `138/138`, depth `20/20` vs `23/23`. The claim's Before paragraph is exactly reproduced; honest. |
| C2 selftest | `record.py --selftest --root <clone> --rev 62e33f7` | 0 | `receipts/c2-selftest.log`: `cases=9 failures=0` — note `green-seats-false-superseded` is a *declared* semantic, so §3 is about scope motion, not a test that contradicts the selftest. |
| C1 selftest | `exact.py --selftest --root <clone> --freeze 5017e1f --rev 62e33f7` | 0 | `receipts/c1-selftest.log`: `cases=16 failures=0` — the selftest bypasses `frozen_path_changed`, which is why it is green while the counted command is exit 2 (§1). |
| C1 battery at `--freeze == --rev` | `exact.py --root <clone> --freeze 62e33f7 --rev 62e33f7` | 0 | `receipts/c1-freeze-eq-rev.json`: `rule_blocks 24`, `rows 4`, `refs 8`, `block_is_last true`, battery `4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`, `mutations_sha256 19a2166e…` |

## 12. Residual risk / not run

- Not run: R47-C1's clause 6/8 pins were not independently recomputed beyond the receipt's
  `battery.mutations_sha256`; the block's own `interpreter_sha256` and `mutations_sha256` values
  were not re-derived from `tools/round-47/exact.py` bytes (another seat owns C1 depth).
- Not run: `--json-out` refusals, non-ancestor revisions, `main_guard` paths (exit-2 class).
- Not verified: whether any `.ufo/waves/round-47/controls/*.json` receipt the claims cite exists
  with the numbers quoted; only `ctl-c2-0-do-nothing`'s *content* was reproduced (base rev).
- The lane moved under this seat (`HEAD` was `3186f69`, then `62e33f7`, then `f7d6e58d`); every
  number above is pinned to a sha named in the receipt, not to `HEAD`.
- The replay commits `22aff284 / d9ba6357 / 635d21ed / 5e9e9edb` live only in the scratch clone
  `$S/fix/lane`, which was removed with `$S`; the receipts and `replay.py` reproduce them from
  the pinned lane sha `62e33f7d`.
- No installs were made; no package manager was touched.

## 13. Reconciliation list for L1 (ordered)

1. Declare one freeze commit that is the last commit touching **both** frozen paths, and state it
   as a sha; §1 shows `5017e1f` and `9018c53b` both exit 2 at the landing.
2. Decide §2: either give `record.py` a `--freeze` arm or delete the "both counters" sentence.
3. Pin the audited section set and forbid a duplicate round number (§3, §4, §8-M1/M2).
4. End a round section only at `^## Round ` / `## Record corrections` and pin per-section atom
   counts (§5).
5. Bind a window correction to the exempted atom's round and refuse `A == B` (§6).
6. Either widen `CORR` to `axes` or remove the claim's two `axes`-correction promises (§7), and
   re-measure `corrections` on the current card — it is 2, not 4.
7. Place `## Round 47` **above** `## Record corrections — round 47`, and extend the existing
   corrections block in place rather than appending a second one (§8-M4).
