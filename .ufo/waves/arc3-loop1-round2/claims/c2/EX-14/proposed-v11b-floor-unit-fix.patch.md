# Patch text (NOT applied) — drop-in fix for the landed per-file floor unit bug

Seat EX-14 (executor, chain c2), arc3-loop1-round2, 2026-10-19. **Blocking
finding for the round's C2 claim.** EX-16 owns the target; this seat wrote
nothing in `.ufo/gates/`.

## Measured defect on the landed bytes

Target as landed at 2026-10-19 09:10:56,
`.ufo/gates/c1-census-v10.py` sha256
`c95a5cf30201a1f862849b04701330e65b3777c877fb9467e4ee38656bbb0d4f`
(the revision that turns the floor into a per-file one; it cites EX-14's map
in its docstring). End-to-end on those bytes (`v11b-matrix.out`,
`receipts-v11b-*.out`):

```
$ python3 census-live-v11b.py --root <repo HEAD>          # ordinary run
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; total loci=17; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)    exit=1
```

A clean HEAD now FAILs. The frozen C2 claim requires the opposite: *"ordinary
runs at HEAD stay PASS 0/0/0/0"*. Root cause: the floor counts **blocks whose
disposition is current-ok** (`for rec in out.get("current-ok", [])`), and
SKILL.md has no such block — its block 10-16 is historical only and its block
18-20 is mixed (3 current-ok + 1 historical) so the block-level disposition is
`info`. Per file the two units differ exactly here (blocks 1 / 4 / **0** vs
assertions 17 / 14 / **3**; `live-floor-units.txt`).

## Fix (verified drop-in)

Scratch variant `/var/tmp/ex14/census-live-v11c-fix.py`, sha256
`bed3b02ee6fff764091efb0648e48c2e3dda1f80157dd8c235018b44764d0a87`
(compiles; matrix below). Diff against the landed bytes:

```diff
@@ .ufo/gates/c1-census-v10.py:533-536
     n_current_ok = len(out.get("current-ok", []))
     floor = {f: 0 for f in files}
-    for rec in out.get("current-ok", []):
-        floor[rec["file"]] += 1
+    # `out` is keyed by BLOCK disposition and SKILL.md has no current-ok block
+    # (block 18-20 is mixed -> disp info), so counting floors from
+    # out["current-ok"] alone reads SKILL.md=0 and false-FAILs a clean HEAD.
+    # Sweep every disposition and count ASSERTIONS (dets).  g11/g7 hold
+    # strings, not records, so they must be skipped.
+    for _disp, _recs in out.items():
+        if _disp in ("g11", "g7"):
+            continue
+        for rec in _recs:
+            for d in rec["asserts"]:
+                if d["disp"] == "current-ok":
+                    floor[rec["file"]] += 1
```

(The report line already prints the per-file numbers; with the fix it reads
`PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3`. No other change is needed.)

## Verified effect (end-to-end `main()`, same four environments)

| environment | landed v11b | with this fix |
|-------------|-------------|---------------|
| head | **FAIL exit 1** `SUSPECT`, `['BLIND-INSTRUMENT']` | **PASS exit 0**, per-file 17/14/3, classes `[]` |
| `atk-missing` (SKILL.md absent) | FAIL `['UNREADABLE']` | FAIL `['UNREADABLE']` (SKILL exempt as unreadable) |
| `atk-nullskill` (present, needle-free SKILL.md) | FAIL `['BLIND-INSTRUMENT']` (right verdict, wrong-ish label) | FAIL `['BLIND-INSTRUMENT']` — verdict correct; a distinct `EMPTY-SCOPE` label is the optional nicety in `proposed-h3-floor-scoping.patch.md` |
| `atk-shrunk` | FAIL (stale) | FAIL (stale), classes `[]` after the fix (no spurious class) |

Receipts: `v11c-matrix.out`, `receipts-v11c-*.out`.

## Why this must land before the round's commit

1. The C2 claim's own acceptance clause ("ordinary runs at HEAD stay PASS
   0/0/0/0") is false on the landed bytes. Any landing receipt captured from
   the current file will show exit 1 at HEAD.
2. The claimed H3 behaviour is otherwise right: the per-file floor is the
   variant this seat measured to dominate the global one (map §5,
   `floor-probe.out`), and the fix keeps that behaviour while restoring the
   clean-HEAD property.
3. Same trap, second occurrence: this seat's own first draft of the per-file
   floor failed the identical way (map §11; `proposed-h3-floor-scoping.patch.md`
   "Trap 1"). The unit is the whole bug — no aggregation change is needed.
