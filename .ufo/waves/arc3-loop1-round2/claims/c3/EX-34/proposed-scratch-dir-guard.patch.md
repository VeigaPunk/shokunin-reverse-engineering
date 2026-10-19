# proposed patch — `selftest --scratch <dir>` guard (seat EX-34, chain c3)

Target: `.ufo/gates/custody-pair/custody-pair.py` · revision under test:
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (EX-31 owns
the write; this seat proposes text only).

Evidence: `robustness-scratch-missingdir.traceback.txt` (this dir). Measured
2026-10-19: `python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch
/var/tmp/ex34/scratch-missing` exits **1** with a raw `FileNotFoundError`
traceback from `tempfile.mkdtemp` (`custody-pair.py:630`), instead of the
declared `EXIT_USAGE = 2` class for bad arguments (`custody-pair.py:124`).
Control: the same command with an existing scratch dir exits 0,
`CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0`.

Two acceptable repairs (either closes the gap; the first keeps the exit-code
contract, the second is a one-liner):

## Option A — fail closed with the declared USAGE code (preferred)

```diff
 def cmd_selftest(args) -> int:
     import tempfile
 
     base = Path(args.scratch).expanduser() if args.scratch else default_scratch()
     if str(base).startswith("/tmp") and not args.scratch:
         print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
         return EXIT_USAGE
+    if not base.is_dir():
+        print("USAGE: scratch base is not a directory: %s" % base, file=sys.stderr)
+        return EXIT_USAGE
     root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
```

## Option B — create the operator-supplied base

```diff
-    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
+    base.mkdir(parents=True, exist_ok=True)
+    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))
```

Note on Option B: it writes to an operator-named path, which for a gate that is
otherwise read-only deserves a moment's thought; Option A leaves the write
surface unchanged and makes the failure legible. Either way the tool never
touches a custody path (the selftest fixtures live under the scratch root).

Suggested selftest case to fence the repair (mirrors the existing
`unparsable-receipt-usage-exit` pattern):

```
run_case(cases, "selftest-missing-scratch-usage-exit",
         lambda: subprocess.run([sys.executable, __file__, "selftest", "--scratch",
                                 "<root>/does-not-exist"], capture_output=True)
                 .returncode == EXIT_USAGE)   # 2, not 1 / traceback
```

This seat has not applied any edit to the real target (seat discipline: only
EX-31 writes `.ufo/gates/custody-pair/`). Verdict for the parent: optional,
low-risk; the label claim (EX-34's task) is unaffected by the gap.
