# PL-4 — C3 G21 append-past-register guard

## Claim and scope

C3 candidate (a): make a new bullet appended after the G21 register's final declared line fail as unevaluable, instead of silently passing. This is a patch-text proposal only; the live instrument and all custody/source files remain untouched. Scratch inputs and patched copies are under `/var/tmp/kaidoku-pl4.NKp739/`.

## First-hand re-derivation and verdicts

| Item | Verdict | Evidence |
|---|---|---|
| Repository identity | **VERIFIED** | `git log -1 --oneline` → `5694506 arc3-loop1-round9: records — SCORECARD round section, LOG entry, round report + scope re-key to EOF (measured at work commit eb5a2c4)`. `git show -s --format='%H' eb5a2c4` → `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`. |
| Instrument identity at HEAD | **VERIFIED** | `sha256sum .ufo/gates/c1-census-v10.py` and `git show HEAD:.ufo/gates/c1-census-v10.py \| sha256sum` both returned `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`; `git diff --quiet HEAD -- .ufo/gates/c1-census-v10.py` succeeded (`gate_worktree_vs_HEAD=identical`). |
| Register boundary | **VERIFIED** | `wc -l PROVINCE.md` → `162 PROVINCE.md`; the two named headings are `.ufo/gates/c1-census-v10.py:97-99` / `PROVINCE.md:73` and `PROVINCE.md:133`, with the last bullet at `PROVINCE.md:162`. The register has 14 rows in the measured clean run (`FRONTIER` definition at gate `:292-308`; output below). `frontier_check` currently only iterates those rows (`:422-444`), and `main`'s readable-file check sets its maximum to declared SCOPE/FRONTIER ends (`:613-617`), so a line after 162 is not a truncated-file error. |
| Named residual on the original gate | **REPRODUCED** | A scratch-only append made the sentinel the exact line 163: `- Frontier append sentinel: real solc/vyper-compiled bytecode untested`. Original gate command: `python3 /var/tmp/kaidoku-pl4.NKp739/seeded163/.ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-pl4.NKp739/seeded163 --quiet`. Exact relevant output: `PROVINCE.md    lines=163  loci=6`; `FRONTIER register (G21): 14 rows asserted, errors: []`; `DECLARED FAIL CLASSES: []`; `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0)`; `exit=0`. |
| Proposed guard, clean control | **VERIFIED** | Applied the diff below only to a scratch copy. `python3 -m py_compile /var/tmp/kaidoku-pl4.NKp739/clean-after/.ufo/gates/c1-census-v10.py` succeeded. The clean scratch run retained `PROVINCE.md    lines=162  loci=6`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0)`, `exit=0`. |
| Proposed guard, same seeded fault | **VERIFIED** | Applied the identical diff to the seeded scratch copy; `python3 -m py_compile /var/tmp/kaidoku-pl4.NKp739/seeded-after/.ufo/gates/c1-census-v10.py` succeeded. Same sentinel at line 163 now gives `FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 unregistered Frontier bullet (G21)']`; `DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']`; `VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0)`; `exit=1`. |

The clean control and seeded fault were both run with the source gate copied into scratch; the `patch -p0` application and both syntax checks ran only under `/var/tmp`. No live gate, custody tool, corpus, tracked file, or Git state was changed by the probe.

## Proposed patch text

```diff
--- .ufo/gates/c1-census-v10.py
+++ .ufo/gates/c1-census-v10.py
@@ -110,10 +110,11 @@
 declared fail classes (FRONTIER-STALE for a FORBIDDEN match, FRONTIER-UNEVALUABLE
 for a REQUIRED-absent or uncheckable row), reported in text and --json. G21
 rows are keyed to the r5-audit tree; any frontier edit re-keys the register in
