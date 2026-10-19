# RV-3 — c1 chain: frontier blind-spot re-derivation + r10 frontier-claim-register patch

Seat: RV-3 (c1 census-instrument chain) · arc3-loop1-round6 · 2026-10-19
Provider: `zai-coding-plan/glm-5.3-flash` (lane-substituted wave, per claims-frozen).
Repo state at measurement: HEAD `c625d5de57e045188b5ce8cd450a57b349f90785`
(`c625d5d`, records of round 5), work `58c3db7` — both re-derived first-hand
via `git rev-parse HEAD` + `git log --oneline -5` this session.
Gate custody: `sha256 .ufo/gates/c1-census-v10.py` =
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`, and the
same digest re-derived after every experiment below — the repo gate was never
modified (write scope honored; git untouched).
Scratch lab: `/var/tmp/rv3-c1/` (nothing under `/tmp`; EDQUOT avoided).
Peer status at artifact-write time: `claims/c1/` held no other seat artifacts
(PL-1..4 / EX-1..4 / RV-1..2 / RV-4 absent); `claims/c2/EX-6/` and
`claims/c3/SC-3.md` had landed (different chains — not mine to reconcile;
VZ/CN seats own peer reconciliation).

## 1. First-hand re-derivations (before-state, rule #14)

Every number below was re-derived this session; none is quoted from a prior
seat or round.

- **Gate SHA-256** — `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
  (`sha256sum .ufo/gates/c1-census-v10.py`).
- **Scoped file sizes** — `wc -l`: PROVINCE.md 162, SKILL.md 390,
  SCORECARD.md 1696 (gate itself 610 lines).
- **SCOPE table PROVINCE rows** (read at gate lines 216-222): 8-13 CURRENT,
  15-26 CURRENT, 40-43 DATED(:40), 44 CURRENT, 45-62 DATED(:45), 64-71
  CURRENT, 119-131 DATED(:119). **No row covers 73-93 or 133-162.**
  Machine check: `grep -nE '"PROVINCE\.md", *(7[3-9]|8[0-9]|9[0-3])|13[3-9]|1[4-6][0-9]'
  .ufo/gates/c1-census-v10.py` → hits only docstring prose (:10, :27) and the
  119-131 row — zero scope rows in the Frontier ranges. VERIFIED.
- **Frontier region content** (Read PROVINCE.md): `## Frontier` :73 (intro
  :75-80, bullets :82-93), `### Round-4 frontier (post-unlock)` :133 (bullets
  :135-162). The EVM bullet :91-93 currently reads "…real solc-0.8.37 carriers
  (Core, arc3-r1/r3) and a vyper-0.4.3 carrier (arc3-r4); selectors stay bare
  hashes…". VERIFIED.
- **Baseline instrument run** (repo root): `python3 .ufo/gates/c1-census-v10.py`
  → exit 0, `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`,
  counts `PROVINCE.md lines=162 loci=6 / SCORECARD.md lines=1696 loci=9 /
  SKILL.md lines=390 loci=2`, live anchors re-derived
  `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`, scope-errors [],
  unreadable [], G2 ok (17/14/3 per file), g7 [], g11 []. VERIFIED.
- **Stale-literal provenance** (the R1 residual): `git show fbbbd45~1:PROVINCE.md`
  and `git show fbbbd45:PROVINCE.md` both show the Frontier EVM bullet as
  "…(Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay
  bare hashes…" — i.e. at the arc3-loop1-round1 WORK commit the corpus entry
  landed but the PROVINCE bullet still carried the retired literal.
  `git log --oneline -S 'real solc-0.8.37 carriers' -- PROVINCE.md` → the
  repair landed at `40de383` (arc3-loop1-round4 work). So the literal sat in
  the UNDECLARED Frontier region across rounds 1-3 while the instrument read
  PASS — the debt is real and historically demonstrated, not just structural.
  VERIFIED.

## 2. Verdicts on the frozen C1 items

