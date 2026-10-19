# proposed-coverage-count — patch text for `.ufo/gates/custody-pair/custody-pair.py`

Authored by SEAT EX-24 (chain c2, executor), wave `arc3-loop1-round3`. **Patch text
only** — the real target is EX-21's write target.

Measured against revision `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`
(re-derived at write time; evidence `../after/M18-*.out`, `../after/M19-*.out`,
`../after/M8b-*.out`).

## The residual (measured, reproducible in 2 commands)

`reference_coverage()` (current revision, ~line 591) decides with
`len(ref_sections) >= required` — **stanza multiplicity** — while its own
`unaccounted:` list is computed by **resolved-path identity**
(`{Path(s["path"]).expanduser().resolve() for s in ref_sections}`).

Two consequences, both measured on the landed revision:

| vector | command | result |
|---|---|---|
| 5× duplicate stanza for ONE path (v1 sums and v2 shapes) | `verify fixtures/v2-dupe-5x.txt --live --require-paths 5` | **exit 0**, `MATCH paths=1/1`, other four custody paths unexamined, **no coverage line printed** |
| 5 unrelated scratch paths | `verify …/r5.txt --live --require-paths 5` | exit 0, `MATCH paths=5/5` |

At an earlier revision (`03bd6242…`, preserved at `tools/interim/` with its run at
`../interim/M8b-v2-5of5-noncanonical-reqpaths5.out`) the pass path printed
`REFERENCE-COVERAGE: 5/5 paths present in reference; unaccounted: <4 paths>` —
a self-contradictory line (5/5 present *and* 4 unaccounted) — which is how this
residual was found. At the landed revision the line is only printed on the
failure path, so the padded receipt passes **silently** (0 occurrences of
`REFERENCE-COVERAGE` in `M18`/`M19`/`M8b`).

Scope note: this is not the D4 forgery boundary. No field is tampered and no
digest is forged — a receipt built by the tool itself and then padded, or simply
a receipt over a different 5-path set, satisfies the gate the claim offers as the
D3 close. The frozen claim's own words are "the other four custody paths
unexamined"; under padding they still are.

## Change (one line, plus a wording fix)

```python
# custody-pair.py, reference_coverage() (~line 591)
-def reference_coverage(ref_sections, required: int) -> tuple[bool, str]:
+def reference_coverage(ref_sections, required: int) -> tuple[bool, str]:
     have = {Path(s["path"]).expanduser().resolve() for s in ref_sections}
     unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in have]
     line = ("REFERENCE-COVERAGE: %d/%d paths present in reference; unaccounted: %s"
-            % (len(ref_sections), required, " ".join(unaccounted) if unaccounted else "(none)"))
-    return len(ref_sections) >= required, line
+            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
+    return len(have) >= required, line
```

Rationale: the count and the `unaccounted` list then share one basis (distinct
resolved paths), and duplicate padding no longer changes the verdict. The
`verify` USAGE message `reference covers %d of the required %d paths` should use
the same basis (`len(have)`), so the printed number matches the count.

Optional, if the parent wants the stronger form of the D3 close (pick one):

- `--require-custody-set` (identity gate): exit 2 unless every canonical path
  (or, for a `--paths`-scoped run, every scoped path) is present by resolved
  identity — the count-based gate then remains the weaker, compatible option.
- default-on gate: `--require-paths 5` implied when the reference names any
  canonical custody path and no explicit `--paths` scope was in force.

## Selftest vector to add with the change

```
case coverage-gate-rejects-duplicate-stanzas   # 5× same path, --require-paths 5 → exit 2
case coverage-gate-passes-distinct-five        # 5 distinct paths                → exit 0
```

Both are fixture-only (scratch dir), no custody path touched.