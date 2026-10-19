# RV-3 — C3 G21 Frontier register completeness

## Verdict

- **Existing append-past-`:162` gap — REPRODUCED.** The committed gate passes with an unregistered Frontier bullet appended at `PROVINCE.md:163`.
- **Candidate check — REPRODUCED on scratch.** The patch below preserves the unmodified baseline as PASS and grades that seeded bullet `FRONTIER-UNEVALUABLE` / FAIL.
- No gate or custody instrument was edited; this artifact contains patch text only.

## First-hand re-derivation

At `HEAD=5694506a862c32d2f7aac44935778bce4b6184f2`, `git show HEAD:.ufo/gates/c1-census-v10.py | sha256sum` yields `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. `git show HEAD:PROVINCE.md | wc -l` yields `162`.

- The G21 register contains 14 rows, as independently returned by the instrument's `frontier_rows` field. The rows are at `.ufo/gates/c1-census-v10.py:292-308`; the final registered span is `PROVINCE.md:161-162` (`:307`).
- `main()` sets each file's `max_end` from the scope and Frontier rows (`.ufo/gates/c1-census-v10.py:613-615`) and only rejects files shorter than that bound (`:623-629`). `frontier_check()` tests only the declared spans (`:422-444`); it does not discover additional Frontier bullets.
- The source Frontier headings are `PROVINCE.md:73` and `:133`; the file ends at `:162`. A seeded appended bullet therefore remains in the final Frontier subsection without a new heading.

The current gate invocation (`python3 .ufo/gates/c1-census-v10.py --root <repo> --json`; the harness projected the listed fields from its JSON) returned:

```text
HEAD_GATE={"declared_fail_classes": [], "exit": 0, "frontier_errors": [], "frontier_rows": 14, "province_lines": 162, "verdict": "PASS"}
```

I copied the four inputs (`c1-census-v10.py`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`) from the named Git revision into `/var/tmp/rv3-g21-final-rmk49w4f/{baseline,seeded}`. The seeded copy adds one Markdown bullet at line 163; no repository input was modified. The committed gate produced:

```text
BEFORE_BASELINE={"declared_fail_classes": [], "exit": 0, "frontier_errors": [], "frontier_rows": 14, "province_lines": 162, "verdict": "PASS"}
BEFORE_SEEDED={"declared_fail_classes": [], "exit": 0, "frontier_errors": [], "frontier_rows": 14, "province_lines": 163, "verdict": "PASS"}
```

This reproduces the silent-pass residual: file growth from 162 to 163 is accepted, with no frontier error.

## Patch text (not applied to the instrument)

Insert into `frontier_check()` after its existing register-row loop and before `return errs` (`.ufo/gates/c1-census-v10.py:429-444`):

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -441,6 +441,21 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    # G21 completeness: every bullet in a Frontier section must have a row.
+    registered = {(f, s) for (f, s, e, req, forb) in FRONTIER}
+    for f in sorted({row[0] for row in FRONTIER}):
+        lines = filelines.get(f)
+        if not lines:
+            continue
+        frontier_level = None
+        for i, line in enumerate(lines):
+            heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
+            if heading:
+                level = len(heading.group(1))
+                if frontier_level is not None and level <= frontier_level:
+                    frontier_level = None
+                if re.search(r"\bfrontier\b", heading.group(2), re.I):
+                    frontier_level = level
+                continue
+            if frontier_level is not None and BULLET.match(line):
+                location = (f, i + 1)
+                if location not in registered:
+                    errs.append("%s:%d unregistered Frontier bullet (G21 frontier register)"
+                                % location)
     return errs
```

The check uses the existing `BULLET` regex and the registered row start coordinates; it does not treat line 75's registered prose row as a missing Markdown bullet. A bullet under a heading containing “Frontier” that lacks a registered start line adds a G21 error; the existing verdict mapping classifies a non-stale frontier error as `FRONTIER-UNEVALUABLE` (`:667-672`).

## Candidate patch measurement

I applied only the above text to a scratch copy of the gate, then ran the same `--json` invocation against the unchanged and seeded scratch roots:

```text
PATCHED_BASELINE={"declared_fail_classes": [], "exit": 0, "frontier_errors": [], "frontier_rows": 14, "province_lines": 162, "verdict": "PASS"}
PATCHED_SEEDED={"declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "exit": 1, "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (G21 frontier register)"], "frontier_rows": 14, "province_lines": 163, "verdict": "FAIL"}
```

This is a scratch-only proposed behavior, not a landed gate change. The detector is deliberately scoped to Markdown bullets under headings containing “Frontier”; it does not claim to detect non-bullet prose or content under a renamed heading.
