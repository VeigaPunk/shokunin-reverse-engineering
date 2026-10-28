# ConnSeparability — the two round-47 claims are separable in one direction only

Seat `ConnSeparability`, wave 1, round 47. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch clone:
`/fast/scratch/hyaku/kaidoku-r47/ConnSeparability/repo3` (removed after the receipts were copied
here). Nothing in the lane tree, the frozen paths or the fleet repo was modified; no install was
needed and none was made.

**Revisions.** Lane tip at clone time `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff`
(2026-10-28T18:00:14Z, `round-47: record the A6 freeze and the A7 measurement`). The record at that
tip declares the freeze `f54b3b6d` (A6) and the measured revision `a0753786` (A7)
(`SCORECARD.md:3688-3690`). All receipts below were produced 18:00:24Z–18:01:34Z against that
clone; each state is a commit in the clone and every receipt carries its command, exit, stdout
sha256 and UTC start (`receipts/matrix.jsonl`).

**The question.** The claims file asserts causal separability in one paragraph: *"R47-C1's counter
reads `SKILL.md`, this file's frozen paths, `tools/round-47/exact.py` and `tools/round-46/gate.py`;
it never reads `SCORECARD.md`. R47-C2's counter reads `SCORECARD.md` and the `.ufo/waves/round-*/`
dispatch and receipt files; it never reads the craft section. Either lands and scores without the
other."* I reverted each landing surface in a scratch clone and scored **both** counters at every
state.

## 1. The method

```sh
D=/fast/scratch/hyaku/kaidoku-r47/ConnSeparability/repo3   # full clone of the lane
git -C "$D" rev-parse --show-toplevel                      # asserted == $D before every commit
# per state: revert a surface, commit, then score both counters at that commit
python3 -I -B tools/round-47/exact.py  --root "$D" --freeze <rev|freeze> --rev <state>
python3 -I -B tools/round-47/record.py --root "$D"                          --rev <state>
```

Exit codes are the counters' own contract: 0 met, 1 not met, 2 could-not-evaluate. Every run used
`TMPDIR`/`HYAKU_SCRATCH` under the scratch root, never `/tmp`. The driver is `record_matrix.py`
and the state builder is `build.sh`, both committed beside this report.

## 2. The grid (both counters, every state, at tip `31b092d1`)

| state (scratch commit) | what changes | C1 | C2 | evidence |
|---|---|---|---|---|
| `S00_both` `31b092d17e` | nothing — the tip's own bytes | **0** | **0** | `receipts/S00_both.c1.selffreeze.json` (sha `918a12a8f991`), `receipts/S00_both.c2.json` (sha `d24410d1bc8b`) |
| `S10_c1out` `cf06c5419b` | `SKILL.md` at base: craft block 24 absent (`record.py`/`exact.py`/card untouched) | **1** | **1** | `receipts/S10_c1out.c1.selffreeze.json` (sha `5313a67e1e65`), `receipts/S10_c1out.c2.json` (sha `d7570e14ebc8`) |
| `S01_c2out_min` `dd5a82b0dd` | `## Record corrections — round 47` deleted, nothing else reverted | **0** | **1** | `receipts/S01_c2out_min.c1.selffreeze.json` (sha `f3a407fd176d`), `receipts/S01_c2out_min.c2.json` (sha `09c43cb1f38f`) |
| `S11_both_min` `3a5214de1a` | block 24 absent + corrections section deleted | **1** | **1** | `receipts/S11_both_min.c1.selffreeze.json` (sha `31486d98e47e`), `receipts/S11_both_min.c2.json` (sha `3af059e4434f`) |
| `S01_c2out_full` `c2152d9da3` | `SCORECARD.md` at base (no corrections, no round-47 section, old axis heads) | **0** | **1** | `receipts/S01_c2out_full.c1.selffreeze.json` (sha `587696df648f`), `receipts/S01_c2out_full.c2.json` (sha `9c18f90ed69c`) |
| `S11_both_full` `03e0c2c328` | `SKILL.md` and `SCORECARD.md` at base | **1** | **1** | `receipts/S11_both_full.c1.selffreeze.json` (sha `1e6177a7d8c6`), `receipts/S11_both_full.c2.json` (sha `041b1a0cc9eb`) |
| `S20_c1refout` `f469f91442` | one craft-block citation range edited to `:900-960` (block 23, **not** block 24) | **0** | **1** | `receipts/S20_c1refout.c1.selffreeze.json` (sha `a1491dca75d0`), `receipts/S20_c1refout.c2.json` (sha `99b733494f4d`) |
| `S21_block24refout` (no matrix row) | block 24's own `round-46.md:57-66` citation edited to `:900-960` | **1** | **1** | `receipts/S21_block24refout.c1.selffreeze.json`, `receipts/S21_block24refout.c2.json` |
| `S12_axes_corr` `304ec1dbb6` | block 24 absent + a truthful `- corrects axes depth: 23/23` injected into the corrections section | **1** | **1** | `receipts/S12_axes_corr.c1.selffreeze.json` (sha `49b3065d86dc`), `receipts/S12_axes_corr.c2.json` (sha `9112d46db6fb`) |
| `S30_noexact` `75589e757d` | `tools/round-47/exact.py` deleted | **1** | **1** | `receipts/S30_noexact.c1.selffreeze.json` (sha `8389df41b344`), `receipts/S30_noexact.c2.json` (sha `cf8585ebfde0`) |
| `S02_nocard` `69a096dbe1` | `SCORECARD.md` deleted | **0** | **2** | `receipts/S02_nocard.c1.selffreeze.json` (sha `8cd252eee7dd`), `receipts/S02_nocard.c2.json` (sha `234b23c027f0`) |

