# Proposed patch text (NOT applied) — fail-closed on an absent scoped file

Seat RV-11 (reviewer, chain c3). Target: `.ufo/gates/c1-census-v10.py` (EX-28's
write; this seat did not touch it). Motivated by attack A5, measured:

```
$ mkdir scratch/atk-missing && cp PROVINCE.md SCORECARD.md scratch/atk-missing/   # SKILL.md absent
$ python3 .ufo/gates/c1-census-v10.py --root scratch/atk-missing --quiet
SKILL.md       lines=0    loci=0
SCOPE-ERRORS (marker assertions): []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)     exit=0
```

An absent/unreadable scoped file whose declared rows are all CURRENT (SKILL.md:
`c1-census-v10.py:94-95`) is silently absorbed as `lines=0 loci=0`; the run still
reports PASS. (SCORECARD.md or PROVINCE.md absent → FAIL, because their DATED rows
trip `assert_markers`.) A deleted or renamed file can therefore shrink the census
without a reading — the same class G6 exists to prevent for growth.

Minimal change, in `main()` (current code at `c1-census-v10.py:382-390`):

```diff
-    out, counts, filelines = {}, {}, {}
+    out, counts, filelines, unreadable = {}, {}, {}, []
     for f in files:
         try:
             lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
-        except OSError:
+        except OSError as ex:
+            unreadable.append("%s: %s" % (f, type(ex).__name__))
             counts[f] = {"lines": 0, "loci": 0}
             filelines[f] = None
             continue
```

and in the verdict expression (`c1-census-v10.py:397-398`):

```diff
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok
+         and (not g11) and g2_ok and (not unreadable)
```

plus a line in the text report next to `SCOPE-ERRORS`, e.g.
`print("UNREADABLE (could-not-evaluate): %r" % unreadable)`.

Semantics: an absent scoped file becomes the declared could-not-evaluate class
(reported, non-zero exit) instead of a silent PASS. Not required for the E22
disposition (not exercised at HEAD: all three files present and byte-identical to
their HEAD blobs); offered as hardening for the next instrument touch.
