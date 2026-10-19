# RV-1 — c1 `ptr_check` blind spot

Seat RV-1, `arc3-loop1-round7`, measured directly against the worktree. The gate was not edited. Scratch copies and the candidate instrument lived only in a `TemporaryDirectory` under `/var/tmp` and were removed on exit.

## Verdict

**C1 overall: DISCREPANCY; do not mark the clean-tree requirement verified.** The collection defect is reproduced and a narrow, receipt-anchored candidate closes the intended `:3298` case in a scratch fixture; a deliberately dead pointer fails there. But current HEAD's `PROVINCE.md:18` contains the full pointer `~/.kimi-code/config.toml:3546`, not `:3298`, and the live `ptr_check` now calls `:3546` stale. Applying the honest collector therefore FAILs on the unmodified current text. Passing current HEAD would require accepting that stale pointer without a matching receipt, or changing source outside this seat's write scope.

## First-hand re-derivations

| Item | Verdict | Evidence |
|---|---|---|
| HEAD/work identity | REPRODUCED | `git rev-parse HEAD` → `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`; `git show -s 2fba56f` → `2fba56fe7d54cfb94ca9332c11cea81667b3b289`, “arc3-loop1-round6: work — census G21 frontier register …”. |
| Census identity | REPRODUCED | `sha256sum .ufo/gates/c1-census-v10.py` → `80027570…` (`8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`); `wc -l` → `713`. |
| Baseline census | REPRODUCED | `python3 .ufo/gates/c1-census-v10.py --quiet` → exit 0, `PROVINCE.md lines=162 loci=6`, `SCORECARD.md lines=1757 loci=9`, `SKILL.md lines=413 loci=2`; G21 `14 rows asserted, errors: []`; `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. Full output follows below. |
| Blind spot | VERIFIED | `.ufo/gates/c1-census-v10.py:511-514` only searches `PTR` under `if not occ`; PIN and VER loci populate `occ` first (`:503-510`). On the `PROVINCE.md:15-26` unit, `PTR.finditer` finds the Devin `:7`, OMP `:8`, and Kimi `:3546` pointers, but the unmodified `classify()` returned `classified ptr detections=[]`. |
| Frozen `:3298` call | REPRODUCED, scope corrected | Calling `ptr_check('~/.kimi-code/config.toml', 3298, live)` returned `stale`; so did line `3546`. But current `PROVINCE.md:18` spells the full path only at `:3546`; `:3298` appears later as “receipt's pointer :3298”, without a path immediately before it, so it is not the current `PTR` regex match. The direct current pointer is `~/.kimi-code/config.toml:3546`. |
| Receipt anchor | VERIFIED as artifact; line proof UNVERIFIABLE from receipt alone | `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt` is 6 lines, SHA-256 `3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553`; line 1 is `2026-10-18T17:55:49Z`, line 4 records the Kimi config digest `bd5a78d1a829f480f12735bdfc18f6f8778e702caac7d766a776eda5597a9f3c`. It contains no `:3298` line number (`receipt_has_line_number=False`). Thus a gate register can pin the receipt identity and marker, but the receipt itself does not mechanically prove which line held the pin. |

Baseline command output (verbatim):

```text
$ python3 .ufo/gates/c1-census-v10.py --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1757 loci=9
SKILL.md       lines=413  loci=2

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
EXIT=0
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  .ufo/gates/c1-census-v10.py
713 .ufo/gates/c1-census-v10.py
```

Direct pointer-probe output (status-only; config line contents were not emitted):

```text
ptr_check(config.toml, 3298, live) -> stale
ptr_check(config.toml, 2940, live) -> stale
ptr_check(config.toml, 3227, live) -> stale
ptr_check(config.toml, 3546, live) -> stale
unit lines 15-26; PTRs=[('/home/vgpnk/.config/devin/mcp_config.json', 7), ('/home/vgpnk/.omp/agent/mcp.json', 8), ('~/.kimi-code/config.toml', 3546)]
classified ptr detections=[]
```

## Candidate patch text (NOT applied)

This minimal candidate collects pointers independently of pins/versions, preserves receipt-backed `:3298` only when the source marker and pinned receipt match, and keeps stale pointers in DATED clauses historical. It deliberately uses the pointer's own clause for inline historical classification: the word “historical” elsewhere on `PROVINCE.md:18` must not excuse the current `:3546` pointer.

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -239,3 +239,3 @@
 """
-import argparse, json, os, re, sys
+import argparse, hashlib, json, os, re, sys
 
@@ -311,2 +311,7 @@
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
+PTR_RECEIPTS = [("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3298,
+                 ".ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt",
+                 "2026-10-18T17:55:49Z",
+                 "3cba32fba1a9724c0ba3bdfdd6fe393afcc51b5354a982c3045f23cedb182553",
+                 r"17:55:49Z receipt's pointer :3298")]
 CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
@@ -483,2 +488,28 @@
 
+def receipt_ptr_check(fname, phys, ptr_path, lineno, text, root):
+    for f, source_line, registered_path, registered_line, receipt_path, stamp, digest, marker in PTR_RECEIPTS:
+        key = (fname, phys, os.path.normpath(os.path.expanduser(ptr_path)), lineno)
+        wanted = (f, source_line, os.path.normpath(os.path.expanduser(registered_path)), registered_line)
+        if key != wanted:
+            continue
+        if not re.search(marker, text, re.I):
+            return "unresolved", "receipt marker missing"
+        try:
+            raw = open(os.path.join(root, receipt_path), "rb").read()
+        except OSError as ex:
+            return "unresolved", "receipt unreadable (%s)" % type(ex).__name__
+        if hashlib.sha256(raw).hexdigest() != digest:
+            return "unresolved", "receipt identity mismatch"
+        try:
+            rows = raw.decode("utf-8").splitlines()
+        except UnicodeDecodeError:
+            return "unresolved", "receipt undecodable"
+        config_path = os.path.normpath(os.path.expanduser(registered_path))
+        receipt_row = next((r for r in rows[1:] if r.endswith("  " + config_path)), None)
+        if not rows or rows[0] != stamp or not receipt_row or not re.match(r"^[0-9a-f]{64}  ", receipt_row):
+            return "unresolved", "receipt stamp/config row mismatch"
+        return "ok", "receipt-anchored current-by-design (%s, sha256=%s)" % (stamp, digest)
+    return None
+
+
 def cache_check(h, stated):
@@ -497,3 +528,3 @@
 
-def classify(fname, lines, live, out):
+def classify(fname, lines, live, out, root):
     loci = []
@@ -510,5 +541,4 @@
             occ.append(("bare", m.start(), m.group(0)))
-        if not occ:
-            for m in PTR.finditer(text):
-                occ.append(("ptr", m.start(), m.group(0)))
+        for m in PTR.finditer(text):
+            occ.append(("ptr", m.start(), m.group(0)))
         if not occ:
@@ -539,4 +569,10 @@
                     pm = PTR.search(text, off)
-                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
-                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    receipt_state = receipt_ptr_check(fname, phys, pm.group(1), int(pm.group(2)), text, root)
+                    state, why = receipt_state if receipt_state is not None else ptr_check(pm.group(1), int(pm.group(2)), live)
+                    if state == "ok":
+                        disp = "current-ok"
+                    elif state == "stale" and (cls == "DATED" or INLINE_MARKER.search(clause)):
+                        disp, why = "historical", "dated pointer/clause"
+                    else:
+                        disp = {"stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                 elif c is None:
@@ -627,3 +663,3 @@
         filelines[f] = lines
-        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out))}
+        counts[f] = {"lines": len(lines), "loci": len(classify(f, lines, live, out, args.root))}
     scope_errors = assert_markers(filelines)
```