The 2×2 the assignment asks for, with C1 read at its declared freeze (`--freeze <rev>`) and C2 read
at the same revision:

|  | **C2 surface landed** | **C2 surface out** |
|---|---|---|
| **C1 surface landed** | `C1 0`, `C2 0` | `C1 0`, `C2 1` |
| **C1 surface out** | `C1 1`, `C2 1` ← **not separable** | `C1 1`, `C2 1` |

One of the four cells breaks the claims file: with block 24 removed and the card untouched, **C2
exits 1**. The counter is not indifferent to the other claim's landing surface.

At the tip the C1 freeze column has a second reading that matters for the record's honesty:

| C1 at rev `31b092d1`, `--freeze` = | exit | receipt |
|---|---|---|
| `f54b3b6d` (the declared freeze A6) | **0**, `refs 9`, `rows 4`, `frozen_path_changed []` | `receipts/S00_both.c1.A6freeze.json` |
| `07d2894e` (A5, the freeze the record declared one commit earlier) | **2**, `reason frozen_path_changed`, `touched ["tools/round-47/exact.py"]`, `restored ["tools/round-47/exact.py"]` | `receipts/S00_both.c1.A5freeze.json` |

Identical bytes, opposite verdicts, the only difference being which commit the label `--freeze`
names. `restored` is precisely the tamper-then-restore signature round 46's gate was built to
surface (R45-CL18), and here it is produced by an ordinary disclosed amendment.

## 3. F1 — C2's `axes` class reads `SKILL.md`, so C2 cannot score without C1's surface

`record.py:115-139` derives the `depth` axis head from the craft section of `SKILL.md`
(`record.py:117` `skill = files("SKILL.md")`), counting every `- **N. …**` block and every block
whose citations resolve; `record.py:140-142` wires it into the `axes` atom through `AXIS_ROW`
(`record.py:39`, `coverage|depth`). The `depth` row of `## Owned axes` now heads `24/24`. Remove
craft block 24 and the same function returns `23/23`:

```
$ python3 -I -B tools/round-47/record.py --root "$D" --rev cf06c5419b5d54663979d32310b18785e30c2ea8
exit 1   failing ['mismatches 1 != 0']
         mismatches [{"class": "axes", "key": "depth",
                      "claimed": [24, 24], "derived": [23, 23]}]
```

Three separate probes show the coupling is not a cardinality accident:

- **S21** breaks one line range inside block 24 (`corpus/lessons/round-46.md:57-66` →
  `:900-960`, over a 102-line file): C1 exit 1
  (`unresolved or unvalidated citations: 2`), C2 exit 1 (`depth` `23/24`).
