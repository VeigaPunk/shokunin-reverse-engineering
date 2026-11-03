# Round 65 — the `.jsc` route under a complete closure; the coverage recipe's stale premise

Base `c99e907cb5576c13a7b22755d776b356fdfc1752`; declaration `4a699a3fbd4073464521540c9e68974ed9939be5`;
operative freeze `922ed89f42bed28173035f3faaf705e0cb70abb7`. Two claims: R65-C1 (depth, capability
acquisition) verified on the executed run with two counter-boundary defects disclosed; R65-C2
(calibration, capability acquisition) an honest stop on two grounds — the frozen naming clause is not
emitted by the counter, and the claim's before-arm is not the superseded recipe (the critic's C2-F1/F2).

## Gate

Access date for the new source: 2026-11-03. Complete fetch/locator/digest evidence:
`.ufo/waves/round-65/w1/ScribeSources/row.md`, `gate.md`, `fetch.json`; seat note `w1/ScribeSources.md`.

| row | opened source and locator | located quote | decision |
|---|---|---|---|
| S266 | https://docs.python.org/3/using/cmdline.html — `#cmdoption-B` raw line 474, under h3 `Miscellaneous options` (line 451); snapshot sha256 `96f87232f979982bd2aa268510c9c89b57186f0f3802840aafa7de1a7537810f`, 171073 bytes, fetched 2026-11-03T23:26:03Z | "If given, Python won’t try to write .pyc files on the import of source modules." (15 words) | admit A docs, scope = the switch's stated effect only; it grounds the cache-free design, never a claim that a given run wrote nothing (the census is that evidence) |
| `sys.dont_write_bytecode` page | https://docs.python.org/3/library/sys.html line 585; sha256 `572c354e…`, 280617 bytes, same fetch instant | same sentence, but the nearest containing heading is the module-level h1 and the attribute is defined as derived from `-B` | reject as the S266 anchor: second-hand setting, heading too broad; kept as the recorded alternative in `fetch.json`, not discarded |
| the frozen R65-C2 naming clause | `plans/round-65-claims.md`; `tools/round-65/coverage-recipe.py:104-108` | `population_dropped` is an integer; the date arm emits no list of the hidden files | reject as verified: claim prose the counter never implements (QUALITY #87). R65-C2 stops honestly; no post-freeze instrument edit |
| the R65-C2 before-arm premise | `tools/round-65/coverage-recipe.py:93` against the superseded recipe A (`SCORECARD.md:100-121` at the base); critic `C2-F1`/`C2-F2`, `w1/CriticClaims/evidence/recipeA-at-base.json` | recipe A verbatim at the base: `knowledge_files 144`, `mapped 142`, `missing` the two November names, `coverage_score 9.86`, no denominator filter; the instrument's date mode invents a filtered population and a `population_dropped` field recipe A never had | reject the before-arm as "the superseded recipe": a stale premise (M65-2). The rule row 102 stays; its cited evidence is corrected by row 103 |
| round-64 container `RECEIPT_ABSENT receipt.json` | `.ufo/waves/round-64/claims.json` command template `--out <receipt.json>` | the token is the placeholder inside the argv template | reject the finding as a real missing receipt; dispositioned in `l1/duties/dispositions.md`; filed bytes stay |

Assimilation: none this round — the `merge/kaidoku/` jsc theme was adopted in round 64 (entries
`jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`); no other staged theme fits these claims, and a
bulk append is refused by CORPUS.md rule 4. `considerthese/` is absent (measured).

Outside spot-check: the round's non-author closure judge supplies it; this lesson does not self-certify
admit/reject agreement.

Convergence: three seats independently found the C2 defects before the L1 read any of them — `ExecCoverage`
(the frozen date receipt names no files), `ScribeLesson` (F-2), and `CriticClaims` (C2-F1/F2: recipe A does
not filter its denominator). That convergence is the reason the verdict is `unprovable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M65-1 | process/scope: the round-64 measuring run wrote Python bytecode caches into the retained toolchain it was measuring | `.ufo/waves/round-65/prep/precache-dirs.txt` (4 directories), `prep/README.md` (15 `*.pyc` counted; filenames not retained — stated limit), and the blocking finding `.ufo/waves/round-64/w1/ReviewerMatrix/review.md:24` F2 | r64 ReviewerMatrix F2 (blocking, but no QUALITY criterion and no predicate clause: the r64 predicate pinned sha256 only) | the r65 cache-free clause plus `-B`/`PYTHONDONTWRITEBYTECODE`. Shown red: `w1/ExecControls/cache-present.json` exit 2 naming `jsc2js-src/View8/__pycache__` and `…/x.pyc`; green after removal (`cache-clean.json` exit 0, 30 entries). The red uses a planted `x.pyc`, so it demonstrates the refusal, not the round-64 file set |
| M65-2 | stale-premise/reference-drift: the round's `date` mode was declared "the superseded date-limited recipe", but the superseded recipe A never filtered its denominator — at the base it reports `coverage_score 9.86` and **names** the two missing files, while the instrument's date mode invents a filtered population and a `population_dropped` count | `w1/CriticClaims/evidence/recipeA-at-base.json` (`knowledge_files 144`, `mapped 142`, `missing` the two names, `coverage_score 9.86`); `tools/round-65/coverage-recipe.py:93`; `l1/c2-before-date.json` (population 142, dropped 2) | critic `C2-F1`/`C2-F2` this round (the premise was never checked against recipe A before the freeze) | the before-arm must run the superseded recipe verbatim; a counter that invents a mode it calls "the superseded recipe" is measuring a new recipe. Red/green: recipe A at base = 9.86 with names; the date mode = 142 population / 2 dropped / no names — they disagree, and the disagreement is the defect. Row 102's rule stands; row 103 supersedes its why clause |
| M65-3 | landing/ordering: the round's carry-in LOG entry (QUALITY #34) landed after the operative freeze instead of before it | `l1/records/m65-3-order.txt`: `git merge-base --is-ancestor <carry-in commit> 922ed89f…` exits 1 for round 65 (the carry-in is in the landing `db98f39c`, a descendant); the same check for r63 (`0fadbd06` → `fbc0f950`) exits 0 | QUALITY #34 itself (the rule was known and not enforced by any check) | the order check becomes a round-duty command: the carry-in must be an ancestor of the freeze. Shown able to fail: red exit 1 at this round's own commit order, green exit 0 at r63's |
| M65-4 | scope: a frozen claim clause ("naming the files it hides") that the frozen counter never implements, and a counter that carries no predicate constant and no receipt carrying the frozen sentence (QUALITY #68's byte-identity clause covered only claim and plan) | `tools/round-65/coverage-recipe.py:104-108` (integer only) and `l1/c2-before-date.json` (`missing []`, `dangling []`, `population_dropped 2`); critic `C2-F3` | QUALITY #87 (every claim clause traced to the counter line that evaluates it) — not applied at the r65 freeze | honest stop for R65-C2; the next claim on this ground must declare only an emitted field, and a NEW freeze must extend the counter and carry the predicate constant before data. No post-freeze edit, no narrowed target |
| M65-5 | counter-boundary: two holes in the R65-C1 counter that the executed run did not hit — (a) the cache-free check runs before `python_probe`, while the before-census is taken after it, so a cache written by the setup probe is absorbed into the baseline; (b) `entries = len(CLOSURE)+3` is emitted but never asserted, so a truncated manifest passes | critic `C1-F1` counterexample (`w1/CriticClaims/evidence/cache-ordering-receipt.json`: a copy with the probe's `-B`/env removed still verifies 18/18, exit 0, while a `parse/__pycache__` file exists); `C1-F2` (`evidence/trunc-manifest-29.json`: one CLOSURE entry deleted, `--manifest` exit 0, `entries 29`) | the critic this round; no clause of the frozen predicate asserts the count or the post-probe state | disclosed, not repaired in place (frozen bytes). Next freeze: `cache_entries(root)` re-run after `python_probe` and folded into `closure.ok`, plus a frozen `COUNT = 30` assertion. The executed round-65 run is clean (the probe runs with `-B` and the env), but the counter would not have caught a probe write |

## Outcome

- R65-C1: 18 of 18 frozen labels reproduced under the 30-entry closure, cache-free start, equal
  before/after census (exit 0). Receipt `.ufo/waves/round-65/w1/ExecMatrix/matrix-run.json`; controls
  `.ufo/waves/round-65/w1/ExecControls/` (selftest 34 cases, do-nothing byte-identical to the frozen arm,
  pin mutation exit 2 naming one path, cache arm exit 2 then 0, census arms 0/1); mutation 6 mutants /
  6 killed (`w1/MutClosure/mutants.md`); reviewer Q1–Q6 closed with nine advisory findings;
  independent manifest re-derivations 30/30 (scout) and 27/27 + 3/3 (sentinel). Two counter-boundary
  defects disclosed (M65-5) and left for a new freeze; the executed observation is unaffected.
- R65-C2: **unprovable** on two grounds — the naming clause is not emitted, and the before-arm misdescribes
  the superseded recipe (recipe A reports 9.86 and names the two files; the instrument's date mode invents a
  filtered population). The after-arm is real: the stem recipe maps 144/144 at the base and 145/145 at the
  landing (`l1/c2-stem-at-landing.json`). No capability row entered; the instrument is registered and its
  outputs re-derive.
- Container text drift, disclosed: `claims.json` atom A3 says "4 venv identity files" where the pinned map
  holds 5 (9 + 12 + 5 + 1 = 27; reviewer A8). The map and the 30-entry total are correct; filed bytes stay.
- Cross-lane (adjacency): `w1/ConnectorCross/overlap.md` — no sibling owns a `.jsc` route counter;
  `souji-shokunin/tools/souji-coverage-agreement.py` already owns a two-sided coverage-map instrument class.
  Reported, not absorbed.
- Toolchain state: cache-free at the freeze and at the wave run; the census at the freeze holds 105 files.

## Census

Round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0,
19 W04, 172 rows (`l1/census-start.txt`). Round end: exit 0, 19 W04, 173 rows (S266 added; mined 163 → 164,
rejected 9 → 9). The 19 W04 duplicate-url warnings are standing named debt, unchanged.
