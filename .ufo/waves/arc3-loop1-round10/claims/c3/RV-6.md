# RV-6 — C3 G21 append-past-:162 guard

Claim: extend the G21 register's self-check so an unregistered Frontier bullet is `FRONTIER-UNEVALUABLE`. This is **patch text only**; I did not modify the gate, custody tool, or any tracked source file.

## First-hand re-derivation

- **HEAD / source state — VERIFIED.** `git rev-parse HEAD` returned `5694506a862c32d2f7aac44935778bce4b6184f2`. `git diff -- .ufo/gates/c1-census-v10.py PROVINCE.md` produced no output. The current gate file SHA-256 was `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.
- **Register and source extent — VERIFIED.** I parsed the `FRONTIER` assignment with Python AST and counted the source lines; output: `frontier_rows=14 province_lines=162`. Source locations: `.ufo/gates/c1-census-v10.py:292-308` declares the 14 rows; `:422-444` checks only those rows; `.ufo/gates/c1-census-v10.py:633` calls that checker. `PROVINCE.md:133-162` ends the named Round-4 Frontier section, with the last registered row at `.ufo/gates/c1-census-v10.py:307`.
- **Live baseline — REPRODUCED.** Command: `python3 .ufo/gates/c1-census-v10.py --json` (exit 0). Exact result fields: `"lines": 162`, `"verdict": "PASS"`, `"frontier_rows": 14`, `"frontier_errors": []`, `"declared_fail_classes": []`.
- **Gap on the existing gate — REPRODUCED.** Scratch tree: `/dev/shm/kaidoku-rv6-final-9vj8osw9/fault`; appended `- **RV-6 seeded-fault** — synthetic unregistered bullet.` to copied `PROVINCE.md`, making it 163 lines. Command: `python3 /dev/shm/kaidoku-rv6-final-9vj8osw9/c1-census-v10-before.py --root /dev/shm/kaidoku-rv6-final-9vj8osw9/fault --quiet` (exit 0). Exact decisive output:

  ```text
  PROVINCE.md    lines=163  loci=6
  FRONTIER register (G21): 14 rows asserted, errors: []
  DECLARED FAIL CLASSES: []
  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
  ```

## Proposed patch text (not applied)

The heading scan is anchored by exact level/title, ends at the next equal-or-higher-level heading or EOF, and requires each bullet start to equal a registered row start. Missing/duplicate headings are unevaluable too. Existing main-path classification turns these non-`FORBIDDEN` frontier errors into `FRONTIER-UNEVALUABLE` (`.ufo/gates/c1-census-v10.py:667-672`).

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -110,10 +110,14 @@
 declared fail classes (FRONTIER-STALE for a FORBIDDEN match, FRONTIER-UNEVALUABLE
 for a REQUIRED-absent or uncheckable row), reported in text and --json. G21
 rows are keyed to the r5-audit tree; any frontier edit re-keys the register in
-the same commit — the same standing rule as the records-commit bound. Residual,
-named: a brand-new bullet appended past :162 (the register's last declared
-line) sits outside the register until re-keyed — the same past-the-bound
-residual the records-commit rule already governs for SCORECARD.md:856+."""
+the same commit — the same standing rule as the records-commit bound.
+Closed here: a self-check resolves the two named Frontier headings and fails
+FRONTIER-UNEVALUABLE when a bullet start is not a registered FRONTIER[] start.
+Section scanning ends at the next heading of equal or higher depth (or EOF),
+so an appended bullet past the prior :162 bound is included. Residual, named:
+non-bullet continuation text added beyond a registered span is still governed
+only by that row's REQUIRED/FORBIDDEN patterns; re-key each edited span in the
+same commit."""
 #!/usr/bin/env python3
 """C1 census instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; the
 v9-era structure and claim text below are retained as the instrument's history,
@@ -216,16 +220,17 @@
   G21 frontier-claim register            (r10, R1 residual): Frontier bullets
                                            (PROVINCE.md :73-93, :133-162)
                                            carry no pin/version/path loci, so
-                                           L3 never fires on them and v10 read
-                                           PASS identically whether or not a
-                                           frontier bullet was stale; the
-                                           FRONTIER[] register asserts each
-                                           declared bullet's REQUIRED earning
-                                           anchors (positive floor) and
-                                           FORBIDDEN retracted literals
-                                           directly on its text; a FORBIDDEN
-                                           match is FRONTIER-STALE, a
-                                           REQUIRED-absent/uncheckable row is
+                                           L3 never fires on them, and the old
+                                           register did not check for unregistered
+                                           bullet starts. Its direct-text rows
+                                           assert REQUIRED/FORBIDDEN anchors; the
+                                           coverage self-check enumerates every
+                                           bullet start beneath both named
+                                           Frontier headings and fails a start
+                                           absent from the register as
+                                           FRONTIER-UNEVALUABLE. A FORBIDDEN
+                                           match is FRONTIER-STALE; a REQUIRED-
+                                           absent/uncheckable row is also
                                            FRONTIER-UNEVALUABLE
 
 Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
@@ -307,6 +312,12 @@
     ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\bIDA\b"], []),
 ]
 
+FRONTIER_SECTIONS = [
+    ("PROVINCE.md", 2, "Frontier"),
+    ("PROVINCE.md", 3, "Round-4 frontier (post-unlock)"),
+]
+
+
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
 VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
@@ -441,6 +452,37 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    return errs
+
+
+def frontier_coverage_check(filelines):
+    errs = []
+    for f, level, title in FRONTIER_SECTIONS:
+        lines = filelines.get(f)
+        if lines is None:
+            continue
+        headings = []
+        for i, line in enumerate(lines):
+            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
+            if m and len(m.group(1)) == level and m.group(2) == title:
+                headings.append(i)
+        if len(headings) != 1:
+            errs.append("%s heading %r has %d matches (G21 coverage uncheckable)"
+                        % (f, title, len(headings)))
+            continue
+        start = headings[0]
+        end = len(lines)
+        for i in range(start + 1, len(lines)):
+            m = re.match(r"^(#{1,6})\s+", lines[i])
+            if m and len(m.group(1)) <= level:
+                end = i
+                break
+        for i in range(start + 1, end):
+            line_no = i + 1
+            if BULLET.match(lines[i]) and not any(
+                    row_f == f and row_start == line_no
+                    for row_f, row_start, _, _, _ in FRONTIER):
+                errs.append("%s:%d unregistered Frontier bullet (G21)" % (f, line_no))
     return errs
 
 
@@ -630,7 +672,7 @@
         filelines[f] = lines
         counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
     scope_errors = assert_markers(filelines)
-    frontier_errors = frontier_check(filelines)
+    frontier_errors = frontier_check(filelines) + frontier_coverage_check(filelines)
     stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
     undecl = out.get("UNDECLARED", [])
     unres = out.get("UNRESOLVED", [])
```

