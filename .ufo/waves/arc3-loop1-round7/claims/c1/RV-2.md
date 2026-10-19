# RV-2 — C1 ptr-check blind spot

## Verdicts

- **VERIFIED — blind spot at HEAD.** `.ufo/gates/c1-census-v10.py:511-514` only appends `PTR` matches when `occ` is empty. The pin/bare-version detections already present in the same unit make the pointer branch unreachable. Direct `classify()` against the current `PROVINCE.md` reported `pointers=0 detections=[]`; the unmodified gate itself still returned PASS.
- **DISCREPANCY — frozen pointer locator.** Current `PROVINCE.md:18` has the full path `~/.kimi-code/config.toml:3546` dated “2026-10-19 re-read”; `:3298` is identified in that same line as the 17:55:49Z receipt pointer and historical. The current gate's `PTR` regex sees `:3546`, not the abbreviated historical `:3298`.
- **REPRODUCED — patch text.** On a scratch copy, the proposed instrument reports the receipt-anchored pointer current-by-design and retains PASS. Re-keying that pointer to the dead line `:999999` on a separate scratch tree yields UNRESOLVED and FAIL.
- **VERIFIED — existing output surface.** Candidate and HEAD JSON key sets are identical (19 keys); G21 remains 14 rows / no errors. `current_ok_per_file` changes only as expected from the three newly detected current pointers: PROVINCE 17→20; SCORECARD 14 and SKILL 3 remain unchanged. No gate or tracked source was edited.

## First-hand measurements

At HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`:

```text
$ sha256sum .ufo/gates/c1-census-v10.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  .ufo/gates/c1-census-v10.py
$ wc -l .ufo/gates/c1-census-v10.py
713 .ufo/gates/c1-census-v10.py
```

The unmodified `python3 .ufo/gates/c1-census-v10.py` returned:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1757 loci=9
SKILL.md       lines=413  loci=2
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Direct call to the current instrument's `ptr_check()` (the printed detail is deliberately redacted; it can include a line excerpt):

```text
ptr_check("~/.kimi-code/config.toml", 3298, live kimi=6.7.0) -> state=stale; line holds no pin; source excerpt suppressed
ptr_check("~/.kimi-code/config.toml", 3546, live kimi=6.7.0) -> state=stale; line holds no pin; source excerpt suppressed
classify(PROVINCE.md): pointers=0 detections=[]
```

## Proposed patch text (not applied)

```diff
--- a/.ufo/gates/c1-census-v10.py
+++ b/.ufo/gates/c1-census-v10.py
@@
 PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
+PTR_RECEIPTS = {
+    ("PROVINCE.md", 18, "~/.kimi-code/config.toml", 3546):
+        ("2026-10-19 re-read", "kimi", "6.7.0"),
+}
 CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
@@
     return "ok", "pins %s" % m.group(1)
 
 
+def ptr_receipt_check(fname, source_line, ptr_path, ptr_line, text, live):
+    record = PTR_RECEIPTS.get((fname, source_line, ptr_path, ptr_line))
+    if record:
+        stamp, client, captured = record
+        carries_pin = any(m.group(1) == captured for m in PIN.finditer(text))
+        if stamp in text and carries_pin and live.get(client) == captured:
+            return "ok", "receipt %s pin %s matches live %s" % (stamp, captured, client)
+    return ptr_check(ptr_path, ptr_line, live)
+
+
 def cache_check(h, stated):
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
@@
                 elif c == "__ptr__":
                     pm = PTR.search(text, off)
-                    state, why = ptr_check(pm.group(1), int(pm.group(2)), live)
+                    state, why = ptr_receipt_check(
+                        fname, phys, pm.group(1), int(pm.group(2)), text, live)
                     disp = {"ok": "current-ok", "stale": "STALE", "unresolved": "UNRESOLVED"}[state]
```

The receipt table binds the exact source locus, target path/line, capture stamp, client and captured pin. It treats that record as current only while the unit still carries the capture stamp and pin and the freshly derived live client anchor still agrees. Other current pointers run through `ptr_check`; the `not had_other_locus` condition retains the old pointer-only path and avoids newly treating already-pinned DATED receipt rows as live pointers.

## Scratch verification

Scratch root: `/var/tmp/kaidoku-rv2-arc3-r7.o_aelzy4`; `clean-tree/` and `seeded-dead-pointer-final/` each contain copies of the three scoped source files. Final candidate SHA-256: `1e7ee0d9b7c89074de9eef37c0da4f8684848f59450219192b329e81c6822f8c`.

Clean candidate run: `python3 <candidate> --root <clean-tree>`:

```text
:16 [ptr] __ptr__=/home/vgpnk/.config/devin/mcp_config.json:7 -> current-ok (pins 6.5.0)
:17 [ptr] __ptr__=/home/vgpnk/.omp/agent/mcp.json:8 -> current-ok (pins 6.5.0)
:18 [ptr] __ptr__=~/.kimi-code/config.toml:3546 -> current-ok (receipt 2026-10-19 re-read pin 6.7.0 matches live kimi)
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

Seeded fault: copied the scratch tree and changed only `PROVINCE.md`'s `config.toml:3546` to `config.toml:999999`. `python3 <candidate> --root <seeded-dead-pointer> --json` produced:

```text
exit=1 verdict=FAIL
PROVINCE.md block 15-26, pointer line 18: UNRESOLVED (line 999999 beyond EOF (4150 lines))
G21=14 rows, frontier_errors=[]; G2=true
unresolved block=[('PROVINCE.md', '15-26', 'UNRESOLVED')]
```

The candidate's JSON keys were the same as the unmodified gate's: `ambiguous, counts, current_ok, current_ok_per_file, declared_fail_classes, frontier_errors, frontier_rows, g11, g2_floor, g2_ok, g7, historical, live, scope_errors, stale, undeclared, unreadable, unresolved, verdict` (`JSON_KEYS_PRESERVED=True`). The clean candidate returned exit 0 / PASS; the seeded run returned exit 1 / FAIL. Scratch-only execution; `.ufo/gates/c1-census-v10.py`, `PROVINCE.md`, `SKILL.md`, and `SCORECARD.md` remained unchanged.
