# CR-3 — SCOPE-row / floor-unit map and the zero-locus attack (evidence index)

Seat CR-3 (critic, chain c2), wave `arc3-loop1-round2`, 2026-10-19.
Task: attack H3 — *is any SCOPE row legitimately zero-locus at HEAD (which would
make the floor a permanent false positive)?*

All measurements are keyed to a sha256 and a UTC time. Repo HEAD throughout:
`14b1682b1128d2e41085ebc79c9addeb8786d420`. Scoped files at HEAD:
PROVINCE.md 162 lines `d075a3c6…`, SKILL.md 371 lines `483b0eba…`,
SCORECARD.md 1417 lines `a7c72950…`.

## Answer, in one line

Yes: **four SCOPE rows are legitimately zero-locus at HEAD** (all DATED), so any
floor whose unit is a SCOPE row reads FAIL on an ordinary run forever; and
**SKILL.md carries zero current-ok *blocks***, so a per-file floor expressed in
the census's block unit has the same failure mode. The floor granularities that
survive at HEAD are, measured: corpus-level (blocks or dets), per-file
**detections**, per-file any-locus, and per-row restricted to CURRENT rows.

## Gate revision timeline (measured while this seat ran)

| sha256 (first 16) | when (UTC) | floor semantics | HEAD run |
|---|---|---|---|
| `6f1d19ff…` | pristine (mtime 07:18) | `g2_ok = n>0 or (all-clean)` (vacuous) | PASS exit 0 — H3 reproduces |
| `59975ae0…` | ~12:06 | in-flight | not run |
| `82fb807e…` | 12:07–12:09 | tree-level: `n_current_ok` **blocks** > 0 | PASS exit 0 |
| `076bd621…` | ~12:10 | in-flight | not run |
| `c95a5cf3…` | 12:10–12:12 | **per-file, BLOCK unit**: `floor[rec["file"]] += 1` | **FAIL exit 1**, `DECLARED ['BLIND-INSTRUMENT']`, `SKILL.md=0` ← claim-blocking revision |
| `df9ffdf9…` | 12:12 onward (landed; EX-16 `after-sha256.txt` re-derived 12:12:15Z, 601 lines) | per-file, **DETECTIONS** | PASS exit 0 |

The claim-blocking revision is captured in `receipts/live2-head.out` /
`live2-head.json` (fail) and the landed revision in `receipts/live3-head.out`
(pass). Both were run against the same HEAD tree; the tree did not move.

## Per-row map at HEAD (pristine gate `6f1d19ff…`)

Tool: `tools/map-rows.py` (imports the frozen instrument read-only; attributes
every detection to the SCOPE row owning its physical line). Receipt:
`receipts/row-map-head.json`. Baseline: verdict PASS, 6/9/2 loci,
17 blocks / 50 dets / 34 current-ok dets.

Zero-locus rows (4 of 20):

| row | class | non-blank lines | gate-bearing lines | needles present |
|---|---|---|---|---|
| PROVINCE.md 40-43 | DATED | 3 | 0 | none |
| SCORECARD.md 417-466 | DATED | 45 | 0 | one bare `6.5.0` prose token at `:463` (round record about e2e re-runs) |
| SCORECARD.md 467-502 | DATED | 31 | 0 | four bare `6.5.0` (`:467`, `:471`, `:496`, `:500`) |
| SCORECARD.md 769-855 | DATED | 83 | 8 | none |

All four are in bounds (max declared end per file 131/20/855 ≤ 162/371/1417),
carry their declared markers, and are needle-free or needle-inert: rows 417-466
and 467-502 hold bare `6.5.0` prose tokens whose enclosing units never match
`REA_GATE`, and `classify()` partitions on `REA_GATE` before it looks for
needles, so those tokens yield no locus. Row-level "non-emptiness" cannot be
defined so as to rescue a row floor: three of the four rows have no
gate-bearing line at all.

No file is zero-locus at HEAD, and no detection line falls outside a declared
row (`undeclared_assert_lines: []`).

## Cross-check against EX-14's map (landed 12:08Z)

`claims/c2/EX-14/scope-locus-map.md` — compared row by row with
`tools/map-rows.py`: **20/20 rows agree on blocks and dets, and the totals agree
(17 blocks / 50 dets / 34 current-ok dets)**; disposition mixes agree on every
row (0 mismatches). EX-14's §3/§4 tables and this seat's independent harness are
therefore two instruments reporting the same substrate.

Independent confirmation of EX-14's unit-trap table (their patch text §"Why the
obvious fix is wrong"), measured by this seat:

```
current-ok BLOCKS per file: {'PROVINCE.md': 1, 'SCORECARD.md': 4, 'SKILL.md': 0}
current-ok DETS   per file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}
```

