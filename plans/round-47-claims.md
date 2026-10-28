# Round 47 claims — freeze

Lane `kaidoku`, round 47, attempt 1. Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`
(`jj-lane.sh state` at claim time: `branch=main local=13a9e9e1 remote=13a9e9e1`).

**Freeze** = the commit that first contains this file and `tools/round-47/` (a directory
pathspec). Receipts under `.ufo/waves/round-47/controls/` are not frozen: a do-nothing
control can only be scored against a freeze that already exists. `git log --format=%H -1 --
plans/round-47-claims.md` re-derives the freeze; the report cites it as
`plans/round-47-claims.md@<freeze>`. Nothing in this file or in `tools/round-47/` changes
after the freeze: a change makes both counters exit 2 `frozen_path_changed`.

Owned axes are all tied at 10 (`SCORECARD.md` `## Owned axes`), none retired, and the last
capability entered in round 43 — the stagnation nudge does not waive the lowest-axis
obligation. Two claims on two distinct tied-lowest axes. Coverage gets no claim: this round
adds no domain surface.

| claim | axis | surface |
|---|---|---|
| R47-C1 | depth | `SKILL.md` `## Queue-drain craft` rule block 24 — the **exactness** matrix over the four round-46 routed instrument defects — and its interpreter `tools/round-47/exact.py` |
| R47-C2 | calibration | the lane's **current self-assessment** (the last two `## Round N` sections of `SCORECARD.md`) re-derived atom by atom against committed repo state by `tools/round-47/record.py` |

**Causal separability.** R47-C1's counter reads `SKILL.md`, this file's frozen paths,
`tools/round-47/exact.py` and `tools/round-46/gate.py`; it never reads `SCORECARD.md`.
R47-C2's counter reads `SCORECARD.md` and the `.ufo/waves/round-*/` dispatch and receipt
files; it never reads the craft section. Either lands and scores without the other. They
share `tools/round-46/gate.py`, which is frozen infrastructure from round 46, not a claimed
surface.

**Why this round exists.** The round-46 non-author spot-check routed four instrument defects
and one HIGH record defect, all named in `corpus/lessons/round-46.md` `## Routed defects`:

- `R46-CL2` the arm-vocabulary check is a substring test, so `blobberish` satisfies `blob`;
- `R46-CL3` the routed-id check requires every id to appear in *some* row, not exactly once,
  so a row can claim an id it does not address;
- `R46-CL4` the mutation list has no digest, so deleting a mutation changes the denominator
  that the claim is judged on without failing a clause;
- `R46-CL6` `gate.history_touched`'s `-m --diff-merges=first-parent` arm is order-sensitive
  and nothing enforces the order;
- `R46-CL7` (HIGH) the registry verdict-map clause binds the digits `0/1/2`, not their
  meanings — a contentless row scores met;
and the same spot-check's `R46-V1..V3` find the lane's own record false about its own
waves, its own empty window, and the revision its before-cell was measured at.

## R47-C1 — depth: an exactness matrix and a counter that binds tokens, cardinality, a digest and a flag order

**Prior state.** Craft block 23 (the round-46 freeze-integrity matrix) is scored by
`tools/round-46/attest.py`, whose four named bindings are loose in the four ways above: a
row's arm cell is accepted when *any* vocabulary token is a substring of it; a routed id is
accepted when it appears in *some* row; the nine-mutation list is checked by count but not
pinned to a digest; and the flag order that makes the history arm see a merge resolution is
a code detail no clause reads.

