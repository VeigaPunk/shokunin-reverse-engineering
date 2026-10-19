# RV-8 — C3 instrument gap measurement

**Chain:** c3 (instrument/custody)  
**Verdict:** **VERIFIED** — the G21 tail-append residual reproduces; the proposed guard catches it on a scratch copy. No instrument or tracked file was edited.

## Re-derived evidence

- `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `git show -s --format='%H %s' 5694506 eb5a2c4` independently resolved the recorded/work commits.
- Read `PROVINCE.md:133-162`; the `### Round-4 frontier (post-unlock)` section ends at line 162. G21 has 14 explicit rows; its last row is `PROVINCE.md:161-162` (`.ufo/gates/c1-census-v10.py:292-308`).
- Current gate source confirms the gap: `frontier_check` tests only declared `FRONTIER` slices (`.ufo/gates/c1-census-v10.py:422-444`); the root read only rejects files shorter than the maximum declared end (`:607-633`). It does not look for new bullets after the final row. The existing frontier errors already become `FRONTIER-UNEVALUABLE` and fail the verdict (`:667-672`), and are emitted in JSON (`:675-682`).

Baseline command:

```bash
python3 .ufo/gates/c1-census-v10.py --root "$PWD" --json
```

Relevant observed JSON fields: `PROVINCE.md: {"lines": 162, "loci": 6}`, `frontier_rows: 14`, `frontier_errors: []`, `declared_fail_classes: []`, `verdict: "PASS"` (exit 0). The same run derived anchors `devin=6.5.0`, `omp=6.5.0`, `kimi=6.7.0`.

## Seeded-fault measurements (scratch only)

Scratch root: `/var/tmp/kaidoku-rv8-bspABc/root`. It contains copies of `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md`; the injected line was exactly:

```text
- **RV-8 seeded tail** — new Frontier bullet with no registered row.
```

It was appended as line 163, after the observed 162-line source. With the unmodified gate:

```bash
python3 .ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-rv8-bspABc/root --json
```

Observed selected JSON: `PROVINCE.md: {"lines": 163, "loci": 6}`, `frontier_rows: 14`, `frontier_errors: []`, `declared_fail_classes: []`, `verdict: "PASS"` (exit 0). Thus the locus-free added bullet is outside every registered slice and passes silently.

I applied the proposed code below only to a scratch copy of the gate (`/var/tmp/kaidoku-rv8-bspABc/c1-proposed.py`), then re-ran the same seeded root. It returned exit 1 with:

```json
{"counts": {"PROVINCE.md": {"lines": 163, "loci": 6}, "SCORECARD.md": {"lines": 1924, "loci": 11}, "SKILL.md": {"lines": 413, "loci": 2}}, "declared_fail_classes": ["FRONTIER-UNEVALUABLE"], "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet beyond declared tail :162 (FRONTIER-UNEVALUABLE)"], "frontier_rows": 14, "verdict": "FAIL"}
```

As a no-regression control, the same patched scratch gate against the unmodified repository root returned `frontier_errors: []`, `declared_fail_classes: []`, `verdict: "PASS"` (exit 0). The source gate remained unchanged (`git diff -- .ufo/gates/c1-census-v10.py` was empty).

## Proposed patch text — not applied

```diff
@@
 FRONTIER = [
@@
     ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\bIDA\b"], []),
 ]
+
+# Re-key with the last G21 row when this Frontier section changes.
+FRONTIER_TAILS = [
+    ("PROVINCE.md", "### Round-4 frontier (post-unlock)", 162),
+]
@@
 def frontier_check(filelines):
@@
     return errs
+
+
+def frontier_tail_check(filelines):
+    """G22: reject bullets after the last declared Frontier register row."""
+    errs = []
+    for (f, heading, tail) in FRONTIER_TAILS:
+        lines = filelines.get(f)
+        if lines is None:
+            continue
+        hits = [i for i, line in enumerate(lines) if line.strip() == heading]
+        if len(hits) != 1:
+            errs.append("%s Frontier heading %r occurs %d times (FRONTIER-UNEVALUABLE)"
+                        % (f, heading, len(hits)))
+            continue
+        start = hits[0]
+        stop = next((i for i in range(start + 1, len(lines))
+                     if re.match(r"^#{1,3} ", lines[i])), len(lines))
+        section_start = start + 1
+        if not section_start < tail <= stop:
+            errs.append("%s:%d declared Frontier tail :%d outside section (FRONTIER-UNEVALUABLE)"
+                        % (f, section_start, tail))
+            continue
+        rows = [r for r in FRONTIER
+                if r[0] == f and section_start <= r[1] < stop]
+        register_tail = max((r[2] for r in rows), default=None)
+        if register_tail != tail:
+            errs.append("%s:%d declared Frontier tail :%d differs from G21 register tail %r (FRONTIER-UNEVALUABLE)"
+                        % (f, section_start, tail, register_tail))
+        for i in range(tail, stop):
+            if BULLET.match(lines[i]):
+                errs.append("%s:%d unregistered Frontier bullet beyond declared tail :%d (FRONTIER-UNEVALUABLE)"
+                            % (f, i + 1, tail))
+    return errs
@@
-    frontier_errors = frontier_check(filelines)
+    frontier_errors = frontier_check(filelines) + frontier_tail_check(filelines)
```

The proposed tail check resolves the named residual without editing or widening `SCOPE`: it requires the configured tail to equal the final G21 row for the named section, scans unregistered section lines after that boundary, and reuses the existing declared `FRONTIER-UNEVALUABLE` verdict path.
