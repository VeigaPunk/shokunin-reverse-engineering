# RevC1Ids — round-47 wave 1 review: C1 clause 4 (routed-id cardinality) and the freeze arithmetic

Seat `RevC1Ids` (reviewer, leaf). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `13a9e9e1`, first freeze `5017e1f7299c3a812e87e7950148f54313dd279e`, declared freeze per the
claims file's own derivation `62e33f7dd75c8e3285967b26419842c106f6c965`, **tips measured
`1e2c3102952dc636650095643c1963c833859019` (findings F1-F10, clause-4 fixture run) and
`f7d6e58d6e7f4e664bf443137c55ee08821de244` (F11 and the review-close table)** — thirteen commits
landed while this seat ran (`git log 3186f69b..f7d6e58d`: `9018c53b` A1, `e856beb5` landing,
`62e33f7d` A2, `2e4ae434` A3, `1e2c3102` A4, `caafeffa` record, `07d2894e` A5, `a631bba0` A5
receipts, `04469ee8` knowledge citation, `f54b3b6d` A6, `a0753786` pin follows A6, `31b092d1` A6
freeze/A7 measurement, `f7d6e58d` routed findings).

Scratch `S=/fast/scratch/hyaku/kaidoku-r47/RevC1Ids` (`TMPDIR`/`HYAKU_SCRATCH`), removed after the
receipts below were copied to `.ufo/waves/round-47/w1/RevC1Ids/`. No installs, no pacman, no writes
outside this seat's report directory and `S`; lane tree read-only throughout (every command below is
a counter invocation or read-only git; nothing was staged, committed or checked out).

---

## 0. Answer to the assignment first: clause 4 does NOT green any of the five forgery shapes

Thirteen fixtures, each a fresh one-commit repo (`git init` in `S`, toplevel asserted, real `SKILL.md`
bytes from `1e2c3102` with only the four table rows rewritten), scored by the frozen counter. Command
shape (per fixture):

```sh
python3 -I -B tools/round-47/exact.py --root <fixture> --freeze <fixtureHEAD> --rev <fixtureHEAD> \
  --no-battery [--profile v2]
```

| fixture | construction | v3 exit | v2 exit |
|---|---|---|---|
| `c4-0-genuine` | landed table, untouched (control) | 0 | 0 |
| `c4-1-two-ids` | row 1 trigger names `R46-CL2` **and** `R46-CL3` | **1** | 0 |
| `c4-2-two-ids-plus-empty` | row 1 names two ids, row 2 names none — the four-id multiset is *exact* | **1** | 0 |
| `c4-3-no-id` | row 2 trigger names no id | **1** | 1 |
| `c4-4-id-outside-frozen-set` | `R46-CL7` in place of `R46-CL2` | **1** | 1 |
| `c4-5-extra-id-beside-real` | `R46-CL7 R46-CL2` in one cell | **1** | 0 |
| `c4-6-same-id-two-rows` | `R46-CL2` in rows 1 and 2, `R46-CL3` nowhere | **1** | 1 |
| `c4-7-id-in-v2-hole-cell` | id moved to the `v2 hole` cell, trigger names none | **1** | 1 |
| `c4-8-id-with-suffix` | trigger `R46-CL2x` | **0 — HOLE (F4)** | 0 |
| `c4-9-id-in-a-negation` | trigger "no `R46-CL2` defect is addressed by this row" | 0 (naming, not addressing) | 0 |
| `c4-10-arm-permutation` | arm cells permuted across the four rows | **0 — HOLE (F5)** | 0 |
| `c4-11-id-twice-one-cell` | `R46-CL2 R46-CL2` in one cell | 1 | 0 |
| `c4-12-ids-also-in-hole-cells` | ids repeated in non-trigger cells (control) | 0 | 0 |

Receipts: `.ufo/waves/round-47/w1/RevC1Ids/receipts/c4-results.json`
(sha256 `d2e9508b5382883cff1016ee14233ba4003b13bcb6b0c7b24e0cd63ee9f38e17`), driver
`…/receipts/attack4.py` (`73326971…`), which regenerates every fixture from `1e2c3102:SKILL.md` plus the
row spec inside the driver; the fixture directories themselves lived under `S` and are reaped.

