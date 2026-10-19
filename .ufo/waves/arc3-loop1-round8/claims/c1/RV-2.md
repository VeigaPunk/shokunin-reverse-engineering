# RV-2 — C1 `ptr_check` extension

## Verdicts

- **VERIFIED — assignment and source identity.** The frozen roster puts RV-2 in C1 (`claims-frozen.md:15-35,68-69`). First-hand `git rev-parse HEAD` returned `904b724258fc9396a016bd9952b5cd40225fb7d8`. The gate is 713 lines; `sha256sum .ufo/gates/c1-census-v10.py` returned `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`.
- **VERIFIED — live target.** `grep -n 'rea-agents@' /home/vgpnk/.kimi-code/config.toml` returned `4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`; `wc -l` returned `4150`. Fresh direct calls to the gate's `ptr_check()` with live pins returned `:4126 -> ('ok', 'pins 6.7.0')` and `:3546 -> state=stale (line holds no rea-agents pin)`. UTF-8 bytes of the line content without its line ending hash to `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1`.
- **VERIFIED — blind spot.** At `.ufo/gates/c1-census-v10.py:511-514`, PTR loci are collected only under `if not occ`; the PROVINCE clause already contains pin/version occurrences, so direct `classify('PROVINCE.md', ...)` on this tree returned no pointer assertions. The existing assertion dispatch is at `:538-541` and can call `ptr_check` once the pointer is collected.
- **CORRECTED — actual baseline is not PASS.** A fresh `python3 .ufo/gates/c1-census-v10.py --json` run exited 1 / `FAIL`: SCORECARD block `1776-1783` is `UNDECLARED`, with `6.4.0` and `6.7.0` at line 1780. The bounded gate scope currently ends at SCORECARD line 855 (`.ufo/gates/c1-census-v10.py:274-275`). The same baseline had stale=0, ambiguous=0, unresolved=0, scope_errors=[], unreadable=[], G2=true, G21=14 rows/errors=[], and G11=[]. A pointer-only patch still fails on this independent existing locus. The proposed patch therefore also declares that exact dated round-7 record, with its own marker line inside the range.
- **REPRODUCED — proposed patch passes on the re-anchored scratch tree.** It reads `PROVINCE.md:18`'s `~/.kimi-code/config.toml:4126` as `current-ok (pins 6.7.0)` and exits 0 / PASS.
- **REPRODUCED — seeded dead re-key fails.** Replacing only the scratch pointer `:4126` with `:999999` exits 1 / FAIL; the pointer at `PROVINCE.md:18` is `UNRESOLVED (line 999999 beyond EOF (4150 lines))`.
- **UNVERIFIABLE — actual landing.** Per the frozen write boundary, this seat only supplies patch text and scratch measurements; neither the gate nor PROVINCE nor a receipt was edited or committed here.

## First-hand measurements

Commands and results from this worktree:

```text
$ git rev-parse HEAD
904b724258fc9396a016bd9952b5cd40225fb7d8
$ sha256sum .ufo/gates/c1-census-v10.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  .ufo/gates/c1-census-v10.py
$ wc -l .ufo/gates/c1-census-v10.py
713 .ufo/gates/c1-census-v10.py
$ grep -n 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ wc -l /home/vgpnk/.kimi-code/config.toml
4150 /home/vgpnk/.kimi-code/config.toml
```

A direct `classify()` call on current `PROVINCE.md` returned `pointers=0 detections=[]`. The baseline gate JSON command exited 1. Measured counters: `counts={'PROVINCE.md': {'lines': 162, 'loci': 6}, 'SCORECARD.md': {'lines': 1813, 'loci': 10}, 'SKILL.md': {'lines': 413, 'loci': 2}}`; `current_ok_per_file={'PROVINCE.md': 17, 'SCORECARD.md': 14, 'SKILL.md': 3}`; the sole undeclared block is `SCORECARD.md:1776-1783` (assertions `6.4.0` and `6.7.0` on line 1780). This is a measured correction to the expected clean baseline, not a pointer result.

## Proposed gate patch text — not applied

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@
     ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
+    ("SCORECARD.md", 1776, 1783, "DATED", 1777, r"2026-10-19-arc3-r7"),
 ]
@@
-        if not occ:
-            for m in PTR.finditer(text):
+        had_other_locus = bool(occ)
+        for m in PTR.finditer(text):
+            phys = line_of(lines, a, b, m.start())
+            ptr_scope, _, _ = scope_of(fname, phys)
+            if ptr_scope == "CURRENT" or not had_other_locus:
                 occ.append(("ptr", m.start(), m.group(0)))
         if not occ:
```

The PTR change evaluates pointers in CURRENT scope even when the same clause already contains a pin/version. It preserves the old pointer-only path, and continues to omit PTRs from DATED clauses that already contain other loci, retaining their historical treatment. The added SCORECARD row is required only because this measured HEAD already fails on that out-of-bound round-7 record; its marker `2026-10-19-arc3-r7` is on line 1777 and within the declared 1776-1783 range. G21 and existing counters/schema are not removed or renamed.

## Scratch verification

Scratch root: `/var/tmp/kaidoku-rv2-arc3-r8-rytct4hf` (not `/tmp`). Candidate gate SHA-256: `1cc82e78c91700966b9ffb68239a8c878359521121ad24dafa733f49278a0d83` (717 lines). The clean scratch source copied the current scoped files and changed only the `PROVINCE.md:18` Kimi pointer from `:3546` to the independently measured live `:4126`; gate code was the patch above. It still reads the real live config and live client anchors. The seeded tree changed only that pointer from `:4126` to `:999999`.

```text
$ python3 /var/tmp/kaidoku-rv2-arc3-r8-rytct4hf/c1-census-v10.py --root /var/tmp/kaidoku-rv2-arc3-r8-rytct4hf/clean-tree
        :16 [ptr] __ptr__=/home/vgpnk/.config/devin/mcp_config.json:7 -> current-ok (pins 6.5.0)
        :17 [ptr] __ptr__=/home/vgpnk/.omp/agent/mcp.json:8 -> current-ok (pins 6.5.0)
        :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=15, SKILL.md=3; total loci=18; floor=1/file)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit=0

$ python3 /var/tmp/kaidoku-rv2-arc3-r8-rytct4hf/c1-census-v10.py --root /var/tmp/kaidoku-rv2-arc3-r8-rytct4hf/seeded-dead-pointer
-- UNRESOLVED (1) --
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:999999 -> UNRESOLVED (line 999999 beyond EOF (4150 lines))
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=19, SCORECARD.md=15, SKILL.md=3; total loci=18; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=1)
exit=1
```

Across baseline and clean candidate, the three `counts` entries are byte-for-byte equal (`PROVINCE 162 lines/6 loci; SCORECARD 1813/10; SKILL 413/2`), the JSON key set is unchanged (19 keys), and G21 remains 14 rows with no errors. The expected current-ok detections increase from 17/14/3 to 20/15/3: three current pointers in PROVINCE become reachable, and the separately declared round-7 record contributes its already-live 6.7.0 assertion. The clean candidate without the extra dated scope row remains FAIL solely on the measured SCORECARD undeclared block.
