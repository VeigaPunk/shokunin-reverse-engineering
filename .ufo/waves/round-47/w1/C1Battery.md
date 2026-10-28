# C1Battery — the four R47-C1 forgeries, built and scored independently

Seat `C1Battery`, round 47 wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`; base `13a9e9e1`; lane HEAD at measurement
`3186f69b49798f2cc05727bbfd1604505fcee03b`. Read-only on the lane tree: nothing outside
`.ufo/waves/round-47/w1/C1Battery/` was written; scratch was
`/fast/scratch/hyaku/kaidoku-r47/C1Battery` (removed after the receipts were copied).

Axes: coverage = every one of the four named classes built and scored under both profiles;
depth = each class mutated by code I wrote (not imported from the counter), plus a reader I
wrote that re-derives the clauses from the fixture bytes; calibration = exact command, exit
code, stdout sha256 and UTC on every run, and two controls that must stay green.

## 1. Result — the four classes discriminate, under my mutations, not the counter's

One-commit fixture per class. Fixture `SKILL.md` = the candidate block-24 bytes
`sha256:bf94d1b5…` inserted into `SKILL.md`; every other file taken from `git show 5017e1f:`.
Every fixture is a fresh `git init` in scratch with `git -C "$D" rev-parse --show-toplevel`
asserted equal to the fixture dir before its single commit.

| class | v2 exit | v3 exit | failing clause (v3) |
|---|---|---|---|
| `substring-arm` | **0** | **1** | 5 — `arm cells not exact vocabulary tokens: ['symbols','once-over','digest-pin','ordering']` |
| `duplicate-routed-id` | **0** | **1** | 4 — `routed cardinality {'R46-CL2':1,'R46-CL3':2,'R46-CL4':1,'R46-CL6':1} != … exactly once` (+ 3 — `rows 5 != 4`) |
| `stale-mutations-digest` | **0** | **1** | 6 — `mutations_sha256 does not match the counter's own mutation list` |
| `flag-order-drift` | **0** | **1** | 7 — `gate.py flag order: 0 correct, 1 reversed` |

`v2_green 4`, `v3_green 0`, `crash 0` — the clause-9 counts, reached without the counter's
`run_battery` ever running for the four rows below. Genuine control (the unmutated candidate):
v2 exit 0, v3 exit 0, and **v3 with the battery enabled exit 0** with
`battery = {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`.

Receipts (command, exit, stdout sha256, UTC in `receipts/runs.json`):

| class | rev | v2 cmd / exit / stdout sha256 | v3 cmd / exit / stdout sha256 | v3 + battery |
|---|---|---|---|---|
| genuine | `cb504a0577b2` | `--profile v2 --no-battery` → 0 / `acc1dabea6085a45…` | `--profile v3 --no-battery` → 0 / `b68db8fe7b353a31…` | 0 / `09563dfcc7b59339…` |
| substring-arm | `f05ce08ce5fb` | 0 / `9c4884c3489263c5…` | 1 / `3e3a91ebbb79e325…` | 1 / `0b25e54dfc47248b…` |
| duplicate-routed-id | `bcc802e9782c` | 0 / `9976ba9fac1e6905…` | 1 / `dc789875abd63b65…` | 1 / `a819c22afedb6ffd…` |
| stale-mutations-digest | `0ec1ca6321bf` | 0 / `e5486de8fa8c2f26…` | 1 / `e3377601e1a724af…` | 1 / `a38f1fd7d2b5c72d…` |
| flag-order-drift | `cf08d4392b6c` | 0 / `ba4a6fa2e4d6cd4f…` | 1 / `4e255856fbbd5926…` | 1 / `8306789b27158934…` |

Command shape for every row (cwd irrelevant; `TMPDIR=$S HYAKU_SCRATCH=$S` set):

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py \
  --root <fixture> --freeze <fixture HEAD> --rev <fixture HEAD> --profile {v2,v3} --no-battery
