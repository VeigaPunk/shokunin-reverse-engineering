# PL-4 — c1 (census instrument): G21 frontier-claim register, r10 patch text + seeded-fault demonstration

Seat PL-4, chain c1, wave arc3-loop1-round6. Measured 2026-10-19 on this host.
Every number below is first-hand this session (rule #14): the command that
produced it is quoted, transcripts live under `PL-4/transcripts/`, scratch was
`/var/tmp/pl4-arc3r6/`. The gate `.ufo/gates/c1-census-v10.py` was NOT
modified — all instrument work happened on scratch copies.

## 0. Deliverable in one line

Patch text (unified diff, §4) extending `.ufo/gates/c1-census-v10.py` IN PLACE
with a **frontier-claim register** (new `FRONTIER[]` table + `frontier_check()`
= assertion family G21): the Frontier region becomes gradable via direct text
assertion instead of loci. Requirement (a) clean tree still PASS — measured on
the real repo root; (b) seeded reintroduction of a declared-stale literal into
`:91-93` FAILs exit 1 with named class `FRONTIER-STALE` — measured on five
scratch trees; (c) every SCOPE row and every existing counter intact — proven
by a 17-key JSON comparison (all equal; only `frontier_rows`/`frontier_errors`
added).

## 1. First-hand re-derivations (the frozen claim's "before" facts)

| # | Fact (claims-frozen C1) | My measurement | Verdict |
|---|---|---|---|
| 1 | HEAD records c625d5d, work 58c3db7 | `git rev-parse HEAD` → `c625d5de57e0…`; `git log --oneline -3` shows `c625d5d arc3-loop1-round5: records … (measured at work commit 58c3db7)` | REPRODUCED |
| 2 | Instrument at `.ufo/gates/c1-census-v10.py` | `sha256sum` → `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`; 610 lines | REPRODUCED |
| 3 | SCOPE covers PROVINCE only 8-13/15-26/40-43/44/45-62/64-71/119-131 | gate `:216-222` (read): exactly those 7 rows; `grep -nE` for any row reaching 73-93 or 133-162 → NO MATCH | REPRODUCED |
| 4 | Frontier region = 73-93 + 133-162 | `PROVINCE.md`: `:73 ## Frontier`, intro `:75-80`, bullets `:82-83/:84-86/:87-88/:89-90/:91-93`, `:95 ## Adjacent`; `:133 ### Round-4 frontier (post-unlock)`, bullets `:135-138/:139-144/:145-146/:147-148/:149-150/:151-156/:157-160/:161-162`; `wc -l PROVINCE.md` → 162 (EOF = `:162`) | REPRODUCED |
| 5 | Instrument "reads PASS identically whether or not those bullets are stale" | v10 run with `--root` on five seeded scratch trees (stale literal reintroduced into :91-93; earning tokens stripped from :91-93 and :135-138; PROVINCE truncated to 161 lines): **all five PASS exit 0** (`transcripts/v10-*.txt`) | REPRODUCED |
| 6 | v10 baseline PASS at HEAD | repo-root run: `live anchors {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`; `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1696 loci=9`, `SKILL.md lines=390 loci=2`; `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 | REPRODUCED |
| 7 | "R4/R5 PROVINCE repairs were clause-audited by hand, not instrument-graded" | operative half verified: the Frontier region is not instrument-gradable at HEAD (items 3+5); the historical by-hand audit itself is not re-derivable from artifacts | PARTLY (operative half REPRODUCED, process UNVERIFIABLE) |

Baseline command (rerunnable): `python3 .ufo/gates/c1-census-v10.py --quiet`
from the repo root.

New blind-spot evidence found beyond the frozen example (item 5, last tree):
v10 reads **PASS on a 161-line PROVINCE.md** — silent content loss past `:131`
(the post-unlock frontier bullets vanishing) is invisible to v10, because
SCOPE's max PROVINCE end is 131. The r10 patch closes this too (G19 threshold
moves to the register's max end 162; measured: same tree → `UNREADABLE: 
['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)']`, exit 1).

## 2. Design decision, recorded per the claim

**Register (option b), not SCOPE declaration (option a).** SCOPE rows are
locus-keyed: `classify()` grades a unit only after it collects PIN/VER
occurrences (falling back to PTR), and a unit with no occurrences is `continue`d
before `scope_of()` is ever consulted (gate `:403-420`, read this session). A
Frontier bullet carries no `rea-agents@` pin, no bare `6.x.y`, no `~/…:N`
pointer — so even a `CURRENT` SCOPE row over `:73-93` would never fire. The
only machinery that can grade these bullets is direct text assertion:
`FRONTIER[]` rows pin each bullet's span and require its earning anchors
(REQUIRED, the positive floor) while forbidding retracted literals (FORBIDDEN).

**In-place extension, not a v11 fork.** (1) Requirement (c) is structurally
guaranteed by a minimal in-place diff and I falsified it with the JSON key
comparison (§5) — a fork guarantees nothing. (2) The fleet invokes the gate by
path; a fork leaves the blind v10 callable alongside the fixed gate, and two
census gates can diverge silently — exactly the failure mode this wave is
closing. (3) The instrument's own convention is in-place provenance blocks
(the r9 block at gate `:47-93` records the previous in-place closure the same
way), with post-edit identity recorded in a landing receipt, not inline (gate
`:89-93`). Revision label: **r10**, block `ARC3-LOOP1-ROUND6 r10 — G21
FRONTIER REGISTER`, citing pre-edit sha `d0772ce8…`.

## 3. Demonstration (requirement b) — six trees × two instruments

Scratch scaffold `/var/tmp/pl4-arc3r6/`: trees `clean`, `seeded-forbidden`,
`seeded-forbidden-only`, `seeded-required-evm`, `seeded-required-riscv`,
`clean-truncated`, each holding byte-copies of PROVINCE.md/SKILL.md/SCORECARD.md
(clean tree sha-verified identical to the repo's). Seeds are content-asserted
edits (`PL-4/seed.py`):

- `seeded-forbidden` :91-93 → "…real solc/vyper-compiled bytecode untested,
  synthetic dispatcher only." (the frozen claim's example literal, line-count
  neutral)
- `seeded-forbidden-only` :91-93 → keeps `solc-0.8.37`/`vyper-0.4.3` tokens,
  adds "untested" — isolates the FORBIDDEN arm
- `seeded-required-evm` :91-93 → "- **EVM bytecode (extended)** — see corpus."
  (earning citations stripped)
- `seeded-required-riscv` :137 → r5-01 citation text removed
- `clean-truncated` → PROVINCE.md truncated to 161 lines, other files intact

| tree | v10 exit | v10 verdict | r10 exit | r10 verdict | r10 declared classes |
|---|---|---|---|---|---|
| clean | 0 | PASS | 0 | PASS | [] |
| seeded-forbidden | 0 | PASS (blind) | 1 | FAIL | ['FRONTIER-STALE'] |
| seeded-forbidden-only | 0 | PASS (blind) | 1 | FAIL | ['FRONTIER-STALE'] |
| seeded-required-evm | 0 | PASS (blind) | 1 | FAIL | ['FRONTIER-UNEVALUABLE'] |
| seeded-required-riscv | 0 | PASS (blind) | 1 | FAIL | ['FRONTIER-UNEVALUABLE'] |
| clean-truncated (161 L) | 0 | PASS (blind) | 1 | FAIL | ['UNREADABLE', 'FRONTIER-UNEVALUABLE'] |

Key r10 error lines (`transcripts/r10-*.txt`):

```
seeded-forbidden:      PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)
                       + REQUIRED 'solc-0\.8\.37' / 'vyper-0\.4\.3' absent
