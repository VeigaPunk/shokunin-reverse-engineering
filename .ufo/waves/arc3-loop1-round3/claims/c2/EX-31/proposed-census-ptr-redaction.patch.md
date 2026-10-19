# Proposed patch text — census pointer-miss output redaction (finding F1)

Seat EX-31 (late join, chain c2) · wave `arc3-loop1-round3` · 2026-10-19.
Target: `.ufo/gates/c1-census-v10.py` — **chain c1's instrument**. This seat does
not own it and did not edit it; the change below is patch TEXT only (frozen
rule: no seat edits another chain's instrument).

Finding and reproduction: `evidence/independent/secret-echo-finding.txt`.
Class: a pointer-miss reason string embeds up to 60 characters of the *target
file's* line, and the reporter prints reason strings verbatim — so grading a
document can copy arbitrary target-file content (here, an API-key line) into
census output and into whatever captures that output.

Minimal, behaviour-preserving change (two hunks; exit classes and verdicts are
unchanged — only the reason string's payload):

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -378,4 +378,6 @@ def ptr_check(ptr_path, lineno, live):
     content = lines[lineno - 1]
     m = re.search(r"rea-agents@(\d+\.\d+\.\d+)", content)
     if not m:
-        return "stale", "line holds no rea-agents pin: %r" % content.strip()[:60]
+        # never echo target-file content: it may hold operator secrets
+        return "stale", ("line holds no rea-agents pin (sha256=%s, %d chars)"
+                         % (hashlib.sha256(content.strip().encode()).hexdigest()[:16],
+                            len(content.strip())))
```

and the import line near the top (`import argparse, json, os, re, sys` →
`import argparse, hashlib, json, os, re, sys`).

Measured equivalence: verdicts and exit codes for all eight variants of
`evidence/independent/variant-*.txt` depend only on the `state` token returned by
`ptr_check` (`"stale"`), never on the reason string; the reporter's `-> %s (%s)`
format keeps the same shape, so no consumer parsing on `no rea-agents pin` sees a
structural change — only the parenthetical payload. Re-run the census before and
after the change and `diff` the verdict lines (expect identical).

Coupled-landing note: this instrument is read by no gate inside the round; the
change is inert to command A and to every round-3 acceptance test. Landing it is
the operator's call, not this wave's.
