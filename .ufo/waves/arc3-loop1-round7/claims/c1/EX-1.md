# EX-1 — C1 pointer reachability

**Disposition:** `classify()` blind spot VERIFIED; patch candidate and seeded-fault result REPRODUCED. The frozen claim’s exact source pointer is CORRECTED below. No gate or tracked source file was changed; patch text and tests are scratch-only.

## First-hand re-derivation

- HEAD is `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`; `.ufo/gates/c1-census-v10.py` is 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`.
- Existing collector at `.ufo/gates/c1-census-v10.py:511-514` only searches `PTR` when `occ` is empty. Direct import/run against current `PROVINCE.md:18`:

```text
PTR.finditer(PROVINCE.md:18)= [('~/.kimi-code/config.toml', 3546)]
classify pointer detections= []
```

  Thus the `@6.7.0` pin in the same `units()` block prevents the only full `path:line` token in that line from reaching `ptr_check()`.
- **Frozen-target correction:** the current source’s full path pointer is `~/.kimi-code/config.toml:3546`, not `:3298`. The strings `:3298`, `:2940`, and `:3227` on that line are bare line suffixes; `PTR` does not match them. `ptr_check(:3298)=stale` is reproducible if called directly, but the current collector does not receive it as a path-pointer token.
- Current live state was independently checked without printing config contents: SHA-256 `977da8727fff68f0a9a139ebdde7e01f09fb3557378990815ac7d7e2d0e583a9`, 4,150 lines, Kimi pin `rea-agents@6.7.0` at line 4,126. `ptr_check(:4126)=ok; pins 6.7.0`; `ptr_check(:3546)=stale; line has no rea-agents pin`. The `:3298`, `:2940`, and `:3227` calls also return stale / no pin.
- The round-1 cross custody receipt `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` independently hashes to `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776`; it contains capture `2026-10-19T09:57:18Z` and captured config hash `8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d`. That captured hash differs from the live config hash above. The proposed register treats the exact `PROVINCE.md:18` pointer as receipt-current-by-design, not as a claim that `:3546` still resolves in today’s live file.

Unmodified gate, `python3 .ufo/gates/c1-census-v10.py --json --root .` (exit 0), selected output:

```json
{"counts":{"PROVINCE.md":{"lines":162,"loci":6},"SCORECARD.md":{"lines":1757,"loci":9},"SKILL.md":{"lines":413,"loci":2}},"current_ok_per_file":{"PROVINCE.md":17,"SCORECARD.md":14,"SKILL.md":3},"frontier_errors":[],"frontier_rows":14,"g2_ok":true,"scope_errors":[],"stale":0,"unresolved":0,"verdict":"PASS"}
```

## Proposed patch text — NOT applied

The receipt rows bind exact file/line/path values to receipt file digests, capture stamps, and captured config hashes. Row `:3298` is retained for the frozen receipt-pointer case; it is dormant against today’s source because there is no full path token at `:3298`.

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -237,7 +237,7 @@
 Exit 0 PASS, 1 FAIL, 2 anchor failure.
 Usage: python3 c1-census-v10.py [--root DIR] [--json] [--quiet]
 """
-import argparse, json, os, re, sys
+import argparse, hashlib, json, os, re, sys
 
 HOME = os.path.expanduser("~")
 CLIENTS = {"devin": HOME + "/.config/devin/mcp_config.json",
@@ -318,6 +318,34 @@
 CLAUSE_SPLIT = re.compile(r"[;()\u2014\u2013]|\.\s")
 HOLDING = re.compile(r"\bheld\b|live[- ]verified", re.I)
 HOLDING_OK = re.compile(r"configured|available|not held|availability|never stands", re.I)
+PTR_RECEIPTS = {
+    ("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3546): (
+        ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt",
+        "b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776",
+        "2026-10-19T09:57:18Z",
+        "8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d"),
+    ("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3298): (
+        ".ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt",
+        "3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553",
+        "2026-10-18T17:55:49Z",
+        "bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c")
+}
+
+
+def receipt_ptr(fname, phys, ptr_path, lineno, root):
+    record = PTR_RECEIPTS.get((fname, phys, ptr_path, lineno))
+    if record is None:
+        return None
+    receipt, digest, captured, config_digest = record
+    try:
+        data = open(os.path.join(root, receipt), "rb").read()
+    except OSError as ex:
+        return "unresolved", "receipt unreadable (%s)" % type(ex).__name__
+    text = data.decode("utf-8", "replace")
+    if hashlib.sha256(data).hexdigest() != digest or captured not in text \
+       or config_digest not in text:
+        return "unresolved", "receipt anchor mismatch %s" % receipt
+    return "ok", "receipt-current by design (%s, %s)" % (receipt, captured)
 
 
 def live_pins():
@@ -495,7 +523,7 @@
     return "ok", "cache holds %s" % m.group(1)
 
 
-def classify(fname, lines, live, out):
+def classify(fname, lines, live, out, root):
     loci = []
     for (a, b, text) in units(lines):
         if not REA_GATE.search(text):
@@ -508,9 +536,8 @@
             if any(s <= m.start() < e for s, e in spans):
                 continue
             occ.append(("bare", m.start(), m.group(0)))
-        if not occ:
-            for m in PTR.finditer(text):
-                occ.append(("ptr", m.start(), m.group(0)))
+        for m in PTR.finditer(text):
+            occ.append(("ptr", m.start(), m.group(0)))
         if not occ:
             continue
         det = []
@@ -537,8 +564,17 @@
                     disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                 elif c == "__ptr__":
                     pm = PTR.search(text, off)
-                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
-                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    ptr_path, ptr_line = pm.group(1), int(pm.group(2))
+                    receipt = receipt_ptr(fname, phys, ptr_path, ptr_line, root)
+                    if receipt is None:
+                        state, why = ptr_check(ptr_path, ptr_line, live)
+                        if state == "stale" and (cls == "DATED" or inline):
+                            disp, why = "historical", "dated scope" if cls == "DATED" else "inline marker"
+                        else:
+                            disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    else:
+                        state, why = receipt
+                        disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                 elif c is None:
                     if cls == "DATED":
                         disp, why = "historical", "dated scope"
@@ -625,7 +661,7 @@
             filelines[f] = None
             continue
         filelines[f] = lines
-        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
+        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out, args.root))}
     scope_errors = assert_markers(filelines)
     frontier_errors = frontier_check(filelines)
     stale, unatt = out.get("STALE", []), out.get("AMBIGUOUS", [])
```

