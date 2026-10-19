# PL-3 — G21 unregistered Frontier bullet guard

## Disposition

- **VERIFIED — live baseline / identity.** `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`; `sha256sum .ufo/gates/c1-census-v10.py` → `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`. Fresh `python3 .ufo/gates/c1-census-v10.py --root . --quiet` → PASS, exit 0 (output below).
- **REPRODUCED — named G21 gap.** The unchanged instrument silently accepts a synthetic bullet appended at physical line 163: G21 stays `14 rows asserted, errors: []`, and the instrument returns PASS/0.
- **REPRODUCED — proposed guard on scratch only.** Applying the patch text below to a scratch copy of the gate flags that same line as `FRONTIER-UNEVALUABLE`, returns FAIL/1; a clean-tree scratch with the patch remains PASS/0.
- **Not landed.** No gate, custody path, PROVINCE.md, SKILL.md, SCORECARD.md, LOG.md, or corpus file was edited. The only repository artifact from this seat is this proposal/report.

## First-hand re-derivation

- `.ufo/gates/c1-census-v10.py:95-116` records the G21 residual. The live `FRONTIER` register has 14 entries and its final range is `PROVINCE.md:161-162` (`:292-308`). `frontier_check()` grades only each registered span by matching REQUIRED/FORBIDDEN text (`:422-444`); it does not enumerate bullet starts outside those spans.
- The live `PROVINCE.md` ends at line 162. The last registered frontier bullet is `PROVINCE.md:161-162`; the seeded bullet therefore starts at line 163.
- Re-derived live Kimi pin: read-only scan of `/home/vgpnk/.kimi-code/config.toml` printed `path=/home/vgpnk/.kimi-code/config.toml lines=4150 matches=1` and `4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`.

Baseline command and exact output excerpt:

```text
$ python3 .ufo/gates/c1-census-v10.py --root . --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1924 loci=11
SKILL.md       lines=413  loci=2
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=18, SKILL.md=3; total loci=19; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
```

## Seeded-fault measurement

Scratch root: `/var/tmp/kaidoku-pl3-confirm-ou6bnyel/root` (copies of the three files read by the gate). Seed: `- **PL-3 seeded unregistered Frontier bullet** — synthetic fault injection.`; read-back output: `SEED_LINE=163:- **PL-3 seeded unregistered Frontier bullet** — synthetic fault injection.` Neither the tracked gate nor any custody path was a write target.

Unmodified gate against the seeded root:

```text
$ python3 .ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-pl3-confirm-ou6bnyel/root --quiet
PROVINCE.md    lines=163  loci=6
SCORECARD.md   lines=1924 loci=11
SKILL.md       lines=413  loci=2
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
```

Patched-copy test used `/var/tmp/kaidoku-pl3-confirm-ou6bnyel/c1-census-v10-patched-copy.py` with the same seeded root:

```text
PROVINCE.md    lines=163  loci=6
SCORECARD.md   lines=1924 loci=11
SKILL.md       lines=413  loci=2
FRONTIER register (G21): 14 rows asserted, errors: ["PROVINCE.md:163 unregistered bullet in '### Round-4 frontier (post-unlock)' (FRONTIER-UNEVALUABLE)"]
DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=1
```

Control: the same patched copy on clean scratch `/var/tmp/kaidoku-pl3-clean-wjsyctov` gave `PROVINCE.md lines=162 loci=6`, `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0.

## Proposed patch text — not applied to the instrument

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -307,6 +307,11 @@
     ("PROVINCE.md", 161, 162, [r"Operator-gated", r"\bIDA\b"], []),
 ]
 
+FRONTIER_SECTIONS = (
+    ("PROVINCE.md", "## Frontier", 2),
+    ("PROVINCE.md", "### Round-4 frontier (post-unlock)", 3),
+)
+
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
 VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
@@ -441,6 +446,27 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    registered_starts = {(f, s) for f, s, e, req, forb in FRONTIER}
+    for f, heading, level in FRONTIER_SECTIONS:
+        lines = filelines.get(f)
+        if not lines:
+            continue
+        starts = [i for i, line in enumerate(lines) if line.strip() == heading]
+        if len(starts) != 1:
+            errs.append("%s: heading %r occurs %d times (FRONTIER-UNEVALUABLE)"
+                        % (f, heading, len(starts)))
+            continue
+        start = starts[0]
+        end = len(lines)
+        for i in range(start + 1, len(lines)):
+            match = SECTION.match(lines[i])
+            if match and len(match.group(0).split()[0]) <= level:
+                end = i
+                break
+        for i in range(start + 1, end):
+            if BULLET.match(lines[i]) and (f, i + 1) not in registered_starts:
+                errs.append("%s:%d unregistered bullet in %r (FRONTIER-UNEVALUABLE)"
+                            % (f, i + 1, heading))
     return errs
```

The check keys off the two Markdown Frontier sections and exact registered row start lines. It reports a moved/missing/duplicate section heading as unevaluable, and any bullet start within either section that has not been keyed by a G21 row also fails unevaluable, requiring the register and text to be reviewed together. The existing REQUIRED/FORBIDDEN grading and L1 SCOPE ranges remain unchanged.
