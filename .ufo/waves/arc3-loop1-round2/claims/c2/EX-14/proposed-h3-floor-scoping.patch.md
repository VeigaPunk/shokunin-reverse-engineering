# Patch text (NOT applied) — optional per-file strengthening of the landed H3 floor

Seat EX-14 (executor, chain c2), arc3-loop1-round2, 2026-10-19. This seat is
**not** the implementer; EX-16 owns `.ufo/gates/c1-census-v10.py`. Offered as a
measured, optional strengthening of the **landed** v11 floor.

Target bytes (landed): `.ufo/gates/c1-census-v10.py`
sha256 `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`.

## What the landed floor does and does not do (measured)

Landed: `g2_ok = n_current_ok > 0` where `n_current_ok = len(out["current-ok"])`
— the count of **blocks whose disposition is current-ok**, tree-wide. Measured
on the landed bytes:

- `head` — PASS exit 0, `G2 … ok (current-ok loci=5, total loci=17, floor=1)`;
- `atk-blind-all` (PIN/VER/PTR neutered) — FAIL exit 1, `['BLIND-INSTRUMENT']`;
- `atk-missing` (SKILL.md absent) — FAIL exit 1, `['UNREADABLE']` (H1 landed);
- `atk-nullskill` (SKILL.md present, 371 lines, rows 10-20 stripped of every
  version/pin/pointer needle) — **PASS exit 0, `declared=[]`,
  `current-ok loci=5, total loci=15`, `SKILL.md loci=0`**.

So one scoped file can collapse to zero loci on an ordinary-looking run and the
run still passes: the frozen C2 wording "FAILs when its positive-floor
assertion finds zero loci in a **non-empty scope**" is met only in the
tree-level reading. Receipts: `live-matrix.out`, `receipts-live-atk-nullskill.out`,
`live-floor-units.txt`.

## Why the obvious fix is wrong (unit trap, measured)

Making the *landed* predicate per-file in its own unit false-FAILs at HEAD:

| file | current-ok blocks (landed unit) | current-ok dets |
|------|--------------------------------:|----------------:|
| PROVINCE.md | 1 | 17 |
| SCORECARD.md | 4 | 14 |
| SKILL.md | **0** | **3** |

SKILL.md carries no current-ok-dispositioned block (block 10-16 is historical
only; block 18-20 is mixed -> disp `info`). Any per-file floor must therefore
aggregate **dets**, not blocks.

## Proposed diff (context = landed bytes; APPLIED ONLY TO A SCRATCH COPY AND VERIFIED)

Verified variant: `/var/tmp/ex14/census-live-v11-ex14-pff.py`, sha256
`dc09239170d7d6551ad6118003fed7518222c55dde2bd16cc36a61b558bee4f7`
(compiles; matrix below). Still **not** applied to the repo.

```diff
@@ .ufo/gates/c1-census-v10.py:513-519
     # G20 (r9, H3): the old second disjunct was true exactly when the run found
     # nothing, so a blind instrument read PASS.  G2 is now a positive floor:
     # at least one current-ok locus in a non-empty scope.
     n_loci = sum((c["loci"] or 0) for c in counts.values())
     n_current_ok = len(out.get("current-ok", []))
-    g2_ok = n_current_ok > 0
-    declared = (["UNREADABLE"] if unreadable else []) + ([] if g2_ok else ["BLIND-INSTRUMENT"])
+    # per-file floor in the DET unit.  Two traps, both measured (below):
+    # blocks are mixed-disposition (SKILL.md has NO current-ok block), and
+    # `out` is keyed by block disposition -- so the det sweep must visit every
+    # disposition, skipping the string-valued g11/g7 keys.
+    cur_by_file = {f: 0 for f in files}
+    for _disp, _recs in out.items():
+        if _disp in ("g11", "g7"):
+            continue
+        for rec in _recs:
+            for d in rec["asserts"]:
+                if d["disp"] == "current-ok":
+                    cur_by_file[rec["file"]] += 1
+    empty_files = [f for f in files if filelines[f] is not None and cur_by_file[f] == 0]
+    blind, empty_scope = n_current_ok == 0, bool(empty_files)
+    g2_ok = not blind and not empty_scope
+    declared = (["UNREADABLE"] if unreadable else []) \
+        + (["BLIND-INSTRUMENT"] if blind else []) \
+        + (["EMPTY-SCOPE"] if empty_scope else [])
```

plus the report line carrying `cur_by_file` (so the floor's substrate is
auditable per file); the verified variant appends
`per-file dets=%r` to the existing G2 print.

### Trap 1 (self-inflicted, caught by measurement)

The first draft of this patch counted dets from `out["current-ok"]` alone. That
false-FAILs at HEAD — `per-file dets={'PROVINCE.md': 3, 'SCORECARD.md': 8,
'SKILL.md': 0}`, `['BLIND-INSTRUMENT', 'EMPTY-SCOPE']`, exit 1 — because the
`out` dict is keyed by **block** disposition and SKILL.md has no current-ok
block at all. The sweep must visit every disposition. Any reviewer/Critic
proposal of the same shape should be rejected on this measurement alone.

### Trap 2 (class hygiene)

Do not let one flag drive both labels: gating both classes on
`n_current_ok > 0 and not empty_files` mislabels the emptied-file case as
`BLIND-INSTRUMENT`. The verified variant computes `blind` and `empty_scope`
separately so the declared class names the right defect.

## Measured effect of this diff (scratch variant, end-to-end `main()`)

| environment | landed v11 | with this diff (verified variant) |
|-------------|------------|-----------------------------------|
| head | PASS exit 0 | **PASS exit 0**, per-file dets 17 / 14 / 3, classes `[]` |
| `atk-missing` (SKILL.md absent) | FAIL `UNREADABLE` | FAIL `UNREADABLE` (SKILL exempt from the floor as unreadable) |
| `atk-nullskill` (present, needle-free) | **PASS exit 0** | **FAIL exit 1**, class `['EMPTY-SCOPE']` |
| `atk-shrunk` | FAIL (stale) | FAIL (stale), classes `[]` — no false class |

Receipts: `pff-matrix.out`, `receipts-pff-*.out`.

Cost/benefit: it closes the present-but-emptied file class (the same class the
external locus-count audit otherwise has to cover by eye) at the price of a new
declared class (`EMPTY-SCOPE`) and one more per-file number in the report. If
the round prefers the tree-level floor, this patch is unnecessary — but then
`atk-nullskill` belongs in the named-residual list beside H4, because the
claim's "non-empty scope" wording is then tree-level by definition.