## Scratch verification

Scratch roots: `/var/tmp/kaidoku-c1-ex1.RB0rD3` (candidate against copied current docs/receipts) and `/var/tmp/kaidoku-c1-ex1-fault.2v4AfI` (same candidate, with only `PROVINCE.md:18` re-keyed from `:3546` to `:999999`). `python3 -m py_compile .ufo/gates/c1-census-v10.py` passed in the candidate scratch root.

Final artifact validation: extracted this file's fenced diff and applied it to a fresh gate copy at `/var/tmp/kaidoku-c1-ex1-verified.zsRJgq/patch-root`; `python3 -m py_compile` passed. The patched gate returned PASS on copied current inputs (PROVINCE loci=6; G21=14; no frontier errors; G2=true). Re-keying only `PROVINCE.md:18` to `:999999` returned FAIL / exit 1 with `~/.kimi-code/config.toml:999999` as `UNRESOLVED` (`line 999999 beyond EOF (4150 lines)`).

Candidate baseline command, exit 0:

```json
{"counts":{"PROVINCE.md":{"lines":162,"loci":6},"SCORECARD.md":{"lines":1757,"loci":9},"SKILL.md":{"lines":413,"loci":2}},"current_ok_per_file":{"PROVINCE.md":20,"SCORECARD.md":16,"SKILL.md":3},"frontier_errors":[],"frontier_rows":14,"g11":[],"g2_ok":true,"scope_errors":[],"stale":0,"unresolved":0,"verdict":"PASS"}
```

The six newly reachable full pointers classified as expected: Devin `:7`, OMP `:8`, and receipt-current-by-design Kimi `:3546` in PROVINCE; Devin `:7` and OMP `:8` in the dated SCORECARD block; Kimi `:1478` in the dated SCORECARD block as `historical`. `counts.loci` and G21 stay unchanged; `current_ok_per_file` rises because the new valid pointer detections are counted by the existing G2 floor.

Seeded-fault command outcome, exit 1:

```json
{"current_ok_per_file":{"PROVINCE.md":19,"SCORECARD.md":16,"SKILL.md":3},"frontier_errors":[],"frontier_rows":14,"g2_ok":true,"gate_exit":1,"unresolved_ptrs":[{"assert":{"client":"__ptr__","disp":"UNRESOLVED","kind":"ptr","line":18,"marker":"inline:18","scope":"CURRENT","value":"~/.kimi-code/config.toml:999999","why":"line 999999 beyond EOF (4150 lines)"},"file":"PROVINCE.md"}],"verdict":"FAIL"}
```

**Residual for the integrator:** today’s live config proves `:3546` is stale and places the pin at `:4126`; the baseline candidate PASS is specifically the requested receipt-register adjudication, not live-line currentness. The full path `:3298` described in frozen claims is absent from current `PROVINCE.md:18` as a path token, so decide whether to reconcile that frozen/source mismatch before landing. This seat did not edit the gate, PROVINCE, or any custody file.
