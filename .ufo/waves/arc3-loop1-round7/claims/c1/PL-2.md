# PL-2 — c1 pointer-instrument seat

## Finding and verdicts

- **VERIFIED — baseline PASS and suppression:** at `HEAD=ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`, `.ufo/gates/c1-census-v10.py` is 713 lines and SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`. `python3 .ufo/gates/c1-census-v10.py --json` exited 0 with `verdict=PASS`, counts `PROVINCE.md={lines:162,loci:6}`, `SCORECARD.md={lines:1757,loci:9}`, `SKILL.md={lines:413,loci:2}`, `frontier_rows=14`, `frontier_errors=[]`, `declared_fail_classes=[]`. Baseline `classify('PROVINCE.md', ...)` block `15-26` had pin/bare assertions and `pointer_asserts=[]`.
- **CORRECTED — exact blind-spot description:** `.ufo/gates/c1-census-v10.py:511-514` collects `PTR` only under `if not occ`; thus the paragraph's pins/bare versions suppress all pointers. Independently, `PROVINCE.md:18` contains the full pointer `~/.kimi-code/config.toml:3546` plus the shorthand receipt reference `:3298` (and shorthand older `:2940`, `:3227`). The existing `PTR` regex at `.ufo/gates/c1-census-v10.py:311` matches only path-plus-line, so `:3298` is not itself a regex match and needs explicit receipt registration. `ptr_check('~/.kimi-code/config.toml', 3546, live)` returned state `stale`; the same direct call for line `3298` also returned `stale`. Devin `...mcp_config.json:7` and OMP `...mcp.json:8` returned `ok`.
- **REPRODUCED — scratch patch:** the patch text below, applied only to `/var/tmp/kaidoku-pl2.DQWcLP`, read the unmodified current source tree as `PASS` (exit 0). JSON key set, `counts`, `frontier_rows=14`, `frontier_errors=[]`, `scope_errors=[]`, `unreadable=[]`, `declared_fail_classes=[]`, `g2_ok=true`, `g2_floor="1/readable-file"`, `g11=[]`, and `g7=[]` matched the original run. Existing `current_ok_per_file` retained its meaning and reflected the new detections: Province 17→21, Scorecard 14→16, Skill 3→3. The dated Scorecard pointer at `SCORECARD.md:291` (`:1478`) was detected but adjudicated historical under its DATED scope, avoiding a false current-tree failure.
- **REPRODUCED — seeded failures:** on two additional scratch trees, changing the full Province pointer `:3546` to `:999999` produced `exit=1`, `FAIL`, one unresolved record, and detected `~/.kimi-code/config.toml:999999 -> UNRESOLVED`; changing it to `:3298` produced `exit=1`, `FAIL`, one stale record, and detected the direct full-path pointer `~/.kimi-code/config.toml:3298 -> STALE`. The registered receipt shorthand `:3298` remained `current-ok` by its exact receipt anchor in both tests. G21 remained 14 rows with no errors. These changes were confined to scratch copies.
- `python3 -m py_compile /var/tmp/kaidoku-pl2.DQWcLP/.ufo/gates/c1-census-v10.py` exited 0. The tracked gate was not edited.

## Patch text only — not applied to `.ufo/gates/c1-census-v10.py`

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -311,2 +311,8 @@
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
+PTR_RECEIPTS = [
+    ("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3546,
+     r"(?P<ptr>~/.kimi-code/config\.toml:3546)` at the 2026-10-19 re-read"),
+    ("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3298,
+     r"17:55:49Z receipt's pointer (?P<ptr>:3298)"),
+]
 CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
@@ -498,1 +504,11 @@
+def ptr_receipt_anchor(fname, phys, val, text, off):
+    for f, line, path, lineno, pattern in PTR_RECEIPTS:
+        if fname != f or phys != line or val != "%s:%d" % (path, lineno):
+            continue
+        match = re.search(pattern, text, re.I)
+        if match and match.start("ptr") == off:
+            return pattern
+    return None
+
+
 def classify(fname, lines, live, out):
@@ -510,5 +526,14 @@
             occ.append(("bare", m.start(), m.group(0)))
-        if not occ:
-            for m in PTR.finditer(text):
-                occ.append(("ptr", m.start(), m.group(0)))
+        ptr_matches = list(PTR.finditer(text))
+        for m in ptr_matches:
+            occ.append(("ptr", m.start(), m.group(0)))
+        for f, receipt_line, receipt_path, receipt_lineno, pattern in PTR_RECEIPTS:
+            if f != fname or not (a + 1 <= receipt_line <= b + 1):
+                continue
+            match = re.search(pattern, text, re.I)
+            off = (match.start("ptr") if match else
+                   sum(len(lines[k].strip()) + 1 for k in range(a, receipt_line - 1)))
+            if not any(m.start() == off for m in ptr_matches):
+                occ.append(("ptr-receipt", off,
+                            "%s:%d" % (receipt_path, receipt_lineno)))
         if not occ:
@@ -538,5 +563,15 @@
                 elif c == "__ptr__":
-                    pm = PTR.search(text, off)
-                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
-                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    ptr_path, ptr_line = val.rsplit(":", 1)
+                    live_state, live_why = ptr_check(ptr_path, int(ptr_line), live)
+                    anchor = ptr_receipt_anchor(fname, phys, val, text, off)
+                    if kind == "ptr-receipt" and anchor is None:
+                        state, why = "unresolved", "registered receipt anchor absent"
+                    elif anchor:
+                        state, why = "ok", "receipt-anchored; live ptr_check=%s" % live_state
+                    elif cls == "DATED" and live_state != "ok":
+                        state, why = "historical", "dated scope"
+                    else:
+                        state, why = live_state, live_why
+                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED",
+                            "historical": "historical"}[state]
                 elif c is None:
```
