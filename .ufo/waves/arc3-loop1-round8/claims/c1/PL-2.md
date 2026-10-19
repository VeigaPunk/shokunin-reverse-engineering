# PL-2 — C1 `ptr_check` extension

**Disposition:** blind spot **VERIFIED**; live anchor **VERIFIED**; candidate patch and seeded-fault behavior **REPRODUCED** on the `7deeb36` work snapshot. **DISCREPANCY:** the strict current-HEAD gate cannot satisfy the clean-PASS criterion because the unmodified gate already fails on an unrelated, out-of-scope SCORECARD block. No gate or tracked source file was edited.

## First-hand re-derivation

- `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`; this records work commit `7deeb36`. The gate bytes at both `HEAD` and `7deeb36` independently measure 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` (`sha256sum .ufo/gates/c1-census-v10.py`).
- At `.ufo/gates/c1-census-v10.py:511-514`, `classify()` only collects `PTR` matches inside `if not occ`. Directly re-running `classify()` on current `PROVINCE.md` block 15-26 yielded `line18 assertions=[('pin','6.7.0','current-ok')]` and `pointer detections=[]`. This confirms the pointer is invisible when the same unit already has a pin.
- **Live pin re-derived:** searching `/home/vgpnk/.kimi-code/config.toml` for `rea-agents@` returned `4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`; `wc -l` returned `4150`. Importing the current gate and calling its own `ptr_check()` with `live_pins()` returned:

  ```text
  live_pins= {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  ptr_check(:3546)= ('stale', "line holds no rea-agents pin: 'max_output_size = 64000'")
  ptr_check(:4126)= ('ok', 'pins 6.7.0')
  ```

- `PROVINCE.md:18` currently names `~/.kimi-code/config.toml:3546`; C2 must change that full path pointer to `:4126` in its same-commit patch. This patch does not mark old receipt data current by assertion: it invokes the existing live `ptr_check()` on whatever full path pointer is actually present. Historical bare suffixes such as `:3298`, `:2940`, and `:3227` are not full `PTR` matches.

## Proposed patch text — not applied to the gate

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@
-        if not occ:
-            for m in PTR.finditer(text):
-                occ.append(("ptr", m.start(), m.group(0)))
+        had_other_locus = bool(occ)
+        for m in PTR.finditer(text):
+            phys = line_of(lines, a, b, m.start())
+            ptr_scope, _, _ = scope_of(fname, phys)
+            if ptr_scope == "CURRENT" or not had_other_locus:
+                occ.append(("ptr", m.start(), m.group(0)))
```

This extends collection to pointers in `CURRENT` scope even when a pin/version locus is already present, while retaining the previous pointer-only behavior elsewhere. The existing `__ptr__` dispatch at `.ufo/gates/c1-census-v10.py:538-541` remains the evaluator. Mixed `DATED` units that already have another locus are not newly reclassified as live pointers.

## Scratch measurements

All candidate edits and runs were confined to `/var/tmp/kaidoku-pl2-r8.__7ucjs2/`; the candidate gate SHA-256 was `e2d98c4e2ee1eb875a455c15d8251f6b0b50643920f3ce0b03bba5637e74f235`. On a scratch copy of the four gate-input files from `7deeb36`, I applied the patch and simulated C2 by changing only the full `PROVINCE.md:18` pointer from `:3546` to the independently measured live `:4126`.

- **Clean live-anchor candidate — REPRODUCED:** `python3 <scratch-gate> --root <scratch-root>` exited 0 / PASS. Its emitted detections included:

  ```text
  :16 [ptr] __ptr__=/home/vgpnk/.config/devin/mcp_config.json:7 -> current-ok (pins 6.5.0)
  :17 [ptr] __ptr__=/home/vgpnk/.omp/agent/mcp.json:8 -> current-ok (pins 6.5.0)
  :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
  FRONTIER register (G21): 14 rows asserted, errors: []
  G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
  VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
  ```

- **Seeded dead-pointer candidate — REPRODUCED:** from a separate copy, changed only the full path pointer `:4126` to `:999999`. It exited 1 / FAIL and emitted `:18 [ptr] __ptr__=~/.kimi-code/config.toml:999999 -> UNRESOLVED (line 999999 beyond EOF (4150 lines))`; G21 remained 14 rows / no errors and G2 remained true. `current_ok_per_file` changed only from PROVINCE 20 to 19 because this one pointer ceased to be current-ok.
- **Counters / historical chain — REPRODUCED:** on the clean `7deeb36` snapshot, baseline versus patched JSON both had 19 keys; `counts` stayed PROVINCE 162 lines / 6 loci, SCORECARD 1757 / 9, SKILL 413 / 2. G21 stayed 14 rows / no errors. The expected `current_ok_per_file` change was PROVINCE 17→20 from the three newly reachable valid pointers; SCORECARD 14 and SKILL 3 were unchanged. The five `historical` block signatures were identical before and after (`HISTORICAL_CHAIN_UNCHANGED=True`, signature SHA-256 `8b8defcf6451de913039702c814dcad18e51a70c3205a651d6131664ceee056d`).

## Current-HEAD acceptance discrepancy

I re-ran the unmodified gate on the actual current tree before candidate testing: `python3 .ufo/gates/c1-census-v10.py --json` exited 1 / FAIL. It reports `SCORECARD.md` 1813 lines / 10 loci and an `UNDECLARED` block `1776-1783`: line 1780 has pin `6.4.0` and bare `6.7.0`, both ambiguous because the block is beyond the gate's declared SCORECARD scope (currently ends at line 855; `.ufo/gates/c1-census-v10.py:274-276`). Baseline still had G21 14 / no errors, G2 true, and the 19-key JSON shape.

The patched candidate against a scratch copy of current `HEAD`, with `PROVINCE.md:18` simulated at live `:4126`, did evaluate that pointer as `current-ok`, but the overall gate still exited 1 / FAIL on the same `SCORECARD.md:1776-1783` UNDECLARED block. This is **not** a C1 patch failure or a seeded-pointer failure; it is a pre-existing current-HEAD acceptance blocker. Therefore the targeted extension/fault behavior is reproduced, but the frozen requirement “PASS on current tree” is **not established** for `HEAD=904b724` unless the scope discrepancy is independently resolved. I did not widen or otherwise change gate scope in this seat.
