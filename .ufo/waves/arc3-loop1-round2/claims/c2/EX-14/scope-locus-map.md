# SCOPE-locus map — expected locus count per scoped file/row under the H3 floor

Seat **EX-14** (executor, chain **c2**), wave `arc3-loop1-round2`, 2026-10-19.
Artifact of the seat task: *classify every scoped file in the SCOPE table by
expected locus count under the H3 floor; which scopes are non-empty by design;
is any scope legitimately zero-locus* (CR-3 will attack this).

Instrument measured: `.ufo/gates/c1-census-v10.py`
sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`
(the round-1 patch texts named `36e96cd5…` — that hash predates the E22 re-key
that landed at HEAD; the sha256 above is the live pre-round-2 bytes, unchanged
by this seat). Repo HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420`.
Scoped files at HEAD: `PROVINCE.md` 162 lines sha256 `d075a3c6…`,
`SKILL.md` 371 lines sha256 `483b0eba…`, `SCORECARD.md` 1417 lines
sha256 `a7c72950…`. This seat wrote no file in the repo except its own report
and this claims directory; the census was copied to `/var/tmp/ex14/` and all
mutations were made on the copy.

## 1. Method

Read-only attribution harness on a scratch copy of the census
(`/var/tmp/ex14/scope_map.py`, `floor_probe.py`, `partial.py`, `run_all.sh` —
copied into this directory):

- invoke `classify()` exactly as `main()` does, then attribute every **det**
  to the SCOPE row owning its primary physical line, and every **block/locus**
  to the row owning its first det line;
