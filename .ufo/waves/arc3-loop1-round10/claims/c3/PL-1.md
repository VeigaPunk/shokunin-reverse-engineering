# PL-1 — C3 G21 frontier register completeness

## Claim and result

**REPRODUCED — current gap.** G21 validates only the 14 explicitly listed `FRONTIER` rows (gate `:292-308`, `:422-444`). The code computes `frontier_errors` by calling `frontier_check(filelines)` (`:632-633`); it does not enumerate bullet starts in the two Frontier sections. The last row ends at `PROVINCE.md:162`; `PROVINCE.md` is 162 lines at HEAD. A synthetic Frontier bullet appended at line 163 is outside every row and passes silently.

**REPRODUCED — proposed guard.** A scratch-only candidate that enumerates bullet starts under `## Frontier` and `### Round-4 frontier (post-unlock)` keeps the unmodified HEAD baseline PASS and flags the synthetic line-163 bullet as `FRONTIER-UNEVALUABLE` (exit 1). This is patch text only; neither the gate nor any custody source was edited.

## Re-derived identity and baseline

Commands/results:

```text
$ git rev-parse HEAD
5694506a862c32d2f7aac44935778bce4b6184f2
$ sha256sum .ufo/gates/c1-census-v10.py
a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b  .ufo/gates/c1-census-v10.py
$ git show HEAD:.ufo/gates/c1-census-v10.py | sha256sum
a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b  -
```

HEAD and worktree gate bytes match. The target docs for both runs were extracted with `git archive HEAD PROVINCE.md SKILL.md SCORECARD.md` into `/var/tmp/kaidoku-pl1-KRj2qG/base`; the fault copy is `/var/tmp/kaidoku-pl1-KRj2qG/seeded163`.

Baseline command:

```text
python3 .ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-pl1-KRj2qG/base --quiet
```

Relevant exact output:

```text
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1924 loci=11
SKILL.md       lines=413  loci=2
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
BASELINE_EXIT=0
```

Seed: append exactly `- **PL-1 seeded-fault** — synthetic Frontier bullet past the registered boundary.` after the existing final newline. Re-derived result: `PROVINCE.md` has 163 lines and this bullet is line 163. Unpatched command:

```text
python3 .ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-pl1-KRj2qG/seeded163 --quiet
```

Relevant exact output:

```text
PROVINCE.md    lines=163  loci=6
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
SEEDED_EXIT=0
```

The live anchors re-derived in both runs were `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`. The silent PASS is explained by the current fixed-row loop (`:429-444`) and verdict only requiring `frontier_errors` to be empty (`:667-672`); the SCOPE loop also only reads through each declared `max_end` (`:613-633`).

## Proposed gate patch text (not applied)

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -419,13 +419,39 @@
     return errs
 
 
+def frontier_bullet_starts(lines):
+    active_level = None
+    starts = set()
+    for n, line in enumerate(lines, 1):
+        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
+        if heading:
+            level = len(heading.group(1))
+            if active_level is not None and level <= active_level:
+                active_level = None
+            if heading.group(2) in ("Frontier", "Round-4 frontier (post-unlock)"):
+                active_level = level
+            continue
+        if active_level is not None and BULLET.match(line):
+            starts.add(n)
+    return starts
+
+
 def frontier_check(filelines):
     """G21 (r10): assert the frontier-claim register directly on bullet text.
     Locus-free bullets never reach classify(), so this is the only grading
-    they get: REQUIRED anchors are the positive floor (a stripped, rewritten
-    or truncated bullet fails REQUIRED-absent), FORBIDDEN literals name the
-    retracted claims whose reintroduction must fail the run (FRONTIER-STALE)."""
+    they get: REQUIRED anchors are the positive floor, FORBIDDEN literals are
+    stale claims, and every Frontier bullet must have a registered row."""
     errs = []
+    for f in sorted({row[0] for row in FRONTIER}):
+        lines = filelines.get(f)
+        if lines is None:
+            continue
+        actual = frontier_bullet_starts(lines)
+        declared = {s for rf, s, e, req, forb in FRONTIER
+                    if rf == f and 1 <= s <= len(lines) and BULLET.match(lines[s - 1])}
+        for n in sorted(actual - declared):
+            errs.append("%s:%d frontier bullet has no G21 row (G21 frontier register)"
+                        % (f, n))
     for (f, s, e, req, forb) in FRONTIER:
         lines = filelines.get(f)
         if not lines:
```

The appended error does not contain `FORBIDDEN`, so the existing classifier at `:667-668` assigns `FRONTIER-UNEVALUABLE`; the existing verdict path then fails the run.

## Candidate validation on scratch only

I copied the gate to `/var/tmp/kaidoku-pl1-KRj2qG/candidate/c1-census-v10.py`, applied the proposed hunk to that copy, and ran `python3 -m py_compile` successfully. These were the candidate results:

```text
$ python3 /var/tmp/kaidoku-pl1-KRj2qG/candidate/c1-census-v10.py --root /var/tmp/kaidoku-pl1-KRj2qG/base --quiet
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
PATCHED_BASELINE_EXIT=0

$ python3 /var/tmp/kaidoku-pl1-KRj2qG/candidate/c1-census-v10.py --root /var/tmp/kaidoku-pl1-KRj2qG/seeded163 --quiet
FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 frontier bullet has no G21 row (G21 frontier register)']
DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
PATCHED_SEEDED_EXIT=1
```

## Scope

No gate, custody tool, corpus, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, or `LOG.md` change is included in this seat artifact. This seat wrote only `claims/c3/PL-1.md` in the repository; the candidate code and faulted docs are isolated under `/var/tmp`.