seeded-forbidden-only: PROVINCE.md:91-93 FORBIDDEN 'untested' matched 'untested' (FRONTIER-STALE)   [exactly one error]
seeded-required-evm:   PROVINCE.md:91-93 REQUIRED 'solc-0\.8\.37' absent (G21 frontier register) [x2 incl. vyper]
seeded-required-riscv: PROVINCE.md:135-138 REQUIRED 'r5-01' absent (G21 frontier register)
clean-truncated:       UNREADABLE: ['PROVINCE.md: 161 lines < declared max 162 (rows beyond EOF)', …]
                       + 14 × "frontier uncheckable (file unreadable)"
```

Requirement (a) on the real tree: `python3 c1-census-v10-r10.py --quiet` with
default `--root` → exit 0, `FRONTIER register (G21): 14 rows asserted,
errors: []`, `DECLARED FAIL CLASSES: []`, VERDICT line byte-identical to
baseline (`transcripts/r10-REPO-ROOT.txt`).

## 4. Patch text (apply to `.ufo/gates/c1-census-v10.py`)

Generated by `diff -u` of the pristine gate vs the built r10 copy; applying it
to a pristine copy of the gate (`patch <file> < patch-v10-to-r10.diff`)
reproduced sha256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`
= the built r10's sha (verified this session). Copy also at
`PL-4/patch-v10-to-r10.diff`; built instrument at `PL-4/c1-census-v10-r10.py`
(713 lines); builder + seeder at `PL-4/build_r10.py`, `PL-4/seed.py`.

