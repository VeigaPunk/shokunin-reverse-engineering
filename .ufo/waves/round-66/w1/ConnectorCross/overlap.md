# ConnectorCross — sibling-overlap scan (r66 w1)

Seat: leaf connector. Read-only sweep over `/home/vgpnk/Projects/shokunin/*-shokunin`
except this lane. No sibling tool was executed; no sibling file written; no clone, copy or
fixture was made (no scratch dir created; `/fast/scratch/hyaku/kaidoku-r66/` holds no
`ConnectorCross/` entry before or after this seat).

Subjects scanned: this round's two counter surfaces only —

- **S1 (R66-C1)** `tools/round-66/closure-boundary.py` (sha256 `3c5cfb03…d071045b`):
  post-probe cache ordering, the frozen `COUNT = 30` assertion (`entries == COUNT`,
  `count_ok`), and the `--skip-run` non-claim.
- **S2 (R66-C2)** `tools/round-66/coverage-selfcheck.py` (sha256 `1be9d046…86555aa`):
  recipe-A transcription + `--equiv` re-run of the committed SCORECARD heredoc, the
  `recipe_a_hidden` LIST, and the two self-assessment atoms with `mismatches`.

Question: does another lane already own (a) a reproduction of a lane's superseded
measurement recipe, (b) a closure-count assertion gate, or (c) a self-assessment
atom/mismatch counter?

## Sweep 1 — the seeded command, then narrowed

```
grep -rIl --include='*.py' -e 'dont_write_bytecode' -e 'closure' -e 'count_ok' -e 'mismatches' \
  /home/vgpnk/Projects/shokunin/*-shokunin/tools /home/vgpnk/Projects/shokunin/*-shokunin/scripts
```

215 files (`.py` only — kumitate's surfaces are `.mjs`, so it is absent here and searched
separately in Sweep 3). Per-lane census of the same hit list:

```
kaidoku 56 | tsukuroi 43 | kama 43 | kotodama 21 | tameshi 16 |
souji 14 | mori 10 | kake 8 | mado 3 | chousa 1
```

Narrowing to the exact tokens of the two surfaces (all from `/home/vgpnk/Projects/shokunin`):

| token | sibling hits | reading |
|---|---|---|
| `count_ok` | **0** (outside this lane) | no sibling emits or asserts a `count_ok` field |
| `recipe_a` / `--recipe` | **0** (outside this lane) | no sibling has a recipe-lettered measurement mode |
| `skip-run` | **0** | no sibling has a skip-run non-claim arm |
| `len(CLOSURE)` / `CLOSURE =` (case-sensitive) | **0** (`DISCLOSURE` only, tameshi `witness-metadata.py:93`, `bash-witness-study.py:186`) | no sibling carries a frozen closure map |
| `dont_write_bytecode` | 13 sibling files (chousa 1, kotodama 7, souji 4, tsukuroi 1) | mechanism only: instruments suppress their own bytecode |
| `mismatches=` emitters | kama `tools/kama-live-replay.py:935,955`; souji `tools/souji-declared-evidence.py:208`; souji `tools/souji-coverage-agreement.py:17-19` | vocabulary overlap, three different populations |

