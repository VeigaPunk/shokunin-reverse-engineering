# Proposed patch text (NOT applied) — exit-code surface of the census instrument

Seat RV-10 (reviewer, chain c2), arc3-loop1-round2, 2026-10-19. Two findings from
the exit-code conformance matrix, both measured on the landed revision
`df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` (601 lines).
This is patch TEXT only: the real target is EX-16's sole write.

Declared map under test (`.ufo/gates/c1-census-v10.py:191-192`):
`Exit 0 PASS, 1 FAIL, 2 anchor failure.`

## R1 — a non-regular scoped file hangs the run (no exit code at all)

Measured: `mkfifo SKILL.md` in a scoped tree, then

```
$ timeout 5 python3 c1-census-v10.py --root <tree> --quiet   # blocks in open()
(no output; harness killed it)   exit=124 from timeout, no census exit code
```

`open()` on a FIFO blocks forever (no writer). A named pipe, socket or device
node left in a scoped path — all reachable by a failed write or a hostile
fixture — takes the instrument out of the 0/1/2 map entirely: a consumer that
waits for an exit code waits forever. Suggested form (mirrors the H1 class):

```diff
 import argparse, json, os, re, sys
+import stat
...
     for f in files:
         path = os.path.join(args.root, f)
+        try:
+            if not stat.S_ISREG(os.lstat(path).st_mode):
+                unreadable.append("%s: not a regular file" % f)
+                counts[f] = {"lines": None, "loci": None}
+                filelines[f] = None
+                continue
+        except OSError:
+            pass   # the open() below re-reports the real errno
         try:
             lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
```

Semantics: a non-regular scoped path joins the declared UNREADABLE class
(exit 1) instead of blocking. This is the only fixture shape found in the whole
matrix that leaves the map by *hanging* rather than by coding wrong.

## R2 — argparse usage errors exit 2, colliding with ANCHOR-FAIL

Measured: `python3 c1-census-v10.py --bogus` → exit 2, no stdout; while the
anchor-failure class prints `ANCHOR-FAIL: {...}` on stdout and returns 2
(`:504`). A consumer that reads only the code cannot tell a typo'd invocation
from an anchor failure. Minimum-cost fix is documentation inside the declared
map line; if a distinct code is wanted, override `argparse`'s exit:

```diff
     ap = argparse.ArgumentParser()
+    # usage errors are not anchor failures: keep them out of the map's 2.
+    ap.error = lambda message: (print("USAGE-ERROR: %s" % message), sys.exit(64))[1]
```

(the `64` is EX_USAGE from sysexits; any value outside 0/1/2 is acceptable as
long as it is declared). Reviewer's note: changing this is optional — the
collision is only hazardous for consumers that do not read stdout.

## What this patch is NOT touching

Scope bounds, needle regexes, dispositions and the G19/G20 fail-closure logic
are untouched by R1/R2 — both are exit-surface-only.
