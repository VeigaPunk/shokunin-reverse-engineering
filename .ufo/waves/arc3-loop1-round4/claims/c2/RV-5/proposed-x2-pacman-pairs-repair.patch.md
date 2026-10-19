# PROVINCE.md repair — Round-4 frontier bullet "Cross-version residuals": pacman-cache pairs BEYOND expac were exercised

Authored by SEAT RV-5 (chain c2, reviewer), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified first-hand)

`PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet `Cross-version
residuals`, current bytes:

> … multi-version pacman pairs beyond expac unexercised …

Falsified by admitted corpus state, twice over:

1. `corpus/knowledge/2026-10-13-r2-version-diff-compare.md:11-18` — the very entry
   the row cites records **three** pacman-cache pairs exercised, not one:
   `1password-cli` 2.34.1-1 → 2.40.0-2 (`usr/bin/op`),
   `expac` 10-12 → 10-13, and `bubblewrap` 0.11.2-1 → 0.12.0-1 (`usr/bin/bwrap`).
   `bwrap` is **beyond expac** by the clause's own words. The entry is admitted
   (`corpus/README.md:33` and `:91`, the map row's probe cell reading
   "live compares on expac/**bwrap** pairs").
2. `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:15-22` — a later round
   exercised further cached pairs, `1password-cli` and `qpdf` 12.3.2-2 → 12.4.1-1,
   through the full pipeline (analyze/search/function/compare, run-log rows 10-16,
   `ev_aedcac02…`/`ev_97c58945…`/`ev_775ddbb4…`/`ev_d6d3c057…`). Admitted at
   `corpus/README.md:35` and `:140`.
   (`2026-10-13-r4-09-js-export-compare.md` adds the obsidian
   `1.12.7 → 1.13.7` pair from `/var/cache/pacman/pkg/`.)

**Why the chain's census missed it (named, with the exact defect).** VZ-2's row
`X2` reads:

```python
add("X2", "Cross-version residuals",
    "multi-version pacman pairs beyond expac unexercised",
    corpus_has(corpus, "expac")[:3],          # <-- presence test, not a truth test
    "current",
    "no corpus entry claims a further pacman version pair")
```

`corpus_has(corpus, "expac")` is satisfied by the entry that *contains the word*
`expac` — including the very file that lists `bwrap` two lines below it. The test
measures keyword presence, so it returns a hit on the falsifier itself. The
note's assertion ("no corpus entry claims a further pacman version pair") is
false on the admitted corpus: `corpus/README.md:91` names bwrap in the probe
cell. Transcript: `evidence/x2-falsifier.txt`.

**Not repaired by any landed patch.** EX-13's
`province-round4-frontier-cross-version-residuals.patch.md` repairs the bullet's
*first* clause (`compare-application-versions`) and explicitly preserves this
clause verbatim ("The second clause stands and is preserved"). EX-14's v2
candidate does the same. So the falsified clause survives every current
candidate.

## Change (same-line replacement, line count held at 4)

This patch repairs the second clause **and** carries EX-13's first-clause repair,
so the parent gets one applyable voice for the whole bullet (the two repairs
target the same four physical lines and cannot land as two separate hunks).

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **Cross-version residuals** — `compare-application-versions` still
-  probe-refused since r2; multi-version pacman pairs beyond expac unexercised
-  [r5-audit C1: merged from the pruned Frontier bullet — its
-  `compare_javascript_export_shapes` item is now held (Core, r4-09)].
+- **Cross-version residuals** — `compare-application-versions` exercised since
+  r12 (all three input classes; the r2 refusal is historical); cached pacman
+  pairs exercised on expac, bwrap, op and qpdf [r5-audit C1: merged from the
+  pruned Frontier bullet — its `compare_javascript_export_shapes` item is now held].
```

## Census conformance

- **Line-neutral**: 4 → 4 lines; `PROVINCE.md` stays at 162 lines (DATED marker
  at line 119 unaffected; this bullet sits at 157-160).
- **Needle-free**: no `rea-agents@x.y.z`, no bare `6.x.y`, no
  `~`/`/`-absolute `path:line`. The round tokens `r12`/`r2` are not version
  pins. Measured on the patched tree: `undeclared=0`
  (`evidence/patch-apply-and-census.txt`).
- Search text is verbatim and unique in `PROVINCE.md`
  (`evidence/patch-apply-and-census.txt`).