`grep -rIln 'Measurement recipes' .../{tools,scripts}` → only this lane's
`tools/round-66/coverage-selfcheck.py`. No sibling extracts or executes another lane's
SCORECARD measurement block. (`mado-shokunin/tools/mado-tripwire.py:336-341,810-884` and
`tameshi-shokunin/tools/bash-witness-study.py:299-303` parse *heredocs* — shell syntax and a
runner's own spec heredoc — never a measurement recipe.)

## Hit list — closest matches (top 3 by docstring, then the adjacent set)

| lane | path:line | what it holds | relation to r66 |
|---|---|---|---|
| tsukuroi | `tools/check-self-assessment.py:2,42-43,60,1093-1096` | "count self-assessment mismatches between a lane's stated axes and observed state"; 27 checks K01–K27; JSON with `mismatches`; exit 0/1/2; `--repo` parameterised | **class owner of (c)**, artifact-incompatible with this lane: requires a `## Axes - ` heading (`:15,461-472`), a capabilities table and `SHONEN.md` (`:447`). kaidoku `SCORECARD.md` has no `^## Axes` heading (only `## Owned axes`, `:19`), so the checker would exit 2 here |
| souji | `tools/souji-declared-evidence.py:7-19` | re-derives SCORECARD assertions at `--rev` (class A paths, class B revisions, class C sha256); `assertions= resolved= skipped= mismatches=`; exit 0 iff `M == 0` | **same shape as (c)**, different atoms: existence/rev/digest, no numeric fraction or score |
| souji | `tools/souji-capability-agreement.py:3-22` | "Counts mismatches between the lane's self-assessment files and what committed bytes show"; stated literal + command per TSV row, executed in a private clone at REV | **closest executed-literal atom counter** in the fleet — but its row list is read from a foreign preregistration commit, and it re-derives nothing itself |
| tameshi | `tools/count-recheck.py:3-24` | "a record's printed counting figure must still be the count its named command produces at the revision the record names"; counting command of record is `git grep -c`; zero-match = 0; exit map pinned | **class owner of printed-count verification**; does **not** cover a manifest-length constant assertion (`len(CLOSURE)+3 == 30`), which is not a `git grep -c` count |
| souji | `tools/souji-coverage-agreement.py:2-18` | two-sided coverage-map instrument: `MISSING-FROM-MAP` / `DANGLING-MAP-PATH`, `mismatches=X`, exit 0 iff X==0; grounded from `corpus/README.md` `ground: F<k>` tables | **coverage ground, different artifact**: the README map, never the SCORECARD recipe-A heredoc or the Owned-axes coverage row. Already cited by the r65 closure (`corpus/lessons/round-65.md:60`) as owning the coverage-map class |
| kama | `tools/round58-c2-counter.py:1-8` | "does the SCORECARD calibration row's account of the outside closure agree with observed repo state and the fleet ledger"; `mismatches=0` | lane-scoped calibration-row mismatch counter; kama's ledger, kama's row |
| kama | `tools/round69-newest-closure-counter.py:1-30` | resolves the newest non-author closure and checks the SCORECARD row names it; `NEWEST_CLOSURE … row_current=` | closure **pointer currency**, not a count; exit 0/1/2 |
| kumitate | `scripts/counter-pins.mjs:1-25` + `.ufo/pins/counter-pins.json` | pinned-counter registry gate: frozen counters byte-identical to frozen sha256s; `COUNTER_PINS: CLEAN pins=<n>` / `DRIFT` / `FAIL-CLOSED` | **(b) neighbour at most**: pins are hashes over kumitate's own paths; the count is printed, never asserted |
| kumitate | `scripts/round-gate.mjs:4-10`, `scripts/control-replay.mjs:1-16` | lane-local round-close pre-check; private replay of frozen controls with exact sanctioned edits | validator/control class, no count constant |
| tabi | `scripts/check-user-round-contract.mjs:451-452` | regexes over `git ls-tree … | wc -l` / `git grep … | wc -l` forms in reports | polices the *form* of counting commands; no count assertion |

## Per-lane verdict (one line each, as asked)

- **souji** — holds the fleet's coverage-map agreement instrument (`souji-coverage-agreement.py`,
  cited by the r65 closure), a SCORECARD assertion re-deriver (`souji-declared-evidence.py`) and
  an executed-stated-literal mismatch counter (`souji-capability-agreement.py`); round 66's C2
  **extends the class** (the first atom that re-derives the knowledge fraction
  `mapped/files` and its rounded score) and **merely neighbours** the first (README map ≠
  SCORECARD recipe A) and the third (no TSV row list, no foreign preregistration binding).
- **kumitate** — holds registry/validator gates: pinned-counter sha256 registry, round-close
  gate, control replay, gate-mutant battery; round 66's C1 **merely neighbours** it: no
  kumitate gate asserts a frozen entry count over a closure manifest, and `counter-pins.json`
  registers kumitate paths only.
- **tameshi** — holds the batteries (mutation runner `mutate-and-run.sh` + 55 tools) and the
  standing **printed-count drift** detector `count-recheck.py`; round 66's C1 **extends** that
  class by one form tameshi does not cover — a manifest-length constant
  (`entries == COUNT`), not a `git grep -c` figure — and duplicates nothing.
- **tsukuroi** — holds the generic cross-lane self-assessment counter
  (`check-self-assessment.py`: `mismatches`, exit 0/1/2, `--repo`); round 66's C2 **neighbours**
  it: same class and vocabulary, incompatible artifact prerequisites (kaidoku has no
  `## Axes - ` table, no `SHONEN.md`), so no contested scope — but the vocabulary overlap is
  real and should be cited.
- **kama** — holds closure *pointer* counters (r58 calibration row, r69 newest-closure) and
  live-replay `mismatches`; round 66's C1 and C2 both **merely neighbour**: kama's population
  is `corpus/lessons/round-*-verifier-spotcheck.md` and its own ledger, never a toolchain
  manifest or a recipe-A heredoc.