The failure text is the clause you would want: `rows naming != 1 routed id: [i]` (exactly-one),
`routed cardinality {...} != each of [...] exactly once` (multiset), and the exit-cell clause.

**Clause 4 as written is implemented correctly for the five named shapes.** The two shapes it does not
catch are F4 (id-token prefix) and F5 (arm/id pairing unbound) below.

---

## Findings

### F1 — BLOCKER: under the claims file's own freeze derivation the counter exits 2 at the tip; the receipts that report `met_target true` use `--freeze` = the measured revision, which makes the freeze arm vacuous

Evidence, all at `--rev 1e2c3102952dc636650095643c1963c833859019`:

```sh
git log --format=%H -1 -- plans/round-47-claims.md      # -> 62e33f7dd75c8e3285967b26419842c106f6c965
python3 -I -B tools/round-47/exact.py --root . --freeze 62e33f7dd75c8e3285967b26419842c106f6c965 \
  --rev 1e2c3102952dc636650095643c1963c833859019 --no-battery
```

| freeze used | exit | receipt |
|---|---|---|
| `62e33f7d` (derivation line) | **2** `frozen_path_changed` | `…/RevC1Ids/c1-battery.json` sha `98a15294…` |
| `9018c53b` (A1 paragraph: "the declared freeze is the commit that carries this paragraph") | **2** `frozen_path_changed` | stdout sha `dbce9388…` |
| `5017e1f7` (first freeze) | **2** `frozen_path_changed` | stdout sha `706cf11c…` |
| `1e2c3102` (= the measured rev) | **0**, `failing []`, `touched 0` | `…/RevC1Ids/c1-battery-tip.json` sha `98ef390e…` |

`touched ['plans/round-47-claims.md', 'tools/round-47/record.py']` for the `5017e1f7..tip` window. The
committed L1 receipts at `.ufo/waves/round-47/l1/scores/` record `freeze == rev` in every one
(`c1-at-L1` freeze `9018c53b` rev `e856beb5`; `c1-at-A2` freeze = rev = `62e33f7d`; `c1-at-A4`
freeze = rev = `1e2c3102`). With `freeze == rev` the freeze arms (`history_touched`, `blob_changed`)
are empty *by construction*: that run cannot distinguish a clean post-freeze edit from no edit, so the
receipt's `frozen_path_changed []` and `touched 0` are not evidence of freeze integrity.

Also confirmed: `…/l1/scores/c1-at-A4.json` reports `met_target true` at a freeze value the claims
file's own derivation command does not produce.

**What the claim would have to say.** The counting command needs a FREEZE distinct from `<REV>` and
still clean at `<REV>`; the current text cannot have both at any tip after A2. One of:
(a) revert `tools/round-47/record.py` to its `62e33f7d` bytes — true as of `1e2c3102`, superseded
by A6 which also rewrote `exact.py` (F11);
(b) declare a third freeze at the amendment commit and state explicitly that `Nothing ... changes
after the freeze` now binds only from that commit, plus the red-before receipt for the
`62e33f7d..A5` window;
(c) keep exit 2 and report both claims as could-not-evaluate — which cannot count toward the axis.

### F2 — HIGH: the claims file's freeze sentence is false for R47-C2 — `record.py` has no freeze arm at all

Claims file, line 10-11: "Nothing in this file or in `tools/round-47/` changes after the freeze: a
change makes **both** counters exit 2 `frozen_path_changed`."

```sh
grep -c freeze tools/round-47/record.py                       # 0  (no --freeze argument, no gate.freeze_state)
python3 -I -B tools/round-47/record.py --root . --rev 1e2c3102952dc636650095643c1963c833859019
# exit 0, mismatches [], met_target true  -> .ufo/waves/round-47/w1/RevC1Ids/c2-at-tip.json
```

`tools/round-47/record.py` was rewritten after the declared freeze (`2e4ae434` A3, `1e2c3102` A4,
`07d2894e` A5; `git diff --stat 62e33f7d..1e2c3102 -- tools/round-47/record.py` → `1 file changed, 14
insertions(+), 3 deletions(-)`, and the tip's bytes hash `abf35257…` against `fb6d5735…` at the
freeze) and C2 still reports met. The counter that was edited is the counter
that cannot see the edit. This is the R46-CL4 class (an unpinned denominator) at claim level: the
instrument registry row even records it — `tools/round-47/record.py` … self pin: "none — the counter's
own bytes are not pinned by the block".

