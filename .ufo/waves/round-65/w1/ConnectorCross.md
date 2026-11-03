# ConnectorCross — cross-lane connector, r65 w1

Base `c99e907cb5576c13a7b22755d776b356fdfc1752`. Axes in play: **coverage, depth, calibration**
(all 10.0). Scope: sibling-overlap scan + one bounded move. No claim judged, no instrument
edited, no sibling tool executed, no file written outside this seat's report dir and its
scratch (`/fast/scratch/hyaku/kaidoku-r65/ConnectorCross`, removed).

Frozen instruments were read, not modified — pins re-measured and equal to the assignment:

```
79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6  tools/round-65/jsc-closure-matrix.py
9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6  tools/round-65/coverage-recipe.py
```

## 1. `.jsc` / View8 / V8-bytecode route counter — no sibling owns one

Sweep (`grep -rn -i -E 'jsc' --include='*.md' --include='*.py' *-shokunin/tools *-shokunin/corpus`,
all lanes but this one): **2 hits, both substring false positives on `js`**
(`kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.md:81`,
`mori-shokunin/corpus/SOURCES.md:138`). The same command shape on this lane returns 10+ genuine
hits (`tools/round-64/jsc-route-matrix.py`, `tools/round-35/c1-coverage-counter.py`,
`tools/round-64/mkcache.js`, `PROVINCE.md:136,154`, `SKILL.md:56,1703,1853`), so the null is a
real null, not a broken pattern. `\bview8\b|\.jsc\b|loadjsc` over sibling
`tools/`+`corpus/`+`SKILL.md`+`PROVINCE.md`: 0 hits (exit 1).

Nearest sibling capabilities, by class:

| lane | path | capability | relation to R65-C1 |
|---|---|---|---|
| tsukuroi | `SKILL.md:1974` | `sys.dont_write_bytecode` before import keeps its own `tools/__pycache__` clean | mechanism, not a route counter |
| tsukuroi + 48 sibling tools | `tools/check-*.py` | same guard, 49 files fleet-wide | a **fleet convention this lane's frozen r65 tools do not follow** (F-3) |
| tsukuroi | `check-exec-environment-r40.py:27`, `check-package-anatomy-r41.py:28`, `check-scrub-record-r42.py:9` | frozen capture dir + MANIFEST pinned by sha256, verified against a registry row | adjacent: frozen-pin verification over kernel/btrfs captures; no live-toolchain closure, no absence-of-writes census |
| chousa / tameshi / souji | `digest-in-tree.py:8`, `pin-disposition.py:5`, `souji-landing-gate.py:719` | pin *consumers* (extract, compare, refuse) | adjacent: none enumerate a closure a priori |

So R65-C1's contribution is genuinely new to the fleet: an a-priori closure manifest (count +
sha256 for every file read and every executable spawned, incl. the transitive View8 import tree)
plus a before/after census that certifies *no write happened*. No sibling claims it.

## 2. Coverage-recipe / knowledge-file completeness counter — class is owned by souji

`population_dropped` is unique to this lane (`plans/round-65-claims.md:79,82,89`,
`tools/round-65/coverage-recipe.py:20,28,34,108,168`, `.ufo/waves/round-65/gen-w1.py:38,120,129,158,185`;
nothing in any sibling). But the **instrument class** is not new:
`souji-shokunin/tools/souji-coverage-agreement.py:4-18` is a two-sided counter over exactly the
same artifact pair (`corpus/README.md` map + `corpus/knowledge` at a rev), and its population is
`git ls-tree -z <rev> -- corpus/knowledge/` — i.e. tree-derived, never filtered by the map's own
token shape. That is precisely the property R65-C2 repairs to. `kama-shokunin/tools/round3*-coverage-audit.py`
is round-scoped (asserts three named entries), and `tsukuroi-shokunin/tools/check-registry-coverage.py`
counts a different population (SKILL gate registry vs tools). Souji is the only class owner, and
it has never been run against this lane's corpus.

## 3. The two new instruments do not overlap each other

The dispatch premise "both read `corpus/README.md`" is **false** for the frozen bytes:

- `jsc-closure-matrix.py` never reads `corpus/README.md`. Its only `README` reference is
  `:92` — `"jsc2js-src/View8/README.md": "557d14a20a622d42f620547b19c41d2f7224bc264f6fc22f64bedb4164efcf50"`,
  a pinned toolchain entry. It runs no `git`; it reads the toolchain root and spawns d8/node/python.
- `coverage-recipe.py` is the only one that touches git (`:118-129`: `ls-tree -r -- <rev> -- corpus/knowledge`,
  `show <rev>:corpus/README.md`) and the only one that parses the coverage map (`:61-96`).

