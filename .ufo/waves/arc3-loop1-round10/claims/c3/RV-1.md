# RV-1 — G21 appended-frontier boundary

**Claim:** C3 operability, gate patch proposal. I selected the G21 register residual; no gate or custody source was edited.

## First-hand findings

- **VERIFIED — checkout identity.** `git rev-parse HEAD` returned `5694506a862c32d2f7aac44935778bce4b6184f2`.
- **VERIFIED — current baseline.** `python3 .ufo/gates/c1-census-v10.py --json` returned `verdict: PASS`, `counts.PROVINCE.md.lines: 162`, `frontier_rows: 14`, and `frontier_errors: []` (same values in the retained `source_baseline` run in `evidence/g21-seeded-measurement.json`).
- **VERIFIED — declared residual.** `.ufo/gates/c1-census-v10.py:114-116` explicitly states a new bullet past `:162` sits outside the register. `FRONTIER` is a fixed list at `.ufo/gates/c1-census-v10.py:292-308`; `frontier_check()` tests only those spans at `:422-444`. The current `PROVINCE.md` has its final registered bullet at `:161-162` and ends at line 162 (`PROVINCE.md:161-162`).
- **REPRODUCED — seeded fault passes silently.** On a scratch document root, I appended `- **RV-1 synthetic unregistered frontier** — seeded G21 boundary fault.` at line 163. The unmodified gate returned exit 0 / `PASS`, with `frontier_errors: []` and no declared fail classes.
- **REPRODUCED — proposed guard detects it without baseline regression.** The patch below was applied only to a scratch copy of the gate. Scratch baseline stayed exit 0 / `PASS`; the seeded copy returned exit 1 / `FAIL`, `frontier_errors: ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"]`, and `declared_fail_classes: ["FRONTIER-UNEVALUABLE"]`.

Exact seeded-measurement command:

```bash
python3 .ufo/waves/arc3-loop1-round10/claims/c3/RV-1/evidence/g21-seeded-measurement.py
```

Its summary output:

```json
{
  "scratch_root": "/var/tmp/kaidoku-rv1-g21-kstoyfei",
  "seeded_bullet_line": 163,
  "checks": {
    "source_baseline_passes": true,
    "source_seeded_passes_silently": true,
    "candidate_baseline_passes": true,
    "candidate_seeded_flags_unregistered_bullet": true
  },
  "cases": {
    "source_baseline": {"exit_code": 0, "verdict": "PASS", "frontier_errors": [], "declared_fail_classes": []},
    "source_seeded": {"exit_code": 0, "verdict": "PASS", "frontier_errors": [], "declared_fail_classes": []},
    "candidate_baseline": {"exit_code": 0, "verdict": "PASS", "frontier_errors": [], "declared_fail_classes": []},
    "candidate_seeded": {
      "exit_code": 1,
      "verdict": "FAIL",
      "frontier_errors": ["PROVINCE.md:163 unregistered Frontier bullet (FRONTIER-UNEVALUABLE)"],
      "declared_fail_classes": ["FRONTIER-UNEVALUABLE"]
    }
  }
}
```

The script records each exact command and full JSON stdout in `evidence/g21-seeded-measurement.json`; the reusable harness is `evidence/g21-seeded-measurement.py`. Scratch inputs and patched gate are under `/var/tmp/kaidoku-rv1-g21-kstoyfei/`.

## Proposed gate patch text (not applied to the instrument)

Also saved as `evidence/g21-frontier-coverage.patch`.

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -441,6 +441,27 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    lines = filelines.get("PROVINCE.md")
+    if lines is not None:
+        registered = [(s, e) for f, s, e, _, _ in FRONTIER if f == "PROVINCE.md"]
+        for heading, level in (
+            ("## Frontier", 2),
+            ("### Round-4 frontier (post-unlock)", 3),
+        ):
+            starts = [i for i, line in enumerate(lines) if line.strip() == heading]
+            if len(starts) != 1:
+                errs.append("PROVINCE.md heading %r occurs %d times (G21 frontier register)"
+                            % (heading, len(starts)))
+                continue
+            start = starts[0]
+            for i in range(start + 1, len(lines)):
+                h = re.match(r"^(#{1,6})\s+", lines[i])
+                if h and len(h.group(1)) <= level:
+                    break
+                if BULLET.match(lines[i]) and not any(s <= i + 1 <= e
+                                                       for s, e in registered):
+                    errs.append("PROVINCE.md:%d unregistered Frontier bullet "
+                                "(FRONTIER-UNEVALUABLE)" % (i + 1))
     return errs
```

This discovers bullets under each named Frontier heading through the next same-or-higher-level heading and requires each to be covered by an existing G21 span. A missing or duplicated heading is also unevaluable. The intended behavior change is limited to reporting an unregistered bullet through the existing `frontier_errors`/`FRONTIER-UNEVALUABLE` failure path; current span checks remain unchanged.

**Disposition:** defect reproduced; patch text and scratch seeded measurement delivered. The live instrument remains unmodified, as required by the seat scope.