**What the claim would have to say.** Either an `interpreter_sha256`-style self pin for `record.py`
(the shape CI's block already uses for `exact.py`), or drop the "both counters" sentence to "a change
makes `exact.py` exit 2" and measure C2 only at a revision whose `record.py` bytes are the executed
bytes. Note the same hazard gate.py names for itself ("the counters grade committed bytes, but they
EXECUTE from the worktree"): `python3 tools/round-47/record.py --rev 62e33f7d` today executes the
*tip's* `record.py` (A3's relaxation) against `62e33f7d`'s `SCORECARD.md`, and nothing in the receipt
names the executed bytes.

### F3 — HIGH: A3 makes the counter implement a weaker predicate than the frozen clause 3 states, with no claims-file paragraph declaring it

`plans/round-47-claims.md:169` (unchanged since the freeze): "A correction that exempts an atom the
card does not contain is itself a defect."

`tools/round-47/record.py` at the tip:

```python
historical = (entry["class"] in ("seats", "window") and key.isdigit()
              and int(key) < oldest)
if not historical:
    corrections_bad.append({"line": entry["text"],
                            "detail": "exempts an atom that does not exist"})
```

and A4's own new selftest asserts exit 0 for a correction that exempts a round-3 atom
(`run("green-historical-correction", 0, ... "- corrects seats round-3: 1 waves, 2 seats total")`).
`git log --format=%h 62e33f7d..1e2c3102 -- plans/round-47-claims.md` is **empty** (stdout sha of the
empty output `e3b0c442…`), so neither A3 nor A4 has a claims-file paragraph, while A1/A2 do — and
the file is untouched at `f7d6e58d` as well (F11).

So the rule text and the running predicate disagree, and the claims file is the rule. The relaxation is
bounded (clause 4 caps `exempted <= 3`, and the historical correction must still re-derive against
`.ufo/waves/round-3/*-dispatch.json`), which is why this is HIGH and not a blocker.

**What the claim would have to say.** Clause 3 would have to be amended to: "A correction that exempts
an atom the card does not contain is a defect, except a `seats`/`window` correction whose key is a
round older than both sections, which must still re-derive" — and that amendment needs its own
disclosed freeze entry, as A1/A2 have.

### F4 — MEDIUM: clause 4 accepts a trigger cell that names no routed id when the id token is a prefix of a longer token

`ID = re.compile(r"R46-CL\d+")` with `findall` on the trigger cell; no anchoring. Fixture
`fx-c4-8-id-with-suffix-*` (built by `…/receipts/attack4.py`), trigger cell
`R46-CL2x the substring arm test`:

```sh
python3 -I -B tools/round-47/exact.py --root <fixture> --freeze <fixtureHEAD> --rev <fixtureHEAD> --no-battery
# exit 0, routed_counts {"R46-CL2": 1, "R46-CL3": 1, "R46-CL4": 1, "R46-CL6": 1}
```

`R46-CL2x` (also `R46-CL6b`, `XR46-CL2`) is not a routed id, yet the counter books it as one. This is
row 1's defect class — "containment over a lowercased cell, so any superstring passes" — reproduced one
level down, inside the clause that closes it. No battery forgery covers it, so `v3_green` stays 0.

**What the claim would have to say.** Clause 4: "the trigger cell contains exactly one token that
full-matches `R46-CL[0-9]+` and that id is in the frozen set" — i.e. `(?<![A-Za-z0-9])R46-CL[0-9]+(?![A-Za-z0-9])`
or a `fullmatch` per whitespace/backtick-split token — plus a fifth forgery `id-token-suffix`.

### F5 — MEDIUM: clause 5 checks the arm column as a vocabulary set and never binds an arm to its row's id

Fixture `fx-c4-10-arm-permutation-*`: the four rows keep their ids and the arm cells are rotated
(`R46-CL2`→`order`, `R46-CL3`→`digest`, `R46-CL4`→`once`, `R46-CL6`→`symbol`). Exit **0**.

The matrix's actual content is the *pairing* ("this routed defect is closed by this arm"); clause 4
binds the multiset of ids and clause 5 binds the multiset of arms, but nothing binds row to row. A
permuted block satisfies clauses 4 and 5 and every kill rule, so the counter cannot tell the landed
matrix from one whose rows contradict the lesson text. The landed block does pair correctly
(`R46-CL2↔symbol`, `R46-CL3↔once`, `R46-CL4↔digest`, `R46-CL6↔order`), so this is instrument weakness,
not a false landed claim.

**What the claim would have to say.** Clause 5 would need the expected map, e.g. "row naming `R46-CL2`
carries `symbol`, `R46-CL3` `once`, `R46-CL4` `digest`, `R46-CL6` `order`", and a forgery
`arm-swap` that exchanges two rows' arm cells.

### F6 — LOW-MEDIUM: the claim's `blobberish` kill rule is false as written

Claims file: "A block with `blobberish` in a v3-arm cell fails clause 5 while the v2 profile passes it."

Measured (fixture `fx-k1-blobberish-*`, driver `…/receipts/attack4b.py`): **v3 exit 1 and v2 exit 1** —
`blobberish` contains none of `symbol`, `once`, `digest`, `order`, so v2 fails it too. The v2-green
superstring is `order-ish` (fixture `k1b-order-ish`: v2 **0**, v3 **1**), which is what
`_m_substring_arm` actually uses. The kill rule transplants round-46's vocabulary (`blob`) into round
47's.

**What the claim would have to say.** "A block whose arm cell is `order-ish` (or `symbolish`,
`digestive`, `once-over`) fails clause 5 while the v2 profile passes it."

