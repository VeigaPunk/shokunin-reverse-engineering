# H1 re-anchored + complete patch text (post-G18 HEAD) — NOT APPLIED

Seat EX-12 (c2, executor), arc3-loop1-round2, 2026-10-19. Patch TEXT only; the c2
real-path writer is EX-16, and EX-16's in-flight revision `82fb807e…` (560 lines,
measured 12:07Z) already implements everything below. This file exists for the
record, for a revert-reapply, and as the mechanically-applicable form of
`RV-11/proposed-missing-file-guard.patch.md`.

## Why the original fenced diff must not be copied verbatim (measured)

- Verbatim extraction of the md's two fenced blocks, GNU `patch --fuzz=0`: hunk 1
  lands at 438 (offset +57), **hunk 2 FAILED** → exit 1 (reproduced on post-G18
  HEAD *and* on the pre-G18 revision it was drafted against, `36e96cd5…`).
- `git apply --check` (no fuzz by design): `patch does not apply`, exit 1.
- Default fuzz: both hunks land, hunk 2 "succeeded at 455 with fuzz 1" — content
  then verified correct against a hand-built control (both sha256 `2586b014…`).
- Isolation: the same edit expressed as a bare `-`/`+` hunk applies at fuzz=0;
  a hand-built hunk that carries the backslash-terminated line
  (`… and (not scope_errors) \`) as context is rejected at fuzz=0 even though
  that line is byte-equal to the file's line. The character itself is not the
  trigger — a `diff -u`-generated hunk containing the same context line applies
  at fuzz=0. Practical rule: generate hunks with `diff`, or keep them bare.

## Verified diff (apply with `patch -p0 --fuzz=0`)

Basis: `.ufo/gates/c1-census-v10.py` sha256
`6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490 lines
(post-G18 HEAD). Copy it to `census-head-6f1d19ff.py`, apply the diff block
below with `patch -p0 --fuzz=0`; the result is 494 lines and must hash
`c1d280a905cf0d19ea3e616e9319fb35fae18dbaea11d957db132b24f808885f`. Self-check
run on this very file's diff block (extracted mechanically from between the
fences), 2026-10-19T12:12Z:

```
$ patch -p0 --fuzz=0 census-h1-ex12.py < artifact-selfcheck.patch
patching file census-h1-ex12.py                     # exit 0, zero rejects
$ sha256sum census-h1-ex12.py
c1d280a905cf0d19ea3e616e9319fb35fae18dbaea11d957db132b24f808885f  census-h1-ex12.py
$ python3 census-h1-ex12.py --root fixtures/absent-skill --quiet ; echo $?
UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
1
$ python3 …/scope-diff.py census-head-6f1d19ff.py census-h1-ex12.py | tail -1
CREEP FLAGS: []
```

The diff carries the two original hunks plus the four required adjustments of
`h1-analysis.md` §4.