| Frozen item | Verdict | Evidence |
|---|---|---|
| HEAD `c625d5d` / work `58c3db7` | VERIFIED | `git rev-parse HEAD`, `git log --oneline -5` (§1) |
| SCOPE covers PROVINCE only at 8-13/15-26/40-43/44/45-62/64-71/119-131 | VERIFIED | gate :216-222 + grep (§1) |
| Frontier 73-93 + 133-162 UNDECLARED (the blind spot) | VERIFIED | same grep; zero SCOPE rows in range |
| "instrument reads PASS identically whether or not those bullets are stale" | REPRODUCED | E1: retired literal planted at :91-93 on a scratch tree → PASS exit 0, counts byte-identical to clean E0 (PROVINCE loci=6 in BOTH — the seeded region yields zero detections) |
| Claim (a): extended instrument still PASS on current tree | REPRODUCED | E2: r10 gate on clean scratch → PASS exit 0, `frontier_errors []`, JSON identical to E0 modulo the two new additive keys, text output identical modulo the new FRONTIER line |
| Claim (b): seeded reintroduction FAILs (named disposition) | REPRODUCED | E3: r10 gate on seeded scratch → exit 1, `declared_fail_classes ['FRONTIER-STALE','FRONTIER-UNATTESTED']`, `FRONTIER-STALE PROVINCE.md:92 stale literal 'untested' reintroduced (cite corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md + …)` |
| Claim (c): every existing SCOPE row + counter intact | REPRODUCED | E2 identity check (above); E5a planted `rea-agents@6.0.0` in CURRENT :8-13 → STALE FAIL; E5b SKILL.md removed → UNREADABLE FAIL; E4 reflow → existing G15 marker error at :119 still fires alongside the new FRONTIER-ANCHOR rows |
| Register citations resolvable (rule #14) | VERIFIED | all cited corpus files exist (`ls` + `wc -l`: r3-pe-arm64 72, r5-01-riscv-bypass 106, arc2-r7-pe-wall 61, r4u-03-unblob-extract greps `sasquatch`, r1/r3/r4 EVM entries present); two absence rows cite `PROVINCE.md:26` (historical receipt) because no corpus entry exists for operator-gated absence — declared in the row text itself |

## 3. Design choice — in-place extension (r10), and why

The frozen claim allows "a v11 or an in-place extension; record which and
why." **Choice: in-place extension of `c1-census-v10.py` to r10** (patch text
below; the landing seat applies it to the gate path unchanged).

Why: (1) the gate is referenced by path across wave receipts and round
records; a rename breaks the reference web without adding falsifiability;
(2) the instrument's own revision convention is in-file provenance blocks
(r9 precedent at the top of the file), and the r10 block below records the
before-sha256, class names, and residual; (3) the alternative "declare the
region in SCOPE" was measured inadequate: E1 proves the frontier produces
ZERO loci (no pin, no 6.x.y — VER only matches `6\.\d+\.\d+` — no
path:line), so SCOPE rows alone would grade nothing; the frozen claim's
second option (a declared secondary classification against a claim register)
is the only variant that makes staleness gradable there. The register is
therefore additive: new table `FRONTIER_REGISTER`, new `frontier_audit()`,
new fail classes FRONTIER-ANCHOR / FRONTIER-UNATTESTED / FRONTIER-STALE,
one new verdict conjunct, two new JSON keys, one new text line. Every
existing SCOPE row, regex, counter, and JSON key is byte-preserved (E2).

Register semantics (per row `(file, start, end, anchor_line, anchor_regex,
required, forbidden, cite)`): the bullet's own first line must match the
anchor at the declared line (G15/G18 analogue — a reflow fails loudly
instead of silently grading shifted lines); every required pattern must
match a line in range (claim-less regression → FRONTIER-UNATTESTED); no
forbidden pattern may match (retired disposition reintroduced →
FRONTIER-STALE). `cite` names the corpus entry (or historical receipt) that
earned the claim. Rows cover all 13 bullets of both Frontier subsections;
the section intro (:75-80) is deliberately unregistered (process
boilerplate, not a surface claim). Only the EVM row carries a forbidden
list — it is the one retired literal with measured provenance
(pre-`40de383` wording recovered from git).

## 4. Patch text (applies to `.ufo/gates/c1-census-v10.py`, in place → r10)

Round-trip verified: `patch -p0` of this exact diff onto a pristine copy
reproduced the working scratch gate byte-identically
(`8e4206796fec2e16fb6f2c1959f33b63bbcb9643471d42472ac6bc2cba195ebf`).