Receipts: `…/receipts/kill-results.json` sha `ba5a1725…`. Other kill rules hold:
`k3-digest-of-three` v3 1/v2 0 (`mutations_sha256 does not match the counter's own mutation list`),
`k4-flag-reversed` v3 1/v2 0 (`gate.py flag order: 0 correct, 1 reversed`), `k5-block23-relabelled` v3 1
(fails at the header: `['trigger','v1 hole','v2 arm','exit']`), `k6-arm-case` `Symbol` → 1,
`k7-arm-punct` `` `symbol`. `` → 1.

### F7 — LOW: a `--json-out` I/O failure exits 1 (a verdict), not 2 (could-not-evaluate)

`gate.emit()` is called outside `gate.main_guard`, so an unwritable target crashes after the verdict is
computed:

```sh
python3 -I -B tools/round-47/exact.py --root . --freeze 1e2c3102 --rev 1e2c3102 \
  --json-out .ufo/waves/round-47/w1/RevC1Ids/no-such-dir/out.json
# exit 1, traceback FileNotFoundError; stdout+stderr sha 98da296e…  (2026-10-28T17:58:11Z)
```

gate.py's own contract: "An unhandled exception is a defect, never a verdict: every entry point catches
it and returns 2" (R45-CL13 (f)). A run that would have been `met_target true` is reported as exit 1.
`out_path()` refuses targets outside the lane root and inside graded heads, but not a missing parent
directory inside the lane root. The honest fix would be a `os.makedirs`/try in `emit` returning 2 —
frozen bytes, so this is L1's call.

### F8 — LOW: `exact.py --selftest` bare exits 2

```sh
python3 -I -B tools/round-47/exact.py --selftest
# exit 2: "the following arguments are required: --root, --freeze, --rev"
```

The documented form in the instrument-registry row
(`--selftest --root . --freeze <F> --rev <R>`) exits 0 with 16 cases, and `record.py --selftest --root .
--rev 0` exits 0 — so the selftests themselves pass; only the natural invocation is rejected because
`add_argument(..., required=True)` is evaluated before the `args.selftest` branch.

### F9 — LOW: the C1 `Before` text names a receipt value the control does not contain

Claims file: "at the freeze the battery cannot even be built (`marker blocks 0`)". `run_battery` is only
reached when the artefact is structurally green (`if with_battery and code == 0`), so at the first freeze
the emitted receipt carries `battery: {"skipped": "artefact fails a structural clause first"}` — the
committed control says exactly that. `marker blocks 0` is only reachable by calling `run_battery`
directly. Minor: the control is honest, the prose overstates what the receipt shows.

