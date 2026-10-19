# PL-1 — C1 `ptr_check` blind spot

**Disposition: REPRODUCED; patch text tested on scratch only.** No gate, tracked source, corpus, or custody path was modified.

## Re-derived evidence and verdicts

- **Instrument identity — VERIFIED.** From this checkout, `git rev-parse HEAD` returned `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`; `.ufo/gates/c1-census-v10.py` is 713 lines and SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`.
- **Pointer collection blind spot — REPRODUCED.** At `.ufo/gates/c1-census-v10.py:511-514`, pointer matches are collected only under `if not occ`; the `PIN`/`VER` scan at `:504-510` makes `occ` non-empty for the pin-carrying statement. The baseline gate returned PASS but serialized zero pointer assertions.
- **Claimed pointer spelling — CORRECTED.** The full path:line token in `PROVINCE.md:18` is `~/.kimi-code/config.toml:3546`. `:3298` occurs as the bare suffix in “17:55:49Z receipt's pointer :3298”, not as a second full path token. I retained both receipt-qualified locations in the candidate register; the ordinary `PTR` regex at gate `:311` finds only `:3546`.
- **Live pointer checks — VERIFIED.** Running the instrument's `ptr_check` against both captured numbers returned stale for `3298` and `3546`. Exact output (the snippet prints only status, not config contents):

  ```text
  PTR matches: [('~/.kimi-code/config.toml', '3546')]
  ptr_check states: {3298: 'stale', 3546: 'stale'}
  source line mentions capture anchors: ['17:55:49Z receipt', '2026-10-19 re-read']
  ```

- **Baseline — REPRODUCED.** `python3 .ufo/gates/c1-census-v10.py --json` on the worktree returned exit 0 / PASS with `counts` `{PROVINCE.md: 162 lines, 6 loci; SCORECARD.md: 1757 lines, 9 loci; SKILL.md: 413 lines, 2 loci}`, `pointer_assertions: 0`, `frontier_rows: 14`, `frontier_errors: []`, and `current_ok_per_file: {PROVINCE.md: 17, SCORECARD.md: 14, SKILL.md: 3}`.
- **Candidate patch — REPRODUCED on scratch.** A copy of the three scoped markdown files and gate was placed under `/var/tmp/kaidoku-pl1-r7-final-83pl5ica/`. The scratch baseline matched the worktree. The candidate PASSed the clean copy and exposed both line-18 pointers as receipt-anchored `current-ok`; it also classified the dated `SCORECARD.md:291` pointer as historical rather than introducing a stale failure.
- **Seeded dead pointer — REPRODUCED on scratch.** Re-keying only the receipt suffix `:3298` to `:999999` in scratch `PROVINCE.md` made the patched gate exit 1 with `unresolved=1`; the unchanged `:3546` reference remained receipt-anchored `current-ok`. The exact gate output is below.
- **G21 and existing counters — VERIFIED on scratch.** The candidate's G21 register text was byte-identical to the original (`G21_REGISTER_IDENTICAL=True`); clean and seeded runs each reported 14 frontier rows and no frontier errors. Clean-run `counts`/loci, G2 verdict, scope errors, G7/G11 lists, and declared fail classes matched baseline. `current_ok_per_file` rose only for new positive detections: PROVINCE 17→19 and SCORECARD 14→16; SKILL remained 3.

## Patch text (not applied)

```diff
@@ -309,6 +309,12 @@
 PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
 VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
+PTR_RECEIPTS = [
+    ("PROVINCE.md", 18, r"~/.kimi-code/config\.toml:(\d+)",
+     "~/.kimi-code/config.toml", 3546, r"2026-10-19 re-read"),
+    ("PROVINCE.md", 18, r"17:55:49Z receipt's pointer\s+:(\d+)",
+     "~/.kimi-code/config.toml", 3298, r"17:55:49Z receipt"),
+]
 CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
 REA_GATE = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)
 INLINE_MARKER = re.compile(r"historical|verified 2026-10-13|not re-probed|superseded|baseline|retain their original", re.I)
@@ -481,6 +487,17 @@
     return "ok", "pins %s" % m.group(1)
 
 
+def ptr_receipt(fname, source_line, source_text, ptr_path, lineno):
+    for f, line, source, path, expected, anchor in PTR_RECEIPTS:
+        if (f != fname or line != source_line or path != ptr_path
+                or expected != lineno):
+            continue
+        match = re.search(source, source_text)
+        if match and int(match.group(1)) == lineno and re.search(anchor, source_text):
+            return anchor
+    return None
+
+
 def cache_check(h, stated):
