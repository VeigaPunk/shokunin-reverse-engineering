# Proposed patch text (NOT applied) — G2 report line mislabels detections as loci

Seat RV-5 (reviewer, chain c2), 2026-10-19. **Patch text only.** The target
`.ufo/gates/c1-census-v10.py` is EX-16's write alone; this seat wrote nothing
outside `claims/c2/RV-5/**` and `seats/RV-5.md`.

Before-state: landed revision sha256
`a4c167631269e5110fbdcf323b6be2a779eaa1e0ca79c98201419261ba9c6bfb`
(behaviour-identical to `df9ffdf963ef…`; both count **dets**):

```
543-547  n_current_ok = sum(1 for recs in out.values() if isinstance(recs, list)
                            for rec in recs if isinstance(rec, dict)
                            for d in rec["asserts"] if d["disp"] == "current-ok")
555-556  for recs in out.values(): ... if d["disp"] == "current-ok": floor[rec["file"]] += 1
591      print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
```

The substrate counted is per-file **current-ok detections (dets)**, but the
printed label says **loci** (records/blocks). Measured at HEAD
(`receipts/label-defect.txt`, in-memory `classify`):

| file | loci | dets | current-ok loci | current-ok dets | printed |
|---|---:|---:|---:|---:|---|
| PROVINCE.md | 6 | 24 | 1 | 17 | `PROVINCE.md=17` |
| SCORECARD.md | 9 | 21 | 4 | 14 | `SCORECARD.md=14` |
| SKILL.md | 2 | 5 | **0** | 3 | `SKILL.md=3` |

So the line prints `SKILL.md=3` while SKILL.md has 0 current-ok loci — the same
label-vs-substrate defect class the court recorded for the custody receipt's
`MTIME_UTC` label in round 1 (a correct number under a wrong name). It also
hides why the interim block-count floor of `076bd621`/`c95a5cf3` false-failed
the ordinary run: in the *locus* unit SKILL.md is 0, in the *det* unit it is 3.

## Diff

```diff
@@ def main():
-    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
-          % ("ok" if g2_ok else "SUSPECT",
-             ", ".join("%s=%d" % (f, floor[f]) for f in files), n_loci))
+    print("G2 positive-assertion guard: %s (current-ok detections per file: %s; "
+          "current-ok loci total=%d; total loci=%d; floor=1 detection/file)"
+          % ("ok" if g2_ok else "SUSPECT",
+             ", ".join("%s=%d" % (f, floor[f]) for f in files),
+             len(out.get("current-ok", [])), n_loci))
```

Optional, same edit: the JSON key `current_ok_per_file` (already neutral) and
the `g2_floor: "1/readable-file"` value are accurate as landed — no change.
Optional second line for the header's r9 block, replacing "the G2 report line
carries the per-file substrate so the number is auditable" with "... carries
the per-file **detection** counts (not loci) ...". Both are wording-only: no
scope row, no needle, no verdict changes (the diff is print-statement text).

Verification of this patch (if applied): `python3 .ufo/gates/c1-census-v10.py
--quiet` at HEAD must still read `PASS 0/0/0/0` exit 0, with the new label
showing `PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3` and `current-ok loci
total=5`.