-the same commit — the same standing rule as the records-commit bound. Residual,
-named: a brand-new bullet appended past :162 (the register's last declared
-line) sits outside the register until re-keyed — the same past-the-bound
-residual the records-commit rule already governs for SCORECARD.md:856+."""
+the same commit — the same standing rule as the records-commit bound. The
+original append-past-:162 residual is closed by the follow-up section walk:
+every bullet in either named Frontier section must fall within a registered
+span or fails FRONTIER-UNEVALUABLE. The SCORECARD.md records-commit bound is
+separate and unchanged."""
 #!/usr/bin/env python3
 """C1 census instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; the
 v9-era structure and claim text below are retained as the instrument's history,
@@ -213,27 +214,25 @@
                                            table).  Do not re-key the unit
                                            without re-running the HEAD
                                            invariance check.)
-  G21 frontier-claim register            (r10, R1 residual): Frontier bullets
+  G21 frontier-claim register            (r10): Frontier bullets
                                            (PROVINCE.md :73-93, :133-162)
                                            carry no pin/version/path loci, so
-                                           L3 never fires on them and v10 read
-                                           PASS identically whether or not a
-                                           frontier bullet was stale; the
-                                           FRONTIER[] register asserts each
-                                           declared bullet's REQUIRED earning
-                                           anchors (positive floor) and
+                                           L3 never fires on them; FRONTIER[]
+                                           asserts each declared bullet's
+                                           REQUIRED positive-floor anchors and
                                            FORBIDDEN retracted literals
-                                           directly on its text; a FORBIDDEN
-                                           match is FRONTIER-STALE, a
-                                           REQUIRED-absent/uncheckable row is
+                                           directly on its text. A FORBIDDEN
+                                           match is FRONTIER-STALE; a REQUIRED-
+                                           absent/uncheckable row or bullet
+                                           outside every registered span is
                                            FRONTIER-UNEVALUABLE
 
 Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
 AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds
 (>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
-unevaluable scoped file AND frontier_errors == 0 (G21 frontier register, r10:
-every declared frontier bullet carries its REQUIRED anchors and none carries a
-FORBIDDEN retracted literal).
+unevaluable scoped file AND frontier_errors == 0 (G21: declared bullets carry
+REQUIRED anchors and no FORBIDDEN literals; every bullet in either named
+Frontier section lies within a registered span).
 Exit 0 PASS, 1 FAIL, 2 anchor failure.
 Usage: python3 c1-census-v10.py [--root DIR] [--json] [--quiet]
 """
@@ -281,7 +280,9 @@
 # construction; these rows are keyed by DIRECT TEXT ASSERTION, not by locus,
 # and deliberately live OUTSIDE SCOPE (a CURRENT SCOPE row would still never
 # fire -- classify() needs a locus to grade). Register files must also appear
-# in SCOPE (the read loop is keyed on SCOPE's file set). Each row:
+# in SCOPE (the read loop is keyed on SCOPE's file set). The named Frontier
+# sections are separately scanned; bullets outside every registered span are
+# FRONTIER-UNEVALUABLE. Each row:
 #   (file, start, end, [REQUIRED regex...], [FORBIDDEN regex...])
 # REQUIRED  at least one match per pattern inside the declared span (positive
 #           floor: a stripped/rewritten/truncated bullet fails REQUIRED-absent)
@@ -420,11 +421,10 @@
 
 
 def frontier_check(filelines):
-    """G21 (r10): assert the frontier-claim register directly on bullet text.
-    Locus-free bullets never reach classify(), so this is the only grading
-    they get: REQUIRED anchors are the positive floor (a stripped, rewritten
-    or truncated bullet fails REQUIRED-absent), FORBIDDEN literals name the
-    retracted claims whose reintroduction must fail the run (FRONTIER-STALE)."""
+    """G21 (r10): assert registered claims and bullet coverage in Frontier.
+    Locus-free bullets never reach classify(), so the register checks REQUIRED
+    anchors and FORBIDDEN literals directly; a bullet outside every registered
+    span in either named Frontier section is FRONTIER-UNEVALUABLE."""
     errs = []
     for (f, s, e, req, forb) in FRONTIER:
         lines = filelines.get(f)
@@ -441,6 +441,25 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    registered = {}
+    for (f, s, e, req, forb) in FRONTIER:
+        registered.setdefault(f, set()).update(range(s, e + 1))
+    section_level = None
+    for lineno, line in enumerate(filelines.get("PROVINCE.md") or [], 1):
+        heading = re.match(r"^(#{1,6})\s+", line)
+        if heading:
+            level = len(heading.group(1))
+            title = line.strip()
+            if title == "## Frontier":
+                section_level = level
+            elif title == "### Round-4 frontier (post-unlock)":
+                section_level = level
+            elif section_level is not None and level <= section_level:
+                section_level = None
+        if (section_level is not None and BULLET.match(line)
+                and lineno not in registered.get("PROVINCE.md", set())):
+            errs.append("PROVINCE.md:%d unregistered Frontier bullet (G21)"
+                        % lineno)
     return errs
 
 
```

## Boundary and residual

The proposed scanner walks the two currently named Frontier sections (`## Frontier` and `### Round-4 frontier (post-unlock)`) and requires each `-` or `*` bullet line to fall inside a physical range represented in `FRONTIER`. The fault at line 163 is thereby unregistered and reuses the existing `frontier_errors` → `FRONTIER-UNEVALUABLE` → exit-1 path (`.ufo/gates/c1-census-v10.py:667-684`). It does not claim to detect an unregistered claim rewritten inside a currently registered span; that remains subject to the existing content assertions/re-key discipline. The heading names are explicit by design and would need updating if the Frontier headings are renamed or split differently.