@@ -508,9 +525,22 @@
             if any(s <= m.start() < e for s, e in spans):
                 continue
             occ.append(("bare", m.start(), m.group(0)))
-        if not occ:
-            for m in PTR.finditer(text):
+        version_occ = tuple(occ)
+        for m in PTR.finditer(text):
+            lo, hi = clause_bounds(text, m.start())
+            shares_version_clause = any(kind in ("pin", "bare") and lo <= off < hi
+                                        for kind, off, _ in version_occ)
+            if not version_occ or shares_version_clause:
+                occ.append(("ptr", m.start(), m.group(0)))
+        for f, source_line, source, ptr_path, expected, anchor in PTR_RECEIPTS:
+            if fname != f:
+                continue
+            for m in re.finditer(source, text):
+                if line_of(lines, a, b, m.start(1)) != source_line:
+                    continue
+                value = "%s:%s" % (ptr_path, m.group(1))
+                if not any(kind == "ptr" and val == value for kind, _, val in occ):
+                    occ.append(("ptr", m.start(1), value))
         if not occ:
             continue
@@ -536,9 +566,26 @@
                     state, why = cache_check(cache_h.group(1), val)
                     disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                 elif c == "__ptr__":
-                    pm = PTR.search(text, off)
-                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
-                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    pm = PTR.fullmatch(val)
+                    if pm:
+                        ptr_path, ptr_line = pm.group(1), int(pm.group(2))
+                        state, live_why = ptr_check(ptr_path, ptr_line, live)
+                        anchor = ptr_receipt(fname, phys, lines[phys - 1], ptr_path, ptr_line)
+                        if anchor:
+                            live_state = state
+                            state, why = "ok", "receipt-anchored %s; live ptr_check=%s" % (anchor, live_state)
+                        elif state == "ok":
+                            why = live_why
+                        elif state == "unresolved":
+                            why = live_why
+                        elif cls == "DATED" or inline:
+                            state, why = "historical", "dated scope" if cls == "DATED" else "inline marker"
+                        else:
+                            state, why = "stale", live_why
+                    else:
+                        state, why = "unresolved", "malformed pointer locus: %r" % val
+                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED",
+                            "historical": "historical"}[state]
```

## Scratch outputs

Patched clean copy (`python3 c1-census-v10.py --root <scratch>/repo`):

```text
exit: 0
:18 [ptr] __ptr__=~/.kimi-code/config.toml:3546 -> current-ok (receipt-anchored 2026-10-19 re-read; live ptr_check=stale)
:18 [ptr] __ptr__=~/.kimi-code/config.toml:3298 -> current-ok (receipt-anchored 17:55:49Z receipt; live ptr_check=stale)
:288 [ptr] __ptr__=~/.config/devin/mcp_config.json:7 -> current-ok (pins 6.5.0)
:289 [ptr] __ptr__=~/.omp/agent/mcp.json:8 -> current-ok (pins 6.5.0)
:291 [ptr] __ptr__=~/.kimi-code/config.toml:1478 -> historical (dated scope)
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=19, SCORECARD.md=16, SKILL.md=3; total loci=17; floor=1/file)
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Seeded copy (one scratch-only replacement `17:55:49Z receipt's pointer :3298` → `:999999`):

```text
exit: 1
:18 [ptr] __ptr__=~/.kimi-code/config.toml:3546 -> current-ok (receipt-anchored 2026-10-19 re-read; live ptr_check=stale)
:18 [ptr] __ptr__=~/.kimi-code/config.toml:999999 -> UNRESOLVED (line 999999 beyond EOF (4150 lines))
:288 [ptr] __ptr__=~/.config/devin/mcp_config.json:7 -> current-ok (pins 6.5.0)
:289 [ptr] __ptr__=~/.omp/agent/mcp.json:8 -> current-ok (pins 6.5.0)
:291 [ptr] __ptr__=~/.kimi-code/config.toml:1478 -> historical (dated scope)
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=18, SCORECARD.md=16, SKILL.md=3; total loci=17; floor=1/file)
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=1)
```

The receipt allowlist is intentionally explicit and line-bound: those two current-tree pointers have stale live `ptr_check` results, so the output preserves that raw result while the exact captured statements are accepted as current-by-design. A changed line number cannot match the expected receipt entry and falls through to ordinary live classification. Any additional or updated receipt needs a re-derived anchor and registry entry.
