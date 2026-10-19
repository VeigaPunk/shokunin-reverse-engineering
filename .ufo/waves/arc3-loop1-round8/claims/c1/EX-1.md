# EX-1 — C1 `ptr_check` reachability

**Disposition:** blind spot **VERIFIED**; frozen live-line correction **VERIFIED**; HEAD baseline **DISCREPANCY** (independent undeclared R7 tail); candidate patch and seeded-fault checks **REPRODUCED** on scratch. No gate or tracked source was changed.

## First-hand re-derivation

- **VERIFIED — source identity and blind spot.** `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`; `sha256sum .ufo/gates/c1-census-v10.py` → `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`; `wc -l` → `713`. At `.ufo/gates/c1-census-v10.py:504-514`, `classify()` accumulates pin/bare-version occurrences, then scans `PTR` only inside `if not occ`. `PROVINCE.md:18` contains both a Kimi version pin and a full path pointer. Direct import/call on current `PROVINCE.md` returned `unmodified classify PROVINCE ptr assertions: 0`.
- **VERIFIED — live anchor.** Narrow read of `~/.kimi-code/config.toml` found 4,150 lines and one `rea-agents@` match:

  ```text
  live_pin_line: count=4150 matches=[(4126, 'args = [ "-y", "rea-agents@6.7.0", "mcp" ]')] sha256_without_newline=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
  sha256_including_LF=eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
  ```

  Direct call using the live anchor dictionary: `ptr_check("~/.kimi-code/config.toml", 4126, live)` → `('ok', 'pins 6.7.0')`; line `3546` → `stale`. Thus the current `PROVINCE.md:18` `:3546` token is **CORRECTED** to `:4126` for the C1 scratch test; C2 must make that same-line source edit and land its independently written content-hash receipt.
- **VERIFIED — source scope and historical behavior.** Gate SCOPE has `PROVINCE.md:15-26` as `CURRENT` (`.ufo/gates/c1-census-v10.py:255-257`); the pointer cannot be excused by the word “historical” later on the same physical line. Its existing inline-marker exception did excuse an in-range stale pointer in a first scratch variant, so the pointer branch below applies historical fallback to `DATED` scope only. A separately checked dated pointer remains historical after the final patch: copied `SCORECARD.md:291`, `~/.kimi-code/config.toml:1478` → `historical`.
- **DISCREPANCY — current HEAD versus the work commit.** Current HEAD's `SCORECARD.md` is 1,813 lines, versus 1,757 at `7deeb36` (full commit `7deeb36045209f3fbeb4460edd7aef5b5270af22`). HEAD has the R7 section at `SCORECARD.md:1759-1813`, but gate SCOPE ends at `:855` (`.ufo/gates/c1-census-v10.py:264-275`). The unmodified current-HEAD scratch gate therefore exits FAIL on undeclared `SCORECARD.md` locus `1776-1783`. A bounded DATED row for this already-present R7 section is included in the proposed patch; it does not widen the old `:769-855` bound.

## Proposed gate patch — text only, not applied

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

The first hunk is required for this actual HEAD to satisfy the PASS condition: the R7 section is already in HEAD but outside declared SCOPE. The second makes full path pointers reachable even when their clause already has pins/versions. The third retains stale pointers in `DATED` historical text as historical while a stale pointer in `CURRENT` scope (including `PROVINCE.md:18`) remains a failure. `ptr_check()` still evaluates the live target; no receipt is faked or hard-coded in this C1 patch. The C2 line-content receipt remains a same-commit integration dependency.

## Scratch verification

All files below are copies under `/var/tmp/kaidoku-c1-ex1-r8-verified-m8h3wdsq/`; the candidate gate contains exactly the diff above. The clean copy changes only its `PROVINCE.md:18` pointer from `:3546` to the freshly measured `:4126`.

- `python3 -m py_compile /var/tmp/kaidoku-c1-ex1-r8-verified-m8h3wdsq/candidate-clean/c1-census-v10.py` passed.
- Baseline command, current HEAD copies, exit 1:

  ```text
  baseline current HEAD: exit=1 verdict=FAIL counts={"PROVINCE.md": {"lines": 162, "loci": 6}, "SCORECARD.md": {"lines": 1813, "loci": 10}, "SKILL.md": {"lines": 413, "loci": 2}} undeclared=[('SCORECARD.md', '1776-1783')] G21=14 frontier_errors=[]
  ```

- Candidate clean command, exit 0:

  ```text
  candidate clean: exit=0 verdict=PASS counts={"PROVINCE.md": {"lines": 162, "loci": 6}, "SCORECARD.md": {"lines": 1813, "loci": 10}, "SKILL.md": {"lines": 413, "loci": 2}} floor={"PROVINCE.md": 20, "SCORECARD.md": 17, "SKILL.md": 3} G21=14 frontier_errors=[] keys_preserved=True
  PROVINCE.md pointer_assertions=[(16, '/home/vgpnk/.config/devin/mcp_config.json:7', 'current-ok', 'pins 6.5.0'), (17, '/home/vgpnk/.omp/agent/mcp.json:8', 'current-ok', 'pins 6.5.0'), (18, '~/.kimi-code/config.toml:4126', 'current-ok', 'pins 6.7.0')]
  SCORECARD.md pointer_assertions=[(288, '~/.config/devin/mcp_config.json:7', 'current-ok', 'DATED'), (289, '~/.omp/agent/mcp.json:8', 'current-ok', 'DATED'), (291, '~/.kimi-code/config.toml:1478', 'historical', 'DATED')]
  clean_gate: exit=0 verdict=PASS stale=0 ambiguous=0 undeclared=0 unresolved=0 scope_errors=0 unreadable=0 g11=0 g2_ok=True declared_fail_classes=[]
  ```

  The JSON top-level contract is 19 keys before and after, identical names. Counts/loci and G21 output remain present; G21 is still 14 rows with no frontier errors. `current_ok_per_file` is PROVINCE=20, SCORECARD=17, SKILL=3 after the previously unreachable pointer assertions are counted.
- Seeded in-range dead re-key `:4126` → `:3546`, exit 1:

  ```text
  dead in-range re-key :3546: exit=1 verdict=FAIL G21=14 frontier_errors=0 PROVINCE_ptr_faults=[['stale', 18, '~/.kimi-code/config.toml:3546', 'STALE', 'line-has-no-pin']]
  ```

  The measurement reports only the safe failure class; `ptr_check`'s source excerpt is not emitted. An additional out-of-range re-key to `:999999` also exited 1 with `UNRESOLVED` / `beyond-EOF` (4,150 lines).

**Residual / integration boundary:** no gate edit or C2 receipt was made here. The tested clean tree assumes C2 updates `PROVINCE.md:18` to `:4126`; the final combined commit must include C2's line-content receipt. The exact line-content hash above excludes the LF; the LF-inclusive hash is also recorded to make the byte convention explicit. C1 patch remains a proposal pending chain integration.