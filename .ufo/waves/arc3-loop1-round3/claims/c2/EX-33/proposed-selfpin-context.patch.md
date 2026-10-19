# self-pin context — PATCH TEXT (seat EX-33, chain c2, arc3-loop1-round3)

Target: `.ufo/gates/custody-pair/custody-pair.py` (**EX-21's write target** —
this seat does not edit it; patch text only). Anchors verified at the settled
revision `7cd19c3c…`: `:295` (`tool_sha = …`) and `:300` (`"# tool: %s  sha256 %s"`).

Measured basis (this seat's audit, `claims/c2/EX-33/selfpin.md`):
- A1: the pin is a render-time disk read, so it can name bytes that did not
  execute (deterministic demo: executed `112d01dc…`, pin `a37cf1af…`).
- A3: copies are indistinguishable in the header except by hash — the basename
  is all the header carries (`# tool: tool.py sha256 0ce819c3…` from a scratch copy).
- A6: a vanished tool pins `(unavailable)`; such a receipt still verifies cleanly.

Claim-free change (three additive lines + one start-time hash), all read-only:

```diff
 TOOL_PATH = Path(__file__).resolve()
+TOOL_SHA_AT_START = sha256_file(TOOL_PATH) if TOOL_PATH.exists() else "(unavailable)"
@@ render_receipt
-    tool_sha = sha256_file(TOOL_PATH) if TOOL_PATH.exists() else "(unavailable)"
+    tool_sha = sha256_file(TOOL_PATH) if TOOL_PATH.exists() else "(unavailable)"
     ...
-        "# tool: %s  sha256 %s" % (TOOL_PATH.name, tool_sha),
+        "# tool: %s  sha256 %s" % (TOOL_PATH.name, tool_sha),
+        "# tool-path: %s" % TOOL_PATH,
+        "# tool-sha-at-start: %s" % TOOL_SHA_AT_START,
+        ("# tool-window: WARN tool file changed during this capture (start %s end %s)"
+         % (TOOL_SHA_AT_START, tool_sha)) if TOOL_SHA_AT_START != tool_sha else
+        "# tool-window: stable",
```

Rationale, one line each:
- `tool-path` makes copies distinguishable from the canonical file without a hash
  lookup (A3).
- `tool-sha-at-start` + `# tool-window:` turn A1 from a silent misattribution into
  a visible warning; a receipt that pins bytes that never ran is now self-labelled.
- No exit-class change is proposed: the receipt remains written (the audit's
  reader-side check C1/C2 stays authoritative), so the declared map is untouched.

What this does NOT fix (named, not implied): the pin still is not an anchor —
receivers must keep cross-checking it (A4), and D5's threat-model sentence still
governs. Selftest impact: none of the existing 22 cases reads these lines; two
new cases would pin the window behavior if the implementer wants coverage.