## Scratch measurement

The candidate gate was generated from the above text in a `/var/tmp` `TemporaryDirectory`; the repo gate remained byte-identical. The receipt fixture copied the three scoped Markdown files and the receipt file into scratch, then changed only the full Kimi pointer `:3546` → `:3298` so it matched the frozen receipt-anchored pointer. The seeded fault changed that exact scratch pointer `:3298` → `:1` (an existing config line with no REA pin). The untouched-HEAD-text case copied the current source verbatim.

```text
baseline original gate: exit=0 verdict=PASS
  counts={'PROVINCE.md': {'lines': 162, 'loci': 6}, 'SCORECARD.md': {'lines': 1757, 'loci': 9}, 'SKILL.md': {'lines': 413, 'loci': 2}}
  current_ok_per_file={'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}

candidate gate, unchanged HEAD text: exit=1 verdict=FAIL stale=1 unresolved=0
  PTR=[('PROVINCE.md', 16, '/home/vgpnk/.config/devin/mcp_config.json:7', 'current-ok'), ('PROVINCE.md', 17, '/home/vgpnk/.omp/agent/mcp.json:8', 'current-ok'), ('PROVINCE.md', 18, '~/.kimi-code/config.toml:3546', 'STALE')]
  G21=14 rows, errors=0; G2=True
  current_ok_per_file={'PROVINCE.md': 19, 'SCORECARD.md': 16, 'SKILL.md': 3}

candidate gate, receipt-anchored :3298 fixture: exit=0 verdict=PASS stale=0 unresolved=0
  PROVINCE_PTRS=[('PROVINCE.md', 16, '/home/vgpnk/.config/devin/mcp_config.json:7', 'current-ok'), ('PROVINCE.md', 17, '/home/vgpnk/.omp/agent/mcp.json:8', 'current-ok'), ('PROVINCE.md', 18, '~/.kimi-code/config.toml:3298', 'current-ok')]
  G21=14 rows, errors=0; G2=True
  current_ok_per_file={'PROVINCE.md': 20, 'SCORECARD.md': 16, 'SKILL.md': 3}

candidate gate, seeded dead-line :1 fault: exit=1 verdict=FAIL stale=1 unresolved=0
  PTR=[('PROVINCE.md', 16, '/home/vgpnk/.config/devin/mcp_config.json:7', 'current-ok'), ('PROVINCE.md', 17, '/home/vgpnk/.omp/agent/mcp.json:8', 'current-ok'), ('PROVINCE.md', 18, '~/.kimi-code/config.toml:1', 'STALE')]
  G21=14 rows, errors=0; G2=True
  current_ok_per_file={'PROVINCE.md': 19, 'SCORECARD.md': 16, 'SKILL.md': 3}

SCOPE_identical=True; FRONTIER_identical=True; FRONTIER_rows=14
JSON schema: removed=[]; added=[]; shared=19
```

The receipt fixture and seed establish the narrow register behavior, not requirement (a) on actual HEAD. The current HEAD-text copy fails because `:3546` is stale. Also, the receipt register is an explicit human adjudication anchored to the receipt artifact; the stored receipt has only a whole-file digest, not a preserved config snapshot or line-number field. Do not silently label this a fully machine-proven current pointer.

## Scope

No gate, corpus, PROVINCE, SKILL, SCORECARD, LOG, or other tracked file was edited. Only this seat artifact is intended to be written. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched. No `/tmp` scratch was used.