The rest of that control reproduces **byte-identically**: my run
(`--freeze 5017e1f7 --rev 5017e1f7 --no-battery`, exit 1) is dict-equal to
`.ufo/waves/round-47/controls/ctl-c1-0-do-nothing.json` — `block_present 0`, `rule_blocks 23`,
`marker_occurrences 0`, `failing ['marker_occurrences 0 != 1', 'marker_block_count 0 != 1']`.
Receipt `…/receipts/do-nothing.json` sha `5f42beab…`.

### F10 — LOW (documentation, possibly another seat's scope): clause 2's `classes` field does not exist in the C2 receipt

Claims clause 2: "`classes` covers all five". `record.py` emits `atoms_by_class` and fails with
`no atoms of class(es) [...]` (`record.py:376-379`); there is no `classes` key in the receipt (my run of
`c2-at-tip.json` has not got one). The predicate is implemented; the receipt name the claim uses is not.
Recorded for reconciliation with the C2 seats, not re-derived further here.

### F11 — HIGH: the `interpreter_sha256` pin was rewritten after the freeze to follow a changed counter, so it no longer binds the block to the frozen instrument

The pin's whole purpose is to catch a post-freeze change to `exact.py`. It cannot: the pin lives in
`SKILL.md`, which is not frozen, so it moves with the counter. Measured at the tip
`f7d6e58d6e7f4e664bf443137c55ee08821de244`:

```sh
sha256sum tools/round-47/exact.py     # 01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5
git show 5017e1f:tools/round-47/exact.py | sha256sum   # dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c
git show f54b3b6d -- tools/round-47/exact.py          # A6 rewrites _fixture_files
git show a0753786 --stat                              # "block 24's interpreter pin follows A6", SKILL.md 1 line
```

