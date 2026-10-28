# R45W2Rollback — reversibility of the round-45 landing

Seat `R45W2Rollback`, round 45 wave 2, leaf, lane `kaidoku-shokunin`. Read-only on the lane
tree and the fleet repo; every write of this seat is under
`.ufo/waves/round-45/w2/R45W2Rollback/` plus the trailer file
`.ufo/waves/round-45/w2/R45W2Rollback.md` named by the assignment. Nothing was staged,
committed, stashed or pushed in the lane; every mutation below lives in a scratch clone that
was removed after the receipts were copied here.

- Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing
  `e715263cb51b713c342ab992d527fe9d61d6f8ff`; A1
  `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` (the prompt's measured revision); tip
  `0ee50aaff516571aa607769bbbdf19a3db90dfa5` (the record's A3 measured revision, where the
  wave-2 record commits also live).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback`; `TMPDIR=$S`; clone
  `$S/clone` at `e715263` with `git -C "$S/clone" rev-parse --show-toplevel` asserted equal to
  the clone before the first mutant commit. Python 3.14.8, git 2.56.0. No installs, no
  package-manager action (pacman untouched), no network.

Mutation inputs (the exact bytes each verdict rests on; `SKILL.md` is the only path mutated):

| mutant | scratch commit | SKILL.md sha256 | lines | removed range |
|---|---|---|---|---|
| `m1` block 22 only | `dea1af58da20758e8d5d8f528d0d8cf1d07dc8e7` | `66175002156b831302b0c6bc87150035a3af8af73b8347987f626f1707d9b8e6` | 1596 | 1-based 547–589 (43 lines, incl. trailing blank) |
| `m2` registry only | `9d81a12d83396787f517c1c088850ee4963699df` | `5d00838c8af2db36eda05489f401ddb58897d715100e71ebb6ce4eff28b54258` | 1615 | 1-based 1616–1639 (to EOF) |
| `m3` both (= pre-landing) | `43b5efb08e776023e362283a5b0926c6bef4dd1b` | `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` | 1572 | both |
| `m4` rows 6+10 dropped | `637b1565efde8932040ee953cea105b960918ebd` | `87ab9c83baa3eece76cd469c5315ada9f3963477329a9220aee2bb8b9960e47e` | 1637 | two table rows (8 remain) |
| `m5` rows 6+9+10 dropped | `40afee900065f2ee1e20beb84b3305b82f6c144f` | `6038a11c781b331d1c14fae7a6d7e189e68b904d7e2166f8e6641149d7493626` | 1636 | three table rows (7 remain) |
| tip textual revert | `9e947c5e4ab2285891dc687ac07b8b3b06953bfc` | `32fb1a265da04c07c958cf04a4f4552bdec94fb527ef863cf1e08e313c03b724` | 1572 | block 22 as amended (1-based 547–611) + registry (1639–1661) |

`m3` and the tip revert both hash to the pre-landing/base `SKILL.md`
(`32fb1a26…`): the removals are exact, not approximate.

## Verdict table

| # | attack (what it targets) | target | verdict |
|---|---|---|---|
| A | remove block 22 → command A `rule_blocks` back to 21, no other block's citations change | R45-C1 clause 1; `## Measurement recipes` A | **holds** |
| A′ | counter behaviour on the same removal | R45-C1 clauses 1–6 | **holds** (c1 exit 1, four clauses named; c2 unaffected) |
| B | no surviving `SKILL.md` text depends on block 22 / the new section | R45-C1 "landed surface" | **falsified** — one surviving registry row names "rule block 22" |
| C1 | no dangling reference at the measured revision (registry receipt pointer) | R45-C2 registry prose | **falsified** — 0 receipt entries at `e715263`/A1, 57 at tip |
| C2 | lesson evidence pointer resolves | `corpus/lessons/round-45.md:16` (M45-1) | **falsified** — directory never created at any revision |
| C3 | lesson's other evidence pointers | `round-45.md:40,60` | **falsified at the measured revision**; resolves only at tip |
| C4 | block-only removal vs the lesson | `round-45.md:6,28` | two identity mentions remain; no line citation dangles |
| D1 | full textual revert at the landing | landing `e715263` | **holds** — byte-identical to `9ff920cd` |
| D2 | full textual revert at the measured tip | tip / A3-amended block 22 | **holds** — byte-identical to base `149133d4` |
| D3 | commit-level revert | `git revert e715263` at tip | **does not reverse cleanly** (conflict `UU SKILL.md`, `UD` lesson) — fact, not a claim violation |
| E1 | dead weight: rows no claim needs | R45-C1 clause 3 (`rows >= 8`) | rows 6 and 10 are surplus: 8-row mutant is met |
| E2 | row 10's exit cell vs its own interpreter | block 22 row 10 | **falsified** — empty range + dirty frozen file exits 1, row says 0 |
| E3 | row 6 reachability and receipt cell | block 22 row 6 | **dead under first-match; receipt cell names fields the gate never emits** |
| E4 | block title "every arm has a red case" | block 22 title vs A3 body + selftest names | **overstated** (`blob` has no dedicated case) |
| E5 | dead registry row | R45-C2 scope | **holds** — all six rows load-bearing |
| E6 | A1's knowledge citation is not dead weight | depth axis / command A | **holds** — load-bearing (9.55 → 10.0) |
| F | first-cell exactness (adjacent axis) | R45-C2 clause 2 | **falsified** — prose-prefixed first cell passes |

## A. (a) Block-22 removal: command A returns to 21, no other block's citations change — holds

Command: the `## Measurement recipes` **A** script, verbatim, run as `python3 -B measure.py
<rev>` with cwd `$S/clone`; `measure.py` is that recipe plus a per-block dump (index, body
sha256, ref names, resolved flag, unresolved list). Aggregate receipts:

| rev | role | `rule_blocks` | `citation_resolved_rules` | `depth_score` | `mapped`/`knowledge_files` | receipt |
|---|---|---|---|---|---|---|
| `9ff920cd` | pre-landing | 21 | 21 | 10.0 | 138/138 | `cmdA-pre` |
| `e715263` | landing | 22 | 21 | 9.55 | 138/138 | `cmdA-land` |
| `1f4b27f8` | A1 (measured) | 22 | 22 | 10.0 | 138/138 | `cmdA-a1` |
| `0ee50aaf` | tip (A3) | 22 | 22 | 10.0 | 138/138 | `cmdA-tip` |
| `m1` | block 22 removed | **21** | **21** | **10.0** | 138/138 | `cmdA-m1` |
| `m2` | registry removed | 22 | 21 | 9.55 | 138/138 | `cmdA-m2` |
| `m3` | both removed | **21** | **21** | **10.0** | 138/138 | `cmdA-m3` |
| tip revert | both, amended text | **21** | **21** | **10.0** | 138/138 | `cmdA-tiprevert` |

The count returns to 21 exactly, and the citation-resolved count returns to 21 with it. No
other block's citations change, proved at block granularity rather than by the aggregate:
blocks 1–20 are byte-identical between the pre-landing file and `m1`/`m3`; block 21 differs
only in trailing blank lines (`rstrip` equal) and keeps its single citation
`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`, resolved; every block's ref count,
ref-name set and `resolved` flag is unchanged in `m1`, `m2` and `m3`.

Two facts the aggregate masks, both relevant to the claim:

- The landing commit itself **lowered** the depth axis: at `e715263` block 22 has zero
  `corpus/knowledge/` refs, so command A reports `22` blocks / `21` resolved / depth `9.55`.
  A1's added citation is what makes the axis whole. Consequently removing block 22 *raises*
  command A depth from 9.55 to 10.0 — the removal repays a cost the landing introduced before
  A1. This is not a reversal defect; it is the reason A1 exists, and A1's own message says so.
- `m2` shows command A is blind to the registry section (identical to the landing: 22/21/9.55).
  The C1 and C2 surfaces are causally separate in both directions: c2 exit 0 on `m1`, c1 exit 0
  on `m2`.

Counter behaviour on the same mutants (`python3 -I -B tools/round-45/c1-counter.py --root
$S/clone --freeze f762b727… --rev <mutant> --json-out …`):

- `m1`: c1 exit **1**, `failing = ["rule_blocks 21 != 22", "block22_present 0 != 1",
  "block22_rows 0 < 8", "block22 table header lacks trigger/arm/exit/receipt",
  "block22_refs 0 < 4"]`; c2 exit **0**.
- `m2`: c1 exit **0**; c2 exit **1**, `unregistered` = all six scope paths.
- `m3`: c1 exit **1**; c2 exit **1** (six unregistered).
- tip revert: c1 exit **1** (21 blocks); c2 exit **1** (six unregistered).

So the removal is detected by exactly the instrument the claim names, and neither counter
covers the other's surface.

## B. (b) No surviving `SKILL.md` text depends on block 22 or the new section — falsified (one row)

Direction that holds: with the registry section removed (`m2`), the only surviving hits for
the removed surface are inside block 22 itself (`<!-- freeze-integrity-table v1 -->`, line 567);
no text outside the section refers to it, and command A is unchanged.

Direction that fails: with block 22 removed (`m1`), line 1591 of the mutant is the surviving
registry row

```
| `tools/round-45/c1-counter.py` | gate — R45-C1 depth: rule block 22 in `## Queue-drain craft`, its citations, and the interpreter's own selftest | …
```

Exact input: `m1`. Differing value: one surviving `SKILL.md` span references the removed block
(the other three hits at lines 1574, 1579, 1592 are the registry's own text). Fix: describe the
counter as "the craft rule block this round added" with no number, or edit that row in the same
removal. This is a descriptive dependency, not a functional one — c1 still runs and c2 still
passes on `m1` (exit 0) — so the claim's "no surviving text depends" phrasing is what fails,
not the instrument.

## C. (c) Dangling references — falsified at the measured revision

**C1 — registry receipt pointer.** The registry section's own prose says "Every row was read
from source and its self-test run at the round-45 freeze `f762b727`; receipts
`.ufo/waves/round-45/w1/R45W1Reg*/`". Measured with
`git ls-tree -r --name-only <rev> -- .ufo/waves/round-45/w1 | grep -c R45W1Reg`:

- `e715263` (landing): **0**
- `1f4b27f8` (A1, measured): **0**
- `0ee50aaf` (tip): **57**

The pointer resolves only four commits after the landing. It is not caused by the removal
(removing block 22 does not touch it), but it means the landing's registry section, at the
revision it was committed and at the revision the record measures, cites evidence that does not
exist there. Fix: land the registry receipts before the landing, or move the landing after wave
1's evidence commits.

**C2 — lesson evidence pointer (permanent).** `corpus/lessons/round-45.md:16` (M45-1) cites
`.ufo/waves/round-45/w1/R45W1InhSweepEvidence/` as "the re-derived audit of commit
`c86ea508`". That directory exists at **no** revision:
`git log --all --oneline --diff-filter=A -- '.ufo/waves/round-45/w1/R45W1InhSweepEvidence*'`
prints nothing (exit 0, empty), and `.ufo/waves/round-45/r45-w1-results.json` records the seat
as `"output": null`, note `"never spawned: host job-cap refusal during wave fill; wave
completed without it (partial-fill loss recorded by L1)"`. The lesson asserts a re-derivation
whose container was never created. This survives the removal unchanged (it is dangling at
every revision), so it is not a reversibility defect of the landing — it is a standing dangling
reference in the record the seat was asked to check. Fix: point M45-1 at the report that
actually carries the derivation, or say the seat never ran.

**C3 — lesson forward pointers.** `round-45.md:40` cites
`.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md` and `:60` cites
`.ufo/waves/round-45/w1/R45W1CensusDupClass`; both are absent at `e715263` and A1 and present
at tip. Same class as C1 (record committed before its evidence), same fix.

**C4 — the lesson and a block-only removal.** The lesson names block 22 twice by identity
(`:6` "R45-C1 depth (SKILL rule block 22, the freeze-integrity decision table…", `:28` "block
22's dirty arm parses…") and contains **no** `SKILL.md:<line>` citation at all. A block-only
removal therefore leaves two identity references to a block that no longer exists, but no line
citation dangles. A full landing revert removes the lesson with the block (same commit), so
this is specific to the task's block-only scope.

## D. Full textual revert — holds, exactly

- **D1, at the landing.** `m3` (block 22 + registry removed, nothing else) has `SKILL.md`
  sha256 `32fb1a26…`, byte-identical to pre-landing `9ff920cd`, 1572 lines.
- **D2, at the measured tip.** Removing block 22 as amended by A1/A2/A3 (1-based 547–611) and
  the registry section as corrected by A3 (1639–1661) yields sha256 `32fb1a26…`, byte-identical
  to the round base `149133d4`, 1572 lines. Counters at that rev: c1 exit 1 (`rule_blocks 21 !=
  22`), c2 exit 1 (six unregistered), command A 21/21/10.0 with 138/138 mapped.
- **D3, commit-level.** `git -c … revert --no-commit e715263` at tip exits **1** with
  `UU SKILL.md` and `UD corpus/lessons/round-45.md`; reverting A3 first exits **1** with `UU
  corpus/lessons/round-45.md` because `a63d109f` later edited the same lesson region. So the
  landing is reversible as text (or by rewinding the four `SKILL.md` commits in order with
  conflict resolution), but not as one `git revert`. Reported as a fact about the landing's
  shape, not as a claim violation: the amendments are part of the landing.

## E. Dead weight — two table rows no claim needs, one of them false

**E1 — the floor is exactly 8 rows; rows 6 and 10 are surplus.** Claims R45-C1 clause 3 is
`block22_rows >= 8`. `m4` drops row 6 ("one bulk commit sweeps N frozen paths beside unrelated
paths") and row 10 ("FREEZE equals REV (empty range)"): rows **8**, c1 exit **0**,
`met_target true`, `failing []`. `m5` drops rows 6, 9 and 10: rows **7**, c1 exit **1**,
`block22_rows 7 < 8`. No claim clause names either row; the claims name "bulk sweep" only as a
`--selftest` case, and name no empty-range case at all.

**E2 — row 10 is false against its own interpreter.** Input: `FREEZE == REV` and the frozen
worktree dirty. Fixture `$S/fx-empty-dirty` (`git -C "$D" init -q`, toplevel asserted;
`frozen/a.txt` committed then modified, freeze = rev =
`34f967c5b3543e2e5733334430663285a916022a`):

```
python3 -I -B tools/round-45/frozen-path-preflight.py --root "$D" \
  --freeze HEAD --rev HEAD --pathspec frozen/ --freeze-path frozen \
  --require-pathspec --check-dirty
→ exit 1, dirty: [" M frozen/a.txt"], verdict: "frozen_path_changed"
```

Row 10 says `FREEZE equals REV (empty range) | all arms | 0 | verdict clean`. The arm cell is
also wrong: the dirty arm is range-independent. And under the block's own reading rule ("the
first row whose trigger holds decides"), row 9's trigger — no touch, no dirty file, every
frozen blob equal — holds for a clean empty range, so row 10 is unreachable even where it is
true. Fix: delete row 10; row 9 already decides the empty range.

**E3 — row 6 is unreachable and its receipt cell over-promises.** Row 1's trigger ("any commit
in FREEZE..REV touches a frozen path") holds for every bulk sweep, so row 6 can never be the
first match. Its receipt cell promises "`touched[]` count and the frozen subset"; the gate's
receipt on the sweep fixture (`$S/fx-sweep`, freeze `34f967c5`, rev
`127908a4285571b3ea9e67b4ebaf8425d2de7d9a`, eight frozen files plus `outside.txt` in one
commit) has keys exactly `blob_changed, dirty, freeze, freeze_paths, gate, pathspec, restored,
rev, touched, verdict`, `touched` length 8 — there is no count field and no frozen-subset
field, and the log is pathspec-scoped, so `touched` is already the frozen subset. Fix: fold the
sweep into row 1's trigger, or make the receipt cell say "`touched[]`, scoped by `--pathspec`;
`len()` is the count".

**E4 — title overstates, and no claim needs the title.** Block 22's title says "every arm has a
red case". A3's body in the same block says the red cases are "arm-covering but not
arm-isolating — deleting the `restored` classification or the `blob` arm alone still reads 11/0
because `touched` absorbs the kill", and the 11 selftest case names are `green-clean`,
`red-touched`, `red-restored`, `red-dirty`, `green-dirty-without-arm`,
`red-dirfreeze-no-pathspec`, `green-dirfreeze-pathspec`, `red-unknown-freeze`,
`red-nonancestor`, `red-bulk-sweep`, `green-empty-range` — there is no `blob` case and no case
named `pathspec-required`. The claims' own red-case list omits `blob` too. Fix: "every arm a
fixture can separate has one red case", which is what the body already says.

**E5 — the registry has no dead row.** All six rows are load-bearing for R45-C2: each scope
path must be the first cell of some row whose third cell names `0`, `1`, `2`; dropping the
section makes c2 exit 1 with exactly six unregistered. No row can be removed without failing
the claim.

**E6 — A1's knowledge citation is not dead weight.** At `e715263` block 22 has 0
`corpus/knowledge/` refs and command A depth is 9.55; at A1 (and every later revision) it has
one resolving ref and depth is 10.0. The citation is what the depth axis scores.

## F. Adjacent finding, reported for the L1 (not this seat's axis, not scored)

R45-C2 clause 2 says "some `SKILL.md` registry row's **first cell is exactly** that path
(backticked, path equality)". The implementation accepts any first cell that *contains* a
backticked tool path. Mutant `f40eb88f917ba129a9bab3172ce6a38138a01db6` rewrites one row's
first cell to ``see the `tools/round-44/c1-run.sh` script``:

```
python3 -I -B tools/round-45/c2-counter.py --root clone --freeze f762b727… --rev f40eb88f… 
→ exit 0, met_target true, unregistered [], thin []
```

So a prose-prefixed cell satisfies the predicate although the claim says path equality. This
is a prefix-tolerance gap, not row counting (the counter's selftest does test wrong-path rows).
Routed here because it fell out of the dead-weight check; the C2-instrument seats own the
verdict.

## Costs and residual limits

- **Insertion cost.** The block-22 insertion at 1-based line 547 shifts every later `SKILL.md`
  line by +43. There are 79 `SKILL.md:<line>` references in tracked markdown (excluding
  `.ufo/` and `corpus/evidence/`); 16 point past line 545; at the landing all 16 point at
  different text than at pre-landing, and the +43 shift repairs all 16 (`final-checks.out`).
  They are historical lesson/claim citations, so the lane tolerates the drift; the removal
  repays it. This is the only side-effect the removal has on the rest of the repo, and it is a
  repair, not a harm.
- **What is not reversible.** The text is exactly reversible (D1/D2). The residue that is not
  is the record's evidence set: C1's receipts and C2/C3's reports exist only at later
  revisions, and C2's directory never exists at all. Removal neither creates nor fixes that.
- **Not run.** No re-fetch of S140/S141 (source-seat axis; no network in this seat). No scoring
  of the depth or calibration axis beyond the removal's effect on command A and the two
  counters. The two counter selftests were re-run from the clone's bytes (`c1-selftest` 9/0,
  `c2-selftest` 7/0) and only confirm the registry rows' stated case counts; they are not a new
  audit. No lane or fleet file was mutated.
- **Lane cleanliness.** Before this seat's writes, `git -C <lane> status --porcelain` showed
  only pre-existing untracked w2/l1 seat artifacts. `git rev-parse` of
  `plans/round-45-claims.md` and of the `tools/round-45` tree at HEAD equals the freeze
  (`f93df4c3bd4069a0cd576d9649f1157609b6a5d5`,
  `8cb6fa801ed16c54f3db14bb7c432a3d5385997e`). The scratch clone, fixtures and `$S` were removed
  after copying the receipts here.

## Receipts

Files under `receipts/`; each `<name>.receipt` carries `name`, `utc`, `cmd`, `exit`,
`stdout_sha256`, `stderr_sha256`; `<name>.out`/`.err` are the captured streams and
`c1-*.json`/`c2-*.json` the counters' `--json-out`. Full commands for the load-bearing runs:

- command A: `python3 -B measure.py <rev>` (cwd `$S/clone`) — the SCORECARD `## Measurement
  recipes` A script plus the per-block dump.
- c1: `python3 -I -B tools/round-45/c1-counter.py --root "$PWD" --freeze f762b727… --rev
  <rev> --json-out receipts/c1-<tag>.json` (cwd `$S/clone`).
- c2: same with `c2-counter.py`.
- preflight: `python3 -I -B tools/round-45/frozen-path-preflight.py --root "$D" --freeze …
  --rev … --pathspec frozen/ --freeze-path frozen --require-pathspec [--check-dirty]` on the
  asserted fixtures.
- revert tests: `git -c user.name=m -c user.email=m@x revert --no-commit <sha>` at tip.

| receipt | exit | UTC | stdout sha256 |
|---|---|---|---|
| `c1-a1` | 0 | 2026-10-28T16:02:13Z | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` |
| `c1-land` | 0 | 2026-10-28T16:02:13Z | `cb869305df9b64d68e106ce1acfa326dd6d73c8b15f18b07d7546b898c5cc95f` |
| `c1-m1` | 1 | 2026-10-28T16:02:14Z | `96b7c056f88901130cf8303784f5a2fd4c37709e6ad70b08d6d9e0580550d71b` |
| `c1-m2` | 0 | 2026-10-28T16:02:14Z | `c71b96dffaacce86e5aaba0da135444e62c11e1f8116dd0fbbd01624e6980001` |
| `c1-m3` | 1 | 2026-10-28T16:02:14Z | `0e099c38ea2ae0581613d241eb8025a37ef44ae82f86039566d637ff3a641711` |
| `c1-m4` | 0 | 2026-10-28T16:04:14Z | `1a9cc9af4fd2e1e762a198a14e1ee42bc3e711945eeb392a7f9e6cd693fdabe7` |
| `c1-m5` | 1 | 2026-10-28T16:04:14Z | `2a227bcd264bcc46f4bfe23bc1a9de76de4fbece2071426f97e3642030bf6314` |
| `c1-selftest` | 0 | 2026-10-28T16:06:30Z | `296734f224877a86e8d216bcde5382bbe0f18ff1dadddb1d18099f3754fdac6d` |
| `c1-tip` | 0 | 2026-10-28T16:02:13Z | `4b2eb21a619c15438c73c6cf56a868fc046f5cef85d46d343acc07ecbb337e9c` |
| `c2-a1` | 0 | 2026-10-28T16:02:13Z | `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca` |
| `c2-land` | 0 | 2026-10-28T16:02:13Z | `a292755ac912dd2499e8320261686d3be984e111c5b870777fdf7a3dcd41aad0` |
| `c2-loosecell` | 0 | 2026-10-28T16:07:05Z | `1f415b6fa323b323e0dee7c11f689b32f6700c84f3b1c0b38d8ce345dfa3c2fd` |
| `c2-m1` | 0 | 2026-10-28T16:02:14Z | `dd078e9d0e41daecad831afe049dfcc69fdfbb84176cfcc304a7882aab2213ce` |
| `c2-m2` | 1 | 2026-10-28T16:02:14Z | `099ea05cfbeb0208b47b7ec74f585e3b149d915be84f082362519db03c50b1d5` |
| `c2-m3` | 1 | 2026-10-28T16:02:14Z | `ab7a6b879930a72223c1272bc57acb0783d4622378ffa1a904bfb0718aa9a9f1` |
| `c2-selftest` | 0 | 2026-10-28T16:06:30Z | `aea7e363e5661efcc038df11f2e88380c11815b480d9458f9cc26370b40b0f2d` |
| `c2-tip` | 0 | 2026-10-28T16:02:13Z | `7528d520399fbdf1aa5844108bc77940dd4852412b599592a2e9af531f558361` |
| `cmdA-a1` | 0 | 2026-10-28T16:02:13Z | `d7dfcc3eac57945f6a00e4d4707f08c402d0de31d09f77d546de22c481c6c065` |
| `cmdA-land` | 0 | 2026-10-28T16:02:12Z | `6c5dc35d9d2aec250010fcdb1cbcd278bb6870278719709ff5e336004a268af5` |
| `cmdA-m1` | 0 | 2026-10-28T16:02:14Z | `ab2fac3d8ad11bfe6280d2fade98652be418dcbf86c7586cf781cedf9fbf5d9a` |
| `cmdA-m2` | 0 | 2026-10-28T16:02:14Z | `6b9da21aa4acd5b43060f830654d50acdefe78af914e1405dd2af3603ce4df61` |
| `cmdA-m3` | 0 | 2026-10-28T16:02:14Z | `d34f04fe848c12b64713999fa4b36d4dd69b5a764732d91fb8013ab9dd693ffd` |
| `cmdA-tip` | 0 | 2026-10-28T16:02:13Z | `1b08fe220b7a17c17166b83b5d1f5e82fe740cede8738e1de6c4d20291cf74ed` |
| `cmdA-pre` | 0 | 2026-10-28T16:08:40Z | `6b84660511b237f17bdbd7ea93d080976d80cf62e83453b519bbfed84bc50d6d` |
| `cmdA-tiprevert` | 0 | 2026-10-28T16:07:05Z | `fa27bf2bb8dd90efedcfe50bb1629b327629fe3544b8e8dc58059bfda22b5069` |
| `c1-tiprevert` | 1 | 2026-10-28T16:08:40Z | `346a48ea82ed23f557170b51d2a5567c8906c5bdc1079c16d341b3da7a3e0c53` |
| `c2-tiprevert` | 1 | 2026-10-28T16:08:40Z | `87aaea90f7c1079096ccf82a115c3942ee49aba24258f9fde1f9e614e6f6d6b8` |
| `final-checks` | 0 | 2026-10-28T16:06:12Z | `5d72c200bc6c0880f08fafcb32150edf3ab1104571717e1071807dd3d6c6e349` |
| `preflight-bulk-sweep` | 1 | 2026-10-28T16:03:43Z | `96fb78a982d2537ce988a84a72c42a4b148df9b7d5dbfcf89fb0a688cdaa16b2` |
| `preflight-empty-range-dirty` | 1 | 2026-10-28T16:03:43Z | `c58ccd3784f168e6ba511a89934b88e1a4ce75dbed4f0250ed35fc10e3369c1c` |
| `preflight-selftest` | 0 | 2026-10-28T16:03:43Z | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` |
| `revert-single` | 1 | 2026-10-28T16:04:57Z | `e0a1f67eaa2ba3fd0b9aee594487dcd03246fdc1abcf92f0625f42532c2f91aa` |
| `revert-ordered` | 1 | 2026-10-28T16:07:05Z | `1ded1ab20eb4df6b499ce4784b673c2abea22817b94068b89ed22f2b513dc115` |

`cmdA-tiprevert`'s sha is recorded in its `.receipt`; `mutations.json` holds the mutation
identities, the removed ranges and the two byte-equality flags (`m3_equals_prelanding: true`,
`tiprevert_equals_base: true`). Every exit code above is semantic: `0` met/clean, `1`
not-met/violation (the preflight fixtures and the reverts are *expected* 1s), `2` never
occurred in this seat's runs.