- count per row: blocks (the census's `loci` unit), dets (assertions), disp mix,
  kinds, and *gate-only lines* (lines matching `REA_GATE` that produced no det);
- evaluate six candidate H3 floor predicates (see §5) in four environments:
  `head`, `blind` (needles neutered, CR-5's H3 injection), `skilly`
  (SKILL.md absent, RV-11's H1 injection), `nullskill` (SKILL.md present but
  needle-free, a new fixture of this seat).

## 2. Baseline at HEAD

```
$ python3 .ufo/gates/c1-census-v10.py --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

17 blocks / 50 dets, of which **34 dets are current-ok**:
PROVINCE 17, SCORECARD 14, SKILL 3 (`floor-probe.out`, env `head`).

## 3. The map — 20 rows, expected occupancy

Occupancy is not uniform: 16 rows carry loci, **4 rows carry none**.

| # | row | class | blocks | dets | disp mix | occupancy class |
|---|-----|-------|-------:|-----:|----------|-----------------|
| 0 | PROVINCE.md 8-13 | CURRENT | 1 | 3 | cur-ok 2, hist 1 | locus-bearing |
| 1 | PROVINCE.md 15-26 | CURRENT | 1 | 11 | cur-ok 10, hist 1 | locus-bearing (largest) |
| 2 | PROVINCE.md 40-43 | DATED | **0** | **0** | — | **zero by design — structural** |
| 3 | PROVINCE.md 44-44 | CURRENT | 1 | 3 | cur-ok 3 | locus-bearing |
| 4 | PROVINCE.md 45-62 | DATED | 1 | 5 | cur-ok 2, hist 3 | locus-bearing |
| 5 | PROVINCE.md 64-71 | CURRENT | 1 | 1 | hist 1 | locus-bearing, no current-ok |
| 6 | PROVINCE.md 119-131 | DATED | 1 | 1 | hist 1 | locus-bearing |
| 7 | SKILL.md 10-16 | CURRENT | 1 | 1 | hist 1 | locus-bearing, no current-ok |
| 8 | SKILL.md 18-20 | CURRENT | 1 | 4 | cur-ok 3, hist 1 | locus-bearing |
| 9 | SCORECARD.md 56-60 | CURRENT | 1 | 6 | cur-ok 4, hist 2 | locus-bearing |
| 10 | SCORECARD.md 273-326 | DATED | 1 | 2 | cur-ok 1, hist 1 | locus-bearing (thinnest DATED span, 54 lines) |
| 11 | SCORECARD.md 417-466 | DATED | **0** | **0** | — | **zero by design — latent (needle, no gate)** |
| 12 | SCORECARD.md 467-502 | DATED | **0** | **0** | — | **zero by design — latent (needle, no gate)** |
| 13 | SCORECARD.md 503-533 | DATED | 1 | 3 | hist 2, cur-ok 1 | locus-bearing |
| 14 | SCORECARD.md 534-560 | DATED | 1 | 1 | hist 1 | locus-bearing |
| 15 | SCORECARD.md 619-619 | DATED | 1 | 1 | cur-ok 1 | locus-bearing |
| 16 | SCORECARD.md 620-620 | DATED | 1 | 1 | hist 1 | locus-bearing |
| 17 | SCORECARD.md 636-702 | DATED | 1 | 1 | cur-ok 1 | locus-bearing |
| 18 | SCORECARD.md 703-768 | DATED | 2 | 6 | cur-ok 6 | locus-bearing |
| 19 | SCORECARD.md 769-855 | DATED | **0** | **0** | — | **zero by design — latent (gate, no needle)** |

Block/det detail with line numbers and values: `row-inventory.txt` (verbatim
instrument attribution, e.g. row 18 = blocks 732-738 and 748-767).

**Answer to the frozen question: yes — a scope is legitimately zero-locus, four
of them, and all four are DATED rows.** Reasons are structural, not incidental:

- **row 2 (PROVINCE.md 40-43)** — *gate-free and needle-free*. The row is a
  table header (`:40` "Surfaces owned now — each verified on this host
  2026-10-13.", `:42`/`:43` column headers). Zero `REA_GATE` lines, zero
  `PIN`/`VER`/`PTR` matches. No instrument edit short of a gate-vocabulary
  change can ever populate it (`zero-rows-gate-scan.txt`).
- **rows 11, 12 (SCORECARD.md 417-466, 467-502)** — *needle-bearing but
  gate-free*. `VER` matches exist (`:463` `6.5.0`; `:467` `6.5.0`, `:471`
  `6.5.0`, `:496` `6.5.0`, `:500` `6.5.0`) but every enclosing unit is
  gate-silent, and `classify()` partitions on `REA_GATE` first, so these
  needles yield no locus (unit `453-465`, `467-467`, `469-473`, `495-501`,
  all `gate=False`; `zero-row-blocks.txt`). This is the "round-record prose
  about 6.5.0 without naming a client surface" shape.
- **row 19 (SCORECARD.md 769-855)** — *gate-bearing but needle-free*. Eight
  lines carry gate vocabulary (`:778`, `:785`, `:804`, `:813`, `:821`, `:824`,
  `:825`, `:832` — e.g. `config.toml line-numbers are unpinnable`, custody
  prose) yet contain no version/pin/pointer needle. Latent: a widened needle
  vocabulary (G4-class change) or an added `path:line` in that prose would
  create loci here; a widened `REA_GATE` would do it for rows 11/12.

**File level: no file is zero-locus at HEAD** (6/9/2). But a file *can* go
zero-locus while remaining gate-clean and readable: fixture `nullskill`
(needles stripped from SKILL.md:10-20, everything else byte-identical) reads
`SKILL.md lines=371 loci=0` and PASS exit 0 (`receipts-atk-nullskill-v10.out`).
SKILL.md is the thinnest scope — 2 blocks, 4 dets, all in two CURRENT rows —
so it is the file where a zero-locus collapse would first appear silently.

## 4. Non-empty-by-design scopes (the floor's legitimate anchors)

The floor "must not fire" set and its current margin:

| scope | blocks | current-ok dets | current-ok rows | margin over a >=1 floor |
|-------|-------:|----------------:|----------------:|-------------------------|
| PROVINCE.md | 6 | 17 | 4 of 7 rows | 17x |
| SCORECARD.md | 9 | 14 | 6 of 10 rows | 14x |
| SKILL.md | 2 | 3 | 1 of 2 rows | 3x (**thinnest**) |

Per-row margins are *not* uniform and must not be assumed: rows 5, 6, 7, 14,
16 carry **no current-ok det** (historical only), and rows 2, 11, 12, 19 carry
nothing at all. A floor expressed at row granularity therefore has 4
structural false positives at HEAD (§5, variants D/F).

## 5. Floor-variant matrix (the measured decision table)

Six candidate predicates, each evaluated in four environments. `PASS` means
"the predicate is satisfied" — desired at `head`, undesired at `blind`:

| variant | predicate | head | blind | skilly | nullskill |
|---------|-----------|:----:|:-----:|:------:|:---------:|
| A | global `current-ok` dets > 0 (CR-5's minimal patch) | PASS | FAIL | **PASS** | **PASS** |
| B | per **readable** scoped file `current-ok` dets > 0 | PASS | FAIL | PASS | **FAIL** |
| B2 | per scoped file incl. unreadable | PASS | FAIL | FAIL | FAIL |
| C | global blocks (loci) > 0 | PASS | FAIL | **PASS** | **PASS** |
| D | per row >= 1 det (any disp) | **FAIL** | FAIL | FAIL | FAIL |
| E | per CURRENT row >= 1 det | PASS | FAIL | FAIL | FAIL |
| F | per row >= 1 `current-ok` det | **FAIL** | FAIL | FAIL | FAIL |

Receipts: `floor-probe.out` (all four envs), `run-all.sh` +
`receipts-*.out` (end-to-end exit codes on the real `main()`).

Findings, each with its measurement:

1. **Per-row floors are refuted** (D, F): they FAIL on an ordinary HEAD run
   because of the four legitimately empty DATED rows of §3. D additionally
   fails the moment any row is legitimately empty; F also fails rows 5/6/7/14/16
   (historical-only). Neither may be shipped.
2. **Variant E passes HEAD but conflates classes**: it reports an absent or
   emptied file as "empty scope" (`skilly`, `nullskill` FAIL) rather than as
   the declared unreadable/emptied class, and it would false-FAIL the ordinary
   run if the two SKILL.md rows were ever rewritten to version-free prose.
3. **A floor alone never catches an absent scoped file.** With SKILL.md absent,
   A and C still PASS (`skilly`: 45 dets, 31 current-ok survive from the other
   two files); the end-to-end receipt shows `atk-missing-v11floorA` → PASS
   exit 0. H1's unreadable guard is therefore *not* subsumed by H3 — the two
   patch texts close different holes and both are needed.
4. **A alone (CR-5's minimal patch) does not catch an emptied file**: the
   `nullskill` fixture reads PASS under A. B closes it; B is equivalent to A on
   `head`/`blind`/`skilly` and strictly stronger on `nullskill`, so **B
   dominates A on every environment measured**. B's correctness on `skilly`
   depends on treating unreadable files as out of floor scope — which is
   exactly right *only* when the H1 guard separately declares them, i.e. B+H1
   is the closed pair; B alone would let a deleted file pass (it exempts
   itself), and A/B2-inclusive do worse (B2 loses the readable/unreadable
   distinction the H1 class exists to report).
5. **The floor is a token floor, not a coverage floor.** `blind` at 0 dets
   trips it, but any run retaining >=1 current-ok det clears it: the `VER`-only
   neuter fixture drops 17 blocks -> 8 and 34 current-ok -> 12 and still
   satisfies A (`partial-neuter.out`; end-to-end it exits 1, but on a spurious
   `STALE`, not on the floor). Expect CR-3 to attack precisely this: the floor
   buys detection of the *total* blind class only, and the claim text should be
   read that way.

## 6. Recommended floor text (for EX-16, patch text only)

In `main()`, replacing the vacuous second disjunct of `g2_ok`, and scoping the
floor to readable files so that absence stays H1's class:

```python
# H3 positive floor: every readable scoped file must contribute at least one
# current-ok assertion.  Unreadable files are the H1 class and are exempt here
# (they already force FAIL via `unreadable`); empty-because-needle-free is NOT
# exempt -- that is the coverage collapse this floor exists to catch.
floor = {f: 0 for f in files}
for rec in out.get("current-ok", []):
    floor[rec["file"]] += 1
h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
g2_ok = h3_ok          # replaces: ... > 0 or (not stale and not unatt and not undecl and not unres)
```

with the report line carrying the substrate so the number is auditable, e.g.
`G2 positive-assertion guard: ok (current-ok per file: PROVINCE.md=17
SCORECARD.md=14 SKILL.md=3)`. Full patch text: `proposed-h3-floor-scoping.patch.md`
in this directory. **This seat is not the implementer; nothing here is applied.**

## 7. Scope-bounds invariance (creep audit)

This map proposes **no** change to `SCOPE`: all 20 rows keep their exact
bounds, class, marker line and marker regex. The four zero-locus rows are
zero *by measurement*, and the correct response is a floor that tolerates them,
**not** a re-key that excludes them — excluding them would be the r4 laundering
path (a locus planted inside rows 11/12/19 would then read UNDECLARED -> FAIL,
which is the intended behaviour). Creep check for the round's certificate: at
HEAD blocks are 6/9/2 and the map's per-row inventory (`row-inventory.txt`)
is the invariance baseline for EX-28's `scope-diff.py` audit of the v11 diff —
no row added, no DATED bound widened, no CURRENT->DATED flip, no open-ended
bound.

## 8. Attacks attempted (adversarial checks of these findings)

| attack | setup | result | verdict |
|--------|-------|--------|---------|
| Per-row floor false positive | evaluate D/F at HEAD | both FAIL on 4 DATED rows (blocks=0, no gate lines) | **refutes per-row floors** |
| Floor vs absent file | `skilly` + end-to-end v11-floorA | A/B/C PASS, exit 0 | **floor alone insufficient; H1 required** |
| Floor vs emptied file | `nullskill` (new fixture) | A/C PASS; B FAIL | **B needed for this class** |
| Floor vs partial blind | `ver-neutered` | 17->8 blocks, 34->12 cur-ok, floor A satisfied; exit 1 only via a spurious STALE | **floor is not an invariance check — named residual** |
| Floor vs total blind | `all-neutered` v11 floorA | `G2 … SUSPECT`, FAIL exit 1 | **H3 closes the round-1 injection class** |
| Zero-locus row promoted | needle-strip PROVINCE rows 0/1/4/5/6 | block 15-26 ptr fallback runs, exposes `PROVINCE.md:18 -> ~/.kimi-code/config.toml:3298` as STALE ("line holds no rea-agents pin") | **found dormant coverage gap (§9), not a floor defect** |

Structural self-check on this artifact: the attribution harness never writes to
the repo, the census bytes were re-hashed after the runs (same sha256), and the
four "zero by design" claims are each backed by a line-level scan
(`zero-rows-gate-scan.txt`, `zero-row-blocks.txt`), not by inference.

## 9. Named residuals / newly surfaced debt (for the chain, not fixed here)

- **R1 — ptr fallback is unreachable behind version occurrences.** In
  `classify()`, `PTR` is evaluated only `if not occ`. Blocks that carry a
  version occurrence never resolve their pointers. Measured consequence: at
  HEAD, PROVINCE.md block 15-26 holds three pointer claims (`:16`, `:17`, `:18`)
  that are *never checked*; when the fixture promotes the fallback, `:18`
  (`~/.kimi-code/config.toml:3298`) reads STALE — the line now holds
  `[models."github-copilot/gpt-6-luna"]`. This is visible only under a
  scope-composition change; it is out of H3's minimal scope but is real debt
  for the next instrument round. (The custody path itself was **not** opened by
  this seat — the quoted line is the instrument's own `ptr_check` output.)
- **R2 — floor coarseness**: §5.5. Detection of the blind class does not imply
  detection of *narrowed* detection; only the external diff audit
  (`scope-diff.py`) plus the per-row baseline of §3 covers that.
- **R3 — SKILL.md margin is 3.** The thinnest file is also the one whose
  absence H1 exists for; any future per-file floor should carry SKILL.md's
  expected occupancy explicitly (rows 10-16 and 18-20), so a collapse to
  0 loci is a declared FAIL rather than a silent PASS.

## 11. Live v11 verification (added 2026-10-19, after EX-16's write landed)

Mid-seat, `.ufo/gates/c1-census-v10.py` changed under this seat: sha256
`6f1d19ff…` (the bytes measured in §§1-9) -> **`82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`**,
mtime 2026-10-19 09:06:50, +145 diff lines (`live-v11.diff`, `census-live-v11.py`).
The landed patch is EX-16's v11: H1 as an `unreadable` class (OSError **and**
`len(lines) < declared max_end`), H3 as `g2_ok = n_current_ok > 0` (floor = 1,
tree-level), plus a `declared_fail_classes` report/JSON field. **No SCOPE row
was touched** — the round-1 differ confirms independently:

```
$ python3 scope-diff.py census.py census-live-v11.py
rows before=20 after=20  ADDED (0):  REMOVED (0):  CHANGED (0):  CREEP FLAGS: []
exit=0
```

and per-row occupancy is byte-identical across the edit (blocks/dets/disps,
all 20 rows; `scope-map-live.json` vs `scope-map.json`).

End-to-end matrix on the live bytes (`live-matrix.out`, `receipts-live-*.out`):

| environment | verdict | exit | declared classes | G2 line |
|-------------|---------|------|------------------|---------|
| head | PASS | 0 | `[]` | ok (current-ok loci=5, total loci=17, floor=1) |
| `atk-missing` (SKILL.md absent) | FAIL | 1 | `['UNREADABLE']` | ok (5/15) |
| `atk-blind-all` (needles neutered) | FAIL | 1 | `['BLIND-INSTRUMENT']` | SUSPECT (0/0) |
| `atk-shrunk` | FAIL | 1 | `[]` | ok (5/13) — fails on the dormant `STALE` of §9/R1 |
| `atk-nullskill` (present, needle-free SKILL.md) | **PASS** | **0** | `[]` | ok (5/15) |

So both round-1 holes are closed on the landed bytes, and **the nullskill gap
survives the landed patch** — the residual the map predicted in §5.4.

**Why the floor cannot simply be made per-file in its own unit.** The landed
floor counts `len(out["current-ok"])`, i.e. **blocks whose disposition is
current-ok**, and per file that is:

| file | current-ok **blocks** (landed unit) | current-ok **dets** (assertions) |
|------|-----------------------------------:|---------------------------------:|
| PROVINCE.md | 1 | 17 |
| SCORECARD.md | 4 | 14 |
| **SKILL.md** | **0** | **3** |

SKILL.md's two blocks are *mixed*-disposition (`block 10-16` historical only;
`block 18-20` = 3 current-ok + 1 historical -> disp `info`), so a per-file floor
in the landed unit would **false-FAIL at HEAD**; the same predicate in the det
unit passes. This is a hard constraint on any CR-3 proposal to "scope the floor
per file": it must change the unit (dets, or per-file `current-ok` assertions),
not merely the aggregation. If the round keeps the tree-level floor, the claim
text's "zero loci in a non-empty **scope**" must be read tree-level, and the
nullskill residual belongs in the named-residual list next to H4 — it is the
same class (only the external locus-count audit sees it).

## 11b. Second landed revision: the unit trap fired in production (2026-10-19 09:10:56)

The target moved again while this seat was writing: `c1-census-v10.py` sha256
`82fb807e…` -> **`c95a5cf30201a1f862849b04701330e65b3777c877fb9467e4ee38656bbb0d4f`**
(mtime 09:10:56, `census-live-v11b.py`; its docstring adopts this map's variant
B and credits it). The revision lands the per-file floor **in the block unit** —
`for rec in out.get("current-ok", []): floor[rec["file"]] += 1` — which is
exactly "Trap 1" of `proposed-h3-floor-scoping.patch.md`, now firing end-to-end
on a clean tree (`v11b-matrix.out`, `receipts-v11b-*.out`):

```
$ python3 census-live-v11b.py --root <repo HEAD>
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=1
```

**A clean HEAD fails**, violating the frozen C2 acceptance clause "ordinary
runs at HEAD stay PASS 0/0/0/0". The map's own per-file table (§11) is the
explanation: SKILL.md has 0 current-ok **blocks** and 3 current-ok
**assertions**. A drop-in fix (sweep every disposition, count dets, skip the
string-valued `g11`/`g7` keys) is verified on a scratch copy
(`census-live-v11c-fix.py`, sha256 `bed3b02e…`): head PASS exit 0 with per-file
17/14/3, `atk-missing` FAIL `UNREADABLE`, `atk-nullskill` FAIL
`BLIND-INSTRUMENT`, `atk-shrunk` FAIL (stale) with no spurious class
(`v11c-matrix.out`, `receipts-v11c-*.out`). Patch text:
`proposed-v11b-floor-unit-fix.patch.md`. This seat did not apply it.

## 11c. Third landed revision: unit fixed, HEAD green (2026-10-19 09:11:50)

`c95a5cf3…` -> **`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43`**
(mtime 09:11:50, `census-live-v11d.py`). The floor now counts **current-ok
assertions per readable file** (the block-unit sweep replaced by an
`isinstance`-guarded sweep, dets counted, `n_current_ok` re-based to dets).
Measured on those bytes (`v11d-matrix.out`, `receipts-v11d-*.out`):

| environment | verdict | exit | per-file / classes |
|-------------|---------|------|--------------------|
| head | PASS | 0 | `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`; `[]` |
| `atk-missing` | FAIL | 1 | SKILL.md=0 exempt as unreadable; `['UNREADABLE']` |
| `atk-nullskill` | FAIL | 1 | SKILL.md=0; `['BLIND-INSTRUMENT']` |
| `atk-shrunk` | FAIL | 1 | stale=1; `[]` (no spurious class) |

This agrees with this seat's independently verified fix on every verdict and
count (`v11c-matrix.out` vs `v11d-matrix.out`), so the blocking defect of §11b
is closed. Residual (cosmetic, worth wording around in the landing receipt):
the G2 line says "loci" for two different units in one sentence — per-file
numbers are **assertions**, `total loci` is **blocks**.

## 12. Evidence index (this directory)

| file | content |
|------|---------|
| `scope-locus-map.md` | this artifact |
| `proposed-h3-floor-scoping.patch.md` | optional per-file strengthening in the det unit, verified (not applied) |
| `proposed-v11b-floor-unit-fix.patch.md` | drop-in fix for the v11b block-unit bug (historically blocking; superseded by v11d) |
| `v11b-matrix.out`, `v11c-matrix.out`, `v11d-matrix.out` + `receipts-v11{b,c,d}-*.out` | end-to-end evidence: v11b red at HEAD, fix green, v11d green (shipped state) |
| `census-live-v11b.py`, `census-live-v11c-fix.py`, `census-live-v11d.py` | the three captured revisions (live bytes + verified fix) |
| `row-inventory.txt` | per-row block/det attribution at HEAD, with values |
| `zero-rows-gate-scan.txt` | line-level gate/needle scan of the 4 empty rows |
| `zero-row-blocks.txt` | enclosing unit + `REA_GATE` status for the needle-bearing empty rows |
| `floor-probe.out` | variants A–F x 4 environments (pre-edit bytes) |
| `partial-neuter.out` | per-needle neuter matrix (PIN/VER/PTR, 8 combinations) |
| `run-all.out` + `receipts-*.out` | end-to-end `main()` exit codes, 8 configurations, pre-edit bytes |
| `live-matrix.out` + `receipts-live-*.out` | end-to-end matrix on the **landed** v11 bytes |
| `live-floor-units.txt` | per-file floor-unit table (blocks vs dets) on landed bytes |
| `live-v11.diff`, `census-live-v11.py` | the landed edit, captured + hashed |
| `scope-map.json`, `scope-map-live.json` | per-row attribution pre-edit vs landed (invariance check) |
| `head-hashes.txt` | sha256 of census + the three scoped files |
| `scope_map.py`, `floor_probe.py`, `partial.py`, `run_all.sh`, `run_live.sh`, `scope-diff.py` | harness + round-1 differ (scratch copies, repo-untouched) |