**Landed surface.** One new rule block in `## Queue-drain craft`, title beginning `24. `,
marker `<!-- exactness-table v3 -->` occurring exactly once in `SKILL.md`, the block being
the **last** craft block. Its table's header cells are exactly
`trigger | v2 hole | v3 arm | exit`, exactly four rows, every row exactly four cells, every
exit cell exactly one of `0`, `1`, `2`; every row's trigger cell names exactly one routed
`R46-CL<n>` id and the four ids R46-CL2, R46-CL3, R46-CL4, R46-CL6 each appear exactly once;
every row's v3-arm cell is exactly one token of `symbol`, `once`, `digest`, `order`; at
least three citations carry a line selector while resolving at the measured revision inside
`corpus/lessons/`, `corpus/knowledge/`, `plans/` or `tools/round-47/`, and
`corpus/lessons/round-46.md` is among them; the block carries
`mutations_sha256:<64 hex>` equal to the digest of `tools/round-47/exact.py`'s own
`MUTATIONS` name list in order, and `interpreter_sha256:<64 hex>` equal to the sha256 of
`tools/round-47/exact.py` at the measured revision.

**Predicate (each clause computed by `tools/round-47/exact.py --profile v3`).**

1. `marker_occurrences == 1`; `block_present == 1`; the marked block is the last craft block
   and its title starts with `24. `.
2. Header cells equal `["trigger", "v2 hole", "v3 arm", "exit"]` exactly.
3. `rows == 4`; every row four cells; every exit cell in `{0,1,2}`.
4. Every row's trigger cell names exactly one `R46-CL<n>` id, and the multiset over the four
   rows is exactly `{R46-CL2, R46-CL3, R46-CL4, R46-CL6}` (each once).
5. Every v3-arm cell, stripped of backticks and spaces, is one of `symbol`, `once`, `digest`,
   `order` — an equality, not a containment.
6. `mutations_sha256` equals sha256 over `"\n".join(name for name, _ in MUTATIONS)` of the
   counter's own mutation list, and the block names all four mutation names.
7. `tools/round-46/gate.py` at the measured revision contains the literal
   `"-m", "--diff-merges=first-parent"` exactly once and contains the reversed pair
   `"--diff-merges=first-parent", "-m"` zero times.
8. `refs >= 3`, every reference carries a line selector and resolves at `--rev`, the path set
   is validated, and `corpus/lessons/round-46.md` is cited; both sha256 pins match.
9. `battery.forgeries_total == 4`, `battery.v2_green == 4`, `battery.v3_green == 0`,
   `battery.genuine_green == 1`, `battery.crash == 0`. The four forgeries mutate the landed
   block (or, for `flag-order-drift`, the `gate.py` copy in the fixture repo) one defect
   class at a time: `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`,
   `flag-order-drift`; each is scored in a one-commit fixture repo under both profiles.

**Target.** `failing == []`, counter exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze <FREEZE> --rev <REV> --json-out <OUT>
```

**Before.** `controls/ctl-c1-0-do-nothing.json`: at the freeze the counter exits 1 with
`block_present 0`, `rule_blocks 23`, `marker_occurrences 0`. A do-nothing `SKILL.md` cannot
reach the target. `controls/ctl-c1-2-freeze-battery-absent.json`: at the freeze the battery
cannot even be built (`marker blocks 0`), so `forgeries_total == 4` is unreachable before the
landing. `controls/ctl-c1-1-v2-profile.json` (produced after the landing, when a block exists
to mutate): the four forgeries scored with `--profile v2` (the ported round-46 semantics)
exit 0, `v2_green 4` — the four holes measured, not asserted.

**Kill rule.** A block with `blobberish` in a v3-arm cell fails clause 5 while the v2 profile
passes it. A block with the same routed id in two rows fails clause 4. A block whose
`mutations_sha256` was computed over three of the four mutations fails clause 6 and a
deleted mutation changes the printed digest. A fixture whose `gate.py` carries the reversed
flag pair fails clause 7. A block that reuses block 23's text relabelled `24. ` fails clauses
2–6.

## R47-C2 — calibration: the current self-assessment is re-derived atom by atom, and every mismatch is corrected

**Prior state.** The lane's self-assessment is prose. The round-46 non-author spot-check
found three of its atoms false at the tip it cites (`corpus/lessons/round-46-verifier-spotcheck.md`
R46-V1 seat counts, R46-V2 the "empty" window, R46-V3 the before-cell revision), and the
lane had no command that could have caught any of them: every counting command the lane
owns reads the artefact, none reads the record.

**Landed surface.** `tools/round-47/record.py` extracts four atom classes from the last two
`## Round N` sections of `SCORECARD.md` at `--rev` and re-derives each one from committed
repo state:

