# EX-2 — C1 `ptr_check` extension on the live anchor

**Disposition:** The pointer blind spot is **VERIFIED** and the proposed gate patch plus seeded-fault catch are **REPRODUCED** on scratch. The raw checkout is not yet clean: `PROVINCE.md:18` still points to `:3546`, so the clean result below is the same-commit landing fixture with the planned C2 `:4126` re-anchor applied to its scratch copy. The gate also needs a scope re-key for the appended R7 SCORECARD record; without it, the unmodified gate already fails before this C1 fix.

## First-hand re-derivation

- `git rev-parse HEAD` → `904b724258fc9396a016bd9952b5cd40225fb7d8`. `.ufo/gates/c1-census-v10.py` → 713 lines, SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` (`sha256sum`, `wc -l`).
- Safely filtered `~/.kimi-code/config.toml` for only the `rea-agents@` line: file has 4,150 lines; the unique match is `4126: args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. `live_pins()` independently returned `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}`. The exact 42-byte line content excluding its line terminator hashes to `eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1` (including the LF, `eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675`). `ptr_check("~/.kimi-code/config.toml", 4126, live)` → `('ok', 'pins 6.7.0')`.
- Current `PROVINCE.md:18` still contains `~/.kimi-code/config.toml:3546`; parsing that line with the gate's `PTR` finds `[('~/.kimi-code/config.toml', 3546)]`, but baseline `classify()` returns no `ptr` assertion for its `15-26` block. Direct `ptr_check(..., 3546, live)` returns state `stale`. The cause is `.ufo/gates/c1-census-v10.py:511-514`: pointer collection is nested under `if not occ`, after the pin/version matches have already populated `occ`.
- The unmodified gate also fails on the current checkout for an independent, measurable records-bound issue. Command `python3 .ufo/gates/c1-census-v10.py --json --root .` → exit 1 / `FAIL`; counts are PROVINCE `162/6`, SCORECARD `1813/10`, SKILL `413/2`; undeclared is `SCORECARD.md` block `1776-1783`, with line `1780` values `6.4.0` and `6.7.0`. G21 is `(14, [])`, G2 is true. The current R7 record spans `SCORECARD.md:1759-1813`; `.ufo/gates/c1-census-v10.py:41-45` says appended records beyond the declared bound must be locus-free or re-keyed as a DATED range with its own marker.

## Patch text — scratch only; not applied to the gate

This takes the RV-2 current-scope filter approach: gather pointers in CURRENT scope even when a pin/version was already found, while preserving the prior behavior for pointer-only units. A DATED unit that already has its own pin/version locus does not newly turn its historic receipt chain into a live pointer assertion. The added SCOPE row re-keys the existing R7 SCORECARD record as DATED under the gate's stated records-commit rule; it changes no G21 rows.

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@ -273,6 +273,7 @@
 
     ("SCORECARD.md", 703, 768, "DATED", 704, r"arc2-loop1-round2"),
     ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),
+    ("SCORECARD.md", 1759, 1813, "DATED", 1759, r"arc3-loop1-round7"),
 ]
 
 # ---- L1b: frontier-claim register (r10, G21). Frontier bullets carry no
@@ -508,8 +509,11 @@
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

## Scratch verification

Scratch root: `/var/tmp/kaidoku-ex2-arc3-r8.fWv5Xa/`. The copied gate alone was patched; the copied `PROVINCE.md:18` was changed from `:3546` to the freshly measured live `:4126` for the same-commit C2 landing fixture. `SCORECARD.md` and `SKILL.md` were copies of the current tree. The fault tree derives from that clean tree and changes only the pointer `:4126` to `:999999`. No repository source or gate was edited. Candidate gate identity: 717 lines, SHA-256 `a4bc309534283ed6edecaad2d84d4e4ea69c95f2c0d5538bf2cffa97d2d70ece`.

- `python3 -m py_compile gate/c1-census-v10.py` → PASS.
- Candidate `python3 gate/c1-census-v10.py --root tree --json` → exit 0 / PASS. Direct `classify()` on the candidate and clean copied documents reported:

```text
PROVINCE patched pointer block=15-26 disp=info ptrs=[
  (16, '/home/vgpnk/.config/devin/mcp_config.json:7', 'current-ok', 'pins 6.5.0'),
  (17, '/home/vgpnk/.omp/agent/mcp.json:8', 'current-ok', 'pins 6.5.0'),
  (18, '~/.kimi-code/config.toml:4126', 'current-ok', 'pins 6.7.0')]
```

The rest of the candidate JSON summary was `counts={'PROVINCE.md': {'lines': 162, 'loci': 6}, 'SCORECARD.md': {'lines': 1813, 'loci': 10}, 'SKILL.md': {'lines': 413, 'loci': 2}}`; `stale=0`, `ambiguous=0`, `undeclared=0`, `unresolved=0`, `scope_errors=[]`, `unreadable=[]`, `g11=[]`; G21 `(14, [])`; G2 `true`, floor `1/readable-file`; `current_ok_per_file={'PROVINCE.md': 20, 'SCORECARD.md': 15, 'SKILL.md': 3}`.
- The DATED history remains distinguished: candidate `classify()` on SCORECARD block `288-295` leaves the `6.4.0` assertion at line 291 as `historical` / `dated scope`; the receipt-stamped suffixes on the copied PROVINCE line (`:3298`, `:2940`, `:3227`) were left unchanged.
- Compared the unmodified and candidate instruments against the same clean scratch root: both JSON objects have 19 keys (`json_keysets_equal=True`); both report G21 `(14, [])` (`g21_value_equal=True`). Baseline returns FAIL for the undeclared R7 record; candidate returns PASS. The G21 register and JSON contract are preserved.
- Seeded-fault command `python3 gate/c1-census-v10.py --root fault --json` → exit 1 / FAIL. The new pointer assertion is `PROVINCE.md:18`, value `~/.kimi-code/config.toml:999999`, disposition `UNRESOLVED`, reason `line 999999 beyond EOF (4150 lines)`. G21 remains `(14, [])`; G2 remains true.

## Item verdicts

- **VERIFIED — live anchor:** line 4126 contains the live 6.7.0 pin; the measured content hash and direct `ptr_check()` result are above.
- **DISCREPANCY — raw source pointer:** checked-out `PROVINCE.md:18` remains `:3546` and resolves stale. The clean PASS requires C2's `:4126` edit in the same landing commit; this seat did not edit PROVINCE.
- **VERIFIED — blind spot:** the HEAD collector skips the current pin-carrying pointer; the baseline direct classification returned zero pointer assertions.
- **REPRODUCED — patch and clean landing fixture:** after the candidate gate patch plus scratch-only C2 re-anchor and SCORECARD DATED re-key, the live Kimi pointer is explicitly `current-ok` and the instrument returns PASS.
- **REPRODUCED — seeded fault:** a dead re-key is detected as UNRESOLVED and makes the candidate fail.
- **VERIFIED — counters/history:** 19 JSON keys unchanged, G21 still 14 rows / no errors, G2 floor still true; the pre-existing DATED `6.4.0` record remains historical.
- **UNVERIFIABLE here — authenticity of older custody receipts:** they were not re-read or re-adjudicated. This patch does not use them to exempt the new live `:4126` pointer.

No files outside this artifact were modified in the repository. The actual gate remains unpatched; integration must land this patch with C2's PROVINCE re-anchor and preserve/re-key the R7 SCORECARD range as shown.