```

`--no-battery` is not a convenience: `score()` applies the battery counts **in both profiles**
when a battery is present, and the counter's own `run_battery` scores its fixtures with
`battery=None`. `--profile v2 --no-battery` is the exact analogue of that call; `--profile v2`
alone is not (finding F4).

### What each mutation was, in my code (not the counter's)

* `substring-arm` — every arm cell replaced by a **superstring of that row's own token**:
  `symbol→symbols`, `once→once-over`, `digest→digest-pin`, `order→ordering`. v2's check is
  `any(tok in cell)` on the lowercased cell, so all four pass it; v3's equality does not.
* `duplicate-routed-id` — a fifth row appended whose trigger names `R46-CL3`, which row 2
  already addresses. All four ids still present, so v2's "appears in *some* row" test passes.
  (The counter's own built-in version duplicates `R46-CL2` and sets all arms to `order-ish`;
  mine duplicates `R46-CL3` and leaves the arms alone.)
* `stale-mutations-digest` — pin replaced by a sha256 over **three names chosen differently
  from the counter's own slice** (`substring-arm`, `duplicate-routed-id`, `flag-order-drift`,
  i.e. `447178b4…`, not the counter's `b7d3e477…` over its first three). The block still states
  all four names, so only the equality fails.
* `flag-order-drift` — the fixture's `tools/round-46/gate.py` copy: the single
  `"-m", "--diff-merges=first-parent"` literal replaced by
  `"--diff-merges=first-parent", "-m"`. Block bytes unchanged (`skill_diff_lines 0`).

## 2. Why this is not the counter's self-report

Six independent legs, all measured:

1. **Independent mutation code.** `attack.py` does not import `exact.py`; it re-implements each
   class from the claims file's clause text, with different literals from the counter's
   `_m_*` functions (different superstrings, different three-name subset, different duplicated
   id). The four reds above are produced by *my* mutations.
2. **Independent clause reader.** `read_clauses()` re-derives marker count, header, row count,
   per-row id arity, id multiset, arm tokens, both sha256 pins, the two gate literals and every
   citation (allow-list, selector, line-count resolution, must-cite) from the fixture's own
   bytes. It names exactly the same clause(s) as the counter's `failing` list on **all 14
   fixtures** — no extra and no missing verdict. (The one apparent disagreement,
   `block23-relabelled`, was a false match in my own comparison script: the string `marker:`
   occurs inside the counter's arm-cell message.)
3. **The instrument is not red-always.** The genuine candidate scores `0` under v3, both
   without and with the battery. A counter that failed everything would "discriminate"
   trivially; this one does not.
4. **v2 is not red-always either.** All four forgeries and both escape probes score `0` under
   v2 — so the red is attributable to the v3-only clauses, not to a shared parse defect.
5. **Controls that are a change but not the defect stay green.** A prose word changed in the
   block (`checkable→inspectable`) → v3 exit 0; a comment line appended to the fixture
   `gate.py` → v3 exit 0, `gate_order_literal 1`, `gate_order_reversed 0`. So clause 7 reads
   the *flag literal*, not "the file changed", and clause 6 reads the pin, not "the block
   changed".
6. **The receipt carries values, not just a verdict.** For each class the mechanism is
   visible in the counter's own numbers — `arm_tokens ['symbols','once-over','digest-pin',
   'ordering']`, `routed_counts {'R46-CL3': 2}` vs `rows 5`, `mutations_sha256` vs
   `mutations_sha256_expected`, `gate_order_literal 0` / `gate_order_reversed 1` — and my
   reader reproduces each of those values independently.

**And yet the self-report is not sufficient**, which is the point of the next section: a
forgery *outside* the counter's four seeded classes passes the full counting command.

## 3. Findings

### F1 (HIGH, escape) the full counting command passes an arm-permuted block

Clause 5 is a **membership** test (`arm in VOCAB`), not a binding of the arm to the row that
needs it. Rotate the four tokens one row (`CL2→digest`, `CL3→symbol`, `CL4→order`,
`CL6→once`): every cell is a vocabulary token, `failing == []`, `met_target true`, and the
battery still reports `4/4/0/1/0` because `genuine_green` scores the *permuted* block as the
genuine one and it passes.

```sh
python3 -I -B …/tools/round-47/exact.py --root <fx> --freeze b50cbd88327b… --rev b50cbd88327b… --profile v3
```

| profile | exit | stdout sha256 | failing |
|---|---|---|---|
| v2 | 0 | `c39c4ab76d9da541…` | `[]` |
| v3 | 0 | `b0b7d385bbd1509a…` | `[]` |
| v3 + battery | **0** | `98068f7ce2cecd35…` | `[]`, `met_target true`, battery `4/4/0/1/0` |

Fixture bytes: `fixtures/SKILL.arm-permutation.md` (`sha256:d01177b8…`); block diff:
`diffs/diff-arm-permutation.skill.diff`. Why it matters: the block's own row text asserts a
meaning (`symbol` is the equality arm, `order` is the gate literal arm), and a table that
contradicts its own prose scores `met`. This is the **R46-CL7 class recurring inside the
round-47 block** — a clause that binds tokens rather than the token's meaning. Clause 5 is
frozen (`tools/round-47/`), so it cannot be tightened this round: recommend a round-48 routed
defect (`R47-CL1`) to bind a bijection `R46-CL2→symbol, R46-CL3→once, R46-CL4→digest,
R46-CL6→order`, and record the escape as a stated limit of the R47-C1 claim.

### F2 (HIGH, escape) six identical two-line citations satisfy clause 8

`receipt["refs"]` counts **matches**, not distinct spans, and `MUST_CITE` is satisfied by any
occurrence of the path. Replacing every selectored citation in the block (6 of them) with
`corpus/lessons/round-46.md:1-2` — a path that resolves, but names the round title and nothing
about any of the four defects — yields `refs 8` (the 6 trivial ones plus 2 self-reference
matches), `bad_refs []`, `must_cite true`, `cited` = `{corpus/lessons/round-46.md,
tools/round-47/exact.py}`, `failing []` — `met_target true` — and the battery still green.

| profile | exit | stdout sha256 | failing |
|---|---|---|---|
| v2 | 0 | `7084ea50644439fd…` | `[]` |
| v3 | 0 | `eb7a6ff660bd176c…` | `[]` |
| v3 + battery | **0** | `7a1297cf7793a37f…` | `[]`, battery `4/4/0/1/0` |

Fixture bytes: `fixtures/SKILL.citation-vacuity.md` (`sha256:7cba303a…`); diff:
`diffs/diff-citation-vacuity.skill.diff`. This is the **R45-CL9 class** ("a citation resolves
but names nothing about the defect") reappearing at the *count* rather than the *shape* of the
citation set. Frozen clause 8 cannot be changed this round; recommend a round-48 routed defect
(`R47-CL2`): `refs >= 3` over **distinct** `(path, span)` pairs, at least three distinct paths,
and no span shorter than, say, 3 lines — plus keep `MUST_CITE` pointing at the routed-defects
section rather than the file.

### F3 (calibration) the claims file's kill-rule literal does not demonstrate the v2 hole

`plans/round-47-claims.md` R47-C1 **Kill rule** says "A block with `blobberish` in a v3-arm cell
fails clause 5 while the v2 profile passes it." Measured: `blobberish` is not a superstring of
any token in *this* counter's vocabulary (`symbol`, `once`, `digest`, `order`), so v2 **fails**
too.

```sh
… --profile v2 --no-battery   → exit 1, stdout sha256 d9cc318332b19419…, failing ["arm cells outside the vocabulary"]
… --profile v3 --no-battery   → exit 1, stdout sha256 c6fab366245882e2…
```

`blob`/`blobberish` is round-46's vocabulary (`attest.py`); R47's superstring demonstrations are
`order-ish`, `symbols`, `once-over`, `digest-pin`. The kill rule as written is not reproducible;
the sentence needs the token that actually holds (the counter's own `--selftest` case
`red-arm-substring` uses `order-ish`). Fixture: `fixtures/` (rebuilt by `attack.py` case
`blobberish-arm`).

### F4 (calibration) `--profile v2` with the battery is *not* the v2 hole

`score()` applies clause-9 battery keys under both profiles. On the `substring-arm` fixture,
the naive control command

```sh
… --profile v2            (no --no-battery) → exit 1, stdout sha256 0127f30dabc371b7…,
                                            failing ["battery genuine_green 0 != 1"]