```diff
--- c1-census-v10.py	2026-10-19 12:46:41.184570194 -0300
+++ c1-census-v10-r10.py	2026-10-19 13:30:25.449839276 -0300
@@ -90,7 +90,30 @@
   receipts/after/after-sha256.txt + landing-diff.md), NOT inline: an artifact
   that records its own byte-identity must re-derive it after every revision,
   so a hash written into the file it hashes would be stale by construction
-  (the queue-drain rule-#14 discipline)."""
+  (the queue-drain rule-#14 discipline).
+
+ARC3-LOOP1-ROUND6 r10 — G21 FRONTIER REGISTER (2026-10-19, seat PL-4; instrument
+sha256 before this edit d0772ce8…). The round-1 R1 residual closes: the Frontier
+region (PROVINCE.md :73-93 `## Frontier`, :133-162 `### Round-4 frontier
+(post-unlock)`) is UNDECLARED in SCOPE, and its bullets carry no pin/version/
+path loci, so L3 never fires on them and the instrument read PASS identically
+whether or not a frontier bullet was stale (measured before this edit: v10
+returns PASS exit 0 on a scratch tree carrying the retracted literal "real
+solc/vyper-compiled bytecode untested" back inside :91-93). Closed as a
+declared SECONDARY classification for locus-free bullets (the register option,
+not a SCOPE declaration — a SCOPE row would still never fire: classify() needs
+a locus). FRONTIER[] rows pin each bullet's span and assert REQUIRED earning
+anchors (positive floor: a stripped, rewritten-empty or truncated bullet fails
+REQUIRED-absent) and FORBIDDEN retracted literals (a reintroduced stale literal
+fails FRONTIER-STALE). SCOPE bounds are UNCHANGED and every existing counter
+keeps its semantics; the run gains one counter (frontier_errors) and two
+declared fail classes (FRONTIER-STALE for a FORBIDDEN match, FRONTIER-UNEVALUABLE
+for a REQUIRED-absent or uncheckable row), reported in text and --json. G21
+rows are keyed to the r5-audit tree; any frontier edit re-keys the register in
+the same commit — the same standing rule as the records-commit bound. Residual,
+named: a brand-new bullet appended past :162 (the register's last declared
+line) sits outside the register until re-keyed — the same past-the-bound
+residual the records-commit rule already governs for SCORECARD.md:856+."""
 #!/usr/bin/env python3
 """C1 census instrument v10-r9 (arc3-loop1-round2: H1+H3 fail-closures; the
 v9-era structure and claim text below are retained as the instrument's history,
@@ -190,11 +213,27 @@
                                            table).  Do not re-key the unit
                                            without re-running the HEAD
                                            invariance check.)
+  G21 frontier-claim register            (r10, R1 residual): Frontier bullets
+                                           (PROVINCE.md :73-93, :133-162)
+                                           carry no pin/version/path loci, so
+                                           L3 never fires on them and v10 read
+                                           PASS identically whether or not a
+                                           frontier bullet was stale; the
+                                           FRONTIER[] register asserts each
+                                           declared bullet's REQUIRED earning
+                                           anchors (positive floor) and
+                                           FORBIDDEN retracted literals
+                                           directly on its text; a FORBIDDEN
+                                           match is FRONTIER-STALE, a
+                                           REQUIRED-absent/uncheckable row is
+                                           FRONTIER-UNEVALUABLE
 
 Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
 AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds
 (>= 1 current-ok DETECTION per readable scoped file, r9 floor) AND no
-unevaluable scoped file.
+unevaluable scoped file AND frontier_errors == 0 (G21 frontier register, r10:
+every declared frontier bullet carries its REQUIRED anchors and none carries a
+FORBIDDEN retracted literal).
 Exit 0 PASS, 1 FAIL, 2 anchor failure.
 Usage: python3 c1-census-v10.py [--root DIR] [--json] [--quiet]
 """
@@ -236,6 +275,37 @@
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
 ]
 
+# ---- L1b: frontier-claim register (r10, G21). Frontier bullets carry no
+# pin/version/path loci, so the L1/L2/L3 machinery is silent on them by
+# construction; these rows are keyed by DIRECT TEXT ASSERTION, not by locus,
+# and deliberately live OUTSIDE SCOPE (a CURRENT SCOPE row would still never
+# fire -- classify() needs a locus to grade). Register files must also appear
+# in SCOPE (the read loop is keyed on SCOPE's file set). Each row:
+#   (file, start, end, [REQUIRED regex...], [FORBIDDEN regex...])
+# REQUIRED  at least one match per pattern inside the declared span (positive
+#           floor: a stripped/rewritten/truncated bullet fails REQUIRED-absent)
+# FORBIDDEN no match may occur (a reintroduced retracted literal fails
+#           FRONTIER-STALE). Patterns are case-insensitive.
+# Keyed to the r5-audit tree (HEAD c625d5d); any frontier edit re-keys the
+# register in the same commit.
+FRONTIER = [
+    ("PROVINCE.md", 75, 80, [r"Claimed in MINT\.md, not yet held"], []),
+    ("PROVINCE.md", 82, 83, [r"PE subtypes", r"x86-64 AND ARM64"], []),
+    ("PROVINCE.md", 84, 86, [r"32 MiB", r"oldest-first"], []),
+    ("PROVINCE.md", 87, 88, [r"Alternate providers", r"\bIDA\b"], []),
+    ("PROVINCE.md", 89, 90, [r"unsupported_host"], []),
+    ("PROVINCE.md", 91, 93, [r"EVM bytecode", r"solc-0\.8\.37", r"vyper-0\.4\.3"],
+     [r"untested"]),
+    ("PROVINCE.md", 135, 138, [r"RISC-V", r"r5-01"], []),
+    ("PROVINCE.md", 139, 144, [r"90 MB PE", r"arc2-r7"], []),
+    ("PROVINCE.md", 145, 146, [r"\.jsc", r"Ignition"], []),
+    ("PROVINCE.md", 147, 148, [r"sasquatch", r"unblob"], []),
+    ("PROVINCE.md", 149, 150, [r"adb device surface", r"22/24"], []),
+    ("PROVINCE.md", 151, 156, [r"1Password", r"asar"], []),
+    ("PROVINCE.md", 157, 160, [r"Cross-version", r"r12-02|r14-01"], []),
+    ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\bIDA\b"], []),
+]
+
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
 VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
@@ -348,6 +418,31 @@
     return errs
 
 
+def frontier_check(filelines):
+    """G21 (r10): assert the frontier-claim register directly on bullet text.
+    Locus-free bullets never reach classify(), so this is the only grading
+    they get: REQUIRED anchors are the positive floor (a stripped, rewritten
+    or truncated bullet fails REQUIRED-absent), FORBIDDEN literals name the
+    retracted claims whose reintroduction must fail the run (FRONTIER-STALE)."""
+    errs = []
+    for (f, s, e, req, forb) in FRONTIER:
+        lines = filelines.get(f)
+        if not lines:
+            errs.append("%s:%d-%d frontier uncheckable (file unreadable)" % (f, s, e))
+            continue
+        seg = "\n".join(lines[s - 1:e])
+        for pat in req:
+            if not re.search(pat, seg, re.I):
+                errs.append("%s:%d-%d REQUIRED %r absent (G21 frontier register)"
+                            % (f, s, e, pat))
+        for pat in forb:
+            m = re.search(pat, seg, re.I)
+            if m:
+                errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
+                            % (f, s, e, pat, m.group(0)))
+    return errs
+
+
 def cache_versions():
     """G17: every version present in an npx rea-agents cache."""
     vers = set()
@@ -513,7 +608,8 @@
         return 2
     out, counts, filelines, unreadable = {}, {}, {}, []
     for f in files:
-        max_end = max((s[2] for s in SCOPE if s[0] == f), default=0)
+        max_end = max([s[2] for s in SCOPE if s[0] == f]
+                      + [r[2] for r in FRONTIER if r[0] == f], default=0)
         try:
             lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
         except OSError as ex:
@@ -531,6 +627,7 @@
         filelines[f] = lines
         counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
     scope_errors = assert_markers(filelines)
+    frontier_errors = frontier_check(filelines)
     stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
     undecl = out.get("UNDECLARED", [])
     unres = out.get("UNRESOLVED", [])
@@ -564,15 +661,19 @@
                     floor[rec["file"]] += 1
     h3_ok = all(floor[f] > 0 for f in files if filelines[f] is not None)
     g2_ok = h3_ok
-    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])
+    frontier_class = (["FRONTIER-STALE"] if any("FORBIDDEN" in e for e in frontier_errors)
+                      else ["FRONTIER-UNEVALUABLE"] if frontier_errors else [])
+    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"]) \
+               + frontier_class
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok and (not unreadable)
+         and (not g11) and g2_ok and (not unreadable) and (not frontier_errors)
     verdict = "PASS" if ok else "FAIL"
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                           "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                           "unresolved": unres, "scope_errors": scope_errors,
                           "unreadable": unreadable, "declared_fail_classes": declared,
+                          "frontier_rows": len(FRONTIER), "frontier_errors": frontier_errors,
                           "g2_ok": g2_ok, "g2_floor": "1/readable-file", "current_ok_per_file": floor,
                           "g11": g11, "g7": g7,
                           "historical": out.get("historical", []),
@@ -594,6 +695,8 @@
                     print("      :%d [%s] %s=%s -> %s (%s)" %
                           (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
+    print("FRONTIER register (G21): %d rows asserted, errors: %r"
+          % (len(FRONTIER), frontier_errors))
     print("UNREADABLE (could-not-evaluate): %r" % unreadable)
     print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
           % ("ok" if g2_ok else "SUSPECT",
```