| class | atom | derived from |
|---|---|---|
| `seats` | `Waves: A + B = C seats` and `Wave 1: A seats; wave 2: B seats` | `.ufo/waves/round-<N>/*-dispatch.json` → `counts.spawn` per dispatched wave, in file order |
| `window` | a sentence claiming `git log …` "is empty" over a window `X..Y` and a pathspec | the same `git log --name-status` run at `--rev`; a window naming `<tip>`/`<REV>` placeholders is `unverifiable`, which counts as a mismatch |
| `path` | every `.ufo/waves/…` token in the two sections | existence at `--rev` |
| `rev` | every backticked 7–40 hex token in the two sections | `git rev-parse --verify` plus ancestor-of-branch |
| `axes` | the leading `<resolved>/<total>` of each `coverage` and `depth` row of the **current** `## Owned axes` table | the coverage map against `corpus/knowledge/*.md`, and command A's citation-resolution count over `## Queue-drain craft `, both at `--rev` |

Repairs append a `## Record corrections — round 47` section to `SCORECARD.md`. Each
`- corrects <class> <key>: <statement>` line exempts the atoms it names and is itself
re-derived: a `seats` correction must state the correct dispatched-wave count and seat total,
a `window` correction must state a window the counter itself reproduces as empty. An
exemption whose correction is false keeps the atom red.

**Predicate (each clause computed by `tools/round-47/record.py`).**

1. `mismatches == []` — no atom disagrees with committed state and none is `unverifiable`.
2. `classes` covers all five (`seats`, `window`, `path`, `rev`, `axes`).
3. `corrections >= 2` and every correction line itself re-derives (`corrections_bad == []`);
   a `seats` correction must state `<n> waves, <total> seats total`, a `window` correction
   must state `empty in A..B -- paths`, an `axes` correction must state `<resolved>/<total>`.
   A correction that exempts an atom the card does not contain is itself a defect.
4. `exempted <= 3` — the repair may not exempt more atoms than the record defects it names.
   A `window` exemption covers only an atom whose window pair the correction states, or an
   atom that names no concrete window.
5. `sections` is exactly the last two `## Round N` headings of `SCORECARD.md` at `--rev`.
6. `battery.correction_forgeries == 3`, `battery.forgeries_green == 0`: three forged
   corrections (a seats total the dispatch files contradict, a window that is not empty, an
   exemption naming an atom that does not exist) each score the counter red.

The five classes are scoped: `seats`/`window`/`path`/`rev` read the last two `## Round N`
sections, `axes` reads only the current `## Owned axes` table — a historical snapshot table
inside a round section is a record of that round, not a claim about today.

**Target.** `failing == []`, counter exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev <REV> --json-out <OUT>
```

**Before.** `controls/ctl-c2-0-do-nothing.json`: at the base revision the counter exits 1
with `mismatches 4` naming the round-45 seat atom (claimed `wave 2: 32`, dispatched `36`),
the round-46 window atom whose window names a `<tip>` placeholder, the `coverage` row's
leading `133/133` against the observable `138/138`, and the `depth` row's leading `20/20`
against the observable `23/23`. `mismatches == 0` is unreachable for a do-nothing round.

**Kill rule.** Deleting the corrections section restores the two corrected mismatches. A corrections
section that exempts bubbles without re-deriving anything fails clause 3/4 (the vacuity
battery case). An exemption for an atom that does not exist fails clause 3. Editing a
dispatch `counts.spawn` to match a false claim leaves clauses 1 and 3 red because the
correction's own total is re-derived against the same files.

## Frozen paths (exact)

- `plans/round-47-claims.md`
- `tools/round-47/`

## Non-goals

No domain surface is touched: no knowledge entry, no coverage-map row, no `PROVINCE.md`
row. The round's frontier step is cited in the report's Sources section, not claimed here.
