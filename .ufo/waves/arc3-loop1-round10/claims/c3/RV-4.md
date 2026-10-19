# RV-4 — C3 instrument patch draft

**Chain:** `c3` — operability. **Claim:** close the G21 Frontier-register residual by detecting Frontier bullets that are outside the explicit register. This is patch text and scratch evidence only; neither the live instrument nor a custody tool was edited.

## Re-derived state and verdicts

- **Revision identity — VERIFIED.** `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `git rev-parse eb5a2c4` → `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. The gate source hash measured by `sha256sum .ufo/gates/c1-census-v10.py` was `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.
- **Current G21 baseline — VERIFIED.** Source code declares 14 `FRONTIER` rows (`.ufo/gates/c1-census-v10.py:292-308`); the independent run reports `FRONTIER register (G21): 14 rows asserted, errors: []`. The live `PROVINCE.md` is 162 lines and the untouched current gate returns PASS.
- **Append-past-boundary residual — REPRODUCED.** `PROVINCE.md:133-162` is the second Frontier region, and `:162` is the source file's EOF. A scratch-only new Frontier bullet at :163 is read by the gate but not checked: current source still reports no frontier errors and PASS exit 0.
- **Patch behavior — VERIFIED on scratch.** Applying the diff below to a scratch copy preserves baseline PASS and rejects that same :163 seed as `FRONTIER-UNEVALUABLE`, exit 1.
- **Live source change — NOT APPLIED by design.** The task requires patch TEXT and a scratch measurement, not an instrument edit. The current gate remains unchanged.

The gap is visible in the live implementation: `main()` computes the declared maximum line (`:614-615`) and only rejects files *shorter* than it (`:623-629`); `frontier_check()` grades only the listed rows and returns (`:422-444`). The result is passed through the declared `FRONTIER-UNEVALUABLE` classification and verdict (`:667-684`). G21's prose records the same boundary (`:95-116`), but that prose does not enforce it.

## Proposed gate patch text — do not apply from this seat

Insert inside `frontier_check(filelines)`, after the existing `for (f, s, e, req, forb) in FRONTIER` loop and before its `return errs` (`.ufo/gates/c1-census-v10.py:429-444`):

```diff
@@
         for pat in forb:
             m = re.search(pat, seg, re.I)
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    prov = filelines.get("PROVINCE.md")
+    if prov is not None:
+        declared_starts = {s for f, s, e, req, forb in FRONTIER if f == "PROVINCE.md"}
+        declared_end = max(e for f, s, e, req, forb in FRONTIER if f == "PROVINCE.md")
+        active_level = None
+        for n, line in enumerate(prov, 1):
+            heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
+            if heading:
+                heading_level = len(heading.group(1))
+                title = heading.group(2)
+                if heading_level in (2, 3) and re.match(
+                        r"^(?:Frontier|Round-4 frontier)(?:\s|$)", title, re.I):
+                    active_level = heading_level
+                elif active_level is not None and heading_level <= active_level:
+                    active_level = None
+                continue
+            if active_level is not None and re.match(r"^\s*[-*+]\s+", line) \\
+                    and n not in declared_starts:
+                errs.append("PROVINCE.md:%d undeclared Frontier bullet (G21 register ends at :%d)" %
+                            (n, declared_end))
     return errs
```

The check is limited to the two named Frontier headings. It permits only registered bullet start lines; an unregistered list item is appended to `frontier_errors`, which the existing classifier grades as `FRONTIER-UNEVALUABLE`. It derives the bound from `FRONTIER`, rather than pinning `162` in code. Existing declared-row anchor checks remain intact.

## Scratch measurement

All inputs and the copied gate were under `/var/tmp/rv4-g21-exact.sLAba2/`; no scratch input was written into the repository. The clean and fault roots each held copies of `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md`. Seed operation asserted the original had 162 lines and a final newline, then appended exactly one bullet, producing line 163 (no intervening blank line). Gate run commands:

```sh
python3 /var/tmp/rv4-g21-exact.sLAba2/gate-current.py --root /var/tmp/rv4-g21-exact.sLAba2/base --quiet
python3 /var/tmp/rv4-g21-exact.sLAba2/gate-current.py --root /var/tmp/rv4-g21-exact.sLAba2/fault --quiet
python3 /var/tmp/rv4-g21-exact.sLAba2/gate-patched.py --root /var/tmp/rv4-g21-exact.sLAba2/base --quiet
python3 /var/tmp/rv4-g21-exact.sLAba2/gate-patched.py --root /var/tmp/rv4-g21-exact.sLAba2/fault --quiet
```

Exact relevant stdout from the current-gate baseline:

```text
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Seed operation output:

```text
seeded line=163; resulting lines=163; text='- **RV-4 seeded fault** — unregistered Frontier claim appended after the declared register bound.'
```

Exact relevant stdout from the current gate on that seed:

```text
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
current seeded-fault exit=0
```

Exact relevant stdout from the patched scratch gate on the clean baseline:

```text
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Exact relevant stdout from the patched scratch gate on the same seed:

```text
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 undeclared Frontier bullet (G21 register ends at :162)']
DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
patched seeded-fault exit=1
```

A first scratch attempt accidentally inserted a blank line before the bullet and was discarded; the final rerun above appends directly after the existing trailing newline and is the evidence for this claim.

## Reproduction recipe

From the lane repo, create two scratch roots under `/var/tmp`, copy `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md` into each, and copy `.ufo/gates/c1-census-v10.py` to a scratch gate. Run the copied gate against the clean root. In the second root append only `- **RV-4 seeded fault** — unregistered Frontier claim appended after the declared register bound.` plus its final newline; verify it is line 163, then rerun the current gate. For the after measurement, apply the diff above only to the copied gate and rerun against both roots. Expected oracle: current gate `PASS / exit 0` on both roots; patched scratch gate `PASS / exit 0` on clean and `FRONTIER-UNEVALUABLE / exit 1` on the seeded root.
