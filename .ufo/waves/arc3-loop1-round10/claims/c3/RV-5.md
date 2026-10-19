# RV-5 — C3 G21 Frontier tail coverage

## Verdict

- **Live tail gap — REPRODUCED.** At HEAD `5694506a862c32d2f7aac44935778bce4b6184f2`, the gate is SHA-256 `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. The live `PROVINCE.md` has 162 lines; the G21 register's last span ends at line 162 (`.ufo/gates/c1-census-v10.py:292-308`; `PROVINCE.md:133-162`). `frontier_check()` checks only the fixed `FRONTIER` entries (`.ufo/gates/c1-census-v10.py:422-444`), so a new bullet after that bound is not enumerated.
- **Seeded current behavior — REPRODUCED, silent PASS.** A scratch copy with a new bullet at line 163 still reports 14 rows, no G21 errors or declared fail classes, and PASS / exit 0.
- **Patch behavior — REPRODUCED on scratch only.** The patch below preserves PASS on the clean copy and reports `FRONTIER-UNDECLARED`, line 163, FAIL / exit 1 on that same seeded copy. This is proposed text only; I did not edit the live gate or any custody/corpus/tracked file.

## First-hand measurement

The clean live invocation `python3 .ufo/gates/c1-census-v10.py --json` exited 0 with `"verdict": "PASS"`, `"frontier_rows": 14`, and `"frontier_errors": []`. For the controlled before/after measurement, I copied `PROVINCE.md`, `SCORECARD.md`, and `SKILL.md` under `/var/tmp/rv5-g21-hqe8bxl1` and ran the gate as `python3 <gate-copy> --root <scratch-root> --quiet`. The temporary directory was automatically removed after measurement.

Exact decisive output from the four scratch runs:

```text
--- unpatched clean scratch (exit=0) ---
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
--- unpatched seeded scratch (exit=0) ---
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
--- patched clean scratch (exit=0) ---
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
FRONTIER coverage (G21): unregistered bullets: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
--- patched seeded scratch (exit=1) ---
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
FRONTIER coverage (G21): unregistered bullets: ['PROVINCE.md:163 unregistered Frontier bullet (G21)']
DECLARED FAIL CLASSES: ['FRONTIER-UNDECLARED']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Seed inserted only in the scratch copy: `- **Synthetic tail probe** — no G21 row covers this appended claim.` The existing fixed-row check gives no error because its loop runs over `FRONTIER`, not actual bullet starts (`.ufo/gates/c1-census-v10.py:429-444`). The proposed extra check scans the two named Frontier sections and fails a bullet start not covered by a register span. It leaves all existing G21 row checks intact.

## Proposed patch text (not applied)

Exact diff against the measured gate source:

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -444,6 +444,36 @@
     return errs
 
 
+def frontier_coverage_check(filelines):
+    """G21: reject Frontier bullets that no register span covers."""
+    errs = []
+    f = "PROVINCE.md"
+    lines = filelines.get(f)
+    if lines is None:
+        return errs
+    for heading, level in (("## Frontier", 2),
+                           ("### Round-4 frontier (post-unlock)", 3)):
+        start = next((i for i, line in enumerate(lines) if line == heading), None)
+        if start is None:
+            errs.append("%s heading %r missing (G21)" % (f, heading))
+            continue
+        end = len(lines)
+        for i in range(start + 1, len(lines)):
+            m = re.match(r"^(#{1,6})\s", lines[i])
+            if m and len(m.group(1)) <= level:
+                end = i
+                break
+        for i in range(start + 1, end):
+            if BULLET.match(lines[i]):
+                line_no = i + 1
+                covered = any(row[0] == f and row[1] <= line_no <= row[2]
+                              for row in FRONTIER)
+                if not covered:
+                    errs.append("%s:%d unregistered Frontier bullet (G21)"
+                                % (f, line_no))
+    return errs
+
+
 def cache_versions():
     """G17: every version present in an npx rea-agents cache."""
     vers = set()
@@ -631,6 +661,7 @@
         counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
     scope_errors = assert_markers(filelines)
     frontier_errors = frontier_check(filelines)
+    frontier_coverage_errors = frontier_coverage_check(filelines)
     stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
     undecl = out.get("UNDECLARED", [])
     unres = out.get("UNRESOLVED", [])
@@ -666,10 +697,13 @@
     g2_ok = h3_ok
     frontier_class = (["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors)
                       else ["FRONTIER-UNEVALUABLE"] if frontier_errors else [])
+    if frontier_coverage_errors:
+        frontier_class.append("FRONTIER-UNDECLARED")
     declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"]) \
                + frontier_class
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors)
+         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors) \
+         and (not frontier_coverage_errors)
     verdict = "PASS" if ok else "FAIL"
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
@@ -677,6 +711,7 @@
                           "unresolved": unres, "scope_errors": scope_errors,
                           "unreadable": unreadable, "declared_fail_classes": declared,
                           "frontier_rows": len(FRONTIER), "frontier_errors": frontier_errors,
+                          "frontier_coverage_errors": frontier_coverage_errors,
                           "g2_ok": g2_ok, "g2_floor": "1/readable-file", "current_ok_per_file": floor,
                           "g11": g11, "g7": g7,
                           "historical": out.get("historical", []),
@@ -700,6 +735,7 @@
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
     print("FRONTIER register (G21): %d rows asserted, errors: %r"
           % (len(FRONTIER), frontier_errors))
+    print("FRONTIER coverage (G21): unregistered bullets: %r" % frontier_coverage_errors)
     print("UNREADABLE (could-not-evaluate): %r" % unreadable)
     print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
           % ("ok" if g2_ok else "SUSPECT",
 ```

## Boundary

This demonstrates the frozen C3 before/after condition against the current gate without changing it: before, the synthetic appended bullet is silently accepted; with the proposed guard in a scratch gate, it is explicitly undeclared and fails, while the clean fixture remains PASS. The section-heading parser and extra JSON/text reporting are part of the proposed diff; no post-integration or live-gate result is claimed.
