# ConnectorCross — r66 w1 (scoped report)

Seat: leaf connector, read-only. Detail and the full hit list:
`.ufo/waves/round-66/w1/ConnectorCross/overlap.md`. No sibling tool executed, no sibling
file written, no scratch dir created.

## Findings

- **F1 — no sibling owns R66-C1's surface.** Fleet-wide token scan outside this lane:
  `count_ok` 0 hits, `len(CLOSURE)`/`CLOSURE =` 0 hits (only tameshi's `DISCLOSURE`),
  `skip-run` 0 hits. The 30-entry `CLOSURE` is this lane's toolchain map (3 d8 builds +
  `View8` + 4 venv entries + `inputs/atom.compiled.dist.jsc`) pinned to the r65 instrument;
  the count assertion is unowned outside kaidoku.
- **F2 — R66-C2's recipe reproduction is this lane's own.** `grep -rIln 'Measurement recipes'`
  over sibling `tools/`+`scripts/` returns nothing; the banner `**A - source-derived
  controls.**` and the heredoc extractor exist only here. mado's heredoc work
  (`mado-tripwire.py:336-341`) is shell syntax; tameshi's (`bash-witness-study.py:299-303`)
  is its own runner spec.
- **F3 — the self-assessment **class** is owned three times over; the atoms are not.**
  tsukuroi `tools/check-self-assessment.py:2,42-43` is a generic `--repo` self-assessment
  mismatch counter (27 checks, `mismatches`, exit 0/1/2) but requires a `## Axes - ` heading
  (`:15,461-472`) and `SHONEN.md` — kaidoku `SCORECARD.md` has neither (`## Owned axes` at
  `:19`), so it exits 2 here. souji `tools/souji-capability-agreement.py:3-22` counts
  stated-literal vs command mismatches from a foreign preregistration TSV;
  `tools/souji-declared-evidence.py:7-19` re-derives SCORECARD path/rev/sha256 assertions
  (`assertions=… mismatches=M`). Neither computes a knowledge fraction or a rounded score.
  The two R66-C2 atoms (`round(10*mapped/files,2)`; the cited `<mapped>/<files>`) have no
  sibling implementation.
- **F4 — nearest count-gate neighbours are adjacent, not duplicate.** tameshi
  `tools/count-recheck.py:3-24` verifies a *printed* count against `git grep -c` at a named
  rev — a different form from a manifest-length constant; kumitate
  `scripts/counter-pins.mjs:1-25` asserts sha256 identity over its own pinned paths and only
  *prints* `pins=<n>`; kama `round69-newest-closure-counter.py` checks closure *pointer
  currency*, not cardinality.
- **F5 — uncited class.** This lane's `SKILL.md` cites neither souji nor tsukuroi
  (`grep -i 'souji\|tsukuroi' SKILL.md` → no matches), while the r65 closure already
  recorded souji as owning the coverage-map class (`corpus/lessons/round-65.md:60`). Any
  novelty sentence for C2 must cite the class precedent or drop the claim.

## Ownership boundary

| surface | verdict |
|---|---|
| (a) superseded / committed measurement-recipe reproduction | **kaidoku-owned** — recipe lives in this lane's SCORECARD, population is this lane's `corpus/knowledge` at a revision |
| (b) closure-count assertion gate | **kaidoku-owned** — `CLOSURE` is the lane toolchain manifest; no fleet `count_ok` or closure constant |
| (c) self-assessment atom/mismatch counter | **class shared** (tsukuroi, souji, kama r58/r69), **atoms lane-local** — report the class, do not absorb or claim it |

**Report, not absorb:** to souji, the coverage-fraction atom is a natural TSV row for
`souji-capability-agreement.py`; to tameshi, `count_ok` is a printed-count form outside
`count-recheck.py`'s `git grep -c` scope; to tsukuroi, the `mismatches`/exit-0-1-2 vocabulary
duplicates `check-self-assessment.py` but the checkers cannot merge on this lane's SCORECARD.

**Risk stated:** three lanes print `mismatches` over three populations with three exit maps;
receipts should name their atom population inline to prevent cross-lane mis-reads.

## Commands run (all read-only, cwd `/home/vgpnk/Projects/shokunin`)

1. seeded `grep -rIl --include='*.py' -e dont_write_bytecode -e closure -e count_ok -e mismatches …`
   → 215 files; census `kaidoku 56 | tsukuroi 43 | kama 43 | kotodama 21 | tameshi 16 | souji 14 | mori 10 | kake 8 | mado 3 | chousa 1`.
2. token narrowing `count_ok` / `recipe_a` / `skip-run` → 0 sibling hits each; `CLOSURE` → 0.
3. `grep -rIln 'Measurement recipes'` → only `tools/round-66/coverage-selfcheck.py`.
4. `grep -n 'add_argument'` + heading prerequisites for tsukuroi/souji CLIs (line refs above).
5. `sha256sum tools/round-66/{closure-boundary,coverage-selfcheck}.py` →
   `3c5cfb03…d071045b` / `1be9d046…86555aa` (match claims.json).
6. `/fast/scratch/hyaku/kaidoku-r66/` inspected: no `ConnectorCross/` (nothing to delete).