- **S20** breaks a citation in the *previous* block, 23 — a block C1 does not grade at all: **C1
  exit 0** (`failing []`) while **C2 exit 1** (`depth 23/24`). An edit wholly outside the depth
  claim's own surface turns the calibration claim red.
- **S30** deletes `tools/round-47/exact.py`: C1 exit 1 (`interpreter absent at rev`), C2 exit 1
  (`depth 23/24`), because block 24 cites the interpreter file and the `axes` derivation resolves
  that citation too.

Consequence for the kill rule the claims file states for C1 ("A block that reuses block 23's text
relabelled `24. ` fails clauses 2–6"): the same edit that fails C1 also fails C2, so an L1 that
lands only part of C1 and re-measures both counters will see two red claims and cannot tell which
one it broke. That is the operational cost of the coupling, not just a wording problem.

Second-order effect: the coupling is to the **whole craft section**, not to block 24. Every future
round that appends a craft block (block 25 in round 48) or edits an older block's citation
arithmetic moves `depth_pair`'s numerator or denominator, so C2's green becomes a function of a
document that changes every round by design — and the row head must be edited in the same commit to
keep it green. S20 is that effect, measured today.

## 4. F2 — the repair path the record designates is unreachable

The claims file's clause 3 says *"an `axes` correction must state `<resolved>/<total>`"* and the
corrections section carries two such lines (`- corrects axes coverage: 138/138`,
`- corrects axes depth: 24/24`). They are never parsed: `CORR` (`record.py:50`) is
`^- corrects (seats|window|path|rev) …`, and the `axes` class is absent from that alternation even
though `CLASSES` (`record.py:38`) lists it. The card has four `- corrects` lines; the counter
reports `corrections 2`, `exempted 1` at the tip (`receipts/S00_both.c2.json`,
`atoms 44`, `atoms_by_class {"axes": 2, "path": 8, "rev": 31, "seats": 1, "window": 2}`).

**S12** is the direct falsifier: block 24 absent (so `depth` is genuinely `23/23`) plus a truthful
`- corrects axes depth: 23/23 — the head the C1-out state actually derives` injected inside the
corrections section. C2 still exits 1 with the same `depth 24/24 → 23/23` mismatch, and still
reports `corrections 2`. A correct repair of the exact atom C2 is complaining about has no effect.

This is the M47-1 class (`unreachable-clause`) recurring inside the other claim's instrument: the
predicate text describes an `axes` correction shape that the parser cannot produce. It is also
shown by dead code — `corrects()` has two `axes` branches, `record.py:280` (live but unreachable
through `CORR`) and `record.py:292-297`, which reads `atom["axis"]` in a function where `atom` is
undefined and would raise `NameError` if it were ever reached. `gate.main_guard` would turn that
into exit 2, i.e. a could-not-evaluate that looks like a broken instrument rather than a defect.

## 5. F3 — separability holds in the C2-out direction, strictly

`SKILL.md` untouched, the corrections section deleted (`S01_c2out_min`) or the whole card reverted
to base (`S01_c2out_full`): C1 exits **0** with the full battery in both states
(`forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`), and with
`SCORECARD.md` deleted from the tree entirely (`S02_nocard`) C1 still exits 0 (`refs 9`,
`failing []`). C1 does not read C2's surface in any of the three shapes.

So the paragraph in the claims file is half true: the C1→C2 arrow is broken, the C2→C1 arrow is
sound.

## 6. F4 — the freeze arm is one-sided, and vacuous where it is declared

- `record.py` contains **0** occurrences of `freeze_state` or `--freeze`; C2 has no freeze arm at
  all. `exact.py` has one (`exact.py:385-408`). The claims file's rule — *"a change makes both
  counters exit 2 `frozen_path_changed`"* — is therefore false for C2 by construction.
- The instrument that actually changed after its own claim's landing is the one with no arm:
  `tools/round-47/record.py` moved at `2e4ae434` (A3) and `07d2894e` (A5), both **after**
  `e856beb5` landed the corrections section C2 scores. `tools/round-47/exact.py` moved at
  `f54b3b6d` (A6). Each move was made green by re-declaring the freeze at the new commit (A1…A6);
  with `--freeze` set to the previous declaration the same bytes exit 2 with `restored`
  non-empty (§2). The arm has therefore never had discriminating power against a post-landing
  instrument edit — it can only be satisfied, never failed, by a round that keeps amending.
- The claim's own artefact is not in the frozen set: `## Frozen paths (exact)` lists
  `plans/round-47-claims.md` and `tools/round-47/`, not `SKILL.md`. Block 24 was rewritten after the
  freeze that was declared at the time (`04469ee8` re-pointed its citations and `a0753786` moved its
  `interpreter_sha256`), and no arm covers that. The pin forces the editor to update the pin in the
  same commit — it detects staleness, not tampering.

This is adjacent to routed defect R47-CL5 ("a counter amendable after the landing cannot be told
apart from one tuned to it"); what is new is the asymmetry — the frozen-set rule is enforced on C1
only, and the file that drifted after its landing (`record.py`) is the unarmed one.

## 7. F5 — the round's after-cell misquotes the receipt it cites, and C2 cannot catch it

`SCORECARD.md:3701` (R47-C2 after-cell) reads *"exit 0, `atoms 50`, `mismatches []`, `corrections 2`
both re-derived, `exempted 2 <= 3` … (`.ufo/waves/round-47/l1/scores/c2-at-A7.json`)"* and its
`measured at` cell says `1e2c310295`; `SCORECARD.md:25` (calibration row) says *"re-derives 50
atoms"* citing the same receipt.

Reproducing the cited receipt byte-for-byte:

```
$ git -C "$D" show f54b3b6d:tools/round-47/record.py > /dev/null   # A6 instrument
$ python3 -I -B tools/round-47/record.py --root "$D" --rev a07537869cf37963dff559fc75271dfa8fbb2542
exit 0 ; stdout identical to .ufo/waves/round-47/l1/scores/c2-at-A7.json (byte compare: True)
receipt: rev a0753786, atoms 42, corrections 2, exempted 1, mismatches []
```

So the receipt says **42 atoms, 1 exempted, measured at `a0753786`**; the prose says 50 atoms,
2 exempted, measured at `1e2c310295`. `50` and `2` are the A4-era numbers: the `## Round 47`
section did not exist at A4, so the window there was rounds 45–46 and the base-revert state in this
grid still measures 50 (`receipts/S01_c2out_full.c2.json`). At the tip the count is **44**. The
number moves with every edit to the card's last two round sections (42 → 44 between A7 and
`31b092d1`), so a row that quotes it must quote the receipt of the *final* revision.

This is the R46-V class exactly — the lane's record false about its own measurement — and no
counter owned by this round can see it, because `record.py` re-derives atoms from the round
sections and never its own after-cell. The C1 row is consistent in the same spot (`refs 9`,
`rows 4` match `c1-at-A7.json`; I reproduced C1 at `a0753786` with `--freeze f54b3b6d` → exit 0).

## 8. Proposed move (one, bounded)

**Make the record state the dependency it actually has, and make the after-cell quote the receipt it
cites.** Landing edits, all outside the frozen bytes:

1. `SCORECARD.md` `## Round 47`: replace the (unmeasured) separability assertion with the measured
   one — *"C2 is not separable from C1 in the C1-out direction: `record.py:115` derives `depth`
   from `SKILL.md`'s craft section, so block 24's absence scores `depth 23/23` against the row's
   `24/24` and C2 exits 1; C1 is separable: with the card deleted C1 exits 0. Grid and receipts:
   the ConnSeparability seat report for this wave."*
2. Route a new defect (next free id, `R47-CL9`): the `axes` class couples C2 to every craft block in
   `SKILL.md`; `CORR`'s alternation excludes `axes`, so the correction form clause 3 names can never
   parse (an unreachable-clause repeat of M47-1 inside C2); `record.py:292-297` is a dead duplicate
   that would `NameError` on `atom` if reached. Suggested round-48 shape: bind the `axes` head to a
   named command-A receipt at a recorded revision (the pattern the calibration row already uses for
   command B) instead of re-deriving it live from the other claim's artefact.
3. Fix the two after-cell numbers to the cited receipt and to the revision that will actually be
   measured: `atoms <n>` / `exempted <m>` from the *final* revision's receipt, and the `measured at`
   cell to the rev that receipt names (`a0753786`, not `1e2c310295`). Then re-run both counters once
   at the final revision and quote those numbers (see §9.2) — the atom count is not stable across
   edits to the same section.

**Axes.** calibration: improves (the record stops asserting an unmeasured property and stops
misquoting three numbers of its own receipt — the observable is record↔repo agreement, which is what
the axis row claims to measure). depth: unchanged (no `SKILL.md` edit, no new craft block, block 24
and `exact.py` untouched, so `interpreter_sha256` need not move). coverage: unchanged (no corpus
file, no coverage-map row). No frozen byte is edited, so no claim's predicate changes.

**Risks, measured.**

- Any new sentence in `## Round 47` becomes atoms. A literal `.ufo/waves/…` token creates a `path`
  atom resolved with `git show <rev>:<path>`, so the seat directory must be **committed before** the
  measured revision or the sentence must name the report without the `.ufo/waves/` prefix. A
  backticked 7–40 hex creates a `rev` atom that must resolve *and* be an ancestor of the measured
  rev — my fixture commits (`cf06c541`, `f469f914`, …) live in a scratch clone and must **never** be
  cited that way.
- Re-declaring the freeze a seventh time (if `record.py` is edited to change the `CORR`
  alternation now) would repeat the A6 pattern: a red-before receipt at the pre-edit revision is
  mandatory, and the claims file's own sentence "Nothing in this file or in `tools/round-47/`
  changes after the freeze" would be false for the seventh time. The cheaper honest option is to
  state the defect and leave `record.py` alone this round (option 1–3 above do not need it).
- Changing `record.py` would not change `exact.py`, so block 24's `interpreter_sha256` stays valid;
  changing `exact.py` (it does not need to change) would require moving that pin in the same commit.

## 9. Verification the integration owner should run

1. `python3 -I -B tools/round-47/exact.py --root . --freeze <final-freeze> --rev <final-rev>` →
   expect exit 0, `refs 9`, `rows 4`, `frozen_path_changed []`.
2. `python3 -I -B tools/round-47/record.py --root . --rev <final-rev>` → expect exit 0 **and**
   compare `atoms`, `corrections`, `exempted` with the numbers written in the row. This comparison
   is the check that catches F5; the counter does not perform it.
3. `python3 -I -B tools/round-47/exact.py --root . --freeze <the previous freeze> --rev <final-rev>`
   → expect exit 2 `frozen_path_changed` with `restored` naming the file that moved. That is the
   drift the freeze series hides; report it, do not fix it by relabelling.
4. Separability control, one command pair in any clone: `git checkout <base> -- SKILL.md`, then
   `record.py --rev <clone-HEAD>` → expect exit 1 with `depth 23/23`. After the §8 landing, the
   record will predict exactly this value; before it, the record predicts exit 0.

## 10. Not run (claimed nowhere)

- The `--profile v2` path beyond the battery the counters run themselves; no merge/octopus or
  worktree-dirty scenario (that is routed R47-CL1, untouched here).
- `record.py --selftest` (the claims file itself records it as non-runnable, R46-CL8).
- No alternate git version, no `git worktree` fixture, no concurrency on the same fixture repo.
- The lane tip moved twice during this seat's work (`07d2894e` → `31b092d1`); every number above is
  pinned to `31b092d1` and every receipt names its own revision, but a later tip will re-derive
  different atom counts for C2 by construction (§7).

## Sources

- `plans/round-47-claims.md@62e33f7d` — the claims, the predicates, the separability paragraph, the
  frozen path list.
- `tools/round-47/exact.py@31b092d1` — `evaluate()` / `gate.freeze_state` wiring (`:385-408`).
- `tools/round-47/record.py@31b092d1` — `depth_pair` `:115-139`, `axis_pairs` `:140-142`,
  `AXIS_ROW` `:39`, `CORR` `:50`, `corrects()` `:258-300`.
- `tools/round-46/gate.py@31b092d1` — `freeze_state` `:144-196` (`restored`, `frozen_path_changed`).
- `SCORECARD.md@31b092d1` — `:25` (calibration row), `:3682-3696` (freeze series A1–A6),
  `:3700-3701` (the two claim rows), `:19-32` (`## Owned axes`), `:3663-3678` (corrections).
- `.ufo/waves/round-47/l1/scores/{c1,c2}-at-A7.json` — the receipts F5 compares against.