Write paths are disjoint: `jsc-closure-matrix` → `--out` receipt, `--census OUT`, `--work`
scratch cells; `coverage-recipe` → `--out` only (plus stdout). No shared code, no shared input,
no shared output. This is *good* separation — the one composition failure is in-lane against an
older instrument, not between these two.

Duplicated logic that should have been composed (**lane composition rule**):

| source | map parse | population |
|---|---|---|
| `tools/round-35/c1-coverage-counter.py:137-141` | substring of entry filename anywhere in whole README | fixed two-entry dict |
| `tools/round-65/coverage-recipe.py:61-96` | `## Coverage map` section, backtick spans, comma-split, `CLAIM_RE`, `claimed` = `knowledge/` prefix **or** dated stem | full stem list / date-filtered |
| `souji-coverage-agreement.py:31-40,75-90` | `ground`-headed tables, `KNOWLEDGE_PATH` requires `knowledge/<name>` | full tree (`ls-tree -z`) |

R65-C2 added the second in-lane parser of one artifact instead of generalising the r35 one or
citing the souji class. Consequence worth flagging to the L1's knowledge entry: the r65
`claimed` heuristic admits a **bare dated stem** as a map token, while souji's requires a
`knowledge/` path — the two instruments will disagree on any token written without the prefix,
so a future cross-lane census cannot reconcile by class name. Suggested (non-binding) repair of
the *write-up*, not the frozen bytes: name the mapping `missing ≡ MISSING-FROM-MAP` /
`dangling ≡ DANGLING-MAP-PATH` and note the token-shape divergence.

## 4. Contested scope

None. `.jsc`/View8/closure-census: unowned outside this lane (0 hits). Coverage-map agreement:
souji owns the class for **its own** corpus; the two corpora are disjoint and no sibling reads
this lane's `corpus/README.md`. The only in-lane contest is against this lane's own r35 counter
and r64 matrix, which R65-C1/C2 extend rather than contradict.

## Contradictions (stated, not smoothed)

**F-1 — the R65-C2 predicate asks the frozen instrument to do something it cannot do.**
Verbatim predicate clause: "the superseded date-limited recipe … reports a non-zero
`population_dropped` **naming the files it hides**". Measured at base
(`python3 -B tools/round-65/coverage-recipe.py --root . --rev c99e907… --recipe date --out …`, exit 1):

```
{"dangling": [], "exit": 1, "knowledge_files": 144, "mapped": 142, "mismatches": 2,
 "missing": [], "population": 142, "population_dropped": 2, "recipe": "date",
 "rev": "c99e907cb5576c13a7b22755d776b356fdfc1752", "tool": "tools/round-65/coverage-recipe.py"}
```

`population_dropped` is `len(files) - len(population)`, an **integer**; the code emits no name
list for it (`:108`), and the two hidden files appear in neither `missing` (`:104`,
population-intersection only) nor `dangling` (both are written bare, so `claimed` is false).
The docstring `:34` ("files the recipe's own filter keeps out of the population") promises names
the code does not produce. **The naming exists only in the claims prose
(`plans/round-65-claims.md:89`), not in any instrument receipt.** Frozen bytes: report, do not
patch. Whichever seat certifies R65-C2 must attach an out-of-band name derivation, or the
predicate's naming clause rests on an assertion.

Independently measured names, sharing no code with the recipe:

```
git -C . ls-tree -r --name-only c99e907… -- corpus/knowledge | wc -l          → 145
git -C . ls-tree -r --name-only c99e907… -- corpus/knowledge | grep -cE '2026-10-[0-9]{2}-' → 142
git -C . ls-tree -r --name-only c99e907… -- corpus/knowledge | grep -vE '2026-10-[0-9]{2}-'
  corpus/knowledge/.gitkeep
  corpus/knowledge/jsc-mapper-cli-contract.md
  corpus/knowledge/jsc-mapper-release-inventory.md
```

**F-2 — the repair swapped a date filter for an extension filter, and the predicate cannot see
the difference.** `read_inputs` keeps only `.md` (`:123-127`), so the `stem` arm's population is
144 while the tree holds 145 blobs: `.gitkeep` is still silently out — it is simply invisible
because it can never appear in a map. Stem arm (measured, exit 0):
`population 144, mapped 144, missing [], dangling [], population_dropped 0, mismatches 0`.
That satisfies the predicate (`mismatches == 0`, `mapped > 0`) and is honest against the
docstring's declared population (`every corpus/knowledge/*.md`, `:22`), but "no denominator
narrowing" is **not** what the predicate proves — it proves "no *date* narrowing". Stated as a
residual, not a defect.