## Ownership boundary

| surface | owner | evidence |
|---|---|---|
| **(a)** reproduction of a measurement recipe (superceded r1 `date` filter in r65; committed recipe-A heredoc re-run in r66 `--equiv`) | **kaidoku's own.** The recipe lives in kaidoku `SCORECARD.md` "Measurement recipes", its population is `corpus/knowledge/*.md` at a kaidoku revision, and the extractor must parse this lane's banner (`**A - source-derived controls.**`, claims.json A6). No sibling has a recipe-lettered mode or executes a foreign SCORECARD block; the only fleet-wide `Measurement recipes` references are other lanes' own SCORECARD prose | Sweep 1 token table; `grep -rIln 'Measurement recipes'` → this lane only |
| **(b)** closure-count assertion gate (`entries == 30`, `count_ok`) | **kaidoku's own.** `CLOSURE` is this lane's toolchain map (3 d8 builds + `jsc2js-src/View8` + venv 4 entries + `inputs/…jsc`), pinned to the r65 instrument's sha256 and hosted under `/home/vgpnk/.local/share/kaidoku-jsc`. Fleet-wide `count_ok` = 0 hits; `CLOSURE` constant = 0 hits. kumitate's pin registry and tsukuroi/kama registry gates assert identity/occurrence, not cardinality | Sweep 1 token table; `kumitate/.ufo/pins/counter-pins.json` |
| **(c)** self-assessment atom/mismatch counter | **class shared, atoms lane-local.** The class is owned three times over outside this lane (tsukuroi `check-self-assessment.py`, souji `souji-capability-agreement.py` + `souji-declared-evidence.py`, kama r58/r69 for the calibration row). Round 66's two atoms — A1 `round(10*stem.mapped/stem.files, 2)` vs the coverage row's head score; A2 the cited `<mapped>/<files> knowledge files` vs the stem recipe — are implemented by **no sibling** and cannot be, because both sides are this lane's recipe output | Sweep 1; tsukuroi `:15,461-472` prerequisite mismatch; kaidoku `SCORECARD.md:19` |

## What should be reported to owning lanes (not absorbed)

1. **To souji** — the coverage-fraction atom family is a candidate row for
   `souji-capability-agreement.py`: (stated literal, command) = (the coverage row's head score
   and its `<mapped>/<files> knowledge files`, `python3 -I -B tools/round-66/coverage-selfcheck.py
   --selfcheck --rev <rev>`). Its TSV shape fits without a new instrument; nothing of it is
   absorbed here.
2. **To tameshi** — `count_ok` is a printed-count form outside `count-recheck.py`'s counting
   command of record (`git grep -c`): the figure is a manifest length, not a grep count. Report
   as a possible row family; do not widen tameshi's detector from this seat.
3. **To tsukuroi** — the r66 C2 receipt vocabulary (`mismatches`, exit 0/1/2) duplicates
   `check-self-assessment.py`'s, but the checkers cannot be unified on this lane (missing
   `## Axes - ` table / `SHONEN.md`). Report the vocabulary; keep the checkers separate.
4. **Not to be absorbed, not to be claimed as new**: the class of (c) generally. `SKILL.md` in
   this lane cites neither souji nor tsukuroi (`grep -i 'souji\|tsukuroi' SKILL.md` → no
   matches), so any novelty sentence for C2 must name tsukuroi/souji as the class precedent, or
   drop the novelty claim.

## Residual risks stated, not smoothed

- **Vocabulary collision is the real hazard, not duplicated code.** Three lanes print
  `mismatches` with three exit maps over three populations; a reader comparing receipts across
  lanes will mis-read a `mismatches 0` as agreement. The r66 receipts should name their atom
  population inline (claims.json A7 already does; the receipt field set should too).
- **A2's denominator is unstable by construction**: the cited fraction is compared against
  `stem.mapped/stem.files` at the same revision, so the atom is green only while the SCORECARD
  row and `corpus/knowledge` are measured in the same run. Any sibling that later re-derives
  the fraction from a different recipe (souji's README-map count is 142/142-shaped) will
  disagree with this counter on a map token written without the `knowledge/` prefix — the same
  divergence the r65 closure already recorded for `coverage-recipe.py` (`corpus/lessons/round-65.md:60`).
- **No sibling round-66 counter work exists to coordinate with.** The only sibling round-66
  artifact found on these surfaces is `kumitate-shokunin/PROVINCE.md:20` (an `omp/18.13.1`
  measurement), unrelated to either counter.
