# Round 65 claims — kaidoku-shokunin (attempt 1)

Base: `c99e907cb5576c13a7b22755d776b356fdfc1752` (the round-64 verifier spot-check
commit). Owned axes: coverage, depth, calibration (all at 10.0; the stagnation nudge
is not fired: window N=10, last capability entered round 63). Two claims, distinct
axes, causally separable. No fresh-start binding: of the last three closures, r62 and
r63 were admitted and r64 stopped honestly on its own predicate (not a rejected
closure); the fresh-start rule (three rejected closures in a row) is not triggered.

Instruments are committed BEFORE this file (`tools/round-65/jsc-closure-matrix.py`,
`tools/round-65/coverage-recipe.py`) — the QUALITY #33 order — and pinned by sha256 in
the claims container. Each was dry-run end to end on development inputs before the
freeze (QUALITY #83/#84).

## R65-C1 — depth, capability acquisition: the `.jsc` route under a complete closure

Round 64 reproduced the 18/18 label matrix but stopped honestly: its frozen clause
"every input and binary sha256 equal to its pin" could not be certified (round-64
non-author review F1: D2/D3 `snapshot_blob.bin`, `icudtl.dat` variants and the
transitive View8 tree unpinned; F2: the View8 run wrote `__pycache__` into the frozen
toolchain). This claim repairs the closure — every file the run reads and every
executable it spawns is pinned, the tree must start cache-free, every subprocess runs
with bytecode writes disabled, and a census proves the run wrote nothing — then
re-runs the same frozen predictions under it.

Predicate (byte-identical in `.ufo/waves/round-65/claims.json`, the counter constant
and every receipt):

> R65-C1 is verified iff (i) the frozen closure manifest matches every one of its
> entries (count and sha256) with no Python bytecode cache present before the first
> run, (ii) all 18 runs reproduce the frozen predicted label of their cell
> (dump|view8|check), and (iii) the after-run toolchain census equals the before-run
> census.

Counter: `tools/round-65/jsc-closure-matrix.py --probe .ufo/waves/round-64/inputs/probe-electron.jsc --work <scratch> --out <receipt>`.
Exit 0 verified / 1 not verified / 2 could-not-evaluate.

Closure (30 pinned entries): the three d8 builds (`d8`, `snapshot_blob.bin`,
`icudtl.dat` each — 9), the 12 files under `jsc2js-src/View8/` (the whole import
closure), the venv identity (`parse/__init__.py`, `parse/__init__.pyi`, dist-info
`METADATA`+`RECORD`, `pyvenv.cfg`), the Typora artifact, the Electron probe artifact,
the resolved `node` binary and the resolved venv interpreter. Census: every regular
file under the toolchain root except `jsc2js-src/.git/`.

Kill rule: any closure finding, any label mismatch, an unequal census, or a run that
needs an instrument edit after the freeze → the claim is not verified; report the
stop, never re-predict. A missing tool or input → could-not-evaluate, not a pass.

Before-arm: `--skip-run` (the do-nothing control: 0/18, exit 1) plus the record of the
r64 stop (its `matrix-run.json` reproduced 18/18 under the OLD, incomplete closure).
After-arm: the frozen matrix run under the new closure.

Controls that must fail before data (QUALITY #48/#67/#72): (1) the do-nothing
`--skip-run` → 0/18 exit 1; (2) a scratch toolchain copy with one pinned byte flipped
→ manifest exit 2 naming the path; (3) a scratch copy with one `__pycache__` file
added → manifest exit 2 naming the cache; (4) two censuses of the same tree → exit 0,
one census pair with an added file → exit 1; (5) the matrix's own selftest must run its
outer CLI on green and red fixtures (34 cases).

Sourced claim: the closure's bytecode-write clause cites S266 (Python documentation,
`-B` / `PYTHONDONTWRITEBYTECODE`) opened this round; the knowledge entry
`corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md` cites the row.

## R65-C2 — calibration, capability: the coverage recipe stops hiding files

The r1-era command-A recipe derives both sides of the coverage fraction from the same
`2026-10-\d{2}-` token filter, so a knowledge file whose name is not October-dated
leaves the denominator silently and the recipe still prints a perfect score. Round 64
named the defect and left the recipe unrepaired; at this base the tree holds 144
knowledge files and command A assesses 142. The repaired recipe keys on file stems
over the full blob list and reports the old recipe's blind spot as a count.

Predicate (byte-identical in the claims container, the counter constant and the
receipts):

> R65-C2 is verified iff the repaired stem-keyed recipe reports, over the repository
> at the measured revision, `mismatches == 0` with `mapped > 0`, while the superseded
> date-limited recipe on the same revision reports a non-zero
> `population_dropped` naming the files it hides.

Counter: `tools/round-65/coverage-recipe.py --root <lane> --rev <rev> --recipe stem` (after)
and `--recipe date` (before). `mismatches = missing + dangling + population_dropped`;
exit 0 clean / 1 any mismatch / 2 could-not-evaluate.

Kill rule: a stem run with any missing, dangling or dropped file, or a date run that
does not drop the November-named files, fails the claim; a zero-file tree or a missing
coverage-map section is could-not-evaluate, never clean.

Before-arm: `--recipe date` at the base — population 142/144, `population_dropped` 2
(`jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`), mismatches 2, exit 1.
After-arm: `--recipe stem` at the same base — 144/144, mismatches 0, exit 0 — and the
SCORECARD coverage row gains the repaired command as its current-tree measurement
(the historical round-53 measurement stays, dated).

Controls before data: the do-nothing case is the unchanged date recipe (exit 1, 2
dropped); a junk-row fixture (a `knowledge/2026-10-09-ghost` token with no file) must
go red; a non-dated map token must still map its file; a map section with no dated
tokens must not be reported clean. The instrument's selftest runs the outer CLI over
28 cases including these.

## Frontier step (not a third claim)

- `corpus/SOURCES.md`: one row opened this round (S266, Python documentation for `-B`
  and `PYTHONDONTWRITEBYTECODE`), with the Gate recording URL, access date and a
  ≤25-word located quote; census before → after with exit codes.
- One mistake mined into `corpus/lessons/round-65.md` `## Mistakes` with a red
  demonstration.
- Assimilation: none this round — the `merge/kaidoku/` jsc theme was adopted in round
  64 (entries `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`); no other
  staged theme fits these claims, and a bulk append is refused by CORPUS.md rule 4.

## Round shape

One v1 wave, 12 seats (policy band 8–16), attack seats reviewer + critic + 2
mutation-testers = 4/12 (33% ≥ 25%), one connector, three executors, two scribes, one
scout, one sentinel. L1 holds the planner seat (validator rejects a planner role).
Seat outputs land under `.ufo/waves/round-65/w1/<seat>/`; the L1 integrates and lands.