```diff
--- census-head-6f1d19ff.py	2026-10-19 09:01:46.325761598 -0300
+++ census-h1-ex12.py	2026-10-19 09:09:38.333359246 -0300
@@ -118,7 +118,8 @@
                                            naming :40; now a SCOPE-ERROR)
 
 Verdict: PASS iff stale == 0 AND ambiguous == 0 AND undeclared == 0
-AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds.
+AND unresolved == 0 AND scope_errors == 0 AND g11 == [] AND G2 holds
+AND no scoped file is unevaluable (unreadable).
 Exit 0 PASS, 1 FAIL, 2 anchor failure.
 Usage: python3 c1-census-v9.py [--root DIR] [--json] [--quiet]
 """
@@ -435,11 +436,12 @@
     if not all(live.values()):
         print("ANCHOR-FAIL: %r" % live)
         return 2
-    out, counts, filelines = {}, {}, {}
+    out, counts, filelines, unreadable = {}, {}, {}, []
     for f in files:
         try:
             lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
-        except OSError:
+        except OSError as ex:
+            unreadable.append("%s: %s" % (f, type(ex).__name__))
             counts[f] = {"lines": 0, "loci": 0}
             filelines[f] = None
             continue
@@ -452,19 +454,20 @@
     g11, g7 = out.get("g11", []), out.get("g7", [])
     g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)
     ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
-         and (not g11) and g2_ok
+         and (not g11) and g2_ok and (not unreadable)
     verdict = "PASS" if ok else "FAIL"
     if args.json:
         print(json.dumps({"live": live, "counts": counts, "verdict": verdict,
                           "stale": stale, "ambiguous": unatt, "undeclared": undecl,
                           "unresolved": unres, "scope_errors": scope_errors,
+                          "unreadable": unreadable,
                           "g11": g11, "g7": g7, "g2_ok": g2_ok,
                           "historical": out.get("historical", []),
                           "current_ok": out.get("current-ok", [])}, indent=1))
         return 0 if verdict == "PASS" else 1
     print("live anchors (re-derived): %r" % live)
     for f, c in counts.items():
-        print("%-14s lines=%-4d loci=%s" % (f, c["lines"], c["loci"]))
+        print("%-14s lines=%-4s loci=%s" % (f, c["lines"], c["loci"]))
     if not args.quiet:
         for k in ("STALE", "AMBIGUOUS", "UNDECLARED", "UNRESOLVED",
                   "historical", "current-ok", "info"):
@@ -478,6 +481,7 @@
                     print("      :%d [%s] %s=%s -> %s (%s)" %
                           (d["line"], d["kind"], d["client"], d["value"], d["disp"], d["why"]))
     print("\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
+    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
     print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))
     print("G7 configured!=held warnings: %r" % g7)
     print("G11 current-ok without receipt language: %r" % g11)
```

What each hunk is for: hunk 1 = the docstring verdict definition (adjustment 4,
without it the instrument's self-description contradicts its behaviour); hunk 2 =
H1's read loop; hunk 3 = H1's verdict term plus adjustment 2 (`--json` class);
hunk 4 = adjustment 3 (`%-4s`, so a `None` line count cannot raise
`TypeError: %d format` — that crash is measured on the in-flight revision
`65442158…` at `c1-census-v10.py:533`) and adjustment 1 (the UNREADABLE text
line the original md mandated only in prose). Not included here, deliberately:
the pre-existing self-reference drift `:47` "instrument v9" / `:123`
`Usage: python3 c1-census-v9.py` inside a file named `c1-census-v10.py` — a
rename or a v11 copy must re-derive those.

## Landing checklist (the half-application hazard is measured, not hypothetical)

`patch` applies hunk 1 and leaves hunk 2 in `.rej`; the resulting file parses,
runs, and still reads the absent-file case as `PASS exit 0` — the guard is inert
because nothing consults `unreadable`. So:

1. apply at fuzz=0 and require zero rejects (or hand-edit and require the
   resulting sha to match the control);
2. run the absent-file fixture and require `VERDICT: FAIL` + the UNREADABLE line
   + exit 1 — never "the variable exists" and never "exit != 0" alone;
3. run the ordinary tree and require `PASS 0/0/0/0`;
4. run `scope-diff.py` against the pre-edit file and require 0 creep flags
   (measured 0 for this diff);
5. re-derive the landed file's sha256 after the last revision into the landing
   receipt, not into the file it hashes (queue-drain rule #14).

## Residual not closed by H1 (named, measured)

A scoped file padded with content-free lines to ≥ its declared max end (fixture:
SKILL.md = 371 blank lines) yields `lines=371 loci=0`, no UNREADABLE, no
declared class, `VERDICT: PASS` exit 0 — on HEAD and on `82fb807e…` (both
measured). H1 closes *unreadable*, H3 closes *whole-tree blindness*; a per-file
erasure above the declared max end is seen by neither. It was not a round-1
injection, so the frozen C2 claim stands; it is a candidate for the next
instrument touch (per-file floor over declared rows, or a declared-max-end-scaled
content check).