```

even though the same fixture is a clean v2 green (`v2_green 4`) inside the battery. Consequence
for the L1: `controls/ctl-c1-1-v2-profile.json` must be produced with `--no-battery`, or it will
record exit 1 and the "four holes measured" control will read as a failure of the claim.

### F5 (calibration, live edit) the earlier worktree draft would not have scored

Two worktree snapshots of `SKILL.md` existed while this seat ran:

| snapshot | arm cells | v2 | v3 |
|---|---|---|---|
| `sha256:25b12b19…` (earlier) | `symbol: the arm cell must equal one token…`, `once: …`, `digest: …`, `order: …` | 0 | **1** — `arm cells not exact vocabulary tokens` (all four) |
| `sha256:bf94d1b5…` (captured, used for every fixture here) | `` `symbol` ``, `` `once` ``, `` `digest` ``, `` `order` `` | 0 | 0 |

Receipt: fixture rev `66ca9b812e3c…`, v3 stdout sha256 `9e5d1bd87b6e476f…`, v3+battery 1
(`8aff54a8…` / v2). Both snapshots preserved: `fixtures/SKILL.draftA.25b12b19.md`,
`fixtures/SKILL.candidate.bf94d1b5.md`. The landing must be the bare-token form; the annotated
form is exactly the R46-CL2 defect the block describes.

### F6 (depth note) `duplicate-routed-id` cannot be isolated from clause 3 while v2 stays green

Five rows is what makes the class v2-green, and five rows also trips `rows != 4`, so v3's red
is `3` **and** `4`. Clause 4 does fire on its own arithmetic (`routed_counts {'R46-CL3': 2}`);
the isolated probe `cardinality-only` (four rows, `CL2` twice, `CL3` dropped) is red under v3
with `failing` = the cardinality clause **only** — but it is also red under v2 (`routed ids not
named by any row: ['R46-CL3']`), which is itself the proof that v2's arm is presence, not
count. Receipts: fixture rev `4537eb9c44de…`, v3 exit 1 stdout sha256 `57411fcad630f55a…`,
v2 exit 1 stdout sha256 `d7300dccc401e0f4…`.

## 4. Other controls (all green, i.e. the clause reads the defect and not the change)

| probe | v2 | v3 | note |
|---|---|---|---|
| `mutations-name-removed` (the word `flag-order-drift` deleted from prose) | 0 | 1 (`mutation names not stated`) | clause 6's second half is live |
| `digest-reorder` (same four names, reversed order) | 0 | 1 | the pin is order-bound, as the claims file says |
| `block-prose-control` (one prose word changed) | 0 | 0 | v3 is not "block changed" |
| `gate-comment-control` (a comment line appended to `gate.py`) | 0 | 0 | clause 7 is the literal, not a file hash |
| `block23-relabelled` (block 23's table relabelled `24. ` + the v3 marker) | 1 | 1 | the claims file's kill rule holds: clauses 2–6 all fire |

## 5. What the L1 should do with this

1. Land the block at `sha256:bf94d1b5…` (bare arm tokens). Do not land the annotated form (F5).
2. Expect, at the landing revision, `--profile v3` → exit 0 with
   `battery {4,4,0,1,0}` and `genuine_green 1`; anything else means the landed bytes differ
   from the candidate.
3. Produce `ctl-c1-1-v2-profile.json` with `--profile v2 --no-battery` (F4).
4. Do **not** claim R47-C1 as "no forgery passes". Claim "the four named classes are caught";
   F1 and F2 are two forgeries that pass the frozen clause set (arm-token permutation; citation
   vacuity), both `met_target true` under the full counting command. They belong in the round
   report's limits and as routed round-48 defects.
5. The claims file's kill-rule sentence for `blobberish` (F3) is not reproducible; the round's
   report should state the token that holds (`order-ish`), since the claims file is frozen.

## 6. Not run

* The real-counting command at a *landed* revision: the block is uncommitted at HEAD
  `3186f69b`, so `--rev HEAD` at the lane exits 1 (`marker_occurrences 0`, `rule_blocks 23`,
  fenced control `base-v3.json`, stdout sha256 `6530e91da56290f5…`, 2026-10-28T17:49:36Z).
  Every score in this report is at a one-commit scratch fixture, not at a landing.
* `--selftest` of `exact.py` and of any other counter (that is the verification seat's).
* No build, lint, test or formatter of the lane tree; no git mutation anywhere outside scratch
  fixtures; no commit, push or stage in the lane.

## 7. Reproduce

`attack.py` (copy in this directory, `sha256:fdd19c29676429ae…`) rebuilds every fixture from
`fixtures/SKILL.candidate.bf94d1b5.md` placed at `$S/gen/SKILL.candidate.md` and from
`git -C <lane> show 5017e1f7:<path>`, then re-runs all 14 cases:

```sh
S=/fast/scratch/hyaku/kaidoku-r47/C1Battery; mkdir -p "$S/gen"
cp .ufo/waves/round-47/w1/C1Battery/fixtures/SKILL.candidate.bf94d1b5.md "$S/gen/SKILL.candidate.md"
TMPDIR=$S HYAKU_SCRATCH=$S python3 -I -B .ufo/waves/round-47/w1/C1Battery/attack.py
```

Evidence index in this directory: `receipts/runs.json` (every run: cmd, exit, stdout sha256,
stdout bytes, UTC, receipt path), `receipts/fx-*-{v2,v3}-{nobat,bat}.json` (counter stdout per
run), `receipts/v2-with-battery-substring-arm.json`, `receipts/draftA.json`,
`receipts/harness-stdout.txt`, `receipts/manifest.txt` (UTC + sha256 of every receipt file),
`diffs/diff-<class>.{skill,gate}.diff` (byte-level isolation), `fixtures/SKILL.*.md`
(the exact `SKILL.md` bytes each row was scored on).

## Risks

* The lane `SKILL.md` was edited by another seat while this seat measured (F5 records both
  snapshots). All fixture scores are pinned to the captured bytes and their sha256; a later
  candidate must be re-scored rather than assumed equal.
* The `duplicate-routed-id` row's red is two clauses (F6); reading only `rows 5 != 4` would
  overstate what was demonstrated.