**F-3 — the census root and the cache witness are different directories.** Clause (i) requires no
bytecode cache "before the first run"; clause (iii) compares the toolchain-root census. Both are
scoped to `/home/vgpnk/.local/share/kaidoku-jsc` — which is currently cache-free (`find
/home/vgpnk/.local/share/kaidoku-jsc -name __pycache__ -not -path '*/.git/*'` → empty). But this
lane's *own* `tools/round-65/__pycache__` exists with both frozen `.pyc`s, mtime
`2026-11-03 20:24:49.800` — after prep (`prep/precache-dirs.txt`, 20:11:33) and before this
seat's first command (`w1/ConnectorCross/`, 20:26:05), so not written by this seat (this seat ran
`python3 -B` with `PYTHONDONTWRITEBYTECODE=1`). Cause is visible in the bytes: neither frozen
instrument sets `sys.dont_write_bytecode` at import (`grep` finds only `:55 import sys` in
`coverage-recipe.py` and `SUBPROCESS_ENV = {"PYTHONDONTWRITEBYTECODE": "1"}` at
`jsc-closure-matrix.py:129` — that protects *subprocesses*, not the instrument when imported or
run as a module), while 49 sibling tools and `souji-coverage-agreement.py:26` set the guard. Net
effect: a run can leave `__pycache__` in the lane tree and still pass both clauses, and nothing in
the receipt distinguishes "toolchain clean" from "nothing anywhere wrote bytecode".

## Proposed move (one, bounded)

**Attach a two-file "shadow measurement" sidecar to the receipt directory, produced by shell
only, sharing no code with either frozen instrument:**

1. `dropped-names.txt` — the exact command
   `git -C <lane> ls-tree -r --name-only <base> -- corpus/knowledge | grep -vE '2026-10-[0-9]{2}-' | grep '\.md$'`,
   its exit code, the two names, and the file's own sha256. Cross-check: line count == the frozen
   date arm's `population_dropped`.
2. `cache-sweep.txt` — one `find <toolchain-root> -name __pycache__ -o -name '*.pyc'` **plus**
   `find <lane>/tools/round-65 -name __pycache__ -o -name '*.pyc'`, timestamped, run immediately
   before the first matrix cell.

Why it is the non-obvious move: F-1 shows the predicate's naming clause has no instrument behind
it, and F-3 shows the "no bytecode cache" clause can be read as global while a lane-local cache is
present. Both gaps close with two read-only shell commands that *derive the numbers from a
different code path* than the instruments they check — the sidecar measures the instruments instead
of trusting them.

Axes:
- **calibration** ↑ — the naming clause becomes measured evidence, and the integer is
  independently reproduced (`2 == 2`) rather than restated; the `.md`-filter residual is dated in
  the same file so the "population" word is not over-read.
- **coverage** ↑ — the dropped files and the lane-local cache become visible in-tree; the blind
  spot and the cache leak stop being prose.
- **depth** — untouched: no claim wording, no predicate, no byte of either frozen instrument.
- **harm check** — read-only; nothing written under the toolchain root; no sibling tool executed
  (respects "sibling repos read-only grep only"); no git mutation; no new claim.

Risks: (a) sidecar misread as instrument output → prefix filenames `shadow-`, state the command
line and exit code in each file, and never fold its number into `mismatches`; (b) the name
derivation reuses the same *date regex*, so it is independent of the recipe's **code**, not of
its *pattern* — say so in the header; (c) a future population with a nested directory would make
the name count diverge from `population_dropped` — the sidecar must assert equality and fail
loudly (record both numbers) rather than silently agree.

Verification the L1 can run (no instrument edit): the two shell blocks above, then
`wc -l shadow-dropped-names.txt` vs the date-arm JSON's `population_dropped`, and
`sha256sum shadow-dropped-names.txt` recorded in the receipt. Expected now:
names exactly `jsc-mapper-cli-contract`, `jsc-mapper-release-inventory`; count 2; toolchain
cache sweep empty; lane `tools/round-65` sweep 2 `.pyc`.

VERDICT: no sibling contest on either claim; R65-C1's closure-plus-census is unowned fleet-wide
and R65-C2's instrument class is owned by souji (class citation owed, parser duplication noted).
Two predicate-shaped gaps are real and measured — the date arm cannot name the files its
predicate says it names (F-1), and the cache clause is scoped narrower than its wording (F-3) —
and both close with one read-only sidecar, no frozen byte touched.
