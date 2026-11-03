# ConnectorCross — sibling-overlap scan (r65 w1)

Seat: leaf connector. Read-only sweep over `/home/vgpnk/Projects/shokunin/*-shokunin`
except this lane. No sibling tool was executed; no sibling file written.

## Sweep 1 — `.jsc` / View8 / V8-bytecode route counter

Command (all lanes but kaidoku; `tools/`, `corpus/`, `SKILL.md`, `PROVINCE.md`):

```
grep -rn -i -E 'jsc' --include='*.md' --include='*.py' *-shokunin/tools *-shokunin/corpus
```
→ 2 hits, both false positives on the substring `js`: `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.md:81`
("rechecked by `R16AdjScoutNow`") and `mori-shokunin/corpus/SOURCES.md:138` (a URL).

Positive control on the same command shape, this lane only: 10+ hits
(`kaidoku-shokunin/tools/round-64/jsc-route-matrix.py`, `tools/round-35/c1-coverage-counter.py`,
`tools/round-64/mkcache.js`, `PROVINCE.md:136,154`, `SKILL.md:56,1703,1853`).

`\bview8\b|\.jsc\b|loadjsc` over sibling `tools/`+`corpus/`+`SKILL.md`+`PROVINCE.md`: **0 hits** (exit 1).

## Table

| lane | path:line | what it claims | overlap class |
|---|---|---|---|
| — (all siblings) | — | no `.jsc` / View8 / `loadjsc` route counter anywhere outside this lane | **none** — no sibling owns the route matrix |
| tsukuroi | `SKILL.md:1974` | "`sys.dont_write_bytecode` precedes the import so read-only invocations do not generate `tools/__pycache__`" | mechanism-only: bytecode-write suppression for its own tools, **not** a `.jsc` route counter |
| tsukuroi (+ 48 other sibling tools) | `tools/check-*.py` (49 files set `dont_write_bytecode`) | fleet-wide convention: instruments suppress their own bytecode writes | mechanism class, **owned** — this lane's frozen r65 tools do not adopt it (see report F-3) |
| tsukuroi | `tools/check-exec-environment-r40.py:27`, `check-package-anatomy-r41.py:28`, `check-scrub-record-r42.py:9` | frozen capture directory + MANIFEST pinned by sha256, verified against a registry row | adjacent class: **frozen-pin verification**, but over btrfs/kernel captures, never a live toolchain closure + absence-of-writes census |
| souji | `tools/souji-coverage-agreement.py:4-18` | two-sided coverage map over `corpus/README.md` + `corpus/knowledge`: `MISSING-FROM-MAP` (entry with `ground: F<k>` named by no map row) and `DANGLING-MAP-PATH` (map path absent from the tree); population via `git ls-tree -z <rev> -- corpus/knowledge/` | **owns the instrument class** R65-C2 repairs: population derived from the tree, not from the map's own filter |
| kama | `tools/round37-coverage-audit.py:1-10` (+ 35/36/38, 42/43) | round-scoped: a named coverage-map block names three specific entries; each exists; each cites a new S-id | narrower: round-assertion, not a population counter |
| tsukuroi | `tools/check-registry-coverage.py:1` | SKILL.md gate/probe registry vs committed tools | different population (registries, not knowledge files) |

## Sweep 2 — `population_dropped` / knowledge-file completeness counter

`grep -rn 'population_dropped' .` fleetwide → only this lane:
`plans/round-65-claims.md:79,82,89`, `tools/round-65/coverage-recipe.py:20,28,34,108,168`,
`.ufo/waves/round-65/gen-w1.py:38,120,129,158,185`.

Conclusion: the *name* is unique to this lane; the *instrument class* is not — souji's
`souji-coverage-agreement.py` is a two-sided knowledge-map population counter over the same
artifact pair (`corpus/README.md` map + `corpus/knowledge` at a rev) and already derives its
population the way the r65 `stem` recipe does. No sibling runs it against this lane's corpus.

## In-lane duplication (same lane)

| source | artifact read | parse | population |
|---|---|---|---|
| `tools/round-35/c1-coverage-counter.py:137-141` | `corpus/README.md` (whole file), `corpus/knowledge` (`ls-tree`, line 100) | substring: `if p.rsplit("/",1)[1] not in readme` | fixed two-entry `ENTRIES` dict |
| `tools/round-65/coverage-recipe.py:61-96,123-129` | `## Coverage map` section only, `corpus/knowledge` (`ls-tree -r`) | backticked spans, comma-split, `CLAIM_RE`, `claimed` = `knowledge/` prefix OR dated stem | full stem list / date-filtered list |
| `souji-shokunin/tools/souji-coverage-agreement.py:31-40,75-90` | `ground`-headed README tables, `ls-tree -z` | `CODE_SPAN` + `KNOWLEDGE_PATH` (`knowledge/<name>` only), front-matter `ground:` | full tree |

Three parsers, one artifact. R65-C2 added the second in-lane parser instead of composing the
r35 one or citing souji's class; the r65 `claimed` heuristic (bare dated stem counts as claimed)
diverges from souji's (`knowledge/` path required), so the two instruments will disagree on any
map token written without the `knowledge/` prefix or without a date.

VERDICT: no contested sibling scope. The `.jsc`/View8 route and the closure-plus-census are
unowned outside this lane; the R65-C2 instrument class is owned by souji
(`souji-coverage-agreement.py`), so R65-C2's contribution is the *repair evidence*, not a new
capability — the lane re-implemented the parser instead of composing it, and skipped the
fleet-standard `dont_write_bytecode` guard its own frozen tools would need.
