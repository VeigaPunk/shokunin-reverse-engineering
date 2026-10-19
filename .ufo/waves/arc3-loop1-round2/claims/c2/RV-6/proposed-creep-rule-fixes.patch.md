# Proposed patch text (NOT applied) — two creep-differ rule defects

Seat RV-6 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19. Patch TEXT
only: `.ufo/gates/` and round-1 wave trees are outside this seat's write scope.
Targets, both measured this round:

- (a) `.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py`
  (sha256 `e0d2384c1220c4e8e7faf1f98b74118489ab4985e56a10df77c9f40af5438504`,
  the copy EX-21 re-used at `claims/c2/EX-21/cr5-tool/scope-diff.py`) — the
  chain's creep-audit instrument of record.
- (b) EX-21's `claims/c2/EX-21/scope-audit.py` (round-2 auditor).

## Defect 1 — coverage-loss blindness (scope-diff.py)

Measured: a removed row with no replacement is not flagged.

```
$ python3 scope-diff.py before.py F11-pure-row-deletion-534-560.py
rows before=20 after=19
REMOVED (1): - SCORECARD.md 534-560 DATED …
CREEP FLAGS: []          # exit 1 only via the added/removed != 0 rule
```

Same for a *narrowed* bound (F12: `636-702` → `636-690`): `CREEP FLAGS: []`.
Round-2's own auditor (EX-21's) and RV-6's both flag this as
`CREEP row removed (coverage loss): …`.

Proposed addition after the widen-by-add/remove loop in `main()`:

```diff
+    for (f, s, e, cls, ml, mr) in removed:
+        if not any(a[0] == f and (a[2] - a[1]) == (e - s) for a in added):
+            flags.append("CREEP row removed (coverage loss): %s %d-%d %s"
+                         % (f, s, e, cls))
```

(same-width same-file replacement = legitimate renumber, r8 precedent; anything
else = coverage loss.)

## Defect 2 — dead widen branches (scope-diff.py)

`key(r) = (file, start, end)`, so `changed` only ever holds rows with an
*identical* key. In the `changed` loop,
`if a[2] > b[2] and a[3] == "DATED"` (end widened) and
`if a[1] < b[1] and a[3] == "DATED"` (start moved earlier) can never fire.
Measured: F1 (273-326 → 273-330) and F5 (45-62 → 44-62) both report
`CHANGED (0)`; the flag arrives from `widen-by-add/remove`. Harmless (widening
is still caught) but the two branches read as coverage that does not exist.

Proposed: delete both blocks, or keep them with a comment that widening is
detected via the add/remove path.

## Defect 3 — EOF-bound rule measured against the wrong file (scope-audit.py)

`compare()` sets `nlines = after["lines"]` (the line count of the *census
script*, 560), not of the row's scoped file, so
`if e == nlines: "CREEP bound reaches last line of file"` tests the wrong
object. Measured: an added row `SCORECARD.md 1268-1417` (150 lines, ending
exactly at SCORECARD.md's live EOF) yields `CREEP FLAGS: []` from both
scope-audit.py and scope-diff.py; RV-6's audit flags
`CREEP bound reaches file EOF: SCORECARD.md 1268-1417 DATED (lines=1417)`.

Proposed: resolve the scoped file's line count (the tool already receives a
root path in `invariance` mode; `compare` would need a `--root`), i.e.

```diff
-    nlines = after["lines"]
+    nlines = line_count(root, f)   # scoped file, not the script
```

Also in EX-21's `run-audit.sh`: the second-opinion leg is mis-pathed
(`"$HERE/../cr5-tool/scope-diff.py"`; the copy lives at `$HERE/cr5-tool/`), so
that leg writes `No such file or directory` + `exit=2` into its receipt while
the run continues. Measured in RV-6's re-run:
`claims/c2/RV-6/logs/ex21-runner/cr5-scope-diff.out`.

```diff
-  python3 "$HERE/../cr5-tool/scope-diff.py" "$BASE" "$LANDED" > "$OUT/cr5-scope-diff.out" 2>&1
+  python3 "$HERE/cr5-tool/scope-diff.py" "$BASE" "$LANDED" > "$OUT/cr5-scope-diff.out" 2>&1
```

None of the three defects has any bearing on the landed round-2 diff (which is
clean under all three instruments, plus RV-6's). They are recorded because the
instrument is the chain's certificate for future diffs.
