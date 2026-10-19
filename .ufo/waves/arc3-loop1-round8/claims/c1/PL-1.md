# PL-1 — C1 `ptr_check` extension

**Disposition:** the blind spot is VERIFIED; the live `:4126` anchor is VERIFIED; the scratch candidate and seeded-fault behavior are REPRODUCED. The checked-out `PROVINCE.md:18` still contains `:3546`, so the clean acceptance run below simulates C2’s re-anchor on scratch only. The candidate patch was never applied to the gate or any tracked file.

## First-hand re-derivation

- Checkout HEAD: `904b724258fc9396a016bd9952b5cd40225fb7d8`. Gate identity: `.ufo/gates/c1-census-v10.py`, 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`.
- Blind spot VERIFIED: `classify()` only collects `PTR` matches under `if not occ` (`.ufo/gates/c1-census-v10.py:511-514`). On the current `PROVINCE.md`, direct `classify()` returned `BASELINE_CLASSIFY_PROVINCE_LINE_18_PTR=[]` even though line 18 contains both a pin and a full path pointer.
- Live anchor VERIFIED. Targeted grep returned:

  ```text
  /home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  ```

  The gate’s independently re-derived anchors were `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`; direct `ptr_check('~/.kimi-code/config.toml', 4126, live)` returned `('ok', 'pins 6.7.0')`. Direct check of `:3546` returned `stale`.
- Source discrepancy VERIFIED: current `PROVINCE.md:18` still says `~/.kimi-code/config.toml:3546`; no source file was changed here. On that original pointer, the candidate correctly returns `STALE`/exit 1. It does not let the line’s separate `historical` wording excuse a stale pointer in CURRENT scope.
- Baseline acceptance DISCREPANCY: the unmodified gate is already FAIL on this checkout, independently of C1. `SCORECARD.md` has 1,813 lines, while the gate’s last declared SCORECARD range ends at 855. `python3 .ufo/gates/c1-census-v10.py --root . --json` returned exit 1 with one UNDECLARED block, `SCORECARD.md` block `1776-1783`, pin/bare values at line 1780. The proposed patch adds a narrow DATED row for the measured R7 section (`1759-1813`, marker at 1759); without that scope repair a claimed clean PASS would be false. The marker is `SCORECARD.md:1759`, `## arc3-loop1-round7 ...`; the undeclared locus is `SCORECARD.md:1780`.

## Proposed gate patch — not applied

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -273,6 +273,7 @@
 
     ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
+    ("SCORECARD.md", 1759, 1813, "DATED", 1759, r"arc3-loop1-round7"),
 ]
 
 # ---- L1b: frontier-claim register (r10, G21). Frontier bullets carry no
@@ -508,9 +509,8 @@
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
@@ -538,7 +538,10 @@
                 elif c == "__ptr__":
                     pm = PTR.search(text, off)
                     state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
-                    disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
+                    if state == "stale" and cls == "DATED":
+                        disp, why = "historical", "dated scope"
+                    else:
+                        disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
                 elif c is None:
                     if cls == "DATED":
                         disp, why = "historical", "dated scope"
```

The collector now evaluates every full path pointer, including when the same clause already has a pin/version. A stale pointer in DATED scope remains historical; a CURRENT pointer is graded by `ptr_check` regardless of an inline marker. The extra SCORECARD range is required by the checked-out R7 record and is bounded to the bytes measured here; if integration appends a SCORECARD section past line 1813, rederive/re-key it in the landing change rather than widening it without a marker.

## Scratch verification

Scratch root: `/var/tmp/kaidoku-pl1-r8.khwt3i/`. Candidate SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`, 716 lines. `python3 -m py_compile /var/tmp/kaidoku-pl1-r8.khwt3i/candidate/c1-census-v10.py` passed.

For the clean case, only the scratch copy of `PROVINCE.md:18` was re-anchored from `:3546` to the independently measured live `:4126`; the other scoped source copies were unchanged. The candidate run returned:

```text
CLEAN_EXIT=0 VERDICT=PASS
CLEAN_LINE_18_PTR=[{"client": "__ptr__", "disp": "current-ok", "kind": "ptr", "line": 18, "marker": "inline:18", "scope": "CURRENT", "value": "~/.kimi-code/config.toml:4126", "why": "pins 6.7.0"}]
COUNTS={'PROVINCE.md': {'lines': 162, 'loci': 6}, 'SCORECARD.md': {'lines': 1813, 'loci': 10}, 'SKILL.md': {'lines': 413, 'loci': 2}} CURRENT_OK_PER_FILE={'PROVINCE.md': 20, 'SCORECARD.md': 17, 'SKILL.md': 3} G21=14 FRONTIER_ERRORS=[] G2=True JSON_KEYS=19
```

Seeded-fault REPRODUCED: the fault tree differs from clean only by `PROVINCE.md:18` changing `:4126` to `:999999` (confirmed by `diff -ru`). The candidate returned:

```text
FAULT_EXIT=1 VERDICT=FAIL unresolved_blocks=1
FAULT_LINE_18_PTR=[{"client": "__ptr__", "disp": "UNRESOLVED", "kind": "ptr", "line": 18, "marker": "inline:18", "scope": "CURRENT", "value": "~/.kimi-code/config.toml:999999", "why": "line 999999 beyond EOF (4150 lines)"}]
G21=14 frontier_errors=[] G2=True
```

Counter/contract check VERIFIED: baseline and candidate JSON each have 19 keys and identical key sets. `counts` remain identical: PROVINCE `162 lines/6 loci`, SCORECARD `1813/10`, SKILL `413/2`; G21 remains 14 rows with no errors and G2 stays true. `current_ok_per_file` increases from `{PROVINCE.md: 17, SCORECARD.md: 14, SKILL.md: 3}` to `{PROVINCE.md: 20, SCORECARD.md: 17, SKILL.md: 3}` because newly evaluated live pointers (and the now-scoped R7 record) add current-ok detections; this is the expected new measurement, not a dropped counter.

Gate SHA-256 remained `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`; no gate, PROVINCE, SKILL, SCORECARD, corpus, LOG, or other tracked source file was edited. The scratch candidate is evidence only; C2 still must land the PROVINCE re-anchor and receipt.
