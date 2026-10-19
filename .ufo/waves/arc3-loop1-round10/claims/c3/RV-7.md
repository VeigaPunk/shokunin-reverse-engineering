# RV-7 — C3 G21 append-boundary instrument check

**Chain:** c3 (operability)
**Selected move:** close the G21 residual where an added Frontier bullet after the last registered line is not graded.
**Scope:** patch text and scratch measurement only. The tracked gate and custody tool were not edited.

## Independent re-derivation

- The frozen roster assigns RV-7 to c3; C3 requires patch text plus a seeded scratch measurement (`claims-frozen.md:51-65, 67-72`).
- `git rev-parse HEAD` → `5694506a862c32d2f7aac44935778bce4b6184f2`.
- `sha256sum .ufo/gates/c1-census-v10.py` → `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`.
- `PROVINCE.md` has 162 lines; its last Frontier bullet is at `PROVINCE.md:161-162`. The 14 G21 rows occupy `PROVINCE.md:75-93` and `:135-162` (`c1-census-v10.py:292-308`). The gate’s own residual is recorded at `c1-census-v10.py:114-116`.
- `frontier_check()` evaluates only the declared rows and their spans (`c1-census-v10.py:422-444`); it does not enumerate Frontier bullets outside those spans. The run’s `max_end` check rejects truncation but not growth (`:613-629`). An unregistered bullet with no L3-recognized locus therefore escapes the existing checks.
- The tracked gate and `PROVINCE.md` were clean under `git status --short -- .ufo/gates/c1-census-v10.py PROVINCE.md` before this artifact was written.

**VERIFIED — live baseline.** Command: `python3 .ufo/gates/c1-census-v10.py --quiet` (run at HEAD, not a quoted prior result). Exact output:

```text
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
exit=0
```

## Seeded-fault measurement on scratch

Scratch inputs are under `/var/tmp/kaidoku-rv7-g21-verified-hdlg15to/root` (copies of `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md`). Only the scratch `PROVINCE.md` was changed. Its new line 163 is:

```text
- **Seeded RV-7 fault** — real solc/vyper-compiled bytecode untested.
```

Scratch `PROVINCE.md` SHA-256: `bbc9fbd79b05d18346b755d568bd6f80c7e282066aaf66333fa54491ebf64c97`.

**REPRODUCED — unpatched gate silently passes the fault.** Command:
`python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py --root /var/tmp/kaidoku-rv7-g21-verified-hdlg15to/root --quiet`

```text
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit=0
```

## Patch text — not applied to the instrument

The scratch-only candidate adds a closed-world check for Markdown bullets under headings whose text contains “Frontier.” It treats any bullet start not represented by a registered row start as unevaluable; the existing classifier then declares `FRONTIER-UNEVALUABLE` and fails the run (`c1-census-v10.py:667-680`).

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -441,6 +441,25 @@
             if m:
                 errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                             % (f, s, e, pat, m.group(0)))
+    for f in sorted({row[0] for row in FRONTIER}):
+        lines = filelines.get(f)
+        if not lines:
+            continue
+        registered = {s for row_file, s, _, _, _ in FRONTIER
+                      if row_file == f and 1 <= s <= len(lines)
+                      and BULLET.match(lines[s - 1])}
+        level = None
+        for i, line in enumerate(lines):
+            heading = SECTION.match(line)
+            if heading:
+                new_level = len(line) - len(line.lstrip("#"))
+                if level is not None and new_level <= level:
+                    level = None
+                if re.search(r"\bfrontier\b", line, re.I):
+                    level = new_level
+                continue
+            if level is not None and BULLET.match(line) and i + 1 not in registered:
+                errs.append("%s:%d unregistered frontier bullet (G21)" % (f, i + 1))
     return errs
```

A first scratch draft matched against the `SECTION` regex fragment instead of the full heading text and did not detect the fault; it was corrected before the final measurement below. The diff above is the corrected version actually tested.

**VERIFIED — corrected scratch patch detects the seeded fault.** Command:
`python3 /var/tmp/kaidoku-rv7-g21-verified-hdlg15to/c1-census-v10-patched.py --root /var/tmp/kaidoku-rv7-g21-verified-hdlg15to/root --quiet`

```text
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 unregistered frontier bullet (G21)']
DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit=1
```

**VERIFIED — no false positive on the current input.** Running that same patched scratch gate against the unmodified repository input (162-line `PROVINCE.md`) returned `FRONTIER register (G21): 14 rows asserted, errors: []`, `DECLARED FAIL CLASSES: []`, `VERDICT: PASS`, exit 0.

## Per-item verdicts

- **G21 append-past-162 gap — VERIFIED / REPRODUCED.** The unpatched gate returned PASS and zero frontier errors with the seeded line at `PROVINCE.md:163` in scratch.
- **Proposed gate improvement — VERIFIED on scratch only.** The corrected patch rejects the seeded unregistered bullet as `FRONTIER-UNEVALUABLE`; the current input still passes. No source edit is requested or made by this seat.
- **Custody-pair candidate — UNVERIFIABLE / not selected.** This seat chose the instrument residual and did not re-measure custody-pair coverage.

**Remaining boundary:** this check detects unregistered Markdown bullets in headings containing “Frontier”; renaming a section so its heading no longer contains that word, or adding non-bullet prose claims, is outside this patch’s measured scope. Integration should apply the patch and re-run the gate in the landing worktree.
