# CR-2 patch text — H1 guard: label fidelity, operator remedy, and the H3-floor
# false-FAIL episode (measured). NOT applied by this seat; EX-16 owns the target.

Seat CR-2 (chain c2, critic) — arc3-loop1-round2, 2026-10-19.
Instrument under attack: `.ufo/gates/c1-census-v10.py`. Receipts:
`evidence/` (64 files, this directory).

## 0. Identity timeline (the target moved six times during this seat)

| time (-0300) | sha256 (short) | note |
|---|---|---|
| 09:01 | `6f1d19ff…` | committed HEAD revision (git blob, extracted via `git show HEAD:`) |
| 09:05 | `2a89793a…` | EX-16 mid-write |
| 09:06:50 | `82fb807e…` | H1+H3 landed, tree-level G2 floor — full matrix run against it |
| 09:10:50 | `09e270c2…` | per-file current-ok **block** floor introduced |
| 09:10:56 | `c95a5cf3…` | same semantics — the false-FAIL below was measured here |
| 09:11:50 | `df9ffdf9…` | floor switched to current-ok **assertions** — closes the false FAIL |

Every claim below is bound to a sha. C1 rule #14 consequence for the wave: any
seat that recorded the instrument's identity before 09:11 (`RV-8` records
`6f1d19ff…`) holds a superseded identity; the landing receipt must re-derive it.

## 1. The seat question — does the guard fire on a legitimate scoped-file rename?

Measured at `df9ffdf9` (`evidence/df9ffdf9__*.txt`):

| case (root) | result | reading |
|---|---|---|
| `rename-rekeyed-COHERENT` — SKILL.md moved to GUIDE.md **and** its two SCOPE rows re-keyed in the same edit | PASS exit 0 (`GUIDE.md=3` dets) | **no false fire** |
| `rename-norekey` — file moved, table not re-keyed | FAIL `['SKILL.md: FileNotFoundError']` | intended catch: the declared table points at nothing |
| `symlink-move` — file moved, an in-place symlink keeps the declared path readable | PASS exit 0 | a compatibility shim is not punished |
| `undeclared_move` — an *unscoped* file moved inside the root | PASS exit 0 | guard reach = the declared file set, nothing wider |

Verdict: **H1 does not false-fire on a legitimate rename.** A rename is only
punished when the SCOPE table is left stale, which is the failure the round
intends to surface. Corroboration: the round-1 `scope-diff.py` differ shows the
coherent re-key as REMOVED 2 / ADDED 2 rows with `CREEP FLAGS: []` and exit 1
(change, not creep), so the scope audit does not obstruct a rename either.

## 2. F6 (blocking, now closed) — the per-file G2 floor false-FAILed the ordinary run

At `c95a5cf3…` the ordinary run at the live repo root read **FAIL exit 1**
(`evidence/landed3__live-repo.txt`, `floorfix__live_c95a5cf3_.txt`):

```
G2 positive-assertion guard: SUSPECT (current-ok loci per file: PROVINCE.md=1, SCORECARD.md=4, SKILL.md=0; floor=1/file)
DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)     exit=1
```

Cause: the floor counted current-ok *block records*, and `SKILL.md`'s only
locus-bearing block carries block disposition `info` (its one locus at
`SKILL.md:12` is `scope=CURRENT disp=historical why=inline marker value=6.4.0`),
so `SKILL.md` scored 0 and the floor was unsatisfiable at HEAD — a *false fire
on a legitimate tree state*, the same failure class this seat was sent to hunt
for, one granularity up from renames. It contradicted the frozen C2 invariant
"ordinary runs at HEAD stay PASS 0/0/0/0".

Closed at `df9ffdf9…` by EX-16/EX-14 switching the floor to current-ok
*assertions* (the header comment names the same measurement). Independently
re-verified by this seat at `df9ffdf9`: live root PASS exit 0, and every closure
still holds — `absent-skill`, `empty-skill`, `trunc-skill` FAIL via UNREADABLE;
`skl-blank-400` (SKILL.md readable, 400 length-satisfying but locus-free lines)
FAIL via `BLIND-INSTRUMENT`; `blind-all` (needles neutered) FAIL via
`BLIND-INSTRUMENT`; `rename-rekeyed-COHERENT` PASS.

Alternative fix measured and **not needed** (kept for the record): a per-file
*locus* floor plus the tree-level current-ok floor (`/var/tmp/cr2/cr2-floorfix.py`;
live root PASS, all closures held). The landed assertion-count floor is
sufficient; no change proposed.

## 3. Still-open deltas at `df9ffdf9` (severity: operability/cosmetic)

F2 — **the class label over-claims on the rows-beyond-EOF subclass** (a
*readable* file reported under `UNREADABLE`):