Between `62e33f7d` (the claims file's declared freeze) and the tip, **four commits changed the frozen
directory and none has a claims-file paragraph**:

```
f54b3b6d round-47: A6 - the battery fixture carries every citation the landed block names
07d2894e round-47: A5 - the ghost-atom forgery lands inside the corrections section
1e2c3102 round-47: A4 - the historical-correction selftest fixture gets its round-3 dispatch
2e4ae434 round-47: A3 - a seats/window correction for a round older than the window stays valid evidence
```

and `git log -1 -- plans/round-47-claims.md` is still `62e33f7d` — the disclosed series stops at A2. The
A2 paragraph's own warranty ("Every clause, threshold and kill rule is byte-identical to A1") is false
of the executed instrument after A5 (the `ghost_atom` forgery now inserts into the corrections section)
and A6 (the battery's fixture file set is derived from the block's own citations).

Consequence at the tip: `exact.py --freeze 62e33f7d --rev f7d6e58d` → exit 2, `touched
['tools/round-47/exact.py', 'tools/round-47/record.py']`
(`…/receipts/c1-at-declared-freeze-tip.json`), while `--freeze f7d6e58d --rev f7d6e58d` → exit 0
(`…/receipts/c1-at-tip-selfref.json`) and `record.py --rev f7d6e58d` → exit 0
(`…/receipts/tip-c2.json`).

**What the claim would have to say.** Either the pin is dropped in favour of a freeze-anchored
statement ("the block's rows are scored by `exact.py@5017e1f`"), or every amendment needs its own
claims-file paragraph and a *new* red-before receipt naming the previous freeze. A pin written by the
author of the change it is supposed to detect is not a pin.

---

## State at review close (tip `f7d6e58d`)

| fact | value |
|---|---|
| claims-file last touch (`git log -1 -- plans/round-47-claims.md`) | `62e33f7d` (A2) |
| frozen-path commits after that freeze | 4 (`2e4ae434`, `1e2c3102`, `07d2894e`, `f54b3b6d`) |
| `exact.py` sha at `5017e1f` / at tip | `dcef54f1…` / `01a4bca7…` |
| `record.py` sha at `62e33f7d` / at tip | `fb6d5735…` / `abf35257…` |
| C1 at the declared freeze | exit **2** `frozen_path_changed` |
| C1 at `freeze == rev == tip` | exit **0**, `failing []` (battery 4/4/0/1/0) |
| C2 at tip (`--rev f7d6e58d`) | exit **0**, `mismatches []`, `corrections 2`, `corrections_bad []` |

Clause-4 holes re-confirmed against the **tip** instruments (`exact.py` `01a4bca7`, tip `SKILL.md`,
the knowledge entry present):

| fixture | v3 exit | v2 exit |
|---|---|---|
| `t0-genuine` | 0 | 0 |
| `t8-id-with-suffix` (`R46-CL2x` in row 1) | **0 — F4 stands** | 0 |
| `t8b-substring-id-mid-table` (`R46-CL2x` in row 3) | **0 — F4 stands** | 0 |
| `t10-arm-permutation` (arm cells rotated one row) | **0 — F5 stands** | 0 |

Receipts `…/receipts/tip-results.json` (sha `50d90ea9…`), driver `…/receipts/tipcheck.py`
(`dbd3146f…`). The holes are unchanged by A6; re-reporting them against a seventh instrument
revision would be pure re-derivation.

---

## Verified green (what I did *not* find wrong)

- **V1** Landed block 24, structural profile: `rule_blocks 24`, `marker_occurrences 1`,
  `block_is_last true`, `header ["trigger","v2 hole","v3 arm","exit"]`, `rows 4`,
  `routed_counts {CL2:1, CL3:1, CL4:1, CL6:1}`, `arm_tokens ['symbol','once','digest','order']`,
  `mutations_sha256` = `19a2166e…` = expected, `interpreter_sha256` = `dcef54f1…` = expected,
  `gate_order_literal 1` / `gate_order_reversed 0`, `refs 8`, `unresolved_citations []`,
  evidence: `…/RevC1Ids/c1-battery-tip.json`.
- **V2** Battery at `freeze == rev == 1e2c3102`: `forgeries_total 4`, `v2_green 4`, `v3_green 0`,
  `genuine_green 1`, `crash 0`; per forgery `(v2, v3)`: substring-arm `(0,1)`, duplicate-routed-id
  `(0,1)`, stale-mutations-digest `(0,1)`, flag-order-drift `(0,1)`. The four holes are measured, not
  asserted — pending F1, which is about *which* freeze this may be claimed at.
- **V3** The pinned digests are over the counter's own list: `MUT_DIGEST` recomputed by importing
  `exact.py` matches the block's pin, and at `1e2c3102` `sha256(5017e1f:tools/round-47/exact.py)` =
  `sha256(1e2c3102:tools/round-47/exact.py)` = `dcef54f1…` (exact.py had not changed after the freeze
  at that point; A6 later did, and rewrote the pin — F11).
- **V4** Do-nothing control reproduces exactly (F9 above).
- **V5** Both selftests green in their documented form: C1 `--selftest --root . --freeze 0 --rev 0`
  → exit 0, `EXACT_SELFTEST: cases=16 failures=0` (`…/receipts/ex-selftest-doc.json`); C2
  `--selftest --root . --rev 0` → exit 0, `cases` 10, `failures` 0 at the tip. The registry row's
  "9 cases" is the `5017e1f7` count (A4 added `green-historical-correction`), so that row is not drift
  — but it does mean the counter's own case count changed after the freeze, which is F2/F3 again.

## Receipts index

`.ufo/waves/round-47/w1/RevC1Ids/`

| file | sha256 |
|---|---|
| `c1-battery.json` (freeze `62e33f7d`, rev tip: exit 2) | `98a15294e14bb03410a39fde64c0af80c1bc08e68a3bc19904f718d5e6e1dd01` |
| `c1-battery-tip.json` (freeze = rev = tip: exit 0) | `98ef390e1c1a3eaa1e0d2b9f3a9c635a4870c257b2cdebad4c4a87497616ea6d` |
| `c2-at-tip.json` / `c2-head.json` (exit 0) | `c609b3e1c8ac00d03f8b80c9313d96b25466e53116b40121422f43e94224209d` |
| `receipts/c4-results.json` | `d2e9508b5382883cff1016ee14233ba4003b13bcb6b0c7b24e0cd63ee9f38e17` |
| `receipts/kill-results.json` | `ba5a1725c191dd04f711fefb8d908ee293856cbab56ed44daaa31f3cbf86a35a` |
| `receipts/receipts.json` (cmd/exit/stdout-sha/UTC per pinned run) | `bf6cb6e169f8d0d95a1e0ad28a4c1de658dbb1c6d067da250e71534de272930a` |
| `receipts/attack4.py` / `attack4b.py` / `receipts.py` | `73326971…` / `48a5c709…` / `be3048aa…` |
| `receipts/do-nothing.json` | `5f42beab…` |
| `receipts/emit-crash.txt` (F7 traceback) | `98da296e…` |
| `receipts/ex-selftest-doc.json` (F8/V5, C1 selftest 16/0) | `0249b80f58085f0d52cca3f7ae3f731d88d38dd4daaca6f84cefa023e3028aaa` |
| `receipts/c1-at-declared-freeze-tip.json` (F11: exit 2 at `f7d6e58d`) | `fcc106d3b7d1bb4f42ea05c41bf58c4b419062e506abfd4220b633da4bb8af44` |
| `receipts/c1-at-tip-selfref.json` (F11: exit 0 at `freeze == rev == f7d6e58d`) | `d714a444c6aa8b1c498c48097ff293516e8482241e9dfc110bd9232cb94649df` |
| `receipts/tip-c2.json` (C2 exit 0 at `f7d6e58d`) | `ba75e586ae523621bfeabf8d2a8cdd022bf6ef56fb404c9ecb3faab1ec84000b` |
| `receipts/tip-results.json` (F4/F5 re-confirmed at the tip) | `50d90ea9f14691d9318c8892c24392bcffee4174b0ee3fc08fa98ad7ca54ec81` |
| `receipts/tipcheck.py` | `dbd3146fc614f27171cb71e9cc20ce62b8c6eaebb506b8b0b7aad6faf77eb17e` |
| `receipts/c4-13.json` (incidental: a fixture missing a cited path reds clause 8 — the defect A6 fixed) | `e8a7bf01964e394d5bf40d6a96ecb018ca73b7953607302661d5d7f1c22ef1d1` |

## Residual risk and verification gaps

1. **The lane moved thirteen times under this seat**, and two of the moves were amendments to frozen
   instruments (`f54b3b6d` A6 rewrote `exact.py`; `07d2894e` A5 rewrote `record.py`). F1-F10 are
   pinned to `1e2c3102`, F11 and the close table to `f7d6e58d`; anything later re-opens F1/F2/F3/F11
   and re-derives V1/V2/V3 against a different `exact.py`. Re-derive
   `git log -1 -- plans/round-47-claims.md` and `sha256sum tools/round-47/exact.py` before scoring.
2. **F2's C2 half is a code-vs-claim divergence, not a fixture.** I did not build the A3 discriminator
   (a `.ufo/waves/round-3` dispatch set plus a `- corrects seats round-3: …` line scoring 0 at the tip
   and 1 at `62e33f7d`); A4's own selftest case name (`green-historical-correction`) is the direct
   evidence, and the C2 seats own the record-side fixtures. Not run: a full C2 forgery battery against
   the frozen `62e33f7d` bytes with the tip's `SCORECARD.md`.
3. **Not run**: `exact.py` at the derived freeze for each intermediate `--rev` between `62e33f7d` and
   the tip. The window is `record.py` for `62e33f7d..1e2c3102` and both instruments after A6, so C1's
   verdict there is necessarily exit 2; I sampled the endpoints only (`c1-at-declared-freeze-tip.json`,
   `c1-battery.json`).
4. **F4/F5 are holes in a counter that is frozen**, so the honest options are: report them as residual
   (the landed block does not exercise them), or amend with a fifth/sixth forgery in a disclosed
   amendment — which by F2's logic makes the claim's own freeze story weaker, not stronger.
5. Scratch `S` was removed after the receipts above were copied. `.ufo/waves/round-47/w1/RevC1Ids/` and
   this file are the only writes this seat made in the lane. One accidentally created directory in the
   fleet root (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-47/w1/RevC1Ids`, empty) was removed
   immediately; nothing was written to `/tmp`.