## 5. Counter integrity (requirement c) — measured

`--json` on the clean tree, v10 vs r10, key-by-key:

```
shared keys: 17  mismatched: []          (live, counts, verdict, stale,
ambiguous, undeclared, unresolved, scope_errors, unreadable,
declared_fail_classes, g2_ok, g2_floor, current_ok_per_file, g11, g7,
historical, current_ok)
r10-only keys: ['frontier_errors', 'frontier_rows']
counts equal: True
current_ok_per_file: {'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}   (unchanged)
```

No SCOPE row is touched (the diff contains zero `-`/`+` lines inside the SCOPE
table); the `VERDICT:` print format is byte-identical (the G21 count is a
separate new line); the G2 floor, G15/G18 marker machinery, G19 semantics (now
also covering register rows — strictly fail-CLOSED, never a new silence) are
unchanged. Post-landing gate identity is NOT recorded inline (the gate's own
rule-#14 discipline, gate `:89-93`); record it in the landing receipt.

## 6. Residuals (named, not silently open)

1. **Past-the-bound appends**: a brand-new bullet appended beyond `:162` sits
   outside the register until re-keyed — the same residual the records-commit
   standing rule (gate `:41-45`) already governs for SCORECARD.md:856+.
   Insertions anywhere inside `:73-162` are caught: above `:119` they shift the
   DATED marker row (G15 SCOPE-ERROR, existing machinery — not re-measured
   here, it is v10 behavior kept intact), inside `:132-162` they shift
   register spans (REQUIRED-absent — measured via the seeded arms).
2. **Re-key discipline**: any legitimate PROVINCE.md frontier edit (bullet
   graduation to Core, r5-audit-style pruning) must re-key `FRONTIER[]` in the
   same commit; until then the run fails closed. Same standing rule as SCOPE.
3. **Forbidden-literal coverage is earned, not exhaustive**: only literals on
   record (the pre-arc3-r1 "untested" claim for `:91-93`; the six pruned
   pre-round-4 bullets are guarded structurally by their bullets' REQUIRED
   anchors, not by FORBIDDEN patterns) are declared. New retractions extend
   the register.

## 7. What I did NOT do

- Did not modify the gate, PROVINCE.md, SKILL.md, SCORECARD.md, corpus, or any
  tracked file (git used read-only: rev-parse/log/status/ls only).
- Did not re-derive other chains' numbers (c2 command-A counts, c3
  rule_blocks) — outside this seat's chain.
- The `--root` runs against scratch trees read live HOME configs and the npm
  cache for anchors (read-only), so `live` in scratch JSON reflects this host,
  not the tree — identical for v10 and r10, so the comparison stands.

## 8. Landing recipe for the parent

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
patch .ufo/gates/c1-census-v10.py < .ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff
sha256sum .ufo/gates/c1-census-v10.py   # expect 8002757078a685f5…e18d14aecca, 713 lines
python3 .ufo/gates/c1-census-v10.py --quiet   # expect exit 0, PASS,
  # FRONTIER register (G21): 14 rows asserted, errors: []
```

Then record post-edit identity in the landing receipt, not in the gate.