```diff
--- pristine.py	2026-10-19 13:00:47.172332181 -0300
+++ c1-census-v10-r10.py	2026-10-19 12:55:36.129415242 -0300
@@ -1,5 +1,19 @@
 """C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.
 
+ARC3-LOOP1-ROUND6 r10 — FRONTIER-CLAIM REGISTER (2026-10-19, RV-3; instrument
+sha256 before this edit d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5).
+The Frontier region (PROVINCE.md "## Frontier" :73-93 + "### Round-4 frontier
+(post-unlock)" :133-162) was UNDECLARED — no SCOPE row covered it and its
+bullets are locus-free (no rea-agents pin, no 6.x.y, no path:line), so the run
+read PASS identically whether or not a frontier bullet was stale (R1 residual,
+measured this round: the retired literal "real solc/vyper-compiled bytecode
+untested" planted back into the :91-93 bullet reads PASS exit 0 under r9).
+Closure is a declared L1b secondary classification — FRONTIER_REGISTER +
+frontier_audit(): per-bullet anchor (G15/G18 analogue), required corpus-earned
+claims, forbidden retired literals; new fail classes FRONTIER-ANCHOR /
+FRONTIER-UNATTESTED / FRONTIER-STALE. Additive only: every existing SCOPE row,
+counter and verdict disjunct is unchanged; the verdict gains one conjunct.
+
 E22 DISPOSITION — arc3-loop1-round1, EX-28 (measured 2026-10-19 at HEAD
 e845c2b; instrument sha256 before this edit 36e96cd5…). The arc2-loop1-round3
 carried debt "census scope-table drift (FAIL undeclared=2 at 766-line HEAD vs
@@ -236,6 +250,63 @@
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
 ]
 
+# ---- L1b: frontier-claim register (r10) -----------------------------------
+# Frontier bullets are locus-free by construction, so the L2/L3 needles never
+# classify them; staleness there is graded here.  Row shape:
+#   (file, start, end, anchor_line, anchor_regex, required, forbidden, cite)
+#   anchor    the bullet's own first line must match anchor_regex at
+#             anchor_line (G15/G18 analogue: a reflow fails loudly, never
+#             silently grades the wrong lines);
+#   required  every pattern must match a line in [start, end], else
+#             FRONTIER-UNATTESTED (claim-less regression);
+#   forbidden no pattern may match a line in [start, end], else
+#             FRONTIER-STALE (retired disposition reintroduced);
+#   cite      the corpus entry / receipt that earned the claim (rule #14).
+# The "## Frontier" intro (:75-80) is deliberately unregistered: it is process
+# boilerplate, not a surface claim.
+FRONTIER_REGISTER = [
+    ("PROVINCE.md", 82, 83, 82, r"PE subtypes",
+     [r"ARM64"], [],
+     "corpus/knowledge/2026-10-13-r3-pe-arm64.md"),
+    ("PROVINCE.md", 84, 86, 84, r"Recorded crashes",
+     [r"32 MiB"], [],
+     "corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md"),
+    ("PROVINCE.md", 87, 88, 87, r"Alternate providers",
+     [r"REA_IDA_MCP_CONFIG"], [],
+     "PROVINCE.md:26 provider-key inventory (historical receipt; operator-gated absence, no corpus entry)"),
+    ("PROVINCE.md", 89, 90, 89, r"macOS-only surfaces",
+     [r"unsupported_host"], [],
+     "corpus/knowledge/2026-10-13-r3-keyed-archive-carriers.md"),
+    ("PROVINCE.md", 91, 93, 91, r"EVM bytecode",
+     [r"real solc-0\.8\.37", r"vyper-0\.4\.3"],
+     [r"untested"],
+     "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md + 2026-10-19-arc3-r3-evm-optimizer-shapes.md + 2026-10-19-arc3-r4-evm-vyper-leg.md"),
+    ("PROVINCE.md", 135, 138, 135, r"RISC-V analysis",
+     [r"r5-01"], [],
+     "corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md"),
+    ("PROVINCE.md", 139, 144, 139, r"PE scale wall",
+     [r"arc2-r7", r"CLOSED"], [],
+     "corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md"),
+    ("PROVINCE.md", 145, 146, 145, r"source mapping",
+     [r"Ignition"], [],
+     "corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md"),
+    ("PROVINCE.md", 147, 148, 147, r"sasquatch",
+     [r"7z fallback"], [],
+     "corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md"),
+    ("PROVINCE.md", 149, 150, 149, r"adb device surface",
+     [r"22/24"], [],
+     "corpus/knowledge/2026-10-13-r4u-06-adb-surface.md"),
+    ("PROVINCE.md", 151, 156, 151, r"asar analysis",
+     [r"r4-06"], [],
+     "corpus/knowledge/2026-10-13-r4-06-1password-asar.md + 2026-10-13-r4-05-signal-asar.md"),
+    ("PROVINCE.md", 157, 160, 157, r"Cross-version residuals",
+     [r"compare-application-versions"], [],
+     "corpus/knowledge/2026-10-13-r4-10-real-version-pair.md"),
+    ("PROVINCE.md", 161, 162, 161, r"Operator-gated",
+     [r"HOPPER_LAUNCHER_PATH"], [],
+     "PROVINCE.md:26 provider-key inventory (historical receipt; operator-gated absence, no corpus entry)"),
+]
+
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
 VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
@@ -348,6 +419,30 @@
     return errs
 
 
+def frontier_audit(filelines):
+    """r10: the L1b frontier-claim register (see FRONTIER_REGISTER)."""
+    errs = []
+    for (f, s, e, al, ar, req, forb, cite) in FRONTIER_REGISTER:
+        lines = filelines.get(f)
+        if not lines:
+            continue  # UNREADABLE (H1 class) already fails the run
+        if not (1 <= al <= len(lines)) or not re.search(ar, lines[al - 1]):
+            errs.append(("FRONTIER-ANCHOR", "%s:%d anchor %r absent (register row %d-%d needs re-key)"
+                         % (f, al, ar, s, e)))
+            continue
+        seg = lines[s - 1:e]
+        for pat in req:
+            if not any(re.search(pat, ln) for ln in seg):
+                errs.append(("FRONTIER-UNATTESTED", "%s:%d-%d required claim %r not found (cite %s)"
+                             % (f, s, e, pat, cite)))
+        for k, ln in enumerate(seg):
+            for pat in forb:
+                if re.search(pat, ln):
+                    errs.append(("FRONTIER-STALE", "%s:%d stale literal %r reintroduced (cite %s)"
+                                 % (f, s + k, pat, cite)))
+    return errs
+
+
 def cache_versions():
     """G17: every version present in an npx rea-agents cache."""
     vers = set()
@@ -531,6 +626,7 @@
         filelines[f] = lines
         counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
     scope_errors = assert_markers(filelines)
+    frontier_errors = frontier_audit(filelines)
     stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
     undecl = out.get("UNDECLARED", [])
     unres = out.get("UNRESOLVED", [])
@@ -564,9 +660,10 @@
                     floor[rec["file"]] += 1
     h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
     g2_ok = h3_ok
-    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])
+    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"]) \
+               + sorted({cls for cls, _ in frontier_errors})
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok and (not unreadable)
+         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors)
     verdict = "PASS" if ok else "FAIL"
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
@@ -575,6 +672,8 @@
                           "unreadable": unreadable, "declared_fail_classes": declared,
                           "g2_ok": g2_ok, "g2_floor": "1/readable-file", "current_ok_per_file": floor,
                           "g11": g11, "g7": g7,
+                          "frontier_rows": len(FRONTIER_REGISTER),
+                          "frontier_errors": ["%s %s" % (c, m) for c, m in frontier_errors],
                           "historical": out.get("historical", []),
                           "current_ok": out.get("current-ok", [])}, indent=1))
         return 0 if verdict == "PASS" else 1
@@ -594,6 +693,9 @@
                     print("      :%d [%s] %s=%s -> %s (%s)" %
                           (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
+    print("FRONTIER register (r10): %d rows, %d error(s)%s"
+          % (len(FRONTIER_REGISTER), len(frontier_errors),
+             "" if not frontier_errors else ": " + "; ".join("%s %s" % (c, m) for c, m in frontier_errors)))
     print("UNREADABLE (could-not-evaluate): %r" % unreadable)
     print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
           % ("ok" if g2_ok else "SUSPECT",
```
