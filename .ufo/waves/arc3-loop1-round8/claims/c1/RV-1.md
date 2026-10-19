# RV-1 — C1 `ptr_check` reachability

## Verdicts

- **VERIFIED — live anchor re-derived.** `Grep("rea-agents@", ~/.kimi-code/config.toml)` returned `/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. Direct calls to this gate's `ptr_check()` returned `:4126=ok`, `:3546=stale`, `:999999=unresolved` (state only; no config-line excerpt emitted).
- **VERIFIED — blind spot at HEAD.** `.ufo/gates/c1-census-v10.py:511-514` searches `PTR` only under `if not occ`; `PROVINCE.md:18` has a pin/version and the full pointer, so unmodified `classify()` emits zero pointer detections.
- **REPRODUCED — patch mechanism and clean-anchor pointer grading.** The scratch-only patch below discovers all three current-scope config pointers; the Kimi pointer at `:4126` grades `current-ok`. It leaves the existing JSON keys, locus counts and G21 register intact.
- **REPRODUCED — seeded dead re-key.** Changing only the scratch `PROVINCE.md:18` pointer from `:4126` back to the actually dead `:3546` grades it `STALE` and returns exit 1.
- **DISCREPANCY — full gate PASS requirement.** The unmodified gate already fails at HEAD on an unrelated, out-of-scope `SCORECARD.md:1780` assertion. The patched clean-anchor run retains that same failure, so this seat cannot claim the full clean-tree PASS criterion. Exact locus and output are below.

## First-hand re-derivation

- `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`.
- `sha256sum .ufo/gates/c1-census-v10.py` → `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`; `wc -l` → `713`.
- Current source `PROVINCE.md:18` still names `~/.kimi-code/config.toml:3546`; the declared scope in the gate is `PROVINCE.md:15-26` CURRENT (`.ufo/gates/c1-census-v10.py:255-260`). The `:4126` value was independently re-derived from the live config, not copied from prior seat evidence.
- Baseline command `python3 .ufo/gates/c1-census-v10.py --quiet` returned exit 1:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1813 loci=10
SKILL.md       lines=413  loci=2

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=18; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

  A first-hand JSON read isolated the existing failure: `SCORECARD.md`, block `1776-1783`, with pin `6.4.0` and bare version `6.7.0` at line 1780. `SCORECARD.md:1776-1783` is a round-7 closed coverage record; line 1780 says “per `rea-agents@6.4.0`/`6.7.0` package source”. It lies beyond the gate's final declared SCORECARD scope ending at line 855 (`.ufo/gates/c1-census-v10.py:274-275`). Baseline JSON: `counts={PROVINCE.md:162 lines/6 loci, SCORECARD.md:1813 lines/10 loci, SKILL.md:413 lines/2 loci}`, `undeclared=[SCORECARD.md block 1776-1783]`, `frontier_rows=14`, `frontier_errors=[]`, `g2_ok=true`.

## Gate patch text — NOT applied

This collects pointers in CURRENT scope even when a pin/bare version already exists in the same unit. In units with no other locus, it retains the prior pointer-only collection behavior. Thus co-located DATED pointers remain treated as before; no receipt exception or historical-chain rewrite is introduced.

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -508,8 +508,11 @@
             if any(s <= m.start() < e for s, e in spans):
                 continue
             occ.append(("bare", m.start(), m.group(0)))
-        if not occ:
-            for m in PTR.finditer(text):
+        had_other_locus = bool(occ)
+        for m in PTR.finditer(text):
+            phys = line_of(lines, a, b, m.start())
+            ptr_scope, _, _ = scope_of(fname, phys)
+            if ptr_scope == "CURRENT" or not had_other_locus:
                 occ.append(("ptr", m.start(), m.group(0)))
         if not occ:
             continue
```

## Scratch measurements

All candidate work was isolated under `/var/tmp/kaidoku-r8-rv1.mRAYsY/`; the repository gate and source files were not edited. The clean fixture copied the current scoped files, applied the gate patch above to its gate copy, and simulated the C2 same-commit re-anchor in the scratch `PROVINCE.md:18` only (`:3546` → `:4126`). `python3 -m py_compile /var/tmp/kaidoku-r8-rv1.mRAYsY/clean/.ufo/gates/c1-census-v10.py` passed.

Clean-anchor command: `python3 <scratch-gate> --json --root /var/tmp/kaidoku-r8-rv1.mRAYsY/clean`. Compact result from that run and direct `classify()`:

```json
{"PROVINCE_pointer_detections":[[16,"/home/vgpnk/.config/devin/mcp_config.json:7","current-ok","pins 6.5.0"],[17,"/home/vgpnk/.omp/agent/mcp.json:8","current-ok","pins 6.5.0"],[18,"~/.kimi-code/config.toml:4126","current-ok","pins 6.7.0"]],"baseline_json_keys_equal":true,"candidate_exit":1,"candidate_verdict":"FAIL","counts":{"PROVINCE.md":{"lines":162,"loci":6},"SCORECARD.md":{"lines":1813,"loci":10},"SKILL.md":{"lines":413,"loci":2}},"current_ok_per_file":{"PROVINCE.md":20,"SCORECARD.md":14,"SKILL.md":3},"declared_fail_classes":[],"frontier_errors":[],"frontier_rows":14,"g2_ok":true,"py_compile":"PASS","undeclared":[["SCORECARD.md","1776-1783",[[1780,"pin","6.4.0"],[1780,"bare","6.7.0"]]]]}
```

Seeded-fault fixture copied that candidate and changed only its `PROVINCE.md:18` pointer from `:4126` to the known-dead `:3546`. Command: `python3 <scratch-gate> --json --root /var/tmp/kaidoku-r8-rv1.mRAYsY/fault`.

```json
{"PROVINCE_pointer_detections":[[16,"/home/vgpnk/.config/devin/mcp_config.json:7","current-ok"],[17,"/home/vgpnk/.omp/agent/mcp.json:8","current-ok"],[18,"~/.kimi-code/config.toml:3546","STALE"]],"exit":1,"fault_rekey":"3546","frontier_errors":[],"frontier_rows":14,"g2_ok":true,"stale_ptrs":[["PROVINCE.md",[[16,"/home/vgpnk/.config/devin/mcp_config.json:7","current-ok"],[17,"/home/vgpnk/.omp/agent/mcp.json:8","current-ok"],[18,"~/.kimi-code/config.toml:3546","STALE"]]]],"undeclared":[["SCORECARD.md","1776-1783"]],"verdict":"FAIL"}
```

The pointer behavior and seeded-fault detection reproduce, but both overall candidate runs remain FAIL for the pre-existing SCORECARD locus. G21 remains 14 rows with no errors; `g2_ok=true`; counts/loci remain `6/10/2`; the baseline and candidate JSON key sets compare equal. The gate must not be reported as meeting C1's whole-run PASS criterion until the separate SCORECARD scope/locus discrepancy is resolved without hiding it.