```
UNREADABLE (could-not-evaluate): ['SCORECARD.md: 766 lines < declared max 855 (rows beyond EOF)']
```
(`evidence/landed_hist_hist-tree-679af5d.txt`.) The instrument's own G19 text
says "unreadable/undeclarable"; the printed class name does not. Same defect
family as the round-1 `MTIME_UTC` label defect (C3's measured origin).

F2b — **the G2 line's per-file figures are current-ok *assertions*, labelled
`loci`** (`:576-578` prints `floor[f]`, built from `d["disp"] == "current-ok"`,
under the text "current-ok loci per file"; `--json` mirrors it as
`current_ok_per_file`). Units and label disagree.

F3 — **no remedy in any message.** Both constructors name file + cause only
(`:506` `"%s: %s"`, `:512` `"%s: %d lines < declared max %d (rows beyond EOF)"`);
nothing says what to do. An operator reading `SKILL.md: FileNotFoundError` must
already know the action is "re-key the SCOPE rows (if it moved) or restore the
file (if deleted)" — the one thing the fail-closed guard makes urgent.

Proposed patch (Option 1, minimal; **apply by content**, line numbers are of
`df9ffdf9…`):

```diff
@@ :506 UNREADABLE message constructors — name the action
-            unreadable.append("%s: %s" % (f, type(ex).__name__))
+            unreadable.append("%s: %s -- restore/read the file, or re-key its "
+                              "SCOPE rows if it moved" % (f, type(ex).__name__))
@@ :512 rows-beyond-EOF constructor — name the action
             unreadable.append("%s: %d lines < declared max %d (rows beyond EOF)"
-                              % (f, len(lines), max_end))
+                              " -- re-key its SCOPE rows or restore the file"
+                              % (f, len(lines), max_end))
@@ :575 label — state both subclasses, keep the token
-    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
+    print("UNREADABLE (could-not-evaluate: unreadable-or-rows-beyond-EOF): %r" % unreadable)
@@ :576 G2 line — say what the numbers are
-    print("G2 positive-assertion guard: %s (current-ok loci per file: %s; total loci=%d; floor=1/file)"
+    print("G2 positive-assertion guard: %s (current-ok assertions per file: %s; total loci=%d; floor=1/file)"
@@ docstring label reference — keep text == output
-     class -- reported (`UNREADABLE (could-not-evaluate): [...]`
+     class -- reported (`UNREADABLE (could-not-evaluate: unreadable-or-rows-beyond-EOF): [...]`
```

The class token `UNREADABLE` stays unchanged in `declared_fail_classes` and
`--json`, so no verifier assertion breaks.

## 4. F5 — the round-1 H1 patch text's line anchors are stale (artifact defect)

`claims/c3/RV-11/proposed-missing-file-guard.patch.md:20,36` cites "current code
at `c1-census-v10.py:382-390`" and the verdict expression at ":397-398". At the
pristine instrument (`6f1d19ff…`) those lines are (receipt
`evidence/v10-pristine-anchors.txt`):

```
v10-pristine:382 |                     else:
v10-pristine:390 |                         disp, why = "STALE", "live %s=%s" % (c, live.get(c))
v10-pristine:397 |                             "scope": cls, "disp": disp, "marker": marker, "why": why})
v10-pristine:398 |         if not det:
v10-pristine:438 |     out, counts, filelines = {}, {}, {}
v10-pristine:442 |         except OSError:
v10-pristine:454 |     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
v10-pristine:455 |          and (not g11) and g2_ok
```

The real sites are `:438-445` and `:454-455`. EX-16 applied the patch by
content, so nothing was harmed — but the frozen debt text (`claims-frozen.md:39`)
points at an artifact whose anchors do not resolve at its own target. This is
the C1 rule-#14 class (an artifact's self-referential identity went stale) and
should be re-anchored or annotated in the round report.

## 5. F4 — historical trees: the rows-beyond-EOF rule adds a cause, not a verdict

Of the 7 round-1 replication trees, 6 now report
`SCORECARD.md: N lines < declared max 855 (rows beyond EOF)`
(`b21c0da` 701, `fd30b9c`/`679af5d` 766, `158a966`/`1692acb`/`265e1aa` 854;
`evidence/landed_hist_*.txt`). **No verdict flips**: those 6 were already FAIL
under v10, and `6bc4c29` (1158 lines) still PASSes. The H1 guard itself changes
nothing on historical roots (UNREADABLE `[]` for all 7 at `82fb807e…`).
Recommended landing-note sentence: "the rows-beyond-EOF class also fires on
pre-round-2 replication trees, where the declared bound exceeds the old file
length; it is a re-derivation artifact there, not a new defect."

## 6. Residuals (named, not closed here)

- G2 floor is per-file over current-ok assertions; per-needle *partial*
  blindness (e.g. PIN alone neutered) still reads PASS — H4 self-certification,
  already named in the landed header and `claims-frozen.md:48-50`.
- The guard cannot see *content* shrink above the declared max end (a scoped
  file can lose undeclared prose regions while `len(lines) >= max_end`). Out of
  H1's scope; no assertion proposed (that would be new scope surface).
- Sub-class token split (`UNREADABLE` vs `ROWS-BEYOND-EOF` in
  `declared_fail_classes`) is the machine-readable analogue of F2; deferred to
  the next instrument touch to avoid moving the token mid-wave.