## Floor-variant matrix at HEAD (pristine gate + one predicate each)

Tools: `tools/mkvariants.py` (sealed: asserts the source sha) generates the
variants; receipts `receipts/v-*-head.out`; fixture receipts `v-*-gut.out`,
`v-*-noskill.out`, `v-none-inj.out`.

| variant (unit of "scope") | HEAD | blind needles | SKILL absent | needles stripped from SKILL.md |
|---|:--:|:--:|:--:|:--:|
| row (any declared row ≥1 det) | **FAIL** (4 rows) | FAIL | FAIL | FAIL |
| CURRENT row only | PASS | FAIL | FAIL | FAIL |
| per-file, blocks | **FAIL** (SKILL.md=0) — measured live at revision `c95a5cf3…` | — | — | — |
| per-file, any loci | PASS | FAIL | PASS (rows absent = H1's class) | FAIL |
| corpus blocks > 0 | PASS | FAIL | PASS | PASS (hole) |
| corpus dets > 0 | PASS | FAIL | PASS | PASS (hole) |

## Live-gate receipts (landed revision `df9ffdf9…`, 601 lines)

```
$ python3 .ufo/gates/c1-census-v10.py --quiet          # HEAD, ordinary run
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit=0
   → receipts/live3-head.out

$ python3 live4-blind.py --root <repo>                  # PIN/VER/PTR neutered
G2 positive-assertion guard: SUSPECT (… 0, 0, 0; total loci=0)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL                                                        exit=1
   → receipts/live4-blind-head.out

$ python3 .ufo/gates/c1-census-v10.py --root root-gut --quiet   # SKILL needles stripped in place, 371 lines
G2 positive-assertion guard: SUSPECT (PROVINCE.md=17, SCORECARD.md=14, SKILL.md=0; total loci=15)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL                                                        exit=1
   → receipts/live3-root-gut.out

$ python3 .ufo/gates/c1-census-v10.py --root root-noskill --quiet
UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']
DECLARED FAIL CLASSES: ['UNREADABLE']
VERDICT: FAIL                                                        exit=1
   → receipts/live3-root-noskill.out
```

Claim-blocking revision, same command family, `c95a5cf3…`, 12:10Z:

```
$ python3 .ufo/gates/c1-census-v10.py --quiet          # HEAD, ordinary run
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      exit=1
   → receipts/live2-head.out (sha keyed in receipts/live2-head.json)
```

## Fixtures used (all scratch, none in the repo)

| fixture | construction | purpose |
|---|---|---|
| `root-inj` | `rea-agents@6.3.0` planted into SCORECARD.md:769-855 (DATED) and into SKILL.md:15 (CURRENT) | row functionality: zero-locus row still dates a planted pin (`historical`, block 780-781); CURRENT row still reads STALE |
| `root-gut` | SKILL.md 371 lines, all `rea-agents@x.y.z` and bare versions neutralized in place | file-level collapse without line-count change (keeps H1's truncation guard quiet) |
| `root-noskill` | SKILL.md absent | H1 interaction |
| `root-record` | SKILL.md needle-free **and** its two SCOPE rows re-keyed to DATED (marker `None`, scratch copy of the gate only) | pure-record file: last latent false-positive path of the per-file floor |

## Optional refinement, measured

`current_row_files = {r[0] for r in SCOPE if r[3] == "CURRENT"}`; restrict the
per-file det floor to files in that set.

| environment | landed floor (`df9ffdf9…`) | refined floor |
|---|:--:|:--:|
| HEAD | PASS | PASS (unchanged, 17/14/3) |
| SKILL needles stripped | FAIL | FAIL (class preserved) |
| `root-record` (all-DATED file) | **FAIL** (false positive, latent) | PASS |

Receipts: `receipts/live-refined-head.out`, `live-refined-gut.out`,
`live-record-record.out`, `live-refined-record-record.out`.

## Partial-needle blindness (independent check of EX-16's named residual)

Landed revision, one needle regex neutered at a time:

| neutered | exit | blocks | current-ok blocks | note |
|---|:--:|:--:|:--:|---|
| PIN | 0 PASS | 6/9/2 (unchanged) | 5 | VER still matches the version inside the pin — silent |
| VER | 1 FAIL | 3/3/2 | 4 | fails, but on a spurious STALE not on the floor |
| PTR | 0 PASS | 6/9/2 (unchanged) | 5 | pointers are consulted only `if not occ` |

Receipts: `receipts/live-nop-{PIN,VER,PTR}.out`. The floor buys detection of the
*total* blind class only; the residual is H4/self-certification as named.