## Scratch validation

- Candidate script was created and byte-compiled only under `/dev/shm/kaidoku-rv6-final-9vj8osw9/`; the source gate remained untouched.
- **Clean candidate — VERIFIED.** `python3 /dev/shm/kaidoku-rv6-final-9vj8osw9/c1-census-v10-candidate.py --root /dev/shm/kaidoku-rv6-final-9vj8osw9/clean --quiet` exited 0; `PROVINCE.md lines=162`, 14 rows, no frontier errors, `VERDICT: PASS`.
- **Seeded candidate — REPRODUCED.** Same command with `--root /dev/shm/kaidoku-rv6-final-9vj8osw9/fault` exited 1. Exact decisive output:

  ```text
  PROVINCE.md    lines=163  loci=6
  FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 unregistered Frontier bullet (G21)']
  DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
  ```

## Per-item verdicts and limit

- Existing append-past-:162 residual: **REPRODUCED** — current gate returns PASS on the seeded bullet.
- Proposed G21 coverage self-check: **REPRODUCED** — clean copy remains PASS; seeded copy fails at line 163 as `FRONTIER-UNEVALUABLE`.
- Live instrument edit status: **VERIFIED** — patch is not applied; source changes remain outside this seat's write scope.
- Non-bullet continuation text appended beyond a registered bullet span: **UNVERIFIABLE / not claimed closed** — this patch only enumerates bullet starts; that separate residual is named in the proposed gate text.
